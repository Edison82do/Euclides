# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR POR 0.1 O POR 0.01 (paso M.13; NCETM 2.19, punto 2).  'Multiplicar por 0.1 es lo
mismo que dividir entre 10; por 0.01, lo mismo que dividir entre 100.'  Cada cifra BAJA un sitio (dos
con 0.01): 35 x 0.1 = 3.5 (las 3 decenas se vuelven 3 unidades, las 5 unidades 5 decimas).  Por menos de
uno sale MENOS (punto 4).  Se COMPRUEBA con la operacion contraria: 3.5 x 10 = 35 (las cifras suben)."""

PIEZA = {
    "id": "multiplicar_por_una_decima",
    "nombre": "por 0.1 o 0.01: las cifras bajan de sitio",
    "unidad": "M.13",
    "responde": "multiplicar_decimal",
    "rapidez": 2,
    "que_hace": "x 0.1 es : 10 (las cifras bajan un sitio); x 0.01 es : 100 (dos sitios)",
    "condiciones": [
        ("uno_es_una_decima_o_una_centesima", "ningun factor es 0.1 ni 0.01"),
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
    x, y = s["x"], s["y"]
    por, otro = (x, y) if x in ("0.1", "0.01") else (y, x)
    c, k = _leer(u, otro)
    k2 = k + 1 if por == "0.1" else k + 2               # cuantas cifras quedan detras del punto (recitar)
    if k2 > 3:
        raise ValueError("bajando las cifras quedarian mas de tres detras del punto: todavia no (llego a las milesimas)")
    valor = _escribir(c, k2)
    sitios = "un sitio" if por == "0.1" else "dos sitios"
    # LA VUELTA: por 10 (o 100), las cifras vuelven a subir y tiene que salir el de antes
    cv, kv = _leer(u, valor)
    sube = [0] if por == "0.1" else [0, 0]                # x 10: un cero detras; x 100: dos (M.9)
    sube.extend(u.cifras_de(cv))
    m = u.escribir_cifras(sube)
    atras = _escribir(m, kv)
    return {"valor": valor, "metodo": "por %s: las cifras bajan %s (M.13)" % (por, sitios),
            "cuenta": "%s x %s = %s : %s = %s  (cada cifra baja %s)"
                      % (otro, por, otro, "10" if por == "0.1" else "100", valor, sitios),
            "pasos": ["POR %s ES ENTRE %s (NCETM 2.19, punto 2): %s x %s = %s : %s"
                      % (por, "10" if por == "0.1" else "100", otro, por, otro, "10" if por == "0.1" else "100"),
                      "CADA CIFRA BAJA %s: %s -> %s" % (sitios.upper(), otro, valor)],
            "vuelta": "%s x %s = %s (las cifras vuelven a subir)" % (valor, "10" if por == "0.1" else "100", atras),
            "vuelta_ok": atras == _escribir(c, k)}
