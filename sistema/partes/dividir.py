# -*- coding: utf-8 -*-
"""
Euclides - DIVIDIR: REPARTIR Y AGRUPAR (paso M.3 del plan pedagogico, 5 oct 2026).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

NCETM 2.6: agrupar (cuantos grupos de d salen?) y repartir (cuantos le tocan a cada uno de d?); las
dos se hallan contando de divisor en divisor; a veces sobra (resto); atajos: las tablas y la mitad;
casos de cero, el mismo y entre uno.  Common Core 3.OA.B.6: dividir es buscar un factor desconocido,
asi que se COMPRUEBA multiplicando.  Aqui se lee, se dibuja y se explica; la cuenta la hacen las
piezas de 'dividir'.
"""

import re

_DIV_SIMBOLO = re.compile(r"^(\d+)\s*[:÷/]\s*(\d+)$")
_DIV_ENTRE = re.compile(r"^(?:repart\w*\s+)?(\d+)\s+entre\s+(\d+)$")
_DIV_GRUPOS = re.compile(r"^(\d+)\s+en\s+grupos\s+de\s+(\d+)$")


def es_division(texto):
    t = " ".join(texto.lower().split())
    return bool(_DIV_SIMBOLO.match(t) or _DIV_ENTRE.match(t) or _DIV_GRUPOS.match(t))


def decidir_dividir(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    t = " ".join(texto.lower().split())
    lectura = "las_dos"
    m = _DIV_SIMBOLO.match(t)
    if not m:
        m = _DIV_ENTRE.match(t)
        lectura = "repartir"
    if not m:
        m = _DIV_GRUPOS.match(t)
        lectura = "agrupar"
    if not m:
        return {"conclusion": "no_entiendo"}
    total, d = int(m.group(1)), int(m.group(2))
    if decir(total, saber) is None or decir(d, saber) is None:
        return {"conclusion": "no_entiendo", "porque": "solo se contar hasta %s" % techo(saber)}
    r = aplicar("dividir", {"total": total, "divisor": d}, saber)
    out = {"total": total, "divisor": d, "lectura": lectura, "aplicado": r}
    if r["conclusion"] != "hecho":
        out.update(conclusion="imposible", porque=r.get("porque"))
        return out
    q, resto = r["valor"], r["resultado"].get("resto", 0)
    # LA COMPROBACION (3.OA.B.6: factor desconocido): cociente x divisor (+ resto) = dividendo
    pm = aplicar("multiplicar", {"a": q, "b": d}, saber)
    total_vuelta = pm.get("valor")
    if resto and total_vuelta is not None:
        total_vuelta = aplicar("sumar", {"a": total_vuelta, "b": resto}, saber).get("valor")
    out.update(conclusion="hecho", valor=q, resto=resto, comprobacion_ok=total_vuelta == total,
               comprobacion="%d x %d%s = %s" % (q, d, " + %d" % resto if resto else "", total_vuelta))
    return out


def _dibujo_grupos(q, d, resto, saber):
    g = "(" + " ".join("o" for _ in levantar_dedos(decir(d, saber), saber) or []) + ")"
    partes = [g for _ in levantar_dedos(decir(q, saber), saber) or []]
    if resto:
        partes.append("sobran: " + " ".join("o" for _ in levantar_dedos(decir(resto, saber), saber) or []))
    return "  ".join(partes)


def _dibujo_reparto(q, d, resto, saber):
    lineas, k = [], "cero"
    cada = " ".join("o" for _ in levantar_dedos(decir(q, saber), saber) or []) or "(nada)"
    while k != decir(d, saber):
        k = siguiente(k, saber)
        lineas.append("        el %d: %s" % (leer(k, saber), cada))
    if resto:
        lineas.append("        sobran: %s" % " ".join("o" for _ in levantar_dedos(decir(resto, saber), saber) or []))
    return lineas


def explicar_dividir(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_dividir(texto, saber)
    if r["conclusion"] == "no_entiendo":
        return ("NO ENTIENDO ESTO: %s\n   se escribe asi:  12 entre 3   (repartir)   o   12 en grupos de 3   "
                "(agrupar)   o   12 : 3" % r.get("porque", "dime cuanto hay y entre cuantos (o de cuanto el grupo)"))
    t, d = r["total"], r["divisor"]
    L = ["PREGUNTA (M.3): %d : %d   (%d es el DIVIDENDO, %d el DIVISOR)" % (t, d, t, d), ""]
    lect = {"repartir": ["REPARTIR %d entre %d: cuantos le tocan a cada uno?" % (t, d)],
            "agrupar": ["AGRUPAR %d en grupos de %d: cuantos grupos salen?" % (t, d)],
            "las_dos": ["se puede leer de DOS maneras (NCETM 2.6):",
                        "  REPARTIR %d entre %d: cuantos le tocan a cada uno?" % (t, d),
                        "  AGRUPAR %d en grupos de %d: cuantos grupos salen?" % (t, d),
                        "  (las dos dan el mismo numero: se cuentan igual, de %d en %d)" % (d, d)]}[r["lectura"]]
    L.append("  1. LEER: " + lect[0])
    L.extend("           " + x for x in lect[1:])
    L.append("")
    ap = r["aplicado"]
    L.append("  2. PRUEBO TODO LO QUE SE PARA DIVIDIR:")
    for f in ap["candidatos"]:
        if f.get("descartado"):
            L.append("        [no]  %-42s porque %s" % (f["nombre"], f["descartado"]))
        elif f.get("no_salio"):
            L.append("        [no]  %-42s no salio: %s" % (f["nombre"], f["no_salio"]))
        elif f["id"] == ap.get("pieza", {}).get("id"):
            L.append("        [SI]  %-42s <- el mas corto que encaja: ESTE" % f["nombre"])
        else:
            L.append("        [si]  %-42s tambien servia (es mas largo)" % f["nombre"])
    L.append("")
    if r["conclusion"] != "hecho":
        L.append("  NO SE PUEDE: %s" % r.get("porque"))
        L.append("")
        L.append("RESULTADO: no_se_puede")
        return "\n".join(L)
    q, resto = r["valor"], r["resto"]
    L.append("  3. %s" % ap["resultado"]["cuenta"].replace("; ", "\n     "))
    if levantar_dedos(decir(q, saber), saber) is not None and levantar_dedos(decir(d, saber), saber) is not None:
        L.append("")
        if r["lectura"] in ("agrupar", "las_dos"):
            L.append("     agrupando:  %s" % (_dibujo_grupos(q, d, resto, saber) or "(ningun grupo)"))
        if r["lectura"] in ("repartir", "las_dos"):
            L.append("     repartiendo (una ronda = uno para cada uno):")
            L.extend(_dibujo_reparto(q, d, resto, saber))
    L.append("")
    L.append("  4. COMPRUEBO multiplicando (dividir es buscar el factor que falta): %s ... %s"
             % (r["comprobacion"], "SI" if r["comprobacion_ok"] else "NO"))
    L.append("")
    L.append("  %d : %d = %d%s   (%d es el COCIENTE%s)" % (t, d, q, (", y sobra 1" if resto == 1 else ", y sobran %d" % resto) if resto else "",
                                                          q, "; %d el RESTO" % resto if resto else ""))
    if resto:                                          # M.8 (NCETM 2.12): el resto, en la ecuacion
        L.append("  en una ecuacion: %d = %d x %d + %d" % (t, q, d, resto))
        L.append("  el RESTO (%d) es MENOR que el divisor (%d): si sobraran %d o mas, cabria otro grupo (NCETM 2.12)."
                 % (resto, d, d))
    else:
        L.append("  sin resto: %d es MULTIPLO de %d (contando de %d en %d se llega justo)." % (t, d, d, d))
    L.append("")
    L.append("RESULTADO: %d%s" % (q, " resto %d" % resto if resto else ""))
    return "\n".join(L)


# ---------------------------------------------------------------- comprobar: 17 : 5 = 3 resto 2   (M.8)

_ORDEN_COMPROBAR_DIV = re.compile(r"^comprobar:?\s*(\d+)\s*[:/]\s*(\d+)\s*=\s*(\d+)(?:\s*(?:resto|r|y sobran?)\s*(\d+))?$")


def es_comprobar_division(texto):
    return bool(_ORDEN_COMPROBAR_DIV.match(" ".join(texto.lower().split())))


def decidir_comprobar_division(t, d, q, resto, saber=None):
    """NCETM 2.12: una respuesta de division esta bien si cociente x divisor + resto = dividendo Y el
    resto es MENOR que el divisor."""
    if saber is None:
        saber = cargar_conocimiento()
    m = aplicar("multiplicar", {"a": q, "b": d}, saber)
    if m["conclusion"] != "hecho":
        return {"conclusion": "no_se", "porque": m.get("porque")}
    vuelta = aplicar("sumar", {"a": m["valor"], "b": resto}, saber)["valor"] if resto else m["valor"]
    cuadra = vuelta == t
    menor = resto != d and not viene_despues(decir(resto, saber), decir(d, saber), saber)
    r = {"conclusion": "hecho", "producto": m["valor"], "vuelta": vuelta, "cuadra": cuadra, "menor": menor,
         "valor": "si" if cuadra and menor else "no"}
    if not (cuadra and menor):
        buena = aplicar("dividir", {"total": t, "divisor": d}, saber)
        if buena["conclusion"] == "hecho":
            r["buena"] = (buena["valor"], buena["resultado"].get("resto", 0))
    return r


def explicar_comprobar_division(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    m = _ORDEN_COMPROBAR_DIV.match(" ".join(texto.lower().split()))
    t, d, q = int(m.group(1)), int(m.group(2)), int(m.group(3))
    resto = int(m.group(4)) if m.group(4) else 0
    L = ["PREGUNTA (M.8): esta bien %d : %d = %d%s?  (NCETM 2.12)" % (t, d, q, " resto %d" % resto if resto else ""), ""]
    if d == 0:
        return "\n".join(L + ["  NO SE PUEDE: no se divide entre cero.", "", "RESULTADO: no_se_puede"])
    r = decidir_comprobar_division(t, d, q, resto, saber)
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["  %s" % r.get("porque"), "", "RESULTADO: no_se"])
    L.append("  1. LA VUELTA: %d x %d%s = %d  ... %s" % (q, d, " + %d" % resto if resto else "", r["vuelta"],
                                                    "cuadra con %d" % t if r["cuadra"] else "NO es %d" % t))
    L.append("  2. EL RESTO (%d) es menor que el divisor (%d)? ... %s" % (resto, d, "SI" if r["menor"] else
             "NO: con %d sobrando cabe OTRO grupo de %d" % (resto, d)))
    if r["valor"] == "no" and "buena" in r:
        L.append("")
        L.append("  la buena: %d : %d = %d%s" % (t, d, r["buena"][0], " resto %d" % r["buena"][1] if r["buena"][1] else ""))
    L += ["", "RESULTADO: %s" % r["valor"]]
    return "\n".join(L)


def explicar_division_corta(texto, saber=None):
    """'corta: 72 : 3': la division corta (NCETM 2.15) aunque haya otro camino mas corto."""
    if saber is None:
        saber = cargar_conocimiento()
    m = _DIV_SIMBOLO.match(" ".join(texto.lower().split()))
    if not m:
        return "NO ENTIENDO ESTO: se escribe asi:  corta: 72 : 3"
    t, d = int(m.group(1)), int(m.group(2))
    L = ["PREGUNTA (M.11): %d : %d con la DIVISION CORTA  (NCETM 2.15; 4.NBT.B.6)" % (t, d), ""]
    r = aplicar("division_corta", {"total": t, "divisor": d}, saber)
    if r["conclusion"] != "hecho":
        porque = r.get("porque") or (r["candidatos"][0].get("descartado") if r.get("candidatos") else "")
        return "\n".join(L + ["  NO SE PUEDE: %s" % porque, "", "RESULTADO: no_se_puede"])
    L.append("     %s" % r["resultado"]["cuenta"].replace("; ", "\n     "))
    L.append("")
    L.append("  LA VUELTA: %s ... %s" % (r["resultado"]["vuelta"], "SI" if r["resultado"]["vuelta_ok"] else "NO"))
    resto = r["resultado"].get("resto", 0)
    L += ["", "RESULTADO: %d%s" % (r["valor"], " resto %d" % resto if resto else "")]
    return "\n".join(L)
