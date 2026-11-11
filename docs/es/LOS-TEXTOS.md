# Los textos

Las letras latinas y las cifras son las de la fuente de la BIOS desde el "0" (la casilla = la letra - 0x30: 0x11 es
la A, 0x10 el espacio), que el arranque copia a la VRAM (`letras_pon`, 0xB2F0). El nombre y los dibujos son casillas
propias del cartucho.

| direcci&oacute;n | texto | |
|---|---|---|
| 0x5695 | 妖怪屋敷 (4 filas de 16 casillas) | el nombre: "la mansi&oacute;n de los y&#333;kai" |
| 0x56D5 | CASIO (casillas 0x8A-0x8F) | |
| 0x56DB | PUSH TRIG:1 OR SPACE | |
| 0x56EF | COPYRIGHT 1986 &copy; CASIO | |
| 0x5705 | HISCORE:0000000 | SCORE (0x5707) es su final |
| 0x5714 | GAME OVER | |
| 0xAF4D | CONTINUE PUSH TRIG1 / END      PUSH TRIG2 | |
| 0xA839 / 0xA846 | el texto del final, 13 + 13 casillas | con casillas propias y kana; no se ha visto en las grabaciones |
