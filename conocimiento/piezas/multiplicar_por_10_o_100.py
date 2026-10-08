# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR POR 10 O POR 100 (paso M.9; NCETM 2.13, puntos 1, 3 y 5).  Por 10, CADA CIFRA SUBE
UN SITIO: las unidades se vuelven decenas, las decenas centenas...  El sitio de las unidades queda vacio y
lo marca un cero (23 x 10 = 230).  Por 100, dos sitios: es multiplicar por 10 DOS VECES.
(La REGLA 6 de la centena: no se 'anade un cero' sin mas; el cero aparece porque las cifras suben.)"""

PIEZA = {
    "id": "multiplicar_por_10_o_100",
    "nombre": "por 10 o por 100: las cifras suben de sitio",
    "unidad": "M.9",
    "responde": "multiplicar",
    "rapidez": 2,
    "que_hace": "por 10 cada cifra sube un sitio; por 100, dos (por 10 dos veces)",
    "condiciones": [
        ("un_factor_es_10_o_100", "ningun factor es 10 ni 100"),
    ],
    "usa": [],
}

_SITIOS = ("unidades", "decenas", "centenas", "millares", "decenas de millar", "centenas de millar",
           "millones", "decenas de millon")   # F.6: 100000 x 10 reventaba; N.6: hasta diez millones


def _subir(u, n):
    """Cada cifra un sitio arriba: el de las unidades queda vacio (un cero)."""
    return u.escribir_cifras([0] + u.cifras_de(n))


def hacer(s, u):
    a, b = s["a"], s["b"]
    por, otro = (b, a) if b in (10, 100) else (a, b)
    pasos = []
    v = otro
    veces = ("una",) if por == 10 else ("una", "otra")
    for _ in veces:
        nuevo = _subir(u, v)
        if u.decir(nuevo) is None:
            raise ValueError("%d x %d se sale de mi lista" % (a, b))
        pasos.append("%d x 10 = %d" % (v, nuevo))
        v = nuevo
    # LA VUELTA: bajar las cifras otra vez (quitar el sitio de las unidades) tiene que dar el de antes
    w = v
    for _ in veces:
        w = u.escribir_cifras(u.cifras_de(w)[1:]) if w else 0
    cif = u.cifras_de(otro)
    lectura = ", ".join("%d %s" % (c, _SITIOS[i]) for i, c in reversed(list(enumerate(cif))))
    return {"valor": v, "metodo": "las cifras suben de sitio (M.9)",
            "cuenta": "%d x %d: %s; cada cifra sube %s (%s)%s -> %d" % (
                a, b, lectura, "un sitio" if por == 10 else "DOS sitios, por 10 dos veces",
                "; ".join(pasos), "" if por == 10 else "", v),
            "vuelta": "%d : %d = %d (las cifras bajan otra vez)" % (v, por, w), "vuelta_ok": w == otro}
