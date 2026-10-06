# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO S.1: "VECES" Y FRACCIONES PARA COMPARAR (NCETM 2.17; 4.OA.A.1-2).
El plan y sus trampas: diario/2026-10-07-paso-S1-veces.md
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
TMP = tempfile.mkdtemp(prefix="s1_")
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


print("=" * 78)
print("PASO S.1 - VECES Y FRACCIONES PARA COMPARAR  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRAMPAS DEL PLAN")
    comprobar("A1 4 veces 6 -> 24 (no 10)", S("veces: 4 veces 6"), "24")
    t = motor.explicar_pregunta("veces: 4 veces 6", SABER)
    comprobar("A2 ... y avisa: 4 veces mas no es 4 mas", "NO es 4 mas" in t, True)
    comprobar("A3 cuantas veces 24 y 6 -> 4;  25 y 6 -> no entero",
              (S("cuantas veces: 24 y 6"), S("cuantas veces: 25 y 6")), ("4", "no_entero"))
    comprobar("A4 la larga: 6 cm y 4 veces mas larga -> 24 cm",
              S("La cuerda roja mide 6 cm. La azul es 4 veces mas larga. Cuanto mide la azul?"), "24 cm")
    comprobar("A5 la corta: 24 cm es 4 veces la roja -> 6 cm (no 96 ni 20)",
              S("La azul mide 24 cm. Es 4 veces mas larga que la roja. Cuanto mide la roja?"), "6 cm")
    comprobar("A6 la fraccion: 1/4 de 24 -> 6 cm",
              S("La azul mide 24 cm. La roja mide 1/4 de la azul. Cuanto mide la roja?"), "6 cm")
    comprobar("A7 cuantas veces mas larga: 24 y 6 -> 4 veces",
              S("La azul mide 24 cm y la roja 6 cm. Cuantas veces es mas larga la azul?"), "4 veces")
    comprobar("A8 los problemas de R.1 siguen igual", S("Ana tiene 5 manzanas. Le dan 3. Cuantas tiene ahora?"), "8")

    print("\nB - LOS CUATRO TIPOS (muestra) CONTRA EL TESTIGO")
    rnd = random.Random(217)
    malos = []
    for _ in range(40):
        k, c = rnd.randint(2, 9), rnd.randint(1, 20)
        g = k * c
        casos = [
            ("La cuerda roja mide %d cm. La azul es %d veces mas larga. Cuanto mide la azul?" % (c, k), "%d cm" % g),
            ("La azul mide %d cm. Es %d veces mas larga que la roja. Cuanto mide la roja?" % (g, k), "%d cm" % c),
            ("La azul mide %d cm. La roja mide 1/%d de la azul. Cuanto mide la roja?" % (g, k), "%d cm" % c),
            ("La azul mide %d cm y la roja %d cm. Cuantas veces es mas larga la azul?" % (g, c), "%d veces" % k),
        ]
        for q, e in casos:
            if S(q) != e:
                malos.append((q, S(q), e))
    comprobar("B1 160 problemas", malos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("-" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
