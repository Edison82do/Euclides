# -*- coding: utf-8 -*-
"""
Euclides - PROBLEMAS CON DOS INCOGNITAS (paso S.3 del plan pedagogico, 8 oct 2026; 6.o).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

NCETM 1.31 (Problems with two unknowns):
  punto 1: pueden tener una solucion, varias o ninguna.
  punto 2: la relacion entre las dos se dice de forma aditiva (8 mas) o multiplicativa (el triple).
  punto 3: la barra ensena la estructura.
  punto 4: hay UNA sola si se da la suma y la diferencia, o la suma y un multiplo.
  punto 5: si no se deja dibujar, se prueba en orden (una, varias o infinitas).
Las cuentas las hacen las piezas de 'dos_incognitas' (y su comprobacion, 'cumplen_las_ecuaciones').  Aqui solo se
LEEN las ecuaciones (a + b = 30; a - b = 8), se dice de que FORMA es cada una, se dibuja la barra y se explica.
"""

import re

_DI_PREFIJO = re.compile(r"^(dos\s+incognitas|incognitas)\s*:\s*")
_DI_TOKEN = re.compile(r"\d+(?:\.\d+)?|[a-z]|[+\-=]")
_DI_FORMAS = ("a + b = 30 (la suma)   a - b = 8  o  a = b + 8 (la diferencia)   a = 3 x b (el multiplo)   "
              "a x b = 24 (el producto)   2 x a + 5 x b = 32 (la suma con pesos)")


def _di_limpio(texto):
    t = texto.lower().replace("−", "-").replace("×", " x ").replace("*", " x ").replace("¿", "")
    for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u")):
        t = t.replace(a, b)
    return " ".join(t.strip().rstrip(".").split())


def _di_tokens(lado):
    """'2 x a + 5 x b' -> [("n","2"), ("op","x"), ("l","a"), ("op","+"), ...], o None si hay algo que no es."""
    crudos = _DI_TOKEN.findall(lado)
    if "".join(crudos) != lado.replace(" ", ""):
        return None
    out, prev = [], None
    for c in crudos:
        if c[0].isdigit():
            tok = ("n", c)
        elif c == "x" and prev is not None and prev[0] in ("n", "l"):
            tok = ("op", "x")                                # entre dos cosas: es POR
        elif c.isalpha():
            tok = ("l", c)
        elif c in "+-":
            tok = ("op", c)
        else:
            tok = ("=", c)
        out.append(tok)
        prev = tok
    return out


def _di_terminos(toks):
    """Los terminos de un lado con su signo: [("+", [("n","2"), ("l","a")]), ...].  None si esta mal escrito."""
    terminos, signo, factores, espera = [], "+", [], "cosa"
    for t in toks:
        if espera == "cosa":
            if t[0] not in ("n", "l"):
                return None
            factores.append(t)
            espera = "op"
        elif t == ("op", "x"):
            espera = "cosa"
        elif t[0] == "op":
            terminos.append((signo, factores))
            signo, factores, espera = t[1], [], "cosa"
        else:
            return None
    if espera != "op":
        return None
    terminos.append((signo, factores))
    return terminos


def _di_trozos(texto):
    t = _di_limpio(texto)
    m = _DI_PREFIJO.match(t)
    con_orden = m is not None
    if m:
        t = t[m.end():]
    return [x.strip() for x in t.split(";") if x.strip()], con_orden


def _di_letras_de(texto):
    """Las letras de una ecuacion (o None si no es una ecuacion escrita con numeros, letras, + - x y un =)."""
    toks = _di_tokens(texto)
    if not toks or [t for t in toks if t[0] == "="] != [("=", "=")]:
        return None
    return [t[1] for t in toks if t[0] == "l"]


def es_orden_dos_incognitas(texto):
    """Ecuaciones (una o varias, separadas por ';') con DOS letras distintas entre todas; o con la orden delante."""
    trozos, con_orden = _di_trozos(texto)
    if con_orden:
        return True
    if not trozos:
        return False
    letras = []
    for tr in trozos:
        ls = _di_letras_de(tr)
        if ls is None:
            return False
        letras += ls
    return len(set(letras)) >= 2


# ---------------------------------------------------------------- leer cada ecuacion: de que FORMA es

def _di_numero(f):
    """'08' -> '8', '1.50' -> '1.5'.  Mirar las cifras."""
    if "." in f:
        f = f.rstrip("0").rstrip(".")
    e, punto, d = f.partition(".")
    e = e.lstrip("0") or "0"
    return "%s.%s" % (e, d) if punto else e


def _di_es_numero(lado):
    return len(lado) == 1 and lado[0][0] == "+" and len(lado[0][1]) == 1 and lado[0][1][0][0] == "n"


def _di_es_letra(lado):
    return len(lado) == 1 and lado[0][0] == "+" and len(lado[0][1]) == 1 and lado[0][1][0][0] == "l"


def _di_letra_con_peso(termino):
    """('+', [n, l]) o ('+', [l, n]) o ('+', [l]) -> (letra, peso); None si no."""
    signo, fs = termino
    if signo != "+":
        return None
    ls = [f[1] for f in fs if f[0] == "l"]
    ns = [f[1] for f in fs if f[0] == "n"]
    if len(ls) != 1 or len(ns) > 1:
        return None
    return ls[0], _di_numero(ns[0]) if ns else "1"


def _di_forma(texto):
    """Una ecuacion -> {"tipo": lineal | diferencia | multiplo | producto, ...} o {"error": ...}."""
    toks = _di_tokens(texto)
    k = toks.index(("=", "="))
    izq, der = _di_terminos(toks[:k]), _di_terminos(toks[k + 1:])
    if izq is None or der is None:
        return {"error": "'%s' esta mal escrita" % texto}
    if _di_es_numero(izq) and not _di_es_numero(der):
        izq, der = der, izq                               # 24 = a + b es lo mismo que a + b = 24
    escrita = "%s = %s" % (_di_lado(izq), _di_lado(der))
    if _di_es_numero(der):
        n = _di_numero(der[0][1][0][1])
        if len(izq) == 2 and izq[1][0] == "+":
            p, q = _di_letra_con_peso(izq[0]), _di_letra_con_peso(izq[1])
            if p and q and p[0] != q[0]:
                return {"tipo": "lineal", "letras": [p[0], q[0]], "coef": {p[0]: p[1], q[0]: q[1]}, "n": n,
                        "texto": escrita}
        if len(izq) == 2 and izq[1][0] == "-" and _di_es_letra(izq[:1]) and \
                len(izq[1][1]) == 1 and izq[1][1][0][0] == "l" and izq[0][1][0][1] != izq[1][1][0][1]:
            mayor, menor = izq[0][1][0][1], izq[1][1][0][1]
            return {"tipo": "diferencia", "mayor": mayor, "menor": menor, "letras": [mayor, menor], "n": n,
                    "texto": escrita}
        if len(izq) == 1 and izq[0][0] == "+" and [f[0] for f in izq[0][1]] == ["l", "l"] and \
                izq[0][1][0][1] != izq[0][1][1][1]:
            return {"tipo": "producto", "letras": [izq[0][1][0][1], izq[0][1][1][1]], "n": n, "texto": escrita}
        return {"error": "'%s' no se de que forma es" % texto}
    if not _di_es_letra(izq):
        izq, der = der, izq
    if _di_es_letra(izq):
        uno = izq[0][1][0][1]
        if len(der) == 2:
            a, b = der
            if a[0] == "+" and len(a[1]) == 1 and len(b[1]) == 1:
                x, y = a[1][0], b[1][0]
                if b[0] == "+" and {x[0], y[0]} == {"l", "n"}:            # a = b + 8  o  a = 8 + b
                    otra, n = (x[1], y[1]) if x[0] == "l" else (y[1], x[1])
                    if otra != uno:
                        return {"tipo": "diferencia", "mayor": uno, "menor": otra, "letras": [uno, otra],
                                "n": _di_numero(n), "texto": escrita}
                if b[0] == "-" and x[0] == "l" and y[0] == "n" and x[1] != uno:      # a = b - 8: b tiene 8 mas
                    return {"tipo": "diferencia", "mayor": x[1], "menor": uno, "letras": [x[1], uno],
                            "n": _di_numero(y[1]), "texto": escrita}
        if len(der) == 1:
            p = _di_letra_con_peso(der[0])
            if p and p[0] != uno and "." not in p[1] and p[1] != "0":
                return {"tipo": "multiplo", "grande": uno, "chico": p[0], "k": p[1], "letras": [uno, p[0]],
                        "texto": escrita}
    return {"error": "'%s' no se de que forma es" % texto}


def _di_lado(terminos):
    trozos = []
    for k, (signo, fs) in enumerate(terminos):
        t = " x ".join(_di_numero(f[1]) if f[0] == "n" else f[1] for f in fs)
        trozos.append(t if not k else "%s %s" % (signo, t))
    return " ".join(trozos)


def _di_leer(texto):
    trozos, _ = _di_trozos(texto)
    if not trozos:
        return {"error": "no hay ninguna ecuacion"}
    eqs, letras = [], []
    for tr in trozos:
        if _di_letras_de(tr) is None:
            return {"error": "'%s' no es una ecuacion (numeros, letras, + - x y un =)" % tr}
        f = _di_forma(tr)
        if "error" in f:
            return f
        eqs.append(f)
        for l in f["letras"]:
            if l not in letras:
                letras.append(l)
    return {"ecuaciones": eqs, "letras": sorted(letras)}


# ---------------------------------------------------------------- decidir

def _di_numeros(eqs):
    for e in eqs:
        for clave in ("n", "k"):
            if clave in e:
                yield e[clave]
        for c in e.get("coef", {}).values():
            yield c


def _di_problema(eqs, saber):
    for f in _di_numeros(eqs):
        e, _, d = f.partition(".")
        if len(d) > 3:
            return "todavia_no", "%s tiene mas de tres cifras detras del punto: llego a las milesimas (D.2)" % f
        if decir(escribir_cifras([int(c) for c in reversed(e)]), saber) is None:
            return "no_alcanza", "%s se pasa de mi lista (llego a %s)" % (f, techo(saber))
    for e in eqs:
        pesos = list(e.get("coef", {}).values())
        if "k" in e:
            pesos.append(e["k"])
        for c in pesos:
            if "." in c:
                return "todavia_no", "un peso con decimales (%s): por ahora los pesos son enteros" % c
    return None


def decidir_dos_incognitas(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    o = _di_leer(texto)
    if "error" in o:
        if "no se de que forma" in o["error"]:
            return {"conclusion": "todavia_no", "porque": "%s; las formas que se: %s" % (o["error"], _DI_FORMAS)}
        return {"conclusion": "no_entiendo", "porque": o["error"]}
    r = dict(o)
    if len(o["letras"]) != 2:
        r.update(conclusion="todavia_no", porque="hay %s letras: por ahora, problemas con DOS incognitas"
                 % decir(len(o["letras"]), saber))
        return r
    if o["ecuaciones"][2:]:
        r.update(conclusion="todavia_no", porque="hay %s ecuaciones: por ahora, una o dos"
                 % decir(len(o["ecuaciones"]), saber))
        return r
    p = _di_problema(o["ecuaciones"], saber)
    if p:
        r.update(conclusion=p[0], porque=p[1])
        return r
    situacion = {"letras": o["letras"], "ecuaciones": o["ecuaciones"]}
    a = aplicar("dos_incognitas", situacion, saber)
    r["situacion"] = situacion
    if a["conclusion"] != "hecho":
        porques = [f.get("no_salio", "") for f in a.get("candidatos", []) if f.get("no_salio")]
        porque = porques[0] if porques else (a.get("porque") or a["conclusion"])
        if "se pasa del techo" in porque:
            r.update(conclusion="no_alcanza", porque=porque)
        else:
            r.update(conclusion="todavia_no", porque=porque)
        r["candidatos"] = a.get("candidatos", [])
        return r
    res = a["resultado"]
    r.update({"conclusion": "hecho", "valor": a["valor"], "pieza": a["pieza"]["id"], "metodo": res["metodo"],
              "pasos": res["pasos"], "vuelta": res["vuelta"], "cuantas": res["cuantas"],
              "soluciones": res.get("soluciones", []), "resultado": res,
              "tambien": a.get("tambien_servian", [])})
    return r


# ---------------------------------------------------------------- explicar

def _di_que_dice(e):
    if e["tipo"] == "lineal":
        a, b = e["letras"]
        if e["coef"][a] == "1" and e["coef"][b] == "1":
            return "la SUMA: %s y %s juntas son %s" % (a, b, e["n"])
        return "una suma con PESOS: %s veces %s y %s veces %s juntan %s" % (e["coef"][a], a, e["coef"][b], b, e["n"])
    if e["tipo"] == "diferencia":
        return "la DIFERENCIA: %s tiene %s mas que %s (relacion ADITIVA)" % (e["mayor"], e["n"], e["menor"])
    if e["tipo"] == "multiplo":
        return "%s es %s veces %s (relacion MULTIPLICATIVA)" % (e["grande"], e["k"], e["chico"])
    return "el PRODUCTO: %s por %s da %s" % (e["letras"][0], e["letras"][1], e["n"])


def _di_de_tipo(r, tipo):
    return [e for e in r["ecuaciones"] if e["tipo"] == tipo]


def _di_barra(r, saber):
    """La barra de NCETM, con las dos barras ALINEADAS (empiezan en el mismo sitio, una debajo de la otra)."""
    dif, mul, lin = _di_de_tipo(r, "diferencia"), _di_de_tipo(r, "multiplo"), _di_de_tipo(r, "lineal")
    suma = [e for e in lin if set(e["coef"].values()) == {"1"}]
    if r["ecuaciones"][2:] or not r["ecuaciones"][1:]:
        return []
    if dif and suma:
        d = dif[0]
        trozo = "[%s]" % ("  %s  " % d["menor"]).center(9)
        return ["     %s: %s[ %s ]   \\" % (d["mayor"], trozo, d["n"]),
                "     %s: %s         } juntas: %s" % (d["menor"], trozo, suma[0]["n"])]
    if mul and (suma or dif):
        m = mul[0]
        k = escribir_cifras([int(c) for c in reversed(m["k"])])
        if viene_despues(decir(k, saber), "seis", saber):
            grande = "[ %s ][ %s ] ... (%s trozos)" % (m["chico"], m["chico"], m["k"])
        else:
            grande = "".join("[ %s ]" % m["chico"] for _ in range(k, 0, -1))
        L = ["     %s: %s" % (m["grande"], grande), "     %s: [ %s ]" % (m["chico"], m["chico"])]
        if suma:
            L[1] = "%s   } juntas: %s" % (L[1].ljust(len(L[0])), suma[0]["n"])
            L[0] += "   \\"
        elif dif[0]["mayor"] == m["grande"]:
            L.append("         la diferencia (%s) son los trozos que %s tiene DE MAS" % (dif[0]["n"], m["grande"]))
        return L
    return []


def _di_cuenta(terminos, saber):
    try:
        a = aplicar("combinar", {"terminos": terminos}, saber)
    except Exception:
        return None
    return a["valor"] if a["conclusion"] == "hecho" else None


def _di_errores(r, saber):
    """Los errores tipicos, calculados para ensenarlos (y que se vea que NO son la respuesta)."""
    L = []
    dif, mul, lin = _di_de_tipo(r, "diferencia"), _di_de_tipo(r, "multiplo"), _di_de_tipo(r, "lineal")
    if r["pieza"].startswith("suma_y_diferencia") and r["cuantas"] == "una":
        total, d = lin[0]["n"], dif[0]["n"]
        mitad = _di_valor_de("dividir_decimal", {"x": total, "d": "2"}, saber)
        if mitad is not None:
            mal = _di_cuenta([["+", [mitad]], ["+", [d]]], saber)
            junta = _di_cuenta([["+", [mitad]], ["+", [mal]]], saber) if mal else None
            if junta:
                L.append("     OJO: NO es %s : 2 = %s y %s + %s = %s: asi juntan %s, no %s (primero se QUITA la diferencia)"
                         % (total, mitad, mitad, d, mal, junta, total))
    if r["pieza"] == "suma_y_multiplo_con_la_barra":
        total, k = lin[0]["n"], mul[0]["k"]
        if k != "1":
            mal = _di_valor_de("dividir_decimal", {"x": total, "d": k}, saber)
            if mal is not None:
                L.append("     OJO: NO es %s : %s = %s: los trozos son %s y UNO mas, el de %s" % (
                    total, k, mal, k, mul[0]["chico"]))
    if r["pieza"] == "diferencia_y_multiplo_con_la_barra" and r["cuantas"] == "una":
        d, k = dif[0]["n"], mul[0]["k"]
        mal = _di_valor_de("dividir_decimal", {"x": d, "d": k}, saber)
        if mal is not None:
            L.append("     OJO: NO es %s : %s = %s: la diferencia son los trozos DE MAS, uno menos que %s" % (d, k, mal, k))
    return L


def _di_valor_de(pieza, situacion, saber):
    try:
        a = aplicar(pieza, situacion, saber)
    except Exception:
        return None
    return a["valor"] if a["conclusion"] == "hecho" else None


def _di_cuantas(r):
    c = r["cuantas"]
    p = r["pieza"]
    if p in ("suma_y_diferencia_quitando_la_diferencia", "suma_y_diferencia_anadiendo_la_diferencia",
             "suma_y_multiplo_con_la_barra", "diferencia_y_multiplo_con_la_barra"):
        if c == "una":
            return ("  CUANTAS: UNA sola (NCETM 1.31, punto 4): con la %s, la barra no deja otra manera de "
                    "repartir" % ("suma y la diferencia" if p.startswith("suma_y_dif") else
                                  "suma y la relacion multiplicativa" if p.startswith("suma") else "diferencia y el multiplo"))
        return "  CUANTAS: %s (NCETM 1.31, punto 1: tambien puede no haber ninguna, o muchas)" % c.upper()
    if p == "probar_en_orden":
        return ("  CUANTAS: %s (probe las %s, todas en orden: NCETM 1.31, punto 5)"
                % ({"una": "UNA", "varias": "VARIAS", "ninguna": "NINGUNA"}[c], r["resultado"]["pruebas"]))
    return "  CUANTAS: %s (NCETM 1.31, punto 1: no siempre hay una sola)" % c.upper()


def explicar_dos_incognitas(texto, saber):
    r = decidir_dos_incognitas(texto, saber)
    if r["conclusion"] == "no_entiendo":
        return ("NO ENTIENDO ESTO: %s\n   se escribe asi:  a + b = 30; a - b = 8      a + b = 24; a = 3 x b\n"
                "                    a x b = 24; a + b = 10      a + b = 10" % r["porque"])
    L = ["PREGUNTA (S.3): problemas con DOS INCOGNITAS  (NCETM 1.31)", ""]
    for e in r.get("ecuaciones", []):
        L.append("  %s   -> %s" % (e["texto"].ljust(22), _di_que_dice(e)))
    if r["conclusion"] != "hecho":
        etiqueta = {"no_alcanza": "NO ALCANZA"}.get(r["conclusion"], "TODAVIA NO")
        return "\n".join(L + ["", "  %s: %s" % (etiqueta, r["porque"]), "", "RESULTADO: %s" % r["conclusion"]])
    barra = _di_barra(r, saber)
    if barra:
        L += ["", "  LA BARRA (las dos alineadas, una debajo de la otra; NCETM 1.31, punto 3):"] + barra
    L.append("")
    L += ["  %d. %s" % (i + 1, p) for i, p in enumerate(r["pasos"])]
    L.append("     (%s)" % r["metodo"])
    if r["resultado"].get("con_enteros"):
        L.append("     (%s; con decimales, una)" % r["resultado"]["con_enteros"])
    for otra in r.get("tambien", []):
        try:
            a = aplicar(otra, r["situacion"], saber)
        except Exception:
            a = {"conclusion": "no_salio"}
        if a["conclusion"] == "hecho":
            if a["valor"] == r["valor"]:
                dice = "LO MISMO: la estructura no cambia"
            elif r["resultado"].get("con_enteros") and a["valor"] == "ninguna" and otra == "probar_en_orden":
                dice = "LO MISMO: probando con enteros no hay ninguna (la de la barra es con decimales)"
            else:
                dice = "NO COINCIDE, algo esta mal"
            L.append("     OTRA ESTRATEGIA (%s): sale %s ... %s" % (otra, a["valor"], dice))
        else:
            fila = [f for f in a.get("candidatos", []) if f.get("no_salio")]
            if fila:
                L.append("     OTRA ESTRATEGIA (%s): no me sale (%s)" % (otra, fila[0]["no_salio"]))
    L += _di_errores(r, saber)
    L.append(_di_cuantas(r))
    if r["vuelta"]:
        L.append("  COMPRUEBO poniendo los numeros en las ecuaciones: %s" % r["vuelta"])
    return "\n".join(L + ["", "RESULTADO: %s" % r["valor"]])


def explicar_orden_dos_incognitas(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    return explicar_dos_incognitas(texto, saber)
