# Las teclas 8, 9, -, ^ y la del yen (la fila 1, bits 0-4) sostenidas al acabar la presentacion de CASIO
# (0xE023 = 1: la vida llena y los golpes no la quitan) y una partida larga con el piloto. 20000 cuadros.
source [file join [file dirname [info script]] piloto.tcl]
proc toca {fila bit} {
    keymatrixdown $fila $bit
    after time 0.08 "keymatrixup $fila $bit"
}
proc guion {n} {
    if {$n < 330} { keymatrixdown 1 0x1F } elseif {$n == 330} { keymatrixup 1 0x1F }
    if {[m 0xE000] == 0} {
        keymatrixup 8 0xF1
        if {$n == 400} { toca 8 0x01 }
        return [expr {$n >= 20000}]
    }
    piloto $n
    return [expr {$n >= 20000}]
}
