# -*- coding: utf-8 -*-
"""Pieza de PASAR POR UNA FILA MAS PEQUENA (paso M.21; NCETM 2.27, puntos 1 y 4; 6.RP.A.3a): la tabla de razon con una
fila de en medio.
    6 | 9          ni de 6 a 10 ni dentro de 6 | 9 hay un numero justo de veces;
    2 | 3          pero 6 | 9 se hace mas pequena dividiendo LAS DOS entre 3 (la forma mas simple, F.6): 2 | 3;
   10 | ?          de 2 a 10 es x 5: 3 x 5 = 15
Cuesta mas (tres cuentas): solo se usa si entre las filas y dentro de la fila no salen.
LA VUELTA: la fila pequena por su factor da la fila conocida, y por el otro factor da la fila del hueco (multiplicando).
La trampa: dividir solo UNA columna; la vuelta la caza."""

PIEZA = {
    "id": "proporcion_pasando_por_una_fila_mas_pequena",
    "nombre": "pasar por una fila mas pequena (dividir las dos columnas) y escalar",
    "unidad": "M.21",
    "responde": "proporcion",
    "rapidez": 7,
    "que_hace": "6 es a 9 como 10 es a ?: 6 | 9 = 2 | 3 (entre 3); de 2 a 10 es x 5: 3 x 5 = 15 (NCETM 2.27)",
    "condiciones": [
        ("es_una_tabla_de_razon_con_un_hueco", "no es una tabla de razon de enteros (sin ceros) con UN hueco"),
        ("la_fila_conocida_se_puede_hacer_mas_pequena",
         "la fila conocida ya es la mas pequena (sus dos numeros solo comparten el 1)"),
    ],
    "usa": ["simplificar_fraccion", "dividir", "multiplicar"],
}


def _justo(u, n, d):
    r = u.usar("dividir", total=n, divisor=d)
    return None if r["resultado"].get("resto", 0) else r["valor"]


def _fila(f):
    return "%s | %s" % tuple("?" if x is None else "%d" % x for x in f)


def hacer(s, u):
    c, h = s["conocida"], s["con_hueco"]
    j = 0 if h[0] is None else 1                      # la columna del hueco
    r = u.usar("simplificar_fraccion", a=c[0], b=c[1])["resultado"]
    p = (r["arriba"], r["abajo"])
    if p == c:
        raise ValueError("%s ya es la fila mas pequena" % _fila(c))
    m = _justo(u, c[0], p[0])                         # lo que se dividio
    pasos = ["la tabla de razon:  %s  /  %s" % (_fila(c), _fila(h)),
             "hago la fila %s mas pequena dividiendo LAS DOS columnas entre %d: %s  (%s)"
             % (_fila(c), m, _fila(p), r.get("metodo", "F.6"))]
    pequeno, sabido = p[1 - j], h[1 - j]
    if pequeno == sabido:
        k = 1
    elif u.viene_despues(u.decir(sabido), u.decir(pequeno)):
        k = _justo(u, sabido, pequeno)
    else:
        k = None
    if k is None:
        raise ValueError("de la fila %s a %d no hay un numero justo de veces" % (_fila(p), sabido))
    v = p[j] if k == 1 else u.usar("multiplicar", a=p[j], b=k)["valor"]
    pasos.append("de la fila %s a la del hueco: de %d a %d es x %d; la otra columna: %d x %d = %d"
                 % (_fila(p), pequeno, sabido, k, p[j], k, v))
    # LA VUELTA: la fila pequena por m da la conocida; por k da la del hueco
    c0, c1 = u.usar("multiplicar", a=p[0], b=m)["valor"], u.usar("multiplicar", a=p[1], b=m)["valor"]
    nueva = (v, sabido) if j == 0 else (sabido, v)
    h0 = nueva[0] if k == 1 else u.usar("multiplicar", a=p[0], b=k)["valor"]
    h1 = nueva[1] if k == 1 else u.usar("multiplicar", a=p[1], b=k)["valor"]
    ok = (c0, c1) == c and (h0, h1) == nueva
    vl = "%s x %d = %d | %d y %s x %d = %d | %d" % (_fila(p), m, c0, c1, _fila(p), k, h0, h1)
    return {"valor": v, "factor": k, "metodo": "pasar por una fila mas pequena (M.21; NCETM 2.27)",
            "pasos": pasos, "cuenta": "; ".join(pasos),
            "vuelta": "%s ... %s" % (vl, "SI" if ok else "NO"), "vuelta_ok": ok,
            "vuelta_explicada": "multiplico la fila pequena: %s (salen las dos filas)" % vl}
