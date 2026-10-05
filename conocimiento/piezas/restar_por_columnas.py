# -*- coding: utf-8 -*-
"""Pieza de calculo: RESTAR POR COLUMNAS (unidades 7.5 y 7.6).  Columna a columna; si arriba no
llega, se CAMBIA una de la columna de al lado por diez (tambien a traves de un cero)."""

PIEZA = {
    "id": "restar_por_columnas",
    "nombre": "las columnas",
    "unidad": "7.6",
    "responde": "restar",
    "rapidez": 40,
    "que_hace": "resta columna a columna desde las unidades, cambiando cuando arriba no llega",
    "condiciones": [
        ("el_de_abajo_no_es_mayor", "se quitaria mas de lo que hay (no hay restas negativas, 5.4)"),
    ],
    "usa": ["7.6"],
}


def hacer(s, u):
    r = u.leccion("7.6")(str(s["a"]), "-", str(s["b"]), u.saber)
    if r["conclusion"] != "se_puede":
        raise ValueError(r["conclusion"])
    return {"valor": r["total_valor"], "metodo": "las columnas (7.6)",
            "cuenta": r["expresion_cifras"], "vuelta": r.get("verificacion_texto"),
            "vuelta_ok": bool(r.get("verificacion"))}
