# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO F.4: FRACCIONES MAYORES QUE UN ENTERO; NUMEROS MIXTOS E IMPROPIAS (NCETM 3.5; 4.NF.B.3).
El plan y sus trampas: diario/2026-10-07-paso-F4-mayores-que-un-entero.md
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
TMP = tempfile.mkdtemp(prefix="f4_")
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


def mixto_testigo(n, b):
    e, r = divmod(n, b)
    if e == 0:
        return "%d/%d" % (n, b) if n else "0"
    return "%d" % e if r == 0 else "%d %d/%d" % (e, r, b)


def signo(x, y):
    return ">" if x > y else "<" if x < y else "="


print("=" * 78)
print("PASO F.4 - FRACCIONES MAYORES QUE UN ENTERO  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRAMPAS DEL PLAN")
    comprobar("A1 fraccion: 7/4 -> 1 3/4", S("fraccion: 7/4"), "siete cuartos = 1 3/4")
    comprobar("A2 fraccion: 8/4 -> 2", S("fraccion: 8/4"), "ocho cuartos = 2")
    comprobar("A3 mixto: 2 3/4 -> 11/4 (no 23/4)", S("mixto: 2 3/4"), "11/4")
    comprobar("A4 recta: 7/4 -> a siete trozos (de 0 a 2)", S("recta: 7/4"), "a siete trozos de 1/4 del 0")
    comprobar("A5 7/4 de 12 -> 21;  entero: 5/4 es 15 -> 12", (S("7/4 de 12"), S("entero: 5/4 es 15")), ("21", "12"))
    comprobar("A6 5/4 + 3/4 -> 2;  7/4 - 2/4 -> 1 1/4", (S("5/4 + 3/4"), S("7/4 - 2/4")), ("2", "1 1/4"))
    comprobar("A7 2 3/4 + 1 1/4 -> 4 (no 3 4/8)", S("2 3/4 + 1 1/4"), "4")
    comprobar("A8 3 - 1/4 -> 2 3/4", S("3 - 1/4"), "2 3/4")
    comprobar("A9 comparar 2 1/4 y 1 3/4 -> por los enteros", S("comparar: 2 1/4 y 1 3/4"), "2 1/4 > 1 3/4")
    comprobar("A10 comparar 2 1/4 y 2 3/4 -> por las partes", S("comparar: 2 1/4 y 2 3/4"), "2 1/4 < 2 3/4")
    comprobar("A11 1/2 + 1/4 -> sigue todavia no (5.o)", S("1/2 + 1/4"), "todavia_no")
    comprobar("A12 3 - 1 sigue siendo una resta de enteros", S("3 - 1"), "2")

    print("\nB - IMPROPIA <-> MIXTO (b de 2 a 12, hasta 5 enteros), IDA Y VUELTA")
    malos = []
    for b in range(2, 13):
        for e in range(0, 6):
            for a in range(0, b):
                if e == 0:
                    continue
                n = e * b + a
                r = S("mixto: %d %d/%d" % (e, a, b))
                if r != "%d/%d" % (n, b):
                    malos.append(("mixto", e, a, b, r))
                if motor.decidir_cuenta_mixta((0, n, b), "+", (0, 0, b), SABER)["valor"] != (n, b):
                    malos.append(("vuelta", n, b))
    comprobar("B1 los mixtos y sus impropias", malos[:3], [])

    print("\nC - SUMAS Y RESTAS CON EL MISMO DE ABAJO (con mixtos), CONTRA EL TESTIGO")
    rnd = random.Random(35)
    malos = []
    for _ in range(250):
        b = rnd.randint(2, 12)
        x = (rnd.randint(0, 4), rnd.randint(0, b - 1), b)
        y = (rnd.randint(0, 4), rnd.randint(0, b - 1), b)
        op = rnd.choice("+-")
        fx, fy = x[0] + Fraction(x[1], b), y[0] + Fraction(y[1], b)
        v = fx + fy if op == "+" else fx - fy
        r = motor.decidir_cuenta_mixta(x, op, y, SABER)
        if v < 0:
            if r["conclusion"] != "imposible":
                malos.append((x, op, y, r["conclusion"]))
            continue
        if r["conclusion"] != "hecho" or Fraction(*r["valor"]) != v or not r["de_acuerdo"]:
            malos.append((x, op, y, r.get("valor")))
    comprobar("C1 250 cuentas, por los dos caminos", malos[:3], [])

    print("\nD - COMPARAR MIXTOS")
    malos = []
    for _ in range(200):
        b = rnd.randint(2, 12)
        b2 = rnd.choice((b, rnd.randint(2, 12)))
        x = (rnd.randint(0, 4), rnd.randint(1, b - 1), b)
        y = (rnd.randint(0, 4), rnd.randint(1, b2 - 1), b2)
        fx, fy = x[0] + Fraction(x[1], b), y[0] + Fraction(y[1], b2)
        r = motor.decidir_comparar_mixtos(x, y, SABER)
        comun = b == b2 or x[1] == y[1]
        if x[0] != y[0] or comun:
            if r["conclusion"] != "hecho" or r["valor"] != signo(fx, fy):
                malos.append((x, y, r.get("valor"), signo(fx, fy)))
        elif r["conclusion"] == "hecho":
            malos.append((x, y, "se atrevio"))
    comprobar("D1 200 parejas: enteros primero; si no, las partes (o todavia no)", malos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("-" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
