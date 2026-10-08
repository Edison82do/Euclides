# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO N.5: LOS NUMEROS NEGATIVOS (NCETM 1.27; Common Core 6.NS.C.5-7).
El plan y sus trampas: diario/2026-10-07-paso-N5-negativos.md
Python solo aparece aqui como TESTIGO externo.
"""
import os
import random
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)
TMP = tempfile.mkdtemp(prefix="n5_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia
import motor  # noqa: E402
import probar  # noqa: E402
from _muestras import modo  # noqa: E402

BIEN = MAL = 0


def comprobar(nombre, obtenido, esperado):
    global BIEN, MAL
    if obtenido == esperado:
        BIEN += 1
        print("  bien    %s" % nombre)
    else:
        MAL += 1
        print("  FALLA   %s\n          esperado=%r  obtenido=%r" % (nombre, esperado, obtenido))


SABER = motor.cargar_conocimiento()


def S(t):
    return probar.preguntar(probar.como_problema(t), SABER)[0]


def signo(a, b):
    return ">" if a > b else "<" if a < b else "="


print("=" * 78)
print("PASO N.5 - LOS NUMEROS NEGATIVOS  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRAMPAS DEL PLAN")
    comprobar("A1 -3 > -7 (no -7 > -3 por 'siete es mas que tres')", S("comparar: -3 y -7"), "-3 > -7")
    comprobar("A2 -1 < 0", S("comparar: -1 y 0"), "-1 < 0")
    comprobar("A3 -100 < 2", S("comparar: -100 y 2"), "-100 < 2")
    comprobar("A4 recta: 3 - 8 = -5 (no 5)", S("recta: 3 - 8"), "-5")
    comprobar("A5 recta: -4 + 7 = 3 (no -11 ni 11)", S("recta: -4 + 7"), "3")
    comprobar("A6 recta: -4 - 3 = -7 (no -1)", S("recta: -4 - 3"), "-7")
    comprobar("A7 recta: -6 + 2 = -4", S("recta: -6 + 2"), "-4")
    comprobar("A8 recta: 5 - 5 = 0", S("recta: 5 - 5"), "0")
    comprobar("A9 intervalo: -4 y 7 = 11 (no 3)", S("intervalo: -4 y 7"), "11")
    comprobar("A10 intervalo: -9 y -2 = 7 (no 11)", S("intervalo: -9 y -2"), "7")
    comprobar("A11 3 - 8 SIN la recta: con cosas no se puede", S("3 - 8"), "imposible")
    comprobar("A12 negativo: -5 se lee menos cinco", S("negativo: -5"), "menos cinco")
    comprobar("A13 negativo: 0 no es ni positivo ni negativo", S("negativo: 0"), "cero")

    print("\nB - CONTAR EN LA RECTA CRUZANDO EL CERO")
    comprobar("B1 desde 3 bajando 6", S("recta: desde 3 bajando 6"), "2, 1, 0, -1, -2, -3")
    comprobar("B2 desde -5 subiendo 7", S("recta: desde -5 subiendo 7"), "-4, -3, -2, -1, 0, 1, 2")
    comprobar("B3 desde -9 bajando 3", S("recta: desde -9 bajando 3"), "-10, -11, -12")

    print("\nC - LA TEMPERATURA (el cambio)")
    comprobar("C1 -4 grados, sube 7", S("La temperatura es -4 grados. Sube 7 grados. Cual es ahora?"), "3 grados")
    comprobar("C2 3 grados, baja 8", S("Hace 3 grados y baja 8 grados. Cuantos grados hace?"), "-5 grados")
    comprobar("C3 de -6 a 5: subio 11", S("Por la manana hace -6 grados y a mediodia 5 grados. Cuanto subio?"),
              "11 grados")
    comprobar("C4 'menos 2 grados' con palabras", S("Hace menos 2 grados y baja 5 grados. Cuantos grados hace?"),
              "-7 grados")

    print("\nD - CONTRA EL TESTIGO")
    mal = []
    for a in range(-20, 21):
        for b in range(0, 21):
            for op in "+-":
                esperado = a + b if op == "+" else a - b
                if S("recta: %d %s %d" % (a, op, b)) != str(esperado):
                    mal.append((a, op, b))
    comprobar("D1 todas las de -20..20 mas/menos 0..20 en la recta (1722)", mal[:3], [])
    mal = [(a, b) for a in range(-20, 21) for b in range(-20, 21)
           if (a < 0 or b < 0) and S("comparar: %d y %d" % (a, b)) != "%d %s %d" % (a, signo(a, b), b)]
    comprobar("D2 todas las comparaciones con algun negativo de -20 a 20", mal[:3], [])
    mal = [(a, b) for a in range(-20, 21) for b in range(-20, 21)
           if S("intervalo: %d y %d" % (a, b)) != str(abs(a - b))]
    comprobar("D3 todos los intervalos de -20 a 20", mal[:3], [])
    azar = random.Random(20261007)
    mal = []
    for _ in range(200):
        a, b, op = azar.randint(-1000, 1000), azar.randint(0, 1000), azar.choice("+-")
        if S("recta: %d %s %d" % (a, op, b)) != str(a + b if op == "+" else a - b):
            mal.append((a, op, b))
    comprobar("D4 una muestra hasta +-1000 (200)", mal[:3], [])

    print("\nE - LOS BORDES")
    comprobar("E1 recta: -9999999 - 5: se pasa (N.6; N.4 era -999999 - 5)", S("recta: -9999999 - 5"), "no_alcanza")
    comprobar("E2 lo de siempre no cambia: comparar: 7 y 3", S("comparar: 7 y 3"), "7 > 3")
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
