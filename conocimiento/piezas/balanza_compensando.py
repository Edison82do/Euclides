# -*- coding: utf-8 -*-
"""Pieza de la BALANZA (paso E.2): COMPENSAR sin calcular los lados.  8 + 4 = ? + 5: el 5 es UNO MAS
que el 4, asi que el hueco tiene que ser UNO MENOS que el 8: 7.  Lo que se pone de mas en un sitio
se quita en el otro, y la balanza sigue igual (NCETM 1.29; Carpenter et al.: 57 + 22 = ? + 21).
Solo cuenta la diferencia pequena (con los dedos); los lados no se calculan."""

PIEZA = {
    "id": "balanza_compensando",
    "nombre": "compensar (lo que sube en un sitio, baja en el otro)",
    "unidad": "E.2",
    "responde": "balanza",
    "rapidez": 5,
    "que_hace": "compara el numero conocido con su pareja del otro lado y mueve el hueco al reves",
    "condiciones": [
        ("los_dos_lados_son_sumas", "no son dos sumas (en la resta la compensacion va de otra manera)"),
        ("hay_una_pareja_cerca", "ningun numero del otro lado esta cerca del conocido (no caben en los dedos)"),
    ],
    "usa": [],
}


def hacer(s, u):
    c, h = s["completo"], s["con_hueco"]
    k = h["a"] if h["b"] == "?" else h["b"]
    for p, otro in ((c["b"], c["a"]), (c["a"], c["b"])):
        if u.viene_despues(u.decir(k), u.decir(p)):
            d = u.contar_hasta(u.decir(p), u.decir(k))
            mas = True
        else:
            d = u.contar_hasta(u.decir(k), u.decir(p))
            mas = False
        if d is not None and u.levantar_dedos(d) is not None:
            break
    if mas:
        r = u.contar_atras(u.decir(otro), d)
        frase = "%d es %s mas que %d; para que la balanza siga igual, el hueco es %s MENOS que %d: %d  (sin calcular los lados)"
    else:
        r = u.contar_adelante(u.decir(otro), d)
        frase = "%d es %s menos que %d; para que la balanza siga igual, el hueco es %s MAS que %d: %d  (sin calcular los lados)"
    if r.get("resultado") is None:
        raise ValueError("no hay numero: el otro plato ya pesa mas")
    v = u.leer(r["resultado"])
    return {"valor": v, "metodo": "compensar (E.2)",
            "cuenta": frase % (k, d, p, d, otro, v),
            "vuelta": "", "vuelta_ok": True}
