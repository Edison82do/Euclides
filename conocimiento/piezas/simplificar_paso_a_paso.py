# -*- coding: utf-8 -*-
"""Pieza de SIMPLIFICAR UNA FRACCION (paso F.6; NCETM 3.7, punto 3): PASO A PASO, con los factores comunes que se
VEN, como en el cuaderno: los dos acaban en 0 -> entre 10 (un cero menos a cada uno); los dos pares -> entre 2; los
dos acaban en 0 o en 5 -> entre 5; si no, se prueba el 3 y el 7 dividiendo (con las tablas).  12/18 -> 6/9 (: 2) ->
2/3 (: 3).  Y se sigue hasta que ya no compartan nada (12/18 no se queda en 6/9).
CUANDO YA NO SE VE NINGUNO, se comprueba que es la forma mas simple: cada numero se parte en doses, treses, cincos y
sietes (dividiendo) y se mira el TROZO GRANDE que le queda.  Si a uno no le queda nada (1 000 000 son solo doses y
cincos), no pueden compartir nada mas.  Si a los dos les queda el mismo trozo (26/39: 13 y 13), ese trozo es otro
factor comun.  Si no, los factores del trozo mas pequeno (M.15) se prueban en el otro.
LA VUELTA: multiplicar de vuelta arriba y abajo por cada numero que se dividio, al reves: sale la de partida."""

PIEZA = {
    "id": "simplificar_paso_a_paso",
    "nombre": "paso a paso, con los factores que se ven",
    "unidad": "F.6",
    "responde": "simplificar_fraccion",
    "rapidez": 6,
    "que_hace": "12/18 -> 6/9 (entre 2) -> 2/3 (entre 3), y mira que ya no compartan nada mas",
    "condiciones": [
        ("ninguno_es_cero", "arriba o abajo hay un cero"),
    ],
    "usa": ["dividir", "multiplicar", "parejas_de_factores"],
}

_PARES = (0, 2, 4, 6, 8)


def _entre(u, n, d):
    """n : d si sale JUSTO; None si sobra algo.  ValueError si no se hacer esa division."""
    try:
        r = u.usar("dividir", total=n, divisor=d)
    except Exception as e:
        raise ValueError("para mirar si %d se reparte justo entre %d no me sale la division (%s)" % (n, d, e))
    if r["resultado"].get("resto", 0):
        return None
    return r["valor"]


def _uno_que_se_ve(u, a, b):
    """El primer factor comun que se VE: (d, por que) o None."""
    ua, ub = u.cifras_de(a)[0], u.cifras_de(b)[0]
    if ua == 0 and ub == 0:
        return 10, "los dos acaban en 0"
    if ua in _PARES and ub in _PARES:
        return 2, "los dos son pares"
    if ua in (0, 5) and ub in (0, 5):
        return 5, "los dos acaban en 0 o en 5"
    for d in (3, 7):
        if _entre(u, a, d) is not None and _entre(u, b, d) is not None:
            return d, "los dos se reparten justo entre %d" % d
    return None


def _trozo_grande(u, n):
    """n partido en doses, treses, cincos y sietes mientras se pueda: (lo que queda, en cuantos se partio)."""
    partes = []
    for d in (2, 3, 5, 7):
        while n != 1:
            q = _entre(u, n, d)
            if q is None:
                break
            partes.append("%d" % d)
            n = q
    return n, partes


def _uno_grande(u, a, b, notas):
    """Ya no comparten 2, 3, 5 ni 7.  Comparten algun factor mas grande?  (d, por que) o None (es la mas simple)."""
    ta, pa = _trozo_grande(u, a)
    tb, pb = _trozo_grande(u, b)
    for n, t, p in ((a, ta, pa), (b, tb, pb)):
        if p[1:] or (p and t != 1):
            notas.append("%d = %s%s" % (n, " x ".join(p), " x %d" % t if t != 1 else ""))
        elif not p:
            notas.append("%d no se parte en doses, treses, cincos ni sietes" % n)
    if ta == 1 or tb == 1:
        n = a if ta == 1 else b
        notas.append("a %d no le queda ningun trozo grande (todo son doses, treses, cincos o sietes), y esos ya no "
                     "los comparten: solo comparten el 1" % n)
        return None
    if ta == tb:
        return ta, "a los dos les queda el mismo trozo grande, %d" % ta
    chico, otro = (tb, ta) if u.viene_despues(u.decir(ta), u.decir(tb)) else (ta, tb)
    try:
        fs = u.usar("parejas_de_factores", n=chico)["resultado"]["factores"]
    except Exception:
        raise ValueError("todavia no: para saber si %d y %d comparten algun factor grande haria falta la division "
                         "larga (6.o)" % (ta, tb))
    for f in fs:
        if f != 1 and _entre(u, otro, f) is not None:
            return f, "los trozos grandes (%d y %d) comparten el %d" % (ta, tb, f)
    notas.append("los trozos grandes (%d y %d) solo comparten el 1" % (ta, tb))
    return None


def hacer(s, u):
    a, b = s["a"], s["b"]
    pasos, lineas, notas = [], [], []
    while a != 1 and b != 1:
        f = _uno_que_se_ve(u, a, b)
        if f is None:
            notas = []                       # lo que se dice es lo de la ULTIMA mirada
            f = _uno_grande(u, a, b, notas)
        if f is None:
            break
        d, porque = f
        na, nb = _entre(u, a, d), _entre(u, b, d)
        lineas.append("%d/%d -> %d/%d   (entre %d: %s)" % (a, b, na, nb, d, porque))
        pasos.append((d, porque))
        a, b = na, nb
    if a == 1:
        por_que = "arriba queda un 1: el unico factor del 1 es el 1"
    elif b == 1:
        por_que = "abajo queda un 1: es un numero entero"
    else:
        por_que = "; ".join(notas)
    # LA VUELTA: multiplicar de vuelta, al reves
    va, vb, vuelta = a, b, ["%d/%d" % (a, b)]
    for d, _ in reversed(pasos):
        va = u.usar("multiplicar", a=va, b=d)["valor"]
        vb = u.usar("multiplicar", a=vb, b=d)["valor"]
        vuelta.append("%d/%d (x %d)" % (va, vb, d))
    return {"valor": "%d" % a if b == 1 else "%d/%d" % (a, b), "arriba": a, "abajo": b, "pasos": pasos,
            "metodo": "paso a paso, con los factores que se ven (F.6)",
            "cuenta": "\n".join(lineas) if lineas else "no se ve ningun factor comun",
            "por_que_ya": por_que,
            "vuelta": " -> ".join(vuelta), "vuelta_ok": (va, vb) == (s["a"], s["b"])}
