#!/usr/bin/env python3
"""EL CONTENIDO de la web de esta ROM: lo unico que es de este juego.

jekyll.py y make_web.py son la maquinaria y no llevan dentro el nombre de
ningun juego: lo leen de aqui.

Todas las cifras de aqui estan medidas sobre esta ROM, con las herramientas
de tools/: CODIGO y DATOS los imprime tools/presupuesto.py (make sanity),
INSTRUCCIONES, COMENTARIOS y RUTINAS los da tools/densidad.py (make densidad:
"de N" rutinas, "N instrucciones, M comentarios").
"""

NOMBRE = "Youkai Yashiki"
EDITOR = "Casio"
ANIO = 1986
REPOSITORIO = "https://github.com/antxiko/YoukaiYashiki-disassembly"
SHA1 = "15345c8745028c96fc79036b2e3e180ad2f62dab"

CODIGO = 14711
DATOS = 18057
RUTINAS = 878
INSTRUCCIONES = 6590
COMENTARIOS = 2671


def densidad(idioma):
    """El porcentaje comentado, con la coma o el punto de cada idioma."""
    d = "%.1f" % (100.0 * COMENTARIOS / INSTRUCCIONES)
    return d.replace(".", ",") if idioma == "es" else d


PIE_LEGAL = {
    "es": "<em>Youkai Yashiki</em> (妖怪屋敷, \"la mansi&oacute;n de los y&#333;kai\") es un juego de Casio para MSX, de "
          "1986, en un cartucho de 32 KB. Todos los derechos sobre el juego siguen siendo de sus titulares. Este "
          "trabajo es de preservaci&oacute;n, estudio y documentaci&oacute;n, y la imagen de la ROM no se distribuye.",
    "en": "<em>Youkai Yashiki</em> (妖怪屋敷, \"the y&#333;kai mansion\") is a 1986 Casio game for the MSX, on a 32 KB "
          "cartridge. All rights in the game remain with their holders. This is preservation, study and documentation "
          "work, and the ROM image is not distributed.",
}

PORTADA = {
    "es": dict(
        titulo="Youkai Yashiki - desensamblado comentado",
        claim="Un juego de plataformas por cinco lugares encantados, del cementerio a la mansi&oacute;n, pantalla a "
              "pantalla por escaleras y puertas: el protagonista salta, lanza su arma contra los y&#333;kai, recoge "
              "lo que encuentra y en cada sala vence al suceso que la guarda. El t&iacute;tulo sale de ejecutar la ROM, "
              "cotejado con openMSX punto a punto; la partida en GIF, jugada en openMSX; las m&uacute;sicas, de su "
              "propio motor, id&eacute;nticas a openMSX cuadro a cuadro en las que suenan en las grabaciones.",
        ficha=["Casio - <b>(c) 1986</b>",
               "Cartucho de <b>32 KB</b> (cabecera en 0x4000)",
               "<b>MSX</b>", "Volcado <b>15345c87...</b>"],
        aviso="<b>Aqu&iacute; no hay capturas del juego.</b> El t&iacute;tulo sale de ejecutar la ROM y los GIF son "
              "la ROM <b>funcionando en openMSX</b>: en cada cuadro se apuntan la VRAM, la RAM y los registros del "
              "VDP, y <b>c&oacute;digo nuestro los pinta</b>.",
    ),
    "en": dict(
        titulo="Youkai Yashiki - commented disassembly",
        claim="A platform game through five haunted places, from the graveyard to the mansion, screen by screen by "
              "ladders and doors: the hero jumps, throws his weapon at the y&#333;kai, picks up what he finds and in "
              "each place beats the event that guards it. The title comes from running the ROM, checked against "
              "openMSX point by point; the game in GIF, played in openMSX; the tunes, from its own engine, identical "
              "to openMSX frame by frame in those that play in the recordings.",
        ficha=["Casio - <b>(c) 1986</b>",
               "<b>32 KB</b> cartridge (header at 0x4000)",
               "<b>MSX</b>", "Dump <b>15345c87...</b>"],
        aviso="<b>There are no screenshots of the game here.</b> The title comes from running the ROM and the GIFs "
              "are the ROM <b>running in openMSX</b>: on every frame the VRAM, the RAM and the VDP registers are "
              "logged, and <b>our own code paints them</b>.",
    ),
}

PAGINAS = [
    [("THE-GAME.html", "LA-PARTIDA.html", "The game", "La partida",
      "the CASIO intro, the title, the controls, the lives and the endurance, the falls and GAME OVER",
      "la presentaci&oacute;n de CASIO, el t&iacute;tulo, los mandos, las vidas y el aguante, las ca&iacute;das y "
      "GAME OVER"),
     ("THE-PLACES.html", "LOS-LUGARES.html", "The places", "Los lugares",
      "the five places and their 74 screens, the five events (the bosses) and the ending",
      "los cinco lugares y sus 74 pantallas, los cinco sucesos (los jefes) y el final"),
     ("THE-SPRITES.html", "LOS-SPRITES.html", "The sprites", "Los sprites",
      "the hero, his weapon, the y&#333;kai type by type and the pause, put together from the ROM tables",
      "el protagonista, su arma, los y&#333;kai tipo a tipo y la pausa, montados desde las tablas de la ROM"),
     ("THE-TEXTS.html", "LOS-TEXTOS.html", "The texts", "Los textos",
      "every text in the ROM", "todos los textos de la ROM"),
     ("THE-MUSIC.html", "LA-MUSICA.html", "The music", "La m&uacute;sica",
      "the tunes, from its own sound engine and checked against openMSX",
      "las m&uacute;sicas, de su propio motor de sonido y cotejadas con openMSX")],
    [("CURIOSITIES.html", "CURIOSIDADES.html", "Curiosities", "Curiosidades",
      "the five keys on the title, F1, a demo that plays the BIOS, leftovers",
      "las cinco teclas del t&iacute;tulo, F1, una demostraci&oacute;n que juega la BIOS, sobrantes"),
     ("SECRETS-AND-BUGS.html", "SECRETOS-Y-FALLOS.html", "Secrets and bugs", "Secretos y fallos",
      "what was searched for: the five keys, F1 and the demo that plays the BIOS, the high score set to zero past 9,999,990, the cursor keys and joystick mixed, and lives for points that do not exist",
      "lo que se ha buscado: las cinco teclas, F1 y la demostraci&oacute;n que juega la BIOS, el r&eacute;cord a cero pasados los 9.999.990, los cursores y el mando que se mezclan, y unas vidas por puntos que no existen")],
    [("UNDER-THE-HOOD.html", "POR-DENTRO.html", "Under the hood", "Por dentro",
      "rebuilding the ROM, the cartridge, the BIOS it uses, the loop, the screens, the RAM and the tools",
      "rehacer la ROM, el cartucho, la BIOS que usa, el bucle, las pantallas, la RAM y las herramientas")],
]

# Repositorio nuevo: no hay paginas viejas que redirigir.
VIEJAS = {}

LOGOTIPO = "logotipo.png"
