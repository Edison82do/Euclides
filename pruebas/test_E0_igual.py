# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO E.0: EL = , VERDADERO O FALSO (Common Core 1.OA.D.7).
El plan y sus trampas: diario/2026-10-05-paso-E0-el-igual.md
Python solo aparece aqui como TESTIGO externo.
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
TMP = tempfile.mkdtemp(prefix="igual_")
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


def V(texto):
    r = motor.decidir_igualdad(texto, SABER)
    if r["conclusion"] == "no_entiendo":
        return "no_entiendo", r
    return (r["valor"] if r["conclusion"] == "hecho" else "no_se_puede"), r


print("=" * 78)
print("PASO E.0 - EL = : VERDADERO O FALSO  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LOS EJEMPLOS DEL ESTANDAR (1.OA.D.7)")
    for frase, esperado in (("6 = 6", "verdadero"), ("7 = 8 - 1", "verdadero"),
                            ("5 + 2 = 2 + 5", "verdadero"), ("4 + 1 = 5 + 2", "falso")):
        comprobar("A %s -> %s" % (frase, esperado), V(frase)[0], esperado)

    print("\nB - LAS TRAMPAS")
    v, r = V("4 + 1 = 5 + 2")
    comprobar("B1 4 + 1 = 5 + 2: dice la trampa ('el = no dice da')", "no dice 'da'" in r["resultado"]["cuenta"], True)
    comprobar("B2 10 = 8 + 2: el resultado a la izquierda tambien vale", V("10 = 8 + 2")[0], "verdadero")
    v, r = V("7 = 7")
    comprobar("B3 7 = 7 sin ninguna operacion, y sin calcular", (v, r["pieza"]["id"]), ("verdadero", "igual_escrito_igual"))
    v, r = V("5 + 2 = 2 + 5")
    comprobar("B4 5 + 2 = 2 + 5 SIN CALCULAR (dar la vuelta, P.5)", (v, r["pieza"]["id"]),
              ("verdadero", "igual_dando_la_vuelta"))
    v, r = V("3 + 5 = 8 + 2 = 10")
    comprobar("B5 la cadena 3 + 5 = 8 + 2 = 10 es FALSA y lo dice", (v, "cadena" in r["resultado"]["cuenta"]),
              ("falso", True))
    comprobar("B6 8 + 4 = 12 + 5 (escribir 'lo que da' y seguir): FALSO", V("8 + 4 = 12 + 5")[0], "falso")
    comprobar("B7 3 - 5 = 2: un lado no es ningun numero -> no se puede decir", V("3 - 5 = 2")[0], "no_se_puede")
    comprobar("B8 sin = no es una igualdad", V("4 + 1")[0], "no_entiendo")
    comprobar("B9 47 + 30 = 80 - 3: con numeros grandes y metodos distintos", V("47 + 30 = 80 - 3")[0], "verdadero")
    comprobar("B10 5 - 2 = 2 - 5 NO es 'dar la vuelta' (en la resta no hay vuelta)", V("5 - 2 = 2 - 5")[0], "no_se_puede")

    print("\nC - LA MUESTRA: IGUALDADES AL AZAR CONTRA EL TESTIGO")
    azar = random.Random(20261005)

    def lado():
        a, b = azar.randint(0, 60), azar.randint(0, 60)
        k = azar.randint(0, 2)
        if k == 0:
            return str(a), a
        if k == 1:
            return "%d + %d" % (a, b), a + b
        a, b = max(a, b), min(a, b)
        return "%d - %d" % (a, b), a - b
    fallos, verdaderas = [], 0
    for _ in range(400):
        (ti, vi), (td, vd) = lado(), lado()
        if azar.random() < 0.4:                     # que haya bastantes verdaderas
            td, vd = str(vi), vi
        esperado = "verdadero" if vi == vd else "falso"
        verdaderas += esperado == "verdadero"
        if V("%s = %s" % (ti, td))[0] != esperado:
            fallos.append("%s = %s" % (ti, td))
    comprobar("C1 400 igualdades (%d verdaderas): todas bien juzgadas" % verdaderas, fallos[:3], [])

    print("\nD - LA ORDEN DEL PROBADOR")
    t = motor.explicar_pregunta("verdad: 4 + 1 = 5 + 2", SABER)
    comprobar("D1 'verdad: 4 + 1 = 5 + 2' explica y dice FALSO", t.strip().endswith("RESULTADO: FALSO"), True)
    t = motor.explicar_pregunta("verdadero o falso: 10 = 8 + 2", SABER)
    comprobar("D2 'verdadero o falso: ...' tambien vale", t.strip().endswith("RESULTADO: VERDADERO"), True)
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
