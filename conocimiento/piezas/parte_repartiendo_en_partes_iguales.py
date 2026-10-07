# -*- coding: utf-8 -*-
"""Pieza de HALLAR LAS PARTES CUANDO SON IGUALES (paso S.2; NCETM 1.28, punto 1: la estructura parte-parte-todo
tambien es MULTIPLICATIVA).  Todo 24 en 4 partes iguales (?, ?, ?, ?): se cuentan las partes recitando y se
REPARTE, 24 : 4 = 6 (M.3).  Si no sale justo, se cambia a la unidad mas pequena como en M.13 (26 : 4 = 6.5);
si ni asi, no salen partes iguales.  Se COMPRUEBA con la operacion contraria: 4 x 6 = 24."""

PIEZA = {
    "id": "parte_repartiendo_en_partes_iguales",
    "nombre": "partes iguales que faltan: repartir el todo",
    "unidad": "S.2",
    "responde": "parte_del_todo",
    "rapidez": 10,
    "que_hace": "todo 24 en ?, ?, ?, ? iguales -> 24 : 4 = 6",
    "condiciones": [
        ("faltan_todas_y_son_iguales", "no faltan todas las partes siendo iguales"),
    ],
    "usa": ["dividir", "dividir_decimal", "multiplicar", "multiplicar_decimal"],
}


def hacer(s, u):
    todo = _normal(s["todo"])
    palabra = "cero"
    for _ in s["partes"]:                    # contar las partes recitando
        palabra = u.siguiente(palabra)
    n = u.leer(palabra)
    como = None
    if "." not in todo:
        r = u.usar("dividir", total=_n(u, todo), divisor=n)
        if not r["resultado"].get("resto"):
            parte, como = "%d" % r["valor"], r["resultado"].get("metodo", "")
    if como is None:
        try:
            r = u.usar("dividir_decimal", x=todo, d="%d" % n)
        except Exception as e:
            raise ValueError("no salen %s partes iguales justas de %s: %s" % (palabra, todo, e))
        parte, como = _normal(r["valor"]), r["resultado"].get("metodo", "")
    paso = "%s en %s partes IGUALES: lo reparto, %s : %d = %s  (%s)" % (todo, palabra, todo, n, parte, como)
    vuelta, ok = _juntar(u, n, parte, todo)
    return {"valor": parte, "metodo": "repartir el todo en partes iguales (NCETM 1.28, punto 1; S.2)",
            "cuantas": n, "pasos": [paso], "vuelta": vuelta, "vuelta_ok": ok}


def _juntar(u, n, parte, todo):
    """La contraria: cuantas son x lo que vale una tiene que dar el todo."""
    if "." in parte:
        v = _normal(u.usar("multiplicar_decimal", x=parte, y="%d" % n)["valor"])
    else:
        v = "%d" % u.usar("multiplicar", a=n, b=_n(u, parte))["valor"]
    bien = v == todo
    return "%d x %s = %s%s" % (n, parte, v, "" if bien else " (y tenia que dar %s)" % todo), bien


def _n(u, f):
    return u.escribir_cifras([int(c) for c in reversed(f)])


def _normal(f):
    if "." in f:
        f = f.rstrip("0").rstrip(".")
    e, punto, d = f.partition(".")
    e = e.lstrip("0") or "0"
    return "%s.%s" % (e, d) if punto else e
