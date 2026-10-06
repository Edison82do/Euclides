# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO E.6: ES RAZONABLE?  ESTIMAR REDONDEANDO (Common Core 3.OA.D.8).
El plan y sus trampas: diario/2026-10-06-paso-E6-razonable.md
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
TMP = tempfile.mkdtemp(prefix="e6_")
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


def Z(a, op, b, resp):
    r = motor.decidir_razonable(a, op, b, resp, SABER)
    return r.get("valor") if r["conclusion"] == "hecho" else r["conclusion"]


# --- el TESTIGO externo (Python)
def red(n):
    m = 100 if n >= 100 else 10
    return (n + m // 2) // m * m


def mov(n):
    return 50 if n >= 100 else 5


def banda_testigo(a, op, b):
    if op == "x":
        p, g = (a, b) if a < 10 else (b, a)
        est, ban = p * red(g), p * mov(g)
    else:
        est = red(a) + red(b) if op == "+" else red(a) - red(b)
        ban = mov(a) + mov(b)
    return max(est - ban, 0), min(est + ban, 1000), est


def de_verdad(a, op, b):
    return {"+": a + b, "-": a - b, "x": a * b}[op]


def sin_llevada(a, b):
    """El error tipico: sumar columna a columna sin llevar (38 + 47 -> 75)."""
    out, m = 0, 1
    while a or b:
        out += ((a % 10 + b % 10) % 10) * m
        a, b, m = a // 10, b // 10, m * 10
    return out


print("=" * 78)
print("PASO E.6 - ES RAZONABLE? ESTIMAR REDONDEANDO  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRAMPAS DEL PLAN (3.OA.D.8)")
    comprobar("A1 estimar 38 + 47 -> cerca de 90 (40 + 50)", S("estimar: 38 + 47"), "cerca de 90")
    comprobar("A2 38 + 47 = 75 -> NO (la llevada olvidada)", Z(38, "+", 47, 75), "no")
    comprobar("A3 38 + 47 = 85 -> SI, y es la buena", Z(38, "+", 47, 85), "si")
    comprobar("A4 38 + 47 = 95 -> razonable pero MAL (lo dice)", Z(38, "+", 47, 95), "si, pero mal: es 85")
    comprobar("A5 38 + 47 = 815 -> NO (cifras fuera de sitio)", Z(38, "+", 47, 815), "no")
    comprobar("A6 92 - 38 = 64 -> NO (banda 40 a 60)", Z(92, "-", 38, 64), "no")
    comprobar("A7 3 x 47 = 141 -> SI (3 x 50 = 150, banda 15)", Z(3, "x", 47, 141), "si")
    comprobar("A8 3 x 47 = 1210 y = 121 -> NO", (Z(3, "x", 47, 1210), Z(3, "x", 47, 121)), ("no", "no"))
    comprobar("A9 estimar 247 + 385 -> cerca de 600 (centenas)", S("estimar: 247 + 385"), "cerca de 600")
    comprobar("A10 dividir y dos factores grandes -> todavia_no",
              (S("estimar: 12 : 3"), S("estimar: 23 x 47")), ("todavia_no", "todavia_no"))
    comprobar("A11 2 x 3 -> no hace falta estimar (es de la tabla)", S("razonable: 2 x 3 = 6"), "no_hace_falta")
    comprobar("A12 30 - 52 -> imposible", S("razonable: 30 - 52 = 4"), "imposible")
    comprobar("A13 'estimar: hola' -> no_entiendo", S("estimar: hola"), "no_entiendo")
    t = motor.explicar_pregunta("razonable: 38 + 47 = 95", SABER)
    comprobar("A14 la explicacion: razonable no es lo mismo que correcta",
              ("razonable no es lo mismo que correcta" in t, "errores grandes" in t), (True, True))

    print("\nB - MUESTRA: LA BANDA CONTRA EL TESTIGO; LA BUENA NUNCA SE RECHAZA")
    rnd = random.Random(66)
    cuentas = []
    while len(cuentas) < 90:
        a, b = rnd.randint(10, 600), rnd.randint(10, 400)
        if a + b <= 900:
            cuentas.append((a, "+", b))
    while len(cuentas) < 150:
        a, b = rnd.randint(10, 999), rnd.randint(10, 600)
        if a >= b:
            cuentas.append((a, "-", b))
    while len(cuentas) < 190:
        cuentas.append((rnd.randint(2, 9), "x", rnd.randint(11, 99)))
    malos_banda, buenas_rechazadas, hechas = [], [], 0
    for a, op, b in cuentas:
        r = motor.decidir_estimar(a, op, b, SABER)
        if r["conclusion"] != "hecho":
            continue
        hechas += 1
        if (r["desde"], r["hasta"], r["estimacion"]) != banda_testigo(a, op, b):
            malos_banda.append((a, op, b, r["desde"], r["hasta"], banda_testigo(a, op, b)))
        if Z(a, op, b, de_verdad(a, op, b)) != "si":
            buenas_rechazadas.append((a, op, b))
    comprobar("B1 %d cuentas: la estimacion y la banda, igual que el testigo" % hechas, malos_banda[:3], [])
    comprobar("B2 la respuesta buena SIEMPRE es razonable (la banda no miente)", buenas_rechazadas[:3], [])
    comprobar("B3 casi todas se pudieron estimar (las demas: se sale de mil)", hechas >= 180, True)

    print("\nC - LAS RESPUESTAS MALAS TIPICAS")
    raros, cazadas, vistas = [], 0, 0
    for a, op, b in cuentas:
        verdad = de_verdad(a, op, b)
        malas = [verdad + 10, verdad + 100, verdad * 10]
        if verdad >= 100:
            malas.append(verdad - 100)
        if op == "+":
            malas.append(sin_llevada(a, b))
        for m in malas:
            if m == verdad:
                continue
            desde, hasta, _ = banda_testigo(a, op, b)
            esperado = "si, pero mal: es %d" % verdad if desde <= m <= hasta and m <= 1000 else "no"
            obtenido = Z(a, op, b, m)
            if obtenido in ("todavia_no",):
                continue
            vistas += 1
            if obtenido == "no":
                cazadas += 1
            if obtenido != esperado:
                raros.append((a, op, b, m, obtenido, esperado))
    comprobar("C1 %d respuestas malas: cazadas fuera de la banda, 'razonable pero mal' dentro" % vistas,
              raros[:3], [])
    comprobar("C2 la estimacion caza de verdad (%d de %d fuera de la banda; ninguna mala dio 'si' en C1)" % (cazadas, vistas), cazadas > 0, True)
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("-" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
