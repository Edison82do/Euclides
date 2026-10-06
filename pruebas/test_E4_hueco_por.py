# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO E.4: EL HUECO EN x Y : (Common Core 3.OA.A.4, 3.OA.B.6; NCETM 2.6).
El plan y sus trampas: diario/2026-10-05-paso-E4-hueco-por.md
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
TMP = tempfile.mkdtemp(prefix="huecopor_")
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


def E(texto):
    r = motor.decidir_ecuacion(texto, SABER)
    return (r.get("valor") if r["conclusion"] == "hecho" else r["conclusion"]), r


print("=" * 78)
print("PASO E.4 - EL HUECO EN x Y :  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LOS EJEMPLOS DEL ESTANDAR (3.OA.A.4)")
    comprobar("A1 8 x ? = 48 -> 6", E("8 x ? = 48")[0], 6)
    comprobar("A2 5 = _ : 3 -> 15", E("5 = _ : 3")[0], 15)
    comprobar("A3 6 x 6 = ? -> 36", E("6 x 6 = ?")[0], 36)

    print("\nB - EL SITIO DEL HUECO DICE QUE SE BUSCA (NCETM 2.6)")
    v, r = E("3 x ? = 12")
    comprobar("B1 3 x ? = 12: cuantos en cada grupo -> REPARTIR", (v, r["como"]), (4, "repartir"))
    v, r = E("? x 4 = 12")
    comprobar("B2 ? x 4 = 12: cuantos grupos -> AGRUPAR", (v, r["como"]), (3, "agrupar"))
    v, r = E("12 : ? = 4")
    comprobar("B3 12 : ? = 4: el divisor -> agrupar", (v, r["como"]), (3, "agrupar"))
    v, r = E("? : 3 = 4")
    comprobar("B4 ? : 3 = 4: el dividendo -> multiplicar (deshacer)", (v, r["como"]), (12, "multiplicar"))
    v, r = E("12 = ? x 3")
    comprobar("B5 el = al reves da igual, y se comprueba con E.0", (v, r["comprobacion"], r["comprobacion_ok"]),
              (4, "12 = 4 x 3", True))
    comprobar("B6 con palabras alrededor y ÷", (E("Que numero falta: 3 x ? = 12?")[0], E("? ÷ 3 = 4")[0]), (4, 12))

    print("\nC - LAS TRAMPAS")
    comprobar("C1 3 x ? = 13: no hay numero entero (sobra 1)", E("3 x ? = 13")[0], "no_entero")
    comprobar("C2 13 : 3 = ?: tampoco da justo", E("13 : 3 = ?")[0], "no_entero")
    comprobar("C3 0 x ? = 5: imposible", E("0 x ? = 5")[0], "imposible")
    comprobar("C4 0 x ? = 0: cualquier numero vale", E("0 x ? = 0")[0], "cualquiera")
    comprobar("C5 12 : ? = 0 y ? : 0 = 3: imposibles", (E("12 : ? = 0")[0], E("? : 0 = 3")[0]), ("imposible", "imposible"))
    comprobar("C6 ? x ? = 12: dos huecos", E("? x ? = 12")[0], "dos_huecos")
    comprobar("C7 3 x 4 = ? x 6: la balanza con x, todavia no", E("3 x 4 = ? x 6")[0], "todavia_no")
    comprobar("C8 las de + y - siguen igual: 8 + ? = 11 -> 3", E("8 + ? = 11")[0], 3)
    r = motor.decidir_igualdad("12 : 3 = 4", SABER)
    comprobar("C9 el = entiende : (12 : 3 = 4 VERDADERO; 13 : 3 = 4 no da justo)",
              (r["valor"], motor.decidir_igualdad("13 : 3 = 4", SABER)["conclusion"]), ("verdadero", "no_salio"))

    print("\nD - LA MUESTRA: LAS SEIS POSICIONES A LOS DOS LADOS DEL =")
    azar = random.Random(20261005)
    fallos, n = [], 0
    for _ in range(60):
        a, b = azar.randint(1, 12), azar.randint(1, 12)
        c = a * b
        for eq, esp in (("%d x %d = ?" % (a, b), c), ("%d x ? = %d" % (a, c), b), ("? x %d = %d" % (b, c), a),
                        ("%d : %d = ?" % (c, b), a), ("%d : ? = %d" % (c, a), b), ("? : %d = %d" % (b, a), c)):
            for texto in (eq, " = ".join(reversed(eq.split(" = ")))):
                n += 1
                v, r = E(texto)
                if v != esp or not r.get("comprobacion_ok"):
                    fallos.append("%s -> %s" % (texto, v))
    comprobar("D1 %d ecuaciones: todas bien y comprobadas con E.0" % n, fallos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
