#!/usr/bin/env python3
"""Las musicas de Youkai Yashiki, EJECUTANDO su propio motor de sonido (ver motor_musica.py).

El motor es `sonido` (0xB77C; el de otros Casio, aqui 2 bytes antes que en The Stone of Wisdom), una vez por cuadro desde la interrupcion: tres pedidos (la musica 0xE2BE
en los tres canales; un efecto del canal A 0xE2C0; uno de B y C 0xE2C2) que ganan a lo que suena si su numero es
menor. La musica la pide `musica_pide` (0xB777): escribe el numero en 0xE2BE; el fondo de la partida es un efecto
de los canales B y C (0xE2C2: el 5, el 4 tras una puerta, el 2 con el suceso de la sala), que el bucle pide cada cuadro.
Aqui se escribe igual y se corre 0xB77C cuadro a cuadro; el motor llega al PSG por la BIOS (WRTPSG), que se atrapa. Las piezas tienen bucles
(0xFD-0xFC, 0xFB-0xFA, 0xF9-0xF8) y la orden 0xFE vuelve a empezar: las que vuelven, vuelven.

Uso:  musica.py registros N [cuadros] | mp3 N f.mp3 | todas docs/audio | cotejo
"""
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import motor_musica  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (numero, fichero, quien la pide); los numeros de 100 en adelante son efectos de B y C (100 + n en 0xE2C2)
MUSICAS = [
    (4, "musica_casio.mp3", "la presentacion de CASIO (0xB5EA)"),
    (2, "musica_sala.mp3", "una sala empieza (0x808D)"),
    (5, "musica_caida.mp3", "el protagonista cae (0xAE2B)"),
    (6, "musica_continuar.mp3", "CONTINUE / END (0xAEB9)"),
    (1, "musica_game_over.mp3", "GAME OVER (0xAF35)"),
    (7, "musica_suceso.mp3", "el suceso de la sala vencido (0x8393) y el ultimo (0x84D9)"),
    (3, "musica_final.mp3", "el final (0xA82B)"),
    (105, "musica_fondo.mp3", "la partida (0x81C1: el efecto 5 de B y C)"),
    (104, "musica_fondo_puerta.mp3", "tras una puerta (0x81C5: el efecto 4)"),
    (102, "musica_fondo_suceso.mp3", "con el suceso de la sala (0x81B3: el efecto 2)"),
]
VOCES = (0xE280, 0xE2B6)          # los tres canales, 18 bytes cada uno


def cfg(numero):
    pide = [("b", 0xE2C2, numero - 100)] if numero >= 100 else [("b", 0xE2BE, numero)]
    return dict(rom="youkai.rom", org=0x4000, sp=0xF000, frame=0xB77C,
                pistas={numero: pide}, psg0={7: 0xB8},
                ram=VOCES, hz=60, max_s=120, cuadros_previos=0)


def sonando(z, numero):
    """Lo que suena (0xE2BD la musica, 0xE2C1 el efecto de B y C) y lo pedido (0xE2BE, 0xE2C2)."""
    if numero >= 100:
        return z.mem[0xE2C1] or z.mem[0xE2C2]
    return z.mem[0xE2BD] or z.mem[0xE2BE]


def rom():
    return open(os.path.join(RAIZ, "youkai.rom"), "rb").read()


def ejecuta(numero, maximo=None):
    c = cfg(numero)
    maximo = maximo or c["hz"] * c["max_s"]
    z = motor_musica.arranca(c, rom(), numero)
    a, b = c["ram"]
    cuadros, vistos = [], {}
    for k in range(maximo):
        cuadros.append(motor_musica.cuadro(z))
        h = hashlib.sha1(bytes(z.mem[a:b])).digest()
        if h in vistos:
            return cuadros, (None if vistos[h] == k else vistos[h])
        vistos[h] = k + 1
        if k > 2 and not sonando(z, numero):
            return cuadros, None
    return cuadros, None


def mp3(numero, ruta):
    hz = 60
    cuadros, vuelta = ejecuta(numero)
    todo, fundido = motor_musica.desarrolla(cuadros, vuelta, hz)
    motor_musica.a_mp3(motor_musica.sintetiza(todo, hz), ruta, fundido, hz)
    print("%-26s %d cuadros (%.1f s), vuelve al %s" % (os.path.basename(ruta), len(cuadros),
                                                      len(cuadros) / hz, vuelta))


def estados(numero, maximo, inicio, siembra=None):
    """Cada cuadro del motor ejecutado: la RAM de las voces y los registros del PSG (desde los de `inicio`).
    `siembra`: la RAM del sonido (0xE280-0xE2D5) como la tenia el juego en ese cuadro."""
    c = cfg(numero)
    z = motor_musica.arranca(c, rom(), numero)
    if siembra:
        z.mem[0xE280:0xE2D6] = siembra
    for r in range(16):                 # el PSG como estaba: RDPSG lo lee para bajar el volumen
        z.maq.psg[r] = inicio[r]
    a, b = c["ram"]
    regs = list(inicio)
    out = [(bytes(z.mem[a:b]), tuple(regs))]
    for _ in range(maximo):
        for r, v in motor_musica.cuadro(z):
            if r < 16:
                regs[r] = v
        out.append((bytes(z.mem[a:b]), tuple(regs)))
    return out


def cotejo():
    """Los tonos y los volumenes del motor ejecutado contra los del PSG que grabo openMSX al entrar en cada
    interrupcion (work/*.bin, con la RAM 0xE000-0xEFFF). La musica empieza en el cuadro en que 0xE2BD (la que suena)
    pasa a ser su numero; el motor arranca con la RAM del sonido (0xE280-0xE2D5) y el PSG de ese cuadro, y cada
    cuadro grabado se empareja con el cuadro del motor que tiene la MISMA RAM en los tres canales (0xE280, 54
    bytes). Se miran los canales A (0, 1, 8), B (2, 3, 9) y C (4, 5, 10) mientras la musica sigue; el A, solo sin
    un efecto suyo (0xE2BF a 0), y B y C, sin uno de los suyos (0xE2C1 a 0)."""
    import vdp
    out = []
    for grab in ("atraccion", "partida", "trucos", "forzada"):
        ruta = os.path.join(RAIZ, "work", grab + ".bin")
        if not os.path.exists(ruta):
            continue
        cs = list(vdp.cuadros(ruta, 0x1000))
        for numero, fichero, _ in MUSICAS:
            casilla = 0x2C1 if numero >= 100 else 0x2BD
            n_ = numero - 100 if numero >= 100 else numero
            num = lambda k, casilla=casilla: cs[k]["ram"][casilla]
            k0 = next((k for k in range(1, len(cs)) if num(k) == n_ and num(k - 1) != n_), None)
            if k0 is None:
                continue
            emu = estados(numero, 60 * 60, cs[k0]["psg"], bytes(cs[k0]["ram"][0x280:0x2D6]))
            e, malos, mirados, sueltos = 0, [], 0, 0
            for j in range(k0 + 1, min(len(cs), k0 + 60 * 40)):
                # los efectos de B y C se emparejan solo por sus dos canales (el A lleva los disparos)
                ram = bytes(cs[j]["ram"][0x292:0x2B6] if numero >= 100 else cs[j]["ram"][0x280:0x2B6])
                if num(j) != n_:
                    break
                hallado = next((x for x in range(e, min(e + 8, len(emu)))
                                if (emu[x][0][0x12:] if numero >= 100 else emu[x][0]) == ram), None)
                if hallado is None:
                    sueltos += 1
                    continue
                e = hallado
                mirados += 1
                p, r = cs[j]["psg"], emu[e][1]
                if numero >= 100:
                    mirar = [(2, 3, 9), (4, 5, 10)]
                else:
                    mirar = ([] if cs[j]["ram"][0x2BF] else [(0, 1, 8)]) + ([] if cs[j]["ram"][0x2C1] else [(2, 3, 9), (4, 5, 10)])

                def distinto(t, a, v):
                    if p[v] != r[v]:
                        return True
                    return bool(p[v] & 0x1F) and (p[t] != r[t] or (p[a] & 15) != (r[a] & 15))
                if any(distinto(*c) for c in mirar):
                    malos.append(j - k0)
            out.append((fichero, grab, k0, mirados, malos, sueltos))
    return out


def main(argv):
    if argv and argv[0] == "cotejo":
        for fichero, grab, k0, mirados, malos, sueltos in cotejo():
            print("%-26s %s, empieza en el cuadro %d: %d cuadros mirados, %d distintos %s; %d sin pareja"
                  % (fichero, grab, k0, mirados, len(malos), malos[:8], sueltos))
        return 0
    if argv and argv[0] == "todas":
        os.makedirs(argv[1], exist_ok=True)
        for numero, fichero, _ in MUSICAS:
            if fichero.endswith(".mp3"):
                mp3(numero, os.path.join(argv[1], fichero))
        return 0
    if argv and argv[0] == "mp3":
        mp3(int(argv[1]), argv[2])
        return 0
    if argv and argv[0] == "registros":
        cuadros, vuelta = ejecuta(int(argv[1]), int(argv[2]) if len(argv) > 2 else None)
        for i, escr in enumerate(cuadros):
            print("%5d %s" % (i, " ".join("%X=%02X" % rv for rv in escr)))
        print("cuadros: %d, vuelve al %s" % (len(cuadros), vuelta))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
