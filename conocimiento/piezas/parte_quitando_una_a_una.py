# -*- coding: utf-8 -*-
"""Pieza de HALLAR LA PARTE QUE FALTA QUITANDO LAS PARTES UNA A UNA (paso S.2; NCETM 1.28, punto 3: 'si se sabe
el todo y todas las partes menos una, la que falta se puede calcular').  Todo 100, partes 37, ? y 25:
100 - 37 = 63; 63 - 25 = 38.  Las restas (con el punto en su sitio) las hace 'combinar' (M.16).  Si por el
camino me bajo de cero, las partes que se saben ya PASAN DEL TODO: no puede ser.  Se COMPRUEBA con la
operacion contraria: todas las partes, con la que salio, tienen que sumar el todo (37 + 38 + 25 = 100)."""

PIEZA = {
    "id": "parte_quitando_una_a_una",
    "nombre": "quitar del todo las partes que se saben, una a una",
    "unidad": "S.2",
    "responde": "parte_del_todo",
    "rapidez": 20,
    "que_hace": "todo 100, partes 37, ?, 25 -> 100 - 37 = 63; 63 - 25 = 38",
    "condiciones": [
        ("falta_una_sola_parte", "no falta exactamente UNA parte de un todo que se sabe"),
    ],
    "usa": ["combinar"],
}


def hacer(s, u):
    todo = _normal(s["todo"])
    se_saben = [_normal(p) for p in s["partes"] if p is not None]
    terminos = [["+", [todo]]]
    terminos.extend(["-", [p]] for p in se_saben)
    try:
        r = u.usar("combinar", terminos=terminos)
    except Exception as e:
        if "debajo del cero" in str(e):
            raise ValueError("no puede ser: las partes que se saben (%s) ya PASAN DEL TODO (%s)"
                             % (", ".join(se_saben), todo))
        raise
    parte = r["valor"]
    vuelta, ok = _sumar_todas(u, s["partes"], parte, todo)
    return {"valor": parte, "metodo": "quitar del todo las partes que se saben, una a una (NCETM 1.28, S.2)",
            "pasos": r["resultado"]["pasos"], "vuelta": vuelta, "vuelta_ok": ok}


def _sumar_todas(u, partes, parte, todo):
    """La contraria: las partes, con la que salio en su sitio, tienen que juntar el todo."""
    todas = [parte if p is None else _normal(p) for p in partes]
    try:
        v = u.usar("combinar", terminos=[["+", [p]] for p in todas])["valor"]
    except Exception as e:
        return "%s: no se puede (%s)" % (" + ".join(todas), e), False
    bien = _normal(v) == todo
    return "%s = %s%s" % (" + ".join(todas), v, "" if bien else " (y tenia que dar %s)" % todo), bien


def _normal(f):
    if "." in f:
        f = f.rstrip("0").rstrip(".")
    e, punto, d = f.partition(".")
    e = e.lstrip("0") or "0"
    return "%s.%s" % (e, d) if punto else e
