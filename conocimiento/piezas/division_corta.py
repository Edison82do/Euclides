# -*- coding: utf-8 -*-
"""Pieza de DIVIDIR (paso M.11; NCETM 2.15; Common Core 4.NBT.B.6): LA DIVISION CORTA.  De IZQUIERDA a
DERECHA (al reves que la suma): en cada sitio, cuantas veces cabe el divisor (un hecho de la tabla que se
sabe); lo que SOBRA se CAMBIA por diez de la columna siguiente (1 decena = 10 unidades), como en la resta
por columnas (7.6).  Lo que sobra al final es el resto.
      72 : 3:  7 decenas : 3 -> 2 decenas (2 x 3 = 6), sobra 1 decena -> 10 unidades + 2 = 12 unidades;
               12 : 3 = 4  ->  24"""

PIEZA = {
    "id": "division_corta",
    "nombre": "la division corta (de izquierda a derecha, cambiando)",
    "unidad": "M.11",
    "responde": "dividir",
    "rapidez": 7,
    "que_hace": "en cada sitio cuantas veces cabe el divisor; lo que sobra se cambia por diez de la columna de al lado",
    "condiciones": [
        ("el_divisor_es_de_una_cifra_y_el_dividendo_de_varias", "el divisor no es de una cifra (2 a 9) o el dividendo no pasa de nueve"),
    ],
    "usa": ["multiplicar"],
}

_SITIO = ("unidades", "decenas", "centenas", "millares", "decenas de millar")


def _cuantas_veces(u, actual, d):
    """La mayor q (0..9) con q x d <= actual, mirando la tabla del d en la memoria.  (q, q x d)."""
    q, mejor = "cero", (0, 0)
    pa = u.decir(actual)
    while True:
        qq = u.leer(q)
        if qq == 0:
            p = 0
        elif qq == 1:
            p = d
        else:
            h = u.recuerdo("%d x %d" % (qq, d)) or u.recuerdo("%d x %d" % (d, qq))
            if not h:
                raise ValueError("no se de memoria %d x %d (primero hay que saberse las tablas)" % (qq, d))
            p = h["valor"]
        if p != actual and u.viene_despues(u.decir(p), pa):
            return mejor
        mejor = (qq, p)
        if q == "nueve":
            return mejor
        q = u.siguiente(q)


_UNO = {"unidades": "unidad", "decenas": "decena", "centenas": "centena", "millares": "millar",
        "decenas de millar": "decena de millar"}


def _n(n, sitio):
    return "%d %s" % (n, _UNO[sitio] if n == 1 else sitio)


def hacer(s, u):
    t, d = s["total"], s["divisor"]
    cif = list(reversed(u.cifras_de(t)))                     # de IZQUIERDA a derecha
    sitios = list(reversed(_SITIO[:len(cif)]))
    cociente, sobra, pasos, empezado, antes_sitio = [], 0, [], False, None
    for c, sitio in zip(cif, sitios):
        actual = u.escribir_cifras([c] + u.cifras_de(sobra)) if sobra else c
        q, p = _cuantas_veces(u, actual, d)
        resto = u.leer(u.contar_hasta(u.decir(p), u.decir(actual)))
        if sobra:
            pasos.append("sobra%s %s: se CAMBIA%s por %s, y con %s que hay son %s" % (
                "" if sobra == 1 else "n", _n(sobra, antes_sitio), "" if sobra == 1 else "N",
                _n(u.escribir_cifras([0] + u.cifras_de(sobra)), sitio), _n(c, sitio), _n(actual, sitio)))
        if q == 0 and not empezado:
            pasos.append("%s : %d -> no da ni una para cada uno: pasan a la columna siguiente" % (_n(actual, sitio), d))
        else:
            empezado = True
            pasos.append("%s : %d = %s (%d x %d = %d)%s" % (
                _n(actual, sitio), d, _n(q, sitio), q, d, p, ", sobra%s %d" % ("" if resto == 1 else "n", resto) if resto else ""))
            cociente.append(q)
        sobra, antes_sitio = resto, sitio
    q_total = u.escribir_cifras(list(reversed(cociente))) if cociente else 0
    # LA VUELTA: cociente x divisor + resto = dividendo
    m = u.usar("multiplicar", a=q_total, b=d)["valor"] if q_total else 0
    vuelta = u.sumar_por_columnas(m, sobra) if sobra else m
    escrito = "".join(str(x) for x in cociente) or "0"
    dibujo = ["      %s" % escrito.rjust(len(str(t))), "    --%s" % "".join("-" for _ in str(t)),
              "  %d | %d" % (d, t)]
    if sobra:
        pasos.append("al final sobra%s %d: es el RESTO" % ("" if sobra == 1 else "n", sobra))
    return {"valor": q_total, "resto": sobra, "metodo": "la division corta (M.11)",
            "cuenta": "%s; %s" % ("; ".join(dibujo), "; ".join(pasos)),
            "vuelta": "%d x %d%s = %d" % (q_total, d, " + %d" % sobra if sobra else "", vuelta),
            "vuelta_ok": vuelta == t}
