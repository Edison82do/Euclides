# -*- coding: utf-8 -*-
"""Pieza de HALLAR EL TODO CUANDO LAS PARTES SON IGUALES (paso S.2; NCETM 1.28, punto 1: 'las relaciones son
aditivas o MULTIPLICATIVAS; las dos se ven en la estructura parte-parte-todo').  Partes 6, 6, 6, 6: son 4
partes iguales de 6 (se cuentan recitando: una, dos, tres, cuatro), y el todo es 4 x 6 = 24.  Con un decimal,
la multiplicacion de M.13 (2.5, 2.5, 2.5 -> 3 x 2.5 = 7.5).  Se COMPRUEBA con la operacion contraria:
repartir el todo en esas partes (24 : 4 = 6); si eso no se puede (pide la division larga), sumando las partes."""

PIEZA = {
    "id": "todo_por_partes_iguales",
    "nombre": "partes iguales: cuantas son por lo que vale una",
    "unidad": "S.2",
    "responde": "todo_de_las_partes",
    "rapidez": 6,
    "que_hace": "6, 6, 6, 6 -> 4 partes iguales de 6 -> 4 x 6 = 24",
    "condiciones": [
        ("se_saben_todas_las_partes", "no se saben todas las partes: no es buscar el todo"),
        ("todas_las_partes_son_iguales", "las partes no son todas iguales"),
    ],
    "usa": ["multiplicar", "multiplicar_decimal", "dividir", "dividir_decimal", "combinar"],
}


def hacer(s, u):
    partes = [_normal(p) for p in s["partes"]]
    una = partes[0]
    palabra = "cero"
    for _ in partes:                         # contar las partes recitando
        palabra = u.siguiente(palabra)
    n = u.leer(palabra)
    if "." in una:
        r = u.usar("multiplicar_decimal", x=una, y="%d" % n)
        todo = _normal(r["valor"])
    else:
        r = u.usar("multiplicar", a=n, b=_n(u, una))
        if u.decir(r["valor"]) is None:
            raise ValueError("se pasa del millon: %d x %s no tiene nombre en mi lista" % (n, una))
        todo = "%d" % r["valor"]
    paso = "%s: son %s partes IGUALES de %s -> %d x %s = %s  (%s)" % (
        ", ".join(partes), palabra, una, n, una, todo, r["resultado"]["metodo"])
    vuelta, ok = _repartir(u, todo, n, una, partes)
    return {"valor": todo, "metodo": "partes iguales: cuantas son x lo que vale una (NCETM 1.28, punto 1; S.2)",
            "orden": partes, "cuantas": n, "pasos": [paso], "vuelta": vuelta, "vuelta_ok": ok}


def _repartir(u, todo, n, una, partes):
    """La contraria: el todo entre cuantas son tiene que dar una parte."""
    try:
        if "." in todo or "." in una:
            q = _normal(u.usar("dividir_decimal", x=todo, d="%d" % n)["valor"])
        else:
            r = u.usar("dividir", total=_n(u, todo), divisor=n)
            if r["resultado"].get("resto"):
                raise ValueError("sobra algo")
            q = "%d" % r["valor"]
        bien = q == una
        return "%s : %d = %s%s" % (todo, n, q, "" if bien else " (y tenia que dar %s)" % una), bien
    except Exception:
        pass
    v = u.usar("combinar", terminos=[["+", [p]] for p in partes])["valor"]   # no se puede repartir: sumando
    bien = _normal(v) == todo
    return "%s = %s (repartir no me sale: lo sumo)%s" % (" + ".join(partes), v, "" if bien else " y NO da %s" % todo), bien


def _n(u, f):
    """'175' -> 175: LEER las cifras de un entero escrito."""
    return u.escribir_cifras([int(c) for c in reversed(f)])


def _normal(f):
    if "." in f:
        f = f.rstrip("0").rstrip(".")
    e, punto, d = f.partition(".")
    e = e.lstrip("0") or "0"
    return "%s.%s" % (e, d) if punto else e
