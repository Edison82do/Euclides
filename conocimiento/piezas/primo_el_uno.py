# -*- coding: utf-8 -*-
"""Pieza de PRIMO O COMPUESTO (paso M.15; NCETM 2.21, punto 3): EL UNO.  Un primo tiene EXACTAMENTE dos
factores; el 1 solo tiene UNO (1 x 1): no es primo ni compuesto.  Es el error tipico ('el 1 es primo
porque se divide entre 1 y entre si mismo'): con el 1, 'el 1' y 'si mismo' son el MISMO factor."""

PIEZA = {
    "id": "primo_el_uno",
    "nombre": "el 1: un solo factor",
    "unidad": "M.15",
    "responde": "primo",
    "rapidez": 1,
    "que_hace": "el 1 tiene un solo factor (1 x 1): ni primo ni compuesto",
    "condiciones": [
        ("es_el_uno", "no es el 1"),
    ],
    "usa": ["multiplicar", "dividir"],
}


def hacer(s, u):
    m = u.usar("multiplicar", a=1, b=1)["valor"]
    q = u.usar("dividir", total=1, divisor=1)["valor"]
    return {"valor": "ni_primo_ni_compuesto", "factores": [1], "parejas": [(1, 1)],
            "metodo": "el 1 tiene un solo factor (M.15; NCETM 2.21, punto 3)",
            "cuenta": "1 = 1 x 1: el unico factor es el 1; un primo tiene DOS factores distintos",
            "vuelta": "1 x 1 = %d, 1 : 1 = %d" % (m, q), "vuelta_ok": m == 1 and q == 1}
