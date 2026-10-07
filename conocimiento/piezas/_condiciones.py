# -*- coding: utf-8 -*-
"""
LAS CONDICIONES DE APLICACION, escritas UNA vez y usadas por todas las piezas.

Cada una recibe (s, u): la SITUACION y lo que se puede usar (el mecanismo: u.viene_despues,
u.levantar_dedos, ...).  Devuelve cierto o falso.  Ninguna hace cuentas de Python: comparan,
miran que hay en la situacion, o preguntan al mecanismo.


DE_APLICACION: las que, si fallan, no dicen "esto no es lo mio" sino "esto es lo mio, pero es
IMPOSIBLE" (quitar mas de lo que hay).  Entonces el problema no tiene solucion, y se dice.
"""


# ---- usar la equivalencia (paso M.12; NCETM 2.18)
def _eq_sin_ceros_acaba_en_5(n, u):
    c = u.cifras_de(n)
    while len(c) > 1 and c[0] == 0:
        c = c[1:]
    return c[0] == 5


def _eq_es_par(n, u):
    return n != 0 and u.cifras_de(n)[0] in (0, 2, 4, 6, 8)


def _eq_pasa_de_doce(n, u):
    """No es un factor de las tablas (hasta el doce): ahi manda la tabla."""
    p = u.decir(n)
    return p is None or u.viene_despues(p, "doce")


def _eq_doblar_y_partir(s, u):
    a, b = s.get("a"), s.get("b")
    if not isinstance(a, int) or not isinstance(b, int) or 0 in (a, b):
        return False
    if not (_eq_pasa_de_doce(a, u) or _eq_pasa_de_doce(b, u)):
        return False
    return any(_eq_sin_ceros_acaba_en_5(f, u) and _eq_es_par(g, u) for f, g in ((a, b), (b, a)))


def _eq_escalar_division(s, u):
    t, d = s.get("total"), s.get("divisor")
    if not isinstance(t, int) or not isinstance(d, int) or t == 0 or d in (0, 1, 10, 100):
        return False
    if len(u.cifras_de(d)) == 1 and len(u.cifras_de(t)) < 3:     # una division de las tablas
        return False
    return (u.cifras_de(t)[0] == 0 and u.cifras_de(d)[0] == 0) or _eq_sin_ceros_acaba_en_5(d, u)


def _m13_es_decimal(x):
    """M.13: '0.3' lleva punto; '4' no.  (Es MIRAR si hay punto, no calcular.)"""
    return isinstance(x, str) and "." in x


def _m13_un_decimal_y_un_entero(s):
    x, y = s.get("x"), s.get("y")
    if not (isinstance(x, str) and isinstance(y, str)):
        return False
    return _m13_es_decimal(x) != _m13_es_decimal(y)


def _m13_el_entero_es_corto(s):
    """NCETM 2.19 (punto 3): el entero es de UNA cifra; o 10 o 100 (las cifras suben de sitio, M.9)."""
    ent = s["y"] if _m13_es_decimal(s["x"]) else s["x"]
    return ent in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "100")


# ---- tres factores (paso M.14; NCETM 2.20): situacion {"factores": ["25", "7", "4"]} (en texto: puede haber UN decimal)
def _m14_factores(s):
    f = s.get("factores")
    return f if isinstance(f, list) and all(isinstance(x, str) for x in f) else []


def _m14_acaba_en_5(f):
    """'25', '50', '0.5', '1.25': sin los ceros del final, la ultima cifra es un 5.  Es MIRAR, no calcular."""
    return f.replace(".", "").rstrip("0").endswith("5")


def _m14_es_par(f):
    return f != "0" and f[-1] in "02468"


def _m14_decenas_justas(f):
    """'20', '100', '3000': un entero que acaba en cero (y no es el cero)."""
    return "." not in f and f != "0" and f.endswith("0")


def _m14_amigos(f, g):
    """Uno acaba en 5 y el otro es par: su producto son decenas justas (25 x 4 = 100; 0.5 x 2 = 1)."""
    if "." in f and "." in g:
        return False
    return (_m14_acaba_en_5(f) and _m14_es_par(g)) or (_m14_acaba_en_5(g) and _m14_es_par(f))


def _m14_hay_pareja_facil(s):
    fs = _m14_factores(s)
    if any(_m14_decenas_justas(f) or "." in f for f in fs):     # decenas justas al final; el decimal, con uno corto
        return True
    return any(_m14_amigos(f, g) for i, f in enumerate(fs) for g in fs[i + 1:])


# ---- factores, multiplos y primos (paso M.15; NCETM 2.21): situacion {"n": 36}
def _m15_entero_positivo(s, u):
    n = s.get("n")
    return isinstance(n, int) and not isinstance(n, bool) and n != 0 and u.decir(n) is not None


def _m15_pareja_de_100(s, u):
    a, b = s.get("a"), s.get("b")
    if not isinstance(a, int) or not isinstance(b, int):
        return False
    return any(f in (25, 50, 20) and _eq_pasa_de_doce(g, u) for f, g in ((a, b), (b, a)))


# ---- combinar x con + y - (paso M.16; NCETM 2.22): situacion {"terminos": [["+", ["3"]], ["+", ["4", "5"]]]}
#      (cada termino: su signo y sus factores; un factor es un numero en texto o un parentesis {"terminos": ...})
def _m16_terminos(s):
    t = s.get("terminos")
    return t if isinstance(t, list) and t else []


def _m16_productos(terminos):
    """Todos los productos (listas de factores), tambien los de dentro de los parentesis."""
    for _, fs in terminos:
        yield fs
        for f in fs:
            if isinstance(f, dict):
                for x in _m16_productos(f["terminos"]):
                    yield x


def _m16_hay_cuenta(s):
    """Hay algo que hacer: dos terminos o mas, o un producto (de numeros o de parentesis)."""
    t = _m16_terminos(s)
    return len(t) >= 2 or any(len(fs) >= 2 for fs in _m16_productos(t))


def _m16_un_decimal(s):
    return all(len([f for f in fs if not isinstance(f, dict) and "." in f]) < 2
               for fs in _m16_productos(_m16_terminos(s)))


def _m16_factor_comun(s):
    """Dos terminos de uno o dos numeros (sin parentesis), al menos uno con dos, que comparten un factor
    entero que no es 0.  Comparar es LEER si dos numeros se escriben igual."""
    t = _m16_terminos(s)
    if len(t) != 2:
        return False
    f1, f2 = t[0][1], t[1][1]
    if any(isinstance(f, dict) for x in (f1, f2) for f in x) or len(f1) > 2 or len(f2) > 2:
        return False
    if len(f1) == 1 and len(f2) == 1:
        return False
    limpio = [f.lstrip("0") or "0" for f in f1 if "." not in f]
    return any(a != "0" and a in [g.lstrip("0") or "0" for g in f2 if "." not in g] for a in limpio)


# ---- parte-parte-todo con tres partes o mas (paso S.2; NCETM 1.28): situacion {"partes": ["37", "25", "63"]}
#      o {"todo": "100", "partes": ["37", None, "25"]} (None: la parte que falta; todas None con "iguales": True)
def _ppt_partes(s):
    p = s.get("partes")
    return p if isinstance(p, list) else []


def _ppt_se_saben_todas(s):
    """Dos partes o mas y todas escritas (falta el TODO).  Mirar, no contar: hay algo detras de la primera."""
    p = _ppt_partes(s)
    return bool(p[1:]) and None not in p and s.get("todo") is None


def _ppt_falta_una_sola(s):
    """Hay un todo y falta UNA parte: hay un None y, quitandolo, no queda otro."""
    p = _ppt_partes(s)
    if s.get("todo") is None or None not in p or not p[1:]:
        return False
    resto = list(p)
    resto.remove(None)
    return None not in resto


def _ppt_se_saben_dos_o_mas(s):
    return bool([x for x in _ppt_partes(s) if x is not None][1:])


def _ppt_iguales_que_faltan(s):
    p = _ppt_partes(s)
    return s.get("todo") is not None and bool(s.get("iguales")) and bool(p[1:]) and set(p) == {None}


def _ppt_normal(f):
    """'6.50' -> '6.5', '06' -> '6': se escriben igual?  (mirar las cifras, no calcular)"""
    if "." in f:
        f = f.rstrip("0").rstrip(".")
    e, punto, d = f.partition(".")
    e = e.lstrip("0") or "0"
    return "%s.%s" % (e, d) if punto else e


def _ppt_todas_iguales(s):
    if not _ppt_se_saben_todas(s):
        return False
    n = [_ppt_normal(x) for x in _ppt_partes(s)]
    return all(x == n[0] for x in n)


def _ppt_ultima_cifra(f, k):
    """La ultima cifra de f con el punto alineado a k cifras decimales (escribir ceros, no calcular)."""
    e, _, d = f.partition(".")
    return d.ljust(k, "0")[-1] if k else e[-1]


def _ppt_son_amigas(f, g, u):
    """Las ultimas cifras (con el punto en su sitio) hacen DIEZ: 37 y 63 (7 y 3), 1.25 y 0.75 (5 y 5).
    Se cuenta con los dedos: desde la una, tantos pasos como la otra."""
    k = max(len(f.partition(".")[2]), len(g.partition(".")[2]))
    a, b = _ppt_ultima_cifra(f, k), _ppt_ultima_cifra(g, k)
    if a == "0" or b == "0":
        return False
    r = u.contar_adelante(u.decir(int(a)), u.decir(int(b)))
    return r.get("resultado") == "diez"


def _ppt_hay_amigas(s, u):
    p = _ppt_partes(s)
    if not _ppt_se_saben_todas(s) or not p[2:]:
        return False
    return any(_ppt_son_amigas(f, g, u) for i, f in enumerate(p) for g in p[i + 1:])


def _tipo(s):
    return s.get("tipo")


def _decenas_justas(n, u):
    """30, 40 ... 90: dos cifras y la de las unidades es un cero (se LEEN las cifras)."""
    c = u.cifras_de(n)
    return len(c) == 2 and c[0] == 0


def _acaba_en_nueve(n, u):
    """19, 29 ... 89: dos cifras, acaba en nueve, y la decena siguiente sigue siendo de dos cifras."""
    c = u.cifras_de(n)
    return len(c) == 2 and c[0] == 9 and c[1] != 9


def _mitad_conocida(s, u):
    for f, k in ((s["b"], s["a"]), (s["a"], s["b"])):
        if f in (4, 8, 6):
            m = {4: 2, 8: 4, 6: 3}[f]
            if u.recuerdo("%d x %d" % (k, m)) or u.recuerdo("%d x %d" % (m, k)):
                return True
    return False


def _se_puede_partir(s, u):
    """La distributiva (M.6): f = p + q con p x k y q x k sabidos (p entre 10, 5, 2, 4, 3)."""
    def sabido(x, k):
        return x == 1 or u.recuerdo("%d x %d" % (x, k)) or u.recuerdo("%d x %d" % (k, x))
    for f, k in ((s["a"], s["b"]), (s["b"], s["a"])):
        if len(u.cifras_de(f)) > 2:                      # se parte un numero pequeno (los grandes: por sitios, M.10)
            continue
        for p in (10, 5, 2, 4, 3):
            if u.viene_despues(u.decir(f), u.decir(p)):
                q = u.leer(u.contar_hasta(u.decir(p), u.decir(f)))
                if sabido(p, k) and sabido(q, k):
                    return True
    return False


def _tercio_conocido(s, u):
    for f, k in ((s["b"], s["a"]), (s["a"], s["b"])):
        if f == 9 and (u.recuerdo("%d x 3" % k) or u.recuerdo("3 x %d" % k)):
            return True
    return False


def _en_las_tablas(s, u):
    q = "cero"
    while True:
        h = u.recuerdo("%d x %d" % (u.leer(q), s["divisor"]))
        if h and h["valor"] == s["total"]:
            return True
        if q == "diez":
            return False
        q = u.siguiente(q)


def _saltos_de_diez(a, b, u):
    """Cuantos saltos de diez hay de a hasta b (como mucho nueve), o None si no se llega."""
    v, saltos = a, "cero"
    while v != b:
        if saltos == "nueve":
            return None
        v = u.subir_una_decena(v)
        if v is None or u.viene_despues(u.decir(v), u.decir(b)):
            return None
        saltos = u.siguiente(saltos)
    return saltos


def _conocido(s):
    h = s["con_hueco"]
    return h["a"] if h["b"] == "?" else h["b"]


def _comparten(s):
    if "completo" not in s:
        return False
    c, h = s["completo"], s["con_hueco"]
    if c["op"] != h["op"]:
        return False
    if c["op"] == "+":
        return _conocido(s) in (c["a"], c["b"])
    return (h["b"] == "?" and h["a"] == c["a"]) or (h["a"] == "?" and h["b"] == c["b"])


def _cerca(k, p, u):
    """De k a p (o de p a k) caben los pasos en los dedos."""
    a, b = (p, k) if u.viene_despues(u.decir(k), u.decir(p)) else (k, p)
    d = u.contar_hasta(u.decir(a), u.decir(b))
    return d is not None and u.levantar_dedos(d) is not None


def _menor(s, u):
    return s["b"] if u.viene_despues(u.decir(s["a"]), u.decir(s["b"])) else s["a"]


def _p7_redondo(u, n, ceros):
    """P.7: el redondo de al lado de n (la pieza buscar_el_redondo_cercano), o None."""
    try:
        return u.usar("buscar_el_redondo_cercano", n=n, ceros=ceros)["resultado"]
    except Exception:
        return None


def _p7_facil(u, p, q):
    """P.7: de p a q hay un cambio FACIL: cabe en los dedos o son decenas/centenas justas (20, 300...)."""
    if u.decir(p) is None or u.decir(q) is None:
        return False
    g, m = (p, q) if u.viene_despues(u.decir(p), u.decir(q)) else (q, p)
    try:
        d = u.usar("restar_por_columnas", a=g, b=m)["valor"]
    except Exception:
        return False
    return u.levantar_dedos(u.decir(d)) is not None or u.cifras_de(d)[0] == 0


def _p7_parejas(u, i, d):
    """P.7: como se emparejan los numeros de dos sumas o dos restas para ver el cambio facil.  En la resta,
    minuendo con minuendo y sustraendo con sustraendo; en la suma, tambien cruzados.  None si no hay."""
    if i.get("op") not in ("+", "-") or d.get("op") != i["op"]:
        return None
    formas = [((i["a"], d["a"]), (i["b"], d["b"]))]
    if i["op"] == "+":
        formas.append(((i["a"], d["b"]), (i["b"], d["a"])))
    for f in formas:
        if all(_p7_facil(u, p, q) for p, q in f):
            return f
    return None


def _p7_resta_valida(u, l):
    return l.get("op") != "-" or not u.viene_despues(u.decir(l["b"]), u.decir(l["a"]))


def _p7_balanza_de_restas(s, u):
    if "completo" not in s or s["completo"]["op"] != "-" or s["con_hueco"]["op"] != "-":
        return False
    c, h = s["completo"], s["con_hueco"]
    if h["a"] == "?" and h["b"] == "?":
        return False
    return _p7_facil(u, c["a"], h["a"]) if h["b"] == "?" else _p7_facil(u, c["b"], h["b"])


CONDICIONES = {
    # ---- los pasos de un problema (resolvedor, R.1)
    "es_un_cambio": lambda s, u: _tipo(s) in ("cambio", "deshacer", "cambio_desconocido"),
    "se_sabe_el_cambio": lambda s, u: s.get("n") is not None,
    "no_se_sabe_el_cambio": lambda s, u: _tipo(s) == "cambio_desconocido",
    "va_hacia_adelante": lambda s, u: _tipo(s) == "cambio",
    "va_hacia_atras": lambda s, u: _tipo(s) == "deshacer",
    "el_monton_crece": lambda s, u: s.get("signo") == "+",
    "el_monton_disminuye": lambda s, u: s.get("signo") == "-",
    "hay_bastantes": lambda s, u: s["n"] <= s["antes"],
    "hay_bastantes_al_deshacer": lambda s, u: s["n"] <= s["despues"],
    "el_despues_no_es_menor": lambda s, u: s["despues"] >= s["antes"],
    "el_despues_no_es_mayor": lambda s, u: s["despues"] <= s["antes"],
    "se_piden_los_dos_juntos": lambda s, u: _tipo(s) == "juntar",
    "son_la_misma_cosa": lambda s, u: (not s.get("cosa_a") or not s.get("cosa_b")
                                       or s["cosa_a"] == s["cosa_b"]),
    "se_pide_el_hueco": lambda s, u: _tipo(s) == "comparar",
    "hay_una_comparacion": lambda s, u: _tipo(s) == "comparacion",
    "el_que_falta_tiene_menos": lambda s, u: s.get("falta") == "menor",
    "el_que_falta_tiene_mas": lambda s, u: s.get("falta") == "mayor",
    "hay_un_todo_y_una_parte": lambda s, u: _tipo(s) == "parte",
    "la_parte_cabe_en_el_todo": lambda s, u: s["parte"] <= s["todo"],
    # ---- los metodos de calculo (situacion: {"a": .., "b": ..})
    "el_segundo_cabe_en_los_dedos": lambda s, u: u.levantar_dedos(u.decir(s["b"])) is not None,
    "los_dos_son_de_una_cifra": lambda s, u: not u.viene_despues(u.decir(s["a"]), "nueve")
    and not u.viene_despues(u.decir(s["b"]), "nueve"),
    "la_suma_cruza_el_diez": lambda s, u: u.viene_despues(
        u.contar_adelante(u.decir(s["a"]), u.decir(s["b"]))["resultado"], "diez"),
    "el_total_tiene_nombre": lambda s, u: u.sumar_por_columnas(s["a"], s["b"]) is not None,
    # ---- multiplicacion corta (paso M.10; NCETM 2.14): un factor de una cifra (2..9), el otro de varias
    "los_dos_factores_de_varias_cifras": lambda s, u: (len(u.cifras_de(s.get("a", 0))) >= 2
                                                        and len(u.cifras_de(s.get("b", 0))) >= 2),
    "un_factor_de_una_cifra_y_otro_de_varias": lambda s, u: any(
        len(u.cifras_de(x)) == 1 and x not in (0, 1) and len(u.cifras_de(y)) >= 2
        for x, y in ((s.get("a", 0), s.get("b", 0)), (s.get("b", 0), s.get("a", 0)))),
    "el_divisor_es_de_una_cifra_y_el_dividendo_de_varias": lambda s, u: s.get("divisor") not in (None, 0, 1)
        and len(u.cifras_de(s["divisor"])) == 1 and len(u.cifras_de(s.get("total") or 0)) >= 2,
    # ---- por 10 y por 100 (paso M.9; NCETM 2.13)
    "un_factor_es_10_o_100": lambda s, u: s.get("a") in (10, 100) or s.get("b") in (10, 100),
    "el_divisor_es_10_o_100": lambda s, u: s.get("divisor") in (10, 100),
    "un_factor_acaba_en_cero": lambda s, u: any(x and u.cifras_de(x)[0] == 0 for x in (s.get("a"), s.get("b"))),
    "el_dividendo_acaba_en_cero": lambda s, u: bool(s.get("total")) and u.cifras_de(s["total"])[0] == 0
                                                and s.get("divisor") not in (0, 1, 10, 100),
    # ---- miles justos (paso N.4; NCETM 1.26: lo de hasta mil sirve para los miles)
    "los_dos_son_miles_justos": lambda s, u: all(len(u.cifras_de(x)) >= 5 and u.cifras_de(x)[:3] == [0, 0, 0]
                                                for x in (s["a"], s["b"])),
    # ---- centenas justas (paso N.3; NCETM 1.22: 'al sumar o restar multiplos de 100, sale un multiplo de 100')
    "los_dos_son_centenas_justas": lambda s, u: all(len(u.cifras_de(x)) >= 3 and u.cifras_de(x)[0] == 0
                                                   and u.cifras_de(x)[1] == 0 for x in (s["a"], s["b"])),
    "el_de_abajo_no_es_mayor": lambda s, u: not u.viene_despues(u.decir(s["b"]), u.decir(s["a"])),
    # ---- la memoria (paso 3)
    "se_permite_recordar": lambda s, u: not s.get("sin_memoria"),
    "la_suma_esta_en_la_memoria": lambda s, u: u.recuerdo("%d + %d" % (s["a"], s["b"])) is not None,
    "la_resta_esta_en_la_memoria": lambda s, u: u.recuerdo("%d - %d" % (s["a"], s["b"])) is not None,
    "el_segundo_no_es_menor": lambda s, u: not u.viene_despues(u.decir(s["a"]), u.decir(s["b"])),
    # ---- multiplicar (paso M.1): situacion {"a": grupos, "b": cuantos en cada grupo}
    "los_grupos_tienen_nombre_x": lambda s, u: u.decir(s["a"]) is not None,
    # N.4: sumar grupo a grupo es para POCOS grupos (hasta doce), leyendolo como haga falta (la conmutativa)
    "pocos_grupos_en_alguna_lectura": lambda s, u: any(u.decir(x) is not None and not u.viene_despues(u.decir(x), "doce")
                                                       for x in (s["a"], s["b"])),
    # ---- problemas de x y : (paso R.2): el esquema de grupos iguales {"busca", "grupos", "en_cada", "total"}
    "se_busca_el_total": lambda s, u: s.get("busca") == "total",
    "se_busca_cuantos_en_cada": lambda s, u: s.get("busca") == "en_cada",
    "se_busca_cuantos_grupos": lambda s, u: s.get("busca") == "grupos",
    "se_saben_grupos_y_en_cada": lambda s, u: s.get("grupos") is not None and s.get("en_cada") is not None,
    "se_saben_total_y_grupos": lambda s, u: s.get("total") is not None and s.get("grupos") is not None,
    "se_saben_total_y_en_cada": lambda s, u: s.get("total") is not None and s.get("en_cada") is not None,
    # ---- dividir (paso M.3): situacion {"total": .., "divisor": ..}
    "el_divisor_no_es_cero": lambda s, u: s["divisor"] != 0,
    "es_un_caso_especial": lambda s, u: s["total"] == 0 or s["total"] == s["divisor"] or s["divisor"] == 1,
    "el_divisor_es_dos": lambda s, u: s["divisor"] == 2,
    "la_division_esta_en_las_tablas": lambda s, u: _en_las_tablas(s, u),
    # ---- doblar tablas (paso M.4)
    "se_puede_doblar_una_tabla": lambda s, u: _mitad_conocida(s, u),
    "se_puede_triplicar_el_3": lambda s, u: _tercio_conocido(s, u),
    "un_factor_se_puede_partir": lambda s, u: _se_puede_partir(s, u),
    # ---- las tablas (paso M.2)
    "un_factor_es_cero_o_uno": lambda s, u: s["a"] in (0, 1) or s["b"] in (0, 1),
    "un_factor_es_dos": lambda s, u: s["a"] == 2 or s["b"] == 2,
    "la_otra_lectura_se_salta": lambda s, u: u.decir(s["a"]) in ("dos", "cinco", "diez")
    and u.decir(s["b"]) not in ("dos", "cinco", "diez"),
    "el_producto_esta_en_la_memoria": lambda s, u: u.recuerdo("%d x %d" % (s["a"], s["b"])) is not None,
    # ---- suma de iguales (paso M.0): situacion {"veces": .., "n": ..}
    "cada_grupo_se_salta": lambda s, u: u.decir(s["n"]) in ("dos", "cinco", "diez"),
    "los_grupos_tienen_nombre": lambda s, u: u.decir(s["veces"]) is not None,
    # ---- par e impar; saltar de diez (paso N.1)
    "es_de_veinte_o_menos": lambda s, u: not u.viene_despues(u.decir(s["n"]), "veinte"),
    "pasa_de_veinte": lambda s, u: u.viene_despues(u.decir(s["n"]), "veinte"),
    "se_llega_saltando_de_diez": lambda s, u: _saltos_de_diez(s["a"], s["b"], u) is not None,
    # ---- la balanza (paso E.2): situacion {"completo": {a, op, b}, "con_hueco": {a, op, b} con un "?"}
    "hay_un_plato_completo": lambda s, u: "completo" in s and "con_hueco" in s,
    "comparten_un_numero": lambda s, u: _comparten(s),
    "los_dos_lados_son_sumas": lambda s, u: "completo" in s and s["completo"]["op"] == "+"
    and s["con_hueco"]["op"] == "+",
    "hay_una_pareja_cerca": lambda s, u: any(_cerca(_conocido(s), p, u)
                                             for p in (s["completo"]["a"], s["completo"]["b"])),
    # ---- el = (paso E.0): situacion {"lados": [{"texto", "n"} o {"texto", "a", "op", "b"}, ...]}
    "hay_dos_lados_o_mas": lambda s, u: len(s.get("lados", ())) >= 2,
    "todos_los_lados_estan_escritos_igual": lambda s, u: len(s.get("lados", ())) >= 2
    and all(l["texto"] == s["lados"][0]["texto"] for l in s["lados"]),
    "son_los_mismos_numeros_al_reves": lambda s, u: len(s.get("lados", ())) == 2
    and s["lados"][0].get("op") in ("+", "x") and s["lados"][1].get("op") == s["lados"][0].get("op")
    and s["lados"][0]["a"] == s["lados"][1]["b"] and s["lados"][0]["b"] == s["lados"][1]["a"],
    # ---- dar la vuelta (paso P.5)
    "el_primero_es_menor": lambda s, u: u.viene_despues(u.decir(s["b"]), u.decir(s["a"])),
    "el_primero_es_corto": lambda s, u: _decenas_justas(s["a"], u)
    or u.levantar_dedos(u.decir(s["a"])) is not None,
    # ---- restar pensando en sumar (paso P.6): se MIRA cuanto hay de uno a otro, contando
    "estan_cerca": lambda s, u: not u.viene_despues(
        u.decir(s["a"]), u.contar_adelante(u.decir(s["b"]), "diez").get("resultado") or "mil"),
    "hacia_arriba_es_mas_corto": lambda s, u: u.viene_despues(
        u.decir(s["b"]), u.contar_hasta(u.decir(s["b"]), u.decir(s["a"])) or "mil"),
    # ---- las tecnicas para ir mas rapido (paso 4)
    "el_segundo_son_decenas_justas": lambda s, u: _decenas_justas(s["b"], u),
    "son_casi_dobles": lambda s, u: u.siguiente(u.decir(s["a"])) == u.decir(s["b"])
    or u.siguiente(u.decir(s["b"])) == u.decir(s["a"]),
    "el_doble_lo_se_de_memoria": lambda s, u: u.recuerdo("%d + %d" % (_menor(s, u), _menor(s, u))) is not None,
    "ninguno_es_cero": lambda s, u: s["a"] != 0 and s["b"] != 0,
    "uno_acaba_en_nueve": lambda s, u: _acaba_en_nueve(s["a"], u) or _acaba_en_nueve(s["b"], u),
    "el_de_abajo_acaba_en_nueve": lambda s, u: _acaba_en_nueve(s["b"], u),
    "el_de_arriba_llega_a_la_decena": lambda s, u: not u.viene_despues(
        u.siguiente(u.decir(s["b"])), u.decir(s["a"])),
    # ---- comparar fracciones (paso F.1; NCETM 3.2): situacion {"a": (arriba, abajo), "b": (arriba, abajo)}
    "son_fracciones_unitarias": lambda s, u: s["a"][0] == 1 and s["b"][0] == 1,
    "mismo_denominador": lambda s, u: s["a"][1] == s["b"][1],
    "mismo_numerador": lambda s, u: s["a"][0] == s["b"][0],
    "comparten_arriba_o_abajo": lambda s, u: s["a"][0] == s["b"][0] or s["a"][1] == s["b"][1],
    # ---- usar la equivalencia (paso M.12; NCETM 2.18)
    "un_factor_acaba_en_cinco_y_el_otro_es_par": lambda s, u: _eq_doblar_y_partir(s, u),
    "se_puede_escalar_la_division": lambda s, u: _eq_escalar_division(s, u),
    "dos_lados_por_o_entre": lambda s, u: len(s.get("lados", ())) == 2
    and s["lados"][0].get("op") in ("x", ":") and s["lados"][1].get("op") == s["lados"][0].get("op"),
    "la_balanza_es_de_por_o_entre": lambda s, u: s["completo"].get("op") in ("x", ":")
    and s["con_hueco"].get("op") == s["completo"]["op"],
    # ---- decimales por enteros (paso M.13; NCETM 2.19): situacion {"x": "0.3", "y": "4"} o {"x": "7.2", "d": "3"}
    "un_decimal_y_un_entero": lambda s, u: _m13_un_decimal_y_un_entero(s),
    "el_entero_es_de_una_cifra_o_10_o_100": lambda s, u: _m13_el_entero_es_corto(s),
    "uno_es_una_decima_o_una_centesima": lambda s, u: s.get("x") in ("0.1", "0.01") or s.get("y") in ("0.1", "0.01"),
    "el_divisor_es_de_una_cifra_sin_el_cero": lambda s, u: s.get("d") in ("1", "2", "3", "4", "5", "6", "7", "8", "9"),
    "el_divisor_es_un_10_o_un_100": lambda s, u: s.get("d") in ("10", "100"),
    # ---- tres factores (paso M.14; NCETM 2.20): situacion {"factores": ["25", "7", "4"]}
    "hay_tres_factores_o_mas": lambda s, u: len(_m14_factores(s)) >= 3,
    "como_mucho_un_decimal": lambda s, u: len([f for f in _m14_factores(s) if "." in f]) < 2,
    "algun_factor_es_cero": lambda s, u: "0" in _m14_factores(s),
    "ningun_factor_es_cero": lambda s, u: "0" not in _m14_factores(s),
    "hay_una_pareja_facil": lambda s, u: _m14_hay_pareja_facil(s),
    # ---- factores, multiplos y primos (paso M.15; NCETM 2.21)
    "es_un_entero_positivo": lambda s, u: _m15_entero_positivo(s, u),
    "es_el_uno": lambda s, u: s.get("n") == 1,
    "pasa_de_uno": lambda s, u: _m15_entero_positivo(s, u) and s["n"] != 1,
    "un_factor_es_25_50_o_20_y_el_otro_grande": lambda s, u: _m15_pareja_de_100(s, u),
    # ---- combinar x con + y - (paso M.16; NCETM 2.22)
    "hay_alguna_cuenta": lambda s, u: _m16_hay_cuenta(s),
    "cada_producto_con_un_decimal_como_mucho": lambda s, u: _m16_un_decimal(s),
    "hay_un_factor_comun": lambda s, u: _m16_factor_comun(s),
    # ---- parte-parte-todo con tres partes o mas (paso S.2; NCETM 1.28)
    "se_saben_todas_las_partes": lambda s, u: _ppt_se_saben_todas(s),
    "hay_tres_partes_o_mas": lambda s, u: bool(_ppt_partes(s)[2:]),
    "hay_dos_partes_amigas": lambda s, u: _ppt_hay_amigas(s, u),
    "todas_las_partes_son_iguales": lambda s, u: _ppt_todas_iguales(s),
    "falta_una_sola_parte": lambda s, u: _ppt_falta_una_sola(s),
    "se_saben_dos_partes_o_mas": lambda s, u: _ppt_se_saben_dos_o_mas(s),
    "faltan_todas_y_son_iguales": lambda s, u: _ppt_iguales_que_faltan(s),
    # ---- la compensacion con numeros grandes (paso P.7; NCETM 1.29)
    "el_numero_tiene_nombre": lambda s, u: u.decir(s["n"]) is not None,
    "un_sumando_esta_cerca_de_un_redondo": lambda s, u: any(_p7_redondo(u, x, s.get("ceros", 2)) is not None
                                                            for x in (s["a"], s["b"])),
    "el_de_abajo_esta_cerca_de_un_redondo": lambda s, u: _p7_redondo(u, s["b"], s.get("ceros", 2)) is not None,
    "dos_sumas_o_dos_restas_con_cambios_faciles": lambda s, u: len(s.get("lados", ())) == 2
    and all(_p7_resta_valida(u, l) for l in s["lados"] if "op" in l)
    and _p7_parejas(u, s["lados"][0], s["lados"][1]) is not None,
    "los_dos_lados_son_restas_con_un_cambio_facil": lambda s, u: _p7_balanza_de_restas(s, u),
    "se_sabe_un_hecho_de_la_misma_cuenta": lambda s, u: "hecho" in s and s["hecho"].get("op") in ("+", "-")
    and s["nuevo"].get("op") == s["hecho"]["op"],
    "los_cambios_desde_el_hecho_son_faciles": lambda s, u: _p7_parejas(u, s["hecho"], s["nuevo"]) is not None,
    "la_cuenta_nueva_es_suma_o_resta": lambda s, u: s.get("nuevo", {}).get("op") in ("+", "-"),
    # ---- redondear (paso N.2; 3.NBT.A.1): el numero esta en la lista, y el sitio es decena o centena
    "se_puede_redondear": lambda s, u: u.decir(s["n"]) is not None and s.get("a") in (
        "decena", "centena", "millar", "decena de millar", "centena de millar"),
}

DE_APLICACION = {"el_divisor_no_es_cero", "hay_bastantes", "hay_bastantes_al_deshacer", "la_parte_cabe_en_el_todo",
                 "el_despues_no_es_menor", "el_despues_no_es_mayor", "el_de_abajo_no_es_mayor"}
