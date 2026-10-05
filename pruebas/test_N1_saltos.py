# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO N.1: CONTAR DE n EN n (2.NBT.A.2) Y PAR O IMPAR (2.OA.C.3); NCETM 2.1.
El plan y sus trampas: diario/2026-10-05-paso-N1-par-impar-saltos.md
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
TMP = tempfile.mkdtemp(prefix="saltos_")
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
NUM = numeros(0, 1000)
DE = {"dos": 2, "cinco": 5, "diez": 10, "cien": 100}

print("=" * 78)
print("PASO N.1 - CONTAR DE n EN n; PAR E IMPAR  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - EL SALTO (mecanismo)")
    for de, k in DE.items():
        fallos = [n for n in NUM if motor.saltar(n, de, SABER) != (n + k if n + k <= 1000 else None)]
        comprobar("A un salto de %d desde cualquier numero (y None si pasa de mil)  (%d casos)" % (k, len(NUM)),
                  fallos[:3], [])

    print("\nB - LAS SERIES")
    r = motor.contar_de_en("dos", 0, 20, SABER)
    comprobar("B1 de 2 en 2 hasta 20", (r["serie"], r["llega"]), (list(range(2, 21, 2)), True))
    r = motor.contar_de_en("cinco", 0, 50, SABER)
    comprobar("B2 de 5 en 5 hasta 50", r["serie"], list(range(5, 51, 5)))
    r = motor.contar_de_en("cinco", 3, 50, SABER)
    comprobar("B3 de 5 en 5 desde 3: el 50 no se toca (48 -> 53)", (r["llega"], r["serie"][-1], r["despues"]), (False, 48, 53))
    r = motor.contar_de_en("diez", 47, 97, SABER)
    comprobar("B4 de 10 en 10 desde 47 hasta 97", r["serie"], [57, 67, 77, 87, 97])
    r = motor.contar_de_en("cien", 250, None, SABER)
    comprobar("B5 de 100 en 100 desde 250: se para antes de pasar de mil", (r["serie"][-1], r["se_sale"]), (950, True))
    t = motor.explicar_pregunta("de 3 en 3 hasta 30", SABER)
    comprobar("B6 de 3 en 3 todavia no (no esta en el estandar de 2.o)", t.startswith("NO ENTIENDO"), True)

    print("\nC - PAR O IMPAR")
    fallos_v, fallos_p = [], []
    for n in NUM:
        r = motor.decidir_paridad(n, SABER)
        if r["valor"] != ("par" if n % 2 == 0 else "impar"):
            fallos_v.append(n)
        if r["pieza"]["id"] != ("par_emparejando" if n <= 20 else "par_por_la_ultima_cifra"):
            fallos_p.append(n)
    comprobar("C1 par o impar de 0 a 1000 contra el testigo  (%d casos)" % len(NUM), fallos_v[:3], [])
    comprobar("C2 hasta 20 empareja (2.OA.C.3); despues mira la ultima cifra", fallos_p[:3], [])
    r = motor.decidir_paridad(14, SABER)
    comprobar("C3 14 es par y es un doble: 14 = 7 + 7", "14 = 7 + 7" in r["resultado"]["cuenta"], True)
    r = motor.decidir_paridad(7, SABER)
    comprobar("C4 7: tres parejas y uno suelto", "tres parejas y uno suelto" in r["resultado"]["cuenta"], True)
    comprobar("C5 0 es par (cero parejas, no sobra ninguno)", motor.decidir_paridad(0, SABER)["valor"], "par")
    r = motor.decidir_paridad(846, SABER)
    comprobar("C6 846: dice POR QUE basta la ultima cifra (diez se empareja entero)",
              (r["valor"], "diez se empareja entero" in r["resultado"]["cuenta"]), ("par", True))

    print("\nD - CONTAR HASTA, SALTANDO DE DIEZ (lo pendiente de E.1)")
    r = motor.decidir_ecuacion("47 + ? = 77", SABER)
    calc = r["paso"]["resultado"]
    comprobar("D1 47 + ? = 77 -> 30 saltando: 57, 67, 77",
              (r["valor"], calc["pieza"]["id"], "57, 67, 77" in calc["resultado"]["cuenta"]),
              (30, "contar_hasta_de_diez_en_diez", True))
    r = motor.decidir_ecuacion("47 + ? = 78", SABER)
    comprobar("D2 47 + ? = 78: las unidades no son iguales -> se cuenta", (r["valor"], r["paso"]["resultado"]["pieza"]["id"]),
              (31, "contar_desde_hasta"))
    fallos = []
    for a in NUM:
        for k in range(0, 10):
            b = a + 10 * k
            if b > 1000:
                continue
            r = motor.aplicar("contar_hasta", {"a": a, "b": b}, SABER)
            if r["valor"] != b - a or r["pieza"]["id"] != "contar_hasta_de_diez_en_diez" or not r["resultado"]["vuelta_ok"]:
                fallos.append("%d->%d" % (a, b))
    comprobar("D3 muestra: de a hasta a + 10, 20 ... 90 saltando, con la vuelta", fallos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
