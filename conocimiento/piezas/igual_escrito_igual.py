# -*- coding: utf-8 -*-
"""Pieza de la IGUALDAD (paso E.0): si los lados del = estan escritos IGUAL (7 = 7, 3 + 4 = 3 + 4),
es verdad sin calcular nada: una cosa es el mismo numero que ella misma.
Es el primer ejemplo del estandar (1.OA.D.7: '6 = 6'): un = sin ninguna operacion."""

PIEZA = {
    "id": "igual_escrito_igual",
    "nombre": "estan escritos igual",
    "unidad": "E.0",
    "responde": "igualdad",
    "rapidez": 1,
    "que_hace": "si todos los lados estan escritos igual, es verdad sin calcular",
    "condiciones": [
        ("todos_los_lados_estan_escritos_igual", "los lados no estan escritos igual"),
    ],
    "usa": [],
}


def hacer(s, u):
    t = s["lados"][0]["texto"]
    return {"valor": "verdadero", "metodo": "estan escritos igual (E.0)",
            "cuenta": "a los dos lados pone %s: una cosa es el mismo numero que ella misma (sin calcular)" % t,
            "vuelta": "", "vuelta_ok": True}
