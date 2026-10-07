# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR UN DECIMAL POR UN ENTERO (paso M.13; NCETM 2.19, puntos 1 y 3; 5.NBT.B.7).
CONTAR EN LA UNIDAD PEQUENA ('unitising'): 0.3 son 3 decimas, y 4 x 3 decimas = 12 decimas, igual que
4 x 3 unidades = 12 unidades.  12 decimas = 1.2.  Con mas cifras es lo mismo: 3.27 son 327 centesimas;
327 x 4 = 1308 (la cuenta de ENTEROS la hacen las piezas de multiplicar); 1308 centesimas = 13.08.
Leer las cifras sin el punto es x 10 o x 100 (las cifras suben de sitio); volver a poner el punto es
: 10 o : 100 (bajan).  Se COMPRUEBA dividiendo: 1.2 : 4 tiene que dar 0.3."""

PIEZA = {
    "id": "multiplicar_decimal_contando_partes",
    "nombre": "contar en decimas (o centesimas) y multiplicar como enteros",
    "unidad": "M.13",
    "responde": "multiplicar_decimal",
    "rapidez": 5,
    "que_hace": "0.3 x 4 = 3 decimas x 4 = 12 decimas = 1.2: la cuenta de enteros y el punto en su sitio",
    "condiciones": [
        ("un_decimal_y_un_entero", "no es un decimal por un entero (decimal por decimal es de 6.o)"),
        ("el_entero_es_de_una_cifra_o_10_o_100",
         "el entero no es de una cifra (NCETM 2.19: por un numero de una cifra, o por 10 o 100; con mas cifras, "
         "la multiplicacion larga, 6.o)"),
    ],
    "usa": ["multiplicar", "dividir_decimal"],
}

_UNIDAD = {0: ("unidad", "unidades"), 1: ("decima", "decimas"), 2: ("centesima", "centesimas"),
           3: ("milesima", "milesimas")}


def _leer(u, x):
    """'3.27' -> (327, 2): las cifras sin el punto, y cuantas hay detras.  Es LEER, no calcular."""
    e, _, d = x.partition(".")
    return u.escribir_cifras([int(c) for c in reversed("%s%s" % (e, d))]), len(d)


def _escribir(n, k):
    """1308 centesimas -> '13.08';  60 decimas -> '6'.  Es ESCRIBIR las cifras y poner el punto."""
    s = str(n)
    if k == 0:
        return s
    while len(s) <= k:
        s = "0%s" % s
    e, d = s[:-k], s[-k:].rstrip("0")
    return "%s.%s" % (e, d) if d else e


def _cuantas(n, k):
    uno, varios = _UNIDAD[k]
    return "%d %s" % (n, uno if n == 1 else varios)


def hacer(s, u):
    dec, ent = (s["x"], s["y"]) if "." in s["x"] else (s["y"], s["x"])
    c, k = _leer(u, dec)
    n, _ = _leer(u, ent)
    if k > 3:
        raise ValueError("con mas de tres cifras detras del punto todavia no (llego a las milesimas)")
    if n == 0 or c == 0:
        raise ValueError("por cero no hay nada que contar")
    if u.decir(c) is None:
        raise ValueError("%s contado en %s se sale de mi lista" % (dec, _UNIDAD[k][1]))
    try:
        r = u.usar("multiplicar", a=c, b=n)
    except Exception as e:
        raise ValueError("la cuenta de enteros %d x %d no me sale: me paso de mi lista o me falta un metodo (%s)"
                         % (c, n, e))
    p = r["valor"]
    if u.decir(p) is None:
        raise ValueError("el producto, contado en %s, se sale de mi lista" % _UNIDAD[k][1])
    valor = _escribir(p, k)
    pasos = ["CONTANDO EN %s: %s son %s  (leo las cifras sin el punto: x %s)"
             % (_UNIDAD[k][1].upper(), dec, _cuantas(c, k), "10" if k == 1 else "100" if k == 2 else "1000"),
             "LA CUENTA DE ENTEROS: %d x %d = %d  (%s)  ->  %s"
             % (c, n, p, r["resultado"]["metodo"], _cuantas(p, k)),
             "EL PUNTO EN SU SITIO: %s = %s  (las cifras bajan %s)"
             % (_cuantas(p, k), valor, "un sitio: : 10" if k == 1 else "dos sitios: : 100" if k == 2
                else "tres sitios: : 1000")]
    # LA VUELTA, con la operacion contraria: el producto entre el entero tiene que dar el decimal
    original = _escribir(c, k)
    w = u.usar("dividir_decimal", x=valor, d=ent)
    atras, como = w["valor"], "%s : %s = %s" % (valor, ent, w["valor"])
    return {"valor": valor, "metodo": "contar en %s y multiplicar como enteros (M.13)" % _UNIDAD[k][1],
            "cuenta": "%s x %s = %s x %d = %s = %s" % (dec, ent, _cuantas(c, k), n, _cuantas(p, k), valor),
            "pasos": pasos, "unidad_pequena": _UNIDAD[k][1], "en_pequenas": p,
            "vuelta": como, "vuelta_ok": atras == original}
