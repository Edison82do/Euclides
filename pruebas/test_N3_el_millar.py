# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO N.3: EL 1000 Y LOS NUMEROS DE CUATRO CIFRAS (NCETM 1.22; 4.NBT.A.1-3).
El plan y sus trampas: diario/2026-10-06-paso-N3-el-millar.md
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
TMP = tempfile.mkdtemp(prefix="n3_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia
import motor  # noqa: E402
import probar  # noqa: E402
from _muestras import modo, numeros  # noqa: E402

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


# --- el TESTIGO: los nombres en castellano, escritos aparte (otra implementacion)
U = "cero uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciseis diecisiete dieciocho diecinueve".split()
VEINTI = {20: "veinte", 21: "veintiuno", 22: "veintidos", 23: "veintitres", 24: "veinticuatro", 25: "veinticinco",
          26: "veintiseis", 27: "veintisiete", 28: "veintiocho", 29: "veintinueve"}
D = {3: "treinta", 4: "cuarenta", 5: "cincuenta", 6: "sesenta", 7: "setenta", 8: "ochenta", 9: "noventa"}
C = {1: "ciento", 2: "doscientos", 3: "trescientos", 4: "cuatrocientos", 5: "quinientos", 6: "seiscientos",
     7: "setecientos", 8: "ochocientos", 9: "novecientos"}


def nombre_testigo(n):
    if n < 20:
        return U[n]
    if n < 30:
        return VEINTI[n]
    if n < 100:
        return D[n // 10] + ("" if n % 10 == 0 else " y " + U[n % 10])
    if n == 100:
        return "cien"
    if n < 1000:
        return C[n // 100] + ("" if n % 100 == 0 else " " + nombre_testigo(n % 100))
    if n == 10000:
        return "diez mil"
    m = "mil" if n // 1000 == 1 else U[n // 1000] + " mil"
    return m + ("" if n % 1000 == 0 else " " + nombre_testigo(n % 1000))


def signo(a, b):
    return ">" if a > b else "<" if a < b else "="


print("=" * 78)
print("PASO N.3 - EL 1000 Y LOS NUMEROS DE CUATRO CIFRAS  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRAMPAS DEL PLAN")
    comprobar("A1 nombre: 2005 -> dos mil cinco", S("nombre: 2005"), "dos mil cinco")
    comprobar("A2 numero: dos mil cinco -> 2005 (no 20005 ni 205)", S("numero: dos mil cinco"), "2005")
    comprobar("A3 nombre: 1000 -> mil (no 'un mil');  1001 -> mil uno", (S("nombre: 1000"), S("nombre: 1001")), ("mil", "mil uno"))
    r = motor.decidir_millar(3045, SABER)
    comprobar("A4 millar: 3045 -> 30 centenas aunque la cifra sea 0; 304 decenas",
              (r["cuantas"]["centenas"], r["cuantas"]["decenas"]), (30, 304))
    comprobar("A5 millar: 3045 -> 3000 + 40 + 5", S("millar: 3045"), "3000 + 40 + 5")
    comprobar("A6 comparar 999 y 1000 -> 1000 (mas cifras)", S("comparar: 999 y 1000"), "999 < 1000")
    comprobar("A7 comparar 3456 y 3465 -> decide la de las decenas", S("comparar: 3456 y 3465"), "3456 < 3465")
    comprobar("A8 comparar 4999 y 5001 -> decide el millar", S("comparar: 4999 y 5001"), "4999 < 5001")
    comprobar("A9 redondear 3456 al millar -> 3000;  3500 -> 4000;  9500 -> 10000",
              (S("redondear: 3456 al millar"), S("redondear: 3500 al millar"), S("redondear: 9500 al millar")),
              ("3000", "4000", "10000"))
    comprobar("A10 columnas: 2345 + 1678 -> 4023", "4023" in S("columnas: 2345 + 1678"), True)
    comprobar("A11 300 + 800 -> 1100 (11 centenas)", S("300 + 800"), "1100")
    t = motor.explicar_pregunta(probar.como_problema("300 + 800"), SABER)
    comprobar("A12 ... contando centenas como cosas", "11 centenas" in t, True)
    comprobar("A13 nombre: 10001 -> todavia no (5.o)", S("nombre: 10001"), "fuera_de_mi_secuencia")
    comprobar("A14 de 1000 en 1000", S("de 1000 en 1000"), "1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000")
    t = motor.explicar_pregunta("millar: 1000", SABER)
    comprobar("A15 mil = 10 centenas = 100 decenas; 2 x 500, 4 x 250, 5 x 200",
              ("10 centenas = 100 decenas = 1000 unidades" in t, "4 x 250 = 1000" in t), (True, True))

    print("\nB - LOS NOMBRES DE 1 A 10000 (todos) CONTRA EL TESTIGO, Y LA VUELTA")
    malos = [n for n in range(1, 10001) if motor.decir(n, SABER) != nombre_testigo(n)]
    comprobar("B1 los 10000 nombres", malos[:3], [])
    malos = [n for n in numeros(1, 10000) if motor.leer(nombre_testigo(n), SABER) != n]
    comprobar("B2 nombre -> numero (muestra)", malos[:3], [])

    print("\nC - COMPARAR POR LAS CIFRAS (muestra) CONTRA EL TESTIGO, Y CON LA LISTA")
    rnd = random.Random(1022)
    pares = [(rnd.randint(0, 10000), rnd.randint(0, 10000)) for _ in range(300)] + \
            [(rnd.randint(1000, 9999), 0) for _ in range(20)] + [(999, 1000), (1000, 999), (5000, 5000), (4999, 5001)]
    pares += [(a, a + d) for a in (1234, 5050, 9000) for d in (1, 10, 100, 1000) if a + d <= 10000]
    malos = []
    for a, b in pares:
        r = motor.decidir_comparar_numeros(a, b, SABER)
        if r["valor"] != signo(a, b) or not r.get("lista_ok"):
            malos.append((a, b, r["valor"]))
    comprobar("C1 %d parejas" % len(pares), malos[:3], [])

    print("\nD - DESCOMPONER (muestra)")
    malos = []
    for n in numeros(0, 10000):
        r = motor.decidir_millar(n, SABER)
        c = r["cuantas"]
        if (c["millares"], c["centenas"], c["decenas"], c["unidades"]) != (n // 1000, n // 100, n // 10, n):
            malos.append(n)
        if sum(x["vale"] for x in r["sitios"]) != n:
            malos.append(("suma", n))
    comprobar("D1 cuantos millares, centenas, decenas y unidades; y la suma de los valores", malos[:3], [])

    print("\nE - REDONDEAR AL MILLAR (muestra), los dos caminos")
    malos = []
    for n in numeros(0, 10000):
        r = motor.decidir_redondear(n, "millar", SABER)
        if r["conclusion"] != "hecho" or r["valor"] != (n + 500) // 1000 * 1000 or len(r["todos"]) != 2:
            malos.append((n, r.get("valor")))
    comprobar("E1 al millar", malos[:3], [])

    print("\nF - LO DE TRES CIFRAS SIRVE PARA CUATRO: COLUMNAS Y CENTENAS JUSTAS (muestra)")
    malos = []
    for _ in range(60):
        a, b = rnd.randint(0, 6000), rnd.randint(0, 4000)
        r = motor.aplicar("sumar", {"a": a, "b": b}, SABER)
        if r.get("valor") != a + b:
            malos.append((a, "+", b, r.get("valor")))
        x, y = max(a, b), min(a, b)
        r = motor.aplicar("restar", {"a": x, "b": y}, SABER)
        if r.get("valor") != x - y:
            malos.append((x, "-", y, r.get("valor")))
    for a in range(100, 6000, 700):
        for b in range(100, 4000, 900):
            r = motor.aplicar("sumar", {"a": a // 100 * 100, "b": b // 100 * 100}, SABER)
            if r.get("valor") != a // 100 * 100 + b // 100 * 100 or r["pieza"]["id"] != "sumar_centenas_justas":
                malos.append(("centenas", a, b, r.get("valor"), r.get("pieza", {}).get("id")))
    comprobar("F1 sumas y restas de cuatro cifras; centenas justas contando centenas", malos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("-" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
