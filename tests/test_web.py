"""La web, comprobada contra el listado: las cifras de la portada y el
barrido de nombres y ficheros de otros juegos de la serie."""

import os
import re
import subprocess
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from test_listado import ASM, FILA, TAM      # noqa: E402

DOCS = os.path.join(RAIZ, "docs")

# Los demas juegos de la serie. Que el nombre de otro salga en una pagina de
# este es casi siempre un copia y pega.
OTROS_JUEGOS = (
    "Tennis", "Pitfall", "Temptations", "Stardust", "Ale Hop", "Colt 36",
    "Antarctic", "Athletic Land", "Monkey Academy", "F-1 Spirit", "Pippols",
    "Time Pilot", "Frogger", "Super Cobra", "Billiards", "Mahjong",
    "Hyper Rally", "Nemesis", "Demonia", "Cabbage", "Hole in One",
    "Casio World Open", "3D Golf", "Konami's Baseball", "Yie Ar Kung-Fu",
    "King's Valley", "Sky Jaguar", "Mopi Ranger", "Descubrimiento",
    "War in Middle Earth", "Ping Pong", "Soccer", "Football", "Road Fighter",
    "Hyper Sports", "Hyper Olympic", "Goonies", "Knightmare", "Twin Bee",
    "Penguin", "Bomber", "Circus Charlie", "Comic Bakery", "Magical Tree",
    "King Kong", "Vampire Killer", "Q*bert", "Qbert", "Quarth", "Metal Gear",
    "Space Manbow", "Salamander", "Parodius", "Contra", "Usas", "Galious",
    "Goemon", "Hinotori", "Shalom", "Rastan", "Dunk Shot", "Pennant",
    "Game Master", "Synthesizer", "Majutsushi", "Sparkie", "Juno First",
    "Crazy Train", "Pooyan", "Ski Command", "Exciting Baseball", "Exciting Jockey",
    "Pachinko", "Car Fighter", "Ice World", "Shindobaddo", "Sindbad", "Simbad",
    "Eagle Fighter", "Exoide", "Iga Ninpouchou", "Ninpouchou", "Mangetsu", "Koneko", "Moai", "Kenja", "Stone of Wisdom", "Seal of Hades", "Hadesu",
)

# La seccion del codigo compartido con los otros Konami de la serie los
# nombra a proposito: la escribe pon_en_webs.py, de MSX-disassembly-database.
_COMPARTIDO = re.compile(
    r"(?:^## |<h2[^>]*>)(?:Code shared with other Konami cartridges|"
    r"Código compartido con otros cartuchos de Konami)"
    r".*?(?=^## |<h2|</main>|<footer|\Z)", re.S | re.M)


def lee_texto(ruta):
    with open(ruta, encoding="utf-8") as f:
        return f.read()


def bytes_de_datos_del_listado():
    """Cuantos bytes salen en filas defb/defw: los DATOS del cartucho."""
    n = 0
    for ln in lee_texto(ASM).splitlines():
        m = FILA.match(ln)
        if not m:
            continue
        toks = [t for t in m.group(2).split(",") if t.strip()]
        n += len(toks) * (1 if m.group(1) == "b" else 2)
    return n


def densidad():
    return subprocess.run(
        [sys.executable, os.path.join(RAIZ, "tools", "densidad.py"), ASM],
        capture_output=True, text=True, check=True).stdout


class LasCifrasDeLaPortada(unittest.TestCase):
    def setUp(self):
        import contenido_web
        self.w = contenido_web

    def test_la_suma_de_bytes_da_el_cartucho(self):
        self.assertEqual(self.w.CODIGO + self.w.DATOS, TAM)

    def test_las_cifras_de_bytes_son_las_de_este_listado(self):
        datos = bytes_de_datos_del_listado()
        self.assertEqual(self.w.DATOS, datos)
        self.assertEqual(self.w.CODIGO, TAM - datos)

    def test_la_densidad_y_las_rutinas_son_las_del_listado(self):
        salida = densidad()
        m = re.search(r"(\d+) instrucciones, (\d+) comentarios", salida)
        self.assertEqual(self.w.INSTRUCCIONES, int(m.group(1)))
        self.assertEqual(self.w.COMENTARIOS, int(m.group(2)))
        m = re.search(r"por debajo del 10 %, de (\d+)", salida)
        self.assertEqual(self.w.RUTINAS, int(m.group(1)))

    def test_las_paginas_dicen_las_mismas_cifras(self):
        es = lee_texto(os.path.join(DOCS, "es", "POR-DENTRO.md"))
        en = lee_texto(os.path.join(DOCS, "UNDER-THE-HOOD.md"))
        mil = lambda n, s: f"{n:,}".replace(",", s)   # noqa: E731
        for n in (self.w.CODIGO, self.w.DATOS, self.w.COMENTARIOS, self.w.INSTRUCCIONES):
            self.assertIn(mil(n, "."), es)
            self.assertIn(mil(n, ","), en)
        self.assertIn(self.w.densidad("es") + " %", es)
        self.assertIn(self.w.densidad("en") + "%", en)

    def test_la_ficha_dice_el_volcado(self):
        for idioma in ("es", "en"):
            ficha = " ".join(self.w.PORTADA[idioma]["ficha"])
            self.assertIn(self.w.SHA1[:8], ficha)


class SinNombresDeOtroJuego(unittest.TestCase):
    def _revisa(self, ruta):
        texto = _COMPARTIDO.sub("", lee_texto(ruta))
        for juego in OTROS_JUEGOS:
            self.assertNotIn(juego, texto, "%s nombra a %s" % (ruta, juego))

    def test_el_encabezado_del_listado_es_de_este_juego(self):
        cabeza = "\n".join(lee_texto(ASM).splitlines()[:30])
        for juego in OTROS_JUEGOS:
            self.assertNotIn(juego, cabeza)

    def test_la_licencia_y_los_avisos_son_de_este_juego(self):
        for fn in ("LICENSE", "README.md", "README.es.md", "AVISO-LEGAL.md",
                   "LEGAL-NOTICE.md"):
            self._revisa(os.path.join(RAIZ, fn))
            self.assertIn("Youkai Yashiki", lee_texto(os.path.join(RAIZ, fn)))

    def test_las_herramientas_no_apuntan_a_otro_juego(self):
        for fn in os.listdir(os.path.join(RAIZ, "tools")):
            if fn.endswith((".py", ".sh", ".tcl", ".ps1")):
                texto = lee_texto(os.path.join(RAIZ, "tools", fn)).lower()
                for rom in re.findall(r"['\"/ ](\w+)\.rom", texto):
                    self.assertIn(rom, ("youkai", "cbios_main_msx1_jp"), "%s: %s.rom" % (fn, rom))

    def test_la_web_no_nombra_otro_juego(self):
        for raiz, _, ficheros in os.walk(DOCS):
            for fn in ficheros:
                if fn.endswith((".md", ".html")):
                    self._revisa(os.path.join(raiz, fn))


class LasImagenes(unittest.TestCase):
    def test_estan_todas_las_que_se_nombran(self):
        for raiz, _, ficheros in os.walk(DOCS):
            for fn in ficheros:
                if not fn.endswith(".md"):
                    continue
                texto = lee_texto(os.path.join(raiz, fn))
                for img in re.findall(r"\]\(((?:\.\./)?imagenes/[^)]+)\)", texto):
                    self.assertTrue(os.path.exists(os.path.normpath(os.path.join(raiz, img))),
                                    "%s: falta %s" % (fn, img))

    def test_los_dos_idiomas_tienen_las_mismas_imagenes(self):
        pares = [("THE-GAME.md", "LA-PARTIDA.md"), ("THE-PLACES.md", "LOS-LUGARES.md"),
                 ("THE-SPRITES.md", "LOS-SPRITES.md"), ("THE-TEXTS.md", "LOS-TEXTOS.md"), ("THE-MUSIC.md", "LA-MUSICA.md"),
                 ("CURIOSITIES.md", "CURIOSIDADES.md"), ("SECRETS-AND-BUGS.md", "SECRETOS-Y-FALLOS.md"), ("UNDER-THE-HOOD.md", "POR-DENTRO.md")]
        for en, es in pares:
            ie = re.findall(r"imagenes/([^)]+)\)", lee_texto(os.path.join(DOCS, en)))
            ia = re.findall(r"imagenes/([^)]+)\)", lee_texto(os.path.join(DOCS, "es", es)))
            self.assertEqual(ie, ia, en)

    def test_las_diez_musicas(self):
        for f in ("casio", "sala", "caida", "continuar", "game_over", "suceso", "final", "fondo", "fondo_puerta",
                  "fondo_suceso"):
            self.assertTrue(os.path.exists(os.path.join(DOCS, "audio", "musica_%s.mp3" % f)))
            for pag in ("THE-MUSIC.md", "es/LA-MUSICA.md"):
                self.assertIn("musica_%s.mp3" % f, lee_texto(os.path.join(DOCS, pag)))

    def test_cada_gif_una_vez(self):
        """Cada GIF sale en una sola pagina de cada idioma, y todos salen."""
        for carpeta in (DOCS, os.path.join(DOCS, "es")):
            vistos = []
            for fn in os.listdir(carpeta):
                if fn.endswith(".md"):
                    vistos += re.findall(r"imagenes/([^)]+\.gif)\)", lee_texto(os.path.join(carpeta, fn)))
            self.assertEqual(len(vistos), len(set(vistos)), carpeta)
            gifs = [f for f in os.listdir(os.path.join(DOCS, "imagenes")) if f.endswith(".gif")]
            self.assertEqual(sorted(vistos), sorted(gifs), carpeta)

if __name__ == "__main__":
    unittest.main()


class TodosLosDibujos(unittest.TestCase):
    """Cada dibujo de la tabla de sprites de la ROM (los 0x800 bytes de 0x5800) sale en la tabla de Los sprites de los
    dos idiomas, con quien lo pone o como sin uso; y lo que dice la web cuadra con el listado: la direccion de cada uso
    es una instruccion que escribe ese dibujo (o lo calcula) en un sprite, y el sin uso no lo escribe ninguna."""

    def setUp(self):
        import hojas
        self.h = hojas

    def test_los_64_en_la_tabla_de_los_dos_idiomas(self):
        for pag in ("THE-SPRITES.md", os.path.join("es", "LOS-SPRITES.md")):
            texto = lee_texto(os.path.join(DOCS, pag))
            filas = [ln for ln in texto.splitlines() if ln.startswith("| 0x")]
            listados = set()
            for ln in filas:
                listados.update(int(x, 16) for x in re.findall(r"0x([0-9A-F]{2})\b", ln.split("|")[1]))
            self.assertEqual(listados, set(range(0, 256, 4)), pag)

    def test_cada_uso_es_una_escritura_de_dibujo(self):
        lineas = {}
        for ln in lee_texto(ASM).splitlines():
            m = re.search(r";([0-9a-f]{4})\b", ln)
            if m and ln.startswith("\t"):
                lineas.setdefault(int(m.group(1), 16), ln)
        for d, a in self.h.USOS.items():
            ln = lineas[a]
            self.assertRegex(ln, r"ld \((?:i[xy]\+0[0-3][28]h|0e3[0-9a-f]2h)\),", "0x%02X en 0x%04X" % (d, a))
            if "),a" not in ln.replace("\t", ""):
                self.assertIn("0%02xh" % d, ln.lower(), "0x%02X en 0x%04X" % (d, a))

    def test_nadie_escribe_el_0x90(self):
        for ln in lee_texto(ASM).splitlines():
            if re.search(r"ld \((?:i[xy]\+0[0-3][28]h|0e3[0-9a-f]2h)\),0?90h", ln):
                self.fail(ln)
        self.assertEqual(self.h.SIN_USO, [0x90])
        self.assertEqual(set(self.h.USOS) | set(self.h.SIN_USO), set(range(0, 256, 4)))
