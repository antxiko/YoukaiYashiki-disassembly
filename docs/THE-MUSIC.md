# The music

The tunes, in three voices. They are not hand-made recordings: `tools/musica.py` **runs the ROM's own sound engine**
with `tools/z80run.py` -the sound routine (`sonido`, 0xB77C), frame by frame, with the number the game writes- and
logs what it writes to the PSG through the BIOS (WRTPSG).

**Checked against openMSX**, the five that play in the recordings (`tools/guiones/`: the demo, the pilot's game, the
one with the title keys and the forced one): the intro, a place starting, the fall, GAME OVER and the game's
background, **0 different** in every frame looked at. The other five come from running the engine with their number
and could not be checked: they do not play in any recording.

## The engine

It is the one other Casio games use, at almost the same address: it serves three
**requests** -a tune (0xE2BE), a channel A effect (0xE2C0) and a B and C one (0xE2C2)- and the lower number wins. The
tables: eight tunes at 0xB700 (number 0, nothing), eight channel A effects at 0xB730, six B and C ones at 0xB740 and
fourteen durations at 0xBA2D. During the game the background is a B and C **effect** that the loop asks for on every
pass (`sonido_fondo`, 0x81AD).

| | who asks for it | length | checked |
|---|---|---:|---|
| the CASIO intro | 0xB5EA | 1.1 s | yes |
| a place starts | 0x808D | 4.3 s | yes |
| the game's background | the loop (effect 5) | 14.9 s, asked for again | yes |
| the fall | 0xAE2B | 0.8 s | yes |
| GAME OVER | 0xAF35 | 2.7 s | yes |
| CONTINUE / END | 0xAEB9 | 5.2 s | no |
| the background after a door | the loop (effect 4) | 17.1 s | no |
| the background with the event | the loop (effect 2) | 8.6 s | no |
| the event beaten | 0x8393 and 0x84D9 | 10.7 s | no |
| the ending | 0xA82B | 8.6 s | no |

## The CASIO intro

<audio controls src="audio/musica_casio.mp3"></audio>

## A place starts

<audio controls src="audio/musica_sala.mp3"></audio>

## The game's background

<audio controls src="audio/musica_fondo.mp3"></audio>

## The fall

<audio controls src="audio/musica_caida.mp3"></audio>

## GAME OVER

<audio controls src="audio/musica_game_over.mp3"></audio>

## CONTINUE / END

<audio controls src="audio/musica_continuar.mp3"></audio>

## The background after a door

<audio controls src="audio/musica_fondo_puerta.mp3"></audio>

## The background with the event

<audio controls src="audio/musica_fondo_suceso.mp3"></audio>

## The event beaten

<audio controls src="audio/musica_suceso.mp3"></audio>

## The ending

<audio controls src="audio/musica_final.mp3"></audio>
