# -*- coding: utf-8 -*-
"""Pieza de DIVIDIR (paso M.3; NCETM 2.6, punto 4: 'si el divisor es dos, la MITAD').  Se hacen
parejas y se da una de cada pareja a cada lado (lo de N.1 y M.2).  Si sobra uno, ese es el resto."""

PIEZA = {
    "id": "dividir_a_la_mitad",
    "nombre": "la mitad (el divisor es dos)",
    "unidad": "M.3",
    "responde": "dividir",
    "rapidez": 5,
    "que_hace": "entre 2 es la mitad: parejas, una para cada lado",
    "condiciones": [
        ("el_divisor_es_dos", "el divisor no es dos"),
    ],
    "usa": [],
}


def hacer(s, u):
    actual, cada, objetivo = "cero", "cero", u.decir(s["total"])
    while actual != objetivo:
        uno = u.siguiente(actual)
        if uno == objetivo:
            v = u.leer(cada)
            return {"valor": v, "resto": 1, "metodo": "la mitad (M.3)",
                    "cuenta": "parejas, una para cada lado: %d para cada lado y SOBRA 1" % v,
                    "vuelta": "", "vuelta_ok": True}
        actual = u.siguiente(uno)
        cada = u.siguiente(cada)
    v = u.leer(cada)
    return {"valor": v, "resto": 0, "metodo": "la mitad (M.3)",
            "cuenta": "parejas, una para cada lado: %d para cada lado, no sobra ninguno" % v,
            "vuelta": "", "vuelta_ok": True}
