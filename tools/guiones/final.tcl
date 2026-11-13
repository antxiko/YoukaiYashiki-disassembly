# EL FINAL, FORZADO: con las teclas del titulo, la partida; en el cuadro 700, la sala 4 (0xE00A = 4) y F1 (empieza
# otra vez, ya la 4; el cartel pide el boton: la barra cada 60 cuadros). 60 cuadros despues de verse el protagonista en la sala 4 (0xE0A3 >= 0x30 y su Y menor
# que 0xC0, a la vista), lo que el final pide puesto a mano: el suceso de la sala 4 vencido (0xE047 = 1) y
# los objetos del sexto lugar cogidos (0xE048 = 4, 0xE049 = 5, 0xE04A = 2); y la pantalla 0x3C (fila 3, columna 8
# del plano 4), la del personaje del final (tipo 0x0B), entrando por arriba (0xE198 = 3), como por el pozo de la 0x3B.
# Despues no se toca nada. Hasta que la sala se acaba (0xE186 = 2) y 300 cuadros mas, o 6000.
proc pon {a v} { debug write memory $a $v }
proc toca {fila bit} {
    keymatrixdown $fila $bit
    after time 0.08 "keymatrixup $fila $bit"
}
set ::fin 0
set ::listo 0
set ::visto 0
proc guion {n} {
    if {$n < 330} { keymatrixdown 1 0x1F } elseif {$n == 330} { keymatrixup 1 0x1F }
    if {$n == 400} { toca 8 0x01 }
    if {$n == 700} { pon 0xE00A 4; toca 6 0x20 }
    if {$::listo == 0 && $n > 760 && $n % 60 == 0} { toca 8 0x01 }
    if {$::listo == 0 && $n > 700 && [m 0xE0A3] >= 0x30 && [m 0xE300] < 0xC0} { incr ::visto }
    if {$::listo == 0 && $::visto == 60} {
        set ::listo $n
        pon 0xE047 1; pon 0xE048 4; pon 0xE049 5; pon 0xE04A 2
        pon 0xE0A2 3; pon 0xE0A1 8; pon 0xE0A3 0x3C
        pon 0xE301 0x94; pon 0xE311 0x94
        pon 0xE198 3
    }
    if {$::fin == 0 && $::listo > 0 && [m 0xE186] == 2} { set ::fin $n }
    return [expr {($::fin > 0 && $n >= $::fin + 300) || $n >= 6000}]
}
