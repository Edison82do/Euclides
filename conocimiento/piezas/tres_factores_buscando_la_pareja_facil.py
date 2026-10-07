# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR TRES FACTORES (o mas) BUSCANDO LA PAREJA FACIL (paso M.14; NCETM 2.20, puntos 4
y 5).  'La conmutativa y la asociativa se pueden usar al multiplicar tres numeros o mas; el orden se
elige segun la cuenta mas sencilla.'  25 x 7 x 4: el 25 y el 4 son AMIGOS (uno acaba en 5 y el otro es
par: dan decenas justas), 25 x 4 = 100, y 100 x 7 = 700.  Si un factor ya son decenas justas, se deja
para el final: 7 x 20 x 3 -> 7 x 3 = 21, 21 x 20 = 420.  Con un decimal igual: 0.25 x 7 x 4 -> 0.25 x 4 =
1, 1 x 7 = 7; y si no hay pareja amiga, el decimal se multiplica por cada entero de una cifra, uno a uno
(6 x 8 x 0.37 -> 0.37 x 6 = 2.22, 2.22 x 8 = 17.76; no 48 x 0.37, que es la multiplicacion larga).  Se COMPRUEBA dividiendo el producto entre los factores, uno a uno."""

PIEZA = {
    "id": "tres_factores_buscando_la_pareja_facil",
    "nombre": "cambiar el orden: primero la pareja que da decenas justas",
    "unidad": "M.14",
    "responde": "multiplicar_tres",
    "rapidez": 5,
    "que_hace": "25 x 7 x 4 = (25 x 4) x 7 = 100 x 7 = 700: el orden que haga la cuenta mas facil",
    "condiciones": [
        ("hay_tres_factores_o_mas", "no son tres factores o mas"),
        ("como_mucho_un_decimal", "hay dos decimales: decimal por decimal es de 6.o"),
        ("ningun_factor_es_cero", "hay un cero: el producto es cero sin hacer cuentas"),
        ("hay_una_pareja_facil", "ninguna pareja da decenas justas (uno que acabe en 5 con uno par), "
                                 "ningun factor son decenas justas y no hay decimal: no hay un orden mas facil"),
    ],
    "usa": ["multiplicar", "multiplicar_decimal", "dividir", "dividir_decimal"],
}


def _acaba_en_5(f):
    return f.replace(".", "").rstrip("0").endswith("5")


def _par(f):
    return f != "0" and f[-1] in "02468"


def _justas(f):
    return "." not in f and f != "0" and f.endswith("0")


def _corto(f):
    """M.13: un decimal solo se multiplica por un entero de una cifra, o por 10 o 100."""
    return "." not in f and (len(f) == 1 or f in ("10", "100"))


def _amigos(f, g):
    if "." in f and "." in g:
        return False
    if ("." in f and not _corto(g)) or ("." in g and not _corto(f)):
        return False
    return (_acaba_en_5(f) and _par(g)) or (_acaba_en_5(g) and _par(f))


def _elegir(quedan):
    """La pareja que se multiplica ahora, y por que."""
    for i, f in enumerate(quedan):
        for g in quedan[i + 1:]:
            if _amigos(f, g) and not (_justas(f) and _justas(g)):
                cinco, par = (f, g) if _acaba_en_5(f) else (g, f)
                return f, g, "%s acaba en 5 y %s es par: juntos dan una cuenta redonda" % (cinco, par)
    decimal = [f for f in quedan if "." in f]
    if decimal:
        # M.13: un decimal por un entero de UNA cifra (o por 10 o 100); el decimal va con cada entero, uno a uno
        cortos = [f for f in quedan if _corto(f)]
        if cortos:
            return decimal[0], cortos[0], "el decimal por un entero corto (M.13), uno a uno"
    justas = [f for f in quedan if _justas(f)]
    otros = [f for f in quedan if not _justas(f)]
    if len(otros) >= 2:
        if justas:
            return otros[0], otros[1], "dejo %s para el final (decenas justas)" % " y ".join(justas)
        return otros[0], otros[1], "los que quedan"
    return quedan[0], quedan[1], "con decenas justas es facil"


def hacer(s, u):
    fs = s["factores"]
    quedan, pasos, orden = list(fs), [], []
    while len(quedan) > 1:
        f, g, porque = _elegir(quedan)
        v, como = _por(u, f, g)
        pasos.append("%s x %s = %s  (%s; %s)" % (f, g, v, porque, como))
        orden.append("%s x %s" % (f, g))
        quedan.remove(f)
        quedan.remove(g)
        quedan.append(v)
    valor = quedan[0]
    vuelta, ok = _vuelta(u, valor, fs)
    return {"valor": valor, "metodo": "cambiar el orden: primero la pareja facil (conmutativa y asociativa, M.14)",
            "cuenta": "%s = %s" % (" x ".join(fs), valor), "pasos": pasos, "orden": orden,
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
