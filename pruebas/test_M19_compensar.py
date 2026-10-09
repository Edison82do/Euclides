# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.19: CALCULAR COMPENSANDO (NCETM 2.25, 'Using compensation to calculate').
El plan y sus trampas: diario/2026-10-09-paso-M19-compensar.md
Pocas y representativas (decision de Carlos).  Lo nuevo son PIEZAS de 'multiplicar': entran por el modelo comun (la
tabla de puertas y el resolvedor), sin puerta nueva.  Python solo aparece aqui como TESTIGO externo.
"""
import importlib.util
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
TMP = tempfile.mkdtemp(prefix="m19_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia
import motor  # noqa: E402
import probar  # noqa: E402
from _muestras import modo  # noqa: E402

BIEN = MAL = 0
REDONDEA = "multiplicar_redondeando_un_factor"
POR_5_25 = "multiplicar_por_5_o_25_compensando"


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


def M(a, b):
    return motor.aplicar("multiplicar", {"a": a, "b": b}, SABER)


def modulo(nombre, cambiar):
    """La pieza leida de su archivo y TRUCADA: 'cambiar' = (lo que hay, lo que se pone)."""
    src = open(os.path.join(PIEZAS, nombre + ".py"), encoding="utf-8").read()
    assert cambiar[0] in src, cambiar[0]
    src = src.replace(cambiar[0], cambiar[1])
    ruta = os.path.join(TMP, nombre + ".py")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(src)
    sp = importlib.util.spec_from_file_location("m19_" + nombre, ruta)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def main():
    t0 = time.time()
    azar = random.Random(2025)
    print("=" * 78)
    print("PASO M.19 - CALCULAR COMPENSANDO  (%s)" % modo())
    print("=" * 78)

    print("\nA - SIN LAS TABLAS EN LA MEMORIA: no puede compensar (ni comprobarlo); sale lo de antes")
    r = M(399, 6)
    comprobar("A1 399 x 6 sin las tablas -> 2394, sin compensar", (r.get("valor"), r["pieza"]["id"] != REDONDEA),
              (2394, True))
    motor.aprender("tablas", SABER)

    print("\nB - CADA PIEZA CONTRA EL TESTIGO (y su vuelta cuadra)")
    redondos = [d * 10 ** n for d in range(1, 10) for n in range(1, 7)]
    pares = []
    for _ in range(40):
        f = azar.choice(redondos) - azar.choice([1, 2])
        g = azar.randint(2, 9999)
        if f > 12 and g % 10 and f * g < 10000000:
            pares.append((f, g) if azar.random() < 0.5 else (g, f))
    muestras = {REDONDEA: pares,
                POR_5_25: [(5, azar.randint(13, 999999)) for _ in range(12)]
                + [(25, azar.randint(13, 99999)) for _ in range(12)]}      # (x 100 tiene que caber en la lista)
    for pid, lista in muestras.items():
        lista = [(a, b) for a, b in lista if a * b < 10000000 and (a % 10 and b % 10)]
        mal, vueltas = [], 0
        for a, b in lista:
            r = motor.aplicar(pid, {"a": a, "b": b}, SABER)
            if r["conclusion"] != "hecho" or r["valor"] != a * b:
                mal.append((a, b, r["conclusion"], r.get("valor"), r.get("porque")))
            elif r["resultado"]["vuelta_ok"] and r["resultado"]["vuelta"]:
                vueltas += 1
        comprobar("B %s: %d multiplicaciones contra el testigo, sin fallos" % (pid, len(lista)), mal[:3], [])
        comprobar("B ... y en todas su vuelta (las operaciones contrarias) cuadra", vueltas, len(lista))

    print("\nC - EL CONTROL ELIGE POR EL COSTO (compensa solo cuando sale mas corto)")
    for a, b, pid in ((399, 6, REDONDEA),                     # el ejemplo de Carlos: 400 x 6 - 6
                      (6, 399, REDONDEA),
                      (98, 37, REDONDEA),                     # 3700 - 2 x 37
                      (1999, 7, REDONDEA),
                      (99, 99, REDONDEA),
                      (5, 4683, POR_5_25),                    # x 10 y la mitad
                      (25, 37, POR_5_25),                     # x 100 y la mitad de la mitad
                      (47, 6, "multiplicacion_corta"),        # a 3 de 50: tres grupos de mas ya no compensan (M.10)
                      (347, 6, "multiplicacion_corta"),       # no esta cerca de un redondo
                      (401, 6, "multiplicacion_corta"),       # por ENCIMA del redondo: eso es partir (la corta)
                      (25, 16, "multiplicar_escalando"),      # doblar y partir sigue antes (M.12)
                      (400, 6, "multiplicar_por_decenas_justas"),
                      (399, 20, "multiplicar_quitando_los_ceros"),
                      (8, 7, "recordar_producto"),
                      (11, 12, "recordar_producto")):
        r = M(a, b)
        comprobar("C %d x %d -> %s" % (a, b, pid), (r.get("valor"), r.get("pieza", {}).get("id")), (a * b, pid))
    r = M(399, 6)
    comprobar("C la cuenta de 399 x 6 dice el redondo y el GRUPO de mas",
              "400 x 6 = 2400" in r["resultado"]["cuenta"] and "2400 - 6 = 2394" in r["resultado"]["cuenta"], True)

    print("\nD - LAS TRAMPAS: una pieza TRUCADA no se da por buena (su vuelta no cuadra)")
    base = motor.cargar_piezas()
    trampas = (
        (REDONDEA, ('total = u.usar("restar", a=RG, b=grupos)["valor"]',
                    'total = u.usar("sumar", a=RG, b=grupos)["valor"]'), (399, 6), "compensar al reves (2400 + 6)"),
        (REDONDEA, ('total = u.usar("restar", a=RG, b=grupos)["valor"]',
                    'total = u.usar("restar", a=RG, b=k)["valor"]'), (399, 6), "quitar 1 y no UN GRUPO (2400 - 1)"),
        (REDONDEA, ('total = u.usar("restar", a=RG, b=grupos)["valor"]',
                    'total = u.usar("restar", a=RG, b=k)["valor"]'), (98, 37), "quitar 2 y no dos grupos (3700 - 2)"),
        (POR_5_25, ("    for _ in range(mitades):\n        m = u.usar", "    for _ in range(1):\n        m = u.usar"),
         (25, 37), "escalar mal: 3700 : 2 (una mitad sola)"),
    )
    for pid, cambio, (a, b), que in trampas:
        u = motor._Lo_que_puede_usar(base["piezas"][pid], base, SABER)
        try:
            res = modulo(pid, cambio).hacer({"a": a, "b": b}, u)
            cazado = res["vuelta_ok"] is False
        except (ValueError, motor.NoSalio):
            cazado = True
        comprobar("D %s: %d x %d trucada -> la vuelta la caza" % (que, a, b), cazado, True)

    print("\nE - CERCA DEL TECHO (diez millones)")
    comprobar("E 1999999 x 5 -> 9999995 (2000000 x 5 es justo el techo)", S("1999999 x 5"), "9999995")
    r = M(1999999, 5)
    comprobar("E ... compensando", r.get("pieza", {}).get("id"), REDONDEA)
    comprobar("E 2999999 x 4 se pasa: no_se_puede (como antes)", S("2999999 x 4"), "no_se_puede")
    comprobar("E 25 x 399999 -> 9999975", S("25 x 399999"), "9999975")
    r = M(25, 399999)
    comprobar("E ... sin x 100 y la mitad de la mitad (39999900 se sale de mi lista): otro metodo",
              (r.get("valor"), r.get("pieza", {}).get("id") != POR_5_25), (9999975, True))

    print("\nF - POR EL MODELO COMUN (sin puerta nueva)")
    for q, esperado in (("resolver: n = 399 x 6", "n = 2394"),
                        ("n : 7 = 1999", "13993"),
                        ("6 x n = 2394", "399"),
                        ("1999 x 7 + 1", "13994"),
                        ("2 x 49 x 5", "490"),
                        ("a + b = 1188; a = 11 x b", "a = 1089, b = 99")):
        comprobar("F %s -> %s" % (q, esperado), S(q), esperado)
    t = motor.explicar_pregunta("399 x 6", SABER)
    comprobar("F la explicacion de 399 x 6 dice que compensa y lo comprueba",
              "redondear un factor y compensar" in t and "2394 : 6 = 399 ... SI" in t, True)

    print("\nG - LO QUE YA HABIA DE COMPENSAR (P.7, sumas y restas) SIGUE IGUAL")
    comprobar("G 4997 + 2345 -> 7342", S("4997 + 2345"), "7342")
    r = motor.aplicar("sumar", {"a": 4997, "b": 2345}, SABER)
    comprobar("G ... con la misma suma (5000 + 2342), P.7", r["pieza"]["id"], "sumar_misma_suma")
    comprobar("G 625 - 398 -> 227", S("625 - 398"), "227")

    print("\nH - EL TIEMPO (cada pregunta muy por debajo de 2 s)")
    for q in ("399 x 6", "9999 x 999", "25 x 399999", "n : 7 = 1999"):
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
