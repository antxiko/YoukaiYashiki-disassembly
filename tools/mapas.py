"""Los planos de los seis lugares de Youkai Yashiki, PINTADOS EJECUTANDO LA ROM: cada pantalla en su sitio del plano
de su lugar (0x4038: filas de diez, el numero de la pantalla en cada sitio), montada por pantalla_monta (0x9257) en la
RAM (0xE700, 32 x 20 casillas, las filas 2-21 de la pantalla) sobre la RAM y la VRAM de un cuadro grabado del lugar
(work/forzada.bin). Las casillas son las mismas en todos los lugares; solo cambia el color de las 0x41-0x47
(sala_colores, 0x8206). El sexto lugar (el 5, al que llevan las puertas 28-32 de 0xA0D7) no esta en la grabacion: se
pinta sobre un cuadro del lugar 4 con sala_colores ejecutada para el 5 (el mismo color, 0x30).

Cotejo: cada pantalla montada contra la tabla de nombres grabada (work/forzada.bin, trucos.bin y partida.bin) en los
ultimos cuadros con ella (0xE0A3) en el lugar (0xE00A): el mejor de ellos.

Uso: mapas.py docs/imagenes
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import vdp                  # noqa: E402
from bios import Msx        # noqa: E402
from PIL import Image       # noqa: E402

RAIZ = os.path.dirname(AQUI)
ROM = open(os.path.join(RAIZ, "youkai.rom"), "rb").read()
NOMBRES = 32 * 20


def w(a):
    return ROM[a - 0x4000] | ROM[a - 0x3FFF] << 8


def plano(lugar):
    p, fin = w(0x4038 + 2 * lugar), (w(0x4038 + 2 * lugar + 2) if lugar < 5 else 0x41AC)
    b = ROM[p - 0x4000:fin - 0x4000]
    return [list(b[k:k + 10]) for k in range(0, len(b), 10)]


def monta(c, lugar, pantalla):
    m = Msx(ROM, 0x4000)
    m.mem[0xE000:0xF000] = c["ram"]
    m.vdp.vram[:] = c["vram"]
    if lugar != c["ram"][0x00A]:
        m.mem[0xE00A] = lugar
        m.llama(0x8206)                 # sala_colores
    m.mem[0xE0A3] = pantalla
    m.llama(0x9257)
    return bytes(m.mem[0xE700:0xE700 + NOMBRES]), bytes(m.vdp.vram)


def main(salida):
    cuadro = {}
    grabadas = {}
    for grab in ("forzada", "trucos", "partida"):
      for c in vdp.cuadros(os.path.join(RAIZ, "work", grab + ".bin")):
        r = c["ram"]
        if not (r[0x000] and c["regs"][1] & 0x40) or r[0x00A] > 5:
            continue
        if grab == "forzada":
            cuadro[r[0x00A]] = c
        g = grabadas.setdefault((r[0x00A], r[0x0A3]), [])
        g.append(c["vram"][0x1840:0x1840 + NOMBRES])
        del g[:-40]
    cuadro.setdefault(5, cuadro[4])
    total = [0, 0, 0]
    for lugar in range(6):
        c = cuadro[lugar]
        pl = plano(lugar)
        usadas = [(f, k) for f, fila in enumerate(pl) for k, n in enumerate(fila) if n]
        f0, f1 = min(f for f, _ in usadas), max(f for f, _ in usadas)
        k0, k1 = min(k for _, k in usadas), max(k for _, k in usadas)
        hoja = Image.new("RGB", ((k1 - k0 + 1) * 256, (f1 - f0 + 1) * 160), (0, 0, 0))
        notas = []
        for f, k in usadas:
            n = pl[f][k]
            nombres, vram = monta(c, lugar, n)
            v = bytearray(vram)
            v[0x1840:0x1840 + NOMBRES] = nombres
            im = vdp.imagen(bytes(v), c["regs"], 1, con_sprites=False).crop((0, 16, 256, 176))
            hoja.paste(im, ((k - k0) * 256, (f - f0) * 160))
            g = grabadas.get((lugar, n))
            if g:
                d = min(sum(1 for a, b in zip(nombres, x) if a != b) for x in g)
                total[0] += 1
                total[1] += d == 0
                notas.append("%02X:%d" % (n, d))
            else:
                total[2] += 1
        hoja = hoja.resize((hoja.size[0] // 2, hoja.size[1] // 2), Image.NEAREST)
        ruta = os.path.join(salida, "plano_%d.png" % lugar)
        hoja.save(ruta, optimize=True)
        print("lugar %d: %d pantallas, %s; cotejo: %s" % (lugar, len(usadas), ruta, " ".join(notas) or "-"))
    print("pantallas cotejadas %d (iguales %d), sin grabar %d" % tuple(total))


if __name__ == "__main__":
    main(sys.argv[1])
