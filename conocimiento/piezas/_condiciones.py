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
    "el_segundo_no_es_menor": lambda s, u: not u.viene_despues(u.decir(s["a"]), u.decir(s["b"])),
}

DE_APLICACION = {"hay_bastantes", "hay_bastantes_al_deshacer", "la_parte_cabe_en_el_todo",
                 "el_despues_no_es_menor", "el_despues_no_es_mayor", "el_de_abajo_no_es_mayor"}
