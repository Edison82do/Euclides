# -*- coding: utf-8 -*-
"""
Euclides - USAR LA EQUIVALENCIA Y LA COMPENSACION PARA CALCULAR, con + y - (paso P.7, 7 oct 2026; 5.o).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

NCETM 1.29 (Using equivalence and the compensation property to calculate), los seis puntos:
  1 la misma suma (uno sube, el otro baja lo mismo);  2 cambiar un sumando (la suma cambia lo mismo);
  3 la misma diferencia (los dos cambian lo mismo);   4 cambiar el minuendo (la diferencia cambia lo mismo);
  5 cambiar el sustraendo (la diferencia cambia AL REVES);  6 equilibrar ecuaciones.
Las cuentas las hacen las piezas (sumar_misma_suma, restar_misma_diferencia, ..., derivar_compensando,
igual_compensando, balanza_misma_diferencia).  Aqui solo se LEEN las ordenes y se explica:
    si 600 - 200 = 400: 600 - 201 = ?        (derivar de un hecho que se sabe)
    equivalente: 1000 - 397                  (la cadena: 1000 - 397 = 1003 - 400 = 603; tambien con decimales)
"""

import re

_CMP_N = r"(\d+)"
_CMP_SI = re.compile(r"^si\s+" + _CMP_N + r"\s*([+\-])\s*" + _CMP_N + r"\s*=\s*" + _CMP_N
                     + r"\s*[:,;]?\s*(?:entonces\s+)?" + _CMP_N + r"\s*([+\-])\s*" + _CMP_N + r"\s*(?:=\s*\?)?$")
_CMP_EQ = re.compile(r"^equivalente:?\s*(\d+(?:[.,]\d+)?)\s*([+\-])\s*(\d+(?:[.,]\d+)?)$")


def _cmp_limpio(texto):
    return " ".join(texto.replace("−", "-").lower().strip().split())


def es_orden_derivar(texto):
    return bool(re.match(r"^si\s+\d", _cmp_limpio(texto)))


def es_equivalente_suma_resta(texto):
    return bool(_CMP_EQ.match(_cmp_limpio(texto)))


def _cmp_tabla(r):
    L = []
    elegida = r.get("pieza", {}).get("id")
    for f in r["candidatos"]:
        if f.get("descartado"):
            L.append("    [no]  %-40s porque %s" % (f["nombre"], f["descartado"]))
        elif f.get("no_salio"):
            L.append("    [no]  %-40s encajaba, pero NO SALIO: %s" % (f["nombre"], f["no_salio"]))
        elif f["id"] == elegida:
            L.append("    [SI]  %-40s <- el mas corto que encaja: ESTE" % f["nombre"])
        else:
            L.append("    [si]  %-40s tambien servia (es mas largo)" % f["nombre"])
    return L


# ------------------------------------------------------------------ derivar de un hecho (puntos 2, 4, 5)

def explicar_orden_derivar(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    m = _CMP_SI.match(_cmp_limpio(texto))
    if not m:
        return ("NO ENTIENDO ESTO: dame una cuenta que se sabe y otra que se parece.\n"
                "   se escribe asi:  si 600 - 200 = 400: 600 - 201 = ?      o   si 250 + 250 = 500: 251 + 250 = ?")
    a, op, b, r0, c, op2, d = (m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6), m.group(7))
    a, b, r0, c, d = (int(x) for x in (a, b, r0, c, d))
    for x in (a, b, r0, c, d):
        if decir(x, saber) is None:
            return "NO ENTIENDO ESTO: solo se llegar hasta %s" % techo(saber)
    hecho = {"a": a, "op": op, "b": b, "r": r0}
    nuevo = {"a": c, "op": op2, "b": d}
    L = ["PREGUNTA (P.7): si %d %s %d = %d, cuanto es %d %s %d?  (NCETM 1.29)" % (a, op, b, r0, c, op2, d), ""]
    # 1. EL HECHO QUE ME DAN: un hecho falso no se usa (nunca contestar con seguridad algo falso)
    if op == "-" and viene_despues(decir(b, saber), decir(a, saber), saber):
        L += ["  EL HECHO NO SE PUEDE: %d - %d quitaria mas de lo que hay." % (a, b), "", "RESULTADO: hecho_falso"]
        return "\n".join(L)
    w = aplicar("sumar" if op == "+" else "restar", {"a": a, "b": b}, saber)
    if w["conclusion"] != "hecho" or w["valor"] != r0:
        L += ["  1. MIRO EL HECHO: %d %s %d = %s, no %d.  EL HECHO NO ES VERDAD: no lo uso."
              % (a, op, b, w.get("valor", "?"), r0), "", "RESULTADO: hecho_falso"]
        return "\n".join(L)
    L.append("  1. MIRO EL HECHO: %d %s %d = %d ... es verdad (%s)." % (a, op, b, r0, w["resultado"]["metodo"]))
    L.append("")
    L.append("  2. PRUEBO TODO LO QUE SE:")
    r = aplicar("derivar", {"hecho": hecho, "nuevo": nuevo}, saber)
    L += _cmp_tabla(r)
    L.append("")
    if r["conclusion"] != "hecho":
        L += ["  NO SE PUEDE: %s" % (r.get("porque") or r["conclusion"]), "", "RESULTADO: no_se_puede"]
        return "\n".join(L)
    res = r["resultado"]
    L.append("  3. %s:" % res["metodo"].upper())
    for linea in res["cuenta"].split("\n"):
        L.append("        %s" % linea)
    v = r["valor"]
    # LA TRAMPA DEL PUNTO 5: creer que si el sustraendo sube, la diferencia tambien sube
    if op == "-" and op2 == "-" and a == c and b != d:
        sube = viene_despues(decir(d, saber), decir(b, saber), saber)
        g, p = (d, b) if sube else (b, d)
        k = aplicar("restar", {"a": g, "b": p}, saber)
        mal = aplicar("sumar" if sube else "restar", {"a": r0, "b": k.get("valor", 0)}, saber) \
            if k["conclusion"] == "hecho" else {"conclusion": "no"}
        if mal["conclusion"] == "hecho" and mal["valor"] != v:
            L.append("")
            L.append("  LA TRAMPA (la que mas cuesta, dice NCETM): %d NO.  El sustraendo %s, pero la diferencia va AL "
                     "REVES: si se quita mas, queda menos; si se quita menos, queda mas." % (mal["valor"], "sube" if sube else "baja"))
    L.append("")
    L.append("  4. COMPRUEBO haciendo la cuenta nueva: %s ... %s" % (res["vuelta"], "SI" if res["vuelta_ok"] else "NO"))
    L += ["", "RESULTADO: %d" % v]
    return "\n".join(L)


# ------------------------------------------------------------------ equivalente: con + y - (puntos 1, 2, 3, 5)

_CMP_PIEZAS = {"+": ("sumar_misma_suma", "sumar_redondeando_y_quitando"),
               "-": ("restar_misma_diferencia", "restar_quitando_de_mas_y_devolviendo")}


def explicar_equivalente_suma_resta(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    m = _CMP_EQ.match(_cmp_limpio(texto))
    if not m:
        return ("NO ENTIENDO ESTO: dame una suma o una resta.\n"
                "   se escribe asi:  equivalente: 4997 + 2456     o     equivalente: 1000 - 397")
    x, op, y = m.group(1).replace(",", "."), m.group(2), m.group(3).replace(",", ".")
    k = _dec_lugares(x, y)
    L = ["PREGUNTA (P.7): %s %s %s usando la COMPENSACION  (NCETM 1.29)" % (x, op, y), ""]
    if viene_despues(decir(k, saber), decir(_DEC_MAX, saber), saber):
        L += ["  TODAVIA NO: con mas de %d cifras detras del punto (D.2 llega a las milesimas)." % _DEC_MAX,
              "", "RESULTADO: todavia_no"]
        return "\n".join(L)
    a, b = _dec_en_pequenas(x, k), _dec_en_pequenas(y, k)
    if decir(a, saber) is None or decir(b, saber) is None:
        L += ["  NO ALCANZA: %s pasa de mi lista (%s de %s)." % (
            "contado en %s" % _DEC_NOMBRE[k][1] if k else "el numero", techo(saber), _DEC_NOMBRE[k][1] if k else "unidades"),
            "", "RESULTADO: no_alcanza"]
        return "\n".join(L)
    if k:
        L.append("  Lo cuento en %s (D.1, D.2): %s = %s, %s = %s.  El redondo sera un ENTERO."
                 % (_DEC_NOMBRE[k][1], x, _dec_cuantas(a, k), y, _dec_cuantas(b, k)))
    if op == "+":
        L += ["  LA REGLA (punto 1): si un sumando sube y el otro baja LO MISMO, la SUMA no cambia.",
              "  (y punto 2: si solo cambia uno, la suma cambia lo mismo: lo que sobra se quita.)"]
    else:
        L += ["  LA REGLA (punto 3): si el minuendo y el sustraendo cambian LO MISMO (hacia el mismo lado),",
              "  la DIFERENCIA no cambia.  (y punto 5: si solo cambia el sustraendo, la diferencia va AL REVES.)"]
    L.append("")
    if op == "-" and viene_despues(decir(b, saber), decir(a, saber), saber):
        L += ["  NO SE PUEDE: se quitaria mas de lo que hay (no hay restas negativas aqui, 5.4).", "",
              "RESULTADO: no_se_puede"]
        return "\n".join(L)
    situacion = {"a": a, "b": b, "ceros": k if k else 2}
    r = None
    porques = []
    for pieza in _CMP_PIEZAS[op]:
        r = aplicar(pieza, situacion, saber)
        if r["conclusion"] == "hecho":
            break
        fila = r["candidatos"][0] if r.get("candidatos") else {}
        porques.append(fila.get("descartado") or fila.get("no_salio") or r.get("porque") or r["conclusion"])
    if r["conclusion"] != "hecho":
        L += ["  NO ENCAJA: %s." % porques[0], "  (Se hace de otra manera: '%s %s %s'.)" % (x, op, y), "",
              "RESULTADO: no_encaja"]
        return "\n".join(L)
    res = r["resultado"]

    def escribe(n):
        return _dec_escribir(n, k)
    cadena = ["%s %s %s" % (escribe(p), o, escribe(q)) for p, o, q in res["cadena"]]
    v = r["valor"]
    L.append("  LA CADENA (cada paso vale lo mismo que el anterior):")
    L.append("        %s" % "\n      = ".join(cadena + [escribe(v)]))
    L.append("")
    L.append("  %s" % res["cuenta"])
    # LA VUELTA, con la operacion contraria y por las columnas
    if op == "+":
        w = aplicar("restar_por_columnas", {"a": v, "b": b}, saber)
        ok = w["conclusion"] == "hecho" and w["valor"] == a
        L.append("  COMPRUEBO restando: %s - %s = %s ... %s" % (escribe(v), y, escribe(w.get("valor", 0)), "SI" if ok else "NO"))
    else:
        w = aplicar("sumar_por_columnas", {"a": v, "b": b}, saber)
        ok = w["conclusion"] == "hecho" and w["valor"] == a
        L.append("  COMPRUEBO sumando: %s + %s = %s ... %s" % (escribe(v), y, escribe(w.get("valor", 0)), "SI" if ok else "NO"))
    L += ["", "RESULTADO: %s" % escribe(v) if ok else "RESULTADO: no_cuadra"]
    return "\n".join(L)


# ------------------------------------------------------------------ la trampa de la balanza con restas (punto 6)

def _cmp_trampa_balanza_resta(completo, con_hueco, saber):
    """74 - 28 = 75 - ?: la respuesta equivocada de compensar COMO EN LA SUMA (el minuendo sube 1, el
    sustraendo baja 1: 27).  Devuelve (numero, porque) o None."""
    if completo.get("op") != "-" or con_hueco.get("op") != "-":
        return None
    if con_hueco["b"] == "?":
        p, q, mover = completo["a"], con_hueco["a"], completo["b"]
    else:
        p, q, mover = completo["b"], con_hueco["b"], completo["a"]
    if p == q:
        return None
    sube = viene_despues(decir(q, saber), decir(p, saber), saber)
    g, m = (q, p) if sube else (p, q)
    d = aplicar("restar", {"a": g, "b": m}, saber)
    if d["conclusion"] != "hecho":
        return None
    mal = aplicar("restar" if sube else "sumar", {"a": mover, "b": d["valor"]}, saber)
    if mal["conclusion"] != "hecho":
        return None
    return mal["valor"], "compensar al reves, como en la SUMA: en la resta los dos se mueven hacia el MISMO lado"
