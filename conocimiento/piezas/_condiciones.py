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
    # ---- redondear (paso N.2; 3.NBT.A.1): el numero esta en la lista, y el sitio es decena o centena
    "se_puede_redondear": lambda s, u: u.decir(s["n"]) is not None and s.get("a") in (
        "decena", "centena", "millar", "decena de millar", "centena de millar"),
}

DE_APLICACION = {"el_divisor_no_es_cero", "hay_bastantes", "hay_bastantes_al_deshacer", "la_parte_cabe_en_el_todo",
                 "el_despues_no_es_menor", "el_despues_no_es_mayor", "el_de_abajo_no_es_mayor"}
