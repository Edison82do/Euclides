# -*- coding: utf-8 -*-
"""Pieza del resolvedor: la vuelta de anadir (se busca lo que habia antes)  (unidad 5.2 + 5.4)."""

PIEZA = {
    "id": "deshacer_lo_que_llego",
    "nombre": "la vuelta de anadir (se busca lo que habia antes)",
    "unidad": "5.2 + 5.4",
    "responde": "paso",
    "que_hace": "lo que hay despues - lo que llego = lo que habia antes",
    "condiciones": [
        ("es_un_cambio", "aqui no hay un antes y un despues (nada cambia con el tiempo)"),
        ("se_sabe_el_cambio", "no se sabe cuanto cambio (eso es justo lo que se busca)"),
        ("va_hacia_atras", "no se busca el antes, se busca el despues"),
        ("el_monton_crece", "el cambio no fue que llegaran, fue que se fueran"),
        ("hay_bastantes_al_deshacer", "lo que llego es mas de lo que hay ahora, y eso no puede ser"),
    ],
    "usa": ["restar"],
}


def hacer(s, u):
    return u.usar("restar", a=s["despues"], b=s["n"])
