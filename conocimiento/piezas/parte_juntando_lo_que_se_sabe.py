# -*- coding: utf-8 -*-
"""Pieza de HALLAR LA PARTE QUE FALTA JUNTANDO PRIMERO LO QUE SE SABE (paso S.2; NCETM 1.28, punto 3: 'se
pueden usar estrategias distintas para calcular la parte que falta, pero la estructura es la misma').
Todo 100, partes 37, ? y 25: primero junto lo que se sabe, 37 + 25 = 62 (una suma, mas facil que restar dos
veces); luego UNA sola resta, 100 - 62 = 38.  Lo que se sabe lo junta la pregunta 'todo_de_las_partes' (asi
las parejas amigas tambien valen aqui).  Si lo que se sabe ya pasa del todo, no puede ser.  Se COMPRUEBA con
la operacion contraria: todas las partes, con la que salio, tienen que sumar el todo."""

PIEZA = {
    "id": "parte_juntando_lo_que_se_sabe",
    "nombre": "juntar primero las partes que se saben y quitarlas de una vez",
    "unidad": "S.2",
    "responde": "parte_del_todo",
    "rapidez": 12,
    "que_hace": "todo 100, partes 37, ?, 25 -> 37 + 25 = 62; 100 - 62 = 38",
    "condiciones": [
        ("falta_una_sola_parte", "no falta exactamente UNA parte de un todo que se sabe"),
        ("se_saben_dos_partes_o_mas", "solo se sabe una parte: es una sola resta, no hay nada que juntar"),
    ],
    "usa": ["todo_de_las_partes", "combinar"],
}


def hacer(s, u):
    todo = _normal(s["todo"])
    se_saben = [_normal(p) for p in s["partes"] if p is not None]
    j = u.usar("todo_de_las_partes", partes=se_saben)
    junto = j["valor"]
    pasos = ["junto lo que se sabe: %s" % p for p in j["resultado"]["pasos"]]
    try:
        r = u.usar("combinar", terminos=[["+", [todo]], ["-", [junto]]])
    except Exception as e:
        if "debajo del cero" in str(e):
            raise ValueError("no puede ser: las partes que se saben (%s) ya PASAN DEL TODO (%s)"
                             % (" + ".join(se_saben), todo))
        raise
    parte = r["valor"]
    pasos.extend("y lo quito de una vez: %s" % p for p in r["resultado"]["pasos"])
    vuelta, ok = _sumar_todas(u, s["partes"], parte, todo)
    return {"valor": parte, "metodo": "juntar lo que se sabe (%s) y quitarlo de una vez (NCETM 1.28, S.2)"
                                      % j["pieza"]["id"],
            "junto": junto, "pasos": pasos, "vuelta": vuelta, "vuelta_ok": ok}


def _sumar_todas(u, partes, parte, todo):
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
