# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.11: LA DIVISION CORTA (NCETM 2.15; 4.NBT.B.6).
El plan y sus trampas: diario/2026-10-06-paso-M11-division-corta.md
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
TMP = tempfile.mkdtemp(prefix="m11_")
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


def DC(t, d):
    r = motor.aplicar("division_corta", {"total": t, "divisor": d}, SABER)
    if r["conclusion"] != "hecho":
        return r["conclusion"]
    return (r["valor"], r["resultado"]["resto"], r["resultado"]["vuelta_ok"])


print("=" * 78)
print("PASO M.11 - LA DIVISION CORTA  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - SIN LAS TABLAS NO SE USA")
    comprobar("A1 corta: 72 : 3 sin memoria -> no se puede", S("corta: 72 : 3"), "no_se_puede")
    comprobar("A2 ... pero 72 : 3 se divide de otra manera", S("72 : 3"), "24")
    motor.aprender("tablas", SABER)

    print("\nB - LAS TRAMPAS DEL PLAN")
    t = motor.explicar_pregunta("corta: 72 : 3", SABER)
    comprobar("B1 72 : 3 -> 24, cambiando la decena que sobra",
              (t.strip().splitlines()[-1], "sobra 1 decena: se CAMBIA por 10 unidades" in t), ("RESULTADO: 24", True))
    comprobar("B2 84 : 4 -> 21;  96 : 8 -> 12;  75 : 4 -> 18 resto 3",
              (DC(84, 4), DC(96, 8), DC(75, 4)), ((21, 0, True), (12, 0, True), (18, 3, True)))
    t = motor.explicar_pregunta("corta: 305 : 5", SABER)
    comprobar("B3 305 : 5 -> 61 (las 3 centenas pasan a decenas)",
              (t.strip().splitlines()[-1], "no da ni una para cada uno" in t), ("RESULTADO: 61", True))
    comprobar("B4 4321 : 7 -> 617 resto 2;  100 : 7 -> 14 resto 2", (DC(4321, 7), DC(100, 7)), ((617, 2, True), (14, 2, True)))
    comprobar("B5 72 : 3 normal ya va por la corta", motor.aplicar("dividir", {"total": 72, "divisor": 3}, SABER)["pieza"]["id"],
              "division_corta")

    print("\nC - MUESTRAS CONTRA EL TESTIGO, CON LA VUELTA")
    malos = []
    for d in range(2, 10):
        for t in range(10, 1000, 7):
            if DC(t, d) != (t // d, t % d, True):
                malos.append((t, d, DC(t, d)))
    comprobar("C1 de 10 a 999 (de 7 en 7) entre 2..9", malos[:3], [])
    rnd = random.Random(215)
    malos = []
    for _ in range(150):
        t, d = rnd.randint(1000, 10000), rnd.randint(2, 9)
        if DC(t, d) != (t // d, t % d, True):
            malos.append((t, d, DC(t, d)))
    comprobar("C2 150 de cuatro cifras", malos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("-" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
