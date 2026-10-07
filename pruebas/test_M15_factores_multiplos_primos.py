# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.15: FACTORES, MULTIPLOS, PRIMOS Y COMPUESTOS (NCETM 2.21; 4.OA.B.4).
El plan y sus trampas: diario/2026-10-07-paso-M15-factores-multiplos-primos.md
Python solo aparece aqui como TESTIGO externo (los restos con %, los productos con *).
"""
import os
import random
import shutil
import sys
import tempfile
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)
TMP = tempfile.mkdtemp(prefix="m15_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia (hasta la parte I)
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


def L(ns):
    return ", ".join(str(x) for x in ns)


def T_factores(n):
    """El testigo: los factores de n, con el % de Python."""
    return [d for d in range(1, n + 1) if n % d == 0]


def T_primo(n):
    if n < 2:
        return "ni_primo_ni_compuesto"
    return "primo" if len(T_factores(n)) == 2 else "compuesto"


print("=" * 78)
print("PASO M.15 - FACTORES, MULTIPLOS, PRIMOS Y COMPUESTOS  (%s)" % modo())
print("=" * 78)

try:
    print("\nA - LAS TRAMPAS DEL PLAN")
    comprobar("A1 primo: 1 -> ni primo ni compuesto (no 'primo')", S("primo: 1"), "ni_primo_ni_compuesto")
    comprobar("A2 primo: 2 -> primo (aunque sea par)", S("primo: 2"), "primo")
    comprobar("A3 primo: 91 -> compuesto (7 x 13: impar y compuesto)", S("primo: 91"), "compuesto")
    comprobar("A4 primo: 9 -> compuesto", S("primo: 9"), "compuesto")
    comprobar("A5 primo: 51 -> compuesto (5 + 1 = 6: 3 x 17)", S("primo: 51"), "compuesto")
    salida = motor.explicar_pregunta("primo: 51", SABER)
    comprobar("A6 ... por la regla corta de las cifras, con su pareja 3 x 17",
              ("sus cifras suman 51 -> 6" in salida, "3 x 17 = 51" in salida), (True, True))
    comprobar("A7 factores: 36 -> nueve factores, el 6 una sola vez", S("factores: 36"), "1, 2, 3, 4, 6, 9, 12, 18, 36")
    salida = motor.explicar_pregunta("factores: 36", SABER)
    comprobar("A8 ... impar porque es un CUADRADO (6 x 6)", "son 9 factores: IMPAR" in salida and "CUADRADO" in salida, True)
    comprobar("A9 factores: 12 -> con el 1 y el 12", S("factores: 12"), "1, 2, 3, 4, 6, 12")
    comprobar("A10 21 es multiplo de 7 -> si", S("21 es multiplo de 7"), "si")
    comprobar("A11 7 es multiplo de 21 -> NO (7 es factor de 21)", S("7 es multiplo de 21"), "no")
    salida = motor.explicar_pregunta("7 es multiplo de 21", SABER)
    comprobar("A12 ... y dice que es al reves: 7 es FACTOR de 21", "es AL REVES: 7 es FACTOR de 21" in salida, True)
    comprobar("A13 multiplos de 7 empieza en 7 (7 x 1), no en 0", S("multiplos de 7"), "7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84")
    comprobar("A14 factores: 169 -> todavia no (dividir entre 13: la division larga)", S("factores: 169"), "todavia_no")
    comprobar("A15 factores: 168 -> si (13 x 13 = 169 ya se pasa)", S("factores: 168"), L(T_factores(168)))
    comprobar("A16 primo: 1000 -> compuesto (2 x 500)", S("primo: 1000"), "compuesto")
    comprobar("A17 primo: 997 -> todavia no (sin regla corta y pide la division larga)", S("primo: 997"), "todavia_no")
    comprobar("A18 factores comunes: 7 y 13 -> solo el 1", S("factores comunes: 7 y 13"), "1")
    comprobar("A19 con 100: 25 x 36 -> 900 (36 = 9 x 4; 25 x 4 = 100)", S("con 100: 25 x 36"), "900")
    comprobar("A20 es 37 primo? escrito directamente (con su ?) -> primo", S("es 37 primo?"), "primo")
    comprobar("A21 7 es factor de 91 -> si", S("7 es factor de 91"), "si")
    comprobar("A22 primos hasta 100 -> los 25", S("primos hasta 100"),
              L([n for n in range(2, 101) if T_primo(n) == "primo"]))
    comprobar("A23 factores: 0 -> no se puede", S("factores: 0"), "no_se_puede")
    comprobar("A24 multiplos comunes: 4 y 6 -> 12, 24 ...", S("multiplos comunes: 4 y 6"), "12, 24, 36, 48, 60, 72")
    comprobar("A25 factores primos: 60 -> 2, 3, 5", S("factores primos: 60"), "2, 3, 5")
    comprobar("A26 lo de antes sigue: divisible: 51 entre 3", S("divisible: 51 entre 3"), "si")
    comprobar("A27 lo de antes sigue: 25 x 36 lo hace doblar y partir (M.12)",
              motor.aplicar("multiplicar", {"a": 25, "b": 36}, SABER)["pieza"]["id"], "multiplicar_escalando")

    print("\nB - CADA PIEZA SE COMPRUEBA CON LA OPERACION CONTRARIA (la vuelta de verdad)")
    base = motor.cargar_piezas()
    for pid, sit in (("parejas_de_factores_en_orden", {"n": 36}), ("primo_el_uno", {"n": 1}),
                     ("compuesto_por_una_regla_corta", {"n": 51}), ("primo_buscando_parejas", {"n": 37}),
                     ("multiplicar_con_las_parejas_de_100", {"a": 25, "b": 36})):
        r = motor.aplicar(pid, sit, SABER)
        res = r.get("resultado", {})
        comprobar("B %s: vuelta real (%s)" % (pid, res.get("vuelta")),
                  (r["conclusion"], bool(res.get("vuelta")), res.get("vuelta_ok")), ("hecho", True, True))
    p = base["piezas"]["parejas_de_factores_en_orden"]
    u = motor._Lo_que_puede_usar(p, base, SABER)
    vuelta = p["hacer"].__globals__["_vuelta"]
    comprobar("B la vuelta de las parejas CAZA una division falsa (36 : 5 = 7 y sobran 2)",
              vuelta(u, 36, [(5, 7, 2)])[1], False)
    comprobar("B ... y da por buena la verdadera (36 : 5 = 7 y sobra 1)", vuelta(u, 36, [(5, 7, 1)])[1], True)
    comprobar("B compuesto_por_una_regla_corta no le sale a 97 (ninguna regla): pasa a las parejas",
              motor.aplicar("compuesto_por_una_regla_corta", {"n": 97}, SABER)["conclusion"], "no_salio")

    print("\nC - DOMINIO: las parejas de factores de TODOS los numeros del 1 al 168, contra el testigo")
    malos, t0, lento = [], time.time(), 0.0
    for n in range(1, 169):
        t1 = time.time()
        r = motor.decidir_factores(n, SABER)
        lento = max(lento, time.time() - t1)
        tf = T_factores(n)
        cuadrado = any(d * d == n for d in range(1, n + 1))
        if r.get("factores") != tf or r.get("cuantos") != len(tf) or r.get("cuadrado") != cuadrado \
                or (len(tf) % 2 == 1) != cuadrado or not r.get("vuelta_ok"):
            malos.append(n)
    comprobar("C1 168 numeros: los factores, cuantos, impar <=> cuadrado, y la vuelta (%.1f s; el mas lento %.2f s)"
              % (time.time() - t0, lento), malos, [])
    comprobar("C2 cada uno en menos de 2 s", lento < 2, True)
    malos = [n for n in (169, 170, 200, 500, 1000) if motor.decidir_factores(n, SABER)["conclusion"] != "todavia_no"]
    comprobar("C3 desde 169: todavia no (169, 170, 200, 500, 1000)", malos, [])
    salida = motor.explicar_pregunta("factores: 100", SABER)
    comprobar("C4 factores: 100 dice las parejas de 100 (punto 6)", "LAS PAREJAS DE 100" in salida, True)

    print("\nD - DOMINIO: primo o compuesto del 0 al 168, contra el testigo")
    malos = []
    for n in range(0, 169):
        if S("primo: %d" % n) != T_primo(n):
            malos.append(n)
    comprobar("D1 169 numeros (0 al 168)", malos, [])
    malos = [n for n in range(2, 169) if T_primo(n) == "compuesto" and n % 2 and n % 3 and n % 5
             and motor.decidir_primo(n, SABER).get("pieza") != "primo_buscando_parejas"]
    comprobar("D2 los compuestos sin regla corta (49, 77, 91, 119 ...) los encuentra buscando parejas", malos, [])
    malos = [n for n in range(4, 169) if T_primo(n) == "compuesto" and (n % 2 == 0 or n % 5 == 0 or n % 3 == 0)
             and motor.decidir_primo(n, SABER).get("pieza") != "compuesto_por_una_regla_corta"]
    comprobar("D3 los que tienen 2, 3 o 5 de factor los dice la regla corta", malos, [])
    comprobar("D4 escrito de otras formas: es primo 37 / 37 es primo / el 2 es primo",
              (S("es primo 37"), S("37 es primo"), S("el 2 es primo")), ("primo", "primo", "primo"))

    print("\nE - LA CRIBA")
    for n in (2, 10, 30, 50, 100):
        comprobar("E primos hasta %d" % n, S("primos hasta %d" % n), L([k for k in range(2, n + 1) if T_primo(k) == "primo"]))
    comprobar("E primos hasta 1 -> ninguno", S("primos hasta 1"), "ninguno")
    comprobar("E primos hasta 101 -> todavia no (la criba de 5.o llega a 100)", S("primos hasta 101"), "todavia_no")
    salida = motor.explicar_pregunta("primos hasta 100", SABER)
    comprobar("E la criba para en el 11 (11 x 11 = 121) y se comprueba por otro camino",
              ("11 x 11 = 121 ya se pasa de 100" in salida, "todos tienen solo la pareja 1 x n ... SI" in salida), (True, True))

    print("\nF - LOS MULTIPLOS")
    malos = []
    for d in range(1, 13):
        if S("multiplos de %d" % d) != L([d * k for k in range(1, 13)]):
            malos.append(d)
        if S("multiplos de %d hasta 100" % d) != L([d * k for k in range(1, 101) if d * k <= 100]):
            malos.append(("hasta", d))
    comprobar("F1 los multiplos de 1 a 12 (los doce primeros y hasta 100)", malos, [])
    comprobar("F2 multiplos de 0 -> 0", S("multiplos de 0"), "0")
    comprobar("F3 multiplos de 37 hasta 20 -> ninguno", S("multiplos de 37 hasta 20"), "ninguno")
    comprobar("F4 multiplos de 1 hasta 500 -> todavia no (mas de cien, no uno a uno)", S("multiplos de 1 hasta 500"), "todavia_no")
    t1 = time.time()
    r = S("multiplos de 250000")
    comprobar("F5 multiplos de 250000: hasta el millon, y rapido (%.2f s)" % (time.time() - t1),
              (r, time.time() - t1 < 2), ("250000, 500000, 750000, 1000000", True))
    comprobar("F6 multiplos de 13: un salto grande es una SUMA", S("multiplos de 13"), L([13 * k for k in range(1, 13)]))

    print("\nG - ES MULTIPLO / ES FACTOR (1 al 100 y numeros de una cifra), y del reves")
    azar = random.Random(20261007)
    malos = []
    for n in sorted(set(azar.sample(range(1, 101), 40)) | {1, 9, 10, 99, 100}):
        for d in range(1, 10):
            esperado = "si" if n % d == 0 else "no"
            if S("%d es multiplo de %d" % (n, d)) != esperado:
                malos.append((n, "multiplo", d))
            if S("%d es factor de %d" % (d, n)) != esperado:
                malos.append((d, "factor", n))
            if d < n and S("%d es multiplo de %d" % (d, n)) != "no":
                malos.append((d, "multiplo al reves", n))
    comprobar("G1 450 preguntas de multiplo y de factor (y 'el pequeno multiplo del grande': no)", malos, [])
    comprobar("G2 0 es multiplo de 7 -> si (7 x 0)", S("0 es multiplo de 7"), "si")
    comprobar("G3 0 es factor de 7 -> no", S("0 es factor de 7"), "no")
    comprobar("G4 es 91 multiplo de 7? escrito con su ?", S("es 91 multiplo de 7?"), "si")

    print("\nH - COMUNES Y PRIMOS")
    malos = []
    for a, b in [(azar.randint(1, 168), azar.randint(1, 168)) for _ in range(30)] + [(24, 36), (12, 18), (1, 100)]:
        esperado = L([x for x in T_factores(a) if x in T_factores(b)])
        if S("factores comunes: %d y %d" % (a, b)) != esperado:
            malos.append((a, b))
    comprobar("H1 33 parejas: factores comunes", malos, [])
    malos = []
    for a in range(1, 13):
        for b in range(1, 13):
            g, p = max(a, b), min(a, b)
            esperado = L([g * k for k in range(1, 13) if (g * k) % p == 0])
            if S("multiplos comunes: %d y %d" % (a, b)) != esperado:
                malos.append((a, b))
    comprobar("H2 los 144 multiplos comunes de 1 a 12", malos, [])
    malos = []
    for n in range(1, 169, 3):
        esperado = L([x for x in T_factores(n) if T_primo(x) == "primo"]) or "ninguno"
        if S("factores primos: %d" % n) != esperado:
            malos.append(n)
    comprobar("H3 56 numeros: factores primos", malos, [])

    print("\nI - LAS PAREJAS DE 100 (punto 6), con las tablas aprendidas")
    motor.aprender("tablas", SABER)
    malos, no = [], []
    for f, p in ((25, 4), (50, 2), (20, 5)):
        for g in range(13, 400, 7):
            r = S("con 100: %d x %d" % (f, g))
            if g % p == 0:
                if r != str(f * g):
                    malos.append((f, g, r))
            elif r != "no_encaja":
                no.append((f, g, r))
    comprobar("I1 las que encajan dan el producto del testigo", malos, [])
    comprobar("I2 las que no encajan (36 no se parte en grupos de ...) lo dicen", no, [])
    comprobar("I3 con 100: 7 x 8 -> no encaja", S("con 100: 7 x 8"), "no_encaja")

    print("\nJ - NUMEROS GRANDES, CERCA DEL TECHO, y el TIEMPO (con las tablas aprendidas)")
    for texto, esperado in (("primo: 1000000", "compuesto"), ("primo: 999999", "compuesto"),
                            ("primo: 999995", "compuesto"), ("primo: 999998", "compuesto"),
                            ("primo: 1000001", "todavia_no"), ("primo: 999997", "todavia_no"),
                            ("primo: 1001", "todavia_no"), ("primo: 155", "compuesto"),
                            ("factores: 144", L(T_factores(144))), ("factores: 167", "1, 167"),
                            ("7 es factor de 1000000", "no"), ("1000000 es multiplo de 8", "si"),
                            ("multiplos de 83333", L([83333 * k for k in range(1, 13)]))):
        t1 = time.time()
        r = S(texto)
        dt = time.time() - t1
        comprobar("J %s -> %s (%.2f s)" % (texto, esperado, dt), (r, dt < 2), (esperado, True))
    azar = random.Random(7)
    malos, nunca_primo = [], []
    for n in azar.sample(range(169, 1000000), 60):
        r = motor.decidir_primo(n, SABER)
        if r["conclusion"] == "hecho" and r["valor"] != T_primo(n):
            malos.append(n)
        if (n % 2 == 0 or n % 5 == 0 or n % 3 == 0) and r.get("valor") != "compuesto":
            nunca_primo.append(n)
    comprobar("J 60 numeros grandes al azar: nunca dice algo falso", malos, [])
    comprobar("J ... y los que tienen 2, 3 o 5 de factor los dice compuestos", nunca_primo, [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\nTOTAL: %d/%d" % (BIEN, BIEN + MAL))
