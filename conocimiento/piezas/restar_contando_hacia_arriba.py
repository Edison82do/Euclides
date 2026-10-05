# -*- coding: utf-8 -*-
"""Pieza de calculo: RESTAR CONTANDO HACIA ARRIBA (paso P.6; Common Core 1.OA.B.4: la resta es un
problema de SUMANDO DESCONOCIDO).  13 - 8: cuanto le falta al 8 para llegar al 13?  Se cuenta
desde el 8 hacia arriba: 9, 10, 11, 12, 13 -> cinco dedos.  Porque 8 + 5 = 13.
La Progression de Common Core: contar hacia arriba para restar es mas facil que hacia atras.
Pero solo conviene si los numeros estan CERCA; si se quita poco (13 - 2), hacia atras es mas corto."""

PIEZA = {
    "id": "restar_contando_hacia_arriba",
    "nombre": "contar hacia arriba (cuanto le falta?)",
    "unidad": "P.6",
    "responde": "restar",
    "rapidez": 12,
    "que_hace": "desde lo que se quita cuento hacia arriba hasta lo que habia: lo que cuento es la resta",
    "condiciones": [
        ("el_de_abajo_no_es_mayor", "se quitaria mas de lo que hay (no hay restas negativas, 5.4)"),
        ("estan_cerca", "estan lejos: de uno a otro no cabe en los dedos"),
        ("hacia_arriba_es_mas_corto", "se quita poco: es mas corto contar hacia atras"),
    ],
    "usa": [],
}


def hacer(s, u):
    desde, hasta = u.decir(s["b"]), u.decir(s["a"])
    dichas, p = [], desde
    while p != hasta:                                 # se recita hacia arriba, un dedo por palabra
        p = u.siguiente(p)
        dichas.append(str(u.leer(p)))
    pasos = u.contar_hasta(desde, hasta)
    v = u.leer(pasos)
    # LA VUELTA es la suma: lo que se quito + lo que falta = lo que habia
    vuelta = u.contar_adelante(desde, pasos)
    return {"valor": v, "metodo": "contar hacia arriba (P.6)",
            "cuenta": "%d - %d = %d  (cuanto le falta al %d para llegar al %d? %s: %d dedos.  "
                      "Porque %d + %d = %d)"
                      % (s["a"], s["b"], v, s["b"], s["a"], ", ".join(dichas) or "nada", v,
                         s["b"], v, s["a"]),
            "vuelta": "%s + %s = %s" % (desde, pasos, vuelta.get("resultado")),
            "vuelta_ok": vuelta.get("resultado") == hasta}
