# Youkai Yashiki - commented disassembly

*(También [en castellano](README.es.md).)*

The commented disassembly of **Youkai Yashiki** (妖怪屋敷, "the yōkai mansion"; Casio, 1986) for the MSX: a 32 KB cartridge with its header at 0x4000.

- **100%** of the binary explained: 14,711 bytes of code and 18,057 of named data, not one byte unassigned.
- **40.5%** of the listing commented, 878 routines and labels, none below 10% of comments.
- The listing reassembles into the original ROM **byte for byte**.
- The title comes from running the ROM, checked against openMSX point by point; the CASIO intro, the demo, the game, GAME OVER and the five places, played in GIF in openMSX; the ten tunes, from its own sound engine, the five that play in the recordings identical to openMSX frame by frame.
- Five keys held at the title fill the hero's endurance for the whole game, and the demo reads its controls from the start of the BIOS.

The site: <https://antxiko.github.io/YoukaiYashiki-disassembly/>
(in Spanish: <https://antxiko.github.io/YoukaiYashiki-disassembly/es/>).

## Reproducing it

The ROM image is not distributed. Put yours in the root as `youkai.rom` (the original GoodMSX `[!]` dump, sha1 `15345c87...`) and run `make`. The details, in [UNDER THE HOOD](docs/UNDER-THE-HOOD.md).

## Legal

The game belongs to Casio and its rights holders. The licence in `LICENSE` covers only the tools, the comments, the analysis and the documentation here. See [LEGAL-NOTICE.md](LEGAL-NOTICE.md).
