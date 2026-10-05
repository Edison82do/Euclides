# -*- coding: utf-8 -*-
"""Pieza del resolvedor: cuantos se fueron (se cuenta desde lo que queda hasta lo que habia)  (unidad 5.5 + 7.4)."""

PIEZA = {
    "id": "lo_que_se_fue",
    "nombre": "cuantos se fueron (se cuenta desde lo que queda hasta lo que habia)",
    "unidad": "5.5 + 7.4",
    "responde": "paso",
    "que_hace": "desde lo que queda se cuenta hacia adelante hasta lo que habia; los pasos son lo que se fue",
    "condiciones": [
        ("es_un_cambio", "aqui no hay un antes y un despues (nada cambia con el tiempo)"),
        ("no_se_sabe_el_cambio", "el cambio ya se sabe; lo que falta es otra cosa"),
        ("el_monton_disminuye", "el monton no disminuye, crece"),
        ("el_despues_no_es_mayor", "despues hay MAS que antes, y si se fue algo eso no puede ser"),
    ],
    "usa": ["contar_hasta"],
}


def hacer(s, u):
    return u.usar("contar_hasta", a=s["despues"], b=s["antes"])
