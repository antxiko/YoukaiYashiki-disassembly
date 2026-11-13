# LOS CINCO SUCESOS (los jefes), FORZADOS: con las teclas del titulo (el aguante lleno, los golpes no lo quitan), la
# partida. Por cada lugar (0xE00A) de la lista: si el suceso de antes no se vencio (si se vencio, el juego pasa solo al
# lugar siguiente), el lugar y F1 (empieza otra vez, ya ese; el cartel pide el boton: la
# barra cada 60 cuadros); 60 cuadros despues de verse al protagonista, la llave del suceso puesta a mano (0xE046 = 5:
# sala_suceso pide 0xE046 mayor que el lugar) y la pantalla del suceso (0x852E) con su fila y columna del plano
# (0xE0A2, 0xE0A1), entrando por su lado (0xE198: 2 por la izquierda, 3 por arriba) como al llegar andando. Entonces
# juega un piloto hecho para el suceso: anda hasta su X, mira a la derecha, tira el arma cada 16 cuadros y salta cada
# 50; en el 2 (hay que llegar a su sitio, Y 0x68-0x77 y X 0x88-0x97, y andando por debajo de 0x71 aparta), desde su X
# salta hacia la derecha. Hasta que el lugar se acaba (0xE186 = 2, o 0xE047 = 1 en el 4) y 240 cuadros mas, o 4000
# cuadros; el siguiente.
proc pon {a v} { debug write memory $a $v }
proc toca {fila bit} {
    keymatrixdown $fila $bit
    after time 0.08 "keymatrixup $fila $bit"
}
# lugar pantalla fila columna lado X-del-piloto salto-a-la-derecha
set ::jefes {
    {0 0x09 0 7 2 0x60 0}
    {1 0x12 9 1 3 0x60 0}
    {2 0x1E 3 5 2 0x6C 1}
    {3 0x2F 2 9 2 0x60 0}
    {4 0x44 6 9 2 0x60 0}
}
set ::i -1
set ::paso 0
set ::desde 0
set ::visto 0
set ::fin 0
proc empieza {n} {
    incr ::i
    if {$::i >= [llength $::jefes]} { return 1 }
    if {!$::fin} {
        pon 0xE00A [lindex $::jefes $::i 0]
        toca 6 0x20
    }
    set ::paso 1; set ::desde $n; set ::visto 0
    puts stderr "jefe $::i en $n"
    return 0
}
proc piloto_jefe {n x0 salto} {
    set x [m 0xE301]
    keymatrixup 8 0xF0
    if {$salto} {
        keymatrixup 6 0x04
        if {$x < $x0 - 4} { keymatrixdown 8 0x80 } elseif {$x > $x0 + 4} { keymatrixdown 8 0x10 } else {
            keymatrixdown 8 0x80
            if {$n % 4 == 0} { keymatrixdown 6 0x04 }
        }
        return
    }
    if {$x < $x0 - 10} { keymatrixdown 8 0x80 } elseif {$x > $x0 + 10} { keymatrixdown 8 0x10 } elseif {$n % 16 == 14} { keymatrixdown 8 0x80 }
    if {$n % 16 == 0} { keymatrixdown 8 0x01 }
    if {$n % 16 == 2} { keymatrixup 8 0x01 }
    if {$n % 50 == 10} { keymatrixdown 6 0x04 }
    if {$n % 50 == 12} { keymatrixup 6 0x04 }
}
proc guion {n} {
    if {$n < 330} { keymatrixdown 1 0x1F } elseif {$n == 330} { keymatrixup 1 0x1F }
    if {$n == 400} { toca 8 0x01 }
    if {$n == 700} { return [empieza $n] }
    if {$::paso == 1} {
        if {$n % 60 == 0} { toca 8 0x01 }
        if {$n > $::desde + 60 && [m 0xE300] < 0xC0 && [m 0xE183] == 0 && [m 0xE186] == 0} { incr ::visto }
        if {$::visto == 60} {
            lassign [lindex $::jefes $::i] l s f c lado
            keymatrixup 8 0xF1
            pon 0xE046 5
            pon 0xE0A2 $f; pon 0xE0A1 $c; pon 0xE0A3 $s
            if {$lado == 2} { pon 0xE300 0x80; pon 0xE310 0x80; pon 0xE301 0xF0; pon 0xE311 0xF0 }
            pon 0xE198 $lado
            set ::paso 2; set ::desde $n; set ::fin 0
        }
    } elseif {$::paso == 2} {
        piloto_jefe $n [lindex $::jefes $::i 5] [lindex $::jefes $::i 6]
        if {$::fin == 0 && ([m 0xE186] == 2 || [m 0xE047] == 1)} { set ::fin $n }
        if {($::fin > 0 && $n >= $::fin + 240) || $n >= $::desde + 4000} {
            keymatrixup 8 0xF1; keymatrixup 6 0x04
            pon 0xE047 0
            return [empieza $n]
        }
    }
    return 0
}
