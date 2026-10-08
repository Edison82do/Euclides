# -*- coding: utf-8 -*-
"""Pieza de SIMPLIFICAR UNA FRACCION (paso F.6; NCETM 3.7, puntos 2 y 3): LA RELACION VERTICAL.  Si el de arriba
cabe justo en el de abajo (5/20: 20 : 5 = 4), el de abajo es 4 veces el de arriba, como en 1/4: de una vez,
5/20 = 1/4 (se divide arriba y abajo entre el 5, que es un factor comun).  Al reves con las impropias: 12/4, el de
arriba es 3 veces el de abajo: 12/4 = 3/1 = 3.  Lo que sale ya es lo mas simple: arriba (o abajo) queda un 1.
LA VUELTA: multiplicar de vuelta arriba y abajo por lo que se dividio; tiene que salir la de partida."""

PIEZA = {
    "id": "simplificar_por_el_de_arriba",
    "nombre": "el pequeno cabe justo en el grande (vertical)",
    "unidad": "F.6",
    "responde": "simplificar_fraccion",
    "rapidez": 3,
    "que_hace": "5/20: 20 : 5 = 4, el de abajo es 4 veces el de arriba -> 1/4 de una vez",
    "condiciones": [
        ("ninguno_es_cero", "arriba o abajo hay un cero"),
        ("ninguno_es_uno", "arriba o abajo ya hay un 1: no hay nada que dividir"),
        ("el_pequeno_cabe_justo_en_el_grande", "el mas pequeno no cabe justo en el mas grande (sobra algo al dividir)"),
    ],
    "usa": ["dividir", "multiplicar"],
}


def hacer(s, u):
    a, b = s["a"], s["b"]
    impropia = u.viene_despues(u.decir(a), u.decir(b))
    chico, grande = (b, a) if impropia else (a, b)
    k = u.usar("dividir", total=grande, divisor=chico)["valor"]
    arriba, abajo = (k, 1) if impropia else (1, k)
    # LA VUELTA: arriba y abajo por el que se dividio (el pequeno)
    va = u.usar("multiplicar", a=arriba, b=chico)["valor"]
    vb = u.usar("multiplicar", a=abajo, b=chico)["valor"]
    if a == b:
        cuenta = "arriba y abajo son el mismo numero: divido los dos entre %d -> 1/1 = 1 (un entero)" % a
    elif impropia:
        cuenta = "el de arriba es %d veces el de abajo (%d : %d = %d): divido los dos entre %d -> %d/1 = %d" % (
            k, a, b, k, b, k, k)
    else:
        cuenta = "el de abajo es %d veces el de arriba (%d : %d = %d): divido los dos entre %d -> 1/%d" % (
            k, b, a, k, a, k)
    return {"valor": "%d" % arriba if abajo == 1 else "%d/%d" % (arriba, abajo), "arriba": arriba, "abajo": abajo,
            "pasos": [(chico, "el pequeno cabe justo en el grande")],
            "metodo": "el pequeno cabe justo en el grande (F.6)", "cuenta": cuenta,
            "por_que_ya": "queda un 1 %s: el unico factor del 1 es el 1" % ("abajo" if impropia else "arriba"),
            "vuelta": "%d x %d = %d y %d x %d = %d -> %d/%d" % (arriba, chico, va, abajo, chico, vb, va, vb),
            "vuelta_ok": (va, vb) == (a, b)}
