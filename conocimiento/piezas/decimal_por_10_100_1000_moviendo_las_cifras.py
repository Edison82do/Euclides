# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR UN DECIMAL POR 10, 100 O 1000 MOVIENDO LAS CIFRAS (paso M.23; NCETM 2.29, punto 1;
5.NBT.A.1-2).  Por 10 cada cifra SUBE un sitio a la izquierda; por 100, dos; por 1000, tres (un sitio por cada
cero).  El PUNTO no se mueve: son las cifras las que pasan por encima de el.  Los sitios que quedan vacios los
marca un cero: 4.5 x 1000 -> las 4 unidades pasan a 4 millares, las 5 decimas a 5 centenas -> 4500.  NO es
'anadir ceros' (4.5000 es el mismo 4.5).  Se COMPRUEBA con la operacion contraria: bajar las cifras los mismos
sitios tiene que dar el de partida."""

PIEZA = {
    "id": "decimal_por_10_100_1000_moviendo_las_cifras",
    "nombre": "un decimal por 10, 100 o 1000: las cifras suben de sitio",
    "unidad": "M.23",
    "responde": "multiplicar_decimal",
    "rapidez": 1.5,
    "que_hace": "por 10, 100 o 1000 cada cifra sube uno, dos o tres sitios (uno por cada cero); el punto se queda",
    "condiciones": [
        ("un_decimal_y_un_entero", "no es un decimal por un entero"),
        ("el_entero_es_10_100_o_1000", "el entero no es 10, 100 ni 1000"),
    ],
    "usa": [],
}

_ENTEROS = ("unidades", "decenas", "centenas", "millares", "decenas de millar", "centenas de millar", "millones")
_DECIMALES = ("decimas", "centesimas", "milesimas")


def _partir(x):
    """'4.5' -> las cifras de delante del punto y las de detras, cada una con el NOMBRE de su sitio (leer)."""
    e, _, d = x.partition(".")
    delante = [(c, _ENTEROS[i]) for i, c in reversed(list(enumerate(reversed(e))))]
    detras = [(c, _DECIMALES[j]) for j, c in enumerate(d)]
    return delante, detras


def _subir(delante, detras):
    """Un sitio a la izquierda: la primera de detras del punto pasa delante; si no hay, el sitio vacio es un cero."""
    delante.append(detras.pop(0) if detras else ("0", None))


def _bajar(delante, detras):
    """Un sitio a la derecha: la ultima de delante del punto pasa detras; si no hay, el sitio vacio es un cero."""
    detras.insert(0, delante.pop() if delante else ("0", None))


def _escribir(delante, detras):
    """Las cifras y el punto: sin los ceros de la izquierda del todo ni los de la derecha del todo (D.2)."""
    e = "".join(c for c, _ in delante).lstrip("0") or "0"
    d = "".join(c for c, _ in detras).rstrip("0")
    return "%s.%s" % (e, d) if d else e


def _normal(x):
    return _escribir(*_partir(x))


def hacer(s, u):
    dec, por = (s["x"], s["y"]) if "." in s["x"] else (s["y"], s["x"])
    if dec.partition(".")[2][3:]:
        raise ValueError("con mas de tres cifras detras del punto todavia no (llego a las milesimas)")
    delante, detras = _partir(dec)
    for _ in por[1:]:                                   # un sitio por cada cero de 10, 100 o 1000
        _subir(delante, detras)
    valor = _escribir(delante, detras)
    if u.decir(u.escribir_cifras([int(c) for c in reversed(valor.replace(".", ""))])) is None:
        raise ValueError("%s x %s se sale de mi lista" % (dec, por))
    sitios = {"10": "UN sitio", "100": "DOS sitios", "1000": "TRES sitios"}[por]
    nombres = list(_ENTEROS[:len(delante)])
    nombres.reverse()
    movidas = ["%s %s -> %s %s" % (c, de, c, a) for (c, de), a in zip(delante, nombres) if de and c != "0"]
    movidas.extend("%s %s -> %s %s" % (c, de, c, a) for (c, de), a in zip(detras, _DECIMALES) if de and c != "0")
    pasos = ["POR %s CADA CIFRA SUBE %s (uno por cada cero); el punto se queda: %s" % (por, sitios, "; ".join(movidas)),
             "los sitios que quedan vacios los marca un cero: %s x %s = %s  (NO es 'anadir ceros')" % (dec, por, valor)]
    # LA VUELTA, con la operacion contraria: bajar las cifras los mismos sitios
    d2, t2 = _partir(valor)
    for _ in por[1:]:
        _bajar(d2, t2)
    atras = _escribir(d2, t2)
    return {"valor": valor, "metodo": "las cifras suben %s (M.23)" % sitios.lower(),
            "cuenta": "%s x %s: cada cifra sube %s -> %s" % (dec, por, sitios.lower(), valor), "pasos": pasos,
            "vuelta": "%s : %s = %s (las cifras bajan otra vez %s)" % (valor, por, atras, sitios.lower()),
            "vuelta_ok": atras == _normal(dec)}
