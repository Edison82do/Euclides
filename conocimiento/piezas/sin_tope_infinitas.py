# -*- coding: utf-8 -*-
"""Pieza de UNA RELACION SOLA: INFINITAS (paso S.3; NCETM 1.31, puntos 1 y 5).  a - b = 3 o a = 3 x b, solas, no
ponen ningun tope: para CUALQUIER b hay una a (b = 0, a = 3; b = 1, a = 4; b = 2, a = 5 ...): infinitas soluciones,
aun con enteros.  Para saber cuanto vale cada una hace falta otra cosa (la suma, por ejemplo).
Se COMPRUEBA poniendo tres ejemplos en la ecuacion."""

PIEZA = {
    "id": "sin_tope_infinitas",
    "nombre": "una relacion sola: para cada una hay otra (infinitas)",
    "unidad": "S.3",
    "responde": "dos_incognitas",
    "rapidez": 5,
    "que_hace": "a - b = 3:  b = 0, a = 3;  b = 1, a = 4;  b = 2, a = 5 ...  (infinitas)",
    "condiciones": [
        ("es_una_relacion_sola", "no es una relacion sola (una diferencia o un multiplo)"),
    ],
    "usa": ["combinar", "cumplen_las_ecuaciones"],
}


def hacer(s, u):
    eq = s["ecuaciones"][0]
    if eq["tipo"] == "diferencia":
        chica, grande = eq["menor"], eq["mayor"]
        de = lambda v: _cuenta(u, [["+", [v]], ["+", [eq["n"]]]])
        dice = "%s es %s y %s mas" % (grande, chica, eq["n"])
    else:
        chica, grande = eq["chico"], eq["grande"]
        de = lambda v: _cuenta(u, [["+", [eq["k"], v]]])
        dice = "%s es %s veces %s" % (grande, eq["k"], chica)
    ejemplos = []
    for v in ("0", "1", "2"):
        ejemplos.append({chica: v, grande: de(v)})
    pasos = ["%s, y nada mas: para CUALQUIER %s hay una %s" % (dice, chica, grande),
             "; ".join("%s = %s, %s = %s" % (chica, e[chica], grande, e[grande]) for e in ejemplos) + " ...",
             "no hay tope: INFINITAS, aun con enteros (para saber cuanto vale cada una hace falta otro dato)"]
    trozos, ok = [], True
    for e in ejemplos:
        t, bien = _comprobar(u, s, e)
        trozos.append(t)
        ok = ok and bien
    return {"valor": "infinitas", "soluciones": [], "ejemplos": ejemplos, "cuantas": "infinitas",
            "metodo": "una relacion sola no pone tope (NCETM 1.31, punto 1)", "pasos": pasos,
            "vuelta": "; ".join(trozos), "vuelta_ok": ok}


def _comprobar(u, s, valores):
    r = u.usar("cumplen_las_ecuaciones", ecuaciones=s["ecuaciones"], valores=valores)
    return "; ".join(r["resultado"]["lineas"]), r["valor"] == "si" and r["resultado"]["vuelta_ok"]


def _cuenta(u, terminos):
    try:
        return _normal(u.usar("combinar", terminos=terminos)["valor"])
    except Exception as e:                          # 'combinar' no sale (por debajo del cero, o se pasa del techo)
        raise ValueError(str(e))


def _n(u, f):
    """'175' -> 175: LEER las cifras de un entero escrito."""
    return u.escribir_cifras([int(c) for c in reversed(f)])


def _normal(f):
    if "." in f:
        f = f.rstrip("0").rstrip(".")
    e, punto, d = f.partition(".")
    e = e.lstrip("0") or "0"
    return "%s.%s" % (e, d) if punto else e
