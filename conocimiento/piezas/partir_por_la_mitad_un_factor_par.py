# -*- coding: utf-8 -*-
"""Pieza de LA MITAD DE UN PRODUCTO partiendo antes un factor PAR (paso M.24; NCETM 2.30, punto 2: 'el area de un
triangulo es la base por la altura perpendicular, y luego dividir entre dos').
    6 x 4 : 2   ->  el 6 es par: su mitad es 3;  3 x 4 = 12          (en vez de 24 : 2)
    13 x 8 : 2  ->  el 8 es par: su mitad es 4;  13 x 4 = 52
Es la asociativa de los tres factores (M.14, NCETM 2.20): partir antes o despues da lo mismo, y antes las cuentas son
mas pequenas.  Solo si uno de los factores es PAR (se mira la ultima cifra): si no, la mitad tendria un trozo.
OJO, el error tipico: partir LOS DOS factores (6 x 4 : 2 = 3 x 2 = 6): es la mitad de la mitad.
LA VUELTA, con la contraria y por otro camino: el doble de lo que sale tiene que ser a x b, multiplicado entero."""

PIEZA = {
    "id": "partir_por_la_mitad_un_factor_par",
    "nombre": "partir antes por la mitad el factor par (6 x 4 : 2 = 3 x 4)",
    "unidad": "M.24",
    "responde": "mitad_de_un_producto",
    "rapidez": 4,
    "que_hace": "6 x 4 : 2 = 3 x 4 = 12: la mitad del factor par, y luego multiplicar (NCETM 2.30; M.14)",
    "condiciones": [
        ("es_un_producto_de_dos_enteros_entre_dos", "no es a x b : 2 con dos enteros (que no sean 0)"),
        ("uno_de_los_factores_es_par", "ninguno de los dos factores es par: su mitad tendria un trozo"),
    ],
    "usa": ["dividir", "multiplicar", "sumar"],
}


def _es_par(u, n):
    return u.cifras_de(n)[0] in (0, 2, 4, 6, 8)


def hacer(s, u):
    a, b = s["a"], s["b"]
    par, otro = (a, b) if _es_par(u, a) else (b, a)
    r = u.usar("dividir", total=par, divisor=2)
    mitad = r["valor"]
    if r["resultado"].get("resto", 0):
        raise ValueError("la mitad de %d no salio justa" % par)
    v = otro if mitad == 1 else u.usar("multiplicar", a=mitad, b=otro)["valor"] if mitad else 0
    if u.decir(v) is None:
        raise ValueError("el producto se pasa de mi lista")
    pasos = ["%d es par: su mitad es %d" % (par, mitad),
             "%d x %d = %d" % (mitad, otro, v) if par == a else "%d x %d = %d" % (otro, mitad, v)]
    # LA VUELTA: el doble de lo que sale; y a x b por el otro camino (multiplicando los factores enteros)
    doble = u.usar("sumar", a=v, b=v)["valor"]
    entero = u.usar("multiplicar", a=a, b=b)["valor"]
    ok = doble == entero
    return {"valor": v, "resto": 0,
            "metodo": "partir antes el factor par por la mitad (M.24; NCETM 2.30)",
            "pasos": pasos, "cuenta": "; ".join(pasos),
            "vuelta": "%d + %d = %d;  %d x %d = %d ... %s" % (v, v, doble, a, b, entero, "SI" if ok else "NO"),
            "vuelta_ok": ok,
            "vuelta_explicada": "el doble de %d es %d, que es %d x %d multiplicado entero" % (v, doble, a, b)}
