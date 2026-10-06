# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.8: LA DIVISION CON RESTO (NCETM 2.12; 4.NBT.B.6, 4.OA.A.3).
El plan y sus trampas: diario/2026-10-06-paso-M8-division-con-resto.md
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
TMP = tempfile.mkdtemp(prefix="m8_")
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


def P(t):
    r = motor.decidir_R2_problema(t, SABER)
    return (r.get("valor"), r.get("resto")) if r["conclusion"] == "hecho" else r["conclusion"]


print("=" * 78)
print("PASO M.8 - LA DIVISION CON RESTO  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRAMPAS DEL PLAN")
    comprobar("A1 17 : 5 -> 3 resto 2", S("17 : 5"), "3 resto 2")
    t = motor.explicar_pregunta("17 : 5", SABER)
    comprobar("A2 ... con la ecuacion 17 = 3 x 5 + 2 y el resto menor que el divisor",
              ("17 = 3 x 5 + 2" in t, "MENOR que el divisor" in t), (True, True))
    t = motor.explicar_pregunta("15 : 5", SABER)
    comprobar("A3 15 : 5 -> sin resto: multiplo", "MULTIPLO de 5" in t, True)
    comprobar("A4 coches que hacen falta -> 4 (arriba)", P("Hay 17 ninos. En cada coche caben 5. Cuantos coches hacen falta?"), (4, 0))
    comprobar("A5 libros que puede comprar -> 3 (abajo)", P("Tiene 17 euros. Cada libro cuesta 5 euros. Cuantos libros puede comprar?"), (3, 0))
    comprobar("A6 cuantos sobran -> 2", P("Reparte 17 caramelos entre 5 ninos. Cuantos sobran?"), (2, 0))
    comprobar("A7 sin decir como, se dice el resto: 3 y sobran 2", P("Mete 17 caramelos en bolsas de 5. Cuantas bolsas salen?"), (3, 2))
    comprobar("A8 sin resto no hay que interpretar: 15 ninos -> 3 coches", P("Hay 15 ninos. En cada coche caben 5. Cuantos coches hacen falta?"), (3, 0))
    comprobar("A9 comprobar: 17 : 5 = 2 resto 7 -> no (el resto no es menor)", S("comprobar: 17 : 5 = 2 resto 7"), "no")
    comprobar("A10 comprobar: 17 : 5 = 3 resto 1 -> no;  3 resto 2 -> si",
              (S("comprobar: 17 : 5 = 3 resto 1"), S("comprobar: 17 : 5 = 3 resto 2")), ("no", "si"))
    comprobar("A11 coche/coches: el plural no confunde", P("Hay 20 ninos. En cada coche caben 4. Cuantos coches hacen falta?"), (5, 0))

    print("\nB - TODAS LAS DIVISIONES 0..200 ENTRE 1..12 (cociente, resto < divisor) CONTRA EL TESTIGO")
    malos = []
    for d in range(1, 13):
        for t in range(0, 201):
            r = motor.decidir_dividir("%d : %d" % (t, d), SABER)
            if (r.get("valor"), r.get("resto")) != (t // d, t % d) or not r.get("comprobacion_ok"):
                malos.append((t, d, r.get("valor"), r.get("resto")))
    comprobar("B1 2412 divisiones", malos[:3], [])

    print("\nC - COMPROBAR RESPUESTAS (buenas y malas)")
    rnd = random.Random(212)
    malos = []
    for _ in range(150):
        d = rnd.randint(2, 12)
        t = rnd.randint(0, 150)
        q, r0 = t // d, t % d
        for (qq, rr) in ((q, r0), (q - 1, r0 + d), (q, r0 + 1), (q + 1, r0)):
            if qq < 0 or rr < 0 or (qq == q + 1 and False):
                continue
            esperado = "si" if qq * d + rr == t and rr < d else "no"
            if motor.decidir_comprobar_division(t, d, qq, rr, SABER)["valor"] != esperado:
                malos.append((t, d, qq, rr))
    comprobar("C1 600 respuestas: bien solo si la vuelta cuadra y el resto es menor que el divisor", malos[:3], [])

    print("\nD - LOS TRES PROBLEMAS (muestra)")
    malos = []
    for _ in range(40):
        d = rnd.randint(2, 9)
        t = rnd.randint(d, 90)
        q, r0 = t // d, t % d
        a = P("Hay %d ninos. En cada coche caben %d. Cuantos coches hacen falta?" % (t, d))
        b = P("Tiene %d euros. Cada libro cuesta %d euros. Cuantos libros puede comprar?" % (t, d))
        c = P("Reparte %d caramelos entre %d ninos. Cuantos sobran?" % (t, d))
        if a != (q + (1 if r0 else 0), 0) or b != (q, 0) or c != (r0, 0):
            malos.append((t, d, a, b, c))
    comprobar("D1 arriba, abajo y el resto, en 40 problemas", malos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("-" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
