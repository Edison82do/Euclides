# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 0.2 - formar y reconocer GRUPOS por atributo.

  A) CASOS DE EJEMPLO  - los que estan escritos en el conocimiento.
  B) CASOS DE DOMINIO  - NO programados: casos nuevos que el sistema tiene que resolver
     con lo que ya sabe.  Incluye TRAMPAS sacadas de los errores tipicos documentados:
     cambiar de criterio, mezclar atributos, grupos no exhaustivos, confundir el valor
     con el atributo, y dar por sabido lo que no esta escrito.

Uso:  python pruebas/test_0_2.py
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

from motor import (cargar_conocimiento, decidir_0_2_reconocer, decidir_0_2_formar,  # noqa: E402
                   escena_0_2, parsear_criterio, explicar_0_2_reconocer, explicar_0_2_formar,
                   explicar_pregunta)


# ------------------------------------------------------------------ reconocer

# (titulo, escena en texto, conclusion esperada, atributos esperados)
EJEMPLOS_RECONOCER = [
    ("E1 dos rojos, distinta forma",
     "caja_A(color=rojo,forma=cubo); caja_B(color=rojo,forma=esfera)",
     "grupo_atributo", ["color"]),
    ("E2 dos cubos, distinto color",
     "caja_A(color=rojo,forma=cubo); caja_B(color=azul,forma=cubo)",
     "grupo_atributo", ["forma"]),
]

DOMINIO_RECONOCER = [
    ("D1 tres rojos de tres formas distintas",
     "a(color=rojo,forma=cubo); b(color=rojo,forma=esfera); c(color=rojo,forma=cilindro)",
     "grupo_atributo", ["color"]),

    ("D2 TRAMPA: dos rojos y uno al que no se le sabe el color",
     "a(color=rojo,forma=cubo); b(color=rojo,forma=esfera); c(forma=cilindro)",
     "no_decidible", []),

    ("D3 ninguno comparte nada",
     "a(color=rojo,forma=cubo); b(color=azul,forma=esfera)",
     "sin_atributo_comun", []),

    ("D4 TRAMPA: comparten DOS atributos a la vez",
     "a(color=rojo,forma=cubo); b(color=rojo,forma=cubo)",
     "grupo_atributo", ["color", "forma"]),

    ("D5 TRAMPA: un solo objeto no es un grupo",
     "a(color=rojo,forma=cubo)",
     "una_sola_entidad", []),

    ("D6 un mismo nombre con DOS colores distintos PRUEBA que son dos objetos",
     "casa(color=azul); casa(color=rojo)",
     "sin_atributo_comun", []),

    ("D7 TRAMPA: la MISMA entidad repetida igual no es un grupo",
     "casa(color=azul); casa(color=azul)",
     "una_sola_entidad", []),

    ("D8 separar por comas de fuera: un objeto con atributos y otro sin ellos",
     "casa(color=azul), carro",
     "no_decidible", []),

    ("D9 la MISMA casa descrita dos veces sin contradecirse: sus datos se SUMAN y sigue siendo un objeto",
     "casa(color=blanco); casa(forma=cuadrada)",
     "una_sola_entidad", []),
]

# ------------------------------------------------------------------ formar

# (titulo, escena en texto, criterio, conclusion esperada, miembros esperados)
EJEMPLOS_FORMAR = [
    ("F1 los rojos de una escena mezclada",
     "a(color=rojo,forma=cubo); b(color=azul,forma=cubo); c(color=rojo,forma=esfera)",
     "color=rojo", "grupo_formado", ["a", "c"]),
]

DOMINIO_FORMAR = [
    ("F2 TRAMPA: pedir los rojos y uno no declara su color",
     "a(color=rojo); b(forma=cubo)",
     "color=rojo", "no_decidible", []),

    ("F3 TRAMPA: pedir los verdes y no hay ninguno verde",
     "a(color=rojo); b(color=azul)",
     "color=verde", "no_hay_grupo", []),

    ("F4 TRAMPA: el VALOR no es el ATRIBUTO (tono=rojo no es color=rojo)",
     "a(color=rojo); b(tono=rojo)",
     "color=rojo", "no_decidible", []),

    ("F5 formar los cubos",
     "a(color=rojo,forma=cubo); b(color=azul,forma=esfera); c(color=verde,forma=cubo)",
     "forma=cubo", "grupo_formado", ["a", "c"]),
]


def correr_reconocer(casos, saber, etiqueta):
    print("=" * 76)
    print(etiqueta)
    print("=" * 76)
    bien = 0
    for titulo, texto, concl_esp, attrs_esp in casos:
        escena = escena_0_2(texto)
        try:
            r = decidir_0_2_reconocer(escena, saber)
            concl, attrs = r["conclusion"], r["atributos_compartidos"]
        except ValueError:
            concl, attrs = "no_decidible", []
        ok = concl == concl_esp and (
            concl_esp != "grupo_atributo" or sorted(attrs) == sorted(attrs_esp))
        bien += ok
        print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
        print("       esperado=%s %s   obtenido=%s %s" % (concl_esp, attrs_esp, concl, attrs))
        if not ok:
            print(explicar_0_2_reconocer(escena, saber))
    print("-- %d/%d correctos\n" % (bien, len(casos)))
    return bien, len(casos)


def correr_formar(casos, saber, etiqueta):
    print("=" * 76)
    print(etiqueta)
    print("=" * 76)
    bien = 0
    for titulo, texto, crit_txt, concl_esp, miembros_esp in casos:
        escena = escena_0_2(texto)
        criterio = parsear_criterio(crit_txt)
        try:
            r = decidir_0_2_formar(escena, criterio, saber)
            concl, miembros = r["conclusion"], r["miembros"]
        except ValueError:
            concl, miembros = "no_decidible", []
        ok = concl == concl_esp and (
            concl_esp != "grupo_formado" or sorted(miembros) == sorted(miembros_esp))
        bien += ok
        print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
        print("       esperado=%s %s   obtenido=%s %s" % (concl_esp, miembros_esp, concl, miembros))
        if not ok:
            print(explicar_0_2_formar(escena, criterio, saber))
    print("-- %d/%d correctos\n" % (bien, len(casos)))
    return bien, len(casos)


def correr_robustez(saber):
    """
    El sistema NUNCA debe soltar un traceback delante de quien prueba.  Si no entiende
    lo escrito, tiene que decirlo.  Estas pruebas fijan ese comportamiento.
    """
    print("=" * 76)
    print("C) ROBUSTEZ - lo que no se entiende se dice, no revienta")
    print("=" * 76)
    entradas = [
        "caja(colorrojo)",
        "caja(color=)",
        "caja(=rojo)",
        "(color=rojo)",
        "caja(color=rojo",
        "caja(color=rojo))",
        "color=: a(color=rojo)",
    ]
    bien = 0
    for e in entradas:
        try:
            salida = explicar_pregunta(e, saber)
            if isinstance(salida, str) and salida.startswith("NO ENTIENDO"):
                bien += 1
                print("OK     se dice 'NO ENTIENDO' -> %r" % e)
            else:
                print("FALLA  deberia decir 'NO ENTIENDO' -> %r" % e)
                print("       dijo: %s" % salida.splitlines()[0] if salida else "       nada")
        except Exception as ex:
            print("FALLA  reviento con %r -> %r" % (e, ex))
    print("-- %d/%d correctos\n" % (bien, len(entradas)))
    return bien, len(entradas)


def correr_pluralidad(saber):
    """
    Lo pedido por Carlos el 2026-10-03: 0.2 NO puede ocultar lo que 0.1 ya sabe.
    La respuesta lleva DOS capas: cuantas cosas hay (0.1) y si comparten atributos (0.2).
    """
    print("=" * 76)
    print("D) LAS DOS CAPAS - pluralidad (0.1) y atributos (0.2), siempre las dos")
    print("=" * 76)
    casos = [
        ("casa(color=azul); carro", "varios_objetos", "no_decidible",
         "son dos cosas, pero el color del carro no se sabe"),
        ("casa; carro", "varios_objetos", "sin_atributo_comun",
         "ninguno declara atributos: no hay criterio"),
        ("casa(color=azul)", "un_objeto", "una_sola_entidad",
         "una sola cosa: la pregunta de grupo no aplica"),
        ("casa(color=blanco); casa(forma=cuadrada)", "un_objeto", "una_sola_entidad",
         "la misma casa descrita dos veces: sus datos se suman"),
        ("casa(color=blanco); carro(color=negro)", "varios_objetos", "sin_atributo_comun",
         "el caso de Carlos: dos objetos, ningun atributo en comun"),
        ("casa(color=blanco); casa(color=rojo)", "varios_objetos", "sin_atributo_comun",
         "dos colores distintos: PRUEBA de que son dos objetos"),
    ]
    bien = 0
    for texto, plu_esp, concl_esp, nota in casos:
        try:
            r = decidir_0_2_reconocer(escena_0_2(texto), saber)
            plu, concl = r["pluralidad"], r["conclusion"]
        except ValueError:
            plu, concl = "?", "no_decidible"
        ok = (plu == plu_esp) and (concl == concl_esp)
        bien += ok
        print("%-6s %-44s 0.1=%s  0.2=%s   %s" % ("OK" if ok else "FALLA", texto, plu, concl, nota))
        if not ok:
            print("       esperado: 0.1=%s  0.2=%s" % (plu_esp, concl_esp))
    print("-- %d/%d correctos\n" % (bien, len(casos)))
    return bien, len(casos)


def main():
    saber = cargar_conocimiento()

    a1 = correr_reconocer(EJEMPLOS_RECONOCER, saber, "A) RECONOCER - casos de ejemplo")
    b1 = correr_reconocer(DOMINIO_RECONOCER, saber, "B) RECONOCER - prueba de dominio (no programados)")
    a2 = correr_formar(EJEMPLOS_FORMAR, saber, "A) FORMAR - casos de ejemplo")
    b2 = correr_formar(DOMINIO_FORMAR, saber, "B) FORMAR - prueba de dominio (no programados)")
    rb = correr_robustez(saber)
    dp = correr_pluralidad(saber)

    print("=" * 76)
    print("TRAZA DE LA TRAMPA PRINCIPAL (D2: un objeto cuyo color no se sabe)")
    print("=" * 76)
    print(explicar_0_2_reconocer(escena_0_2(
        "a(color=rojo,forma=cubo); b(color=rojo,forma=esfera); c(forma=cilindro)"), saber))
    print()

    ok = sum(x[0] for x in (a1, b1, a2, b2, rb, dp))
    total = sum(x[1] for x in (a1, b1, a2, b2, rb, dp))
    print("TOTAL: %d/%d" % (ok, total))
    if ok != total:
        print("RESULTADO: ROJO")
        return 1
    print("RESULTADO: VERDE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
