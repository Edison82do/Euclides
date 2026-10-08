# -*- coding: utf-8 -*-
"""Pieza de UNA SUMA SOLA: TODAS LAS PAREJAS (paso S.3; NCETM 1.31, puntos 1 y 5).  a + b = 10 no tiene UNA
respuesta: con enteros, a puede ser 0, 1, 2 ... hasta 10 y b lo que falta: de 0 + 10 a 10 + 0 hay UNA MAS QUE LA
SUMA (11 parejas; si no vale el 0, dos menos: 9).  Se cuentan sin probarlas (recitando: despues del diez, el
once).  Con decimales, infinitas (5.5 + 4.5, 5.25 + 4.75 ...).  Solo a + b = 0 tiene una (0 y 0).
Se COMPRUEBA poniendo en la suma las parejas que se ensenan."""

PIEZA = {
    "id": "una_suma_sola_todas_las_parejas",
    "nombre": "una suma sola: una pareja mas que la suma (con enteros); infinitas con decimales",
    "unidad": "S.3",
    "responde": "dos_incognitas",
    "rapidez": 5,
    "que_hace": "a + b = 10:  0 + 10, 1 + 9 ... 10 + 0 = 11 parejas (9 sin el 0); con decimales, infinitas",
    "condiciones": [
        ("es_una_suma_sola", "no es una suma sola"),
    ],
    "usa": ["combinar", "dividir", "dividir_decimal", "cumplen_las_ecuaciones"],
}


def hacer(s, u):
    eq = s["ecuaciones"][0]
    a, b = s["letras"]
    n = _normal(eq["n"])
    if n == "0":
        valores = {a: "0", b: "0"}
        vuelta, ok = _comprobar(u, s, valores)
        return {"valor": _escribir(s["letras"], valores), "soluciones": [valores], "cuantas": "una",
                "metodo": "una suma de cero: las dos son cero (con numeros que se cuentan)",
                "pasos": ["si juntas son cero, las dos son cero"], "vuelta": vuelta, "vuelta_ok": ok}
    try:
        mitad = _repartir(u, n)
    except ValueError:                              # la mitad, contada en decimas, se pasaria de mi lista
        mitad = None
    ejemplos = [{a: "0", b: n}, {a: n, b: "0"}]
    if mitad is not None:
        ejemplos.insert(1, {a: mitad, b: mitad})
    if "." in n:
        pasos = ["%s no es entero: con ENTEROS no hay NINGUNA pareja" % n,
                 "con DECIMALES, infinitas: %s ..." % "; ".join("%s + %s" % (e[a], e[b]) for e in ejemplos)]
        valor, cuantas = "infinitas con decimales (con enteros, ninguna)", "infinitas"
    else:
        n_p = u.decir(_n(u, n))
        cuantas_p = u.siguiente(n_p)                       # de 0 a n: una mas que n
        lista = _algunas(u, a, b, n, n_p)
        pasos = ["%s va de 0 a %s y %s es lo que falta: %s" % (a, n, b, lista)]
        if cuantas_p is None:                              # una mas que el techo: ya no tiene nombre en mi lista
            pasos.append("de 0 a %s hay UNA MAS que %s, y ese numero ya se pasa de mi lista" % (n, n))
            valor = "una pareja mas que %s con enteros; infinitas con decimales" % n
        else:
            sin_cero = u.anterior(u.anterior(cuantas_p))   # sin 0 + n ni n + 0
            pasos.append("de 0 a %s hay UNA MAS que %s: %s parejas de enteros (%s si no vale el 0)" % (
                n, n, cuantas_p.upper(), sin_cero))
            valor = "%d parejas con enteros (%d sin el 0); infinitas con decimales" % (
                u.leer(cuantas_p), u.leer(sin_cero))
        pasos.append("con DECIMALES, infinitas: %s%s" % ("%s + %s, " % (mitad, mitad) if mitad else "",
                                                           _otra_decimal(u, a, b, n)))
        cuantas = "varias"
    vuelta, ok = _comprobar_varias(u, s, ejemplos)
    return {"valor": valor, "soluciones": [], "ejemplos": ejemplos, "cuantas": cuantas,
            "metodo": "una suma sola: no hay UNA respuesta (NCETM 1.31, punto 1)", "pasos": pasos,
            "vuelta": vuelta, "vuelta_ok": ok}


def _algunas(u, a, b, n, n_p):
    """Las parejas en orden: todas si la suma es diez o menos; si no, las tres primeras y la ultima."""
    todas = not u.viene_despues(n_p, "diez")
    trozos, w = [], "cero"
    while True:
        va = "%d" % u.leer(w)
        trozos.append("%s + %s" % (va, _cuenta(u, [["+", [n]], ["-", [va]]])))
        if w == n_p:
            return ", ".join(trozos)
        if not todas and w == "dos":
            return "%s ... %s + 0" % (", ".join(trozos), n)
        w = u.siguiente(w)


def _otra_decimal(u, a, b, n):
    try:
        return "0.5 + %s ..." % _cuenta(u, [["+", [n]], ["-", ["0.5"]]])
    except ValueError:                              # en decimas, el numero se pasaria de mi lista
        return "..."


def _comprobar_varias(u, s, ejemplos):
    trozos, ok = [], True
    for v in ejemplos:
        t, bien = _comprobar(u, s, v)
        trozos.append(t)
        ok = ok and bien
    return "; ".join(trozos), ok


def _comprobar(u, s, valores):
    r = u.usar("cumplen_las_ecuaciones", ecuaciones=s["ecuaciones"], valores=valores)
    return "; ".join(r["resultado"]["lineas"]), r["valor"] == "si" and r["resultado"]["vuelta_ok"]


def _cuenta(u, terminos):
    try:
        return _normal(u.usar("combinar", terminos=terminos)["valor"])
    except Exception as e:                          # 'combinar' no sale (por debajo del cero, o se pasa del techo)
        raise ValueError(str(e))


def _repartir(u, x, entre="2"):
    """x : entre.  Con enteros, primero la division de siempre (las tablas, tambien la del 11 y la del 12); si
    sobra algo, en decimas, centesimas o milesimas (M.13)."""
    if "." not in x:
        try:
            r = u.usar("dividir", total=_n(u, x), divisor=_n(u, entre))
            if not r["resultado"].get("resto"):
                return "%d" % r["valor"]
        except Exception:
            pass
    try:
        return _normal(u.usar("dividir_decimal", x=x, d=entre)["valor"])
    except Exception as e:
        raise ValueError("%s : %s no me sale: %s" % (x, entre, e))


def _escribir(letras, valores):
    return ", ".join("%s = %s" % (l, valores[l]) for l in letras)


def _alinear(f, g):
    e1, _, d1 = f.partition(".")
    e2, _, d2 = g.partition(".")
    k = max(len(d1), len(d2))
    return ("%s%s" % (e1, d1.ljust(k, "0"))).lstrip("0") or "0", ("%s%s" % (e2, d2.ljust(k, "0"))).lstrip("0") or "0"


def _n(u, f):
    """'175' -> 175: LEER las cifras de un entero escrito."""
    return u.escribir_cifras([int(c) for c in reversed(f)])


def _normal(f):
    if "." in f:
        f = f.rstrip("0").rstrip(".")
    e, punto, d = f.partition(".")
    e = e.lstrip("0") or "0"
    return "%s.%s" % (e, d) if punto else e
