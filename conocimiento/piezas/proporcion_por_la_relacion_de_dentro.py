# -*- coding: utf-8 -*-
"""Pieza de LA RELACION DE DENTRO (paso M.21; NCETM 2.27, punto 1; 6.RP.A.3a): la tabla de razon, DENTRO de la fila.
    3 | 12         en la fila conocida la 2.a columna es 4 veces la 1.a (12 : 3 = 4);
    7 | ?          en todas las filas igual (es lo que le toca a UNO):  7 x 4 = 28
(De 3 a 7 no hay un numero justo de veces: entre las filas no sale.)  Encaja si dentro de la fila conocida una columna
cabe justo en la otra (dividiendo).
LA VUELTA: en la fila nueva se divide la grande entre la pequena y tiene que salir el MISMO numero de veces, justo.
La trampa: mezclar las columnas (usar el numero de dentro al reves); la vuelta la caza."""

PIEZA = {
    "id": "proporcion_por_la_relacion_de_dentro",
    "nombre": "dentro de la fila: el mismo numero de veces en todas las filas",
    "unidad": "M.21",
    "responde": "proporcion",
    "rapidez": 5.5,
    "que_hace": "3 es a 12 como 7 es a ?: dentro de la fila es x 4 (12 : 3), asi que 7 x 4 = 28 (NCETM 2.27)",
    "condiciones": [
        ("es_una_tabla_de_razon_con_un_hueco", "no es una tabla de razon de enteros (sin ceros) con UN hueco"),
        ("dentro_de_la_fila_hay_un_factor_justo",
         "dentro de la fila conocida ninguna columna es un numero justo de veces la otra"),
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
    sabido = h[1 - j]
    pasos = ["la tabla de razon:  %s  /  %s" % (_fila(c), _fila(h))]
    if c[0] == c[1]:
        k, grande = 1, 1
    elif u.viene_despues(u.decir(c[1]), u.decir(c[0])):
        k, grande = _justo(u, c[1], c[0]), 1          # la 2.a columna es k veces la 1.a
    else:
        k, grande = _justo(u, c[0], c[1]), 0          # la 1.a columna es k veces la 2.a
    if k is None:
        raise ValueError("dentro de %s ninguna columna es un numero justo de veces la otra" % _fila(c))
    nombre = "2.a" if grande == 1 else "1.a"
    pasos.append("dentro de la fila %s: la %s columna es %d veces la otra (%d : %d = %d); en todas las filas igual"
                 % (_fila(c), nombre, k, c[grande], c[1 - grande], k))
    if j == grande:                                   # el hueco esta en la columna GRANDE: x k
        v = u.usar("multiplicar", a=sabido, b=k)["valor"]
        pasos.append("el hueco: %d x %d = %d" % (sabido, k, v))
        nueva = (v, sabido) if j == 0 else (sabido, v)
    else:                                             # el hueco esta en la columna pequena: : k
        v = _justo(u, sabido, k)
        if v is None:
            raise ValueError("%d no se reparte justo entre %d" % (sabido, k))
        pasos.append("el hueco: %d : %d = %d" % (sabido, k, v))
        nueva = (v, sabido) if j == 0 else (sabido, v)
    otra_vez = _justo(u, nueva[grande], nueva[1 - grande])
    ok = otra_vez == k
    vl = "en la fila nueva %s: %d : %d = %s" % (_fila(nueva), nueva[grande], nueva[1 - grande], otra_vez)
    return {"valor": v, "factor": k, "metodo": "dentro de la fila (M.21; NCETM 2.27)",
            "pasos": pasos, "cuenta": "; ".join(pasos),
            "vuelta": "%s, las mismas %d veces ... %s" % (vl, k, "SI" if ok else "NO"), "vuelta_ok": ok,
            "vuelta_explicada": "divido en la fila nueva: %s, el mismo numero de veces que en %s" % (vl, _fila(c))}
