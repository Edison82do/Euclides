# -*- coding: utf-8 -*-
"""Pieza (paso P.7; NCETM 1.29): VER QUE UN NUMERO ESTA CERCA DE UN REDONDO.  397 esta a 3 de 400;
4997 a 3 de 5000; 1003 se pasa 3 de 1000.  Es lo primero que mira quien compensa: 'con el sustraendo
multiplo de 10, 100 o 1000 la cuenta se hace facil' (guia de NCETM, Upper KS2).
Se cuenta con los dedos, uno, dos o tres pasos hacia adelante y hacia atras, y se LEEN los ceros del
final (cifras_de).  Nada de restos ni divisiones de Python."""

PIEZA = {
    "id": "buscar_el_redondo_cercano",
    "nombre": "buscar el redondo de al lado",
    "unidad": "P.7",
    "responde": "redondo_cercano",
    "rapidez": 5,
    "que_hace": "cuento 1, 2 o 3 hacia adelante y hacia atras y miro si sale un numero con ceros al final",
    "condiciones": [
        ("el_numero_tiene_nombre", "el numero no esta en mi lista"),
    ],
    "usa": [],
}

_PASOS = ("uno", "dos", "tres")


def _ceros(u, n):
    """Los ceros del final de un numero escrito, como PALABRA (se leen cifra a cifra: 5000 -> 'tres')."""
    ceros = []
    for x in u.cifras_de(n):
        if x != 0:
            break
        ceros.append(x)
    return u.decir(len(ceros))


def _mas(u, p, q):
    """p tiene mas ceros que q (lo dice la lista: el que viene despues es el mayor)."""
    return u.viene_despues(p, q)


def hacer(s, u):
    n = s["n"]
    pide = u.decir(s.get("ceros", 2))
    tiene = _ceros(u, n)
    mejor = None
    for d in _PASOS:                         # primero el mas cerca; a igual distancia, el de mas ceros
        for sube, contar in ((True, u.contar_adelante), (False, u.contar_atras)):
            r = contar(u.decir(n), d).get("resultado")
            if r is None or r == "cero":
                continue
            v = u.leer(r)
            z = _ceros(u, v)
            if not _mas(u, pide, z) and _mas(u, z, tiene) and (mejor is None or _mas(u, z, mejor[3])):
                mejor = (v, d, sube, z)
        if mejor:
            break
    if mejor is None:
        raise ValueError("%d no esta a 1, 2 o 3 de un redondo" % n)
    v, d, sube, z = mejor
    # LA VUELTA: desde el redondo, contando los mismos pasos al reves, tiene que salir el numero
    w = (u.contar_atras if sube else u.contar_adelante)(u.decir(v), d).get("resultado")
    return {"valor": v, "pasos": u.leer(d), "sube": sube, "ceros": u.leer(z),
            "metodo": "el redondo de al lado (P.7)",
            "cuenta": "%d esta a %s de %d (%s)" % (n, d, v, "le faltan" if sube else "se pasa"),
            "vuelta": "%d %s %s = %s" % (v, "-" if sube else "+", d, w),
            "vuelta_ok": w == u.decir(n)}
