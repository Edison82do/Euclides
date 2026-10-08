# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.13: MULTIPLICAR Y DIVIDIR DECIMALES POR NUMEROS ENTEROS (NCETM 2.19; 5.NBT.B.7).
El plan y sus trampas: diario/2026-10-07-paso-M13-decimales-por-enteros.md
Python solo aparece aqui como TESTIGO externo (el modulo decimal).
"""
import os
import random
import shutil
import sys
import tempfile
import time
from decimal import Decimal

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)
TMP = tempfile.mkdtemp(prefix="m13_")
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


def P(pregunta, **sit):
    r = motor.aplicar(pregunta, sit, SABER)
    return (r.get("valor"), r["pieza"]["id"]) if r["conclusion"] == "hecho" else (r["conclusion"], None)


def T(d):
    """El testigo: el decimal escrito sin ceros de mas ('1.20' -> '1.2', '6.0' -> '6')."""
    t = format(Decimal(d).normalize(), "f")
    return t


def dec(milesimas, k):
    """Un decimal con k cifras detras del punto, desde un entero (para construir los casos)."""
    s = str(milesimas).rjust(k + 1, "0")
    return "%s.%s" % (s[:-k], s[-k:]) if k else s


print("=" * 78)
print("PASO M.13 - DECIMALES POR Y ENTRE NUMEROS ENTEROS  (%s)" % modo())
print("=" * 78)
try:
    motor.aprender("tablas", SABER)

    print("\nA - LAS TRAMPAS DEL PLAN")
    comprobar("A1 0.3 x 4 -> 1.2 (no 0.12: son 12 DECIMAS)", S("0.3 x 4"), "1.2")
    comprobar("A2 4 x 0.3 -> 1.2 (en cualquier orden)", S("4 x 0.3"), "1.2")
    comprobar("A3 1.5 x 4 -> 6 (no 4.20 ni 6.0)", S("1.5 x 4"), "6")
    comprobar("A4 0.25 x 4 -> 1 (no 1.00)", S("0.25 x 4"), "1")
    comprobar("A5 3.27 x 4 -> 13.08 (327 centesimas x 4)", S("3.27 x 4"), "13.08")
    comprobar("A6 0.12 : 4 -> 0.03 (no 0.3: son 12 CENTESIMAS)", S("0.12 : 4"), "0.03")
    comprobar("A7 0.6 : 2 -> 0.3 (el punto no se pierde)", S("0.6 : 2"), "0.3")
    comprobar("A8 7.2 : 3 -> 2.4", S("7.2 : 3"), "2.4")
    comprobar("A9 1.3 : 4 -> 0.325 (sobra: se cambia a centesimas y a milesimas)", S("1.3 : 4"), "0.325")
    comprobar("A10 35 x 0.1 -> 3.5 (por 0.1 es entre 10)", P("multiplicar_decimal", x="35", y="0.1"),
              ("3.5", "multiplicar_por_una_decima"))
    comprobar("A11 3.5 : 10 -> 0.35 (las cifras bajan un sitio)", P("dividir_decimal", x="3.5", d="10"),
              ("0.35", "dividir_decimal_por_10_o_100"))
    comprobar("A12 0.3 x 0.4 -> todavia no (decimal por decimal, 6.o)", S("0.3 x 0.4"), "todavia_no")
    comprobar("A13 7.2 : 12 -> todavia no (NCETM 2.19: entre una cifra)", S("7.2 : 12"), "todavia_no")
    comprobar("A14 1.5 x 24 -> todavia no (por dos cifras: la multiplicacion larga)", S("1.5 x 24"), "todavia_no")
    comprobar("A15 7.2 : 0 -> no se puede", S("7.2 : 0"), "imposible")
    comprobar("A16 7.2 : 0.3 -> todavia no (entre un decimal)", S("7.2 : 0.3"), "todavia_no")
    comprobar("A17 1 : 3 sin punto sigue siendo la division con resto (M.8)", S("1 : 3"), "0 resto 1")
    comprobar("A18 35 : 10 sin punto sigue siendo 3 resto 5 (M.9)", S("35 : 10"), "3 resto 5")
    comprobar("A19 1.0 : 3 -> todavia no (no sale exacta ni en milesimas)", S("1.0 : 3"), "todavia_no")
    comprobar("A20 0.3 x 0 -> 0", S("0.3 x 0"), "0")
    comprobar("A21 con coma: 2,5 x 3 -> 7.5", S("2,5 x 3"), "7.5")
    comprobar("A22 1.2345 x 2 -> todavia no (diezmilesimas)", S("1.2345 x 2"), "todavia_no")
    comprobar("A23 2.7 + 1.5 sigue siendo 4.2 (D.1)", S("2.7 + 1.5"), "4.2")
    salida = motor.explicar_pregunta("0.3 x 4", SABER)
    comprobar("A24 explica el tamano: por mas de uno sale MAS (punto 4)", "MAYOR que 0.3" in salida, True)
    salida = motor.explicar_pregunta("35 x 0.1", SABER)
    comprobar("A25 ... y por 0.1 sale MENOS", "MENOR que 35" in salida, True)
    salida = motor.explicar_pregunta("3.27 x 4", SABER)
    comprobar("A26 3.27 x 4: otro camino por partes (3 x 4 + 0.27 x 4) que coincide",
              "12 + 1.08 = 13.08 ... COINCIDE" in salida, True)

    print("\nB - CADA PIEZA SE COMPRUEBA CON LA OPERACION CONTRARIA (la vuelta de verdad)")
    for preg, sit, signo in (("multiplicar_decimal", {"x": "0.3", "y": "4"}, ":"),
                             ("multiplicar_decimal", {"x": "35", "y": "0.1"}, "x 10"),
                             ("dividir_decimal", {"x": "7.2", "d": "3"}, " x 3"),
                             ("dividir_decimal", {"x": "3.5", "d": "10"}, "x 10")):
        r = motor.aplicar(preg, sit, SABER)
        comprobar("B %s %s: vuelta '%s'" % (r["pieza"]["id"], sit, r["resultado"]["vuelta"]),
                  signo in r["resultado"]["vuelta"] and r["resultado"]["vuelta_ok"] is True, True)

    print("\nC - DOMINIO: un decimal por un entero de una cifra (o 10, 100), contra el testigo")
    rnd = random.Random(219)
    malos, total, t0, lento = [], 0, time.time(), 0.0
    for k in (1, 2, 3):
        for _ in range(40):
            c = rnd.randint(1, 9999 if k > 1 else 999)
            x = dec(c, k)
            for n in (rnd.randint(2, 9), rnd.choice((1, 10, 100))):
                total += 1
                q = "%s x %d" % (x, n) if total % 2 else "%d x %s" % (n, x)
                t1 = time.time()
                v = S(q)
                lento = max(lento, time.time() - t1)
                if v != T(Decimal(x) * n):
                    malos.append((q, v))
    print("        %d productos en %.1f s (el mas lento %.2f s)" % (total, time.time() - t0, lento))
    comprobar("C1 ningun producto mal (%d)" % total, malos, [])
    comprobar("C2 ninguno tarda mas de 2 s", lento < 2, True)

    print("\nD - DOMINIO: por 0.1 y por 0.01 (las cifras bajan de sitio), contra el testigo")
    malos, total = [], 0
    for _ in range(60):
        k = rnd.choice((0, 0, 1))
        x = dec(rnd.randint(1, 99999), k)
        por = rnd.choice(("0.1", "0.01"))
        total += 1
        v = S("%s x %s" % (x, por))
        if v != T(Decimal(x) * Decimal(por)):
            malos.append((x, por, v))
    comprobar("D1 ningun producto por 0.1 o 0.01 mal (%d)" % total, malos, [])
    comprobar("D2 1.234 x 0.1 -> todavia no (cuatro cifras detras del punto)", S("1.234 x 0.1"), "todavia_no")

    print("\nE - DOMINIO: un decimal entre un numero de una cifra, contra el testigo")
    malos, exactas, cambios, nosale, total = [], 0, 0, 0, 0
    for _ in range(150):
        k = rnd.choice((1, 2, 3))
        d = rnd.randint(2, 9)
        x = dec(rnd.randint(1, 99999), k)
        total += 1
        v = S("%s : %d" % (x, d))
        exacto = Decimal(x) / d
        kf = max(k, -exacto.normalize().as_tuple().exponent)
        if exacto == exacto.quantize(Decimal("0.001")) and Decimal(x).scaleb(kf) > 10000000:
            esperado = "todavia_no"                             # contado en la unidad pequena pasa de diez millones (N.6; antes un millon):
            nosale += 1                                         # no se puede comprobar multiplicando
        elif exacto == exacto.quantize(Decimal("0.001")):
            esperado = T(exacto)
            if exacto == exacto.quantize(Decimal(1).scaleb(-k)):
                exactas += 1
            else:
                cambios += 1
        else:
            esperado = "todavia_no"
            nosale += 1
        if v != esperado:
            malos.append((x, d, v, esperado))
    for _ in range(100):                                        # divisiones hechas para que salgan justas
        k = rnd.choice((1, 2))
        d = rnd.randint(2, 9)
        q = rnd.randint(1, 9999)
        x = dec(q * d, k)
        total += 1
        v = S("%s : %d" % (x, d))
        if v != T(dec(q, k)):
            malos.append((x, d, v))
    print("        %d divisiones (%d justas a la primera, %d cambiando de unidad, %d que no salen)"
          % (total, exactas, cambios, nosale))
    comprobar("E1 ninguna division mal (%d)" % total, malos, [])

    print("\nF - DOMINIO: un decimal entre 10 y entre 100")
    malos, total = [], 0
    for _ in range(50):
        x = dec(rnd.randint(1, 9999), 1)
        for d in (10, 100):
            total += 1
            v = S("%s : %d" % (x, d))
            if v != T(Decimal(x) / d):
                malos.append((x, d, v))
    comprobar("F1 ninguna mal (%d)" % total, malos, [])

    print("\nG - CERCA DEL TECHO (diez millones desde N.6) y el TIEMPO")
    # antes (techo en un millon): 999.999 x 9, 99999.9 x 9, 999999.9 : 3, 999.999 x 2, 2943.4 : 8 -> todavia_no;
    # 5 x 999999 -> no_se_puede.  N.6: esos ya caben; los mismos, una cifra mas arriba, se pasan.
    casos = [("111.111 x 9", "999.999"), ("999.999 : 7", "142.857"), ("99999.9 : 9", "11111.1"),
             ("999.999 x 9", "8999.991"), ("99999.9 x 9", "899999.1"), ("999999.9 : 3", "333333.3"),
             ("9999.999 x 9", "todavia_no"), ("999999.9 x 9", "todavia_no"), ("9999999.9 : 3", "todavia_no"),
             ("0.001 x 9", "0.009"), ("0.001 : 2", "todavia_no"), ("100000 x 0.1", "10000"),
             ("999999 x 0.01", "9999.99"), ("0.5 x 999999", "todavia_no"), ("999.999 x 2", "1999.998"), ("9999.999 x 2", "todavia_no"),
             ("5 x 999999", "4999995"), ("5 x 9999999", "no_se_puede"), ("2943.4 : 8", "367.925"),
             ("29434.2 : 8", "todavia_no"), ("294.34 : 8", "todavia_no"),
             ("29.434 : 8", "todavia_no"), ("33.0 x 7", "231"), ("6.0 : 4", "1.5")]
    for q, esperado in casos:
        t1 = time.time()
        v = S(q)
        dt = time.time() - t1
        comprobar("G %-14s -> %-11s (%.2f s, menos de 2 s)" % (q, esperado, dt), (v, dt < 2), (esperado, True))
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\nTOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
