# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO D.2: CENTESIMAS Y MILESIMAS (NCETM 1.24; 4.NF.C.5-7).
El plan y sus trampas: diario/2026-10-07-paso-D2-centesimas-milesimas.md
Python solo aparece aqui como TESTIGO externo (en milesimas enteras, sin coma flotante).
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
TMP = tempfile.mkdtemp(prefix="d2_")
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


def escribir(n, k):
    """el testigo: n en la unidad 10^-k -> texto sin ceros de sobra."""
    s = str(n).rjust(k + 1, "0")
    e, d = s[:-k], s[-k:].rstrip("0")
    return e if not d else "%s.%s" % (e, d)


def texto(n, k):
    """n en 10^-k escrito con k cifras (con ceros al final si hace falta)."""
    s = str(n).rjust(k + 1, "0")
    return "%s.%s" % (s[:-k], s[-k:])


print("=" * 78)
print("PASO D.2 - CENTESIMAS Y MILESIMAS  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRAMPAS DEL PLAN")
    comprobar("A1 decimal: 2.35 -> 235 centesimas", S("decimal: 2.35"), "235 centesimas")
    comprobar("A2 comparar 0.5 y 0.45 -> 0.5 mayor (no '45 > 5')", S("comparar: 0.5 y 0.45"), "0.5 > 0.45")
    comprobar("A3 comparar 0.3 y 0.30 -> iguales", S("comparar: 0.3 y 0.30"), "0.3 = 0.30")
    comprobar("A4 2.35 + 1.7 -> 4.05 (no 2.52)", S("2.35 + 1.7"), "4.05")
    comprobar("A5 5 - 0.25 -> 4.75;  0.125 + 0.875 -> 1", (S("5 - 0.25"), S("0.125 + 0.875")), ("4.75", "1"))
    comprobar("A6 de 0.01 en 0.01 desde 0.98 -> 0.99, 1, 1.01 (no 0.100)", S("de 0.01 en 0.01 desde 0.98 hasta 1.01"), "0.99, 1, 1.01")
    comprobar("A7 redondear 2.35 a la decima -> 2.4;  2.95 -> 3;  2.35 al entero -> 2",
              (S("redondear: 2.35 a la decima"), S("redondear: 2.95 a la decima"), S("redondear: 2.35")), ("2.4", "3", "2"))
    comprobar("A8 0.1234 -> todavia no", S("0.1234 + 1"), "todavia_no")
    comprobar("A9 fraccion: 35/100 = 0.35 (lo dice)", "35/100 = 0.35" in motor.explicar_pregunta("fraccion: 35/100", SABER), True)
    comprobar("A10 fraccion: 3/10 = 30/100 (4.NF.C.5)", "3/10 = 30/100" in motor.explicar_pregunta("fraccion: 3/10", SABER), True)

    print("\nB - SUMAS Y RESTAS CON HASTA TRES CIFRAS DETRAS DEL PUNTO (muestra), CONTRA EL TESTIGO")
    rnd = random.Random(124)
    malos = []
    for _ in range(300):
        ka, kb = rnd.randint(1, 3), rnd.randint(1, 3)
        a, b = rnd.randint(0, 9999), rnd.randint(0, 9999)
        ta, tb = texto(a, ka), texto(b, kb)
        k = max(ka, kb)
        A, B = a * 10 ** (k - ka), b * 10 ** (k - kb)
        op = rnd.choice("+-")
        v = A + B if op == "+" else A - B
        r = motor.decidir_cuenta_decimal(ta, op, tb, SABER)
        if A > 10000 or B > 10000 or v > 10000:
            if r["conclusion"] == "hecho" and r.get("valor") != escribir(v, k):
                malos.append((ta, op, tb, "grande", r["valor"]))
        elif v < 0:
            if r["conclusion"] != "imposible":
                malos.append((ta, op, tb, r["conclusion"]))
        elif False:
            if r["conclusion"] == "hecho":
                malos.append((ta, op, tb, "se paso", r["valor"]))
        elif r.get("valor") != escribir(v, k):
            malos.append((ta, op, tb, r.get("valor"), escribir(v, k)))
    comprobar("B1 300 cuentas", malos[:3], [])

    print("\nC - COMPARAR Y REDONDEAR (muestra)")
    malos = []
    for _ in range(300):
        ka, kb = rnd.randint(1, 3), rnd.randint(1, 3)
        a, b = rnd.randint(0, 3000), rnd.randint(0, 3000)
        A, B = a * 10 ** (3 - ka), b * 10 ** (3 - kb)
        r = motor.decidir_comparar_decimales(texto(a, ka), texto(b, kb), SABER)
        if r["valor"] != (">" if A > B else "<" if A < B else "="):
            malos.append((texto(a, ka), texto(b, kb), r["valor"]))
    comprobar("C1 300 comparaciones (con distinto numero de cifras)", malos[:3], [])
    malos = []
    for n in range(1, 2000, 7):
        t = texto(n, 2)
        r = S("redondear: %s a la decima" % t)
        if r != escribir((n + 5) // 10, 1):
            malos.append((t, r))
        r = S("redondear: %s" % t)
        if r != str((n + 50) // 100):
            malos.append((t, "entero", r))
    comprobar("C2 redondear a la decima y al entero", malos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("-" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
