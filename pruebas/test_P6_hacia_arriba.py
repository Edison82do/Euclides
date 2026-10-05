# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO P.6: RESTAR PENSANDO EN SUMAR (contar hacia arriba; Common Core 1.OA.B.4).
El plan y sus trampas: diario/2026-10-05-paso-P6-restar-sumando.md
Python (a - b) solo aparece aqui como TESTIGO externo.
"""
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
TMP = tempfile.mkdtemp(prefix="arriba_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia
import motor  # noqa: E402
from _muestras import numeros, modo  # noqa: E402

BIEN = MAL = 0
PIEZA = "restar_contando_hacia_arriba"


def comprobar(nombre, obtenido, esperado):
    global BIEN, MAL
    if obtenido == esperado:
        BIEN += 1
        print("  bien    %s" % nombre)
    else:
        MAL += 1
        print("  FALLA   %s\n          esperado=%r  obtenido=%r" % (nombre, esperado, obtenido))


SABER = motor.cargar_conocimiento()
BASE = motor.cargar_piezas()
R = lambda a, b: motor.aplicar("restar", {"a": a, "b": b}, SABER)     # noqa: E731


def descarte(r):
    return [c.get("descartado") for c in r["candidatos"] if c["id"] == PIEZA][0]


print("=" * 78)
print("PASO P.6 - RESTAR PENSANDO EN SUMAR  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - CUANDO LOS NUMEROS ESTAN CERCA, SE CUENTA HACIA ARRIBA")
    r = R(13, 8)
    comprobar("A1 13 - 8 = 5: del 8 al 13 -> 9, 10, 11, 12, 13",
              (r["pieza"]["id"], r["valor"], "9, 10, 11, 12, 13" in r["resultado"]["cuenta"]), (PIEZA, 5, True))
    comprobar("A2 y dice la suma que hay detras: 8 + 5 = 13", "Porque 8 + 5 = 13" in r["resultado"]["cuenta"], True)
    r = R(52, 48)
    comprobar("A3 52 - 48 = 4 contando 49, 50, 51, 52 (antes: columnas)", (r["pieza"]["id"], r["valor"]), (PIEZA, 4))
    r = R(100, 95)
    comprobar("A4 100 - 95 = 5 sin cambiar centenas por decenas", (r["pieza"]["id"], r["valor"]), (PIEZA, 5))
    rapidas = {p["id"] for p in BASE["piezas"].values()
               if p["responde"] == "restar" and p["rapidez"] < BASE["piezas"][PIEZA]["rapidez"]}
    casos = [(a, a - d) for a in numeros(0, 1000) for d in range(0, 11) if a - d > d]
    mal_valor, mal_eleccion = [], []
    for a, b in casos:
        r = R(a, b)
        if r["conclusion"] != "hecho" or r["valor"] != a - b or not r["resultado"]["vuelta_ok"]:
            mal_valor.append("%d-%d -> %s" % (a, b, r.get("valor")))
            continue
        mas_rapida = [c["id"] for c in r["candidatos"] if c.get("aplica") and c["id"] in rapidas
                      and not c.get("no_salio")]
        if not mas_rapida and r["pieza"]["id"] != PIEZA:
            mal_eleccion.append("%d-%d -> %s" % (a, b, r["pieza"]["id"]))
    comprobar("A5 muestra: numeros cerca -> da bien y la vuelta (la suma) cuadra  (%d casos)" % len(casos),
              mal_valor[:3], [])
    comprobar("A6 y se elige contar hacia arriba salvo que haya algo aun mas corto", mal_eleccion[:3], [])

    print("\nB - LAS TRAMPAS: NO SIEMPRE CONVIENE")
    r = R(13, 2)
    comprobar("B1 13 - 2: estan lejos (11 pasos hacia arriba) -> hacia atras, 2 dedos",
              (r["pieza"]["id"], r["valor"], (descarte(r) or "").startswith("estan lejos")),
              ("restar_con_dedos", 11, True))
    r = R(13, 5)
    comprobar("B2 13 - 5: hacia arriba son 8 pasos, hacia atras 5 -> hacia atras",
              (r["pieza"]["id"], r["valor"], (descarte(r) or "").startswith("se quita poco")),
              ("restar_con_dedos", 8, True))
    r = R(13, 13)
    comprobar("B3 13 - 13 = 0 (no falta nada)", (r["pieza"]["id"], r["valor"]), (PIEZA, 0))
    r = R(8, 13)
    comprobar("B4 8 - 13: imposible (no hay restas negativas)", r["conclusion"], "imposible")

    print("\nC - UN PROBLEMA LO APROVECHA SIN SABER QUE EXISTE")
    r = motor.aplicar("paso", {"tipo": "cambio", "antes": 52, "signo": "-", "n": 48}, SABER)
    comprobar("C1 habia 52 y se van 48: quitar, y calcula contando hacia arriba",
              (r["pieza"]["id"], r["resultado"]["pieza"]["id"], r["valor"]), ("quitar", PIEZA, 4))
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
