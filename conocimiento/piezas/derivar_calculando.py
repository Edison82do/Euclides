# -*- coding: utf-8 -*-
"""Pieza de DERIVAR (paso P.7): no usar el hecho que se sabe y hacer la cuenta nueva entera.  Siempre
sirve (si la cuenta se puede), pero es mas largo: NCETM 1.29 pide 'mirar primero si se puede compensar
y solo calcular si no'."""

PIEZA = {
    "id": "derivar_calculando",
    "nombre": "hacer la cuenta nueva entera",
    "unidad": "P.7",
    "responde": "derivar",
    "rapidez": 20,
    "que_hace": "hago la cuenta nueva sin mirar la que se sabe",
    "condiciones": [
        ("la_cuenta_nueva_es_suma_o_resta", "la cuenta nueva no es una suma ni una resta"),
    ],
    "usa": ["sumar", "restar"],
}


def hacer(s, u):
    n = s["nuevo"]
    if n["op"] == "-" and u.viene_despues(u.decir(n["b"]), u.decir(n["a"])):
        raise ValueError("se quitaria mas de lo que hay (no hay restas negativas, 5.4)")
    otra = "restar" if n["op"] == "+" else "sumar"
    w = u.usar("sumar" if n["op"] == "+" else "restar", a=n["a"], b=n["b"])
    v = w["valor"]
    k = u.usar(otra, a=v, b=n["b"])["valor"]
    return {"valor": v, "metodo": "hacer la cuenta entera",
            "cuenta": "%d %s %d = %d (%s)" % (n["a"], n["op"], n["b"], v, w["resultado"]["metodo"]),
            "vuelta": "%d %s %d = %d" % (v, "-" if n["op"] == "+" else "+", n["b"], k),
            "vuelta_ok": k == n["a"]}
