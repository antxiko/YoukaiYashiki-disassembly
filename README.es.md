# Youkai Yashiki - desensamblado comentado

*(Also [in English](README.md).)*

El desensamblado comentado de **Youkai Yashiki** (妖怪屋敷, "la mansión de los yōkai"; Casio, 1986) para MSX: un cartucho de 32 KB con la cabecera en 0x4000.

- **100 %** del binario explicado: 14.711 bytes de código y 18.057 de datos con nombre, ni un byte sin asignar.
- **40,5 %** del listado comentado, 878 rutinas y etiquetas, ninguna por debajo del 10 % de comentarios.
- El listado se reensambla en la ROM original **byte a byte**.
- El título sale de ejecutar la ROM, cotejado con openMSX punto a punto; la presentación de CASIO, la demostración, la partida, GAME OVER y los cinco lugares, jugados en GIF en openMSX; las diez músicas, de su propio motor de sonido, y las cinco que suenan en las grabaciones idénticas a openMSX cuadro a cuadro.
- Cinco teclas pulsadas en el título llenan el aguante del protagonista para toda la partida, y la demostración lee sus mandos del principio de la BIOS.

La web: <https://antxiko.github.io/YoukaiYashiki-disassembly/es/>
(en inglés: <https://antxiko.github.io/YoukaiYashiki-disassembly/>).

## Reproducirlo

La imagen de la ROM no se distribuye. Pon la tuya en la raíz como `youkai.rom` (el volcado original `[!]` de GoodMSX, sha1 `15345c87...`) y ejecuta `make`. El detalle, en [POR DENTRO](docs/es/POR-DENTRO.md).

## Legal

El juego es de Casio y de sus titulares. La licencia de `LICENSE` cubre solo las herramientas, los comentarios, el análisis y la documentación de aquí. Mira [AVISO-LEGAL.md](AVISO-LEGAL.md).
