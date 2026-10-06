# -*- coding: utf-8 -*-
"""
Euclides - EL = : VERDADERO O FALSO (paso E.0 del plan pedagogico, 5 oct 2026).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

Common Core 1.OA.D.7: 'entender el significado del signo igual y decidir si las ecuaciones de suma
y resta son verdaderas o falsas'.  La Progression: el = 'siempre significa ES EL MISMO NUMERO QUE'.
Aqui solo se LEE la frase y se pregunta a las piezas de 'igualdad' (conocimiento/piezas/igual_*.py).
"""

import re

_LADO_OP = re.compile(r"^(\d+)\s*([+\-x*\u00d7:\u00f7/])\s*(\d+)$")
_LADO_N = re.compile(r"^(\d+)$")


def leer_igualdad(texto):
    """'4 + 1 = 5 + 2' -> [{"texto": "4 + 1", "a": 4, "op": "+", "b": 1}, {...}], o None."""
    t = texto.replace("−", "-").lower().strip().rstrip("?").strip()
    if "=" not in t:
        return None
    lados = []
    for trozo in t.split("="):
        x = " ".join(trozo.split())
        m = _LADO_OP.match(x)
        if m:
            op = "x" if m.group(2) in "x*\u00d7" else (":" if m.group(2) in ":\u00f7/" else m.group(2))
            lados.append({"texto": "%s %s %s" % (m.group(1), op, m.group(3)),
                          "a": int(m.group(1)), "op": op, "b": int(m.group(3))})
            continue
        m = _LADO_N.match(x)
        if m:
            lados.append({"texto": m.group(1), "n": int(m.group(1))})
            continue
        return None
    return lados


def decidir_igualdad(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lados = leer_igualdad(texto)
    if not lados:
        return {"conclusion": "no_entiendo"}
    for l in lados:
        for k in ("a", "b", "n"):
            if k in l and decir(l[k], saber) is None:
                return {"conclusion": "no_entiendo", "porque": "solo se contar hasta %s" % techo(saber)}
    r = aplicar("igualdad", {"lados": lados}, saber)
    r["lados"] = lados
    return r


def explicar_igualdad(texto, saber=None):
    r = decidir_igualdad(texto, saber)
    if r["conclusion"] == "no_entiendo":
        return ("NO ENTIENDO ESTO: dame una igualdad con sumas o restas.\n"
                "   se escribe asi:  verdad: 4 + 1 = 5 + 2      (o  verdad: 10 = 8 + 2)")
    frase = " = ".join(l["texto"] for l in r["lados"])
    L = ["PREGUNTA: %s   es VERDADERO o FALSO?" % frase,
         "  (el = no dice 'da': dice 'ES EL MISMO NUMERO QUE'.  Los lados tienen que valer lo mismo)", ""]
    elegida = r.get("pieza", {}).get("id")
    for f in r["candidatos"]:
        if f.get("descartado"):
            L.append("    [no]  %-34s porque %s" % (f["nombre"], f["descartado"]))
        elif f.get("no_salio"):
            L.append("    [no]  %-34s encajaba, pero NO SALIO: %s" % (f["nombre"], f["no_salio"]))
        elif f["id"] == elegida:
            L.append("    [SI]  %-34s <- el mas corto que encaja: ESTE" % f["nombre"])
        else:
            L.append("    [si]  %-34s tambien servia (es mas largo)" % f["nombre"])
    L.append("")
    if r["conclusion"] != "hecho":
        L.append("  NO SE PUEDE DECIR: %s" % r.get("porque", r["conclusion"]))
        L.append("")
        L.append("RESULTADO: no_se_puede")
        return "\n".join(L)
    L.append("  POR QUE:")
    for linea in r["resultado"]["cuenta"].split("\n"):
        L.append("    " + linea)
    L.append("")
    L.append("RESULTADO: %s" % r["valor"].upper())
    return "\n".join(L)
