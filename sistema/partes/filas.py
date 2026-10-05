# -*- coding: utf-8 -*-
"""
Euclides - FILAS Y COLUMNAS COMO SUMAS IGUALES (paso M.0 del plan pedagogico, 5 oct 2026).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

Common Core 2.OA.C.4: 'usar la suma para hallar el total de objetos colocados en filas y columnas
(hasta 5 y 5); escribir el total como una suma de sumandos iguales'.  Se DIBUJA (pictorico, CPA),
se escribe la suma de iguales, y la hacen las piezas de 'suma_de_iguales'.  Se cuenta tambien por
columnas: es la misma coleccion (la propiedad, 3 x 4 = 4 x 3, es de mas adelante: NCETM 2.3).
"""

import re

_ORDEN_FILAS = re.compile(r"^(\d+)\s+(filas?|columnas?)\s+de\s+(\d+)\s*$")
_POR = re.compile(r"^\d+\s*[x×*]\s*\d+$")


def _repetir(n, veces, saber):
    """'4 + 4 + 4' (texto): se escribe el 4 tantas veces como dice 'veces', recitando."""
    trozos, marca = [], "cero"
    while marca != decir(veces, saber):
        trozos.append(str(n))
        marca = siguiente(marca, saber)
    return " + ".join(trozos)


def _dibujo(filas, columnas, saber):
    lineas, f = [], "cero"
    while f != decir(filas, saber):
        lineas.append("        " + " ".join("o" for _ in levantar_dedos(decir(columnas, saber), saber) or []))
        f = siguiente(f, saber)
    return lineas


def leer_filas(texto):
    t = " ".join(texto.lower().replace(":", " ").split())
    m = _ORDEN_FILAS.match(t)
    if not m:
        return None
    a, que, b = int(m.group(1)), m.group(2), int(m.group(3))
    return (a, b) if que.startswith("fila") else (b, a)          # (filas, de cuantos cada fila)


def decidir_filas(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    t = " ".join(texto.lower().split())
    if _POR.match(t):
        return {"conclusion": "todavia_no", "porque": "todavia no se multiplicar (eso es el paso M.1); "
                "pero si me lo dices como filas lo hago: '3 filas de 4'"}
    fc = leer_filas(t)
    if fc is None:
        return {"conclusion": "no_entiendo"}
    filas, columnas = fc
    if levantar_dedos(decir(filas, saber), saber) is None or levantar_dedos(decir(columnas, saber), saber) is None:
        return {"conclusion": "no_entiendo", "porque": "dibujo hasta 10 filas y 10 columnas"}
    por_filas = aplicar("suma_de_iguales", {"veces": filas, "n": columnas}, saber)
    por_columnas = aplicar("suma_de_iguales", {"veces": columnas, "n": filas}, saber)
    return {"conclusion": "hecho", "filas": filas, "columnas": columnas,
            "por_filas": por_filas, "por_columnas": por_columnas, "valor": por_filas["valor"],
            "igual": por_filas["valor"] == por_columnas["valor"],
            "suma_filas": _repetir(columnas, filas, saber), "suma_columnas": _repetir(filas, columnas, saber),
            "dibujo": _dibujo(filas, columnas, saber),
            "pasa_del_estandar": viene_despues(decir(filas, saber), "cinco", saber)
            or viene_despues(decir(columnas, saber), "cinco", saber)}


def explicar_filas(texto, saber=None):
    r = decidir_filas(texto, saber)
    if r["conclusion"] == "todavia_no":
        return "PREGUNTA: %s\n\n  %s\n\nRESULTADO: todavia_no" % (texto.strip(), r["porque"])
    if r["conclusion"] == "no_entiendo":
        return ("NO ENTIENDO ESTO: %s\n   se escribe asi:  3 filas de 4     (o  3 columnas de 4)"
                % r.get("porque", "dime cuantas filas y de cuantos cada una"))
    f, c = r["filas"], r["columnas"]
    L = ["PREGUNTA (M.0): %d %s de %d: cuantos hay en total?" % (f, "fila" if f == 1 else "filas", c), ""]
    if r["pasa_del_estandar"]:
        L.append("  (el estandar, 2.OA.C.4, llega a 5 filas y 5 columnas; lo hago igual)")
    L.append("  1. LO DIBUJO (cada fila es un grupo IGUAL de %d):" % c)
    L.extend(r["dibujo"] or ["        (no hay ninguna fila)"])
    L.append("")
    pf = r["por_filas"]
    L.append("  2. POR FILAS: %s" % (r["suma_filas"] or "0"))
    L.append("     con %s:\n        %s" % (pf["pieza"]["nombre"], pf["resultado"]["cuenta"].replace("; ", "\n        ")))
    pc = r["por_columnas"]
    L.append("")
    L.append("  3. POR COLUMNAS (la misma coleccion, contada de otra manera): %s" % (r["suma_columnas"] or "0"))
    L.append("     con %s:\n        %s" % (pc["pieza"]["nombre"], pc["resultado"]["cuenta"].replace("; ", "\n        ")))
    L.append("     -> %s" % ("da lo mismo: %d" % r["valor"] if r["igual"] else "NO DA LO MISMO (algo va mal)"))
    L.append("")
    L.append("  LA SUMA DE IGUALES (2.OA.C.4): %s = %d" % (r["suma_filas"] or "0", r["valor"]))
    L.append("")
    L.append("RESULTADO: %d" % r["valor"])
    return "\n".join(L)
