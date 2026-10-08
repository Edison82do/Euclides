# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.10: PARTIR POR SITIOS Y LA MULTIPLICACION CORTA (NCETM 2.14; 4.NBT.B.5).
El plan y sus trampas: diario/2026-10-06-paso-M10-multiplicacion-corta.md
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
TMP = tempfile.mkdtemp(prefix="m10_")
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


def C(pid, a, b):
    r = motor.aplicar(pid, {"a": a, "b": b}, SABER)
    return r.get("valor") if r["conclusion"] == "hecho" else r["conclusion"]


print("=" * 78)
print("PASO M.10 - PARTIR POR SITIOS Y LA MULTIPLICACION CORTA  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - SIN LAS TABLAS EN LA MEMORIA NO SE USAN")
    comprobar("A1 corta: 47 x 6 sin memoria -> no se puede (primero las tablas)", S("corta: 47 x 6"), "no_se_puede")
    comprobar("A2 ... pero 47 x 6 se calcula de otra manera", S("47 x 6"), "282")
    motor.aprender("tablas", SABER)

    print("\nB - LAS TRAMPAS DEL PLAN (con las tablas aprendidas)")
    comprobar("B1 47 x 6 -> 282 con la corta", (S("47 x 6"), motor.aplicar("multiplicar", {"a": 47, "b": 6}, SABER)["pieza"]["id"]),
              ("282", "multiplicacion_corta"))
    t = motor.explicar_pregunta("corta: 347 x 6", SABER)
    comprobar("B2 corta: 347 x 6 -> 2082, llevando a traves del cero",
              (t.strip().splitlines()[-1], "3 x 6 = 18, + 2 que llevaba = 20: escribo 0, llevo 2" in t),
              ("RESULTADO: 2082", True))
    comprobar("B3 ... y partiendo por sitios da lo mismo", ("1800 + 240 + 42 = 2082" in t, "lo mismo: SI" in t), (True, True))
    comprobar("B4 6 x 47 -> 282 (el de una cifra delante)", S("6 x 47"), "282")
    comprobar("B5 25 x 4 -> 100", S("25 x 4"), "100")
    comprobar("B6 1234567 x 9 -> se pasa de diez millones (N.6; N.4 era 123456 x 9)", S("1234567 x 9"), "no_se_puede")

    print("\nC - TODAS LAS DE DOS CIFRAS x UNA CIFRA, Y UNA MUESTRA DE TRES Y CUATRO CIFRAS")
    malos = []
    for n in range(10, 100):
        for k in range(2, 10):
            x, y = C("multiplicacion_corta", n, k), C("multiplicar_partiendo_por_sitios", k, n)
            if x != n * k or y != n * k:
                malos.append((n, k, x, y))
    comprobar("C1 720 productos, por las dos piezas, contra el testigo", malos[:3], [])
    rnd = random.Random(214)
    malos = []
    for _ in range(200):
        n, k = rnd.randint(100, 2000), rnd.randint(2, 9)
        x, y = C("multiplicacion_corta", n, k), C("multiplicar_partiendo_por_sitios", n, k)
        esperado = n * k if n * k <= 1000000 else "no_salio"
        if x != esperado or y != esperado:
            malos.append((n, k, x, y))
    comprobar("C2 200 de tres y cuatro cifras (las que se pasan de diez mil, no salen)", malos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("-" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
