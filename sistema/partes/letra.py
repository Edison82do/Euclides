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


_LE_IMPLICITO = re.compile(r"\d\s*[a-wyz(]|\)\s*[a-wyz(\d]|(?<![a-z])[a-wyz]\s*\(|\dx(?![a-z(\d])|\d\s*x\s*(=|$|[+\-:;)])")


def _le_traducir(e):
    """Un arbol del MODELO comun (U.1) -> el arbol de E.5, si es de su forma: numeros para contar (enteros, sin signo)."""
    if e[0] == "num":
        n = e[1]
        if n[3] != "entero" or n[2] != 1 or (n[0] == "-" and n[1] != 0):
            raise ValueError("no es de E.5: %s no es un numero para contar" % _nu_texto(n))
        return ("n", n[1])
    if e[0] == "letra":
        return ("letra", e[1])
    if e[0] == "par":
        return ("par", _le_traducir(e[1]))
    if e[0] == "neg":
        raise ValueError("no es de E.5: un numero negativo")
    return ("op", e[1], _le_traducir(e[2]), _le_traducir(e[3]))


def _le_leer(texto):
    """E.5 es un TRADUCTOR al modelo (U.4): lee con el lector UNICO (_u_leer) y reconoce SU forma: UNA relacion, con
    numeros para contar, escrita con todos sus signos.  Lo que no es de su forma (fracciones, decimales, negativos,
    '2n') no es de E.5: va al resolvedor universal.  (Antes tenia su propio lector, que leia 1/2 como 1 : 2.)
    Devuelve (izq, der) en el arbol de E.5, o None."""
    t = texto.lower().replace("\u2212", "-").replace("\u00d7", " x ").replace("*", " x ").replace("\u00f7", ":")
    if _LE_IMPLICITO.search(t):
        return None                                      # '2n', '2(n + 1)': por sin escribir, no es de E.5
    try:
        m = _u_leer(t)
        if len(m["relaciones"]) != 1 or m["expresion"] is not None:
            return None
        izq, der = m["relaciones"][0]
        return _le_traducir(izq), _le_traducir(der)
    except (ValueError, IndexError, _NuNoSale):
        return None


def _le_ops(e):
    """Las operaciones de un arbol de E.5, en orden."""
    if e[0] in ("n", "letra"):
        return []
    if e[0] == "par":
        return _le_ops(e[1])
    out = _le_ops(e[2])
    out.append(e[1])
    out.extend(_le_ops(e[3]))
    return out


def _le_letras(e):
    if e[0] == "letra":
        return [e[1]]
    if e[0] == "n":
        return []
    if e[0] == "par":
        return _le_letras(e[1])
    out = _le_letras(e[2])
    out.extend(_le_letras(e[3]))
    return out


def _le_hay_par(e):
    if e[0] == "par":
        return True
    if e[0] == "op":
        return _le_hay_par(e[2]) or _le_hay_par(e[3])
    return False


def es_ecuacion_con_letra(texto):
    """Una ecuacion (con =) escrita sola, con una LETRA o con dos o mas operaciones o parentesis."""
    rel = _le_leer(texto)
    if rel is None:
        return False
    izq, der = rel
    todas = _le_letras(izq)
    todas.extend(_le_letras(der))
    if not todas:                                        # sin letra ni hueco es una igualdad (E.0): verdad o no
        return False
    letras = [l for l in todas if l != "?"]
    ops_i, ops_d = _le_ops(izq), _le_ops(der)
    if letras or _le_hay_par(izq) or _le_hay_par(der) or len(ops_i) >= 2 or len(ops_d) >= 2:
        return True
    # con un hueco '?' y una cuenta por lado: + y - es la balanza (E.2); con x o : a los dos lados, aqui
    return bool(ops_i and ops_d and set(ops_i).union(ops_d) & {"x", ":"})


# --- el arbol de la expresion (con el orden de siempre): el del MODELO comun, traducido (_le_leer)


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
    rel = _le_leer(texto)
    if rel is None:
        return {"conclusion": "no_entiendo", "porque": "no es una ecuacion de E.5 (una relacion con numeros para contar)"}
    izq, der = rel
    letras = _le_letras(izq)
    letras.extend(_le_letras(der))
    r = {"ecuacion": "%s = %s" % (_texto(izq), _texto(der)), "letra": letras[0] if letras else None}
    if not letras:
        r.update(conclusion="sin_letra", porque="no hay letra ni hueco: para saber si es verdad, 'verdad:'")
        return r
    if len(letras) > 1:
        r.update(conclusion="todavia_no", porque="la letra aparece %d veces (o hay dos letras): todavia no"
                 % len(letras))
        return r
    con, sin = (izq, der) if _tiene_letra(izq) else (der, izq)
    hay = set(_le_ops(izq)).union(_le_ops(der))
    if hay & {"x", ":"} and hay & {"+", "-"} and not (_le_hay_par(izq) or _le_hay_par(der)):
        r["nota_orden"] = ("OJO, el orden de siempre (3.OA.D.8): sin parentesis, PRIMERO x y :, LUEGO + y -; "
                           "no se va sin mas de izquierda a derecha")
    pasos = []
    eq = _eq_balanza_por(izq, der, saber)           # M.12 (NCETM 2.18): sin calcular los lados
    if eq is not None:
        r["como"] = "SIN CALCULAR LOS LADOS: la equivalencia (NCETM 2.18)"
        r["equivalencia"] = True
        pasos.append(eq["resultado"]["cuenta"])
        v = eq["valor"]
    else:
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
