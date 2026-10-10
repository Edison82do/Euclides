# -*- coding: utf-8 -*-
"""Pieza de DIVIDIR ENTRE 10, 100 O 1000 MOVIENDO LAS CIFRAS (paso M.23; NCETM 2.29, punto 1; 5.NBT.A.1-2).
Entre 10 cada cifra BAJA un sitio a la derecha; entre 100, dos; entre 1000, tres (uno por cada cero).  El punto
no se mueve; las cifras pasan por debajo de el, y los sitios vacios los marca un cero: 3.5 : 100 = 0.035.
Vale tambien para un ENTERO: 375 : 1000 = 0.375 (lo que en M.9 era '0 resto 375' baja detras del punto).
Llego a las milesimas (D.2): si quedarian mas de tres cifras detras del punto, todavia no.
Se COMPRUEBA con la operacion contraria: subir las cifras los mismos sitios tiene que dar el de partida."""

PIEZA = {
    "id": "entre_10_100_1000_moviendo_las_cifras",
    "nombre": "entre 10, 100 o 1000: las cifras bajan de sitio",
    "unidad": "M.23",
    "responde": "dividir_decimal",
    "rapidez": 1.5,
    "que_hace": "entre 10, 100 o 1000 cada cifra baja uno, dos o tres sitios (uno por cada cero); el punto se queda",
    "condiciones": [
        ("el_divisor_es_10_100_o_1000", "el divisor no es 10, 100 ni 1000"),
        ("lo_que_se_divide_esta_escrito_en_cifras", "lo que se divide no es un numero escrito en cifras"),
    ],
    "usa": [],
}

_ENTEROS = ("unidades", "decenas", "centenas", "millares", "decenas de millar", "centenas de millar", "millones")
_DECIMALES = ("decimas", "centesimas", "milesimas", "diezmilesimas", "cienmilesimas", "millonesimas")


def _partir(x):
    e, _, d = x.partition(".")
    delante = [(c, _ENTEROS[i]) for i, c in reversed(list(enumerate(reversed(e))))]
    detras = [(c, _DECIMALES[j]) for j, c in enumerate(d)]
    return delante, detras


def _subir(delante, detras):
    delante.append(detras.pop(0) if detras else ("0", None))


def _bajar(delante, detras):
    detras.insert(0, delante.pop() if delante else ("0", None))


def _escribir(delante, detras):
    e = "".join(c for c, _ in delante).lstrip("0") or "0"
    d = "".join(c for c, _ in detras).rstrip("0")
    return "%s.%s" % (e, d) if d else e


def _normal(x):
    return _escribir(*_partir(x))


def hacer(s, u):
    x, por = s["x"], s["d"]
    if x.partition(".")[2][3:]:
        raise ValueError("con mas de tres cifras detras del punto todavia no (llego a las milesimas)")
    delante, detras = _partir(x)
    for _ in por[1:]:                                   # un sitio por cada cero de 10, 100 o 1000
        _bajar(delante, detras)
    valor = _escribir(delante, detras)
    if valor.partition(".")[2][3:]:
        raise ValueError("%s : %s: bajando las cifras quedarian mas de tres detras del punto: todavia no "
                         "(llego a las milesimas)" % (x, por))
    sitios = {"10": "UN sitio", "100": "DOS sitios", "1000": "TRES sitios"}[por]
    nombres = list(_ENTEROS[:len(delante)])
    nombres.reverse()
    movidas = ["%s %s -> %s %s" % (c, de, c, a) for (c, de), a in zip(delante, nombres) if de and c != "0"]
    movidas.extend("%s %s -> %s %s" % (c, de, c, a) for (c, de), a in zip(detras, _DECIMALES) if de and c != "0")
    pasos = ["ENTRE %s CADA CIFRA BAJA %s (uno por cada cero); el punto se queda: %s" % (por, sitios, "; ".join(movidas)),
             "los sitios que quedan vacios los marca un cero: %s : %s = %s  (NO es 'quitar ceros')" % (x, por, valor)]
    # LA VUELTA, con la operacion contraria: subir las cifras los mismos sitios
    d2, t2 = _partir(valor)
    for _ in por[1:]:
        _subir(d2, t2)
    atras = _escribir(d2, t2)
    return {"valor": valor, "resto": 0, "metodo": "las cifras bajan %s (M.23)" % sitios.lower(),
            "cuenta": "%s : %s: cada cifra baja %s -> %s" % (x, por, sitios.lower(), valor), "pasos": pasos,
            "vuelta": "%s x %s = %s (las cifras suben otra vez %s)" % (valor, por, atras, sitios.lower()),
            "vuelta_ok": atras == _normal(x)}
