# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 3.2 - EL CERO (ninguno).

Lo que esta unidad tiene que dejar claro:
  - La cantidad de un conjunto VACIO es CERO.  Y su cifra es 0.
  - ANTES el sistema decia "no_decidible" cuando no habia nada; AHORA responde cero.  No se
    equivocaba: le faltaba el cero.  Aprenderlo ha AMPLIADO lo que sabe.
  - LA TRAMPA: cero NO es "no se sabe".  Cero es una cantidad.
  - Donde NO llega: el cero POSICIONAL (el 0 de 10) es del Sistema Decimal, otra unidad.

  A) CASOS DE EJEMPLO  - los del conocimiento.
  B) CASOS DE DOMINIO  - no programados, con trampas.
  C) LIMITES DECLARADOS - lo que esta unidad NO cambia, a proposito.
  D) ROBUSTEZ          - lo mal escrito se dice, no revienta.

Uso:  python pruebas/test_3_2.py
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

from motor import (cargar_conocimiento, decidir_2_3_cuantos, decidir_2_4_tiene,  # noqa: E402
                   decidir_2_6_misma_cantidad, decidir_3_1_cifra, decidir_3_1_cifra_de,
                   decidir_3_1_palabra, escena_0_2, explicar_pregunta)


def correr(saber):
    print("=" * 76)
    print("A/B) EL CERO: la cantidad de un conjunto vacio")
    print("=" * 76)
    casos = [
        ("E1 cuantos: (vacio) -> cero", lambda: decidir_2_3_cuantos([], saber),
         "cero", "cantidad"),
        ("D1 cifra_de: (vacio) -> 0", lambda: decidir_3_1_cifra_de([], saber),
         "cifra", "cifra"),
        ("D2 cifra: cero -> 0", lambda: decidir_3_1_cifra("cero", saber),
         "cifra", "cifra"),
        ("D3 palabra: 0 -> cero", lambda: decidir_3_1_palabra("0", saber),
         "palabra", "palabra"),
        ("D4 TRAMPA: con UN objeto la cantidad NO es cero, es uno",
         lambda: decidir_2_3_cuantos(escena_0_2("cosa"), saber), "hay_cantidad", "cantidad"),
        ("D5 TRAMPA: con TRES objetos tampoco", lambda: decidir_2_3_cuantos(escena_0_2("a,b,c"), saber),
         "hay_cantidad", "cantidad"),
    ]
    esperados = {"E1 cuantos: (vacio) -> cero": "cero", "D1 cifra_de: (vacio) -> 0": "0",
                 "D2 cifra: cero -> 0": "0", "D3 palabra: 0 -> cero": "cero",
                 "D4 TRAMPA: con UN objeto la cantidad NO es cero, es uno": "uno",
                 "D5 TRAMPA: con TRES objetos tampoco": "tres"}
    bien = 0
    for titulo, fn, concl_esp, campo in casos:
        r = fn()
        valor = r.get(campo)
        ok = r["conclusion"] == concl_esp and valor == esperados[titulo]
        bien += ok
        print("%-6s %-58s -> %s" % ("OK" if ok else "FALLA", titulo, valor))
        if not ok:
            print("       esperado=%s  obtenido=%s %s" % (concl_esp, r["conclusion"], valor))
    print("-- %d/%d correctos\n" % (bien, len(casos)))
    return bien, len(casos)


def correr_limites(saber):
    """
    Lo que esta unidad NO cambia, y esta declarado a proposito: las preguntas que NO son de
    cantidad (tiene N?, son iguales?) siguen diciendo "no_decidible" con una coleccion vacia.
    """
    print("=" * 76)
    print("C) LIMITES DECLARADOS: lo que el cero NO cambia (a proposito)")
    print("=" * 76)
    pruebas = [
        ("tiene: (vacio) / uno -> sigue no_decidible", decidir_2_4_tiene([], "uno", saber),
         "no_decidible"),
        ("misma_cantidad: (vacio) / a -> sigue no_decidible",
         decidir_2_6_misma_cantidad([], escena_0_2("a"), saber), "no_decidible"),
    ]
    bien = 0
    for titulo, r, concl_esp in pruebas:
        ok = r["conclusion"] == concl_esp
        bien += ok
        print("%-6s %-52s -> %s" % ("OK" if ok else "FALLA", titulo, r["conclusion"]))
    print("-- %d/%d correctos\n" % (bien, len(pruebas)))
    print("  (El cero solo entra donde la pregunta ES de cantidad: cuantos hay, y cual es su cifra.)\n")
    return bien, len(pruebas)


def correr_robustez(saber):
    print("=" * 76)
    print("D) ROBUSTEZ - lo escrito mal se dice, no revienta")
    print("=" * 76)
    entradas = ["cuantos:", "cuantos: ", "cifra_de:", "cifra: cero", "palabra: 0",
                "cifra: ", "palabra: 00"]
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
    a = correr(saber)
    c = correr_limites(saber)
    d = correr_robustez(saber)

    print("=" * 76)
    print("TRAZA: una coleccion vacia tiene cantidad cero")
    print("=" * 76)
    print(explicar_pregunta("cuantos:", saber))
    print()

    ok = a[0] + c[0] + d[0]
    total = a[1] + c[1] + d[1]
    print("TOTAL: %d/%d" % (ok, total))
    if ok != total:
        print("RESULTADO: ROJO")
        return 1
    print("RESULTADO: VERDE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
