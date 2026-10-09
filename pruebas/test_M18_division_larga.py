# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.18: DIVIDIR ENTRE DOS CIFRAS, LA DIVISION LARGA (NCETM 2.24; 5.NBT.B.6, 6.NS.B.2).
El plan y sus trampas: diario/2026-10-09-paso-M18-division-larga.md
Pocas y representativas (decision de Carlos).  Lo nuevo son PIEZAS de 'dividir': entran por el modelo comun (la
tabla de puertas, el resolvedor y todas las piezas que dividen), sin puerta nueva.  Python solo aparece aqui como
TESTIGO externo.
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
TMP = tempfile.mkdtemp(prefix="m18_")
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


def D(t, d, base=None):
    return motor.aplicar("dividir", {"total": t, "divisor": d}, SABER, base)


def modulo(nombre, cambiar=None):
    """La pieza leida de su archivo; con 'cambiar' = (lo que hay, lo que se pone), una pieza TRUCADA."""
    src = open(os.path.join(PIEZAS, nombre + ".py"), encoding="utf-8").read()
    if cambiar:
        assert cambiar[0] in src, cambiar[0]
        src = src.replace(cambiar[0], cambiar[1])
    ruta = os.path.join(TMP, nombre + ".py")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(src)
    sp = importlib.util.spec_from_file_location("m18_" + nombre, ruta)
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


OLVIDA_EL_0 = ("        cociente.append(q)\n", "        if q:\n            cociente.append(q)\n")


def main():
    t0 = time.time()
    azar = random.Random(2024)
    print("=" * 78)
    print("PASO M.18 - DIVIDIR ENTRE DOS CIFRAS: LA DIVISION LARGA  (%s)" % modo())
    print("=" * 78)

    print("\nA - SIN LAS TABLAS EN LA MEMORIA: la larga sale igual (los multiplos se hacen sumando)")
    r = D(5678, 23)
    comprobar("A1 5678 : 23 sin las tablas -> 246 resto 20 con la larga",
              (r.get("valor"), r.get("resultado", {}).get("resto"), r.get("pieza", {}).get("id")),
              (246, 20, "division_larga"))
    r = D(8544, 24)
    comprobar("A2 8544 : 24 sin las tablas: por los factores no (no se la pareja 4 x 6) -> la larga",
              (r.get("valor"), r.get("pieza", {}).get("id")), (356, "division_larga"))
    motor.aprender("tablas", SABER)

    print("\nB - CADA PIEZA CONTRA EL TESTIGO (y su vuelta cuadra)")
    pares = [(azar.randint(100, 9999999), azar.randint(10, 99)) for _ in range(60)]
    pares = [(t, d) for t, d in pares if t >= 10 * d]
    mal, vueltas = [], 0
    for t, d in pares:
        r = motor.aplicar("division_larga", {"total": t, "divisor": d}, SABER)
        if r["conclusion"] != "hecho" or (r["valor"], r["resultado"]["resto"]) != (t // d, t % d):
            mal.append((t, d, r["conclusion"], r.get("valor"), r.get("porque")))
        elif r["resultado"]["vuelta_ok"]:
            vueltas += 1
    comprobar("B division_larga: %d divisiones de 3 a 7 cifras entre 10..99, contra el testigo" % len(pares), mal[:3], [])
    comprobar("B ... y en todas su vuelta (cociente x divisor + resto) cuadra", vueltas, len(pares))
    compuestos = [12, 14, 15, 16, 18, 21, 24, 27, 28, 32, 35, 36, 42, 45, 48, 54, 56, 63, 64, 72, 81]
    pares = [(azar.randint(10, 99999) * d, d) for d in [azar.choice(compuestos) for _ in range(25)]]
    mal, vueltas = [], 0
    for t, d in pares:
        if t >= 10000000:
            continue
        r = motor.aplicar("dividir_por_un_divisor_compuesto", {"total": t, "divisor": d}, SABER)
        if r["conclusion"] != "hecho" or r["valor"] != t // d:
            mal.append((t, d, r["conclusion"], r.get("valor"), r.get("porque")))
        elif r["resultado"]["vuelta_ok"]:
            vueltas += 1
    comprobar("B dividir_por_un_divisor_compuesto: divisiones justas contra el testigo", mal[:3], [])
    comprobar("B ... y en todas su vuelta (multiplicando) cuadra", vueltas, len([1 for t, d in pares if t < 10000000]))
    r = motor.aplicar("dividir_por_un_divisor_compuesto", {"total": 437, "divisor": 12}, SABER)
    comprobar("B por los factores NO si sobra (437 : 3 : 4 no deja el resto de 437 : 12)", r["conclusion"], "no_salio")

    print("\nC - EL CONTROL ELIGE COMO UN HUMANO DE 6.o")
    for t, d, pid in ((8544, 24, "dividir_por_un_divisor_compuesto"),   # 24 = 4 x 6, justa
                      (5678, 23, "division_larga"),                      # 23 es primo
                      (437, 12, "division_larga"),                       # 12 = 3 x 4, pero sobra
                      (96, 24, "dividir_saltando"),                      # punto 1: el cociente menor que 10 (como antes)
                      (84, 14, "dividir_saltando"),
                      (600, 25, "dividir_escalando"),                    # M.12, igual: 1200 : 50 = 120 : 5
                      (7224, 8, "division_corta"),                       # M.11, igual
                      (840, 12, "dividir_decenas_justas")):              # M.9, igual: 84 : 12 = 7
        r = D(t, d)
        comprobar("C %d : %d = %d resto %d con %s" % (t, d, t // d, t % d, pid),
                  (r.get("valor"), r.get("resultado", {}).get("resto", 0), r.get("pieza", {}).get("id")),
                  (t // d, t % d, pid))
    t = motor.explicar_pregunta("2448 : 23", SABER)
    comprobar("C la explicacion dibuja la larga: los multiplos, restar, bajar, el 0 del cociente y la comprobacion",
              all(x in t for x in ("23 | 2448", "los multiplos de 23 que escribo: 23, 46, 69", "24 - 23 = 1",
                                   "bajo el 4", "un 0 en el cociente", "106 x 23 + 10 = 2448 ... SI",
                                   "RESULTADO: 106 resto 10")), True)

    print("\nD - LAS TRAMPAS")
    for t, d in ((2448, 24), (7224, 24), (24024, 24), (2448, 23), (756, 12), (9999, 99), (9999999, 99),
                 (9999999, 11), (1000000, 13), (990, 99), (100, 10)):
        r = motor.aplicar("division_larga", {"total": t, "divisor": d}, SABER)
        comprobar("D %d : %d = %d resto %d (ceros en el cociente, el primer paso, el techo)" % (t, d, t // d, t % d),
                  (r.get("valor"), r.get("resultado", {}).get("resto"), r.get("resultado", {}).get("vuelta_ok")),
                  (t // d, t % d, True))
    base = motor.cargar_piezas()
    m = modulo("division_larga", OLVIDA_EL_0)
    u = motor._Lo_que_puede_usar(base["piezas"]["division_larga"], base, SABER)
    malo = m.hacer({"total": 2448, "divisor": 23}, u)
    comprobar("D la larga que OLVIDA EL 0 del cociente da %d ... y su vuelta NO cuadra" % malo["valor"],
              (malo["valor"] != 106, malo["vuelta_ok"]), (True, False))
    for pid, sit, cual in (("division_larga", {"total": 5678, "divisor": 23}, "restar"),
                           ("division_larga", {"total": 5678, "divisor": 23}, "multiplicar"),
                           ("dividir_por_un_divisor_compuesto", {"total": 8544, "divisor": 24}, "division_corta"),
                           ("dividir_por_un_divisor_compuesto", {"total": 8544, "divisor": 24}, "multiplicacion_corta")):
        u = motor._Lo_que_puede_usar(base["piezas"][pid], base, SABER)
        try:
            cazado = modulo(pid).hacer(sit, Tramposo(u, cual))["vuelta_ok"] is False
        except (ValueError, motor.NoSalio):
            cazado = True
        comprobar("D %s con '%s' dando uno de mas: su vuelta NO cuadra" % (pid, cual), cazado, True)
    otra = os.path.join(TMP, "piezas")
    shutil.copytree(PIEZAS, otra, ignore=shutil.ignore_patterns("__pycache__"))
    ruta = os.path.join(otra, "division_larga.py")
    src = open(ruta, encoding="utf-8").read().replace(*OLVIDA_EL_0)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(src)
    r = D(2448, 23, motor.cargar_piezas(otra))
    comprobar("D en el motor, con la larga trucada: 2448 : 23 NUNCA da una respuesta falsa", r.get("valor") in (None, 106),
              True)
    comprobar("D 98765 : 123 (divisor de TRES cifras) -> no se puede todavia", S("98765 : 123"), "no_se_puede")
    comprobar("D 7.2 : 12 (un decimal entre dos cifras: de otro paso) -> todavia no", S("7.2 : 12"), "todavia_no")

    print("\nE - POR EL MODELO COMUN: los 'todavia no' que ahora salen (sin puerta nueva)")
    for q, esperado in (("8544 : 24", "356"),
                        ("2448 : 24", "102"),
                        ("24 x n = 8544", "356"),                          # antes no_sale (M.17)
                        ("n x 47 = 9776", "208"),
                        ("resolver: 8544 : n = 24", "n = 356"),
                        ("resolver: n = 437 : 12", "n = 437/12"),          # punto 3: el resto como fraccion
                        ("a + b = 567127; a = 10 x b", "a = 515570, b = 51557"),   # antes todavia_no (S.3)
                        ("factores: 169", "1, 13, 169"),                   # antes todavia_no (M.15)
                        ("primo: 997", "primo"),                           # antes todavia_no (M.15)
                        ("factores: 9991", "1, 97, 103, 9991"),
                        ("primo: 10403", "todavia_no"),                    # el medio pide dividir entre tres cifras
                        ("99 x 99 x 99", "970299"),                        # antes todavia_no (M.14: comprobar dividiendo)
                        ("13 x 17 x 19", "4199")):                         # antes todavia_no (M.14)
        comprobar("E %s -> %s" % (q, esperado), S(q), esperado)
    t = motor.explicar_pregunta("24 x n = 8544", SABER)
    comprobar("E el resolvedor dice con que dividio", "dividir usando los factores del divisor" in t, True)
    r = motor.aplicar("simplificar_fraccion", {"a": 836, "b": 722}, SABER)
    comprobar("E simplificar 836/722 -> 22/19 (antes todavia no: el 19 pedia la division larga)", r.get("valor"), "22/19")

    print("\nF - EL TIEMPO (nada de contar de uno en uno)")
    for q, tope in (("8544 : 24", 2), ("9999999 : 99", 2), ("24 x n = 8544", 2), ("primo: 997", 2),
                    ("factores: 9991", 3)):      # 99 divisiones largas: lo mas largo que pide el ano
        t1 = time.time()
        S(q)
        d = time.time() - t1
        comprobar("F %s (%.2f s, tope %d s)" % (q, d, tope), d < tope, True)

    print("\n(%.1f s)" % (time.time() - t0))
    print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
    shutil.rmtree(TMP, ignore_errors=True)
    return 1 if MAL else 0


if __name__ == "__main__":
    sys.exit(main())
