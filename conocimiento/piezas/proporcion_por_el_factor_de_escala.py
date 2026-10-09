# -*- coding: utf-8 -*-
"""Pieza del FACTOR DE ESCALA (paso M.21; NCETM 2.27, puntos 1, 3 y 4; 6.RP.A.3a): la tabla de razon, ENTRE las filas.
    2 | 5          de 2 a 6 es x 3 (6 : 2 = 3): la otra columna, tambien x 3:  5 x 3 = 15
    6 | ?
Si la fila del hueco es mas pequena, al reves: 12 | 30 y ? | 5 -> de 30 a 5 es : 6, asi que 12 : 6 = 2.
Es lo de los mapas (1 cm son 50000 cm: 7 cm son 50000 x 7) y lo de las figuras semejantes (todas las medidas por el
mismo factor).  Encaja si en la columna que se sabe en las dos filas una cabe justo en la otra (dividiendo).
LA VUELTA, con las contrarias: lo que salio, deshecho por el factor, vuelve a la fila conocida; y el factor por la fila
pequena da la grande.  La trampa: SUMAR (de 2 a 6 son 4 mas, 5 + 4 = 9); la vuelta la caza."""

PIEZA = {
    "id": "proporcion_por_el_factor_de_escala",
    "nombre": "entre las filas: el factor de escala",
    "unidad": "M.21",
    "responde": "proporcion",
    "rapidez": 5,
    "que_hace": "2 es a 5 como 6 es a ?: de 2 a 6 es x 3, asi que 5 x 3 = 15 (NCETM 2.27)",
    "condiciones": [
        ("es_una_tabla_de_razon_con_un_hueco", "no es una tabla de razon de enteros (sin ceros) con UN hueco"),
        ("entre_las_filas_hay_un_factor_justo",
         "entre las filas no hay un numero justo de veces (ninguna cabe justo en la otra)"),
    ],
    "usa": ["dividir", "multiplicar"],
}


def _justo(u, n, d):
    r = u.usar("dividir", total=n, divisor=d)
    return None if r["resultado"].get("resto", 0) else r["valor"]


def _fila(f):
    return "%s | %s" % tuple("?" if x is None else "%d" % x for x in f)


def hacer(s, u):
    c, h = s["conocida"], s["con_hueco"]
    j = 0 if h[0] is None else 1                      # la columna del hueco
    x, y, otro = c[1 - j], h[1 - j], c[j]             # la columna que se sabe en las dos filas, y lo de enfrente
    pasos = ["la tabla de razon:  %s  /  %s" % (_fila(c), _fila(h))]
    if x == y:
        v = otro
        pasos.append("en la %s columna las dos filas tienen %d: es la misma fila (x 1): el hueco es %d"
                     % ("2.a" if j == 0 else "1.a", x, v))
        return {"valor": v, "metodo": "entre las filas (M.21; NCETM 2.27)", "pasos": pasos, "cuenta": "; ".join(pasos),
                "vuelta": "%d | %d es la misma fila ... SI" % (c[0], c[1]), "vuelta_ok": True,
                "vuelta_explicada": "las dos filas son la misma"}
    if u.viene_despues(u.decir(y), u.decir(x)):       # la fila del hueco es mas GRANDE: x k
        k = _justo(u, y, x)
        if k is None:
            raise ValueError("de %d a %d no es un numero justo de veces" % (x, y))
        v = u.usar("multiplicar", a=otro, b=k)["valor"]
        pasos.append("entre las filas: de %d a %d es x %d  (%d : %d = %d): el FACTOR DE ESCALA" % (x, y, k, y, x, k))
        pasos.append("la otra columna, por el mismo factor: %d x %d = %d" % (otro, k, v))
        atras = _justo(u, v, k)
        ida = u.usar("multiplicar", a=x, b=k)["valor"]
        ok = atras == otro and ida == y
        vl = "%d : %d = %s y %d x %d = %d" % (v, k, atras, x, k, ida)
    else:                                             # la fila del hueco es mas PEQUENA: : k
        k = _justo(u, x, y)
        if k is None:
            raise ValueError("de %d a %d no es un numero justo de veces" % (x, y))
        v = _justo(u, otro, k)
        if v is None:
            raise ValueError("de %d a %d es : %d, pero %d no se reparte justo entre %d" % (x, y, k, otro, k))
        pasos.append("entre las filas: de %d a %d es : %d  (%d : %d = %d): el FACTOR DE ESCALA" % (x, y, k, x, y, k))
        pasos.append("la otra columna, por el mismo factor: %d : %d = %d" % (otro, k, v))
        atras = u.usar("multiplicar", a=v, b=k)["valor"]
        ida = u.usar("multiplicar", a=y, b=k)["valor"]
        ok = atras == otro and ida == x
        vl = "%d x %d = %d y %d x %d = %d" % (v, k, atras, y, k, ida)
    return {"valor": v, "factor": k, "metodo": "entre las filas: el factor de escala (M.21; NCETM 2.27)",
            "pasos": pasos, "cuenta": "; ".join(pasos),
            "vuelta": "%s ... %s" % (vl, "SI" if ok else "NO"), "vuelta_ok": ok,
            "vuelta_explicada": "deshago con la contraria: %s (vuelven las dos filas)" % vl}
