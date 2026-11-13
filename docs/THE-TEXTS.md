# The texts

Latin letters and digits are those of the BIOS font from "0" on (tile = letter - 0x30: 0x11 is A, 0x10 the space),
which the start-up copies to VRAM (`letras_pon`, 0xB2F0). The name and the drawings are the cartridge's own tiles.

| address | text | |
|---|---|---|
| 0x5695 | 妖怪屋敷 (4 rows of 16 tiles) | the name: "the y&#333;kai mansion" |
| 0x56D5 | CASIO (tiles 0x8A-0x8F) | |
| 0x56DB | PUSH TRIG:1 OR SPACE | |
| 0x56EF | COPYRIGHT 1986 &copy; CASIO | |
| 0x5705 | HISCORE:0000000 | SCORE (0x5707) is its end |
| 0x5714 | GAME OVER | |
| 0xAF4D | CONTINUE PUSH TRIG1 / END      PUSH TRIG2 | |
| 0xA839 / 0xA846 | めでたし！ (13 + 13 tiles: the top and bottom halves, with the cartridge's own kana) | the ending, twice: "and they lived happily ever after", the closing line of Japanese tales (see [The places](THE-PLACES.html)) |
