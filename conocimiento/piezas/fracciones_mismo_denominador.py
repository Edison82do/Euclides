# -*- coding: utf-8 -*-
"""Pieza de COMPARAR FRACCIONES (paso F.2; NCETM 3.3, punto 7; 3.NF.A.3d): con el MISMO DENOMINADOR las
partes son del mismo tamano, asi que manda el numerador: mas partes es mas."""

PIEZA = {
    "id": "fracciones_mismo_denominador",
    "nombre": "mismo de abajo: manda el de arriba",
    "unidad": "F.2",
    "responde": "comparar_fracciones",
    "rapidez": 2,
    "que_hace": "las partes son del mismo tamano: la que toma mas partes es mayor",
    "condiciones": [
        ("mismo_denominador", "no tienen el mismo de abajo"),
    ],
    "usa": [],
}


def hacer(s, u):
    (na, d), (nb, _) = s["a"], s["b"]
    if na == nb:
        valor, dice = "=", "toman las mismas partes: son iguales"
    elif u.viene_despues(u.decir(na), u.decir(nb)):
        valor, dice = ">", "%d partes son mas que %d partes" % (na, nb)
    else:
        valor, dice = "<", "%d partes son menos que %d partes" % (na, nb)
    return {"valor": valor, "metodo": "mismo de abajo (F.2)",
            "cuenta": "las dos son de partes de 1/%d (del mismo tamano): %s" % (d, dice),
            "vuelta": "", "vuelta_ok": True}
