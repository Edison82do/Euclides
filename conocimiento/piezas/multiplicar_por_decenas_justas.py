# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso M.9; NCETM 2.13, punto 6; Common Core 3.NBT.A.3): si un factor se hace DIEZ
VECES mayor, el producto tambien.  9 x 80: 9 x 8 = 72 (de memoria) y 80 es diez veces 8, asi que el
producto es diez veces 72 = 720 (las cifras suben un sitio).  Es un HECHO DERIVADO: solo si el hecho
pequeno se sabe."""

PIEZA = {
    "id": "multiplicar_por_decenas_justas",
    "nombre": "decenas justas: el hecho pequeno, diez veces",
    "unidad": "M.9",
    "responde": "multiplicar",
    "rapidez": 3,
    "que_hace": "quita los ceros de los factores, usa el hecho que se sabe y sube las cifras otra vez",
    "condiciones": [
        ("un_factor_acaba_en_cero", "ningun factor son decenas justas (30, 80, 400...)"),
    ],
    "usa": [],
}


def _quitar_ceros(u, n):
    cif, ceros = u.cifras_de(n), []
    while len(cif) > 1 and cif[0] == 0:
        cif = cif[1:]
        ceros.append(0)
    return u.escribir_cifras(cif), ceros


def hacer(s, u):
    a, b = s["a"], s["b"]
    pa, ca = _quitar_ceros(u, a)
    pb, cb = _quitar_ceros(u, b)
    if not ca and not cb:
        raise ValueError("no hay ceros que quitar")
    h = u.recuerdo("%d x %d" % (pa, pb)) or u.recuerdo("%d x %d" % (pb, pa))
    if pa == 1 or pb == 1:
        pequeno = pb if pa == 1 else pa
    elif h:
        pequeno = h["valor"]
    else:
        raise ValueError("no se de memoria %d x %d" % (pa, pb))
    ceros = []
    ceros.extend(ca)
    ceros.extend(cb)
    veces = len(ceros)
    ceros.extend(u.cifras_de(pequeno))
    v = u.escribir_cifras(ceros) if pequeno else 0
    if u.decir(v) is None:
        raise ValueError("se sale de mi lista")
    return {"valor": v, "metodo": "decenas justas (M.9)",
            "cuenta": "%d x %d = %d (lo se); %d x %d es %s mayor, asi que el producto tambien: las cifras suben %s -> %d"
                      % (pa, pb, pequeno, a, b, "DIEZ veces" if veces == 1 else "diez veces y otra vez diez",
                         "un sitio" if veces == 1 else "dos sitios", v),
            "vuelta": "%d con las cifras bajadas otra vez: %d" % (v, _quitar_ceros(u, v)[0] if v else 0),
            "vuelta_ok": (not v) or _quitar_ceros(u, v)[0] == _quitar_ceros(u, pequeno)[0]}
