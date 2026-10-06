# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso M.4; NCETM 2.7): 'los productos de la tabla del 4 son el DOBLE de los de
la del 2; los de la del 8, el doble de los de la del 4' (y NCETM 2.8: la del 6, el doble de la del 3).  Es un HECHO DERIVADO: 6 x 4 = el doble de
6 x 2 (que ya se sabe) = 12 + 12 = 24.  Solo encaja si la mitad ya esta en la memoria."""

PIEZA = {
    "id": "multiplicar_doblando",
    "nombre": "doblar la tabla de la mitad (4 desde 2, 8 desde 4, 6 desde 3)",
    "unidad": "M.4",
    "responde": "multiplicar",
    "rapidez": 4,
    "que_hace": "x 4 es el doble de x 2; x 8, de x 4; x 6, de x 3 (si ese ya lo se)",
    "condiciones": [
        ("se_puede_doblar_una_tabla", "ningun factor es 4, 6 u 8, o la mitad (x 2, x 3 o x 4) no la se todavia"),
    ],
    "usa": ["sumar"],
}


def _mitad(s, u):
    for f, k in ((s["b"], s["a"]), (s["a"], s["b"])):
        if f in (4, 8, 6):
            m = {4: 2, 8: 4, 6: 3}[f]
            h = u.recuerdo("%d x %d" % (k, m)) or u.recuerdo("%d x %d" % (m, k))
            if h:
                return k, f, m, h["valor"]
    return None


def hacer(s, u):
    k, f, m, h = _mitad(s, u)
    r = u.usar("sumar", a=h, b=h)
    return {"valor": r["valor"], "metodo": "doblando (M.4)",
            "cuenta": "x %d es el DOBLE de x %d: %d x %d = %d (lo se), y el doble: %d + %d = %d (%s)"
                      % (f, m, k, m, h, h, h, r["valor"], r["resultado"]["metodo"]),
            "vuelta": "", "vuelta_ok": True}
