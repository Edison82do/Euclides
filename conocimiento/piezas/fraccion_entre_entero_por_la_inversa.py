# -*- coding: utf-8 -*-
"""Pieza de UNA FRACCION ENTRE UN ENTERO convirtiendola en una multiplicacion (paso F.8; NCETM 3.9, punto 2: 'To divide
a fraction by a whole number, convert it to an equivalent multiplication'; Common Core 5.NF.B.7a).
    2/3 : 4   ->  dividir entre 4 es tomar la cuarta parte: 2/3 x 1/4 = 2/12   (luego se simplifica: 1/6)
Cada trozo se parte en 4: el de abajo se multiplica por 4 y el de arriba no cambia.  Sirve siempre (tambien cuando el
entero no cabe en el de arriba), pero cuesta mas que repartir los de arriba si caben.
OJO, el error tipico: multiplicar arriba Y abajo por el entero (2/3 : 4 = 8/12, que es 2/3 otra vez).
LA VUELTA, con la contraria: el resultado por el entero (arriba x 4) da 8/12, y dividiendo los dos entre 4 (sin resto)
vuelve a 2/3."""

PIEZA = {
    "id": "fraccion_entre_entero_por_la_inversa",
    "nombre": "convertirlo en una multiplicacion (2/3 : 4 = 2/3 x 1/4 = 2/12)",
    "unidad": "F.8",
    "responde": "fraccion_entre_entero",
    "rapidez": 6,
    "que_hace": "2/3 : 4 = 2/3 x 1/4 = 2/12: el de abajo por el entero (NCETM 3.9, punto 2; 5.NF.B.7a)",
    "condiciones": [
        ("es_una_fraccion_entre_un_entero", "no es una fraccion entre un entero (sin ceros)"),
    ],
    "usa": ["multiplicar", "dividir"],
}


def hacer(s, u):
    a, b, n = s["a"], s["b"], s["n"]
    arriba = a                                       # el de arriba no cambia (por 1)
    abajo = u.usar("multiplicar", a=b, b=n)["valor"]
    if u.decir(abajo) is None:
        raise ValueError("%d x %d se pasa de mi lista" % (b, n))
    pasos = ["dividir entre %d es tomar 1/%d: %d/%d : %d = %d/%d x 1/%d" % (n, n, a, b, n, a, b, n),
             "arriba por arriba: %d x 1 = %d;  abajo por abajo: %d x %d = %d" % (a, a, b, n, abajo),
             "%d/%d : %d = %d/%d" % (a, b, n, arriba, abajo)]
    # LA VUELTA: el resultado por el entero, y deshacer dividiendo los dos entre el entero
    arriba_n = u.usar("multiplicar", a=arriba, b=n)["valor"]
    if u.decir(arriba_n) is None:
        raise ValueError("%d x %d se pasa de mi lista (no puedo comprobar)" % (arriba, n))
    ra = u.usar("dividir", total=arriba_n, divisor=n)
    rb = u.usar("dividir", total=abajo, divisor=n)
    ok = ra["valor"] == a and rb["valor"] == b and not ra["resultado"].get("resto", 0) \
        and not rb["resultado"].get("resto", 0)
    return {"valor": (arriba, abajo),
            "metodo": "convertir la division en una multiplicacion (F.8; NCETM 3.9, punto 2)",
            "pasos": pasos, "cuenta": "; ".join(pasos),
            "vuelta": "%d/%d x %d = %d/%d;  %d : %d = %d y %d : %d = %d ... %s"
                      % (arriba, abajo, n, arriba_n, abajo, arriba_n, n, ra["valor"], abajo, n, rb["valor"],
                         "SI" if ok else "NO"),
            "vuelta_ok": ok,
            "vuelta_explicada": "%d/%d x %d = %d/%d, y dividiendo arriba y abajo entre %d vuelve a %d/%d"
                                % (arriba, abajo, n, arriba_n, abajo, n, a, b)}
