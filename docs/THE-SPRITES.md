# The sprites

Everything on this page is **put together from the ROM tables** with `tools/hojas.py`: the drawings are the 0x800
bytes at 0x5800 that `sprites_dibujos` (0xB36D) puts as they are at 0x3800, and every figure is built with the
drawings and colours the code gives it. Each thing is made of 16-byte sprites from 0xE300 (the first 4, its
attributes): the hero at 0xE300 and 0xE310, his weapon at 0xE320 and the twelve enemies from 0xE340 (+4 the type, by
the table at 0xA1E8). None of these images is a screenshot.

**Checked against openMSX** on the recordings of this site:

- the sprite drawing table (VRAM 0x3800-0x3FFF) is **identical** to the game's on 35,858 frames (4 more catch the
  copy halfway);
- the hero's two sprites, in the same place with the drawing and the drawing + 0x60 in light yellow, on **26,999
  frames, 0 different** (123 more still at zero);
- the weapon, 0x28 or 0x2C, on **13,221 frames, 0 different**;
- the enemies carry one of the drawings (or the next one, + 4) and one of the colours their code gives them on
  14,615 frames; **11 unexplained**. The enemy routines are not named in the listing, so this check does not go type
  by type.

## The hero and his weapon

Two sprites in the same place: the drawing in magenta and the drawing + 0x60 in light yellow (`sala_empieza` 0x806D,
`caida_para` 0x87A3). Standing 0x0C or 0x14 by his side (0x880D), and walking 0x08 to 0x1C. Then the weapon
(`ataque_sale`, 0xE320): 0x28 to the right and 0x2C to the left, which goes out 4 dots per frame:

![The hero and his weapon](imagenes/protagonista.png)

## The ghosts

The drawings and colours the enemy routines (0xA216-0xAD85) put in their sprite, each with the next one (+ 4) when
they change it: 0x38 / 0x3C in white while they wait (0xA216), 0x30 in cyan (0xAAE8), 0x4C in light blue or light red
(0xA451, 0xA457), 0x88 and 0x9C in dark red (0xA4E3), 0xF8 in light red (0xA7A3), 0xAC in light blue (0xAB20), 0xE4
in light yellow (0xABE9: it is an **empty** drawing, nothing shows), 0x40 in light red (0xABF9) or black (0xAD81),
0xB8 in dark blue (0xAC18), 0xA8 in light red (0xAC90), 0xD4-0xE0 in white (0xA884), 0x94 in light red (0xA60A), 0x44
in dark blue (0xA770), 0xE8 and 0xF0 in light red (0xA7AB) and 0xA4 in light red, the second sprite of the 0xD4 one
(0xA91B); at the end, the two that appear when a room is beaten (`suceso_vencido`: 0xAC and 0xB0):

![The drawings of the ghosts](imagenes/enemigos.png)

The hero walking and some ghosts with their two drawings, at the game's pace:

![The hero and the ghosts, frame by frame](imagenes/andar_cuadros.gif)

## The pause

STOP stops the game (`pausa`, 0x8145): it saves the sprites (at 0xE1C0) and puts four in their place, in colour 10:
0xD0 and 0xC8 above the hero, 0xC0 and 0xC4 at his height, one on each side; on top, 0xC8 and 0xCC take turns every 8
frames (0x80E1). Another STOP brings the old ones back. Recorded in openMSX (`tools/guiones/pausa.tcl`), nothing
forced:

![The pause](imagenes/pausa.gif)

## The 64 drawings

The whole drawing table (the 0x800 bytes at 0x5800), in order, with its number. **Some code sets every one of them
except one, 0x90** (framed in red): no instruction in the cartridge writes it into a sprite. 0xE4 is empty and is used
to hide.

![The 64 sprite drawings](imagenes/dibujos.png)

| drawings | what it is | where it is set |
|---|---|---|
| 0x00, 0x04, 0x60, 0x64 | the hero from behind, going up or down (the drawing by his Y) | 0x8A04, 0x8A09 |
| 0x08, 0x0C, 0x10, 0x14, 0x18, 0x1C, 0x68, 0x6C, 0x70, 0x74, 0x78, 0x7C | the hero standing, walking and jumping (and the + 0x60, his second colour) | 0x8EF3, 0x880D, 0x8A9F, 0x8819, 0x8C2F, 0x8EFC, 0x8EF7, 0x8811, 0x8AA7, 0x881D, 0x8C37, 0x8F00 |
| 0x20, 0x80, 0x5C, 0xBC | the hero losing a life, one pair and the other every 4 frames | 0xAE50, 0xAE54, 0xAE5A, 0xAE5E |
| 0x24, 0x84 | the hero hit | 0x8BFC, 0x8C00 |
| 0x28, 0x2C | the weapon, to the right and to the left | 0x860B, 0x8615 |
| 0x30, 0x34 | a cyan ghost | 0xA32A |
| 0x38, 0x3C | the ghosts while they wait | 0xA222 |
| 0x40 | a ghost in light red or black | 0xABF9 |
| 0x44, 0x48 | a dark blue ghost | 0xA76D |
| 0x4C, 0x50 | a ghost in light blue or light red | 0xA45B, 0xA4BC |
| 0x54, 0x58 | the type 7 enemy walking | 0xA601, 0xA68C |
| 0x88, 0x8C, 0x9C, 0xA0 | a two-sprite enemy, in dark red | 0xA4E3, 0xA4E7, 0xA593, 0xA597 |
| 0x94, 0x98 | the other enemies of that routine, walking, in light red | 0xA606, 0xA68C |
| 0xA4 | the second sprite of the 0xD4 one, in light red | 0xA917 |
| 0xA8 | a light red ghost | 0xAC90 |
| 0xAC, 0xB0 | a two-sprite enemy, in light blue and white; and the two that appear when a room is beaten (0x83AD) | 0xAB20, 0xAB24 |
| 0xB4 | with 0xB0, the one that blinks every 8 frames (`suceso_parpadea`) | 0x831F |
| 0xB8 | a dark blue ghost | 0xAC18 |
| 0xC0, 0xC4, 0xC8, 0xCC, 0xD0 | the pause frame (above) | 0x816F, 0x8173, 0x816B, 0x80E9, 0x8167 |
| 0xD4, 0xD8, 0xDC, 0xE0 | the white ghost of 0xA884, also when it jumps | 0xA9F7 |
| 0xE4 | **empty**, nothing shows: it is given to an enemy (0xABE9) and to the hero's four sprites (0x95FC) | 0xABE9 |
| 0xE8, 0xEC, 0xF0, 0xF4 | a two-sprite enemy, in light red and light yellow | 0xA7D0, 0xA7D5 |
| 0xF8, 0xFC | the same enemy, with two other drawings | 0xA7A3, 0xA7A7 |
| 0x90 | **unused**: no code sets it | — |
