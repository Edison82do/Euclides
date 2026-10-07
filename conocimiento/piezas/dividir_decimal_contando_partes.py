# -*- coding: utf-8 -*-
"""Pieza de DIVIDIR UN DECIMAL ENTRE UN NUMERO DE UNA CIFRA (paso M.13; NCETM 2.19, punto 5; 5.NBT.B.7).
CONTAR EN LA UNIDAD PEQUENA: 7.2 son 72 decimas; 72 decimas : 3 = 24 decimas = 2.4 (la division de
ENTEROS la hacen las piezas de dividir).  Si SOBRA algo, se CAMBIA a la unidad mas pequena (1 decima =
10 centesimas, como en la division corta): 1.3 : 4 -> 13 decimas : 4 = 3 y sobra 1 -> 1.30 son 130
centesimas -> 130 : 4 = 32 y sobran 2 -> 1300 milesimas : 4 = 325 -> 0.325.  Hasta las milesimas; si
aun sobra, todavia no.  Se COMPRUEBA multiplicando: 24 decimas x 3 = 72 decimas = 7.2."""

PIEZA = {
    "id": "dividir_decimal_contando_partes",
    "nombre": "contar en decimas (o centesimas) y dividir como enteros",
    "unidad": "M.13",
    "responde": "dividir_decimal",
    "rapidez": 5,
    "que_hace": "7.2 : 3 = 72 decimas : 3 = 24 decimas = 2.4; si sobra, se cambia a la unidad mas pequena",
    "condiciones": [
        ("el_divisor_es_de_una_cifra_sin_el_cero",
         "el divisor no es de una cifra (NCETM 2.19: entre 2 y 9; con dos cifras es la division larga, 6.o)"),
    ],
    "usa": ["dividir", "multiplicar"],
}

_UNIDAD = {0: ("unidad", "unidades"), 1: ("decima", "decimas"), 2: ("centesima", "centesimas"),
           3: ("milesima", "milesimas")}


def _leer(u, x):
    e, _, d = x.partition(".")
    return u.escribir_cifras([int(c) for c in reversed("%s%s" % (e, d))]), len(d)


def _escribir(n, k, ceros=False):
    s = str(n)
    if k == 0:
        return s
    while len(s) <= k:
        s = "0%s" % s
    e, d = s[:-k], s[-k:] if ceros else s[-k:].rstrip("0")
    return "%s.%s" % (e, d) if d else e


def _cuantas(n, k):
    uno, varios = _UNIDAD[k]
    return "%d %s" % (n, uno if n == 1 else varios)


def hacer(s, u):
    x, ds = s["x"], s["d"]
    c, k = _leer(u, x)
    d, _ = _leer(u, ds)
    if k > 3:
        raise ValueError("con mas de tres cifras detras del punto todavia no (llego a las milesimas)")
    if u.decir(c) is None:
        raise ValueError("%s contado en %s se sale de mi lista" % (x, _UNIDAD[k][1]))
    pasos = []
    if k:
        pasos.append("CONTANDO EN %s: %s son %s" % (_UNIDAD[k][1].upper(), x, _cuantas(c, k)))
    r = u.usar("dividir", total=c, divisor=d)
    q, resto = r["valor"], r["resultado"].get("resto") or 0
    pasos.append("LA CUENTA DE ENTEROS: %s : %d = %s%s  (%s)"
                 % (_cuantas(c, k), d, _cuantas(q, k), ", sobra%s %s" % ("" if resto == 1 else "n", _cuantas(resto, k))
                    if resto else "", r["resultado"]["metodo"]))
    cifras_q = u.cifras_de(q)                                 # el cociente se va ESCRIBIENDO, cifra a cifra
    lleno = [0] + u.cifras_de(c)                              # lo que habia, con un cero mas detras por cada cambio
    while resto:
        if k == 3:
            raise ValueError("%s : %s no sale exacta ni contando en milesimas (repartir mas fino, o redondear "
                             "el cociente, es de mas adelante)" % (x, ds))
        k = k + 1
        cambiado = u.escribir_cifras([0] + u.cifras_de(resto))    # 1 de las de antes = 10 de las nuevas
        r = u.usar("dividir", total=cambiado, divisor=d)
        cifra, nuevo = r["valor"], r["resultado"].get("resto") or 0
        pasos.append("SOBRA%s %s: lo CAMBIO por %s (1 %s = 10 %s): %s : %d = %s%s  (escribo un cero detras: %s)"
                     % ("" if resto == 1 else "N", _cuantas(resto, k - 1), _UNIDAD[k][1], _UNIDAD[k - 1][0],
                        _UNIDAD[k][1], _cuantas(cambiado, k), d, _cuantas(cifra, k),
                        ", sobra%s %s" % ("" if nuevo == 1 else "n", _cuantas(nuevo, k)) if nuevo else "",
                        _escribir(u.escribir_cifras(lleno), k, ceros=True)))
        cifras_q = [cifra] + cifras_q                         # la cifra nueva va DETRAS (en el sitio pequeno)
        lleno = [0] + lleno
        resto = nuevo
    q = u.escribir_cifras(cifras_q)
    c = u.escribir_cifras(lleno[1:])
    valor = _escribir(q, k)
    if k:
        pasos.append("EL PUNTO EN SU SITIO: %s = %s" % (_cuantas(q, k), valor))
    # LA VUELTA, con la operacion contraria: el cociente por el divisor tiene que dar lo que habia
    if q and u.decir(q) is None:
        raise ValueError("el cociente, contado en %s, se sale de mi lista: no lo puedo comprobar" % _UNIDAD[k][1])
    try:
        m = u.usar("multiplicar", a=q, b=d)["valor"] if q else 0
    except Exception:
        raise ValueError("%s, contado en %s, se sale de mi lista: no lo puedo comprobar" % (x, _UNIDAD[k][1]))
    atras = _escribir(m, k)
    return {"valor": valor, "resto": 0, "metodo": "contar en %s y dividir como enteros (M.13)" % _UNIDAD[k][1],
            "cuenta": "%s : %s = %s : %d = %s = %s" % (x, ds, _cuantas(c, k), d, _cuantas(q, k), valor),
            "pasos": pasos, "unidad_pequena": _UNIDAD[k][1],
            "vuelta": "%s x %d = %s = %s" % (_cuantas(q, k), d, _cuantas(m, k), atras),
            "vuelta_ok": atras == _escribir(_leer(u, x)[0], len(x.partition(".")[2]))}
