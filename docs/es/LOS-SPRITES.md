# Los sprites

Todo lo de esta página está **montado desde las tablas de la ROM** con `tools/hojas.py`: los dibujos son los 0x800
bytes de 0x5800 que `sprites_dibujos` (0xB36D) pone tal cual en 0x3800, y cada figura se arma con los dibujos y los
colores que le da el código. Cada cosa son sprites de 16 bytes desde 0xE300 (los 4 primeros, sus atributos): el
protagonista en 0xE300 y 0xE310, su arma en 0xE320 y los doce enemigos desde 0xE340 (+4 el tipo, por la tabla de
0xA1E8). Ninguna de estas imágenes es una captura.

**Cotejado con openMSX** en las grabaciones de esta web:

- la tabla de dibujos de los sprites (VRAM 0x3800-0x3FFF) es **idéntica** a la del juego en 35.858 cuadros (otros 4
  pillan la copia a medias);
- los dos sprites del protagonista, en el mismo sitio con el dibujo y el dibujo + 0x60 en amarillo claro, en
  **26.999 cuadros, 0 distintos** (otros 123 aún a cero);
- el arma, 0x28 o 0x2C, en **13.221 cuadros, 0 distintos**;
- los enemigos llevan uno de los dibujos (o el siguiente, + 4) y uno de los colores que les da su código en 14.615
  cuadros; **11 sin explicar**. Las rutinas de los enemigos no tienen nombre en el listado, así que este cotejo no va
  tipo a tipo.

## El protagonista y su arma

Dos sprites en el mismo sitio: el dibujo en magenta y el dibujo + 0x60 en amarillo claro (`sala_empieza` 0x806D,
`caida_para` 0x87A3). De pie 0x0C o 0x14 según su lado (0x880D), y andando de 0x08 a 0x1C. Después el arma
(`ataque_sale`, 0xE320): 0x28 a la derecha y 0x2C a la izquierda, que sale a 4 puntos por cuadro:

![El protagonista y su arma](../imagenes/protagonista.png)

## Los fantasmas

Los dibujos y colores que las rutinas de los enemigos (0xA216-0xAD85) ponen en su sprite, cada uno con el siguiente
(+ 4) cuando lo cambian: 0x38 / 0x3C en blanco mientras esperan (0xA216), 0x30 en cian (0xAAE8), 0x4C en azul claro o
rojo claro (0xA451, 0xA457), 0x88 y 0x9C en rojo oscuro (0xA4E3), 0xF8 en rojo claro (0xA7A3), 0xAC en azul claro
(0xAB20), 0xE4 en amarillo claro (0xABE9), 0x40 en rojo claro (0xABF9) o negro (0xAD81), 0xB8 en azul oscuro
(0xAC18), 0xA8 en rojo claro (0xAC90), 0xD4-0xE0 en blanco (0xA884) y 0xA4 en rojo claro (0xA60A); al final, los dos
que salen al vencer una sala (`suceso_vencido`: 0xAC y 0xB0):

![Los dibujos de los fantasmas](../imagenes/enemigos.png)

El protagonista andando y algunos fantasmas con sus dos dibujos, al ritmo del juego:

![El protagonista y los fantasmas, cuadro a cuadro](../imagenes/andar_cuadros.gif)
