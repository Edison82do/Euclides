# -*- coding: utf-8 -*-
"""Pieza de SIMPLIFICAR UNA FRACCION (paso F.6; NCETM 3.7, punto 3): CON EL MAYOR FACTOR COMUN.  Se sacan los
factores del de arriba y los del de abajo (M.15: probando 1, 2, 3 ... dividiendo, hasta cruzarse), se miran los que
estan en las dos listas y se divide entre el MAYOR: 12/18 -> factores de 12: 1, 2, 3, 4, 6, 12; de 18: 1, 2, 3, 6, 9,
18; el mayor comun es 6 -> 2/3 de una vez.  Es mas largo (dos listas) y con las tablas solo llega hasta 168.
LA VUELTA: multiplicar de vuelta arriba y abajo por el factor comun."""

PIEZA = {
    "id": "simplificar_con_el_mayor_factor_comun",
    "nombre": "con el mayor factor comun (las dos listas)",
    "unidad": "F.6",
    "responde": "simplificar_fraccion",
    "rapidez": 9,
    "que_hace": "12/18: los factores de 12 y de 18; el mayor comun es 6 -> 2/3 de una vez",
    "condiciones": [
        ("ninguno_es_cero", "arriba o abajo hay un cero"),
    ],
    "usa": ["parejas_de_factores", "dividir", "multiplicar"],
}


def hacer(s, u):
    a, b = s["a"], s["b"]
    fa = u.usar("parejas_de_factores", n=a)["resultado"]["factores"]
    fb = u.usar("parejas_de_factores", n=b)["resultado"]["factores"]
    comunes = [f for f in fa if f in fb]
    g = comunes[-1]                      # las listas van de menor a mayor: el ultimo comun es el mayor
    arriba = u.usar("dividir", total=a, divisor=g)["valor"]
    abajo = u.usar("dividir", total=b, divisor=g)["valor"]
    va = u.usar("multiplicar", a=arriba, b=g)["valor"]
    vb = u.usar("multiplicar", a=abajo, b=g)["valor"]
    lista = lambda xs: ", ".join("%d" % x for x in xs)
    cuenta = ["los factores de %d: %s" % (a, lista(fa)), "los factores de %d: %s" % (b, lista(fb)),
              "en las dos listas: %s;  el MAYOR es %d" % (lista(comunes), g)]
    if g == 1:
        cuenta.append("solo comparten el 1: ya esta en su forma mas simple")
    else:
        cuenta.append("divido arriba y abajo entre %d: %d : %d = %d,  %d : %d = %d" % (g, a, g, arriba, b, g, abajo))
    return {"valor": "%d" % arriba if abajo == 1 else "%d/%d" % (arriba, abajo), "arriba": arriba, "abajo": abajo,
            "pasos": [(g, "el mayor factor comun")] if g != 1 else [],
            "metodo": "con el mayor factor comun (F.6; M.15)", "cuenta": "\n".join(cuenta),
            "por_que_ya": "despues de dividir entre el MAYOR factor comun ya no comparten nada mas que el 1",
            "vuelta": "%d x %d = %d y %d x %d = %d -> %d/%d" % (arriba, g, va, abajo, g, vb, va, vb),
            "vuelta_ok": (va, vb) == (a, b)}
