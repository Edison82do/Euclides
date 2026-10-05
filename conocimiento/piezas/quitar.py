# -*- coding: utf-8 -*-
"""Pieza del resolvedor: quitar (reduccion)  (unidad 5.4)."""

PIEZA = {
    "id": "quitar",
    "nombre": "quitar (reduccion)",
    "unidad": "5.4",
    "responde": "paso",
    "que_hace": "lo que habia - lo que se va = lo que queda",
    "condiciones": [
        ("es_un_cambio", "aqui no hay un antes y un despues (nada cambia con el tiempo)"),
        ("se_sabe_el_cambio", "no se sabe cuanto cambio (eso es justo lo que se busca)"),
        ("va_hacia_adelante", "no se busca el despues, se busca el antes"),
        ("el_monton_disminuye", "el monton no disminuye, crece"),
        ("hay_bastantes", "se irian mas de los que hay (no se puede quitar mas de lo que hay, 5.4)"),
    ],
    "usa": ["restar"],
}


def hacer(s, u):
    return u.usar("restar", a=s["antes"], b=s["n"])
