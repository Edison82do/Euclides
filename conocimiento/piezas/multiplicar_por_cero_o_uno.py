# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso M.2; NCETM 2.4): 'cuando CERO es un factor, el producto es cero; cuando
UNO es un factor, el producto es el otro factor'.  Sin calcular."""

PIEZA = {
    "id": "multiplicar_por_cero_o_uno",
    "nombre": "un factor es cero o uno",
    "unidad": "M.2",
    "responde": "multiplicar",
    "rapidez": 1,
    "que_hace": "si un factor es 0, el producto es 0; si un factor es 1, el producto es el otro",
    "condiciones": [
        ("un_factor_es_cero_o_uno", "ningun factor es cero ni uno"),
    ],
    "usa": [],
}


def hacer(s, u):
    a, b = s["a"], s["b"]
    if a == 0 or b == 0:
        v, porque = 0, "un factor es CERO: %s, asi que no hay nada" % (
            "no hay ningun grupo" if a == 0 else "los grupos estan vacios")
    elif a == 1:
        v, porque = b, "un factor es UNO: un solo grupo de %d, son %d" % (b, b)
    else:
        v, porque = a, "un factor es UNO: %d grupos de uno, son %d" % (a, a)
    return {"valor": v, "metodo": "un factor es cero o uno (M.2)",
            "cuenta": "%s  (sin calcular)" % porque, "vuelta": "", "vuelta_ok": True}
