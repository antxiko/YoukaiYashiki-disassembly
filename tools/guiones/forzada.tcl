# GRABACION FORZADA, con las teclas del titulo (el aguante lleno y los golpes no lo quitan): en el 1000, la sala 1
# (0xE00A = 1) y F1 (con aguante, el protagonista cae sin perder vida y la sala empieza otra vez: ya la 1); en el
# 2500, la 2; en el 4000, la 3; en el 5500, la 4. El piloto juega entre medias. Hasta 7000 cuadros.
source [file join [file dirname [info script]] piloto.tcl]
proc pon {a v} { debug write memory $a $v }
proc toca {fila bit} {
    keymatrixdown $fila $bit
    after time 0.08 "keymatrixup $fila $bit"
}
proc guion {n} {
    if {$n < 330} { keymatrixdown 1 0x1F } elseif {$n == 330} { keymatrixup 1 0x1F }
    if {$n == 400} { toca 8 0x01 }
    foreach {t s} {1000 1 2500 2 4000 3 5500 4} {
        if {$n == $t} { pon 0xE00A $s; toca 6 0x20 }
    }
    if {[m 0xE000] == 1} { piloto $n }
    return [expr {$n >= 7000}]
}
