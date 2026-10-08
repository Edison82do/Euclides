# -*- coding: utf-8 -*-
"""Pieza de COMPARAR FRACCIONES (paso F.6; NCETM 3.7, punto 1): dos fracciones que no comparten ni el de arriba ni
el de abajo pueden ser EQUIVALENTES: 3/12 y 1/4 se simplifican a la misma (1/4) -> son IGUALES.  (La trampa del
audit de NCETM: creer que 3/12 es mayor porque sus numeros son mas grandes.)  Si no son equivalentes, para saber
cual es mayor hace falta el mismo de abajo: eso es del paso siguiente (NCETM 3.8): no sale.
LA VUELTA: desde la forma mas simple se multiplica de vuelta hasta cada una (la contraria de simplificar)."""

PIEZA = {
    "id": "fracciones_equivalentes_simplificando",
    "nombre": "simplificar las dos (equivalentes?)",
    "unidad": "F.6",
    "responde": "comparar_fracciones",
    "rapidez": 5,
    "que_hace": "3/12 y 1/4: las dos se simplifican a 1/4 -> son iguales (equivalentes)",
    "condiciones": [
        ("no_comparten_arriba_ni_abajo", "comparten el de arriba o el de abajo (eso ya se compara sin simplificar)"),
    ],
    "usa": ["simplificar_fraccion", "dividir", "multiplicar"],
}


def hacer(s, u):
    fa, fb = s["a"], s["b"]
    ra = u.usar("simplificar_fraccion", a=fa[0], b=fa[1])["resultado"]
    rb = u.usar("simplificar_fraccion", a=fb[0], b=fb[1])["resultado"]
    if ra["valor"] != rb["valor"]:
        raise ValueError("no son equivalentes (%d/%d = %s y %d/%d = %s); para saber cual es mayor hace falta el mismo "
                         "de abajo (NCETM 3.8): todavia no" % (fa[0], fa[1], ra["valor"], fb[0], fb[1], rb["valor"]))
    sa, sb = ra["arriba"], ra["abajo"]
    vuelta, ok = [], True
    for f in (fa, fb):                     # la forma mas simple, por k, tiene que dar cada una
        k = u.usar("dividir", total=f[1], divisor=sb)["valor"]
        va = u.usar("multiplicar", a=sa, b=k)["valor"]
        vb = u.usar("multiplicar", a=sb, b=k)["valor"]
        vuelta.append("%d/%d x %d = %d/%d" % (sa, sb, k, va, vb))
        ok = ok and (va, vb) == f
    return {"valor": "=", "metodo": "simplificar las dos (F.6)",
            "cuenta": "%d/%d = %s y %d/%d = %s: la MISMA forma mas simple, son EQUIVALENTES (valen lo mismo; que "
                      "los numeros de una sean mas grandes no la hace mayor: sus partes son mas pequenas)"
                      % (fa[0], fa[1], ra["valor"], fb[0], fb[1], rb["valor"]),
            "vuelta": ";  ".join(vuelta), "vuelta_ok": ok}
