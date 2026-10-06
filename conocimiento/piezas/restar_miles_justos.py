# -*- coding: utf-8 -*-
"""Pieza de calculo: RESTAR MILES JUSTOS (paso N.4; NCETM 1.26, punto 4).  623 000 - 278 000: 623 mil menos
278 mil = 345 mil.  El mil se cuenta como UNA cosa."""

PIEZA = {
    "id": "restar_miles_justos",
    "nombre": "contar miles hacia atras",
    "unidad": "N.4",
    "responde": "restar",
    "rapidez": 3,
    "que_hace": "si los dos son miles justos, se restan los miles como si fueran cosas",
    "condiciones": [
        ("los_dos_son_miles_justos", "no son los dos miles justos (345 000, 2 000...)"),
        ("el_de_abajo_no_es_mayor", "se quitaria mas de lo que hay (no hay restas negativas, 5.4)"),
    ],
    "usa": [],
}


def _miles(u, n):
    return u.escribir_cifras(u.cifras_de(n)[3:])


def hacer(s, u):
    ma, mb = _miles(u, s["a"]), _miles(u, s["b"])
    m = u.leer(u.contar_hasta(u.decir(mb), u.decir(ma)))   # de mb a ma, contando hacia arriba (P.6)
    total = u.escribir_cifras([0, 0, 0] + u.cifras_de(m)) if m else 0
    adelante = u.sumar_por_columnas(m, mb)
    return {"valor": total, "metodo": "contar miles (N.4)",
            "cuenta": "%d - %d: %d mil - %d mil = %d mil (%d - %d = %d) = %d"
                      % (s["a"], s["b"], ma, mb, m, ma, mb, m, total),
            "vuelta": "%d mil + %d mil = %d mil" % (m, mb, adelante), "vuelta_ok": adelante == ma}
