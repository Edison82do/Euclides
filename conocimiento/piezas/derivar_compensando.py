# -*- coding: utf-8 -*-
"""Pieza de DERIVAR (paso P.7; NCETM 1.29, puntos 2, 4 y 5): SACAR UNA CUENTA NUEVA DE UNA QUE SE SABE.
   Si 250 + 250 = 500, entonces 251 + 250 = 501  (un sumando sube 1: la suma sube 1).
   Si 600 - 200 = 400, entonces 601 - 200 = 401  (el minuendo sube 1: la diferencia sube 1)
                       y        600 - 201 = 399  (el sustraendo SUBE 1: la diferencia BAJA 1).
Solo se cuentan los cambios; el resultado que se sabe se mueve.  La vuelta: la cuenta nueva, hecha."""

PIEZA = {
    "id": "derivar_compensando",
    "nombre": "mover el resultado que se sabe",
    "unidad": "P.7",
    "responde": "derivar",
    "rapidez": 5,
    "que_hace": "miro cuanto cambia cada numero y muevo el resultado que ya se: sin volver a calcular",
    "condiciones": [
        ("se_sabe_un_hecho_de_la_misma_cuenta", "no se sabe una cuenta de la misma clase (+ o -)"),
        ("los_cambios_desde_el_hecho_son_faciles", "los cambios no son faciles (en los dedos o decenas/centenas justas)"),
    ],
    "usa": ["restar_por_columnas", "sumar", "restar"],
}


def _cambio(u, p, q):
    if p == q:
        return "igual", 0
    if u.viene_despues(u.decir(q), u.decir(p)):
        return "sube", u.usar("restar_por_columnas", a=q, b=p)["valor"]
    return "baja", u.usar("restar_por_columnas", a=p, b=q)["valor"]


def _facil(u, p, q):
    c = _cambio(u, p, q)
    return u.levantar_dedos(u.decir(c[1])) is not None or u.cifras_de(c[1])[0] == 0


def hacer(s, u):
    h, n = s["hecho"], s["nuevo"]
    formas = [((h["a"], n["a"]), (h["b"], n["b"]))]
    if h["op"] == "+":
        formas.append(((h["a"], n["b"]), (h["b"], n["a"])))
    forma = next((f for f in formas if all(_facil(u, p, q) for p, q in f)), None)
    if forma is None:
        raise ValueError("los cambios no son faciles")
    (p1, q1), (p2, q2) = forma
    c1, c2 = _cambio(u, p1, q1), _cambio(u, p2, q2)
    if h["op"] == "+":
        empuja = [(c1, "un sumando", c1[0]), (c2, "el otro sumando", c2[0])]
        que = "la suma"
    else:
        al_reves = {"sube": "baja", "baja": "sube", "igual": "igual"}
        empuja = [(c1, "el minuendo", c1[0]), (c2, "el sustraendo", al_reves[c2[0]])]
        que = "la diferencia"
    v = h["r"]
    lineas = ["se sabe: %d %s %d = %d" % (h["a"], h["op"], h["b"], h["r"])]
    # primero lo que SUBE y luego lo que BAJA (para no quedarse sin nada que quitar por el camino)
    for sentido in ("sube", "baja"):
        for (c, quien, efecto), (p, q) in zip(empuja, ((p1, q1), (p2, q2))):
            if c[0] == "igual" or efecto != sentido:
                continue
            if efecto == "sube":
                v2 = u.usar("sumar", a=v, b=c[1])["valor"]
            else:
                if u.viene_despues(u.decir(c[1]), u.decir(v)):
                    raise ValueError("%s bajaria de cero: no hay restas negativas (5.4)" % que)
                v2 = u.usar("restar", a=v, b=c[1])["valor"]
            lineas.append("%s %s %d (%d -> %d): %s %s %d -> %d %s %d = %d"
                          % (quien, c[0].upper(), c[1], p, q, que, efecto.upper(), c[1],
                             v, "+" if efecto == "sube" else "-", c[1], v2))
            v = v2
    for (c, quien, efecto), (p, q) in zip(empuja, ((p1, q1), (p2, q2))):
        if c[0] == "igual":
            lineas.append("%s no cambia (%d)" % (quien, p))
    # LA VUELTA: la cuenta nueva, hecha de verdad (sin el hecho que se sabia)
    w = u.usar("sumar" if n["op"] == "+" else "restar", a=n["a"], b=n["b"])
    return {"valor": v, "metodo": "mover el resultado (P.7)",
            "cuenta": "\n".join(lineas),
            "vuelta": "%d %s %d = %d (%s)" % (n["a"], n["op"], n["b"], w["valor"], w["resultado"]["metodo"]),
            "vuelta_ok": w["valor"] == v}
