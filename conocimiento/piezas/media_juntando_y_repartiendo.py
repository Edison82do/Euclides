# -*- coding: utf-8 -*-
"""Pieza de LA MEDIA (paso M.20; NCETM 2.26, punto 2): 'la media es la suma de los valores dividida entre cuantos
valores hay'.  Se juntan los valores sumando y el total se reparte por igual entre cuantos son:
    3, 4, 6  ->  3 + 4 = 7; 7 + 6 = 13;  13 : 3 = 4 y sobra 1  (la media es 4 1/3: lo que sobra tambien se reparte)
    0, 4, 8  ->  el 0 CUENTA como valor: 12 : 3 = 4 (no 12 : 2)
LA VUELTA, con las operaciones contrarias: la media por cuantos son, mas lo que sobro, vuelve al total; y al total se
le quitan los valores, uno a uno, hasta que no queda nada."""

PIEZA = {
    "id": "media_juntando_y_repartiendo",
    "nombre": "juntar todos los valores y repartir el total por igual entre cuantos son",
    "unidad": "M.20",
    "responde": "media",
    "rapidez": 9,
    "que_hace": "3, 4, 6 -> 3 + 4 + 6 = 13;  13 : 3 = 4 y sobra 1 -> 4 1/3 (NCETM 2.26)",
    "condiciones": [
        ("son_valores_enteros_y_tantas_partes_como_valores",
         "no son dos valores enteros o mas repartidos entre CUANTOS son: no es una media"),
    ],
    "usa": ["sumar", "dividir", "multiplicar", "restar"],
}


def hacer(s, u):
    vs, k = list(s["valores"]), s["partes"]
    total, pasos = 0, []
    for v in vs:
        if v == 0:
            continue                       # sumar cero deja lo mismo (pero el cero CUENTA al repartir)
        if total == 0:
            total = v
            continue
        nuevo = u.usar("sumar", a=total, b=v)["valor"]
        if u.decir(nuevo) is None:
            raise ValueError("el total se pasa de mi lista")
        pasos.append("%d + %d = %d" % (total, v, nuevo))
        total = nuevo
    if total == 0:
        q, resto = 0, 0
    else:
        r = u.usar("dividir", total=total, divisor=k)
        q, resto = r["valor"], r["resultado"].get("resto", 0)
    pasos.append("%d : %d = %d%s" % (total, k, q, (", y sobra %d (que tambien se reparte: %d/%d para cada uno)"
                                                   % (resto, resto, k)) if resto else ""))
    # LA VUELTA: la media por cuantos son, mas lo que sobro, vuelve al total; y quitando los valores no queda nada
    vl = []
    w = u.usar("multiplicar", a=q, b=k)["valor"] if q else 0
    vl.append("%d x %d = %d" % (q, k, w))
    if resto:
        w2 = u.usar("sumar", a=w, b=resto)["valor"]
        vl.append("%d + %d = %d" % (w, resto, w2))
        w = w2
    ok = w == total
    queda = total
    for v in reversed(vs):
        if v == 0 or not ok:
            continue
        if u.viene_despues(u.decir(v), u.decir(queda)):
            ok = False
            break
        queda = 0 if v == queda else u.usar("restar", a=queda, b=v)["valor"]
    ok = ok and queda == 0
    vl.append("y al total le quito los valores: queda %d" % queda)
    return {"valor": q, "resto": resto, "partes": k,
            "metodo": "juntar los valores y repartir el total entre %d (M.20; NCETM 2.26)" % k,
            "pasos": pasos,
            "cuenta": "; ".join(pasos),
            "vuelta": "%s ... %s" % ("; ".join(vl), "SI" if ok else "NO"), "vuelta_ok": ok,
            "vuelta_explicada": "con las operaciones contrarias: %d x %d%s = %d, el total; y quitandole los valores "
                                "no queda nada" % (q, k, (" + %d" % resto) if resto else "", total)}
