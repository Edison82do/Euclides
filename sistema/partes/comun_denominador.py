# -*- coding: utf-8 -*-
"""
Euclides - EL MISMO DE ABAJO: SUMAR Y RESTAR FRACCIONES CON DISTINTO DE ABAJO (paso F.7, 8 oct 2026; 5.o).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

NCETM 3.8 (Common denomination: more adding and subtracting), los cinco puntos:
  1-3 fracciones RELACIONADAS (1/2 y 1/4; 3/4 y 5/8): se cambia UNA para que tengan el mismo de abajo;
  4   NO relacionadas (1/3 y 1/4): el PRODUCTO de los de abajo sirve de denominador comun;
  5   comparar: pasarlas al mismo de abajo es uno de varios metodos (piezas fracciones_con_el_mismo_de_*).
Common Core 5.NF.A.1 (tambien con mixtos) y 5.NF.A.2 (el error 1/2 + 1/3 = 2/5 se caza porque 2/5 < 1/2).
Las cuentas las hacen las piezas (mismo_de_abajo_*) y las de siempre (sumar, restar, simplificar_fraccion);
aqui se pide cada paso y se explica.  fracciones.py manda aqui las cuentas con distinto de abajo.
"""


def _cd_texto(f):
    return "%d/%d" % f


def decidir_cuenta_distintas(fa, signo, fb, saber=None):
    """fa, fb: (arriba, abajo) con distinto de abajo.  Devuelve {conclusion, valor: (arriba, abajo) en su forma mas
    simple, sin_simplificar: (S, D), comun: lo de mismo_de_abajo, vuelta, vuelta_ok, error_tipico ...}."""
    if saber is None:
        saber = cargar_conocimiento()
    r = {"a": fa, "b": fb, "signo": signo, "distintas": True}
    for f in (fa, fb):
        p = _fr_problema(f[0], f[1], saber)
        if p:
            r.update(conclusion=p[0], porque=p[1])
            return r
    comun = aplicar("mismo_de_abajo", {"a": fa, "b": fb}, saber)
    r["comun"] = comun
    if comun["conclusion"] != "hecho":
        r.update(conclusion="todavia_no", porque=comun.get("porque") or "no encuentro el mismo de abajo")
        return r
    (xa, d), (xb, _) = comun["valor"]
    r["nuevas"] = comun["valor"]
    if signo == "-" and viene_despues(decir(xb, saber), decir(xa, saber), saber):
        r.update(conclusion="imposible", porque="%d/%d es MAYOR que %d/%d (%d/%d contra %d/%d): se quita mas de lo que "
                 "hay" % (fb[0], fb[1], fa[0], fa[1], xb, d, xa, d))
        return r
    preg = "sumar" if signo == "+" else "restar"
    x = aplicar(preg, {"a": xa, "b": xb}, saber)
    if x["conclusion"] != "hecho":
        r.update(conclusion="todavia_no", porque=x.get("porque") or "no me sale %d %s %d" % (xa, signo, xb))
        return r
    s = x["valor"]
    r["metodo"] = x["pieza"]["nombre"]
    r["sin_simplificar"] = (s, d)
    # LA VUELTA (sumar y restar son inversas), y la primera, dividida de vuelta, tiene que ser la de partida
    inv = aplicar("restar" if signo == "+" else "sumar", {"a": s, "b": xb}, saber).get("valor")
    k = comun["resultado"]["por"][0]
    va = aplicar("dividir", {"total": inv, "divisor": k}, saber) if inv is not None else {"conclusion": "no"}
    vd = aplicar("dividir", {"total": d, "divisor": k}, saber)
    vuelta_ok = inv == xa and va.get("conclusion") == "hecho" and (va["valor"], vd["valor"]) == fa \
        and not va["resultado"].get("resto", 0) and not vd["resultado"].get("resto", 0)
    r["vuelta"] = "%d/%d %s %d/%d = %s/%d%s" % (
        s, d, "-" if signo == "+" else "+", xb, d, inv, d,
        "" if k == 1 else ", y %s/%d entre %d -> %s/%s" % (inv, d, k, va.get("valor"), vd.get("valor")))
    r["vuelta_ok"] = vuelta_ok
    # SIMPLIFICAR al final (F.6), si se puede
    if s == 0:
        r["valor"], r["simplificado"] = (0, d), None
    else:
        simp = aplicar("simplificar_fraccion", {"a": s, "b": d}, saber)
        if simp["conclusion"] == "hecho":
            r["valor"] = (simp["resultado"]["arriba"], simp["resultado"]["abajo"])
            r["simplificado"] = simp["resultado"]
        else:
            r["valor"], r["simplificado"] = (s, d), None
    r["error_tipico"] = _cd_error_tipico(fa, signo, fb, xa, xb, saber)
    r["conclusion"] = "hecho" if vuelta_ok else "no_cuadra"
    if not vuelta_ok:
        r["porque"] = "la vuelta no cuadra (%s)" % r["vuelta"]
    return r


def _cd_error_tipico(fa, signo, fb, xa, xb, saber):
    """El error de 'arriba con arriba y abajo con abajo' (5.NF.A.2), y por que se ve que esta mal SIN la cuenta buena:
    1/2 + 1/3 = 2/5, pero 2/5 es menor que 1/2.  None si no se puede decir."""
    if signo == "+":
        ea = aplicar("sumar", {"a": fa[0], "b": fb[0]}, saber).get("valor")
        eb = aplicar("sumar", {"a": fa[1], "b": fb[1]}, saber).get("valor")
        mayor = fb if viene_despues(decir(xb, saber), decir(xa, saber), saber) else fa
        if ea is None or eb is None:
            return None
        c = aplicar("comparar_fracciones", {"a": (ea, eb), "b": mayor}, saber)
        if c["conclusion"] == "hecho" and c["valor"] == "<":
            return ("%s + %s NO es %d/%d (sumar arriba con arriba y abajo con abajo): %d/%d es MENOR que %s, y sumarle "
                    "algo no puede dar menos" % (_cd_texto(fa), _cd_texto(fb), ea, eb, ea, eb, _cd_texto(mayor)))
        return None
    if viene_despues(decir(fb[1], saber), decir(fa[1], saber), saber) or fa[1] == fb[1]:
        return None
    ea = aplicar("restar", {"a": fa[0], "b": fb[0]}, saber)
    eb = aplicar("restar", {"a": fa[1], "b": fb[1]}, saber)
    if ea["conclusion"] != "hecho" or eb["conclusion"] != "hecho":
        return None
    c = aplicar("comparar_fracciones", {"a": (ea["valor"], eb["valor"]), "b": fa}, saber)
    if c["conclusion"] == "hecho" and c["valor"] == ">":
        return ("%s - %s NO es %d/%d (restar arriba con arriba y abajo con abajo): %d/%d es MAYOR que %s, y quitarle "
                "algo no puede dar mas" % (_cd_texto(fa), _cd_texto(fb), ea["valor"], eb["valor"], ea["valor"],
                                           eb["valor"], _cd_texto(fa)))
    return None


def explicar_cuenta_distintas(fa, signo, fb, saber, mixtos=None):
    """mixtos: (x, y) en la forma de _fr_termino si la cuenta venia con numeros mixtos (ya pasados a impropias)."""
    r = decidir_cuenta_distintas(fa, signo, fb, saber)
    izq, der = (_fr_texto_termino(mixtos[0]), _fr_texto_termino(mixtos[1])) if mixtos else (_cd_texto(fa), _cd_texto(fb))
    L = ["PREGUNTA (F.7): %s %s %s  (NCETM 3.8: el mismo de abajo; 5.NF.A.1)" % (izq, signo, der), ""]
    if mixtos:
        L.append("  0. LOS MIXTOS, A IMPROPIAS (F.4): %s = %s y %s = %s" % (izq, _cd_texto(fa), der, _cd_texto(fb)))
    if r["conclusion"] in ("todavia_no", "imposible") and "comun" not in r:
        etiqueta = {"imposible": "NO SE PUEDE"}.get(r["conclusion"], "TODAVIA NO")
        return "\n".join(L + ["  %s: %s" % (etiqueta, r["porque"]), "", "RESULTADO: %s" % r["conclusion"]])
    L.append("  1. las partes son de TAMANOS DISTINTOS (1/%d y 1/%d): asi no se pueden contar juntas." % (fa[1], fb[1]))
    L.append("     Busco el MISMO DE ABAJO (el denominador comun).  PRUEBO TODO LO QUE SE:")
    L += ["  " + x for x in _eqf_tabla(r["comun"])]
    if r["comun"]["conclusion"] != "hecho":
        return "\n".join(L + ["", "  TODAVIA NO: %s" % r["porque"], "", "RESULTADO: todavia_no"])
    res = r["comun"]["resultado"]
    (xa, d), (xb, _) = r["nuevas"]
    L.append("     %s:" % res["metodo"].upper())
    L.append("        %s" % res["cuenta"])
    L.append("        la vuelta (divido de vuelta): %s ... %s" % (res["vuelta"], "SI" if res["vuelta_ok"] else "NO"))
    L.append("     %s %s %s  =  %d/%d %s %d/%d" % (_cd_texto(fa), signo, _cd_texto(fb), xa, d, signo, xb, d))
    if r["conclusion"] == "imposible":
        return "\n".join(L + ["", "  NO SE PUEDE: %s." % r["porque"], "", "RESULTADO: imposible"])
    if r["conclusion"] == "todavia_no":
        return "\n".join(L + ["", "  TODAVIA NO: %s" % r["porque"], "", "RESULTADO: todavia_no"])
    s, _ = r["sin_simplificar"]
    L.append("  2. ahora las partes son del MISMO TAMANO (1/%d): se cuentan como en F.3" % d)
    L.append("     %d %s %d = %d  (%s);  el de abajo NO cambia -> %d/%d" % (xa, signo, xb, s, r["metodo"], s, d))
    L.append("  3. LA VUELTA: %s ... %s" % (r["vuelta"], "SI" if r["vuelta_ok"] else "NO"))
    simp = r["simplificado"]
    if s == 0:
        L.append("  4. %d/%d: no queda ninguna parte, es CERO." % (s, d))
    elif simp is None:
        L.append("  4. %d/%d: no se simplificarla todavia (se queda asi)." % (s, d))
    elif (simp["arriba"], simp["abajo"]) == (s, d):
        L.append("  4. %d/%d ya esta en su forma mas simple (%s)." % (s, d, simp["por_que_ya"]))
    else:
        L.append("  4. SIMPLIFICO (F.6, %s): %d/%d = %s  (la vuelta: %s ... %s)" % (
            simp["metodo"], s, d, simp["valor"], simp["vuelta"], "SI" if simp["vuelta_ok"] else "NO"))
    final = _fr_texto_valor(r["valor"], saber)
    a, b = r["valor"]
    if b != 1 and a != 0 and viene_despues(decir(a, saber), decir(b, saber), saber):
        L.append("     %d/%d es mas de un entero (F.4): %d/%d = %s" % (a, b, a, b, final))
    if r["error_tipico"] and not mixtos:
        L.append("")
        L.append("  EL ERROR TIPICO (5.NF.A.2): %s." % r["error_tipico"])
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["", "  ALGO NO CUADRA: %s" % r["porque"], "", "RESULTADO: no_cuadra"])
    L += ["", "RESULTADO: %s" % final]
    return "\n".join(L)
