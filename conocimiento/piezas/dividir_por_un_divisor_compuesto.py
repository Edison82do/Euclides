# -*- coding: utf-8 -*-
"""Pieza de DIVIDIR (paso M.18; NCETM 2.24, la division usando factores; la contraria del punto 5 de 2.23): si el
divisor de dos cifras es una pareja de la tabla (24 = 4 x 6), se divide entre uno de sus factores y luego entre el otro:
dos divisiones cortas.
    8544 : 24 = 8544 : 4 : 6:  8544 : 4 = 2136;  2136 : 6 = 356
Solo si se reparte JUSTO las dos veces: con resto, el resto cambia de tamano por el camino (437 : 3 : 4 no deja el
resto de 437 : 12), y eso se deja a la division larga.  La pareja se busca en lo que se sabe de memoria, la de en medio.
LA VUELTA: el cociente por el segundo factor y luego por el primero (la multiplicacion corta) vuelve al dividendo."""

PIEZA = {
    "id": "dividir_por_un_divisor_compuesto",
    "nombre": "dividir usando los factores del divisor (: 24 = : 4 y : 6)",
    "unidad": "M.18",
    "responde": "dividir",
    "rapidez": 9.2,
    "que_hace": "parte el divisor de dos cifras en dos de la tabla (24 = 4 x 6) y hace dos divisiones cortas",
    "condiciones": [
        ("el_divisor_de_dos_cifras_es_una_pareja_de_la_tabla",
         "el divisor no es de dos cifras con el cociente de 10 o mas, o no es una pareja de la tabla que me se"),
    ],
    "usa": ["division_corta", "multiplicacion_corta"],
}


def _pareja(u, f):
    if len(u.cifras_de(f)) != 2 or u.cifras_de(f)[0] == 0:
        return None
    mejor = None
    for p in range(2, 10):
        for q in range(p, 10):
            h = u.recuerdo("%d x %d" % (p, q)) or u.recuerdo("%d x %d" % (q, p))
            if h and h["valor"] == f:
                mejor = (p, q)
    return mejor


def hacer(s, u):
    t, d = s["total"], s["divisor"]
    par = _pareja(u, d)
    if not par:
        raise ValueError("%d no es una pareja de la tabla que me se" % d)
    p, q = par
    r1 = u.usar("division_corta", total=t, divisor=p)
    if r1["resultado"].get("resto"):
        raise ValueError("%d : %d no es justa: con resto, el resto cambia de tamano por el camino (uso otro metodo)"
                         % (t, p))
    m = r1["valor"]
    r2 = u.usar("division_corta", total=m, divisor=q)
    if r2["resultado"].get("resto"):
        raise ValueError("%d : %d no es justa: con resto, el resto cambia de tamano por el camino (uso otro metodo)"
                         % (m, q))
    c = r2["valor"]
    # LA VUELTA: deshacer con la multiplicacion, de la ultima a la primera
    v1 = u.usar("multiplicacion_corta", a=c, b=q)["valor"]
    v2 = u.usar("multiplicacion_corta", a=v1, b=p)["valor"]
    ok = v1 == m and v2 == t
    return {"valor": c, "resto": 0, "metodo": "dividir usando los factores del divisor (M.18; NCETM 2.24)",
            "cuenta": "%d = %d x %d, asi que %d : %d = %d : %d : %d; %d : %d = %d   (la corta); %d : %d = %d   (la corta)"
                      % (d, p, q, t, d, t, p, q, t, p, m, m, q, c),
            "vuelta": "%d x %d = %d; %d x %d = %d ... %s" % (c, q, v1, v1, p, v2, "SI" if ok else "NO"),
            "vuelta_ok": ok,
            "vuelta_explicada": "con la operacion contraria: multiplicando por %d y luego por %d vuelve %d" % (q, p, t)}
