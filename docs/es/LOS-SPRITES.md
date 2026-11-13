# Los sprites

Todo lo de esta página está **montado desde las tablas de la ROM** con `tools/hojas.py`: los dibujos son los 0x800
bytes de 0x5800 que `sprites_dibujos` (0xB36D) pone tal cual en 0x3800, y cada figura se arma con los dibujos y los
colores que le da el código. Cada cosa son sprites de 16 bytes desde 0xE300 (los 4 primeros, sus atributos): el
protagonista en 0xE300 y 0xE310, su arma en 0xE320 y los doce enemigos desde 0xE340 (+4 el tipo, por la tabla de
0xA1E8). Ninguna de estas imágenes es una captura.

**Cotejado con openMSX** en las grabaciones de esta web:

- la tabla de dibujos de los sprites (VRAM 0x3800-0x3FFF) es **idéntica** a la del juego en 60.887 cuadros (otros 6
  pillan la copia a medias);
- los dos sprites del protagonista, en el mismo sitio con el dibujo y el dibujo + 0x60 en amarillo claro, en
  **48.170 cuadros, 0 distintos** (otros 172 aún a cero);
- el arma, 0x28 o 0x2C, en **24.243 cuadros, 0 distintos**;
- los y&#333;kai, **tipo a tipo**: cada uno lleva un dibujo y un color de los que le da el código de su tipo, en
  **35.966 cuadros, 0 distintos**, de 14 tipos (los demás no salen en las grabaciones).

## El protagonista y su arma

Dos sprites en el mismo sitio: el dibujo en magenta y el dibujo + 0x60 en amarillo claro (`sala_empieza` 0x806D,
`caida_para` 0x87A3). De pie 0x0C o 0x14 según su lado (0x880D), y andando de 0x08 a 0x1C. Después el arma
(`ataque_sale`, 0xE320): 0x28 a la derecha y 0x2C a la izquierda, que sale a 4 puntos por cuadro:

![El protagonista y su arma](../imagenes/protagonista.png)

## Los y&#333;kai, tipo a tipo

Cada y&#333;kai lleva su tipo en +4 y la tabla de 0xA1E8 lo manda a su rutina: 23 tipos, del 0x00 al 0x16. Aquí cada
uno con los dibujos y colores que le da su código, montados desde la ROM (`TIPOS` en `tools/hojas.py`). Los que
esperan (`enemigo_espera`, 0xA216) salen antes con 0x38/0x3C en blanco, y al vencerlos todos se quedan un momento con
0x38/0x3C en su color (0xA22C): eso no se repite en la hoja.

![Los y&#333;kai, tipo a tipo](../imagenes/enemigos.png)

| tipo | rutina | qué hace | entradas en las pantallas (0x4EBE) |
|---|---|---|---|
| 0x01 | 0xA278 | espera y luego salta de un lado a otro (las alturas de 0xA434), 0x30/0x34 cada 8 cuadros, cian y blanco cada 2; cada cinco vencidos, el aguante se llena | 22, en 12 pantallas |
| 0x02 | 0xA278 | lo mismo en blanco; vencido, el aguante sube medio | 11 |
| 0x03 | 0xA444 | 0x4C/0x50 en azul claro: de vez en cuando, un paso de 8 puntos a un lado si las casillas le dejan | 23 |
| 0x04 | 0xA444 | lo mismo en rojo claro; tocado, **se parte en dos**, uno al lado del otro, los dos del tipo 0x03 en azul oscuro (0xA394) | 18 |
| 0x05 | 0xA4C3 | dos sprites uno encima del otro (0x88/0x8C y 0x9C/0xA0, rojo oscuro y amarillo oscuro) que saltan hacia los lados (0x8FA2); cinco golpes | 3 |
| 0x07 | 0xA5EB | 0x54/0x58 en blanco, andando y saltando (0x8F91); tres golpes, y tras cada uno parpadea en cian | 5 |
| 0x08 | 0xA5EB | 0x94/0x98 en rojo claro; tras el primer golpe, verde claro; dos golpes y el aguante se llena. Solo en el sexto lugar | 5 |
| 0x09 | 0xA6B7 | espera y luego **vuela** por la pantalla al azar (Y 0x10-0xA0), 0x44/0x48 en azul oscuro | 41, en 21 pantallas |
| 0x0B | 0xA778 | **la chica del final** (ver [Los lugares](LOS-LUGARES.html)): dos sprites en el mismo sitio, 0xE8/0xEC y 0xF0/0xF4 andando, 0xF8/0xFC de pie | 1, la pantalla 0x3C |
| 0x0C | 0xA853 | el fantasma blanco, 0xD4-0xE0: entra por un borde o aparece, anda y tira un 0x0D; con la vuelta (0xE009) a 1 o en el lugar 4 a veces azul claro, desde la vuelta 2 en rojo claro | 48, en 33 pantallas |
| 0x0D | 0xAA49 | lo que tira el 0x0C: 0xA4 en rojo claro, 3 puntos por cuadro hasta salirse de la pantalla | (lo pone el 0x0C) |
| 0x10 | 0xABB8 | **suceso del lugar 1**: de los ojos de la calavera (X 0x6C o 0xAA, Y 0x64), primero con el dibujo vacío 0xE4 y luego un rayo, 0xB8 o 0xA8 según el lado del protagonista, amarillo claro; cada golpe cuenta para el suceso | (el suceso) |
| 0x11 | 0xACC6 | **suceso del lugar 2**: 0x38/0x3C en azul claro | (el suceso) |
| 0x12 | 0xABB8 | **suceso del lugar 3**: un ojo, 0x40 en rojo claro, desde los mismos sitios que el 0x10 | (el suceso) |
| 0x13 | 0xAD6F | **suceso del lugar 3**: la pupila del ojo grande (Y 0x76, X 0x90), 0x40, que va 16 puntos a cada lado; negra, y cada golpe le cambia el color (golpes x 2 + 1); a los cinco, el suceso vencido | (el suceso) |
| 0x15, 0x16 | 0xAA9A | **suceso del lugar 4**: una llama (0xAC) sobre un fantasma (0xB0, blanco), el 0x15 a la derecha (X 0xD8) en amarillo claro o rojo claro y el 0x16 a la izquierda (X 0x28) en cian o azul claro; salen arriba un momento, al azar; tocado, el borde parpadea y cae | (el suceso) |
| 0x0E, 0x0F, 0x14 | 0xA853 | la misma rutina que el 0x0C; ninguna pantalla los usa | 0 |
| 0x00, 0x06, 0x0A | &mdash; | nada: el 0x00 no se mueve (`enemigos` lo salta) y las rutinas del 0x06 (0xA5EA) y el 0x0A (0xA777) son un `ret` solo; su sprite no lleva dibujo ni color, así que **no se ve nada**. Tres pantallas (0x10, 0x23 y 0x40) llevan un 0x06 | 41 + 3 |

El protagonista andando y tres y&#333;kai (0x01, 0x03 y 0x09) con sus dos dibujos, al ritmo del juego:

![El protagonista y los fantasmas, cuadro a cuadro](../imagenes/andar_cuadros.gif)

## La pausa

STOP para el juego (`pausa`, 0x8145): guarda los sprites (en 0xE1C0) y con cuatro hace un dibujo donde estaba el
protagonista: la cara 0xD0 (magenta) y el vapor 0xC8 (amarillo claro) 16 puntos más arriba, y 0xC0 y 0xC4 (color 10)
a su altura, uno a cada lado; parece el protagonista metido en una tina. El vapor se turna con 0xCC cada 8 cuadros
(0x80E1). Con otro STOP vuelven los de antes. Grabado en openMSX (`tools/guiones/pausa.tcl`), sin forzar nada; el GIF
lleva **solo los cuatro sprites** de la grabación, sin la pantalla:

![La pausa](../imagenes/pausa.gif)

## Los 64 dibujos

La tabla de dibujos entera (los 0x800 bytes de 0x5800), en orden, con su número. **Todos los pone algún código menos
uno, el 0x90** (enmarcado en rojo): ninguna instrucción del cartucho lo escribe en un sprite. El 0xE4 está vacío y sirve
para esconder.

![Los 64 dibujos de los sprites](../imagenes/dibujos.png)

| dibujos | qué es | dónde lo pone |
|---|---|---|
| 0x00, 0x04, 0x60, 0x64 | el protagonista de espaldas, subiendo o bajando (el dibujo según su Y) | 0x8A04, 0x8A09 |
| 0x08, 0x0C, 0x10, 0x14, 0x18, 0x1C, 0x68, 0x6C, 0x70, 0x74, 0x78, 0x7C | el protagonista de pie, andando y saltando (y el + 0x60, su segundo color) | 0x8EF3, 0x880D, 0x8A9F, 0x8819, 0x8C2F, 0x8EFC, 0x8EF7, 0x8811, 0x8AA7, 0x881D, 0x8C37, 0x8F00 |
| 0x20, 0x80, 0x5C, 0xBC | el protagonista al perder una vida, una pareja y la otra cada 4 cuadros | 0xAE50, 0xAE54, 0xAE5A, 0xAE5E |
| 0x24, 0x84 | el protagonista tocado | 0x8BFC, 0x8C00 |
| 0x28, 0x2C | el arma, a la derecha y a la izquierda | 0x860B, 0x8615 |
| 0x30, 0x34 | los fantasmas que saltan, tipos 0x01 (cian y blanco) y 0x02 (blanco) | 0xA32A |
| 0x38, 0x3C | los y&#333;kai mientras esperan y al vencerlos; el tipo 0x11 (suceso del lugar 2) | 0xA222 |
| 0x40 | los ojos del suceso del lugar 3: el 0x12 (rojo claro) y la pupila 0x13 (negra, luego un color por golpe) | 0xABF9 |
| 0x44, 0x48 | el tipo 0x09, volando, en azul oscuro | 0xA76D |
| 0x4C, 0x50 | los tipos 0x03 (azul claro) y 0x04 (rojo claro), y las dos mitades de un 0x04 (azul oscuro) | 0xA45B, 0xA4BC |
| 0x54, 0x58 | el tipo 0x07, andando | 0xA601, 0xA68C |
| 0x88, 0x8C, 0x9C, 0xA0 | el tipo 0x05, dos sprites uno encima del otro, rojo oscuro y amarillo oscuro | 0xA4E3, 0xA4E7, 0xA593, 0xA597 |
| 0x94, 0x98 | el tipo 0x08, andando, en rojo claro (el sexto lugar) | 0xA606, 0xA68C |
| 0xA4 | lo que tira el fantasma blanco (tipo 0x0D), en rojo claro | 0xA917 |
| 0xA8 | el rayo del suceso del lugar 1 (tipo 0x10) con el protagonista a la derecha | 0xAC90 |
| 0xAC, 0xB0 | el suceso del lugar 4 (tipos 0x15 y 0x16: llama y fantasma); y los dos que suben al vencer un suceso (0x83AD) | 0xAB20, 0xAB24 |
| 0xB4 | con 0xB0, el que parpadea cada 8 cuadros (`suceso_parpadea`) | 0x831F |
| 0xB8 | el rayo del suceso del lugar 1 (tipo 0x10) con el protagonista a la izquierda | 0xAC18 |
| 0xC0, 0xC4, 0xC8, 0xCC, 0xD0 | la pausa: el protagonista en una tina (arriba) | 0x816F, 0x8173, 0x816B, 0x80E9, 0x8167 |
| 0xD4, 0xD8, 0xDC, 0xE0 | el fantasma blanco (tipo 0x0C), también en su salto | 0xA9F7 |
| 0xE4 | **vacío**, no se ve: se lo pone a un enemigo (0xABE9) y a los cuatro sprites del protagonista (0x95FC) | 0xABE9 |
| 0xE8, 0xEC, 0xF0, 0xF4 | **la chica del final** (tipo 0x0B) andando: dos sprites en el mismo sitio, rojo claro y amarillo claro | 0xA7D0, 0xA7D5 |
| 0xF8, 0xFC | la chica de pie, al salir y al encontrarse con el protagonista | 0xA7A3, 0xA7A7 |
| 0x90 | **sin uso**: ningún código lo pone | — |
