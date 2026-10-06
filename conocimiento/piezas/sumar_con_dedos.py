# -*- coding: utf-8 -*-
"""Pieza de calculo: SUMAR CON LOS DEDOS (unidad 7.1).  Se anota el primero, se levantan los dedos
del segundo, y por cada dedo que se baja se dice la palabra siguiente.  Contar desde el primero:
la segunda etapa de las estrategias de los ninos."""

PIEZA = {
    "id": "sumar_con_dedos",
    "nombre": "contar con los dedos",
    "unidad": "7.1",
    "responde": "sumar",
    "rapidez": 20,
    "que_hace": "anota el primero y cuenta hacia adelante tantos dedos como el segundo",
    "condiciones": [
        ("el_segundo_cabe_en_los_dedos", "el segundo pasa de diez: no cabe en los dedos"),
        ("el_total_tiene_nombre", "el total se pasa de mi lista de contar (un millon)"),
    ],
    "usa": ["7.1"],
}


def hacer(s, u):
    r = u.leccion("7.1")(u.decir(s["a"]), u.decir(s["b"]), u.saber)
    if r["conclusion"] != "se_puede":
        raise ValueError(r["conclusion"])
    vuelta = u.contar_atras(r["total"], u.decir(s["b"]))
    return {"valor": r["total_valor"], "metodo": "los dedos (7.1)",
            "cuenta": "%d + %d = %d  (desde el %d, %d dedos hacia adelante)"
            % (s["a"], s["b"], r["total_valor"], s["a"], s["b"]),
            "vuelta": "%s - %s = %s" % (r["total"], u.decir(s["b"]), vuelta.get("resultado")),
            "vuelta_ok": vuelta.get("resultado") == u.decir(s["a"])}
