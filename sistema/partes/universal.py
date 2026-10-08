# -*- coding: utf-8 -*-
"""
Euclides - EL RESOLVEDOR UNIVERSAL, PRIMERA FASE: EL MODELO Y EL LECTOR SIMBOLICO (fase U.1 del plan U, 8 oct 2026).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

Plan U (diario/2026-10-08-PLAN-U-volverlo-universal.md): ante algo escrito con simbolos que NINGUN paso preparo, el
sistema lo LEE (un solo lector), lo pone en un MODELO (las cantidades que faltan, las relaciones entre ellas, lo que se
pide) y lo RESUELVE con lo que ya sabe, sin recetas de ninguna familia de problemas:

  1. CALCULAR DESPEJANDO: una relacion en la que falta UNA sola cantidad.  Si sale una vez, se DESHACE de fuera hacia
     dentro (trabajar hacia atras, Polya; es lo de E.5).  Si sale varias veces, se cuentan los TROZOS (la barra de
     NCETM 1.31: x = y y z = 2 x y -> 1 + 1 + 2 = 4 trozos de y) y se deshace.
  2. SUSTITUIR: si ninguna relacion tiene una sola cantidad, una que este dicha con las otras (x = y; o aislada
     deshaciendo: a + b = 1/2 -> a = 1/2 - b) se pone en las demas: quedan menos cantidades que faltan.
  3. COMPROBAR: al final, los numeros se ponen en TODAS las relaciones de partida (no en las transformadas).
Las cuentas las hace el NUMERO comun (numero.py), que a su vez se las pide a las piezas de siempre.  Con un
presupuesto de pasos (conocimiento/universal.kn): un humano no da cien vueltas.

El lector amplia el de letra.py (el orden de siempre y los parentesis) con: varias letras, varias relaciones con ';',
fracciones (1/2), decimales (4.5 o 4,5), negativos (-3, x = -2, 3 x (-2)), 2n = 2 x n.  La 'x' es POR entre dos
cosas y LETRA en los demas sitios.
"""

import re

_U_PREFIJO = re.compile(r"^resolver\s*:?\s*")
_U_TOKEN = re.compile(r"\d+\s*/\s*\d+(?![\d.,])|\d+(?:[.,]\d+)?|[a-z]|[()+\-:=;?_/]")
_U_FUERTES = ("x", ":")


class _UNoSale(Exception):
    """El resolvedor no llega: 'conclusion' dice como (todavia_no, ninguna, no_se_puede)."""
    def __init__(self, conclusion, porque):
        Exception.__init__(self, porque)
        self.conclusion = conclusion
        self.porque = porque


def _u_limpio(texto):
    t = texto.lower().strip().replace("−", "-").replace("×", " x ").replace("*", " x ").replace("÷", ":")
    t = t.replace("¿", "").rstrip(".").strip()
    return _U_PREFIJO.sub("", t).strip()


def es_orden_resolver(texto):
    return bool(re.match(r"^resolver(\s*:|\s)", texto.lower().strip()))


# ------------------------------------------------------------- 1. LEER: los simbolos, uno a uno

_U_DE = re.compile(r"(\d+\s*/\s*\d+|\d+[.,]\d+)\s+de\s+(?=[\d(a-z?_])")


def _u_tokens(t):
    t = _U_DE.sub(r"\1 x ", t)                         # 3/4 de 20 = 3/4 x 20 (F.1; 5.NF.B.4): 'de' es POR
    if re.search(r"[a-z]{2,}", t):
        return None                                      # hay palabras: eso es de U.3 (el lector de palabras)
    crudos = _U_TOKEN.findall(t)
    if "".join(crudos).replace(" ", "") != re.sub(r"\s+", "", t):
        return None                                      # hay algo que no es de una expresion
    fin_de_cosa = ("num", "letra", ")")
    principio_de_cosa = ("num", "letra", "(")
    clases = []
    for c in crudos:
        if c[0].isdigit():
            clases.append(("num", c))
        elif c in "?_":
            clases.append(("letra", "?"))
        elif c.isalpha():
            clases.append(("letra", c))                  # 'x' se decide abajo, mirando a los lados
        elif c == "/":
            clases.append(("op", ":"))
        elif c in "+-:":
            clases.append(("op", c))
        else:
            clases.append((c, c))
    out = []
    for i, tok in enumerate(clases):
        if tok == ("letra", "x") and out and out[-1][0] in fin_de_cosa and i + 1 < len(clases) \
                and clases[i + 1][0] in principio_de_cosa:
            tok = ("op", "x")                            # entre dos cosas: es POR
        if out and out[-1][0] in fin_de_cosa and tok[0] in principio_de_cosa:
            if (out[-1][0], tok[0]) in (("num", "letra"), ("num", "("), ("letra", "("), (")", "("), (")", "letra")):
                out.append(("op", "x"))                  # 2n = 2 x n;  2(a + 1) = 2 x (a + 1)
            else:
                return None                              # '3 4' o 'a b': no se sabe que es
        out.append(tok)
    return out


def _u_arbol(toks):
    """El arbol de una expresion, con el orden de siempre: primero x y :, luego + y -; el '-' de delante es negativo."""
    quedan = list(toks)

    def ver():
        return quedan[0] if quedan else (None, None)

    def atomo():
        if not quedan:
            raise ValueError("falta algo al final")
        t = quedan.pop(0)
        if t[0] == "num":
            return ("num", _nu_leer(t[1]))
        if t[0] == "letra":
            return ("letra", t[1])
        if t[0] == "(":
            e = suma()
            if not quedan or quedan.pop(0)[0] != ")":
                raise ValueError("falta cerrar un parentesis")
            return ("par", e)
        raise ValueError("no entiendo '%s' donde va un numero" % t[1])

    def unario():
        if ver() == ("op", "-"):
            quedan.pop(0)
            e = unario()
            return ("num", _nu_opuesto(e[1])) if e[0] == "num" else ("neg", e)
        return atomo()

    def producto():
        e = unario()
        while ver()[0] == "op" and ver()[1] in _U_FUERTES:
            op = quedan.pop(0)[1]
            e = ("op", op, e, unario())
        return e

    def suma():
        e = producto()
        while ver()[0] == "op" and ver()[1] in "+-":
            op = quedan.pop(0)[1]
            e = ("op", op, e, producto())
        return e

    e = suma()
    if quedan:
        raise ValueError("sobra algo al final")
    return e


def _u_leer(texto):
    """El MODELO: {'cantidades': las letras en el orden en que salen, 'relaciones': [(izq, der)], 'expresion': arbol
    (si no hay '=')}.  ValueError si no se deja leer."""
    t = _u_limpio(texto)
    toks = _u_tokens(t)
    if not toks:
        raise ValueError("no es una expresion escrita con numeros, letras y + - x : ( ) = ;")
    trozos, actual = [], []
    for tok in toks:
        if tok[0] == ";":
            trozos.append(actual)
            actual = []
        else:
            actual.append(tok)
    trozos.append(actual)
    trozos = [tr for tr in trozos if tr]
    if not trozos:
        raise ValueError("no hay nada que leer")
    modelo = {"cantidades": [], "relaciones": [], "expresion": None, "texto": t}
    for tr in trozos:
        iguales = [k for k, tok in enumerate(tr) if tok[0] == "="]
        if not iguales:
            if len(trozos) > 1:
                raise ValueError("con ';' cada trozo tiene que ser una relacion (con un =)")
            modelo["expresion"] = _u_arbol(tr)
        elif len(iguales) > 1:
            raise ValueError("una relacion lleva UN signo =")
        else:
            k = iguales[0]
            modelo["relaciones"].append((_u_arbol(tr[:k]), _u_arbol(tr[k + 1:])))
        for tok in tr:
            if tok[0] == "letra" and tok[1] not in modelo["cantidades"]:
                modelo["cantidades"].append(tok[1])
    if modelo["expresion"] is not None and modelo["cantidades"]:
        raise ValueError("una expresion con letras y sin '=' no se puede calcular")
    return modelo


def es_expresion_simbolica(texto):
    """Lo lee entero el lector simbolico, y hay algo que hacer: una cuenta (dos numeros o mas) o una relacion."""
    if es_orden_resolver(texto):
        return True
    try:
        m = _u_leer(texto)
    except (ValueError, _NuNoSale):
        return False
    if m["relaciones"]:
        return True
    return m["expresion"][0] in ("op", "par", "neg") and _u_hay_cuenta(m["expresion"])


def _u_la_puerta_no_llega(salida):
    """'no_entiendo' o 'todavia_no' si lo que contesto una puerta vieja es eso; si no, None."""
    if salida.startswith("NO ENTIENDO"):
        return "no_entiendo"
    lineas = salida.strip().splitlines()
    if lineas and lineas[-1].strip() == "RESULTADO: todavia_no":
        return "todavia_no"
    return None


def _u_le_toca_al_resolvedor(texto, vieja, saber):
    """LA RED DE SEGURIDAD (U.1, ampliada en U.2 tras la revision de U.1): una puerta vieja no llega ('no entiendo' o
    'todavia no') y el lector simbolico lo lee entero.  Si el resolvedor llega a una respuesta comprobada (hecho, o
    ninguna porque las relaciones se contradicen), contesta el.  Con 'todavia no', solo si hay una RELACION con letras: el 'todavia no' de una cuenta sin
    letras es respetar el ano (12 : 3 + 1, 2/3 x 3/4), no un problema de forma."""
    if not vieja or not es_expresion_simbolica(texto):
        return False
    if vieja == "todavia_no":
        try:
            m = _u_leer(texto)
        except (ValueError, _NuNoSale):
            return False
        if not m["relaciones"] or not m["cantidades"]:
            return False
    try:
        r = decidir_resolver(texto, saber)
    except Exception:
        return False
    if r["conclusion"] == "ninguna":             # ninguna porque se contradicen, si; probando en orden solo es ninguna
        return not r.get("probado")              # con numeros para contar (podria haberla con decimales): no basta
    return r["conclusion"] == "hecho"


def _u_hay_cuenta(e):
    if e[0] == "op":
        return True
    if e[0] in ("par", "neg"):
        return _u_hay_cuenta(e[1])
    return False


# ------------------------------------------------------------- el arbol: escribirlo, sus letras, sustituir

def _u_texto(e):
    if e[0] == "num":
        return _nu_texto(e[1])
    if e[0] == "letra":
        return e[1]
    if e[0] == "par":
        return "(%s)" % _u_texto(e[1])
    if e[0] == "neg":
        dentro = _u_texto(e[1])
        return "-%s" % (dentro if e[1][0] in ("letra", "par") else "(%s)" % dentro)
    izq, der = _u_texto(e[2]), _u_texto(e[3])
    if e[3][0] == "num" and _nu_texto(e[3][1]).startswith("-"):
        der = "(%s)" % der
    return "%s %s %s" % (izq, e[1], der)


def _u_letras(e):
    if e[0] == "letra":
        return [e[1]]
    if e[0] == "num":
        return []
    if e[0] in ("par", "neg"):
        return _u_letras(e[1])
    out = _u_letras(e[2])
    out.extend(_u_letras(e[3]))
    return out


def _u_letras_rel(rel):
    out = _u_letras(rel[0])
    out.extend(_u_letras(rel[1]))
    return out


def _u_distintas(lista):
    out = []
    for x in lista:
        if x not in out:
            out.append(x)
    return out


def _u_poner(e, letra, valor):
    """Pone 'valor' (un arbol) donde esta la letra.  Si no es una cosa sola, entre parentesis."""
    if e[0] == "letra":
        if e[1] != letra:
            return e
        return valor if valor[0] in ("num", "letra", "par") else ("par", valor)
    if e[0] == "num":
        return e
    if e[0] in ("par", "neg"):
        return (e[0], _u_poner(e[1], letra, valor))
    return ("op", e[1], _u_poner(e[2], letra, valor), _u_poner(e[3], letra, valor))


def _u_poner_todas(e, valores):
    for letra, v in valores.items():
        e = _u_poner(e, letra, ("num", v))
    return e


def _u_rel_texto(rel):
    return "%s = %s" % (_u_texto(rel[0]), _u_texto(rel[1]))


def _u_nombre(letra):
    return "el hueco" if letra == "?" else letra


# ------------------------------------------------------------- calcular (con el numero comun)

def _u_valor(e, saber, pasos):
    """Calcula un arbol sin letras, en el ORDEN DE SIEMPRE (el arbol ya lo tiene)."""
    if e[0] == "num":
        return e[1]
    if e[0] == "par":
        return _u_valor(e[1], saber, pasos)
    if e[0] == "neg":
        return _nu_opuesto(_u_valor(e[1], saber, pasos))
    if e[0] == "letra":
        raise _UNoSale("todavia_no", "falta saber cuanto vale %s" % _u_nombre(e[1]))
    a = _u_valor(e[2], saber, pasos)
    b = _u_valor(e[3], saber, pasos)
    return _u_cuenta(e[1], a, b, saber, pasos)


def _u_cuenta(op, a, b, saber, pasos):
    try:
        return _nu_cuenta(op, a, b, saber, pasos)
    except _NuNoSale as ex:
        con = "no_se_puede" if "entre cero" in str(ex) else "todavia_no"
        raise _UNoSale(con, str(ex))


# ------------------------------------------------------------- operador 1: CALCULAR DESPEJANDO

_U_CONTRARIA = {"+": "-", "-": "+", "x": ":", ":": "x"}


def _u_deshacer(e, objetivo, saber, pasos):
    """La letra esta UNA vez dentro de e, y e tiene que valer 'objetivo': se deshace de fuera hacia dentro (E.5)."""
    if e[0] == "letra":
        return objetivo
    if e[0] == "par":
        return _u_deshacer(e[1], objetivo, saber, pasos)
    if e[0] == "neg":
        pasos.append("deshago el '-' de delante: %s = %s" % (_u_texto(e[1]), _nu_texto(_nu_opuesto(objetivo))))
        return _u_deshacer(e[1], _nu_opuesto(objetivo), saber, pasos)
    op, izq, der = e[1], e[2], e[3]
    if _u_letras(izq):
        otro = _u_valor(der, saber, pasos)
        if op == "x" and _nu_es_cero(otro):
            _u_por_cero(objetivo, izq)
        inv = _U_CONTRARIA[op]
        pasos.append("deshago '%s %s': %s = %s %s %s" % (op, _nu_parentesis(otro), _u_texto(izq),
                                                         _nu_parentesis(objetivo), inv, _nu_parentesis(otro)))
        return _u_deshacer(izq, _u_cuenta(inv, objetivo, otro, saber, pasos), saber, pasos)
    otro = _u_valor(izq, saber, pasos)
    if op == "x" and _nu_es_cero(otro):
        _u_por_cero(objetivo, der)
    if op in ("+", "x"):                                 # conmutativas: como si estuviera a la izquierda
        inv = _U_CONTRARIA[op]
        pasos.append("deshago '%s %s': %s = %s %s %s" % (_nu_parentesis(otro), op, _u_texto(der),
                                                         _nu_parentesis(objetivo), inv, _nu_parentesis(otro)))
        nuevo = _u_cuenta(inv, objetivo, otro, saber, pasos)
    else:                                                # otro - der = objetivo  ->  der = otro - objetivo
        pasos.append("%s %s %s = %s, asi que %s = %s %s %s" % (
            _nu_parentesis(otro), op, _u_texto(der), _nu_parentesis(objetivo), _u_texto(der),
            _nu_parentesis(otro), op, _nu_parentesis(objetivo)))
        if op == ":" and _nu_es_cero(objetivo):
            raise _UNoSale("ninguna", "%s : algo nunca da 0 (salvo que el de delante sea 0)" % _nu_texto(otro))
        nuevo = _u_cuenta(op, otro, objetivo, saber, pasos)
    return _u_deshacer(der, nuevo, saber, pasos)


def _u_por_cero(objetivo, e):
    """0 x algo es siempre 0 (M.2): si tiene que dar 0, vale cualquiera; si no, ninguno."""
    if _nu_es_cero(objetivo):
        raise _UNoSale("todavia_no", "0 x %s es 0 siempre: %s puede valer CUALQUIER numero (infinitas; U.2)"
                       % (_u_texto(e), _u_texto(e)))
    raise _UNoSale("ninguna", "0 x %s es 0 siempre, nunca %s: ningun numero cumple" % (_u_texto(e), _nu_texto(objetivo)))


class _UNoLineal(Exception):
    pass


def _u_lineal(e, letra, saber, pasos):
    """Los TROZOS: e = (coef) trozos de la letra + (suelto).  Devuelve (coef, suelto) como numeros.
    Solo si la letra no se multiplica por si misma ni divide (si no, _UNoLineal)."""
    if e[0] == "letra":
        return ("+", 1, 1, "entero"), _NU_CERO
    if not _u_letras(e):
        return _NU_CERO, _u_valor(e, saber, pasos)
    if e[0] == "par":
        return _u_lineal(e[1], letra, saber, pasos)
    if e[0] == "neg":
        c, k = _u_lineal(e[1], letra, saber, pasos)
        return _nu_opuesto(c), _nu_opuesto(k)
    op, izq, der = e[1], e[2], e[3]
    if op in "+-":
        c1, k1 = _u_lineal(izq, letra, saber, pasos)
        c2, k2 = _u_lineal(der, letra, saber, pasos)
        return _u_cuenta(op, c1, c2, saber, pasos), _u_cuenta(op, k1, k2, saber, pasos)
    if op == "x" and not _u_letras(izq):
        v = _u_valor(izq, saber, pasos)
        c, k = _u_lineal(der, letra, saber, pasos)
        return _u_cuenta("x", v, c, saber, pasos), _u_cuenta("x", v, k, saber, pasos)
    if not _u_letras(der):
        v = _u_valor(der, saber, pasos)
        c, k = _u_lineal(izq, letra, saber, pasos)
        return _u_cuenta(op, c, v, saber, pasos), _u_cuenta(op, k, v, saber, pasos)
    raise _UNoLineal("%s se multiplica o se divide por si misma" % _u_nombre(letra))


def _u_despejar(rel, letra, saber, pasos):
    """Operador 1.  La unica letra que falta en la relacion: deshaciendo (si sale una vez) o contando trozos."""
    izq, der = rel
    veces = len(_u_letras_rel(rel))
    if veces == 1:
        con, sin = (izq, der) if _u_letras(izq) else (der, izq)
        objetivo = _u_valor(sin, saber, pasos)
        if con[0] == "letra":
            return objetivo
        pasos.append("deshago de fuera hacia dentro (trabajar hacia atras): %s = %s"
                     % (_u_texto(con), _nu_texto(objetivo)))
        return _u_deshacer(con, objetivo, saber, pasos)
    pasos.append("%s sale %d veces: cuento los TROZOS de %s (la barra)" % (_u_nombre(letra), veces, _u_nombre(letra)))
    try:
        c1, k1 = _u_lineal(izq, letra, saber, [])
        c2, k2 = _u_lineal(der, letra, saber, [])
    except _UNoLineal as ex:
        raise _UNoSale("todavia_no", "%s: todavia no (eso es probar en orden, U.2)" % ex)
    for lado, c_, k_ in ((izq, c1, k1), (der, c2, k2)):
        pasos.append("%s  es  %s" % (_u_texto(lado), _u_trozos_texto(c_, k_, letra)))
    sub = []
    c = _u_cuenta("-", c1, c2, saber, sub) if not _nu_es_cero(c2) else c1
    if c[0] == "-":                              # los trozos se QUITAN: son lo que va de lo de un lado a lo del otro
        c = _nu_opuesto(c)
        k = _u_cuenta("-", k1, k2, saber, sub) if not _nu_es_cero(k2) else k1
        nota = "los trozos se QUITAN: son lo que va de %s a %s" % (_nu_texto(k2), _nu_texto(k1))
    else:
        k = _u_cuenta("-", k2, k1, saber, sub) if not _nu_es_cero(k1) else k2
        nota = "los trozos a un lado y lo suelto al otro"
    if sub:
        pasos.append(nota + ":")
        pasos.extend(sub)
    if _nu_es_cero(c):
        if _nu_es_cero(k):
            raise _UNoSale("todavia_no", "los trozos de %s se van: vale CUALQUIER numero (infinitas; U.2)"
                           % _u_nombre(letra))
        raise _UNoSale("ninguna", "los trozos de %s se van y queda %s = 0: ningun numero cumple"
                       % (_u_nombre(letra), _nu_texto(k)))
    pasos.append("junto: %s trozos de %s = %s" % (_nu_texto(c), _u_nombre(letra), _nu_texto(k)))
    if _nu_iguales(c, ("+", 1, 1, "entero"), saber):
        return k
    pasos.append("un trozo: %s : %s" % (_nu_parentesis(k), _nu_parentesis(c)))
    return _u_cuenta(":", k, c, saber, pasos)


# ------------------------------------------------------------- operador 2: SUSTITUIR

def _u_aislar(e, objetivo, letra):
    """Como _u_deshacer, pero con letras: e (con la letra UNA vez) = objetivo (un arbol) -> letra = arbol."""
    def par(x):
        return x if x[0] in ("num", "letra", "par") else ("par", x)
    while e[0] != "letra":
        if e[0] == "par":
            e = e[1]
            continue
        if e[0] == "neg":
            e, objetivo = e[1], ("neg", par(objetivo))
            continue
        op, izq, der = e[1], e[2], e[3]
        if letra in _u_letras(izq):
            e, objetivo = izq, ("op", _U_CONTRARIA[op], par(objetivo), par(der))
        elif op in ("+", "x"):
            e, objetivo = der, ("op", _U_CONTRARIA[op], par(objetivo), par(izq))
        else:
            e, objetivo = der, ("op", op, par(izq), par(objetivo))
    return objetivo


def _u_elegir_para_sustituir(rels):
    """La relacion y la letra: primero una letra SOLA en un lado (x = y); si no, una que salga UNA vez."""
    orden = sorted(range(len(rels)), key=lambda i: len(_u_distintas(_u_letras_rel(rels[i]))))
    for i in orden:
        izq, der = rels[i]
        for lado, otro in ((izq, der), (der, izq)):
            if lado[0] == "letra" and lado[1] not in _u_letras(otro):
                return i, lado[1], otro, "sola"
    for i in orden:
        todas = _u_letras_rel(rels[i])
        for letra in _u_distintas(todas):
            if todas.count(letra) == 1:
                izq, der = rels[i]
                con, sin = (izq, der) if letra in _u_letras(izq) else (der, izq)
                return i, letra, _u_aislar(con, sin, letra), "aislada"
    return None


# ------------------------------------------------------------- el resolvedor: el bucle con presupuesto

def _u_trozos_texto(c, k, letra):
    """'2 trozos de b y 1/2 suelto';  con trozos en negativo: '1/2 quitando 2 trozos de b'."""
    n = _u_nombre(letra)
    if _nu_es_cero(c):
        return "%s suelto" % _nu_texto(k)
    trozos = "%s %s de %s" % (_nu_texto(c).lstrip("-"), "trozo" if _nu_texto(c).lstrip("-") == "1" else "trozos", n)
    if _nu_es_cero(k):
        return trozos if c[0] == "+" else "0 quitando %s" % trozos
    if c[0] == "+":
        return "%s y %s suelto" % (trozos, _nu_texto(k))
    return "%s quitando %s" % (_nu_texto(k), trozos)


def _u_presupuesto(saber):
    t = str((saber.get("universal") or {}).get("presupuesto_de_pasos", "20"))
    return int(t) if t.isdigit() else 20


def decidir_resolver(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = {"texto": texto, "etapas": []}
    try:
        modelo = _u_leer(texto)
    except _NuNoSale as ex:
        r.update(conclusion="todavia_no", porque=str(ex))
        return r
    except (ValueError, IndexError) as ex:
        r.update(conclusion="no_entiendo", porque=str(ex))
        return r
    r["modelo"] = modelo
    try:
        if modelo["expresion"] is not None:
            pasos = []
            v = _u_valor(modelo["expresion"], saber, pasos)
            r["etapas"].append(("CALCULO en el orden de siempre (primero x y :, luego + y -)", pasos))
            r.update(conclusion="hecho", valor=v, respuesta=_nu_texto(v))
            _u_tambien_decimal(r, v, modelo, saber)
            return r
        valores = _u_buscar(modelo, saber, r)
    except _UNoSale as ex:
        r.update(conclusion=ex.conclusion, porque=ex.porque)
        return r
    except KeyError as ex:                       # un numero sin nombre (pasa del techo)
        r.update(conclusion="todavia_no", porque="un numero se pasa de mi techo (%s): %s" % (techo(saber), ex))
        return r
    if valores is None:                          # relaciones sin letras: verdad o no
        return r
    if r.get("probado"):                         # probar en orden (U.2): una, varias o ninguna
        return _u_probado(r, valores, modelo, saber)
    r["valores"] = valores
    _u_comprobar(modelo, valores, saber, r)
    if r["comprobacion_ok"]:
        r["conclusion"] = "hecho"
        r["respuesta"] = _u_escribir_valores(valores, modelo)
    else:
        r.update(conclusion="no_cuadra", porque="al poner los numeros en las relaciones de partida no cuadra")
    return r


def _u_escribir_valores(valores, modelo):
    return ", ".join("%s = %s" % (_u_nombre(l), _nu_texto(valores[l])) for l in modelo["cantidades"])


def _u_probado(r, soluciones, modelo, saber):
    """Las soluciones de probar en orden (cada una ya comprobada en TODAS las relaciones de partida)."""
    lineas, ok = [], True
    for v in soluciones:
        sub = {}
        _u_comprobar(modelo, v, saber, sub)
        lineas.extend(sub["comprobacion"])
        ok = ok and sub["comprobacion_ok"]
    r["comprobacion"] = lineas
    r["comprobacion_ok"] = ok
    r["cuantas"] = "ninguna" if not soluciones else ("una" if not soluciones[1:] else "varias")
    r["nota"] = "con numeros para contar, desde el 0"
    if viene_despues(decir(len(modelo["cantidades"]), saber), decir(len(modelo["relaciones"]), saber), saber):
        r["nota"] = "%s; con decimales o fracciones habria infinitas (falta una relacion que las pare)" % r["nota"]
    if not ok:
        r.update(conclusion="no_cuadra", porque="al poner los numeros en las relaciones de partida no cuadra")
    elif not soluciones:
        r.update(conclusion="ninguna", porque="probe en orden y ninguna cumple (%s)" % r["nota"])
    else:
        r.update(conclusion="hecho", respuesta="; ".join(_u_escribir_valores(v, modelo) for v in soluciones))
    return r


def _u_tambien_decimal(r, v, modelo, saber):
    """Si en el enunciado habia decimales y la respuesta es una fraccion, se dice tambien en decimal si sale justo."""
    if v[3] == "fraccion" and v[2] != 1 and re.search(r"\d[.,]\d", modelo["texto"]):
        d = _nu_en_decimas(v, saber, [])
        if d is not None:
            r["tambien"] = "%s = %s" % (_nu_texto(v), _nu_texto(d))


def _u_buscar(modelo, saber, r):
    """Los operadores, por turnos, hasta saberlo todo (o hasta agotar el presupuesto)."""
    rels = list(modelo["relaciones"])
    if not modelo["cantidades"]:                 # sin letras: es una igualdad (E.0): verdad o no
        pasos, ok = [], True
        for izq, der in rels:
            vi, vd = _u_valor(izq, saber, pasos), _u_valor(der, saber, pasos)
            ok = ok and _nu_iguales(vi, vd, saber)
        r["etapas"].append(("CALCULO cada lado", pasos))
        r.update(conclusion="hecho", respuesta="VERDADERO" if ok else "FALSO", verdad=ok)
        return None
    soluciones = _bu_resolver(rels, saber, r["etapas"], modelo["relaciones"])     # U.2: buscar con control
    probado = any(t.startswith("PRUEBO EN ORDEN") for t, _ in r["etapas"])
    if not probado:
        faltan = [l for l in modelo["cantidades"] if l not in soluciones[0]]
        if faltan:
            raise _UNoSale("todavia_no", "faltan relaciones: %s puede valer cualquier cosa (infinitas)"
                           % ", ".join(_u_nombre(l) for l in faltan))
        return soluciones[0]
    r["probado"] = True
    r["soluciones"] = soluciones
    return soluciones


# ------------------------------------------------------------- 4. COMPROBAR en las relaciones de partida

def _u_comprobar(modelo, valores, saber, r):
    lineas, ok = [], True
    for rel in modelo["relaciones"]:
        pasos = []
        try:
            izq, der = _u_poner_todas(rel[0], valores), _u_poner_todas(rel[1], valores)
            vi, vd = _u_valor(izq, saber, pasos), _u_valor(der, saber, pasos)
            bien = _nu_iguales(vi, vd, saber)
            lineas.append("%s  ->  %s = %s  ->  %s = %s ... %s" % (_u_rel_texto(rel), _u_texto(izq), _u_texto(der),
                                                                  _nu_texto(vi), _nu_texto(vd), "SI" if bien else "NO"))
        except _UNoSale as ex:
            bien = False
            lineas.append("%s  ->  no lo puedo calcular (%s)" % (_u_rel_texto(rel), ex.porque))
        ok = ok and bien
    r["comprobacion"] = lineas
    r["comprobacion_ok"] = ok


# ------------------------------------------------------------- explicar

def explicar_resolver(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_resolver(texto, saber)
    if r["conclusion"] == "no_entiendo":
        return ("NO ENTIENDO ESTO: %s\n   se escribe asi:  resolver: a + b = 1/2; a - b = 1/4     resolver: 3 x n = 4.5"
                "     1/2 + 0.25     -3 + 2 x 4" % r.get("porque", ""))
    L = ["PREGUNTA (U.1-U.2, el resolvedor): %s" % _u_limpio(texto), ""]
    m = r.get("modelo")
    if m:
        L.append("  EL MODELO:")
        if m["expresion"] is not None:
            L.append("     una cuenta para calcular: %s" % _u_texto(m["expresion"]))
        else:
            L.append("     lo que falta: %s" % (", ".join(_u_nombre(l) for l in m["cantidades"]) or "nada (es una igualdad)"))
            for k, rel in enumerate(m["relaciones"]):
                L.append("     relacion %d: %s" % (_u_siguiente(k, saber), _u_rel_texto(rel)))
            L.append("     se pide: %s" % (", ".join(_u_nombre(l) for l in m["cantidades"]) or "si es verdad"))
        L.append("")
    for k, (titulo, pasos) in enumerate(r["etapas"]):
        L.append("  %d. %s" % (_u_siguiente(k, saber), titulo))
        for p in pasos:
            L.append("        %s" % p)
    if r.get("comprobacion"):
        L.append("")
        L.append("  COMPRUEBO en las relaciones de PARTIDA:")
        for c in r["comprobacion"]:
            L.append("        %s" % c)
    if r.get("tambien"):
        L.append("")
        L.append("  en decimal: %s" % r["tambien"])
    if r.get("cuantas"):
        L.append("")
        L.append("  CUANTAS: %s (%s)" % (r["cuantas"].upper(), r["nota"]))
    L.append("")
    if r["conclusion"] == "hecho":
        L.append("RESULTADO: %s" % r["respuesta"])
    else:
        etiqueta = {"ninguna": "NINGUNA", "no_se_puede": "NO SE PUEDE", "no_cuadra": "NO CUADRA"}.get(
            r["conclusion"], "TODAVIA NO")
        L.append("  %s: %s" % (etiqueta, r.get("porque", "")))
        L.append("")
        L.append("RESULTADO: %s" % r["conclusion"])
    return "\n".join(L)


def explicar_orden_resolver(texto, saber=None):
    return explicar_resolver(texto, saber)


def _u_siguiente(k, saber):
    """k + 1, recitando (el siguiente en la lista): para numerar los pasos."""
    return leer(siguiente(decir(k, saber), saber), saber)
