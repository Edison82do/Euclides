# -*- coding: utf-8 -*-
"""
Euclides - EL DINERO: PESOS Y CENTAVOS (paso D.3 del plan pedagogico, 7 oct 2026; 4.o).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

NCETM 1.25 (Addition and subtraction: money); Common Core 4.MD.A.2.  Un centavo es la CENTESIMA parte de
un peso: el dinero se escribe con centesimas (D.2).  Las cuentas se hacen en centavos (como cosas) o en
columnas; el cambio se cuenta HACIA ADELANTE (la diferencia, P.6).  (NCETM usa libras y peniques; aqui,
pesos y centavos.)
"""

import re

_PRECIO = r"\$?\s*(\d+(?:[.,]\d+)?)"
_ORDEN_DINERO = re.compile(r"^dinero:?\s*" + _PRECIO + r"$")
_ORDEN_PRECIOS = re.compile(r"^(?:calcular:?\s*)?\$\s*(\d+(?:[.,]\d+)?)\s*([+\-])\s*\$?\s*(\d+(?:[.,]\d+)?)$")
_ORDEN_CAMBIO = re.compile(r"^cambio:?\s*(?:pago|paga|con)\s+" + _PRECIO + r"\s+(?:por|para|y cuesta|y cuestan)\s+(.+)$")


def _din_limpio(texto):
    return " ".join(texto.lower().strip().rstrip("?").split())


def es_orden_dinero(texto):
    t = _din_limpio(texto)
    return bool(_ORDEN_DINERO.match(t) or _ORDEN_PRECIOS.match(t) or _ORDEN_CAMBIO.match(t))


def _centavos(precio):
    """'3.45' -> 345;  '3' -> 300;  '3.5' -> 350 (se LEEN las cifras y se completa con ceros)."""
    return _dec_en_pequenas(precio.replace(",", "."), 2)


def _pesos(c):
    """345 -> '$3.45' (siempre con dos cifras de centavos, como se escribe el dinero)."""
    s = str(c)
    while len(s) < 3:
        s = "0" + s
    return "$%s.%s" % (s[:-2], s[-2:])


def _din_problema(*precios):
    for p in precios:
        if len(_dec_leer(p.replace(",", "."))[1]) > 2:
            return "los centavos se escriben con DOS cifras: %s no es un precio" % p
        if decir(_centavos(p), cargar_conocimiento()) is None:
            return "%s en centavos se sale de mi lista" % p
    return None


# ---------------------------------------------------------------- dinero: $3.45

def explicar_dinero(precio, saber):
    p = _din_problema(precio)
    L = ["PREGUNTA (D.3): que es %s?  (NCETM 1.25: un centavo es la centesima parte de un peso)"
         % ("$%s" % precio if p else _pesos(_centavos(precio))), ""]
    if p:
        return "\n".join(L + ["  NO ENTIENDO: %s" % p, "", "RESULTADO: no_entiendo"])
    c = _centavos(precio)
    ci = cifras_de(c)
    pesos, cent = escribir_cifras(ci[2:]), escribir_cifras(ci[:2])
    L.append("  %d %s y %d %s  (lo de detras del punto son CENTESIMAS de peso: centavos)" % (
        pesos, "peso" if pesos == 1 else "pesos", cent, "centavo" if cent == 1 else "centavos"))
    L.append("  cada peso son 100 centavos: %s son %d centavos" % (_pesos(c), c))
    L += ["", "RESULTADO: %d centavos" % c]
    return "\n".join(L)


# ---------------------------------------------------------------- $2.99 + $1.50

def explicar_precios(x, signo, y, saber):
    p = _din_problema(x, y)
    L = ["PREGUNTA (D.3): %s %s %s  (NCETM 1.25)" % ("$%s" % x if p else _pesos(_centavos(x)), signo,
                                                   "$%s" % y if p else _pesos(_centavos(y))), ""]
    if p:
        return "\n".join(L + ["  NO ENTIENDO: %s" % p, "", "RESULTADO: no_entiendo"])
    cx, cy = _centavos(x), _centavos(y)
    r = decidir_cuenta_decimal(_dec_escribir(cx, 2) if cx else "0", signo, _dec_escribir(cy, 2) if cy else "0", saber)
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["  NO SE PUEDE: %s" % r.get("porque"), "", "RESULTADO: %s" % r["conclusion"]])
    total = _centavos(r["valor"])
    L.append("  1. EN CENTAVOS (como cosas): %d %s %d = %d centavos" % (cx, signo, cy, total))
    L.append("  2. EN COLUMNAS (D.2):")
    for c in r["columnas"]:
        c = c.replace("decimas hacen una unidad", "decenas de centavos hacen un peso").replace("unidades:", "pesos:")
        L.append("        %s" % c.replace("centesimas", "centavos").replace("decimas", "decenas de centavos"))
    # NCETM 1.25, punto 2: compensar los precios que acaban en .99 / .95
    if signo == "+":
        for a, b in ((cx, cy), (cy, cx)):
            u = cifras_de(a)
            if len(u) >= 2 and u[1] == 9 and u[0] in (5, 9):
                falta = leer(contar_hasta(decir(u[0], saber), "diez", saber), saber)
                redondo = aplicar("sumar", {"a": a, "b": falta}, saber)["valor"]
                con = aplicar("sumar", {"a": redondo, "b": b}, saber)["valor"]
                quita = aplicar("restar", {"a": con, "b": falta}, saber)["valor"]
                L.append("  3. COMPENSANDO (NCETM 1.25, punto 2): %s es %s menos que %s; %s + %s = %s, y le "
                         "quito %s: %s ... %s" % (_pesos(a), "1 centavo" if falta == 1 else "%d centavos" % falta,
                                                  _pesos(redondo), _pesos(redondo), _pesos(b), _pesos(con),
                                                  "ese centavo" if falta == 1 else "esos %d centavos" % falta,
                                                  _pesos(quita), "lo mismo" if quita == total else "NO CUADRA"))
                break
    L += ["", "RESULTADO: %s" % _pesos(total)]
    return "\n".join(L)


# ---------------------------------------------------------------- cambio: pago $10 por $6.35

def decidir_cambio(pago, precios, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    p = _din_problema(pago, *precios)
    if p:
        return {"conclusion": "no_entiendo", "porque": p}
    partes = [_centavos(x) for x in precios]
    total = partes[0]
    for x in partes[1:]:
        total = aplicar("sumar", {"a": total, "b": x}, saber)["valor"]
    paga = _centavos(pago)
    r = {"partes": partes, "total": total, "paga": paga}
    if total != paga and viene_despues(decir(total, saber), decir(paga, saber), saber):
        r.update(conclusion="no_alcanza", porque="cuesta %s y se paga %s: no alcanza" % (_pesos(total), _pesos(paga)))
        return r
    # CONTAR HACIA ADELANTE (NCETM 1.25, punto 3): hasta la decena de centavos, hasta el peso, hasta lo pagado
    saltos, v = [], total
    for hasta_sitio in (1, 2):
        ci = cifras_de(v)
        while len(ci) <= hasta_sitio:
            ci.append(0)
        if any(ci[:hasta_sitio]):
            tope = leer(siguiente(decir(escribir_cifras(ci[hasta_sitio:]), saber), saber), saber)
            tope = escribir_cifras([0 for _ in range(hasta_sitio)] + cifras_de(tope))
            if tope == paga or not viene_despues(decir(tope, saber), decir(paga, saber), saber):
                d = leer(contar_hasta(decir(v, saber), decir(tope, saber), saber), saber)
                saltos.append((v, tope, d))
                v = tope
    if v != paga:
        d = aplicar("restar", {"a": paga, "b": v}, saber)["valor"]
        saltos.append((v, paga, d))
    cambio = 0
    for _, _, d in saltos:
        cambio = aplicar("sumar", {"a": cambio, "b": d}, saber)["valor"]
    vuelta = aplicar("sumar", {"a": total, "b": cambio}, saber)["valor"]
    r.update(conclusion="hecho", saltos=saltos, cambio=cambio, valor=_pesos(cambio), vuelta_ok=vuelta == paga)
    return r


def explicar_cambio(pago, precios, saber):
    r = decidir_cambio(pago, precios, saber)
    if r["conclusion"] == "no_entiendo":
        return "PREGUNTA (D.3): el cambio\n\n  NO ENTIENDO: %s\n\nRESULTADO: no_entiendo" % r["porque"]
    L = ["PREGUNTA (D.3): se paga %s por %s: cuanto es el CAMBIO?  (NCETM 1.25)" % (
        _pesos(_centavos(pago)), " + ".join(_pesos(_centavos(x)) for x in precios)), ""]
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["  %s" % r["porque"], "", "RESULTADO: %s" % r["conclusion"]])
    if len(precios) > 1:
        L.append("  1. EL TODO Y LAS PARTES (NCETM 1.25, punto 5): lo que se paga es el TODO; las cosas y el cambio")
        L.append("     son las PARTES.  Las cosas juntas: %s = %s" % (" + ".join(_pesos(x) for x in r["partes"]), _pesos(r["total"])))
        L.append("        [ %s | cambio: ? ]  = %s" % (" | ".join(_pesos(x) for x in r["partes"]), _pesos(r["paga"])))
    L.append("  %s. CONTANDO HACIA ADELANTE desde %s hasta %s (como en la tienda; la diferencia, P.6):"
             % ("2" if len(precios) > 1 else "1", _pesos(r["total"]), _pesos(r["paga"])))
    for a, b, d in r["saltos"]:
        L.append("        de %s a %s: %s" % (_pesos(a), _pesos(b), _pesos(d)))
    L.append("     el cambio: %s = %s" % (" + ".join(_pesos(d) for _, _, d in r["saltos"]) or "$0.00", r["valor"]))
    L.append("  LO COMPRUEBO: %s + %s = %s ... %s" % (_pesos(r["total"]), r["valor"], _pesos(r["paga"]),
                                                    "SI" if r["vuelta_ok"] else "NO"))
    L += ["", "RESULTADO: %s" % r["valor"]]
    return "\n".join(L)


# ---------------------------------------------------------------- la puerta

def explicar_orden_dinero(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    t = _din_limpio(texto)
    m = _ORDEN_DINERO.match(t)
    if m:
        return explicar_dinero(m.group(1), saber)
    m = _ORDEN_PRECIOS.match(t)
    if m:
        return explicar_precios(m.group(1), m.group(2), m.group(3), saber)
    m = _ORDEN_CAMBIO.match(t)
    if m:
        precios = [x.strip().lstrip("$").strip() for x in re.split(r"\s*\+\s*|\s+y\s+", m.group(2))]
        if not all(re.match(r"^\d+(?:[.,]\d+)?$", x) for x in precios):
            return "NO ENTIENDO ESTO: se escribe asi:  cambio: pago $10 por $6.35   (o por $3.45 + $6.80)"
        return explicar_cambio(m.group(1), precios, saber)
    return "NO ENTIENDO ESTO: se escribe asi:  dinero: $3.45    $2.99 + $1.50    cambio: pago $10 por $6.35"
