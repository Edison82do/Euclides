# -*- coding: utf-8 -*-
"""
Euclides - LOS NUMEROS NEGATIVOS (paso N.5 del plan pedagogico, 7 oct 2026; 5.o).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

NCETM 1.27 (Negative numbers: counting, comparing and calculating); Common Core 6.NS.C.5-7.
La recta sigue a la IZQUIERDA del cero como un ESPEJO: antes del cero va "menos uno", antes de
"menos uno" va "menos dos"...  Cuanto mayor es la cifra detras del signo, mas lejos del cero y MAS
PEQUENO.  Cruzar el cero es como "hacer diez": hasta el cero, y lo que queda despues.

Un numero con signo se guarda como (signo, cuanto): ("-", 5) es -5.  "cuanto" es un numero natural
de los de siempre, y todas sus cuentas se hacen con las piezas (sumar, restar), sin calculadora.
"""

import re

_NEG_NUM = r"([+-−]?\s?\d+)"
_ORDEN_NEGATIVO = re.compile(r"^negativo:?\s*" + _NEG_NUM + r"$")
_ORDEN_COMPARAR = re.compile(r"^comparar:?\s*" + _NEG_NUM + r"\s*(?:y|,|con)\s*" + _NEG_NUM + r"$")
_ORDEN_INTERVALO = re.compile(r"^(?:intervalo|distancia):?\s*(?:de|entre)?\s*" + _NEG_NUM + r"\s*(?:y|a|,|hasta)\s*" + _NEG_NUM + r"$")
_ORDEN_RECTA_CUENTA = re.compile(r"^recta:?\s*" + _NEG_NUM + r"\s*([+-])\s*(\d+)$")
_ORDEN_RECTA_PASOS = re.compile(r"^recta:?\s*desde\s*" + _NEG_NUM + r"\s*(subiendo|bajando)\s*(\d+)$")
_TEMP_INICIO = re.compile(r"(?:es|hace|esta a|marca|de)\s+" + _NEG_NUM + r"\s*grados")
_TEMP_CAMBIO = re.compile(r"\b(sube|baja|subio|bajo)\s+(\d+)\s*grados?")
_TEMP_DOS = re.compile(_NEG_NUM + r"\s*grados?\b.*?\b" + _NEG_NUM + r"\s*grados?")
_TEMP_PREG_CAMBIO = re.compile(r"cuant\w* (?:ha |han )?(?:subido|subio|bajado|bajo|cambiado|cambio|diferencia)")


def _neg_limpio(texto):
    t = texto.lower().replace("−", "-")
    for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("¿", ""), ("¡", ""), ("º", ""), ("°", "")):
        t = t.replace(a, b)
    t = re.sub(r"\bmenos\s+(\d)", r"-\1", t)
    return " ".join(t.strip().split())


def _neg_leer(txt):
    """'-5' -> ('-', 5); '7' o '+7' -> ('+', 7).  El cero no tiene signo: ('+', 0)."""
    s = txt.replace(" ", "")
    signo = "-" if s.startswith("-") else "+"
    cuanto = int(s.lstrip("+-"))
    if cuanto == 0:
        signo = "+"
    return signo, cuanto


def _neg_texto(x):
    return "-%d" % x[1] if x[0] == "-" else "%d" % x[1]


def _neg_nombre(x, saber):
    n = decir(x[1], saber)
    return "menos %s" % n if x[0] == "-" else n


def _neg_cabe(x, saber):
    return decir(x[1], saber) is not None


def _neg_mas_lejos(a, b, saber):
    """a esta MAS lejos del cero que b (mirando solo las cifras: viene despues en la lista)."""
    return viene_despues(decir(a, saber), decir(b, saber), saber)


def _neg_comparar(x, y, saber):
    """'<', '>' o '=' entre dos numeros con signo (NCETM 1.27, punto 4)."""
    if x == y:
        return "="
    if x[0] != y[0]:
        return "<" if x[0] == "-" else ">"
    lejos = _neg_mas_lejos(x[1], y[1], saber)
    if x[0] == "+":
        return ">" if lejos else "<"
    return "<" if lejos else ">"


def _neg_sumar(a, b, saber):
    return aplicar("sumar", {"a": a, "b": b}, saber)["valor"]


def _neg_restar(a, b, saber):
    return aplicar("restar", {"a": a, "b": b}, saber)["valor"]


def _neg_mover(x, sube, k, saber):
    """Moverse k pasos en la recta desde x, subiendo (a la derecha) o bajando (a la izquierda).
    Devuelve (resultado, lineas que lo explican)."""
    signo, m = x
    hacia_el_cero = (signo == "+" and not sube) or (signo == "-" and sube)
    if not hacia_el_cero:
        r = _neg_sumar(m, k, saber)
        lado = "derecha" if sube else "izquierda"
        return (signo if m else ("+" if sube else "-"), r), [
            "  me ALEJO del cero hacia la %s: %d + %d = %d  (se suman los pasos)" % (lado, m, k, r)]
    if not viene_despues(decir(k, saber), decir(m, saber), saber):
        r = _neg_restar(m, k, saber)
        return (signo if r else "+", r), [
            "  me ACERCO al cero %d pasos y no llego a cruzarlo: %d - %d = %d" % (k, m, k, r)]
    queda = _neg_restar(k, m, saber)
    nuevo = "+" if sube else "-"
    return (nuevo, queda), [
        "  CRUZO EL CERO (como hacer diez: hasta el cero, y lo que queda):",
        "     de %s al cero hay %d pasos;  %d - %d = %d pasos me quedan" % (_neg_texto(x), m, k, m, queda),
        "     y los doy %s del cero: %s" % ("a la DERECHA" if sube else "a la IZQUIERDA", _neg_texto((nuevo, queda)))]


def _neg_paso(x, sube, saber):
    """Un paso en la recta con la lista (espejo a la izquierda del cero)."""
    signo, m = x
    if (signo == "+") == sube or m == 0:
        if m == 0:
            return ("+" if sube else "-", 1)
        return (signo, leer(siguiente(decir(m, saber), saber), saber))
    return (signo if m != 1 else "+", leer(anterior(decir(m, saber), saber), saber))


def _neg_intervalo(x, y, saber):
    """La distancia entre x y y en la recta (NCETM 1.27, punto 5)."""
    if x[0] == y[0] or x[1] == 0 or y[1] == 0:
        g, p = (x[1], y[1]) if not viene_despues(decir(y[1], saber), decir(x[1], saber), saber) else (y[1], x[1])
        r = _neg_restar(g, p, saber)
        if x[1] == 0 or y[1] == 0:
            como = "uno es el cero: la distancia es la cifra del otro, %d" % r
        else:
            como = "los dos al mismo lado del cero: %d - %d = %d" % (g, p, r)
        return r, como
    r = _neg_sumar(x[1], y[1], saber)
    return r, "uno a cada lado del cero: %d hasta el cero y %d desde el cero, %d + %d = %d" % (
        x[1], y[1], x[1], y[1], r)


# --------------------------------------------------------------------------- las ordenes

def es_orden_negativos(texto):
    t = _neg_limpio(texto)
    if t.startswith("problema:"):
        t = t[len("problema:"):].strip()
    if _ORDEN_NEGATIVO.match(t) or _ORDEN_INTERVALO.match(t) or _ORDEN_RECTA_CUENTA.match(t) or _ORDEN_RECTA_PASOS.match(t):
        return True
    m = _ORDEN_COMPARAR.match(t)
    if m and ("-" in m.group(1) or "-" in m.group(2)):
        return True
    return "grados" in t and bool(_TEMP_CAMBIO.search(t) or _TEMP_PREG_CAMBIO.search(t))


def _neg_no_cabe(saber):
    return "\n".join(["NO SE PUEDE: me paso de lo que se (los numeros llegan a %s, y a la izquierda a menos %s)"
                      % (techo(saber), techo(saber)), "", "RESULTADO: no_alcanza"])


def explicar_negativo(x, saber):
    L = ["PREGUNTA (N.5): que es %s?  (NCETM 1.27, puntos 2-4)" % _neg_texto(x), ""]
    if x[1] == 0:
        L += ["  el CERO no es ni positivo ni negativo: es la frontera.", "", "RESULTADO: cero"]
        return "\n".join(L)
    lado = "IZQUIERDA" if x[0] == "-" else "DERECHA"
    L.append("  se lee: %s" % _neg_nombre(x, saber))
    L.append("  esta a la %s del cero, a %d pasos: %s" % (lado, x[1],
             "es NEGATIVO (menor que cero)" if x[0] == "-" else "es POSITIVO (mayor que cero)"))
    if x[0] == "-":
        L.append("  el signo menos delante de la cifra dice que es negativo; cuanto mayor la cifra, mas lejos del cero")
        if x[1] <= 10:
            marcas = ["-%d" % k for k in range(x[1], 0, -1)]
            marcas.extend(["0", "1", "2"])
            L.append("     %s" % " ".join(marcas))
    L += ["", "RESULTADO: %s" % _neg_nombre(x, saber)]
    return "\n".join(L)


def explicar_comparar_negativos(x, y, saber):
    s = _neg_comparar(x, y, saber)
    L = ["PREGUNTA (N.5): cual es mayor, %s o %s?  (NCETM 1.27, punto 4; 6.NS.C.7)" % (_neg_texto(x), _neg_texto(y)), ""]
    if x[0] != y[0]:
        neg = x if x[0] == "-" else y
        L.append("  %s esta a la IZQUIERDA del cero y el otro no: el de la izquierda es MENOR" % _neg_texto(neg))
    elif x[0] == "-" and s != "=":
        lejos = x if s == "<" else y
        L.append("  los dos son negativos: el de cifra MAYOR (%d) esta MAS LEJOS del cero, a la izquierda: es el MENOR"
                 % lejos[1])
        L.append("  OJO: -%d NO es mayor que -%d aunque %d sea mayor que %d (piensa en el frio: %s grados es mas frio)"
                 % (lejos[1], (y if lejos is x else x)[1], lejos[1], (y if lejos is x else x)[1], _neg_texto(lejos)))
    else:
        L.append("  los dos a la derecha del cero: se comparan como siempre (N.3)")
    L += ["", "RESULTADO: %s %s %s" % (_neg_texto(x), s, _neg_texto(y))]
    return "\n".join(L)


def decidir_recta_cuenta(x, op, k, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    if not _neg_cabe(x, saber) or decir(k, saber) is None:
        return {"conclusion": "no_alcanza"}
    try:
        r, lineas = _neg_mover(x, op == "+", k, saber)
    except (KeyError, NoSalio):
        return {"conclusion": "no_alcanza"}
    if not _neg_cabe(r, saber):
        return {"conclusion": "no_alcanza"}
    return {"conclusion": "hecho", "valor": r, "lineas": lineas}


def explicar_recta_cuenta(x, op, k, saber):
    r = decidir_recta_cuenta(x, op, k, saber)
    L = ["PREGUNTA (N.5): %s %s %d en la RECTA  (NCETM 1.27, punto 5)" % (_neg_texto(x), op, k), "",
         "  %s %d es %s %d pasos (a la %s)" % (op, k, "SUBIR" if op == "+" else "BAJAR", k,
                                              "derecha" if op == "+" else "izquierda")]
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["", _neg_no_cabe(saber)])
    L += r["lineas"]
    if x[0] == "+" and op == "-" and r["valor"][0] == "-":
        L.append("  (con COSAS no se pueden quitar %d de %d: no hay bastantes.  En la RECTA si: se pasa del cero)" % (k, x[1]))
    L += ["", "  %s %s %d = %s" % (_neg_texto(x), op, k, _neg_texto(r["valor"])), "",
          "RESULTADO: %s" % _neg_texto(r["valor"])]
    return "\n".join(L)


def explicar_recta_pasos(x, sube, k, saber):
    L = ["PREGUNTA (N.5): desde %s, %s %d  (contar en la recta cruzando el cero; NCETM 1.27)"
         % (_neg_texto(x), "subiendo" if sube else "bajando", k), ""]
    if not _neg_cabe(x, saber) or decir(k, saber) is None:
        return "\n".join(L + [_neg_no_cabe(saber)])
    if viene_despues(decir(k, saber), "cincuenta", saber):
        return "\n".join(L + ["  son muchos pasos para decirlos uno a uno: mejor  recta: %s %s %d"
                              % (_neg_texto(x), "+" if sube else "-", k), "", "RESULTADO: demasiados_pasos"])
    pasos, actual, marca = [], x, "cero"
    while marca != decir(k, saber):
        actual = _neg_paso(actual, sube, saber)
        if not _neg_cabe(actual, saber):
            return "\n".join(L + [_neg_no_cabe(saber)])
        pasos.append(_neg_texto(actual))
        marca = siguiente(marca, saber)
    L.append("  un paso cada vez (a la izquierda del cero la cifra SUBE: -1, -2, -3...):")
    L.append("     %s" % ", ".join(pasos))
    L += ["", "RESULTADO: %s" % ", ".join(pasos)]
    return "\n".join(L)


def explicar_intervalo(x, y, saber):
    L = ["PREGUNTA (N.5): cuanto hay de %s a %s?  (intervalo a traves del cero; NCETM 1.27, punto 5)"
         % (_neg_texto(x), _neg_texto(y)), ""]
    if not (_neg_cabe(x, saber) and _neg_cabe(y, saber)):
        return "\n".join(L + [_neg_no_cabe(saber)])
    try:
        r, como = _neg_intervalo(x, y, saber)
    except (KeyError, NoSalio):
        return "\n".join(L + [_neg_no_cabe(saber)])
    L += ["  %s" % como, "", "RESULTADO: %d" % r]
    return "\n".join(L)


def explicar_temperatura(texto, saber):
    t = _neg_limpio(texto)
    if t.startswith("problema:"):
        t = t[len("problema:"):].strip()
    L = ["PREGUNTA (N.5): %s" % texto.strip(), "  (la temperatura: los negativos representan un CAMBIO; NCETM 1.27, punto 1)", ""]
    cambio = _TEMP_CAMBIO.search(t)
    if _TEMP_PREG_CAMBIO.search(t) and not cambio:
        m = _TEMP_DOS.search(t)
        if not m:
            return "NO ENTIENDO ESTO: necesito las dos temperaturas (por ejemplo: por la manana -6 grados y a mediodia 5 grados)"
        x, y = _neg_leer(m.group(1)), _neg_leer(m.group(2))
        try:
            r, como = _neg_intervalo(x, y, saber)
        except (KeyError, NoSalio):
            return "\n".join(L + [_neg_no_cabe(saber)])
        s = _neg_comparar(x, y, saber)
        verbo = "SUBIO" if s == "<" else "BAJO" if s == ">" else "no cambio"
        L += ["  de %s grados a %s grados: %s" % (_neg_texto(x), _neg_texto(y), como),
              "  la temperatura %s %d grados" % (verbo, r), "", "RESULTADO: %d grados" % r]
        return "\n".join(L)
    m = _TEMP_INICIO.search(t)
    if not (m and cambio):
        return "NO ENTIENDO ESTO: dime la temperatura y cuanto sube o baja (la temperatura es -4 grados. sube 7 grados.)"
    x = _neg_leer(m.group(1))
    sube = cambio.group(1).startswith("sub")
    k = int(cambio.group(2))
    r = decidir_recta_cuenta(x, "+" if sube else "-", k, saber)
    if r["conclusion"] != "hecho":
        return "\n".join(L + [_neg_no_cabe(saber)])
    L.append("  empieza en %s grados y %s %d: es %s %s %d en la recta" % (_neg_texto(x), "SUBE" if sube else "BAJA",
                                                                        k, _neg_texto(x), "+" if sube else "-", k))
    L += r["lineas"]
    L += ["", "RESULTADO: %s grados" % _neg_texto(r["valor"])]
    return "\n".join(L)


def explicar_orden_negativos(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    t = _neg_limpio(texto)
    if t.startswith("problema:"):
        t = t[len("problema:"):].strip()
    m = _ORDEN_NEGATIVO.match(t)
    if m:
        x = _neg_leer(m.group(1))
        return explicar_negativo(x, saber) if _neg_cabe(x, saber) else _neg_no_cabe(saber)
    m = _ORDEN_COMPARAR.match(t)
    if m:
        x, y = _neg_leer(m.group(1)), _neg_leer(m.group(2))
        if not (_neg_cabe(x, saber) and _neg_cabe(y, saber)):
            return _neg_no_cabe(saber)
        return explicar_comparar_negativos(x, y, saber)
    m = _ORDEN_INTERVALO.match(t)
    if m:
        return explicar_intervalo(_neg_leer(m.group(1)), _neg_leer(m.group(2)), saber)
    m = _ORDEN_RECTA_CUENTA.match(t)
    if m:
        return explicar_recta_cuenta(_neg_leer(m.group(1)), m.group(2), int(m.group(3)), saber)
    m = _ORDEN_RECTA_PASOS.match(t)
    if m:
        return explicar_recta_pasos(_neg_leer(m.group(1)), m.group(2) == "subiendo", int(m.group(3)), saber)
    return explicar_temperatura(texto, saber)
