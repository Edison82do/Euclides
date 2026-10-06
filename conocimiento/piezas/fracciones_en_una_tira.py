# -*- coding: utf-8 -*-
"""Pieza de COMPARAR FRACCIONES (paso F.1; NCETM 3.1 'el tamano de las partes se puede comparar'): lo
CONCRETO.  Se imagina una tira que se pueda partir en las dos maneras (de a x b cuadritos), se reparte
de las dos maneras (M.3) y se cuentan los cuadritos de cada trozo.  El que tiene mas cuadritos es mayor."""

PIEZA = {
    "id": "fracciones_en_una_tira",
    "nombre": "en una tira de cuadritos",
    "unidad": "F.1",
    "responde": "comparar_fracciones",
    "rapidez": 9,
    "que_hace": "una tira de a x b cuadritos, partida de las dos maneras: se comparan los trozos",
    "condiciones": [
        ("comparten_arriba_o_abajo", "arriba y abajo son distintos en las dos (eso es de 5.o: equivalentes)"),
    ],
    "usa": ["multiplicar", "dividir"],
}


def hacer(s, u):
    da, db = s["a"][1], s["b"][1]
    if da == db:
        tira = da
    else:
        tira = u.usar("multiplicar", a=da, b=db)["valor"]
    ta = _trozo(u, tira, s["a"])
    tb = _trozo(u, tira, s["b"])
    if ta == tb:
        valor, dice = "=", "los dos trozos tienen lo mismo"
    elif u.viene_despues(u.decir(ta), u.decir(tb)):
        valor, dice = ">", "%d/%d es mas grande" % s["a"]
    else:
        valor, dice = "<", "%d/%d es mas grande" % s["b"]
    return {"valor": valor, "metodo": "la tira (F.1)",
            "cuenta": "una tira de %d cuadritos: %d/%d son %s y %d/%d son %s: %s"
                      % (tira, s["a"][0], da, _cuadritos(ta), s["b"][0], db, _cuadritos(tb), dice),
            "vuelta": "", "vuelta_ok": True}


def _cuadritos(n):
    return "1 cuadrito" if n == 1 else "%d cuadritos" % n


def _trozo(u, tira, f):
    """a/b de la tira: se reparte en b y se toman a partes."""
    una = u.usar("dividir", total=tira, divisor=f[1])["valor"]
    if f[0] == 1:
        return una
    return u.usar("multiplicar", a=f[0], b=una)["valor"]
