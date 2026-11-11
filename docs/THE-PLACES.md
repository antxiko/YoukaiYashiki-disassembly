# The places

Five places (0xE00A, 0 to 4), each with its **map**: rows of ten cells with the number of the screen in each spot
(0x4038). In all, **74 screens** of 32 x 20 tiles, each with its description (0x41AC: pieces, fills, ladders and
drawings) and its list of y&#333;kai and objects (0x4EBE). One goes from one to another by the edges -the new one
slides in from that side-, by the ladders and by the doors, which lead to another place (0xA0D7: the place, the
column and the row of the destination).

The y&#333;kai (0xE340, up to twelve) are of 23 types: some wait and jump, others walk, fly or fall; the objects
(0xE400) are what can be picked up, doors and decorations.

With the five keys on the title (full endurance and blows do not take it, see [Curiosities](CURIOSITIES.html)), the
pilot against the y&#333;kai of the graveyard:

![The graveyard, with the title keys](imagenes/fantasmas.gif)

## The events

Each place has its **event** (`sala_suceso`, 0x8252): a large drawing that appears on a given screen (the one at
0x852E for each place) with its y&#333;kai, and that has to be beaten:

| place | the event |
|---|---|
| 0 | the drawing at 0x7700; six blows of the weapon on its spot |
| 1 | the one at 0x7780 and two y&#333;kai of type 0x10; ten blows |
| 2 | the one at 0x7740 and two of type 0x11; reaching its spot |
| 3 | the one at 0x77C0 and three y&#333;kai (0x12 and 0x13); five blows |
| 4 | two y&#333;kai (0x15 and 0x16); four blows: the ending is set going (0xE047) |

Once beaten, tune 7 plays, two sprites go up and the place is over: the endurance fills up and the next one starts;
after 4, place 0 again with one more round (0xE009).

**The ending**: with the mark of place 4 and certain objects picked up (0xE048, 0xE049 and 0xE04A = 2), a character
appears (the y&#333;kai of type 11, 0xA778) and walks to the right; on reaching it, a text comes up (0xA839 and
0xA846) and tune 3. No recording got that far: this comes from the code.

## The places, forced

The GIFs of places 1 to 4 are **forced**: the place put by hand (0xE00A) and F1, so that the hero falls and the place
starts again, now the new one. The pilot plays with the title keys.

![Place 1 (forced)](imagenes/sala_1.gif)

![Place 2 (forced)](imagenes/sala_2.gif)

![Place 3 (forced)](imagenes/sala_3.gif)

![Place 4 (forced)](imagenes/sala_4.gif)
