# -*- coding: utf-8 -*-
"""
Euclides - MULTIPLICAR = GRUPOS IGUALES (paso M.1 del plan pedagogico, 5 oct 2026).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

Common Core 3.OA.A.1: '5 x 7 es el total de objetos en 5 grupos de 7'.  NCETM 2.2: los grupos pueden
ser iguales o desiguales; hay que decir cuantos grupos y cuantos en cada uno; los iguales se escriben
como suma repetida y como multiplicacion; tambien con grupos de cero y de uno.
Aqui solo se LEE, se DIBUJA y se explica; la cuenta la hacen las piezas de 'multiplicar'.
"""

import re

_POR = re.compile(r"^(\d+)\s*[x×*]\s*(\d+)$")
_GRUPOS = re.compile(r"^(\d+)\s+grupos?\s+de\s+(\d+)$")
_DESIGUALES = re.compile(r"^grupos\s+de\s+([\d,\sy]+)$")


def es_multiplicacion(texto):
    t = " ".join(texto.lower().split())
    return bool(_POR.match(t) or _GRUPOS.match(t) or _DESIGUALES.match(t))


def decidir_multiplicar(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    t = " ".join(texto.lower().split())
    m = _DESIGUALES.match(t)
    if m:
        nums = [int(x) for x in re.findall(r"\d+", m.group(1))]
        if any(decir(n, saber) is None for n in nums) or len(nums) < 2:
            return {"conclusion": "no_entiendo"}
        if all(n == nums[0] for n in nums):
            t = "%d grupos de %d" % (len(nums), nums[0])
        else:
            total, pasos = nums[0], []
            for n in nums[1:]:
                r = aplicar("sumar", {"a": total, "b": n}, saber)
                if r["conclusion"] != "hecho":
                    return {"conclusion": "no_se_puede", "porque": r.get("porque")}
                pasos.append("%d + %d = %d" % (total, n, r["valor"]))
                total = r["valor"]
            return {"conclusion": "desiguales", "grupos": nums, "valor": total, "pasos": pasos}
    m = _POR.match(t) or _GRUPOS.match(t)
    if not m:
        return {"conclusion": "no_entiendo"}
    a, b = int(m.group(1)), int(m.group(2))
    if decir(a, saber) is None or decir(b, saber) is None:
        return {"conclusion": "no_entiendo", "porque": "solo se contar hasta mil"}
    r = aplicar("multiplicar", {"a": a, "b": b}, saber)
    out = {"a": a, "b": b, "aplicado": r}
    if r["conclusion"] != "hecho":
        out.update(conclusion="no_se_puede", porque="me paso de mil (mi lista de contar llega a mil)")
        return out
    out.update(conclusion="hecho", valor=r["valor"])
    return out


def _suma_repetida(a, b, saber):
    trozos, marca = [], "cero"
    while marca != decir(a, saber):
        trozos.append(str(b))
        marca = siguiente(marca, saber)
    return " + ".join(trozos)


def explicar_multiplicar(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_multiplicar(texto, saber)
    if r["conclusion"] == "no_entiendo":
        return ("NO ENTIENDO ESTO: %s\n   se escribe asi:  3 x 4    (o  3 grupos de 4,  o  grupos de 2, 3 y 4)"
                % r.get("porque", "dime cuantos grupos y cuantos en cada uno"))
    if r["conclusion"] == "desiguales":
        g = r["grupos"]
        return "\n".join([
            "PREGUNTA (M.1): grupos de %s" % ", ".join(str(x) for x in g), "",
            "  LOS GRUPOS NO SON IGUALES (NCETM 2.2: los grupos pueden ser iguales o desiguales).",
            "  Con grupos desiguales NO se escribe una multiplicacion: es una suma.",
            "    %s" % "; ".join(r["pasos"]), "",
            "  %s = %d" % (" + ".join(str(x) for x in g), r["valor"]), "",
            "RESULTADO: %d" % r["valor"]])
    a, b = r["a"], r["b"]
    L = ["PREGUNTA (M.1): %d x %d" % (a, b), "",
         "  1. LEER: %d x %d son %d %s de %d  (el %d dice CUANTOS GRUPOS; el %d, CUANTOS HAY EN CADA UNO)"
         % (a, b, a, "grupo" if a == 1 else "grupos", b, a, b)]
    if b == 0:
        L.append("     (grupos de CERO: cada grupo esta vacio)")
    if a == 0:
        L.append("     (CERO grupos: no hay nada)")
    if levantar_dedos(decir(a, saber), saber) is not None and levantar_dedos(decir(b, saber), saber) is not None:
        grupo = "(" + " ".join("o" for _ in levantar_dedos(decir(b, saber), saber) or []) + ")"
        dibujo = "  ".join(grupo for _ in levantar_dedos(decir(a, saber), saber) or [])
        L.append("")
        L.append("  2. LO DIBUJO:  %s" % (dibujo or "(ningun grupo)"))
    L.append("")
    if levantar_dedos(decir(a, saber), saber) is not None:
        suma = _suma_repetida(a, b, saber) or "0"
    else:
        suma = "%d + %d + ... + %d   (el %d, %d veces)" % (b, b, b, b, a)
    L.append("  3. LA SUMA REPETIDA (NCETM 2.2): %s" % suma)
    ap = r["aplicado"]
    if r["conclusion"] != "hecho":
        L.append("")
        L.append("  NO SE PUEDE: %s" % r["porque"])
        L.append("")
        L.append("RESULTADO: no_se_puede")
        return "\n".join(L)
    pasos = ap["resultado"].get("pasos") or []
    L.append("     con %s:" % ap["resultado"]["metodo"])
    if len(pasos) > 12:
        L.extend("        %s" % p for p in pasos[:5])
        L.append("        ... (%d sumas mas)" % len(pasos[5:]))
        L.extend("        %s" % p for p in pasos[-2:])
    else:
        L.append("        %s" % ap["resultado"]["cuenta"].replace("; ", "\n        "))
    L.append("")
    L.append("  4. LA MULTIPLICACION: %d x %d = %d" % (a, b, r["valor"]))
    L.append("")
    L.append("RESULTADO: %d" % r["valor"])
    return "\n".join(L)
