# -*- coding: utf-8 -*-
"""Pieza de calculo: SUMAR DE DIEZ EN DIEZ (paso 4: tecnicas para ir mas rapido).
47 + 30: desde el 47 se dan tres saltos de diez: 57, 67, 77.  Un salto de diez no se cuenta (no
son diez pasos): se ESCRIBE, la cifra de las decenas pasa a la siguiente (como en la tabla del
cien).  Es la estrategia de "saltar" (jump) de la investigacion: sumar decenas a un numero
cualquiera sin tocar las unidades."""

PIEZA = {
    "id": "sumar_de_diez_en_diez",
    "nombre": "de diez en diez",
    "unidad": "P.4",
    "responde": "sumar",
    "rapidez": 5,
    "que_hace": "si el segundo son decenas justas (30, 40...), salta de diez en diez desde el primero",
    "condiciones": [
        ("el_segundo_son_decenas_justas", "el segundo no son decenas justas (30, 40 ... 90)"),
        ("el_total_tiene_nombre", "el total se pasa de mil"),
    ],
    "usa": [],
}


def _saltos(p):
    return "un salto" if p == "uno" else "%s saltos" % p


def hacer(s, u):
    saltos = u.decir(u.cifras_de(s["b"])[1])        # 30 -> tres saltos (la cifra de las decenas)
    v, camino, marca = s["a"], [], "cero"
    while marca != saltos:
        v = u.subir_una_decena(v)
        if v is None:
            raise ValueError("me salgo de la lista saltando de diez en diez")
        camino.append(str(v))
        marca = u.siguiente(marca)
    # LA VUELTA: los mismos saltos hacia atras tienen que llevar al primero
    w, marca = v, "cero"
    while marca != saltos:
        w = u.bajar_una_decena(w)
        marca = u.siguiente(marca)
    return {"valor": v, "metodo": "de diez en diez (P.4)",
            "cuenta": "%d + %d = %d  (%s de diez desde %d: %s)"
            % (s["a"], s["b"], v, _saltos(saltos), s["a"], ", ".join(camino)),
            "vuelta": "%d - %d = %d  (%s hacia atras)" % (v, s["b"], w, _saltos(saltos)),
            "vuelta_ok": w == s["a"]}
