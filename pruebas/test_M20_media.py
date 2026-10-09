# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.20: LA MEDIA (NCETM 2.26, 'Mean average and equal shares').
El plan y sus trampas: diario/2026-10-09-paso-M20-la-media.md
Pocas y representativas (decision de Carlos).  Lo nuevo son PIEZAS de la pregunta 'media', que el resolvedor pide
cuando ve (v1 + ... + vk) : k; sin puerta nueva.  Python solo aparece aqui como TESTIGO externo.
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
TMP = tempfile.mkdtemp(prefix="m20_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia
import motor  # noqa: E402
import probar  # noqa: E402
from _muestras import modo  # noqa: E402

BIEN = MAL = 0
JUNTAR = "media_juntando_y_repartiendo"
NIVELAR = "media_nivelando"


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


def MEDIA(vs, pieza="media"):
    return motor.aplicar(pieza, {"valores": list(vs), "partes": len(vs)}, SABER)


def testigo(vs):
    """La media con Python (SOLO el testigo): (cociente, resto) y el texto del numero comun."""
    q, r = divmod(sum(vs), len(vs))
    f = Fraction(sum(vs), len(vs))
    return (q, r), ("%d" % f.numerator if f.denominator == 1 else "%d/%d" % (f.numerator, f.denominator))


def texto_media(vs):
    return "(%s) : %d" % (" + ".join("%d" % v for v in vs), len(vs))


def modulo(nombre, cambiar):
    """La pieza leida de su archivo y TRUCADA: 'cambiar' = (lo que hay, lo que se pone)."""
    src = open(os.path.join(PIEZAS, nombre + ".py"), encoding="utf-8").read()
    assert cambiar[0] in src, cambiar[0]
    src = src.replace(cambiar[0], cambiar[1])
    ruta = os.path.join(TMP, nombre + ".py")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(src)
    sp = importlib.util.spec_from_file_location("m20_" + nombre, ruta)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def main():
    t0 = time.time()
    azar = random.Random(2026)
    print("=" * 78)
    print("PASO M.20 - LA MEDIA (repartir por igual)  (%s)" % modo())
    print("=" * 78)

    print("\nA - SIN LAS TABLAS EN LA MEMORIA: la media sale igual (repartir con los saltos)")
    r = MEDIA([3, 5, 7])
    comprobar("A1 3, 5, 7 sin las tablas -> 5", r.get("valor"), 5)
    motor.aprender("tablas", SABER)

    print("\nB - CADA PIEZA CONTRA EL TESTIGO (enteras y no enteras), con su vuelta")
    muestras = [[3, 5, 7], [3, 4, 6], [0, 4, 8], [1, 2], [0, 0, 1], [7], ]
    muestras = [m for m in muestras if len(m) >= 2]
    for _ in range(12):
        k = azar.randint(2, 6)
        muestras.append([azar.randint(0, 999) for _ in range(k)])
    malas = []
    for vs in muestras:
        r = MEDIA(vs, JUNTAR)
        if (r.get("conclusion"), (r.get("valor"), r.get("resultado", {}).get("resto"))) != ("hecho", testigo(vs)[0]) \
                or not r["resultado"]["vuelta_ok"]:
            malas.append(vs)
    comprobar("B juntar y repartir: %d medias como el testigo" % len(muestras), malas, [])
    cerca = [[98, 102, 100, 104], [41, 45, 60], [12, 13], [50, 50, 50], [9999998, 9999999, 10000000]]
    for _ in range(12):
        k = azar.randint(2, 6)
        b = azar.randint(10, 999990)
        cerca.append([b + azar.randint(0, 20) for _ in range(k)])
    malas = []
    for vs in cerca:
        r = MEDIA(vs, NIVELAR)
        if (r.get("conclusion"), (r.get("valor"), r.get("resultado", {}).get("resto"))) != ("hecho", testigo(vs)[0]) \
                or not r["resultado"]["vuelta_ok"]:
            malas.append(vs)
    comprobar("B nivelar: %d medias como el testigo" % len(cerca), malas, [])
    r = MEDIA([98, 102, 100, 104], NIVELAR)
    comprobar("B nivelar 98, 102, 100, 104: la base, lo de encima (12) y 12 : 4 = 3",
              "el mas bajo es 98" in r["resultado"]["cuenta"] and "junto: 12" in r["resultado"]["cuenta"]
              and "12 : 4 = 3" in r["resultado"]["cuenta"], True)
    comprobar("B ... y se comprueba por el EQUILIBRIO", r["resultado"]["vuelta"],
              "por encima de 101 sobra 4; por debajo falta 4 ... SI")

    print("\nC - QUE ELIGE EL CONTROL (el costo): nivelar SOLO si estan cerca y no son pequenos")
    for vs, pid in (([98, 102, 100, 104], NIVELAR), ([41, 45, 60], NIVELAR), ([3, 5, 7], JUNTAR),
                    ([3, 4, 6], JUNTAR), ([10, 50], JUNTAR), ([100, 121], JUNTAR), ([100, 120], NIVELAR),
                    ([0, 4, 8], JUNTAR)):
        r = MEDIA(vs)
        comprobar("C %s -> %s" % (vs, pid), (r.get("conclusion"), r.get("pieza", {}).get("id")), ("hecho", pid))
    r = motor.aplicar("media", {"valores": [3, 5, 7], "partes": 2}, SABER)
    comprobar("C 3, 5, 7 entre 2 no es una media: ninguna pieza", r["conclusion"], "ninguna")

    print("\nD - LAS TRAMPAS: una pieza TRUCADA no se da por buena (su vuelta no cuadra)")
    base = motor.cargar_piezas()
    trampas = (
        (NIVELAR, ('r = u.usar("dividir", total=encima, divisor=k)',
                   'r = u.usar("dividir", total=encima, divisor=len(trozos))'), [98, 102, 100, 104],
         "repartir lo de encima solo entre los de arriba"),
        (NIVELAR, ('media = bajo if q == 0 else u.usar("sumar", a=bajo, b=q)["valor"]', 'media = bajo'),
         [41, 45, 60], "olvidar el trozo (quedarse en la base)"),
        (JUNTAR, ('r = u.usar("dividir", total=total, divisor=k)',
                  'r = u.usar("dividir", total=total, divisor=len([v for v in vs if v]))'), [0, 4, 8],
         "olvidar el cero al contar (12 : 2)"),
        (JUNTAR, ('q, resto = r["valor"], r["resultado"].get("resto", 0)', 'q, resto = r["valor"], 0'), [3, 4, 6],
         "tirar lo que sobra (13 : 3 = 4)"),
        (JUNTAR, ('nuevo = u.usar("sumar", a=total, b=v)["valor"]', 'nuevo = u.usar("sumar", a=total, b=1)["valor"]'),
         [3, 5, 7], "juntar mal los valores"),
    )
    for pid, cambio, vs, que in trampas:
        u = motor._Lo_que_puede_usar(base["piezas"][pid], base, SABER)
        try:
            res = modulo(pid, cambio).hacer({"valores": vs, "partes": len(vs)}, u)
            cazado = res["vuelta_ok"] is False
        except (ValueError, motor.NoSalio, ZeroDivisionError):
            cazado = True
        comprobar("D %s: %s trucada -> la vuelta la caza" % (que, vs), cazado, True)

    print("\nE - POR EL MODELO COMUN: el resolvedor (sin puerta nueva)")
    for q, esperado in (("resolver: m = (98 + 102 + 100 + 104) : 4", "m = 101"),
                        ("resolver: m = (3 + 4 + 6) : 3", "m = 13/3"),
                        ("resolver: m = (0 + 4 + 8) : 3", "m = 4"),
                        ("resolver: m = (2 + 3) : 2", "m = 5/2"),
                        ("resolver: 3 x m = 3 + 5 + 7", "m = 5"),
                        ("resolver: (4 + 7 + n) : 3 = 6", "n = 7"),
                        ("resolver: a = (31 + 35 + 30) : 3; b = (28 + 40) : 2", "a = 32, b = 34")):
        comprobar("E %s -> %s" % (q, esperado), S(q), esperado)
    t = motor.explicar_pregunta("resolver: m = (98 + 102 + 100 + 104) : 4", SABER)
    comprobar("E la explicacion dice LA MEDIA, que nivela y lo comprueba",
              "LA MEDIA de 98, 102, 100 y 104" in t and "nivelar" in t and "sobra 4; por debajo falta 4 ... SI" in t,
              True)
    t = motor.explicar_pregunta("resolver: m = (3 + 4 + 6) : 3", SABER)
    comprobar("E la media no entera: lo que sobra tambien se reparte (4 y 1/3)",
              "4 y 1/3 = 13/3" in t and "m = 13/3" in t, True)

    print("\nF - CERCA DEL TECHO (diez millones): el total se pasa, pero nivelar no lo necesita")
    comprobar("F (9999998 + 9999999 + 10000000) : 3 -> 9999999",
              S("resolver: m = (9999998 + 9999999 + 10000000) : 3"), "m = 9999999")
    comprobar("F (9999999 + 10000000) : 2: nivela (9999999 y 1/2), pero 19999999/2 no se puede escribir -> todavia no",
              (MEDIA([9999999, 10000000]).get("valor"), S("resolver: m = (9999999 + 10000000) : 2")),
              (9999999, "todavia_no"))
    comprobar("F (5000000 + 6000000) : 2: lejos y el total se pasa -> todavia no (como antes)",
              S("resolver: m = (5000000 + 6000000) : 2"), "todavia_no")

    print("\nG - LO QUE NO CAMBIA")
    comprobar("G (3 + 5 + 7) : 3 sin letras sigue respetando el ano (2.28)", S("(3 + 5 + 7) : 3"), "todavia_no")
    t = motor.explicar_pregunta("resolver: m = (3 + 5 + 7) : 5", SABER)
    comprobar("G (3 + 5 + 7) : 5 no es una media (5 no es cuantos son): como antes",
              ("LA MEDIA" not in t, S("resolver: m = (3 + 5 + 7) : 5")), (True, "m = 3"))
    comprobar("G (2.5 + 3.5) : 2 con decimales: como antes", S("resolver: m = (2.5 + 3.5) : 2"), "m = 3")
    malas = []
    for vs in muestras[:10]:
        if S("resolver: m = %s" % texto_media(vs)) != "m = %s" % testigo(vs)[1]:
            malas.append(vs)
    comprobar("G el numero es el de siempre (10 medias por el resolvedor, contra el testigo)", malas, [])

    print("\nH - EL TIEMPO (cada pregunta muy por debajo de 2 s)")
    for q in ("resolver: m = (98 + 102 + 100 + 104) : 4", "resolver: m = (9999998 + 9999999 + 10000000) : 3",
              "resolver: m = (987 + 654 + 321 + 123 + 456 + 789) : 6"):
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
