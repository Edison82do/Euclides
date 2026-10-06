# -*- coding: utf-8 -*-
"""
Euclides - PROBLEMAS DE x Y : CON POCAS PALABRAS (paso R.2 del plan pedagogico, 5 oct 2026).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

Common Core 3.OA.A.3 (grupos iguales, filas y columnas, medidas).  CGI: multiplicar, dividir
agrupando, dividir repartiendo.  INSTRUCCION POR ESQUEMAS (Jitendra; Xin): el esquema de GRUPOS
IGUALES tiene tres casillas -- cuantos GRUPOS, cuantos EN CADA uno, el TOTAL --; el problema da dos y
pregunta por una.  Las casillas se llenan por los NOMBRES (bolsa = el grupo; caramelo = la cosa), no
por palabras clave.  La operacion la deciden las piezas de 'paso_por' (conocimiento/piezas/).
Singapur: el modelo de BARRAS.
"""

import re

# LAS FORMAS (lenguaje rustico, 6.).  Cada una dice que casillas del esquema llena.
_R2_HECHOS = [
    ("grupos_con", re.compile(r"^(?:(?:\w+ )?(?:hay|tiene|tienen|compra|compro|trae|son|lleva) )?(?P<g>\d+) (?P<grupo>\w+) "
                              r"(?:con|de) (?P<m>\d+) (?P<cosa>\w+)(?: cada (?:una|uno|1))?$")),
    ("en_n_grupos", re.compile(r"^(?:hay |tiene |tienen |se reparten |estan )?(?P<t>\d+) (?P<cosa>\w+) "
                               r"(?:repartid\w+ )?en (?P<g>\d+) (?P<grupo>\w+)(?: iguales)?$")),
    ("filas", re.compile(r"^(?:.* )?(?:hay )?(?P<g>\d+) (?P<grupo>filas|columnas) de (?P<m>\d+) (?P<cosa>\w+)$")),
    ("cada", re.compile(r"^(?:y )?(?:en )?cada (?P<grupo>\w+) (?:tiene|lleva|trae|pesa|cuesta|mide|vale|hay|caben|le dan|recibe) "
                        r"(?P<m>\d+)(?: (?P<cosa>\w+))?$")),
    ("reparte", re.compile(r"^(?:\w+ )?repart\w* (?P<t>\d+) (?P<cosa>\w+) entre (?P<g>\d+) (?P<grupo>\w+)$")),
    ("en_grupos_de", re.compile(r"^(?:\w+ )?(?:mete|metio|pone|puso|guarda|guardo|coloca|coloco|empaqueta|reparte|pon|mete)\w* "
                                r"(?P<t>\d+) (?P<cosa>\w+) en (?P<grupo>\w+) de (?P<m>\d+)$")),
    # E.5: un SEGUNDO paso (lo que cambia despues): se dicen ANTES que 'hay_n'
    ("cambio_mas", re.compile(r"^(?:y )?(?:luego )?(?:\w+ )?(?:le dan|les dan|compra|compran|gana|ganan|encuentra|"
                              r"recibe|reciben|le regalan|les regalan|llegan|traen) (?P<n>\d+)(?: \w+)?(?: mas)?$")),
    ("cambio_menos", re.compile(r"^(?:y )?(?:luego )?(?:\w+ )?(?:se come|se comen|regala|regalan|pierde|pierden|da|dan|"
                                r"gasta|gastan|vende|venden|se van|se rompen|se lleva|se llevan|usa|usan) "
                                r"(?P<n>\d+)(?: \w+)?$")),
    ("hay_n", re.compile(r"^(?:\w+ )?(?:hay|tiene|tienen|compra|compro|trae|son|junta|junto) (?P<n>\d+) (?P<x>\w+)$")),
]
_R2_PREGUNTAS = [
    ("final", re.compile(r"^cuant\w* (?:\w+ )?(?:le |les )?(?:quedan|queda|tiene ahora|tienen ahora|hay ahora)$")),
    ("cuanto_pesan", re.compile(r"^cuanto (?:pesan|cuestan|miden|valen) (?P<g>\d+) (?P<grupo>\w+)$")),
    ("a_cada", re.compile(r"^cuant\w* (?:\w+ )?(?:le )?(?:toca\w*|da\w*|recibe\w*) (?:a )?cada")),
    ("en_cada", re.compile(r"^cuant\w* (?P<x>\w+) (?:hay|tiene|lleva|van|caben) (?:en )?cada (?P<grupo>\w+)$")),
    ("en_total", re.compile(r"^cuant\w* (?:(?P<x>\w+) )?hay en total$")),
    ("cuantos_x", re.compile(r"^cuant\w* (?P<x>\w+) (?:hay|son|tiene|tienen|salen|hacen|hace|necesita\w*|llena\w*|habra\w*|se llenan|le dio|tenia)(?: .*)?$")),
]
# las formas que solo puede tener un problema de grupos iguales (para elegir R.2 en vez de R.1)
_R2_PROPIAS = {"grupos_con", "en_n_grupos", "filas", "cada", "reparte", "en_grupos_de", "cuanto_pesan", "a_cada", "en_cada"}


def _raiz(w):
    w = (w or "").lower()
    for fin in ("es", "s"):
        if w.endswith(fin) and len(w) > len(fin) + 2:
            return w[:-len(fin)]
    return w


def _mismo(a, b):
    return bool(a and b) and (_raiz(a) == _raiz(b) or a == b)


def _frases_r2(texto, saber):
    lecturas = []
    t = _normalizar(texto)
    out = []
    for trozo in [x.strip() for x in re.split(r"[.?!;:]", t) if x.strip()]:
        trozo = re.sub(r"\s+", " ", _leer_numeros(trozo, saber, lecturas)).replace(",", "").strip()
        if trozo.startswith("y "):
            trozo = trozo[2:]
        out.append(trozo)
    return out


def _encajar_r2(frase):
    for nombre, rx in _R2_PREGUNTAS:
        m = rx.match(frase)
        if m and frase.startswith("cuant"):
            return "pregunta", nombre, m.groupdict()
    for nombre, rx in _R2_HECHOS:
        m = rx.match(frase)
        if m:
            return "hecho", nombre, m.groupdict()
    return None, None, None


def es_problema_por(texto, saber=None):
    """Tiene alguna forma que solo puede ser de grupos iguales?"""
    if saber is None:
        saber = cargar_conocimiento()
    return any(_encajar_r2(f)[1] in _R2_PROPIAS for f in _frases_r2(texto, saber))


def leer_problema_por(texto, saber=None):
    """Llena el ESQUEMA de grupos iguales: {"grupos", "en_cada", "total", "busca", "grupo", "cosa"}."""
    if saber is None:
        saber = cargar_conocimiento()
    e = {"grupos": None, "en_cada": None, "total": None, "busca": None, "grupo": None, "cosa": None,
         "medida": False}
    leidas, pendientes, pregunta, cambios = [], [], None, []
    for f in _frases_r2(texto, saber):
        tipo, nombre, g = _encajar_r2(f)
        if tipo is None:
            return {"error": "no entiendo esta frase: '%s'" % f, "leidas": leidas}
        leidas.append({"frase": f, "forma": nombre})
        if tipo == "pregunta":
            pregunta = (nombre, g)
            continue
        if nombre == "hay_n":
            pendientes.append(g)
            continue
        if nombre in ("cambio_mas", "cambio_menos"):
            cambios.append(("+" if nombre == "cambio_mas" else "-", int(g["n"]), f))
            continue
        if g.get("grupo"):
            e["grupo"] = e["grupo"] or g["grupo"]
        if g.get("cosa"):
            e["cosa"] = e["cosa"] or g["cosa"]
        if nombre in ("grupos_con", "filas"):
            e["grupos"], e["en_cada"] = int(g["g"]), int(g["m"])
        elif nombre == "cada":
            e["en_cada"] = int(g["m"])
            if re.search(r" (pesa|cuesta|mide|vale) ", " %s " % f):
                e["medida"] = True
        elif nombre in ("reparte", "en_n_grupos"):
            e["total"], e["grupos"] = int(g["t"]), int(g["g"])
        elif nombre == "en_grupos_de":
            e["total"], e["en_cada"] = int(g["t"]), int(g["m"])
    # 'hay 12 caramelos' / 'hay 4 cajas': la casilla la decide el NOMBRE
    for g in pendientes:
        if _mismo(g["x"], e["grupo"]):
            e["grupos"] = int(g["n"])
        elif _mismo(g["x"], e["cosa"]) or e["cosa"] is None:
            e["total"] = int(g["n"])
            e["cosa"] = e["cosa"] or g["x"]
        else:
            return {"error": "no se si '%s' son los grupos o las cosas" % g["x"], "leidas": leidas}
    if pregunta is None:
        return {"error": "no hay pregunta", "leidas": leidas}
    nombre, g = pregunta
    e["cambios"] = cambios
    if cambios:
        # DOS PASOS (3.OA.D.8): primero el total de los grupos iguales, luego lo que cambia
        if nombre not in ("final", "en_total", "cuantos_x"):
            return {"error": "con un segundo paso solo se preguntar por lo que hay al final", "leidas": leidas}
        e["busca"] = "total"
        e["leidas"] = leidas
        return e
    if nombre == "final":
        return {"error": "pregunta por lo que queda, pero no dice que cambie nada", "leidas": leidas}
    if nombre == "cuanto_pesan":
        e["busca"], e["grupos"] = "total", int(g["g"])
    elif nombre in ("a_cada", "en_cada"):
        e["busca"] = "en_cada"
    elif nombre == "en_total":
        e["busca"] = "total"
    else:
        x = g.get("x")
        e["palabra_pregunta"] = x
        if _mismo(x, e["grupo"]):
            e["busca"] = "grupos"
        elif _mismo(x, e["cosa"]):
            e["busca"] = "total"
        else:
            return {"error": "no se si la pregunta ('%s') es por los grupos o por las cosas" % x, "leidas": leidas}
    e["leidas"] = leidas
    return e


def decidir_R2_problema(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    e = leer_problema_por(texto, saber)
    if "error" in e:
        return {"conclusion": "no_entiendo", "porque": e["error"], "leidas": e.get("leidas", [])}
    sit = {k: e[k] for k in ("busca", "grupos", "en_cada", "total")}
    p = aplicar("paso_por", sit, saber)
    r = {"esquema": e, "paso": p}
    if p["conclusion"] != "hecho":
        r.update(conclusion="no_se" if p["conclusion"] != "imposible" else "imposible", porque=p.get("porque"))
        return r
    calc = p["resultado"]
    v = p["valor"]
    resto = calc["resultado"].get("resto", 0) if isinstance(calc.get("resultado"), dict) else 0
    lleno = dict(sit)
    lleno[e["busca"]] = v
    r.update(conclusion="hecho", valor=v, resto=resto, lleno=lleno)
    if not resto:
        t = "%d x %d = %d" % (lleno["grupos"], lleno["en_cada"], lleno["total"])
        r["comprobacion"] = t
        r["comprobacion_ok"] = decidir_igualdad(t, saber).get("valor") == "verdadero"
    else:
        r["comprobacion"] = "%d x %d + %d = %d" % (lleno["grupos"], lleno["en_cada"], resto, lleno["total"])
        r["comprobacion_ok"] = True
    unidad = (e.get("palabra_pregunta") or e["grupo"]) if e["busca"] == "grupos" else (e["cosa"] or "")
    r["unidad"] = unidad
    if e.get("cambios"):
        _segundo_paso(e, r, saber)
    return r


def _segundo_paso(e, r, saber):
    """E.5 (3.OA.D.8): el total de los grupos iguales es el ANTES del segundo paso (R.1).  Y se escribe
    la ECUACION CON LETRA, que se resuelve tambien por su lado (letra.py) y tiene que dar lo mismo."""
    v = r["valor"]
    r["pasos2"] = []
    expr = "%d x %d" % (r["lleno"]["grupos"], r["lleno"]["en_cada"])
    for signo, n, frase in e["cambios"]:
        p = aplicar("paso", {"tipo": "cambio", "antes": v, "signo": signo, "n": n}, saber)
        if p["conclusion"] != "hecho":
            r.update(conclusion="imposible", porque=p.get("porque"))
            return
        r["pasos2"].append({"frase": frase, "pieza": p["pieza"]["nombre"], "antes": v, "signo": signo, "n": n,
                            "valor": p["valor"], "metodo": p["resultado"]["resultado"]["metodo"]})
        v = p["valor"]
        expr = "%s %s %d" % (expr, signo, n)
    letra = (e["cosa"] or "n")[0]
    if letra == "x":
        letra = "n"
    r["ecuacion"] = "%s = %s" % (expr, letra)
    el = decidir_ecuacion_letra(r["ecuacion"], saber)
    r["ecuacion_ok"] = el.get("valor") == v
    r["valor_paso1"], r["valor"], r["resto"] = r["valor"], v, 0


def _barra(lleno, busca, saber):
    """El MODELO DE BARRAS (Singapur): el total partido en grupos iguales; '?' en lo que falta."""
    g, m, t = lleno["grupos"], lleno["en_cada"], lleno["total"]
    trozo = "?" if busca == "en_cada" else str(m)
    total = "?" if busca == "total" else str(t)
    if busca == "grupos" or levantar_dedos(decir(g, saber), saber) is None:
        cuerpo = " | ".join([trozo, trozo, "..."]) if busca == "grupos" else " | ".join([trozo, trozo, "...", trozo])
        abajo = "(? trozos)" if busca == "grupos" else "(%d trozos)" % g
    else:
        cuerpo = " | ".join(trozo for _ in levantar_dedos(decir(g, saber), saber))
        abajo = "(%d trozos)" % g
    linea = "[ %s ]" % cuerpo
    return ["        %s" % linea, "        %s" % ("'" + "-" * (len(linea) - 2) + "'"),
            "        total: %s   %s" % (total, abajo)]


def explicar_R2_problema(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_R2_problema(texto, saber)
    L = ["PREGUNTA (R.2): un problema de GRUPOS IGUALES  (el esquema: grupos, en cada uno, total)",
         "ENUNCIADO: %s" % texto.strip(), ""]
    if r["conclusion"] == "no_entiendo":
        L += ["  NO ENTIENDO: %s" % r["porque"], "", "RESULTADO: no_entiendo"]
        return "\n".join(L)
    e = r["esquema"]
    L.append("  1. LEER (cada frase con su forma):")
    for x in e["leidas"]:
        L.append("     %-48s -> %s" % ("'%s'" % x["frase"], x["forma"]))
    L.append("")
    nombre = {"grupos": "cuantos GRUPOS (%s)" % e["grupo"], "en_cada": "cuantos EN CADA GRUPO",
              "total": "el TOTAL (%s)" % (e["cosa"] or "")}
    L.append("  2. EL ESQUEMA (se llena por los nombres, no por palabras clave):")
    for k in ("grupos", "en_cada", "total"):
        L.append("     %-34s %s" % (nombre[k] + ":", "?  <- LO QUE SE BUSCA" if e["busca"] == k else
                                     (e[k] if e[k] is not None else "(no se sabe)")))
    if e["medida"]:
        L.append("     (es una MEDIDA: cada %s pesa, cuesta o mide lo mismo, en %s; 3.OA.A.3)" % (e["grupo"], e["cosa"] or "?"))
    L.append("")
    L.append("  3. PRUEBO TODO LO QUE SE:")
    p = r["paso"]
    for f in p["candidatos"]:
        if f.get("aplica"):
            L.append("        [SI]  %s" % f["nombre"])
        else:
            L.append("        [no]  %-42s porque %s" % (f["nombre"], f.get("descartado") or f.get("no_salio")))
    L.append("")
    if r["conclusion"] != "hecho":
        L += ["  NO SE PUEDE: %s" % r.get("porque"), "", "RESULTADO: %s" % r["conclusion"]]
        return "\n".join(L)
    calc = p["resultado"]
    L.append("  4. APLICO: %s  ->  %s" % (p["pieza"]["nombre"], p["pieza"]["que_hace"]))
    cuenta = calc["resultado"]["cuenta"]
    L.append("     con %s: %s%s" % (calc["resultado"]["metodo"], cuenta.split("; ")[0],
                                   "; ..." if "; " in cuenta else ""))
    L.append("")
    L.append("  5. LA BARRA (Singapur), antes y despues:")
    sin = dict(r["lleno"])
    L.extend(_barra(sin, e["busca"], saber))
    L.extend(_barra(r["lleno"], None, saber))
    L.append("")
    L.append("  6. COMPRUEBO: %s ... %s" % (r["comprobacion"], "SI" if r["comprobacion_ok"] else "NO"))
    if r.get("pasos2"):
        L.append("")
        L.append("  7. EL SEGUNDO PASO (3.OA.D.8): lo que hay despues de los grupos iguales")
        for p in r["pasos2"]:
            L.append("     '%s' -> %s: %d %s %d = %d   (%s)" % (p["frase"], p["pieza"], p["antes"], p["signo"],
                                                              p["n"], p["valor"], p["metodo"]))
        L.append("")
        L.append("  8. LA ECUACION CON LETRA: %s   -> %s = %d (resuelta por su lado: %s)"
                 % (r["ecuacion"], r["ecuacion"].split("= ")[-1], r["valor"], "lo mismo" if r["ecuacion_ok"] else "NO CUADRA"))
    L.append("")
    sobra = (", y sobra%s %d" % ("" if r["resto"] == 1 else "n", r["resto"])) if r["resto"] else ""
    L.append("RESULTADO: %d %s%s" % (r["valor"], r["unidad"], sobra))
    return "\n".join(L)
