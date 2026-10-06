# -*- coding: utf-8 -*-
"""Pieza de DIVIDIR (paso M.3; NCETM 2.6, punto 4: 'usar los hechos de multiplicar que ya se saben';
Common Core 3.OA.B.6: dividir es buscar un FACTOR DESCONOCIDO).  30 : 5 -> que numero por 5 da 30?
En la memoria esta 6 x 5 = 30: el cociente es 6."""

PIEZA = {
    "id": "dividir_con_la_tabla",
    "nombre": "la tabla que me se (factor desconocido)",
    "unidad": "M.3",
    "responde": "dividir",
    "rapidez": 3,
    "que_hace": "busca en la memoria que numero por el divisor da el total",
    "condiciones": [
        ("el_divisor_no_es_cero", "el divisor es cero: no se puede repartir entre nadie"),
        ("se_permite_recordar", "se pidio hacerlo sin memoria"),
        ("la_division_esta_en_las_tablas", "no tengo en la memoria ningun producto con ese divisor que de ese total"),
    ],
    "usa": [],
}


def hacer(s, u):
    q = "cero"
    while True:
        h = u.recuerdo("%d x %d" % (u.leer(q), s["divisor"]))
        if h and h["valor"] == s["total"]:
            v = u.leer(q)
            return {"valor": v, "resto": 0, "metodo": "la tabla (M.3)",
                    "cuenta": "que numero por %d da %d?  En la memoria: %d x %d = %d  -> %d"
                              % (s["divisor"], s["total"], v, s["divisor"], s["total"], v),
                    "vuelta": "", "vuelta_ok": True}
        if q == "diez":
            raise ValueError("no esta en las tablas que me se")
        q = u.siguiente(q)
