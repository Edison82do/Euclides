# -*- coding: utf-8 -*-
"""Pieza de calculo: RECORDAR una suma que ya se sabe DE MEMORIA (paso 3 del plan).
La memoria se GANA (memoria.py): solo esta lo que el sistema calculo y comprobo antes.  Y al usar
un recuerdo se vuelve a comprobar por la vuelta: si no cuadra, NO se usa (no sale, y el motor
pasa al metodo siguiente)."""

PIEZA = {
    "id": "recordar_suma",
    "nombre": "lo se de memoria",
    "unidad": "memoria",
    "responde": "sumar",
    "rapidez": 1,
    "que_hace": "si la suma ya la aprendi (y la comprobe), la recuerdo",
    "condiciones": [
        ("se_permite_recordar", "se pidio hacerlo sin memoria (para aprender, o para ver el camino largo)"),
        ("la_suma_esta_en_la_memoria", "no la tengo en la memoria (todavia no la he aprendido)"),
    ],
    "usa": [],
}


def hacer(s, u):
    h = u.recuerdo("%d + %d" % (s["a"], s["b"]))
    v = h["valor"]
    # LA VUELTA, contando: un recuerdo que no cuadra no se usa
    vuelta = u.contar_atras(u.decir(v), u.decir(s["b"]))
    if vuelta.get("resultado") != u.decir(s["a"]):
        raise ValueError("el recuerdo %d + %d = %d NO cuadra al comprobarlo: no lo uso" % (s["a"], s["b"], v))
    return {"valor": v, "metodo": "de memoria (lo aprendi con %s, el %s)" % (h["como"], h["fecha"]),
            "cuenta": "%d + %d = %d" % (s["a"], s["b"], v),
            "vuelta": "%s - %s = %s" % (u.decir(v), u.decir(s["b"]), vuelta.get("resultado")),
            "vuelta_ok": True}
