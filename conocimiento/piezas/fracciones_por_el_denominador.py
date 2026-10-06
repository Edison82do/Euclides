# -*- coding: utf-8 -*-
"""Pieza de COMPARAR FRACCIONES UNITARIAS (paso F.1; NCETM 3.2, punto 5): 'las fracciones unitarias se
comparan mirando el denominador: cuanto MAYOR el denominador, MENOR la fraccion'.  Si el entero se
parte en mas partes, cada parte es mas pequena.  (El error tipico: '5 es mas que 3, asi que 1/5 es mas'.)"""

PIEZA = {
    "id": "fracciones_por_el_denominador",
    "nombre": "la regla: mas partes, partes mas pequenas",
    "unidad": "F.1",
    "responde": "comparar_fracciones",
    "rapidez": 3,
    "que_hace": "dos fracciones unitarias: la de MAS partes es la MAS pequena",
    "condiciones": [
        ("son_fracciones_unitarias", "no son las dos de 'uno' arriba (unitarias)"),
    ],
    "usa": [],
}


def hacer(s, u):
    da, db = s["a"][1], s["b"][1]
    if da == db:
        return {"valor": "=", "metodo": "la regla (F.1)",
                "cuenta": "las dos parten el entero en %d partes: son la misma parte" % da, "vuelta": "", "vuelta_ok": True}
    mas_partes_a = u.viene_despues(u.decir(da), u.decir(db))
    valor = "<" if mas_partes_a else ">"
    mas, menos = (da, db) if mas_partes_a else (db, da)
    return {"valor": valor, "metodo": "la regla (F.1)",
            "cuenta": "en %d partes las partes son MAS PEQUENAS que en %d partes: 1/%d es menos que 1/%d"
                      % (mas, menos, mas, menos), "vuelta": "", "vuelta_ok": True}
