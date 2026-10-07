# -*- coding: utf-8 -*-
"""Pieza de HALLAR EL TODO SUMANDO LAS PARTES EN ORDEN (paso S.2; NCETM 1.28, punto 2).  'En muchos contextos
el todo se halla juntando las partes; se pueden usar estrategias distintas, pero la estructura es la misma.'
Partes 37, 25 y 63: 37 + 25 = 62; 62 + 63 = 125.  Las sumas (tambien con decimales, el punto en su sitio) las
hace la pregunta 'combinar' de M.16.  Se COMPRUEBA con la operacion contraria: al todo se le quitan las partes,
de la ultima a la primera, y tiene que quedar la primera (125 - 63 - 25 = 37)."""

PIEZA = {
    "id": "todo_sumando_en_orden",
    "nombre": "juntar las partes una detras de otra, en el orden en que vienen",
    "unidad": "S.2",
    "responde": "todo_de_las_partes",
    "rapidez": 20,
    "que_hace": "37, 25, 63 -> 37 + 25 = 62; 62 + 63 = 125",
    "condiciones": [
        ("se_saben_todas_las_partes", "no se saben todas las partes (o no hay dos o mas): no es buscar el todo"),
    ],
    "usa": ["combinar"],
}


def hacer(s, u):
    partes = [_normal(p) for p in s["partes"]]
    r = u.usar("combinar", terminos=[["+", [p]] for p in partes])
    todo = r["valor"]
    vuelta, ok = _quitar_de_la_ultima_a_la_primera(u, todo, partes)
    return {"valor": todo, "metodo": "juntar las partes en el orden en que vienen (NCETM 1.28, S.2)",
            "orden": partes, "pasos": r["resultado"]["pasos"], "vuelta": vuelta, "vuelta_ok": ok}


def _quitar_de_la_ultima_a_la_primera(u, todo, partes):
    """La operacion contraria: todo - la ultima - ... - la segunda tiene que dejar la primera."""
    terminos = [["+", [todo]]]
    terminos.extend(["-", [p]] for p in reversed(partes[1:]))
    texto = " - ".join([todo] + list(reversed(partes[1:])))
    try:
        queda = u.usar("combinar", terminos=terminos)["valor"]
    except Exception as e:
        return "%s: no se puede (%s)" % (texto, e), False
    bien = _normal(queda) == partes[0]
    return "%s = %s%s" % (texto, queda, "" if bien else " (y tenia que quedar %s)" % partes[0]), bien


def _normal(f):
    """'1.50' -> '1.5';  '007' -> '7'.  Es mirar las cifras, no calcular."""
    if "." in f:
        f = f.rstrip("0").rstrip(".")
    e, punto, d = f.partition(".")
    e = e.lstrip("0") or "0"
    return "%s.%s" % (e, d) if punto else e
