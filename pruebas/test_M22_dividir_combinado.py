# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.22: COMBINAR LA DIVISION CON LA SUMA Y LA RESTA (NCETM 2.28, 'Combining division with addition and
subtraction').  El plan y sus trampas: diario/2026-10-10-paso-M22-dividir-combinado.md
Pocas y representativas (decision de Carlos).  El orden (punto 1) ya lo sabe el MODELO COMUN: la cuenta con division que
la puerta vieja de M.16 no sabe leer va al resolvedor (sin puerta nueva).  La distributiva (punto 2) son PIEZAS de la
pregunta 'divisor_comun', que el resolvedor pide.  Python solo aparece aqui como TESTIGO externo.
"""
import importlib.util
import os
import random
import re
import shutil
import sys
import tempfile
import time
from fractions import Fraction

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)
TMP = tempfile.mkdtemp(prefix="m22_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia
import motor  # noqa: E402
import probar  # noqa: E402

BIEN = MAL = 0
JUNTAR = "juntar_sobre_el_divisor_comun"
CADA = "dividir_cada_una_y_juntar"


def comprobar(nombre, obtenido, esperado):
    global BIEN, MAL
    if obtenido == esperado:
        BIEN += 1
        print("  bien    %s" % nombre)
    else:
        MAL += 1
        print("  FALLA   %s\n          esperado=%r  obtenido=%r" % (nombre, esperado, obtenido))


SABER = motor.cargar_conocimiento()
PIEZAS = os.path.join(RAIZ, "conocimiento", "piezas")


def S(t):
    return probar.preguntar(probar.como_problema(t), SABER)[0]


def X(t):
    return motor.explicar_pregunta(t, SABER)


def DC(terminos, divisor, pieza="divisor_comun"):
    return motor.aplicar(pieza, {"terminos": terminos, "divisor": divisor}, SABER)


def testigo(cuenta):
    """La cuenta con Python (SOLO el testigo), en fracciones: ':' es dividir."""
    py = re.sub(r"(\d+)", r"Fraction(\1)", cuenta.replace(":", "/").replace("x", "*"))
    return eval(py, {"Fraction": Fraction})


def escrito(w):
    return "%d" % w.numerator if w.denominator == 1 else "%d/%d" % (w.numerator, w.denominator)


def modulo(nombre, cambiar):
    """La pieza leida de su archivo y TRUCADA: 'cambiar' = (lo que hay, lo que se pone)."""
    src = open(os.path.join(PIEZAS, nombre + ".py"), encoding="utf-8").read()
    assert cambiar[0] in src, cambiar[0]
    src = src.replace(cambiar[0], cambiar[1])
    ruta = os.path.join(TMP, nombre + ".py")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(src)
    sp = importlib.util.spec_from_file_location("m22_" + nombre, ruta)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def main():
    t0 = time.time()
    azar = random.Random(2028)
    print("=" * 78)
    print("PASO M.22: COMBINAR LA DIVISION CON LA SUMA Y LA RESTA (NCETM 2.28)")
    print("=" * 78)

    print("\nA - EL ORDEN (punto 1): sin parentesis la : antes que la + y la -; con parentesis, lo de dentro")
    malas, n = [], 0
    for _ in range(12):
        d = azar.randint(2, 9)
        q = azar.randint(1, 12)
        a = q * d                                   # (el testigo prepara divisiones justas: Python solo aqui)
        b = azar.randint(0, 40)
        formas = ["%d + %d : %d" % (b, a, d), "%d : %d + %d" % (a, d, b), "(%d + %d) : %d" % (a, d * b, d),
                  "%d - %d : %d" % (b + q, a, d), "%d + %d : %d - %d" % (b, a, d, azar.randint(0, b))]
        for c in formas:
            n += 1
            if S(c) != escrito(testigo(c)):
                malas.append(c)
    comprobar("A %d cuentas sin letras (la cuenta sola), contra el testigo" % n, malas, [])
    for c, esperado in (("20 - 12 : 4", "17"), ("(20 - 12) : 4", "2"), ("12 : 3 + 1", "5"),
                        ("36 : (2 + 7)", "4"), ("100 - 48 : 6 + 2", "94"), ("12 : 3 x 2", "8")):
        comprobar("A %s -> %s" % (c, esperado), S(c), esperado)

    print("\nB - LAS PIEZAS de 'divisor_comun' contra el testigo, con su vuelta")
    for pid in (JUNTAR, CADA):
        malas, n = [], 0
        for _ in range(20):
            d = azar.randint(2, 12)
            k = azar.randint(2, 3)
            if pid == CADA:
                vs = [azar.randint(0, 15) * d for _ in range(k)]
            else:
                vs = [azar.randint(0, 90) for _ in range(k)]
            signos = ["+"] + [azar.choice("+-") for _ in range(k - 1)]
            if testigo(" ".join("%s %d" % sv for sv in zip(signos, vs)).lstrip("+ ")) < 0:
                signos = ["+"] * k
            for i in range(2, k + 1):                   # (el testigo mira que no se baje de cero por el camino)
                if testigo(" ".join("%s %d" % sv for sv in zip(signos[:i], vs[:i])).lstrip("+ ")) < 0:
                    signos = ["+"] * k
            ts = [list(x) for x in zip(signos, vs)]
            r = DC(ts, d, pid)
            w = testigo(" ".join("%s %d : %d" % (s, v, d) for s, v in ts).lstrip("+ "))
            n += 1
            sale = Fraction(r["valor"]) + Fraction(r["resultado"].get("resto", 0), d) if r["conclusion"] == "hecho" else None
            if sale != w or r["resultado"]["vuelta_ok"] is not True or "... SI" not in r["resultado"]["vuelta"]:
                malas.append((ts, d))
        comprobar("B %s: %d casos, el numero del testigo y la vuelta en SI" % (pid, n), malas, [])

    print("\nC - QUE ELIGE EL CONTROL (el costo: una division en vez de varias)")
    for ts, d, esperado in (([["+", 12], ["+", 6]], 3, JUNTAR),
                            ([["+", 7], ["+", 9]], 4, JUNTAR),
                            ([["+", 50], ["-", 15], ["+", 5]], 5, JUNTAR),
                            ([["+", 9999990], ["+", 20]], 10, CADA)):  # juntar se pasa del techo: cada una
        r = DC(ts, d)
        comprobar("C %s entre %d -> %s" % (ts, d, esperado), r["conclusion"] == "hecho" and r["pieza"]["id"], esperado)
    comprobar("C 7 : 4 + 9 : 4: dividir cada una no sale justo (no la usa)", DC([["+", 7], ["+", 9]], 4, CADA)["conclusion"],
              "no_salio")
    comprobar("C 5 : 5 - 15 : 5: lo de arriba se baja de cero -> ninguna pieza (como antes, con negativos)",
              DC([["+", 5], ["-", 15]], 5)["conclusion"], "no_salio")
    comprobar("C divisores distintos no son de la pregunta", DC([["+", 12], ["+", 12]], 0)["conclusion"], "ninguna")

    print("\nD - LAS TRAMPAS: una pieza TRUCADA no se da por buena (su vuelta no cuadra)")
    base = motor.cargar_piezas()
    trampas = (
        (JUNTAR, ('r = u.usar("dividir", total=total, divisor=d)',
                  'r = u.usar("dividir", total=total, divisor=u.usar("sumar", a=d, b=d)["valor"])'),
         ([["+", 12], ["+", 6]], 3), "juntar tambien los divisores (18 : 6)"),
        (JUNTAR, ('nuevo = total if v == 0 else (v if total == 0 else u.usar("sumar", a=total, b=v)["valor"])',
                  'nuevo = total'),
         ([["+", 12], ["+", 6]], 3), "olvidar juntar uno de arriba"),
        (CADA, ('q = r["valor"]', 'q = v'),
         ([["+", 12], ["+", 6]], 3), "olvidar dividir (12 + 6 sin repartir)"),
        (CADA, ('nuevo = total if q == 0 else (q if total == 0 else u.usar("sumar", a=total, b=q)["valor"])',
                'nuevo = total if q == 0 else (q if total == 0 else u.usar("multiplicar", a=total, b=q)["valor"])'),
         ([["+", 12], ["+", 6]], 3), "multiplicar los cocientes en vez de sumarlos"),
    )
    for pid, cambio, (ts, d), que in trampas:
        u = motor._Lo_que_puede_usar(base["piezas"][pid], base, SABER)
        try:
            res = modulo(pid, cambio).hacer({"terminos": ts, "divisor": d}, u)
            cazado = res["vuelta_ok"] is False
        except (ValueError, motor.NoSalio, ZeroDivisionError, RuntimeError):
            cazado = True
        comprobar("D %s trucada -> la vuelta la caza" % que, cazado, True)

    print("\nE - POR EL MODELO COMUN (sin puerta nueva): la cuenta sola, verdad:, combinar:, resolver:")
    for q, esperado in (("12 : 3 + 6 : 3", "6"), ("7 : 4 + 9 : 4", "4"), ("combinar: 50 : 5 - 15 : 5", "7"),
                        ("verdad: 12 : 3 + 6 : 3 = 18 : 6", "falso"), ("verdad: 12 : 3 + 6 : 3 = (12 + 6) : 3", "verdadero"),
                        ("12 : 3 + 6 : 3 = 18 : 3", "verdadero"),
                        ("(3 + 5 + 7) : 3", "5"), ("resolver: 1 : 4 + 6 : 4", "7/4"), ("7 : 2 + 1", "9/2"),
                        ("resolver: r = 12 : 3 + 6 : 3", "r = 6"), ("resolver: r : 3 + 6 : 3 = 5", "r = 9")):
        comprobar("E %s -> %s" % (q, esperado), S(q), esperado)
    comprobar("E la cuenta con division va al resolvedor (no hay puerta nueva)",
              (motor.puerta_de("12 : 3 + 1", SABER), motor.puerta_de("3 + 4 x 5", SABER)), ("simbolica", "combinar"))
    t = X("7 : 4 + 9 : 4")
    comprobar("E la explicacion junta sobre el 4, lo comprueba y avisa de no juntar los divisores",
              "EL MISMO DIVISOR, 4" in t and "(7 + 9) : 4" in t and "16 : 4 = 4" in t and "... SI" in t
              and "los divisores NO se juntan" in t, True)

    print("\nF - EL ERROR TIPICO en la explicacion: de izquierda a derecha sin mirar")
    t = X("20 - 12 : 4")
    comprobar("F 20 - 12 : 4: ensena que (20 - 12) : 4 = 2 esta MAL", "(20 - 12) : 4, saldria 2: esta MAL" in t, True)
    comprobar("F (20 - 12) : 4 no lleva el aviso (el parentesis manda)", "OJO" in X("(20 - 12) : 4"), False)
    comprobar("F 12 : 3 + 1 no lleva el aviso (de izquierda a derecha sale lo mismo)", "OJO" in X("12 : 3 + 1"), False)

    print("\nG - ENTRE CERO Y CERCA DEL TECHO")
    comprobar("G 12 : 0 + 1 -> no se puede", S("12 : 0 + 1"), "no_se_puede")
    comprobar("G 0 : 3 + 0 : 3 -> 0", S("0 : 3 + 0 : 3"), "0")
    comprobar("G 9999990 : 10 + 20 : 10 -> 1000001 (juntar se pasaria del techo: cada una)",
              S("9999990 : 10 + 20 : 10"), "1000001")
    comprobar("G 9999999 : 1 + 3 : 1 -> se pasa del techo: todavia no", S("9999999 : 1 + 3 : 1"), "todavia_no")
    comprobar("G 9999999 : 1 + 1 : 1 -> 10000000 (el techo tiene nombre)", S("9999999 : 1 + 1 : 1"), "10000000")
    comprobar("G 9999998 : 2 + 2 : 2 -> 5000000", S("9999998 : 2 + 2 : 2"), "5000000")

    print("\nH - LO QUE NO CAMBIA")
    for q, esperado in (("3 + 4 x 5", "23"), ("4 x 6 + 4 x 2", "32"), ("verdad: 3 + 4 x 5 = 23", "verdadero"),
                        ("2 x 3 - 4 x 5", "todavia_no"), ("resolver: 5 : 5 - 15 : 5", "-2"),
                        ("resolver: 2 : 5 = 6 : r", "r = 15"), ("resolver: 0 : r = 0", "todavia_no"),
                        ("12 : 3", "4"), ("resolver: (12 + 6) : 3", "6")):
        comprobar("H %s -> %s" % (q, esperado), S(q), esperado)
    comprobar("H 12 : 3 + 12 : 4 (divisores distintos): el orden de siempre, 7", S("12 : 3 + 12 : 4"), "7")

    print("\nI - EL TIEMPO (cada pregunta muy por debajo de 2 s)")
    for q in ("100 - 48 : 6 + 2", "9999990 : 10 + 20 : 10", "50 : 5 - 15 : 5 + 5 : 5", "resolver: r : 3 + 6 : 3 = 5"):
        t1 = time.time()
        S(q)
        d = time.time() - t1
        comprobar("I %s (%.2f s)" % (q, d), d < 2, True)

    print("\n(%.1f s)" % (time.time() - t0))
    print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
    shutil.rmtree(TMP, ignore_errors=True)
    return 1 if MAL else 0


if __name__ == "__main__":
    sys.exit(main())
