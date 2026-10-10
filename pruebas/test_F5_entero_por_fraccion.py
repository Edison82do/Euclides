# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO F.5: MULTIPLICAR UN ENTERO POR UNA FRACCION (NCETM 3.6; 4.NF.B.4).
El plan y sus trampas: diario/2026-10-07-paso-F5-entero-por-fraccion.md
Python solo aparece aqui como TESTIGO externo.
"""
import os
import random
import shutil
import sys
import tempfile
from fractions import Fraction

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)
TMP = tempfile.mkdtemp(prefix="f5_")
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


def mixto(num, b):
    """el testigo, SIN simplificar (eso es de 5.o): num/b como numero mixto."""
    e, r = divmod(num, b)
    if e == 0:
        return "%d/%d" % (num, b) if num else "0"
    return "%d" % e if r == 0 else "%d %d/%d" % (e, r, b)


print("=" * 78)
print("PASO F.5 - UN ENTERO POR UNA FRACCION  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRAMPAS DEL PLAN")
    comprobar("A1 3 x 2/5 -> 1 1/5 (no 6/15)", S("3 x 2/5"), "1 1/5")
    comprobar("A2 3 x 1 2/5 -> 4 1/5 (no 3 2/5)", S("3 x 1 2/5"), "4 1/5")
    comprobar("A3 12 x 1/4 y 1/4 x 12 -> 3", (S("12 x 1/4"), S("1/4 x 12")), ("3", "3"))
    comprobar("A4 12 x 3/4 -> 9", S("12 x 3/4"), "9")
    comprobar("A5 5 x 1/5 -> 1;  0 x 3/4 -> 0;  4 x 3/4 -> 3", (S("5 x 1/5"), S("0 x 3/4"), S("4 x 3/4")), ("1", "0", "3"))
    # caso viejo (hasta F.8): 2/3 x 3/4 -> todavia_no (fraccion por fraccion era de 6.o).  Desde F.8 (NCETM 3.9) es del ano:
    # lo hace el resolvedor; un mixto por una fraccion sigue 'todavia no'
    comprobar("A6 2/3 x 3/4 -> 1/2 desde F.8 (6.o, NCETM 3.9); 2 1/2 x 1/3 -> todavia no",
              (S("2/3 x 3/4"), S("2 1/2 x 1/3")), ("1/2", "todavia_no"))
    comprobar("A7 3 x 4 sigue siendo de enteros", S("3 x 4"), "12")

    print("\nB - n x a/b Y n x (mixto), CONTRA EL TESTIGO (muestra)")
    rnd = random.Random(36)
    malos = []
    for _ in range(300):
        n, b = rnd.randint(0, 12), rnd.randint(2, 12)
        e, a = rnd.choice((0, 0, 1, 2, 3)), rnd.randint(0, 2 * b)
        if e and a >= b:
            a = a % b
        x = (n, 0, None)
        y = (e, a, b)
        r = motor.decidir_por_fraccion(x, y, SABER)
        v = n * (e + Fraction(a, b))
        if r["conclusion"] != "hecho" or Fraction(*r["valor"]) != v or r.get("de_acuerdo") is False:
            malos.append((n, e, a, b, r.get("valor")))
        elif S("%d x %s" % (n, ("%d %d/%d" % (e, a, b)) if e else "%d/%d" % (a, b))) != mixto(n * (e * b + a), b):
            malos.append(("texto", n, e, a, b, mixto(n * (e * b + a), b)))
    comprobar("B1 300 productos (y su texto como numero mixto)", malos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("-" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
