# -*- coding: utf-8 -*-
"""Pieza de DIVIDIR UN DECIMAL ENTRE 10 O 100 (paso M.13; NCETM 2.19, punto 2; viene de M.9).  Entre 10
cada cifra BAJA un sitio; entre 100, dos: 3.5 : 10 = 0.35.  Con decimales no sobra nada: lo que en M.9
era el resto ahora baja a las decimas o a las centesimas.  Se COMPRUEBA multiplicando: 0.35 x 10 = 3.5."""

PIEZA = {
    "id": "dividir_decimal_por_10_o_100",
    "nombre": "un decimal entre 10 o 100: las cifras bajan de sitio",
    "unidad": "M.13",
    "responde": "dividir_decimal",
    "rapidez": 2,
    "que_hace": "entre 10 cada cifra baja un sitio (las unidades se vuelven decimas); entre 100, dos",
    "condiciones": [
        ("el_divisor_es_un_10_o_un_100", "el divisor no es 10 ni 100"),
    ],
    "usa": [],
}


def _leer(u, x):
    e, _, d = x.partition(".")
    return u.escribir_cifras([int(c) for c in reversed("%s%s" % (e, d))]), len(d)


def _escribir(n, k):
    s = str(n)
    if k == 0:
        return s
    while len(s) <= k:
        s = "0%s" % s
    e, d = s[:-k], s[-k:].rstrip("0")
    return "%s.%s" % (e, d) if d else e


def hacer(s, u):
    x, d = s["x"], s["d"]
    c, k = _leer(u, x)
    k2 = k + 1 if d == "10" else k + 2
    if k2 > 3:
        raise ValueError("bajando las cifras quedarian mas de tres detras del punto: todavia no (llego a las milesimas)")
    valor = _escribir(c, k2)
    sitios = "un sitio" if d == "10" else "dos sitios"
    # LA VUELTA: el cociente por 10 (o 100): las cifras suben y tiene que salir el de antes
    cv, kv = _leer(u, valor)
    sube = [0] if d == "10" else [0, 0]                # x 10: un cero detras; x 100: dos (M.9)
    sube.extend(u.cifras_de(cv))
    m = u.escribir_cifras(sube)
    atras = _escribir(m, kv)
    return {"valor": valor, "resto": 0, "metodo": "entre %s: las cifras bajan %s (M.13)" % (d, sitios),
            "cuenta": "%s : %s = %s  (cada cifra baja %s; lo que era resto baja detras del punto)" % (x, d, valor, sitios),
            "pasos": ["ENTRE %s CADA CIFRA BAJA %s: %s -> %s" % (d, sitios.upper(), x, valor),
                      "(en M.9 lo que no llegaba a un grupo de diez era el RESTO; con decimales baja detras del punto)"],
            "vuelta": "%s x %s = %s (las cifras vuelven a subir)" % (valor, d, atras),
            "vuelta_ok": atras == _escribir(c, k)}
