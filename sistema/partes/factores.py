# -*- coding: utf-8 -*-
"""
Euclides - FACTORES, MULTIPLOS, PRIMOS Y COMPUESTOS (paso M.15 del plan pedagogico, 7 oct 2026; 5.o).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

NCETM 2.21 (Factors, multiples, prime numbers and composite numbers); Common Core 4.OA.B.4.
  punto 1: los factores son enteros positivos que se multiplican para dar un numero;
  punto 2: se buscan con ORDEN; van POR PAREJAS; los CUADRADOS tienen un numero impar de factores;
           con mas de dos factores, COMPUESTO;
  punto 3: un PRIMO tiene exactamente DOS factores (el 1 no: tiene uno);
  punto 4: factor COMUN (de dos numeros); factor PRIMO (un factor que es primo);
  punto 5: un MULTIPLO es el numero por un entero; multiplo COMUN;
  punto 6: las parejas de factores de 100 sirven para calcular (25 x 36 = 100 x 9).
Las cuentas las hacen las piezas (preguntas 'parejas_de_factores' y 'primo', y la pieza
multiplicar_con_las_parejas_de_100) y el mecanismo (saltar de n en n).  Aqui solo se leen las
ordenes, se pregunta y se explica.
"""

import re

_FM_N = r"(\d+)"
_FM_FACTORES = re.compile(r"^(?:factores|divisores|parejas(?:\s+de\s+factores)?)(?::\s*|\s+de\s+|\s+)(?:de\s+)?" + _FM_N + r"$")
_FM_PRIMO = re.compile(r"^(?:primo:?\s*" + _FM_N + r"|es\s+primo:?\s*" + _FM_N + r"|es\s+(?:el\s+)?" + _FM_N
                       + r"\s+(?:un\s+)?(?:numero\s+)?primo|(?:el\s+)?" + _FM_N + r"\s+es\s+(?:un\s+)?(?:numero\s+)?primo)$")
_FM_CRIBA = re.compile(r"^(?:primos\s+hasta(?:\s+el)?|criba(?::|\s+hasta)?(?:\s+el)?)\s*" + _FM_N + r"$")
_FM_MULTIPLOS = re.compile(r"^multiplos(?::\s*|\s+de\s+|\s+)(?:de\s+)?" + _FM_N + r"(?:\s+hasta(?:\s+el)?\s+" + _FM_N + r")?$")
_FM_ES = re.compile(r"^(?:es\s+)?(?:el\s+)?" + _FM_N + r"\s+(?:es\s+)?(?:un\s+)?(multiplo|factor|divisor)\s+de(?:l)?\s+"
                    + _FM_N + r"$")
_FM_COMUNES = re.compile(r"^(factores|multiplos)\s+comunes(?::\s*|\s+de\s+|\s+)(?:de\s+)?" + _FM_N + r"\s*(?:y|,)\s*"
                         + _FM_N + r"$")
_FM_PRIMOS_DE = re.compile(r"^factores\s+primos(?::\s*|\s+de\s+|\s+)(?:de\s+)?" + _FM_N + r"$")
_FM_CON100 = re.compile(r"^con\s+(?:las\s+parejas\s+de\s+)?(?:el\s+)?100:?\s*" + _FM_N + r"\s*[x*×]\s*" + _FM_N + r"$")
_FM_ORDENES = (_FM_FACTORES, _FM_PRIMO, _FM_CRIBA, _FM_MULTIPLOS, _FM_ES, _FM_COMUNES, _FM_PRIMOS_DE, _FM_CON100)



def _fm_pasa(a, b, saber):
    """a es MAYOR que b: se mira con el mecanismo (viene despues en la lista / mas cifras), no con el '>' de
    Python.  (Arreglo tras la revision de M.15.)"""
    pa, pb = decir(a, saber), decir(b, saber)
    if pa is None or pb is None:
        return pa is None and pb is not None          # el que no tiene nombre es el que se pasa del techo
    return viene_despues(pa, pb, saber)


def _fm_limpio(texto):
    t = texto.lower()
    for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("¿", "")):
        t = t.replace(a, b)
    return " ".join(t.strip().rstrip("?").strip().split())


def es_orden_factores(texto):
    t = _fm_limpio(texto)
    return any(r.match(t) for r in _FM_ORDENES)


def _fm_lista(ns):
    return ", ".join("%d" % x for x in ns)


def _fm_contar(cosas, saber):
    """Cuantas hay: se CUENTAN recitando (una palabra por cosa).  Devuelve el numero."""
    k = "cero"
    for _ in cosas:
        k = siguiente(k, saber)
    return leer(k, saber)


def _fm_saltar(v, d, saber):
    """Un salto de d desde v: con los dedos si d es pequeno (N.1); si no, una SUMA (un salto grande es una
    suma, no d pasos).  None si se sale de la lista."""
    p = decir(d, saber)
    if p is not None and levantar_dedos(p, saber) is not None:
        return saltar(v, p, saber)
    r = aplicar("sumar", {"a": v, "b": d}, saber)
    return r["valor"] if r["conclusion"] == "hecho" else None


def _fm_porques(r):
    """Por que no salio: lo que dijo cada pieza que lo intento."""
    out = [c["no_salio"] for c in r.get("candidatos", []) if c.get("no_salio")]
    return out or [r.get("porque") or r["conclusion"]]


# ---------------------------------------------------------------- las parejas de factores

def decidir_factores(n, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    if n == 0:
        return {"conclusion": "no_se_puede", "porque": "todo numero por 0 da 0: los factores son de los enteros "
                                                      "positivos (del 1 en adelante)"}
    r = aplicar("parejas_de_factores", {"n": n}, saber)
    if r["conclusion"] != "hecho":
        return {"conclusion": "todavia_no", "porque": "; ".join(_fm_porques(r)) if r["conclusion"] != "ninguna"
                else "%d pasa de mi techo (un millon)" % n}
    res = dict(r["resultado"])
    res["conclusion"] = "hecho"
    res["cuantos"] = _fm_contar(res["factores"], saber)
    return res


def explicar_factores(n, saber):
    L = ["PREGUNTA (M.15): los FACTORES de %d  (NCETM 2.21, puntos 1 y 2; 4.OA.B.4)" % n, ""]
    r = decidir_factores(n, saber)
    if r["conclusion"] == "no_se_puede":
        return "\n".join(L + ["  NO SE PUEDE: %s" % r["porque"], "", "RESULTADO: no_se_puede"])
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["  TODAVIA NO: %s" % r["porque"], "", "RESULTADO: todavia_no"])
    L.append("  un factor es un numero que, multiplicado por otro, da %d (punto 1).  Los busco CON ORDEN, probando"
             " 1, 2, 3 ... y dividiendo (punto 2):" % n)
    for d, q, resto in r["probados"]:
        if resto:
            L.append("     %2d?  %d : %d = %d y sobra%s %d  -> no" % (d, n, d, q, "" if resto == 1 else "n", resto))
        elif q == d:
            L.append("     %2d?  %d : %d = %d  -> %d x %d: el %d va CONSIGO MISMO" % (d, n, d, q, d, q, d))
        else:
            L.append("     %2d?  %d : %d = %d  -> la pareja %d x %d" % (d, n, d, q, d, q))
    if r["cruce"]:
        d, q, _ = r["cruce"]
        L.append("     %2d?  %d : %d = %d: el companero ya es MAS PEQUENO que el %d; ya me los encontraria al reves:"
                 " PARO" % (d, n, d, q, d))
    elif r["por_si_mismo"]:
        L.append("     %s" % r["por_si_mismo"])
    elif r["cuadrado"]:
        L.append("     con el %d por si mismo ya llegue al medio: PARO" % r["parejas"][-1][0])
    L.append("  LAS PAREJAS: %s" % r["valor"])
    L.append("  en RECTANGULOS de %d cuadraditos (filas x columnas): %s" % (n, ", ".join(
        "%d fila%s de %d" % (d, "" if d == 1 else "s", q) for d, q in r["parejas"])))
    L.append("  LOS FACTORES (los de delante y, al reves, sus companeros): %s" % _fm_lista(r["factores"]))
    par = decidir_paridad(r["cuantos"], saber)["valor"] == "par"
    if r["cuadrado"]:
        d = r["parejas"][-1][0]
        L.append("  son %d factores: IMPAR, porque el %d va con el mismo (%d x %d): %d es un numero CUADRADO"
                 " (un cuadrado de %d por %d)" % (r["cuantos"], d, d, d, n, d, d))
    else:
        L.append("  son %d factores: %s, porque van de dos en dos (por parejas)" % (r["cuantos"], "PAR" if par else "IMPAR"))
    if n == 1:
        L.append("  el 1 tiene UN solo factor: no es primo ni compuesto")
    elif r["cuantos"] == 2:
        L.append("  tiene EXACTAMENTE DOS factores (1 y %d): es PRIMO; solo se puede poner en UNA fila (punto 3)" % n)
    else:
        L.append("  tiene MAS de dos factores: es COMPUESTO (punto 2)")
    L.append("  y %d es MULTIPLO de cada uno de sus factores (4.OA.B.4)" % n)
    if n == 100:
        L.append("  LAS PAREJAS DE 100 sirven para calcular (punto 6): 25 x 4, 50 x 2, 20 x 5  (prueba: con 100: 25 x 36)")
    L.append("  COMPRUEBO cada division con la contraria (multiplicando): %s ... SI" % r["vuelta"])
    return "\n".join(L + ["", "RESULTADO: %s" % _fm_lista(r["factores"])])


# ---------------------------------------------------------------- primo o compuesto

def decidir_primo(n, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    if n == 0:
        return {"conclusion": "hecho", "valor": "ni_primo_ni_compuesto", "pieza": None,
                "cuenta": "el 0 no: los primos y los compuestos son enteros positivos (todo numero por 0 da 0)"}
    r = aplicar("primo", {"n": n}, saber)
    if r["conclusion"] != "hecho":
        return {"conclusion": "todavia_no", "porques": _fm_porques(r) if r["conclusion"] != "ninguna"
                else ["%d pasa de mi techo (un millon)" % n]}
    res = dict(r["resultado"])
    res.update({"conclusion": "hecho", "pieza": r["pieza"]["id"]})
    return res


def explicar_primo(n, saber):
    L = ["PREGUNTA (M.15): %d es PRIMO o COMPUESTO?  (NCETM 2.21, puntos 2 y 3; 4.OA.B.4)" % n, ""]
    r = decidir_primo(n, saber)
    if r["conclusion"] != "hecho":
        L.append("  TODAVIA NO:")
        L += ["     - %s" % p for p in r["porques"]]
        return "\n".join(L + ["", "RESULTADO: todavia_no"])
    L.append("  un PRIMO tiene EXACTAMENTE DOS factores (el 1 y el mismo); un COMPUESTO tiene MAS de dos")
    if r["pieza"] is None:
        return "\n".join(L + ["  %s" % r["cuenta"], "", "RESULTADO: %s" % r["valor"]])
    L.append("  %s" % r["metodo"])
    L.append("  %s" % r["cuenta"])
    if r["pieza"] == "primo_el_uno":
        L.append("  OJO: el 1 NO es primo (el error tipico: 'se divide entre 1 y entre si mismo'; aqui son el MISMO)")
    elif r["pieza"] == "primo_buscando_parejas":
        L.append("  las parejas: %s" % ", ".join("%d x %d" % p for p in r["parejas"]))
        if r["valor"] == "primo":
            L.append("  solo se puede poner en UNA fila de %d" % n)
    if r["valor"] == "primo" and n == 2:
        L.append("  OJO: el 2 es PAR y es PRIMO (el unico primo par)")
    if r["valor"] == "compuesto" and decidir_paridad(n, saber)["valor"] == "impar":
        L.append("  OJO: es IMPAR y NO es primo (no todos los impares son primos)")
    L.append("  COMPRUEBO con la contraria: %s ... SI" % r["vuelta"])
    return "\n".join(L + ["", "RESULTADO: %s" % r["valor"]])


# ---------------------------------------------------------------- la criba

def decidir_criba(hasta, saber=None):
    """La criba de Eratostenes: del 2 al 'hasta'; se tachan los multiplos de cada uno que queda, contando
    de n en n; se para cuando el siguiente, por si mismo, ya se pasa."""
    if saber is None:
        saber = cargar_conocimiento()
    if viene_despues(decir(hasta, saber) or "mil", "cien", saber):
        return {"conclusion": "todavia_no", "porque": "la criba de 5.o llega hasta 100 (4.OA.B.4: del 1 al 100)"}
    if hasta < 2:
        return {"conclusion": "hecho", "primos": [], "tachados": {}, "pasos": []}
    numeros, p = [], "dos"
    while True:
        numeros.append(leer(p, saber))
        if p == decir(hasta, saber):
            break
        p = siguiente(p, saber)
    tachado, pasos = {}, []
    for p in numeros:
        if p in tachado:
            continue
        pp = aplicar("multiplicar", {"a": p, "b": p}, saber)["valor"]
        if _fm_pasa(pp, hasta, saber):
            pasos.append("el %d: %d x %d = %d ya se pasa de %d -> PARO: lo que queda sin tachar es primo" % (p, p, p, pp, hasta))
            break
        v, nuevos = p, []
        while True:
            v = _fm_saltar(v, p, saber)
            if v is None or _fm_pasa(v, hasta, saber):
                break
            if v not in tachado:
                tachado[v] = p
                nuevos.append(v)
        pasos.append("el %d se queda; tacho sus multiplos contando de %d en %d: %s" % (
            p, p, p, _fm_lista(nuevos) if nuevos else "(ya estaban tachados)"))
    return {"conclusion": "hecho", "primos": [x for x in numeros if x not in tachado], "tachados": tachado,
            "pasos": pasos}


def explicar_criba(hasta, saber):
    L = ["PREGUNTA (M.15): los numeros PRIMOS hasta %d  (la CRIBA de Eratostenes; NCETM 2.21; 4.OA.B.4)" % hasta, ""]
    r = decidir_criba(hasta, saber)
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["  TODAVIA NO: %s" % r["porque"], "", "RESULTADO: todavia_no"])
    L.append("  escribo del 2 al %d (el 1 no: tiene un solo factor)" % hasta)
    L += ["    %s" % p for p in r["pasos"]]
    malos = [x for x in r["primos"] if decidir_primo(x, saber).get("valor") != "primo"]
    cuantos = _fm_contar(r["primos"], saber)
    L.append("  quedan %d: %s" % (cuantos, _fm_lista(r["primos"]) or "ninguno"))
    L.append("  COMPRUEBO por OTRO camino (buscando las parejas de cada uno): %s" % (
        "todos tienen solo la pareja 1 x n ... SI" if not malos else "NO CUADRA con %s" % _fm_lista(malos)))
    return "\n".join(L + ["", "RESULTADO: %s" % (_fm_lista(r["primos"]) or "ninguno")])


# ---------------------------------------------------------------- los multiplos

def decidir_multiplos(d, hasta=None, saber=None):
    """Los multiplos de d contando de d en d: los doce primeros, o hasta 'hasta'."""
    if saber is None:
        saber = cargar_conocimiento()
    if d == 0:
        return {"conclusion": "hecho", "lista": [0], "cero": True}
    lista, k, v = [], "uno", d
    if hasta is not None and _fm_pasa(v, hasta, saber):
        return {"conclusion": "hecho", "lista": lista}
    while True:
        lista.append(v)
        if hasta is None and k == "doce":
            break
        v = _fm_saltar(v, d, saber)
        if v is None:
            return {"conclusion": "hecho", "lista": lista, "techo": True}
        if hasta is not None and _fm_pasa(v, hasta, saber):
            break
        if k == "cien":
            return {"conclusion": "todavia_no", "porque": "son mas de cien multiplos: no los digo uno a uno "
                                                          "(los doce primeros con 'multiplos de %d')" % d}
        k = siguiente(k, saber)
    return {"conclusion": "hecho", "lista": lista}


def explicar_multiplos(d, hasta, saber):
    L = ["PREGUNTA (M.15): los MULTIPLOS de %d%s  (NCETM 2.21, punto 5)" % (d, " hasta %d" % hasta if hasta is not None else ""), ""]
    r = decidir_multiplos(d, hasta, saber)
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["  TODAVIA NO: %s" % r["porque"], "", "RESULTADO: todavia_no"])
    if r.get("cero"):
        return "\n".join(L + ["  0 por cualquier numero es 0: el unico multiplo de 0 es el 0", "", "RESULTADO: 0"])
    if not r["lista"]:
        return "\n".join(L + ["  el primer multiplo, %d x 1 = %d, ya se pasa de %d: ninguno" % (d, d, hasta), "",
                              "RESULTADO: ninguno"])
    L.append("  un multiplo de %d es %d por un entero: %d x 1, %d x 2 ... Se sacan CONTANDO DE %d EN %d:" % (d, d, d, d, d, d))
    k, filas = "uno", []
    for v in r["lista"]:
        filas.append("%d x %d = %d" % (d, leer(k, saber), v))
        k = siguiente(k, saber)
    for i in range(0, len(filas), 6):
        L.append("     " + ";  ".join(filas[i:i + 6]))
    if r.get("techo"):
        L.append("  (el siguiente ya pasa de un millon, mi techo)")
    ultimo, veces = r["lista"][-1], _fm_contar(r["lista"], saber)
    c = aplicar("multiplicar", {"a": d, "b": veces}, saber)
    if c["conclusion"] == "hecho":
        L.append("  COMPRUEBO el ultimo multiplicando: %d x %d = %d ... %s" % (d, veces, c["valor"],
                                                                           "SI" if c["valor"] == ultimo else "NO"))
    L.append("  (OJO: los multiplos SALEN de multiplicar; los factores ENTRAN: %d es FACTOR de %d, y %d es MULTIPLO de %d)"
             % (d, ultimo, ultimo, d))
    return "\n".join(L + ["", "RESULTADO: %s" % _fm_lista(r["lista"])])


def _fm_divide(n, d, saber):
    """n se reparte en grupos de d sin que sobre?  (decidir_divisible de M.4/M.5).  (si/no, las lineas)"""
    txt = explicar_divisible("%d entre %d" % (n, d), saber).splitlines()
    res = txt[-1].replace("RESULTADO:", "").strip()
    return res, [x for x in txt[1:-1] if x.strip()]


def explicar_es_multiplo(a, que, b, saber):
    que = "factor" if que == "divisor" else que
    L = ["PREGUNTA (M.15): %d es %s de %d?  (NCETM 2.21, puntos 1 y 5; 4.OA.B.4)" % (a, que.upper(), b), ""]
    n, d = (a, b) if que == "multiplo" else (b, a)       # siempre: n se divide entre d?
    if d == 0:
        txt = ("  el 0 no es factor de nada (todo por 0 da 0)" if que == "factor"
               else "  los multiplos de 0 son el 0 (todo por 0 da 0)")
        return "\n".join(L + [txt, "", "RESULTADO: %s" % ("si" if n == 0 else "no")])
    if que == "multiplo":
        L.append("  %d es multiplo de %d si sale de MULTIPLICAR %d por un entero: si %d se reparte en grupos de %d"
                 " sin que sobre" % (a, b, b, a, b))
    else:
        L.append("  %d es factor de %d si %d por un entero da %d: si %d se reparte en grupos de %d sin que sobre"
                 % (a, b, a, b, b, a))
    if n == 0:
        return "\n".join(L + ["  %d x 0 = 0: si" % d, "", "RESULTADO: si"])
    if _fm_pasa(d, n, saber):
        L.append("  %d es mas pequeno que %d: %d x 1 ya es %d, que se pasa: NO" % (n, d, d, d))
        r2, _ = _fm_divide(d, n, saber)
        if r2 == "si":
            L.append("  OJO: es AL REVES: %d es %s de %d (los factores ENTRAN en la multiplicacion; los multiplos SALEN)"
                     % (a, "FACTOR" if que == "multiplo" else "MULTIPLO", b))
        return "\n".join(L + ["", "RESULTADO: no"])
    res, lineas = _fm_divide(n, d, saber)
    L.extend(lineas)
    if res not in ("si", "no"):
        return "\n".join(L + ["", "RESULTADO: %s" % res])
    if res == "si":
        q = aplicar("dividir", {"total": n, "divisor": d}, saber)["valor"]
        c = aplicar("multiplicar", {"a": d, "b": q}, saber)
        if c["conclusion"] == "hecho":
            L.append("  COMPRUEBO multiplicando: %d x %d = %d ... %s" % (d, q, c["valor"], "SI" if c["valor"] == n else "NO"))
    return "\n".join(L + ["", "RESULTADO: %s" % res])


# ---------------------------------------------------------------- comunes y primos

def explicar_factores_comunes(a, b, saber):
    L = ["PREGUNTA (M.15): los FACTORES COMUNES de %d y %d  (NCETM 2.21, punto 4)" % (a, b), ""]
    ra, rb = decidir_factores(a, saber), decidir_factores(b, saber)
    for n, r in ((a, ra), (b, rb)):
        if r["conclusion"] != "hecho":
            return "\n".join(L + ["  TODAVIA NO (%d): %s" % (n, r["porque"]), "", "RESULTADO: todavia_no"])
        L.append("  los factores de %d (por parejas: %s): %s" % (n, r["valor"], _fm_lista(r["factores"])))
    comunes = [x for x in ra["factores"] if x in rb["factores"]]
    L.append("  los que estan en LAS DOS listas: %s" % _fm_lista(comunes))
    L.append("  el MAYOR factor comun: %d%s" % (comunes[-1], "  (solo el 1: no comparten ningun otro)" if comunes == [1] else ""))
    return "\n".join(L + ["", "RESULTADO: %s" % _fm_lista(comunes)])


def explicar_multiplos_comunes(a, b, saber):
    L = ["PREGUNTA (M.15): los MULTIPLOS COMUNES de %d y %d  (NCETM 2.21, punto 5)" % (a, b), ""]
    if 0 in (a, b):
        return "\n".join(L + ["  con el 0 el unico multiplo es el 0", "", "RESULTADO: 0"])
    g, p = (a, b) if _fm_pasa(a, b, saber) else (b, a)
    r = decidir_multiplos(g, None, saber)
    L.append("  cuento los del MAS GRANDE, de %d en %d: %s" % (g, g, _fm_lista(r["lista"])))
    L.append("  y miro cuales son tambien multiplos de %d (se reparten en grupos de %d sin que sobre):" % (p, p))
    comunes = []
    for v in r["lista"]:
        res, _ = _fm_divide(v, p, saber)
        if res not in ("si", "no"):
            return "\n".join(L + ["  TODAVIA NO: no se mirar si %d se divide entre %d" % (v, p), "", "RESULTADO: todavia_no"])
        if res == "si":
            comunes.append(v)
    L.append("     %s" % (_fm_lista(comunes) if comunes else "ninguno de estos"))
    if comunes:
        L.append("  el MAS PEQUENO de los comunes: %d  (y siguen: los comunes son multiplos de %d)" % (comunes[0], comunes[0]))
    return "\n".join(L + ["", "RESULTADO: %s" % (_fm_lista(comunes) or "ninguno")])


def explicar_factores_primos(n, saber):
    L = ["PREGUNTA (M.15): los FACTORES PRIMOS de %d  (NCETM 2.21, punto 4: un factor que ademas es primo)" % n, ""]
    r = decidir_factores(n, saber)
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["  TODAVIA NO: %s" % r.get("porque"), "", "RESULTADO: todavia_no"])
    L.append("  los factores de %d: %s" % (n, _fm_lista(r["factores"])))
    primos = []
    for f in r["factores"]:
        p = decidir_primo(f, saber)
        if p["conclusion"] != "hecho":
            return "\n".join(L + ["  TODAVIA NO: no se si %d es primo" % f, "", "RESULTADO: todavia_no"])
        L.append("     %d: %s" % (f, {"primo": "PRIMO", "compuesto": "compuesto",
                                     "ni_primo_ni_compuesto": "ni primo ni compuesto (el 1)"}[p["valor"]]))
        if p["valor"] == "primo":
            primos.append(f)
    L.append("  los factores primos: %s" % (_fm_lista(primos) or "ninguno"))
    return "\n".join(L + ["", "RESULTADO: %s" % (_fm_lista(primos) or "ninguno")])


def explicar_con_100(a, b, saber):
    L = ["PREGUNTA (M.15): %d x %d con LAS PAREJAS DE 100  (NCETM 2.21, punto 6: 4 x 25, 2 x 50, 5 x 20)" % (a, b), ""]
    r = aplicar("multiplicar_con_las_parejas_de_100", {"a": a, "b": b}, saber)
    if r["conclusion"] != "hecho":
        L.append("  NO ENCAJA: %s" % "; ".join(_fm_porques(r) if r["conclusion"] != "ninguna"
                                                  else [r["candidatos"][0].get("descartado", "")]))
        return "\n".join(L + ["", "RESULTADO: no_encaja"])
    res = r["resultado"]
    L.append("  %s" % res["cuenta"])
    L.append("  COMPRUEBO deshaciendo: %s ... SI" % res["vuelta"])
    return "\n".join(L + ["", "RESULTADO: %d" % res["valor"]])


# ---------------------------------------------------------------- la puerta

def explicar_orden_factores(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    t = _fm_limpio(texto)
    m = _FM_PRIMOS_DE.match(t)
    if m:
        return explicar_factores_primos(int(m.group(1)), saber)
    m = _FM_COMUNES.match(t)
    if m:
        f = explicar_factores_comunes if m.group(1) == "factores" else explicar_multiplos_comunes
        return f(int(m.group(2)), int(m.group(3)), saber)
    m = _FM_FACTORES.match(t)
    if m:
        return explicar_factores(int(m.group(1)), saber)
    m = _FM_PRIMO.match(t)
    if m:
        return explicar_primo(int([g for g in m.groups() if g][0]), saber)
    m = _FM_CRIBA.match(t)
    if m:
        return explicar_criba(int(m.group(1)), saber)
    m = _FM_MULTIPLOS.match(t)
    if m:
        return explicar_multiplos(int(m.group(1)), int(m.group(2)) if m.group(2) else None, saber)
    m = _FM_ES.match(t)
    if m:
        return explicar_es_multiplo(int(m.group(1)), m.group(2), int(m.group(3)), saber)
    m = _FM_CON100.match(t)
    if m:
        return explicar_con_100(int(m.group(1)), int(m.group(2)), saber)
    return ("NO ENTIENDO ESTO: se escribe asi:  factores: 36    primo: 37    primos hasta 100    multiplos de 7\n"
            "   91 es multiplo de 7    7 es factor de 91    factores comunes: 24 y 36    multiplos comunes: 4 y 6\n"
            "   factores primos: 60    con 100: 25 x 36")
