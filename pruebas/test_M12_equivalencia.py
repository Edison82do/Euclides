# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.12: USAR LA EQUIVALENCIA PARA CALCULAR (NCETM 2.18).
El plan y sus trampas: diario/2026-10-07-paso-M12-equivalencia.md
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
TMP = tempfile.mkdtemp(prefix="m12_")
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


def P(pid, **sit):
    """(valor, id de la pieza) de una pregunta o de una pieza por su nombre."""
    r = motor.aplicar(pid, sit, SABER)
    return (r.get("valor"), r["pieza"]["id"]) if r["conclusion"] == "hecho" else (r["conclusion"], None)


print("=" * 78)
print("PASO M.12 - USAR LA EQUIVALENCIA PARA CALCULAR  (%s)" % modo())
print("=" * 78)
try:
    motor.aprender("tablas", SABER)

    print("\nA - LAS TRAMPAS DEL PLAN")
    comprobar("A1 25 x 16 -> 400, doblando y partiendo por la mitad",
              P("multiplicar", a=25, b=16), (400, "multiplicar_escalando"))
    comprobar("A2 equivalente: 25 x 16 -> 400", S("equivalente: 25 x 16"), "400")
    comprobar("A3 equivalente: 25 x 15 -> no encaja (15 es impar)", S("equivalente: 25 x 15"), "no_encaja")
    comprobar("A4 ... pero 25 x 15 se hace de otra manera: 375", S("25 x 15"), "375")
    comprobar("A5 165 : 5 -> 33 doblando los dos", P("dividir", total=165, divisor=5), (33, "dividir_escalando"))
    comprobar("A6 equivalente: 180 : 20 -> 9 (un cero menos a los dos)", S("equivalente: 180 : 20"), "9")
    comprobar("A7 equivalente: 375 : 25 -> 15", S("equivalente: 375 : 25"), "15")
    comprobar("A8 17 : 5 -> 3 resto 2 (no 'resto 4', el de 34 : 10)", S("17 : 5"), "3 resto 2")
    comprobar("A9 170 : 15 no es justa: la equivalencia no se usa (el resto cambiaria)",
              P("dividir_escalando", total=170, divisor=15)[0], "no_salio")
    comprobar("A10 ... y 170 : 15 da 11 resto 5", S("170 : 15"), "11 resto 5")
    comprobar("A11 verdad: 3 x 12 = 6 x 6 -> VERDADERO sin calcular",
              (S("verdad: 3 x 12 = 6 x 6"), P("igualdad", lados=motor.leer_igualdad("3 x 12 = 6 x 6"))[1]),
              ("verdadero", "igual_escalando"))
    comprobar("A12 verdad: 3 x 12 = 4 x 11 -> FALSO (la compensacion de la suma no vale)",
              S("verdad: 3 x 12 = 4 x 11"), "falso")
    comprobar("A13 verdad: 96 : 4 = 48 : 2 -> VERDADERO sin calcular",
              (S("verdad: 96 : 4 = 48 : 2"), P("igualdad", lados=motor.leer_igualdad("96 : 4 = 48 : 2"))[1]),
              ("verdadero", "igual_escalando"))
    comprobar("A14 verdad: 96 : 4 = 192 : 2 -> FALSO (en : los dos cambian IGUAL)",
              S("verdad: 96 : 4 = 192 : 2"), "falso")
    comprobar("A15 24 x 5 = 12 x ? -> 10 (no 3 ni 17)", S("24 x 5 = 12 x ?"), "10")
    comprobar("A16 180 : 20 = 18 : ? -> 2 (no 200)", S("180 : 20 = 18 : ?"), "2")
    comprobar("A17 ? : 5 = 330 : 10 -> 165", S("? : 5 = 330 : 10"), "165")
    comprobar("A18 las tablas siguen con la tabla: 5 x 8 no se escala",
              P("multiplicar", a=5, b=8)[1] != "multiplicar_escalando", True)
    comprobar("A19 125 x 24 -> 3000 (250 x 12, 500 x 6, 1000 x 3)", P("multiplicar", a=125, b=24),
              (3000, "multiplicar_escalando"))

    print("\nB - DOMINIO: multiplicar doblando y partiendo (f acaba en 5, g par), contra el testigo")
    malos, salen, total = [], 0, 0
    for f in range(5, 200, 10):
        for g in range(2, 42, 4):
            total += 1
            v, pid = P("multiplicar_escalando", a=f, b=g)
            if pid:
                salen += 1
                if v != f * g:
                    malos.append((f, g, v))
            w = P("multiplicar", a=f, b=g)[0]
            if w != f * g:
                malos.append(("todo", f, g, w))
    print("        %d productos; %d salen por la equivalencia" % (total, salen))
    comprobar("B1 ningun producto mal (%d)" % total, malos, [])
    comprobar("B2 la mayoria sale por la equivalencia", salen > total // 2, True)

    print("\nC - DOMINIO: dividir cambiando los dos, contra el testigo")
    malos, salen, total = [], 0, 0
    for d in (5, 15, 25, 35, 45, 50, 75, 125, 250, 20, 30, 40, 60, 80, 200, 300, 400):
        for q in list(range(1, 41, 3)) + [55, 99]:
            for resto in (0, 1):
                t = q * d + (resto and d - 1)
                total += 1
                v, pid = P("dividir_escalando", total=t, divisor=d)
                if pid:
                    salen += 1
                    if (v, resto) != (t // d, 0):
                        malos.append((t, d, v))
                w = S("%d : %d" % (t, d))
                esperado = str(t // d) if t % d == 0 else "%d resto %d" % (t // d, t % d)
                if w != esperado:
                    malos.append(("todo", t, d, w))
    print("        %d divisiones; %d salen por la equivalencia (solo justas)" % (total, salen))
    comprobar("C1 ninguna division mal (%d)" % total, malos, [])
    # Arreglo del 7 oct (revision): con divisor de mas de doce, mas de cien saltos es la division
    # LARGA (6.o, NCETM 2.24): todavia no.  Antes se contaba de uno en uno y tardaba minutos.
    comprobar("C1b 1814 : 15 (120 saltos y resto) -> todavia no (division larga, 6.o)", S("1814 : 15"), "no_se_puede")
    comprobar("C2 por la equivalencia solo salen las justas, y casi todas", salen > total // 3, True)

    print("\nD - DOMINIO: igualdades equivalentes (verdaderas sin calcular) y sus trampas")
    rnd = random.Random(1218)
    malos, n = [], 0
    for a in range(2, 13):
        for b in range(2, 25):
            for k in (2, 3, 4, 5, 10):
                if b % k:
                    continue
                n += 1
                t = "%d x %d = %d x %d" % (a, b, a * k, b // k)
                pid = P("igualdad", lados=motor.leer_igualdad(t))[1]
                if S("verdad: " + t) != "verdadero" or pid not in ("igual_escalando", "igual_dando_la_vuelta"):
                    malos.append(t)                                  # (3 x 6 = 6 x 3 es dar la vuelta)
                t = "%d x %d = %d x %d" % (a, b, a + 1, b - 1)        # la compensacion de la suma
                if S("verdad: " + t) != ("verdadero" if a * b == (a + 1) * (b - 1) else "falso"):
                    malos.append(t)
    for _ in range(100):
        d, q, k = rnd.randint(2, 12), rnd.randint(1, 30), rnd.choice((2, 3, 5, 10))
        n += 1
        t = "%d : %d = %d : %d" % (q * d * k, d * k, q * d, d)
        if (S("verdad: " + t), P("igualdad", lados=motor.leer_igualdad(t))[1]) != ("verdadero", "igual_escalando"):
            malos.append(t)
        if d % k == 0:
            t = "%d : %d = %d : %d" % (q * d, d, q * d * k, d // k)  # cambiar al reves: la trampa
            if S("verdad: " + t) != "falso":
                malos.append(t)
    print("        %d igualdades" % n)
    comprobar("D1 todas bien (%d)" % n, malos, [])

    print("\nE - DOMINIO: el hueco en a x b = c x ? y en a : b = c : ?, contra el testigo")
    malos, n, sin_calcular = [], 0, 0
    for _ in range(100):
        a, b, k = rnd.randint(2, 30), rnd.randint(1, 12), rnd.choice((2, 3, 4, 5, 10))
        if rnd.random() < 0.5:
            t, v = "%d x %d = %d x ?" % (a * k, b, a), b * k
        else:
            t, v = "%d x %d = %d x ?" % (a, b * k, a * k), b
        n += 1
        if S(t) != str(v):
            malos.append(t)
        sin_calcular += bool(motor.decidir_ecuacion_letra(t, SABER).get("equivalencia"))
        q, d = rnd.randint(1, 30), rnd.randint(2, 12)
        t, v = "%d : %d = %d : ?" % (q * d * k, d * k, q * d), d
        n += 1
        if S(t) != str(v):
            malos.append(t)
        sin_calcular += bool(motor.decidir_ecuacion_letra(t, SABER).get("equivalencia"))
    print("        %d huecos; %d sin calcular los lados" % (n, sin_calcular))
    comprobar("E1 todos los huecos bien (%d)" % n, malos, [])
    comprobar("E2 todos sin calcular los lados", sin_calcular, n)
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
print("=" * 78)
sys.exit(1 if MAL else 0)
