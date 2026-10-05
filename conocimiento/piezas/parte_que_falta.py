# -*- coding: utf-8 -*-
"""Pieza del resolvedor: la parte que falta (partir el todo)  (unidad 5.1)."""

PIEZA = {
    "id": "parte_que_falta",
    "nombre": "la parte que falta (partir el todo)",
    "unidad": "5.1",
    "responde": "paso",
    "que_hace": "el todo - la parte que se sabe = la otra parte",
    "condiciones": [
        ("hay_un_todo_y_una_parte", "no hay un todo conocido del que falte una parte"),
        ("la_parte_cabe_en_el_todo", "la parte es mayor que el todo, y eso no puede ser"),
    ],
    "usa": ["restar"],
}


def hacer(s, u):
    return u.usar("restar", a=s["todo"], b=s["parte"])
