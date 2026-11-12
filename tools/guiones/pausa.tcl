# LA PAUSA, nada forzado: la partida con el piloto (piloto.tcl); a los 300 cuadros de juego, STOP (la fila 7, bit 4,
# tecla_stop 0xB4CA): la pausa (0xE1B7, `pausa` 0x8145) con el marco de cuatro sprites; 300 cuadros quieto y STOP otra
# vez. Hasta 1200 cuadros de juego.
source [file join [file dirname [info script]] piloto.tcl]
proc toca {fila bit} {
    keymatrixdown $fila $bit
    after time 0.08 "keymatrixup $fila $bit"
}
set ::juego 0
proc guion {n} {
    if {[m 0xE000] == 0} {
        keymatrixup 8 0xF1
        if {$n == 400} { toca 8 0x01 }
        return [expr {$n >= 20000}]
    }
    incr ::juego
    if {$::juego == 300 || $::juego == 600} { toca 7 0x10 }
    if {$::juego < 300 || $::juego > 610} { piloto $n } else { keymatrixup 8 0xF1 }
    return [expr {$::juego >= 1200}]
}
