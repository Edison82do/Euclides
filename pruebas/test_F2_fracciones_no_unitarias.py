# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO F.2: FRACCIONES NO UNITARIAS; EN LA RECTA; COMPARAR (NCETM 3.3; 3.NF.A.2, A.3c, A.3d).
El plan y sus trampas: diario/2026-10-06-paso-F2-fracciones-no-unitarias.md
Python solo aparece aqui como TESTIGO externo.
"""
import os
import random
import shutil
import sys
import tempfile
from fractions import Fraction

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)
TMP = tempfile.mkdtemp(prefix="f2_")
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
    return probar.preguntar(t, SABER)[0]


def signo(x, y):
    return ">" if x > y else "<" if x < y else "="


print("=" * 78)
print("PASO F.2 - FRACCIONES NO UNITARIAS; EN LA RECTA; COMPARAR  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRAMPAS DEL PLAN")
    comprobar("A1 fraccion: 3/4 -> tres cuartos", S("fraccion: 3/4"), "tres cuartos")
    comprobar("A2 fraccion: 4/4 -> un entero", S("fraccion: 4/4"), "un entero")
    comprobar("A3 fraccion: 5/4 -> desde F.4 (4.o) si: cinco cuartos = 1 1/4", S("fraccion: 5/4"), "cinco cuartos = 1 1/4")
    comprobar("A4 fraccion: 0/4 -> cero;  3/1 -> 3 enteros", (S("fraccion: 0/4"), S("fraccion: 3/1")), ("cero", "3 enteros"))
    comprobar("A5 comparar 2/5 y 3/5 -> 3/5 mayor", S("comparar: 2/5 y 3/5"), "2/5 < 3/5")
    comprobar("A6 comparar 2/3 y 2/5 -> 2/3 mayor (no 'cinco es mas')", S("comparar: 2/3 y 2/5"), "2/3 > 2/5")
    comprobar("A7 comparar 2/3 y 3/5 -> todavia no (5.o)", S("comparar: 2/3 y 3/5"), "todavia_no")
    comprobar("A8 3/4 de 12 -> 9", S("3/4 de 12"), "9")
    comprobar("A9 2/3 de 10 -> no sale justo", S("2/3 de 10"), "no_sale")
    comprobar("A10 entero: 3/4 es 9 -> 12;  es 10 -> no sale",
              (S("entero: 3/4 es 9"), S("entero: 3/4 es 10")), ("12", "no_sale"))
    comprobar("A11 recta: 3/4 -> a tres trozos", S("recta: 3/4"), "a tres trozos de 1/4 del 0")
    t = motor.explicar_pregunta("recta: 3/4", SABER)
    comprobar("A12 la recta se dibuja: 0 ... 1 y la marca bajo el tercer palito",
              ("|----|----|----|----|" in t, "               ^" in t), (True, True))
    t = motor.explicar_pregunta("fraccion: 3/4", SABER)
    comprobar("A13 3/4 = 1/4 + 1/4 + 1/4", "1/4 + 1/4 + 1/4  (NCETM 3.3)" in t, True)

    print("\nB - COMPARAR: TODAS LAS PAREJAS QUE COMPARTEN ARRIBA O ABAJO (b de 2 a 12, a <= b)")
    fr = [(a, b) for b in range(2, 13) for a in range(1, b + 1)]
    malos, n, otras = [], 0, 0
    for x in fr:
        for y in fr:
            r = motor.decidir_comparar_fracciones(x, y, SABER)
            if x[0] == y[0] or x[1] == y[1]:
                n += 1
                esperado = signo(Fraction(*x), Fraction(*y))
                if r["conclusion"] != "hecho" or r["valor"] != esperado or len(r["todos"]) < 2:
                    malos.append((x, y, r.get("valor"), esperado))
            else:
                otras += 1
                if r["conclusion"] == "hecho":
                    malos.append((x, y, "se atrevio", r.get("valor")))
    comprobar("B1 %d parejas bien, con dos caminos o mas; %d sin nada en comun -> no se atreve" % (n, otras),
              malos[:3], [])

    print("\nC - a/b DE n (muestra)")
    rnd = random.Random(32)
    malos = []
    casos = [(a, b, b * k) for b in range(2, 13) for a in (1, 2, b - 1, b) for k in (0, 1, 3, 7, 10)] + \
            [(rnd.randint(1, 12), rnd.randint(2, 12), rnd.randint(1, 150)) for _ in range(120)]
    for a, b, n in casos:
        if a > b:
            continue
        r = motor.decidir_fraccion_de(a, b, n, SABER)
        esperado = a * n // b if n % b == 0 else "no_sale"
        obtenido = r.get("valor") if r["conclusion"] == "hecho" else r["conclusion"]
        if obtenido != esperado:
            malos.append((a, b, n, obtenido, esperado))
    comprobar("C1 a/b de n: repartir y tomar a partes", malos[:3], [])

    print("\nD - EL ENTERO DESDE UNA PARTE NO UNITARIA")
    malos = []
    for b in range(2, 13):
        for a in range(1, b + 1):
            for una in (1, 2, 5):
                r = motor.decidir_entero(a, b, a * una, SABER)
                if r.get("valor") != b * una:
                    malos.append((a, b, a * una, r.get("valor")))
    comprobar("D1 a/b es a x u -> el entero es b x u", malos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("-" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
