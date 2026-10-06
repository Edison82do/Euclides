# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO N.2: REDONDEAR A LA DECENA Y A LA CENTENA (Common Core 3.NBT.A.1).
El plan y sus trampas: diario/2026-10-06-paso-N2-redondear.md
Python solo aparece aqui como TESTIGO externo.
"""
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)
TMP = tempfile.mkdtemp(prefix="n2_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia
import motor  # noqa: E402
import probar  # noqa: E402
from _muestras import modo, numeros  # noqa: E402

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


def R(n, a):
    r = motor.decidir_redondear(n, a, SABER)
    return r.get("valor") if r["conclusion"] == "hecho" else r["conclusion"]


def testigo(n, a):
    """El testigo externo: Python, la decena o centena mas cercana; en la mitad, hacia arriba."""
    m = 10 if a == "decena" else 100
    return (n + m // 2) // m * m


def S(t):
    return probar.preguntar(t, SABER)[0]


print("=" * 78)
print("PASO N.2 - REDONDEAR A LA DECENA Y A LA CENTENA  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRAMPAS DEL PLAN (3.NBT.A.1)")
    comprobar("A1 37 -> 40 (pasa de la mitad, 35)", R(37, "decena"), 40)
    comprobar("A2 32 -> 30 (no llega a la mitad)", R(32, "decena"), 30)
    comprobar("A3 35 -> 40 (justo en la mitad: convenio, sube)", R(35, "decena"), 40)
    comprobar("A4 40 -> 40 (ya es redondo)", R(40, "decena"), 40)
    comprobar("A5 247 a la centena -> 200 (no 300 por la cadena)", R(247, "centena"), 200)
    comprobar("A6 250 a la centena -> 300 (mitad)", R(250, "centena"), 300)
    comprobar("A7 249 a la centena -> 200", R(249, "centena"), 200)
    comprobar("A8 995 a la decena -> 1000 (cambia la centena)", R(995, "decena"), 1000)
    comprobar("A9 950 a la centena -> 1000", R(950, "centena"), 1000)
    comprobar("A10 49 a la centena -> 0", R(49, "centena"), 0)
    comprobar("A11 4 a la decena -> 0;  5 -> 10;  0 -> 0", (R(4, "decena"), R(5, "decena"), R(0, "decena")), (0, 10, 0))
    comprobar("A12 1000 -> 1000 a los dos sitios", (R(1000, "decena"), R(1000, "centena")), (1000, 1000))
    comprobar("A13 1001 -> no esta en la lista", R(1001, "decena"), "ninguna")

    print("\nB - DE 0 A 1000 CONTRA EL TESTIGO (muestra), LOS DOS CAMINOS DE ACUERDO")
    for a in ("decena", "centena"):
        malos, vistos = [], 0
        extra = [x for x in range(0, 1001, 5)] if a == "decena" else [x for x in range(0, 1001, 50)]
        for n in numeros(0, 1000, extra=extra):
            vistos += 1
            r = motor.decidir_redondear(n, a, SABER)
            dos = len(r.get("todos", [])) == 2
            if r["conclusion"] != "hecho" or r["valor"] != testigo(n, a) or not dos:
                malos.append((n, r["conclusion"], r.get("valor"), testigo(n, a)))
        comprobar("B %d numeros a la %s: igual que el testigo, por la recta y por el atajo" % (vistos, a),
                  malos[:3], [])

    print("\nC - LA CADENA (el error documentado: 247 -> 250 -> 300)")
    cadenas = [n for n in range(0, 1001) if n % 100 in (45, 46, 47, 48, 49)][:40]
    malos = [n for n in cadenas if R(n, "centena") != testigo(n, "centena")]
    comprobar("C1 %d numeros donde la cadena engana (x45 a x49): todos bien" % len(cadenas), malos, [])
    t = motor.explicar_pregunta("redondear: 247", SABER)
    comprobar("C2 y la explicacion avisa de la trampa", "TRAMPA DE LA CADENA" in t, True)
    t = motor.explicar_pregunta("redondear: 37", SABER)
    comprobar("C3 donde no hay trampa, no avisa", "TRAMPA DE LA CADENA" in t, False)

    print("\nD - LA EXPLICACION Y EL PROBADOR")
    t = motor.explicar_pregunta("redondear: 37 a la decena", SABER)
    comprobar("D1 la recta: entre 30 y 40, la mitad 35, cuanto hay a cada lado",
              ("37 esta entre 30 y 40" in t, "La mitad del camino es 35" in t, "de 37 a 40 hay 3" in t), (True, True, True))
    t = motor.explicar_pregunta("redondear: 35 a la decena", SABER)
    comprobar("D2 la mitad: dice que es un CONVENIO", "CONVENIO" in t, True)
    comprobar("D3 'redondear: 37' -> las dos", S("redondear: 37"), "decena 40, centena 0")
    comprobar("D4 'redondear: 247 a la centena' -> 200", S("redondear: 247 a la centena"), "200")
    comprobar("D5 'redondear: 37 a la decena mas cercana' -> 40", S("redondear: 37 a la decena mas cercana"), "40")
    comprobar("D6 al millar -> todavia_no", S("redondear: 4567 al millar"), "todavia_no")
    comprobar("D7 'redondear: hola' -> no_entiendo", S("redondear: hola"), "no_entiendo")
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("-" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
