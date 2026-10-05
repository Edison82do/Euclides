# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 5.1 - COMPONER Y DESCOMPONER.

Lo que esta unidad tiene que dejar claro:
  - DESCOMPONER: partir una coleccion en DOS partes, TODAS las maneras.
  - COMPONER:    juntar dos partes y decir el TODO.
  - NO se repite la pareja al reves: 2+3 y 3+2 son LA MISMA (el orden no importa, unidad 2.5).
  - El CERO es una parte valida (0+5), pero el cero NO se puede partir.
  - Y la IDA Y LA VUELTA cuadran: juntar lo que se ha partido devuelve el todo.

Se corre asi:   py -3 pruebas/test_5_1.py
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

from motor import (cargar_conocimiento, decidir_5_1_componer, decidir_5_1_descomponer,  # noqa: E402
                   escena_0_2, explicar_pregunta)

BIEN = [0]
TOTAL = [0]

# UNIDAD 6.1: la secuencia llega a 100, asi que hacen falta nombres hasta 120 para poder
# probar que "pasa de cien" de verdad (antes bastaba con diez).
NOMBRES = ["o%d" % i for i in range(1, 121)]


def comprobar(titulo, obtenido, esperado):
    ok = obtenido == esperado
    BIEN[0] += ok
    TOTAL[0] += 1
    print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
    if not ok:
        print("       esperado=%s  obtenido=%s" % (esperado, obtenido))
    return ok


def coleccion(n):
    return escena_0_2(",".join(NOMBRES[:n]))


def main():
    saber = cargar_conocimiento()

    # ------------------------------------------------------------------ descomponer
    print("=" * 76)
    print("A) DESCOMPONER: todas las maneras de partir en DOS")
    print("=" * 76)
    r = decidir_5_1_descomponer(coleccion(5), saber)
    comprobar("A1 cinco se parte de TRES maneras", r["cuantas_maneras"], 3)
    comprobar("A2 y son las del NCETM: 0+5, 1+4, 2+3", r["parejas"], [(0, 5), (1, 4), (2, 3)])
    r = decidir_5_1_descomponer(coleccion(4), saber)
    comprobar("A3 cuatro: 0+4, 1+3, 2+2", r["parejas"], [(0, 4), (1, 3), (2, 2)])
    r = decidir_5_1_descomponer(coleccion(1), saber)
    comprobar("A4 uno solo se parte de UNA manera (0+1)", r["parejas"], [(0, 1)])
    r = decidir_5_1_descomponer(coleccion(10), saber)
    comprobar("A5 diez se parte de SEIS maneras", r["cuantas_maneras"], 6)
    print("")

    # ------------------------------------------------------------------ no repite el orden
    print("=" * 76)
    print("B) NO SE REPITE LA PAREJA AL REVES (el orden no importa, unidad 2.5)")
    print("=" * 76)
    problemas = 0
    for n in range(1, 11):
        parejas = set(decidir_5_1_descomponer(coleccion(n), saber)["parejas"])
        for (a, b) in parejas:
            if (b, a) in parejas and a != b:
                problemas += 1
    comprobar("B1 ninguna pareja aparece tambien del reves", problemas, 0)
    r = decidir_5_1_descomponer(coleccion(5), saber)
    comprobar("B2 (por eso 5 tiene 3 maneras y no 6)", len(r["parejas"]), 3)
    comprobar("B3 y el sistema LO EXPLICA",
              "NO REPITO LA PAREJA AL REVES" in explicar_pregunta("descomponer: a,b,c,d,e", saber), True)
    print("")

    # ------------------------------------------------------------------ el cero
    print("=" * 76)
    print("C) EL CERO: parte valida, pero no se parte")
    print("=" * 76)
    r = decidir_5_1_descomponer(coleccion(3), saber)
    comprobar("C1 el cero es una parte valida: esta '0 y 3'", (0, 3) in r["parejas"], True)
    r = decidir_5_1_descomponer(escena_0_2(""), saber)
    comprobar("C2 TRAMPA: el cero NO se puede partir", r["conclusion"], "el_cero_no_se_parte")
    salida = explicar_pregunta("descomponer:", saber)
    comprobar("C3 y distingue las dos cosas (parte / todo)",
              "NO un TODO" in salida or "no un TODO" in salida, True)
    print("")

    # ------------------------------------------------------------------ componer
    print("=" * 76)
    print("D) COMPONER: juntar las partes")
    print("=" * 76)
    r = decidir_5_1_componer(coleccion(2), coleccion(3), saber)
    comprobar("D1 dos y tres son cinco", r.get("total"), "cinco")
    comprobar("D2 y con las cifras: 2 y 3 son 5", r.get("total_cifra"), "5")
    r = decidir_5_1_componer(coleccion(3), coleccion(2), saber)
    comprobar("D3 al reves tambien: tres y dos son cinco (conmutatividad)", r.get("total"), "cinco")
    r = decidir_5_1_componer(coleccion(0), coleccion(4), saber)
    comprobar("D4 vacio y cuatro son cuatro (el cero es una parte)", r.get("total"), "cuatro")
    r = decidir_5_1_componer(coleccion(0), coleccion(0), saber)
    comprobar("D5 dos vacios son cero", r.get("total"), "cero")
    print("")

    # ------------------------------------------------------------------ LA IDA Y LA VUELTA
    print("=" * 76)
    print("E) LA PRUEBA DE HIERRO: la vuelta cuadra con la ida")
    print("=" * 76)
    # Para cada n (1..10) y CADA pareja de su descomposicion, juntarlas tiene que devolver n.
    malas = 0
    probadas = 0
    for n in range(1, 11):
        d = decidir_5_1_descomponer(coleccion(n), saber)
        for (a, b) in d["parejas"]:
            c = decidir_5_1_componer(coleccion(a), coleccion(b), saber)
            probadas += 1
            if c.get("total") != d["total"]:
                malas += 1
                print("       NO CUADRA: %d = %d + %d -> juntando sale %s (deberia ser %s)"
                      % (n, a, b, c.get("total"), d["total"]))
    comprobar("E1 las %d parejas de 1..10, juntadas, devuelven su todo" % probadas, malas, 0)
    comprobar("E2 y son 35 parejas probadas (1+2+2+3+3+4+4+5+5+6)", probadas, 35)
    salida = explicar_pregunta("descomponer: a,b,c,d,e", saber)
    comprobar("E3 el sistema declara la verificacion", "VERIFICACION (por la vuelta)" in salida, True)
    print("")

    # ------------------------------------------------------------------ limites
    print("=" * 76)
    print("F) LIMITES Y TRAMPAS")
    print("=" * 76)
    r = decidir_5_1_descomponer(escena_0_2(",".join("o%d" % i for i in range(1, 1002))), saber)
    # UNIDAD 6.1: once objetos YA se cuentan y 6+6 = doce ya se puede; el limite esta en cien.
    comprobar("F1 TRAMPA: mas de MIL objetos -> no_alcanza", r["conclusion"], "no_alcanza")
    r = decidir_5_1_componer(coleccion(6), coleccion(6), saber)
    comprobar("F2 (MEJORA 6.1): SEIS Y SEIS ya SI se juntan -> doce (antes no llegaba)",
              r.get("total"), "doce")
    # UNIDAD 6.7: el techo subio a MIL; 60+60 ya se puede.
    # (con nombres GENERADOS: la lista fija de arriba es corta)
    r = decidir_5_1_componer(escena_0_2(",".join("o%d" % (i + 1) for i in range(600))), escena_0_2(",".join("o%d" % (i + 1) for i in range(600))), saber)
    comprobar("F2b TRAMPA: seiscientos y seiscientos (1200) pasa de MIL -> no_alcanza",
              r["conclusion"], "no_alcanza")
    salida = explicar_pregunta("componer: a,b,c", saber)
    comprobar("F3 sin la barra -> NO ENTIENDO (hacen falta DOS partes)", "NO ENTIENDO" in salida, True)
    print("")

    # ------------------------------------------------------------------ identidad (0.1)
    print("=" * 76)
    print("G) PASA POR LA IDENTIDAD (unidad 0.1)")
    print("=" * 76)
    r = decidir_5_1_descomponer(escena_0_2("casa(color=rojo), casa(forma=cuadrado), carro"), saber)
    comprobar("G1 la casa repetida es UNA: son 2 objetos, no 3", r["cuantas_maneras"], 2)
    comprobar("G2 y el todo es 'dos'", r["total"], "dos")
    print("")

    # ------------------------------------------------------------------ robustez
    print("=" * 76)
    print("H) ROBUSTEZ: contesta a todo, no revienta")
    print("=" * 76)
    for q in ["descomponer:", "descomponer: a", "descomponer: o1,o2,o3,o4,o5,o6,o7,o8,o9,o10",
              "componer: / ", "componer: a / b", "componer: / a,b",
              "descomponer: casa(color=rojo), casa"]:
        salida = explicar_pregunta(q, saber)
        comprobar("H '%s'" % q[:38], ("RESULTADO:" in salida or "NO ENTIENDO" in salida), True)
    print("")

    print("=" * 76)
    print("UNIDAD 5.1: %d/%d correctos" % (BIEN[0], TOTAL[0]))
    print("=" * 76)
    return 0 if BIEN[0] == TOTAL[0] else 1


if __name__ == "__main__":
    sys.exit(main())
