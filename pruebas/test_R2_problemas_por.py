# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO R.2: PROBLEMAS DE x Y : CON POCAS PALABRAS (3.OA.A.3; CGI; esquemas; barras).
El plan y sus trampas: diario/2026-10-05-paso-R2-problemas-por.md
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
TMP = tempfile.mkdtemp(prefix="r2_")
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


def P(texto):
    r = motor.decidir_R2_problema(texto, SABER)
    if r["conclusion"] != "hecho":
        return r["conclusion"], None, r
    return (r["valor"], r["resto"], r["unidad"]), r["paso"]["pieza"]["id"], r


print("=" * 78)
print("PASO R.2 - PROBLEMAS DE x Y :  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRES ESTRUCTURAS (CGI / NCETM 2.6)")
    comprobar("A1 3 bolsas con 4 caramelos cada una -> 12 caramelos (multiplicar)",
              P("Hay 3 bolsas con 4 caramelos cada una. Cuantos caramelos hay?")[:2],
              ((12, 0, "caramelos"), "juntar_grupos_iguales"))
    comprobar("A2 reparte 12 entre 3 ninos -> 4 a cada uno (repartir)",
              P("Reparte 12 caramelos entre 3 ninos. Cuantos le tocan a cada uno?")[:2],
              ((4, 0, "caramelos"), "repartir_en_partes_iguales"))
    comprobar("A3 mete 12 en bolsas de 4 -> 3 bolsas (agrupar)",
              P("Mete 12 caramelos en bolsas de 4. Cuantas bolsas salen?")[:2],
              ((3, 0, "bolsas"), "agrupar_en_grupos_iguales"))

    print("\nB - LAS TRES SITUACIONES (3.OA.A.3)")
    comprobar("B1 filas: 3 filas de 4 sillas -> 12 sillas", P("En el cine hay 3 filas de 4 sillas. Cuantas sillas hay?")[0],
              (12, 0, "sillas"))
    v, p, r = P("Cada caja pesa 5 kilos. Cuanto pesan 4 cajas?")
    comprobar("B2 medida: cada caja pesa 5 kilos, 4 cajas -> 20 kilos", (v, r["esquema"]["medida"]), ((20, 0, "kilos"), True))
    comprobar("B3 grupos con palabras de otra manera: 'Juan tiene 5 cajas de 6 galletas'",
              P("Juan tiene 5 cajas de 6 galletas. Cuantas galletas tiene?")[0], (30, 0, "galletas"))
    comprobar("B4 'hay 20 lapices en 4 cajas iguales' -> 5 en cada caja",
              P("Hay 20 lapices en 4 cajas iguales. Cuantos lapices hay en cada caja?")[0], (5, 0, "lapices"))

    print("\nC - CONTRA LAS PALABRAS CLAVE (el esquema se llena por los nombres)")
    v, p, r = P("Hay 12 caramelos. Cada nino tiene 3. Cuantos ninos hay?")
    comprobar("C1 'cada' con DIVIDIR: 12 caramelos, cada nino 3 -> 4 ninos", (v, p), ((4, 0, "ninos"), "agrupar_en_grupos_iguales"))
    v, p, r = P("Hay 4 cajas. Cada caja tiene 6 lapices. Cuantos lapices hay?")
    comprobar("C2 'cada' con MULTIPLICAR: 4 cajas, cada caja 6 -> 24", (v, p), ((24, 0, "lapices"), "juntar_grupos_iguales"))
    texto = "Ana y Luis tienen 12 entre los dos. Ana tiene 5. Cuantas tiene Luis?"
    comprobar("C3 'entre los dos' no es repartir: sigue siendo de R.1 (juntar) -> 7",
              (motor.es_problema_por(texto, SABER), motor.decidir_R1_problema(texto, SABER).get("valor")), (False, 7))
    comprobar("C4 'Ana tiene 5. Le dan 3...' sigue en R.1",
              motor.es_problema_por("Ana tiene 5 manzanas. Le dan 3. Cuantas tiene ahora?", SABER), False)

    print("\nD - LO QUE SOBRA, EL DIBUJO Y LA COMPROBACION")
    comprobar("D1 14 en bolsas de 4 -> 3 bolsas y sobran 2", P("Mete 14 caramelos en bolsas de 4. Cuantas bolsas salen?")[0],
              (3, 2, "bolsas"))
    t = motor.explicar_pregunta("problema: Reparte 12 caramelos entre 3 ninos. Cuantos le tocan a cada uno?", SABER)
    comprobar("D2 la barra antes y despues: [ ? | ? | ? ] y [ 4 | 4 | 4 ]", ("[ ? | ? | ? ]" in t, "[ 4 | 4 | 4 ]" in t), (True, True))
    comprobar("D3 y se comprueba con E.0: 3 x 4 = 12", "COMPRUEBO: 3 x 4 = 12 ... SI" in t, True)
    comprobar("D4 una frase que no entiende -> no entiendo (no adivina)",
              P("Hay 3 bolsas con 4 caramelos cada una. Las bolsas son azules. Cuantos caramelos hay?")[0], "no_entiendo")

    print("\nE - LA MUESTRA: LAS TRES ESTRUCTURAS CON NUMEROS AL AZAR")
    azar = random.Random(20261005)
    fallos, n = [], 0
    for _ in range(40):
        g, m = azar.randint(1, 10), azar.randint(1, 10)
        t_ = g * m
        for texto, esp in (("Hay %d bolsas con %d caramelos cada una. Cuantos caramelos hay?" % (g, m), t_),
                           ("Reparte %d caramelos entre %d ninos. Cuantos le tocan a cada uno?" % (t_, g), m),
                           ("Mete %d caramelos en bolsas de %d. Cuantas bolsas salen?" % (t_, m), g)):
            n += 1
            v, p, r = P(texto)
            if v == "no_entiendo" or v[0] != esp or not r.get("comprobacion_ok"):
                fallos.append("%s -> %s" % (texto, v))
    comprobar("E1 %d problemas, todos bien y comprobados" % n, fallos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
