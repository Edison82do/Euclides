# -*- coding: utf-8 -*-
"""
Euclides - AREA Y PERIMETRO (paso G.1 del plan pedagogico, 7 oct 2026; 4.o).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

NCETM 2.16 (Multiplicative contexts: area and perimeter 1); Common Core 3.MD.C.5-7, 3.MD.D.8, 4.MD.A.3.
El PERIMETRO es la distancia alrededor (se SUMAN los lados; en un poligono regular, se MULTIPLICA).
El AREA es la superficie (se cuentan los CUADRADITOS: filas y columnas, M.0; y es multiplicar los lados).
Euclides no ve figuras: se describen con palabras y numeros.
"""

import re

_LADOS_REGULAR = {"triangulo": 3, "cuadrado": 4, "pentagono": 5, "hexagono": 6, "heptagono": 7,
                  "octogono": 8, "octagono": 8, "eneagono": 9, "decagono": 10}
_UNI = r"(?:\s*(cm|m|mm|km))?"
_RECT = r"rectangulo\s+(\d+)" + _UNI + r"\s*[x×*]\s*(\d+)" + _UNI
_ORDEN_PER_RECT = re.compile(r"^perimetro:?\s*(?:de\s+(?:un\s+)?)?" + _RECT + r"$")
_ORDEN_PER_REG = re.compile(r"^perimetro:?\s*(?:de\s+(?:un\s+)?)?(\w+)(?:\s+regular)?\s+de\s+(\d+)" + _UNI + r"$")
_ORDEN_PER_LADOS = re.compile(r"^perimetro:?\s*(\d+(?:\s*,\s*\d+)+)" + _UNI + r"$")
_ORDEN_AREA_RECT = re.compile(r"^area:?\s*(?:de\s+(?:un\s+)?)?" + _RECT + r"$")
_ORDEN_AREA_CUAD = re.compile(r"^area:?\s*(?:de\s+(?:un\s+)?)?cuadrado\s+de\s+(\d+)" + _UNI + r"$")
_ORDEN_AREA_COMP = re.compile(r"^area:?\s*(\d+\s*x\s*\d+(?:\s*\+\s*\d+\s*x\s*\d+)+)" + _UNI + r"$")
_ORDEN_LADO = re.compile(r"^lado:?\s*(?:de\s+(?:un\s+)?)?(\w+)(?:\s+regular)?\s+de\s+perimetro\s+(\d+)" + _UNI + r"$")
_ORDEN_COMP_RECT = re.compile(r"^comparar:?\s*" + _RECT + r"\s+y\s+" + _RECT + r"$")


def _geo_limpio(texto):
    t = texto.lower().replace("á", "a").replace("í", "i").replace("é", "e").replace("ó", "o")
    return " ".join(t.strip().rstrip("?").split())


def es_orden_geometria(texto):
    t = _geo_limpio(texto)
    return any(p.match(t) for p in (_ORDEN_PER_RECT, _ORDEN_PER_REG, _ORDEN_PER_LADOS, _ORDEN_AREA_RECT,
                                    _ORDEN_AREA_CUAD, _ORDEN_AREA_COMP, _ORDEN_LADO, _ORDEN_COMP_RECT))


def _u(unidad):
    return " %s" % unidad if unidad else ""


def _u2(unidad):
    return " %s cuadrados" % unidad if unidad else " unidades cuadradas"


def _sumar_lista(nums, saber):
    total = nums[0]
    for x in nums[1:]:
        total = aplicar("sumar", {"a": total, "b": x}, saber)["valor"]
    return total


def _por(a, b, saber):
    r = aplicar("multiplicar", {"a": a, "b": b}, saber)
    return r.get("valor") if r["conclusion"] == "hecho" else None


# ---------------------------------------------------------------- perimetro

def decidir_perimetro_rectangulo(a, b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    suma = _sumar_lista([a, b, a, b], saber)
    dos = _sumar_lista([_por(2, a, saber), _por(2, b, saber)], saber)
    return {"conclusion": "hecho", "valor": suma, "comprobacion_ok": suma == dos}


def explicar_perimetro_rectangulo(a, b, unidad, saber):
    r = decidir_perimetro_rectangulo(a, b, saber)
    L = ["PREGUNTA (G.1): el PERIMETRO de un rectangulo de %d x %d%s  (NCETM 2.16)" % (a, b, _u(unidad)), "",
         "  el perimetro es la distancia ALREDEDOR del borde: se suman los cuatro lados (dos de %d y dos de %d)" % (a, b),
         "     %d + %d + %d + %d = %d%s" % (a, b, a, b, r["valor"], _u(unidad)),
         "  compruebo: 2 x %d + 2 x %d = %d ... %s" % (a, b, r["valor"], "SI" if r["comprobacion_ok"] else "NO"),
         "  (se mide en unidades de LONGITUD: no son cuadraditos)"]
    L += ["", "RESULTADO: %d%s" % (r["valor"], _u(unidad))]
    return "\n".join(L)


def explicar_perimetro_regular(figura, lado, unidad, saber):
    L = ["PREGUNTA (G.1): el PERIMETRO de un %s de lado %d%s  (NCETM 2.16, punto 3)" % (figura, lado, _u(unidad)), ""]
    n = _LADOS_REGULAR.get(figura)
    if n is None:
        return "\n".join(L + ["  NO ENTIENDO: no se cuantos lados tiene un '%s' (se: %s)" % (figura, ", ".join(sorted(_LADOS_REGULAR))),
                              "", "RESULTADO: no_entiendo"])
    v = _por(n, lado, saber)
    L.append("  un %s %stiene %d lados IGUALES: el perimetro es %d veces %d" % (
        figura, "(regular) " if figura not in ("cuadrado",) else "", n, n, lado))
    L.append("     %s = %d x %d = %d%s" % (" + ".join(str(lado) for _ in _fr_marcas(n, saber)), n, lado, v, _u(unidad)))
    L += ["", "RESULTADO: %d%s" % (v, _u(unidad))]
    return "\n".join(L)


def explicar_perimetro_lados(lados, unidad, saber):
    v = _sumar_lista(lados, saber)
    L = ["PREGUNTA (G.1): el PERIMETRO de una figura con lados %s%s  (NCETM 2.16, punto 2)" % (", ".join(str(x) for x in lados), _u(unidad)), "",
         "  alrededor del borde: se suman todos los lados",
         "     %s = %d%s" % (" + ".join(str(x) for x in lados), v, _u(unidad)), "", "RESULTADO: %d%s" % (v, _u(unidad))]
    return "\n".join(L)


def explicar_lado(figura, perimetro, unidad, saber):
    L = ["PREGUNTA (G.1): el LADO de un %s de perimetro %d%s  (NCETM 2.16, punto 3: lo inverso, dividir)" % (figura, perimetro, _u(unidad)), ""]
    n = _LADOS_REGULAR.get(figura)
    if n is None:
        return "\n".join(L + ["  NO ENTIENDO: no se cuantos lados tiene un '%s'" % figura, "", "RESULTADO: no_entiendo"])
    r = aplicar("dividir", {"total": perimetro, "divisor": n}, saber)
    resto = r["resultado"].get("resto", 0)
    L.append("  %d lados iguales hacen %d: cada lado es %d : %d = %d%s" % (n, perimetro, perimetro, n, r["valor"],
                                                                     (", y sobra 1" if resto == 1 else ", y sobran %d" % resto) if resto else ""))
    if resto:
        return "\n".join(L + ["  NO SALE ENTERO: %d no se reparte justo en %d lados iguales" % (perimetro, n), "", "RESULTADO: no_sale"])
    L.append("  compruebo: %d x %d = %d ... SI" % (n, r["valor"], perimetro))
    L += ["", "RESULTADO: %d%s" % (r["valor"], _u(unidad))]
    return "\n".join(L)


# ---------------------------------------------------------------- area

def decidir_area_rectangulo(a, b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    v = _por(a, b, saber)
    filas = aplicar("suma_de_iguales", {"veces": b, "n": a}, saber)
    return {"conclusion": "hecho" if v is not None else "todavia_no", "valor": v,
            "por_filas": filas.get("valor"), "comprobacion_ok": filas.get("valor") == v}


def _cuadricula(a, b, saber):
    if levantar_dedos(decir(a, saber), saber) is None or levantar_dedos(decir(b, saber), saber) is None:
        return []
    fila = "".join("[]" for _ in _fr_marcas(a, saber))
    return ["        %s" % fila for _ in _fr_marcas(b, saber)]


def explicar_area_rectangulo(a, b, unidad, saber):
    r = decidir_area_rectangulo(a, b, saber)
    L = ["PREGUNTA (G.1): el AREA de un rectangulo de %d x %d%s  (NCETM 2.16; 3.MD.C.7)" % (a, b, _u(unidad)), ""]
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["  se sale de mi lista", "", "RESULTADO: todavia_no"])
    L.append("  el area es la SUPERFICIE: cuantos cuadraditos de 1%s de lado caben dentro" % _u(unidad))
    L.extend(_cuadricula(a, b, saber))
    L.append("  %d filas de %d cuadraditos (M.0): %s = %s" % (b, a, " + ".join(str(a) for _ in _fr_marcas(b, saber))
                                                             if levantar_dedos(decir(b, saber), saber) else "...",
                                                             r["por_filas"]))
    L.append("  y es MULTIPLICAR los lados: %d x %d = %d ... %s" % (a, b, r["valor"], "lo mismo" if r["comprobacion_ok"] else "NO"))
    L.append("  (se mide en unidades CUADRADAS%s)" % (": %s" % _u2(unidad).strip() if unidad else ""))
    L += ["", "RESULTADO: %d%s" % (r["valor"], _u2(unidad))]
    return "\n".join(L)


def explicar_area_compuesta(rects, unidad, saber):
    L = ["PREGUNTA (G.1): el AREA de una figura hecha de rectangulos: %s  (NCETM 2.16, punto 6)"
         % " + ".join("%d x %d" % r for r in rects), ""]
    areas = []
    for a, b in rects:
        v = _por(a, b, saber)
        areas.append(v)
        L.append("  rectangulo de %d x %d: %d x %d = %d" % (a, b, a, b, v))
    total = _sumar_lista(areas, saber)
    L.append("  se parte la figura en rectangulos y se SUMAN las areas: %s = %d%s" % (" + ".join(str(x) for x in areas), total, _u2(unidad)))
    L += ["", "RESULTADO: %d%s" % (total, _u2(unidad))]
    return "\n".join(L)


def explicar_comparar_rectangulos(r1, r2, unidad, saber):
    (a, b), (c, d) = r1, r2
    A1, A2 = decidir_area_rectangulo(a, b, saber)["valor"], decidir_area_rectangulo(c, d, saber)["valor"]
    P1, P2 = decidir_perimetro_rectangulo(a, b, saber)["valor"], decidir_perimetro_rectangulo(c, d, saber)["valor"]
    L = ["PREGUNTA (G.1): rectangulo %d x %d contra rectangulo %d x %d  (3.MD.D.8: el area y el perimetro son DOS cosas)"
         % (a, b, c, d), ""]
    L.append("  AREA (cuadraditos de dentro):   %d x %d = %d   y   %d x %d = %d   -> %s" % (
        a, b, A1, c, d, A2, "la MISMA area" if A1 == A2 else "distinta area"))
    L.append("  PERIMETRO (el borde):           %d y %d   -> %s" % (P1, P2, "el MISMO perimetro" if P1 == P2 else "distinto perimetro"))
    if A1 == A2 and P1 != P2:
        L.append("  OJO: la misma area con distinto perimetro: el area y el perimetro NO van juntos")
    if P1 == P2 and A1 != A2:
        L.append("  OJO: el mismo perimetro con distinta area: el area y el perimetro NO van juntos")
    L += ["", "RESULTADO: area %s, perimetro %s" % ("igual" if A1 == A2 else "distinta", "igual" if P1 == P2 else "distinto")]
    return "\n".join(L)


# ---------------------------------------------------------------- la puerta

def explicar_orden_geometria(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    t = _geo_limpio(texto)
    m = _ORDEN_PER_RECT.match(t)
    if m:
        return explicar_perimetro_rectangulo(int(m.group(1)), int(m.group(3)), m.group(2) or m.group(4), saber)
    m = _ORDEN_PER_LADOS.match(t)
    if m:
        return explicar_perimetro_lados([int(x) for x in re.findall(r"\d+", m.group(1))], m.group(2), saber)
    m = _ORDEN_PER_REG.match(t)
    if m:
        return explicar_perimetro_regular(m.group(1), int(m.group(2)), m.group(3), saber)
    m = _ORDEN_AREA_RECT.match(t)
    if m:
        return explicar_area_rectangulo(int(m.group(1)), int(m.group(3)), m.group(2) or m.group(4), saber)
    m = _ORDEN_AREA_CUAD.match(t)
    if m:
        return explicar_area_rectangulo(int(m.group(1)), int(m.group(1)), m.group(2), saber)
    m = _ORDEN_AREA_COMP.match(t)
    if m:
        rects = [(int(a), int(b)) for a, b in re.findall(r"(\d+)\s*x\s*(\d+)", m.group(1))]
        return explicar_area_compuesta(rects, m.group(2), saber)
    m = _ORDEN_LADO.match(t)
    if m:
        return explicar_lado(m.group(1), int(m.group(2)), m.group(3), saber)
    m = _ORDEN_COMP_RECT.match(t)
    if m:
        g = m.groups()
        return explicar_comparar_rectangulos((int(g[0]), int(g[2])), (int(g[4]), int(g[6])), g[1] or g[3], saber)
    return "NO ENTIENDO ESTO: se escribe asi:  area: rectangulo 5 x 3    perimetro: cuadrado de 6"
