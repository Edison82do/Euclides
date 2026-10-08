# -*- coding: utf-8 -*-
"""Pieza de COMPARAR FRACCIONES (paso F.7; NCETM 3.8, punto 5: 'varios metodos'): el MISMO DE ARRIBA.  2/3 y 3/4: si
uno de arriba cabe justo en el otro se cambia solo una; si no, cada una por el de arriba de la otra: 2/3 = 6/9 y
3/4 = 6/8.  Se toman las mismas partes (6), y las de 1/8 son mas grandes que las de 1/9 (F.2: manda el de abajo, al
reves) -> 3/4 es mayor.
LA VUELTA: cada una se divide de vuelta entre lo que se multiplico y tiene que salir la de partida."""

PIEZA = {
    "id": "fracciones_con_el_mismo_de_arriba",
    "nombre": "pasarlas al mismo de arriba",
    "unidad": "F.7",
    "responde": "comparar_fracciones",
    "rapidez": 7,
    "que_hace": "2/3 y 3/4 -> 6/9 y 6/8: las mismas partes, y los octavos son mas grandes -> 3/4 es mayor",
    "condiciones": [
        ("no_comparten_arriba_ni_abajo", "comparten el de arriba o el de abajo (eso ya se compara sin cambiarlas)"),
        ("ninguno_de_arriba_es_cero", "una de las dos es cero (cero partes)"),
    ],
    "usa": ["dividir", "multiplicar"],
}


def _justo(u, n, d):
    r = u.usar("dividir", total=n, divisor=d)
    return None if r["resultado"].get("resto", 0) else r["valor"]


def hacer(s, u):
    fa, fb = s["a"], s["b"]
    a_mayor = u.viene_despues(u.decir(fa[0]), u.decir(fb[0]))
    chico, grande = (fb[0], fa[0]) if a_mayor else (fa[0], fb[0])
    k = _justo(u, grande, chico)
    if k is not None:                                    # relacionados arriba: cambio solo una
        por = (1, k) if a_mayor else (k, 1)
        como = "%d : %d = %d, justo: cambio solo una (por %d)" % (grande, chico, k, k)
    else:                                                # cada una por el de arriba de la otra
        por = (fb[0], fa[0])
        como = "cada una por el de arriba de la otra"
    nuevas, vueltas, ok = [], [], True
    for f, m in ((fa, por[0]), (fb, por[1])):
        na = u.usar("multiplicar", a=f[0], b=m)["valor"]
        nb = u.usar("multiplicar", a=f[1], b=m)["valor"]
        if u.decir(nb) is None:
            raise ValueError("%d x %d = %d no esta en mi lista" % (f[1], m, nb))
        va, vb = _justo(u, na, m), _justo(u, nb, m)
        ok = ok and (va, vb) == f
        nuevas.append((na, nb))
        vueltas.append("%d/%d : %d -> %s/%s" % (na, nb, m, va, vb))
    (xa, da), (xb, db) = nuevas
    ok = ok and xa == xb
    if da == db:
        valor, dice = "=", "las mismas partes y del mismo tamano: son IGUALES"
    elif u.viene_despues(u.decir(da), u.decir(db)):
        valor, dice = "<", "las de 1/%d son mas grandes que las de 1/%d: %d/%d es mayor" % (db, da, fb[0], fb[1])
    else:
        valor, dice = ">", "las de 1/%d son mas grandes que las de 1/%d: %d/%d es mayor" % (da, db, fa[0], fa[1])
    return {"valor": valor, "metodo": "el mismo de arriba (F.7)",
            "cuenta": "%s: %d/%d = %d/%d y %d/%d = %d/%d; se toman %d partes en las dos y %s"
                      % (como, fa[0], fa[1], xa, da, fb[0], fb[1], xb, db, xa, dice),
            "vuelta": ";  ".join(vueltas), "vuelta_ok": ok}
