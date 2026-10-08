# -*- coding: utf-8 -*-
"""Pieza del HUECO EN DOS FRACCIONES EQUIVALENTES (paso F.6; NCETM 3.7, punto 2): LA RELACION VERTICAL.
4/12 = 5/?: de 4 a 5 no es por un numero justo, pero DENTRO de 4/12 el de abajo es 3 veces el de arriba (12 : 4 = 3);
en todas sus equivalentes tambien (como en 1/3): 5 x 3 = 15.  Con las impropias, al reves: en 12/4 el de arriba es
3 veces el de abajo.
LA VUELTA: las dos fracciones se simplifican (dividiendo, la contraria de multiplicar) y dan la MISMA."""

PIEZA = {
    "id": "hueco_por_la_relacion_vertical",
    "nombre": "la relacion vertical (dentro de la fraccion)",
    "unidad": "F.6",
    "responde": "hueco_equivalente",
    "rapidez": 5,
    "que_hace": "4/12 = 5/?: en 4/12 el de abajo es 3 veces el de arriba, asi que 5 x 3 = 15",
    "condiciones": [
        ("hay_un_hueco_y_una_fraccion_completa", "no hay una fraccion completa y otra con UN hueco"),
    ],
    "usa": ["dividir", "multiplicar", "simplificar_fraccion"],
}


def _justo(u, n, d):
    r = u.usar("dividir", total=n, divisor=d)
    return None if r["resultado"].get("resto", 0) else r["valor"]


def hacer(s, u):
    (p, q), (x, y) = s["completa"], s["con_hueco"]
    k = _justo(u, q, p)
    if k is not None:                  # abajo = arriba x k
        if x is None:
            v = _justo(u, y, k)
            if v is None:
                raise ValueError("en %d/%d el de abajo es %d veces el de arriba, pero %d no se reparte justo entre %d"
                                 % (p, q, k, y, k))
            cuenta = "en %d/%d el de ABAJO es %d veces el de arriba (%d : %d = %d);  arriba: %d : %d = %d" % (
                p, q, k, q, p, k, y, k, v)
        else:
            v = u.usar("multiplicar", a=x, b=k)["valor"]
            cuenta = "en %d/%d el de ABAJO es %d veces el de arriba (%d : %d = %d);  abajo: %d x %d = %d" % (
                p, q, k, q, p, k, x, k, v)
    else:
        k = _justo(u, p, q)
        if k is None:
            raise ValueError("dentro de %d/%d ninguno es un numero justo de veces el otro" % (p, q))
        if x is None:                  # arriba = abajo x k
            v = u.usar("multiplicar", a=y, b=k)["valor"]
            cuenta = "en %d/%d el de ARRIBA es %d veces el de abajo (%d : %d = %d);  arriba: %d x %d = %d" % (
                p, q, k, p, q, k, y, k, v)
        else:
            v = _justo(u, x, k)
            if v is None:
                raise ValueError("en %d/%d el de arriba es %d veces el de abajo, pero %d no se reparte justo entre %d"
                                 % (p, q, k, x, k))
            cuenta = "en %d/%d el de ARRIBA es %d veces el de abajo (%d : %d = %d);  abajo: %d : %d = %d" % (
                p, q, k, p, q, k, x, k, v)
    nueva = (v, y) if x is None else (x, v)
    s1 = u.usar("simplificar_fraccion", a=p, b=q)["valor"]
    s2 = u.usar("simplificar_fraccion", a=nueva[0], b=nueva[1])["valor"]
    return {"valor": v, "fraccion": nueva, "metodo": "la relacion vertical (F.6)", "cuenta": cuenta,
            "vuelta": "simplifico las dos: %d/%d = %s y %d/%d = %s" % (p, q, s1, nueva[0], nueva[1], s2),
            "vuelta_ok": s1 == s2}
