# piloto.tcl - un jugador sencillo para Youkai Yashiki: anda hacia un lado (cambia cada 300 cuadros, o si no se
# mueve en 60), la barra (el arma) 2 cuadros de cada 16 y GRAPH (el salto) 2 de cada 50.
proc m {a} { return [debug read memory $a] }
set ::lado 0x80
set ::px -1
set ::quieto 0
proc piloto {n} {
    if {$n % 16 == 0} { keymatrixdown 8 0x01 }
    if {$n % 16 == 2} { keymatrixup 8 0x01 }
    if {$n % 50 == 10} { keymatrixdown 6 0x04 }
    if {$n % 50 == 12} { keymatrixup 6 0x04 }
    set x [m 0xE301]
    if {$x == $::px} { incr ::quieto } else { set ::quieto 0; set ::px $x }
    if {$n % 300 == 0 || $::quieto > 60} {
        set ::quieto 0
        if {$::lado == 0x80} { set ::lado 0x10 } else { set ::lado 0x80 }
    }
    keymatrixup 8 0xF0
    keymatrixdown 8 $::lado
}
