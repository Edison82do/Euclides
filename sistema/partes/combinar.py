# -*- coding: utf-8 -*-
"""
Euclides - COMBINAR LA MULTIPLICACION CON LA SUMA Y LA RESTA (paso M.16 del plan pedagogico, 7 oct 2026; 5.o).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

NCETM 2.22 (Combining multiplication with addition and subtraction); Common Core 5.OA.A.1-2.
  punto 1: sin parentesis, la multiplicacion se hace ANTES que la suma o la resta; con parentesis, primero
           lo de dentro.  (La suma y la resta, de izquierda a derecha, en el orden en que vienen.)
  punto 2: al sumar o restar productos con un FACTOR COMUN se puede usar la distributiva (4 x 6 + 4 x 2 = 4 x 8).
Las cuentas las hacen las piezas de la pregunta 'combinar' (combinar_en_el_orden_de_siempre y
combinar_sacando_el_factor_comun).  Aqui solo se LEE la expresion, se pregunta a las piezas y se explica.
La division combinada es 2.28 (6.o): todavia no.
"""

import re

_CO_NUM = r"\d+(?:\.\d+)?"
_CO_TOKEN = re.compile(_CO_NUM + r"|[x()+\-:]")


def _co_limpio(texto):
    t = texto.lower().replace("−", "-").replace("×", "x").replace("*", "x").replace("÷", ":")
    t = t.replace("[", "(").replace("]", ")").replace("·", "x")
    t = re.sub(r"(\d),(\d)", r"\1.\2", t)
    return " ".join(t.strip().rstrip("?").split())


def _co_tokens(t):
    """'3 + 4 x 5' -> ['3', '+', '4', 'x', '5'], o None si hay algo que no es de una cuenta."""
    toks = _CO_TOKEN.findall(t)
    if not toks or "".join(toks) != t.replace(" ", ""):
        return None
    if re.search(r"\d\s+\d", t):                    # dos numeros seguidos: no se que es
        return None
    return toks


def _co_arbol(toks):
    """Los terminos con su signo; cada termino, sus factores; un factor es un numero (texto) o un parentesis
    {"terminos": ...}.  Leer, no calcular.  ValueError si esta mal escrito."""
    quedan = list(toks)

    def ver():
        return quedan[0] if quedan else None

    def factor():
        t = quedan.pop(0) if quedan else None
        if t is None:
            raise ValueError("falta un numero al final")
        if t == "(":
            e = expresion()
            if ver() != ")":
                raise ValueError("falta cerrar un parentesis")
            quedan.pop(0)
            return {"terminos": e}
        if re.match(_CO_NUM + "$", t):
            return _dp_normal(t)
        raise ValueError("no entiendo '%s' donde va un numero" % t)

    def termino():
        fs = [factor()]
        while ver() in ("x", ":"):
            if quedan.pop(0) == ":":
                raise _CoDividir()
            fs.append(factor())
        return fs

    def expresion():
        ts = [["+", termino()]]
        while ver() in ("+", "-"):
            ts.append([quedan.pop(0), termino()])
        return ts

    e = expresion()
    if quedan:
        raise ValueError("sobra '%s'" % quedan[0])
    return e


class _CoDividir(Exception):
    pass


def _co_leer(texto):
    """(arbol, None) o (None, (conclusion, porque))."""
    toks = _co_tokens(texto)
    if toks is None:
        return None, ("no_entiendo", "no es una cuenta de numeros con x, + y - (y parentesis)")
    try:
        return _co_arbol(toks), None
    except _CoDividir:
        return None, ("todavia_no", "dividir dentro de una cuenta combinada es NCETM 2.28 (6.o): por ahora, "
                                    "solo la x con la + y la -")
    except ValueError as e:
        return None, ("no_entiendo", str(e))


def _co_cuantas_ops(toks):
    return len([t for t in toks if t in ("x", "+", "-", ":")])


def _co_x_es_letra(texto):
    """'x + 5': la x va donde un numero; es una LETRA (E.5), no 'por'."""
    error = _co_leer(texto)[1]
    return bool(error) and "'x' donde va un numero" in error[1]


def _co_es_combinada(texto):
    """Para ENRUTAR: dos operaciones o mas, o un parentesis con su cuenta.  '2 x 3 x 4' es M.14 (solo x)."""
    toks = _co_tokens(texto)
    if toks is None or _co_x_es_letra(texto):
        return False
    ops = [t for t in toks if t in ("x", "+", "-", ":")]
    if len(ops) < 2:
        return False
    return "(" in toks or any(o != ops[0] for o in ops) or ops[0] in ("+", "-")


def _co_partir_igualdad(t):
    if t.count("=") != 1:
        return None
    a, b = t.split("=")
    return a.strip(), b.strip()


def es_orden_combinar(texto):
    t = _co_limpio(texto)
    if t.startswith("combinar"):
        return True
    m = re.match(r"^(calcular|verdad)\s*:?\s*(.*)$", t)
    orden, resto = (m.group(1), m.group(2)) if m else ("", t)
    lados = _co_partir_igualdad(resto)
    if lados:
        if orden == "calcular":
            return False
        return all(_co_tokens(x) and not _co_x_es_letra(x) for x in lados) and any(_co_es_combinada(x) for x in lados)
    return orden != "verdad" and _co_es_combinada(resto)


# ---------------------------------------------------------------- calcular

def _co_productos(terminos):
    for _, fs in terminos:
        yield fs
        for f in fs:
            if isinstance(f, dict):
                for x in _co_productos(f["terminos"]):
                    yield x


def _co_numeros(terminos):
    for fs in _co_productos(terminos):
        for f in fs:
            if not isinstance(f, dict):
                yield f


def _co_problema(arbol, saber):
    """Lo que no toca este ano, o no cabe, antes de preguntar a las piezas."""
    for f in _co_numeros(arbol):
        e, _, d = f.partition(".")
        if len(d) > 3:
            return "todavia_no", "%s tiene mas de tres cifras detras del punto: llego a las milesimas (D.2)" % f
        if decir(int(e), saber) is None:
            return "no_alcanza", "%s se pasa de mi lista (llego a %s)" % (f, techo(saber))
    for fs in _co_productos(arbol):
        if len([f for f in fs if not isinstance(f, dict) and "." in f]) > 1:
            return "todavia_no", "%s es un decimal por otro decimal: eso es de 6.o" % " x ".join(
                f for f in fs if not isinstance(f, dict))
    return None


def _co_conclusion_de(porque):
    if "se pasa del techo" in porque:
        return "no_alcanza"
    return "todavia_no"


def _co_texto(terminos, marcar=False):
    """El arbol escrito; con marcar, las multiplicaciones (las que van primero) entre comillas latinas."""
    trozos = []
    for i, (signo, fs) in enumerate(terminos):
        partes = ["(%s)" % _co_texto(f["terminos"], marcar) if isinstance(f, dict) else f for f in fs]
        t = " x ".join(partes)
        if marcar and len(fs) > 1 and len(terminos) > 1:
            t = "«%s»" % t
        trozos.append(t if i == 0 else "%s %s" % (signo, t))
    return " ".join(trozos)


def decidir_combinar(texto, saber=None):
    """texto: la cuenta sola ('3 + 4 x 5').  Pregunta a las piezas de 'combinar'."""
    if saber is None:
        saber = cargar_conocimiento()
    arbol, error = _co_leer(_co_limpio(texto))
    if error:
        return {"conclusion": error[0], "porque": error[1]}
    r = {"arbol": arbol, "texto": _co_texto(arbol)}
    p = _co_problema(arbol, saber)
    if p:
        r.update({"conclusion": p[0], "porque": p[1]})
        return r
    if len(arbol) == 1 and len(arbol[0][1]) == 1:
        f = arbol[0][1][0]
        if not isinstance(f, dict):
            r.update({"conclusion": "hecho", "valor": f, "pieza": "", "pasos": [], "vuelta": "", "solo": True})
            return r
        return decidir_combinar(_co_texto(f["terminos"]), saber)
    a = aplicar("combinar", {"terminos": arbol}, saber)
    if a["conclusion"] != "hecho":
        porque = a.get("porque") or a["conclusion"]
        r.update({"conclusion": _co_conclusion_de(porque), "porque": porque})
        return r
    res = a["resultado"]
    r.update({"conclusion": "hecho", "valor": a["valor"], "pieza": a["pieza"]["id"], "metodo": res["metodo"],
              "pasos": res["pasos"], "vuelta": res["vuelta"], "resultado": res,
              "tambien": a.get("tambien_servian", [])})
    return r


def _co_valor_de(arbol, saber, pieza="combinar"):
    """El valor de otro arbol (para ensenar el error tipico, o el otro camino).  None si no sale."""
    try:
        a = aplicar(pieza, {"terminos": arbol}, saber)
    except Exception:
        return None
    return a["valor"] if a["conclusion"] == "hecho" else None


def _co_de_izquierda_a_derecha(arbol):
    """El ERROR TIPICO: ir de izquierda a derecha sin mirar (3 + 4 x 5 como (3 + 4) x 5).  None si no aplica:
    hay parentesis, o ninguna x va detras de una + o una -."""
    if any(isinstance(f, dict) for fs in _co_productos(arbol) for f in fs):
        return None
    if not any(len(fs) > 1 for _, fs in arbol[1:]):
        return None
    acc = {"terminos": [["+", [arbol[0][1][0]]]]}
    for f in arbol[0][1][1:]:
        acc = {"terminos": [["+", [acc, f]]]}
    for signo, fs in arbol[1:]:
        acc = {"terminos": [["+", [acc]], [signo, [fs[0]]]]}
        for f in fs[1:]:
            acc = {"terminos": [["+", [acc, f]]]}
    return acc["terminos"]


def _co_suma_antes(arbol):
    """El otro ERROR TIPICO: creer que la suma va antes que la resta (10 - 3 + 2 como 10 - (3 + 2))."""
    for i in range(1, len(arbol)):
        if arbol[i][0] == "-" and i + 1 < len(arbol) and arbol[i + 1][0] == "+":
            junto = {"terminos": [["+", arbol[i][1]], ["+", arbol[i + 1][1]]]}
            nuevo = list(arbol[:i])
            nuevo.append(["-", [junto]])
            nuevo.extend(arbol[i + 2:])
            return nuevo
    return None


def _co_lineas(r, saber):
    """Las lineas que explican una cuenta combinada ya hecha."""
    L = []
    arbol = r["arbol"]
    if r["pieza"] == "combinar_sacando_el_factor_comun":
        L.append("  FACTOR COMUN (NCETM 2.22, punto 2: la distributiva): una multiplicacion en vez de dos")
        for i, paso in enumerate(r["pasos"]):
            L.append("  %d. %s" % (i + 1, paso))
        otro = _co_valor_de(arbol, saber, "combinar_en_el_orden_de_siempre")
        if otro is not None:
            L.append("     en el orden de siempre (%s): sale %s ... %s" % (
                _co_texto(arbol, marcar=True), otro, "LO MISMO" if otro == r["valor"] else "NO COINCIDE, algo esta mal"))
        a = r["resultado"]["comun"]
        b, signo, c, _ = r["resultado"]["dentro"]
        if signo == "+" and all(len(fs) == 2 for _, fs in arbol):
            mal = _co_valor_de([["+", [{"terminos": [["+", [a]], ["+", [a]]]}, {"terminos": [["+", [b]], ["+", [c]]]}]]],
                               saber)
            if mal is not None:
                L.append("     OJO: NO es (%s + %s) x (%s + %s) = %s: el %s es el MISMO grupo; se juntan los otros"
                         % (a, a, b, c, mal, a))
    else:
        L.append("  EL ORDEN DE SIEMPRE (NCETM 2.22, punto 1): primero lo de DENTRO del parentesis; luego las x; "
                 "luego + y -, de izquierda a derecha")
        if any(len(fs) > 1 for _, fs in arbol) and len(arbol) > 1:
            L.append("     rodeo las multiplicaciones: %s" % _co_texto(arbol, marcar=True))
        for i, paso in enumerate(r["pasos"]):
            L.append("  %d. %s" % (i + 1, paso))
        mal = _co_de_izquierda_a_derecha(arbol)
        v = _co_valor_de(mal, saber) if mal else None
        if v is not None and v != r["valor"]:
            L.append("     OJO: de izquierda a derecha sin mirar saldria %s: esta MAL (la x va antes que la + y la -)" % v)
        mal = _co_suma_antes(arbol)
        v = _co_valor_de(mal, saber) if mal else None
        if v is not None and v != r["valor"]:
            L.append("     OJO: la suma NO va antes que la resta: %s = %s esta MAL (van en el orden en que vienen)"
                     % (_co_texto(mal), v))
    if r["vuelta"]:
        L.append("  COMPRUEBO con la operacion contraria, de la ultima cuenta a la primera: %s ... SI" % r["vuelta"])
    L.append("     (%s)" % r["metodo"])
    return L


def explicar_combinar(texto, saber):
    r = decidir_combinar(texto, saber)
    titulo = r.get("texto") or _co_limpio(texto)
    L = ["PREGUNTA (M.16): %s  (NCETM 2.22: combinar la x con la + y la -)" % titulo, ""]
    if r["conclusion"] == "no_entiendo":
        return "NO ENTIENDO ESTO: %s\n   se escribe asi:  3 + 4 x 5    (3 + 4) x 5    combinar: 4 x 6 + 4 x 2" \
               % r["porque"]
    if r["conclusion"] != "hecho":
        etiqueta = {"no_se_puede": "NO SE PUEDE", "no_alcanza": "NO ALCANZA"}.get(r["conclusion"], "TODAVIA NO")
        return "\n".join(L + ["  %s: %s" % (etiqueta, r["porque"]), "", "RESULTADO: %s" % r["conclusion"]])
    if r.get("solo"):
        return "\n".join(L + ["  es un numero solo: no hay cuenta que hacer", "", "RESULTADO: %s" % r["valor"]])
    L += _co_lineas(r, saber)
    return "\n".join(L + ["", "RESULTADO: %s" % r["valor"]])


# ---------------------------------------------------------------- verdad: con cuentas combinadas

def explicar_verdad_combinada(izq, der, saber):
    L = ["PREGUNTA (M.16): %s = %s  es verdad?  (el = dice que los dos lados son EL MISMO numero)" % (izq, der), ""]
    valores = []
    for nombre, lado in (("izquierda", izq), ("derecha", der)):
        r = decidir_combinar(lado, saber)
        if r["conclusion"] == "no_entiendo":
            return "NO ENTIENDO ESTO: %s\n   se escribe asi:  verdad: 3 + 4 x 5 = 23" % r["porque"]
        if r["conclusion"] != "hecho":
            etiqueta = {"no_se_puede": "NO SE PUEDE", "no_alcanza": "NO ALCANZA"}.get(r["conclusion"], "TODAVIA NO")
            return "\n".join(L + ["  el lado de la %s: %s: %s" % (nombre, etiqueta, r["porque"]), "",
                                  "RESULTADO: %s" % r["conclusion"]])
        if r.get("solo"):
            L.append("  a la %s: %s (un numero solo)" % (nombre, r["valor"]))
        else:
            L.append("  a la %s: %s" % (nombre, r["texto"]))
            L += ["  " + x for x in _co_lineas(r, saber)]
            L.append("    -> vale %s" % r["valor"])
        valores.append(r["valor"])
    si = valores[0] == valores[1]
    L.append("  %s %s %s" % (valores[0], "es el mismo numero que" if si else "NO es el mismo numero que", valores[1]))
    return "\n".join(L + ["", "RESULTADO: %s" % ("VERDADERO" if si else "FALSO")])


def explicar_orden_combinar(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    t = _co_limpio(texto)
    m = re.match(r"^(combinar|calcular|verdad)\s*:?\s*(.*)$", t)
    resto = m.group(2) if m else t
    lados = _co_partir_igualdad(resto)
    if lados:
        return explicar_verdad_combinada(lados[0], lados[1], saber)
    return explicar_combinar(resto, saber)
