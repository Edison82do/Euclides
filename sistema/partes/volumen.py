# -*- coding: utf-8 -*-
"""
Euclides - MULTIPLICAR TRES FACTORES Y EL VOLUMEN (paso M.14 del plan pedagogico, 7 oct 2026; 5.o).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

NCETM 2.20 (Multiplication with three factors and volume); Common Core 5.MD.C.3-5.
  punto 1: el volumen es el ESPACIO que ocupa algo (cuantos cubitos caben dentro);
  punto 2: se mide en unidades CUBICAS (cm3, m3);
  punto 3: el volumen de una caja es largo x ancho x alto;
  punto 4: la conmutativa y la asociativa valen con tres factores o mas;
  punto 5: el orden se elige segun la cuenta mas sencilla (25 x 7 x 4 = 25 x 4 x 7 = 100 x 7).
Y el problema inverso con la division (la altura de una caja de volumen 60 y base 5 x 3).
Las cuentas de tres factores las hacen las piezas tres_factores_* (pregunta 'multiplicar_tres').
Aqui solo se leen las ordenes, se pregunta a las piezas y se explica.
"""

import re

_VOL_N = r"\d+(?:[.,]\d+)?"
_VOL_U = r"(?:\s*(mm|cm|dm|m|km))?"
_VOL_UNIDADES = {"mm": "mm", "cm": "cm", "dm": "dm", "m": "m", "km": "km"}
_TF_ORDEN = re.compile(r"^(?:calcular:?\s*)?(" + _VOL_N + r"(?:\s*[x*×]\s*" + _VOL_N + r"){2,})$")
_VOL_PRE = r"^volumen:?\s*(?:de\s+)?(?:(?:una?|el)\s+)?"
_VOL_MEDIDA = "(" + _VOL_N + ")" + _VOL_U
_VOL_CAJA = re.compile(_VOL_PRE + r"(?:caja|cuboide|prisma|ortoedro)?\s*(?:de\s+)?" + _VOL_MEDIDA + r"\s*[x*×]\s*"
                       + _VOL_MEDIDA + r"\s*[x*×]\s*" + _VOL_MEDIDA + r"$")
_VOL_CUBO = re.compile(_VOL_PRE + r"cubo\s+de\s+(?:arista\s+|lado\s+)?" + _VOL_MEDIDA + r"$")
_VOL_CAJA_SOLA = _VOL_N + r"\s*[x*×]\s*" + _VOL_N + r"\s*[x*×]\s*" + _VOL_N
_VOL_COMP = re.compile(_VOL_PRE + r"(" + _VOL_CAJA_SOLA + r"(?:\s*\+\s*" + _VOL_CAJA_SOLA + r")+)" + _VOL_U + r"$")
_VOL_HUECO_T = r"(\?|" + _VOL_N + r")" + _VOL_U
_VOL_HUECO = re.compile(_VOL_PRE + r"(?:caja|cuboide|prisma|ortoedro)?\s*" + _VOL_HUECO_T + r"\s*[x*×]\s*"
                        + _VOL_HUECO_T + r"\s*[x*×]\s*" + _VOL_HUECO_T + r"\s*=\s*(" + _VOL_N + r")" + _VOL_U
                        + r"(?:\s*cubicos)?$")
_TF_LADO = _VOL_N + r"(?:\s*[x*×]\s*" + _VOL_N + r")*"
_TF_VERDAD = re.compile(r"^verdad:?\s*(" + _TF_LADO + r")\s*=\s*(" + _TF_LADO + r")$")


def _vol_limpio(texto):
    t = texto.lower().replace("ú", "u").replace("³", "3")
    t = re.sub(r"\b(cm|m|mm|dm|km)3\b", r"\1", t)
    return " ".join(t.strip().rstrip("?").split())


def _vol_factores(texto):
    return [_dp_normal(x.replace(",", ".")) for x in re.findall(_VOL_N, texto)]


def es_orden_volumen(texto):
    """Tres factores o mas ('25 x 7 x 4'), 'volumen: ...', o 'verdad:' con un lado de tres factores."""
    t = _vol_limpio(texto)
    if _TF_ORDEN.match(t) or t.startswith("volumen"):
        return True
    m = _TF_VERDAD.match(t)
    return bool(m) and any(len(_vol_factores(m.group(i))) >= 3 for i in (1, 2))


def _vol_unidad_cubica(unidad):
    return " %s cubicos" % unidad if unidad else " unidades cubicas"


# ---------------------------------------------------------------- tres factores

def decidir_tres_factores(factores, saber=None):
    """factores: lista de textos ('25', '7', '0.25').  Pregunta a las piezas de 'multiplicar_tres'."""
    if saber is None:
        saber = cargar_conocimiento()
    fs = [_dp_normal(f.replace(",", ".")) for f in factores]
    largos = [f for f in fs if "." in f and len(f.partition(".")[2]) > 3]
    if largos:
        return {"conclusion": "todavia_no", "porque": "%s tiene mas de tres cifras detras del punto: llego a las "
                                                      "milesimas (D.2)" % largos[0], "factores": fs}
    r = aplicar("multiplicar_tres", {"factores": fs}, saber)
    if r["conclusion"] != "hecho":
        return {"conclusion": "todavia_no", "porque": _dp_porque(r), "factores": fs}
    res = r["resultado"]
    return {"conclusion": "hecho", "valor": r["valor"], "pieza": r["pieza"]["id"], "metodo": res["metodo"],
            "pasos": res.get("pasos", []), "vuelta": res.get("vuelta", ""), "factores": fs,
            "tambien": r.get("tambien_servian", [])}


def _tf_en_orden(fs, saber):
    """El orden de siempre, para ensenar que sale LO MISMO (la asociativa).  None si no sale."""
    r = aplicar("tres_factores_en_orden", {"factores": fs}, saber)
    return r["resultado"] if r["conclusion"] == "hecho" else None


def _tf_lineas(r, saber):
    """Las lineas que explican una cuenta de tres factores ya hecha (r de decidir_tres_factores)."""
    L = []
    for i, paso in enumerate(r["pasos"]):
        L.append("  %d. %s" % (i + 1, paso))
    fs = r["factores"]
    if r["pieza"] == "tres_factores_buscando_la_pareja_facil":
        L.append("  EL ORDEN (NCETM 2.20, puntos 4 y 5): los factores se pueden CAMBIAR DE SITIO (conmutativa) y JUNTAR "
                 "de otra manera (asociativa); elijo la cuenta mas facil")
        otro = _tf_en_orden(fs, saber)
        if otro and [p.split("  (")[0] for p in otro["pasos"]] == [p.split("  (")[0] for p in r["pasos"]]:
            L.append("     aqui el orden de siempre ya es el facil")
        elif otro:
            L.append("     en el orden de siempre: %s ... SALE LO MISMO (%s), pero con cuentas mas dificiles"
                     % (", ".join(p.split("  (")[0] for p in otro["pasos"]), otro["valor"])
                     if otro["valor"] == r["valor"] else
                     "     en el orden de siempre sale %s: NO COINCIDE, algo esta mal" % otro["valor"])
        else:
            L.append("     en el orden de siempre no me sale tan facil (%s x %s primero se me complica)" % (fs[0], fs[1]))
    if r["vuelta"]:
        L.append("  COMPRUEBO con la operacion contraria (dividir, uno a uno): %s ... SI" % r["vuelta"])
    L.append("     (%s)" % r["metodo"])
    return L


def explicar_tres_factores(factores, saber):
    r = decidir_tres_factores(factores, saber)
    L = ["PREGUNTA (M.14): %s  (NCETM 2.20: tres factores o mas)" % " x ".join(r["factores"]), ""]
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["  TODAVIA NO: %s" % r["porque"], "", "RESULTADO: todavia_no"])
    L += _tf_lineas(r, saber)
    return "\n".join(L + ["", "RESULTADO: %s" % r["valor"]])


# ---------------------------------------------------------------- el volumen

def _vol_misma_unidad(unidades):
    puestas = [x for x in unidades if x]
    if not puestas:
        return True, ""
    if len(puestas) != len(unidades) and len(puestas) != 1:
        return False, ""
    return all(x == puestas[0] for x in puestas), puestas[0]


def _vol_capas(l, a, h, saber):
    """5.MD.C.5a: la capa del fondo (l x a cubitos, el area de G.1) y h capas.  None si no sale."""
    capa = decidir_decimal_por(l, "x", a, saber)
    if capa["conclusion"] != "hecho":
        return None
    total = decidir_decimal_por(capa["valor"], "x", h, saber)
    if total["conclusion"] != "hecho":
        return None
    return capa["valor"], total["valor"]


def _vol_dentro(l, a, h, saber):
    """Los cubitos de DENTRO, que no se ven: (l - 2) x (a - 2) x (h - 2).  None si alguna medida no
    pasa de dos (entonces todos tocan el borde) o hay decimales."""
    if any("." in x for x in (l, a, h)):
        return None
    ns = [int(x) for x in (l, a, h)]
    if any(decir(n, saber) is None or not viene_despues(decir(n, saber), "dos", saber) for n in ns):
        return None
    menos = ["%d" % aplicar("restar", {"a": n, "b": 2}, saber)["valor"] for n in ns]
    r = decidir_tres_factores(menos, saber)
    return (menos, r["valor"]) if r["conclusion"] == "hecho" else None


def decidir_volumen(l, a, h, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_tres_factores([l, a, h], saber)
    if r["conclusion"] != "hecho":
        return r
    r["capas"] = _vol_capas(*r["factores"], saber=saber)
    return r


def explicar_volumen_caja(medidas, unidades, saber, cubo=False):
    ok, unidad = _vol_misma_unidad(unidades)
    fs = [_dp_normal(x.replace(",", ".")) for x in medidas]
    if not ok:
        fs = ["%s%s" % (x, " %s" % v if v else "") for x, v in zip(fs, unidades)]
        unidad = ""
    titulo = ("un CUBO de arista %s%s" % (fs[0], " %s" % unidad if unidad else "") if cubo else
              "una caja de %s%s" % (" x ".join(fs), " %s" % unidad if unidad else ""))
    L = ["PREGUNTA (M.14): el VOLUMEN de %s  (NCETM 2.20; 5.MD.C.3-5)" % titulo, ""]
    if not ok:
        return "\n".join(L + ["  TODAVIA NO: las tres medidas tienen que estar en la MISMA unidad (%s); pasar de una "
                              "unidad a otra es de mas adelante" % ", ".join(x or "sin unidad" for x in unidades),
                              "", "RESULTADO: todavia_no"])
    if "0" in fs:
        return "\n".join(L + ["  una medida es 0: no es una caja, es plana; no ocupa espacio", "", "RESULTADO: 0"])
    r = decidir_volumen(fs[0], fs[1], fs[2], saber)
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["  TODAVIA NO: %s" % r["porque"], "", "RESULTADO: todavia_no"])
    l, a, h = fs
    u1 = " %s" % unidad if unidad else " unidad"
    if cubo:
        L.append("  un cubo tiene las tres aristas IGUALES: largo, ancho y alto son %s%s" % (l, " %s" % unidad if unidad else ""))
    L.append("  el volumen es el ESPACIO que ocupa (punto 1): cuantos cubitos de 1%s de lado caben dentro" % u1)
    if r["capas"]:
        capa, total = r["capas"]
        L.append("  LA CAPA DE ABAJO: %s filas de %s cubitos (el area, G.1): %s x %s = %s cubitos" % (a, l, l, a, capa))
        if "." not in l and "." not in a:
            L.extend(_cuadricula(int(l), int(a), saber))
        L.append("  HAY %s CAPAS IGUALES (el alto): %s x %s = %s  (la capa por el alto, 5.MD.C.5a)" % (h, capa, h, total))
        L.append("  y es MULTIPLICAR LAS TRES MEDIDAS (punto 3), en el orden mas facil (punto 5):")
    else:
        L.append("  es MULTIPLICAR LAS TRES MEDIDAS (punto 3), en el orden mas facil (punto 5):")
    L += _tf_lineas(r, saber)
    if r["capas"]:
        L.append("  por capas y multiplicando las tres: %s y %s ... %s" % (
            r["capas"][1], r["valor"], "LO MISMO" if _dp_normal(r["capas"][1]) == r["valor"] else "NO COINCIDE"))
    dentro = _vol_dentro(l, a, h, saber)
    if dentro:
        fuera = aplicar("restar", {"a": int(r["valor"]), "b": int(dentro[1])}, saber)["valor"]
        L.append("  OJO: tambien cuentan los cubitos de DENTRO, que no se ven: dentro hay %s = %s; desde fuera se "
                 "ven %d; en total %s" % (" x ".join(dentro[0]), dentro[1], fuera, r["valor"]))
    suma = decidir_cuenta_decimal(l, "+", a, saber)
    if suma["conclusion"] == "hecho":
        suma = decidir_cuenta_decimal(suma["valor"], "+", h, saber)
    if suma["conclusion"] == "hecho" and suma["valor"] != r["valor"]:
        L.append("  OJO: NO es sumar las medidas (%s + %s + %s = %s): eso no cuenta cubitos" % (l, a, h, suma["valor"]))
    L.append("  se mide en unidades CUBICAS (punto 2):%s" % _vol_unidad_cubica(unidad))
    return "\n".join(L + ["", "RESULTADO: %s%s" % (r["valor"], _vol_unidad_cubica(unidad))])


def explicar_volumen_compuesto(cajas_texto, unidad, saber):
    cajas = [_vol_factores(c) for c in re.findall(_VOL_CAJA_SOLA, cajas_texto)]
    L = ["PREGUNTA (M.14): el VOLUMEN de una figura hecha de cajas: %s  (NCETM 2.20; 5.MD.C.5c)"
         % " + ".join(" x ".join(c) for c in cajas), ""]
    vols = []
    for c in cajas:
        r = decidir_tres_factores(c, saber)
        if r["conclusion"] != "hecho":
            return "\n".join(L + ["  TODAVIA NO: %s" % r["porque"], "", "RESULTADO: todavia_no"])
        L.append("  la caja de %s = %s   (%s; compruebo: %s)" % (" x ".join(c), r["valor"], ", ".join(
            p.split("  (")[0] for p in r["pasos"]), r["vuelta"]))
        vols.append(r["valor"])
    total = vols[0]
    for v in vols[1:]:
        s = decidir_cuenta_decimal(total, "+", v, saber)
        if s["conclusion"] != "hecho":
            return "\n".join(L + ["  TODAVIA NO: la suma se me sale de la lista", "", "RESULTADO: todavia_no"])
        total = s["valor"]
    L.append("  se parte la figura en cajas que no se pisan y se SUMAN los volumenes: %s = %s%s"
             % (" + ".join(vols), total, _vol_unidad_cubica(unidad)))
    return "\n".join(L + ["", "RESULTADO: %s%s" % (total, _vol_unidad_cubica(unidad))])


def _vol_entre(x, d, saber):
    """x : d (d entero, no cero).  El cociente en texto, o None si no sale justo (ni en milesimas)."""
    if "." not in x:
        r = aplicar("dividir", {"total": int(x), "divisor": int(d)}, saber)
        if r["conclusion"] == "hecho" and not r["resultado"].get("resto"):
            return "%d" % r["valor"], r["resultado"]["metodo"]
    r = aplicar("dividir_decimal", {"x": x, "d": d}, saber)
    if r["conclusion"] == "hecho":
        return _dp_normal(r["valor"]), r["resultado"]["metodo"]
    return None


def explicar_volumen_hueco(medidas, unidades, volumen, saber):
    puestas = [x for x in unidades if x]
    ok, unidad = all(x == puestas[0] for x in puestas), (puestas[0] if puestas else "")
    V = _dp_normal(volumen.replace(",", "."))
    vistas = [x if x == "?" else _dp_normal(x.replace(",", ".")) for x in medidas]
    L = ["PREGUNTA (M.14): una caja de %s tiene un volumen de %s: cuanto mide lo que falta?  (NCETM 2.20: el problema "
         "inverso, con la division)" % (" x ".join(vistas), V), ""]
    if vistas.count("?") != 1:
        return "\n".join(L + ["  NO ENTIENDO: tiene que faltar UNA medida (un solo ?)", "", "RESULTADO: no_entiendo"])
    if not ok:
        return "\n".join(L + ["  TODAVIA NO: las medidas tienen que estar en la MISMA unidad", "", "RESULTADO: todavia_no"])
    sabidas = [x for x in vistas if x != "?"]
    if "0" in sabidas or V == "0":
        return "\n".join(L + ["  con una medida 0 (o volumen 0) no hay caja: cualquier medida o ninguna", "",
                              "RESULTADO: no_sale"])
    if any("." in x for x in sabidas):
        return "\n".join(L + ["  TODAVIA NO: habria que dividir ENTRE un decimal (6.o)", "", "RESULTADO: todavia_no"])
    L.append("  el volumen es las tres medidas multiplicadas: %s = %s" % (" x ".join(vistas), V))
    L.append("  DESHAGO cada medida que se, DIVIDIENDO (la operacion contraria), una a una:")
    actual = V
    for d in sorted(sabidas, key=len):
        q = _vol_entre(actual, d, saber)
        if q is None:
            return "\n".join(L + ["     %s : %s no sale justo (ni en milesimas): esa caja no tiene una medida que yo "
                                  "sepa escribir" % (actual, d), "", "RESULTADO: no_sale"])
        L.append("     %s : %s = %s   (%s)" % (actual, d, q[0], q[1]))
        actual = q[0]
    puesto = [actual if x == "?" else x for x in vistas]
    c = decidir_tres_factores(puesto, saber)
    if c["conclusion"] != "hecho" or c["valor"] != V:
        return "\n".join(L + ["  COMPRUEBO multiplicando: %s = %s ... NO CUADRA" % (" x ".join(puesto), c.get("valor")),
                              "", "RESULTADO: no_cuadra"])
    L.append("  COMPRUEBO multiplicando las tres: %s = %s ... SI" % (" x ".join(puesto), c["valor"]))
    u1 = " %s" % unidad if unidad else ""
    return "\n".join(L + ["", "RESULTADO: %s%s" % (actual, u1)])


# ---------------------------------------------------------------- la igualdad con tres factores

def _tf_valor_lado(fs, saber):
    if len(fs) == 1:
        return fs[0]
    if len(fs) == 2:
        r = decidir_decimal_por(fs[0], "x", fs[1], saber)
    else:
        r = decidir_tres_factores(fs, saber)
    return _dp_normal(r["valor"]) if r["conclusion"] == "hecho" else None


def explicar_verdad_tres(izq, der, saber):
    a, b = _vol_factores(izq), _vol_factores(der)
    L = ["PREGUNTA (M.14): %s = %s  verdadero o falso?  (NCETM 2.20, punto 4)" % (" x ".join(a), " x ".join(b)), ""]
    if sorted(a) == sorted(b):
        L.append("  son LOS MISMOS FACTORES en otro orden: con tres factores tambien se pueden cambiar de sitio "
                 "(conmutativa) y juntar como se quiera (asociativa).  No hace falta calcular")
        return "\n".join(L + ["", "RESULTADO: VERDADERO"])
    va, vb = _tf_valor_lado(a, saber), _tf_valor_lado(b, saber)
    if va is None or vb is None:
        return "\n".join(L + ["  TODAVIA NO: un lado no me sale", "", "RESULTADO: todavia_no"])
    L.append("  no son los mismos factores: calculo cada lado")
    L.append("     %s = %s" % (" x ".join(a), va))
    L.append("     %s = %s" % (" x ".join(b), vb))
    if va == vb:
        L.append("  dan el mismo numero (%s): por eso el = es verdadero" % va)
        return "\n".join(L + ["", "RESULTADO: VERDADERO"])
    L.append("  %s no es %s: el = es falso" % (va, vb))
    return "\n".join(L + ["", "RESULTADO: FALSO"])


# ---------------------------------------------------------------- la puerta

def explicar_orden_volumen(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    t = _vol_limpio(texto)
    m = _TF_ORDEN.match(t)
    if m:
        return explicar_tres_factores(_vol_factores(m.group(1)), saber)
    m = _TF_VERDAD.match(t)
    if m:
        return explicar_verdad_tres(m.group(1), m.group(2), saber)
    m = _VOL_CUBO.match(t)
    if m:
        return explicar_volumen_caja([m.group(1), m.group(1), m.group(1)], [m.group(2), m.group(2), m.group(2)],
                                     saber, cubo=True)
    m = _VOL_CAJA.match(t)
    if m:
        g = m.groups()
        return explicar_volumen_caja([g[0], g[2], g[4]], [g[1], g[3], g[5]], saber)
    m = _VOL_COMP.match(t)
    if m:
        return explicar_volumen_compuesto(m.group(1), m.group(2), saber)
    m = _VOL_HUECO.match(t)
    if m:
        g = m.groups()
        return explicar_volumen_hueco([g[0], g[2], g[4]], [g[1], g[3], g[5], g[7]], g[6], saber)
    return ("NO ENTIENDO ESTO: se escribe asi:  25 x 7 x 4    volumen: caja 5 x 3 x 2 cm    volumen: cubo de 4\n"
            "   volumen: 5 x 3 x 2 + 4 x 4 x 1    volumen: 5 x 3 x ? = 60    verdad: 2 x 3 x 4 = 4 x 3 x 2")
