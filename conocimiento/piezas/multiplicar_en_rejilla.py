# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso N.4; Common Core 4.NBT.B.5: 'multiply two two-digit numbers, using
strategies based on place value and the properties of operations ... rectangular arrays, and/or area
models'; NCETM 2.14 punto 3): LA REJILLA (el modelo de area).
18 x 38: se parten LOS DOS por sitios, 18 = 10 + 8 y 38 = 30 + 8, y se hace una rejilla:
     x  | 30   8
    10  | 300  80
     8  | 240  64      y se suman las cuatro casillas: 300 + 80 + 240 + 64 = 684.
Cada casilla es un hecho de la tabla (1 x 3, 8 x 8...) con las cifras subidas de sitio (M.9)."""

PIEZA = {
    "id": "multiplicar_en_rejilla",
    "nombre": "la rejilla (partir los dos por sitios, el modelo de area)",
    "unidad": "N.4",
    "responde": "multiplicar",
    "rapidez": 10,
    "que_hace": "parte los dos factores por sitios, multiplica casilla a casilla y suma las casillas",
    "condiciones": [
        ("los_dos_factores_de_varias_cifras", "no son dos numeros de varias cifras"),
    ],
    "usa": ["sumar", "suma_de_iguales"],
}


def _hecho(u, x, k):
    """Un hecho de una cifra por una cifra: de memoria (las tablas); si no, con la suma de iguales."""
    if x == 0 or k == 0:
        return 0
    if x == 1:
        return k
    if k == 1:
        return x
    h = u.recuerdo("%d x %d" % (x, k)) or u.recuerdo("%d x %d" % (k, x))
    if h:
        return h["valor"]
    return u.usar("suma_de_iguales", veces=x, n=k)["valor"]


def _subir(u, cifra, ceros):
    """La cifra subida de sitio: se escriben 'ceros' ceros a su derecha (M.9)."""
    cs = [0 for _ in range(ceros)]
    cs.extend(u.cifras_de(cifra))
    return u.escribir_cifras(cs)


def hacer(s, u):
    a, b = s["a"], s["b"]
    casillas, lineas = [], []
    for i, c in enumerate(u.cifras_de(a)):
        if c == 0:
            continue
        fila = _subir(u, c, i)
        for j, d in enumerate(u.cifras_de(b)):
            if d == 0:
                continue
            col = _subir(u, d, j)
            p = _hecho(u, c, d)
            sitios = [0 for _ in range(i)]
            sitios.extend([0 for _ in range(j)])
            sitios.extend(u.cifras_de(p))
            casilla = u.escribir_cifras(sitios) if p else 0
            lineas.append("%d x %d = %d (%d x %d = %d)" % (fila, col, casilla, c, d, p))
            casillas.append(casilla)
    total = 0
    for p in casillas:
        try:
            total = u.usar("sumar", a=total, b=p)["valor"]
        except KeyError:
            raise ValueError("la suma de las casillas se sale de mi lista")
    if u.decir(total) is None:
        raise ValueError("se sale de mi lista")
    lineas.reverse()                                       # se lee de las grandes a las pequenas
    partes = " + ".join(str(x) for x in reversed(casillas))
    return {"valor": total, "metodo": "la rejilla (N.4)",
            "cuenta": "parto los dos por sitios; casilla a casilla: %s; sumo las casillas: %s = %d"
                      % ("; ".join(lineas), partes, total),
            "vuelta": "", "vuelta_ok": True}
