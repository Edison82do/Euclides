# -*- coding: utf-8 -*-
"""Pieza de los PROBLEMAS DE x Y : (paso R.2; 3.OA.A.3; CGI: multiplicar).  El esquema de GRUPOS
IGUALES (Jitendra): se saben cuantos grupos y cuantos en cada uno; falta el TOTAL -> multiplicar."""

PIEZA = {
    "id": "juntar_grupos_iguales",
    "nombre": "juntar grupos iguales (falta el total)",
    "unidad": "R.2 + M.1",
    "responde": "paso_por",
    "que_hace": "cuantos grupos x cuantos en cada uno = el total",
    "condiciones": [
        ("se_busca_el_total", "no se busca el total"),
        ("se_saben_grupos_y_en_cada", "no se sabe cuantos grupos o cuantos hay en cada uno"),
    ],
    "usa": ["multiplicar"],
}


def hacer(s, u):
    return u.usar("multiplicar", a=s["grupos"], b=s["en_cada"])
