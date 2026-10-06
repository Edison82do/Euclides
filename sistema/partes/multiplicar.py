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
        return {"conclusion": "no_entiendo", "porque": "solo se contar hasta %s" % techo(saber)}
    r = aplicar("multiplicar", {"a": a, "b": b}, saber)
    out = {"a": a, "b": b, "aplicado": r}
    if r["conclusion"] != "hecho":
        out.update(conclusion="no_se_puede", porque="me paso de %s (mi lista de contar llega ahi)" % techo(saber))
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
    L.append("")
    L.append("     PRUEBO TODO LO QUE SE PARA MULTIPLICAR:")
    for f in ap["candidatos"]:
        if f.get("descartado"):
            L.append("        [no]  %-46s porque %s" % (f["nombre"], f["descartado"]))
        elif f.get("no_salio"):
            L.append("        [no]  %-46s no salio: %s" % (f["nombre"], f["no_salio"]))
        elif f["id"] == ap["pieza"]["id"]:
            L.append("        [SI]  %-46s <- el mas corto que encaja: ESTE" % f["nombre"])
        else:
            L.append("        [si]  %-46s tambien servia (es mas largo)" % f["nombre"])
    L.append("     con %s:" % ap["resultado"]["metodo"])
    if len(pasos) > 12:
        L.extend("        %s" % p for p in pasos[:5])
        L.append("        ... (%d sumas mas)" % len(pasos[5:]))
        L.extend("        %s" % p for p in pasos[-2:])
    else:
        L.append("        %s" % ap["resultado"]["cuenta"].replace("; ", "\n        "))
    if ap["pieza"]["id"] == "multiplicacion_corta":          # M.10: el algoritmo, comprobado partiendo
        otra = aplicar("multiplicar_partiendo_por_sitios", {"a": a, "b": b}, saber)
        if otra["conclusion"] == "hecho":
            L.append("     LO COMPRUEBO PARTIENDO POR SITIOS (NCETM 2.14, punto 1):")
            L.append("        %s" % otra["resultado"]["cuenta"].replace("; ", "\n        "))
            L.append("        ... %s" % ("lo mismo: SI" if otra["valor"] == r["valor"] else "NO CUADRA"))
    L.append("")
    L.append("  4. LA MULTIPLICACION: %d x %d = %d   (%d y %d son los FACTORES; %d es el PRODUCTO)"
             % (a, b, r["valor"], a, b, r["valor"]))
    pa = decidir_paridad(a, saber)["valor"]
    pb = decidir_paridad(b, saber)["valor"]
    pp = "par" if "par" in (pa, pb) else "impar"
    L.append("     par o impar (NCETM 2.9): %s x %s -> el producto es %s" % (pa, pb, pp.upper()))
    if a == b:
        L.append("     los dos factores son IGUALES: %d es un NUMERO CUADRADO (%d filas de %d, en cuadrado)"
                 % (r["valor"], a, a))
    L.append("")
    L.append("RESULTADO: %d" % r["valor"])
    return "\n".join(L)


# ------------------------------------------------------------- M.2: las tablas, la mitad

_TABLAS = {"2": "dos", "5": "cinco", "10": "diez"}


def explicar_tabla(texto, saber=None):
    """'tabla del 5': 1 x 5 ... 10 x 5, contando de 5 en 5 (NCETM 2.3 y 2.4: cada producto es el
    anterior mas 5)."""
    if saber is None:
        saber = cargar_conocimiento()
    m = re.match(r"^tabla\s+del\s+(\d+)$", " ".join(texto.lower().split()))
    if not m:
        return "NO ENTIENDO ESTO: se escribe asi:  tabla del 2   (o del 5, o del 10)"
    n = m.group(1)
    if n in _DERIVA:
        return _tabla_doblando(n, saber)
    if n not in _TABLAS:
        return ("PREGUNTA (M.2): tabla del %s\n\n  TODAVIA NO: se las tablas del 2 al 12 (NCETM 2.3 a 2.11; "
                "hasta 12 x 12 al acabar 4.o).  Pero %s x 4 lo calculo: escribelo.\n\n"
                "RESULTADO: todavia_no" % (n, n))
    L = ["PREGUNTA (M.2): la tabla del %s  (grupos de %s; cada producto es el anterior MAS %s)" % (n, n, n), ""]
    v, k, fila = 0, "cero", []
    while True:
        L.append("    %2d x %s = %d" % (leer(k, saber), n, v))
        fila.append(str(v))
        if k == "diez":
            break
        v = saltar(v, _TABLAS[n], saber)
        k = siguiente(k, saber)
    L.append("")
    L.append("  (es contar de %s en %s: %s)" % (n, n, ", ".join(fila)))
    L.append("")
    L.append("RESULTADO: %s" % ", ".join(fila))
    return "\n".join(L)


def mitad(n, saber=None):
    """La MITAD de n (NCETM 2.5: lo contrario del doble), hasta 20: se hacen parejas y se reparte una
    de cada pareja a cada lado.  Se comprueba con el doble.  Devuelve {"valor"} o {"conclusion"}."""
    if saber is None:
        saber = cargar_conocimiento()
    if viene_despues(decir(n, saber), "veinte", saber):
        return {"conclusion": "todavia_no"}
    actual, cada_lado, objetivo = "cero", "cero", decir(n, saber)
    while actual != objetivo:
        uno = siguiente(actual, saber)
        if uno == objetivo:
            return {"conclusion": "impar", "sobra": leer(cada_lado, saber)}
        actual = siguiente(uno, saber)
        cada_lado = siguiente(cada_lado, saber)
    v = leer(cada_lado, saber)
    doble = aplicar("sumar", {"a": v, "b": v}, saber)
    return {"conclusion": "hecho", "valor": v, "comprobacion": doble["valor"] == n,
            "doble": "%d + %d = %d (%s)" % (v, v, doble["valor"], doble["resultado"]["metodo"])}


def explicar_mitad(texto, saber=None):
    t = texto.strip().rstrip("?").strip()
    if not t.isdigit():
        return "NO ENTIENDO ESTO: se escribe asi:  mitad: 14"
    n = int(t)
    r = mitad(n, saber)
    L = ["PREGUNTA (M.2): la MITAD de %d  (lo contrario del doble: que numero, mas el mismo, da %d?)" % (n, n), ""]
    if r["conclusion"] == "todavia_no":
        L += ["  TODAVIA NO: por ahora parto hasta 20 (los dobles que se); mas grande es REPARTIR (M.3).", "",
              "RESULTADO: todavia_no"]
    elif r["conclusion"] == "impar":
        L += ["  hago parejas y reparto una de cada pareja a cada lado: %d a cada lado y SOBRA UNO." % r["sobra"],
              "  %d es impar: no tiene mitad exacta (sin partir uno por la mitad)." % n, "", "RESULTADO: impar"]
    else:
        L += ["  hago parejas y reparto una de cada pareja a cada lado: %d a cada lado, no sobra ninguno." % r["valor"],
              "  COMPRUEBO con el doble: %s ... %s" % (r["doble"], "SI" if r["comprobacion"] else "NO"), "",
              "RESULTADO: %d" % r["valor"]]
    return "\n".join(L)


# ------------------------------------------------------------- M.4: las tablas del 4 y del 8; divisible


def _fila_de(n, saber):
    """Los productos 0 x n ... 10 x n, sacados como dice NCETM: el 2 y el 3 contando de n en n; el 4,
    el 8 y el 6 DOBLANDO (2 -> 4 -> 8; 3 -> 6); el 9 TRIPLICANDO el 3."""
    def doble(x):
        return aplicar("sumar", {"a": x, "b": x}, saber)["valor"]
    if n in ("2", "3"):
        out, v, k = [], 0, "cero"
        while True:
            out.append(v)
            if k == "diez":
                return out
            r = contar_adelante(decir(v, saber), {"2": "dos", "3": "tres"}[n], saber)
            v = leer(r["resultado"], saber)
            k = siguiente(k, saber)
    if n in ("4", "8", "6"):
        return [doble(x) for x in _fila_de({"4": "2", "8": "4", "6": "3"}[n], saber)]
    if n == "9":
        return [aplicar("sumar", {"a": doble(x), "b": x}, saber)["valor"] for x in _fila_de("3", saber)]
    if n in ("5", "10"):
        out, v, k = [], 0, "cero"
        while True:
            out.append(v)
            if k == "diez":
                return out
            v = saltar(v, _TABLAS[n], saber)
            k = siguiente(k, saber)
    if n == "7":                                       # 7 = 5 + 2 (la distributiva, NCETM 2.10)
        return [aplicar("sumar", {"a": x, "b": y}, saber)["valor"]
                for x, y in zip(_fila_de("5", saber), _fila_de("2", saber))]
    if n == "1":                                       # k grupos de 1 son k (NCETM 2.4): recitar
        return _cifras_de_una(saber) + [10]
    if n in ("11", "12"):                              # 11 = 10 + 1;  12 = 10 + 2  (NCETM 2.11)
        return [aplicar("sumar", {"a": x, "b": y}, saber)["valor"]
                for x, y in zip(_fila_de("10", saber), _fila_de({"11": "1", "12": "2"}[n], saber))]
    return None


_DERIVA = {"3": (None, "contar de 3 en 3", "NCETM 2.8"), "4": ("2", "el DOBLE", "NCETM 2.7"),
           "8": ("4", "el DOBLE", "NCETM 2.7"), "6": ("3", "el DOBLE", "NCETM 2.8"),
           "9": ("3", "el TRIPLE", "NCETM 2.8"), "7": ("5 y 2", "PARTIR", "NCETM 2.9 y 2.10"),
           "11": ("10 y 1", "PARTIR", "NCETM 2.11"), "12": ("10 y 2", "PARTIR", "NCETM 2.11")}


def _tabla_doblando(n, saber):
    """Las tablas que salen de otras: 4 y 8 (doblando el 2), 6 (doblando el 3), 9 (triplicando el 3);
    y la del 3 contando de 3 en 3."""
    base, como, fuente = _DERIVA[n]
    fila = _fila_de(n, saber)
    if n == "7":
        L = ["PREGUNTA (M.6): la tabla del 7  (7 = 5 + 2: cada producto es el de la del 5 MAS el de la del 2;"
             " la distributiva, NCETM 2.10)", ""]
        for k, (v, a, b) in enumerate(zip(fila, _fila_de("5", saber), _fila_de("2", saber))):
            L.append("    %2d x 7 = %2d x 5 + %2d x 2 = %2d + %2d = %d" % (k, k, k, a, b, v))
    elif n in ("11", "12"):
        q = {"11": "1", "12": "2"}[n]
        L = ["PREGUNTA (M.7): la tabla del %s  (%s = 10 + %s: cada producto es el de la del 10 MAS el de la del %s;"
             " la distributiva, NCETM 2.11)" % (n, n, q, q), ""]
        for k, (v, a, b) in enumerate(zip(fila, _fila_de("10", saber), _fila_de(q, saber))):
            L.append("    %2d x %s = %2d x 10 + %2d x %s = %3d + %2d = %d" % (k, n, k, k, q, a, b, v))
        if n == "12":
            dobles = [aplicar("sumar", {"a": x, "b": x}, saber)["valor"] for x in _fila_de("6", saber)]
            L.append("")
            L.append("  COMPRUEBO (NCETM 2.11, punto 3): cada producto de la del 12 es el DOBLE del de la del 6 ... %s"
                     % ("SI" if dobles == fila else "NO"))
    elif base:
        L = ["PREGUNTA (M.4/M.5): la tabla del %s  (cada producto es %s del de la tabla del %s; %s)"
             % (n, como, base, fuente), ""]
        fb = _fila_de(base, saber)
        for k, (v, b) in enumerate(zip(fila, fb)):
            L.append("    %2d x %s = %s de %2d x %s (%2d) = %d" % (k, n, como.lower(), k, base, b, v))
    else:
        L = ["PREGUNTA (M.5): la tabla del %s  (contar de %s en %s; %s)" % (n, n, n, fuente), ""]
        for k, v in enumerate(fila):
            L.append("    %2d x %s = %d" % (k, n, v))
    txt = ", ".join(str(x) for x in fila)
    L += ["", "  (y seguidos se diferencian en %s: contar de %s en %s: %s)" % (n, n, n, txt), "",
          "RESULTADO: %s" % txt]
    return "\n".join(L)


def decidir_divisible(n, d, saber=None):
    """NCETM 2.7 (punto 5), con MITADES: entre 2 si se parte por la mitad sin que sobre; entre 4 si se
    puede DOS veces; entre 8, TRES veces."""
    if saber is None:
        saber = cargar_conocimiento()
    if d in (3, 9, 6):
        return _divisible_por_cifras(n, d, saber)
    if d == 12:                                        # NCETM 2.11: entre 3 Y entre 4
        r3, r4 = decidir_divisible(n, 3, saber), decidir_divisible(n, 4, saber)
        out = {"conclusion": "hecho", "valor": r3["valor"] and r4["valor"], "regla": "3_y_4", "por3": r3, "por4": r4}
        if out["valor"]:
            out["cociente"] = aplicar("dividir", {"total": n, "divisor": 12}, saber)["valor"]
        return out
    if d == 11 and len(cifras_de(n)) == 2:             # NCETM 2.11: dos cifras iguales (11, 22 ... 99)
        c = cifras_de(n)
        out = {"conclusion": "hecho", "valor": c[0] == c[1], "regla": "cifras_iguales", "cifras": c}
        if out["valor"]:
            out["cociente"] = c[0]
        return out
    veces = {2: "uno", 4: "dos", 8: "tres"}.get(d)
    if veces is None:
        r = aplicar("dividir", {"total": n, "divisor": d}, saber)
        if r["conclusion"] != "hecho":
            return {"conclusion": "imposible", "porque": r.get("porque")}
        resto = r["resultado"].get("resto", 0)
        return {"conclusion": "hecho", "valor": not resto, "regla": "dividiendo", "cociente": r["valor"],
                "resto": resto, "metodo": r["resultado"]["metodo"]}
    v, hecho, camino = n, "cero", [str(n)]
    while hecho != veces:
        r = aplicar("dividir", {"total": v, "divisor": 2}, saber)
        if r["resultado"].get("resto"):
            return {"conclusion": "hecho", "valor": False, "camino": camino, "falla_en": v}
        v = r["valor"]
        camino.append(str(v))
        hecho = siguiente(hecho, saber)
    return {"conclusion": "hecho", "valor": True, "camino": camino, "cociente": v}


def _suma_de_cifras(n, saber):
    cif = cifras_de(n)
    total = 0
    for c in cif:
        total = aplicar("sumar", {"a": total, "b": c}, saber)["valor"]
    return total


def _divisible_por_cifras(n, d, saber):
    """NCETM 2.8 (punto 6): entre 3 si la SUMA DE LAS CIFRAS se divide entre 3; entre 9 si se divide
    entre 9 (se suman las cifras hasta que queda una sola: 3, 6 o 9 -> entre 3; 9 -> entre 9);
    entre 6 si es PAR y se divide entre 3."""
    camino, v = [str(n)], n
    while viene_despues(decir(v, saber), "nueve", saber):
        v = _suma_de_cifras(v, saber)
        camino.append(str(v))
    entre3 = v in (0, 3, 6, 9)
    entre9 = v in (0, 9)
    par = decidir_paridad(n, saber)["valor"] == "par"
    valor = {3: entre3, 9: entre9, 6: entre3 and par}[d]
    out = {"conclusion": "hecho", "valor": valor, "camino": camino, "cifra": v, "par": par, "regla": "cifras"}
    if valor:
        out["cociente"] = aplicar("dividir", {"total": n, "divisor": d}, saber)["valor"]
    return out


def explicar_divisible(texto, saber=None):
    m = re.match(r"^(\d+)\s+entre\s+(\d+)$", " ".join(texto.lower().split()))
    if not m:
        return "NO ENTIENDO ESTO: se escribe asi:  divisible: 36 entre 4"
    n, d = int(m.group(1)), int(m.group(2))
    r = decidir_divisible(n, d, saber)
    L = ["PREGUNTA (M.4/M.5): %d se puede dividir entre %d sin que sobre?" % (n, d), ""]
    if r["conclusion"] == "todavia_no":
        return "\n".join(L + ["  TODAVIA NO: por ahora se mirarlo entre 2, 3, 4, 6, 8 y 9 (NCETM 2.7 y 2.8).", "", "RESULTADO: todavia_no"])
    if r["conclusion"] == "imposible":
        return "\n".join(L + ["  NO SE PUEDE: %s" % r.get("porque"), "", "RESULTADO: no_se_puede"])
    if r.get("regla") == "dividiendo":
        L.append("  %s: DIVIDO con lo que se (%s)" % (
            "la regla del 11 de 4.o es para DOS cifras (NCETM 2.11); con mas" if d == 11 else
            "para el %d no hay regla corta (NCETM 2.9)" % d, r["metodo"]))
        L.append("  %s" % ("SI: %d entre %d da %d, justo." % (n, d, r["cociente"]) if r["valor"]
                           else "NO: da %d y sobra%s %d." % (r["cociente"], "" if r["resto"] == 1 else "n", r["resto"])))
        L += ["", "RESULTADO: %s" % ("si" if r["valor"] else "no")]
        return "\n".join(L)
    if r.get("regla") == "cifras":
        L.append("  la regla (NCETM 2.8): se suman las cifras hasta que queda UNA: %s" % " -> ".join(r["camino"]))
        if d == 3:
            L.append("  entre 3 si esa cifra es 0, 3, 6 o 9: es %d" % r["cifra"])
        elif d == 9:
            L.append("  entre 9 si esa cifra es 0 o 9: es %d" % r["cifra"])
        else:
            L.append("  entre 6 si es PAR (%s) y se divide entre 3 (la cifra es %d)" % ("si" if r["par"] else "no", r["cifra"]))
        L.append("  %s" % ("SI: %d entre %d da %d, justo." % (n, d, r["cociente"]) if r["valor"] else "NO."))
        L += ["", "RESULTADO: %s" % ("si" if r["valor"] else "no")]
        return "\n".join(L)
    if r.get("regla") == "3_y_4":
        r3, r4 = r["por3"], r["por4"]
        L.append("  la regla (NCETM 2.11): entre 12 si se divide entre 3 Y entre 4 (12 = 3 x 4).")
        L.append("    entre 3? se suman las cifras: %s -> %s" % (" -> ".join(r3["camino"]), "SI" if r3["valor"] else "NO"))
        L.append("    entre 4? dos mitades sin que sobre: %s -> %s" % (" -> ".join(r4["camino"]), "SI" if r4["valor"] else "NO"))
        L.append("  %s" % ("SI: %d entre 12 da %d, justo." % (n, r["cociente"]) if r["valor"] else "NO."))
        L += ["", "RESULTADO: %s" % ("si" if r["valor"] else "no")]
        return "\n".join(L)
    if r.get("regla") == "cifras_iguales":
        L.append("  la regla (NCETM 2.11): un numero de dos cifras se divide entre 11 si las DOS CIFRAS son IGUALES"
                 " (11, 22 ... 99).")
        L.append("  %d: %d y %d -> %s" % (n, r["cifras"][1], r["cifras"][0],
                                        "iguales: SI, %d entre 11 da %d." % (n, r["cociente"]) if r["valor"] else "distintas: NO."))
        L += ["", "RESULTADO: %s" % ("si" if r["valor"] else "no")]
        return "\n".join(L)
    veces = {2: "UNA vez", 4: "DOS veces", 8: "TRES veces"}[d]
    L.append("  la regla (con mitades): entre %d si se puede partir por la mitad %s sin que sobre." % (d, veces))
    L.append("  %s" % " -> ".join(r["camino"]))
    if r["valor"]:
        L.append("  SI: %d entre %d da %d, justo." % (n, d, r["cociente"]))
    else:
        L.append("  NO: el %d ya no se parte por la mitad sin que sobre uno." % r["falla_en"])
    L += ["", "RESULTADO: %s" % ("si" if r["valor"] else "no")]
    return "\n".join(L)



# ------------------------------------------------------------- M.10: corta: 347 x 6

def explicar_corta(texto, saber=None):
    """'corta: 347 x 6': el algoritmo de la multiplicacion corta (NCETM 2.14), aunque haya un camino mas corto."""
    if saber is None:
        saber = cargar_conocimiento()
    m = _POR.match(" ".join(texto.lower().split()))
    if not m:
        return "NO ENTIENDO ESTO: se escribe asi:  corta: 347 x 6"
    a, b = int(m.group(1)), int(m.group(2))
    L = ["PREGUNTA (M.10): %d x %d con la MULTIPLICACION CORTA  (NCETM 2.14; 4.NBT.B.5)" % (a, b), ""]
    r = aplicar("multiplicacion_corta", {"a": a, "b": b}, saber)
    if r["conclusion"] != "hecho":
        porque = r.get("porque") or (r["candidatos"][0].get("descartado") if r.get("candidatos") else "")
        return "\n".join(L + ["  NO SE PUEDE: %s" % porque, "", "RESULTADO: no_se_puede"])
    L.append("        %s" % r["resultado"]["cuenta"].replace("; ", "\n        "))
    otra = aplicar("multiplicar_partiendo_por_sitios", {"a": a, "b": b}, saber)
    if otra["conclusion"] == "hecho":
        L.append("")
        L.append("  LO COMPRUEBO PARTIENDO POR SITIOS:")
        L.append("        %s" % otra["resultado"]["cuenta"].replace("; ", "\n        "))
        L.append("        ... %s" % ("lo mismo: SI" if otra["valor"] == r["valor"] else "NO CUADRA"))
    L += ["", "RESULTADO: %d" % r["valor"]]
    return "\n".join(L)
