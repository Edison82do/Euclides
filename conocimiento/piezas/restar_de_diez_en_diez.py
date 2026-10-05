# -*- coding: utf-8 -*-
"""Pieza de calculo: RESTAR DE DIEZ EN DIEZ (paso 4).  77 - 30: desde el 77, tres saltos de diez
hacia atras: 67, 57, 47.  La cifra de las decenas pasa a la anterior; las unidades no se tocan."""

PIEZA = {
    "id": "restar_de_diez_en_diez",
    "nombre": "de diez en diez hacia atras",
    "unidad": "P.4",
    "responde": "restar",
    "rapidez": 5,
    "que_hace": "si lo que se quita son decenas justas (30, 40...), salta de diez en diez hacia atras",
    "condiciones": [
        ("el_segundo_son_decenas_justas", "lo que se quita no son decenas justas (30, 40 ... 90)"),
        ("el_de_abajo_no_es_mayor", "se quitaria mas de lo que hay (no hay restas negativas, 5.4)"),
    ],
    "usa": [],
}


def _saltos(p):
    return "un salto" if p == "uno" else "%s saltos" % p


def hacer(s, u):
    saltos = u.decir(u.cifras_de(s["b"])[1])
    v, camino, marca = s["a"], [], "cero"
    while marca != saltos:
        v = u.bajar_una_decena(v)
        if v is None:
            raise ValueError("no quedan decenas que quitar")
        camino.append(str(v))
        marca = u.siguiente(marca)
    w, marca = v, "cero"
    while marca != saltos:
        w = u.subir_una_decena(w)
        marca = u.siguiente(marca)
    return {"valor": v, "metodo": "de diez en diez hacia atras (P.4)",
            "cuenta": "%d - %d = %d  (%s de diez hacia atras desde %d: %s)"
            % (s["a"], s["b"], v, _saltos(saltos), s["a"], ", ".join(camino)),
            "vuelta": "%d + %d = %d  (%s hacia adelante)" % (v, s["b"], w, _saltos(saltos)),
            "vuelta_ok": w == s["a"]}
