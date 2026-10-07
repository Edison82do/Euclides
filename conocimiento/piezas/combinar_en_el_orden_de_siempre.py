# -*- coding: utf-8 -*-
"""Pieza de COMBINAR LA MULTIPLICACION CON LA SUMA Y LA RESTA EN EL ORDEN DE SIEMPRE (paso M.16; NCETM 2.22,
punto 1; 5.OA.A.1).  'Sin parentesis, la multiplicacion se hace antes que la suma o la resta; con parentesis,
primero lo de dentro.'  3 + 4 x 5: rodeo la multiplicacion, 4 x 5 = 20; luego 3 + 20 = 23 (no 35, que seria ir
de izquierda a derecha sin mirar).  (3 + 4) x 5: primero el parentesis, 3 + 4 = 7; luego 7 x 5 = 35.  La suma y
la resta, DE IZQUIERDA A DERECHA en el orden en que vienen: 10 - 3 + 2 = 7 + 2 = 9 (no 10 - 5).
Cada cuenta pequena la hacen las piezas que ya hay; con decimales, la suma y la resta van con el punto en su
sitio (como las columnas de D.2: se cuenta en las unidades mas pequenas).  Se COMPRUEBA deshaciendo las cuentas
de la ultima a la primera con la operacion contraria: 23 - 3 = 20, 20 : 5 = 4, queda el 4."""

PIEZA = {
    "id": "combinar_en_el_orden_de_siempre",
    "nombre": "primero el parentesis, luego las x, luego + y - de izquierda a derecha",
    "unidad": "M.16",
    "responde": "combinar",
    "rapidez": 20,
    "que_hace": "3 + 4 x 5 = 3 + 20 = 23;  (3 + 4) x 5 = 7 x 5 = 35;  10 - 3 + 2 = 9",
    "condiciones": [
        ("hay_alguna_cuenta", "no hay ninguna cuenta que hacer: es un numero solo"),
        ("cada_producto_con_un_decimal_como_mucho", "hay un decimal por otro decimal: eso es de 6.o"),
    ],
    "usa": ["sumar", "restar", "multiplicar", "multiplicar_decimal", "multiplicar_tres", "dividir",
            "dividir_decimal"],
}


def hacer(s, u):
    cuentas = []
    valor = _expresion(u, s["terminos"], cuentas, "")
    vuelta, ok = _vuelta(u, cuentas)
    return {"valor": valor, "metodo": "el orden de siempre: parentesis, x, y luego + y - de izquierda a derecha "
                                      "(NCETM 2.22, M.16)",
            "pasos": [_paso(c) for c in cuentas], "cuentas": cuentas, "vuelta": vuelta, "vuelta_ok": ok}


def _paso(c):
    if c["op"] == "x3":
        texto = "%s = %s" % (" x ".join(c["factores"]), c["v"])
    else:
        texto = "%s %s %s = %s" % (c["a"], c["op"], c["b"], c["v"])
    return "%s%s  (%s)" % (texto, c["donde"], c["como"])


def _expresion(u, terminos, cuentas, donde):
    """Los terminos con su signo: primero el producto de cada uno, luego + y - de izquierda a derecha."""
    valores = []
    for signo, factores in terminos:
        valores.append((signo, _termino(u, factores, cuentas, donde)))
    actual = valores[0][1]
    for signo, v in valores[1:]:
        if signo == "+":
            nuevo, como = _mas(u, actual, v)
        else:
            nuevo, como = _menos(u, actual, v)
        cuentas.append({"op": signo, "a": actual, "b": v, "v": nuevo, "como": como, "donde": donde})
        actual = nuevo
    return actual


def _termino(u, factores, cuentas, donde):
    fs = []
    for f in factores:
        if isinstance(f, dict):                       # un parentesis: PRIMERO lo de dentro
            fs.append(_expresion(u, f["terminos"], cuentas, "   <- dentro del parentesis"))
        else:
            fs.append(_normal(f))
    if len(fs) == 1:
        return fs[0]
    if len(fs) == 2:
        v, como = _por(u, fs[0], fs[1])
        cuentas.append({"op": "x", "a": fs[0], "b": fs[1], "v": v, "como": como, "donde": donde})
        return v
    try:
        r = u.usar("multiplicar_tres", factores=fs)
    except Exception as e:
        raise ValueError("%s no me sale: %s" % (" x ".join(fs), e))
    v = _normal(r["valor"])
    cuentas.append({"op": "x3", "factores": fs, "v": v, "donde": donde,
                    "como": "tres factores, M.14: %s" % "; ".join(r["resultado"]["pasos"])})
    return v


# ---- LA VUELTA: de la ultima cuenta a la primera, con la contraria

def _vuelta(u, cuentas):
    trozos, ok = [], True
    for c in reversed(cuentas):
        texto, bien = _deshacer_una(u, c)
        trozos.append(texto)
        ok = ok and bien
    return ", ".join(trozos), ok


def _deshacer_una(u, c):
    if c["op"] == "+":
        x, _ = _menos(u, c["v"], c["b"])
        bien = x == c["a"]
        return "%s - %s = %s%s" % (c["v"], c["b"], x, "" if bien else " (y tenia que dar %s)" % c["a"]), bien
    if c["op"] == "-":
        x, _ = _mas(u, c["v"], c["b"])
        bien = x == c["a"]
        return "%s + %s = %s%s" % (c["v"], c["b"], x, "" if bien else " (y tenia que dar %s)" % c["a"]), bien
    fs = c["factores"] if c["op"] == "x3" else [c["a"], c["b"]]
    return _deshacer_producto(u, c["v"], fs)


def _deshacer_producto(u, producto, fs):
    """Dividir el producto entre los factores, uno a uno, hasta que quede uno: tiene que ser el que falta.
    Si no se puede dividir (un factor 0, o pide la division larga), se multiplica en el OTRO ORDEN."""
    actual, quedan, pasos = producto, list(fs), []
    while len(quedan) > 1:
        q, d = None, None
        for f in quedan:
            if "." not in f and f != "0":
                q = _entre(u, actual, f)
                if q is not None:
                    d = f
                    break
        if q is None:
            return _otro_orden(u, producto, fs)
        pasos.append("%s : %s = %s" % (actual, d, q))
        quedan.remove(d)
        actual = q
    bien = _normal(actual) == _normal(quedan[0])
    return "%s%s" % (", ".join(pasos), "" if bien else " (y tenia que quedar %s)" % quedan[0]), bien


def _otro_orden(u, producto, fs):
    otra = list(reversed(fs))
    if len(otra) == 2:
        v, _ = _por(u, otra[0], otra[1])
    else:
        v = _normal(u.usar("multiplicar_tres", factores=otra)["valor"])
    bien = _normal(v) == _normal(producto)
    return "%s = %s (no se puede dividir: multiplico en el otro orden)%s" % (
        " x ".join(otra), v, "" if bien else " y NO da %s" % producto), bien


# ---- las cuentas pequenas (cada pieza lleva su copia: una pieza solo usa lo suyo)

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
