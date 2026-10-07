# -*- coding: utf-8 -*-
"""Pieza de SACAR EL FACTOR COMUN (paso M.16; NCETM 2.22, punto 2: 'al sumar o restar expresiones de
multiplicar que tienen un factor comun, se puede aplicar la propiedad distributiva').
4 x 6 + 4 x 2: los dos llevan un 4: son 6 cuatros y 2 cuatros, 8 cuatros: 4 x (6 + 2) = 4 x 8 = 32.  UNA
multiplicacion en vez de dos (17 x 6 + 3 x 6 = 20 x 6 = 120).  Tambien con la resta: 7 x 5 - 7 x 3 = 7 x 2 = 14.
Un numero suelto es ese numero UNA vez: 5 x 4 + 5 = 5 x (4 + 1) = 5 x 5.  OJO, el error tipico: NO es
(4 + 4) x (6 + 2); se juntan los OTROS factores, no los comunes.
Se COMPRUEBA con las contrarias: 32 : 4 = 8 (cuantos cuatros hay), 8 - 2 = 6 (y tenian que ser 6)."""

PIEZA = {
    "id": "combinar_sacando_el_factor_comun",
    "nombre": "sacar el factor comun (la distributiva): a x b + a x c = a x (b + c)",
    "unidad": "M.16",
    "responde": "combinar",
    "rapidez": 5,
    "que_hace": "4 x 6 + 4 x 2 = 4 x (6 + 2) = 4 x 8 = 32;  7 x 5 - 7 x 3 = 7 x 2 = 14",
    "condiciones": [
        ("hay_alguna_cuenta", "no hay ninguna cuenta que hacer: es un numero solo"),
        ("cada_producto_con_un_decimal_como_mucho", "hay un decimal por otro decimal: eso es de 6.o"),
        ("hay_un_factor_comun", "no son dos productos (o un producto y un numero suelto) con un factor entero "
                                "en comun"),
    ],
    "usa": ["sumar", "restar", "multiplicar", "multiplicar_decimal", "dividir", "dividir_decimal"],
}


def _factor_comun(terminos):
    """[['+', ['4', '6']], ['+', ['4', '2']]] -> ('4', '6', '+', '2'): el comun, lo que queda de cada uno, el
    signo.  Comparar es LEER si dos numeros se escriben igual.  None si no hay."""
    if len(terminos) != 2:
        return None
    (_, f1), (signo, f2) = terminos
    if any(isinstance(f, dict) for x in (f1, f2) for f in x) or len(f1) > 2 or len(f2) > 2 or (len(f1) == 1 and len(f2) == 1):
        return None
    f1, f2 = [_normal(f) for f in f1], [_normal(f) for f in f2]
    for a in f1:
        if "." in a or a == "0" or a not in f2:
            continue
        r1, r2 = list(f1), list(f2)
        r1.remove(a)
        r2.remove(a)
        return a, (r1[0] if r1 else "1"), signo, (r2[0] if r2 else "1")
    return None


def hacer(s, u):
    t = s["terminos"]
    a, b, signo, c = _factor_comun(t)
    pasos = []
    sueltos = [x for x in (t[0][1], t[1][1]) if len(x) == 1]
    if sueltos:
        pasos.append("%s suelto es %s UNA vez: %s x 1" % (a, a, a))
    pasos.append("los dos llevan el %s: son %s veces %s %s %s veces %s, o sea %s x (%s %s %s)"
                 % (a, b, a, "y" if signo == "+" else "menos", c, a, a, b, signo, c))
    if signo == "+":
        dentro, como = _mas(u, b, c)
    else:
        dentro, como = _menos(u, b, c)
    pasos.append("%s %s %s = %s  (%s)" % (b, signo, c, dentro, como))
    valor, como = _por(u, a, dentro)
    pasos.append("%s x %s = %s  (%s)" % (a, dentro, valor, como))
    # LA VUELTA: cuantos 'a' hay (dividir), y deshacer la suma o la resta
    cuantos = _entre(u, valor, a)
    if cuantos is None:
        raise ValueError("no lo puedo comprobar dividiendo %s entre %s" % (valor, a))
    if signo == "+":
        otra, _ = _menos(u, cuantos, c)
        vuelta = "%s : %s = %s, %s - %s = %s" % (valor, a, cuantos, cuantos, c, otra)
    else:
        otra, _ = _mas(u, cuantos, c)
        vuelta = "%s : %s = %s, %s + %s = %s" % (valor, a, cuantos, cuantos, c, otra)
    ok = cuantos == dentro and otra == b
    vuelta = "%s%s" % (vuelta, ", que es el %s del principio" % b if ok else " (y tenia que ser %s)" % b)
    return {"valor": valor, "metodo": "sacar el factor comun: la distributiva (NCETM 2.22, punto 2; M.16)",
            "pasos": pasos, "comun": a, "dentro": [b, signo, c, dentro],
            "vuelta": vuelta, "vuelta_ok": ok}


# ---- las cuentas pequenas (cada pieza lleva su copia: una pieza solo usa lo suyo; la misma que en
#      combinar_en_el_orden_de_siempre)

def _n(u, f):
    """'175' -> 175: LEER las cifras de un entero escrito."""
    return u.escribir_cifras([int(c) for c in reversed(f)])


def _normal(f):
    """'1.50' -> '1.5';  '007' -> '7'.  Es mirar las cifras, no calcular."""
    if "." in f:
        f = f.rstrip("0").rstrip(".")
    e, punto, d = f.partition(".")
    e = e.lstrip("0") or "0"
    return "%s.%s" % (e, d) if punto else e


def _alinear(f, g):
    """'3.25' y '1.5' -> ('325', '150', 2): el punto en su sitio, contado en las unidades mas pequenas
    (centesimas).  Es escribir ceros a la derecha, no calcular."""
    e1, _, d1 = f.partition(".")
    e2, _, d2 = g.partition(".")
    k = max(len(d1), len(d2))
    return ("%s%s" % (e1, d1.ljust(k, "0"))).lstrip("0") or "0", \
        ("%s%s" % (e2, d2.ljust(k, "0"))).lstrip("0") or "0", k


def _con_punto(n, k):
    """1308 contadas en centesimas -> '13.08'.  Poner el punto k cifras desde la derecha."""
    t = "%d" % n
    if not k:
        return t
    t = t.rjust(k + 1, "0")
    return _normal("%s.%s" % (t[:-k], t[-k:]))


def _mas(u, f, g):
    a, b, k = _alinear(f, g)
    try:
        r = u.usar("sumar", a=_n(u, a), b=_n(u, b))
    except Exception:
        raise ValueError("se pasa del millon: %s + %s no tiene nombre en mi lista" % (f, g))
    return _con_punto(r["valor"], k), r["resultado"]["metodo"]


def _menos(u, f, g):
    a, b, k = _alinear(f, g)
    na, nb = _n(u, a), _n(u, b)
    pa, pb = u.decir(na), u.decir(nb)
    if pa is None or pb is None:
        raise ValueError("se pasa del millon: %s o %s no tiene nombre en mi lista" % (f, g))
    if u.viene_despues(pb, pa):
        raise ValueError("por debajo del cero: a %s no le puedo quitar %s (por el camino me bajo de cero; los "
                         "negativos, N.5, solo los se en la recta)" % (f, g))
    r = u.usar("restar", a=na, b=nb)
    return _con_punto(r["valor"], k), r["resultado"]["metodo"]


def _por(u, f, g):
    """f x g, los dos en texto.  Un entero por otro: la pregunta 'multiplicar'; un decimal por un entero:
    'multiplicar_decimal' (M.13).  Devuelve (el producto en texto, el metodo)."""
    if "." in f and "." in g:
        raise ValueError("%s x %s es un decimal por otro decimal: eso es de 6.o" % (f, g))
    try:
        if "." in f or "." in g:
            r = u.usar("multiplicar_decimal", x=f, y=g)
            return _normal(r["valor"]), r["resultado"]["metodo"]
        r = u.usar("multiplicar", a=_n(u, f), b=_n(u, g))
    except Exception as e:
        raise ValueError("%s x %s no me sale: %s" % (f, g, e))
    if u.decir(r["valor"]) is None:
        raise ValueError("se pasa del millon: %s x %s no tiene nombre en mi lista" % (f, g))
    return "%d" % r["valor"], r["resultado"]["metodo"]


def _entre(u, x, d):
    """x : d, con d un entero que no es cero.  El cociente en texto, o None si no sale justo o no se."""
    try:
        if "." not in x:
            r = u.usar("dividir", total=_n(u, x), divisor=_n(u, d))
            if not r["resultado"].get("resto"):
                return "%d" % r["valor"]
            if len(d) != 1:
                return None
        return _normal(u.usar("dividir_decimal", x=x, d=d)["valor"])
    except Exception:
        return None
