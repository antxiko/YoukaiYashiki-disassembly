#!/usr/bin/env python3
"""Los cinco sucesos (los jefes) de Youkai Yashiki, PINTADOS EJECUTANDO LA ROM: sobre el cuadro grabado justo antes de
que salga cada uno (work/jefes.bin, tools/guiones/jefes.tcl: su pantalla, 0x852E, con el protagonista ya dentro), se
ejecuta `sala_suceso` (0x8252) con tools/bios.py: carga los dibujos del suceso (`dibujo_suceso` 0x84DF: 0x2C0 bytes de
0x8533 + 2 x lugar a las casillas 0x90 de los tres tercios, y sus colores) y su rutina pone el dibujo grande
(`dibujo_8x8`, 8 x 8 casillas de 0x7700, 0x7780, 0x7740 o 0x77C0) y los tipos de sus enemigos. La imagen es la zona de
juego (filas 2-21) sin sprites.

El cuadro de partida es el ultimo con 0xE1B1 a 0 (aun sin cargar nada) y la pantalla ya quieta (0xE198 = 0): la
grabacion toma la VRAM al entrar la interrupcion, que puede llegar a mitad de una copia (en el primer cuadro con
0xE1B1 = 1 faltaban colores del tercer tercio). En ese cuadro el protagonista puede ir aun por la X 0x27: en el mismo
paso del bucle `prota_mueve` lo pasa a 0x28 antes de `sala_suceso`, y asi se pone. Las filas 2-21 de la tabla de
nombres se toman de la pantalla de la RAM (0xE700), la que se ve al acabar de entrar: entrando por arriba, en ese
cuadro la fila 2 de la VRAM aun era la de la pantalla de antes.

Cotejo: la VRAM que deja la ejecucion (la tabla de nombres de las filas 2-21, las de arriba llevan los puntos; los
dibujos y los colores de las casillas) contra la grabada 5 cuadros despues de que el juego lo ponga (0xE1B0 pasa a
1), y los tipos de los cuatro primeros enemigos (0xE344, +16...) contra la RAM grabada.

Uso: jefes.py docs/imagenes
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import vdp                  # noqa: E402
from bios import Msx        # noqa: E402

RAIZ = os.path.dirname(AQUI)
ROM = open(os.path.join(RAIZ, "youkai.rom"), "rb").read()
PANTALLAS = [ROM[0x852E - 0x4000 + k] for k in range(5)]       # suceso_tabla: la pantalla de cada lugar


def cuadros_jefes():
    """Por lugar: (el ultimo cuadro con 0xE1B1 = 0, el quinto despues de que 0xE1B0 pase a 1)."""
    previo, salen, cuenta = {}, {}, {}
    for c in vdp.cuadros(os.path.join(RAIZ, "work", "jefes.bin")):
        r = c["ram"]
        lugar = r[0x00A]
        if not r[0x000] or lugar > 4 or r[0x0A3] != PANTALLAS[lugar] or lugar in salen:
            continue
        if r[0x1B0] >= 1 and lugar in previo:
            cuenta[lugar] = cuenta.get(lugar, 0) + 1
            if cuenta[lugar] == 5:
                salen[lugar] = (previo[lugar], c)
        elif r[0x1B1] == 0 and r[0x198] == 0:
            previo[lugar] = c
    return salen


def ejecuta(c):
    m = Msx(ROM, 0x4000)
    m.mem[0xE000:0xF000] = c["ram"]
    m.vdp.vram[:] = c["vram"]
    m.vdp.vram[0x1840:0x1AC0] = m.mem[0xE700:0xE980]     # la pantalla de la RAM, la que se ve al acabar de entrar
    m.ix = 0xE300
    if m.mem[0xE301] < 0x28:        # en ese mismo paso del bucle, prota_mueve lo lleva a 0x28 antes de sala_suceso
        m.mem[0xE301] = 0x28
    m.llama(0x8252)                 # sala_suceso
    return m


def main(salida):
    from PIL import Image
    iguales = 0
    for lugar, (antes, despues) in sorted(cuadros_jefes().items()):
        m = ejecuta(antes)
        v, g = bytes(m.vdp.vram), despues["vram"]
        zonas = {"nombres": (0x1840, 0x1AC0), "dibujos": (0x0000, 0x1800), "colores": (0x2000, 0x3800)}
        dif = {k: sum(1 for i in range(a, b) if v[i] != g[i]) for k, (a, b) in zonas.items()}
        tipos = [m.mem[0xE344 + 16 * k] for k in range(4)]
        tipos_g = [despues["ram"][0x344 + 16 * k] for k in range(4)]
        bien = not any(dif.values()) and tipos == tipos_g
        iguales += bien
        im = vdp.imagen(v, despues["regs"], 1, con_sprites=False).crop((0, 16, 256, 176))
        ruta = os.path.join(salida, "jefe_%d.png" % lugar)
        im.save(ruta, optimize=True)
        print("lugar %d, pantalla 0x%02X: %s; distintos %s; enemigos %s %s" % (
            lugar, PANTALLAS[lugar], ruta, dif, " ".join("%02X" % t for t in tipos if t),
            "IGUAL" if bien else "DISTINTO"))
    print("sucesos iguales a la grabacion: %d de 5" % iguales)


if __name__ == "__main__":
    main(sys.argv[1])
