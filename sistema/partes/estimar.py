# -*- coding: utf-8 -*-
"""
Euclides - ES RAZONABLE?  ESTIMAR REDONDEANDO (paso E.6 del plan pedagogico, 6 oct 2026).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

Common Core 3.OA.D.8: 'valorar si la respuesta es razonable usando calculo mental y estimacion,
incluido el redondeo'.  Cada numero se redondea (N.2), se hace la cuenta facil con las piezas, y se
dice la BANDA: cuanto se pudieron mover los numeros al redondear (5 cada uno a la decena, 50 a la
centena).  Fuera de la banda, la respuesta esta mal SEGURO.  Dentro, es razonable... que no es lo
mismo que correcta: por eso despues se hace la cuenta de verdad, y se dice.
"""

import re

_CUENTA_ESTIMAR = re.compile(r"^(\d+)\s*([+\-x*:/])\s*(\d+)\s*$")
_CUENTA_RAZONABLE = re.compile(r"^(\d+)\s*([+\-x*:/])\s*(\d+)\s*=\s*(\d+)\s*$")
_OP_ESTIMAR = {"+": "+", "-": "-", "x": "x", "*": "x", ":": ":", "/": ":"}
_PREGUNTA_DE = {"+": "sumar", "-": "restar", "x": "multiplicar"}
_MOVIMIENTO = {"decena": 5, "centena": 50}


def _sitio_para_estimar(n):
    """Hasta 99, a la decena; de 100 en adelante, a la centena (se mira cuantas cifras tiene)."""
    return "centena" if len(cifras_de(n)) >= 3 else "decena"


def _hacer(op, a, b, saber):
    r = aplicar(_PREGUNTA_DE[op], {"a": a, "b": b}, saber)
    return r["valor"] if r["conclusion"] == "hecho" else None


def decidir_estimar(a, op, b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = {"a": a, "op": op, "b": b}
    if op == ":":
        r.update(conclusion="todavia_no", porque="estimar una division todavia no (hacen falta numeros compatibles)")
        return r
    if decir(a, saber) is None or decir(b, saber) is None:
        r.update(conclusion="todavia_no", porque="los numeros tienen que estar en mi lista (hasta mil)")
        return r
    if op == "-" and viene_despues(decir(b, saber), decir(a, saber), saber):
        r.update(conclusion="imposible", porque="%d es mas que %d: no se puede quitar" % (b, a))
        return r
    redondeos, movido = [], []
    if op == "x":
        unos = [len(cifras_de(a)) == 1, len(cifras_de(b)) == 1]
        if all(unos):
            r.update(conclusion="no_hace_falta", porque="los dos son de una cifra: es un hecho de la tabla, no se estima")
            return r
        if not any(unos):
            r.update(conclusion="todavia_no", porque="los dos factores pasan de una cifra: todavia no (3.o pide un factor de una cifra)")
            return r
        pequeno, grande = (a, b) if unos[0] else (b, a)
        sitio = _sitio_para_estimar(grande)
        rg = decidir_redondear(grande, sitio, saber)
        redondeos.append((grande, sitio, rg["valor"]))
        ea, eb = (a, rg["valor"]) if unos[0] else (rg["valor"], b)
        banda = _hacer("x", pequeno, _MOVIMIENTO[sitio], saber)
        r["por_que_banda"] = "%d se movio como mucho %d, y va %d veces: como mucho %d x %d = %d" % (
            grande, _MOVIMIENTO[sitio], pequeno, pequeno, _MOVIMIENTO[sitio], banda)
    else:
        ea_b = []
        for n in (a, b):
            sitio = _sitio_para_estimar(n)
            rn = decidir_redondear(n, sitio, saber)
            redondeos.append((n, sitio, rn["valor"]))
            movido.append(_MOVIMIENTO[sitio])
            ea_b.append(rn["valor"])
        ea, eb = ea_b
        banda = _hacer("+", movido[0], movido[1], saber)
        r["por_que_banda"] = ("al redondear, %d se movio como mucho %d y %d como mucho %d: la cuenta de verdad "
                              "no se aleja mas de %d + %d = %d" % (a, movido[0], b, movido[1], movido[0], movido[1], banda))
    est = _hacer(op, ea, eb, saber)
    if est is None or banda is None:
        r.update(conclusion="todavia_no", porque="la cuenta facil se me sale de la lista")
        return r
    desde = _hacer("-", est, banda, saber) if not viene_despues(decir(banda, saber), decir(est, saber), saber) else 0
    hasta = _hacer("+", est, banda, saber)
    r["tope"] = hasta is None
    if hasta is None:                                   # la banda pasa de mil: mi lista acaba ahi
        hasta = 1000
    r.update(conclusion="hecho", redondeos=redondeos, facil="%d %s %d" % (ea, op, eb), estimacion=est,
             banda=banda, desde=desde, hasta=hasta)
    return r


def _dentro(n, r, saber):
    """Cae n dentro de la banda?  Se mira en la LISTA si va antes o despues de los bordes."""
    pn = decir(n, saber)
    if pn is None:
        return False                                    # pasa de mil: la banda no llega ahi
    if viene_despues(decir(r["desde"], saber), pn, saber):
        return False
    if r["hasta"] is not None and decir(r["hasta"], saber) is not None and viene_despues(pn, decir(r["hasta"], saber), saber):
        return False
    return True


def decidir_razonable(a, op, b, respuesta, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_estimar(a, op, b, saber)
    r["respuesta"] = respuesta
    if r["conclusion"] != "hecho":
        return r
    r["razonable"] = _dentro(respuesta, r, saber)
    de_verdad = _hacer(op, a, b, saber)
    r["de_verdad"] = de_verdad
    r["correcta"] = de_verdad == respuesta
    r["valor"] = "no" if not r["razonable"] else ("si" if r["correcta"] else "si, pero mal: es %d" % de_verdad)
    return r


def _leer_cuenta(texto, patron):
    t = " ".join(texto.lower().strip().rstrip("?").split())
    m = patron.match(t)
    if not m:
        return None
    g = list(m.groups())
    return [int(g[0]), _OP_ESTIMAR[g[1]], int(g[2])] + [int(x) for x in g[3:]]


def _lineas_estimacion(r):
    L = ["  1. REDONDEO cada numero (N.2):"]
    for n, sitio, v in r["redondeos"]:
        L.append("        %d a la %s -> %d" % (n, sitio, v))
    L.append("  2. LA CUENTA FACIL: %s = %d" % (r["facil"], r["estimacion"]))
    L.append("  3. LA BANDA: %s." % r["por_que_banda"])
    L.append("        la cuenta de verdad tiene que estar entre %d y %d%s" % (
        r["desde"], r["hasta"], "  (la banda sigue, pero mi lista acaba en mil)" if r.get("tope") else ""))
    return L


def explicar_estimar(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    c = _leer_cuenta(texto, _CUENTA_ESTIMAR)
    if c is None:
        return "NO ENTIENDO ESTO: dame una cuenta.\n   se escribe asi:  estimar: 38 + 47"
    a, op, b = c
    r = decidir_estimar(a, op, b, saber)
    L = ["PREGUNTA (E.6): cuanto da MAS O MENOS %d %s %d?  (3.OA.D.8: estimar redondeando)" % (a, op, b), ""]
    if r["conclusion"] != "hecho":
        etiqueta = {"todavia_no": "TODAVIA NO", "imposible": "NO SE PUEDE", "no_hace_falta": "NO HACE FALTA"}[r["conclusion"]]
        return "\n".join(L + ["  %s: %s" % (etiqueta, r["porque"]), "", "RESULTADO: %s" % r["conclusion"]])
    L.extend(_lineas_estimacion(r))
    L += ["", "RESULTADO: cerca de %d" % r["estimacion"]]
    return "\n".join(L)


def explicar_razonable(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    c = _leer_cuenta(texto, _CUENTA_RAZONABLE)
    if c is None:
        return "NO ENTIENDO ESTO: dame una cuenta con su respuesta.\n   se escribe asi:  razonable: 38 + 47 = 75"
    a, op, b, resp = c
    r = decidir_razonable(a, op, b, resp, saber)
    L = ["PREGUNTA (E.6): es RAZONABLE decir que %d %s %d = %d?  (3.OA.D.8)" % (a, op, b, resp), ""]
    if r["conclusion"] != "hecho":
        etiqueta = {"todavia_no": "TODAVIA NO", "imposible": "NO SE PUEDE", "no_hace_falta": "NO HACE FALTA"}[r["conclusion"]]
        return "\n".join(L + ["  %s: %s" % (etiqueta, r["porque"]), "", "RESULTADO: %s" % r["conclusion"]])
    L.extend(_lineas_estimacion(r))
    if r["razonable"]:
        L.append("  4. %d cae DENTRO de la banda: es RAZONABLE." % resp)
    elif decir(resp, saber) is None:
        L.append("  4. %d pasa de mil, y la banda acaba en %d: NO es razonable, seguro que esta mal." % (resp, r["hasta"]))
    else:
        L.append("  4. %d cae FUERA de la banda (%d a %d): NO es razonable, seguro que esta mal." % (resp, r["desde"], r["hasta"]))
    L.append("")
    L.append("  5. Y LA CUENTA DE VERDAD (razonable no es lo mismo que correcta): %d %s %d = %d"
             % (a, op, b, r["de_verdad"]))
    if r["razonable"] and not r["correcta"]:
        L.append("     OJO: %d era razonable, pero NO es la buena.  La estimacion caza los errores grandes,"
                 " no los pequenos." % resp)
    elif r["correcta"]:
        L.append("     y %d es la buena." % resp)
    L += ["", "RESULTADO: %s" % r["valor"]]
    return "\n".join(L)
