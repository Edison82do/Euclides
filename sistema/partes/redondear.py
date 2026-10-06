# -*- coding: utf-8 -*-
"""
Euclides - REDONDEAR A LA DECENA Y A LA CENTENA (paso N.2 del plan pedagogico, 6 oct 2026).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

Common Core 3.NBT.A.1: 'usar el valor de posicion para redondear a la decena o a la centena mas
cercana'.  Se ENTIENDE en la recta (de cual esta mas cerca; la mitad del camino) y el atajo de la cifra
lo resume: las dos piezas se hacen y tienen que coincidir (pregunta 'redondear', todas_iguales).
Es lo que hace falta para la estimacion de 3.OA.D.8 ('es razonable la respuesta?'), el paso E.6.
"""

import re

_ORDEN_REDONDEAR = re.compile(
    r"^(\d+)(?:\s+(?:a\s+la|al|a)\s+(decena|centena|diez|cien|millar|mil|unidad)(?:\s+mas\s+cercana)?)?\s*$")
_SITIO_DE = {"decena": "decena", "diez": "decena", "centena": "centena", "cien": "centena",
             "millar": "millar", "mil": "millar"}                                 # N.3 (4.NBT.A.3)


def decidir_redondear(n, a, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    return aplicar("redondear", {"n": n, "a": a}, saber)


def _leer_orden_redondear(texto):
    t = " ".join(texto.lower().replace("á", "a").strip().rstrip("?").split())
    m = _ORDEN_REDONDEAR.match(t)
    if not m:
        return None
    return int(m.group(1)), m.group(2)


def explicar_redondear(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    leido = _leer_orden_redondear(texto)
    if leido is None:
        return ("NO ENTIENDO ESTO: dame un numero y, si quieres, el sitio.\n"
                "   se escribe asi:  redondear: 37     redondear: 247 a la centena")
    n, sitio = leido
    L = ["PREGUNTA (N.2): redondear %d  (3.NBT.A.1: a la decena o a la centena MAS CERCANA)" % n, ""]
    if sitio == "unidad" or decir(n, saber) is None:
        porque = ("a la unidad no se redondea: ya es un numero entero" if sitio == "unidad" else
                  "%d no esta en mi lista (llego hasta %s)" % (n, techo(saber)))
        return "\n".join(L + ["  TODAVIA NO: %s" % porque, "", "RESULTADO: todavia_no"])
    sitios = [_SITIO_DE[sitio]] if sitio else ["decena", "centena"]
    if not sitio and len(cifras_de(n)) >= 4:
        sitios.append("millar")                                           # N.3: de cuatro cifras, tambien al millar
    finales, valores = [], {}
    for a in sitios:
        r = decidir_redondear(n, a, saber)
        L.append("  %s %s:" % ("AL" if a == "millar" else "A LA", a.upper()))
        if r["conclusion"] != "hecho":
            L.append("    NO SALE: %s" % r.get("porque"))
            finales.append("%s %s" % (a, r["conclusion"]))
            continue
        for pid, res in sorted(r.get("todos", []), key=lambda x: x[0] != "redondear_en_la_recta"):
            nombre = "EN LA RECTA" if pid == "redondear_en_la_recta" else "EL ATAJO"
            primera = True
            for linea in res["cuenta"].splitlines():
                L.append("    %-12s %s" % (nombre + ":" if primera else "", linea))
                primera = False
        valores[a] = r["valor"]
        L.append("    -> los dos caminos dicen %d" % r["valor"])
        L.append("")
        finales.append("%d" % r["valor"] if sitio else "%s %d" % (a, r["valor"]))
    if not sitio and "decena" in valores and "centena" in valores:
        cadena = decidir_redondear(valores["decena"], "centena", saber)
        if cadena["conclusion"] == "hecho" and cadena["valor"] != valores["centena"]:
            L.append("  OJO, LA TRAMPA DE LA CADENA: si redondeara %d (lo ya redondeado) a la centena saldria %d;"
                     % (valores["decena"], cadena["valor"]))
            L.append("  pero se redondea el NUMERO, %d, y %d esta mas cerca de %d."
                     % (n, n, valores["centena"]))
            L.append("")
    L.append("RESULTADO: %s" % ", ".join(finales))
    return "\n".join(L)
