# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO S.3: PROBLEMAS CON DOS INCOGNITAS (NCETM 1.31; Year 6).
El plan y sus trampas: diario/2026-10-08-paso-S3-dos-incognitas.md
Python solo aparece aqui como TESTIGO externo.
"""
import importlib.util
import os
import random
import shutil
import sys
import tempfile
import time
from decimal import Decimal
from fractions import Fraction

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)
TMP = tempfile.mkdtemp(prefix="s3_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria propia: solo las tablas
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


def D(t):
    return motor.decidir_dos_incognitas(t, SABER)


def txt(x):
    """El testigo escribe un numero como lo escribe Euclides: sin ceros de sobra."""
    x = Decimal(str(x)) if not isinstance(x, Decimal) else x
    t = format(x.normalize(), "f")
    return t


def sol(a, b):
    return "a = %s, b = %s" % (txt(a), txt(b))


print("=" * 78)
print("PASO S.3 - PROBLEMAS CON DOS INCOGNITAS  (%s)" % modo())
print("=" * 78)
try:
    motor.aprender("tablas", SABER)          # en 6.o las tablas ya se saben (repartir con la division corta las pide)

    print("\nA - LAS TRAMPAS DEL PLAN")
    comprobar("A1 a + b = 30; a - b = 8 -> a = 19, b = 11", S("a + b = 30; a - b = 8"), "a = 19, b = 11")
    t = motor.explicar_pregunta("a + b = 30; a - b = 8", SABER)
    comprobar("A2 ... dice el error: NO es 30 : 2 = 15 y 15 + 8 = 23 (juntan 38)",
              "NO es 30 : 2 = 15 y 15 + 8 = 23: asi juntan 38" in t, True)
    comprobar("A3 ... dibuja la barra y dice que hay UNA sola (punto 4)",
              ("LA BARRA" in t, "UNA sola" in t), (True, True))
    comprobar("A4 ... la otra estrategia (anadir la diferencia) da lo mismo",
              "suma_y_diferencia_anadiendo_la_diferencia): sale a = 19, b = 11 ... LO MISMO" in t, True)
    comprobar("A5 a + b = 24; a = 3 x b -> a = 18, b = 6", S("a + b = 24; a = 3 x b"), "a = 18, b = 6")
    t = motor.explicar_pregunta("a + b = 24; a = 3 x b", SABER)
    comprobar("A6 ... 4 trozos iguales, y NO 24 : 3 = 8", ("CUATRO trozos IGUALES" in t, "NO es 24 : 3 = 8" in t),
              (True, True))
    comprobar("A7 a - b = 20; a = 3 x b -> a = 30, b = 10", S("a - b = 20; a = 3 x b"), "a = 30, b = 10")
    comprobar("A8 ... 2 trozos de mas, y NO 20 : 3",
              ("DOS trozos DE MAS" in motor.explicar_pregunta("a - b = 20; a = 3 x b", SABER),), (True,))
    comprobar("A9 a + b = 10; a - b = 12 -> ninguna", S("a + b = 10; a - b = 12"), "ninguna")
    comprobar("A10 a + b = 9; a - b = 4 -> a = 6.5, b = 2.5", S("a + b = 9; a - b = 4"), "a = 6.5, b = 2.5")
    comprobar("A11 ... y dice que con enteros no habria ninguna",
              "con enteros no habria NINGUNA" in motor.explicar_pregunta("a + b = 9; a - b = 4", SABER), True)
    comprobar("A12 a + b = 10 -> 11 parejas (9 sin el 0); infinitas con decimales", S("a + b = 10"),
              "11 parejas con enteros (9 sin el 0); infinitas con decimales")
    comprobar("A13 a - b = 3 -> infinitas", S("a - b = 3"), "infinitas")
    comprobar("A14 a = 3 x b -> infinitas", S("a = 3 x b"), "infinitas")
    comprobar("A15 a x b = 24; a + b = 10 -> 4 y 6, y 6 y 4", S("a x b = 24; a + b = 10"),
              "a = 4, b = 6; a = 6, b = 4")
    comprobar("A16 a + b = 10; 2 x a + 5 x b = 32 -> a = 6, b = 4", S("a + b = 10; 2 x a + 5 x b = 32"), "a = 6, b = 4")
    comprobar("A17 2 x a + 3 x b = 20 -> cuatro soluciones", S("2 x a + 3 x b = 20"),
              "a = 10, b = 0; a = 7, b = 2; a = 4, b = 4; a = 1, b = 6")
    comprobar("A18 b - a = 8 (la grande es b)", S("b - a = 8; a + b = 30"), "a = 11, b = 19")
    comprobar("A19 x + y = 30; x = y + 8", S("x + y = 30; x = y + 8"), "x = 19, y = 11")
    comprobar("A20 24 = a + b (el numero a la izquierda)", S("24 = a + b; a = 3 x b"), "a = 18, b = 6")
    comprobar("A21 a = b - 8 (b tiene 8 mas)", S("a + b = 30; a = b - 8"), "a = 11, b = 19")
    comprobar("A22 dinero: a + b = 1.20; a - b = 0.40", S("a + b = 1.20; a - b = 0.40"), "a = 0.8, b = 0.4")
    comprobar("A23 tres decimales: a + b = 1.235; a - b = 0.115", S("a + b = 1.235; a - b = 0.115"), "a = 0.675, b = 0.56")
    # (U.2, arreglo de la revision de U.1: cuando S.3 dice "todavia no" a una ecuacion que el lector simbolico lee,
    #  el resolvedor universal tiene su oportunidad: A24, A29, F3, F4 y F8 los resuelve el, y lo comprueba)
    comprobar("A24 a + b = 1.001; a - b = 0 -> el resolvedor (S.3: diezmilesimas)", S("a + b = 1.001; a - b = 0"),
              "a = 1001/2000, b = 1001/2000")
    comprobar("A25 cerca del techo: a + b = 9999999; a - b = 1", S("a + b = 9999999; a - b = 1"),
              "a = 5000000, b = 4999999")
    comprobar("A26 cerca del techo: a + b = 10000000; a = 4 x b", S("a + b = 10000000; a = 4 x b"),
              "a = 8000000, b = 2000000")
    comprobar("A27 a + b = 10000001 -> no alcanza", S("a + b = 10000001; a - b = 1"), "no_alcanza")
    comprobar("A28 a + b = 100; a x b = 2400 -> todavia no (ni 101 pruebas ni dividir entre 13 o mas)",
              S("a + b = 100; a x b = 2400"), "todavia_no")
    comprobar("A29 a + b = 500; 2 x a + 5 x b = 1600 -> S.3 no (demasiadas pruebas); el resolvedor junta",
              S("a + b = 500; 2 x a + 5 x b = 1600"), "a = 300, b = 200")
    comprobar("A30 ... y dice que la puerta vieja decia todavia no",
              "la puerta vieja decia: TODAVIA NO" in motor.explicar_pregunta("a + b = 500; 2 x a + 5 x b = 1600", SABER),
              True)

    print("\nB - SUMA Y DIFERENCIA (punto 4), contra el testigo")
    azar = random.Random(20261008)
    casos = [(s, d) for s in (0, 1, 2, 9, 10, 99, 100, 1000) for d in (0, 1, 2, 9, 10) if d <= s]
    casos += [(azar.randint(0, 9999), 0) for _ in range(10)]
    casos += [(azar.randint(0, 9999999), azar.randint(0, 99999)) for _ in range(60)]
    casos += [(azar.randint(0, 999), azar.randint(0, 999)) for _ in range(40)]
    mal, cuantos, ningunas, aun_no = [], 0, 0, []
    for s_, d_ in casos:
        r = D("a + b = %d; a - b = %d" % (s_, d_))
        if r["conclusion"] in ("todavia_no", "no_alcanza") and (s_ + d_) % 2 and s_ > 999999:
            aun_no.append((s_, d_))            # medio de siete cifras: contado en decimas se pasa del techo
            continue
        if d_ > s_:
            esperado = "ninguna"
            ningunas += 1
        else:
            esperado = sol(Fraction(s_ + d_, 2), Fraction(s_ - d_, 2)) if (s_ + d_) % 2 == 0 else \
                sol(Decimal(s_ + d_) / 2, Decimal(s_ - d_) / 2)
        cuantos += 1
        if r.get("valor") != esperado:
            mal.append((s_, d_, r.get("valor"), esperado))
    comprobar("B1 %d problemas de suma y diferencia (pares, impares, ninguna, grandes): bien o 'todavia no', nunca mal"
              % cuantos, mal[:3], [])
    print("          (%d con un medio de siete cifras no lo dan: en decimas se pasan del techo y no se pueden comprobar)" % len(aun_no))
    comprobar("B1b ... y no lo dan solo con medios de siete cifras (los demas, todos bien)",
              all((s_ + d_) % 2 and s_ > 999999 for s_, d_ in aun_no), True)
    otra = []
    for s_, d_ in casos[:60]:
        sit = D("a + b = %d; a - b = %d" % (s_, d_))["situacion"]
        q = motor.aplicar("suma_y_diferencia_quitando_la_diferencia", sit, SABER)
        n = motor.aplicar("suma_y_diferencia_anadiendo_la_diferencia", sit, SABER)
        if q.get("valor") != n.get("valor"):
            otra.append((s_, d_, q.get("valor"), n.get("valor")))
    comprobar("B2 quitando y anadiendo la diferencia dan siempre lo mismo (60)", otra[:3], [])
    mal = []
    for _ in range(40):
        a, b = sorted([Decimal(azar.randint(0, 99999)) / 1000, Decimal(azar.randint(0, 99999)) / 1000], reverse=True)
        r = D("a + b = %s; a - b = %s" % (txt(a + b), txt(a - b)))
        if r.get("valor") != sol(a, b):
            mal.append((txt(a + b), txt(a - b), r.get("valor"), sol(a, b)))
    comprobar("B3 40 con milesimas (la solucion con tres decimales)", mal[:3], [])

    print("\nC - SUMA Y MULTIPLO; DIFERENCIA Y MULTIPLO (la barra de trozos iguales)")
    mal = []
    for k in range(1, 13):
        for b in (0, 1, 7, 25, azar.randint(0, 99999)):
            r = D("a + b = %d; a = %d x b" % (k * b + b, k))
            if k >= 9 and b > 12 and r["conclusion"] == "todavia_no":
                continue                       # repartir un numero grande entre 10 o mas: la division larga (NCETM 2.24)
            if r.get("valor") != sol(k * b, b):
                mal.append((k, b, r.get("valor")))
    comprobar("C1 suma y multiplo, k de 1 a 12 (60; repartir uno grande entre 10 o mas: bien o todavia no)", mal[:3], [])
    comprobar("C1b a + b = 77; a = 10 x b: 11 trozos, con la tabla del 11", S("a + b = 77; a = 10 x b"), "a = 70, b = 7")
    comprobar("C1c a + b = 567127; a = 10 x b: 11 trozos de un numero grande -> a = 515570, b = 51557 (antes todavia no: "
              "la division larga, hecha en M.18)", S("a + b = 567127; a = 10 x b"), "a = 515570, b = 51557")
    mal = []
    for k in range(2, 13):
        for b in (0, 1, 7, 25, azar.randint(0, 99999)):
            r = D("a - b = %d; a = %d x b" % (k * b - b, k))
            if k >= 11 and b > 12 and r["conclusion"] == "todavia_no":
                continue
            if r.get("valor") != sol(k * b, b):
                mal.append((k, b, r.get("valor")))
    comprobar("C2 diferencia y multiplo, k de 2 a 12 (55; repartir uno grande entre 10 o mas: bien o todavia no)", mal[:3], [])
    comprobar("C3 a + b = 10; a = 3 x b -> con decimas: a = 7.5, b = 2.5", S("a + b = 10; a = 3 x b"), "a = 7.5, b = 2.5")
    comprobar("C4 a - b = 5; a = 1 x b -> ninguna (son la misma barra)", S("a - b = 5; a = 1 x b"), "ninguna")
    comprobar("C5 a - b = 0; a = 1 x b -> infinitas", S("a - b = 0; a = 1 x b"), "infinitas")
    comprobar("C6 el multiplo escrito al reves: b x 3 = a", S("a + b = 24; b x 3 = a"), "a = 18, b = 6")

    print("\nD - PROBAR EN ORDEN (punto 5), contra el testigo que prueba todo")

    def testigo(conds, hasta):
        return [(a, b) for a in range(0, hasta + 1) for b in range(0, hasta + 1) if all(c(a, b) for c in conds)]

    def escribir(lista):
        return "; ".join(sol(a, b) for a, b in lista) if lista else "ninguna"

    mal = []
    for p in (6, 12, 24, 36, 48, 60, 72, 100, 121, 144):
        for sm in (7, 10, 14, 20, 25, 26, 37):
            esp = escribir(testigo([lambda a, b: a * b == p, lambda a, b: a + b == sm], p))
            r = S("a x b = %d; a + b = %d" % (p, sm))
            if r != esp:
                mal.append((p, sm, r, esp))
    comprobar("D1 producto y suma (70)", mal[:3], [])
    mal = []
    for n in range(0, 25):
        for tot in (n, 2 * n + 3, 3 * n + 1, 5 * n - 2):
            if tot < 0:
                continue
            esp = escribir(testigo([lambda a, b: a + b == n, lambda a, b: 2 * a + 5 * b == tot], max(n, 1)))
            r = S("a + b = %d; 2 x a + 5 x b = %d" % (n, tot))
            if r != esp:
                mal.append((n, tot, r, esp))
    comprobar("D2 monedas de 2 y de 5: suma y suma con pesos (100)", mal[:3], [])
    mal = []
    for p, q, n in ((2, 3, 20), (3, 2, 20), (5, 7, 60), (4, 6, 30), (1, 4, 17), (3, 3, 12), (7, 9, 100), (2, 2, 7)):
        esp = escribir(testigo([lambda a, b: p * a + q * b == n], n))
        r = S("%d x a + %d x b = %d" % (p, q, n))
        if sorted(r.split("; ")) != sorted(esp.split("; ")):        # el orden: el de la letra que se prueba
            mal.append((p, q, n, r, esp))
    comprobar("D3 una suma con pesos sola: todas las de enteros (8)", mal[:3], [])
    mal = []
    for p in (1, 6, 7, 16, 24, 36, 100, 144):
        esp = escribir(testigo([lambda a, b: a * b == p], p))
        r = S("a x b = %d" % p)
        if r != esp:
            mal.append((p, r, esp))
    comprobar("D4 un producto solo: las parejas de factores en los dos ordenes (8)", mal[:3], [])
    comprobar("D5 producto y diferencia: a x b = 24; a - b = 2", S("a x b = 24; a - b = 2"), "a = 6, b = 4")
    comprobar("D6 dos sumas distintas: ninguna", S("a + b = 10; a + b = 12"), "ninguna")
    r = D("a + b = 10; 2 x a + 5 x b = 32")
    comprobar("D7 ... cuenta las pruebas otra vez en la vuelta (11 de 11)", "hice 11 y tenia que hacer 11" in r["vuelta"], True)
    comprobar("D8 2 x a + 3 x b = 20 prueba con el que MAS pesa (b, 7 pruebas)",
              "b va de 0 a 6 (7 pruebas)" in motor.explicar_pregunta("2 x a + 3 x b = 20", SABER), True)

    print("\nE - UNA SOLA ECUACION (punto 1: no siempre hay una sola)")
    mal = []
    for n in (1, 2, 3, 9, 10, 11, 99, 100, 5000, 9999999):
        r = S("a + b = %d" % n)
        esp = "%d parejas con enteros (%d sin el 0); infinitas con decimales" % (n + 1, n - 1)
        if r != esp:
            mal.append((n, r, esp))
    comprobar("E1 a + b = n: una pareja mas que n (y dos menos sin el 0)", mal, [])
    comprobar("E2 a + b = 0 -> a = 0, b = 0", S("a + b = 0"), "a = 0, b = 0")
    comprobar("E3 a + b = 4.5 -> infinitas con decimales, con enteros ninguna", S("a + b = 4.5"),
              "infinitas con decimales (con enteros, ninguna)")
    comprobar("E4 a + b = 10000000 (la cuenta se pasa del techo, y lo dice)", S("a + b = 10000000"),
              "una pareja mas que 10000000 con enteros; infinitas con decimales")
    comprobar("E5 x = y + 5 solo -> infinitas", S("x = y + 5"), "infinitas")

    print("\nF - LO QUE NO ES DE ESTE PASO (o no se entiende)")
    comprobar("F1 tres letras: todavia no", S("a + b + c = 10"), "todavia_no")
    comprobar("F2 dos problemas con cuatro letras: todavia no", S("a + b = 3; c + d = 4"), "todavia_no")
    comprobar("F3 tres ecuaciones: S.3 no; el resolvedor: se contradicen", S("a + b = 10; a - b = 2; a = 2 x b"),
              "ninguna")
    comprobar("F4 un peso con decimales: S.3 no; el resolvedor si", S("a + b = 10; a = 2.5 x b"), "a = 50/7, b = 20/7")
    comprobar("F5 'dos incognitas: hola' -> no entiendo", S("dos incognitas: hola"), "no_entiendo")
    comprobar("F6 con la orden delante", S("dos incognitas: a + b = 30; a - b = 8"), "a = 19, b = 11")
    comprobar("F7 una sola letra sigue siendo de E.5: x + 5 = 12", S("x + 5 = 12"), "7")
    comprobar("F8 la misma letra dos veces: E.5 no; el resolvedor cuenta los trozos", S("a + a = 10"), "a = 5")
    comprobar("F9 una forma que no conozco: todavia no y dice las que si",
              "las formas que se" in motor.explicar_pregunta("a x b + a = 10; a - b = 1", SABER), True)

    print("\nG - CADA PIEZA NUEVA SE COMPRUEBA DE VERDAD (si una cuenta sale mal, la vuelta lo caza)")
    base = motor.cargar_piezas()

    def modulo(nombre):
        sp = importlib.util.spec_from_file_location(nombre, os.path.join(RAIZ, "conocimiento", "piezas", nombre + ".py"))
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        return m

    def uno_mas(v):
        return txt(Decimal(v) + 1)

    class Tramposo:
        """Lo que se le da a la pieza, pero una pregunta (la que se nombra) da uno de mas."""

        def __init__(self, real, cual):
            self._real, self._cual = real, cual

        def __getattr__(self, k):
            return getattr(self._real, k)

        def usar(self, nombre, **sit):
            r = self._real.usar(nombre, **sit)
            if nombre == self._cual:
                r = dict(r)
                r["valor"] = uno_mas(r["valor"]) if isinstance(r["valor"], str) else r["valor"] + 1
            return r

    for nombre, texto, cual in (
            ("suma_y_diferencia_quitando_la_diferencia", "a + b = 30; a - b = 8", "dividir"),
            ("suma_y_diferencia_quitando_la_diferencia", "a + b = 30; a - b = 8", "combinar"),
            ("suma_y_diferencia_anadiendo_la_diferencia", "a + b = 30; a - b = 8", "dividir"),
            ("suma_y_diferencia_anadiendo_la_diferencia", "a + b = 30; a - b = 8", "combinar"),
            ("suma_y_multiplo_con_la_barra", "a + b = 24; a = 3 x b", "dividir"),
            ("suma_y_multiplo_con_la_barra", "a + b = 24; a = 3 x b", "combinar"),
            ("diferencia_y_multiplo_con_la_barra", "a - b = 20; a = 3 x b", "dividir"),
            ("diferencia_y_multiplo_con_la_barra", "a - b = 20; a = 3 x b", "combinar"),
            ("probar_en_orden", "a + b = 10; 2 x a + 5 x b = 32", "combinar"),
            ("probar_en_orden", "2 x a + 3 x b = 20", "dividir"),
            ("una_suma_sola_todas_las_parejas", "a + b = 10", "dividir"),
            ("suma_y_diferencia_quitando_la_diferencia", "a + b = 9; a - b = 4", "dividir_decimal"),
            ("suma_y_multiplo_con_la_barra", "a + b = 10; a = 3 x b", "dividir_decimal"),
            ("sin_tope_infinitas", "a - b = 3", "combinar")):
        sit = D(texto)["situacion"]
        pieza = base["piezas"][nombre]
        m = modulo(nombre)
        u = motor._Lo_que_puede_usar(pieza, base, SABER)
        bien = m.hacer(sit, u)
        comprobar("G %s (%s) = %s y su vuelta cuadra" % (nombre, texto, bien["valor"]),
                  (bien["vuelta_ok"], bool(bien["vuelta"])), (True, True))
        try:
            mal = m.hacer(sit, Tramposo(u, cual))
            cazado = mal["vuelta_ok"] is False
        except (ValueError, motor.NoSalio):
            cazado = True
        comprobar("G %s: con '%s' dando uno de mas, la vuelta NO cuadra" % (nombre, cual), cazado, True)
    p = base["piezas"]["poner_los_numeros_en_las_ecuaciones"]
    sit = D("a + b = 30; a - b = 8")["situacion"]
    r1 = motor.aplicar("cumplen_las_ecuaciones", dict(sit, valores={"a": "19", "b": "11"}), SABER)
    r2 = motor.aplicar("cumplen_las_ecuaciones", dict(sit, valores={"a": "20", "b": "10"}), SABER)
    comprobar("G la comprobacion dice SI a 19 y 11 y NO a 20 y 10 (suman 30, pero no se llevan 8)",
              (r1["valor"], r2["valor"]), ("si", "no"))

    print("\nH - LOS CONTEXTOS (los enunciados de R.1: 'entre los dos' y 'mas que')")
    comprobar("H1 Ana y Luis tienen 30 entre los dos; Ana tiene 8 mas -> Luis 11",
              S("Ana y Luis tienen 30 entre los dos. Ana tiene 8 mas que Luis. Cuantas tiene Luis?"), "11")
    comprobar("H2 ... y Ana 19", S("Ana y Luis tienen 30 entre los dos. Ana tiene 8 mas que Luis. Cuantas tiene Ana?"), "19")
    comprobar("H3 con 'menos que': Luis tiene 8 menos que Ana -> Ana 19",
              S("Ana y Luis tienen 30 canicas entre los dos. Luis tiene 8 menos que Ana. Cuantas tiene Ana?"), "19")
    comprobar("H4 9 entre los dos y 4 mas -> sin solucion (saldria 6.5 canicas)",
              S("Ana y Luis tienen 9 canicas entre los dos. Ana tiene 4 mas que Luis. Cuantas tiene Ana?"), "sin_solucion")
    comprobar("H5 10 entre los dos y 12 mas -> sin solucion",
              S("Ana y Luis tienen 10 entre los dos. Ana tiene 12 mas que Luis. Cuantas tiene Ana?"), "sin_solucion")
    comprobar("H6 lo de antes sigue: dar vueltas sin dato -> no_se_resolver",
              motor.decidir_R1_problema("Ana tiene 3 mas que Luis. Luis tiene 2 menos que Ana. Cuantas tiene Ana?",
                                        SABER)["conclusion"], "no_se_resolver")
    mal = []
    for _ in range(30):
        l = azar.randint(0, 4000)
        d_ = azar.randint(0, 4000)
        r = S("Ana y Luis tienen %d entre los dos. Ana tiene %d mas que Luis. Cuantas tiene Luis?" % (2 * l + d_, d_))
        if r != str(l):
            mal.append((l, d_, r))
    comprobar("H7 30 problemas con palabras contra el testigo", mal[:3], [])

    print("\nI - EL TIEMPO (cada pregunta muy por debajo de 2-3 s)")
    lentas = []
    for q in ("a + b = 9999999; a - b = 1", "a + b = 10000000; a = 4 x b", "a + b = 9999999; a = 2 x b",
              "a - b = 9999990; a = 10 x b", "a + b = 29; 2 x a + 3 x b = 70", "a x b = 144; a + b = 24",
              "a + b = 9999999", "2 x a + 3 x b = 60", "a + b = 25; a - b = 7.5", "a + b = 500; 2 x a + 5 x b = 1600",
              "a + b = 30; a - b = 8"):
        t0 = time.time()
        motor.explicar_pregunta(q, SABER)
        dt = time.time() - t0
        if dt > 2.0:
            lentas.append((q, round(dt, 2)))
    comprobar("I1 11 preguntas grandes (explicadas enteras), ninguna de mas de 2 s", lentas, [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print()
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(0 if MAL == 0 else 1)
