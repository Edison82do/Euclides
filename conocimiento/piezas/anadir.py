# -*- coding: utf-8 -*-
"""Pieza del resolvedor: anadir (aumentacion)  (unidad 5.2)."""

PIEZA = {
    "id": "anadir",
    "nombre": "anadir (aumentacion)",
    "unidad": "5.2",
    "responde": "paso",
    "que_hace": "lo que habia + lo que llega = lo que hay despues",
    "condiciones": [
        ("es_un_cambio", "aqui no hay un antes y un despues (nada cambia con el tiempo)"),
        ("se_sabe_el_cambio", "no se sabe cuanto cambio (eso es justo lo que se busca)"),
        ("va_hacia_adelante", "no se busca el despues, se busca el antes"),
        ("el_monton_crece", "el monton no crece, disminuye"),
    ],
    "usa": ["sumar"],
}


def hacer(s, u):
    return u.usar("sumar", a=s["antes"], b=s["n"])
