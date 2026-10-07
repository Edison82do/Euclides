# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso M.15; NCETM 2.21, punto 6): 'las parejas de factores de 100 sirven para
calcular de forma eficiente'.  100 = 4 x 25 = 2 x 50 = 5 x 20.  25 x 36: 36 son 9 grupos de 4, y 25 x 4 =
100, asi que 25 x 36 = 100 x 9 = 900.  Va detras de doblar y partir (M.12), que hace lo mismo en otros
pasos; se pide por su nombre con 'con 100: 25 x 36'.
Se COMPRUEBA deshaciendo: 900 : 100 = 9, y 9 x 4 = 36 (el otro factor)."""

PIEZA = {
    "id": "multiplicar_con_las_parejas_de_100",
    "nombre": "una pareja de 100 (4 x 25, 2 x 50, 5 x 20)",
    "unidad": "M.15",
    "responde": "multiplicar",
    "rapidez": 7,
    "que_hace": "25 x 36 = 25 x 4 x 9 = 100 x 9 = 900",
    "condiciones": [
        ("un_factor_es_25_50_o_20_y_el_otro_grande", "ningun factor es 25, 50 o 20 con el otro de mas de doce"),
    ],
    "usa": ["sumar", "dividir_a_la_mitad", "dividir_por_10_o_100", "multiplicar_por_10_o_100"],
}

_COMPANERO = {25: 4, 50: 2, 20: 5}


def _veces(u, k, p):
    """k x p con p pequeno (2, 4 o 5): k + k + ... (p veces), sumando."""
    total, hechas = k, "uno"
    while hechas != u.decir(p):
        total = u.usar("sumar", a=total, b=k)["valor"]
        hechas = u.siguiente(hechas)
    return total


def _entre(u, g, p):
    """g : p sin calculadora.  Entre 2, la mitad; entre 4, la mitad de la mitad (NCETM 2.7); entre 5, el doble
    entre 10 (35 : 5 = 70 : 10).  Devuelve (cociente, si sobro algo, como)."""
    if p == 5:
        doble = u.usar("sumar", a=g, b=g)["valor"]
        r = u.usar("dividir_por_10_o_100", total=doble, divisor=10)["resultado"]
        return r["valor"], bool(r["resto"]), "%d : 5 = %d : 10" % (g, doble)
    v, como = g, ["%d" % g]
    for _ in range(2 if p == 4 else 1):
        r = u.usar("dividir_a_la_mitad", total=v, divisor=2)["resultado"]
        if r.get("resto"):
            return None, True, ""
        v = r["valor"]
        como.append("%d" % v)
    return v, False, "la mitad%s: %s" % (" de la mitad" if p == 4 else "", " -> ".join(como))


def hacer(s, u):
    a, b = s["a"], s["b"]
    f, g = (a, b) if a in _COMPANERO else (b, a)
    p = _COMPANERO[f]
    k, sobra, como = _entre(u, g, p)
    if sobra:
        raise ValueError("%d no se parte en grupos de %d sin que sobre" % (g, p))
    cien = _veces(u, f, p)
    v = u.usar("multiplicar_por_10_o_100", a=k, b=cien)["valor"]
    atras = u.usar("dividir_por_10_o_100", total=v, divisor=100)["resultado"]
    otra = _veces(u, atras["valor"], p)
    return {"valor": v, "metodo": "una pareja de 100 (M.15; NCETM 2.21, punto 6)",
            "cuenta": "%d = %d x %d (%s), y %d x %d = %d: %d x %d = %d x %d = %d"
                      % (g, k, p, como, f, p, cien, f, g, cien, k, v),
            "vuelta": "%d : 100 = %d, %d x %d = %d" % (v, atras["valor"], atras["valor"], p, otra),
            "vuelta_ok": cien == 100 and not atras["resto"] and otra == g}
