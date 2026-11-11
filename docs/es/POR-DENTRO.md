# Por dentro

## Rehacer la ROM

`make verify` ensambla `src/youkai.asm` con pasmo y sale la ROM de 32 KB **byte a byte**. `make sanity` comprueba lo
que el reensamblado no cubre: que ning&uacute;n byte declarado como datos se lea como c&oacute;digo, que ning&uacute;n
punto de entrada caiga en datos y que los 32.768 bytes est&eacute;n explicados. `make test` pasa los tests. La ROM no
est&aacute; en el repositorio: hay que ponerla en la ra&iacute;z como `youkai.rom` (el volcado de GoodMSX, `[!]`, sha1
`15345c87...`; las versiones 1.1 de theNestruo y Yazio son modificaciones y no son esta).

| | bytes |
|---|---|
| c&oacute;digo trazado | 14.711 |
| datos con nombre | 18.057 |
| sin explicar | 0 |

El listado tiene 2.671 comentarios en 6.590 instrucciones (40,5 %), 878 rutinas y etiquetas, ninguna por debajo del
10 % comentado, y ninguna rutina llamada sin nombre.

## El cartucho

32 KB en 0x4000-0xBFFF, con la cabecera en 0x4000. INIT (0x4010) pone el cartucho tambi&eacute;n en la p&aacute;gina
2 y salta a 0x8000, que vuelve al arranque (0x7E80). Primero van los datos: los planos de los lugares (0x4038), las
74 pantallas (0x41AC) y sus y&#333;kai y objetos (0x4EBE), las piezas y los dibujos (0x54C7), los textos (0x5695), los
sprites (0x5800) y las casillas con sus colores (0x6000-0x7E7F). El c&oacute;digo va de 0x7E80 a 0xB757, con algunas
tablas en medio; detr&aacute;s, el sonido (0xB700-0xBFFF).

## La BIOS que usa

RSLREG y ENASLT para el slot; SETGRP, CHGCLR, WRTVDP, DISSCR y ENASCR; FILVRM, LDIRVM, WRTVRM y RDVRM; GTSTCK y GTTRIG
para los mandos y SNSMAT para la barra, GRAPH, STOP, F1 y las cinco teclas; WRTPSG para el sonido. Lee la fuente de
la BIOS (0x1D3F) y, en la demostraci&oacute;n, sus primeros bytes como mandos.

## La interrupci&oacute;n y el bucle

El arranque pone un salto a 0xB475 en el gancho H.TIMI. La interrupci&oacute;n hace el silencio pedido, corre el
sonido, cuenta cuadros y lee F1, STOP, los botones y la palanca. La partida corre en el **bucle** (`bucle`, 0x80B1):
una vez por cuadro, el sonido de fondo y, si no hay pausa, los y&#333;kai y objetos de la pantalla, el protagonista
(tocado, la ca&iacute;da, la palanca, el salto y el arma), las escaleras, los puntos, los y&#333;kai, el suceso, los
objetos y el parpadeo (`bucle_juego`, 0x80EE).

**Las pantallas.** Cada pantalla se monta en la RAM (0xE700, 32 x 20 casillas) desde su descripci&oacute;n
(`pantalla_monta`, 0x9257) y se copia a la VRAM desde la fila 2. Para cambiar de pantalla, la vieja y la nueva se
juntan (0xE980 y 0xEC00) y la ventana se desliza. El protagonista mira las casillas de sus pies, de su cuerpo y de los
lados (0x8C93 y siguientes): por debajo de 0x34, o de 0x3C a 0x7F, no sujetan.

## C&oacute;mo se ha hecho

El trazado sigue el c&oacute;digo desde INIT, la interrupci&oacute;n y las dos tablas de saltos (los objetos, 0x947B,
y los y&#333;kai, 0xA1E8), declaradas en `src/youkai.entries`. Lo dem&aacute;s se **midi&oacute; en openMSX**
(`tools/omsx_cobertura.tcl`) en un Philips VG 8020: no qued&oacute; fuera del trazado nada de lo que se ejecut&oacute;.
Parte de los comentarios vienen de otros Casio ya hechos (`comun/casio/porta.py`, en los tramos id&eacute;nticos;
tambi&eacute;n el motor de sonido) y otros se pusieron por regla donde el significado es seguro
(`work/reglas.py`: IX es siempre el protagonista, 0xE300), revisados.

Las grabaciones de la web (`tools/guiones/*.tcl`, grabadas con `tools/lanza_graba.ps1` en C-BIOS) apuntan, en cada
cuadro, los registros del VDP, la RAM desde 0xE000, el PSG y la VRAM que cambi&oacute;. `tools/pantallas.py` ejecuta
el t&iacute;tulo con `tools/bios.py` y lo coteja con la grabaci&oacute;n (**0 puntos distintos**), `tools/gifs.py` hace
los GIF y `tools/musica.py` ejecuta el motor de sonido.

## La RAM

| | |
|---|---|
| 0xE000 | jugando |
| 0xE009 | las vueltas |
| 0xE00A / 0xE0A0 | el lugar / el de antes |
| 0xE023 | las cinco teclas del t&iacute;tulo |
| 0xE028 / 0xE029 | la demostraci&oacute;n / su lista de mandos |
| 0xE047 | el final en marcha |
| 0xE0A1 / 0xE0A2 / 0xE0A3 | la columna y la fila en el plano / la pantalla |
| 0xE0A8 / 0xE0A9 | las vidas / el aguante (en medias) |
| 0xE180 | la palanca |
| 0xE183 / 0xE186 | la ca&iacute;da / el lugar acabado |
| 0xE198 | el lado por el que se sale de la pantalla |
| 0xE1B0 / 0xE1B2 | el suceso / sus golpes |
| 0xE1B3 / 0xE1B5 / 0xE1B7 | F1 / STOP / la pausa |
| 0xE280-0xE2D5 | el sonido |
| 0xE300 | el protagonista (y el arma, 0xE320) |
| 0xE340 | los doce y&#333;kai |
| 0xE400 | los objetos de la pantalla |
| 0xE700 | la pantalla (32 x 20) |
