# -*- coding: utf-8 -*-
"""Pieza del resolvedor: la diferencia (comparar)  (unidad 5.5)."""

PIEZA = {
    "id": "diferencia",
    "nombre": "la diferencia (comparar)",
    "unidad": "5.5",
    "responde": "paso",
    "que_hace": "el grande - el pequeno = el hueco entre los dos",
    "condiciones": [
        ("se_pide_el_hueco", "la pregunta no pide cuantos mas o cuantos menos"),
    ],
    "usa": ["restar"],
}


def hacer(s, u):
    return u.usar("restar", a=s["grande"], b=s["pequeno"])
