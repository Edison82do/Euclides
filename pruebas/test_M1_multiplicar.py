# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.1: MULTIPLICAR = GRUPOS IGUALES (3.OA.A.1; NCETM 2.2).
El plan y sus trampas: diario/2026-10-05-paso-M1-multiplicar.md
Python (a * b) solo aparece aqui como TESTIGO externo: el sistema suma grupos iguales.
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
TMP = tempfile.mkdtemp(prefix="por_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia
import motor  # noqa: E402
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
M = lambda t: motor.decidir_multiplicar(t, SABER)     # noqa: E731

print("=" * 78)
print("PASO M.1 - MULTIPLICAR = GRUPOS IGUALES  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - a x b SON a GRUPOS DE b (3.OA.A.1)")
    comprobar("A1 3 x 4 = 12", M("3 x 4")["valor"], 12)
    comprobar("A2 5 x 7 = 35 (el ejemplo del estandar)", M("5 x 7")["valor"], 35)
    comprobar("A3 se escribe x, el aspa o el asterisco, o con palabras",
              [M(t)["valor"] for t in ("3 x 4", "3 × 4", "3 * 4", "3 grupos de 4")], [12, 12, 12, 12])
    r = M("3 x 4")
    comprobar("A4 no hay cuenta nueva: es la suma de iguales de M.0",
              r["aplicado"]["resultado"]["pasos"] and r["aplicado"]["pieza"]["usa"], ["suma_de_iguales"])
    t = motor.explicar_pregunta("3 x 4", SABER)
    comprobar("A5 dice que es cada numero (NCETM 2.2: cuantos grupos y cuantos en cada uno)",
              "el 3 dice CUANTOS GRUPOS; el 4, CUANTOS HAY EN CADA UNO" in t, True)
    comprobar("A6 dibuja los grupos y escribe la suma repetida",
              ("(o o o o)  (o o o o)  (o o o o)" in t, "4 + 4 + 4" in t), (True, True))

    print("\nB - GRUPOS DE CERO Y DE UNO (NCETM 2.2, punto 5)")
    comprobar("B1 4 x 0 = 0 y 0 x 4 = 0", (M("4 x 0")["valor"], M("0 x 4")["valor"]), (0, 0))
    comprobar("B2 4 x 1 = 4 y 1 x 4 = 4", (M("4 x 1")["valor"], M("1 x 4")["valor"]), (4, 4))

    print("\nC - GRUPOS DESIGUALES (NCETM 2.2, punto 1)")
    r = M("grupos de 2, 3 y 4")
    comprobar("C1 grupos de 2, 3 y 4: desiguales, se suman: 9", (r["conclusion"], r["valor"]), ("desiguales", 9))
    r = M("grupos de 4, 4 y 4")
    comprobar("C2 grupos de 4, 4 y 4: son iguales -> 3 x 4", (r["conclusion"], r["a"], r["b"], r["valor"]),
              ("hecho", 3, 4, 12))

    print("\nD - LAS TRAMPAS")
    r = M("5 x 2")
    comprobar("D1 5 x 2 = 10 (en M.1 saltando de 2 en 2; desde M.2, el doble de 5)",
              (r["valor"], r["aplicado"]["pieza"]["id"]), (10, "multiplicar_con_dobles"))
    comprobar("D2 40 x 30: pasa de mil -> no se puede", M("40 x 30")["conclusion"], "no_se_puede")
    comprobar("D3 3 x ? = 12: todavia no (dividir)", motor.decidir_ecuacion("3 x ? = 12", SABER)["conclusion"], "todavia_no")
    comprobar("D4 3 x 4 = ? ya no se lee como '4 = ?' (una puerta que habria mentido)",
              motor.decidir_ecuacion("3 x 4 = ?", SABER)["conclusion"], "todavia_no")

    print("\nE - CONTRA EL TESTIGO")
    fallos = [(a, b) for a in range(0, 11) for b in range(0, 11) if M("%d x %d" % (a, b))["valor"] != a * b]
    comprobar("E1 todas las de 0 a 10 por 0 a 10 (121)", fallos[:3], [])
    azar = random.Random(20261005)
    fallos, n = [], 0
    while n < 150:
        a, b = azar.randint(0, 60), azar.randint(0, 200)
        if a * b > 1000:
            continue
        n += 1
        if M("%d x %d" % (a, b))["valor"] != a * b:
            fallos.append((a, b))
    comprobar("E2 una muestra hasta mil (150)", fallos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
