#!/usr/bin/env python3
"""Los sprites de Youkai Yashiki MONTADOS DESDE LA ROM (ninguna imagen es una captura).

Los dibujos son los 0x800 bytes de 0x5800 que `sprites_dibujos` (0xB36D) pone tal cual en 0x3800; sprites de 16 x 16.
Cada cosa son sprites de 16 bytes desde 0xE300 (los 4 primeros, sus atributos): el protagonista en 0xE300 y 0xE310,
el arma en 0xE320 y los doce enemigos desde 0xE340 (+4 el tipo, por la tabla 0xA1E8).

  protagonista.png   dos sprites en el mismo sitio: el dibujo en magenta y el dibujo + 0x60 en amarillo claro (`sala_empieza`
                     0x806D, `caida_para` 0x87A3): de pie 0x0C y 0x14 (0x880D, por su lado), andando 0x08-0x1C; y el
                     arma (0xE320, `ataque_sale`): 0x28 o 0x2C segun el lado
  enemigos.png       TIPO A TIPO (la tabla de rutinas 0xA1E8): las figuras que el codigo de cada tipo pone, con sus
                     dibujos y colores (TIPOS)
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
# LOS TIPOS DE ENEMIGO (la tabla de rutinas 0xA1E8, +4 del enemigo): (tipos, rutina, figuras). Cada figura es una
# imagen: sus sprites (dibujo, color, dx, dy). Los que esperan (`enemigo_espera` 0xA216) salen antes con 0x38/0x3C en
# blanco, y al vencerlos (0xA22C) se quedan con 0x38/0x3C en su color: eso no se repite aqui. Los tipos 0x00 (el
# enemigo no se mueve: `enemigos` salta los de tipo 0), 0x06 (0xA5EA) y 0x0A (0xA777) no tienen nada: sus rutinas son
# un `ret` y su sprite no lleva dibujo ni color.
TIPOS = [
    ((0x01,), 0xA278, [[(0x30, 7, 0, 0)], [(0x34, 15, 0, 0)]]),
    ((0x02,), 0xA278, [[(0x30, 15, 0, 0)], [(0x34, 15, 0, 0)]]),
    ((0x03,), 0xA444, [[(0x4C, 5, 0, 0)], [(0x50, 5, 0, 0)], [(0x4C, 4, 0, 0)]]),
    ((0x04,), 0xA444, [[(0x4C, 9, 0, 0)], [(0x50, 9, 0, 0)], [(0x4C, 4, -4, 0), (0x4C, 4, 4, 0)]]),
    ((0x05,), 0xA4C3, [[(0x88, 6, 0, 0), (0x8C, 10, 0, 16)], [(0x9C, 6, 0, 0), (0xA0, 10, 0, 16)]]),
    ((0x07,), 0xA5EB, [[(0x54, 15, 0, 0)], [(0x58, 15, 0, 0)], [(0x54, 7, 0, 0)]]),
    ((0x08,), 0xA5EB, [[(0x94, 9, 0, 0)], [(0x98, 9, 0, 0)], [(0x94, 3, 0, 0)]]),
    ((0x09,), 0xA6B7, [[(0x44, 4, 0, 0)], [(0x48, 4, 0, 0)]]),
    ((0x0B,), 0xA778, [[(0xE8, 9, 0, 0), (0xEC, 11, 0, 0)], [(0xF0, 9, 0, 0), (0xF4, 11, 0, 0)],
                       [(0xF8, 9, 0, 0), (0xFC, 11, 0, 0)]]),
    ((0x0C, 0x0E, 0x0F, 0x14), 0xA853, [[(0xD4, 15, 0, 0)], [(0xD8, 15, 0, 0)], [(0xDC, 15, 0, 0)],
                                        [(0xE0, 15, 0, 0)], [(0xD4, 9, 0, 0)], [(0xD4, 5, 0, 0)]]),
    ((0x0D,), 0xAA49, [[(0xA4, 9, 0, 0)]]),
    ((0x10,), 0xABB8, [[(0xB8, 11, 0, 0)], [(0xA8, 11, 0, 0)]]),
    ((0x11,), 0xACC6, [[(0x38, 5, 0, 0)], [(0x3C, 5, 0, 0)]]),
    ((0x12,), 0xABB8, [[(0x40, 9, 0, 0)]]),
    ((0x13,), 0xAD6F, [[(0x40, 1, 0, 0)], [(0x40, 3, 0, 0)], [(0x40, 5, 0, 0)], [(0x40, 7, 0, 0)], [(0x40, 9, 0, 0)]]),
    ((0x15,), 0xAA9A, [[(0xAC, 11, 0, 0), (0xB0, 15, 0, 16)], [(0xAC, 9, 0, 0), (0xB0, 15, 0, 16)]]),
    ((0x16,), 0xAA9A, [[(0xAC, 7, 0, 0), (0xB0, 15, 0, 16)], [(0xAC, 5, 0, 0), (0xB0, 15, 0, 16)]]),
]
# Los que pasan por `enemigo_espera` (0x38/0x3C en blanco antes de moverse)
ESPERAN = {0x01, 0x02, 0x05, 0x07, 0x08, 0x09}
# Lo que no se ve: el 0x10 espera con el dibujo vacio 0xE4 (0xABE9); y el 0x0C que no entra por un borde (0xA8A6) se
# queda UN cuadro con el color 15 y el dibujo que tuviera (0x00 tras `enemigos_borra`: el protagonista de espaldas)
EXTRA = {0x10: {(0xE4, 11)}, 0x0C: {(0x00, 15)}, 0x0E: {(0x00, 15)}, 0x0F: {(0x00, 15)}, 0x14: {(0x00, 15)}}


def permitidos(tipo):
    """(dibujo, color) que el codigo de ese tipo pone en su primer sprite: sus dibujos (y el + 4) con sus colores (el
    codigo los cambia por separado), la espera en blanco, vencido 0x38/0x3C en sus colores, y EXTRA."""
    for tipos, _, figuras in TIPOS:
        if tipo in tipos:
            colores = {f[0][1] for f in figuras}
            dibujos = {f[0][0] + k for f in figuras for k in (0, 4)} | {0x38, 0x3C}
            r = {(d, c) for d in dibujos for c in colores} | EXTRA.get(tipo, set())
            if tipo in ESPERAN:
                r |= {(0x38, 15), (0x3C, 15)}
            return r
    return set()


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
    """Una fila por tipo: su numero y sus figuras."""
    from PIL import ImageDraw
    pat, E = patrones(), 3
    alto = [20 + 16 * any(dy for f in figs for *_, dy in f) for _, _, figs in TIPOS]
    im = Image.new("RGB", (160 * E, (sum(alto) + 4) * E), FONDO)
    d = ImageDraw.Draw(im)
    y = 2
    for (tipos, _, figuras), h in zip(TIPOS, alto):
        d.text((2 * E, (y + 5) * E), " ".join("%02X" % t for t in tipos), fill=(255, 255, 0))
        for k, fig in enumerate(figuras):
            for dib, c, dx, dy in fig:
                pinta(im, pat, dib, 30 + 21 * k + dx, y + dy, c, E)
        y += h
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
        for k, i in enumerate((0, 2, 7)):                 # los tipos 0x01, 0x03 y 0x09, con sus dos dibujos
            dib, c, _, _ = TIPOS[i][2][(n // 8) % 2][0]
            pinta(im, pat, dib, 22 + 20 * k, 2, c, E)
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
    4) los enemigos (0xE340, 16 bytes), TIPO A TIPO: el dibujo y el color de su primer sprite, uno de los que pone el
       codigo de su tipo (permitidos); cuantos cuadros de cada tipo."""
    pat = patrones()
    tot = dict(patrones=0, pat_carga=0, pat_mal=0, prota=0, prota_sin_poner=0, prota_mal=0, arma=0, arma_mal=0,
               enemigos=0, enemigos_mal=0)
    por_tipo = {}
    for grab in ("atraccion", "partida", "forzada", "trucos", "jefes", "final"):
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
                ok = (e[2], e[3] & 15) in permitidos(e[4])
                tot["enemigos"] += ok
                tot["enemigos_mal"] += not ok
                pt = por_tipo.setdefault("%02X" % e[4], [0, 0])
                pt[0 if ok else 1] += 1
    tot["por_tipo"] = dict(sorted(por_tipo.items()))
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
