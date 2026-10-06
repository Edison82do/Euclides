# -*- coding: utf-8 -*-
"""Pieza de calculo: RESTAR CENTENAS JUSTAS (paso N.3; NCETM 1.22, punto 2).  1100 - 800: 11 centenas
menos 8 centenas = 3 centenas = 300.  La centena se cuenta como UNA cosa."""

PIEZA = {
    "id": "restar_centenas_justas",
    "nombre": "contar centenas hacia atras",
    "unidad": "N.3",
    "responde": "restar",
    "rapidez": 4,
    "que_hace": "si los dos son centenas justas, se restan las centenas como si fueran cosas",
    "condiciones": [
        ("los_dos_son_centenas_justas", "no son los dos centenas justas (300, 800, 2500...)"),
        ("el_de_abajo_no_es_mayor", "se quitaria mas de lo que hay (no hay restas negativas, 5.4)"),
    ],
    "usa": [],
}


def _centenas(u, n):
    return u.escribir_cifras(u.cifras_de(n)[2:])


def hacer(s, u):
    ca, cb = _centenas(u, s["a"]), _centenas(u, s["b"])
    c = u.leer(u.contar_hasta(u.decir(cb), u.decir(ca)))   # de cb a ca, contando hacia arriba (P.6)
    total = u.escribir_cifras([0, 0] + u.cifras_de(c)) if c else 0
    adelante = u.sumar_por_columnas(c, cb)                 # la vuelta, tambien en centenas
    return {"valor": total, "metodo": "contar centenas (N.3)",
            "cuenta": "%d - %d: %d centenas - %d centenas = %d centenas (%d - %d = %d, contando de uno a otro) = %d"
                      % (s["a"], s["b"], ca, cb, c, ca, cb, c, total),
            "vuelta": "%d + %d: %d centenas + %d centenas = %d centenas" % (total, s["b"], c, cb, adelante),
            "vuelta_ok": adelante == ca}
