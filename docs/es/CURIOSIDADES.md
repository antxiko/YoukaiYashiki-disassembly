# Curiosidades

## Cinco teclas a la vez

Si al acabar la presentaci&oacute;n de CASIO est&aacute;n pulsadas a la vez las teclas **8, 9, -, ^ y la del yen**
(toda la fila 1 del teclado menos sus tres bits altos) y no el 0, el juego pone 0xE023 = 1 (0x7F01): la partida
empieza con el **aguante lleno** y los golpes no lo quitan (`golpe`, 0xB146, vuelve sin hacer nada). Con ellas est&aacute;n
grabados los GIF de los lugares.

## F1

F1 derriba al protagonista. Sin aguante, antes pone las vidas a 1: la ca&iacute;da es GAME OVER directo
(`f1_atiende`, 0x8129). Con aguante, la ca&iacute;da lleva a CONTINUE PUSH TRIG1 / END PUSH TRIG2.

## La demostraci&oacute;n juega la BIOS

Los mandos de la demostraci&oacute;n se leen de una lista, un byte cada 16 cuadros, que empieza en **0x0000**: el
principio de la BIOS del MSX. No hay lista hecha a prop&oacute;sito, y con otra BIOS la demostraci&oacute;n se juega
de otra manera.

## El arranque en la p&aacute;gina 1

INIT (0x4010) pone el cartucho en la p&aacute;gina 2 y salta a 0x8000, que es un `jp` de vuelta a 0x7E80: el
arranque est&aacute; al final de la p&aacute;gina 1, detr&aacute;s de los gr&aacute;ficos.

## Sobrantes

- **C&oacute;digo muerto**: 47 bytes en 0x93D1, 23 en 0xA9D6, 19 en 0xAFA3 (una rutina que saca un objeto que se sale de
  la pantalla) y un `ret` en 0xA4C2; ning&uacute;n salto llega y la medida de cobertura en openMSX no pasa.
- **Los 23 bytes de 0xA9D6** est&aacute;n en medio del salto del fantasma blanco (0xA989-0xA9D3) y son otra bajada
  del mismo salto: la Y dos m&aacute;s por cuadro (`inc (iy+0)` dos veces), la cuenta (+0x0E) una menos y, acabada, el
  estado 1 y +0x0D a cero, como la bajada que s&iacute; se usa (0xA9B2), que va por la tabla 0x8F91. Parece la bajada
  de antes de la tabla. No toca el dibujo.
- **El dibujo 0x90, sin uso**: de los 64 de la tabla de sprites, es el &uacute;nico que ninguna instrucci&oacute;n
  pone en un sprite ([Los sprites](LOS-SPRITES.html)). Lo encontr&oacute; N&eacute;stor Sancho, que en su
  [parche](https://github.com/theNestruo/msx-youkaiyashiki-patch) usa esos 23 bytes para ponerlo en el salto del
  fantasma blanco; que el juego lo pensara para eso no se puede saber por el c&oacute;digo.
- **Relleno**: 12 bytes 0xF0 en 0x7FF4, 30 bytes FB 00 en 0xB6E2 y el resto del marcador tras GAME OVER (0x571D).
