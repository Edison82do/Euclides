# -*- coding: utf-8 -*-
"""Pieza de la IGUALDAD (paso E.0): 5 + 2 = 2 + 5 es verdad SIN CALCULAR, porque son los mismos dos
numeros juntados al reves, y juntar no depende del orden (lo aprendido en P.5, la conmutativa).
Es PENSAMIENTO RELACIONAL (Carpenter et al.): ver la relacion entre los lados sin hacer la cuenta."""

PIEZA = {
    "id": "igual_dando_la_vuelta",
    "nombre": "son los mismos numeros al reves",
    "unidad": "E.0 + P.5",
    "responde": "igualdad",
    "rapidez": 2,
    "que_hace": "a + b = b + a: juntar no depende del orden, asi que es verdad sin calcular",
    "condiciones": [
        ("son_los_mismos_numeros_al_reves", "no son dos sumas con los mismos numeros al reves"),
    ],
    "usa": [],
}


def hacer(s, u):
    i, d = s["lados"]
    if i["op"] == "x":
        return {"valor": "verdadero", "metodo": "los factores al reves (E.0 + M.2)",
                "cuenta": "%s y %s son los mismos factores al reves: %d grupos de %d y %d grupos de %d son "
                          "las mismas filas y columnas vistas de lado (NCETM 2.3: los factores en cualquier "
                          "orden, el producto es el mismo).  No hace falta calcular"
                          % (i["texto"], d["texto"], i["a"], i["b"], d["a"], d["b"]),
                "vuelta": "", "vuelta_ok": True}
    return {"valor": "verdadero", "metodo": "dar la vuelta (E.0 + P.5)",
            "cuenta": "%s y %s son los mismos numeros juntados al reves: juntar %d y %d es lo mismo que "
                      "juntar %d y %d (P.5).  No hace falta calcular"
                      % (i["texto"], d["texto"], i["a"], i["b"], d["a"], d["b"]),
            "vuelta": "", "vuelta_ok": True}
