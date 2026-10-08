# -*- coding: utf-8 -*-
"""Pieza de calculo: SUMAR POR COLUMNAS (unidades 7.3 y 7.6).  Unidad con unidad, decena con
decena, centena con centena, y lo que pasa de nueve se lleva.  Cada columna, con los dedos."""

PIEZA = {
    "id": "sumar_por_columnas",
    "nombre": "las columnas",
    "unidad": "7.6",
    "responde": "sumar",
    "rapidez": 40,
    "que_hace": "suma columna a columna desde las unidades, llevandose lo que pasa de nueve",
    "condiciones": [
        ("el_total_tiene_nombre", "el total se pasa de lo que se escribir (mi techo)"),
    ],
    "usa": ["7.6"],
}


def hacer(s, u):
    r = u.leccion("7.6")(str(s["a"]), "+", str(s["b"]), u.saber)
    if r["conclusion"] != "se_puede":
        raise ValueError(r["conclusion"])
    return {"valor": r["total_valor"], "metodo": "las columnas (7.6)",
            "cuenta": r["expresion_cifras"], "vuelta": r.get("verificacion_texto"),
            "vuelta_ok": bool(r.get("verificacion"))}
