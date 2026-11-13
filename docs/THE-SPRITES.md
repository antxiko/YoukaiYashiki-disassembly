# The sprites

Everything on this page is **put together from the ROM tables** with `tools/hojas.py`: the drawings are the 0x800
bytes at 0x5800 that `sprites_dibujos` (0xB36D) puts as they are at 0x3800, and every figure is built with the
drawings and colours the code gives it. Each thing is made of 16-byte sprites from 0xE300 (the first 4, its
attributes): the hero at 0xE300 and 0xE310, his weapon at 0xE320 and the twelve enemies from 0xE340 (+4 the type, by
the table at 0xA1E8). None of these images is a screenshot.

**Checked against openMSX** on the recordings of this site:

- the sprite drawing table (VRAM 0x3800-0x3FFF) is **identical** to the game's on 60,887 frames (6 more catch the
  copy halfway);
- the hero's two sprites, in the same place with the drawing and the drawing + 0x60 in light yellow, on **48,170
  frames, 0 different** (172 more still at zero);
- the weapon, 0x28 or 0x2C, on **24,243 frames, 0 different**;
- the y&#333;kai, **type by type**: each one carries a drawing and a colour that the code of its type gives it, on
  **35,966 frames, 0 different**, of 14 types (the others are not in the recordings).

## The hero and his weapon

Two sprites in the same place: the drawing in magenta and the drawing + 0x60 in light yellow (`sala_empieza` 0x806D,
`caida_para` 0x87A3). Standing 0x0C or 0x14 by his side (0x880D), and walking 0x08 to 0x1C. Then the weapon
(`ataque_sale`, 0xE320): 0x28 to the right and 0x2C to the left, which goes out 4 dots per frame:

![The hero and his weapon](imagenes/protagonista.png)

## The y&#333;kai, type by type

Each y&#333;kai carries its type at +4 and the table at 0xA1E8 sends it to its routine: 23 types, 0x00 to 0x16. Here
each one with the drawings and colours its code gives it, put together from the ROM (`TIPOS` in `tools/hojas.py`).
The ones that wait (`enemigo_espera`, 0xA216) first show 0x38/0x3C in white, and once beaten they all stay a moment
with 0x38/0x3C in their colour (0xA22C): that is not repeated in the sheet.

![The y&#333;kai, type by type](imagenes/enemigos.png)

| type | routine | what it does | entries in the screens (0x4EBE) |
|---|---|---|---|
| 0x01 | 0xA278 | waits, then hops from side to side (the heights at 0xA434), 0x30/0x34 every 8 frames, cyan and white every 2; every five beaten, the endurance fills up | 22, on 12 screens |
| 0x02 | 0xA278 | the same in white; beaten, the endurance goes up a half | 11 |
| 0x03 | 0xA444 | 0x4C/0x50 in light blue: every so often, a step of 8 dots to one side if the tiles let it | 23 |
| 0x04 | 0xA444 | the same in light red; hit, it **splits in two**, side by side, both of type 0x03 in dark blue (0xA394) | 18 |
| 0x05 | 0xA4C3 | two sprites one above the other (0x88/0x8C and 0x9C/0xA0, dark red and dark yellow) that jump to the sides (0x8FA2); five blows | 3 |
| 0x07 | 0xA5EB | 0x54/0x58 in white, walking and jumping (0x8F91); three blows, and after each one it flashes in cyan | 5 |
| 0x08 | 0xA5EB | 0x94/0x98 in light red; after the first blow, light green; two blows and the endurance fills up. Only in the sixth place | 5 |
| 0x09 | 0xA6B7 | waits, then **flies** around the screen at random (Y 0x10-0xA0), 0x44/0x48 in dark blue | 41, on 21 screens |
| 0x0B | 0xA778 | **the girl of the ending** (see [The places](THE-PLACES.html)): two sprites in the same place, 0xE8/0xEC and 0xF0/0xF4 walking, 0xF8/0xFC standing | 1, screen 0x3C |
| 0x0C | 0xA853 | the white ghost, 0xD4-0xE0: comes in from an edge or appears, walks and throws a 0x0D; with the round (0xE009) at 1 or in place 4 sometimes light blue, from round 2 in light red | 48, on 33 screens |
| 0x0D | 0xAA49 | what the 0x0C throws: 0xA4 in light red, 3 dots per frame until it leaves the screen | (the 0x0C puts it) |
| 0x10 | 0xABB8 | **event of place 1**: from the skull's eyes (X 0x6C or 0xAA, Y 0x64), first with the empty drawing 0xE4, then a bolt, 0xB8 or 0xA8 by the hero's side, light yellow; each blow counts for the event | (the event) |
| 0x11 | 0xACC6 | **event of place 2**: 0x38/0x3C in light blue | (the event) |
| 0x12 | 0xABB8 | **event of place 3**: an eye, 0x40 in light red, from the same spots as the 0x10 | (the event) |
| 0x13 | 0xAD6F | **event of place 3**: the pupil of the big eye (Y 0x76, X 0x90), 0x40, going 16 dots to each side; black, and each blow changes its colour (blows x 2 + 1); at five, the event is beaten | (the event) |
| 0x15, 0x16 | 0xAA9A | **event of place 4**: a flame (0xAC) over a ghost (0xB0, white), the 0x15 on the right (X 0xD8) in light yellow or light red and the 0x16 on the left (X 0x28) in cyan or light blue; they appear at the top for a moment, at random; hit, the border flashes and it falls | (the event) |
| 0x0E, 0x0F, 0x14 | 0xA853 | the same routine as the 0x0C; no screen uses them | 0 |
| 0x00, 0x06, 0x0A | &mdash; | nothing: the 0x00 does not move (`enemigos` skips it) and the routines of 0x06 (0xA5EA) and 0x0A (0xA777) are a bare `ret`; their sprite has no drawing or colour, so **nothing shows**. Three screens (0x10, 0x23 and 0x40) carry a 0x06 | 41 + 3 |

The hero walking and three y&#333;kai (0x01, 0x03 and 0x09) with their two drawings, at the game's pace:

![The hero and the ghosts, frame by frame](imagenes/andar_cuadros.gif)

## The pause

STOP stops the game (`pausa`, 0x8145): it saves the sprites (at 0xE1C0) and turns four into a picture where the hero
was: the face 0xD0 (magenta) and the steam 0xC8 (light yellow) 16 dots above, and 0xC0 and 0xC4 (colour 10) at his
height, one on each side; it looks like the hero in a tub. The steam takes turns with 0xCC every 8 frames (0x80E1).
Another STOP brings the old ones back. Recorded in openMSX (`tools/guiones/pausa.tcl`), nothing forced; the GIF has
**only the four sprites** of the recording, without the screen:

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
| 0x30, 0x34 | the hopping ghosts, types 0x01 (cyan and white) and 0x02 (white) | 0xA32A |
| 0x38, 0x3C | the y&#333;kai while they wait and once beaten; the type 0x11 (event of place 2) | 0xA222 |
| 0x40 | the eyes of the event of place 3: the 0x12 (light red) and the pupil 0x13 (black, then a colour per blow) | 0xABF9 |
| 0x44, 0x48 | the type 0x09, flying, in dark blue | 0xA76D |
| 0x4C, 0x50 | the types 0x03 (light blue) and 0x04 (light red), and the two halves of a 0x04 (dark blue) | 0xA45B, 0xA4BC |
| 0x54, 0x58 | the type 0x07, walking | 0xA601, 0xA68C |
| 0x88, 0x8C, 0x9C, 0xA0 | the type 0x05, two sprites one above the other, dark red and dark yellow | 0xA4E3, 0xA4E7, 0xA593, 0xA597 |
| 0x94, 0x98 | the type 0x08, walking, in light red (the sixth place) | 0xA606, 0xA68C |
| 0xA4 | what the white ghost throws (type 0x0D), in light red | 0xA917 |
| 0xA8 | the bolt of the event of place 1 (type 0x10) with the hero on the right | 0xAC90 |
| 0xAC, 0xB0 | the event of place 4 (types 0x15 and 0x16: flame and ghost); and the two that go up when an event is beaten (0x83AD) | 0xAB20, 0xAB24 |
| 0xB4 | with 0xB0, the one that blinks every 8 frames (`suceso_parpadea`) | 0x831F |
| 0xB8 | the bolt of the event of place 1 (type 0x10) with the hero on the left | 0xAC18 |
| 0xC0, 0xC4, 0xC8, 0xCC, 0xD0 | the pause: the hero in a tub (above) | 0x816F, 0x8173, 0x816B, 0x80E9, 0x8167 |
| 0xD4, 0xD8, 0xDC, 0xE0 | the white ghost (type 0x0C), also when it jumps | 0xA9F7 |
| 0xE4 | **empty**, nothing shows: it is given to an enemy (0xABE9) and to the hero's four sprites (0x95FC) | 0xABE9 |
| 0xE8, 0xEC, 0xF0, 0xF4 | **the girl of the ending** (type 0x0B) walking: two sprites in the same place, light red and light yellow | 0xA7D0, 0xA7D5 |
| 0xF8, 0xFC | the girl standing, when she appears and when she meets the hero | 0xA7A3, 0xA7A7 |
| 0x90 | **unused**: no code sets it | — |
