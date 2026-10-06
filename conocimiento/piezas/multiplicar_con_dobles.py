# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso M.2; NCETM 2.5): 'si DOS es un factor, se usan los DOBLES'.
7 x 2 (7 grupos de 2) y 2 x 7 (2 grupos de 7) son el doble de 7: 7 + 7 = 14."""

PIEZA = {
    "id": "multiplicar_con_dobles",
    "nombre": "el doble (un factor es dos)",
    "unidad": "M.2",
    "responde": "multiplicar",
    "rapidez": 6,
    "que_hace": "si un factor es 2, el producto es el doble del otro: x + x",
    "condiciones": [
        ("un_factor_es_dos", "ningun factor es dos"),
    ],
    "usa": ["sumar"],
}


def hacer(s, u):
    x = s["b"] if s["a"] == 2 else s["a"]
    r = u.usar("sumar", a=x, b=x)
    return {"valor": r["valor"], "metodo": "el doble (M.2)",
            "cuenta": "un factor es 2: es el DOBLE de %d: %d + %d = %d (%s)"
                      % (x, x, x, r["valor"], r["resultado"]["metodo"]),
            "vuelta": "", "vuelta_ok": True}
