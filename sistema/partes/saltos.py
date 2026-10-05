# -*- coding: utf-8 -*-
"""
Euclides - CONTAR DE n EN n, y PAR O IMPAR (paso N.1 del plan pedagogico, 5 oct 2026).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

Common Core 2.NBT.A.2 ('contar de 5 en 5, de 10 en 10 y de 100 en 100') y 2.OA.C.3 (par o impar,
emparejando o contando de 2 en 2).  NCETM 2.1: 'podemos contar de forma eficiente en grupos de dos,
de cinco, de diez'.  El salto lo da el MECANISMO (saltar); aqui solo se lee la orden y se explica.
"""

import re

_DE = {"2": "dos", "5": "cinco", "10": "diez", "100": "cien"}
_ORDEN_SALTOS = re.compile(r"^de\s+(\d+)\s+en\s+(\d+)(?:\s+desde\s+(\d+))?(?:\s+hasta\s+(\d+))?\s*$")


def contar_de_en(de, desde, hasta, saber):
    """La serie de 'desde' saltando de 'de' (dos, cinco, diez, cien) hasta 'hasta' (o diez saltos).
    Devuelve {"serie": [...], "llega": True/False/None, "se_sale": True/False}."""
    serie, v, saltos = [], desde, "cero"
    while True:
        if hasta is None and saltos == "diez":
            return {"serie": serie, "llega": None, "se_sale": False}
        nuevo = saltar(v, de, saber)
        if nuevo is None:
            return {"serie": serie, "llega": False if hasta is not None else None, "se_sale": True}
        if hasta is not None and viene_despues(decir(nuevo, saber), decir(hasta, saber), saber):
            return {"serie": serie, "llega": False, "se_sale": False, "despues": nuevo}
        serie.append(nuevo)
        v = nuevo
        saltos = siguiente(saltos, saber)
        if hasta is not None and nuevo == hasta:
            return {"serie": serie, "llega": True, "se_sale": False}


def explicar_saltos(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    m = _ORDEN_SALTOS.match(" ".join(texto.lower().split()))
    if not m or m.group(1) != m.group(2) or m.group(1) not in _DE:
        return ("NO ENTIENDO ESTO: se puede contar de 2 en 2, de 5 en 5, de 10 en 10 o de 100 en 100.\n"
                "   se escribe asi:  de 5 en 5 hasta 50      o   de 10 en 10 desde 47 hasta 97")
    de = _DE[m.group(1)]
    desde = int(m.group(3)) if m.group(3) else 0
    hasta = int(m.group(4)) if m.group(4) else None
    for n in (desde, hasta):
        if n is not None and decir(n, saber) is None:
            return "NO ENTIENDO ESTO: solo se contar hasta mil."
    r = contar_de_en(de, desde, hasta, saber)
    como = ("se recita en voz baja con %s dedos y se dice en voz alta el ultimo" % de
            if de in ("dos", "cinco") else
            "no se cuentan %s pasos: se ESCRIBE la cifra de las %s (sube una)"
            % (de, "decenas" if de == "diez" else "centenas"))
    L = ["PREGUNTA (N.1): contar de %s en %s desde %d%s" % (m.group(1), m.group(1), desde,
                                                             "" if hasta is None else " hasta %d" % hasta),
         "  (cada salto: %s)" % como, ""]
    L.append("  %d, %s" % (desde, ", ".join(str(x) for x in r["serie"])))
    if r["llega"] is True:
        L.append("  -> llego justo al %d (%d saltos)" % (hasta, len(r["serie"])))
    elif r["llega"] is False and r.get("se_sale"):
        L.append("  -> no llego al %d: me salgo de mi lista (mil)" % hasta)
    elif r["llega"] is False:
        L.append("  -> el %d NO se toca saltando de %s en %s desde %d: del %s salto al %d"
                 % (hasta, m.group(1), m.group(1), desde, r["serie"][-1] if r["serie"] else desde, r["despues"]))
    elif r.get("se_sale"):
        L.append("  -> me paro: el siguiente salto pasa de mil")
    L.append("")
    L.append("RESULTADO: %s" % ", ".join(str(x) for x in r["serie"]))
    return "\n".join(L)


def decidir_paridad(n, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    return aplicar("paridad", {"n": n}, saber)


def explicar_paridad(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    t = texto.strip().rstrip("?").strip()
    if not t.isdigit() or decir(int(t), saber) is None:
        return ("NO ENTIENDO ESTO: dame un numero de 0 a 1000.\n"
                "   se escribe asi:  par: 14")
    n = int(t)
    r = decidir_paridad(n, saber)
    L = ["PREGUNTA (N.1): %d es PAR o IMPAR?  (par: se puede repartir en parejas sin que sobre ninguno)" % n, ""]
    elegida = r.get("pieza", {}).get("id")
    for f in r["candidatos"]:
        if f.get("descartado"):
            L.append("    [no]  %-34s porque %s" % (f["nombre"], f["descartado"]))
        elif f["id"] == elegida:
            L.append("    [SI]  %-34s <- el mas corto que encaja: ESTE" % f["nombre"])
        else:
            L.append("    [si]  %-34s tambien servia (es mas largo)" % f["nombre"])
    L.append("")
    L.append("  %s" % r["resultado"]["cuenta"])
    L.append("")
    L.append("RESULTADO: %s" % r["valor"].upper())
    return "\n".join(L)
