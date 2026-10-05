# -*- coding: utf-8 -*-
"""Pieza de calculo: RESTAR CON LOS DEDOS (unidad 7.4).  Se anota el primero, se levantan los dedos
del segundo, y por cada dedo que se baja se dice la palabra ANTERIOR."""

PIEZA = {
    "id": "restar_con_dedos",
    "nombre": "contar hacia atras con los dedos",
    "unidad": "7.4",
    "responde": "restar",
    "rapidez": 20,
    "que_hace": "anota el primero y cuenta hacia atras tantos dedos como el segundo",
    "condiciones": [
        ("el_de_abajo_no_es_mayor", "se quitaria mas de lo que hay (no hay restas negativas, 5.4)"),
        ("el_segundo_cabe_en_los_dedos", "el segundo pasa de diez: no cabe en los dedos"),
    ],
    "usa": ["7.4"],
}


def hacer(s, u):
    r = u.leccion("7.4")(u.decir(s["a"]), u.decir(s["b"]), u.saber)
    if r["conclusion"] != "se_puede":
        raise ValueError(r["conclusion"])
    vuelta = u.contar_adelante(r["resta"], u.decir(s["b"]))
    return {"valor": r["quedan"], "metodo": "los dedos hacia atras (7.4)",
            "cuenta": "%d - %d = %d  (desde el %d, %d dedos hacia atras)"
            % (s["a"], s["b"], r["quedan"], s["a"], s["b"]),
            "vuelta": "%s + %s = %s" % (r["resta"], u.decir(s["b"]), vuelta.get("resultado")),
            "vuelta_ok": vuelta.get("resultado") == u.decir(s["a"])}
