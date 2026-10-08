# -*- coding: utf-8 -*-
"""
Euclides - FRACCIONES EQUIVALENTES Y SIMPLIFICAR (paso F.6, 8 oct 2026; 5.o).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

NCETM 3.7 (Finding equivalent fractions and simplifying fractions), los tres puntos:
  1 fracciones con distinto arriba y abajo que VALEN LO MISMO son equivalentes;
  2 la relacion multiplicativa entre el de arriba y el de abajo se mantiene: se generan multiplicando o dividiendo
    los dos POR EL MISMO numero (la relacion horizontal, de una a otra; y la vertical, dentro de cada una);
  3 simplificar: dividir arriba y abajo entre un factor comun.
Common Core 4.NF.A.1.  Las cuentas las hacen las piezas (simplificar_*, hueco_*, fracciones_equivalentes_*);
aqui solo se LEEN las ordenes y se explica:
    equivalentes: 2/3                 la familia (4/6, 6/9, 8/12 ...), con las tiras
    simplificar: 12/18                la forma mas simple, con los metodos y la vuelta
    2/3 = ?/12    4/12 = 5/?          el hueco
    equivalentes: 2/3 y 8/12          si / no  (y  2/3 = 8/12  -> verdadero / falso)
"""

import re

_EQF_F = r"(\d+)\s*/\s*(\d+)"
_EQF_H = r"(\d+|\?)\s*/\s*(\d+|\?)"
_EQF_FAMILIA = re.compile(r"^(?:fracciones\s+)?equivalentes:?\s*(?:de\s+)?" + _EQF_F + r"$")
_EQF_PAREJA = re.compile(r"^(?:son\s+)?(?:fracciones\s+)?equivalentes:?\s*" + _EQF_F + r"\s*(?:y|,|con|=)\s*" + _EQF_F + r"$")
_EQF_SIMPLIFICAR = re.compile(r"^simplifica(?:r)?:?\s*" + _EQF_F + r"$")
_EQF_HUECO = re.compile(r"^(?:ecuacion:?\s*)?" + _EQF_H + r"\s*=\s*" + _EQF_H + r"$")
_EQF_IGUALDAD = re.compile(r"^(?:verdad:?\s*)?" + _EQF_F + r"\s*=\s*" + _EQF_F + r"$")
_EQF_ANCHO = (24, 60)               # el largo de las tiras: 24 cuadritos (medios ... doceavos) o 60 (quintos, decimos)


def _eqf_limpio(texto):
    return " ".join(texto.lower().replace("ó", "o").strip().rstrip(".").split())


def es_orden_equivalentes(texto):
    t = _eqf_limpio(texto)
    if any(p.match(t) for p in (_EQF_FAMILIA, _EQF_PAREJA, _EQF_SIMPLIFICAR, _EQF_IGUALDAD)):
        return True
    m = _EQF_HUECO.match(t)
    return bool(m) and t.count("?") == 1


def _eqf_tabla(r):
    L = []
    elegida = r.get("pieza", {}).get("id")
    for f in r["candidatos"]:
        if f.get("descartado"):
            L.append("    [no]  %-46s porque %s" % (f["nombre"], f["descartado"]))
        elif f.get("no_salio"):
            L.append("    [no]  %-46s encajaba, pero NO SALIO: %s" % (f["nombre"], f["no_salio"]))
        elif f["id"] == elegida:
            L.append("    [SI]  %-46s <- el mas corto que encaja: ESTE" % f["nombre"])
        else:
            L.append("    [si]  %-46s tambien servia (es mas largo)" % f["nombre"])
    return L


def _eqf_problema(numeros, saber):
    """None si todos los numeros se pueden usar; si no, (conclusion, por que)."""
    for n in numeros:
        if n is not None and decir(n, saber) is None:
            return "todavia_no", "%d no esta en mi lista (llego hasta %s)" % (n, techo(saber))
    return None


def _eqf_justo(n, d, saber):
    """n : d si sale justo (M.3/M.8); None si sobra algo o no se hacer la division."""
    r = aplicar("dividir", {"total": n, "divisor": d}, saber)
    if r["conclusion"] != "hecho" or r["resultado"].get("resto", 0):
        return None
    return r["valor"]


def _eqf_simplificar(a, b, saber):
    return aplicar("simplificar_fraccion", {"a": a, "b": b}, saber)


def _eqf_tiras(fracciones, saber):
    """Las tiras de las fracciones que se pueden dibujar con el mismo largo (24 o 60 cuadritos): lo tomado (#) mide
    lo mismo en todas si son equivalentes.  [] si no se puede dibujar ninguna pareja."""
    for ancho in _EQF_ANCHO:
        filas = []
        for a, b in fracciones:
            if b == 1 or viene_despues(decir(a, saber), decir(b, saber), saber):
                continue
            cada = _eqf_justo(ancho, b, saber)
            if cada is not None:
                filas.append("     %-7s %s" % ("%d/%d" % (a, b), _fr_tira(b, cada, a, saber)))
        if filas[1:]:
            return filas
    return []


# ---------------------------------------------------------------- simplificar: 12/18

def explicar_simplificar(a, b, saber):
    L = ["PREGUNTA (F.6): simplificar %d/%d  (NCETM 3.7, punto 3: dividir arriba y abajo entre un FACTOR COMUN)"
         % (a, b), ""]
    if b == 0:
        return "\n".join(L + ["  NO SE PUEDE: no se puede partir un entero en CERO partes", "", "RESULTADO: imposible"])
    p = _eqf_problema((a, b), saber)
    if p:
        return "\n".join(L + ["  TODAVIA NO: %s" % p[1], "", "RESULTADO: %s" % p[0]])
    if a == 0:
        return "\n".join(L + ["  0/%d: no se toma ninguna parte, es CERO (con partes del tamano que sea)." % b, "",
                              "RESULTADO: 0"])
    r = _eqf_simplificar(a, b, saber)
    L.append("  PRUEBO TODO LO QUE SE:")
    L += _eqf_tabla(r)
    L.append("")
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["  TODAVIA NO: %s" % (r.get("porque") or r["conclusion"]), "", "RESULTADO: todavia_no"])
    res = r["resultado"]
    L.append("  %s:" % res["metodo"].upper())
    for linea in res["cuenta"].split("\n"):
        L.append("        %s" % linea)
    L.append("")
    if (res["arriba"], res["abajo"]) == (a, b):
        L.append("  %d/%d YA ESTA EN SU FORMA MAS SIMPLE: %s." % (a, b, res["por_que_ya"]))
        if a != 1:
            L.append("  (no solo las unitarias, como 1/3, estan en su forma mas simple: %d/%d tambien)" % (a, b))
    else:
        L.append("  ES LA FORMA MAS SIMPLE? %s." % res["por_que_ya"])
        if res["abajo"] == 1:
            L.append("  %d/%d es un numero ENTERO: %s %s justo%s (%s/1)." % (
                a, b, res["valor"], "entero" if res["arriba"] == 1 else "enteros", "" if res["arriba"] == 1 else "s",
                res["valor"]))
        else:
            L.append("  Simplificar NO cambia lo que vale: %d/%d y %s son EQUIVALENTES; solo son partes mas grandes y "
                     "se toman menos." % (a, b, res["valor"]))
        tiras = _eqf_tiras([(a, b), (res["arriba"], res["abajo"])], saber)
        if tiras:
            L += [""] + tiras
    L.append("")
    L.append("  LA VUELTA (multiplico de vuelta arriba y abajo): %s ... %s" % (res["vuelta"], "SI" if res["vuelta_ok"] else "NO"))
    L += ["", "RESULTADO: %s" % res["valor"]]
    return "\n".join(L)


# ---------------------------------------------------------------- equivalentes: 2/3  (la familia)

def explicar_familia(a, b, saber):
    L = ["PREGUNTA (F.6): la familia de %d/%d, sus fracciones EQUIVALENTES  (NCETM 3.7, puntos 1 y 2)" % (a, b), ""]
    if b == 0:
        return "\n".join(L + ["  NO SE PUEDE: no se puede partir un entero en CERO partes", "", "RESULTADO: imposible"])
    p = _eqf_problema((a, b), saber)
    if p:
        return "\n".join(L + ["  TODAVIA NO: %s" % p[1], "", "RESULTADO: %s" % p[0]])
    if a == 0:
        return "\n".join(L + ["  0/%d es cero: todas las 0/n valen lo mismo (cero)." % b, "", "RESULTADO: 0"])
    L.append("  HACIA ARRIBA: multiplico el de arriba y el de abajo POR EL MISMO numero (la relacion horizontal):")
    arriba, k, todo_ok = [], "uno", True
    while k != "seis":
        k = siguiente(k, saber)
        n = leer(k, saber)
        ma = aplicar("multiplicar", {"a": a, "b": n}, saber)
        mb = aplicar("multiplicar", {"a": b, "b": n}, saber)
        if ma["conclusion"] != "hecho" or mb["conclusion"] != "hecho" or decir(mb["valor"], saber) is None:
            L.append("     x %d: ya no cabe en mi lista (llego hasta %s)" % (n, techo(saber)))
            break
        na, nb = ma["valor"], mb["valor"]
        va, vb = _eqf_justo(na, n, saber), _eqf_justo(nb, n, saber)
        ok = (va, vb) == (a, b)
        todo_ok = todo_ok and ok
        L.append("     x %d:  %d/%d = %d/%d    (%d x %d = %d, %d x %d = %d;  la vuelta: %d : %d = %s, %d : %d = %s ... %s)"
                 % (n, a, b, na, nb, a, n, na, b, n, nb, na, n, va, nb, n, vb, "SI" if ok else "NO"))
        arriba.append((na, nb))
    # hacia abajo: dividiendo entre los factores comunes
    abajo = []
    r = _eqf_simplificar(a, b, saber)
    if r["conclusion"] == "hecho" and (r["resultado"]["arriba"], r["resultado"]["abajo"]) != (a, b):
        sa = r["resultado"]["arriba"]
        g = _eqf_justo(a, sa, saber)
        fs = aplicar("parejas_de_factores", {"n": g}, saber) if g else {"conclusion": "no"}
        if fs["conclusion"] == "hecho":
            L.append("  HACIA ABAJO: divido los dos entre un FACTOR COMUN (los factores de %d: %s):" % (
                g, ", ".join("%d" % f for f in fs["resultado"]["factores"])))
            for f in fs["resultado"]["factores"][1:]:
                da, db = _eqf_justo(a, f, saber), _eqf_justo(b, f, saber)
                L.append("     : %d:  %d/%d = %d/%d" % (f, a, b, da, db))
                abajo.append((da, db))
            abajo.reverse()
        else:
            L.append("  HACIA ABAJO: se simplifica hasta %s" % r["valor"])
            abajo.append((sa, r["resultado"]["abajo"]))
    elif r["conclusion"] == "hecho":
        L.append("  HACIA ABAJO: nada; %d/%d ya esta en su forma mas simple (%s)." % (a, b, r["resultado"]["por_que_ya"]))
    L.append("")
    # la relacion vertical
    kv = _eqf_justo(b, a, saber)
    if kv is not None and a != b:
        L.append("  LA RELACION VERTICAL: en %d/%d el de abajo es %d veces el de arriba (%d : %d = %d); en TODAS las de la "
                 "familia tambien%s" % (a, b, kv, b, a, kv, (" (la tabla del %d): %s" % (kv, ", ".join(
                     "%d x %d = %d" % (x, kv, y) for x, y in arriba[:3]))) if arriba else "."))
    elif a != b and _eqf_justo(a, b, saber) is not None:
        kv = _eqf_justo(a, b, saber)
        L.append("  LA RELACION VERTICAL: en %d/%d el de arriba es %d veces el de abajo; en todas las de la familia "
                 "tambien." % (a, b, kv))
    else:
        L.append("  La relacion entre el de arriba y el de abajo es LA MISMA en todas: se multiplican los dos por lo mismo.")
    L.append("  (Solo vale MULTIPLICAR o DIVIDIR los dos por el mismo numero: sumar lo mismo arriba y abajo NO da una "
             "equivalente.)")
    familia = list(abajo)
    familia.append((a, b))
    familia.extend(arriba)
    tiras = _eqf_tiras(familia, saber)
    if tiras:
        L += ["", "  LAS TIRAS (el mismo entero, partido de distintas maneras: lo tomado mide lo mismo):"] + tiras
    if not todo_ok:
        L.append("  ALGO NO CUADRA en la vuelta")
    L += ["", "RESULTADO: %s" % " = ".join("%d/%d" % f for f in familia)]
    return "\n".join(L)


# ---------------------------------------------------------------- equivalentes: 2/3 y 8/12  /  2/3 = 8/12

def decidir_pareja(fa, fb, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = {"a": fa, "b": fb}
    if 0 in (fa[1], fb[1]):
        r.update(conclusion="imposible", porque="no se puede partir un entero en CERO partes")
        return r
    p = _eqf_problema((fa[0], fa[1], fb[0], fb[1]), saber)
    if p:
        r.update(conclusion=p[0], porque=p[1])
        return r
    if fa[0] == 0 or fb[0] == 0:
        r.update(conclusion="hecho", valor=fa[0] == fb[0], formas=("0" if fa[0] == 0 else "?", "0" if fb[0] == 0 else "?"),
                 porque="las dos son cero" if fa[0] == fb[0] else "una es cero y la otra no", trampas=[])
        return r
    ra, rb = _eqf_simplificar(fa[0], fa[1], saber), _eqf_simplificar(fb[0], fb[1], saber)
    for x in (ra, rb):
        if x["conclusion"] != "hecho":
            r.update(conclusion="todavia_no", porque=x.get("porque") or x["conclusion"])
            return r
    r.update(conclusion="hecho", valor=ra["valor"] == rb["valor"], formas=(ra["valor"], rb["valor"]),
             metodos=(ra["resultado"]["metodo"], rb["resultado"]["metodo"]),
             vueltas=(ra["resultado"]["vuelta_ok"], rb["resultado"]["vuelta_ok"]))
    # la relacion horizontal, si la hay (de la pequena a la grande)
    chica, grande = (fb, fa) if viene_despues(decir(fa[1], saber), decir(fb[1], saber), saber) else (fa, fb)
    ka, kb = _eqf_justo(grande[0], chica[0], saber), _eqf_justo(grande[1], chica[1], saber)
    r["horizontal"] = (chica, grande, ka, kb)
    # LAS TRAMPAS
    trampas = []
    if not r["valor"] and chica != grande:
        if not viene_despues(decir(chica[0], saber), decir(grande[0], saber), saber):
            da = aplicar("restar", {"a": grande[0], "b": chica[0]}, saber).get("valor")
            db = aplicar("restar", {"a": grande[1], "b": chica[1]}, saber).get("valor")
            if da is not None and da == db and da != 0:
                trampas.append("de %d/%d a %d/%d se SUMA %d arriba y abajo: sumar lo mismo NO da una equivalente; "
                               "hay que MULTIPLICAR (o dividir) los dos por el mismo numero"
                               % (chica[0], chica[1], grande[0], grande[1], da))
        if ka is not None and kb is not None and ka != kb:
            trampas.append("arriba es POR %d y abajo POR %d: no es el MISMO numero" % (ka, kb))
    if r["valor"] and fa != fb:
        trampas.append("los numeros de %d/%d son mas grandes, pero VALE LO MISMO que %d/%d: sus partes son mas pequenas "
                       "y se toman mas" % (grande[0], grande[1], chica[0], chica[1]))
    r["trampas"] = trampas
    return r


def explicar_pareja(fa, fb, saber, como_verdad=False):
    r = decidir_pareja(fa, fb, saber)
    L = ["PREGUNTA (F.6): %d/%d y %d/%d son EQUIVALENTES (valen lo mismo)?  (NCETM 3.7, punto 1)" % (fa[0], fa[1], fb[0], fb[1]), ""]
    if r["conclusion"] != "hecho":
        etiqueta = {"imposible": "NO SE PUEDE"}.get(r["conclusion"], "TODAVIA NO")
        return "\n".join(L + ["  %s: %s" % (etiqueta, r["porque"]), "", "RESULTADO: %s" % r["conclusion"]])
    si = r["valor"]
    if "metodos" not in r:
        L.append("  %s." % r["porque"])
    else:
        L.append("  1. SIMPLIFICO LAS DOS (dividiendo entre los factores comunes; cada una con su vuelta):")
        L.append("        %d/%d = %s   (%s)" % (fa[0], fa[1], r["formas"][0], r["metodos"][0]))
        L.append("        %d/%d = %s   (%s)" % (fb[0], fb[1], r["formas"][1], r["metodos"][1]))
        L.append("     %s" % ("LA MISMA forma mas simple: son EQUIVALENTES." if si else
                              "formas mas simples DISTINTAS: NO son equivalentes."))
        chica, grande, ka, kb = r["horizontal"]
        if si and ka is not None and ka == kb and chica != grande:
            L.append("  2. Y SE VE LA RELACION HORIZONTAL: %d/%d -> %d/%d, arriba y abajo POR %d (%d x %d = %d, %d x %d = %d)"
                     % (chica[0], chica[1], grande[0], grande[1], ka, chica[0], ka, grande[0], chica[1], ka, grande[1]))
    for t in r["trampas"]:
        L.append("  LA TRAMPA: %s." % t)
    if como_verdad:
        return "\n".join(L + ["", "RESULTADO: %s" % ("VERDADERO" if si else "FALSO")])
    return "\n".join(L + ["", "RESULTADO: %s" % ("si" if si else "no")])


# ---------------------------------------------------------------- 2/3 = ?/12

def explicar_hueco_equivalente(izq, der, saber):
    """izq, der: (arriba, abajo) con None en el hueco."""
    txt = lambda f: "%s/%s" % tuple("?" if v is None else "%d" % v for v in f)
    L = ["PREGUNTA (F.6): %s = %s, que numero va en el hueco?  (NCETM 3.7, punto 2)" % (txt(izq), txt(der)), ""]
    completa, con_hueco = (der, izq) if None in izq else (izq, der)
    p, q = completa
    x, y = con_hueco
    if q == 0 or y == 0:
        return "\n".join(L + ["  NO SE PUEDE: no se puede partir un entero en CERO partes", "", "RESULTADO: imposible"])
    pr = _eqf_problema((p, q, x, y), saber)
    if pr:
        return "\n".join(L + ["  TODAVIA NO: %s" % pr[1], "", "RESULTADO: %s" % pr[0]])
    if p == 0 or x == 0:
        if p == 0 and x is None:
            return "\n".join(L + ["  0/%d es cero: la otra tambien tiene que ser cero: 0/%d." % (q, y), "", "RESULTADO: 0"])
        if p == 0 and x == 0:
            return "\n".join(L + ["  las dos son cero: abajo vale cualquier numero (menos el 0).", "",
                                  "RESULTADO: cualquiera"])
        return "\n".join(L + ["  una es cero y la otra no: no hay ningun numero que las haga iguales.", "",
                              "RESULTADO: no_sale"])
    r = aplicar("hueco_equivalente", {"completa": completa, "con_hueco": con_hueco}, saber)
    L.append("  PRUEBO TODO LO QUE SE:")
    L += _eqf_tabla(r)
    L.append("")
    if r["conclusion"] != "hecho":
        sin_entero = [f["no_salio"] for f in r["candidatos"]
                      if f["id"] == "hueco_simplificando_primero" and "NO HAY NINGUN ENTERO" in f.get("no_salio", "")]
        if sin_entero:
            return "\n".join(L + ["  %s." % sin_entero[0], "", "RESULTADO: no_sale"])
        return "\n".join(L + ["  TODAVIA NO: %s" % (r.get("porque") or r["conclusion"]), "", "RESULTADO: todavia_no"])
    res = r["resultado"]
    L.append("  %s:" % res["metodo"].upper())
    L.append("        %s" % res["cuenta"])
    L.append("        %d/%d = %d/%d  (arriba y abajo, POR EL MISMO numero)" % (p, q, res["fraccion"][0], res["fraccion"][1]))
    L.append("")
    L.append("  LA VUELTA: %s ... %s" % (res["vuelta"], "SI" if res["vuelta_ok"] else "NO"))
    L += ["", "RESULTADO: %d" % res["valor"]]
    return "\n".join(L)


# ---------------------------------------------------------------- la puerta

def explicar_orden_equivalentes(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    t = _eqf_limpio(texto)
    m = _EQF_SIMPLIFICAR.match(t)
    if m:
        return explicar_simplificar(int(m.group(1)), int(m.group(2)), saber)
    m = _EQF_PAREJA.match(t)
    if m:
        g = [int(v) for v in m.groups()]
        return explicar_pareja((g[0], g[1]), (g[2], g[3]), saber)
    m = _EQF_FAMILIA.match(t)
    if m:
        return explicar_familia(int(m.group(1)), int(m.group(2)), saber)
    m = _EQF_IGUALDAD.match(t)
    if m:
        g = [int(v) for v in m.groups()]
        return explicar_pareja((g[0], g[1]), (g[2], g[3]), saber, como_verdad=True)
    m = _EQF_HUECO.match(t)
    if m and t.count("?") == 1:
        g = [None if v == "?" else int(v) for v in m.groups()]
        return explicar_hueco_equivalente((g[0], g[1]), (g[2], g[3]), saber)
    return ("NO ENTIENDO ESTO: se escribe asi:  equivalentes: 2/3    simplificar: 12/18    2/3 = ?/12\n"
            "                                    equivalentes: 2/3 y 8/12    2/3 = 8/12")
