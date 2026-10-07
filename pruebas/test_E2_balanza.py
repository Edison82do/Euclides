# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO E.2: EL = COMO BALANZA (Falkner, Levi y Carpenter; Knuth et al.; NCETM 1.29).
El plan y sus trampas: diario/2026-10-05-paso-E2-balanza.md
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
TMP = tempfile.mkdtemp(prefix="balanza_")
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
    pieza = r.get("paso", {}).get("pieza", {}).get("id")
    return (r.get("valor") if r["conclusion"] == "hecho" else r["conclusion"]), pieza, r


print("=" * 78)
print("PASO E.2 - EL = COMO BALANZA  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - EL PROBLEMA FAMOSO: 8 + 4 = ? + 5")
    v, p, r = E("8 + 4 = ? + 5")
    comprobar("A1 da 7", v, 7)
    comprobar("A2 sin calcular los lados: compensando", p, "balanza_compensando")
    comprobar("A3 y descarta 12 y 17 con E.0 (las respuestas de siempre)",
              [t.split(" NO")[0] for t in r["trampas"]], ["12", "17"])
    comprobar("A4 las dos dan FALSO", all(t.endswith("FALSO") for t in r["trampas"]), True)
    comprobar("A5 comprobado con E.0", r["comprobacion"], "8 + 4 = 7 + 5")

    print("\nB - PENSAR SIN CALCULAR (pensamiento relacional)")
    v, p, r = E("57 + 22 = ? + 21")
    comprobar("B1 57 + 22 = ? + 21 -> 58 compensando (21 es uno menos que 22)", (v, p), (58, "balanza_compensando"))
    comprobar("B2 8 + 4 = 8 + ? -> 4: el mismo numero en los dos platos", E("8 + 4 = 8 + ?")[:2], (4, "balanza_mismo_numero"))
    comprobar("B3 12 - 5 = 12 - ? -> 5", E("12 - 5 = 12 - ?")[:2], (5, "balanza_mismo_numero"))
    comprobar("B4 ? - 3 = 9 - 3 -> 9", E("? - 3 = 9 - 3")[:2], (9, "balanza_mismo_numero"))

    print("\nC - CUANDO NO SE PUEDE COMPENSAR, SE CALCULA UN PLATO")
    # OBSOLETA POR MEJORA (P.7, 7 oct): antes era (14, "balanza_calculando_un_lado"): en E.2 la resta no se
    # compensaba.  Desde P.7 (NCETM 1.29, la misma diferencia) si: el sustraendo baja 1, el minuendo tambien: 14.
    comprobar("C1 15 - 7 = ? - 6 -> 14 (resta: la misma diferencia, P.7)", E("15 - 7 = ? - 6")[:2],
              (14, "balanza_misma_diferencia"))
    comprobar("C2 8 + 4 = 15 - ? -> 3 (operaciones distintas)", E("8 + 4 = 15 - ?")[:2], (3, "balanza_calculando_un_lado"))
    comprobar("C3 8 + 4 = ? + 13 -> imposible (el otro plato ya pesa mas)", E("8 + 4 = ? + 13")[0], "imposible")
    comprobar("C4 30 + 40 = ? + 5: lejos para compensar -> calculando: 65", E("30 + 40 = ? + 5")[:2],
              (65, "balanza_calculando_un_lado"))

    print("\nD - LA MUESTRA: EL HUECO EN LAS CUATRO POSICIONES, CON + Y CON -")
    azar = random.Random(20261005)
    fallos, n = [], 0
    for _ in range(150):
        for op1 in "+-":
            for op2 in "+-":
                a, b = azar.randint(0, 60), azar.randint(0, 60)
                if op1 == "-":
                    a, b = max(a, b), min(a, b)
                total = a + b if op1 == "+" else a - b
                x = azar.randint(0, 60)
                # el hueco: en el otro plato, con x conocido, en las dos posiciones
                if op2 == "+":
                    if x > total:
                        continue
                    casos = [("? + %d" % x, total - x), ("%d + ?" % x, total - x)]
                else:
                    casos = [("? - %d" % x, total + x)]
                    if x >= total:
                        casos.append(("%d - ?" % x, x - total))
                for hueco, esperado in casos:
                    for eq in ("%d %s %d = %s" % (a, op1, b, hueco), "%s = %d %s %d" % (hueco, a, op1, b)):
                        if esperado > 1000:
                            continue
                        n += 1
                        v, p, r = E(eq)
                        if v != esperado or not r.get("comprobacion_ok"):
                            fallos.append("%s -> %s" % (eq, v))
    comprobar("D1 %d balanzas: todas bien y comprobadas por E.0" % n, fallos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
