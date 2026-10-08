# -*- coding: utf-8 -*-
"""Pieza de COMPARAR FRACCIONES (paso F.7; NCETM 3.8, punto 5): 2/3 y 3/4 no comparten ni el de arriba ni el de abajo.
Se pasan al MISMO DE ABAJO (pregunta mismo_de_abajo): 8/12 y 9/12.  Ahora las partes son del mismo tamano y manda el
de arriba (F.2): 8 partes son menos que 9 -> 2/3 < 3/4.
LA VUELTA: cada fraccion nueva se divide de vuelta (arriba y abajo entre lo que se multiplico) y tiene que salir la de
partida; y las dos nuevas tienen que tener el MISMO de abajo.  (No se fia de la comprobacion de la otra pieza.)"""

PIEZA = {
    "id": "fracciones_con_el_mismo_de_abajo",
    "nombre": "pasarlas al mismo de abajo",
    "unidad": "F.7",
    "responde": "comparar_fracciones",
    "rapidez": 6,
    "que_hace": "2/3 y 3/4 -> 8/12 y 9/12: 8 doceavos son menos que 9 -> 2/3 < 3/4",
    "condiciones": [
        ("no_comparten_arriba_ni_abajo", "comparten el de arriba o el de abajo (eso ya se compara sin cambiarlas)"),
    ],
    "usa": ["mismo_de_abajo", "dividir"],
}


def hacer(s, u):
    fa, fb = s["a"], s["b"]
    r = u.usar("mismo_de_abajo", a=fa, b=fb)
    (xa, d1), (xb, d2) = r["valor"]
    res = r["resultado"]
    if xa == xb:
        valor, dice = "=", "toman las mismas partes: son IGUALES (equivalentes)"
    elif u.viene_despues(u.decir(xa), u.decir(xb)):
        valor, dice = ">", "%d partes son mas que %d" % (xa, xb)
    else:
        valor, dice = "<", "%d partes son menos que %d" % (xa, xb)
    vueltas, ok = [], d1 == d2
    for (x, d), k, f in (((xa, d1), res["por"][0], fa), ((xb, d2), res["por"][1], fb)):
        va, vb = u.usar("dividir", total=x, divisor=k), u.usar("dividir", total=d, divisor=k)
        ok = ok and (va["valor"], vb["valor"]) == f and not va["resultado"].get("resto", 0) \
            and not vb["resultado"].get("resto", 0)
        vueltas.append("%d/%d : %d -> %d/%d" % (x, d, k, va["valor"], vb["valor"]))
    return {"valor": valor, "metodo": "el mismo de abajo (F.7)",
            "cuenta": "%s -> %d/%d y %d/%d: partes del mismo tamano, %s" % (res["cuenta"], xa, d1, xb, d2, dice),
            "vuelta": ";  ".join(vueltas), "vuelta_ok": ok}
