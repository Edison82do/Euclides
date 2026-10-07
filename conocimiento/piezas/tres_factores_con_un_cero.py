# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR TRES FACTORES CUANDO UNO ES CERO (paso M.14; NCETM 2.20; M.2: por cero, nada).
5 x 0 x 999: si un factor es cero, no hay ningun grupo (o los grupos estan vacios): el producto es 0, y no
hace falta ninguna cuenta.  Se COMPRUEBA con la operacion contraria: 0 entre un factor que no sea cero
da 0, y eso tiene que ser el producto de los demas (que llevan el cero).  Si todos son cero, entre cero
no se puede dividir: se comprueba multiplicando en el otro orden."""

PIEZA = {
    "id": "tres_factores_con_un_cero",
    "nombre": "hay un cero: el producto es cero",
    "unidad": "M.14",
    "responde": "multiplicar_tres",
    "rapidez": 1,
    "que_hace": "5 x 0 x 999 = 0: con un factor cero no hay nada",
    "condiciones": [
        ("hay_tres_factores_o_mas", "no son tres factores o mas"),
        ("algun_factor_es_cero", "ningun factor es cero"),
    ],
    "usa": ["multiplicar", "dividir"],
}


def _cosas(u, f):
    """Un decimal contado en su unidad pequena ('0.25' -> 25 centesimas); un entero, tal cual."""
    return u.escribir_cifras([int(c) for c in reversed(f.replace(".", ""))])


def _producto_de(u, fs):
    """El producto de los que quedan, empezando por el cero (la pregunta 'multiplicar': por cero, M.2)."""
    lista = sorted(fs, key=lambda f: f != "0")
    actual = _cosas(u, lista[0])
    for f in lista[1:]:
        actual = u.usar("multiplicar", a=actual, b=_cosas(u, f))["valor"]
    return actual


def hacer(s, u):
    fs = s["factores"]
    divisor = next((f for f in fs if f != "0" and "." not in f), None)
    if divisor is not None:
        q = u.usar("dividir", total=0, divisor=u.escribir_cifras([int(c) for c in reversed(divisor)]))["valor"]
        resto = list(fs)
        resto.remove(divisor)
        p = _producto_de(u, resto)
        vuelta = "0 : %s = %d, y %s (los demas, con su cero) = %d" % (divisor, q, " x ".join(resto), p)
        ok = q == 0 and p == 0
    else:
        p = _producto_de(u, list(reversed(fs)))
        vuelta = "entre cero no se divide: en el otro orden, %s = %d" % (" x ".join(reversed(fs)), p)
        ok = p == 0
    return {"valor": "0", "metodo": "un factor es cero: no hay nada (M.2)",
            "cuenta": "%s = 0" % " x ".join(fs),
            "pasos": ["hay un 0 entre los factores: ningun grupo, o grupos vacios -> 0, sin hacer cuentas"],
            "vuelta": vuelta, "vuelta_ok": ok}
