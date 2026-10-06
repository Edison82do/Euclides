# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO G.1: AREA Y PERIMETRO (NCETM 2.16; 3.MD.C.7, 3.MD.D.8, 4.MD.A.3).
El plan y sus trampas: diario/2026-10-07-paso-G1-area-perimetro.md
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
TMP = tempfile.mkdtemp(prefix="g1_")
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
print("PASO G.1 - AREA Y PERIMETRO  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRAMPAS DEL PLAN")
    comprobar("A1 area 5 x 3 -> 15 (no 16);  perimetro -> 16 (no 15)",
              (S("area: rectangulo 5 x 3"), S("perimetro: rectangulo 5 x 3")), ("15 unidades cuadradas", "16"))
    comprobar("A2 cuadrado de 6: perimetro 24 (no 36), area 36",
              (S("perimetro: cuadrado de 6"), S("area: cuadrado de 6")), ("24", "36 unidades cuadradas"))
    comprobar("A3 lado de un cuadrado de perimetro 24 -> 6;  de 25 -> no sale",
              (S("lado: cuadrado de perimetro 24"), S("lado: cuadrado de perimetro 25")), ("6", "no_sale"))
    comprobar("A4 triangulo de 5 -> 15;  hexagono de 5 cm -> 30 cm",
              (S("perimetro: triangulo de 5"), S("perimetro: hexagono de 5 cm")), ("15", "30 cm"))
    comprobar("A5 lados 4, 7, 5 -> 16", S("perimetro: 4, 7, 5"), "16")
    comprobar("A6 compuesta 6 x 4 + 3 x 2 -> 30", S("area: 6 x 4 + 3 x 2"), "30 unidades cuadradas")
    comprobar("A7 6 x 2 y 4 x 3: misma area, distinto perimetro",
              S("comparar: rectangulo 6 x 2 y rectangulo 4 x 3"), "area igual, perimetro distinto")
    comprobar("A8 con unidades: 5 cm x 3 cm -> 15 cm cuadrados", S("area: rectangulo 5 cm x 3 cm"), "15 cm cuadrados")
    comprobar("A9 decagono de 3 -> 30;  'estrella de 3' -> no entiendo",
              (S("perimetro: decagono de 3"), S("perimetro: estrella de 3")), ("30", "no_entiendo"))

    print("\nB - RECTANGULOS DE 1x1 A 12x12 CONTRA EL TESTIGO")
    malos = []
    for a in range(1, 13):
        for b in range(1, 13):
            ra = motor.decidir_area_rectangulo(a, b, SABER)
            rp = motor.decidir_perimetro_rectangulo(a, b, SABER)
            if ra["valor"] != a * b or not ra["comprobacion_ok"] or rp["valor"] != 2 * (a + b) or not rp["comprobacion_ok"]:
                malos.append((a, b, ra["valor"], rp["valor"]))
    comprobar("B1 144 rectangulos: area (por filas y multiplicando) y perimetro (sumando y 2 x)", malos[:3], [])

    print("\nC - POLIGONOS REGULARES Y COMPUESTAS")
    nombres = {3: "triangulo", 4: "cuadrado", 5: "pentagono", 6: "hexagono", 7: "heptagono", 8: "octogono", 9: "eneagono", 10: "decagono"}
    malos = []
    for n, f in nombres.items():
        for lado in range(1, 21):
            if S("perimetro: %s de %d" % (f, lado)) != str(n * lado):
                malos.append((f, lado))
            if S("lado: %s de perimetro %d" % (f, n * lado)) != str(lado):
                malos.append(("lado", f, lado))
    comprobar("C1 8 poligonos x 20 lados, y lo inverso", malos[:3], [])
    rnd = random.Random(216)
    malos = []
    for _ in range(50):
        a, b, c, d = [rnd.randint(1, 12) for _ in range(4)]
        if S("area: %d x %d + %d x %d" % (a, b, c, d)) != "%d unidades cuadradas" % (a * b + c * d):
            malos.append((a, b, c, d))
    comprobar("C2 50 figuras compuestas de dos rectangulos", malos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("-" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
