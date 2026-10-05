# -*- coding: utf-8 -*-
"""Pieza de la BALANZA (paso E.2): calcular el plato COMPLETO (8 + 4 = 12) y entonces queda una
ecuacion de E.1 (12 = ? + 5), que resuelven las piezas de los problemas (R.1).  Es lo que hace quien
entiende que el = es 'es el mismo numero que': los dos platos valen lo mismo."""

PIEZA = {
    "id": "balanza_calculando_un_lado",
    "nombre": "calcular el plato completo",
    "unidad": "E.2",
    "responde": "balanza",
    "rapidez": 20,
    "que_hace": "calcula el lado sin hueco; el otro lado tiene que valer lo mismo (y eso es E.1)",
    "condiciones": [
        ("hay_un_plato_completo", "no hay un lado sin hueco"),
    ],
    "usa": ["sumar", "restar", "paso"],
}


def hacer(s, u):
    c, h = s["completo"], s["con_hueco"]
    r = u.usar("sumar" if c["op"] == "+" else "restar", a=c["a"], b=c["b"])
    total = r["valor"]
    if h["b"] == "?":
        sit = {"tipo": "cambio_desconocido", "antes": h["a"], "despues": total, "signo": h["op"]}
    else:
        sit = {"tipo": "deshacer", "despues": total, "signo": h["op"], "n": h["b"]}
    p = u.usar("paso", **sit)
    v = p["valor"]
    hueco = "%s %s %s" % ("?" if h["a"] == "?" else h["a"], h["op"], "?" if h["b"] == "?" else h["b"])
    return {"valor": v, "metodo": "calcular el plato completo (E.2)",
            "cuenta": "el plato completo: %d %s %d = %d (%s).  Entonces %s tiene que valer %d: %s (%s) -> %d"
                      % (c["a"], c["op"], c["b"], total, r["resultado"]["metodo"], hueco, total,
                         p["pieza"]["nombre"], p["resultado"]["resultado"]["cuenta"], v),
            "vuelta": "", "vuelta_ok": True}
