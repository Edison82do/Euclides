# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO P.5: DAR LA VUELTA (el orden no importa al juntar; Common Core 1.OA.B.3).
El plan y sus trampas: diario/2026-10-05-paso-P5-dar-la-vuelta.md
Python (a + b) solo aparece aqui como TESTIGO externo.
"""
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
TMP = tempfile.mkdtemp(prefix="vuelta_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia
import motor  # noqa: E402
from _muestras import numeros, modo  # noqa: E402

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
S = lambda a, b: motor.aplicar("sumar", {"a": a, "b": b}, SABER)     # noqa: E731

print("=" * 78)
print("PASO P.5 - DAR LA VUELTA  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - SE DA LA VUELTA CUANDO AYUDA")
    r = S(3, 47)
    comprobar("A1 3 + 47 = 50: empiezo por el 47 y cuento 3 con los dedos",
              (r["pieza"]["id"], r["valor"], "47 + 3 = 50" in r["resultado"]["cuenta"]),
              ("sumar_dando_la_vuelta", 50, True))
    comprobar("A2 y dice POR QUE se puede", "lo mismo que juntar 47 y 3" in r["resultado"]["cuenta"], True)
    r = S(30, 47)
    comprobar("A3 30 + 47 = 77: la vuelta y de diez en diez (57, 67, 77)",
              (r["pieza"]["id"], r["valor"], "57, 67, 77" in r["resultado"]["cuenta"]),
              ("sumar_dando_la_vuelta", 77, True))
    cortos = list(range(0, 11)) + [20, 30, 40, 50, 60, 70, 80, 90]
    casos = [(a, b) for a in cortos for b in numeros(0, 1000) if a < b and a + b <= 1000]
    fallos = []
    for a, b in casos:
        r = S(a, b)
        if r["conclusion"] != "hecho" or r["valor"] != a + b or not r["resultado"]["vuelta_ok"]:
            fallos.append("%d+%d -> %s %s" % (a, b, r.get("pieza", {}).get("id"), r.get("valor")))
    comprobar("A4 muestra: primero corto y menor -> da bien y la vuelta cuadra  (%d casos)" % len(casos),
              fallos[:3], [])
    fallos = []
    for a, b in casos:
        r = S(a, b)
        ids = [c["id"] for c in r["candidatos"] if c.get("aplica") and not c.get("no_salio")]
        if a >= 10 and b >= 10 and "sumar_dando_la_vuelta" in ids and r["pieza"]["id"] == "sumar_por_columnas":
            fallos.append("%d+%d" % (a, b))
    comprobar("A5 si la vuelta encaja, nunca se acaba en las columnas", fallos[:3], [])

    print("\nB - LAS TRAMPAS")
    r = S(47, 3)
    fila = [c for c in r["candidatos"] if c["id"] == "sumar_dando_la_vuelta"][0]
    comprobar("B1 47 + 3 ya empieza por el grande: no hay vuelta que dar",
              (fila.get("descartado", "").startswith("ya empieza por el grande"), r["pieza"]["id"]),
              (True, "sumar_con_dedos"))
    r = S(15, 47)
    fila = [c for c in r["candidatos"] if c["id"] == "sumar_dando_la_vuelta"][0]
    comprobar("B2 15 + 47: el 15 no es corto -> darle la vuelta no ayuda -> columnas",
              ("no ayuda" in fila.get("descartado", ""), r["pieza"]["id"], r["valor"]),
              (True, "sumar_por_columnas", 62))
    r = S(5, 5)
    comprobar("B3 5 + 5: son iguales, no hay vuelta", r["pieza"]["id"] != "sumar_dando_la_vuelta", True)
    base = motor.cargar_piezas()
    comprobar("B4 en la RESTA no hay vuelta (8 - 3 no es 3 - 8): ninguna pieza de restar la da",
              [p["id"] for p in base["piezas"].values() if p["responde"] == "restar" and "vuelta" in p["id"]], [])
    r = motor.aplicar("restar", {"a": 3, "b": 8}, SABER)
    comprobar("B5 y 3 - 8 sigue siendo imposible", r["conclusion"], "imposible")

    print("\nC - UN PROBLEMA LA APROVECHA SIN SABER QUE EXISTE")
    r = motor.aplicar("paso", {"tipo": "cambio", "antes": 3, "signo": "+", "n": 47}, SABER)
    comprobar("C1 tenia 3 y le dan 47: anadir, y calcula dando la vuelta",
              (r["pieza"]["id"], r["resultado"]["pieza"]["id"], r["valor"]), ("anadir", "sumar_dando_la_vuelta", 50))
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
