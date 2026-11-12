"""Los GIF de la web: tramos de las grabaciones de openMSX (tools/guiones/*.tcl, grabados con
tools/lanza_graba.ps1 en C-BIOS_MSX1_JP, -bp 0xB475 -ram "0xE000 0x1000"), pintados con tools/vdp.py; cada imagen
dura el tiempo emulado que dura en la grabacion.

Los tramos salen de la RAM grabada (work/resumen.py): 0xE000 jugando, 0xE00A la sala, 0xE0A3 la pantalla, 0xE0A8
las vidas, 0xE0A9 el aguante, 0xE183 la muerte, 0xE2BD la musica.

  atraccion   sin tocar nada: la presentacion de CASIO, el titulo y la demostracion
  partida     el piloto (tools/guiones/piloto.tcl): el cementerio, cuatro caidas y GAME OVER
  trucos      las teclas del titulo (el aguante lleno, los golpes no lo quitan) y el piloto contra los fantasmas
  forzada     FORZADA con pokes: las salas 1 a 4 (0xE00A y F1)
  pausa       el piloto y STOP a los 300 cuadros de juego: la pausa con su marco; STOP otra vez a los 600

Las grabaciones son grandes: cada una se lee UNA vez.

Uso: gifs.py docs/imagenes
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vdp          # noqa: E402

# (fichero, grabacion, desde, hasta, cada)
TRAMOS = [
    ("presentacion.gif", "atraccion", 1, 140, 3),       # la presentacion de CASIO
    ("demostracion.gif", "atraccion", 600, 1800, 3),    # la demostracion
    ("salida.gif", "partida", 400, 900, 2),             # la partida empieza y la primera caida
    ("game_over.gif", "partida", 2150, 2700, 3),        # la ultima caida y GAME OVER
    ("fantasmas.gif", "trucos", 400, 1400, 3),          # con las teclas del titulo: el cementerio
    ("sala_1.gif", "forzada", 1000, 1900, 3),           # FORZADA: la sala 1
    ("sala_2.gif", "forzada", 2500, 3400, 3),           # FORZADA: la sala 2
    ("sala_3.gif", "forzada", 4000, 4900, 3),           # FORZADA: la sala 3
    ("sala_4.gif", "forzada", 5500, 6400, 3),           # FORZADA: la sala 4
    ("pausa.gif", "pausa", 640, 1060, 2),               # STOP: la pausa y su marco, y STOP otra vez
]


def main(salida):
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    solo = sys.argv[2:]
    for grab in dict.fromkeys(t[1] for t in TRAMOS if not solo or t[0] in solo):
        mios = [t for t in TRAMOS if t[1] == grab and (not solo or t[0] in solo)]
        gifs = {t[0]: vdp.Gif() for t in mios}
        tope = max(t[3] for t in mios) + max(t[4] for t in mios)
        espera = {}                                    # fichero -> (imagen, t) pendiente de su duracion
        for n, c in enumerate(vdp.cuadros(os.path.join(raiz, "work", grab + ".bin"))):
            if n > tope:
                break
            for fichero, _, desde, hasta, cada in mios:
                if desde <= n <= hasta + cada and (n - desde) % cada == 0:
                    if fichero in espera:
                        im, t = espera.pop(fichero)
                        gifs[fichero].pon(im, (c["t"] - t) * 1000.0 / gifs[fichero].ms)
                    if n <= hasta:
                        espera[fichero] = (vdp.imagen(c["vram"], c["regs"], 1), c["t"])
        for fichero, _, desde, hasta, cada in mios:
            if fichero in espera:                       # la grabacion acaba antes: la ultima, un paso
                im, _t = espera.pop(fichero)
                gifs[fichero].pon(im, cada)
            ruta = os.path.join(salida, fichero)
            gifs[fichero].guarda(ruta, 4000)
            print("%-24s %4d imagenes, %8d bytes" % (fichero, len(gifs[fichero]), os.path.getsize(ruta)))


if __name__ == "__main__":
    main(sys.argv[1])
