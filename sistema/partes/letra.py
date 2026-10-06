# -*- coding: utf-8 -*-
"""
Euclides - DOS PASOS, CON LA LETRA COMO HUECO (paso E.5 del plan pedagogico, 6 oct 2026).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

Common Core 3.OA.D.8: problemas de dos pasos con las cuatro operaciones, representados con una
ecuacion con una LETRA en lugar de lo desconocido; sin parentesis, las operaciones en el ORDEN DE
SIEMPRE (primero x y :, luego + y -, de izquierda a derecha).  Si la letra esta dentro, se DESHACE de
fuera hacia dentro (trabajar hacia atras, Polya).  Cada cuenta la hacen las piezas (sumar, restar,
multiplicar, dividir); aqui solo se LEE, se ordena y se explica.
"""

import re

_OPS = {"+": "sumar", "-": "restar", "x": "multiplicar", ":": "dividir"}
_FUERTES = ("x", ":")


def _tokens(texto):
    t = texto.lower().replace("−", "-").replace("×", " x ").replace("*", " x ") \
        .replace("÷", ":").replace("/", ":")
    if re.search(r"[a-z]{2,}", t):
        return None                                      # hay palabras: no es una ecuacion sola
    crudos = re.findall(r"\d+|[a-z]|[()+\-:=?_]", t)
    if "".join(crudos) != re.sub(r"\s+", "", t):
        return None                                      # hay algo que no es de una ecuacion
    out, prev = [], None
    for c in crudos:
        if c.isdigit():
            tok = ("n", int(c))
        elif c in "?_":
            tok = ("letra", "?")
        elif c == "x" and prev is not None and prev[0] in ("n", "letra", ")"):
            tok = ("op", "x")                            # entre dos cosas: es POR
        elif c.isalpha():
            tok = ("letra", c)                           # donde va un numero: es una LETRA
        elif c in "+-:":
            tok = ("op", c)
        elif c == "(":
            tok = ("(", c)
        elif c == ")":
            tok = (")", c)
        else:
            tok = ("=", c)
        out.append(tok)
        prev = tok
    return out


def es_ecuacion_con_letra(texto):
    """Una ecuacion (con =) escrita sola, con una LETRA o con dos o mas operaciones o parentesis."""
    toks = _tokens(texto)
    if not toks or sum(1 for t in toks if t[0] == "=") != 1:
        return False
    if not any(t[0] == "letra" for t in toks):          # sin letra ni hueco es una igualdad (E.0): verdad o no
        return False
    letras = [t for t in toks if t[0] == "letra" and t[1] != "?"]
    k = [i for i, t in enumerate(toks) if t[0] == "="][0]
    ops_i = [t[1] for t in toks[:k] if t[0] == "op"]
    ops_d = [t[1] for t in toks[k + 1:] if t[0] == "op"]
    if letras or any(t[0] == "(" for t in toks) or len(ops_i) >= 2 or len(ops_d) >= 2:
        return True
    # con un hueco '?' y una cuenta por lado: + y - es la balanza (E.2); con x o : a los dos lados, aqui
    return bool(ops_i and ops_d and set(ops_i).union(ops_d) & {"x", ":"})


# --- el arbol de la expresion (con el orden de siempre)

def _parse(toks):
    quedan = list(toks)                                  # se van tomando por delante, de uno en uno

    def ver():
        return quedan[0] if quedan else (None, None)

    def tomar():
        return quedan.pop(0)

    def atomo():
        t = tomar()
        if t[0] == "n":
            return ("n", t[1])
        if t[0] == "letra":
            return ("letra", t[1])
        if t[0] == "(":
            e = suma()
            if tomar()[0] != ")":
                raise ValueError("falta cerrar un parentesis")
            return ("par", e)
        raise ValueError("no entiendo '%s'" % (t[1],))

    def producto():
        e = atomo()
        while ver()[0] == "op" and ver()[1] in _FUERTES:
            op = tomar()[1]
            e = ("op", op, e, atomo())
        return e

    def suma():
        e = producto()
        while ver()[0] == "op" and ver()[1] in "+-":
            op = tomar()[1]
            e = ("op", op, e, producto())
        return e

    e = suma()
    if quedan:
        raise ValueError("sobra algo al final")
    return e


def _texto(e, valor_letra=None):
    if e[0] == "n":
        return str(e[1])
    if e[0] == "letra":
        return str(valor_letra) if valor_letra is not None else e[1]
    if e[0] == "par":
        return "(%s)" % _texto(e[1], valor_letra)
    return "%s %s %s" % (_texto(e[2], valor_letra), e[1], _texto(e[3], valor_letra))


def _tiene_letra(e):
    if e[0] == "letra":
        return True
    if e[0] == "n":
        return False
    if e[0] == "par":
        return _tiene_letra(e[1])
    return _tiene_letra(e[2]) or _tiene_letra(e[3])


class _NoSale(Exception):
    pass


def _cuenta(op, a, b, saber, pasos, porque=""):
    if op == ":":
        r = aplicar("dividir", {"total": a, "divisor": b}, saber)
        if r["conclusion"] != "hecho":
            raise _NoSale("%d : %d no se puede (%s)" % (a, b, r.get("porque")))
        if r["resultado"].get("resto"):
            raise _NoSale("%d : %d no da justo (sobra %d): no hay numero entero" % (a, b, r["resultado"]["resto"]))
    else:
        r = aplicar(_OPS[op], {"a": a, "b": b}, saber)
        if r["conclusion"] != "hecho":
            raise _NoSale("%d %s %d no se puede (%s)" % (a, op, b, r.get("porque") or r["conclusion"]))
    v = r["valor"]
    pasos.append("%d %s %d = %d   (%s)%s" % (a, op, b, v, r["resultado"]["metodo"], porque))
    return v


def _valor(e, saber, pasos):
    """Calcula la expresion en el ORDEN DE SIEMPRE (el arbol ya lo tiene: x y : abajo)."""
    if e[0] == "n":
        return e[1]
    if e[0] == "par":
        return _valor(e[1], saber, pasos)
    a = _valor(e[2], saber, pasos)
    b = _valor(e[3], saber, pasos)
    nota = ""
    if e[1] in _FUERTES and _hay_suave_fuera(e, saber):
        nota = ""
    return _cuenta(e[1], a, b, saber, pasos, nota)


def _hay_suave_fuera(e, saber):
    return False


def _deshacer(e, objetivo, saber, pasos):
    """La letra esta dentro de e, y e tiene que valer 'objetivo': se deshace de fuera hacia dentro."""
    if e[0] == "letra":
        return objetivo
    if e[0] == "par":
        return _deshacer(e[1], objetivo, saber, pasos)
    op, izq, der = e[1], e[2], e[3]
    if _tiene_letra(izq):
        otro = _valor(der, saber, pasos)
        inversa = {"+": "-", "-": "+", "x": ":", ":": "x"}[op]
        nuevo = _cuenta(inversa, objetivo, otro, saber, pasos,
                        "   <- deshago '%s %d': %s = %d %s %d" % (op, otro, _texto(izq), objetivo, inversa, otro))
        return _deshacer(izq, nuevo, saber, pasos)
    otro = _valor(izq, saber, pasos)
    if op in ("+", "x"):                                 # conmutativas: igual que si estuviera a la izquierda
        inversa = {"+": "-", "x": ":"}[op]
        nuevo = _cuenta(inversa, objetivo, otro, saber, pasos,
                        "   <- deshago '%d %s': %s = %d %s %d" % (otro, op, _texto(der), objetivo, inversa, otro))
    else:                                                # otro - der = objetivo -> der = otro - objetivo
        nuevo = _cuenta(op, otro, objetivo, saber, pasos,
                        "   <- %d %s %s = %d, asi que %s = %d %s %d" % (otro, op, _texto(der), objetivo,
                                                                     _texto(der), otro, op, objetivo))
    return _deshacer(der, nuevo, saber, pasos)


def decidir_ecuacion_letra(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    toks = _tokens(texto)
    if not toks:
        return {"conclusion": "no_entiendo", "porque": "no es una ecuacion"}
    k = [i for i, t in enumerate(toks) if t[0] == "="]
    if len(k) != 1:
        return {"conclusion": "no_entiendo", "porque": "hace falta UN signo ="}
    try:
        izq, der = _parse(toks[:k[0]]), _parse(toks[k[0] + 1:])
    except (ValueError, IndexError) as ex:
        return {"conclusion": "no_entiendo", "porque": str(ex)}
    letras = [t[1] for t in toks if t[0] == "letra"]
    r = {"ecuacion": "%s = %s" % (_texto(izq), _texto(der)), "letra": letras[0] if letras else None}
    if not letras:
        r.update(conclusion="sin_letra", porque="no hay letra ni hueco: para saber si es verdad, 'verdad:'")
        return r
    if len(letras) > 1:
        r.update(conclusion="todavia_no", porque="la letra aparece %d veces (o hay dos letras): todavia no"
                 % len(letras))
        return r
    con, sin = (izq, der) if _tiene_letra(izq) else (der, izq)
    hay = {t[1] for t in toks if t[0] == "op"}
    if hay & {"x", ":"} and hay & {"+", "-"} and not any(t[0] == "(" for t in toks):
        r["nota_orden"] = ("OJO, el orden de siempre (3.OA.D.8): sin parentesis, PRIMERO x y :, LUEGO + y -; "
                           "no se va sin mas de izquierda a derecha")
    pasos = []
    try:
        objetivo = _valor(sin, saber, pasos)
        r["lado_conocido"] = objetivo
        if con[0] == "letra":
            r["como"] = "calcular el otro lado en el orden de siempre (primero x y :, luego + y -)"
            v = objetivo
        else:
            r["como"] = "DESHACER de fuera hacia dentro (trabajar hacia atras)"
            v = _deshacer(con, objetivo, saber, pasos)
    except _NoSale as ex:
        r.update(conclusion="no_sale", porque=str(ex), pasos=pasos)
        return r
    r.update(valor=v, pasos=pasos)
    # LA COMPROBACION: se pone el numero en la letra y se calcula todo
    comp = []
    try:
        vi, vd = _valor(_sustituir(izq, v), saber, comp), _valor(_sustituir(der, v), saber, comp)
        r["comprobacion"] = "%s = %s  ->  %d = %d" % (_texto(izq, v), _texto(der, v), vi, vd)
        r["comprobacion_ok"] = vi == vd
    except _NoSale:
        r["comprobacion_ok"] = False
    r["conclusion"] = "hecho" if r.get("comprobacion_ok") else "no_cuadra"
    return r


def _sustituir(e, v):
    if e[0] == "letra":
        return ("n", v)
    if e[0] == "n":
        return e
    if e[0] == "par":
        return ("par", _sustituir(e[1], v))
    return ("op", e[1], _sustituir(e[2], v), _sustituir(e[3], v))


def explicar_ecuacion_letra(texto, saber=None):
    r = decidir_ecuacion_letra(texto, saber)
    if r["conclusion"] == "no_entiendo":
        return ("NO ENTIENDO ESTO: %s\n   se escribe asi:  3 x 4 - 5 = c     o   3 x n + 2 = 14"
                % r.get("porque", ""))
    L = ["PREGUNTA (E.5): cuanto vale la letra?   %s" % r["ecuacion"],
         "  (la letra es un HUECO CON NOMBRE; 3.OA.D.8)", ""]
    if r["conclusion"] in ("sin_letra", "todavia_no"):
        return "\n".join(L + ["  %s" % r["porque"], "", "RESULTADO: %s" % r["conclusion"]])
    L.append("  1. COMO: %s." % r.get("como", ""))
    if r.get("nota_orden"):
        L.append("     %s" % r["nota_orden"])
    L.append("")
    L.append("  2. LAS CUENTAS, UNA A UNA:")
    for p in r.get("pasos", []):
        L.append("        %s" % p)
    if r["conclusion"] == "no_sale":
        return "\n".join(L + ["", "  NO SALE: %s" % r["porque"], "", "RESULTADO: no_sale"])
    L.append("")
    L.append("  3. COMPRUEBO poniendo el %d en la letra: %s ... %s"
             % (r["valor"], r.get("comprobacion", ""), "SI" if r["comprobacion_ok"] else "NO"))
    L.append("")
    L.append("RESULTADO: %s = %d" % (r["letra"] if r["letra"] != "?" else "el hueco", r["valor"]))
    return "\n".join(L)
