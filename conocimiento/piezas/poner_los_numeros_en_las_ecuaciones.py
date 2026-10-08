# -*- coding: utf-8 -*-
"""Pieza de COMPROBAR UNA SOLUCION DE DOS INCOGNITAS (paso S.3; NCETM 1.31).  Se ponen los numeros en el sitio de
las letras y se calcula cada ecuacion con el orden de siempre (la pregunta 'combinar', M.16): a = 19, b = 11 en
a + b = 30 da 19 + 11 = 30 (SI); en a - b = 8 da 19 - 11 = 8 (SI).  Es la comprobacion de todas las piezas de dos
incognitas: la cuenta de cada una se hace aqui, no en la pieza que encontro los numeros.
Su vuelta es la de cada cuenta: 'combinar' las deshace de la ultima a la primera con la operacion contraria."""

PIEZA = {
    "id": "poner_los_numeros_en_las_ecuaciones",
    "nombre": "poner los numeros en las letras y calcular cada ecuacion",
    "unidad": "S.3",
    "responde": "cumplen_las_ecuaciones",
    "rapidez": 10,
    "que_hace": "a = 19, b = 11:  19 + 11 = 30 SI;  19 - 11 = 8 SI",
    "condiciones": [
        ("hay_ecuaciones_y_un_numero_para_cada_letra", "no hay ecuaciones, o falta el numero de alguna letra"),
    ],
    "usa": ["combinar"],
}


def hacer(s, u):
    lineas, vueltas, todas, ok = [], [], True, True
    for eq in s["ecuaciones"]:
        texto, si, vuelta, bien = _una(u, eq, s["valores"])
        lineas.append("%s  ->  %s ... %s" % (eq["texto"], texto, "SI" if si else "NO"))
        vueltas.append(vuelta)
        todas = todas and si
        ok = ok and bien
    return {"valor": "si" if todas else "no", "metodo": "poner los numeros en las letras (NCETM 1.31)",
            "lineas": lineas, "pasos": lineas, "vuelta": "; ".join(v for v in vueltas if v), "vuelta_ok": ok}


def _una(u, eq, val):
    """(lo que se calcula, si cumple, la vuelta de la cuenta, si la vuelta cuadro)."""
    t = eq["tipo"]
    if t == "lineal":
        a, b = eq["letras"]
        terminos = [["+", _con_peso(eq["coef"][a], val[a])], ["+", _con_peso(eq["coef"][b], val[b])]]
        debe = eq["n"]
    elif t == "diferencia":
        terminos = [["+", [val[eq["mayor"]]]], ["-", [val[eq["menor"]]]]]
        debe = eq["n"]
    elif t == "multiplo":
        terminos = [["+", [eq["k"], val[eq["chico"]]]]]
        debe = val[eq["grande"]]
    else:                                                  # producto
        a, b = eq["letras"]
        terminos = [["+", [val[a], val[b]]]]
        debe = eq["n"]
    escrito = _escrito(terminos)
    try:
        r = u.usar("combinar", terminos=terminos)
    except Exception as e:
        return "%s no se puede (%s)" % (escrito, str(e).split(":")[0]), False, "", True
    v = _normal(r["valor"])
    si = v == _normal(debe)
    texto = "%s = %s%s" % (escrito, v, "" if si else " (y tiene que ser %s)" % _normal(debe))
    return texto, si, r["resultado"]["vuelta"], r["resultado"]["vuelta_ok"]


def _con_peso(peso, v):
    return [v] if peso == "1" else [peso, v]


def _escrito(terminos):
    trozos = []
    for k, (signo, fs) in enumerate(terminos):
        t = " x ".join(fs)
        trozos.append(t if not k else "%s %s" % (signo, t))
    return " ".join(trozos)


def _normal(f):
    if "." in f:
        f = f.rstrip("0").rstrip(".")
    e, punto, d = f.partition(".")
    e = e.lstrip("0") or "0"
    return "%s.%s" % (e, d) if punto else e
