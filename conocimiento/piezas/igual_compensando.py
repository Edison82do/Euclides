# -*- coding: utf-8 -*-
"""Pieza de la IGUALDAD (paso P.7; NCETM 1.29): VER LA COMPENSACION SIN CALCULAR LOS LADOS.
   250 + 250 = 260 + 240 es VERDAD: un sumando sube 10 y el otro baja 10 (punto 1: la misma suma).
   75 - 28 = 77 - 30 es VERDAD: el minuendo y el sustraendo suben 2 los dos (punto 3: la misma diferencia).
   75 - 28 = 73 - 30 es FALSO: el minuendo baja 2 y el sustraendo sube 2: la diferencia baja 4 (puntos 4 y 5).
Solo mira los CAMBIOS (si son faciles: caben en los dedos o son decenas/centenas justas), no los lados.
Comprueba despues calculando los dos lados (la vuelta)."""

PIEZA = {
    "id": "igual_compensando",
    "nombre": "la compensacion (+: uno sube, otro baja; -: los dos igual)",
    "unidad": "P.7",
    "responde": "igualdad",
    "rapidez": 3,
    "que_hace": "mira cuanto cambia cada numero de un lado al otro y que le pasa a la suma o a la diferencia",
    "condiciones": [
        ("dos_sumas_o_dos_restas_con_cambios_faciles",
         "no son dos sumas o dos restas con cambios faciles de un lado al otro"),
    ],
    "usa": ["restar_por_columnas", "sumar", "restar"],
}


def _cambio(u, p, q):
    """De p a q: ('sube', d), ('baja', d) o ('igual', 0)."""
    if p == q:
        return "igual", 0
    if u.viene_despues(u.decir(q), u.decir(p)):
        return "sube", u.usar("restar_por_columnas", a=q, b=p)["valor"]
    return "baja", u.usar("restar_por_columnas", a=p, b=q)["valor"]


def _parejas(u, i, d):
    formas = [((i["a"], d["a"]), (i["b"], d["b"]))]
    if i["op"] == "+":
        formas.append(((i["a"], d["b"]), (i["b"], d["a"])))
    for f in formas:
        ok = True
        for p, q in f:
            g, m = (p, q) if u.viene_despues(u.decir(p), u.decir(q)) else (q, p)
            k = u.usar("restar_por_columnas", a=g, b=m)["valor"]
            if u.levantar_dedos(u.decir(k)) is None and u.cifras_de(k)[0] != 0:
                ok = False
        if ok:
            return f
    raise ValueError("los cambios no son faciles")


def _neto(u, c1, c2):
    """El cambio del resultado cuando uno cambia c1 y lo otro c2 (los dos 'empujan' el resultado).
    Devuelve ('sube'|'baja'|'igual', cuanto)."""
    (s1, d1), (s2, d2) = c1, c2
    if s1 == "igual":
        return c2
    if s2 == "igual":
        return c1
    if s1 == s2:
        return s1, u.usar("sumar", a=d1, b=d2)["valor"]
    if d1 == d2:
        return "igual", 0
    if u.viene_despues(u.decir(d1), u.decir(d2)):
        return s1, u.usar("restar", a=d1, b=d2)["valor"]
    return s2, u.usar("restar", a=d2, b=d1)["valor"]


_AL_REVES = {"sube": "baja", "baja": "sube", "igual": "igual"}


def hacer(s, u):
    i, d = s["lados"]
    (p1, q1), (p2, q2) = _parejas(u, i, d)
    c1, c2 = _cambio(u, p1, q1), _cambio(u, p2, q2)
    if i["op"] == "+":
        efecto2 = c2
        que, quien1, quien2 = "la suma", "un sumando", "el otro"
        regla = "en la suma, lo que sube un sumando sube la suma; lo que baja, la baja"
    else:
        efecto2 = (_AL_REVES[c2[0]], c2[1])           # el sustraendo empuja AL REVES
        que, quien1, quien2 = "la diferencia", "el minuendo", "el sustraendo"
        regla = "en la resta, el minuendo empuja la diferencia hacia su lado; el sustraendo, AL REVES"
    neto = _neto(u, c1, efecto2)

    def dice(c, p, q):
        return "%d -> %d %s %d" % (p, q, c[0], c[1]) if c[0] != "igual" else "%d se queda igual" % p
    explicacion = "%s: %s;  %s: %s.  (%s)" % (quien1, dice(c1, p1, q1), quien2, dice(c2, p2, q2), regla)
    if neto[0] == "igual":
        valor = "verdadero"
        final = "%s NO cambia (NCETM 1.29).  No hace falta calcular" % que
    else:
        valor = "falso"
        final = "%s %s %d: los lados no valen lo mismo (NCETM 1.29).  No hace falta calcular" % (que, neto[0], neto[1])
    # LA VUELTA: ahora si, se calculan los dos lados; tienen que estar de acuerdo con lo que se vio
    op = "sumar" if i["op"] == "+" else "restar"
    vi = u.usar(op, a=i["a"], b=i["b"])["valor"]
    vd = u.usar(op, a=d["a"], b=d["b"])["valor"]
    return {"valor": valor, "metodo": "la compensacion (P.7)",
            "cuenta": "%s\n-> %s" % (explicacion, final),
            "vuelta": "%s = %d;  %s = %d" % (i["texto"], vi, d["texto"], vd),
            "vuelta_ok": (vi == vd) == (valor == "verdadero")}
