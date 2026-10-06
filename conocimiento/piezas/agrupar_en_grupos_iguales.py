# -*- coding: utf-8 -*-
"""Pieza de los PROBLEMAS DE x Y : (paso R.2; CGI y NCETM 2.6: dividir AGRUPANDO, cuotitiva).  Se sabe
el total y cuantos van en cada grupo; falta CUANTOS GRUPOS salen."""

PIEZA = {
    "id": "agrupar_en_grupos_iguales",
    "nombre": "agrupar (falta cuantos grupos)",
    "unidad": "R.2 + M.3",
    "responde": "paso_por",
    "que_hace": "el total en grupos de tantos = cuantos grupos salen",
    "condiciones": [
        ("se_busca_cuantos_grupos", "no se busca cuantos grupos"),
        ("se_saben_total_y_en_cada", "no se sabe el total o cuantos van en cada grupo"),
    ],
    "usa": ["dividir"],
}


def hacer(s, u):
    return u.usar("dividir", total=s["total"], divisor=s["en_cada"])
