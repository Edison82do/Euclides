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

_DEC_MAX = 3                       # D.1: decimas;  D.2: centesimas y milesimas (NCETM 1.24).
_DEC_NOMBRE = {1: ("decima", "decimas"), 2: ("centesima", "centesimas"), 3: ("milesima", "milesimas")}
_DEC_NUM = r"\d+(?:[.,]\d+)?"
_ORDEN_DECIMAL = re.compile(r"^decimal:?\s*(\d+[.,]\d+|\d+)$")
_ORDEN_DEC_CUENTA = re.compile(r"^(?:calcular:?\s*)?(" + _DEC_NUM + r")\s*([+\-])\s*(" + _DEC_NUM + r")$")
_ORDEN_DEC_COMPARAR = re.compile(r"^comparar:?\s*(" + _DEC_NUM + r")\s*(?:y|con|\?)\s*(" + _DEC_NUM + r")$")
_ORDEN_DEC_REDONDEAR = re.compile(r"^redondear:?\s*(\d+[.,]\d+)(?:\s+(?:al|a la)\s+(entero|decima|centesima))?$")
_ORDEN_DEC_SALTOS = re.compile(r"^de\s+(0[.,]0?0?1)\s+en\s+(0[.,]0?0?1)(?:\s+desde\s+(" + _DEC_NUM + r"))?(?:\s+hasta\s+(" + _DEC_NUM + r"))?$")


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
        return "todavia_no", ("con mas de tres cifras detras del punto todavia no: llego a las milesimas "
                              "(NCETM 1.24); las diezmilesimas son de mas adelante")
    return None


# ---------------------------------------------------------------- decimal: 2.3

def explicar_decimal(texto, saber):
    e, d = _dec_leer(texto)
    k = len(d)
    L = ["PREGUNTA (D.1/D.2): que es %s?  (NCETM 1.23, 1.24; 4.NF.C.6)" % texto, ""]
    p = _dec_problema(texto)
    if p:
        return "\n".join(L + ["  TODAVIA NO: %s" % p[1], "", "RESULTADO: todavia_no"])
    if k == 0:
        return "\n".join(L + ["  %s es un entero (sin punto)." % e, "", "RESULTADO: %s" % e])
    n = _dec_en_pequenas(texto, k)
    uno, varios = _DEC_NOMBRE[k]
    ent = escribir_cifras([int(c) for c in reversed(e)])
    partes = ["%d %s" % (ent, "entero" if ent == 1 else "enteros")]
    sumandos = ["%d" % ent]
    for i, c in enumerate(d):
        partes.append("%s %s" % (c, _DEC_NOMBRE[i + 1][0] if c == "1" else _DEC_NOMBRE[i + 1][1]))
        if c != "0":
            ceros = "".join("0" for _ in range(i))
            sumandos.append("0.%s%s" % (ceros, c))
    L.append("  1. LAS CIFRAS EN SU SITIO: %s" % ", ".join(partes))
    L.append("     una decima es 1/10 del entero; una CENTESIMA es una decima partida en diez (1/100);"
             " una MILESIMA, una centesima partida en diez (1/1000)" if k > 1 else
             "     una decima es 1/10 del entero (F.1: el uno partido en DIEZ partes iguales)")
    L.append("  2. COMO COSAS: %s son %s  (%s = %d x 0.%s1)" % (texto, _dec_cuantas(n, k), texto, n,
                                                              "".join("0" for _ in d[1:])))
    L.append("  3. SUMANDO: %s = %s" % (texto, " + ".join(sumandos)))
    sig = siguiente(decir(ent, saber), saber)
    L.append("  4. EN LA RECTA: entre %d y %s" % (ent, leer(sig, saber) if sig else "?"))
    L += ["", "RESULTADO: %s" % _dec_cuantas(n, k)]
    return "\n".join(L)


# ---------------------------------------------------------------- 2.7 + 1.5

def _dec_columnas(na, nb, k, signo, saber):
    """Las columnas, con el punto: devuelve las lineas que lo cuentan.  Cada columna con un hecho pequeno."""
    ca, cb = cifras_de(na), cifras_de(nb)
    while len(ca) < len(cb):
        ca.append(0)
    while len(cb) < len(ca):
        cb.append(0)
    sitios = [_DEC_NOMBRE[x][1] for x in range(k, 0, -1)]           # de derecha a izquierda: la mas pequena primero
    sitios.extend(["unidades", "decenas", "centenas", "millares", "decenas de millar", "centenas de millar",
                   "millones", "decenas de millon"])
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
                medio = leer(siguiente(decir(i, saber), saber), saber) != j
                lineas.append("%s: no hay bastantes: CAMBIO 1 de las %s por diez %s (alli quedan %d%s) -> %d %s"
                              % (sitios[i], sitios[j], sitios[i], a[j],
                                 "; las columnas de en medio, que estaban a 0, se quedan en 9" if medio else "",
                                 a[i], sitios[i]))
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
    if decir(na, saber) is None or decir(nb, saber) is None:
        return {"conclusion": "todavia_no", "porque": "contado en %s se sale de mi lista (%s)"
                % (_DEC_NOMBRE[k][1], techo(saber))}
    if signo == "-" and viene_despues(decir(nb, saber), decir(na, saber), saber):
        return {"conclusion": "imposible", "porque": "se quita mas de lo que hay"}
    r = aplicar("sumar" if signo == "+" else "restar", {"a": na, "b": nb}, saber)
    if r["conclusion"] != "hecho":
        return {"conclusion": "todavia_no", "porque": r.get("porque") or "se sale de mi lista"}
    return {"conclusion": "hecho", "k": k, "na": na, "nb": nb, "n": r["valor"], "valor": _dec_escribir(r["valor"], k),
            "columnas": _dec_columnas(na, nb, k, signo, saber), "metodo": r["pieza"]["nombre"]}


def explicar_cuenta_decimal(x, signo, y, saber):
    r = decidir_cuenta_decimal(x, signo, y, saber)
    L = ["PREGUNTA (D.1/D.2): %s %s %s  (NCETM 1.23, 1.24: sirven las columnas)" % (x, signo, y), ""]
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
    relleno = len(dx) != len(dy)
    while len(dx) < len(dy):
        dx += "0"
    while len(dy) < len(dx):
        dy += "0"
    nota = ("se escriben con las mismas cifras detras del punto (un cero al final no cambia nada): %s.%s y %s.%s; "
            % (ex, dx, ey, dy)) if relleno else ""
    for i, (a, b) in enumerate(zip(dx, dy)):
        if a != b:
            mayor = viene_despues(decir(int(a), saber), decir(int(b), saber), saber)
            return {"conclusion": "hecho", "valor": ">" if mayor else "<",
                    "porque": "%slos mismos enteros; la primera cifra distinta detras del punto es la de las %s: %s contra %s"
                              % (nota, _DEC_NOMBRE[i + 1][1], a, b)}
    return {"conclusion": "hecho", "valor": "=", "porque": "%slas mismas cifras en todos los sitios" % nota}


def explicar_comparar_decimales(x, y, saber):
    r = decidir_comparar_decimales(x, y, saber)
    L = ["PREGUNTA (D.1/D.2): cual es mayor, %s o %s?  (4.NF.C.7: mirando las cifras, desde el punto)" % (x, y), ""]
    if r["conclusion"] != "hecho":
        return "\n".join(L + ["  TODAVIA NO: %s" % r["porque"], "", "RESULTADO: %s" % r["conclusion"]])
    L.append("  %s" % r["porque"])
    L += ["", "RESULTADO: %s %s %s" % (x, r["valor"], y)]
    return "\n".join(L)


# ---------------------------------------------------------------- redondear: 2.7

def explicar_redondear_decimal(texto, saber, a="entero"):
    """NCETM 1.24, punto 7: a la DECIMA mirando la cifra de las centesimas; al ENTERO mirando la de las
    decimas.  (Se cuenta en la unidad pequena: subir uno es contar uno mas.)"""
    e, d = _dec_leer(texto)
    k = len(d)
    lugar = {"entero": 0, "decima": 1, "centesima": 2}[a]
    nombre = {0: "entero", 1: "decima", 2: "centesima"}[lugar]
    L = ["PREGUNTA (D.1/D.2): %s %s  (NCETM 1.23, 1.24)" % (texto, "al entero mas cercano" if lugar == 0 else
                                                          "a la %s mas cercana" % nombre), ""]
    if lugar >= k:
        return "\n".join(L + ["  ya esta escrito %s: no hay nada que redondear" % ("con enteros" if not lugar else "en %s" % _DEC_NOMBRE[lugar][1]),
                              "", "RESULTADO: %s" % texto])
    corto = "%s.%s" % (e, d[:lugar]) if lugar else e
    base = _dec_en_pequenas(corto, lugar)                        # lo que se queda (en la unidad del sitio)
    cifra = int(d[lugar])
    sube = cifra == 5 or viene_despues(decir(cifra, saber), "cinco", saber)
    arriba = leer(siguiente(decir(base, saber), saber), saber)
    abajo_t, arriba_t = _dec_escribir(base, lugar), _dec_escribir(arriba, lugar)
    mirar = _DEC_NOMBRE[lugar + 1][1]
    L.append("  %s esta entre %s y %s" % (texto, abajo_t, arriba_t))
    L.append("  la cifra de las %s es %d: %s" % (mirar, cifra, "de cinco para arriba: SUBE a %s" % arriba_t
             if sube else "menos de cinco: se QUEDA en %s" % abajo_t))
    L += ["", "RESULTADO: %s" % (arriba_t if sube else abajo_t)]
    return "\n".join(L)


# ---------------------------------------------------------------- de 0.1 en 0.1

def explicar_saltos_decimas(desde, hasta, saber, de="0.1"):
    k = len(_dec_leer(de)[1])
    uno = _DEC_NOMBRE[k][0]
    n = _dec_en_pequenas(desde or "0", k)
    fin = _dec_en_pequenas(hasta, k) if hasta else None
    serie, saltos = [], "cero"
    while saltos != "diez" or fin is not None:
        nuevo = leer(siguiente(decir(n, saber), saber), saber)
        if nuevo is None or (fin is not None and viene_despues(decir(nuevo, saber), decir(fin, saber), saber)):
            break
        serie.append(_dec_escribir(nuevo, k))
        n = nuevo
        saltos = siguiente(saltos, saber)
        if fin is not None and nuevo == fin:
            break
    L = ["PREGUNTA (D.1/D.2): contar de %s en %s desde %s%s  (NCETM 1.23, 1.24)" % (de, de, desde or "0",
                                                                                  " hasta %s" % hasta if hasta else ""),
         "  (cada salto es UNA %s; diez hacen una de la columna de al lado: no se escribe '0.10')" % uno, ""]
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
    if m and m.group(1) == m.group(2):
        return explicar_saltos_decimas(m.group(3) and m.group(3).replace(",", "."),
                                       m.group(4) and m.group(4).replace(",", "."), saber, m.group(1).replace(",", "."))
    m = _ORDEN_DEC_REDONDEAR.match(t)
    if m:
        x = m.group(1).replace(",", ".")
        p = _dec_problema(x)
        if p:
            return "PREGUNTA (D.1): redondear %s\n\n  TODAVIA NO: %s\n\nRESULTADO: todavia_no" % (x, p[1])
        return explicar_redondear_decimal(x, saber, m.group(2) or "entero")
    m = _ORDEN_DEC_COMPARAR.match(t)
    if m:
        return explicar_comparar_decimales(m.group(1).replace(",", "."), m.group(2).replace(",", "."), saber)
    m = _ORDEN_DEC_CUENTA.match(t)
    if m:
        return explicar_cuenta_decimal(m.group(1).replace(",", "."), m.group(2), m.group(3).replace(",", "."), saber)
    return "NO ENTIENDO ESTO: se escribe asi:  decimal: 2.3    2.7 + 1.5    comparar: 0.9 y 1.1    redondear: 2.7"
