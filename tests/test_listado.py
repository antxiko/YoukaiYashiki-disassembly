"""Lo que se afirma de la ROM, comprobado contra sus bytes.

Corre con la ROM delante y sin ella: cuando no esta, la imagen se rehace desde
las filas defb/defw del listado, que si viaja con el repositorio. Sin la ROM
solo se comprueba lo que cae en datos.
"""

import os
import re
import subprocess
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))

ROM = os.path.join(RAIZ, "youkai.rom")
ASM = os.path.join(RAIZ, "src", "youkai.asm")
NOTAS = os.path.join(RAIZ, "src", "youkai.notes")
ORG = 0x4000
TAM = 32768

FILA = re.compile(r"^\s+def(b|w)\s+([0-9a-fA-F,h ]+)\s*;\s*([0-9a-f]{4})")


def imagen_desde_el_listado():
    img = bytearray(TAM)
    with open(ASM, encoding="utf-8") as f:
        for ln in f:
            m = FILA.match(ln)
            if not m:
                continue
            ancho, cuerpo, dirr = m.group(1), m.group(2), int(m.group(3), 16)
            p = dirr - ORG
            for tok in cuerpo.split(","):
                tok = tok.strip().rstrip("h")
                if not tok:
                    continue
                v = int(tok, 16)
                if ancho == "b":
                    img[p] = v
                    p += 1
                else:
                    img[p] = v & 0xFF
                    img[p + 1] = v >> 8
                    p += 2
    return bytes(img)


def lee():
    if os.path.exists(ROM):
        with open(ROM, "rb") as f:
            return f.read()
    return imagen_desde_el_listado()


def b(a):
    return lee()[a - ORG]


def w(a):
    rom = lee()
    return rom[a - ORG] | (rom[a - ORG + 1] << 8)


def instruccion(dirr):
    """La instruccion del listado en esa direccion (sin el comentario)."""
    with open(ASM, encoding="utf-8") as f:
        for ln in f:
            m = re.match(r"^	(\S.*?)\s*;([0-9a-f]{4})", ln)
            if m and int(m.group(2), 16) == dirr:
                return m.group(1).replace("	", " ").strip()


def texto(a, n):
    """Casilla = letra - 0x30 (el orden de la fuente de la BIOS); 0x10 es el espacio."""
    return "".join(" " if c == 0x10 else chr(c + 0x30) for c in lee()[a - ORG:a - ORG + n])




KANA1 = "をぁぃぅぇぉゃゅょっ・あいうえおかきくけこさしすせそ"
KANA2 = "たちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわん"


def kana(a, n):
    """Las casillas 0x86-0x9F y 0xE0-0xFD son las letras de la BIOS con su mismo numero (final_letras)."""
    out = ""
    for c in lee()[a - ORG:a - ORG + n]:
        if 0x86 <= c <= 0x9F:
            out += KANA1[c - 0x86]
        elif 0xE0 <= c <= 0xFD:
            out += KANA2[c - 0xE0]
        elif c == 0xBE:
            out += "゛"
        elif c == 0x10:
            out += " "
        else:
            out += chr(c + 0x30)
    return out


class Cabecera(unittest.TestCase):
    def test_ab_e_init_en_0x4010(self):
        rom = lee()
        self.assertEqual(rom[:2], b"AB")
        self.assertEqual(w(0x4002), 0x4010)

    def test_son_32_kb(self):
        self.assertEqual(len(lee()), TAM)

    def test_el_arranque_esta_en_la_pagina_1(self):
        self.assertEqual(instruccion(0x8000), "jp arranque")


class LaInterrupcion(unittest.TestCase):
    def test_va_por_h_timi(self):
        self.assertEqual([instruccion(a) for a in (0x7E91, 0x7E94, 0x7E99)],
                         ["ld hl,0b475h", "ld (0fda0h),hl", "ld (0fd9fh),a"])


class LosTextos(unittest.TestCase):
    def test_el_titulo(self):
        self.assertEqual(texto(0x56DB, 20), "PUSH TRIG:1 OR SPACE")
        self.assertEqual(texto(0x5714, 9), "GAME OVER")
        self.assertEqual(texto(0x5705, 7), "HISCORE")

    def test_continuar(self):
        self.assertEqual(texto(0xAF4D, 19), "CONTINUE PUSH TRIG1")


class LaPartida(unittest.TestCase):
    def test_las_teclas_del_titulo(self):
        self.assertEqual([instruccion(a) for a in (0x7F01, 0x7F06, 0x7F14)],
                         ["ld a,001h", "cp 0e0h", "ld (0e023h),a"])

    def test_con_ellas_la_vida_llena(self):
        self.assertEqual([instruccion(a) for a in (0x7FE2, 0x7FE4)], ["ld a,006h", "ld (0e0a9h),a"])

    def test_74_pantallas(self):
        ptr = [w(0x41AC + 2 * k) for k in range(74)]
        self.assertTrue(all(0x4240 <= p < 0x4EBE for p in ptr))
        self.assertLess(w(0x41AC + 2 * 74), 0x4000)

    def test_la_demostracion_lee_la_bios(self):
        self.assertEqual([instruccion(a) for a in (0x7F97, 0x7F9A)], ["ld hl,00000h", "ld (0e029h),hl"])


class Tablas(unittest.TestCase):
    def test_objetos_y_enemigos(self):
        self.assertEqual(w(0x947B), 0x94A3)
        self.assertEqual(w(0xA1E8), 0xA278)


class Sonido(unittest.TestCase):
    def test_ocho_musicas(self):
        for k in range(1, 8):
            for j in range(3):
                self.assertTrue(0xBB36 <= w(0xB700 + 6 * k + 2 * j) < 0xC000)


class ElListado(unittest.TestCase):
    def test_densidad_y_flojas(self):
        salida = subprocess.run(
            [sys.executable, os.path.join(RAIZ, "tools", "densidad.py"), ASM],
            capture_output=True, text=True, check=True).stdout
        m = re.search(r"(\d+) instrucciones, (\d+) comentarios", salida)
        self.assertGreaterEqual(int(m.group(2)) * 100, 40 * int(m.group(1)))
        self.assertIn("---- 0 rutinas por debajo del 10 %", salida)

    def test_ningun_call_sin_nombre(self):
        salida = subprocess.run(
            [sys.executable, os.path.join(RAIZ, "tools", "sin_bautizar.py"), ASM],
            capture_output=True, text=True, check=True).stdout
        self.assertTrue(salida.startswith("0 rutinas sin bautizar"), salida[:200])

    def test_cada_comentario_en_su_instruccion(self):
        salida = subprocess.run(
            [sys.executable, os.path.join(RAIZ, "tools", "valida_c.py"), ASM, NOTAS],
            capture_output=True, text=True, check=True).stdout
        self.assertIn("0 fuera de sitio, 0 repetidos", salida)


if __name__ == "__main__":
    unittest.main()
