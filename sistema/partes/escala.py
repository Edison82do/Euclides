# -*- coding: utf-8 -*-
"""
Euclides - "VECES" Y FRACCIONES PARA COMPARAR: LA ESCALA (paso S.1 del plan pedagogico, 7 oct 2026; 4.o).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

NCETM 2.17 (Structures: using measures and comparison to understand scaling); Common Core 4.OA.A.1-2.
La COMPARACION MULTIPLICATIVA: lo largo es "K veces" lo corto (multiplicar); lo corto es "1/K" de lo largo
(dividir).  No es la comparacion aditiva: "4 veces mas" no es "4 mas".
"""

import re

_ORDEN_VECES = re.compile(r"^veces:?\s*(\d+)\s+veces\s+(\d+)$")
_ORDEN_CUANTAS = re.compile(r"^cuantas veces:?\s*(\d+)\s*(?:y|,|con)\s*(\d+)$")
_ADJ = r"(?:mas\s+)?(?:larg\w+|alt\w+|grande\w*|pesad\w+|car\w+|lejos|anch\w+|grues\w+|mayor\w*)"
_H_MIDE = re.compile(r"^(?:la |el |los |las )?(?P<cosa>(?:\w+ )*?\w+) (?:mide|pesa|cuesta|tiene|vale|son|es de) (?P<n>\d+)(?: (?P<u>\w+))?$")
_H_VECES = re.compile(r"^(?:la |el )?(?P<cosa>(?:\w+ )*?\w+?)? ?es (?P<k>\d+) veces " + _ADJ + r"(?: que (?:la |el )?(?P<otra>(?:\w+ )*\w+))?$")
_H_FRAC = re.compile(r"^(?:la |el )?(?P<cosa>(?:\w+ )*?\w+) (?:mide|pesa|cuesta|es) (?P<a>\d+)/(?P<b>\d+) de (?:la |el )?(?P<otra>(?:\w+ )*\w+)$")
_H_DOS = re.compile(r"^(?:la |el )?(?P<c1>(?:\w+ )*?\w+) mide (?P<n1>\d+)(?: (?P<u>\w+))? y (?:la |el )?(?P<c2>(?:\w+ )*?\w+) (?P<n2>\d+)(?: \w+)?$")
_P_CUANTO = re.compile(r"^cuanto (?:mide|pesa|cuesta|vale) (?:la |el )?(?P<cosa>(?:\w+ )*\w+)$")
_P_VECES = re.compile(r"^cuantas veces (?:es |mide )?(?:mas )?\w* ?(?:es )?(?:la |el )?(?P<cosa>(?:\w+ )*\w+)?$")


def _esc_limpio(texto):
    t = texto.lower()
    for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("¿", ""), ("¡", "")):
        t = t.replace(a, b)
    return " ".join(t.strip().split())


def es_orden_escala(texto):
    t = _esc_limpio(texto)
    if t.startswith("problema:"):
        t = t[len("problema:"):].strip()
    if _ORDEN_VECES.match(t) or _ORDEN_CUANTAS.match(t):
        return True
    return bool(re.search(r"\bveces\b", t) or re.search(r"\b\d+/\d+ de (?:la |el )", t)) and "?" in texto


def _cuantas_veces(grande, pequena, saber):
    r = aplicar("dividir", {"total": grande, "divisor": pequena}, saber)
    return r["valor"], r["resultado"].get("resto", 0)


def explicar_veces(k, n, saber):
    v = aplicar("multiplicar", {"a": k, "b": n}, saber)["valor"]
    suma = aplicar("sumar", {"a": k, "b": n}, saber)["valor"]
    L = ["PREGUNTA (S.1): %d veces %d  (NCETM 2.17; 4.OA.A.1)" % (k, n), "",
         "  %d veces %d es %d x %d = %d  (%d es %d veces %d, y tambien %d veces %d)" % (k, n, k, n, v, v, k, n, n, k),
         "  OJO: %d veces mas NO es %d mas (eso seria %d + %d = %d: la comparacion de sumar)" % (k, k, n, k, suma),
         "", "RESULTADO: %d" % v]
    return "\n".join(L)


def explicar_cuantas_veces(g, p, saber):
    L = ["PREGUNTA (S.1): cuantas veces %d es %d?  (NCETM 2.17)" % (g, p), ""]
    if p == 0:
        return "\n".join(L + ["  NO SE PUEDE: ninguna cantidad de veces cero da %d" % g, "", "RESULTADO: no_se_puede"])
    k, resto = _cuantas_veces(g, p, saber)
    L.append("  cuantas veces cabe %d en %d? (dividir, agrupando): %d : %d = %d%s" % (p, g, g, p, k,
                                                                               ", y sobra%s %d" % ("" if resto == 1 else "n", resto) if resto else ""))
    if resto:
        return "\n".join(L + ["  NO es un numero entero de veces.", "", "RESULTADO: no_entero"])
    L.append("  %d es %d veces %d;  y %d es 1/%d de %d (NCETM 2.17, puntos 1 y 2)" % (g, k, p, p, k, g))
    L += ["", "RESULTADO: %d" % k]
    return "\n".join(L)


def decidir_problema_escala(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    t = _esc_limpio(texto)
    if t.startswith("problema:"):
        t = t[len("problema:"):].strip()
    frases = [f.strip() for f in re.split(r"[.?!;]", t) if f.strip()]
    medidas, relacion, pregunta, unidad, ultima = {}, None, None, "", None
    for f in frases:
        m = _P_CUANTO.match(f)
        if m:
            pregunta = ("cuanto", m.group("cosa"))
            continue
        if f.startswith("cuantas veces"):
            pregunta = ("veces", None)
            continue
        m = _H_DOS.match(f)
        if m:
            medidas[m.group("c1")] = int(m.group("n1"))
            medidas[m.group("c2")] = int(m.group("n2"))
            unidad = m.group("u") or unidad
            continue
        m = _H_VECES.match(f)
        if m:
            cosa = m.group("cosa") or ultima
            relacion = ("veces", cosa, int(m.group("k")), m.group("otra"))
            continue
        m = _H_FRAC.match(f)
        if m:
            relacion = ("fraccion", m.group("cosa"), (int(m.group("a")), int(m.group("b"))), m.group("otra"))
            continue
        m = _H_MIDE.match(f)
        if m:
            medidas[m.group("cosa")] = int(m.group("n"))
            unidad = m.group("u") or unidad
            ultima = m.group("cosa")
            continue
        return {"conclusion": "no_entiendo", "porque": "no entiendo esta frase: '%s'" % f}
    if pregunta is None:
        return {"conclusion": "no_entiendo", "porque": "no hay pregunta"}
    def _nombre(x):
        return (x or "").split()[-1] if x else x
    med = {_nombre(k): v for k, v in medidas.items()}
    r = {"unidad": unidad}
    if pregunta[0] == "veces":
        if len(med) != 2:
            return {"conclusion": "no_entiendo", "porque": "para 'cuantas veces' hacen falta las dos medidas"}
        (n1, v1), (n2, v2) = list(med.items())
        g, p = (v1, v2) if viene_despues(decir(v1, saber), decir(v2, saber), saber) or v1 == v2 else (v2, v1)
        if p == 0:
            return {"conclusion": "no_se_puede", "porque": "una de las medidas es cero"}
        k, resto = _cuantas_veces(g, p, saber)
        r.update(tipo="cuantas_veces", grande=g, pequena=p, resto=resto)
        if resto:
            r.update(conclusion="no_entero", porque="%d no es un numero entero de veces %d" % (g, p))
            return r
        r.update(conclusion="hecho", valor=k, como="%d : %d = %d" % (g, p, k), operacion="dividir (agrupar)")
        return r
    if relacion is None:
        return {"conclusion": "no_entiendo", "porque": "no dice cuantas veces (ni que fraccion)"}
    tipo, cosa, k, otra = relacion
    cosa, otra = _nombre(cosa), _nombre(otra)
    buscada = _nombre(pregunta[1])
    if otra is None:                                  # 'la azul es 4 veces mas larga' (que la de antes)
        otras = [x for x in med if x != cosa]
        otra = otras[0] if otras else None
    if tipo == "veces":
        if buscada == cosa and otra in med:           # se sabe la corta: la larga MULTIPLICANDO
            v = aplicar("multiplicar", {"a": k, "b": med[otra]}, saber)["valor"]
            r.update(conclusion="hecho", valor=v, tipo="larga", como="%d x %d = %d" % (k, med[otra], v),
                     operacion="multiplicar", k=k, conocida=med[otra])
            return r
        if buscada == otra and cosa in med:           # se sabe la larga: la corta DIVIDIENDO
            q, resto = _cuantas_veces(med[cosa], k, saber)
            if resto:
                r.update(conclusion="no_entero", porque="%d no se reparte en %d partes iguales" % (med[cosa], k))
                return r
            r.update(conclusion="hecho", valor=q, tipo="corta", como="%d : %d = %d" % (med[cosa], k, q),
                     operacion="dividir", k=k, conocida=med[cosa])
            return r
    if tipo == "fraccion" and buscada == cosa and otra in med:
        d = decidir_fraccion_de(k[0], k[1], med[otra], saber)
        if d["conclusion"] != "hecho":
            r.update(conclusion=d["conclusion"], porque=d.get("porque"))
            return r
        r.update(conclusion="hecho", valor=d["valor"], tipo="fraccion",
                 como="%d/%d de %d: %d : %d = %d%s" % (k[0], k[1], med[otra], med[otra], k[1], d["cada"],
                                                       ", y %d de esas partes: %d" % (k[0], d["valor"]) if k[0] != 1 else ""),
                 operacion="dividir (la fraccion, F.1)")
        return r
    return {"conclusion": "no_entiendo", "porque": "no se que medida se busca"}


def explicar_problema_escala(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_problema_escala(texto, saber)
    L = ["PREGUNTA (S.1): una COMPARACION con 'veces' o con una fraccion  (NCETM 2.17; 4.OA.A.2)",
         "ENUNCIADO: %s" % texto.strip(), ""]
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["  %s" % r.get("porque", r["conclusion"]), "", "RESULTADO: %s" % r["conclusion"]])
    u = " %s" % r["unidad"] if r.get("unidad") else ""
    if r["tipo"] == "larga":
        L.append("  se sabe la CORTA (%d) y la larga es %d VECES ella: MULTIPLICAR (NCETM 2.17, punto 1)" % (r["conocida"], r["k"]))
        suma = aplicar("sumar", {"a": r["conocida"], "b": r["k"]}, saber)["valor"]
        L.append("     %s" % r["como"])
        L.append("  OJO: %d veces mas NO es %d mas (eso seria %d)" % (r["k"], r["k"], suma))
    elif r["tipo"] == "corta":
        L.append("  se sabe la LARGA (%d), que es %d veces la corta: la corta es 1/%d de ella: DIVIDIR (punto 2)" % (r["conocida"], r["k"], r["k"]))
        L.append("     %s" % r["como"])
    elif r["tipo"] == "fraccion":
        L.append("  la corta es una FRACCION de la larga: dividir (F.1; NCETM 2.17, punto 2)")
        L.append("     %s" % r["como"])
    else:
        L.append("  cuantas veces cabe la pequena (%d) en la grande (%d)? DIVIDIR agrupando" % (r["pequena"], r["grande"]))
        L.append("     %s;  y la pequena es 1/%d de la grande" % (r["como"], r["valor"]))
        u = ""
    L += ["", "RESULTADO: %d%s" % (r["valor"], u if r["tipo"] != "cuantas_veces" else " veces")]
    return "\n".join(L)


def explicar_orden_escala(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    t = _esc_limpio(texto)
    m = _ORDEN_VECES.match(t)
    if m:
        return explicar_veces(int(m.group(1)), int(m.group(2)), saber)
    m = _ORDEN_CUANTAS.match(t)
    if m:
        return explicar_cuantas_veces(int(m.group(1)), int(m.group(2)), saber)
    return explicar_problema_escala(texto, saber)
