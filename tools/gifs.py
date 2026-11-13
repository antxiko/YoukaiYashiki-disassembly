"""Los GIF de la web: tramos de las grabaciones de openMSX (tools/guiones/*.tcl, grabados con
tools/lanza_graba.ps1 en C-BIOS_MSX1_JP, -bp 0xB475 -ram "0xE000 0x1000"), pintados con tools/vdp.py; cada imagen
dura el tiempo emulado que dura en la grabacion.

Los tramos salen de la RAM grabada (work/resumen.py): 0xE000 jugando, 0xE00A la sala, 0xE0A3 la pantalla, 0xE0A8
las vidas, 0xE0A9 el aguante, 0xE183 la muerte, 0xE2BD la musica.

  atraccion   sin tocar nada: la presentacion de CASIO, el titulo y la demostracion
  partida     el piloto (tools/guiones/piloto.tcl): el cementerio, cuatro caidas y GAME OVER
  trucos      las teclas del titulo (el aguante lleno, los golpes no lo quitan) y el piloto contra los fantasmas
  forzada     FORZADA con pokes: las salas 1 a 4 (0xE00A y F1)
  pausa       el piloto y STOP a los 300 cuadros de juego: la pausa con su marco; STOP otra vez a los 600. El GIF
              es LIMPIO: solo los cuatro sprites del marco (la tabla de sprites grabada, sin la pantalla), en su
              recuadro de 32 x 32, a 4x y con el fondo transparente, mientras la tabla de sprites grabada lleva el
              marco (el sprite 0 con el dibujo 0xD0: la VRAM va un cuadro por detras de 0xE1B7)
  final       FORZADO (tools/guiones/final.tcl): el final, en la pantalla 0x3C del lugar 4
  jefes       FORZADA (tools/guiones/jefes.tcl): los cinco sucesos, cada uno con un piloto hecho para el; el del
              lugar 1 se vence jugando

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
    ("final.gif", "final", 1180, 1990, 2),              # FORZADO: el final
    ("jefe_0.gif", "jefes", 1182, 2100, 3),             # FORZADA: el suceso del lugar 0
    ("jefe_1.gif", "jefes", 5682, 6600, 3),             # FORZADA: el del lugar 1...
    ("jefe_1_vencido.gif", "jefes", 8560, 9150, 2),     # ...y vencido jugando: la musica 7 y los dos que suben
    ("jefe_2.gif", "jefes", 9808, 10700, 3),            # FORZADA: el del lugar 2
    ("jefe_3.gif", "jefes", 14322, 15200, 3),           # FORZADA: el del lugar 3
    ("jefe_4.gif", "jefes", 18822, 19700, 3),           # FORZADA: el del lugar 4
]
PAUSA = (0x28, 0x5E, 0x48, 0x7E)                        # el recuadro del marco: X 0x28-0x47, Y 0x5E-0x7D


def pausa_limpia(salida, desde=640, hasta=1060, escala=4):
    """La pausa SIN la pantalla: solo los sprites grabados (vdp.sprites sobre nada), en el recuadro del marco."""
    from PIL import Image
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    g = vdp.Gif()
    previo = None
    for n, c in enumerate(vdp.cuadros(os.path.join(raiz, "work", "pausa.bin"))):
        if n > hasta:
            break
        attr = (c["regs"][5] & 0x7F) * 0x80
        if n < desde or c["vram"][attr + 2] != 0xD0:        # la VRAM va un cuadro por detras de la RAM (0xE1B7)
            continue
        t = [[0] * 256 for _ in range(192)]
        vdp.sprites(c["vram"], c["regs"], t)
        x0, y0, x1, y1 = PAUSA
        im = Image.new("P", (x1 - x0, y1 - y0))
        pal = []
        for col in vdp.PALETA:
            pal += list(col)
        im.putpalette(pal + [0] * (768 - len(pal)))
        im.putdata([t[y][x] for y in range(y0, y1) for x in range(x0, x1)])
        im = im.resize((im.width * escala, im.height * escala), Image.NEAREST)
        if previo:
            g.pon(previo[0], (c["t"] - previo[1]) * 1000.0 / g.ms)
        previo = (im, c["t"])
    g.pon(previo[0], 1)
    ruta = os.path.join(salida, "pausa.gif")
    g.guarda(ruta, 4000, transparente=True)
    print("%-24s %4d imagenes, %8d bytes" % ("pausa.gif", len(g), os.path.getsize(ruta)))


def main(salida):
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    solo = sys.argv[2:]
    if not solo or "pausa.gif" in solo:
        pausa_limpia(salida)
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
