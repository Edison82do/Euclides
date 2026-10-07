# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso M.12; NCETM 2.18, punto 1): USAR LA EQUIVALENCIA.  'Si un factor sube
multiplicativamente y el otro baja de la misma manera, el producto NO CAMBIA.'  Doblar y dividir a la
mitad: 25 x 16 = 50 x 8 = 100 x 4 = 400.  Se dobla el factor que acaba en 5 (el 5 se vuelve un 0) y se
parte el otro por la mitad, mientras se pueda; al final un factor son decenas o centenas justas (M.9).
El doble es una suma (x + x); la mitad, parejas (M.3).  No hay cuenta nueva."""

PIEZA = {
    "id": "multiplicar_escalando",
    "nombre": "doblar uno y partir el otro por la mitad",
    "unidad": "M.12",
    "responde": "multiplicar",
    "rapidez": 6,
    "que_hace": "doblo el factor que acaba en 5 y parto el otro por la mitad: el producto no cambia (NCETM 2.18)",
    "condiciones": [
        ("un_factor_acaba_en_cinco_y_el_otro_es_par",
         "ningun factor acaba en 5 con el otro par (o es un hecho de las tablas)"),
    ],
    "usa": ["sumar", "dividir_a_la_mitad", "multiplicar_por_10_o_100", "multiplicar_por_decenas_justas",
            "multiplicacion_corta"],
}

_FINAL = ("multiplicar_por_10_o_100", "multiplicar_por_decenas_justas", "multiplicacion_corta")


def _sin_ceros(u, n):
    c = u.cifras_de(n)
    while len(c) > 1 and c[0] == 0:
        c = c[1:]
    return c


def _sigue(u, f, g):
    """Se puede dar otro paso: f, sin sus ceros, acaba en 5, y g es par (y no es 0)."""
    return _sin_ceros(u, f)[0] == 5 and g != 0 and u.cifras_de(g)[0] in (0, 2, 4, 6, 8)


def hacer(s, u):
    a, b = s["a"], s["b"]
    f, g = (a, b) if _sigue(u, a, b) else (b, a)
    if not _sigue(u, f, g):
        raise ValueError("ningun factor acaba en 5 con el otro par")
    cadena = ["%d x %d" % (a, b)]
    if (f, g) != (a, b):
        cadena.append("%d x %d" % (f, g))
    while _sigue(u, f, g):
        doble = u.usar("sumar", a=f, b=f)["valor"]
        mitad = u.usar("dividir_a_la_mitad", total=g, divisor=2)["valor"]
        if u.decir(doble) is None:
            raise ValueError("el doble de %d se sale de mi lista" % f)
        f, g = doble, mitad
        cadena.append("%d x %d" % (f, g))
    if g == 1:
        v, como = f, "por uno es el mismo numero"
    else:
        v = None
        for nombre in _FINAL:
            try:
                r = u.usar(nombre, a=f, b=g)
            except Exception:
                continue
            v, como = r["valor"], r["resultado"]["metodo"]
            break
        if v is None:
            raise ValueError("%d x %d tampoco me sale facil" % (f, g))
    return {"valor": v, "metodo": "doblar y partir por la mitad (M.12)",
            "cuenta": "%s = %d  (doblo uno y parto el otro por la mitad: el producto no cambia, NCETM 2.18; "
                      "%d x %d con %s)" % (" = ".join(cadena), v, f, g, como),
            "cadena": cadena,
            "vuelta": "", "vuelta_ok": True}
