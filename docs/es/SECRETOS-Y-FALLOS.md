# Secretos y fallos

Lo que se ha buscado en el c&oacute;digo y lo que se ha encontrado. Un fallo solo entra aqu&iacute; si est&aacute;
comprobado: ejecutando la propia rutina del juego (`tools/bios.py`) o contra las grabaciones de openMSX.

## Secretos

Contados en [Curiosidades](CURIOSIDADES.html):

- **8, 9, -, ^ y yen a la vez** al acabar la presentaci&oacute;n de CASIO (0x7F01): el aguante lleno y los golpes no
  lo quitan. Con ellas est&aacute;n grabados los GIF de los lugares.
- **F1** derriba al protagonista; sin aguante, es GAME OVER directo.
- **La demostraci&oacute;n juega la BIOS**: sus mandos son los bytes desde 0x0000, as&iacute; que cambia con el
  ordenador.

Fuera de esas teclas, los mandos se leen en la interrupci&oacute;n: la palanca de los cursores y del mando 1, los
botones del mando 1, la barra y GRAPH.

## Fallo: pasados los 9.999.990 puntos, el r&eacute;cord a cero

Cuando los puntos pasan de 999.999 por dentro (9.999.990 en pantalla, con el 0 fijo), `puntos_suma` (0xB3AF) copia al
r&eacute;cord (0xE094) los puntos **despu&eacute;s de dar la vuelta** (0xB3D9-0xB3E8). Ejecutando aqu&iacute; la suma
del juego:

| puntos (en pantalla) | r&eacute;cord | + | despu&eacute;s: puntos | r&eacute;cord |
|---|---|---|---|---|
| 123.450 | 100.000 | 100 | 123.550 | 123.550 |
| 9.999.900 | 9.999.900 | 100 | **0** | **0** |
| 9.999.500 | 9.999.500 | 900 | **400** | **400** |

## Fallo: los cursores y el mando a la vez

`palanca` (0xB505) junta los cursores y el mando 1 con un `or` (0xB515) de sus n&uacute;meros de direcci&oacute;n.
Con los dos a la vez, ejecut&aacute;ndolo aqu&iacute;, derecha y abajo dan **izquierda** (7), y arriba-derecha y
abajo-derecha, **abajo-izquierda** (6).

## Corregido en el listado

El comentario de `puntos_suma` dec&iacute;a que daba una vida cada 100.000 puntos y otra a los 50.000: estaba copiado
de otro cartucho de Casio con la misma rutina. Ejecut&aacute;ndola aqu&iacute;, de 49.900 a 50.000 las vidas no
cambian, y la rutina no llama a nada m&aacute;s que a las cifras y al r&eacute;cord: **este juego no da vidas por
puntos**.
