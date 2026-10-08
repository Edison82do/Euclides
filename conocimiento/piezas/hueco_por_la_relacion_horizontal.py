# -*- coding: utf-8 -*-
"""Pieza del HUECO EN DOS FRACCIONES EQUIVALENTES (paso F.6; NCETM 3.7, punto 2): LA RELACION HORIZONTAL.
2/3 = ?/12: de 3 a 12 es POR 4 (12 : 3 = 4, justo); arriba tiene que ser lo mismo: 2 x 4 = 8.  Y al reves,
dividiendo: 12/18 = 2/? -> de 12 a 2 es ENTRE 6 (12 : 6 = 2): 18 : 6 = 3.  Arriba y abajo, POR EL MISMO numero.
LA VUELTA: las dos fracciones se simplifican (dividiendo, la contraria de multiplicar) y dan la MISMA."""

PIEZA = {
    "id": "hueco_por_la_relacion_horizontal",
    "nombre": "la relacion horizontal (de una a la otra)",
    "unidad": "F.6",
    "responde": "hueco_equivalente",
    "rapidez": 4,
    "que_hace": "2/3 = ?/12: de 3 a 12 es x 4, asi que arriba tambien x 4: 8",
    "condiciones": [
        ("hay_un_hueco_y_una_fraccion_completa", "no hay una fraccion completa y otra con UN hueco"),
    ],
    "usa": ["dividir", "multiplicar", "simplificar_fraccion"],
}


def _justo(u, n, d):
    r = u.usar("dividir", total=n, divisor=d)
    return None if r["resultado"].get("resto", 0) else r["valor"]


def hacer(s, u):
    (p, q), (x, y) = s["completa"], s["con_hueco"]
    if x is None:                      # el hueco arriba: miro abajo (de q a y) y lo hago arriba (con p)
        de, a, otro, sitio, otro_sitio = q, y, p, "abajo", "arriba"
    else:                              # el hueco abajo: miro arriba (de p a x) y lo hago abajo (con q)
        de, a, otro, sitio, otro_sitio = p, x, q, "arriba", "abajo"
    k = _justo(u, a, de)
    if k is not None:
        v = u.usar("multiplicar", a=otro, b=k)["valor"]
        cuenta = "%s: de %d a %d es POR %d (%d : %d = %d);  %s tambien: %d x %d = %d" % (
            sitio, de, a, k, a, de, k, otro_sitio, otro, k, v)
    else:
        k = _justo(u, de, a)
        if k is None:
            raise ValueError("%s: de %d a %d no es por ni entre un numero justo" % (sitio, de, a))
        v = _justo(u, otro, k)
        if v is None:
            raise ValueError("%s: de %d a %d es entre %d, pero %d no se reparte justo entre %d" % (
                sitio, de, a, k, otro, k))
        cuenta = "%s: de %d a %d es ENTRE %d (%d : %d = %d);  %s tambien: %d : %d = %d" % (
            sitio, de, a, k, de, a, k, otro_sitio, otro, k, v)
    nueva = (v, y) if x is None else (x, v)
    return _con_la_vuelta(u, s, nueva, v, cuenta, "la relacion horizontal (F.6)")


def _con_la_vuelta(u, s, nueva, v, cuenta, metodo):
    (p, q) = s["completa"]
    s1 = u.usar("simplificar_fraccion", a=p, b=q)["valor"]
    s2 = u.usar("simplificar_fraccion", a=nueva[0], b=nueva[1])["valor"]
    return {"valor": v, "fraccion": nueva, "metodo": metodo, "cuenta": cuenta,
            "vuelta": "simplifico las dos: %d/%d = %s y %d/%d = %s" % (p, q, s1, nueva[0], nueva[1], s2),
            "vuelta_ok": s1 == s2}
