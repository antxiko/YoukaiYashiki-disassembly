# Curiosities

## Five keys at once

If, when the CASIO intro ends, the keys **8, 9, -, ^ and yen** are all held (the whole of keyboard row 1 except its
three high bits) and 0 is not, the game sets 0xE023 = 1 (0x7F01): the game starts with **full endurance** and blows
do not take it away (`golpe`, 0xB146, returns doing nothing). The GIFs of the places are recorded with them.

## F1

F1 knocks the hero down. With no endurance, it first sets the lives to 1: the fall is straight GAME OVER
(`f1_atiende`, 0x8129). With endurance, the fall leads to CONTINUE PUSH TRIG1 / END PUSH TRIG2.

## The demo plays the BIOS

The demo's controls are read from a list, one byte every 16 frames, that starts at **0x0000**: the beginning of the
MSX BIOS. There is no list made for it, and with another BIOS the demo plays out differently.

## The start-up in page 1

INIT (0x4010) puts the cartridge in page 2 and jumps to 0x8000, which is a `jp` back to 0x7E80: the start-up is at the
end of page 1, behind the graphics.

## Leftovers

- **Dead code**: 47 bytes at 0x93D1, 23 at 0xA9D6, 19 at 0xAFA3 (a routine that removes an object that goes off the
  screen) and a `ret` at 0xA4C2; no jump reaches them and the coverage measured in openMSX does not go through them.
- **The 23 bytes at 0xA9D6** sit in the middle of the white ghost's jump (0xA989-0xA9D3) and are another way down
  for that jump: Y two more per frame (`inc (iy+0)` twice), the count (+0x0E) one less and, when it ends, state 1 and
  +0x0D to zero, like the way down that is used (0xA9B2), which goes through the table at 0x8F91. It looks like the way
  down from before the table. It does not touch the drawing.
- **Drawing 0x90, unused**: of the 64 in the sprite table, it is the only one no instruction puts in a sprite
  ([The sprites](THE-SPRITES.html)). Néstor Sancho found it; his
  [patch](https://github.com/theNestruo/msx-youkaiyashiki-patch) uses those 23 bytes to show it in the white ghost's
  jump; whether the game meant it for that cannot be told from the code.
- **Filler**: 12 bytes of 0xF0 at 0x7FF4, 30 bytes of FB 00 at 0xB6E2 and the rest of the scoreboard after GAME OVER
  (0x571D).
