# Secrets and bugs

What was searched for in the code and what was found. A bug only goes here if it has been checked: by running the
game's own routine (`tools/bios.py`) or against the openMSX recordings.

## Secrets

Told in [Curiosities](CURIOSITIES.html):

- **8, 9, -, ^ and yen together** when the CASIO intro ends (0x7F01): full stamina, and hits do not take it.
  The GIFs of the places were recorded with them.
- **F1** knocks the hero down; with no stamina, it is straight GAME OVER.
- **The demo plays the BIOS**: its controls are the bytes from 0x0000, so it changes with the computer.

Apart from those keys, the controls are read in the interrupt: the stick from the cursor keys and joystick 1, the
joystick 1 buttons, the space bar and GRAPH.

## Bug: past 9,999,990 points, the high score to zero

When the score goes past 999,999 inside (9,999,990 on screen, with the fixed 0), `puntos_suma` (0xB3AF) copies into the
high score (0xE094) the score **after it has wrapped** (0xB3D9-0xB3E8). Running the game's addition here:

| score (on screen) | high score | + | after: score | high score |
|---|---|---|---|---|
| 123,450 | 100,000 | 100 | 123,550 | 123,550 |
| 9,999,900 | 9,999,900 | 100 | **0** | **0** |
| 9,999,500 | 9,999,500 | 900 | **400** | **400** |

## Bug: the cursor keys and the joystick at once

`palanca` (0xB505) joins the cursor keys and joystick 1 with an `or` (0xB515) of their direction numbers. With both at
once, running it here, right and down give **left** (7), and up-right and down-right give **down-left** (6).

## Bug: the blows on the event of place 1 give 10, 20, 30... points

When the weapon hits a y&#333;kai, the code of its type loads the points into A and jumps to `puntos_suma`. The bolts of
the event of place 1 (type 0x10) do `ld a,010h` (0xA3FC, 100 points, like the 0x11 and the 0x12) and right after it
`ld a,(0e1b2h)` (0xA3FE) to count the blow: the 0x10 is lost, and what is added is **the number of blows**. Recorded in
openMSX (the GIF of that event in [The places](THE-PLACES.html)), the score after each blow: 10, 30, 60, 100, 150,
210, 280, 360, 450 and **550**, where it would be 1,000. The event of place 4 does it the other way round
(`ld a,(0e1b2h)` ... `ld a,020h`, 0xAB63-0xAB6A) and gives its 200 per blow.

## Bug: one frame with the hero's drawing

The white ghost (types 0x0C, 0x0E, 0x0F and 0x14, 0xA853) that does not come in from an edge gets its colour on the
first frame (white, 0xA8A6) but not its drawing, which arrives on the next one: for one frame its sprite shows the
drawing it had, 0x00 after `enemigos_borra`, **the hero seen from behind, in white**. In the recordings of this site
it happens 15 times.

## Fixed in the listing

The comment on `puntos_suma` said it gave a life every 100,000 points and another at 50,000: it had been copied from
another Casio cartridge with the same routine. Running it here, from 49,900 to 50,000 the lives do not change, and the
routine calls nothing but the digits and the high score: **this game gives no lives for points**.
