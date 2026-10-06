# -*- coding: utf-8 -*-
"""Pieza de COMPARAR FRACCIONES (paso F.2; NCETM 3.3, punto 8; 3.NF.A.3d): con el MISMO NUMERADOR se
toman las mismas partes, pero de tamanos distintos: manda el denominador, AL REVES (mas partes en el
entero, partes mas pequenas).  2/3 > 2/5."""

PIEZA = {
    "id": "fracciones_mismo_numerador",
    "nombre": "mismo de arriba: manda el de abajo, al reves",
    "unidad": "F.2",
    "responde": "comparar_fracciones",
    "rapidez": 3,
    "que_hace": "se toman las mismas partes: donde las partes son mas grandes (menos partes), es mayor",
    "condiciones": [
        ("mismo_numerador", "no tienen el mismo de arriba"),
    ],
    "usa": [],
}


def hacer(s, u):
    (n, da), (_, db) = s["a"], s["b"]
    if da == db:
        return {"valor": "=", "metodo": "mismo de arriba (F.2)", "cuenta": "son la misma fraccion",
                "vuelta": "", "vuelta_ok": True}
    a_mas_partes = u.viene_despues(u.decir(da), u.decir(db))
    valor = "<" if a_mas_partes else ">"
    grande, pequena = (db, da) if a_mas_partes else (da, db)
    return {"valor": valor, "metodo": "mismo de arriba (F.2)",
            "cuenta": "las dos toman %s; las de 1/%d son mas grandes que las de 1/%d (menos partes en el "
                      "entero): %d/%d es mayor" % ("1 parte" if n == 1 else "%d partes" % n, grande, pequena, n, grande),
            "vuelta": "", "vuelta_ok": True}
