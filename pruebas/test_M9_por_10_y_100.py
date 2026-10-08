# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.9: MULTIPLICAR Y DIVIDIR POR 10 Y POR 100 (NCETM 2.13; 3.NBT.A.3).
El plan y sus trampas: diario/2026-10-06-paso-M9-por-10-y-100.md
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
TMP = tempfile.mkdtemp(prefix="m9_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia
import motor  # noqa: E402
import probar  # noqa: E402
from _muestras import modo, numeros  # noqa: E402

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


def M(a, b):
    r = motor.aplicar("multiplicar", {"a": a, "b": b}, SABER)
    return (r.get("valor"), r.get("pieza", {}).get("id"))


def D(t, d):
    r = motor.aplicar("dividir", {"total": t, "divisor": d}, SABER)
    return (r.get("valor"), r.get("resultado", {}).get("resto"), r.get("pieza", {}).get("id"))


print("=" * 78)
print("PASO M.9 - MULTIPLICAR Y DIVIDIR POR 10 Y POR 100  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRAMPAS DEL PLAN")
    comprobar("A1 23 x 10 -> 230 (las cifras suben un sitio)", M(23, 10), (230, "multiplicar_por_10_o_100"))
    comprobar("A2 23 x 100 -> 2300 (por 10 dos veces)", M(23, 100), (2300, "multiplicar_por_10_o_100"))
    t = motor.explicar_pregunta("23 x 100", SABER)
    comprobar("A3 ... y lo dice: 23 x 10 = 230, y 230 x 10 = 2300", ("23 x 10 = 230" in t, "230 x 10 = 2300" in t), (True, True))
    comprobar("A4 230 : 10 -> 23;  47 : 10 -> 4 resto 7", (D(230, 10)[:2], D(47, 10)[:2]), ((23, 0), (4, 7)))
    comprobar("A5 2345 : 100 -> 23 resto 45", D(2345, 100)[:2], (23, 45))
    comprobar("A6 999999 x 100 -> se pasa de diez millones (N.6; N.4 era 99999 x 100)", S("999999 x 100"), "no_se_puede")
    comprobar("A7 9 x 80 sin memoria: no se deriva (hace falta saber 9 x 8)", M(9, 80)[1] != "multiplicar_por_decenas_justas", True)
    motor.aprender("tablas", SABER)
    comprobar("A8 con las tablas aprendidas: 9 x 80 -> 720 (9 x 8 = 72, diez veces)", M(9, 80), (720, "multiplicar_por_decenas_justas"))
    comprobar("A9 30 x 40 -> 1200 (3 x 4, y diez y diez)", M(30, 40), (1200, "multiplicar_por_decenas_justas"))
    comprobar("A10 120 : 4 -> 30 (12 : 4 = 3, diez veces)", D(120, 4), (30, 0, "dividir_decenas_justas"))

    print("\nB - POR 10 Y POR 100 (muestra hasta diez mil) CONTRA EL TESTIGO")
    malos = []
    for n in numeros(0, 1000):
        for k in (10, 100):
            v, pid = M(n, k)
            if n * k <= 1000000 and v != n * k:
                malos.append((n, k, v))
            if n * k > 1000000 and v is not None:
                malos.append((n, k, "se paso", v))
    comprobar("B1 n x 10 y n x 100", malos[:3], [])
    malos = []
    for n in numeros(0, 10000):
        for k in (10, 100):
            v, r, pid = D(n, k)
            if (v, r) != (n // k, n % k):
                malos.append((n, k, v, r))
    comprobar("B2 n : 10 y n : 100 (cociente y resto)", malos[:3], [])

    print("\nC - DECENAS JUSTAS (con las tablas sabidas)")
    malos = []
    for a in range(1, 13):
        for b in (10, 20, 30, 50, 70, 90, 110, 200, 400, 900):
            v, pid = M(a, b)
            if v != (a * b if a * b <= 1000000 else None):
                malos.append((a, b, v))
    comprobar("C1 una cifra (o 10, 11, 12) por decenas y centenas justas", malos[:3], [])
    malos = []
    for d in range(2, 13):
        for q in range(0, 13):
            t = d * q * 10
            if t == 0:
                continue
            v, r, pid = D(t, d)
            if (v, r) != (q * 10, 0):
                malos.append((t, d, v, r))
    comprobar("C2 divisiones de decenas justas", malos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("-" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
