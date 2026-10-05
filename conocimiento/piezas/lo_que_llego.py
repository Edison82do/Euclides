# -*- coding: utf-8 -*-
"""Pieza del resolvedor: cuantos llegaron (se cuenta desde el antes hasta el despues)  (unidad 5.5 + 7.1)."""

PIEZA = {
    "id": "lo_que_llego",
    "nombre": "cuantos llegaron (se cuenta desde el antes hasta el despues)",
    "unidad": "5.5 + 7.1",
    "responde": "paso",
    "que_hace": "desde lo que habia se cuenta hacia adelante hasta lo que hay; los pasos son lo que llego",
    "condiciones": [
        ("es_un_cambio", "aqui no hay un antes y un despues (nada cambia con el tiempo)"),
        ("no_se_sabe_el_cambio", "el cambio ya se sabe; lo que falta es otra cosa"),
        ("el_monton_crece", "el monton no crece, disminuye"),
        ("el_despues_no_es_menor", "despues hay MENOS que antes, y si llego algo eso no puede ser"),
    ],
    "usa": ["contar_hasta"],
}


def hacer(s, u):
    return u.usar("contar_hasta", a=s["antes"], b=s["despues"])
