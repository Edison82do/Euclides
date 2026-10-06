# -*- coding: utf-8 -*-
"""
Euclides - LA MEMORIA DE HECHOS (paso 3 del plan, 5 oct 2026).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

LA DECISION DE CARLOS: "en el camino el ser humano memoriza algunos datos y utiliza tecnicas para
agilizar la solucion de problemas; eso es valido aqui, segun va avanzando el aprendizaje".

LA PEDAGOGIA: la memoria llega DESPUES del razonamiento, no en su lugar.  Las fases de Baroody:
contar -> razonar (hechos derivados) -> dominio.  "Fact fluency leads to memorization down the road,
but it doesn't start there."  Y lo que se espera saber de memoria al final de 2.o grado (Common
Core 2.OA.B.2): "know from memory all sums of two one-digit numbers" (y sus restas, hasta 20).

ASI QUE LA MEMORIA SE GANA:
  - Un hecho solo entra si el sistema lo ha CALCULADO con el mecanismo (sin memoria), lo ha
    COMPROBADO por la vuelta, y -- si hay otro metodo que tambien sirve -- por un SEGUNDO camino.
  - Cada hecho guarda COMO se aprendio y cuando.  Nada se escribe a mano.
  - Las restas se aprenden como FAMILIA de la suma (8 + 5 = 13 -> 13 - 5 = 8 y 13 - 8 = 5), y se
    comprueban tambien restando de verdad.
  - Recordar no se salta la comprobacion: la pieza 'recordar' vuelve a comprobar por la vuelta, y
    si un recuerdo no cuadra, NO se usa (se calcula por el camino largo y se dice).

El archivo: conocimiento/memoria/hechos.txt   (una linea por hecho, legible)
"""

import os
import sys  # noqa: F401
import time

_CACHE_MEMORIA = {}


def ruta_memoria():
    return os.environ.get("EUCLIDES_MEMORIA") or \
        os.path.join(RAIZ, "conocimiento", "memoria", "hechos.txt")


def cargar_memoria(ruta=None):
    """{"8 + 5": {"valor": 13, "como": ..., "comprobado": ..., "fecha": ...}, ...}"""
    ruta = ruta or ruta_memoria()
    if not os.path.exists(ruta):
        return {}
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()
    # la firma es el TEXTO entero (la hora del archivo no basta: un cambio en el mismo instante y
    # del mismo largo, como 13 -> 14, no se veria)
    g = _CACHE_MEMORIA.get(ruta)
    if g and g[0] == texto:
        return g[1]
    firma = texto
    hechos = {}
    for linea in texto.splitlines():
        s = linea.strip()
        if not s or s.startswith("#"):
            continue
        partes = [p.strip() for p in s.split("|")]
        cuenta, _, valor = partes[0].partition("=")
        try:
            hechos[cuenta.strip()] = {"valor": int(valor.strip()),
                                      "como": partes[1] if len(partes) > 1 else "?",
                                      "comprobado": partes[2] if len(partes) > 2 else "?",
                                      "fecha": partes[3] if len(partes) > 3 else "?"}
        except ValueError:
            continue
    _CACHE_MEMORIA[ruta] = (firma, hechos)
    return hechos


_CABECERA = """# LA MEMORIA DE EUCLIDES - los hechos que ha APRENDIDO (paso 3 del plan)
# No se escribe a mano: lo escribe el sistema cuando aprende (orden 'aprender: sumas').
# Cada linea:   el hecho | como lo calculo | como lo comprobo | cuando
# Para empezar de cero: orden 'olvidar: todo'.
"""


def _escribir(hechos, ruta):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    def orden(k):
        a, op, b = k.split()
        return (op, int(a), int(b))
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(_CABECERA)
        for k in sorted(hechos, key=orden):
            h = hechos[k]
            f.write("%s = %d | %s | %s | %s\n" % (k, h["valor"], h["como"], h["comprobado"], h["fecha"]))


def _cifras_de_una(saber):
    """cero, uno ... nueve: recitando."""
    out, p = [], "cero"
    while True:
        out.append(leer(p, saber))
        if p == "nueve":
            return out
        p = siguiente(p, saber)


def aprender(que, saber=None, ruta=None):
    """
    Practica y aprende: 'sumas' (las 100 sumas de dos numeros de una cifra) o 'restas' (sus
    restas: la familia de cada suma).  Devuelve {"nuevos", "ya_sabia", "rechazados", "detalle"}.
    """
    if saber is None:
        saber = cargar_conocimiento()
    ruta = ruta or ruta_memoria()
    hechos = dict(cargar_memoria(ruta))
    hoy = time.strftime("%Y-%m-%d")
    res = {"que": que, "nuevos": [], "ya_sabia": [], "rechazados": [], "dos_caminos": 0}
    if que == "tablas":
        return _aprender_tablas(saber, ruta, hechos, hoy, res)
    digitos = _cifras_de_una(saber)
    for a in digitos:
        for b in digitos:
            if que == "sumas":
                clave, sit, op = "%d + %d" % (a, b), {"a": a, "b": b, "sin_memoria": True}, "sumar"
            else:
                # la familia: (a + b) - b = a.  La suma de la que sale se calcula SIN memoria.
                s = aplicar("sumar", {"a": a, "b": b, "sin_memoria": True}, saber)
                if s["conclusion"] != "hecho":
                    continue
                total = s["valor"]
                clave, sit, op = "%d - %d" % (total, b), {"a": total, "b": b, "sin_memoria": True}, "restar"
            if clave in hechos:
                res["ya_sabia"].append(clave)
                continue
            r = aplicar(op, sit, saber)
            if r["conclusion"] != "hecho" or not r["resultado"].get("vuelta_ok"):
                res["rechazados"].append((clave, "no salio o no cuadro la vuelta"))
                continue
            valor = r["valor"]
            comprobado = "la vuelta (%s)" % r["resultado"].get("vuelta")
            if r.get("tambien_servian"):
                otro = aplicar(r["tambien_servian"][0], sit, saber)
                if otro["conclusion"] != "hecho" or otro["valor"] != valor:
                    res["rechazados"].append((clave, "dos caminos dan cosas distintas"))
                    continue
                comprobado += " y otro camino (%s)" % otro["resultado"]["metodo"]
                res["dos_caminos"] += 1
            if op == "restar":
                comprobado += " y es de la familia de %d + %d = %d" % (a, b, total)
                if valor != a:
                    res["rechazados"].append((clave, "no cuadra con su suma"))
                    continue
            hechos[clave] = {"valor": valor, "como": r["resultado"]["metodo"],
                             "comprobado": comprobado, "fecha": hoy}
            res["nuevos"].append(clave)
    _escribir(hechos, ruta)
    res["total_en_memoria"] = len(hechos)
    return res


TABLAS_ENSENADAS = (2, 4, 8, 3, 6, 9, 5, 10, 7)   # M.2: 2, 5, 10;  M.4: 4, 8;  M.5: 3, 6, 9;  M.6: 7 (partiendo)


def _aprender_tablas(saber, ruta, hechos, hoy, res):
    """M.2 y M.4: las tablas del 2, 4, 8, 5 y 10 (0 a 10 grupos, en las dos lecturas).  Cada producto
    se CALCULA sin memoria y se COMPRUEBA con la otra lectura de los grupos (la conmutativa)."""
    factores = _cifras_de_una(saber) + [10]
    for t in TABLAS_ENSENADAS:                 # en orden: la del 4 se saca de la del 2, la del 8 de la del 4
        for k in factores:
            for a, b in ((k, t), (t, k)):
                clave = "%d x %d" % (a, b)
                if clave in res["nuevos"]:                 # 2 x 5 sale en la tabla del 2 y en la del 5
                    continue
                if clave in hechos:
                    if clave not in res["ya_sabia"]:
                        res["ya_sabia"].append(clave)
                    continue
                r = aplicar("multiplicar", {"a": a, "b": b, "sin_memoria": True}, saber)
                otra = aplicar("suma_de_iguales", {"veces": b, "n": a}, saber)
                if r["conclusion"] != "hecho" or otra["conclusion"] != "hecho" or otra["valor"] != r["valor"]:
                    res["rechazados"].append((clave, "las dos lecturas no dan lo mismo"))
                    continue
                hechos[clave] = {"valor": r["valor"], "como": r["resultado"]["metodo"],
                                 "comprobado": "la otra lectura (%d grupos de %d = %d)" % (b, a, otra["valor"]),
                                 "fecha": hoy}
                res["nuevos"].append(clave)
                res["dos_caminos"] += 1
        _escribir(hechos, ruta)                # al acabar cada tabla: la siguiente ya la puede usar (doblar)
    _escribir(hechos, ruta)
    res["total_en_memoria"] = len(hechos)
    return res


def olvidar_todo(ruta=None):
    ruta = ruta or ruta_memoria()
    _escribir({}, ruta)


def explicar_memoria(saber=None):
    hechos = cargar_memoria()
    L = ["PREGUNTA: que se DE MEMORIA?  (conocimiento/memoria/hechos.txt)", ""]
    sumas = sorted(k for k in hechos if "+" in k)
    restas = sorted(k for k in hechos if "-" in k)
    productos = sorted(k for k in hechos if "x" in k)
    L.append("  sumas que se de memoria:  %d   restas: %d   productos (tablas): %d"
             % (len(sumas), len(restas), len(productos)))
    for k in [x for grupo in (sumas, restas, productos) for x in grupo[:3]]:
        h = hechos[k]
        L.append("    %s = %d   aprendido con %s el %s;  comprobado por %s"
                 % (k, h["valor"], h["como"], h["fecha"], h["comprobado"]))
    if not hechos:
        L.append("  (no se nada de memoria todavia: todo lo calculo.  Para aprender: 'aprender: sumas')")
    L.append("")
    L.append("  LA MEMORIA SE GANA: un hecho solo entra despues de calcularlo SIN memoria, comprobarlo")
    L.append("  por la vuelta y, si se puede, por un segundo camino.  Y cuando lo uso, lo vuelvo a")
    L.append("  comprobar: si un recuerdo no cuadra, no lo uso.")
    L.append("")
    L.append("RESULTADO: %d hechos" % len(hechos))
    return "\n".join(L)


def explicar_aprender(que, saber=None):
    que = que.strip().lower()
    if que not in ("sumas", "restas", "tablas"):
        return ("NO ENTIENDO ESTO: se puede aprender 'sumas' o 'restas' (hasta 20), o 'tablas' (del 2, 5 y 10).\n"
                "   se escribe asi:  aprender: sumas")
    r = aprender(que, saber)
    if que == "tablas":
        L = ["PREGUNTA: aprender las TABLAS del %s (de 0 a 10 grupos, en las dos lecturas)"
             % ", ".join(str(t) for t in TABLAS_ENSENADAS), "",
             "  EN ORDEN: la del 4 se saca DOBLANDO la del 2, y la del 8 doblando la del 4 (NCETM 2.7);",
             "  la del 6 doblando la del 3, y la del 9 TRIPLICANDO la del 3 (NCETM 2.8);",
             "  y la del 7 PARTIENDO: 7 = 5 + 2 (la distributiva, NCETM 2.10).",
             "  CALCULO cada producto SIN memoria y lo compruebo con la OTRA LECTURA de los grupos",
             "  (3 x 5 son 3 grupos de 5; y 5 grupos de 3 tienen que dar lo mismo: NCETM 2.3).", "",
             "  nuevos en la memoria:    %d" % len(r["nuevos"]),
             "  ya los sabia:            %d" % len(r["ya_sabia"]),
             "  rechazados:              %d %s" % (len(r["rechazados"]), r["rechazados"][:3] or ""), "",
             "RESULTADO: %d hechos en la memoria" % r["total_en_memoria"]]
        return "\n".join(L)
    L = ["PREGUNTA: aprender las %s hasta 20 (las de dos numeros de una cifra)" % que, ""]
    L.append("  PRACTICO cada una SIN memoria, con el metodo mas corto que tengo, la compruebo por la")
    L.append("  vuelta y, si hay otro metodo que tambien sirve, la hago tambien por ese.")
    L.append("")
    L.append("  nuevas en la memoria:    %d" % len(r["nuevos"]))
    L.append("  ya las sabia:            %d" % len(r["ya_sabia"]))
    L.append("  comprobadas por 2 caminos: %d" % r["dos_caminos"])
    L.append("  rechazadas:              %d %s" % (len(r["rechazados"]), r["rechazados"][:3] or ""))
    L.append("")
    L.append("RESULTADO: %d hechos en la memoria" % r["total_en_memoria"])
    return "\n".join(L)
