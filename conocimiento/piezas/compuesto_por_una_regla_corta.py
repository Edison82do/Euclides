# -*- coding: utf-8 -*-
"""Pieza de PRIMO O COMPUESTO (paso M.15; NCETM 2.21, puntos 2 y 3) con LAS REGLAS CORTAS de M.4/M.5:
si es PAR (y no es el 2), tiene el factor 2; si acaba en 0 o 5 (y no es el 5), el 5; si sus cifras suman
3, 6 o 9 (y no es el 3), el 3.  Entonces tiene mas de dos factores: COMPUESTO, aunque sea grande
(1000 = 2 x 500).  Si ninguna regla encuentra factor, a esta pieza no le sale: hay que buscar las parejas.
Se COMPRUEBA multiplicando la pareja: 2 x 500 = 1000."""

PIEZA = {
    "id": "compuesto_por_una_regla_corta",
    "nombre": "una regla corta (par, acaba en 0 o 5, cifras que suman 3, 6 o 9)",
    "unidad": "M.15",
    "responde": "primo",
    "rapidez": 3,
    "que_hace": "1000 es par: 2 x 500, compuesto (sin buscar todas las parejas)",
    "condiciones": [
        ("pasa_de_uno", "es el 0 o el 1"),
    ],
    "usa": ["dividir", "multiplicar", "sumar"],
}


def _suma_de_cifras(u, n):
    """Se suman las cifras hasta que queda una sola (NCETM 2.8): 51 -> 6;  999999 -> 54 -> 9."""
    v, camino = n, ["%d" % n]
    while u.viene_despues(u.decir(v), "nueve"):
        total = 0
        for c in u.cifras_de(v):
            total = u.usar("sumar", a=total, b=c)["valor"]
        v = total
        camino.append("%d" % v)
    return v, camino


def hacer(s, u):
    n = s["n"]
    ultima = u.cifras_de(n)[0]
    if ultima in (0, 2, 4, 6, 8) and n != 2:
        d, regla = 2, "acaba en %d: es PAR, se parte en dos sin que sobre" % ultima
    elif ultima in (0, 5) and n != 5:
        d, regla = 5, "acaba en %d: se divide entre 5" % ultima
    else:
        v, camino = _suma_de_cifras(u, n)
        if v not in (3, 6, 9) or n == 3:
            raise ValueError("ninguna regla corta le encuentra un factor (no es par, no acaba en 0 ni en 5, y sus "
                             "cifras dan %d)" % v)
        d, regla = 3, "sus cifras suman %s: se divide entre 3" % " -> ".join(camino)
    r = u.usar("dividir", total=n, divisor=d)
    q = r["valor"]
    if r["resultado"].get("resto"):
        raise ValueError("la regla dice que se divide entre %d, y al dividir sobra: algo esta mal" % d)
    m = u.usar("multiplicar", a=d, b=q)["valor"]
    return {"valor": "compuesto", "pareja": (d, q), "regla": regla,
            "metodo": "una regla corta: %s (M.4/M.5)" % regla,
            "cuenta": "%d = %d x %d: ademas del 1 y del %d tiene el %d y el %d" % (n, d, q, n, d, q),
            "vuelta": "%d x %d = %d" % (d, q, m), "vuelta_ok": m == n}
