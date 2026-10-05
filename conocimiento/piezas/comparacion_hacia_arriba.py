# -*- coding: utf-8 -*-
"""Pieza del resolvedor: la diferencia al reves (el que falta tiene MAS)  (unidad 5.5)."""

PIEZA = {
    "id": "comparacion_hacia_arriba",
    "nombre": "la diferencia al reves (el que falta tiene MAS)",
    "unidad": "5.5",
    "responde": "paso",
    "que_hace": "el que se sabe + el hueco = el que tiene mas",
    "condiciones": [
        ("hay_una_comparacion", "no hay ninguna comparacion entre dos (nadie tiene mas que nadie)"),
        ("el_que_falta_tiene_mas", "el que falta es el que tiene MENOS, no el que tiene mas"),
    ],
    "usa": ["sumar"],
}


def hacer(s, u):
    return u.usar("sumar", a=s["conocido"], b=s["n"])
