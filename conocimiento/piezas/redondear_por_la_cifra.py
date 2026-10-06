# -*- coding: utf-8 -*-
"""Pieza de REDONDEAR (paso N.2; 3.NBT.A.1), el ATAJO: mirar solo la cifra de justo a la derecha del
sitio.  Si es 5, 6, 7, 8 o 9 (de la mitad para arriba) se sube; si es 0, 1, 2, 3 o 4 se queda.  Es la
regla que resume lo que se ve en la recta; por eso se hace junto con la recta y tienen que coincidir."""

PIEZA = {
    "id": "redondear_por_la_cifra",
    "nombre": "el atajo: la cifra de la derecha",
    "unidad": "N.2",
    "responde": "redondear",
    "rapidez": 3,
    "que_hace": "mira la cifra de justo a la derecha del sitio: de cinco para arriba sube, si no se queda",
    "condiciones": [
        ("se_puede_redondear", "el numero no esta en mi lista (hasta mil), o el sitio no es decena ni centena"),
    ],
    "usa": [],
}

_SITIOS = {"decena": (1, (0,), 0, "diez", "unidades"), "centena": (2, (0, 1), 1, "cien", "decenas"),
           "millar": (3, (0, 1, 2), 2, "mil", "centenas")}                     # N.3: tambien al millar


def hacer(s, u):
    n = s["n"]
    i, derecha, junto, salto, nombre_junto = _SITIOS[s["a"]]
    cif = u.cifras_de(n)
    while len(cif) <= i:
        cif.append(0)
    abajo_c = list(cif)
    for j in derecha:
        abajo_c[j] = 0
    abajo = u.escribir_cifras(abajo_c)
    d = cif[junto]
    if abajo == n:
        valor, por = n, "a la derecha todo son ceros: ya es redondo"
    elif d == 5 or u.viene_despues(u.decir(d), "cinco"):
        valor = u.saltar(abajo, salto)
        por = "la cifra de las %s es %d (de cinco para arriba): SUBE a %d" % (nombre_junto, d, valor)
    else:
        valor = abajo
        por = "la cifra de las %s es %d (menos de cinco): se QUEDA en %d" % (nombre_junto, d, valor)
    return {"valor": valor, "metodo": "el atajo de la cifra (N.2)", "cuenta": por, "vuelta": "", "vuelta_ok": True}
