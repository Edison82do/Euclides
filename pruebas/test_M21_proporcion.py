# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.21: EL FACTOR DE ESCALA, LA RAZON Y LA PROPORCION (NCETM 2.27, 'Scale factors, ratio and
proportional reasoning').  El plan y sus trampas: diario/2026-10-09-paso-M21-escala-y-razon.md
Pocas y representativas (decision de Carlos).  Lo nuevo son PIEZAS de la pregunta 'proporcion' (la tabla de razon),
que el resolvedor pide cuando ve a : b = c : ? ; sin puerta nueva.  Python solo aparece aqui como TESTIGO externo.
"""
import importlib.util
import os
import random
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
TMP = tempfile.mkdtemp(prefix="m21_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia
import motor  # noqa: E402
import probar  # noqa: E402
from _muestras import modo  # noqa: E402

BIEN = MAL = 0
ENTRE = "proporcion_por_el_factor_de_escala"
DENTRO = "proporcion_por_la_relacion_de_dentro"
PEQUENA = "proporcion_pasando_por_una_fila_mas_pequena"


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


def TABLA(conocida, con_hueco, pieza="proporcion"):
    return motor.aplicar(pieza, {"conocida": conocida, "con_hueco": con_hueco}, SABER)


def testigo(conocida, con_hueco):
    """El hueco con Python (SOLO el testigo): la fraccion que lo cumple."""
    a, b = conocida
    c, d = con_hueco
    return Fraction(c * b, a) if d is None else Fraction(d * a, b)


def modulo(nombre, cambiar):
    """La pieza leida de su archivo y TRUCADA: 'cambiar' = (lo que hay, lo que se pone)."""
    src = open(os.path.join(PIEZAS, nombre + ".py"), encoding="utf-8").read()
    assert cambiar[0] in src, cambiar[0]
    src = src.replace(cambiar[0], cambiar[1])
    ruta = os.path.join(TMP, nombre + ".py")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(src)
    sp = importlib.util.spec_from_file_location("m21_" + nombre, ruta)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def main():
    t0 = time.time()
    azar = random.Random(2027)
    print("=" * 78)
    print("PASO M.21 - EL FACTOR DE ESCALA Y LA TABLA DE RAZON  (%s)" % modo())
    print("=" * 78)

    print("\nA - SIN LAS TABLAS EN LA MEMORIA: lo pequeno sale (dividir con los saltos)")
    r = TABLA((2, 5), (6, None))
    comprobar("A1 2 | 5 y 6 | ? sin las tablas -> 15", r.get("valor"), 15)
    motor.aprender("tablas", SABER)

    print("\nB - CADA PIEZA CONTRA EL TESTIGO (el hueco en las dos columnas, la fila del hueco mayor o menor)")
    casos = {ENTRE: [], DENTRO: [], PEQUENA: []}
    for _ in range(14):                 # entre las filas: la fila del hueco = la conocida x k, o al reves
        p, q, k = azar.randint(1, 60), azar.randint(1, 60), azar.randint(2, 12)
        grande, chica = (p * k, q * k), (p, q)
        j = azar.randint(0, 1)
        if azar.randint(0, 1):
            casos[ENTRE].append((chica, (None, grande[1]) if j == 0 else (grande[0], None)))
        else:
            casos[ENTRE].append((grande, (None, chica[1]) if j == 0 else (chica[0], None)))
    for _ in range(14):                 # dentro de la fila: una columna es k veces la otra
        p, k, c = azar.randint(1, 99), azar.randint(2, 12), azar.randint(1, 999)
        fila = (p, p * k) if azar.randint(0, 1) else (p * k, p)
        grande = 1 if fila[1] != p else 0
        sabido = c if azar.randint(0, 1) else c * k          # a veces el hueco esta en la columna pequena
        j = 1 - grande if sabido == c * k else grande
        casos[DENTRO].append((fila, (None, sabido) if j == 0 else (sabido, None)))
    for _ in range(14):                 # pasar por una fila mas pequena: (p, q) primos entre si, x m y x k
        while True:
            p, q = azar.randint(2, 12), azar.randint(2, 12)
            if Fraction(p, q).numerator == p and p != q:
                break
        m, k = azar.randint(2, 9), azar.randint(2, 40)
        j = azar.randint(0, 1)
        h = (p * k, q * k)
        casos[PEQUENA].append(((p * m, q * m), (None, h[1]) if j == 0 else (h[0], None)))
    for pid, lista in casos.items():
        malas = []
        for c, h in lista:
            w = testigo(c, h)
            r = TABLA(c, h, pid)
            if w.denominator != 1:
                if r.get("conclusion") == "hecho":
                    malas.append((c, h))
                continue
            if (r.get("conclusion"), r.get("valor")) != ("hecho", w.numerator) or not r["resultado"]["vuelta_ok"]:
                malas.append((c, h, r.get("conclusion"), r.get("valor"), r.get("porque")))
        comprobar("B %s: %d tablas como el testigo, con su vuelta" % (pid, len(lista)), malas, [])
    r = TABLA((2, 5), (6, None), ENTRE)
    comprobar("B entre las filas 2 | 5 y 6 | ?: de 2 a 6 es x 3 y 5 x 3 = 15; vuelta 15 : 3 = 5",
              ("de 2 a 6 es x 3" in r["resultado"]["cuenta"] and "5 x 3 = 15" in r["resultado"]["cuenta"],
               r["resultado"]["vuelta"]), (True, "15 : 3 = 5 y 2 x 3 = 6 ... SI"))
    r = TABLA((12, 30), (None, 5), ENTRE)
    comprobar("B entre las filas hacia abajo: 12 | 30 y ? | 5: de 30 a 5 es : 6, 12 : 6 = 2",
              (r.get("valor"), "de 30 a 5 es : 6" in r["resultado"]["cuenta"]), (2, True))
    r = TABLA((3, 12), (7, None), DENTRO)
    comprobar("B dentro: 3 | 12 y 7 | ?: x 4 en todas las filas, 7 x 4 = 28",
              (r.get("valor"), "4 veces" in r["resultado"]["cuenta"], r["resultado"]["vuelta_ok"]), (28, True, True))
    r = TABLA((6, 9), (10, None), PEQUENA)
    comprobar("B la fila pequena: 6 | 9 = 2 | 3 (entre 3), de 2 a 10 x 5, 3 x 5 = 15",
              (r.get("valor"), "2 | 3" in r["resultado"]["cuenta"], r["resultado"]["vuelta"]),
              (15, True, "2 | 3 x 3 = 6 | 9 y 2 | 3 x 5 = 10 | 15 ... SI"))

    print("\nC - QUE ELIGE EL CONTROL (el costo): entre las filas, dentro, la fila pequena; si no sale justo, ninguna")
    for c, h, pid in (((2, 5), (6, None), ENTRE), ((12, 30), (None, 5), ENTRE), ((3, 12), (7, None), DENTRO),
                      ((15, 5), (None, 4), DENTRO), ((6, 9), (10, None), PEQUENA), ((10, 25), (4, None), PEQUENA),
                      ((1, 50000), (7, None), ENTRE)):
        r = TABLA(c, h)
        comprobar("C %s / %s -> %s" % (c, h, pid), (r.get("conclusion"), r.get("pieza", {}).get("id")), ("hecho", pid))
    comprobar("C 2 | 5 y 7 | ?: ningun camino justo (17 y 1/2) -> ninguna pieza",
              TABLA((2, 5), (7, None))["conclusion"], "ninguna")
    comprobar("C 4 | 6 y 9 | ?: la fila pequena 2 | 3 no lleva justo a 9 -> no sale",
              TABLA((4, 6), (9, None))["conclusion"], "no_salio")
    comprobar("C con un cero no es una tabla de razon", TABLA((0, 5), (0, None))["conclusion"], "ninguna")

    print("\nD - LAS TRAMPAS: una pieza TRUCADA no se da por buena (su vuelta no cuadra)")
    base = motor.cargar_piezas()
    trampas = (
        (ENTRE, ('v = u.usar("multiplicar", a=otro, b=k)["valor"]',
                 'v = u.usar("sumar", a=otro, b=u.usar("dividir", total=y, divisor=1)["valor"])["valor"]'),
         ((2, 5), (6, None)), "SUMAR en vez de multiplicar (5 + 4)"),
        (ENTRE, ('v = u.usar("multiplicar", a=otro, b=k)["valor"]', 'v = u.usar("multiplicar", a=x, b=k)["valor"]'),
         ((2, 5), (6, None)), "el factor a la columna equivocada"),
        (ENTRE, ('v = _justo(u, otro, k)\n', 'v = u.usar("multiplicar", a=otro, b=k)["valor"]\n'),
         ((12, 30), (None, 5)), "al reves (x en vez de :)"),
        (DENTRO, ('v = u.usar("multiplicar", a=sabido, b=k)["valor"]',
                  'v = u.usar("multiplicar", a=sabido, b=u.usar("dividir", total=sabido, divisor=1)["valor"])["valor"]'),
         ((3, 12), (7, None)), "mezclar las columnas"),
        (PEQUENA, ('p = (r["arriba"], r["abajo"])', 'p = (r["arriba"], c[1])'),
         ((6, 9), (10, None)), "dividir solo UNA columna"),
    )
    for pid, cambio, (c, h), que in trampas:
        u = motor._Lo_que_puede_usar(base["piezas"][pid], base, SABER)
        try:
            res = modulo(pid, cambio).hacer({"conocida": c, "con_hueco": h}, u)
            cazado = res["vuelta_ok"] is False
        except (ValueError, motor.NoSalio, ZeroDivisionError, RuntimeError):
            cazado = True
        comprobar("D %s: %s / %s trucada -> la vuelta la caza" % (que, c, h), cazado, True)

    print("\nE - POR EL MODELO COMUN: el resolvedor (sin puerta nueva)")
    for q, esperado in (("resolver: 2 : 5 = 6 : r", "r = 15"),
                        ("resolver: 2/5 = 6/r", "r = 15"),
                        ("resolver: r : 5 = 6 : 15", "r = 2"),
                        ("resolver: 4 : r = 10 : 25", "r = 10"),
                        ("resolver: 3 : 12 = 7 : r", "r = 28"),
                        ("resolver: 1 : 50000 = 7 : r", "r = 350000"),
                        ("resolver: 4 : 6 = 10 : r", "r = 15"),
                        ("resolver: 4 x k = 12", "k = 3"),
                        ("resolver: c = 3 x 4", "c = 12")):
        comprobar("E %s -> %s" % (q, esperado), S(q), esperado)
    t = motor.explicar_pregunta("resolver: 6 : 9 = 10 : r", SABER)
    comprobar("E la explicacion dice LA TABLA DE RAZON, pasa por 2 | 3 y lo comprueba",
              "LA TABLA DE RAZON" in t and "2 | 3" in t and "10 | 15 ... SI" in t and "r = 15" in t, True)
    t = motor.explicar_pregunta("resolver: 2 : 5 = 6 : r", SABER)
    comprobar("E 2 : 5 = 6 : r ya no divide entre una fraccion (6 : 2/5): escala x 3",
              "6 : 2/5" not in t and "de 2 a 6 es x 3" in t, True)

    print("\nF - CERCA DEL TECHO (diez millones)")
    comprobar("F 3 : 2000000 = 6 : r -> 4000000 (antes: todavia no, dividia entre 3/2000000)",
              S("resolver: 3 : 2000000 = 6 : r"), "r = 4000000")
    comprobar("F 1 : 2000000 = 6 : r -> 12000000 se pasa del techo: todavia no (como antes)",
              S("resolver: 1 : 2000000 = 6 : r"), "todavia_no")
    comprobar("F 3 : 7 = 9999999 : r: se pasa -> todavia no", S("resolver: 3 : 7 = 9999999 : r"), "todavia_no")
    comprobar("F 9999999 : 3 = r : 1 -> 3333333", S("resolver: 9999999 : 3 = r : 1"), "r = 3333333")

    print("\nG - LO QUE NO CAMBIA (las respuestas de antes)")
    for q, esperado in (("resolver: 2 : 5 = 7 : r", "r = 35/2"),          # no sale justo: como antes
                        ("resolver: 4 : 6 = 9 : r", "r = 27/2"),
                        ("resolver: a : b = 2 : 3; a + b = 40", "a = 16, b = 24"),
                        ("resolver: 2 x r = 5 x 6", "r = 15"),
                        ("resolver: 0 : 5 = 0 : r", "ninguna"),
                        ("resolver: 5 : 0 = 3 : r", "no_se_puede"),
                        ("resolver: 2 : 5 = 0 : r", "no_cuadra"),
                        ("resolver: 8 : 4 = 6 : r", "r = 3"),
                        ("resolver: 25 : 40 = 1000 : r", "r = 1600"),
                        ("6 : 2 x 5", S("6 : 2 x 5"))):
        comprobar("G %s -> %s" % (q, esperado), S(q), esperado)
    malas = []
    for c, h in casos[ENTRE][:6] + casos[DENTRO][:6]:
        w = testigo(c, h)
        izq = "%d : %d" % c
        der = ("r : %d" % h[1]) if h[0] is None else ("%d : r" % h[0])
        esperado = "r = %d" % w.numerator if w.denominator == 1 else "r = %d/%d" % (w.numerator, w.denominator)
        if S("resolver: %s = %s" % (izq, der)) != esperado:
            malas.append((c, h))
    comprobar("G el numero es el del testigo (12 proporciones por el resolvedor)", malas, [])

    print("\nH - EL TIEMPO (cada pregunta muy por debajo de 2 s)")
    for q in ("resolver: 6 : 9 = 10 : r", "resolver: 3 : 2000000 = 6 : r", "resolver: 48 : 36 = r : 15",
              "resolver: 17 : 23 = 34 : r"):
        t1 = time.time()
        S(q)
        d = time.time() - t1
        comprobar("H %s (%.2f s)" % (q, d), d < 2, True)

    print("\n(%.1f s)" % (time.time() - t0))
    print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
    shutil.rmtree(TMP, ignore_errors=True)
    return 1 if MAL else 0


if __name__ == "__main__":
    sys.exit(main())
