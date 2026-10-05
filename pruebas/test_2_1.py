# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 2.1 - CORRESPONDENCIA uno a uno (contar y revisar).

Lo que esta unidad tiene que dejar claro:
  - emparejar: UNA palabra por objeto, en orden, sin repetir ni saltar.
  - los TRES errores de Briars & Secada: objeto sin contar, palabra repetida (el mas comun),
    y saltarse una palabra.  El sistema tiene que SABER CUAL es el error.
  - el sistema NO se inventa palabras de la secuencia que no conoce.
  - repetir el mismo nombre no da dos objetos (unidad 0.1), asi que no da dos palabras.

  A) CASOS DE EJEMPLO  - los del conocimiento.
  B) CASOS DE DOMINIO  - no programados, con trampas.
  C) ROBUSTEZ          - lo mal escrito se dice, no revienta.

Uso:  python pruebas/test_2_1.py
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

from motor import (cargar_conocimiento, decidir_2_1_contar, decidir_2_1_revisar,  # noqa: E402
                   escena_0_2, explicar_2_1_contar, explicar_2_1_revisar, explicar_pregunta)


# (titulo, coleccion, conclusion esperada, emparejamiento esperado)
EJEMPLOS_CONTAR = [
    ("E1 dos objetos", "a, b", "emparejado", [("a", "uno"), ("b", "dos")]),
]

DOMINIO_CONTAR = [
    ("D1 TRAMPA: el mismo nombre tres veces es UN objeto, asi que UNA palabra",
     "a, a, a", "emparejado", [("a", "uno")]),

    # UNIDAD 6.1: la secuencia llega a 100, asi que el techo ya no son diez objetos.
    ("D2 TRAMPA: mas objetos que palabras conoce el sistema -> NO se inventa las que faltan",
     ",".join("o%d" % (i + 1) for i in range(1001)), "no_alcanza_la_secuencia", None),

    ("D2b (MEJORA 6.1): ONCE objetos ya SI se emparejan (antes el sistema solo llegaba a diez)",
     ",".join("o%d" % (i + 1) for i in range(11)), "emparejado", None),

    ("D3 cinco objetos distintos", "a,b,c,d,e", "emparejado",
     [("a", "uno"), ("b", "dos"), ("c", "tres"), ("d", "cuatro"), ("e", "cinco")]),

    ("D4 TRAMPA (encontrada por Carlos): la misma casa descrita con datos que NO chocan es UNA "
     "casa -> tres palabras, no cinco; y los datos se SUMAN",
     "casa(color=blanco), casa, perro, casa(forma=cuadrado), carro", "emparejado",
     [("casa", "uno"), ("perro", "dos"), ("carro", "tres")]),

    ("D5 dos casas con el MISMO atributo y valores que chocan son DOS objetos",
     "casa(color=blanco), casa(color=rojo), carro", "emparejado",
     [("casa#1", "uno"), ("casa#2", "dos"), ("carro", "tres")]),

    ("D6 la coleccion con atributos, con un objeto repetido de verdad",
     "silla(color=azul), silla(color=azul), mesa", "emparejado",
     [("silla", "uno"), ("mesa", "dos")]),
]

# (titulo, coleccion, palabras, conclusion esperada)
EJEMPLOS_REVISAR = [
    ("E2 cuenta correcta", "a,b,c", "uno,dos,tres", "correcta"),
]

DOMINIO_REVISAR = [
    ("D4 TRAMPA: la misma palabra a dos objetos (el error MAS COMUN)",
     "a,b,c", "uno,uno,tres", "palabra_repetida"),

    ("D5 TRAMPA: se salto una palabra de la secuencia",
     "a,b,c", "uno,tres,cuatro", "orden_saltado"),

    ("D6 TRAMPA: un objeto se quedo sin contar",
     "a,b,c", "uno,dos", "faltan_objetos_sin_contar"),

    ("D7 TRAMPA: una palabra que no esta en la secuencia",
     "a,b", "uno,pepito", "palabra_desconocida"),

    ("D7b (MEJORA 6.1): 'once' ya SI es una palabra de la secuencia; pero SALTA el orden",
     "a,b", "uno,once", "orden_saltado"),

    ("D8 TRAMPA: mas palabras que objetos",
     "a,b", "uno,dos,tres", "palabras_de_mas"),

    ("D9 las palabras fuera de orden",
     "a,b", "dos,uno", "orden_saltado"),
]


def correr_contar(casos, saber, etiqueta):
    print("=" * 76)
    print(etiqueta)
    print("=" * 76)
    bien = 0
    for titulo, coleccion, concl_esp, empa_esp in casos:
        r = decidir_2_1_contar(escena_0_2(coleccion), saber)
        concl = r["conclusion"]
        empa = r.get("emparejamiento")
        ok = concl == concl_esp and (empa_esp is None or empa == empa_esp)
        bien += ok
        print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
        if not ok:
            print("       esperado=%s %s" % (concl_esp, empa_esp))
            print("       obtenido=%s %s" % (concl, empa))
    print("-- %d/%d correctos\n" % (bien, len(casos)))
    return bien, len(casos)


def correr_revisar(casos, saber, etiqueta):
    print("=" * 76)
    print(etiqueta)
    print("=" * 76)
    bien = 0
    for titulo, coleccion, palabras, concl_esp in casos:
        ws = [p.strip() for p in palabras.split(",") if p.strip()]
        r = decidir_2_1_revisar(escena_0_2(coleccion), ws, saber)
        concl = r["conclusion"]
        ok = concl == concl_esp
        bien += ok
        print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
        if not ok:
            print("       esperado=%s  obtenido=%s" % (concl_esp, concl))
    print("-- %d/%d correctos\n" % (bien, len(casos)))
    return bien, len(casos)


def correr_robustez(saber):
    print("=" * 76)
    print("C) ROBUSTEZ - lo escrito mal se dice, no revienta")
    print("=" * 76)
    entradas = [
        "contar: ",
        "revisar: a,b,c / ",
        "revisar: / uno,dos",
        "revisar: a,b,c uno,dos,tres",
    ]
    bien = 0
    for e in entradas:
        try:
            salida = explicar_pregunta(e, saber)
            ok = isinstance(salida, str) and salida.strip() != ""
            bien += ok
            print("%-6s %r -> %s" % ("OK" if ok else "FALLA", e, salida.splitlines()[0][:60]))
        except Exception as ex:
            print("FALLA  reviento con %r -> %r" % (e, ex))
    print("-- %d/%d correctos\n" % (bien, len(entradas)))
    return bien, len(entradas)


def main():
    saber = cargar_conocimiento()
    a1 = correr_contar(EJEMPLOS_CONTAR, saber, "A) CONTAR - casos de ejemplo")
    b1 = correr_contar(DOMINIO_CONTAR, saber, "B) CONTAR - prueba de dominio (no programados)")
    a2 = correr_revisar(EJEMPLOS_REVISAR, saber, "A) REVISAR - casos de ejemplo")
    b2 = correr_revisar(DOMINIO_REVISAR, saber, "B) REVISAR - prueba de dominio (no programados)")
    rb = correr_robustez(saber)

    print("=" * 76)
    print("TRAZA DE LA TRAMPA PRINCIPAL (D4: la misma palabra a dos objetos)")
    print("=" * 76)
    print(explicar_2_1_revisar(escena_0_2("a,b,c"), ["uno", "uno", "tres"], saber))
    print()

    ok = a1[0] + b1[0] + a2[0] + b2[0] + rb[0]
    total = a1[1] + b1[1] + a2[1] + b2[1] + rb[1]
    print("TOTAL: %d/%d" % (ok, total))
    if ok != total:
        print("RESULTADO: ROJO")
        return 1
    print("RESULTADO: VERDE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
