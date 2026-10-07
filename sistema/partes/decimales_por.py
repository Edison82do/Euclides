# -*- coding: utf-8 -*-
"""
Euclides - MULTIPLICAR Y DIVIDIR DECIMALES POR NUMEROS ENTEROS (paso M.13 del plan pedagogico, 7 oct 2026; 5.o).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

NCETM 2.19 (Calculation: x/: decimal fractions by whole numbers); Common Core 5.NBT.B.7.
  punto 1: 4 x 0.7 = 4 x 7 decimas = 28 decimas = 2.8 (los hechos que se saben, contando en decimas);
  punto 2: x 0.1 es : 10, x 0.01 es : 100 (las cifras bajan de sitio);
  punto 3: 3.27 x 4 -> 327 x 4 = 1308 -> 13.08 (pasar a entero, la cuenta, ajustar);
  punto 4: por menos de uno sale MENOS; por mas de uno, MAS;
  punto 5: 7.2 : 3 -> 72 : 3 = 24 -> 2.4 (entre un numero de una cifra).
Las cuentas las hacen las piezas multiplicar_decimal_contando_partes, multiplicar_por_una_decima,
dividir_decimal_contando_partes y dividir_decimal_por_10_o_100.  Aqui solo se lee la orden, se pregunta
a las piezas y se explica (con el tamano del punto 4 y otro camino, por partes, para comprobar).
"""

import re

_DP_NUM = r"\d+(?:[.,]\d+)?"
_DP_ORDEN = re.compile(r"^(?:calcular:?\s*)?(" + _DP_NUM + r")\s*([x*×:÷])\s*(" + _DP_NUM + r")$")


def _dp_limpio(texto):
    return " ".join(texto.lower().strip().rstrip("?").split())


def es_orden_decimal_por(texto):
    t = _dp_limpio(texto)
    m = _DP_ORDEN.match(t)
    return bool(m) and bool(re.search(r"\d[.,]\d", t))


def _dp_normal(texto):
    """'0.10' -> '0.1';  '4.0' -> '4';  '007' -> '7'.  Leer las cifras y volver a escribirlas (D.2)."""
    k = len(_dec_leer(texto)[1])
    return _dec_escribir(_dec_en_pequenas(texto, k), k)


def _dp_porque(r):
    """El porque de un 'no' de aplicar(): el de la pieza que mas se acerco."""
    for f in r.get("candidatos", []):
        if f.get("no_salio"):
            return f["no_salio"]
    for f in reversed(r.get("candidatos", [])):
        if f.get("descartado"):
            return f["descartado"]
    return r.get("porque") or r["conclusion"]


def decidir_decimal_por(a, signo, b, saber=None):
    """a x b  (uno decimal y otro entero) o  a : b  (a decimal, b entero).  Devuelve un dict con
    conclusion (hecho | todavia_no | imposible), valor (texto) y lo que hizo la pieza."""
    if saber is None:
        saber = cargar_conocimiento()
    a, b = a.replace(",", "."), b.replace(",", ".")
    p = _dec_problema(a, b)
    if p:
        return {"conclusion": p[0], "porque": p[1]}
    x, y = _dp_normal(a), _dp_normal(b)
    if signo == ":":
        if "." in y:
            return {"conclusion": "todavia_no", "porque": "dividir ENTRE un decimal es de mas adelante (6.o); "
                                                          "en 5.o se divide un decimal entre un entero (NCETM 2.19)"}
        if y == "0":
            return {"conclusion": "imposible", "porque": "entre cero no se puede repartir (M.3)"}
        r = aplicar("dividir_decimal", {"x": x, "d": y}, saber)
    else:
        if "." in x and "." in y and "0.1" not in (x, y) and "0.01" not in (x, y):
            return {"conclusion": "todavia_no", "porque": "un decimal por otro decimal es de 6.o (aqui: un decimal "
                                                          "por un entero, o cualquier numero por 0.1 o 0.01)"}
        if "0" in (x, y):
            otro = y if x == "0" else x
            k = len(_dec_leer(otro)[1])
            r0 = aplicar("multiplicar", {"a": _dec_en_pequenas(otro, k), "b": 0}, saber)
            return {"conclusion": "hecho", "valor": "0", "metodo": r0["pieza"]["nombre"] if r0.get("pieza") else "",
                    "pasos": ["POR CERO: ninguna vez %s, o cero %s: no hay nada (M.2)" % (otro, _DEC_NOMBRE.get(k, ("", "unidades"))[1])],
                    "vuelta": "", "pieza": "por cero", "x": x, "y": y}
        if "." not in x and "." not in y:
            # '33.0 x 7': escrito sin ceros de mas son dos enteros (D.2: un cero al final no cambia nada)
            ra = aplicar("multiplicar", {"a": _dec_en_pequenas(x, 0), "b": _dec_en_pequenas(y, 0)}, saber)
            if ra["conclusion"] != "hecho":
                return {"conclusion": "todavia_no", "porque": _dp_porque(ra)}
            return {"conclusion": "hecho", "valor": str(ra["valor"]), "metodo": ra["resultado"]["metodo"],
                    "pasos": ["SIN CEROS DE MAS: %s x %s = %s x %s, dos enteros: %d  (%s)"
                              % (a, b, x, y, ra["valor"], ra["resultado"]["metodo"])],
                    "vuelta": ra["resultado"].get("vuelta", ""), "pieza": "enteros", "x": x, "y": y}
        r = aplicar("multiplicar_decimal", {"x": x, "y": y}, saber)
    if r["conclusion"] != "hecho":
        return {"conclusion": "todavia_no", "porque": _dp_porque(r)}
    res = r["resultado"]
    return {"conclusion": "hecho", "valor": r["valor"], "metodo": res["metodo"], "pasos": res.get("pasos", []),
            "vuelta": res.get("vuelta", ""), "pieza": r["pieza"]["id"], "x": x, "y": y, "res": res}


def _dp_por_partes(dec, n, saber):
    """Otro camino (5.NBT.B.7: la distributiva): 3.27 x 4 = 3 x 4 + 0.27 x 4.  Devuelve las lineas o []."""
    e, d = _dec_leer(dec)
    if e == "0" or not d.strip("0"):
        return []
    ent = escribir_cifras([int(c) for c in reversed(e)])
    trozo = "0.%s" % d
    r1 = aplicar("multiplicar", {"a": ent, "b": escribir_cifras([int(c) for c in reversed(n)])}, saber)
    r2 = aplicar("multiplicar_decimal", {"x": trozo, "y": n}, saber)
    if r1["conclusion"] != "hecho" or r2["conclusion"] != "hecho":
        return []
    s = decidir_cuenta_decimal(str(r1["valor"]), "+", r2["valor"], saber)
    if s["conclusion"] != "hecho":
        return []
    return [r1["valor"], trozo, r2["valor"], s["valor"]]


def explicar_orden_decimal_por(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    m = _DP_ORDEN.match(_dp_limpio(texto))
    if not m:
        return "NO ENTIENDO ESTO: se escribe asi:  0.3 x 4    4 x 2.35    35 x 0.1    7.2 : 3    3.5 : 10"
    a, op, b = m.group(1).replace(",", "."), m.group(2), m.group(3).replace(",", ".")
    signo = ":" if op in ":÷" else "x"
    L = ["PREGUNTA (M.13): %s %s %s  (NCETM 2.19; 5.NBT.B.7: decimales por y entre enteros)" % (a, signo, b), ""]
    r = decidir_decimal_por(a, signo, b, saber)
    if r["conclusion"] != "hecho":
        etiqueta = {"imposible": "NO SE PUEDE"}.get(r["conclusion"], "TODAVIA NO")
        return "\n".join(L + ["  %s: %s" % (etiqueta, r["porque"]), "", "RESULTADO: %s" % r["conclusion"]])
    for i, paso in enumerate(r["pasos"]):
        L.append("  %d. %s" % (i + 1, paso))
    x, y, valor = r["x"], r["y"], r["valor"]
    if signo == "x" and r["pieza"] == "multiplicar_decimal_contando_partes":
        dec, ent = (x, y) if "." in x else (y, x)
        res = r["res"]
        k = len(_dec_leer(dec)[1])
        if k < 3:
            L.append("     OJO: son %s, no %s: el resultado NO es %s"
                     % (_dec_cuantas(res["en_pequenas"], k) if res["en_pequenas"] != 1 else "1 %s" % _DEC_NOMBRE[k][0],
                        _DEC_NOMBRE[k + 1][1], _dec_escribir(res["en_pequenas"], k + 1)))
        pp = _dp_por_partes(dec, ent, saber)
        if pp:
            L.append("  OTRO CAMINO, POR PARTES (la distributiva): %s x %s = %s x %s + %s x %s = %d + %s = %s ... %s"
                     % (dec, ent, _dec_leer(dec)[0], ent, pp[1], ent, pp[0], pp[2], pp[3],
                        "COINCIDE" if pp[3] == valor else "NO COINCIDE"))
            L.append("     (el entero y las %s NO se multiplican por separado para pegarlos: %s x %s son %s, que se SUMAN)"
                     % (_DEC_NOMBRE[k][1], pp[1], ent, pp[2]))
    if signo == "x" and r["pieza"] not in ("por cero", "enteros"):
        # EL TAMANO (NCETM 2.19, punto 4): por menos de uno sale menos; por mas de uno, mas
        if r["pieza"] == "multiplicar_por_una_decima":
            por, otro = (x, y) if x in ("0.1", "0.01") else (y, x)
        else:
            por, otro = (y, x) if "." in x else (x, y)
        c = decidir_comparar_decimales(por, "1", saber)["valor"]
        t = decidir_comparar_decimales(valor, otro, saber)["valor"]
        palabra = {"<": "MENOR", ">": "MAYOR", "=": "IGUAL"}
        L.append("  EL TAMANO (punto 4): %s es %s que uno, asi que el producto es %s que %s: %s %s %s"
                 % (por, {"<": "menor", ">": "mayor", "=": "igual"}[c], palabra[c], otro, valor, t, otro))
        if c != t:
            L.append("     NO CUADRA con el tamano: algo esta mal")
            return "\n".join(L + ["", "RESULTADO: no_cuadra"])
    if r["vuelta"]:
        L.append("  COMPRUEBO con la operacion contraria: %s ... SI" % r["vuelta"])
    L.append("     (%s)" % r["metodo"])
    L += ["", "RESULTADO: %s" % valor]
    return "\n".join(L)
