# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR TRES FACTORES (o mas) EN EL ORDEN DE SIEMPRE (paso M.14; NCETM 2.20).
2 x 3 x 4: primero 2 x 3 = 6, luego 6 x 4 = 24.  Cada cuenta de dos la hacen las piezas de multiplicar
(o de multiplicar un decimal por un entero, M.13).  Es el camino que sirve siempre, pero no siempre el
mas facil (para eso esta tres_factores_buscando_la_pareja_facil).  Se COMPRUEBA dividiendo: 24 : 2 = 12,
12 : 3 = 4, y queda el 4."""

PIEZA = {
    "id": "tres_factores_en_orden",
    "nombre": "de izquierda a derecha, de dos en dos",
    "unidad": "M.14",
    "responde": "multiplicar_tres",
    "rapidez": 20,
    "que_hace": "2 x 3 x 4: 2 x 3 = 6, 6 x 4 = 24 (el orden de siempre)",
    "condiciones": [
        ("hay_tres_factores_o_mas", "no son tres factores o mas"),
        ("como_mucho_un_decimal", "hay dos decimales: decimal por decimal es de 6.o"),
        ("ningun_factor_es_cero", "hay un cero: el producto es cero sin hacer cuentas"),
    ],
    "usa": ["multiplicar", "multiplicar_decimal", "dividir", "dividir_decimal"],
}


def hacer(s, u):
    fs = s["factores"]
    actual, pasos = fs[0], []
    for f in fs[1:]:
        v, como = _por(u, actual, f)
        pasos.append("%s x %s = %s  (%s)" % (actual, f, v, como))
        actual = v
    vuelta, ok = _vuelta(u, actual, fs)
    return {"valor": actual, "metodo": "en el orden de siempre, de dos en dos (M.14)",
            "cuenta": "%s = %s" % (" x ".join(fs), actual), "pasos": pasos,
            "vuelta": vuelta, "vuelta_ok": ok}


# ---- lo comun a las piezas de tres factores (cada pieza lleva su copia: una pieza solo usa lo suyo)

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


def _deshacer(u, actual, quedan):
    """Dividir 'actual' entre los factores que quedan, uno a uno (primero los cortos).  Si un camino se
    atasca (una division que no se hacer), se prueba otro orden.  Devuelve (pasos, lo que queda, el
    factor que tenia que quedar) o None."""
    if len(quedan) == 1:
        return [], actual, quedan[0]
    for f in sorted((f for f in quedan if "." not in f), key=len):
        q = _entre(u, actual, f)
        if q is None:
            continue
        resto = list(quedan)
        resto.remove(f)
        sigue = _deshacer(u, q, resto)
        if sigue is not None:
            pasos = ["%s : %s = %s" % (actual, f, q)]
            pasos.extend(sigue[0])
            return pasos, sigue[1], sigue[2]
    return None


def _vuelta(u, producto, factores):
    """LA OPERACION CONTRARIA: el producto se va DIVIDIENDO entre los factores, uno a uno, y tiene que
    quedar el ultimo.  Entre el decimal no se divide (6.o): ese se deja para el final.  Devuelve (el texto
    de la vuelta, si cuadra)."""
    camino = _deshacer(u, producto, list(factores))
    if camino is None:
        raise ValueError("no lo puedo comprobar dividiendo (%s entre esos factores pide la division larga, 6.o)"
                         % producto)
    pasos, actual, falta = camino
    ok = _normal(actual) == _normal(falta)
    pasos.append("queda %s, %s" % (actual, "que es el factor que faltaba" if ok else "y tenia que quedar %s" % falta))
    return ", ".join(pasos), ok
