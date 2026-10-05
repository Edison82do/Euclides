# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso M.1; Common Core 3.OA.A.1, NCETM 2.2): a x b son a GRUPOS IGUALES de b.
No hay ninguna cuenta nueva: el x es otra forma de ESCRIBIR grupos iguales (NCETM 2.2: 'los grupos
iguales se pueden escribir como una suma repetida' y 'como una multiplicacion').  Asi que se hace la
SUMA DE IGUALES de M.0 (saltando si los grupos son de 2, 5 o 10; si no, grupo a grupo)."""

PIEZA = {
    "id": "multiplicar_grupos_iguales",
    "nombre": "grupos iguales (la suma repetida)",
    "unidad": "M.1",
    "responde": "multiplicar",
    "rapidez": 20,
    "que_hace": "a x b son a grupos de b: se juntan con la suma de iguales (M.0)",
    "condiciones": [
        ("los_grupos_tienen_nombre_x", "no se cuantos grupos son"),
    ],
    "usa": ["suma_de_iguales"],
}


def hacer(s, u):
    r = u.usar("suma_de_iguales", veces=s["a"], n=s["b"])
    return {"valor": r["valor"], "metodo": "%s (M.0)" % r["pieza"]["nombre"],
            "cuenta": r["resultado"]["cuenta"], "pasos": r["resultado"].get("pasos", []),
            "vuelta": "", "vuelta_ok": True}
