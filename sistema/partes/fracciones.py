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
_ORDEN_CUENTA_FR = re.compile(r"^(?:" + _FR_PATRON + r"|(1))\s*([+\-])\s*" + _FR_PATRON + r"$")
_FR_MIXTO = re.compile(r"^(\d+)\s+(\d+)\s*/\s*(\d+)$")
_FR_SOLA = re.compile(r"^(\d+)\s*/\s*(\d+)$")
_ORDEN_MIXTO = re.compile(r"^mixto:?\s*(\d+)\s+(\d+)\s*/\s*(\d+)$")
_ORDEN_CUENTA_MIXTA = re.compile(r"^(?P<x>[\d/ ]+?)\s*(?P<op>[+\-])\s*(?P<y>[\d/ ]+)$")
_ORDEN_COMPARAR_MIXTO = re.compile(r"^comparar:?\s*(?P<x>[\d/ ]+?)\s*(?:y|,|con)\s*(?P<y>[\d/ ]+)$")
_ORDEN_RECTA = re.compile(r"^recta:?\s*" + _FR_PATRON + r"$")
_ORDEN_PARTES = re.compile(r"^partes:?\s*(\d+)\s*=\s*(\d+(?:\s*\+\s*\d+)*)$")

_NOMBRES_FR = {2: ("medio", "medios"), 3: ("tercio", "tercios"), 4: ("cuarto", "cuartos"),
               5: ("quinto", "quintos"), 6: ("sexto", "sextos"), 7: ("septimo", "septimos"),
               8: ("octavo", "octavos"), 9: ("noveno", "novenos"), 10: ("decimo", "decimos"),
               11: ("onceavo", "onceavos"), 12: ("doceavo", "doceavos")}


def _fr_limpio(texto):
    return " ".join(texto.lower().replace("ó", "o").strip().rstrip("?").split())


def es_orden_fraccion(texto):
    t = _fr_limpio(texto)
    if any(p.match(t) for p in (_ORDEN_FRACCION, _ORDEN_DE, _ORDEN_COMPARAR_FR, _ORDEN_ENTERO, _ORDEN_PARTES,
                                _ORDEN_RECTA, _ORDEN_CUENTA_FR, _ORDEN_MIXTO)):
        return True
    for patron in (_ORDEN_CUENTA_MIXTA, _ORDEN_COMPARAR_MIXTO):    # F.4: con numeros mixtos o enteros
        m = patron.match(t)
        if m and "/" in t:
            x, y = _fr_termino(m.group("x")), _fr_termino(m.group("y"))
            if x and y:
                return True
    return False


def _fr_termino(texto):
    """'2 3/4' -> (2, 3, 4);  '3/4' -> (0, 3, 4);  '3' -> (3, 0, None).  None si no es nada de eso."""
    t = " ".join(texto.split())
    m = _FR_MIXTO.match(t)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    m = _FR_SOLA.match(t)
    if m:
        return 0, int(m.group(1)), int(m.group(2))
    if t.isdigit():
        return int(t), 0, None
    return None


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


def _fr_problema(a, b, saber):
    """None si la fraccion se puede usar aqui (3.o: de 0 a un entero); si no, (conclusion, porque)."""
    if b == 0:
        return "imposible", "no se puede partir un entero en CERO partes"
    if b not in _NOMBRES_FR and b != 1:
        return "todavia_no", "en 3.o las partes van de medios a doceavos (1/2 a 1/12)"
    if decir(a, saber) is None:
        return "todavia_no", "%d no esta en mi lista" % a
    return None


def _fr_mixto(a, b, saber):
    """7/4 -> (1, 3): cuantos ENTEROS caben (agrupar a en grupos de b, M.8) y cuantas partes sobran."""
    if b == 1:
        return a, 0
    r = aplicar("dividir", {"total": a, "divisor": b}, saber)
    return r["valor"], r["resultado"].get("resto", 0)


def _fr_impropia(entero, a, b, saber):
    """2 3/4 -> 11 (cuartos): los enteros son entero x b partes, y se suman las a."""
    if not entero:
        return a
    m = aplicar("multiplicar", {"a": entero, "b": b}, saber)["valor"]
    return aplicar("sumar", {"a": m, "b": a}, saber)["valor"] if a else m


def _fr_texto_mixto(a, b, saber):
    """11/4 -> '2 3/4';  8/4 -> '2';  3/4 -> '3/4'."""
    if b == 1:
        return "%d" % a
    e, r = _fr_mixto(a, b, saber)
    if e == 0:
        return "%d/%d" % (a, b) if a else "0"
    return "%d" % e if r == 0 else "%d %d/%d" % (e, r, b)


# ---------------------------------------------------------------- fraccion: 1/4

def explicar_fraccion(a, b, saber):
    L = ["PREGUNTA (F.1/F.2): que es %d/%d?  (NCETM 3.2, 3.3; 3.NF.A.1)" % (a, b), ""]
    p = _fr_problema(a, b, saber)
    if p:
        return "\n".join(L + ["  %s: %s" % ("NO SE PUEDE" if p[0] == "imposible" else "TODAVIA NO", p[1]),
                              "", "RESULTADO: %s" % p[0]])
    if b == 1:
        if a == 1:
            return "\n".join(L + ["  el entero partido en UNA parte: la parte es el entero entero.", "",
                                  "RESULTADO: un entero"])
        return "\n".join(L + ["  %d/1: enteros partidos en UNA parte cada uno, y se toman %d: %d enteros "
                              "(3.NF.A.3c: los enteros tambien son fracciones)." % (a, a, a), "",
                              "RESULTADO: %d enteros" % a])
    if a == 0:
        return "\n".join(L + ["  %d partes de %d, y no se toma NINGUNA: cero." % (b, b), "", "RESULTADO: cero"])
    nombre = nombre_fraccion(a, b, saber)
    L.append("  %d/%d se lee '%s'." % (a, b, nombre))
    L.append("  el de ABAJO (%d) dice en cuantas partes IGUALES se parte el entero;" % b)
    L.append("  el de ARRIBA (%d) dice cuantas de esas partes se toman." % a)
    L.append("")
    if viene_despues(decir(a, saber), decir(b, saber), saber):
        e, r = _fr_mixto(a, b, saber)
        tiras = [_fr_tira(b, 4, b, saber) for _ in _fr_marcas(e, saber)]
        if r:
            tiras.append(_fr_tira(b, 4, r, saber))
        L.append("     %s" % "  ".join(tiras))
    else:
        L.append("     %s" % _fr_tira(b, 4, a, saber))
    L.append("")
    if a != 1:
        L.append("  %d/%d son %s fracciones de 1/%d: %s  (NCETM 3.3)" % (
            a, b, decir(a, saber), b, " + ".join("1/%d" % b for _ in _fr_marcas(a, saber))))
    L.append("  %s %s hacen un entero (%s)." % (decir(b, saber), _NOMBRES_FR[b][1],
                                                 " + ".join("1/%d" % b for _ in _fr_marcas(b, saber))))
    if a == b:
        L.append("  arriba y abajo el mismo numero: %d/%d es UN ENTERO." % (a, b))
        nombre = "un entero"
    elif viene_despues(decir(a, saber), decir(b, saber), saber):
        e, r = _fr_mixto(a, b, saber)
        L.append("  %d/%d es MAS DE UN ENTERO (fraccion impropia; NCETM 3.5): cuantos enteros caben?" % (a, b))
        L.append("     agrupo %d %s en grupos de %d (cada %d hacen un entero): %d : %d = %d%s"
                 % (a, _NOMBRES_FR[b][1], b, b, a, b, e, ", y sobran %d" % r if r else ""))
        L.append("  %d/%d = %s  (%d %s%s)" % (a, b, _fr_texto_mixto(a, b, saber), e, "entero" if e == 1 else "enteros",
                                            " y %s" % nombre_fraccion(r, b, saber) if r else ", justos"))
        nombre = "%s = %s" % (nombre, _fr_texto_mixto(a, b, saber))
    L += ["", "RESULTADO: %s" % nombre]
    return "\n".join(L)


# ---------------------------------------------------------------- recta: 3/4

def explicar_recta(a, b, saber):
    L = ["PREGUNTA (F.2/F.4): donde esta %d/%d en la recta?  (NCETM 3.3, 3.5; 3.NF.A.2)" % (a, b), ""]
    p = _fr_problema(a, b, saber)
    if p or b == 1:
        porque = p[1] if p else "%d/1 son %d enteros: en la recta de los enteros" % (a, a)
        return "\n".join(L + ["  %s" % porque, "", "RESULTADO: %s" % (p[0] if p else "%d" % a)])
    e, r = _fr_mixto(a, b, saber)
    hasta_entero = e if r == 0 and e else aplicar("sumar", {"a": e, "b": 1}, saber)["valor"]
    if hasta_entero == 0:
        hasta_entero = 1
    bloque = "".join("     " for _ in _fr_marcas(b, saber))           # un entero de ancho
    arriba = "%s%d" % ("".join(str(k).ljust(len(bloque)) for k in _fr_cuenta_hasta(hasta_entero, saber)), hasta_entero)
    linea = "|" + "|".join("----" for _ in _fr_marcas(_fr_impropia(hasta_entero, 0, b, saber), saber)) + "|"
    hasta = "".join("     " for _ in _fr_marcas(a, saber))
    L.append("  cada entero partido en %d trozos IGUALES (cada trozo es 1/%d); %d/%d esta a %s trozos del 0:"
             % (b, b, a, b, decir(a, saber)))
    L.append("")
    L.append("     " + arriba)
    L.append("     " + linea)
    L.append("     " + hasta + "^")
    L.append("     %s%d/%d" % (hasta, a, b))
    L.append("")
    if a == 0:
        L.append("  0/%d cae en el 0." % b)
    elif r == 0:
        L.append("  %d/%d cae justo en el %d: son %d %s." % (a, b, e, e, "entero" if e == 1 else "enteros"))
    elif e == 0:
        L.append("  %d/%d esta entre 0 y 1: es un NUMERO, como los demas, solo que entre dos enteros." % (a, b))
    else:
        L.append("  %d/%d esta entre %d y %d: es %s (NCETM 3.5: los mixtos tambien van en la recta)."
                 % (a, b, e, hasta_entero, _fr_texto_mixto(a, b, saber)))
    L += ["", "RESULTADO: a %s trozos de 1/%d del 0" % (decir(a, saber), b)]
    return "\n".join(L)


def _fr_cuenta_hasta(n, saber):
    """0, 1, ... n - 1 (recitando)."""
    out, k = [], "cero"
    while k != decir(n, saber):
        out.append(leer(k, saber))
        k = siguiente(k, saber)
    return out


# ---------------------------------------------------------------- 1/4 de 12

def decidir_fraccion_de(a, b, n, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = {"a": a, "b": b, "n": n}
    p = _fr_problema(a, b, saber)
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
        p = _fr_problema(a, b, saber)
        if p:
            return {"conclusion": p[0], "porque": p[1]}
    return aplicar("comparar_fracciones", {"a": fa, "b": fb}, saber)


def explicar_comparar_fracciones(fa, fb, saber):
    r = decidir_comparar_fracciones(fa, fb, saber)
    ta, tb = "%d/%d" % fa, "%d/%d" % fb
    L = ["PREGUNTA (F.1/F.2): cual es mayor, %s o %s?  (NCETM 3.2, 3.3; 3.NF.A.3d)" % (ta, tb), ""]
    if r["conclusion"] in ("todavia_no", "imposible"):
        return "\n".join(L + ["  %s: %s" % ("NO SE PUEDE" if r["conclusion"] == "imposible" else "TODAVIA NO",
                                            r["porque"]), "", "RESULTADO: %s" % r["conclusion"]])
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["  TODAVIA NO: arriba y abajo son distintos en las dos; para compararlas hay que "
                              "buscar fracciones equivalentes (NCETM 3.7, 5.o)", "", "RESULTADO: todavia_no"])
    for pid, res in sorted(r.get("todos", []), key=lambda x: x[1]["metodo"]):
        L.append("    %-28s %s" % (res["metodo"] + ":", res["cuenta"]))
    if len(r.get("todos", [])) > 1:
        L.append("    -> %s dicen lo mismo" % ("los dos caminos" if len(r["todos"]) == 2 else "todos los caminos"))
    L += ["", "RESULTADO: %s %s %s" % (ta, r["valor"], tb)]
    return "\n".join(L)


# ---------------------------------------------------------------- entero: 1/4 es 3

def decidir_entero(a, b, parte, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = {"a": a, "b": b, "parte": parte}
    p = _fr_problema(a, b, saber)
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


# ---------------------------------------------------------------- 2/7 + 3/7   (F.3)

def _fr_tira_dos(b, a, c, saber, signo):
    """La tira de b partes: las 'a' primeras con #; luego, si se suma, las 'c' siguientes con +;
    si se resta, de las 'a' se tachan las 'c' ultimas con x."""
    trozos, marca, i_a, i_c = [], "cero", "cero", "cero"
    hasta_quitar = None
    if signo == "-":
        hasta_quitar = aplicar("restar", {"a": a, "b": c}, saber).get("valor")
    while marca != decir(b, saber):
        if i_a != decir(a, saber):
            simbolo = "#"
            if signo == "-" and hasta_quitar is not None and viene_despues(i_a, decir(hasta_quitar, saber), saber) \
                    or (signo == "-" and i_a == decir(hasta_quitar, saber)):
                simbolo = "x"
            i_a = siguiente(i_a, saber)
        elif signo == "+" and i_c != decir(c, saber):
            simbolo = "+"
            i_c = siguiente(i_c, saber)
        else:
            simbolo = "o"
        trozos.append("%s%s%s" % (simbolo, simbolo, simbolo))
        marca = siguiente(marca, saber)
    return "[" + "|".join(trozos) + "]"


def decidir_cuenta_fracciones(fa, signo, fb, saber=None):
    """fa None = el entero 1.  Devuelve {conclusion, valor: (arriba, abajo), ...}."""
    if saber is None:
        saber = cargar_conocimiento()
    r = {"signo": signo, "b": fb}
    if fa is None:
        fa = (fb[1], fb[1])
        r["entero_como"] = fa
    r["a"] = fa
    for f in (fa, fb):
        p = _fr_problema(f[0], f[1], saber)
        if p:
            r.update(conclusion=p[0], porque=p[1])
            return r
    if fa[1] != fb[1]:
        r.update(conclusion="todavia_no", porque="las partes son de tamanos distintos (1/%d y 1/%d): hay que "
                 "buscar el mismo de abajo (NCETM 3.8, 5.o)" % (fa[1], fb[1]))
        return r
    b = fa[1]
    preg = "sumar" if signo == "+" else "restar"
    x = aplicar(preg, {"a": fa[0], "b": fb[0]}, saber)
    if x["conclusion"] != "hecho":
        r.update(conclusion="imposible", porque="no se pueden quitar %d partes de %d" % (fb[0], fa[0]))
        return r
    arriba = x["valor"]
    r["metodo"] = x["pieza"]["nombre"]
    # LA VUELTA (NCETM 3.4: sumar y restar son inversas)
    inv = aplicar("restar" if signo == "+" else "sumar", {"a": arriba, "b": fb[0]}, saber)
    r.update(conclusion="hecho", valor=(arriba, b), vuelta_ok=inv.get("valor") == fa[0],
             vuelta="%d/%d %s %d/%d = %s/%d" % (arriba, b, "-" if signo == "+" else "+", fb[0], b, inv.get("valor"), b))
    return r


def _fr_texto_valor(v, saber=None):
    arriba, b = v
    if arriba == b:
        return "1"
    if arriba == 0:
        return "0"
    if saber is not None and viene_despues(decir(arriba, saber), decir(b, saber), saber):
        return _fr_texto_mixto(arriba, b, saber)                    # F.4: 9/7 -> 1 2/7
    return "%d/%d" % v


def explicar_cuenta_fracciones(fa, signo, fb, saber):
    r = decidir_cuenta_fracciones(fa, signo, fb, saber)
    izq = "1" if fa is None else "%d/%d" % fa
    L = ["PREGUNTA (F.3): %s %s %d/%d  (NCETM 3.4: sumar y restar dentro de un entero)" % (izq, signo, fb[0], fb[1]), ""]
    if r["conclusion"] != "hecho":
        etiqueta = {"imposible": "NO SE PUEDE"}.get(r["conclusion"], "TODAVIA NO")
        return "\n".join(L + ["  %s: %s" % (etiqueta, r["porque"]), "", "RESULTADO: %s" % r["conclusion"]])
    a, b = r["a"]
    c = fb[0]
    if fa is None:
        L.append("  0. el entero se escribe con el mismo arriba y abajo: 1 = %d/%d" % (b, b))
    uno, varios = _NOMBRES_FR[b]
    nom = lambda n: "%s %s" % (decir(n, saber), uno if n == 1 else varios)
    L.append("  1. las partes son del MISMO TAMANO (1/%d): se cuentan como cosas, como manzanas." % b)
    L.append("     %s %s %s = %s   (%d %s %d = %d, %s)" % (nom(a), "mas" if signo == "+" else "menos", nom(c),
                                                           nom(r["valor"][0]), a, signo, c, r["valor"][0], r["metodo"]))
    if signo == "+":
        doble = aplicar("sumar", {"a": b, "b": b}, saber).get("valor")
        L.append("     el de abajo NO se suma: dice de que tamano son las partes, y no cambia "
                 "(el error tipico: %d/%s)." % (r["valor"][0], doble))
    else:
        L.append("     el de abajo NO se resta: dice de que tamano son las partes, y no cambia.")
    if not any(viene_despues(decir(x, saber), decir(b, saber), saber) for x in (a, c, r["valor"][0])):
        L.append("")
        L.append("     %s" % _fr_tira_dos(b, a, c, saber, signo))
    L.append("")
    L.append("  2. LA VUELTA (sumar y restar son inversas): %s ... %s" % (r["vuelta"], "SI" if r["vuelta_ok"] else "NO"))
    if r["valor"][0] == b:
        L.append("  %d/%d: arriba y abajo iguales, es UN ENTERO." % r["valor"])
    if viene_despues(decir(r["valor"][0], saber), decir(b, saber), saber):
        L.append("  %d/%d es mas de un entero (NCETM 3.5): %d/%d = %s" % (r["valor"][0], b, r["valor"][0], b,
                                                                     _fr_texto_mixto(r["valor"][0], b, saber)))
    L += ["", "RESULTADO: %s" % _fr_texto_valor(r["valor"], saber)]
    return "\n".join(L)


# ---------------------------------------------------------------- F.4: mixtos e impropias

def explicar_mixto(e, a, b, saber):
    L = ["PREGUNTA (F.4): %d %d/%d como fraccion impropia  (NCETM 3.5, punto 5)" % (e, a, b), ""]
    p = _fr_problema(a, b, saber)
    if p or b == 1:
        return "\n".join(L + ["  %s" % (p[1] if p else "1 no parte nada"), "", "RESULTADO: %s" % (p[0] if p else "no_entiendo")])
    if a != 0 and not viene_despues(decir(b, saber), decir(a, saber), saber):
        return "\n".join(L + ["  %d/%d ya es un entero o mas: un numero mixto lleva una parte MENOR que un entero" % (a, b),
                              "", "RESULTADO: no_entiendo"])
    m = aplicar("multiplicar", {"a": e, "b": b}, saber)["valor"]
    n = _fr_impropia(e, a, b, saber)
    L.append("  1. cada entero son %d %s: %d %s son %d x %d = %d %s" % (b, _NOMBRES_FR[b][1], e,
             "entero" if e == 1 else "enteros", e, b, m, _NOMBRES_FR[b][1]))
    L.append("  2. y %d %s mas: %d + %d = %d %s" % (a, _NOMBRES_FR[b][1], m, a, n, _NOMBRES_FR[b][1]))
    em, rm = _fr_mixto(n, b, saber)
    L.append("  LA VUELTA: %d : %d = %d, y sobran %d -> %d %d/%d ... %s" % (n, b, em, rm, em, rm, b,
                                                                          "SI" if (em, rm) == (e, a) else "NO"))
    L += ["", "RESULTADO: %d/%d" % (n, b)]
    return "\n".join(L)


def decidir_cuenta_mixta(x, op, y, saber=None):
    """x, y: (entero, arriba, abajo|None).  Mismo de abajo (o enteros).  Dos caminos: partir (enteros con
    enteros, partes con partes) y por impropias; tienen que dar lo mismo."""
    if saber is None:
        saber = cargar_conocimiento()
    bs = {t[2] for t in (x, y) if t[2] is not None}
    if len(bs) != 1:
        return {"conclusion": "todavia_no", "porque": "las partes son de tamanos distintos: hay que buscar el mismo "
                "de abajo (NCETM 3.8, 5.o)"}
    b = bs.pop()
    for t in (x, y):
        p = _fr_problema(t[1], b, saber)
        if p:
            return {"conclusion": p[0], "porque": p[1]}
    nx, ny = _fr_impropia(x[0], x[1], b, saber), _fr_impropia(y[0], y[1], b, saber)
    r = {"b": b, "nx": nx, "ny": ny}
    # camino 1: por impropias (NCETM 3.5, puntos 5 y 6)
    if op == "-" and viene_despues(decir(ny, saber), decir(nx, saber), saber):
        r.update(conclusion="imposible", porque="se quita mas de lo que hay")
        return r
    n = aplicar("sumar" if op == "+" else "restar", {"a": nx, "b": ny}, saber)["valor"]
    r["impropia"] = n
    # camino 2: partir (NCETM 3.5, punto 4): enteros con enteros, partes con partes
    ex, ax = _fr_mixto(nx, b, saber)
    ey, ay = _fr_mixto(ny, b, saber)
    pasos = []
    if op == "+":
        W = aplicar("sumar", {"a": ex, "b": ey}, saber)["valor"]
        P = aplicar("sumar", {"a": ax, "b": ay}, saber)["valor"]
        pasos.append("enteros con enteros: %d + %d = %d;  partes con partes: %d/%d + %d/%d = %d/%d" % (ex, ey, W, ax, b, ay, b, P, b))
        if P == b or viene_despues(decir(P, saber), decir(b, saber), saber):
            P = aplicar("restar", {"a": P, "b": b}, saber)["valor"]
            W = aplicar("sumar", {"a": W, "b": 1}, saber)["valor"]
            pasos.append("%d %s hacen un entero mas (reagrupo): %d enteros%s" % (b, _NOMBRES_FR[b][1], W,
                                                                                " y %d/%d" % (P, b) if P else " justos"))
    else:
        if ay != ax and viene_despues(decir(ay, saber), decir(ax, saber), saber):
            ex = aplicar("restar", {"a": ex, "b": 1}, saber)["valor"]
            ax = aplicar("sumar", {"a": ax, "b": b}, saber)["valor"]
            pasos.append("no hay bastantes partes: CAMBIO un entero por %d/%d -> %d y %d/%d" % (b, b, ex, ax, b))
        W = aplicar("restar", {"a": ex, "b": ey}, saber)["valor"]
        P = aplicar("restar", {"a": ax, "b": ay}, saber)["valor"]
        pasos.append("enteros con enteros: %d - %d = %d;  partes con partes: %d/%d - %d/%d = %d/%d" % (ex, ey, W, ax, b, ay, b, P, b))
    r["pasos_partir"] = pasos
    r["partir"] = _fr_impropia(W, P, b, saber)
    r.update(conclusion="hecho", valor=(n, b), de_acuerdo=r["partir"] == n)
    return r


def _fr_texto_termino(t):
    if t[2] is None:
        return "%d" % t[0]
    return "%d/%d" % (t[1], t[2]) if not t[0] else "%d %d/%d" % t


def explicar_cuenta_mixta(x, op, y, saber):
    r = decidir_cuenta_mixta(x, op, y, saber)
    L = ["PREGUNTA (F.4): %s %s %s  (NCETM 3.5: numeros mixtos e impropias)" % (_fr_texto_termino(x), op,
                                                                              _fr_texto_termino(y)), ""]
    if r["conclusion"] != "hecho":
        etiqueta = {"imposible": "NO SE PUEDE"}.get(r["conclusion"], "TODAVIA NO")
        return "\n".join(L + ["  %s: %s" % (etiqueta, r["porque"]), "", "RESULTADO: %s" % r["conclusion"]])
    b = r["b"]
    L.append("  1. PARTIENDO (como con los enteros):")
    for p in r["pasos_partir"]:
        L.append("        %s" % p)
    L.append("  2. POR IMPROPIAS: %s = %d/%d y %s = %d/%d;  %d/%d %s %d/%d = %d/%d"
             % (_fr_texto_termino(x), r["nx"], b, _fr_texto_termino(y), r["ny"], b, r["nx"], b, op, r["ny"], b,
                r["impropia"], b))
    L.append("     (el de abajo no cambia: dice de que tamano son las partes)")
    L.append("  -> los dos caminos: %s" % ("lo mismo" if r["de_acuerdo"] else "NO CUADRAN"))
    L += ["", "RESULTADO: %s" % _fr_texto_mixto(r["impropia"], b, saber)]
    return "\n".join(L)


def decidir_comparar_mixtos(x, y, saber=None):
    """NCETM 3.5, punto 3: primero los ENTEROS; si son iguales, las partes (como las fracciones propias)."""
    if saber is None:
        saber = cargar_conocimiento()
    res = []
    for t in (x, y):
        if t[2] is None:
            res.append((t[0], 0, None))
            continue
        p = _fr_problema(t[1], t[2], saber)
        if p:
            return {"conclusion": p[0], "porque": p[1]}
        e, a = _fr_mixto(_fr_impropia(t[0], t[1], t[2], saber), t[2], saber)
        res.append((e, a, t[2]))
    (ex, ax, bx), (ey, ay, by) = res
    if ex != ey:
        mayor = viene_despues(decir(ex, saber), decir(ey, saber), saber)
        return {"conclusion": "hecho", "valor": ">" if mayor else "<", "como": "enteros",
                "porque": "%d enteros contra %d: deciden los enteros" % (ex, ey)}
    if not ax and not ay:
        return {"conclusion": "hecho", "valor": "=", "como": "enteros", "porque": "los mismos enteros y nada mas"}
    if not ax or not ay:
        return {"conclusion": "hecho", "valor": "<" if not ax else ">", "como": "partes",
                "porque": "los mismos enteros, y uno no tiene partes"}
    r = decidir_comparar_fracciones((ax, bx), (ay, by), saber)
    if r["conclusion"] != "hecho":
        return {"conclusion": "todavia_no", "porque": "los mismos enteros; las partes no tienen nada en comun (5.o)"}
    return {"conclusion": "hecho", "valor": r["valor"], "como": "partes",
            "porque": "los mismos enteros (%d); deciden las partes: %d/%d %s %d/%d" % (ex, ax, bx, r["valor"], ay, by)}


def explicar_comparar_mixtos(x, y, saber):
    r = decidir_comparar_mixtos(x, y, saber)
    tx, ty = _fr_texto_termino(x), _fr_texto_termino(y)
    L = ["PREGUNTA (F.4): cual es mayor, %s o %s?  (NCETM 3.5, punto 3)" % (tx, ty), ""]
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["  TODAVIA NO: %s" % r["porque"], "", "RESULTADO: %s" % r["conclusion"]])
    L.append("  primero los ENTEROS, luego las partes: %s" % r["porque"])
    L += ["", "RESULTADO: %s %s %s" % (tx, r["valor"], ty)]
    return "\n".join(L)


# ---------------------------------------------------------------- la puerta



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
    m = _ORDEN_MIXTO.match(t)
    if m:
        return explicar_mixto(int(m.group(1)), int(m.group(2)), int(m.group(3)), saber)
    m = _ORDEN_COMPARAR_MIXTO.match(t)
    if m and not _ORDEN_COMPARAR_FR.match(t):
        return explicar_comparar_mixtos(_fr_termino(m.group("x")), _fr_termino(m.group("y")), saber)
    m = _ORDEN_CUENTA_FR.match(t)
    if m:
        g = m.groups()
        primera = (int(g[0]), int(g[1])) if g[0] is not None else None     # None: el entero '1'
        return explicar_cuenta_fracciones(primera, g[3], (int(g[4]), int(g[5])), saber)
    m = _ORDEN_CUENTA_MIXTA.match(t)
    if m and "/" in t and _fr_termino(m.group("x")) and _fr_termino(m.group("y")):
        return explicar_cuenta_mixta(_fr_termino(m.group("x")), m.group("op"), _fr_termino(m.group("y")), saber)
    m = _ORDEN_RECTA.match(t)
    if m:
        return explicar_recta(int(m.group(1)), int(m.group(2)), saber)
    m = _ORDEN_PARTES.match(t)
    if m:
        partes = [int(x) for x in re.findall(r"\d+", m.group(2))]
        return explicar_partes(int(m.group(1)), partes, saber)
    return ("NO ENTIENDO ESTO: se escribe asi:  fraccion: 1/4    1/4 de 12    comparar: 1/3 y 1/5\n"
            "                                    entero: 1/4 es 3    partes: 12 = 4 + 4 + 4    recta: 3/4")
