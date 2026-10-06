# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso M.5; NCETM 2.8): 'los productos de la tabla del 9 son el TRIPLE de los de
la del 3'.  Hecho derivado: 7 x 9 = el triple de 7 x 3 (que ya se sabe) = 21 + 21 + 21 = 63."""

PIEZA = {
    "id": "multiplicar_triplicando",
    "nombre": "triplicar la tabla del 3 (9 desde 3)",
    "unidad": "M.5",
    "responde": "multiplicar",
    "rapidez": 5,
    "que_hace": "x 9 es el triple de x 3 (si ese ya lo se)",
    "condiciones": [
        ("se_puede_triplicar_el_3", "ningun factor es 9, o la tabla del 3 de ese numero no la se todavia"),
    ],
    "usa": ["sumar"],
}


def hacer(s, u):
    k = s["a"] if s["b"] == 9 else s["b"]
    h = (u.recuerdo("%d x 3" % k) or u.recuerdo("3 x %d" % k))["valor"]
    dos = u.usar("sumar", a=h, b=h)
    tres = u.usar("sumar", a=dos["valor"], b=h)
    return {"valor": tres["valor"], "metodo": "triplicando (M.5)",
            "cuenta": "x 9 es el TRIPLE de x 3: %d x 3 = %d (lo se); %d + %d = %d; %d + %d = %d"
                      % (k, h, h, h, dos["valor"], dos["valor"], h, tres["valor"]),
            "vuelta": "", "vuelta_ok": True}
