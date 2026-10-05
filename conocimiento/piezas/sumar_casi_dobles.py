# -*- coding: utf-8 -*-
"""Pieza de calculo: CASI DOBLES (paso 4).  6 + 7: el doble 6 + 6 = 12 lo se de memoria, y el 7
es UNO mas que el 6, asi que es uno mas: 13.  Es un HECHO DERIVADO (Baroody, fase 2: razonar a
partir de lo que ya se sabe).  Por eso solo encaja si el doble YA esta en la memoria: los dobles
son de los primeros hechos que se aprenden."""

PIEZA = {
    "id": "sumar_casi_dobles",
    "nombre": "casi dobles",
    "unidad": "P.4",
    "responde": "sumar",
    "rapidez": 8,
    "que_hace": "si uno es el siguiente del otro (6 y 7), hago el doble del menor y digo el siguiente",
    "condiciones": [
        ("los_dos_son_de_una_cifra", "no son los dos de una cifra"),
        ("son_casi_dobles", "no son casi dobles (uno no es el siguiente del otro)"),
        ("el_doble_lo_se_de_memoria", "el doble no lo se de memoria todavia"),
    ],
    "usa": [],
}


def hacer(s, u):
    m = s["b"] if u.viene_despues(u.decir(s["a"]), u.decir(s["b"])) else s["a"]
    doble = u.recuerdo("%d + %d" % (m, m))["valor"]
    v = u.leer(u.siguiente(u.decir(doble)))           # uno mas que el doble
    vuelta = u.contar_atras(u.decir(v), u.decir(s["b"]))
    return {"valor": v, "metodo": "casi dobles (P.4)",
            "cuenta": "%d + %d = %d  (el doble %d + %d = %d lo se de memoria; uno mas: %d)"
            % (s["a"], s["b"], v, m, m, doble, v),
            "vuelta": "%s - %s = %s" % (u.decir(v), u.decir(s["b"]), vuelta.get("resultado")),
            "vuelta_ok": vuelta.get("resultado") == u.decir(s["a"])}
