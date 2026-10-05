# -*- coding: utf-8 -*-
"""
Euclides - EL RESOLVEDOR (unidad R.1): aplicar todo lo que se sabe, y descartar con razones.

Este archivo es UNA PARTE del motor.  No se importa suelto: lo carga sistema/motor.py, que junta
todas las partes en un solo espacio de nombres.  Ver sistema/partes/__init__.py.

Lo que dice como se lee:      conocimiento/enunciados.kn   (las FORMAS: patrones, no adivinacion)
Lo que dice que se aplica:    conocimiento/resolver_r1.kn  (los conocimientos y sus CONDICIONES)
Aqui solo esta el PROGRAMA que recorre esos datos (regla 6: las decisiones van en archivos de datos).

    problema: Ana tiene 8 manzanas. Tiene 3 mas que Luis. Cuantas tiene Luis?
      -> 5   (y es una RESTA aunque diga "mas": el que falta es el que tiene MENOS)
"""

import os  # noqa: F401
import re
import sys  # noqa: F401


class _NoEntiendo(Exception):
    pass


class _NoSe(Exception):
    pass


# ------------------------------------------------------------------ 1. LEER

_TILDES = str.maketrans("áéíóúüÁÉÍÓÚÜ", "aeiouuAEIOUU")


def _lista(texto):
    return [p.strip() for p in (texto or "").split(",") if p.strip()]


def _normalizar(texto):
    t = texto.translate(_TILDES).lower()
    t = t.replace("¿", " ").replace("¡", " ")
    return t


def _leer_numeros(frase, saber, lecturas):
    """Los numeros dichos con palabras se LEEN con la secuencia (6.1/6.7).  'un'/'una' valen 1."""
    mapa = saber.get("_nombre_a_valor") or {}
    uno = set(saber["enunciados"].get("uno") or [])
    # las frases FIJAS de los huecos ("entre los dos") no son numeros: se copian tal cual
    fijas = [f.split() for v in (saber["enunciados"].get("huecos") or {}).values()
             for f in _lista(v) if " " in f]
    tok = frase.split()
    out = []
    i = 0
    while i < len(tok):
        fija = next((f for f in fijas if tok[i:i + len(f)] == f), None)
        if fija:
            out.extend(fija)
            i += len(fija)
            continue
        hecho = False
        for j in range(min(len(tok), i + 6), i, -1):
            trozo = " ".join(tok[i:j])
            v = 0 if trozo == "cero" else mapa.get(trozo)
            if v is None and j == i + 1 and trozo in uno:
                v = 1
            if v is not None:
                out.append(str(v))
                if trozo != str(v):
                    lecturas.append("'%s' -> %d" % (trozo, v))
                i = j
                hecho = True
                break
        if not hecho:
            out.append(tok[i])
            i += 1
    return " ".join(out)


def _formas(saber):
    """Compila las FORMAS de enunciados.kn a patrones.  Se hace una vez por 'saber'."""
    cache = saber.get("_formas_r1")
    if cache:
        return cache
    e = saber["enunciados"]
    verbos = {k: _lista(v) for k, v in (e.get("verbos") or {}).items()}
    huecos = {k: _lista(v) for k, v in (e.get("huecos") or {}).items()}
    articulos = "|".join(e.get("articulos") or [])

    reservadas = sorted(set(e.get("no_son_nombres") or []) | set(sum(verbos.values(), [])),
                        key=len, reverse=True)
    no_es = r"(?!(?:%s)\b)" % "|".join(re.escape(w) for w in reservadas)

    def hueco(nombre):
        if nombre in ("quien", "otro"):
            return r"(?:(?:%s) )?%s(?P<%s>[a-zñ_]+)" % (articulos, no_es, nombre)
        if nombre == "n":
            return r"(?P<n>\d+)"
        if nombre == "cosa":
            return r"%s(?P<cosa>[a-zñ]+)" % no_es
        if nombre == "mas":
            return r"mas"
        if nombre == "lugar":
            return r"(?P<lugar>(?:en|sobre|dentro de) [a-zñ ]+)"
        if nombre in verbos:
            return r"(?P<verbo>%s)" % "|".join(re.escape(v) for v in verbos[nombre])
        if nombre in huecos:
            return r"(?:%s)" % "|".join(re.escape(v) for v in huecos[nombre])
        raise ValueError("hueco desconocido en enunciados.kn: {%s}" % nombre)

    def compilar(forma):
        trozos = forma.split()
        rx = ""
        for k, t in enumerate(trozos):
            m = re.fullmatch(r"\{([a-z_]+)(\?)?\}", t)
            pieza = hueco(m.group(1)) if m else re.escape(t)
            opcional = bool(m and m.group(2))
            if opcional:
                # el hueco opcional se lleva SU espacio (el de delante; o el de detras si va primero)
                rx += ("(?:%s )?" % pieza) if k == 0 else ("(?: %s)?" % pieza)
            else:
                rx += (" " if k > 0 and not rx.endswith(" )?") else "") + pieza
        return re.compile("^" + rx + "$")

    out = {"hechos": [], "preguntas": []}
    for f in e.get("formas_hechos") or []:
        out["hechos"].append(dict(f, _rx=compilar(f["forma"])))
    for f in e.get("formas_preguntas") or []:
        out["preguntas"].append(dict(f, _rx=compilar(f["forma"])))
    out["no_son_nombres"] = set(e.get("no_son_nombres") or []) | set(sum(verbos.values(), []))
    saber["_formas_r1"] = out
    return out


def _encajar(frase, formas, lista):
    """La primera FORMA en la que la frase encaja ENTERA (y con nombres que son nombres)."""
    for f in formas[lista]:
        m = f["_rx"].match(frase)
        if not m:
            continue
        g = {k: v for k, v in m.groupdict().items() if v is not None}
        if any(g.get(k) in formas["no_son_nombres"] or (g.get(k) or "").isdigit()
               for k in ("quien", "otro", "cosa")):
            continue
        return f, g
    return None, None


def leer_enunciado(texto, saber):
    """Paso 1: LEER.  Devuelve las frases con su forma, o lanza _NoEntiendo con la frase culpable."""
    formas = _formas(saber)
    lecturas = []
    t = _normalizar(texto)
    trozos = [x.strip() for x in re.split(r"[.?!;,:]", t) if x.strip()]
    leidas = []
    conectores = sorted(saber["enunciados"].get("conectores") or [], key=len, reverse=True)
    for trozo in trozos:
        trozo = re.sub(r"\s+", " ", _leer_numeros(trozo, saber, lecturas))
        for c in conectores:
            if trozo.startswith(c + " "):
                trozo = trozo[len(c) + 1:]
                break
        f, g = _encajar(trozo, formas, "preguntas")
        if f:
            leidas.append({"frase": trozo, "tipo": "pregunta", "forma": f, "datos": g})
            continue
        f, g = _encajar(trozo, formas, "hechos")
        if f:
            leidas.append({"frase": trozo, "tipo": "hecho", "forma": f, "datos": g})
            continue
        # se prueba a partir por " y " (Juan tiene 7 y Pedro tiene 4)
        partido = None
        pal = trozo.split(" ")
        for k, w in enumerate(pal):
            if w != "y" or k == 0:
                continue
            izq, der = " ".join(pal[:k]), " ".join(pal[k + 1:])
            fi, gi = _encajar(izq, formas, "hechos")
            fd, gd = _encajar(der, formas, "hechos")
            if fi and fd:
                partido = [({"frase": izq, "tipo": "hecho", "forma": fi, "datos": gi}),
                           ({"frase": der, "tipo": "hecho", "forma": fd, "datos": gd})]
                break
        if partido:
            leidas.extend(partido)
            continue
        raise _NoEntiendo(trozo)
    return leidas, lecturas


# ------------------------------------------------------------------ 2. MONTAR LA SITUACION

def _montar(leidas):
    quienes = {}
    orden = []
    relaciones = []
    totales = []
    pregunta = None
    ultimo = [None]

    def h(nombre):
        if nombre not in quienes:
            quienes[nombre] = {"inicio": None, "inicio_desconocido": False, "cambios": [],
                               "final": None, "cosa": None}
            orden.append(nombre)
        return quienes[nombre]

    lugares = set()

    def quien_es(g, frase, lo_hace_alguien=False):
        q = g.get("quien") or ultimo[0]
        if not q:
            raise _NoEntiendo(frase + "   (no se de quien habla: no se ha nombrado a nadie antes)")
        if lo_hace_alguien and not g.get("quien") and q in lugares:
            raise _NoEntiendo(frase + "   (no se QUIEN lo hace: '%s' es un lugar, y un lugar no lo hace)" % q)
        return q

    for L in leidas:
        g, frase = L["datos"], L["frase"]
        if L["tipo"] == "pregunta":
            if pregunta is not None:
                raise _NoEntiendo(frase + "   (hay DOS preguntas; en R.1 se resuelve una)")
            pregunta = {"pide": L["forma"]["pide"], "quien": g.get("quien"), "otro": g.get("otro"),
                        "cosa": g.get("cosa"), "frase": frase}
            continue
        hecho = L["forma"]["hecho"]
        n = int(g["n"]) if g.get("n") else None
        if hecho == "estado_lugar":
            q = (g.get("lugar") or "alli").strip()
            lugares.add(q)
        elif hecho == "total":
            q = None
        else:
            # gana/pierde con un VERBO DE PERSONA (compra, saca, regala...) necesita a alguien;
            # llegan / se van (verbos de lo que entra y sale) valen tambien para un lugar.
            persona = L["forma"]["id"] in ("gana", "pierde", "se_come")
            q = quien_es(g, frase, lo_hace_alguien=persona)
        if q:
            ultimo[0] = q
        if hecho in ("estado", "estado_lugar"):
            x = h(q)
            if x["cambios"]:
                x["final"] = n
            elif x["inicio"] is None and not x["inicio_desconocido"]:
                x["inicio"] = n
            else:
                raise _NoEntiendo(frase + "   (me dicen dos veces cuantos tiene %s)" % q)
            x["cosa"] = x["cosa"] or g.get("cosa")
        elif hecho == "inicio_desconocido":
            x = h(q)
            x["inicio_desconocido"] = True
            x["cosa"] = x["cosa"] or g.get("cosa")
        elif hecho == "final":
            h(q)["final"] = n
        elif hecho in ("gana", "pierde", "gana_desconocido", "pierde_desconocido"):
            x = h(q)
            x["cambios"].append({"signo": "+" if hecho.startswith("gana") else "-",
                                 "n": n if not hecho.endswith("desconocido") else None,
                                 "frase": frase})
            x["cosa"] = x["cosa"] or g.get("cosa")
        elif hecho in ("tiene_mas_que", "tiene_menos_que"):
            h(q)
            h(g["otro"])
            mayor, menor = (q, g["otro"]) if hecho == "tiene_mas_que" else (g["otro"], q)
            relaciones.append({"mayor": mayor, "menor": menor, "n": n, "frase": frase})
        elif hecho == "total":
            for nombre in (g["quien"], g["otro"]):
                h(nombre)["cosa"] = h(nombre)["cosa"] or g.get("cosa")
            totales.append({"a": g["quien"], "b": g["otro"], "n": n, "frase": frase})
            ultimo[0] = g["otro"]
    if pregunta is None:
        raise _NoEntiendo("(no encuentro la PREGUNTA: sin pregunta no se que buscar)")
    if pregunta["pide"] in ("final", "estado", "inicio", "cambio") and not pregunta["quien"]:
        pregunta["quien"] = ultimo[0]
    if pregunta["pide"] in ("total", "diferencia") and not pregunta["quien"]:
        if len(orden) != 2:
            raise _NoEntiendo(pregunta["frase"] + "   (no se de que dos me preguntas)")
        pregunta["quien"], pregunta["otro"] = orden
    return {"quienes": quienes, "orden": orden, "relaciones": relaciones, "totales": totales,
            "pregunta": pregunta}


# ------------------------------------------------------------------ 3-4. APLICAR, DESCARTAR, CALCULAR

def _condicion(nombre, s):
    t = s["tipo"]
    tabla = {
        "es_un_cambio": lambda: t in ("cambio", "deshacer", "cambio_desconocido"),
        "se_sabe_el_cambio": lambda: s.get("n") is not None,
        "no_se_sabe_el_cambio": lambda: t == "cambio_desconocido",
        "el_despues_no_es_menor": lambda: s["despues"] >= s["antes"],
        "el_despues_no_es_mayor": lambda: s["despues"] <= s["antes"],
        "va_hacia_adelante": lambda: t == "cambio",
        "va_hacia_atras": lambda: t == "deshacer",
        "el_monton_crece": lambda: s.get("signo") == "+",
        "el_monton_disminuye": lambda: s.get("signo") == "-",
        "hay_bastantes": lambda: s["n"] <= s["antes"],
        "hay_bastantes_al_deshacer": lambda: s["n"] <= s["despues"],
        "se_piden_los_dos_juntos": lambda: t == "juntar",
        "son_la_misma_cosa": lambda: (not s.get("cosa_a") or not s.get("cosa_b")
                                      or s["cosa_a"] == s["cosa_b"]),
        "se_pide_el_hueco": lambda: t == "comparar",
        "hay_una_comparacion": lambda: t == "comparacion",
        "el_que_falta_tiene_menos": lambda: s.get("falta") == "menor",
        "el_que_falta_tiene_mas": lambda: s.get("falta") == "mayor",
        "hay_un_todo_y_una_parte": lambda: t == "parte",
        "la_parte_cabe_en_el_todo": lambda: s["parte"] <= s["todo"],
    }
    if nombre not in tabla:
        raise ValueError("condicion desconocida en resolver_r1.kn: %s" % nombre)
    return tabla[nombre]()


_DE_APLICACION = ("hay_bastantes", "hay_bastantes_al_deshacer", "la_parte_cabe_en_el_todo",
                  "el_despues_no_es_menor", "el_despues_no_es_mayor")


def _calcular(op, a, b, saber):
    """La operacion se hace con el METODO del sistema (columnas, y los dedos en cada columna)."""
    if op == "contar_hasta":
        # CONTAR DESDE a HASTA b (5.5, contar hacia adelante): los pasos son la respuesta.
        # La vuelta: desde a, contando esos pasos, se tiene que llegar a b.
        pasos = contar_hasta(decir(a, saber), decir(b, saber), saber)
        if pasos is None:
            raise _NoSe("no se puede contar de %d hasta %d hacia adelante" % (a, b))
        c = leer(pasos, saber)
        v = contar_adelante(decir(a, saber), pasos, saber, con_dedos=False)
        return c, "de %d a %d hay %d pasos" % (a, b, c), "contar (5.5)", \
            "%d + %d = %s" % (a, c, leer(v.get("resultado"), saber)), v.get("resultado") == decir(b, saber)
    if op == "sumar":
        r = decidir_7_3_columnas(str(a), str(b), saber)
        if r["conclusion"] != "se_puede":
            raise _NoSe("%d + %d: %s" % (a, b, r["conclusion"]))
        c = r["total_valor"]
        v = decidir_7_5_columnas(str(c), str(b), saber)          # la vuelta
        ok = v["conclusion"] == "se_puede" and v["resta"] == a
        return c, "%d + %d = %d" % (a, b, c), ("7.6" if r.get("unidad") == "7.6" else "7.3"), \
            "%d - %d = %s" % (c, b, v.get("resta")), ok
    r = decidir_7_5_columnas(str(a), str(b), saber)
    if r["conclusion"] != "se_puede":
        raise _NoSe("%d - %d: %s" % (a, b, r["conclusion"]))
    c = r["resta"]
    v = decidir_7_3_columnas(str(c), str(b), saber)              # la vuelta
    ok = v["conclusion"] == "se_puede" and v["total_valor"] == a
    # OJO: en la 7.5, r["unidad"] es la COLUMNA de las unidades (un dict), no el nombre de la unidad
    return c, "%d - %d = %d" % (a, b, c), ("7.6" if r.get("unidad") == "7.6" else "7.5"), \
        "%d + %d = %s" % (c, b, v.get("total_valor")), ok


def _paso(situacion, que_busca, saber, pasos):
    """Prueba TODOS los conocimientos con esta situacion; descarta con razon; aplica el que queda."""
    tabla = []
    validos = []
    for k in saber["resolver_r1"]["conocimientos"]:
        fila = {"id": k["id"], "nombre": k["nombre"], "unidad": k["unidad"]}
        for c in k["condiciones"]:
            nombre, _, porque = c.partition("|")
            nombre, porque = nombre.strip(), porque.strip()
            if not _condicion(nombre, situacion):
                fila["descartado"] = porque
                fila["falla_en"] = nombre
                fila["pasadas"] = k["condiciones"].index(c)
                break
        else:
            fila["aplica"] = True
            validos.append(k)
        tabla.append(fila)
    paso = {"que_busca": que_busca, "situacion": situacion, "candidatos": tabla}
    pasos.append(paso)
    if not validos:
        cerca = [f for f in tabla if f.get("falla_en") in _DE_APLICACION]
        if cerca:
            paso["imposible"] = cerca[0]
            raise _NoSe("IMPOSIBLE: %s" % cerca[0]["descartado"])
        raise _NoSe("ningun conocimiento que tengo encaja en: %s" % que_busca)
    resultados = []
    for k in validos:
        x, y = [situacion[c.strip()] for c in k["con"].split(",")]
        val, cuenta, metodo, vuelta, ok = _calcular(k["operacion"], x, y, saber)
        resultados.append((k, val, cuenta, metodo, vuelta, ok))
    if len({r[1] for r in resultados}) > 1:
        paso["ambiguo"] = [(r[0]["id"], r[1]) for r in resultados]
        raise _NoSe("AMBIGUO: %s" % ", ".join("%s da %d" % (i, v) for i, v in paso["ambiguo"]))
    k, val, cuenta, metodo, vuelta, ok = resultados[0]
    paso.update({"aplicado": k["id"], "nombre": k["nombre"], "unidad": k["unidad"],
                 "operacion": k["operacion"], "que_hace": k["que_hace"], "cuenta": cuenta,
                 "metodo": metodo, "vuelta": vuelta, "vuelta_ok": ok, "valor": val,
                 "tambien": [r[0]["id"] for r in resultados[1:]]})
    return val


def _valor_de(q, m, saber, pasos, pila=()):
    """Lo que tiene 'q'.  Si no es un dato, se busca combinando lo que se sabe (R.2 en pequeno)."""
    if q in pila:
        raise _NoSe("me doy vueltas: %s depende de %s y al reves; falta un dato de verdad"
                    % (q, " y de ".join(x for x in pila if x != q) or q))
    x = m["quienes"].get(q)
    if x is None:
        raise _NoSe("en el enunciado no hay nadie que se llame '%s'" % q)
    if x["final"] is not None:
        return x["final"]
    if x["inicio"] is not None:
        v = x["inicio"]
        for c in x["cambios"]:
            v = _paso({"tipo": "cambio", "antes": v, "signo": c["signo"], "n": c["n"]},
                      "lo que tiene %s despues de '%s'" % (q, c["frase"]), saber, pasos)
        return v
    for rel in m["relaciones"]:
        if q in (rel["mayor"], rel["menor"]):
            otro = rel["menor"] if q == rel["mayor"] else rel["mayor"]
            vo = _valor_de(otro, m, saber, pasos, pila + (q,))
            return _paso({"tipo": "comparacion", "conocido": vo, "n": rel["n"],
                          "falta": "mayor" if q == rel["mayor"] else "menor"},
                         "lo que tiene %s, sabiendo que '%s'" % (q, rel["frase"]), saber, pasos)
    for tot in m["totales"]:
        if q in (tot["a"], tot["b"]):
            otro = tot["b"] if q == tot["a"] else tot["a"]
            vo = _valor_de(otro, m, saber, pasos, pila + (q,))
            return _paso({"tipo": "parte", "todo": tot["n"], "parte": vo},
                         "lo que tiene %s, sabiendo que '%s'" % (q, tot["frase"]), saber, pasos)
    raise _NoSe("no tengo ningun dato de cuantos tiene %s (y no me lo invento)" % q)


def _resolver(m, saber):
    p = m["pregunta"]
    pasos = []
    pide = p["pide"]
    if pide in ("final", "estado"):
        return _valor_de(p["quien"], m, saber, pasos), pasos
    if pide == "cambio":
        x = m["quienes"].get(p["quien"])
        desconocidos = [c for c in (x or {}).get("cambios", []) if c["n"] is None]
        if x is None or len(desconocidos) != 1 or len(x["cambios"]) != 1:
            raise _NoSe("para saber cuanto cambio necesito UN cambio desconocido, el antes y el despues")
        if x["inicio"] is None or x["final"] is None:
            raise _NoSe("para saber cuanto cambio necesito saber lo que habia antes Y lo que hay despues")
        c = desconocidos[0]
        return _paso({"tipo": "cambio_desconocido", "antes": x["inicio"], "despues": x["final"],
                      "signo": c["signo"]},
                     "cuanto cambio %s con '%s'" % (p["quien"], c["frase"]), saber, pasos), pasos
    if pide == "inicio":
        x = m["quienes"].get(p["quien"])
        if x is None or x["final"] is None:
            raise _NoSe("para saber lo que habia al principio necesito saber lo que hay al final")
        v = x["final"]
        for c in reversed(x["cambios"]):
            v = _paso({"tipo": "deshacer", "despues": v, "signo": c["signo"], "n": c["n"]},
                      "lo que tenia %s antes de '%s'" % (p["quien"], c["frase"]), saber, pasos)
        return v, pasos
    a, b = p["quien"], p["otro"]
    va = _valor_de(a, m, saber, pasos)
    vb = _valor_de(b, m, saber, pasos)
    if pide == "total":
        return _paso({"tipo": "juntar", "a": va, "b": vb,
                      "cosa_a": m["quienes"][a]["cosa"], "cosa_b": m["quienes"][b]["cosa"]},
                     "lo que tienen %s y %s juntos" % (a, b), saber, pasos), pasos
    return _paso({"tipo": "comparar", "grande": max(va, vb), "pequeno": min(va, vb)},
                 "cuantos mas tiene uno que otro (%s y %s)" % (a, b), saber, pasos), pasos


def decidir_R1_problema(texto, saber=None):
    """
    R.1: RESOLVER un problema de suma o resta dicho con palabras.
    Conclusiones: resuelto / no_entiendo / no_se_resolver / sin_solucion / ambiguo.
    """
    if saber is None:
        saber = cargar_conocimiento()
    r = {"texto": texto, "unidad": "R.1"}
    try:
        leidas, lecturas = leer_enunciado(texto, saber)
        r["leidas"], r["lecturas"] = leidas, lecturas
        m = _montar(leidas)
        r["situacion"] = m
    except _NoEntiendo as e:
        r["conclusion"] = "no_entiendo"
        r["frase"] = str(e)
        return r
    try:
        valor, pasos = _resolver(m, saber)
    except _NoSe as e:
        r["pasos"] = locals().get("pasos") or []
        msg = str(e)
        r["conclusion"] = ("sin_solucion" if msg.startswith("IMPOSIBLE")
                           else "ambiguo" if msg.startswith("AMBIGUO") else "no_se_resolver")
        r["porque"] = msg
        return r
    r["pasos"] = pasos
    r["conclusion"] = "resuelto"
    r["valor"] = valor
    p = m["pregunta"]
    r["cosa"] = p.get("cosa") or (m["quienes"].get(p.get("quien") or "", {}) or {}).get("cosa") \
        or next((x["cosa"] for x in m["quienes"].values() if x["cosa"]), None)
    r["verificado"] = all(x.get("vuelta_ok") for x in pasos if "aplicado" in x)
    # AVISO de la trampa de la palabra: se dice, pero NO decide nada
    t = " %s " % _normalizar(texto)
    ops = [x["operacion"] for x in pasos if "aplicado" in x]
    r["avisos"] = []
    if ops and " mas " in t and ops[-1] == "restar":
        r["avisos"].append("el enunciado dice 'mas' y la ultima operacion es una RESTA")
    if ops and " menos " in t and ops[-1] == "sumar":
        r["avisos"].append("el enunciado dice 'menos' y la ultima operacion es una SUMA")
    return r


def explicar_R1_problema(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_R1_problema(texto, saber)
    L = ["PREGUNTA (R.1): resolver este PROBLEMA con lo que se  (aplicar todo, descartar con razones)",
         "ENUNCIADO: %s" % texto.strip(), ""]
    if r["conclusion"] == "no_entiendo":
        L.append("  1. LEER:  esta frase no encaja en ninguna forma que conozca:")
        L.append("       '%s'" % r["frase"])
        L.append("     (las formas estan en conocimiento/enunciados.kn; no adivino lo que no entiendo)")
        L.append("")
        L.append("RESULTADO: no_entiendo")
        return "\n".join(L)
    L.append("  1. LEER (cada frase con su forma; nada se adivina):")
    if r["lecturas"]:
        L.append("     numeros leidos con la secuencia: %s" % "; ".join(r["lecturas"]))
    for x in r["leidas"]:
        L.append("     %-44s -> %s '%s'" % ("'" + x["frase"] + "'", x["tipo"], x["forma"]["id"]))
    m = r["situacion"]
    L.append("")
    L.append("  2. LA SITUACION:")
    for q in m["orden"]:
        x = m["quienes"][q]
        partes = []
        if x["inicio"] is not None:
            partes.append("al principio %d" % x["inicio"])
        if x["inicio_desconocido"]:
            partes.append("al principio NO SE SABE")
        for c in x["cambios"]:
            partes.append("%s%s" % (c["signo"], "?" if c["n"] is None else c["n"]))
        if x["final"] is not None:
            partes.append("al final %d" % x["final"])
        L.append("     %-10s %s%s" % (q, ", ".join(partes) or "(no se dice cuantos)",
                                      ("  [%s]" % x["cosa"]) if x["cosa"] else ""))
    for rel in m["relaciones"]:
        L.append("     comparacion: %s tiene %d MAS que %s" % (rel["mayor"], rel["n"], rel["menor"]))
    for tot in m["totales"]:
        L.append("     todo: %s y %s tienen %d entre los dos" % (tot["a"], tot["b"], tot["n"]))
    p = m["pregunta"]
    L.append("     SE PREGUNTA: %s%s" % (p["pide"], " de " + " y ".join(x for x in (p["quien"], p["otro"]) if x)))
    for i, x in enumerate(r.get("pasos") or []):
        L.append("")
        L.append("  3.%d PASO: busco %s" % (i + 1, x["que_busca"]))
        L.append("      PRUEBO TODO LO QUE SE (y descarto lo que no tiene sentido aqui):")
        for c in x["candidatos"]:
            if c.get("aplica"):
                L.append("        [SI]  %-48s (%s)" % (c["nombre"], c["unidad"]))
            else:
                L.append("        [no]  %-48s porque %s" % (c["nombre"], c["descartado"]))
        if "aplicado" in x:
            L.append("      APLICO: %s  ->  %s" % (x["nombre"], x["que_hace"]))
            L.append("      CALCULO con %s: %s" % (
                ("las columnas (%s)" % x["metodo"]) if x["metodo"].startswith("7.") else x["metodo"],
                x["cuenta"]))
            L.append("      LA VUELTA: %s ... %s" % (x["vuelta"], "SI" if x["vuelta_ok"] else "NO"))
    L.append("")
    if r["conclusion"] != "resuelto":
        L.append("  NO PUEDO DAR UN NUMERO: %s" % r["porque"])
        L.append("  (No me lo invento.  Prefiero decir que no a dar una respuesta que no se sostiene.)")
        L.append("")
        L.append("RESULTADO: %s" % r["conclusion"])
        return "\n".join(L)
    if len([x for x in r["pasos"] if "aplicado" in x]) > 1:
        L.append("  4. COMBINAR: hicieron falta %d pasos; la respuesta de cada uno fue el dato del"
                 " siguiente." % len(r["pasos"]))
    elif not r["pasos"]:
        L.append("  4. NO HACE FALTA OPERAR: el dato que se pide ya esta en el enunciado.")
    L.append("  5. VERIFICADO (cada paso por la vuelta): %s" % ("SI" if r["verificado"] else "NO"))
    for a in r["avisos"]:
        L.append("")
        L.append("  OJO: %s." % a)
        L.append("  Por eso la operacion NO se elige por la palabra (nota de Carlos, 3 oct): sale de")
        L.append("  la situacion, despues de probar todo y descartar lo que no encaja.")
    L.append("")
    L.append("RESULTADO: %d%s" % (r["valor"], (" " + r["cosa"]) if r["cosa"] else ""))
    return "\n".join(L)
