# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.7: LAS TABLAS DEL 11 Y DEL 12 (NCETM 2.11).
El plan y sus trampas: diario/2026-10-06-paso-M7-tablas-11-12.md
Python solo aparece aqui como TESTIGO externo.
"""
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)
TMP = tempfile.mkdtemp(prefix="m7_")
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
print("PASO M.7 - LAS TABLAS DEL 11 Y DEL 12  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TABLAS (partiendo: 10 + 1, 10 + 2)")
    t = motor.explicar_pregunta("tabla del 11", SABER)
    comprobar("A1 tabla del 11: 0 ... 110, cada fila 10 x k + 1 x k",
              (t.strip().splitlines()[-1], "7 x 11 =  7 x 10 +  7 x 1 =  70 +  7 = 77" in t),
              ("RESULTADO: " + ", ".join(str(11 * k) for k in range(11)), True))
    t = motor.explicar_pregunta("tabla del 12", SABER)
    comprobar("A2 tabla del 12: 0 ... 120, y es el doble de la del 6",
              (t.strip().splitlines()[-1], "DOBLE del de la del 6 ... SI" in t),
              ("RESULTADO: " + ", ".join(str(12 * k) for k in range(11)), True))
    comprobar("A3 tabla del 13 -> todavia no", S("tabla del 13"), "todavia_no")

    print("\nB - APRENDER: TODO HASTA 12 x 12")
    a = motor.aprender("tablas", SABER)
    comprobar("B1 aprender: tablas, sin rechazar ninguna", a["rechazados"], [])
    h = motor.cargar_memoria()
    faltan = [(x, y) for x in range(0, 13) for y in range(0, 13)
              if "%d x %d" % (x, y) not in h and not (x in (0, 1) and y in (0, 1))]
    comprobar("B2 en la memoria estan todos los productos hasta 12 x 12", faltan, [])
    malos = [k for k, v in h.items() if " x " in k and v["valor"] != int(k.split(" x ")[0]) * int(k.split(" x ")[1])]
    comprobar("B3 y todos bien (contra el testigo)", malos[:3], [])
    comprobar("B4 11 x 7 se aprendio por el valor de posicion (partiendo 10 + 1, o la corta desde M.10)",
              h["11 x 7"]["como"] in ("partiendo (M.6)", "la multiplicacion corta (M.10)"), True)
    comprobar("B5 12 x 12 = 144 de memoria", S("12 x 12"), "144")

    print("\nC - DIVISIBLE ENTRE 12 (entre 3 y entre 4) Y ENTRE 11")
    malos = []
    for n in range(0, 201):
        r = motor.decidir_divisible(n, 12, SABER)
        if r["valor"] != (n % 12 == 0):
            malos.append(n)
    comprobar("C1 entre 12, de 0 a 200", malos[:3], [])
    malos = []
    for n in range(10, 200):
        r = motor.decidir_divisible(n, 11, SABER)
        if r["valor"] != (n % 11 == 0) or (n < 100 and r["regla"] != "cifras_iguales"):
            malos.append(n)
    comprobar("C2 entre 11, de 10 a 199 (dos cifras: cifras iguales)", malos[:3], [])
    comprobar("C3 las trampas: 84 si, 90 no (no se parte en 4), 77 si, 78 no",
              (S("divisible: 84 entre 12"), S("divisible: 90 entre 12"), S("divisible: 77 entre 11"),
               S("divisible: 78 entre 11")), ("si", "no", "si", "no"))
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("-" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
