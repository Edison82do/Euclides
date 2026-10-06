# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO F.1: LA PARTE Y EL TODO; FRACCIONES UNITARIAS (NCETM 3.1, 3.2; 3.NF.A.1).
El plan y sus trampas: diario/2026-10-06-paso-F1-fracciones-unitarias.md
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
TMP = tempfile.mkdtemp(prefix="f1_")
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
    return probar.preguntar(t, SABER)[0]


def signo(x, y):
    return ">" if x > y else "<" if x < y else "="


print("=" * 78)
print("PASO F.1 - LA PARTE Y EL TODO; FRACCIONES UNITARIAS  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRAMPAS DEL PLAN")
    comprobar("A1 fraccion: 1/4 -> un cuarto", S("fraccion: 1/4"), "un cuarto")
    comprobar("A2 fraccion: 1/2 -> un medio", S("fraccion: 1/2"), "un medio")
    comprobar("A3 1/4 de 12 -> 3 (repartir)", S("1/4 de 12"), "3")
    comprobar("A4 1/2 de 10 -> 5", S("1/2 de 10"), "5")
    comprobar("A5 1/4 de 13 -> no sale justo", S("1/4 de 13"), "no_sale")
    comprobar("A6 comparar 1/3 y 1/5 -> 1/3 es MAYOR (no 'cinco es mas')", S("comparar: 1/3 y 1/5"), "1/3 > 1/5")
    comprobar("A7 comparar 1/4 y 1/4 -> iguales", S("comparar: 1/4 y 1/4"), "1/4 = 1/4")
    comprobar("A8 entero: 1/4 es 3 -> 12", S("entero: 1/4 es 3"), "12")
    comprobar("A9 entero: 1/5 es 7 -> 35", S("entero: 1/5 es 7"), "35")
    comprobar("A10 partes: 12 = 4 + 4 + 4 -> 1/3", S("partes: 12 = 4 + 4 + 4"), "1/3")
    comprobar("A11 partes: 12 = 5 + 4 + 3 -> desiguales", S("partes: 12 = 5 + 4 + 3"), "desiguales")
    comprobar("A12 partes: 12 = 4 + 4 + 3 -> no hacen el entero", S("partes: 12 = 4 + 4 + 3"), "no_hacen_el_entero")
    comprobar("A13 partes: 12 = 6 + 6 -> medios", S("partes: 12 = 6 + 6"), "1/2")
    comprobar("A14 fraccion: 1/0 -> imposible;  1/1 -> un entero",
              (S("fraccion: 1/0"), S("fraccion: 1/1")), ("imposible", "un entero"))
    comprobar("A15 fraccion: 1/13 -> todavia no (3.o: hasta doceavos)", S("fraccion: 1/13"), "todavia_no")
    comprobar("A16 12/3 sigue siendo una division (M.3): 4", S("12/3"), "4")

    print("\nB - COMPARAR TODAS LAS PAREJAS 1/2 .. 1/12 (contra el testigo; la regla y la tira de acuerdo)")
    malos, n = [], 0
    for a in range(2, 13):
        for b in range(2, 13):
            r = motor.decidir_comparar_fracciones((1, a), (1, b), SABER)
            n += 1
            if r["conclusion"] != "hecho" or r["valor"] != signo(Fraction(1, a), Fraction(1, b)) or len(r["todos"]) != 2:
                malos.append((a, b, r.get("valor"), r["conclusion"]))
    comprobar("B1 %d parejas" % n, malos[:3], [])

    print("\nC - 1/b DE n: REPARTIR (muestra, justas y no justas)")
    rnd = random.Random(31)
    malos, vistas = [], 0
    casos = [(b, b * k) for b in range(2, 13) for k in range(0, 11)] + \
            [(rnd.randint(2, 12), rnd.randint(1, 200)) for _ in range(80)]
    for b, n in casos:
        r = motor.decidir_fraccion_de(1, b, n, SABER)
        vistas += 1
        esperado = n // b if n % b == 0 else "no_sale"
        obtenido = r.get("valor") if r["conclusion"] == "hecho" else r["conclusion"]
        if obtenido != esperado:
            malos.append((b, n, obtenido, esperado))
    comprobar("C1 %d casos de 1/b de n" % vistas, malos[:3], [])

    print("\nD - EL ENTERO DESDE UNA PARTE (sumando la parte una y otra vez)")
    malos = []
    for b in range(2, 13):
        for parte in (1, 3, 7, 10, 25):
            r = motor.decidir_entero(1, b, parte, SABER)
            if r["conclusion"] != "hecho" or r["valor"] != b * parte or not r["comprobacion_ok"] or len(r["serie"]) != b:
                malos.append((b, parte, r.get("valor")))
    comprobar("D1 11 x 5 casos: el entero y su comprobacion", malos[:3], [])

    print("\nE - PARTES IGUALES Y DESIGUALES")
    malos = []
    for k in range(1, 9):
        for c in range(2, 9):
            r = motor.decidir_partes(k * c, [k] * c, SABER)
            if r.get("valor") != "1/%d" % c:
                malos.append((k, c, r.get("valor")))
    comprobar("E1 c partes iguales de k: cada una es 1/c", malos[:3], [])
    comprobar("E2 una sola parte: el entero", motor.decidir_partes(5, [5], SABER).get("valor"), "el entero")

    print("\nF - LA EXPLICACION")
    t = motor.explicar_pregunta("1/4 de 12", SABER)
    comprobar("F1 1/4 de 12: reparte y dibuja la tira", ("REPARTO 12 entre 4" in t, "[###|ooo|ooo|ooo]" in t), (True, True))
    t = motor.explicar_pregunta("comparar: 1/3 y 1/5", SABER)
    comprobar("F2 comparar: la regla y la tira", ("MAS PEQUENAS" in t, "tira de 15 cuadritos" in t), (True, True))
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("-" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
