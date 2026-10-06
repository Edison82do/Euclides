# -*- coding: utf-8 -*-
"""
Euclides - LOS DECIMALES (pasos D.1 y D.2 del plan pedagogico, 7 oct 2026; 4.o).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

NCETM 1.23 (decimas) y 1.24 (centesimas y milesimas); Common Core 4.NF.C.5-7.
LA DECIMA ES UNA COSA (el 'unitising' de la 6.2 y la N.3): 2.7 + 1.5 son 27 decimas + 15 decimas = 42
decimas = 4.2.  Diez decimas hacen un entero, como diez unidades una decena.  Las cuentas se hacen en
columnas con el punto alineado, y se comprueban contando en decimas.  Se escribe con PUNTO (NCETM; la
Republica Dominicana); se acepta tambien la coma.  Nada de calculadora: las cifras se leen y se escriben.
"""

import re

_DEC_MAX = 1                       # D.1: decimas.  (D.2 lo sube a 3: centesimas y milesimas.)
_DEC_NOMBRE = {1: ("decima", "decimas"), 2: ("centesima", "centesimas"), 3: ("milesima", "milesimas")}
_DEC_NUM = r"\d+(?:[.,]\d+)?"
_ORDEN_DECIMAL = re.compile(r"^decimal:?\s*(\d+[.,]\d+|\d+)$")
_ORDEN_DEC_CUENTA = re.compile(r"^(?:calcular:?\s*)?(" + _DEC_NUM + r")\s*([+\-])\s*(" + _DEC_NUM + r")$")
_ORDEN_DEC_COMPARAR = re.compile(r"^comparar:?\s*(" + _DEC_NUM + r")\s*(?:y|con|\?)\s*(" + _DEC_NUM + r")$")
_ORDEN_DEC_REDONDEAR = re.compile(r"^redondear:?\s*(\d+[.,]\d+)(?:\s+al\s+entero)?$")
_ORDEN_DEC_SALTOS = re.compile(r"^de\s+0[.,]1\s+en\s+0[.,]1(?:\s+desde\s+(" + _DEC_NUM + r"))?(?:\s+hasta\s+(" + _DEC_NUM + r"))?$")


def _dec_limpio(texto):
    return " ".join(texto.lower().strip().rstrip("?").split())


def _dec_leer(texto):
    """'2.35' -> ('2', '35');  '7' -> ('7', '').  Es LEER las cifras, una a una."""
    t = texto.replace(",", ".")
    if "." in t:
        e, d = t.split(".", 1)
        return (e or "0"), d
    return t, ""


def _dec_lugares(*textos):
    return max(len(_dec_leer(t)[1]) for t in textos)


def _dec_en_pequenas(texto, k):
    """2.7 con k = 1 -> 27 (decimas): se escriben las cifras sin el punto (se rellena con ceros)."""
    e, d = _dec_leer(texto)
    while len(d) < k:
        d += "0"
    return escribir_cifras([int(c) for c in reversed("%s%s" % (e, d))])


def _dec_escribir(n, k):
    """42 decimas -> '4.2';  40 -> '4';  7 -> '0.7'.  Es ESCRIBIR las cifras y poner el punto."""
    s = str(n)
    if k == 0:
        return s
    while len(s) <= k:
        s = "0" + s
    e, d = s[:-k], s[-k:]
    d = d.rstrip("0")
    return e if not d else "%s.%s" % (e, d)


def _dec_cuantas(n, k):
    uno, varios = _DEC_NOMBRE[k]
    return "%d %s" % (n, uno if n == 1 else varios)


def es_orden_decimal(texto):
    t = _dec_limpio(texto)
    if _ORDEN_DECIMAL.match(t) or _ORDEN_DEC_SALTOS.match(t):
        return True
    for patron in (_ORDEN_DEC_CUENTA, _ORDEN_DEC_COMPARAR, _ORDEN_DEC_REDONDEAR):
        if patron.match(t) and re.search(r"\d[.,]\d", t):
            return True
    return False


def _dec_problema(*textos):
    k = _dec_lugares(*textos)
    if k > _DEC_MAX:
        return "todavia_no", ("con %s todavia no: en D.1 solo decimas (una cifra detras del punto); "
                              "las centesimas son D.2 (NCETM 1.24)" % _DEC_NOMBRE.get(k, ("", "mas cifras"))[1])
    return None


# ---------------------------------------------------------------- decimal: 2.3

def explicar_decimal(texto, saber):
    e, d = _dec_leer(texto)
    k = len(d)
    L = ["PREGUNTA (D.1): que es %s?  (NCETM 1.23; 4.NF.C.6)" % texto, ""]
    p = _dec_problema(texto)
    if p:
        return "\n".join(L + ["  TODAVIA NO: %s" % p[1], "", "RESULTADO: todavia_no"])
    if k == 0:
        return "\n".join(L + ["  %s es un entero (sin punto)." % e, "", "RESULTADO: %s" % e])
    n = _dec_en_pequenas(texto, k)
    uno, varios = _DEC_NOMBRE[k]
    ent = escribir_cifras([int(c) for c in reversed(e)])
    dec = escribir_cifras([int(c) for c in reversed(d)])
    L.append("  1. LAS CIFRAS EN SU SITIO: %d %s y %d %s (lo de detras del punto son %s)"
             % (ent, "entero" if ent == 1 else "enteros", dec, uno if dec == 1 else varios, varios))
    L.append("     una %s es 1/10 del entero (F.1: el uno partido en DIEZ partes iguales)" % uno)
    L.append("  2. COMO COSAS: cada entero son 10 %s, asi que %s son %d %s  (%s = %d x 0.1; NCETM 1.23)"
             % (varios, texto, n, varios, texto, n))
    L.append("  3. SUMANDO: %s = %d + %s = %d + %d/10" % (texto, ent, _dec_escribir(dec, k), ent, dec))
    sig = siguiente(decir(ent, saber), saber)
    L.append("  4. EN LA RECTA: entre %d y %s" % (ent, leer(sig, saber) if sig else "?"))
    if dec == 0:
        L.append("     cero decimas: es justo el %d" % ent)
    L += ["", "RESULTADO: %d %s" % (n, uno if n == 1 else varios)]
    return "\n".join(L)


# ---------------------------------------------------------------- 2.7 + 1.5

def _dec_columnas(na, nb, k, signo, saber):
    """Las columnas, con el punto: devuelve las lineas que lo cuentan.  Cada columna con un hecho pequeno."""
    ca, cb = cifras_de(na), cifras_de(nb)
    while len(ca) < len(cb):
        ca.append(0)
    while len(cb) < len(ca):
        cb.append(0)
    sitios = [_DEC_NOMBRE[x][1] for x in (3, 2, 1) if x <= k][-k:] if k else []
    sitios = list(reversed(sitios)) + ["unidades", "decenas", "centenas", "millares", "decenas de millar"]
    lineas, lleva = [], 0
    if signo == "+":
        for i, (x, y) in enumerate(zip(ca, cb)):
            s_ = aplicar("sumar", {"a": x, "b": y}, saber)["valor"]
            if lleva:
                s_ = aplicar("sumar", {"a": s_, "b": lleva}, saber)["valor"]
            c = cifras_de(s_)
            nuevo = escribir_cifras(c[1:])
            lineas.append("%s: %d + %d%s = %d -> escribo %d%s" % (sitios[i], x, y, " + %d" % lleva if lleva else "", s_,
                          c[0], ", llevo %d (%s)" % (nuevo, "diez %s hacen una unidad" % sitios[i] if i == k - 1 else
                                                     "diez hacen uno de la columna de al lado") if nuevo else ""))
            lleva = nuevo
        if lleva:
            lineas.append("lo que llevo (%d) va delante" % lleva)
    else:
        a = list(ca)
        for i, y in enumerate(cb):
            if a[i] != y and viene_despues(decir(y, saber), decir(a[i], saber), saber):
                j = i
                while True:
                    j = siguiente(decir(j, saber), saber) and leer(siguiente(decir(j, saber), saber), saber)
                    if a[j] != 0:
                        break
                a[j] = leer(anterior(decir(a[j], saber), saber), saber)
                m = j
                while True:
                    m = leer(anterior(decir(m, saber), saber), saber)
                    if m == i:
                        break
                    a[m] = 9
                a[i] = escribir_cifras([a[i], 1])
                lineas.append("%s: no hay bastantes: CAMBIO 1 de las %s por diez %s (alli quedan %d) -> %d %s"
                              % (sitios[i], sitios[j], sitios[i], a[j], a[i], sitios[i]))
            r_ = aplicar("restar", {"a": a[i], "b": y}, saber)["valor"]
            lineas.append("%s: %d - %d = %d" % (sitios[i], a[i], y, r_))
    return lineas


def decidir_cuenta_decimal(x, signo, y, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    p = _dec_problema(x, y)
    if p:
        return {"conclusion": p[0], "porque": p[1]}
    k = _dec_lugares(x, y)
    na, nb = _dec_en_pequenas(x, k), _dec_en_pequenas(y, k)
    if signo == "-" and viene_despues(decir(nb, saber), decir(na, saber), saber):
        return {"conclusion": "imposible", "porque": "se quita mas de lo que hay"}
    r = aplicar("sumar" if signo == "+" else "restar", {"a": na, "b": nb}, saber)
    if r["conclusion"] != "hecho":
        return {"conclusion": "todavia_no", "porque": r.get("porque") or "se sale de mi lista"}
    return {"conclusion": "hecho", "k": k, "na": na, "nb": nb, "n": r["valor"], "valor": _dec_escribir(r["valor"], k),
            "columnas": _dec_columnas(na, nb, k, signo, saber), "metodo": r["pieza"]["nombre"]}


def explicar_cuenta_decimal(x, signo, y, saber):
    r = decidir_cuenta_decimal(x, signo, y, saber)
    L = ["PREGUNTA (D.1): %s %s %s  (NCETM 1.23: con decimas sirven las columnas)" % (x, signo, y), ""]
    if r["conclusion"] != "hecho":
        etiqueta = {"imposible": "NO SE PUEDE"}.get(r["conclusion"], "TODAVIA NO")
        return "\n".join(L + ["  %s: %s" % (etiqueta, r["porque"]), "", "RESULTADO: %s" % r["conclusion"]])
    k = r["k"]
    varios = _DEC_NOMBRE[k][1]
    ex, dx = _dec_leer(_dec_escribir(r["na"], k) if "." in x or "," in x else x)
    ancho_e = max(len(_dec_leer(t)[0]) for t in (x, y, r["valor"]))
    def fila(t):
        e, d = _dec_leer(t)
        while len(d) < k:
            d += "0"
        return "%s.%s" % (e.rjust(ancho_e), d)
    L.append("  1. EN COLUMNAS, con el punto alineado:")
    L.append("          %s" % fila(x))
    L.append("        %s %s" % (signo, fila(y)))
    L.append("        --%s" % "".join("-" for _ in fila(x)))
    L.append("          %s" % fila(r["valor"]))
    for c in r["columnas"]:
        L.append("        %s" % c)
    L.append("  2. COMO COSAS (contando en %s): %s %s %s = %s = %s"
             % (varios, _dec_cuantas(r["na"], k), signo, _dec_cuantas(r["nb"], k), _dec_cuantas(r["n"], k), r["valor"]))
    L.append("     (%s)" % r["metodo"])
    L += ["", "RESULTADO: %s" % r["valor"]]
    return "\n".join(L)


# ---------------------------------------------------------------- comparar: 0.9 y 1.1

def decidir_comparar_decimales(x, y, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    p = _dec_problema(x, y)
    if p:
        return {"conclusion": p[0], "porque": p[1]}
    (ex, dx), (ey, dy) = _dec_leer(x), _dec_leer(y)
    vx, vy = escribir_cifras([int(c) for c in reversed(ex)]), escribir_cifras([int(c) for c in reversed(ey)])
    if vx != vy:
        mayor = viene_despues(decir(vx, saber), decir(vy, saber), saber)
        return {"conclusion": "hecho", "valor": ">" if mayor else "<",
                "porque": "los enteros deciden: %d contra %d" % (vx, vy)}
    while len(dx) < len(dy):
        dx += "0"
    while len(dy) < len(dx):
        dy += "0"
    for i, (a, b) in enumerate(zip(dx, dy)):
        if a != b:
            mayor = viene_despues(decir(int(a), saber), decir(int(b), saber), saber)
            return {"conclusion": "hecho", "valor": ">" if mayor else "<",
                    "porque": "los mismos enteros; la primera cifra distinta detras del punto es la de las %s: %s contra %s"
                              % (_DEC_NOMBRE[i + 1][1], a, b)}
    return {"conclusion": "hecho", "valor": "=", "porque": "las mismas cifras en todos los sitios"}


def explicar_comparar_decimales(x, y, saber):
    r = decidir_comparar_decimales(x, y, saber)
    L = ["PREGUNTA (D.1): cual es mayor, %s o %s?  (mirando las cifras, como en N.3)" % (x, y), ""]
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["  TODAVIA NO: %s" % r["porque"], "", "RESULTADO: %s" % r["conclusion"]])
    L.append("  %s" % r["porque"])
    L += ["", "RESULTADO: %s %s %s" % (x, r["valor"], y)]
    return "\n".join(L)


# ---------------------------------------------------------------- redondear: 2.7

def explicar_redondear_decimal(texto, saber):
    e, d = _dec_leer(texto)
    L = ["PREGUNTA (D.1): %s al entero mas cercano  (NCETM 1.23, punto 6)" % texto, ""]
    ent = escribir_cifras([int(c) for c in reversed(e)])
    decima = int(d[0])
    sube = decima == 5 or viene_despues(decir(decima, saber), "cinco", saber)
    arriba = leer(siguiente(decir(ent, saber), saber), saber)
    L.append("  %s esta entre %d y %d; la mitad del camino es %d.5" % (texto, ent, arriba, ent))
    L.append("  la cifra de las decimas es %d: %s" % (decima, "de cinco para arriba: SUBE a %d%s" % (
        arriba, " (justo en la mitad: por CONVENIO)" if decima == 5 and not d[1:].strip("0") else "")
        if sube else "menos de cinco: se QUEDA en %d" % ent))
    L += ["", "RESULTADO: %d" % (arriba if sube else ent)]
    return "\n".join(L)


# ---------------------------------------------------------------- de 0.1 en 0.1

def explicar_saltos_decimas(desde, hasta, saber):
    k = 1
    n = _dec_en_pequenas(desde or "0", k)
    fin = _dec_en_pequenas(hasta, k) if hasta else None
    serie, saltos = [], "cero"
    while saltos != "diez" or fin is not None:
        nuevo = leer(siguiente(decir(n, saber), saber), saber)
        if fin is not None and viene_despues(decir(nuevo, saber), decir(fin, saber), saber):
            break
        serie.append(_dec_escribir(nuevo, k))
        n = nuevo
        saltos = siguiente(saltos, saber)
        if fin is not None and nuevo == fin:
            break
    L = ["PREGUNTA (D.1): contar de 0.1 en 0.1 desde %s%s  (NCETM 1.23, punto 3)" % (desde or "0", " hasta %s" % hasta if hasta else ""),
         "  (cada salto es UNA decima; diez decimas hacen un entero: despues de 0.9 viene 1, no '0.10')", ""]
    L.append("  %s" % ", ".join(serie))
    L += ["", "RESULTADO: %s" % ", ".join(serie)]
    return "\n".join(L)


# ---------------------------------------------------------------- la puerta

def explicar_orden_decimal(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    t = _dec_limpio(texto)
    m = _ORDEN_DECIMAL.match(t)
    if m:
        return explicar_decimal(m.group(1).replace(",", "."), saber)
    m = _ORDEN_DEC_SALTOS.match(t)
    if m:
        return explicar_saltos_decimas(m.group(1) and m.group(1).replace(",", "."),
                                       m.group(2) and m.group(2).replace(",", "."), saber)
    m = _ORDEN_DEC_REDONDEAR.match(t)
    if m:
        x = m.group(1).replace(",", ".")
        p = _dec_problema(x)
        if p:
            return "PREGUNTA (D.1): redondear %s\n\n  TODAVIA NO: %s\n\nRESULTADO: todavia_no" % (x, p[1])
        return explicar_redondear_decimal(x, saber)
    m = _ORDEN_DEC_COMPARAR.match(t)
    if m:
        return explicar_comparar_decimales(m.group(1).replace(",", "."), m.group(2).replace(",", "."), saber)
    m = _ORDEN_DEC_CUENTA.match(t)
    if m:
        return explicar_cuenta_decimal(m.group(1).replace(",", "."), m.group(2), m.group(3).replace(",", "."), saber)
    return "NO ENTIENDO ESTO: se escribe asi:  decimal: 2.3    2.7 + 1.5    comparar: 0.9 y 1.1    redondear: 2.7"
