# -*- coding: utf-8 -*-
"""
Euclides - USAR LA EQUIVALENCIA PARA CALCULAR (paso M.12 del plan pedagogico, 7 oct 2026; 5.o).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

NCETM 2.18 (Using equivalence to calculate):
  punto 1: si un factor sube multiplicativamente y el otro baja de la misma manera, el PRODUCTO no cambia
           (25 x 16 = 50 x 8 = 100 x 4);
  punto 2: si el dividendo y el divisor cambian los dos DE LA MISMA MANERA, el COCIENTE no cambia
           (165 : 5 = 330 : 10;  180 : 20 = 18 : 2).
Las cuentas las hacen las piezas multiplicar_escalando, dividir_escalando, igual_escalando y
balanza_escalando.  Aqui solo esta la orden 'equivalente:' y el enganche de la balanza con x y :.
"""

import re

_EQ_ORDEN = re.compile(r"^equivalente:?\s*(\d+)\s*([x*×:÷/])\s*(\d+)$")


def es_orden_equivalente(texto):
    return texto.strip().lower().startswith("equivalente")


def _eq_hoja(e):
    """Una hoja del arbol de letra.py: un numero o la letra (el hueco)."""
    if e[0] == "n":
        return e[1]
    if e[0] == "letra":
        return "?"
    return None


def _eq_balanza_por(izq, der, saber):
    """'24 x 5 = 12 x ?' o '180 : 20 = 18 : ?': pregunta a las piezas de 'balanza_por'.  Devuelve el
    resultado de aplicar() si salio, o None (y entonces letra.py calcula como siempre)."""
    lados = []
    for e in (izq, der):
        if e[0] != "op" or e[1] not in ("x", ":"):
            return None
        a, b = _eq_hoja(e[2]), _eq_hoja(e[3])
        if a is None or b is None:
            return None
        lados.append({"a": a, "op": e[1], "b": b})
    if lados[0]["op"] != lados[1]["op"]:
        return None
    con = [l for l in lados if "?" in (l["a"], l["b"])]
    if len(con) != 1 or (con[0]["a"] == "?" and con[0]["b"] == "?"):
        return None
    completo = [l for l in lados if l is not con[0]][0]
    r = aplicar("balanza_por", {"completo": completo, "con_hueco": con[0]}, saber)
    return r if r["conclusion"] == "hecho" else None


def explicar_orden_equivalente(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    t = " ".join(texto.strip().lower().split())
    m = _EQ_ORDEN.match(t)
    if not m:
        return ("NO ENTIENDO ESTO: dame una multiplicacion o una division.\n"
                "   se escribe asi:  equivalente: 25 x 16     o     equivalente: 375 : 25")
    a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
    por = op in "x*×"
    for n in (a, b):
        if decir(n, saber) is None:
            return "NO ENTIENDO ESTO: solo se llegar hasta %s" % techo(saber)
    signo = "x" if por else ":"
    L = ["PREGUNTA (M.12): %d %s %d usando la EQUIVALENCIA  (NCETM 2.18)" % (a, signo, b), ""]
    if por:
        L += ["  LA REGLA (punto 1): si un factor sube K veces y el otro baja K veces, el PRODUCTO no cambia.",
              "  Lo facil: doblar el factor que acaba en 5 (el 5 se vuelve 0) y partir el otro por la mitad."]
        pieza, situacion = "multiplicar_escalando", {"a": a, "b": b}
    else:
        L += ["  LA REGLA (punto 2): si el dividendo y el divisor cambian los dos IGUAL, el COCIENTE no cambia.",
              "  Lo facil: si el divisor acaba en 5, doblar los dos; si los dos acaban en 0, quitar un cero a los dos."]
        pieza, situacion = "dividir_escalando", {"total": a, "divisor": b}
    L.append("")
    r = aplicar(pieza, situacion, saber)
    if r["conclusion"] != "hecho":
        fila = r["candidatos"][0] if r.get("candidatos") else {}
        porque = fila.get("descartado") or fila.get("no_salio") or r.get("porque") or r["conclusion"]
        L += ["  NO ENCAJA: %s." % porque,
              "  (Se hace de otra manera: '%d %s %d'.)" % (a, signo, b), "", "RESULTADO: no_encaja"]
        return "\n".join(L)
    res = r["resultado"]
    L.append("  LA CADENA (cada paso vale lo mismo que el anterior):")
    L.append("        %s" % "\n      = ".join(res["cadena"]))
    L.append("")
    L.append("  %s" % res["cuenta"])
    # LA VUELTA, con la operacion contraria (sin la equivalencia): tiene que salir el de antes
    if por:
        w = aplicar("dividir", {"total": r["valor"], "divisor": b}, saber)
        ok = w["conclusion"] == "hecho" and w["valor"] == a and not w["resultado"].get("resto")
        L.append("  COMPRUEBO dividiendo: %d : %d = %s ... %s" % (r["valor"], b, w.get("valor"), "SI" if ok else "NO"))
    else:
        w = aplicar("multiplicar", {"a": r["valor"], "b": b}, saber)
        ok = w["conclusion"] == "hecho" and w["valor"] == a
        L.append("  COMPRUEBO multiplicando: %d x %d = %s ... %s" % (r["valor"], b, w.get("valor"), "SI" if ok else "NO"))
    L += ["", "RESULTADO: %d" % r["valor"] if ok else "RESULTADO: no_cuadra"]
    return "\n".join(L)
