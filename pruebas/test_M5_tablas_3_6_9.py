# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.5: LAS TABLAS DEL 3, 6 Y 9 Y SUS RELACIONES (NCETM 2.8).
El plan y sus trampas: diario/2026-10-05-paso-M5-tablas-3-6-9.md
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
TMP = tempfile.mkdtemp(prefix="m5_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia
import motor  # noqa: E402
from _muestras import numeros, modo  # noqa: E402

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


def P(a, b, **k):
    s = {"a": a, "b": b}
    s.update(k)
    r = motor.aplicar("multiplicar", s, SABER)
    return r.get("valor"), r.get("pieza", {}).get("id"), r


print("=" * 78)
print("PASO M.5 - LAS TABLAS DEL 3, 6 Y 9  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TABLAS Y SUS RELACIONES (NCETM 2.8)")
    for n, rel in ((3, "contar de 3 en 3"), (6, "el doble"), (9, "el triple")):
        t = motor.explicar_pregunta("tabla del %d" % n, SABER)
        comprobar("A tabla del %d (%s)" % (n, rel), (t.strip().splitlines()[-1], rel in t),
                  ("RESULTADO: " + ", ".join(str(n * k) for k in range(11)), True))
    comprobar("A4 tabla del 13: todavia no (la del 7 llego en M.6; la del 11 y 12 en M.7)", motor.explicar_pregunta("tabla del 13", SABER).strip().splitlines()[-1],
              "RESULTADO: todavia_no")

    print("\nB - HECHOS DERIVADOS: SOLO SI LA TABLA DEL 3 YA SE SABE")
    comprobar("B1 sin memoria, 7 x 9 no se triplica", P(7, 9)[1] != "multiplicar_triplicando", True)
    a = motor.aprender("tablas", SABER)
    comprobar("B2 aprender: tablas (2 -> 4 -> 8 -> 3 -> 6 -> 9 -> 5 -> 10), sin rechazar ninguna", a["rechazados"], [])
    h = motor.cargar_memoria()
    comprobar("B3 7 x 9 se aprendio triplicando 7 x 3; 7 x 6 doblando 7 x 3",
              (h["7 x 9"]["como"], h["7 x 6"]["como"]), ("triplicando (M.5)", "doblando (M.4)"))
    r = motor.aplicar("multiplicar", {"a": 7, "b": 9, "sin_memoria": True}, SABER)
    comprobar("B4 7 x 9 sin recordarlo: 21 + 21 + 21 = 63",
              (r["valor"], r["pieza"]["id"], "21 + 21 = 42; 42 + 21 = 63" in r["resultado"]["cuenta"]),
              (63, "multiplicar_triplicando", True))
    r = motor.aplicar("multiplicar", {"a": 8, "b": 6, "sin_memoria": True}, SABER)
    comprobar("B5 8 x 6 sin recordarlo: el doble de 8 x 3 (24 + 24 = 48)", (r["valor"], r["pieza"]["id"]),
              (48, "multiplicar_doblando"))
    fallos = [(a_, b) for a_ in range(0, 11) for b in (3, 6, 9) if P(a_, b)[0] != a_ * b or P(b, a_)[0] != a_ * b]
    comprobar("B6 las tablas del 3, 6 y 9 en las dos lecturas contra el testigo", fallos, [])
    motor.olvidar_todo()

    print("\nC - DIVISIBLE ENTRE 3, 6 Y 9 (la suma de las cifras)")
    r = motor.decidir_divisible(51, 3, SABER)
    comprobar("C1 51 entre 3: si (5 + 1 = 6), da 17", (r["valor"], r["camino"], r.get("cociente")), (True, ["51", "6"], 17))
    comprobar("C2 51 entre 9: no;  51 entre 6: no (impar)",
              (motor.decidir_divisible(51, 9, SABER)["valor"], motor.decidir_divisible(51, 6, SABER)["valor"]), (False, False))
    r = motor.decidir_divisible(999, 9, SABER)
    comprobar("C3 999 entre 9: 9+9+9 = 27 -> 2+7 = 9: si", (r["valor"], r["camino"]), (True, ["999", "27", "9"]))
    fallos = [(n, d) for n in numeros(0, 999) for d in (3, 6, 9)
              if motor.decidir_divisible(n, d, SABER)["valor"] != (n % d == 0)]
    comprobar("C4 la muestra de 0 a 999 entre 3, 6 y 9 contra el testigo", fallos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
