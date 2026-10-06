# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO E.1: ECUACIONES CON HUECO (Common Core 1.OA.D.8).
El plan y sus trampas: diario/2026-10-05-paso-E1-hueco.md
Python solo aparece aqui como TESTIGO externo.
"""
import os
import random
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
TMP = tempfile.mkdtemp(prefix="hueco_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia
import motor  # noqa: E402
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


def E(texto):
    r = motor.decidir_ecuacion(texto, SABER)
    return (r.get("valor") if r["conclusion"] == "hecho" else r["conclusion"]), r


print("=" * 78)
print("PASO E.1 - ECUACIONES CON HUECO  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LOS EJEMPLOS DEL ESTANDAR (1.OA.D.8)")
    comprobar("A1 8 + ? = 11 -> 3", E("8 + ? = 11")[0], 3)
    comprobar("A2 5 = _ - 3 -> 8 (el hueco a la derecha del =)", E("5 = _ - 3")[0], 8)
    comprobar("A3 6 + 6 = _ -> 12", E("6 + 6 = _")[0], 12)

    print("\nB - CADA SITIO DEL HUECO ES UN TIPO DE PROBLEMA (CGI), Y LO RESUELVE SU PIEZA")
    PIEZA = {("+", "resultado"): "anadir", ("+", "cambio"): "lo_que_llego",
             ("+", "comienzo"): "deshacer_lo_que_llego", ("-", "resultado"): "quitar",
             ("-", "cambio"): "lo_que_se_fue", ("-", "comienzo"): "deshacer_lo_que_se_fue"}
    azar = random.Random(20261005)
    fallos = {k: [] for k in PIEZA}
    n = 0
    for _ in range(120):
        a, b = azar.randint(0, 200), azar.randint(0, 200)
        for op in "+-":
            if op == "-":
                a, b = max(a, b), min(a, b)
            c = a + b if op == "+" else a - b
            for donde, eq, esperado in (("resultado", "%d %s %d = ?" % (a, op, b), c),
                                        ("cambio", "%d %s ? = %d" % (a, op, c), b),
                                        ("comienzo", "? %s %d = %d" % (op, b, c), a)):
                for texto in (eq, " = ".join(reversed(eq.split(" = ")))):     # y con el = al reves
                    n += 1
                    v, r = E(texto)
                    pieza = r.get("paso", {}).get("pieza", {}).get("id")
                    if v != esperado or pieza != PIEZA[(op, donde)] or not r.get("comprobacion_ok"):
                        fallos[(op, donde)].append("%s -> %s (%s)" % (texto, v, pieza))
    for (op, donde), f in sorted(fallos.items()):
        comprobar("B %s con el %s desconocido: su pieza, bien y comprobado por E.0" % (
            "juntar" if op == "+" else "separar", donde.upper()), f[:3], [])
    print("          (%d ecuaciones en la muestra)" % n)

    print("\nC - LAS TRAMPAS")
    v, r = E("8 + ? = 5")
    comprobar("C1 8 + ? = 5: imposible (si llega algo no puede haber menos)", v, "imposible")
    comprobar("C2 ? - 9 = 3 -> 12 (deshacer: 3 + 9)", E("? - 9 = 3")[0], 12)
    comprobar("C3 ? + ? = 10: dos huecos, se dice", E("? + ? = 10")[0], "dos_huecos")
    comprobar("C4 8 + 4 = ? + 5: la balanza (desde E.2 se resuelve: 7)", E("8 + 4 = ? + 5")[0], 7)
    comprobar("C5 8 + 3 = 11: no hay hueco", E("8 + 3 = 11")[0], "sin_hueco")
    comprobar("C6 los huecos ?, _, __ y el cuadradito", [E(x)[0] for x in
              ("8 + ? = 11", "8 + _ = 11", "8 + __ = 11", "8 + □ = 11")], [3, 3, 3, 3])
    comprobar("C7 con palabras alrededor: 'Que numero falta en 8 + ? = 11?'",
              E("Que numero falta en 8 + ? = 11?")[0], 3)
    comprobar("C8 900000 + ? = 1200000: se pasa de un millon (N.4) -> no entiendo", E("900000 + ? = 1200000")[0], "no_entiendo")
    v, r = E("? + 3 = 11")
    comprobar("C9 cuenta la ecuacion como historia (lenguaje rustico)", r.get("historia"),
              "tenia algunos, le dan 3, ahora tiene 11: cuantos tenia al principio?")

    print("\nD - ESCRITA DIRECTAMENTE EN EL PROBADOR (sin orden delante)")
    def probar(texto):
        p = subprocess.run([sys.executable, os.path.join(RAIZ, "probar.py"), texto], cwd=RAIZ,
                           capture_output=True, text=True, env=dict(os.environ))
        return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr[-200:]
    comprobar("D1 '8 + ? = 11' -> la ecuacion", probar("8 + ? = 11"), "RESULTADO: 3")
    comprobar("D2 '8 + 3 = 11' -> verdadero o falso", probar("8 + 3 = 11"), "RESULTADO: VERDADERO")
    comprobar("D3 '8 + 3' -> la cuenta (antes contestaba 'un_objeto')", probar("8 + 3"), "RESULTADO: 11")
    comprobar("D4 un problema con su pregunta sigue siendo un problema",
              probar("Ana tiene 5. Le dan 3. Cuantas tiene ahora?"), "RESULTADO: 8")
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
