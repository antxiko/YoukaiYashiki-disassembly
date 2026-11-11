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
