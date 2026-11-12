#!/usr/bin/env python3
"""Los sprites de Youkai Yashiki MONTADOS DESDE LA ROM (ninguna imagen es una captura).

Los dibujos son los 0x800 bytes de 0x5800 que `sprites_dibujos` (0xB36D) pone tal cual en 0x3800; sprites de 16 x 16.
Cada cosa son sprites de 16 bytes desde 0xE300 (los 4 primeros, sus atributos): el protagonista en 0xE300 y 0xE310,
el arma en 0xE320 y los doce enemigos desde 0xE340 (+4 el tipo, por la tabla 0xA1E8).

  protagonista.png   dos sprites en el mismo sitio: el dibujo en magenta y el dibujo + 0x60 en amarillo claro (`sala_empieza`
                     0x806D, `caida_para` 0x87A3): de pie 0x0C y 0x14 (0x880D, por su lado), andando 0x08-0x1C; y el
                     arma (0xE320, `ataque_sale`): 0x28 o 0x2C segun el lado
  enemigos.png       los dibujos y colores que las rutinas de los enemigos (0xA216-0xAD85) ponen en su sprite, cada uno
                     con el siguiente (+ 4) cuando lo cambian; y los dos que se ven al vencer una sala (`suceso_vencido`:
                     0xAC y 0xB0)
  andar_cuadros.gif  el protagonista andando a los dos lados y los enemigos con sus dos dibujos
  dibujos.png        LOS 64 DIBUJOS de la tabla, en orden y en blanco, con su numero: todos los usa algun codigo
                     (USOS) menos 0x90, enmarcado en rojo; 0xE4 esta vacio

Uso: hojas.py docs/imagenes | hojas.py cotejo
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))
import vdp          # noqa: E402

ORG = 0x4000
ROM = open(os.path.join(RAIZ, "youkai.rom"), "rb").read()
FONDO = (64, 64, 80)
POSES = [0x0C, 0x08, 0x10, 0x14, 0x18, 0x1C]
# (dibujos, color, donde lo pone el codigo)
ENEMIGOS = [((0x38, 0x3C), 15, 0xA216), ((0x30, 0x34), 7, 0xAAE8), ((0x4C, 0x50), 5, 0xA451), ((0x4C, 0x50), 9, 0xA457),
            ((0x88, 0x9C), 6, 0xA4E3), ((0xF8,), 9, 0xA7A3), ((0xAC,), 5, 0xAB20), ((0xE4,), 11, 0xABE9),
            ((0x40,), 9, 0xABF9), ((0xB8,), 4, 0xAC18), ((0xA8,), 9, 0xAC90), ((0x40,), 1, 0xAD81),
            ((0xD4, 0xD8, 0xDC, 0xE0), 15, 0xA884), ((0x94, 0x98), 9, 0xA60A), ((0x44, 0x48), 4, 0xA770),
            ((0xE8, 0xF0), 9, 0xA7AB), ((0xA4,), 9, 0xA91B)]

# Quien pone cada dibujo (los 64 de la tabla); la web los lista todos (tests/test_web.py lo comprueba)
USOS = {
    0x00: 0x8A04, 0x04: 0x8A04, 0x60: 0x8A09, 0x64: 0x8A09,
    0x08: 0x8EF3, 0x0C: 0x880D, 0x10: 0x8A9F, 0x14: 0x8819, 0x18: 0x8C2F, 0x1C: 0x8EFC,
    0x68: 0x8EF7, 0x6C: 0x8811, 0x70: 0x8AA7, 0x74: 0x881D, 0x78: 0x8C37, 0x7C: 0x8F00,
    0x20: 0xAE50, 0x80: 0xAE54, 0x5C: 0xAE5A, 0xBC: 0xAE5E, 0x24: 0x8BFC, 0x84: 0x8C00,
    0x28: 0x860B, 0x2C: 0x8615, 0x30: 0xA32A, 0x34: 0xA32A, 0x38: 0xA222, 0x3C: 0xA222,
    0x40: 0xABF9, 0x44: 0xA76D, 0x48: 0xA76D, 0x4C: 0xA45B, 0x50: 0xA4BC, 0x54: 0xA601, 0x58: 0xA68C,
    0x88: 0xA4E3, 0x8C: 0xA4E7, 0x9C: 0xA593, 0xA0: 0xA597, 0x94: 0xA606, 0x98: 0xA68C,
    0xA4: 0xA917, 0xA8: 0xAC90, 0xAC: 0xAB20, 0xB0: 0xAB24, 0xB4: 0x831F, 0xB8: 0xAC18,
    0xC0: 0x816F, 0xC4: 0x8173, 0xC8: 0x816B, 0xCC: 0x80E9, 0xD0: 0x8167,
    0xD4: 0xA9F7, 0xD8: 0xA9F7, 0xDC: 0xA9F7, 0xE0: 0xA9F7, 0xE4: 0xABE9,
    0xE8: 0xA7D0, 0xEC: 0xA7D5, 0xF0: 0xA7D0, 0xF4: 0xA7D5, 0xF8: 0xA7A3, 0xFC: 0xA7A7,
}
SIN_USO = [0x90]


def patrones():
    return ROM[0x5800 - ORG:0x5800 - ORG + 0x800]


def pinta(im, pat, n, x, y, color, escala=1):
    if color & 15 == 0:
        return
    n &= 0xFC
    d = pat[n * 8:n * 8 + 32]
    c = vdp.PALETA[color & 15]
    for fila in range(16):
        for col in range(16):
            if (d[fila + (16 if col >= 8 else 0)] >> (7 - (col & 7))) & 1:
                for ey in range(escala):
                    for ex in range(escala):
                        px, py = (x + col) * escala + ex, (y + fila) * escala + ey
                        if 0 <= px < im.width and 0 <= py < im.height:
                            im.putpixel((px, py), c)


def prota(im, pat, d, x, y, E):
    pinta(im, pat, d + 0x60, x, y, 11, E)
    pinta(im, pat, d, x, y, 13, E)


def hoja(Image):
    pat, E = patrones(), 4
    im = Image.new("RGB", (8 * 20 * E, 20 * E), FONDO)
    for k, d in enumerate(POSES):
        prota(im, pat, d, 2 + 20 * k, 2, E)
    for k, d in enumerate((0x28, 0x2C)):
        pinta(im, pat, d, 2 + 20 * (6 + k), 2, 11, E)
    return im


def hoja_enemigos(Image):
    pat, E = patrones(), 3
    filas = (len(ENEMIGOS) + 1 + 4) // 5
    im = Image.new("RGB", (5 * 60 * E, filas * 20 * E + 4 * E), FONDO)
    k = 0
    for ds, c, _ in ENEMIGOS:
        x, y = 2 + 60 * (k % 5), 2 + 20 * (k // 5)
        for j, d in enumerate(ds[:3]):
            pinta(im, pat, d, x + 18 * j, y, c, E)
        k += 1
    pinta(im, pat, 0xAC, 2 + 60 * (k % 5), 2 + 20 * (k // 5), 15, E)
    pinta(im, pat, 0xB0, 20 + 60 * (k % 5), 2 + 20 * (k // 5), 5, E)
    return im


def hoja_todos(Image):
    from PIL import ImageDraw
    pat, E = patrones(), 3
    im = Image.new("RGB", (16 * 24 * E, 4 * 30 * E), FONDO)
    d = ImageDraw.Draw(im)
    for n in range(0, 256, 4):
        x, y = 4 + 24 * ((n // 4) % 16), 2 + 30 * (n // 64)
        if n in SIN_USO:
            d.rectangle(((x - 2) * E, (y - 2) * E, (x + 18) * E - 1, (y + 18) * E - 1), outline=(255, 64, 64), width=E)
        pinta(im, pat, n, x, y, 15, E)
        d.text((x * E + 8, (y + 19) * E), "%02X" % n, fill=(255, 255, 0))
    return im


def anima(Image):
    pat, E, cuadros = patrones(), 4, []
    for n in range(48):
        im = Image.new("RGB", (5 * 20 * E, 20 * E), FONDO)
        prota(im, pat, 0x08 + (n // 8 % 3) * 4 if n < 24 else 0x10 + (n // 8 % 3) * 4, 2, 2, E)
        for k, (ds, c, _) in enumerate((ENEMIGOS[0], ENEMIGOS[2], ENEMIGOS[4])):
            pinta(im, pat, ds[(n // 8) % len(ds)], 22 + 20 * k, 2, c, E)
        cuadros.append(im)
    return cuadros


def guarda_gif(cuadros, ruta, ms=1000 / 60):
    imgs, durs = [], []
    for im in cuadros:
        if imgs and list(im.getdata()) == list(imgs[-1].getdata()):
            durs[-1] += ms
        else:
            imgs.append(im)
            durs.append(ms)
    imgs[0].save(ruta, save_all=True, append_images=imgs[1:], duration=[max(20, int(round(d))) for d in durs],
                 loop=0, disposal=1)


def cotejo():
    """Contra las grabaciones de openMSX (work/*.bin, la RAM 0xE000-0xEFFF):
    1) la tabla de dibujos de los sprites (VRAM 0x3800-0x3FFF) contra los 0x800 bytes de 0x5800;
    2) el protagonista (0xE300 y 0xE310): en el mismo sitio, el dibujo y el + 0x60 en amarillo claro;
    3) el arma (0xE320): 0x28 o 0x2C;
    4) los enemigos (0xE340, 16 bytes): un dibujo (o el + 4) y un color de los que pone su codigo."""
    pat = patrones()
    dibujos = set()
    colores = set()
    for ds, c, _ in ENEMIGOS:
        dibujos.update(ds)
        dibujos.update(d + 4 for d in ds)
        colores.add(c)
    tot = dict(patrones=0, pat_carga=0, pat_mal=0, prota=0, prota_sin_poner=0, prota_mal=0, arma=0, arma_mal=0,
               enemigos=0, enemigos_mal=0)
    for grab in ("atraccion", "partida", "forzada", "trucos"):
        ruta = os.path.join(RAIZ, "work", grab + ".bin")
        if not os.path.exists(ruta):
            continue
        try:
            cuadros = list(vdp.cuadros(ruta))
        except AssertionError:
            continue
        for c in cuadros:
            v, ram = c["vram"], c["ram"]
            t = v[0x3800:0x4000]
            if any(t):
                n = len(t.rstrip(bytes(1)))
                if t == pat:
                    tot["patrones"] += 1
                elif t[:n] == pat[:n]:
                    tot["pat_carga"] += 1
                else:
                    tot["pat_mal"] += 1
            a, b = ram[0x300:0x304], ram[0x310:0x314]
            if a[0] < 0xC0:
                if a == bytes(4):
                    tot["prota_sin_poner"] += 1
                elif a[:2] == b[:2] and b[2] == (a[2] + 0x60) & 0xFF and b[3] & 15 == 11:
                    tot["prota"] += 1
                else:
                    tot["prota_mal"] += 1
            w = ram[0x320:0x324]
            if w[0] < 0xC0 and w[2]:
                ok = w[2] in (0x28, 0x2C)
                tot["arma"] += ok
                tot["arma_mal"] += not ok
            for k in range(12):
                e = ram[0x340 + 16 * k:0x350 + 16 * k]
                if e[0] >= 0xC0 or e[4] == 0 or e[3] & 15 == 0:
                    continue
                ok = e[2] in dibujos and e[3] & 15 in colores
                tot["enemigos"] += ok
                tot["enemigos_mal"] += not ok
    return tot


def main(argv):
    if argv and argv[0] == "cotejo":
        print(cotejo())
        return 0
    from PIL import Image
    salida = argv[0]
    os.makedirs(salida, exist_ok=True)
    hoja(Image).save(os.path.join(salida, "protagonista.png"))
    hoja_enemigos(Image).save(os.path.join(salida, "enemigos.png"))
    guarda_gif(anima(Image), os.path.join(salida, "andar_cuadros.gif"))
    hoja_todos(Image).save(os.path.join(salida, "dibujos.png"))
    for f in ("protagonista.png", "enemigos.png", "andar_cuadros.gif", "dibujos.png"):
        print(f, os.path.getsize(os.path.join(salida, f)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
