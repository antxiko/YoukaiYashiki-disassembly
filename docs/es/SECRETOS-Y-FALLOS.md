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

## Fallo: los golpes al suceso del lugar 1 dan 10, 20, 30... puntos

Cuando el arma toca a un y&#333;kai, el c&oacute;digo de su tipo carga los puntos en A y salta a `puntos_suma`. Los
rayos del suceso del lugar 1 (tipo 0x10) hacen `ld a,010h` (0xA3FC, 100 puntos, como el 0x11 y el 0x12) y justo
despu&eacute;s `ld a,(0e1b2h)` (0xA3FE) para contar el golpe: el 0x10 se pierde, y lo que se suma es **el n&uacute;mero
de golpes**. Grabado en openMSX (el GIF de ese suceso en [Los lugares](LOS-LUGARES.html)), los puntos tras cada golpe:
10, 30, 60, 100, 150, 210, 280, 360, 450 y **550**, donde ser&iacute;an 1.000. El suceso del lugar 4 lo hace al
rev&eacute;s (`ld a,(0e1b2h)` ... `ld a,020h`, 0xAB63-0xAB6A) y da sus 200 por golpe.

## Fallo: un cuadro con el dibujo del protagonista

El fantasma blanco (tipos 0x0C, 0x0E, 0x0F y 0x14, 0xA853) que no entra por un borde recibe su color en el primer
cuadro (blanco, 0xA8A6) pero no su dibujo, que llega en el siguiente: durante un cuadro su sprite ense&ntilde;a el
dibujo que tuviera, el 0x00 tras `enemigos_borra`, **el protagonista de espaldas, en blanco**. En las grabaciones de
esta web pasa 15 veces.

## Corregido en el listado

El comentario de `puntos_suma` dec&iacute;a que daba una vida cada 100.000 puntos y otra a los 50.000: estaba copiado
de otro cartucho de Casio con la misma rutina. Ejecut&aacute;ndola aqu&iacute;, de 49.900 a 50.000 las vidas no
cambian, y la rutina no llama a nada m&aacute;s que a las cifras y al r&eacute;cord: **este juego no da vidas por
puntos**.
