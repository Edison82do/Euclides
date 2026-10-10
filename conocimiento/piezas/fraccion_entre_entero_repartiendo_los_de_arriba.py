# -*- coding: utf-8 -*-
"""Pieza de UNA FRACCION ENTRE UN ENTERO repartiendo los de arriba (paso F.8; NCETM 3.9, punto 3: 'A more efficient
method can be used to divide a fraction by a whole number when the whole number is a factor of the numerator').
    6/7 : 3   ->  el 3 cabe justo en el 6: 6 septimos : 3 = 2 septimos  (como 6 manzanas : 3 = 2 manzanas)
Solo si el entero cabe JUSTO en el de arriba (se mira dividiendo).  El de abajo no se toca: dice el tamano de los trozos.
OJO, el error tipico: dividir tambien el de abajo (6/9 : 3 = 2/3, que es el mismo numero).
LA VUELTA, con la contraria: lo que sale por el entero vuelve al de arriba (2 x 3 = 6: 6/7)."""

PIEZA = {
    "id": "fraccion_entre_entero_repartiendo_los_de_arriba",
    "nombre": "repartir los de arriba (6/7 : 3 = 2/7)",
    "unidad": "F.8",
    "responde": "fraccion_entre_entero",
    "rapidez": 3,
    "que_hace": "6/7 : 3 = (6 : 3)/7 = 2/7, si el entero cabe justo en el de arriba (NCETM 3.9, punto 3)",
    "condiciones": [
        ("es_una_fraccion_entre_un_entero", "no es una fraccion entre un entero (sin ceros)"),
        ("el_entero_cabe_justo_en_el_de_arriba", "el entero no cabe justo en el de arriba: no se reparte justo"),
    ],
    "usa": ["dividir", "multiplicar"],
}


def hacer(s, u):
    a, b, n = s["a"], s["b"], s["n"]
    r = u.usar("dividir", total=a, divisor=n)
    q = r["valor"]
    if r["resultado"].get("resto", 0):
        raise ValueError("%d no se reparte justo entre %d" % (a, n))
    abajo = b                                        # el de abajo no se toca: dice el tamano de los trozos
    pasos = ["%d cabe justo en %d: reparto los de arriba, %d : %d = %d (el de abajo, %d, no se toca)" % (n, a, a, n, q, b),
             "%d/%d : %d = %d/%d" % (a, b, n, q, abajo)]
    # LA VUELTA: lo que sale por el entero (arriba por el entero; los trozos, del mismo tamano) vuelve a la de partida
    vuelta = u.usar("multiplicar", a=q, b=n)["valor"]
    ok = vuelta == a and abajo == b
    return {"valor": (q, abajo),
            "metodo": "repartir los de arriba (F.8; NCETM 3.9, punto 3)",
            "pasos": pasos, "cuenta": "; ".join(pasos),
            "vuelta": "%d/%d x %d = %d/%d ... %s" % (q, abajo, n, vuelta, abajo, "SI" if ok else "NO"), "vuelta_ok": ok,
            "vuelta_explicada": "%d/%d x %d = %d/%d, vuelve a la de partida" % (q, abajo, n, vuelta, abajo)}
