# -*- coding: utf-8 -*-
"""Pieza de la BALANZA (paso E.2): si los dos platos tienen el MISMO numero, lo demas tiene que pesar
igual.  8 + 4 = 8 + ?  -> 4, sin calcular.  En la resta: 12 - 5 = 12 - ? -> 5;  ? - 3 = 9 - 3 -> 9.
Es pensamiento relacional (Carpenter et al.): mirar la relacion, no hacer la cuenta."""

PIEZA = {
    "id": "balanza_mismo_numero",
    "nombre": "los dos platos tienen un numero igual",
    "unidad": "E.2",
    "responde": "balanza",
    "rapidez": 1,
    "que_hace": "si los dos lados comparten un numero, lo que queda tiene que ser igual (sin calcular)",
    "condiciones": [
        ("comparten_un_numero", "los dos lados no comparten un numero en el mismo papel"),
    ],
    "usa": [],
}


def hacer(s, u):
    c, h = s["completo"], s["con_hueco"]
    if c["op"] == "+":
        k = h["a"] if h["b"] == "?" else h["b"]
        v = c["b"] if c["a"] == k else c["a"]
        porque = ("los dos lados tienen un %d; para que pesen lo mismo, lo otro tiene que ser igual: %d"
                  % (k, v))
    elif h["b"] == "?":
        v, porque = c["b"], ("los dos lados empiezan en %d; para que quede lo mismo, hay que quitar "
                             "lo mismo: %d" % (c["a"], c["b"]))
    else:
        v, porque = c["a"], ("a los dos lados se quita %d; para que quede lo mismo, hay que empezar "
                             "en lo mismo: %d" % (c["b"], c["a"]))
    return {"valor": v, "metodo": "un numero igual en los dos platos (E.2)",
            "cuenta": porque + "  (sin calcular)", "vuelta": "", "vuelta_ok": True}
