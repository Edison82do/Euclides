# -*- coding: utf-8 -*-
"""Pieza de calculo: RESTAR COMPENSANDO (paso 4).  52 - 29: quitar 29 es quitar 30 y devolver
uno.  52 - 30 = 22 (de diez en diez hacia atras), y le devuelvo el uno que quite de mas: 23."""

PIEZA = {
    "id": "restar_compensando",
    "nombre": "compensar (quitar de mas y devolver)",
    "unidad": "P.4",
    "responde": "restar",
    "rapidez": 6,
    "que_hace": "si lo que se quita acaba en nueve (29), quito la decena justa (30) y devuelvo uno",
    "condiciones": [
        ("el_de_abajo_no_es_mayor", "se quitaria mas de lo que hay (no hay restas negativas, 5.4)"),
        ("el_de_abajo_acaba_en_nueve", "lo que se quita no es de dos cifras acabado en nueve (19 ... 89)"),
        ("el_de_arriba_llega_a_la_decena", "el de arriba no llega a la decena justa: no se puede quitar de mas"),
    ],
    "usa": ["restar_de_diez_en_diez"],
}


def hacer(s, u):
    redondo = u.leer(u.siguiente(u.decir(s["b"])))    # 29 -> 30: quito uno de mas
    r = u.usar("restar_de_diez_en_diez", a=s["a"], b=redondo)
    v = u.leer(u.siguiente(u.decir(r["valor"])))      # y lo devuelvo
    vuelta = u.contar_adelante(u.decir(v), u.decir(s["b"]), con_dedos=False)
    return {"valor": v, "metodo": "compensar (P.4)",
            "cuenta": "%d - %d = %d  (quito %d en vez de %d: %s; devuelvo el uno de mas)"
            % (s["a"], s["b"], v, redondo, s["b"], r["resultado"]["cuenta"]),
            "vuelta": "%s + %s = %s" % (u.decir(v), u.decir(s["b"]), vuelta.get("resultado")),
            "vuelta_ok": vuelta.get("resultado") == u.decir(s["a"])}
