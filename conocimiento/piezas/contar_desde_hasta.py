# -*- coding: utf-8 -*-
"""Pieza de calculo: CONTAR DESDE UN NUMERO HASTA OTRO (unidad 5.5: el hueco se cuenta hacia
adelante).  Es como los ninos resuelven 'tenia 5, ahora tiene 8, cuantos le dieron?'."""

PIEZA = {
    "id": "contar_desde_hasta",
    "nombre": "contar desde el uno hasta el otro",
    "unidad": "5.5",
    "responde": "contar_hasta",
    "rapidez": 20,
    "que_hace": "desde el primero se cuenta hacia adelante hasta el segundo; los pasos son la respuesta",
    "condiciones": [
        ("el_segundo_no_es_menor", "el segundo es menor: contando hacia adelante no se llega"),
    ],
    "usa": [],
}


def hacer(s, u):
    # (aqui 'a' es DESDE y 'b' HASTA; la condicion mira que b no sea menor que a)
    pasos = u.contar_hasta(u.decir(s["a"]), u.decir(s["b"]))
    v = u.contar_adelante(u.decir(s["a"]), pasos, con_dedos=False)
    return {"valor": u.leer(pasos), "metodo": "contar (5.5)",
            "cuenta": "de %d a %d hay %d pasos" % (s["a"], s["b"], u.leer(pasos)),
            "vuelta": "%d + %d = %s" % (s["a"], u.leer(pasos), u.leer(v.get("resultado"))),
            "vuelta_ok": v.get("resultado") == u.decir(s["b"])}
