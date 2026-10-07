# -*- coding: utf-8 -*-
"""Pieza de DIVIDIR (paso M.3; NCETM 2.6, punto 4: 'si el divisor es dos, la MITAD').  Se hacen
parejas y se da una de cada pareja a cada lado (lo de N.1 y M.2).  Si sobra uno, ese es el resto.
PASO M.14 (arreglo, 7 oct): con un numero de mas de cien ya no se cuentan parejas de una en una (la mitad
de un millon eran 500 000 parejas y tardaba 15 s): se parte POR SITIOS, de izquierda a derecha, la mitad
de cada cifra; si sobra uno, se CAMBIA por diez de la columna siguiente (como la division corta).  La
mitad de 846: la mitad de 8 centenas (4), de 4 decenas (2), de 6 unidades (3) -> 423.  Se COMPRUEBA
doblando: 423 + 423 = 846."""

PIEZA = {
    "id": "dividir_a_la_mitad",
    "nombre": "la mitad (el divisor es dos)",
    "unidad": "M.3",
    "responde": "dividir",
    "rapidez": 5,
    "que_hace": "entre 2 es la mitad: parejas, una para cada lado",
    "condiciones": [
        ("el_divisor_es_dos", "el divisor no es dos"),
    ],
    "usa": [],
}


def _parejas(u, objetivo):
    """La mitad de un numero pequeno: parejas, una para cada lado.  Devuelve (cada lado, resto)."""
    actual, cada = "cero", "cero"
    while actual != objetivo:
        uno = u.siguiente(actual)
        if uno == objetivo:
            return u.leer(cada), 1
        actual = u.siguiente(uno)
        cada = u.siguiente(cada)
    return u.leer(cada), 0


def _por_sitios(u, t):
    """De izquierda a derecha: la mitad de cada cifra (con la decena que se cambio si sobro uno)."""
    cociente, sobra = [], 0
    for c in reversed(u.cifras_de(t)):
        actual = u.escribir_cifras([c, 1]) if sobra else c
        q, sobra = _parejas(u, u.decir(actual))
        cociente.append(q)
    return u.escribir_cifras(list(reversed(cociente))), sobra


def hacer(s, u):
    t = s["total"]
    if not u.viene_despues(u.decir(t), "cien"):
        v, resto = _parejas(u, u.decir(t))
        return {"valor": v, "resto": resto, "metodo": "la mitad (M.3)",
                "cuenta": ("parejas, una para cada lado: %d para cada lado y SOBRA 1" % v) if resto else
                          "parejas, una para cada lado: %d para cada lado, no sobra ninguno" % v,
                "vuelta": "", "vuelta_ok": True}
    v, resto = _por_sitios(u, t)
    doble = u.sumar_por_columnas(v, v)
    vuelta = u.sumar_por_columnas(doble, 1) if resto else doble
    return {"valor": v, "resto": resto, "metodo": "la mitad por sitios (M.3, M.14)",
            "cuenta": "la mitad de cada cifra, de izquierda a derecha (si sobra uno, se cambia por diez de la de "
                      "al lado): %d%s" % (v, ", y SOBRA 1" if resto else ""),
            "vuelta": "%d + %d%s = %d" % (v, v, " + 1" if resto else "", vuelta), "vuelta_ok": vuelta == t}
