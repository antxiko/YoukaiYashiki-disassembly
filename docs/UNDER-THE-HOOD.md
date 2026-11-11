# Under the hood

## Rebuilding the ROM

`make verify` assembles `src/youkai.asm` with pasmo and out comes the 32 KB ROM **byte for byte**. `make sanity`
checks what reassembly does not cover: that no byte declared as data is read as code, that no entry point falls in
data and that all 32,768 bytes are explained. `make test` runs the tests. The ROM is not in the repository: put it in
the root as `youkai.rom` (the GoodMSX dump, `[!]`, sha1 `15345c87...`; the 1.1 versions by theNestruo and Yazio are
modifications and are not this one).

| | bytes |
|---|---|
| traced code | 14,711 |
| named data | 18,057 |
| unexplained | 0 |

The listing has 2,671 comments in 6,590 instructions (40.5%), 878 routines and labels, none under 10% commented, and
no called routine without a name.

## The cartridge

32 KB at 0x4000-0xBFFF, with the header at 0x4000. INIT (0x4010) also puts the cartridge in page 2 and jumps to
0x8000, which goes back to the start-up (0x7E80). The data comes first: the maps of the places (0x4038), the 74
screens (0x41AC) and their y&#333;kai and objects (0x4EBE), the pieces and drawings (0x54C7), the texts (0x5695), the
sprites (0x5800) and the tiles with their colours (0x6000-0x7E7F). The code goes from 0x7E80 to 0xB757, with some
tables in between; after it, the sound (0xB700-0xBFFF).

## The BIOS it uses

RSLREG and ENASLT for the slot; SETGRP, CHGCLR, WRTVDP, DISSCR and ENASCR; FILVRM, LDIRVM, WRTVRM and RDVRM; GTSTCK
and GTTRIG for the controls and SNSMAT for the space bar, GRAPH, STOP, F1 and the five keys; WRTPSG for the sound. It
reads the BIOS font (0x1D3F) and, in the demo, its first bytes as controls.

## The interrupt and the loop

The start-up puts a jump to 0xB475 in the H.TIMI hook. The interrupt does the requested silence, runs the sound,
counts frames and reads F1, STOP, the buttons and the joystick. The game runs in the **loop** (`bucle`, 0x80B1):
once per frame, the background sound and, if there is no pause, the screen's y&#333;kai and objects, the hero (hit,
the fall, the joystick, the jump and the weapon), the ladders, the points, the y&#333;kai, the event, the objects and
the blinking (`bucle_juego`, 0x80EE).

**The screens.** Each screen is built in RAM (0xE700, 32 x 20 tiles) from its description (`pantalla_monta`,
0x9257) and copied to VRAM from row 2. To change screen, the old one and the new one are put side by side (0xE980 and
0xEC00) and the window slides. The hero looks at the tiles under his feet, at his body and at the sides (0x8C93 and
following): below 0x34, or from 0x3C to 0x7F, they do not hold him.

## How it was done

The trace follows the code from INIT, the interrupt and the two jump tables (the objects, 0x947B, and the
y&#333;kai, 0xA1E8), declared in `src/youkai.entries`. The rest was **measured in openMSX**
(`tools/omsx_cobertura.tcl`) on a Philips VG 8020: nothing that ran was left out of the trace. Part of the comments
come from other Casio games already done (`comun/casio/porta.py`, on identical stretches; the sound engine too) and others were set by rule where the meaning is certain (`work/reglas.py`: IX is always the
hero, 0xE300), and checked.

The recordings for the site (`tools/guiones/*.tcl`, recorded with `tools/lanza_graba.ps1` on C-BIOS) log, on every
frame, the VDP registers, the RAM from 0xE000, the PSG and the VRAM that changed. `tools/pantallas.py` runs the
title with `tools/bios.py` and checks it against the recording (**0 different points**), `tools/gifs.py` makes the
GIFs and `tools/musica.py` runs the sound engine.

## The RAM

| | |
|---|---|
| 0xE000 | playing |
| 0xE009 | the rounds |
| 0xE00A / 0xE0A0 | the place / the one before |
| 0xE023 | the five title keys |
| 0xE028 / 0xE029 | the demo / its list of controls |
| 0xE047 | the ending set going |
| 0xE0A1 / 0xE0A2 / 0xE0A3 | the column and the row on the map / the screen |
| 0xE0A8 / 0xE0A9 | the lives / the endurance (in halves) |
| 0xE180 | the joystick |
| 0xE183 / 0xE186 | the fall / the place over |
| 0xE198 | the side the screen is left by |
| 0xE1B0 / 0xE1B2 | the event / its blows |
| 0xE1B3 / 0xE1B5 / 0xE1B7 | F1 / STOP / the pause |
| 0xE280-0xE2D5 | the sound |
| 0xE300 | the hero (and the weapon, 0xE320) |
| 0xE340 | the twelve y&#333;kai |
| 0xE400 | the screen's objects |
| 0xE700 | the screen (32 x 20) |
