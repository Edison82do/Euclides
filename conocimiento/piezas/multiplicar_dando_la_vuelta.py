# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso M.2; NCETM 2.3 y 2.5, la conmutativa): 'los factores se pueden escribir
en cualquier orden y el producto es el mismo'; 'la misma multiplicacion tiene dos lecturas'.
5 x 7 son 5 grupos de 7, pero tambien 7 grupos de 5: y los grupos de 5 se cuentan con la tabla del 5
(5, 10, 15 ... 35), que es mas corto que sumar 7 + 7 + 7 + 7 + 7."""

PIEZA = {
    "id": "multiplicar_dando_la_vuelta",
    "nombre": "la otra lectura (dar la vuelta a los factores)",
    "unidad": "M.2",
    "responde": "multiplicar",
    "rapidez": 8,
    "que_hace": "a x b se lee como b grupos de a cuando los grupos de a se saltan (2, 5, 10)",
    "condiciones": [
        ("la_otra_lectura_se_salta", "dandole la vuelta tampoco son grupos de 2, 5 o 10 (o ya lo son sin darla)"),
    ],
    "usa": ["suma_de_iguales"],
}


def hacer(s, u):
    r = u.usar("suma_de_iguales", veces=s["b"], n=s["a"])
    return {"valor": r["valor"], "metodo": "la otra lectura (M.2)",
            "cuenta": "%d x %d son %d grupos de %d, pero tambien %d grupos de %d (los factores en cualquier "
                      "orden: el producto es el mismo).  Con la tabla del %d: %s"
                      % (s["a"], s["b"], s["a"], s["b"], s["b"], s["a"], s["a"], r["resultado"]["cuenta"]),
            "pasos": r["resultado"].get("pasos", []), "vuelta": "", "vuelta_ok": True}
