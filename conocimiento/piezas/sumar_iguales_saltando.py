# -*- coding: utf-8 -*-
"""Pieza de SUMA DE IGUALES (paso M.0; Common Core 2.OA.C.4): si cada fila (cada grupo) es de 2, de 5
o de 10, no hace falta sumar fila a fila: se CUENTA DE n EN n (lo de N.1; NCETM 2.1: 'contar en
grupos de dos, de cinco, de diez').  5 filas de 5: 5, 10, 15, 20, 25."""

PIEZA = {
    "id": "sumar_iguales_saltando",
    "nombre": "contar de n en n (una fila, un salto)",
    "unidad": "M.0 + N.1",
    "responde": "suma_de_iguales",
    "rapidez": 5,
    "que_hace": "si cada grupo es de 2, 5 o 10, cuenta saltando: un salto por grupo",
    "condiciones": [
        ("cada_grupo_se_salta", "cada grupo no es de 2, de 5 ni de 10 (solo se saltar de esos)"),
    ],
    "usa": [],
}


def hacer(s, u):
    de = u.decir(s["n"])
    v, marca, serie = 0, "cero", []
    while marca != u.decir(s["veces"]):
        v = u.saltar(v, de)
        if v is None:
            raise ValueError("me salgo de la lista saltando")
        serie.append(str(v))
        marca = u.siguiente(marca)
    return {"valor": v, "metodo": "contar de %d en %d (N.1)" % (s["n"], s["n"]),
            "cuenta": "un salto de %d por cada grupo: %s" % (s["n"], ", ".join(serie) or "ningun salto: 0"),
            "pasos": serie, "vuelta": "", "vuelta_ok": True}
