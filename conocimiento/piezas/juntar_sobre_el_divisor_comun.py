# -*- coding: utf-8 -*-
"""Pieza de JUNTAR SOBRE EL DIVISOR COMUN (paso M.22; NCETM 2.28, punto 2: 'al sumar o restar expresiones de dividir
que tienen un DIVISOR COMUN, se puede aplicar la propiedad distributiva').
    12 : 3 + 6 : 3   ->  los dos se reparten entre 3: es lo mismo que juntar primero y repartir UNA vez:
                         12 + 6 = 18;  18 : 3 = 6
    7 : 4 + 9 : 4    ->  ninguna sale justa, pero juntas: 7 + 9 = 16;  16 : 4 = 4
    50 : 5 - 15 : 5  ->  50 - 15 = 35;  35 : 5 = 7
Una division en vez de varias (como el factor comun de M.16).  OJO, el error tipico: NO es 18 : 6 (los divisores no
se juntan: se reparte entre 3 las dos veces).
LA VUELTA, con las contrarias: lo que toca por el divisor (mas lo que sobro) vuelve a lo juntado; y a lo juntado se le
deshacen las sumas y restas, de la ultima a la primera, hasta volver al primero de arriba."""

PIEZA = {
    "id": "juntar_sobre_el_divisor_comun",
    "nombre": "juntar lo de arriba y repartir UNA vez (la distributiva: a : d + b : d = (a + b) : d)",
    "unidad": "M.22",
    "responde": "divisor_comun",
    "rapidez": 5,
    "que_hace": "12 : 3 + 6 : 3 = (12 + 6) : 3 = 18 : 3 = 6;  7 : 4 + 9 : 4 = 16 : 4 = 4 (NCETM 2.28)",
    "condiciones": [
        ("son_divisiones_con_el_mismo_divisor",
         "no son dos divisiones de enteros o mas, sumadas o restadas, con el MISMO divisor (que no sea 0)"),
    ],
    "usa": ["sumar", "restar", "dividir", "multiplicar"],
}


def hacer(s, u):
    ts, d = s["terminos"], s["divisor"]
    total, pasos, hechas = ts[0][1], [], []
    for signo, v in ts[1:]:
        if signo == "+":
            nuevo = total if v == 0 else (v if total == 0 else u.usar("sumar", a=total, b=v)["valor"])
            if u.decir(nuevo) is None:
                raise ValueError("lo de arriba junto se pasa de mi lista")
        else:
            if u.viene_despues(u.decir(v), u.decir(total)):
                raise ValueError("lo de arriba junto se baja de cero (%d - %d)" % (total, v))
            nuevo = 0 if v == total else (total if v == 0 else u.usar("restar", a=total, b=v)["valor"])
        pasos.append("%d %s %d = %d" % (total, signo, v, nuevo))
        hechas.append((signo, v, total))
        total = nuevo
    if total == 0:
        q, resto = 0, 0
    else:
        r = u.usar("dividir", total=total, divisor=d)
        q, resto = r["valor"], r["resultado"].get("resto", 0)
    pasos.append("%d : %d = %d%s" % (total, d, q, (", y sobra %d" % resto) if resto else ""))
    # LA VUELTA: lo que toca por el divisor (+ lo que sobro) vuelve a lo juntado; deshacer las sumas y restas
    vl = []
    w = u.usar("multiplicar", a=q, b=d)["valor"] if q else 0
    vl.append("%d x %d = %d" % (q, d, w))
    if resto:
        w2 = u.usar("sumar", a=w, b=resto)["valor"]
        vl.append("%d + %d = %d" % (w, resto, w2))
        w = w2
    ok = w == total
    for signo, v, antes in reversed(hechas):
        if not ok:
            break
        if signo == "+":
            if u.viene_despues(u.decir(v), u.decir(w)):
                ok = False
                break
            w2 = 0 if v == w else (w if v == 0 else u.usar("restar", a=w, b=v)["valor"])
            vl.append("%d - %d = %d" % (w, v, w2))
        else:
            w2 = w if v == 0 else (v if w == 0 else u.usar("sumar", a=w, b=v)["valor"])
            vl.append("%d + %d = %d" % (w, v, w2))
        ok = w2 == antes
        w = w2
    ok = ok and w == ts[0][1]
    return {"valor": q, "resto": resto, "divisor": d,
            "metodo": "juntar lo de arriba y repartir una vez entre %d: la distributiva (M.22; NCETM 2.28)" % d,
            "pasos": pasos, "cuenta": "; ".join(pasos),
            "vuelta": "%s ... %s" % ("; ".join(vl), "SI" if ok else "NO"), "vuelta_ok": ok,
            "vuelta_explicada": "con las operaciones contrarias: %d x %d%s = %d, lo juntado; y deshaciendo las sumas y "
                                "restas vuelvo al %d del principio" % (q, d, (" + %d" % resto) if resto else "", total,
                                                                       ts[0][1])}
