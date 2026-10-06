# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO F.3: SUMAR Y RESTAR FRACCIONES DENTRO DE UN ENTERO (NCETM 3.4).
El plan y sus trampas: diario/2026-10-06-paso-F3-sumar-restar-fracciones.md
Python solo aparece aqui como TESTIGO externo.
"""
import os
import shutil
import sys
import tempfile
from fractions import Fraction

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)
TMP = tempfile.mkdtemp(prefix="f3_")
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


print("=" * 78)
print("PASO F.3 - SUMAR Y RESTAR FRACCIONES DENTRO DE UN ENTERO  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRAMPAS DEL PLAN")
    comprobar("A1 2/7 + 3/7 -> 5/7 (no 5/14)", S("2/7 + 3/7"), "5/7")
    t = motor.explicar_pregunta("2/7 + 3/7", SABER)
    comprobar("A2 y dice por que el de abajo no se suma", ("NO se suma" in t, "5/14" in t), (True, True))
    comprobar("A3 5/7 - 2/7 -> 3/7", S("5/7 - 2/7"), "3/7")
    comprobar("A4 1 - 3/8 -> 5/8 (1 = 8/8)", S("1 - 3/8"), "5/8")
    comprobar("A5 3/8 + 5/8 -> 1", S("3/8 + 5/8"), "1")
    comprobar("A6 3/8 - 3/8 -> 0", S("3/8 - 3/8"), "0")
    comprobar("A7 4/7 + 5/7 -> desde F.4 pasa de un entero: 1 2/7", S("4/7 + 5/7"), "1 2/7")
    comprobar("A8 2/7 - 5/7 -> imposible", S("2/7 - 5/7"), "imposible")
    comprobar("A9 1/2 + 1/4 -> todavia no (5.o)", S("1/2 + 1/4"), "todavia_no")
    comprobar("A10 la vuelta: 5/7 - 3/7 = 2/7", "5/7 - 3/7 = 2/7 ... SI" in t, True)

    print("\nB - TODAS LAS CUENTAS a/b + c/b y a/b - c/b (b de 2 a 12) CONTRA EL TESTIGO")
    malos, n = [], 0
    for b in range(2, 13):
        for a in range(0, b + 1):
            for c in range(0, b + 1):
                for sg in "+-":
                    v = Fraction(a, b) + Fraction(c, b) if sg == "+" else Fraction(a, b) - Fraction(c, b)
                    r = motor.decidir_cuenta_fracciones((a, b), sg, (c, b), SABER)
                    n += 1
                    if v < 0:
                        esperado = "imposible"
                    else:
                        esperado = (a + c if sg == "+" else a - c, b)
                    obtenido = r["valor"] if r["conclusion"] == "hecho" else r["conclusion"]
                    if obtenido != esperado or (r["conclusion"] == "hecho" and not r["vuelta_ok"]):
                        malos.append((a, sg, c, b, obtenido, esperado))
    comprobar("B1 %d cuentas, con su vuelta" % n, malos[:3], [])

    print("\nC - RESTAR DE UN ENTERO")
    malos = []
    for b in range(2, 13):
        for a in range(0, b + 1):
            r = motor.decidir_cuenta_fracciones(None, "-", (a, b), SABER)
            if r.get("valor") != (b - a, b):
                malos.append((b, a, r.get("valor")))
    comprobar("C1 1 - a/b = (b - a)/b para todos", malos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("-" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
