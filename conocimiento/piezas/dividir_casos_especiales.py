# -*- coding: utf-8 -*-
"""Pieza de DIVIDIR (paso M.3; NCETM 2.6, punto 5): 'si el dividendo es cero, el cociente es cero; si
el dividendo es igual al divisor, el cociente es uno; si el divisor es uno, el cociente es el
dividendo'.  Sin calcular."""

PIEZA = {
    "id": "dividir_casos_especiales",
    "nombre": "cero, el mismo, o entre uno",
    "unidad": "M.3",
    "responde": "dividir",
    "rapidez": 1,
    "que_hace": "0 : d = 0;  d : d = 1;  n : 1 = n  (sin calcular)",
    "condiciones": [
        ("el_divisor_no_es_cero", "el divisor es cero: no se puede repartir entre nadie (y los grupos de cero nunca se llenan)"),
        ("es_un_caso_especial", "ni el dividendo es cero, ni es igual al divisor, ni el divisor es uno"),
    ],
    "usa": [],
}


def hacer(s, u):
    t, d = s["total"], s["divisor"]
    if t == 0:
        return {"valor": 0, "resto": 0, "metodo": "un caso especial (M.3)",
                "cuenta": "no hay nada que repartir: 0  (sin calcular)", "vuelta": "", "vuelta_ok": True}
    if t == d:
        return {"valor": 1, "resto": 0, "metodo": "un caso especial (M.3)",
                "cuenta": "el total es igual que el divisor: sale 1 (un grupo justo, o uno para cada uno)  (sin calcular)",
                "vuelta": "", "vuelta_ok": True}
    return {"valor": t, "resto": 0, "metodo": "un caso especial (M.3)",
            "cuenta": "entre uno (o en grupos de uno): sale el mismo total, %d  (sin calcular)" % t,
            "vuelta": "", "vuelta_ok": True}
