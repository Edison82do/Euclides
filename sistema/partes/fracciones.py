# -*- coding: utf-8 -*-
"""
Euclides - LAS FRACCIONES (pasos F.1, F.2 y F.3 del plan pedagogico, 6 oct 2026).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

NCETM Spine 3 (Year 3): 3.1 la parte y el todo; 3.2 fracciones unitarias; 3.3 no unitarias;
3.4 sumar y restar dentro de un entero.  Common Core 3.NF.A.1-3.
Una fraccion a/b: el entero partido en b partes IGUALES (el de abajo), y se toman a (el de arriba).
Una fraccion de una cantidad se saca REPARTIENDO (M.3).  Nada de calculadora: las partes se reparten,
se cuentan y se comparan en la lista.
"""

import re

_FR_PATRON = r"(\d+)\s*/\s*(\d+)"
_ORDEN_FRACCION = re.compile(r"^fracci[oó]n:?\s*" + _FR_PATRON + r"$")
_ORDEN_DE = re.compile(r"^" + _FR_PATRON + r"\s+de\s+(\d+)$")
_ORDEN_COMPARAR_FR = re.compile(r"^comparar:?\s*" + _FR_PATRON + r"\s*(?:y|,|con|\?)\s*" + _FR_PATRON + r"$")
_ORDEN_ENTERO = re.compile(r"^entero:?\s*(?:si\s+)?" + _FR_PATRON + r"\s+(?:es|son|=)\s+(\d+)$")
_ORDEN_PARTES = re.compile(r"^partes:?\s*(\d+)\s*=\s*(\d+(?:\s*\+\s*\d+)*)$")

_NOMBRES_FR = {2: ("medio", "medios"), 3: ("tercio", "tercios"), 4: ("cuarto", "cuartos"),
               5: ("quinto", "quintos"), 6: ("sexto", "sextos"), 7: ("septimo", "septimos"),
               8: ("octavo", "octavos"), 9: ("noveno", "novenos"), 10: ("decimo", "decimos"),
               11: ("onceavo", "onceavos"), 12: ("doceavo", "doceavos")}


def _fr_limpio(texto):
    return " ".join(texto.lower().replace("ó", "o").strip().rstrip("?").split())


def es_orden_fraccion(texto):
    t = _fr_limpio(texto)
    return any(p.match(t) for p in (_ORDEN_FRACCION, _ORDEN_DE, _ORDEN_COMPARAR_FR, _ORDEN_ENTERO, _ORDEN_PARTES))


def nombre_fraccion(a, b, saber):
    """3/4 -> 'tres cuartos'; 1/2 -> 'un medio'.  None si el de abajo no tiene nombre todavia."""
    if b not in _NOMBRES_FR:
        return None
    uno, varios = _NOMBRES_FR[b]
    if a == 1:
        return "un " + uno
    return "%s %s" % (decir(a, saber), varios)


def _fr_marcas(n, saber, simbolo="o"):
    """n marcas, contando con la lista (sin multiplicar texto)."""
    out, marca = [], "cero"
    while marca != decir(n, saber):
        out.append(simbolo)
        marca = siguiente(marca, saber)
    return "".join(out)


def _fr_tira(partes, en_cada, tomadas, saber):
    """[###|ooo|ooo|ooo]: 'partes' trozos de 'en_cada' marcas; los 'tomadas' primeros, con #."""
    trozos, marca, tomados = [], "cero", "cero"
    while marca != decir(partes, saber):
        lleno = tomados != decir(tomadas, saber)
        trozos.append(_fr_marcas(en_cada, saber, "#" if lleno else "o"))
        if lleno:
            tomados = siguiente(tomados, saber)
        marca = siguiente(marca, saber)
    return "[" + "|".join(trozos) + "]"


def _fr_problema(a, b, saber, unitarias=True):
    """None si la fraccion se puede usar aqui; si no, (conclusion, porque)."""
    if b == 0:
        return "imposible", "no se puede partir un entero en CERO partes"
    if b not in _NOMBRES_FR and b != 1:
        return "todavia_no", "en 3.o las partes van de medios a doceavos (1/2 a 1/12)"
    if unitarias and a != 1:
        return "todavia_no", "%d/%d no es unitaria (uno arriba): las no unitarias son el paso F.2" % (a, b)
    return None


# ---------------------------------------------------------------- fraccion: 1/4

def explicar_fraccion(a, b, saber):
    L = ["PREGUNTA (F.1): que es %d/%d?  (NCETM 3.2; 3.NF.A.1)" % (a, b), ""]
    p = _fr_problema(a, b, saber, unitarias=_FR_SOLO_UNITARIAS)
    if p:
        return "\n".join(L + ["  %s: %s" % ("NO SE PUEDE" if p[0] == "imposible" else "TODAVIA NO", p[1]),
                              "", "RESULTADO: %s" % p[0]])
    if b == 1:
        return "\n".join(L + ["  el entero partido en UNA parte: la parte es el entero entero.", "",
                              "RESULTADO: un entero"])
    nombre = nombre_fraccion(a, b, saber)
    L.append("  %d/%d se lee '%s'." % (a, b, nombre))
    L.append("  el de ABAJO (%d) dice en cuantas partes IGUALES se parte el entero;" % b)
    L.append("  el de ARRIBA (%d) dice cuantas de esas partes se toman." % a)
    L.append("")
    L.append("     %s" % _fr_tira(b, 4, a, saber))
    L.append("")
    L.append("  %s %s hacen un entero (%s)." % (decir(b, saber), _NOMBRES_FR[b][1],
                                                 " + ".join("1/%d" % b for _ in _fr_marcas(b, saber))))
    L += ["", "RESULTADO: %s" % nombre]
    return "\n".join(L)


# ---------------------------------------------------------------- 1/4 de 12

def decidir_fraccion_de(a, b, n, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = {"a": a, "b": b, "n": n}
    p = _fr_problema(a, b, saber, unitarias=_FR_SOLO_UNITARIAS)
    if p:
        r.update(conclusion=p[0], porque=p[1])
        return r
    rep = aplicar("dividir", {"total": n, "divisor": b}, saber)
    if rep["conclusion"] != "hecho":
        r.update(conclusion="no_sale", porque=rep.get("porque"))
        return r
    resto = rep["resultado"].get("resto", 0)
    if resto:
        r.update(conclusion="no_sale", porque="%d no se reparte en %d partes iguales: sobra %d (habria que "
                 "partir las cosas)" % (n, b, resto), cada=rep["valor"], resto=resto)
        return r
    cada = rep["valor"]
    r.update(cada=cada, metodo_reparto=rep["pieza"]["nombre"])
    if a == 1:
        r.update(conclusion="hecho", valor=cada)
        return r
    # no unitaria (F.2): 'a' partes de 'cada'
    tom = aplicar("multiplicar", {"a": a, "b": cada}, saber)
    if tom["conclusion"] != "hecho":
        r.update(conclusion="no_sale", porque=tom.get("porque"))
        return r
    r.update(conclusion="hecho", valor=tom["valor"])
    return r


def explicar_fraccion_de(a, b, n, saber):
    r = decidir_fraccion_de(a, b, n, saber)
    L = ["PREGUNTA (F.1): cuanto es %d/%d de %d?  (una fraccion de una cantidad: REPARTIR)" % (a, b, n), ""]
    if r["conclusion"] in ("todavia_no", "imposible"):
        return "\n".join(L + ["  %s: %s" % ("NO SE PUEDE" if r["conclusion"] == "imposible" else "TODAVIA NO",
                                            r["porque"]), "", "RESULTADO: %s" % r["conclusion"]])
    L.append("  1. %d/%d: el entero (%d) en %d partes IGUALES -> REPARTO %d entre %d (M.3)" % (a, b, n, b, n, b))
    if r["conclusion"] == "no_sale":
        return "\n".join(L + ["", "  NO SALE JUSTO: %s" % r["porque"], "", "RESULTADO: no_sale"])
    L.append("     a cada parte le tocan %d  (%s)" % (r["cada"], r["metodo_reparto"]))
    L.append("")
    L.append("     %s" % _fr_tira(b, r["cada"], a, saber))
    L.append("")
    if a == 1:
        L.append("  2. 1/%d es UNA parte: %d" % (b, r["valor"]))
    else:
        L.append("  2. %d/%d son %s partes de %d: %d x %d = %d" % (a, b, decir(a, saber), r["cada"], a, r["cada"], r["valor"]))
    L += ["", "RESULTADO: %d" % r["valor"]]
    return "\n".join(L)


# ---------------------------------------------------------------- comparar: 1/3 y 1/5

def decidir_comparar_fracciones(fa, fb, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    for a, b in (fa, fb):
        p = _fr_problema(a, b, saber, unitarias=False)
        if p:
            return {"conclusion": p[0], "porque": p[1]}
    return aplicar("comparar_fracciones", {"a": fa, "b": fb}, saber)


def explicar_comparar_fracciones(fa, fb, saber):
    r = decidir_comparar_fracciones(fa, fb, saber)
    ta, tb = "%d/%d" % fa, "%d/%d" % fb
    L = ["PREGUNTA (F.1): cual es mayor, %s o %s?  (NCETM 3.2, 3.3)" % (ta, tb), ""]
    if r["conclusion"] in ("todavia_no", "imposible"):
        return "\n".join(L + ["  %s: %s" % ("NO SE PUEDE" if r["conclusion"] == "imposible" else "TODAVIA NO",
                                            r["porque"]), "", "RESULTADO: %s" % r["conclusion"]])
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["  %s" % (r.get("porque") or r["conclusion"]), "", "RESULTADO: todavia_no"])
    for pid, res in sorted(r.get("todos", []), key=lambda x: x[1]["metodo"]):
        L.append("    %-28s %s" % (res["metodo"] + ":", res["cuenta"]))
    if len(r.get("todos", [])) > 1:
        L.append("    -> los dos caminos dicen lo mismo")
    L += ["", "RESULTADO: %s %s %s" % (ta, r["valor"], tb)]
    return "\n".join(L)


# ---------------------------------------------------------------- entero: 1/4 es 3

def decidir_entero(a, b, parte, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = {"a": a, "b": b, "parte": parte}
    p = _fr_problema(a, b, saber, unitarias=_FR_SOLO_UNITARIAS)
    if p:
        r.update(conclusion=p[0], porque=p[1])
        return r
    una = parte
    if a != 1:                                       # F.2: 3/4 es 9 -> 1/4 es 9 : 3
        rep = aplicar("dividir", {"total": parte, "divisor": a}, saber)
        if rep["conclusion"] != "hecho" or rep["resultado"].get("resto", 0):
            r.update(conclusion="no_sale", porque="%d no se reparte justo en %d partes" % (parte, a))
            return r
        una = rep["valor"]
    r["una"] = una
    serie, v, marca = [una], una, "uno"
    while marca != decir(b, saber):
        v = aplicar("sumar", {"a": v, "b": una}, saber).get("valor")
        if v is None:
            r.update(conclusion="todavia_no", porque="el entero se sale de mi lista")
            return r
        serie.append(v)
        marca = siguiente(marca, saber)
    m = aplicar("multiplicar", {"a": b, "b": una}, saber)
    r.update(conclusion="hecho", valor=v, serie=serie, comprobacion_ok=m.get("valor") == v)
    return r


def explicar_entero(a, b, parte, saber):
    r = decidir_entero(a, b, parte, saber)
    L = ["PREGUNTA (F.1): si %d/%d es %d, cuanto es el ENTERO?  (NCETM 3.1, 3.2)" % (a, b, parte), ""]
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["  %s" % r["porque"], "", "RESULTADO: %s" % r["conclusion"]])
    if a != 1:
        L.append("  1. %d/%d son %s partes iguales y valen %d: UNA parte es %d : %d = %d" % (
            a, b, decir(a, saber), parte, parte, a, r["una"]))
    L.append("  %s. el entero son %s partes de %d (%d/%d): las sumo una a una" % (
        "2" if a != 1 else "1", decir(b, saber), r["una"], b, b))
    L.append("        %s = %d" % (" + ".join(str(r["una"]) for _ in r["serie"]), r["valor"]))
    L.append("     compruebo: %d x %d = %d ... %s" % (b, r["una"], r["valor"], "SI" if r["comprobacion_ok"] else "NO"))
    L += ["", "RESULTADO: %d" % r["valor"]]
    return "\n".join(L)


# ---------------------------------------------------------------- partes: 12 = 4 + 4 + 4

def decidir_partes(total, partes, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = {"total": total, "partes": partes}
    v = partes[0]
    for p in partes[1:]:
        v = aplicar("sumar", {"a": v, "b": p}, saber).get("valor")
    cuantas = "cero"
    for _ in partes:
        cuantas = siguiente(cuantas, saber)
    r["suman"], r["cuantas"] = v, leer(cuantas, saber)
    if v != total:
        r.update(conclusion="no_hacen_el_entero")
        return r
    iguales = all(p == partes[0] for p in partes)
    r["iguales"] = iguales
    if not iguales:
        r.update(conclusion="desiguales")
        return r
    if r["cuantas"] == 1:
        r.update(conclusion="hecho", valor="el entero")
        return r
    r.update(conclusion="hecho", valor="1/%d" % r["cuantas"])
    return r


def explicar_partes(total, partes, saber):
    r = decidir_partes(total, partes, saber)
    L = ["PREGUNTA (F.1): %d partido asi: %s.  Que parte es cada trozo?  (NCETM 3.1)" % (
        total, " + ".join(str(p) for p in partes)), ""]
    L.append("  1. hacen el entero?  %s = %d ... %s" % (" + ".join(str(p) for p in partes), r["suman"],
                                                     "SI" if r["suman"] == total else "NO, el entero es %d" % total))
    if r["conclusion"] == "no_hacen_el_entero":
        return "\n".join(L + ["", "  Las partes tienen que juntar el entero entero: no son fracciones de %d." % total,
                              "", "RESULTADO: no_hacen_el_entero"])
    L.append("  2. son IGUALES?  %s" % ("SI, todas de %d" % partes[0] if r["iguales"] else "NO"))
    if not r["iguales"]:
        return "\n".join(L + ["", "  Partes DESIGUALES: no son %s.  Una fraccion necesita partes IGUALES (NCETM 3.2)."
                              % (_NOMBRES_FR.get(r["cuantas"], ("", "partes"))[1]), "", "RESULTADO: desiguales"])
    if r["cuantas"] == 1:
        return "\n".join(L + ["", "RESULTADO: el entero"])
    L.append("  3. %s partes iguales: cada una es 1/%d de %d (%s)" % (
        decir(r["cuantas"], saber), r["cuantas"], total, nombre_fraccion(1, r["cuantas"], saber) or "1/%d" % r["cuantas"]))
    L += ["", "RESULTADO: %s" % r["valor"]]
    return "\n".join(L)


# ---------------------------------------------------------------- la puerta

_FR_SOLO_UNITARIAS = True        # F.1: solo unitarias.  F.2 lo abre.


def explicar_orden_fraccion(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    t = _fr_limpio(texto)
    m = _ORDEN_FRACCION.match(t)
    if m:
        return explicar_fraccion(int(m.group(1)), int(m.group(2)), saber)
    m = _ORDEN_DE.match(t)
    if m:
        return explicar_fraccion_de(int(m.group(1)), int(m.group(2)), int(m.group(3)), saber)
    m = _ORDEN_COMPARAR_FR.match(t)
    if m:
        g = [int(x) for x in m.groups()]
        return explicar_comparar_fracciones((g[0], g[1]), (g[2], g[3]), saber)
    m = _ORDEN_ENTERO.match(t)
    if m:
        return explicar_entero(int(m.group(1)), int(m.group(2)), int(m.group(3)), saber)
    m = _ORDEN_PARTES.match(t)
    if m:
        partes = [int(x) for x in re.findall(r"\d+", m.group(2))]
        return explicar_partes(int(m.group(1)), partes, saber)
    return ("NO ENTIENDO ESTO: se escribe asi:  fraccion: 1/4    1/4 de 12    comparar: 1/3 y 1/5\n"
            "                                    entero: 1/4 es 3    partes: 12 = 4 + 4 + 4")
