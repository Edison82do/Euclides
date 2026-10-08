# -*- coding: utf-8 -*-
"""Pieza del MISMO DE ABAJO (paso F.7; NCETM 3.8, punto 4): fracciones NO relacionadas.  1/3 y 1/4: ni 4 : 3 ni 3 : 4
son justos.  El PRODUCTO de los de abajo sirve siempre: 3 x 4 = 12.  Cada una, arriba y abajo, POR EL DE ABAJO DE LA
OTRA: 1/3 = 4/12 (x 4) y 1/4 = 3/12 (x 3).  (Common Core 5.NF.A.1: a/b + c/d = (ad + bc)/bd.)
LA VUELTA: cada una se divide de vuelta entre lo que se multiplico y tiene que salir la de partida."""

PIEZA = {
    "id": "mismo_de_abajo_multiplicando_los_de_abajo",
    "nombre": "multiplicar los de abajo (sirve siempre)",
    "unidad": "F.7",
    "responde": "mismo_de_abajo",
    "rapidez": 6,
    "que_hace": "1/3 y 1/4: 3 x 4 = 12 -> 4/12 y 3/12",
    "condiciones": [
        ("los_de_abajo_son_distintos", "tienen el mismo de abajo (o hay un cero abajo): no hay nada que cambiar"),
    ],
    "usa": ["dividir", "multiplicar"],
}


def hacer(s, u):
    fa, fb = s["a"], s["b"]
    abajo = u.usar("multiplicar", a=fa[1], b=fb[1])["valor"]
    if u.decir(abajo) is None:
        raise ValueError("%d x %d = %d no esta en mi lista" % (fa[1], fb[1], abajo))
    nuevas, vueltas, ok = [], [], True
    for f, k in ((fa, fb[1]), (fb, fa[1])):
        arriba = u.usar("multiplicar", a=f[0], b=k)["valor"]
        va = u.usar("dividir", total=arriba, divisor=k)
        vb = u.usar("dividir", total=abajo, divisor=k)
        ok = ok and (va["valor"], vb["valor"]) == f and not va["resultado"].get("resto", 0) \
            and not vb["resultado"].get("resto", 0)
        nuevas.append((arriba, abajo))
        vueltas.append("%d/%d : %d -> %d/%d" % (arriba, abajo, k, va["valor"], vb["valor"]))
    return {"valor": tuple(nuevas), "abajo": abajo, "por": (fb[1], fa[1]),
            "metodo": "multiplicar los de abajo (F.7)",
            "cuenta": "%d x %d = %d.  Cada una por el de abajo de la otra: %d/%d = %d/%d (x %d) y %d/%d = %d/%d (x %d)"
                      % (fa[1], fb[1], abajo, fa[0], fa[1], nuevas[0][0], abajo, fb[1], fb[0], fb[1], nuevas[1][0],
                         abajo, fa[1]),
            "vuelta": ";  ".join(vueltas), "vuelta_ok": ok}
