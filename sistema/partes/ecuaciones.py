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
_TROZO = re.compile(r"[\d\s+\-=?_□−]*=[\d\s+\-=?_□−]*")


def _es_hueco(x):
    return x in _HUECOS or (x and set(x) == {"_"})


def _leer_lado(x):
    """'8 + ?' -> {"a": 8, "op": "+", "b": "?"};  '11' -> {"n": 11};  '?' -> {"n": "?"}."""
    x = " ".join(x.replace("+", " + ").replace("-", " - ").split())
    partes = x.split(" ")
    def valor(p):
        if _es_hueco(p):
            return "?"
        return int(p) if p.isdigit() else None
    if len(partes) == 1:
        v = valor(partes[0])
        return None if v is None else {"n": v}
    if len(partes) == 3 and partes[1] in "+-":
        a, b = valor(partes[0]), valor(partes[2])
        if a is None or b is None:
            return None
        return {"a": a, "op": partes[1], "b": b}
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
    m = _montar_ecuacion(e["lados"])
    r = {"ecuacion": e["texto"], "lados": e["lados"]}
    if m.get("sin_hueco"):
        r.update(conclusion="sin_hueco", porque="no hay ningun hueco que buscar (para saber si es "
                 "verdad: 'verdad: %s')" % e["texto"])
        return r
    if m.get("dos_huecos"):
        r.update(conclusion="dos_huecos", porque="hay DOS huecos: muchos numeros sirven (5 y 5, 3 y 7...). "
                 "Eso es de mas adelante (NCETM 1.31: problemas con dos desconocidos)")
        return r
    if m.get("balanza"):
        r.update(conclusion="balanza", porque="hay cuentas a los DOS lados del =: eso es la BALANZA "
                 "(paso E.2), todavia no lo se")
        return r
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
    if r["conclusion"] == "no_entiendo":
        return ("NO ENTIENDO ESTO: %s.\n"
                "   se escribe asi:  8 + ? = 11     (o  ecuacion: 5 = ? - 3)" % r.get("porque", ""))
    L = ["PREGUNTA (E.1): que numero va en el hueco?   %s" % r["ecuacion"], ""]
    if r["conclusion"] in ("sin_hueco", "dos_huecos", "balanza"):
        L.append("  %s" % r["porque"])
        L.append("")
        L.append("RESULTADO: %s" % r["conclusion"])
        return "\n".join(L)
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
