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

## The plans

All six places, whole, each screen in its spot on the plan (0x4038), at half size. They are **drawn by running the
ROM** (`tools/mapas.py`): each screen is built by `pantalla_monta` (0x9257) in RAM, over the tiles of a recorded frame
of its place; the tiles are the same everywhere and only the colour of 0x41-0x47 changes (`sala_colores`, 0x8206). No
scoreboard, sprites or the objects that are drawn separately.

The plan holds **a sixth place** (number 5, screens 0x45-0x49), reached by doors 28 to 32 of the table at 0xA0D7, that
no recording has visited: it is drawn with the tiles of place 4, which is the colour `sala_colores` gives it. And four
screens, 0x13 to 0x16, are on no plan at all.

Check: of the 69 screens on the plans, the recordings only go through 7; 3 come out **identical** to the recorded name
table and the other four with 4 to 31 differing tiles out of 640 (the objects). On 4,012 of 4,050 recorded frames (one in
seven), the screen `pantalla_monta` builds here is the same one the game holds in RAM; of the 38 that are not, 29 are
on the first screen, and they have not been looked at one by one.

![Place 0](imagenes/plano_0.png)

![Place 1](imagenes/plano_1.png)

![Place 2](imagenes/plano_2.png)

![Place 3](imagenes/plano_3.png)

![Place 4](imagenes/plano_4.png)

![Place 5, the one never recorded](imagenes/plano_5.png)

## The events (the bosses)

Each place has its **event** (`sala_suceso`, 0x8252), its boss. It is on the screen at 0x852E for the place (0x09,
0x12, 0x1E, 0x2F and 0x44), and that screen only lets the hero in when 0xE046 is greater than the place
(`sala_puerta_mira`, 0x88E9); 0xE046 goes up by one every five of certain objects picked up (`cosa_coge`, 0x977C).
Past X 0x28, `dibujo_suceso` (0x84DF) loads 0x2C0 bytes of drawings into tiles 0x90 of the three thirds (from 0x6800,
0x6C00, 0x6A80, 0x6B80 and 0x6B80 again, with their colours 0x1000 further on) and the event's routine puts its big
drawing, 8 x 8 tiles, and its y&#333;kai:

| place | screen | the event | how it is beaten |
|---|---|---|---|
| 0 | 0x09 | the drawing at 0x7700 (row 10, column 15): a face with long hair; the hair is the five objects of type 0x13 of the screen, drawn afterwards | six blows of the weapon on its spot (X 0x88-0x97, Y 0x48-0x8F); going near pushes the hero 0x20 away; going back past X 0x20 rubs it out |
| 1 | 0x12 | the one at 0x7780 (row 13): a horned skull, and two y&#333;kai of type 0x10, the bolts that come out of its eyes | ten blows on the bolts |
| 2 | 0x1E | the one at 0x7740 (row 13): a cocoon hanging from a tree, and two of type 0x11 | reaching its spot (Y 0x68-0x77, X 0x88-0x97); walking along below Y 0x71 pushes the hero away |
| 3 | 0x2F | the one at 0x77C0 (row 12): a big red eye, two eyes of type 0x12 and the pupil, type 0x13 | five blows on the pupil |
| 4 | 0x44 | no drawing: two y&#333;kai, 0x15 and 0x16, a flame over a ghost at each top corner | four blows: the ending is set going (0xE047 = 1) |

Each one **drawn by running the ROM** (`tools/jefes.py`): over the recorded frame just before it appears,
`sala_suceso` runs in `tools/bios.py`; the play area, without sprites (nor the hair of the 0, which the objects draw later). Check: the name table, the tile drawings and
colours and the types of its y&#333;kai come out **identical** to the recorded ones in the 5 events.

![The event of place 0](imagenes/jefe_0.png)

![The event of place 1](imagenes/jefe_1.png)

![The event of place 2](imagenes/jefe_2.png)

![The event of place 3](imagenes/jefe_3.png)

![The event of place 4](imagenes/jefe_4.png)

Beaten (places 0 to 3, `suceso_vencido` 0x8393): tune 7, the y&#333;kai out, the drawing rubbed out and two sprites
(0xAC and 0xB0) that go up and out; then the place is over (`sala_acabada`, 0xAF73): the endurance fills up and the
next one starts.

**Recorded in openMSX, FORCED** (`tools/guiones/jefes.tcl`): with the title keys, each place put by hand and F1, 0xE046
put by hand and the hero taken to the event's screen, coming in from its side as when walking. Then a pilot made for
the events plays: it walks to an X, faces right, throws the weapon every 16 frames and jumps every 50. It beats the
one of place 1 (ten blows in some 3,000 frames); the others it does not, in 4,000 frames each: in the 0 and the 2 the
hero has to be higher than the floor (Y 0x98), in the 3 it hits the pupil once and in the 4 never.

![The event of place 0 (forced)](imagenes/jefe_0.gif)

![The event of place 1 (forced)](imagenes/jefe_1.gif)

![The event of place 1 beaten, played](imagenes/jefe_1_vencido.gif)

![The event of place 2 (forced)](imagenes/jefe_2.gif)

![The event of place 3 (forced)](imagenes/jefe_3.gif)

![The event of place 4 (forced)](imagenes/jefe_4.gif)

## The ending

Beating the event of place 4 does not end the place: it sets 0xE047 = 1 and tune 7 plays. The ending is on another
screen, **0x3C** (row 3, column 8 of the plan of place 4), which is reached by dropping down the shaft of 0x3B. Its
list (0x4EBE) carries the only y&#333;kai of type 0x0B, **a girl** (0xA778), who only comes out with:

- 0xE047 set (the event of place 4 beaten);
- the objects of types 4 and 5 picked up (0xE048 and 0xE049) and two of type 6 (0xE04A = 2). **Those objects are only
  in the sixth place** (screens 0x45 to 0x49: type 4 on 0x45 and 0x49, type 5 on 0x47, type 6 on 0x46 and 0x48), the
  one that is on no route of the other places, reached by the doors 28 to 32 (see above).

Then she appears on the left (X 0x10, Y 0x80) and the hero can no longer move (0xE047 = 2: `prota_mueve` and `salto`
do nothing); she walks to the right, 0xE8/0xEC and 0xF0/0xF4 every 8 frames. When she gets within 12 dots of him (and
he is standing at Y 0x80), both stand still face to face and **めでたし！** comes up twice (*medetashi*, "and they
lived happily ever after", the closing line of Japanese tales: 0xA839 and 0xA846, 13 + 13 tiles, at rows 6-7 and
9-10), with tune 3. When it ends the place is over (0xE186 = 2): the screen closes, the round goes up (0xE009) and,
with 0xE047 = 2, `sala_empieza` starts **another game** from place 0 (`partida_va`, 0x7FB7): three lives, the objects
at zero, but **the points are kept**; with the round at 1 the white ghosts sometimes come out in light blue, and from
round 2 in light red (see [The sprites](THE-SPRITES.html)).

**Recorded in openMSX, FORCED** (`tools/guiones/final.tcl`): with the title keys, place 4 put by hand and F1; then
0xE047 = 1, the four objects as picked up and screen 0x3C, coming in from above as through the shaft. Nothing else is
touched: the hero falls to the floor, the girl comes out, walks up to him and the rest is the game.

![The ending (forced)](imagenes/final.gif)

## The places, forced

The GIFs of places 1 to 4 are **forced**: the place put by hand (0xE00A) and F1, so that the hero falls and the place
starts again, now the new one. The pilot plays with the title keys.

![Place 1 (forced)](imagenes/sala_1.gif)

![Place 2 (forced)](imagenes/sala_2.gif)

![Place 3 (forced)](imagenes/sala_3.gif)

![Place 4 (forced)](imagenes/sala_4.gif)
