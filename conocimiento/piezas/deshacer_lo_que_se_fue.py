# -*- coding: utf-8 -*-
"""Pieza del resolvedor: la vuelta de quitar (se busca lo que habia antes)  (unidad 5.4)."""

PIEZA = {
    "id": "deshacer_lo_que_se_fue",
    "nombre": "la vuelta de quitar (se busca lo que habia antes)",
    "unidad": "5.4",
    "responde": "paso",
    "que_hace": "lo que queda + lo que se fue = lo que habia antes",
    "condiciones": [
        ("es_un_cambio", "aqui no hay un antes y un despues (nada cambia con el tiempo)"),
        ("se_sabe_el_cambio", "no se sabe cuanto cambio (eso es justo lo que se busca)"),
        ("va_hacia_atras", "no se busca el antes, se busca el despues"),
        ("el_monton_disminuye", "el cambio no fue que se fueran, fue que llegaran"),
    ],
    "usa": ["sumar"],
}


def hacer(s, u):
    return u.usar("sumar", a=s["despues"], b=s["n"])
