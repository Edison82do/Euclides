# -*- coding: utf-8 -*-
"""Pieza del resolvedor: juntar (agregacion)  (unidad 5.2)."""

PIEZA = {
    "id": "juntar",
    "nombre": "juntar (agregacion)",
    "unidad": "5.2",
    "responde": "paso",
    "que_hace": "una parte + la otra parte = el todo",
    "condiciones": [
        ("se_piden_los_dos_juntos", "la pregunta no pide juntar dos montones"),
        ("son_la_misma_cosa", "son cosas distintas, y juntarlas no responde a la pregunta"),
    ],
    "usa": ["sumar"],
}


def hacer(s, u):
    return u.usar("sumar", a=s["a"], b=s["b"])
