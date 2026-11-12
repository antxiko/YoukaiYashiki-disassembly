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

## Fixed in the listing

The comment on `puntos_suma` said it gave a life every 100,000 points and another at 50,000: it had been copied from
another Casio cartridge with the same routine. Running it here, from 49,900 to 50,000 the lives do not change, and the
routine calls nothing but the digits and the high score: **this game gives no lives for points**.
