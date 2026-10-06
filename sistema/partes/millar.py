# -*- coding: utf-8 -*-
"""
Euclides - EL MILLAR Y LOS NUMEROS DE CUATRO CIFRAS (paso N.3 del plan pedagogico, 6 oct 2026; 4.o).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

NCETM 1.22 (Year 4): diez centenas hacen mil; los numeros de mas de mil tienen una estructura que va
con su tamano (ordenar, componer, descomponer); lo de tres cifras sirve para cuatro.
Common Core 4.NBT.A.1-3.  Conocimiento: conocimiento/el_millar.kn.
Como en la 6.7: los nombres se CONSTRUYEN con la regla y la lista de contar llega a diez mil.
"""

import re

_ORDEN_MILLAR = re.compile(r"^millar:?\s*(\d+)$")
_ORDEN_COMPARAR_NUM = re.compile(r"^comparar:?\s*(\d+)\s*(?:y|,|con|\?)\s*(\d+)$")
_SITIOS_NOMBRE = ("unidades", "decenas", "centenas", "millares", "decenas de millar")
_SITIO_UNO = ("unidad", "decena", "centena", "millar", "decena de millar")


def _millares(saber):
    d = saber.get("el_millar") or {}
    out = {}
    for k, v in (d.get("millares") or {}).items():
        try:
            out[int(k)] = v
        except (TypeError, ValueError):
            pass
    return out


def construir_nombre_hasta_diez_mil(n, saber):
    """El nombre de un numero del 1 al 10000, CONSTRUIDO: 'dos mil' + el nombre de lo que queda.
    Hasta mil delega en la 6.7 (misma verdad).  None fuera del 1..10000."""
    if n is None or n < 1 or n > 10000:
        return None
    if n <= 1000:
        return construir_nombre_hasta_mil(n, saber)
    if n == 10000:
        return (saber.get("el_millar") or {}).get("techo_nombre") or "diez mil"
    cif = cifras_de(n)
    mil = _millares(saber).get(cif[3])
    resto = escribir_cifras(cif[:3])
    if not mil:
        return None
    if resto == 0:
        return mil
    nombre_resto = construir_nombre_hasta_mil(resto, saber)
    return "%s %s" % (mil, nombre_resto) if nombre_resto else None


def _secuencia_hasta_diez_mil(saber):
    """Los 10000 nombres, en orden, construidos con la regla (paso N.3, que sube el techo)."""
    return [construir_nombre_hasta_diez_mil(n, saber) for n in range(1, 10001)]


# ---------------------------------------------------------------- millar: 3045

def decidir_millar(n, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    if decir(n, saber) is None:
        return {"conclusion": "todavia_no", "porque": "%d pasa de diez mil: eso es de 5.o (NCETM 1.26)" % n}
    cif = cifras_de(n)
    while len(cif) < 4:
        cif.append(0)
    sitios = []
    for i, c in enumerate(cif):
        valor = escribir_cifras([0 for _ in range(i)] + [c])            # la cifra con sus ceros detras
        sitios.append({"sitio": _SITIOS_NOMBRE[i], "cifra": c, "vale": valor})
    # cuantas hay de cada (no solo sueltas): se TAPAN las cifras de la derecha (204 tiene 20 decenas)
    cuantas = {}
    for i, nombre in enumerate(_SITIOS_NOMBRE[:4]):
        cuantas[nombre] = escribir_cifras(cif[i:])
    return {"conclusion": "hecho", "n": n, "sitios": sitios, "cuantas": cuantas,
            "nombre": decir(n, saber) if n else "cero"}


def explicar_millar(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    m = _ORDEN_MILLAR.match(" ".join(texto.lower().split()))
    if not m:
        return "NO ENTIENDO ESTO: se escribe asi:  millar: 3045"
    n = int(m.group(1))
    r = decidir_millar(n, saber)
    L = ["PREGUNTA (N.3): como esta hecho %d?  (NCETM 1.22; 4.NBT.A.2)" % n, ""]
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["  TODAVIA NO: %s" % r["porque"], "", "RESULTADO: todavia_no"])
    s = r["sitios"]
    L.append("  1. CADA CIFRA EN SU SITIO (la posicion dice el valor):")
    for x in reversed(s):
        L.append("        %-10s %d  -> vale %d" % (x["sitio"], x["cifra"], x["vale"]))
    sumandos = [str(x["vale"]) for x in reversed(s) if x["cifra"]]
    L.append("     %d = %s" % (n, " + ".join(sumandos) if sumandos else "0"))
    L.append("")
    L.append("  2. CUANTAS HAY DE CADA (no solo las sueltas): se tapan las cifras de la derecha")
    for nombre in ("millares", "centenas", "decenas", "unidades"):
        L.append("        %-10s %d" % (nombre, r["cuantas"][nombre]))
    for x in s[1:3]:
        if x["cifra"] == 0 and r["cuantas"][x["sitio"]]:
            L.append("     OJO: la cifra de las %s es 0, pero hay %d %s (el cero solo dice que no hay %s SUELTAS)."
                     % (x["sitio"], r["cuantas"][x["sitio"]], x["sitio"], x["sitio"]))
    if n == 1000:
        L.append("")
        L.append("  3. MIL: 10 centenas = 100 decenas = 1000 unidades.  Y multiplicando (NCETM 1.22):")
        for a, b in ((2, 500), (4, 250), (5, 200)):
            v = aplicar("multiplicar", {"a": a, "b": b}, saber).get("valor")
            L.append("        %d x %d = %s" % (a, b, v))
    L += ["", "  se lee: %s" % r["nombre"], "", "RESULTADO: %s" % " + ".join(sumandos) if sumandos else "RESULTADO: 0"]
    return "\n".join(L)


# ---------------------------------------------------------------- comparar: 3456 y 3465

def decidir_comparar_numeros(a, b, saber=None):
    """4.NBT.A.2: comparar MIRANDO LAS CIFRAS.  Mas cifras, mayor; si no, de izquierda a derecha, la
    primera distinta decide.  Se comprueba con el orden de la lista (el que viene despues es mayor)."""
    if saber is None:
        saber = cargar_conocimiento()
    ca, cb = cifras_de(a), cifras_de(b)
    r = {"a": a, "b": b}
    la, lb = decir(len(ca), saber), decir(len(cb), saber)
    if la != lb:
        a_mas = viene_despues(la, lb, saber)
        r.update(valor=">" if a_mas else "<", como="%d tiene %s cifras y %d tiene %s: el de MAS cifras es mayor"
                 % (a, la, b, lb))
    else:
        r["valor"], r["como"] = "=", "las mismas cifras en todos los sitios: son iguales"
        izq_a, izq_b = list(reversed(ca)), list(reversed(cb))
        sitios = list(reversed(_SITIOS_NOMBRE[:len(ca)]))
        for x, y, sitio in zip(izq_a, izq_b, sitios):
            if x != y:
                a_mas = viene_despues(decir(x, saber), decir(y, saber), saber)
                r["valor"] = ">" if a_mas else "<"
                r["como"] = ("las dos tienen %s cifras; de izquierda a derecha la primera distinta es la de %s "
                             "%s: %d contra %d" % (la, "los" if sitio.startswith(("millares", "decenas de")) else "las",
                                                   sitio, x, y))
                break
    # el segundo camino: el orden de la lista
    pa, pb = decir(a, saber), decir(b, saber)
    if pa is not None and pb is not None:
        lista = "=" if a == b else (">" if viene_despues(pa, pb, saber) else "<")
        r["lista"] = lista
        r["lista_ok"] = lista == r["valor"]
    r["conclusion"] = "hecho"
    return r


def explicar_comparar_numeros(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    m = _ORDEN_COMPARAR_NUM.match(" ".join(texto.lower().split()))
    a, b = int(m.group(1)), int(m.group(2))
    r = decidir_comparar_numeros(a, b, saber)
    L = ["PREGUNTA (N.3): cual es mayor, %d o %d?  (4.NBT.A.2: mirando las cifras)" % (a, b), ""]
    L.append("  1. POR LAS CIFRAS: %s  ->  %d %s %d" % (r["como"], a, r["valor"], b))
    if "lista" in r:
        L.append("  2. COMPRUEBO con la lista de contar (el que viene despues es mayor): %d %s %d ... %s"
                 % (a, r["lista"], b, "SI" if r["lista_ok"] else "NO"))
    L += ["", "RESULTADO: %d %s %d" % (a, r["valor"], b)]
    return "\n".join(L)


def es_comparar_numeros(texto):
    return bool(_ORDEN_COMPARAR_NUM.match(" ".join(texto.lower().split())))
