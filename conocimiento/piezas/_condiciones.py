# -*- coding: utf-8 -*-
"""
LAS CONDICIONES DE APLICACION, escritas UNA vez y usadas por todas las piezas.

Cada una recibe (s, u): la SITUACION y lo que se puede usar (el mecanismo: u.viene_despues,
u.levantar_dedos, ...).  Devuelve cierto o falso.  Ninguna hace cuentas de Python: comparan,
miran que hay en la situacion, o preguntan al mecanismo.

DE_APLICACION: las que, si fallan, no dicen "esto no es lo mio" sino "esto es lo mio, pero es
IMPOSIBLE" (quitar mas de lo que hay).  Entonces el problema no tiene solucion, y se dice.
"""


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
    "el_de_abajo_no_es_mayor": lambda s, u: not u.viene_despues(u.decir(s["b"]), u.decir(s["a"])),
    # ---- la memoria (paso 3)
    "se_permite_recordar": lambda s, u: not s.get("sin_memoria"),
    "la_suma_esta_en_la_memoria": lambda s, u: u.recuerdo("%d + %d" % (s["a"], s["b"])) is not None,
    "la_resta_esta_en_la_memoria": lambda s, u: u.recuerdo("%d - %d" % (s["a"], s["b"])) is not None,
    "el_segundo_no_es_menor": lambda s, u: not u.viene_despues(u.decir(s["a"]), u.decir(s["b"])),
    # ---- multiplicar (paso M.1): situacion {"a": grupos, "b": cuantos en cada grupo}
    "los_grupos_tienen_nombre_x": lambda s, u: u.decir(s["a"]) is not None,
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
    and all(l.get("op") == "+" for l in s["lados"])
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
}

DE_APLICACION = {"hay_bastantes", "hay_bastantes_al_deshacer", "la_parte_cabe_en_el_todo",
                 "el_despues_no_es_menor", "el_despues_no_es_mayor", "el_de_abajo_no_es_mayor"}
