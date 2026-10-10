# -*- coding: utf-8 -*-
"""Pieza de DIVIDIR CADA UNA Y JUNTAR (paso M.22; NCETM 2.28, punto 1: 'sin parentesis, la division se hace ANTES que
la suma o la resta').  El orden de siempre con divisiones que tienen el mismo divisor:
    12 : 3 + 6 : 3   ->  12 : 3 = 4;  6 : 3 = 2;  4 + 2 = 6
Solo si TODAS salen justas (con lo que sobra no se pueden juntar numeros para contar: ahi se junta antes, o se sigue con
fracciones).  Cuesta mas que juntar (varias divisiones en vez de una): es el segundo camino.
LA VUELTA, con las contrarias: cada cociente por el divisor vuelve a su numero de arriba; y deshaciendo las sumas y
restas de los cocientes se vuelve al primero."""

PIEZA = {
    "id": "dividir_cada_una_y_juntar",
    "nombre": "dividir cada una y luego juntar (el orden de siempre: la : antes que la + y la -)",
    "unidad": "M.22",
    "responde": "divisor_comun",
    "rapidez": 20,
    "que_hace": "12 : 3 + 6 : 3 = 4 + 2 = 6 (NCETM 2.28)",
    "condiciones": [
        ("son_divisiones_con_el_mismo_divisor",
         "no son dos divisiones de enteros o mas, sumadas o restadas, con el MISMO divisor (que no sea 0)"),
    ],
    "usa": ["sumar", "restar", "dividir", "multiplicar"],
}


def hacer(s, u):
    ts, d = s["terminos"], s["divisor"]
    pasos, cocientes = [], []
    for signo, v in ts:
        if v == 0:
            q = 0
        else:
            r = u.usar("dividir", total=v, divisor=d)
            if r["resultado"].get("resto"):
                raise ValueError("%d : %d no sale justo: no se pueden juntar los cocientes" % (v, d))
            q = r["valor"]
        pasos.append("%d : %d = %d" % (v, d, q))
        cocientes.append((signo, q, v))
    total, hechas = cocientes[0][1], []
    for signo, q, _ in cocientes[1:]:
        if signo == "+":
            nuevo = total if q == 0 else (q if total == 0 else u.usar("sumar", a=total, b=q)["valor"])
        else:
            if u.viene_despues(u.decir(q), u.decir(total)):
                raise ValueError("se baja de cero (%d - %d)" % (total, q))
            nuevo = 0 if q == total else (total if q == 0 else u.usar("restar", a=total, b=q)["valor"])
        pasos.append("%d %s %d = %d" % (total, signo, q, nuevo))
        hechas.append((signo, q, total))
        total = nuevo
    # LA VUELTA: cada cociente por el divisor vuelve a su numero; deshacer las sumas y restas de los cocientes
    vl, ok = [], True
    for _, q, v in cocientes:
        w = u.usar("multiplicar", a=q, b=d)["valor"] if q else 0
        vl.append("%d x %d = %d" % (q, d, w))
        ok = ok and w == v
    w = total
    for signo, q, antes in reversed(hechas):
        if not ok:
            break
        if signo == "+":
            if u.viene_despues(u.decir(q), u.decir(w)):
                ok = False
                break
            w2 = 0 if q == w else (w if q == 0 else u.usar("restar", a=w, b=q)["valor"])
            vl.append("%d - %d = %d" % (w, q, w2))
        else:
            w2 = w if q == 0 else (q if w == 0 else u.usar("sumar", a=w, b=q)["valor"])
            vl.append("%d + %d = %d" % (w, q, w2))
        ok = w2 == antes
        w = w2
    ok = ok and w == cocientes[0][1]
    return {"valor": total, "resto": 0, "divisor": d,
            "metodo": "dividir cada una entre %d y juntar los cocientes: el orden de siempre (M.22; NCETM 2.28)" % d,
            "pasos": pasos, "cuenta": "; ".join(pasos),
            "vuelta": "%s ... %s" % ("; ".join(vl), "SI" if ok else "NO"), "vuelta_ok": ok,
            "vuelta_explicada": "con las operaciones contrarias: cada cociente por %d vuelve a su numero de arriba; y "
                                "deshaciendo las sumas y restas vuelvo al primer cociente" % d}
