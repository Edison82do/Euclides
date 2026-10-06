# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.3: DIVIDIR, REPARTIR Y AGRUPAR (NCETM 2.6; Common Core 3.OA.A.2, 3.OA.B.6).
El plan y sus trampas: diario/2026-10-05-paso-M3-dividir.md
Python (// y %) solo aparece aqui como TESTIGO externo.
"""
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
TMP = tempfile.mkdtemp(prefix="dividir_")
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


def D(t):
    r = motor.decidir_dividir(t, SABER)
    pieza = r.get("aplicado", {}).get("pieza", {}).get("id")
    return (r.get("valor"), r.get("resto")), pieza, r


print("=" * 78)
print("PASO M.3 - DIVIDIR: REPARTIR Y AGRUPAR  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS DOS ESTRUCTURAS (NCETM 2.6)")
    v, p, r = D("12 en grupos de 3")
    comprobar("A1 agrupar 12 en grupos de 3: 4 grupos, contando 3, 6, 9, 12", (v, r["lectura"], p), ((4, 0), "agrupar", "dividir_saltando"))
    v, p, r = D("12 entre 3")
    comprobar("A2 repartir 12 entre 3: 4 para cada uno", (v, r["lectura"]), ((4, 0), "repartir"))
    v, p, r = D("12 : 3")
    comprobar("A3 12 : 3 (y 12 ÷ 3, 12 / 3): las dos lecturas", (v, r["lectura"], D("12 ÷ 3")[0], D("12 / 3")[0]),
              ((4, 0), "las_dos", (4, 0), (4, 0)))
    t = motor.explicar_pregunta("12 : 3", SABER)
    comprobar("A4 dice DIVIDENDO, DIVISOR y COCIENTE", all(x in t for x in ("DIVIDENDO", "DIVISOR", "COCIENTE")), True)

    print("\nB - A VECES SOBRA (el resto)")
    comprobar("B1 13 : 3 -> 4 y sobra 1", D("13 : 3")[0], (4, 1))
    comprobar("B2 3 : 5 -> 0 y sobran 3 (no llega para un grupo)", D("3 : 5")[0], (0, 3))
    v, p, r = D("100 : 7")
    comprobar("B3 100 : 7 -> 14 y sobran 2, comprobado: 14 x 7 + 2 = 100", (v, r["comprobacion_ok"]), ((14, 2), True))

    print("\nC - LOS ATAJOS Y LOS CASOS (NCETM 2.6, puntos 4 y 5)")
    comprobar("C1 0 : 4, 7 : 7, 9 : 1 sin calcular", [D(x)[:2] for x in ("0 : 4", "7 : 7", "9 : 1")],
              [((0, 0), "dividir_casos_especiales"), ((1, 0), "dividir_casos_especiales"), ((9, 0), "dividir_casos_especiales")])
    comprobar("C2 15 : 2 -> la mitad: 7 y sobra 1", D("15 : 2")[:2], ((7, 1), "dividir_a_la_mitad"))
    comprobar("C3 8 : 0 -> no se puede (entre nadie)", D("8 : 0")[2]["conclusion"], "imposible")
    comprobar("C4 30 : 5 sin las tablas en la memoria -> saltando", D("30 : 5")[:2], ((6, 0), "dividir_saltando"))
    motor.aprender("tablas", SABER)
    v, p, r = D("30 : 5")
    comprobar("C5 30 : 5 con las tablas aprendidas -> 6 x 5 = 30 (factor desconocido)", (v, p), ((6, 0), "dividir_con_la_tabla"))
    comprobar("C6 31 : 5 no esta en la tabla -> (desde M.11) la division corta: 6 y sobra 1", D("31 : 5")[:2], ((6, 1), "division_corta"))
    motor.olvidar_todo()

    print("\nD - CONTRA EL TESTIGO")
    fallos, comp = [], []
    for t in range(0, 101):
        for d in range(1, 11):
            v, p, r = D("%d : %d" % (t, d))
            if v != (t // d, t % d):
                fallos.append("%d:%d -> %s" % (t, d, v))
            if not r.get("comprobacion_ok"):
                comp.append("%d:%d" % (t, d))
    comprobar("D1 de 0 a 100 entre 1 a 10 (1010): cociente y resto", fallos[:3], [])
    comprobar("D2 y todas comprobadas multiplicando", comp[:3], [])
    comprobar("D3 dividir entre cero, siempre no", [D("%d : 0" % t)[2]["conclusion"] for t in (0, 5, 100)], ["imposible"] * 3)
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
