# -*- coding: utf-8 -*-
"""
Euclides - LAS ESTRUCTURAS COMUNES: PARTE-PARTE-TODO CON TRES PARTES O MAS (paso S.2 del plan pedagogico,
7 oct 2026; 5.o).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

NCETM 1.28 (Common structures and the part-part-whole relationship):
  punto 1: las relaciones son aditivas o multiplicativas; las dos se ven en parte-parte-todo (partes iguales).
  punto 2: el todo se halla juntando las partes; estrategias distintas, LA MISMA estructura.
  punto 3: sabiendo el todo y todas las partes menos una, la que falta se calcula; estrategias distintas.
  punto 4: contextos muy distintos tienen la misma estructura de parte que falta.
Las cuentas las hacen las piezas de 'todo_de_las_partes' y 'parte_del_todo'.  Aqui solo se LEE la orden
(con las palabras del contexto, de conocimiento/parte_parte_todo.kn), se dibuja la barra, se pregunta a las
piezas y se explica.
"""

import re

_PT_VALOR = re.compile(r"^\$?\s*(\d+(?:\.\d+)?|\?)(?:\s*[a-z]+)?$")
_PT_IGUALES = re.compile(r"^(\d+)\s+partes\s+iguales$")


def _pt_limpio(texto):
    t = texto.lower().replace("−", "-").replace("¿", "").replace(" ", " ")
    for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ñ", "n")):
        t = t.replace(a, b)
    return " ".join(t.strip().rstrip(".").split())


def _pt_contextos(saber):
    """Los contextos del .kn: {palabra del todo: {"partes": [...], "unidad": ..., "dice": ...}}."""
    k = saber.get("parte_parte_todo", {})
    r = {"todo": {"partes": ["partes"], "unidad": "", "dice": "", "nombre": ""}}
    for linea in k.get("contextos", []) or []:
        trozos = [x.strip() for x in str(linea).split("|")]
        if len(trozos) != 4:
            continue
        r[trozos[0]] = {"partes": [p.strip() for p in trozos[1].split(",")], "unidad": trozos[2],
                        "dice": trozos[3], "nombre": trozos[0]}
    return r


def _pt_leer(texto, saber):
    """'perimetro: 30; lados: 8, 7, 6, ?' -> {"contexto", "todo", "partes", "iguales"}, o None si no es
    una orden de parte-parte-todo, o {"error": ...} si lo es pero esta mal escrita."""
    t = _pt_limpio(texto)
    trozos = [x.strip() for x in t.split(";") if x.strip()]
    if len(trozos) < 2:
        return None
    contextos = _pt_contextos(saber)
    claves = []
    for tr in trozos:
        m = _PT_IGUALES.match(tr)
        if m:
            claves.append(("iguales", m.group(1)))
            continue
        clave, dos, valores = tr.partition(":")
        if not dos:
            return None
        claves.append((clave.strip(), valores.strip()))
    los_todos = [c for c, _ in claves if c in contextos]
    if len(los_todos) != 1:
        return None
    ctx = contextos[los_todos[0]]
    palabras_de_partes = set(ctx["partes"]) | {"partes"}
    r = {"contexto": ctx, "todo": None, "partes": [], "iguales": False}
    for clave, valores in claves:
        if clave == "iguales":
            if r["partes"]:
                return {"error": "'N partes iguales' va en lugar de las partes, no junto a ellas"}
            r["partes"] = [None for _ in range(escribir_cifras([int(c) for c in reversed(valores)]))]
            r["iguales"] = True
            continue
        if clave in contextos:
            m = _PT_VALOR.match(valores)
            if not m:
                return {"error": "el todo ('%s') tiene que ser un numero o un ?" % valores}
            r["todo"] = None if m.group(1) == "?" else m.group(1)
            continue
        if clave not in palabras_de_partes:
            return None
        vs = [v.strip() for v in valores.split(",")]
        if vs and vs[-1].endswith("iguales"):
            vs[-1] = vs[-1].rsplit("iguales", 1)[0].strip()
            r["iguales"] = True
        for v in vs:
            m = _PT_VALOR.match(v)
            if not m:
                return {"error": "'%s' no es una parte: cada parte es un numero o un ? (separadas por comas; "
                                 "los decimales con punto, 4.50)" % v}
            r["partes"].append(None if m.group(1) == "?" else m.group(1))
    if not r["partes"][1:]:
        return {"error": "hacen falta dos partes o mas"}
    return r


def es_orden_parte_todo(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    return _pt_leer(texto, saber) is not None


# ---------------------------------------------------------------- decidir

def _pt_problema(numeros, saber):
    for f in numeros:
        e, _, d = f.partition(".")
        if len(d) > 3:
            return "todavia_no", "%s tiene mas de tres cifras detras del punto: llego a las milesimas (D.2)" % f
        if decir(int(e), saber) is None:
            return "no_alcanza", "%s se pasa de mi lista (llego a %s)" % (f, techo(saber))
    return None


def _pt_conclusion_de(porque):
    if "PASAN DEL TODO" in porque:
        return "no_se_puede"
    if "se pasa del techo" in porque or "no tiene nombre" in porque:
        return "no_alcanza"
    return "todavia_no"


def decidir_parte_todo(texto, saber=None):
    """Lee la orden y pregunta a las piezas.  {"conclusion": hecho | no_se_puede | ..., "valor", "falta": todo|parte}"""
    if saber is None:
        saber = cargar_conocimiento()
    o = _pt_leer(texto, saber)
    if o is None:
        return {"conclusion": "no_entiendo", "porque": "no es una orden de parte-parte-todo"}
    if "error" in o:
        return {"conclusion": "no_entiendo", "porque": o["error"]}
    r = dict(o)
    faltan = [p for p in o["partes"] if p is None]
    numeros = [p for p in o["partes"] if p is not None]
    if o["todo"] is not None:
        numeros.append(o["todo"])
    p = _pt_problema(numeros, saber)
    if p:
        r.update({"conclusion": p[0], "porque": p[1]})
        return r
    if o["todo"] is None:
        if faltan:
            r.update({"conclusion": "no_se_puede", "falta": "todo",
                      "porque": "falta el todo Y falta una parte: con lo que se sabe no se puede saber ninguno"})
            return r
        r["falta"] = "todo"
        situacion = {"partes": list(o["partes"])}
        pregunta = "todo_de_las_partes"
    else:
        r["falta"] = "parte"
        if not faltan:
            return _pt_cuadra(r, saber)
        if faltan[1:] and not (o["iguales"] and not numeros[1:]):
            if o["iguales"]:
                r.update({"conclusion": "todavia_no",
                          "porque": "unas partes se saben y las que faltan son iguales: son dos pasos (quitar y "
                                    "repartir); por ahora, o todas iguales que faltan o una sola que falta"})
            else:
                r.update({"conclusion": "no_se_puede",
                          "porque": "faltan %s partes: con el todo no basta para saber cada una (pueden ser muchas "
                                    "parejas), salvo que sean IGUALES" % decir(len(faltan), saber)})
            return r
        situacion = {"todo": o["todo"], "partes": list(o["partes"]), "iguales": o["iguales"]}
        pregunta = "parte_del_todo"
    a = aplicar(pregunta, situacion, saber)
    r["situacion"], r["pregunta"] = situacion, pregunta
    if a["conclusion"] != "hecho":
        porques = [f.get("no_salio", "") for f in a.get("candidatos", [])] + [a.get("porque") or ""]
        porque = next((x for x in porques if "PASAN DEL TODO" in x), a.get("porque") or a["conclusion"])
        r.update({"conclusion": _pt_conclusion_de(porque), "porque": porque})
        return r
    res = a["resultado"]
    r.update({"conclusion": "hecho", "valor": a["valor"], "pieza": a["pieza"]["id"], "metodo": res["metodo"],
              "pasos": res["pasos"], "vuelta": res["vuelta"], "resultado": res,
              "tambien": a.get("tambien_servian", [])})
    return r


def _pt_cuadra(r, saber):
    """No falta nada: se mira si las partes juntan el todo."""
    a = aplicar("todo_de_las_partes", {"partes": list(r["partes"])}, saber)
    if a["conclusion"] != "hecho":
        r.update({"conclusion": _pt_conclusion_de(a.get("porque") or ""), "porque": a.get("porque")})
        return r
    si = a["valor"] == _pt_normal(r["todo"])
    r.update({"conclusion": "hecho", "valor": "cuadra" if si else "no_cuadra", "cuadra": si, "junto": a["valor"],
              "pasos": a["resultado"]["pasos"], "pieza": a["pieza"]["id"], "vuelta": a["resultado"]["vuelta"],
              "metodo": a["resultado"]["metodo"], "tambien": []})
    return r


def _pt_normal(f):
    if "." in f:
        f = f.rstrip("0").rstrip(".")
    e, punto, d = f.partition(".")
    e = e.lstrip("0") or "0"
    return "%s.%s" % (e, d) if punto else e


# ---------------------------------------------------------------- explicar

def _pt_con_unidad(v, unidad):
    if not unidad:
        return v
    if unidad == "pesos" and "." in v:
        e, _, d = v.partition(".")
        v = "%s.%s" % (e, d.ljust(2, "0"))          # el dinero se escribe con dos cifras de centavos
    return "%s %s" % (v, unidad)


def _pt_barra(r, valor=None):
    """La barra de NCETM: arriba el todo, abajo las partes, con un ? en lo que falta."""
    partes = ["?" if p is None else _pt_normal(p) for p in r["partes"]]
    fila = "| %s |" % " | ".join(x.center(7) for x in partes)
    todo = "?" if r["todo"] is None else _pt_normal(r["todo"])
    ancho = len(fila[2:-2])
    arriba = "| %s |" % todo.center(ancho)
    ctx = r["contexto"]
    nombre_todo = "el todo%s" % (" (%s)" % ctx["nombre"] if ctx["nombre"] else "")
    nombre_partes = "las partes%s" % (" (%s)" % ", ".join(ctx["partes"]) if ctx["nombre"] else "")
    return ["     %s   <- %s" % (arriba, nombre_todo), "     %s   <- %s" % (fila, nombre_partes)]


def _pt_valor_de(pieza, situacion, saber):
    try:
        a = aplicar(pieza, situacion, saber)
    except Exception:
        return None
    return a["valor"] if a["conclusion"] == "hecho" else None


def _pt_combinar(terminos, saber):
    return _pt_valor_de("combinar", {"terminos": terminos}, saber)


def _pt_lineas(r, saber):
    L = []
    ctx = r["contexto"]
    if ctx["nombre"]:
        L.append("  CONTEXTO: %s  ->  %s es el TODO; %s son las PARTES" % (
            ctx["dice"], ctx["nombre"], " y ".join(ctx["partes"])))
        L.append("     es la MISMA estructura parte-parte-todo de siempre (NCETM 1.28, punto 4): solo cambian las palabras")
    L.append("  LA BARRA (arriba el todo, abajo las partes; el ? es lo que falta):")
    L += _pt_barra(r)
    return L


def explicar_parte_todo(texto, saber):
    r = decidir_parte_todo(texto, saber)
    if r["conclusion"] == "no_entiendo":
        return ("NO ENTIENDO ESTO: %s\n   se escribe asi:  partes: 37, 25, 63; todo: ?      todo: 100; partes: 37, ?, 25\n"
                "                    perimetro: 30; lados: 8, 7, 6, ?   todo: 24; 4 partes iguales" % r["porque"])
    L = ["PREGUNTA (S.2): parte-parte-todo con %s partes  (NCETM 1.28: las estructuras comunes)"
         % decir(len(r["partes"]), saber), ""]
    L += _pt_lineas(r, saber)
    unidad = r["contexto"]["unidad"]
    if r["conclusion"] != "hecho":
        etiqueta = {"no_se_puede": "NO SE PUEDE", "no_alcanza": "NO ALCANZA"}.get(r["conclusion"], "TODAVIA NO")
        return "\n".join(L + ["  %s: %s" % (etiqueta, r["porque"]), "", "RESULTADO: %s" % r["conclusion"]])
    if "cuadra" in r:
        L.append("  no falta nada: miro si las partes juntan el todo")
        L += ["  %d. %s" % (i + 1, p) for i, p in enumerate(r["pasos"])]
        L.append("     las partes juntan %s; el todo es %s ... %s" % (
            r["junto"], _pt_normal(r["todo"]), "CUADRA" if r["cuadra"] else "NO CUADRA"))
        return "\n".join(L + ["", "RESULTADO: %s" % r["valor"]])
    if r["falta"] == "todo":
        L.append("  FALTA EL TODO -> junto las partes (NCETM 1.28, punto 2)")
    elif r["iguales"]:
        L.append("  FALTAN LAS PARTES, pero son IGUALES -> reparto el todo (NCETM 1.28, punto 1: tambien es multiplicativa)")
    else:
        L.append("  FALTA UNA PARTE -> quito del todo lo que se sabe (NCETM 1.28, punto 3)")
    L += ["  %d. %s" % (i + 1, p) for i, p in enumerate(r["pasos"])]
    L.append("     (%s)" % r["metodo"])
    for otra in r.get("tambien", []):
        v = _pt_valor_de(otra, r["situacion"], saber)
        if v is not None:
            L.append("     OTRA ESTRATEGIA (%s): sale %s ... %s" % (
                otra, v, "LO MISMO: la estructura no cambia" if v == r["valor"] else "NO COINCIDE, algo esta mal"))
    if r["falta"] == "parte" and not r["iguales"]:
        L += _pt_errores(r, saber)
    if r["vuelta"]:
        L.append("  COMPRUEBO con la operacion contraria: %s ... SI" % r["vuelta"])
    ver = "cada parte: " if r["iguales"] and r["falta"] == "parte" else ""
    return "\n".join(L + ["", "RESULTADO: %s%s" % (ver, _pt_con_unidad(r["valor"], unidad))])


def _pt_errores(r, saber):
    """Los errores tipicos, calculados para ensenarlos (y que se vea que NO son la respuesta)."""
    L = []
    todo = _pt_normal(r["todo"])
    se_saben = [_pt_normal(p) for p in r["partes"] if p is not None]
    mal = _pt_combinar([["+", [todo]]] + [["+", [p]] for p in se_saben], saber)
    if mal is not None:
        L.append("     OJO: NO es %s + %s = %s: el todo NO se suma con las partes (ya las lleva dentro)"
                 % (todo, " + ".join(se_saben), mal))
    if se_saben[1:]:
        mal = _pt_combinar([["+", [todo]], ["-", [se_saben[0]]]], saber)
        if mal is not None:
            L.append("     OJO: NO es %s - %s = %s: hay que quitar TODAS las partes que se saben" % (todo, se_saben[0], mal))
    return L


def explicar_orden_parte_todo(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    return explicar_parte_todo(texto, saber)
