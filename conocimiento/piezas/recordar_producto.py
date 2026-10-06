# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso M.2): RECORDAR un producto de las tablas que ya se aprendio (aprender:
tablas).  Como con las sumas, se vuelve a comprobar: con la otra lectura de los grupos (si a x b, se
mira que b grupos de a den lo mismo).  Si no cuadra, no se usa."""

PIEZA = {
    "id": "recordar_producto",
    "nombre": "lo se de memoria",
    "unidad": "memoria",
    "responde": "multiplicar",
    "rapidez": 1,
    "que_hace": "si el producto ya lo aprendi (y lo comprobe), lo recuerdo",
    "condiciones": [
        ("se_permite_recordar", "se pidio hacerlo sin memoria"),
        ("el_producto_esta_en_la_memoria", "no lo tengo en la memoria (todavia no lo he aprendido)"),
    ],
    "usa": ["suma_de_iguales"],
}


def hacer(s, u):
    h = u.recuerdo("%d x %d" % (s["a"], s["b"]))
    otra = u.usar("suma_de_iguales", veces=s["b"], n=s["a"])        # la otra lectura: b grupos de a
    if otra["valor"] != h["valor"]:
        raise ValueError("el recuerdo %d x %d = %d NO cuadra con %d grupos de %d: no lo uso"
                         % (s["a"], s["b"], h["valor"], s["b"], s["a"]))
    return {"valor": h["valor"], "metodo": "de memoria (lo aprendi con %s, el %s)" % (h["como"], h["fecha"]),
            "cuenta": "%d x %d = %d" % (s["a"], s["b"], h["valor"]),
            "vuelta": "%d grupos de %d tambien son %d" % (s["b"], s["a"], otra["valor"]), "vuelta_ok": True}
