# -*- coding: utf-8 -*-
"""Pieza de los PROBLEMAS DE x Y : (paso R.2; CGI y NCETM 2.6: dividir REPARTIENDO, partitiva).  Se
sabe el total y entre cuantos se reparte; falta CUANTOS LE TOCAN A CADA UNO."""

PIEZA = {
    "id": "repartir_en_partes_iguales",
    "nombre": "repartir (falta cuantos en cada uno)",
    "unidad": "R.2 + M.3",
    "responde": "paso_por",
    "que_hace": "el total repartido entre los grupos = cuantos le tocan a cada uno",
    "condiciones": [
        ("se_busca_cuantos_en_cada", "no se busca cuantos hay en cada uno"),
        ("se_saben_total_y_grupos", "no se sabe el total o entre cuantos se reparte"),
    ],
    "usa": ["dividir"],
}


def hacer(s, u):
    return u.usar("dividir", total=s["total"], divisor=s["grupos"])
