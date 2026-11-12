# Los lugares

Cinco lugares (0xE00A, de 0 a 4), cada uno con su **plano**: filas de diez casillas con el n&uacute;mero de la
pantalla que hay en cada sitio (0x4038). En total, **74 pantallas** de 32 x 20 casillas, cada una con su
descripci&oacute;n (0x41AC: piezas, rellenos, escaleras y dibujos) y su lista de y&#333;kai y objetos (0x4EBE). Se
pasa de una a otra por los bordes -la nueva entra desliz&aacute;ndose por ese lado-, por las escaleras y por las
puertas, que llevan a otro lugar (0xA0D7: el lugar, la columna y la fila de destino).

Los y&#333;kai (0xE340, hasta doce) son de 23 tipos: unos esperan y saltan, otros andan, vuelan o caen; los objetos
(0xE400) son lo que se coge, puertas y adornos.

Con las cinco teclas del t&iacute;tulo (el aguante lleno y los golpes no lo quitan, ver
[Curiosidades](CURIOSIDADES.html)), el piloto contra los y&#333;kai del cementerio:

![El cementerio, con las teclas del t&iacute;tulo](../imagenes/fantasmas.gif)

## Los planos

Los seis lugares enteros, con cada pantalla en su sitio del plano (0x4038), a la mitad de tamaño. Están **pintados
ejecutando la ROM** (`tools/mapas.py`): cada pantalla la monta `pantalla_monta` (0x9257) en la RAM, sobre las
casillas de un cuadro grabado de su lugar; las casillas son las mismas en todos y solo cambia el color de las
0x41-0x47 (`sala_colores`, 0x8206). Sin marcador, sprites ni los objetos que se pintan aparte.

El plano tiene **un sexto lugar** (el 5, con las pantallas 0x45-0x49) al que llevan las puertas 28 a 32 de la tabla
de 0xA0D7, y que ninguna grabación ha visitado: se pinta con las casillas del lugar 4, que es el color que le da
`sala_colores`. Y cuatro pantallas, de la 0x13 a la 0x16, no están en ningún plano.

Cotejo: de las 69 pantallas de los planos, las grabaciones solo pasan por 7; 3 salen **iguales** a la tabla de nombres
grabada y las otras cuatro con entre 4 y 31 casillas distintas de 640 (los objetos). En 4.012 de 4.050 cuadros grabados (uno
de cada siete), la pantalla que monta `pantalla_monta` aquí es la misma que tiene el juego en su RAM; de los 38 que
no, 29 son de la primera pantalla, y no se han mirado uno a uno.

![Lugar 0](../imagenes/plano_0.png)

![Lugar 1](../imagenes/plano_1.png)

![Lugar 2](../imagenes/plano_2.png)

![Lugar 3](../imagenes/plano_3.png)

![Lugar 4](../imagenes/plano_4.png)

![Lugar 5, el que no se ha grabado](../imagenes/plano_5.png)

## Los sucesos

Cada lugar tiene su **suceso** (`sala_suceso`, 0x8252): un dibujo grande que aparece en una pantalla concreta (la de
0x852E para cada lugar) con sus y&#333;kai, y que hay que vencer:

| lugar | el suceso |
|---|---|
| 0 | el dibujo de 0x7700; seis golpes del arma en su sitio |
| 1 | el de 0x7780 y dos y&#333;kai del tipo 0x10; diez golpes |
| 2 | el de 0x7740 y dos del tipo 0x11; llegar a su sitio |
| 3 | el de 0x77C0 y tres y&#333;kai (0x12 y 0x13); cinco golpes |
| 4 | dos y&#333;kai (0x15 y 0x16); cuatro golpes: el final se pone en marcha (0xE047) |

Vencido, suena la m&uacute;sica 7, dos sprites suben y el lugar se acaba: el aguante se llena y empieza el siguiente;
tras el 4, el 0 otra vez con una vuelta m&aacute;s (0xE009).

**El final**: con la marca del lugar 4 y ciertos objetos cogidos (0xE048, 0xE049 y 0xE04A = 2), aparece un personaje
(el y&#333;kai de tipo 11, 0xA778) que anda hacia la derecha; al llegar a &eacute;l, sale un texto (0xA839 y 0xA846)
y la m&uacute;sica 3. Ninguna grabaci&oacute;n ha llegado hasta ah&iacute;: esto sale del c&oacute;digo.

## Los lugares, forzados

Los GIF de los lugares 1 a 4 son **forzados**: el lugar puesto a mano (0xE00A) y F1, con lo que el protagonista cae
y el lugar empieza otra vez, ya el nuevo. Juega el piloto con las teclas del t&iacute;tulo.

![El lugar 1 (forzado)](../imagenes/sala_1.gif)

![El lugar 2 (forzado)](../imagenes/sala_2.gif)

![El lugar 3 (forzado)](../imagenes/sala_3.gif)

![El lugar 4 (forzado)](../imagenes/sala_4.gif)
