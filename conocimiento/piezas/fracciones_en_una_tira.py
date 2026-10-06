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
        ("son_fracciones_unitarias", "no son las dos de 'uno' arriba (unitarias)"),
    ],
    "usa": ["multiplicar", "dividir"],
}


def hacer(s, u):
    da, db = s["a"][1], s["b"][1]
    if da == db:
        tira = da
    else:
        tira = u.usar("multiplicar", a=da, b=db)["valor"]
    ta = u.usar("dividir", total=tira, divisor=da)["valor"]
    tb = u.usar("dividir", total=tira, divisor=db)["valor"]
    if ta == tb:
        valor, dice = "=", "los dos trozos tienen lo mismo"
    elif u.viene_despues(u.decir(ta), u.decir(tb)):
        valor, dice = ">", "1/%d es mas grande" % da
    else:
        valor, dice = "<", "1/%d es mas grande" % db
    return {"valor": valor, "metodo": "la tira (F.1)",
            "cuenta": "una tira de %d cuadritos: 1/%d son %s y 1/%d son %s: %s"
                      % (tira, da, _cuadritos(ta), db, _cuadritos(tb), dice), "vuelta": "", "vuelta_ok": True}


def _cuadritos(n):
    return "1 cuadrito" if n == 1 else "%d cuadritos" % n
