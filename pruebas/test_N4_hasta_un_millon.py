# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO N.4: HASTA UN MILLON (NCETM 1.26; Common Core 4.NBT.A.1-3, 4.NBT.B.4-5).
El plan y sus trampas: diario/2026-10-07-paso-N4-hasta-un-millon.md
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
TMP = tempfile.mkdtemp(prefix="n4_")
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


# --- el TESTIGO: los nombres en castellano, escritos aparte (otra implementacion)
U = ("cero uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciseis "
     "diecisiete dieciocho diecinueve").split()
VEINTI = {20: "veinte", 21: "veintiuno", 22: "veintidos", 23: "veintitres", 24: "veinticuatro", 25: "veinticinco",
          26: "veintiseis", 27: "veintisiete", 28: "veintiocho", 29: "veintinueve"}
D = {3: "treinta", 4: "cuarenta", 5: "cincuenta", 6: "sesenta", 7: "setenta", 8: "ochenta", 9: "noventa"}
C = {1: "ciento", 2: "doscientos", 3: "trescientos", 4: "cuatrocientos", 5: "quinientos", 6: "seiscientos",
     7: "setecientos", 8: "ochocientos", 9: "novecientos"}


def bajo_mil(n):
    if n < 20:
        return U[n]
    if n < 30:
        return VEINTI[n]
    if n < 100:
        return D[n // 10] + ("" if n % 10 == 0 else " y " + U[n % 10])
    if n == 100:
        return "cien"
    return C[n // 100] + ("" if n % 100 == 0 else " " + bajo_mil(n % 100))


def nombre_testigo(n):
    if n == 1000000:
        return "un millon"
    if n < 1000:
        return bajo_mil(n)
    m = n // 1000
    if m == 1:
        miles = "mil"
    else:
        miles = bajo_mil(m)
        if miles.endswith("veintiuno"):
            miles = miles[:-len("veintiuno")] + "veintiun"
        elif miles.endswith("uno"):
            miles = miles[:-3] + "un"
        miles += " mil"
    return miles + ("" if n % 1000 == 0 else " " + bajo_mil(n % 1000))


def signo(a, b):
    return ">" if a > b else "<" if a < b else "="


FRONTERAS = [9999, 10000, 10001, 19999, 20000, 21000, 31000, 99999, 100000, 100001, 101000, 199999, 200005,
             999000, 999999, 1000000]
azar = random.Random(20261007)
MUESTRA = sorted(set(FRONTERAS) | set(azar.sample(range(10001, 1000000), 300)))

print("=" * 78)
print("PASO N.4 - HASTA UN MILLON  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRAMPAS DEL PLAN (los nombres)")
    comprobar("A1 21000 -> veintiun mil (no 'veintiuno mil')", S("nombre: 21000"), "veintiun mil")
    comprobar("A2 101000 -> ciento un mil", S("nombre: 101000"), "ciento un mil")
    comprobar("A3 200005 -> doscientos mil cinco (los ceros del medio no se dicen)", S("nombre: 200005"),
              "doscientos mil cinco")
    comprobar("A4 1000000 -> un millon", S("nombre: 1000000"), "un millon")
    comprobar("A5 1000001: mas alla del millon no me lo invento", S("nombre: 1000001"), "fuera_de_mi_secuencia")
    comprobar("A6 numero: ciento un mil -> 101000", S("numero: ciento un mil"), "101000")
    comprobar("A7 numero: trescientos cuarenta y cinco mil seiscientos setenta y ocho -> 345678",
              S("numero: trescientos cuarenta y cinco mil seiscientos setenta y ocho"), "345678")

    print("\nB - CONTRA EL TESTIGO (muestra de %d numeros, fronteras incluidas)" % len(MUESTRA))
    mal = [n for n in MUESTRA if motor.decir(n, SABER) != nombre_testigo(n)]
    comprobar("B1 decir(n) = el nombre del testigo", mal[:3], [])
    mal = [n for n in MUESTRA if motor.leer(nombre_testigo(n), SABER) != n]
    comprobar("B2 leer(nombre) = n (ida y vuelta)", mal[:3], [])

    print("\nC - SIGUIENTE Y ANTERIOR AL CRUZAR LAS FRONTERAS (NCETM 1.26)")
    for a, b in ((9999, 10000), (99999, 100000), (109999, 110000), (999999, 1000000)):
        comprobar("C %d -> %d" % (a, b), motor.leer(motor.siguiente(motor.decir(a, SABER), SABER), SABER), b)
        comprobar("C %d <- %d" % (a, b), motor.leer(motor.anterior(motor.decir(b, SABER), SABER), SABER), a)
    comprobar("C9 de 10000 en 10000 desde 970000 llega al millon y se para",
              S("de 10000 en 10000 desde 970000"), "980000, 990000, 1000000")
    comprobar("C10 de 100000 en 100000 desde 0", S("de 100000 en 100000 desde 0"),
              "100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000")
    comprobar("C11 contar con los dedos cruzando 100000: 99998 + 4", S("dedos: 99998 + 4"),
              "noventa y nueve mil novecientos noventa y ocho + cuatro = cien mil dos")

    print("\nD - EL VALOR DE CADA CIFRA Y COMPARAR")
    comprobar("D1 millar: 345678 -> 300000 + 40000 + 5000 + 600 + 70 + 8", S("millar: 345678"),
              "300000 + 40000 + 5000 + 600 + 70 + 8")
    comprobar("D2 99999 < 100000 (mas cifras gana)", S("comparar: 99999 y 100000"), "99999 < 100000")
    comprobar("D3 345678 < 345687 (la primera distinta)", S("comparar: 345678 y 345687"), "345678 < 345687")
    pares = [(azar.randint(10000, 999999), azar.randint(10000, 999999)) for _ in range(60)]
    mal = [(a, b) for a, b in pares if S("comparar: %d y %d" % (a, b)) != "%d %s %d" % (a, signo(a, b), b)]
    comprobar("D4 comparar contra el testigo (60 pares)", mal[:3], [])

    print("\nE - SUMAR Y RESTAR (el mil como una cosa; las columnas)")
    comprobar("E1 345000 + 278000 = 623000 (345 mil + 278 mil)", S("345000 + 278000"), "623000")
    r = motor.aplicar("sumar", {"a": 345000, "b": 278000}, SABER)
    comprobar("E2 ... y lo hace contando MILES", "345 mil + 278 mil = 623 mil" in r["resultado"]["cuenta"], True)
    comprobar("E3 623000 - 278000 = 345000", S("623000 - 278000"), "345000")
    comprobar("E4 600000 + 500000: se pasa del millon -> ninguna", S("600000 + 500000"), "ninguna")
    comprobar("E5 columnas: 456789 + 123456", S("columnas: 456789 + 123456"), "456789 + 123456 = 580245")
    comprobar("E6 columnas: 500000 - 1 (cambiar a traves de cinco ceros)", S("columnas: 500000 - 1"),
              "500000 - 1 = 499999")
    mal = []
    for _ in range(40):
        a, b = azar.randint(10000, 500000), azar.randint(10000, 499999)
        if S("columnas: %d + %d" % (a, b)) != "%d + %d = %d" % (a, b, a + b):
            mal.append((a, b))
        x, y = max(a, b), min(a, b)
        if S("columnas: %d - %d" % (x, y)) != "%d - %d = %d" % (x, y, x - y):
            mal.append((x, y))
    comprobar("E7 columnas contra el testigo (40 sumas y 40 restas)", mal[:3], [])

    print("\nF - MULTIPLICAR Y DIVIDIR CON NUMEROS GRANDES")
    # PASO M.14 (7 oct): con la memoria vacia este caso lo resolvia dividir_saltando con 25 000 SALTOS de 4 (no la
    # division corta que dice probar).  Ahora saltar mas de mil veces no se hace; la division corta necesita
    # las tablas: se aprenden antes, como en el PC de Carlos.  (El caso viejo: S("100000 : 4") con memoria vacia.)
    motor.aprender("tablas", SABER)
    comprobar("F1 100000 : 4 = 25000 (antes la division corta se comia una cifra)",
              (S("100000 : 4"), motor.aplicar("dividir", {"total": 100000, "divisor": 4}, SABER)["pieza"]["id"]),
              ("25000", "division_corta"))
    comprobar("F2 18 x 38 = 684 (la rejilla: los dos por sitios)", S("18 x 38"), "684")
    r = motor.aplicar("multiplicar", {"a": 18, "b": 38}, SABER)
    comprobar("F3 ... y la rejilla dice sus casillas: 300 + 80 + 240 + 64",
              (r["pieza"]["id"], "300 + 80 + 240 + 64 = 684" in r["resultado"]["cuenta"]),
              ("multiplicar_en_rejilla", True))
    mal = []
    for _ in range(30):
        a, b = azar.randint(10, 99), azar.randint(10, 99)
        if S("%d x %d" % (a, b)) != str(a * b):
            mal.append((a, b))
    comprobar("F4 dos cifras por dos cifras contra el testigo (30)", mal[:3], [])
    comprobar("F5 99999 x 100 se pasa del millon", S("99999 x 100"), "no_se_puede")
    comprobar("F6 250000 x 8 se pasa del millon (antes REVENTABA: una condicion con un numero sin nombre)",
              S("250000 x 8"), "no_se_puede")
    comprobar("F7 241961 : 243225 = 0 resto 241961, y rapido (los saltos grandes se SUMAN, no se cuentan)",
              S("241961 : 243225"), "0 resto 241961")

    print("\nG - REDONDEAR A LA DECENA Y CENTENA DE MILLAR")
    comprobar("G1 redondear: 345678", S("redondear: 345678"),
              "decena 345680, centena 345700, millar 346000, decena de millar 350000, centena de millar 300000")
    comprobar("G2 redondear: 950000 a la centena de millar -> 1000000",
              S("redondear: 950000 a la centena de millar"), "1000000")
    comprobar("G3 redondear: 84999 a la decena de millar -> 80000",
              S("redondear: 84999 a la decena de millar"), "80000")

    print("\nH - LOS DOS TECHOS (lo que se cuenta con objetos no cambia)")
    comprobar("H1 la lista de CONTAR objetos sigue en diez mil", motor.techo_de_contar(SABER), "diez mil")
    comprobar("H2 los NUMEROS llegan al millon", motor.numero_maximo(SABER), 1000000)
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
