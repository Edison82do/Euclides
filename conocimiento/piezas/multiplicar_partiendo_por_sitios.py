# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso M.10; NCETM 2.14, puntos 1 y 3; Common Core 4.NBT.B.5): PARTIR POR SITIOS.
347 x 6 = 300 x 6 + 40 x 6 + 7 x 6 = 1800 + 240 + 42 = 2082.  Cada producto parcial es un hecho de la
tabla que se sabe (3 x 6 = 18) con las cifras subidas de sitio (M.9).  Es la distributiva (M.6) por sitios."""

PIEZA = {
    "id": "multiplicar_partiendo_por_sitios",
    "nombre": "partir por sitios (productos parciales)",
    "unidad": "M.10",
    "responde": "multiplicar",
    "rapidez": 8,
    "que_hace": "parte el numero grande en centenas, decenas y unidades, multiplica cada parte y suma",
    "condiciones": [
        ("un_factor_de_una_cifra_y_otro_de_varias", "no es un numero de varias cifras por uno de una cifra"),
    ],
    "usa": ["sumar"],
}

_SITIO = ("unidades", "decenas", "centenas", "millares", "decenas de millar", "centenas de millar", "millones")


def _hecho(u, x, k):
    if x == 0:
        return 0
    if x == 1:
        return k
    h = u.recuerdo("%d x %d" % (x, k)) or u.recuerdo("%d x %d" % (k, x))
    if not h:
        raise ValueError("no se de memoria %d x %d (primero hay que saberse las tablas)" % (x, k))
    return h["valor"]


def hacer(s, u):
    a, b = s["a"], s["b"]
    k, n = (a, b) if len(u.cifras_de(a)) == 1 else (b, a)
    parciales, lineas = [], []
    for i, c in enumerate(u.cifras_de(n)):
        if c == 0:
            continue
        p = _hecho(u, c, k)
        ceros = [0 for _ in range(i)]
        ceros.extend(u.cifras_de(p))
        parcial = u.escribir_cifras(ceros) if p else 0
        trozo = u.escribir_cifras([0 for _ in range(i)] + [c])
        lineas.append("%d x %d = %d   (%d x %d = %d, en las %s)" % (trozo, k, parcial, c, k, p, _SITIO[i]))
        parciales.append(parcial)
    total = 0
    for p in parciales:
        total = u.usar("sumar", a=total, b=p)["valor"]
    if u.decir(total) is None:
        raise ValueError("se sale de mi lista")
    partes = " + ".join(str(x) for x in reversed(parciales))
    return {"valor": total, "metodo": "partir por sitios (M.10)",
            "cuenta": "%s; los productos parciales se suman: %s = %d" % ("; ".join(reversed(lineas)), partes, total),
            "vuelta": "", "vuelta_ok": True}
