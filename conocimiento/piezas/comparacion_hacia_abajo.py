# -*- coding: utf-8 -*-
"""Pieza del resolvedor: la diferencia al reves (el que falta tiene MENOS)  (unidad 5.5)."""

PIEZA = {
    "id": "comparacion_hacia_abajo",
    "nombre": "la diferencia al reves (el que falta tiene MENOS)",
    "unidad": "5.5",
    "responde": "paso",
    "que_hace": "el que se sabe - el hueco = el que tiene menos",
    "condiciones": [
        ("hay_una_comparacion", "no hay ninguna comparacion entre dos (nadie tiene mas que nadie)"),
        ("el_que_falta_tiene_menos", "el que falta es el que tiene MAS, no el que tiene menos"),
    ],
    "usa": ["restar"],
}


def hacer(s, u):
    return u.usar("restar", a=s["conocido"], b=s["n"])
