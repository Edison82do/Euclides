# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO D.1: LAS DECIMAS (NCETM 1.23; 4.NF.C.6).
El plan y sus trampas: diario/2026-10-07-paso-D1-decimas.md
Python solo aparece aqui como TESTIGO externo (con enteros de decimas, sin coma flotante).
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
TMP = tempfile.mkdtemp(prefix="d1_")
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


def dec(n):
    """el testigo: n decimas -> texto."""
    e, d = divmod(n, 10)
    return "%d" % e if d == 0 else "%d.%d" % (e, d)


print("=" * 78)
print("PASO D.1 - LAS DECIMAS  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRAMPAS DEL PLAN")
    comprobar("A1 decimal: 2.3 -> 23 decimas;  0.3 -> 3 decimas", (S("decimal: 2.3"), S("decimal: 0.3")), ("23 decimas", "3 decimas"))
    comprobar("A2 decimal: 1.0 -> 10 decimas", S("decimal: 1.0"), "10 decimas")
    comprobar("A3 2.7 + 1.5 -> 4.2 (no 3.12)", S("2.7 + 1.5"), "4.2")
    comprobar("A4 4.2 - 1.5 -> 2.7 (cambiando una unidad por diez decimas)", S("4.2 - 1.5"), "2.7")
    comprobar("A5 0.9 + 0.1 -> 1", S("0.9 + 0.1"), "1")
    comprobar("A6 comparar 0.9 y 1.1 -> 1.1 mayor", S("comparar: 0.9 y 1.1"), "0.9 < 1.1")
    comprobar("A7 redondear 2.7 -> 3;  2.5 -> 3 (convenio);  2.4 -> 2",
              (S("redondear: 2.7"), S("redondear: 2.5"), S("redondear: 2.4")), ("3", "3", "2"))
    comprobar("A8 de 0.1 en 0.1 desde 0.8 -> pasa el uno sin '0.10'", S("de 0.1 en 0.1 desde 0.8 hasta 1.2"), "0.9, 1, 1.1, 1.2")
    comprobar("A9 2.35 + 1 -> desde D.2 (centesimas) si: 3.35", S("2.35 + 1"), "3.35")
    comprobar("A10 la coma tambien vale: 2,7 + 1,5", S("2,7 + 1,5"), "4.2")
    comprobar("A11 2 + 0.5 -> 2.5 (un entero y un decimal)", S("2 + 0.5"), "2.5")
    comprobar("A12 1.5 - 2.5 -> imposible", S("1.5 - 2.5"), "imposible")
    comprobar("A13 las de siempre siguen: 12/3 -> 4;  8 + 3 -> 11", (S("12/3"), S("8 + 3")), ("4", "11"))

    print("\nB - SUMAS Y RESTAS CON DECIMAS (muestra) CONTRA EL TESTIGO")
    rnd = random.Random(123)
    malos = []
    for _ in range(300):
        a, b = rnd.randint(0, 999), rnd.randint(0, 999)
        op = rnd.choice("+-")
        r = motor.decidir_cuenta_decimal(dec(a) if "." in dec(a) else dec(a) + ".0", op, dec(b) if "." in dec(b) else dec(b) + ".0", SABER)
        v = a + b if op == "+" else a - b
        if v < 0:
            if r["conclusion"] != "imposible":
                malos.append((a, op, b, r["conclusion"]))
        elif r.get("valor") != dec(v):
            malos.append((a, op, b, r.get("valor"), dec(v)))
    comprobar("B1 300 cuentas", malos[:3], [])

    print("\nC - COMPARAR Y REDONDEAR (muestra)")
    malos = []
    for _ in range(300):
        a, b = rnd.randint(0, 999), rnd.randint(0, 999)
        r = motor.decidir_comparar_decimales(dec(a) + ("" if a % 10 else ".0"), dec(b) + ("" if b % 10 else ".0"), SABER)
        if r["valor"] != (">" if a > b else "<" if a < b else "="):
            malos.append((a, b, r["valor"]))
    comprobar("C1 300 comparaciones", malos[:3], [])
    malos = []
    for n in range(0, 500, 3):
        if n % 10 == 0:
            continue
        r = S("redondear: %s" % dec(n))
        if r != str((n + 5) // 10):
            malos.append((dec(n), r))
    comprobar("C2 redondear al entero", malos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("-" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
