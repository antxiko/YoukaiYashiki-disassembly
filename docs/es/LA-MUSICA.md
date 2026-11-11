# La m&uacute;sica

Las m&uacute;sicas, a tres voces. No son grabaciones hechas a mano: `tools/musica.py` **ejecuta el motor de sonido
de la propia ROM** con `tools/z80run.py` -la rutina del sonido (`sonido`, 0xB77C), cuadro a cuadro, con el
n&uacute;mero que escribe el juego- y apunta lo que escribe en el PSG por la BIOS (WRTPSG).

**Cotejadas con openMSX** las cinco que suenan en las grabaciones (`tools/guiones/`: la demostraci&oacute;n, la
partida del piloto, la de las teclas del t&iacute;tulo y la forzada): la presentaci&oacute;n, la sala, la ca&iacute;da,
GAME OVER y el fondo de la partida, **0 distintos** en todos los cuadros mirados. Las otras cinco salen de ejecutar
el motor con su n&uacute;mero y no se han podido cotejar: no suenan en ninguna grabaci&oacute;n.

## El motor

Es el de otros juegos de Casio, casi en la misma direcci&oacute;n: atiende tres
**pedidos** -una m&uacute;sica (0xE2BE), un efecto del canal A (0xE2C0) y otro de B y C (0xE2C2)- y gana el de
n&uacute;mero menor. Las tablas: ocho m&uacute;sicas en 0xB700 (la 0, nada), ocho efectos del canal A en 0xB730, seis
de B y C en 0xB740 y catorce duraciones en 0xBA2D. Durante la partida el fondo es un **efecto** de B y C que el bucle
pide en cada pasada (`sonido_fondo`, 0x81AD).

| | qui&eacute;n la pide | dura | cotejada |
|---|---|---:|---|
| la presentaci&oacute;n de CASIO | 0xB5EA | 1,1 s | s&iacute; |
| una sala empieza | 0x808D | 4,3 s | s&iacute; |
| el fondo de la partida | el bucle (efecto 5) | 14,9 s, vuelve a pedirse | s&iacute; |
| la ca&iacute;da | 0xAE2B | 0,8 s | s&iacute; |
| GAME OVER | 0xAF35 | 2,7 s | s&iacute; |
| CONTINUE / END | 0xAEB9 | 5,2 s | no |
| el fondo tras una puerta | el bucle (efecto 4) | 17,1 s | no |
| el fondo con el suceso | el bucle (efecto 2) | 8,6 s | no |
| el suceso vencido | 0x8393 y 0x84D9 | 10,7 s | no |
| el final | 0xA82B | 8,6 s | no |

## La presentaci&oacute;n de CASIO

<audio controls src="../audio/musica_casio.mp3"></audio>

## Una sala empieza

<audio controls src="../audio/musica_sala.mp3"></audio>

## El fondo de la partida

<audio controls src="../audio/musica_fondo.mp3"></audio>

## La ca&iacute;da

<audio controls src="../audio/musica_caida.mp3"></audio>

## GAME OVER

<audio controls src="../audio/musica_game_over.mp3"></audio>

## CONTINUE / END

<audio controls src="../audio/musica_continuar.mp3"></audio>

## El fondo tras una puerta

<audio controls src="../audio/musica_fondo_puerta.mp3"></audio>

## El fondo con el suceso

<audio controls src="../audio/musica_fondo_suceso.mp3"></audio>

## El suceso vencido

<audio controls src="../audio/musica_suceso.mp3"></audio>

## El final

<audio controls src="../audio/musica_final.mp3"></audio>
