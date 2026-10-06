# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO D.3: EL DINERO, PESOS Y CENTAVOS (NCETM 1.25; 4.MD.A.2).
El plan y sus trampas: diario/2026-10-07-paso-D3-dinero.md
Python solo aparece aqui como TESTIGO externo (en centavos enteros).
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
TMP = tempfile.mkdtemp(prefix="d3_")
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


def P(c):
    return "$%d.%02d" % divmod(c, 100)


print("=" * 78)
print("PASO D.3 - EL DINERO  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRAMPAS DEL PLAN")
    comprobar("A1 dinero: $3.45 -> 345 centavos", S("dinero: $3.45"), "345 centavos")
    comprobar("A2 $2.99 + $1.50 -> $4.49 (y compensando)", S("$2.99 + $1.50"), "$4.49")
    t = motor.explicar_pregunta("$2.99 + $1.50", SABER)
    comprobar("A3 ... compensando: $3.00 + $1.50 - 1 centavo", "le quito ese centavo: $4.49 ... lo mismo" in t, True)
    comprobar("A4 $3.45 + $6.80 -> $10.25", S("$3.45 + $6.80"), "$10.25")
    comprobar("A5 cambio de $10 por $6.35 -> $3.65 (contando hacia adelante)", S("cambio: pago $10 por $6.35"), "$3.65")
    comprobar("A6 cambio de $5 por $5 -> $0.00;  de $5 por $6.35 -> no alcanza",
              (S("cambio: pago $5 por $5"), S("cambio: pago $5 por $6.35")), ("$0.00", "no_alcanza"))
    comprobar("A7 varias cosas: $20 por $3.45 + $6.80 + $2.15 -> $7.60", S("cambio: pago $20 por $3.45 + $6.80 + $2.15"), "$7.60")
    comprobar("A8 $3.456 no es un precio", S("dinero: $3.456"), "no_entiendo")

    print("\nB - SUMAS Y RESTAS DE PRECIOS (muestra) CONTRA EL TESTIGO")
    rnd = random.Random(125)
    malos = []
    for _ in range(200):
        a, b = rnd.randint(0, 4999), rnd.randint(0, 4999)
        op = rnd.choice("+-")
        v = a + b if op == "+" else a - b
        r = S("%s %s %s" % (P(a), op, P(b)))
        esperado = P(v) if v >= 0 else "imposible"
        if r != esperado:
            malos.append((P(a), op, P(b), r, esperado))
    comprobar("B1 200 cuentas de precios", malos[:3], [])

    print("\nC - EL CAMBIO (muestra), CONTANDO HACIA ADELANTE, CON SU COMPROBACION")
    malos = []
    for _ in range(200):
        billete = rnd.choice((1, 5, 10, 20, 50))
        n = rnd.randint(1, 3)
        precios = [rnd.randint(1, billete * 100 // n) for _ in range(n)]
        total = sum(precios)
        r = motor.decidir_cambio(str(billete), [P(x)[1:] for x in precios], SABER)
        if total > billete * 100:
            if r["conclusion"] != "no_alcanza":
                malos.append((billete, precios, r["conclusion"]))
        elif r.get("valor") != P(billete * 100 - total) or not r.get("vuelta_ok"):
            malos.append((billete, precios, r.get("valor"), P(billete * 100 - total)))
    comprobar("C1 200 cambios", malos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("-" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
