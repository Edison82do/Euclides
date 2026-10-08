# -*- coding: utf-8 -*-
"""Pieza del HUECO EN DOS FRACCIONES EQUIVALENTES (paso F.6; NCETM 3.7, puntos 2 y 3): SIMPLIFICAR PRIMERO.
4/6 = ?/9: de 6 a 9 no es por un numero justo, y dentro de 4/6 tampoco.  Primero simplifico: 4/6 = 2/3; y de 3 a 9
es por 3: 2 x 3 = 6.  Si el numero que se sabe NO es multiplo del de la forma mas simple (2/3 = ?/10: 10 no es
multiplo de 3), NO HAY NINGUN ENTERO que vaya en el hueco.
LA VUELTA: la que sale se simplifica (dividiendo) y tiene que dar la misma forma mas simple."""

PIEZA = {
    "id": "hueco_simplificando_primero",
    "nombre": "simplificar primero y luego multiplicar",
    "unidad": "F.6",
    "responde": "hueco_equivalente",
    "rapidez": 8,
    "que_hace": "4/6 = ?/9: 4/6 = 2/3, y de 3 a 9 es x 3: 6",
    "condiciones": [
        ("hay_un_hueco_y_una_fraccion_completa", "no hay una fraccion completa y otra con UN hueco"),
    ],
    "usa": ["dividir", "multiplicar", "simplificar_fraccion"],
}


def hacer(s, u):
    (p, q), (x, y) = s["completa"], s["con_hueco"]
    r = u.usar("simplificar_fraccion", a=p, b=q)["resultado"]
    sa, sb = r["arriba"], r["abajo"]
    if x is None:
        de, a, otro, sitio = sb, y, sa, "abajo"
    else:
        de, a, otro, sitio = sa, x, sb, "arriba"
    d = u.usar("dividir", total=a, divisor=de)
    if d["resultado"].get("resto", 0):
        raise ValueError("NO HAY NINGUN ENTERO: %d/%d = %d/%d (la forma mas simple), y %d no es multiplo de %d "
                         "(%d : %d = %d y sobran %d)" % (p, q, sa, sb, a, de, a, de, d["valor"], d["resultado"]["resto"]))
    k = d["valor"]
    v = u.usar("multiplicar", a=otro, b=k)["valor"]
    nueva = (v, y) if x is None else (x, v)
    cuenta = "primero simplifico: %d/%d = %d/%d;  %s: de %d a %d es POR %d;  %d x %d = %d" % (
        p, q, sa, sb, sitio, de, a, k, otro, k, v)
    s2 = u.usar("simplificar_fraccion", a=nueva[0], b=nueva[1])["valor"]
    return {"valor": v, "fraccion": nueva, "metodo": "simplificar primero (F.6)", "cuenta": cuenta,
            "vuelta": "simplifico la que sale: %d/%d = %s (la misma que %d/%d)" % (nueva[0], nueva[1], s2, p, q),
            "vuelta_ok": s2 == r["valor"]}
