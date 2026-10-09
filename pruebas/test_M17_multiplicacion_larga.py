# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.17: ESTRATEGIAS PARA MULTIPLICAR NUMEROS GRANDES Y LA MULTIPLICACION LARGA (NCETM 2.23; 5.NBT.B.5).
El plan y sus trampas: diario/2026-10-09-paso-M17-multiplicacion-larga.md
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
TMP = tempfile.mkdtemp(prefix="m17_")
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
PIEZAS = os.path.join(RAIZ, "conocimiento", "piezas")


def S(t):
    return probar.preguntar(probar.como_problema(t), SABER)[0]


def M(a, b, base=None):
    return motor.aplicar("multiplicar", {"a": a, "b": b}, SABER, base)


def modulo(nombre, cambiar=None):
    """La pieza leida de su archivo; con 'cambiar' = (lo que hay, lo que se pone), una pieza TRUCADA."""
    src = open(os.path.join(PIEZAS, nombre + ".py"), encoding="utf-8").read()
    if cambiar:
        assert cambiar[0] in src, cambiar[0]
        src = src.replace(cambiar[0], cambiar[1])
    ruta = os.path.join(TMP, nombre + ".py")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(src)
    sp = importlib.util.spec_from_file_location("m17_" + nombre, ruta)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


class Tramposo:
    """Lo que se le da a la pieza, pero lo que devuelve UNA pieza que usa (la que se nombra) da uno de mas."""

    def __init__(self, real, cual):
        self._real, self._cual = real, cual

    def __getattr__(self, k):
        return getattr(self._real, k)

    def usar(self, nombre, **sit):
        r = self._real.usar(nombre, **sit)
        if nombre == self._cual:
            r = dict(r)
            r["valor"] = r["valor"] + 1
        return r


def main():
    t0 = time.time()
    azar = random.Random(2023)
    print("=" * 78)
    print("PASO M.17 - ESTRATEGIAS PARA NUMEROS GRANDES Y LA MULTIPLICACION LARGA  (%s)" % modo())
    print("=" * 78)

    print("\nA - SIN LAS TABLAS EN LA MEMORIA: lo de antes (la rejilla, con la suma de iguales)")
    r = M(3456, 247)
    comprobar("A1 3456 x 247 sin las tablas -> 853632 con la rejilla", (r.get("valor"), r["pieza"]["id"]),
              (853632, "multiplicar_en_rejilla"))
    motor.aprender("tablas", SABER)

    print("\nB - CADA PIEZA CONTRA EL TESTIGO (y su vuelta cuadra)")
    muestras = {
        "multiplicar_quitando_los_ceros": [(azar.randint(11, 9999), azar.choice([60, 20, 30, 70, 300, 4000, 50]))
                                           for _ in range(15)] + [(azar.randint(11, 99) * 100, azar.randint(11, 99) * 10)
                                                                  for _ in range(5)],
        "multiplicar_partiendo_un_factor": [(azar.randint(11, 999), azar.randint(11, 99)) for _ in range(20)],
        "multiplicar_por_un_factor_compuesto": [(azar.randint(11, 99999), azar.choice([12, 14, 15, 16, 18, 21, 24, 27,
                                                                                       28, 32, 35, 36, 42, 45, 48, 54,
                                                                                       56, 63, 64, 72, 81]))
                                                for _ in range(20)],
        "multiplicacion_larga": [(azar.randint(10, 99999), azar.randint(10, 999)) for _ in range(30)],
    }
    for pid, pares in muestras.items():
        mal, vueltas = [], 0
        for a, b in pares:
            if a * b >= 10000000:                       # (el testigo mira el techo; el sistema no lo sabe de antemano)
                continue
            r = motor.aplicar(pid, {"a": a, "b": b}, SABER)
            if r["conclusion"] != "hecho" or r["valor"] != a * b:
                mal.append((a, b, r["conclusion"], r.get("valor"), r.get("porque")))
            elif r["resultado"]["vuelta_ok"] and r["resultado"]["vuelta"]:
                vueltas += 1
        comprobar("B %s: una muestra contra el testigo, sin fallos" % pid, mal[:3], [])
        comprobar("B ... y en todas su vuelta (la operacion contraria) cuadra", vueltas,
                  len([1 for a, b in pares if a * b < 10000000]))

    print("\nC - EL CONTROL ELIGE COMO UN HUMANO DE 6.o (lo mental primero; la larga cuando hace falta)")
    for a, b, pid in ((300, 40, "multiplicar_por_decenas_justas"),       # punto 1: el hecho pequeno (M.9)
                      (234, 30, "multiplicar_quitando_los_ceros"),       # punto 2: 234 x 3 y un 0
                      (2300, 450, "multiplicar_quitando_los_ceros"),
                      (347, 6, "multiplicacion_corta"),                  # lo de M.10, igual
                      (25, 48, "multiplicar_escalando"),                 # lo de M.12, igual
                      (37, 46, "multiplicar_partiendo_un_factor"),       # punto 3: dos por dos
                      (326, 47, "multiplicar_partiendo_un_factor"),      # tres por dos
                      (1234, 24, "multiplicar_por_un_factor_compuesto"), # punto 5: 1234 x 4 x 6
                      (3456, 247, "multiplicacion_larga"),               # punto 4
                      (1234, 37, "multiplicacion_larga")):               # 37 es primo: no hay pareja
        r = M(a, b)
        comprobar("C %d x %d = %d con %s" % (a, b, a * b, pid), (r.get("valor"), r.get("pieza", {}).get("id")),
                  (a * b, pid))
    t = motor.explicar_pregunta("3456 x 247", SABER)
    comprobar("C la explicacion dibuja la larga, los ceros que guardan el sitio y la comprobacion",
              all(x in t for x in ("x    247", "138240", "un 0 que guarda el sitio", "dos 0 que guardan el sitio",
                                   "LO COMPRUEBO con la operacion contraria", "138240 : 10 : 4 = 3456 SI",
                                   "RESULTADO: 853632")), True)

    print("\nD - LAS TRAMPAS")
    for a, b in ((3456, 205), (3456, 111), (305, 4007), (99, 99), (3162, 3162), (1001, 9989)):
        r = M(a, b)
        comprobar("D %d x %d = %d (ceros y unos en medio, cerca del techo)" % (a, b, a * b),
                  (r.get("valor"), r["resultado"].get("vuelta_ok") if r.get("resultado") else None), (a * b, True))
    comprobar("D 4567 x 3000 se pasa de diez millones -> no se puede", S("4567 x 3000"), "no_se_puede")
    comprobar("D 3456 x 4567 se pasa de diez millones -> no se puede", S("3456 x 4567"), "no_se_puede")
    base = motor.cargar_piezas()
    # el 0 que guarda el sitio, olvidado (el error tipico): la pieza trucada no se da por buena
    m = modulo("multiplicacion_larga", ("        cs = [0 for _ in range(i)]\n", "        cs = []\n"))
    u = motor._Lo_que_puede_usar(base["piezas"]["multiplicacion_larga"], base, SABER)
    mal = m.hacer({"a": 3456, "b": 247}, u)
    comprobar("D la larga SIN EL 0 que guarda el sitio da %d ... y su vuelta NO cuadra" % mal["valor"],
              (mal["valor"] != 853632, mal["vuelta_ok"]), (True, False))
    for pid, sit, cual in (("multiplicacion_larga", {"a": 3456, "b": 247}, "multiplicacion_corta"),
                           ("multiplicacion_larga", {"a": 3456, "b": 247}, "sumar"),
                           ("multiplicar_partiendo_un_factor", {"a": 326, "b": 47}, "multiplicacion_corta"),
                           ("multiplicar_partiendo_un_factor", {"a": 326, "b": 47}, "sumar"),
                           ("multiplicar_por_un_factor_compuesto", {"a": 1234, "b": 24}, "multiplicacion_corta"),
                           ("multiplicar_quitando_los_ceros", {"a": 234, "b": 30}, "multiplicacion_corta")):
        u = motor._Lo_que_puede_usar(base["piezas"][pid], base, SABER)
        try:
            cazado = modulo(pid).hacer(sit, Tramposo(u, cual))["vuelta_ok"] is False
        except (ValueError, motor.NoSalio):
            cazado = True
        comprobar("D %s con '%s' dando uno de mas: su vuelta NO cuadra" % (pid, cual), cazado, True)
    # y en el motor: una larga trucada no da la respuesta; contesta otra pieza, bien
    otra = os.path.join(TMP, "piezas")
    shutil.copytree(PIEZAS, otra, ignore=shutil.ignore_patterns("__pycache__"))
    ruta = os.path.join(otra, "multiplicacion_larga.py")
    src = open(ruta, encoding="utf-8").read().replace("        cs = [0 for _ in range(i)]\n", "        cs = []\n")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(src)
    r = M(3456, 247, motor.cargar_piezas(otra))
    comprobar("D en el motor, con la larga trucada: 853632 por otra pieza (la rejilla)",
              (r.get("valor"), r.get("pieza", {}).get("id")), (853632, "multiplicar_en_rejilla"))

    print("\nE - POR EL MODELO COMUN: la tabla de puertas y el resolvedor (sin puerta nueva)")
    for q, esperado in (("3456 x 247", "853632"),
                        ("resolver: 3456 x 247", "853632"),
                        ("234 x 56 + 100", "13204"),
                        ("(25 x 48) x 12", "14400"),
                        ("n = 3456 x 247", "853632"),
                        ("n - 1000 = 234 x 56", "14104"),
                        ("n : 24 = 356", "n = 8544"),                     # antes: no_cuadra
                        ("n : 24 - 10 = 346", "n = 8544"),
                        ("resolver: 2 x (n : 24) = 712", "n = 8544"),
                        ("a = 125 x 64; b = a - 7999", "a = 8000, b = 1"),
                        ("x - y = 100; y = 1234 x 24", "x = 29716, y = 29616")):
        comprobar("E %s -> %s" % (q, esperado), S(q), esperado)
    t = motor.explicar_pregunta("resolver: 3456 x 247", SABER)
    comprobar("E el resolvedor dice con que multiplico (la larga)", "con la multiplicacion larga" in t, True)
    t = motor.explicar_pregunta("n : 24 = 356", SABER)
    comprobar("E n : 24 = 356 se comprueba DESHACIENDO (8544 : 24 = 356 porque 356 x 24 = 8544)",
              "8544 : 24 = 356 porque 356 x 24 = 8544 ... SI" in t, True)
    r = motor.decidir_resolver("n : 24 = 356", SABER)
    malo = {"n": ("+", 8545, 1, "entero")}
    motor._u_comprobar(r["modelo"], malo, SABER, r)
    comprobar("E ... y comprobar deshaciendo es de verdad: con n = 8545 NO cuadra", r["comprobacion_ok"], False)

    print("\nF - LO QUE SIGUE SIENDO DE OTRO PASO (la division larga, 2.24; el techo)")
    comprobar("F 24 x n = 8544 -> no_sale (dividir entre dos cifras es 2.24)", S("24 x n = 8544"), "no_sale")
    comprobar("F n = 4567 x 3000 -> no se pasa de diez millones sin decirlo", S("n = 4567 x 3000") in
              ("todavia_no", "no_se_puede", "no_sale"), True)

    print("\nG - EL TIEMPO (nada de contar de uno en uno: cada pregunta muy por debajo de 2 s)")
    for q in ("3456 x 247", "3162 x 3162", "n : 24 = 356", "x - y = 100; y = 1234 x 24"):
        t1 = time.time()
        S(q)
        d = time.time() - t1
        comprobar("G %s (%.2f s)" % (q, d), d < 2, True)

    print("\n(%.1f s)" % (time.time() - t0))
    print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
    shutil.rmtree(TMP, ignore_errors=True)
    return 1 if MAL else 0


if __name__ == "__main__":
    sys.exit(main())
