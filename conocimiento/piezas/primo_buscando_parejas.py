# -*- coding: utf-8 -*-
"""Pieza de PRIMO O COMPUESTO (paso M.15; NCETM 2.21, puntos 2 y 3; 4.OA.B.4): se buscan TODAS las parejas
de factores (la pieza parejas_de_factores_en_orden).  Si solo sale 1 x n, tiene EXACTAMENTE dos factores:
es PRIMO (solo se puede poner en UNA fila).  Si sale mas de una pareja, es COMPUESTO (91 = 7 x 13: impar y
compuesto).  La comprobacion es la de las parejas: cada division, multiplicando de vuelta."""

PIEZA = {
    "id": "primo_buscando_parejas",
    "nombre": "buscar todas las parejas de factores",
    "unidad": "M.15",
    "responde": "primo",
    "rapidez": 10,
    "que_hace": "37: solo 1 x 37 -> dos factores: primo.  91: 1 x 91 y 7 x 13 -> compuesto",
    "condiciones": [
        ("pasa_de_uno", "es el 0 o el 1"),
    ],
    "usa": ["parejas_de_factores"],
}


def hacer(s, u):
    n = s["n"]
    r = u.usar("parejas_de_factores", n=n)["resultado"]
    solo_una = len(r["parejas"]) == 1
    return {"valor": "primo" if solo_una else "compuesto", "parejas": r["parejas"], "factores": r["factores"],
            "pareja": None if solo_una else r["parejas"][1],
            "metodo": "buscando todas las parejas de factores (M.15)",
            "cuenta": "%d = %s: %s" % (n, " = ".join("%d x %d" % p for p in r["parejas"]),
                                       "solo 1 y %d, DOS factores" % n if solo_una else "mas de dos factores"),
            "vuelta": r["vuelta"], "vuelta_ok": r["vuelta_ok"]}
