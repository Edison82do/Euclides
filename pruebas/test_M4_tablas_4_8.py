# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.4: LAS TABLAS DEL 4 Y DEL 8, DOBLANDO LA DEL 2 (NCETM 2.7).
El plan y sus trampas: diario/2026-10-05-paso-M4-tablas-4-8.md
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
TMP = tempfile.mkdtemp(prefix="m4_")
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


def P(a, b):
    r = motor.aplicar("multiplicar", {"a": a, "b": b}, SABER)
    return r.get("valor"), r.get("pieza", {}).get("id"), r


print("=" * 78)
print("PASO M.4 - LAS TABLAS DEL 4 Y DEL 8  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TABLAS, DOBLANDO (NCETM 2.7)")
    for n in (4, 8):
        t = motor.explicar_pregunta("tabla del %d" % n, SABER)
        comprobar("A tabla del %d: 0 ... %d, cada una el doble de la de %d" % (n, 10 * n, n // 2),
                  (t.strip().splitlines()[-1], "el doble de" in t),
                  ("RESULTADO: " + ", ".join(str(n * k) for k in range(11)), True))

    print("\nB - UN HECHO DERIVADO: SOLO SI LA MITAD YA SE SABE")
    v, p, r = P(6, 4)
    comprobar("B1 sin la tabla del 2 en la memoria, 6 x 4 no se dobla", (v, p != "multiplicar_doblando"), (24, True))
    a = motor.aprender("tablas", SABER)
    comprobar("B2 aprender: tablas, en orden (2 -> 4 -> 8), sin rechazar ninguna", a["rechazados"], [])
    h = motor.cargar_memoria()
    comprobar("B3 6 x 4 se aprendio DOBLANDO 6 x 2; 7 x 8 doblando 7 x 4",
              (h["6 x 4"]["como"], h["7 x 8"]["como"]), ("doblando (M.4)", "doblando (M.4)"))
    v, p, r = P(9, 4)
    comprobar("B4 con la tabla del 2 sabida, 9 x 4 de memoria (y doblar tambien servia)",
              (v, p, "multiplicar_doblando" in r.get("tambien_servian", [])), (36, "recordar_producto", True))
    v, p, r = motor.aplicar("multiplicar", {"a": 7, "b": 8, "sin_memoria": True}, SABER).get("valor"), None, None
    r = motor.aplicar("multiplicar", {"a": 7, "b": 8, "sin_memoria": True}, SABER)
    comprobar("B5 7 x 8 sin recordarlo: doblando 7 x 4 = 28 -> 28 + 28 = 56",
              (r["valor"], r["pieza"]["id"], "28 + 28 = 56" in r["resultado"]["cuenta"]), (56, "multiplicar_doblando", True))
    comprobar("B6 3 x 7: ni 4 ni 8 -> no se dobla", P(3, 7)[1] != "multiplicar_doblando", True)
    motor.olvidar_todo()

    print("\nC - DIVISIBLE ENTRE 2, 4 Y 8 (con mitades)")
    r = motor.decidir_divisible(36, 8, SABER)
    comprobar("C1 36 entre 8: no (36 -> 18 -> 9)", (r["valor"], r["camino"]), (False, ["36", "18", "9"]))
    r = motor.decidir_divisible(40, 8, SABER)
    comprobar("C2 40 entre 8: si, da 5", (r["valor"], r["cociente"]), (True, 5))
    comprobar("C3 entre 7: todavia no (entre 3 llega en M.5)", motor.decidir_divisible(36, 7, SABER)["conclusion"], "todavia_no")
    fallos = [(n, d) for n in range(0, 201, 3) for d in (2, 4, 8)
              if motor.decidir_divisible(n, d, SABER)["valor"] != (n % d == 0)]
    comprobar("C4 de 0 a 200 (de 3 en 3) entre 2, 4 y 8 contra el testigo", fallos[:3], [])

    print("\nD - CONTRA EL TESTIGO, CON LAS TABLAS APRENDIDAS")
    motor.aprender("tablas", SABER)
    fallos = [(a, b) for a in range(0, 11) for b in (4, 8) if P(a, b)[0] != a * b or P(b, a)[0] != a * b]
    comprobar("D1 las tablas del 4 y del 8 en las dos lecturas", fallos, [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
