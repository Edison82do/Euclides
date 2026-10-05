# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.0: FILAS Y COLUMNAS COMO SUMAS IGUALES (Common Core 2.OA.C.4).
El plan y sus trampas: diario/2026-10-05-paso-M0-filas.md
Python (f * c) solo aparece aqui como TESTIGO externo: el sistema no multiplica.
"""
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
TMP = tempfile.mkdtemp(prefix="filas_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia
import motor  # noqa: E402
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
F = lambda t: motor.decidir_filas(t, SABER)     # noqa: E731

print("=" * 78)
print("PASO M.0 - FILAS Y COLUMNAS COMO SUMAS IGUALES  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - 3 FILAS DE 4")
    r = F("3 filas de 4")
    comprobar("A1 da 12", r["valor"], 12)
    comprobar("A2 la suma de iguales: 4 + 4 + 4", r["suma_filas"], "4 + 4 + 4")
    comprobar("A3 el dibujo: 3 filas de 4 puntos", [l.split() for l in r["dibujo"]], [["o"] * 4] * 3)
    comprobar("A4 por columnas: 3 + 3 + 3 + 3, y da lo mismo", (r["suma_columnas"], r["igual"]), ("3 + 3 + 3 + 3", True))
    comprobar("A5 se hace sumando grupo a grupo (no multiplicando)", r["por_filas"]["pieza"]["id"], "sumar_iguales_uno_a_uno")

    print("\nB - SALTANDO CUANDO CADA FILA ES DE 2, 5 O 10 (lo de N.1)")
    r = F("5 filas de 5")
    comprobar("B1 5 filas de 5: 5, 10, 15, 20, 25", (r["valor"], r["por_filas"]["pieza"]["id"],
              r["por_filas"]["resultado"]["pasos"]), (25, "sumar_iguales_saltando", ["5", "10", "15", "20", "25"]))
    r = F("4 filas de 2")
    comprobar("B2 4 filas de 2 saltando; por columnas 4 + 4", (r["valor"], r["por_filas"]["pieza"]["id"],
              r["por_columnas"]["pieza"]["id"]), (8, "sumar_iguales_saltando", "sumar_iguales_uno_a_uno"))

    print("\nC - LAS TRAMPAS")
    comprobar("C1 1 fila de 5 -> 5", F("1 fila de 5")["valor"], 5)
    comprobar("C2 0 filas de 4 -> 0 (no hay nada)", F("0 filas de 4")["valor"], 0)
    r = F("3 columnas de 4")
    comprobar("C3 3 columnas de 4 -> 4 filas de 3 en el dibujo", (r["filas"], r["columnas"], r["valor"]), (4, 3, 12))
    comprobar("C4 3 x 4 ya no es de filas: desde M.1 es multiplicar (3 grupos de 4)",
              motor.decidir_multiplicar("3 x 4", SABER)["valor"], 12)
    r = F("7 filas de 8")
    comprobar("C5 7 filas de 8: pasa del estandar (5 x 5), se hace y se avisa", (r["valor"], r["pasa_del_estandar"]), (56, True))
    comprobar("C6 11 filas de 2: no dibujo mas de 10", F("11 filas de 2")["conclusion"], "no_entiendo")

    print("\nD - TODAS LAS FILAS Y COLUMNAS DE 0 A 10 CONTRA EL TESTIGO")
    fallos = []
    for f in range(0, 11):
        for c in range(0, 11):
            r = F("%d filas de %d" % (f, c))
            if r["valor"] != f * c or not r["igual"] or len(r["dibujo"]) != f:
                fallos.append("%dx%d -> %s" % (f, c, r["valor"]))
    comprobar("D1 las 121 (y por filas = por columnas, y el dibujo con sus filas)", fallos[:3], [])

    print("\nE - LA ORDEN")
    t = motor.explicar_pregunta("3 filas de 4", SABER)
    comprobar("E1 '3 filas de 4' dibuja y dice la suma de iguales",
              ("o o o o" in t, "4 + 4 + 4 = 12" in t, t.strip().endswith("RESULTADO: 12")), (True, True, True))
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
