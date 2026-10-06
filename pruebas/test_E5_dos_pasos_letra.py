# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO E.5: DOS PASOS, CON LA LETRA COMO HUECO (Common Core 3.OA.D.8).
El plan y sus trampas: diario/2026-10-06-paso-E5-dos-pasos-letra.md
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
TMP = tempfile.mkdtemp(prefix="e5_")
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


def L(texto):
    r = motor.decidir_ecuacion_letra(texto, SABER)
    return r.get("valor") if r["conclusion"] == "hecho" else r["conclusion"]


def testigo(a, o1, b, o2, c):
    """El testigo externo: Python, con su propio orden de operaciones."""
    py = {"+": "+", "-": "-", "x": "*", ":": "//"}
    return eval("%d %s %d %s %d" % (a, py[o1], b, py[o2], c))


def valida(a, o1, b, o2, c):
    """Solo cuentas que Euclides sabe hacer: sin negativos y con divisiones justas."""
    def paso(x, o, y):
        if o == "-" and x < y:
            return None
        if o == ":" and (y == 0 or x % y):
            return None
        return {"+": x + y, "-": x - y, "x": x * y, ":": x // y if y else None}[o]
    fuertes = ("x", ":")
    if o2 in fuertes and o1 not in fuertes:
        d = paso(b, o2, c)
        return None if d is None else paso(a, o1, d)
    d = paso(a, o1, b)
    return None if d is None else paso(d, o2, c)


print("=" * 78)
print("PASO E.5 - DOS PASOS, CON LA LETRA COMO HUECO  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRAMPAS DEL PLAN (3.OA.D.8)")
    comprobar("A1 3 x 4 - 5 = c -> 7 (primero la multiplicacion)", L("3 x 4 - 5 = c"), 7)
    comprobar("A2 2 + 3 x 4 = n -> 14, NO 20", L("2 + 3 x 4 = n"), 14)
    comprobar("A3 y avisa del orden de siempre",
              "nota_orden" in motor.decidir_ecuacion_letra("2 + 3 x 4 = n", SABER), True)
    comprobar("A4 (2 + 3) x 4 = n -> 20 (el parentesis manda)", L("(2 + 3) x 4 = n"), 20)
    comprobar("A5 3 x n + 2 = 14 -> 4 (deshacer)", L("3 x n + 2 = 14"), 4)
    comprobar("A6 x + 5 = 12 -> 7 (la x es letra)", L("x + 5 = 12"), 7)
    comprobar("A7 20 - 2 x n = 8 -> 6", L("20 - 2 x n = 8"), 6)
    comprobar("A8 12 : n = 3 -> 4 (la letra de divisor)", L("12 : n = 3"), 4)
    comprobar("A9 n + n = 10 -> todavia_no (la letra dos veces)", L("n + n = 10"), "todavia_no")
    comprobar("A10 3 x n + 2 = 13 -> no_sale (no hay numero entero)", L("3 x n + 2 = 13"), "no_sale")
    comprobar("A11 la letra a la izquierda: c = 3 x 4 - 5 -> 7", L("c = 3 x 4 - 5"), 7)
    comprobar("A12 10 - 3 - 2 = n -> 5 (de izquierda a derecha, no 10 - 1)", L("10 - 3 - 2 = n"), 5)
    comprobar("A13 24 : 4 : 2 = n -> 3 (de izquierda a derecha, no 24 : 2)", L("24 : 4 : 2 = n"), 3)

    print("\nB - EL ORDEN DE SIEMPRE, CONTRA EL TESTIGO (muestra fija)")
    rnd = random.Random(55)
    ops = ["+", "-", "x", ":"]
    malos, vistos = [], 0
    while vistos < 120:
        a, b, c = rnd.randint(1, 10), rnd.randint(1, 10), rnd.randint(1, 10)
        o1, o2 = rnd.choice(ops), rnd.choice(ops)
        if o1 == ":":
            a = a * b
        if o2 == ":" and o1 not in ("x", ":"):
            b = b * c
        v = valida(a, o1, b, o2, c)
        if v is None:
            continue
        vistos += 1
        t = "%d %s %d %s %d = n" % (a, o1, b, o2, c)
        if L(t) != testigo(a, o1, b, o2, c):
            malos.append((t, L(t), testigo(a, o1, b, o2, c)))
    comprobar("B1 %d expresiones de dos operaciones: igual que el testigo" % vistos, malos[:3], [])

    print("\nC - LA LETRA EN CADA SITIO: DESHACER Y COMPROBAR")
    malos, vistos = [], 0
    while vistos < 60:
        a, b, c = rnd.randint(1, 10), rnd.randint(1, 10), rnd.randint(1, 10)
        o1, o2 = rnd.choice(ops), rnd.choice(ops)
        if o1 == ":":
            a = a * b
        if o2 == ":" and o1 not in ("x", ":"):
            b = b * c
        v = valida(a, o1, b, o2, c)
        if v is None:
            continue
        vistos += 1
        nums = [a, b, c]
        for i in range(3):
            partes = ["n" if j == i else str(nums[j]) for j in range(3)]
            t = "%s %s %s %s %s = %d" % (partes[0], o1, partes[1], o2, partes[2], v)
            r = motor.decidir_ecuacion_letra(t, SABER)
            # el valor puede no ser el original solo si hay otro que tambien cuadra; se pide la comprobacion
            if r["conclusion"] != "hecho" or not r.get("comprobacion_ok"):
                malos.append((t, r["conclusion"]))
            else:
                puesto = [r["valor"] if j == i else nums[j] for j in range(3)]
                if testigo(puesto[0], o1, puesto[1], o2, puesto[2]) != v:      # el testigo tambien lo pone
                    malos.append((t, r["valor"]))
    comprobar("C1 %d ecuaciones x 3 sitios: la letra se encuentra y comprueba" % vistos, malos[:3], [])

    print("\nD - LA x: LETRA O 'POR'; Y LO QUE NO ES DE AQUI")
    comprobar("D1 3 x x = 12 -> 4 (la primera x es 'por', la segunda letra)", L("3 x x = 12"), 4)
    comprobar("D2 8 + ? = 11 sigue siendo E.1", motor.es_ecuacion_con_letra("8 + ? = 11"), False)
    comprobar("D3 8 + 4 = ? + 5 sigue siendo la balanza E.2", motor.es_ecuacion_con_letra("8 + 4 = ? + 5"), False)
    comprobar("D4 3 x 4 = ? x 6 -> aqui, el hueco = 2", (motor.es_ecuacion_con_letra("3 x 4 = ? x 6"),
                                                       L("3 x 4 = ? x 6")), (True, 2))
    comprobar("D5 'verdad: 3 x 4 = 4 x 3' no es una letra (palabras)",
              motor.es_ecuacion_con_letra("verdad: 3 x 4 = 4 x 3"), False)
    comprobar("D5b '3 x 4 = 4 x 3' sin letra ni hueco es una igualdad (E.0), no de aqui",
              (motor.es_ecuacion_con_letra("3 x 4 = 4 x 3"), probar.preguntar(probar.como_problema("3 x 4 = 4 x 3"), SABER)[0]),
              (False, "verdadero"))
    comprobar("D6 sin letra: 2 + 3 x 4 = 14 -> sin_letra (eso es verdad:)", L("2 + 3 x 4 = 14"), "sin_letra")
    comprobar("D7 dos letras: a + b = 5 -> todavia_no", L("a + b = 5"), "todavia_no")
    comprobar("D8 parentesis sin cerrar -> no_entiendo", L("(2 + 3 x 4 = n"), "no_entiendo")

    print("\nE - PROBLEMAS DE DOS PASOS (un esquema y luego otro)")

    def PR(t):
        r = motor.decidir_R2_problema(t, SABER)
        return (r.get("valor"), r.get("ecuacion"), r.get("ecuacion_ok")) if r["conclusion"] == "hecho" \
            else r["conclusion"]
    comprobar("E1 3 bolsas de 4, se come 5 -> 7, 3 x 4 - 5 = c",
              PR("Ana tiene 3 bolsas con 4 caramelos cada una. Se come 5. Cuantos le quedan?"),
              (7, "3 x 4 - 5 = c", True))
    comprobar("E2 3 bolsas de 4, le dan 5 -> 17",
              PR("Ana tiene 3 bolsas con 4 caramelos cada una. Le dan 5. Cuantos tiene ahora?"),
              (17, "3 x 4 + 5 = c", True))
    comprobar("E3 se come 20 de 12 -> imposible",
              PR("Ana tiene 3 bolsas con 4 caramelos cada una. Se come 20. Cuantos le quedan?"), "imposible")
    comprobar("E4 sin cambio sigue siendo R.2: 12",
              PR("Hay 3 bolsas con 4 caramelos cada una. Cuantos caramelos hay?")[0], 12)

    print("\nF - EL PROBADOR")
    comprobar("F1 preguntar '3 x 4 - 5 = c' -> 7", probar.preguntar("3 x 4 - 5 = c", SABER)[0], "7")
    comprobar("F2 preguntar 'n + n = 10' -> todavia_no", probar.preguntar("n + n = 10", SABER)[0], "todavia_no")
    t = motor.explicar_pregunta("3 x n + 2 = 14", SABER)
    comprobar("F3 la explicacion deshace y comprueba",
              ("DESHACER" in t, "COMPRUEBO" in t, t.strip().splitlines()[-1]), (True, True, "RESULTADO: n = 4"))
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("-" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
