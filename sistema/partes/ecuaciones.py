# -*- coding: utf-8 -*-
"""
Euclides - ECUACIONES CON HUECO (paso E.1 del plan pedagogico, 5 oct 2026).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

Common Core 1.OA.D.8: 'determinar el numero desconocido que hace verdadera una ecuacion de suma o
resta con tres numeros' (8 + ? = 11, 5 = _ - 3, 6 + 6 = _).  CGI: cada sitio del hueco ES un tipo
de problema.  Asi que aqui NO se resuelve nada: se LEE la ecuacion, se traduce a la SITUACION de un
problema (la misma que usa el resolvedor, R.1), y la resuelven las piezas de pasos que ya existen.
Despues se COMPRUEBA con lo de E.0: se pone el numero en el hueco y se pregunta si es verdad.
"""

import re

_HUECOS = ("?", "_", "□")          # ?, _ (o __), el cuadradito
_TROZO = re.compile("[\\d\\s+\\-=?_\u25a1\u2212x*\u00d7:\u00f7/]*=[\\d\\s+\\-=?_\u25a1\u2212x*\u00d7:\u00f7/]*")


def _es_hueco(x):
    return x in _HUECOS or (x and set(x) == {"_"})


def _leer_lado(x):
    """'8 + ?' -> {"a": 8, "op": "+", "b": "?"};  '11' -> {"n": 11};  '?' -> {"n": "?"}."""
    x = re.sub("\\s*([+\\-x*\u00d7:\u00f7/])\\s*", r" \1 ", x.lower()).strip()
    x = " ".join(x.split())
    partes = x.split(" ")
    def valor(p):
        if _es_hueco(p):
            return "?"
        return int(p) if p.isdigit() else None
    if len(partes) == 1:
        v = valor(partes[0])
        return None if v is None else {"n": v}
    if len(partes) == 3 and partes[1] in ("+", "-", "x", "*", "\u00d7", ":", "\u00f7", "/"):
        a, b = valor(partes[0]), valor(partes[2])
        if a is None or b is None:
            return None
        op = {"*": "x", "\u00d7": "x", "\u00f7": ":", "/": ":"}.get(partes[1], partes[1])
        return {"a": a, "op": op, "b": b}
    return None


def leer_ecuacion(texto):
    """Busca la ecuacion dentro del texto (las palabras de alrededor no molestan) y la lee.
    Devuelve {"lados": [izq, der], "texto": ...} o {"error": porque}."""
    t = texto.replace("−", "-").replace("¿", " ")
    t = re.sub(r"(\d)\s*\?\s*$", r"\1", t.strip())      # '... = 11?' : ese ? es de la pregunta
    trozos = [m.group(0) for m in _TROZO.finditer(t) if re.search(r"\d", m.group(0))]
    if not trozos:
        return {"error": "no veo ninguna ecuacion (hace falta un =)"}
    eq = max(trozos, key=len).strip()
    eq = re.sub("^[\\s:\u00f7/x*\u00d7+\\-]+|[\\s:\u00f7/x*\u00d7+\\-]+$", "", eq)   # ": 3 x ? = 12" (los dos puntos eran del texto)
    lados_txt = eq.split("=")
    if len(lados_txt) != 2:
        return {"error": "hay %s signos =: aqui va una ecuacion con UN =" % len(lados_txt[1:])}
    lados = [_leer_lado(x) for x in lados_txt]
    if None in lados:
        return {"error": "no entiendo uno de los lados de '%s'" % eq}
    return {"lados": lados, "texto": " = ".join(_escribir_lado(l) for l in lados)}


def _escribir_lado(l, hueco="?"):
    def e(v):
        return hueco if v == "?" else str(v)
    if "n" in l:
        return e(l["n"])
    return "%s %s %s" % (e(l["a"]), l["op"], e(l["b"]))


def _huecos(l):
    return [k for k in ("a", "b", "n") if l.get(k) == "?"]


# la ecuacion -> la situacion de un problema (CGI).  Las historias en lenguaje rustico (6).
_TIPOS = {
    ("+", "resultado"): ("juntar, con el RESULTADO desconocido",
                         "tenia {a}, le dan {b}: cuantos tiene ahora?"),
    ("+", "cambio"): ("juntar, con el CAMBIO desconocido",
                      "tenia {a}, le dan algunos, ahora tiene {c}: cuantos le dieron?"),
    ("+", "comienzo"): ("juntar, con el COMIENZO desconocido (el mas dificil)",
                        "tenia algunos, le dan {b}, ahora tiene {c}: cuantos tenia al principio?"),
    ("-", "resultado"): ("separar, con el RESULTADO desconocido",
                         "tenia {a}, se van {b}: cuantos quedan?"),
    ("-", "cambio"): ("separar, con el CAMBIO desconocido",
                      "tenia {a}, se van algunos, quedan {c}: cuantos se fueron?"),
    ("-", "comienzo"): ("separar, con el COMIENZO desconocido (el mas dificil)",
                        "tenia algunos, se van {b}, quedan {c}: cuantos tenia al principio?"),
}


def _montar_ecuacion(lados):
    """Devuelve (situacion, tipo, cuenta, total_a_la_izquierda) o {"error"/"balanza"/...}."""
    huecos = sum((_huecos(l) for l in lados), [])
    if not huecos:
        return {"sin_hueco": True}
    if len(huecos) > 1:
        return {"dos_huecos": True}
    con_op = [l for l in lados if "op" in l]
    if len(con_op) != 1:
        if not con_op:
            return {"error": "no hay ninguna suma ni resta"}
        return {"balanza": True}
    cuenta = con_op[0]
    otro = [l for l in lados if l is not cuenta][0]
    a, op, b, c = cuenta["a"], cuenta["op"], cuenta["b"], otro["n"]
    if c == "?":
        donde = "resultado"
        sit = {"tipo": "cambio", "antes": a, "signo": op, "n": b}
    elif b == "?":
        donde = "cambio"
        sit = {"tipo": "cambio_desconocido", "antes": a, "despues": c, "signo": op}
    else:
        donde = "comienzo"
        sit = {"tipo": "deshacer", "despues": c, "signo": op, "n": b}
    nombre, historia = _TIPOS[(op, donde)]
    return {"situacion": sit, "donde": donde, "tipo": nombre,
            "historia": historia.format(a=a, b=b, c=c),
            "izquierda": lados.index(cuenta) == 1}


def decidir_ecuacion(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    e = leer_ecuacion(texto)
    if "error" in e:
        return {"conclusion": "no_entiendo", "porque": e["error"]}
    for l in e["lados"]:
        for k in ("a", "b", "n"):
            if isinstance(l.get(k), int) and decir(l[k], saber) is None:
                return {"conclusion": "no_entiendo", "porque": "solo se contar hasta mil"}
    r = {"ecuacion": e["texto"], "lados": e["lados"]}
    if any(l.get("op") in ("x", ":") for l in e["lados"]):
        return _resolver_por(e, r, saber)
    m = _montar_ecuacion(e["lados"])
    if m.get("sin_hueco"):
        r.update(conclusion="sin_hueco", porque="no hay ningun hueco que buscar (para saber si es "
                 "verdad: 'verdad: %s')" % e["texto"])
        return r
    if m.get("dos_huecos"):
        r.update(conclusion="dos_huecos", porque="hay DOS huecos: muchos numeros sirven (5 y 5, 3 y 7...). "
                 "Eso es de mas adelante (NCETM 1.31: problemas con dos desconocidos)")
        return r
    if m.get("balanza"):
        return _resolver_balanza(e, r, saber)
    if "error" in m:
        r.update(conclusion="no_entiendo", porque=m["error"])
        return r
    r.update(m)
    p = aplicar("paso", m["situacion"], saber)
    r["paso"] = p
    if p["conclusion"] != "hecho":
        r.update(conclusion="imposible" if p["conclusion"] == "imposible" else "no_se",
                 porque=p.get("porque"))
        return r
    v = p["valor"]
    r["valor"] = v
    # LA COMPROBACION, con lo de E.0: el numero en el hueco, y es verdad?
    con_numero = " = ".join(_escribir_lado(l, str(v)) for l in e["lados"])
    comp = decidir_igualdad(con_numero, saber)
    r["comprobacion"] = con_numero
    r["comprobacion_ok"] = comp.get("valor") == "verdadero"
    r["conclusion"] = "hecho" if r["comprobacion_ok"] else "no_cuadra"
    return r


def explicar_ecuacion(texto, saber=None):
    r = decidir_ecuacion(texto, saber)
    if r.get("por"):
        return _explicar_por(r)
    if r["conclusion"] == "todavia_no":
        return "PREGUNTA (E.1): %s\n\n  TODAVIA NO: %s\n\nRESULTADO: todavia_no" % (texto.strip(), r["porque"])
    if r["conclusion"] == "no_entiendo":
        return ("NO ENTIENDO ESTO: %s.\n"
                "   se escribe asi:  8 + ? = 11     (o  ecuacion: 5 = ? - 3)" % r.get("porque", ""))
    L = ["PREGUNTA (E.1): que numero va en el hueco?   %s" % r["ecuacion"], ""]
    if r["conclusion"] in ("sin_hueco", "dos_huecos", "balanza"):
        L.append("  %s" % r["porque"])
        L.append("")
        L.append("RESULTADO: %s" % r["conclusion"])
        return "\n".join(L)
    if r.get("balanza"):
        return _explicar_balanza(r)
    L.append("  1. LEER: es %s." % r["tipo"])
    L.append("     Contado como una historia: %s" % r["historia"])
    if r["izquierda"]:
        L.append("     (el resultado esta a la IZQUIERDA del =: da igual, el = es 'es el mismo numero que', E.0)")
    L.append("")
    L.append("  2. PRUEBO TODO LO QUE SE (las piezas de los problemas, R.1):")
    p = r["paso"]
    for f in p["candidatos"]:
        if f.get("aplica"):
            L.append("        [SI]  %s  (%s)" % (f["nombre"], f["unidad"]))
        else:
            L.append("        [no]  %-46s porque %s" % (f["nombre"], f.get("descartado") or f.get("no_salio")))
    L.append("")
    if r["conclusion"] in ("imposible", "no_se"):
        L.append("  NO HAY NUMERO QUE VAYA EN EL HUECO: %s" % r.get("porque"))
        L.append("")
        L.append("RESULTADO: %s" % r["conclusion"])
        return "\n".join(L)
    calc = p["resultado"]
    L.append("  3. APLICO: %s  ->  %s" % (p["pieza"]["nombre"], p["pieza"]["que_hace"]))
    L.append("     CALCULO con %s: %s" % (calc["resultado"]["metodo"], calc["resultado"]["cuenta"]))
    L.append("")
    L.append("  4. COMPRUEBO (E.0): pongo el %d en el hueco -> %s ... %s"
             % (r["valor"], r["comprobacion"], "VERDADERO" if r["comprobacion_ok"] else "FALSO"))
    L.append("")
    L.append("RESULTADO: %d" % r["valor"])
    return "\n".join(L)


def _resolver_balanza(e, r, saber):
    """E.2: cuentas a los DOS lados del =.  Pregunta a las piezas de 'balanza'."""
    izq, der = e["lados"]
    con_hueco, completo = (izq, der) if _huecos(izq) else (der, izq)
    r["balanza"] = True
    r["tipo"] = "una BALANZA: hay cuentas a los dos lados del =, y los dos platos pesan lo mismo"
    b = aplicar("balanza", {"completo": completo, "con_hueco": con_hueco}, saber)
    r["paso"] = b
    if b["conclusion"] != "hecho":
        r.update(conclusion="imposible", porque=b.get("porque"))
        return r
    v = b["valor"]
    r["valor"] = v
    con_numero = " = ".join(_escribir_lado(l, str(v)) for l in e["lados"])
    r["comprobacion"] = con_numero
    r["comprobacion_ok"] = decidir_igualdad(con_numero, saber).get("valor") == "verdadero"
    # LAS DOS RESPUESTAS EQUIVOCADAS FAMOSAS (Falkner, Levi y Carpenter): poner lo que 'da' el plato
    # completo (12), o sumar todo lo que se ve (17).  Se prueban en el hueco con E.0.
    trampas = []
    vc = aplicar("sumar" if completo["op"] == "+" else "restar",
                 {"a": completo["a"], "b": completo["b"]}, saber)
    if vc["conclusion"] == "hecho":
        candidatos = [(vc["valor"], "poner lo que da %s (leer el = como 'da')" % _escribir_lado(completo))]
        k = con_hueco["a"] if con_hueco["b"] == "?" else con_hueco["b"]
        if completo["op"] == "+" and con_hueco["op"] == "+":
            todo = aplicar("sumar", {"a": vc["valor"], "b": k}, saber)
            if todo["conclusion"] == "hecho":
                candidatos.append((todo["valor"], "sumar todo lo que se ve"))
        for n, porque in candidatos:
            if n == v:
                continue
            t = " = ".join(_escribir_lado(l, str(n)) for l in e["lados"])
            ok = decidir_igualdad(t, saber).get("valor")
            trampas.append("%d NO (%s): %s es %s" % (n, porque, t, (ok or "imposible").upper()))
    r["trampas"] = trampas
    r["conclusion"] = "hecho" if r["comprobacion_ok"] else "no_cuadra"
    return r


def _explicar_balanza(r):
    L = ["PREGUNTA (E.2): que numero va en el hueco?   %s" % r["ecuacion"], ""]
    L.append("  1. LEER: es %s." % r["tipo"])
    L.append("     (el = no dice 'da': dice que los DOS lados son el mismo numero, E.0)")
    L.append("")
    L.append("  2. PRUEBO TODO LO QUE SE:")
    b = r["paso"]
    elegida = b.get("pieza", {}).get("id")
    for f in b["candidatos"]:
        if f.get("descartado"):
            L.append("        [no]  %-52s porque %s" % (f["nombre"], f["descartado"]))
        elif f.get("no_salio"):
            L.append("        [no]  %-52s no salio: %s" % (f["nombre"], f["no_salio"]))
        elif f["id"] == elegida:
            L.append("        [SI]  %-52s <- el mas corto que encaja: ESTE" % f["nombre"])
        else:
            L.append("        [si]  %-52s tambien servia (es mas largo)" % f["nombre"])
    L.append("")
    if r["conclusion"] == "imposible":
        L.append("  NO HAY NUMERO QUE VAYA EN EL HUECO: %s" % r.get("porque"))
        L.append("")
        L.append("RESULTADO: imposible")
        return "\n".join(L)
    L.append("  3. %s" % b["resultado"]["cuenta"])
    L.append("")
    L.append("  4. COMPRUEBO (E.0): pongo el %d en el hueco -> %s ... %s"
             % (r["valor"], r["comprobacion"], "VERDADERO" if r["comprobacion_ok"] else "FALSO"))
    if r.get("trampas"):
        L.append("")
        L.append("  5. LAS RESPUESTAS EQUIVOCADAS DE SIEMPRE, y por que no:")
        for t in r["trampas"]:
            L.append("        %s" % t)
    L.append("")
    L.append("RESULTADO: %d" % r["valor"])
    return "\n".join(L)



# ---------------------------------------------------------------- E.4: el hueco en x y :

_HISTORIAS_POR = {
    ("x", "resultado"): ("el PRODUCTO: {a} grupos de {b}, cuantos son?", "multiplicar"),
    ("x", "b"): ("cuantos hay EN CADA GRUPO: {a} grupos iguales hacen {c} -> REPARTIR {c} entre {a}", "repartir"),
    ("x", "a"): ("CUANTOS GRUPOS: grupos de {b} hasta hacer {c} -> AGRUPAR {c} en grupos de {b}", "agrupar"),
    (":", "resultado"): ("el COCIENTE: {a} repartido entre {b} (o en grupos de {b})", "dividir"),
    (":", "b"): ("el DIVISOR: entre cuantos se reparte {a} para que toquen {c}? -> AGRUPAR {a} en grupos de {c}", "agrupar"),
    (":", "a"): ("el DIVIDENDO: cuanto habia, si al repartir entre {b} tocan {c}? -> deshacer: {c} x {b}", "multiplicar"),
}


def _resolver_por(e, r, saber):
    """E.4 (3.OA.A.4): el hueco en una multiplicacion o division.  El SITIO del hueco dice que se
    busca (NCETM 2.6); se resuelve con multiplicar o dividir (M.1-M.3) y se comprueba con E.0."""
    r["por"] = True
    huecos = sum((_huecos(l) for l in e["lados"]), [])
    if not huecos:
        r.update(conclusion="sin_hueco", porque="no hay ningun hueco (para saber si es verdad: 'verdad: %s')" % e["texto"])
        return r
    if len(huecos) > 1:
        r.update(conclusion="dos_huecos", porque="hay DOS huecos: muchos numeros sirven (2 y 6, 3 y 4...)")
        return r
    con_op = [l for l in e["lados"] if "op" in l]
    if len(con_op) != 1:
        r.update(conclusion="todavia_no", porque="cuentas a los DOS lados del = con x o : (la balanza con x): todavia no")
        return r
    c_ = con_op[0]
    otro = [l for l in e["lados"] if l is not c_][0]
    a, op, b, c = c_["a"], c_["op"], c_["b"], otro["n"]
    donde = "resultado" if c == "?" else ("b" if b == "?" else "a")
    frase, como = _HISTORIAS_POR[(op, donde)]
    tipo = frase.format(a=a, b=b, c=c)
    if 0 in (a, b) and donde != "resultado":            # con un cero no hay reparto que contar
        tipo = tipo.split(" -> ")[0]
    r.update(tipo=tipo, como=como, izquierda=e["lados"].index(c_) == 1)

    def dividir_justo(total, d):
        p = aplicar("dividir", {"total": total, "divisor": d}, saber)
        r["paso"] = p
        if p["conclusion"] != "hecho":
            return None, "%d : %d no se puede (%s)" % (total, d, p.get("porque"))
        if p["resultado"].get("resto"):
            return None, ("%d no se reparte justo: da %d y sobra %d. No hay un numero entero que haga verdad la igualdad"
                          % (total, p["valor"], p["resultado"]["resto"]))
        return p["valor"], None

    def multiplicar(x, y):
        p = aplicar("multiplicar", {"a": x, "b": y}, saber)
        r["paso"] = p
        return (p.get("valor"), None) if p["conclusion"] == "hecho" else (None, "me paso de mil")

    if op == "x" and donde == "resultado":
        v, porque = multiplicar(a, b)
    elif op == "x":
        conocido = a if donde == "b" else b
        if conocido == 0:
            if c == 0:
                r.update(conclusion="cualquiera", porque="un factor es cero: el producto es 0 ponga lo que ponga en el "
                         "hueco. CUALQUIER numero vale")
            else:
                r.update(conclusion="imposible", porque="un factor es cero: el producto siempre es 0, nunca %d" % c)
            return r
        v, porque = dividir_justo(c, conocido)
    elif donde == "resultado":
        v, porque = dividir_justo(a, b)
    elif donde == "b":
        if c == 0:
            if a:
                r.update(conclusion="imposible", porque="para que toquen 0 habria que repartir entre nadie: no se puede")
            else:
                r.update(conclusion="cualquiera", porque="0 repartido entre cualquiera (menos cero) da 0: cualquier "
                         "numero, menos el cero, vale")
            return r
        v, porque = dividir_justo(a, c)
    else:
        if b == 0:
            r.update(conclusion="imposible", porque="dividir entre cero no se puede")
            return r
        v, porque = multiplicar(c, b)
    if v is None:
        r.update(conclusion="no_entero" if "justo" in (porque or "") else "imposible", porque=porque)
        return r
    r["valor"] = v
    con_numero = " = ".join(_escribir_lado(l, str(v)) for l in e["lados"])
    r["comprobacion"] = con_numero
    r["comprobacion_ok"] = decidir_igualdad(con_numero, saber).get("valor") == "verdadero"
    r["conclusion"] = "hecho" if r["comprobacion_ok"] else "no_cuadra"
    return r


def _explicar_por(r):
    L = ["PREGUNTA (E.4): que numero va en el hueco?   %s" % r["ecuacion"], ""]
    if r["conclusion"] in ("sin_hueco", "dos_huecos", "todavia_no"):
        return "\n".join(L + ["  %s" % r["porque"], "", "RESULTADO: %s" % r["conclusion"]])
    L.append("  1. LEER: el hueco esta en %s." % r["tipo"])
    if r.get("izquierda"):
        L.append("     (el resultado esta a la IZQUIERDA del =: da igual, E.0)")
    L.append("")
    if r["conclusion"] != "hecho":
        L += ["  2. %s" % r.get("porque"), "", "RESULTADO: %s" % r["conclusion"]]
        return "\n".join(L)
    p = r["paso"]
    L.append("  2. %s con %s:" % (r["como"].upper(), p["pieza"]["nombre"]))
    L.append("        %s" % p["resultado"]["cuenta"].replace("; ", "\n        "))
    L.append("")
    L.append("  3. COMPRUEBO (E.0): pongo el %d en el hueco -> %s ... %s"
             % (r["valor"], r["comprobacion"], "VERDADERO" if r["comprobacion_ok"] else "FALSO"))
    L.append("")
    L.append("RESULTADO: %d" % r["valor"])
    return "\n".join(L)
