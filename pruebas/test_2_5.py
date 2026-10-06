# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 2.5 - EL ORDEN NO IMPORTA (el de los objetos; el de las palabras si).

Lo que esta unidad tiene que dejar claro:
  - Hay DOS clases de reglas: LOGICAS (obligatorias: 1-a-1, orden de las palabras, cardinalidad) y
    CONVENCIONALES (opcionales: por donde empiezas, en que direccion vas).
  - PSEUDOERROR (Gelman & Meck): un conteo que solo rompe una regla convencional -> es VALIDO,
    aunque empiece por donde quiera.  (Caso real de los estudios: contar primero los balones de
    futbol y luego los de baloncesto, intercalados en la fila.)
  - COMPENSACION: saltarse uno y contar otro dos veces -> INVALIDO, aunque el total cuadre, porque
    la correspondencia uno a uno esta rota.

  A) CASOS DE EJEMPLO  - los del conocimiento.
  B) CASOS DE DOMINIO  - no programados, con trampas.
  C) ROBUSTEZ          - lo mal escrito se dice, no revienta.

Uso:  python pruebas/test_2_5.py
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

from motor import (cargar_conocimiento, decidir_2_5_conteo,  # noqa: E402
                   decidir_2_5_orden, escena_0_2, explicar_pregunta)


# (titulo, coleccion, conclusion esperada)
EJEMPLOS_ORDEN = [
    ("E1 tres objetos en dos ordenes -> coinciden", "a,b,c", "coinciden"),
]

DOMINIO_ORDEN = [
    ("D1 un solo objeto -> coinciden", "cosa", "coinciden"),

    ("D2 cinco objetos -> coinciden", "a,b,c,d,e", "coinciden"),

    ("D3 diez objetos -> coinciden", "a,b,c,d,e,f,g,h,i,j", "coinciden"),

    ("D4 TRAMPA: mas objetos que la lista (N.3: diez mil) -> no puede decidirlo",
     ",".join("o%d" % (i + 1) for i in range(10001)), "no_alcanza_la_secuencia"),

    ("D4b (MEJORA 6.1): ONCE objetos ya SI se pueden decidir",
     ",".join("o%d" % (i + 1) for i in range(11)), "coinciden"),

    ("D5 TRAMPA: la casa repetida es UNA casa, y el orden sigue sin importar",
     "casa(color=blanco), casa(forma=cuadrado)", "coinciden"),
]

# (titulo, recorrido, palabras, conclusion esperada)
EJEMPLOS_CONTEO = [
    ("E2 recorrido normal y bien dicho -> valido", "a,b,c", "uno,dos,tres", "valido"),
]

DOMINIO_CONTEO = [
    ("D6 TRAMPA (PSEUDOERROR): empieza por el tercero -> SIGUE siendo valido",
     "c,a,b", "uno,dos,tres", "valido"),

    ("D7 TRAMPA (PSEUDOERROR, el caso de los estudios): cuenta primero los cinco de un color y "
     "luego los otros cinco, intercalados en la fila -> VALIDO",
     "f1,f2,f3,f4,f5,b1,b2,b3,b4,b5",
     "uno,dos,tres,cuatro,cinco,seis,siete,ocho,nueve,diez", "valido"),

    ("D7-bis TRAMPA: con mas objetos que palabras, los ultimos quedan sin contar",
     "f1,f2,f3,f4,f5,b1,b2,b3,b4,b5,b6",
     "uno,dos,tres,cuatro,cinco,seis,siete,ocho,nueve,diez", "faltan_objetos_sin_contar"),

    ("D8 TRAMPA (COMPENSACION): se salta uno y cuenta otro dos veces -> INVALIDO aunque el total "
     "cuadre",
     "a,b,b,c", "uno,dos,tres,cuatro", "objeto_repetido"),

    ("D9 TRAMPA (COMPENSACION): el mismo objeto al principio y al final",
     "a,b,c,a", "uno,dos,tres,cuatro", "objeto_repetido"),

    ("D10 TRAMPA: la misma palabra dos veces -> palabra_repetida",
     "a,b,c", "uno,dos,dos", "palabra_repetida"),

    ("D11 TRAMPA: se salto el dos -> orden_saltado",
     "a,b,c", "uno,tres,cuatro", "orden_saltado"),

    ("D12 TRAMPA: mas palabras que objetos -> palabras_de_mas",
     "a,b", "uno,dos,tres", "palabras_de_mas"),

    ("D13 TRAMPA: menos palabras que objetos -> faltan_objetos_sin_contar",
     "a,b,c", "uno,dos", "faltan_objetos_sin_contar"),

    ("D14 (MEJORA 6.1): 'once' ya SI esta en la lista; pero SALTA el orden",
     "a,b", "uno,once", "orden_saltado"),

    ("D14b TRAMPA: una palabra que no esta en la lista -> palabra_desconocida",
     "a,b", "uno,pepito", "palabra_desconocida"),

    ("D15 el recorrido entero al reves, bien dicho -> valido",
     "e,d,c,b,a", "uno,dos,tres,cuatro,cinco", "valido"),
]


def correr_orden(saber):
    print("=" * 76)
    print("A/B) ORDEN: contar la coleccion de dos maneras")
    print("=" * 76)
    bien = 0
    casos = EJEMPLOS_ORDEN + DOMINIO_ORDEN
    for titulo, coleccion, concl_esp in casos:
        r = decidir_2_5_orden(escena_0_2(coleccion), saber)
        ok = r["conclusion"] == concl_esp and (concl_esp != "coinciden" or r.get("coinciden"))
        bien += ok
        print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
        if not ok:
            print("       esperado=%s  obtenido=%s coinciden=%s"
                  % (concl_esp, r["conclusion"], r.get("coinciden")))
    print("-- %d/%d correctos\n" % (bien, len(casos)))
    return bien, len(casos)


def correr_conteo(saber):
    print("=" * 76)
    print("A/B) CONTEO: juzgar un recorrido  (pseudoerror vs compensacion)")
    print("=" * 76)
    bien = 0
    casos = EJEMPLOS_CONTEO + DOMINIO_CONTEO
    for titulo, recorrido, palabras, concl_esp in casos:
        ws = [p.strip() for p in palabras.split(",") if p.strip()]
        r = decidir_2_5_conteo(escena_0_2(recorrido), ws, saber)
        ok = r["conclusion"] == concl_esp
        bien += ok
        print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
        if not ok:
            print("       esperado=%s  obtenido=%s" % (concl_esp, r["conclusion"]))
    print("-- %d/%d correctos\n" % (bien, len(casos)))
    return bien, len(casos)


def correr_varios_ordenes(saber):
    """El mismo conjunto de cinco, contado en orden, al reves, y barajado: siempre cinco."""
    print("=" * 76)
    print("C) MUCHOS ORDENES: el mismo conjunto barajado de varias formas -> siempre lo mismo")
    print("=" * 76)
    ordenes = ["a,b,c,d,e", "e,d,c,b,a", "c,e,a,d,b", "b,d,a,c,e"]
    bien = 0
    for o in ordenes:
        r = decidir_2_5_orden(escena_0_2(o), saber)
        ok = r["conclusion"] == "coinciden" and r.get("coinciden")
        bien += ok
        print("%-6s %-14s -> %s (%s)" % ("OK" if ok else "FALLA", o, r["conclusion"],
                                         r.get("cantidad_derecho")))
    print("-- %d/%d correctos\n" % (bien, len(ordenes)))
    return bien, len(ordenes)


def correr_robustez(saber):
    print("=" * 76)
    print("D) ROBUSTEZ - lo escrito mal se dice, no revienta")
    print("=" * 76)
    entradas = ["orden:", "orden: ", "conteo:", "conteo: a,b /", "conteo: / uno,dos",
                "conteo: a,b", "conteo: caja(colorrojo) / uno"]
    bien = 0
    for e in entradas:
        try:
            salida = explicar_pregunta(e, saber)
            ok = isinstance(salida, str) and salida.strip() != ""
            bien += ok
            print("%-6s %r -> %s" % ("OK" if ok else "FALLA", e, salida.splitlines()[0][:50]))
        except Exception as ex:
            print("FALLA  reviento con %r -> %r" % (e, ex))
    print("-- %d/%d correctos\n" % (bien, len(entradas)))
    return bien, len(entradas)


def main():
    saber = cargar_conocimiento()
    a = correr_orden(saber)
    b = correr_conteo(saber)
    c = correr_varios_ordenes(saber)
    d = correr_robustez(saber)

    print("=" * 76)
    print("TRAZA DE LA TRAMPA PRINCIPAL (el pseudoerror: empezar por donde quiera)")
    print("=" * 76)
    print(explicar_pregunta("conteo: c,a,b / uno,dos,tres", saber))
    print()
    print("=" * 76)
    print("TRAZA DE LA COMPENSACION (se salta uno y cuenta otro dos veces)")
    print("=" * 76)
    print(explicar_pregunta("conteo: a,b,b,c / uno,dos,tres,cuatro", saber))
    print()

    ok = a[0] + b[0] + c[0] + d[0]
    total = a[1] + b[1] + c[1] + d[1]
    print("TOTAL: %d/%d" % (ok, total))
    if ok != total:
        print("RESULTADO: ROJO")
        return 1
    print("RESULTADO: VERDE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
