# -*- coding: utf-8 -*-
"""
PRUEBAS DE LAS TECNICAS PARA IR MAS RAPIDO (paso 4 del plan, 5 oct 2026).

Cada tecnica es una PIEZA.  Lo que tiene que quedar demostrado (una prueba = una afirmacion; las
grandes recorren una muestra: fronteras + azar fijo):
  A. El mecanismo nuevo: saltar una decena (subir y bajar) ESCRIBIENDO la cifra, con sus fronteras.
  B. De diez en diez (sumar y restar): da bien, la vuelta cuadra, y GANA donde encaja.
  C. Compensar (sumar y restar): da bien, la vuelta cuadra, y gana donde encaja.
  D. Casi dobles: solo si el doble ya se sabe de memoria (es un hecho DERIVADO).
  E. Donde NO encajan, se descartan con su porque, y gana otro metodo.
  F. Un problema las aprovecha sin saber que existen.
Python (a + b) solo aparece aqui, como TESTIGO externo: el sistema no lo usa.
"""
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
TMP = tempfile.mkdtemp(prefix="tecnicas_")
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


def recorrer(nombre, casos, pregunta, pieza, testigo):
    """UNA afirmacion sobre toda la muestra: la pieza da lo que dice el testigo, la vuelta cuadra,
    y el motor la ELIGE (es la mas corta que encaja)."""
    fallos = []
    for a, b in casos:
        r = motor.aplicar(pregunta, {"a": a, "b": b}, SABER)
        if r["conclusion"] != "hecho" or r["pieza"]["id"] != pieza or r["valor"] != testigo(a, b) \
                or not r["resultado"]["vuelta_ok"]:
            fallos.append("%d,%d -> %s %s" % (a, b, r.get("pieza", {}).get("id"), r.get("valor")))
    comprobar("%s  (%d casos)" % (nombre, len(casos)), fallos[:3], [])


SABER = motor.cargar_conocimiento()
NUM = numeros(0, 1000)
DECENAS = [10, 20, 30, 40, 50, 60, 70, 80, 90]
NUEVES = [19, 29, 39, 49, 59, 69, 79, 89]

print("=" * 78)
print("LAS TECNICAS PARA IR MAS RAPIDO  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - EL MECANISMO: SALTAR UNA DECENA ESCRIBIENDO LA CIFRA")
    comprobar("A1 47 -> 57 y 57 -> 47", (motor.subir_una_decena(47, SABER), motor.bajar_una_decena(57, SABER)), (57, 47))
    comprobar("A2 la cifra nueve pasa a cero y sube la de al lado: 95 -> 105, 990 -> 1000",
              (motor.subir_una_decena(95, SABER), motor.subir_una_decena(990, SABER)), (105, 1000))
    comprobar("A3 a traves de un cero: 105 -> 95, 1000 -> 990",
              (motor.bajar_una_decena(105, SABER), motor.bajar_una_decena(1000, SABER)), (95, 990))
    comprobar("A4 sin decenas que quitar (7) o pasando de un millon (999995, N.4): no hay salto",
              (motor.bajar_una_decena(7, SABER), motor.subir_una_decena(999995, SABER)), (None, None))

    print("\nB - DE DIEZ EN DIEZ")
    recorrer("B1 a + 30, 40 ...: de diez en diez, bien y con la vuelta",
             [(a, b) for a in NUM for b in DECENAS if a + b <= 1000], "sumar", "sumar_de_diez_en_diez",
             lambda a, b: a + b)
    recorrer("B2 a - 30, 40 ...: de diez en diez hacia atras",
             [(a, b) for a in NUM for b in DECENAS if a >= b], "restar", "restar_de_diez_en_diez",
             lambda a, b: a - b)
    r = motor.aplicar("sumar", {"a": 47, "b": 30}, SABER)
    comprobar("B3 y dice los saltos: 47 + 30 -> 57, 67, 77", "57, 67, 77" in r["resultado"]["cuenta"], True)

    print("\nC - COMPENSAR")
    recorrer("C1 x9 + b: le doy uno al que acaba en nueve (en los dos ordenes)",
             [p for a in NUM for x in NUEVES for p in ((x, a), (a, x))
              if a != 0 and a + x <= 1000 and a not in DECENAS], "sumar", "sumar_compensando",
             lambda a, b: a + b)
    recorrer("C2 a - x9: quito la decena justa y devuelvo uno",
             [(a, x) for a in NUM for x in NUEVES if a > x], "restar", "restar_compensando",
             lambda a, b: a - b)
    r = motor.aplicar("sumar", {"a": 29, "b": 14}, SABER)
    comprobar("C3 29 + 14 = 43 y dice como: 30 + 13", (r["valor"], "30 + 13" in r["resultado"]["cuenta"]), (43, True))

    print("\nD - CASI DOBLES (un hecho derivado: necesita el doble de memoria)")
    r = motor.aplicar("sumar", {"a": 6, "b": 7}, SABER)
    fila = [c for c in r["candidatos"] if c["id"] == "sumar_casi_dobles"][0]
    comprobar("D1 con la memoria vacia no encaja: el doble no lo se", fila.get("descartado"),
              "el doble no lo se de memoria todavia")
    motor.aprender("sumas", SABER)
    casi = [(a, b) for a in range(10) for b in range(10) if a - b in (1, -1)]
    fallos = []
    for a, b in casi:
        r = motor.aplicar("sumar", {"a": a, "b": b, "sin_memoria": True}, SABER)
        if (r.get("pieza", {}).get("id"), r.get("valor")) != ("sumar_casi_dobles", a + b):
            fallos.append((a, b, r.get("pieza", {}).get("id")))
    comprobar("D2 sabiendo los dobles, las 18 casi dobles salen por casi dobles", fallos, [])
    r = motor.aplicar("sumar", {"a": 6, "b": 7, "sin_memoria": True}, SABER)
    comprobar("D3 y dice de que doble sale: 6 + 6 = 12, uno mas", "6 + 6 = 12" in r["resultado"]["cuenta"], True)
    r = motor.aplicar("sumar", {"a": 6, "b": 7}, SABER)
    comprobar("D4 pero si 6 + 7 ya se sabe, se recuerda (es mas corto)", r["pieza"]["id"], "recordar_suma")
    motor.olvidar_todo()

    print("\nE - DONDE NO ENCAJAN, SE DESCARTAN CON SU PORQUE")
    r = motor.aplicar("sumar", {"a": 47, "b": 5}, SABER)
    comprobar("E1 47 + 5: ni decenas justas ni acaba en nueve -> cuenta 5 con los dedos desde 47",
              (r["pieza"]["id"], r["valor"]), ("sumar_con_dedos", 52))
    desc = {c["id"]: c.get("descartado") for c in r["candidatos"]}
    comprobar("E2 con su porque", (desc["sumar_de_diez_en_diez"], desc["sumar_compensando"]),
              ("el segundo no son decenas justas (30, 40 ... 90)",
               "ninguno es de dos cifras acabado en nueve (19, 29 ... 89)"))
    r = motor.aplicar("sumar", {"a": 99, "b": 14}, SABER)
    # OBSOLETA POR MEJORA (P.7, 7 oct): antes era ("sumar_por_columnas", 113): la compensacion de P.4 no
    # encaja (99 no es de dos cifras acabado en nueve), pero ahora la MISMA SUMA de P.7 (NCETM 1.29) si:
    # 99 + 14 = 100 + 13.  Lo que se sigue afirmando: P.4 no encaja, y sale 113.
    comprobar("E3 99 + 14: la decena siguiente del 99 es 100, no es de dos cifras -> P.4 no; la misma suma (P.7)",
              ([c.get("descartado") for c in r["candidatos"] if c["id"] == "sumar_compensando"],
               r["pieza"]["id"], r["valor"]),
              (["ninguno es de dos cifras acabado en nueve (19, 29 ... 89)"], "sumar_misma_suma", 113))
    r = motor.aplicar("sumar", {"a": 29, "b": 0}, SABER)
    comprobar("E4 29 + 0: no hay nada que pasar de uno a otro",
              [c.get("descartado") for c in r["candidatos"] if c["id"] == "sumar_compensando"],
              ["uno es cero: no hay nada que pasar de uno a otro"])
    r = motor.aplicar("restar", {"a": 29, "b": 29}, SABER)
    comprobar("E5 29 - 29: no se puede quitar 30 de 29 -> otro metodo, y da 0",
              (r["pieza"]["id"] != "restar_compensando", r["valor"]), (True, 0))

    print("\nF - UN PROBLEMA LAS APROVECHA SIN SABER QUE EXISTEN")
    r = motor.aplicar("paso", {"tipo": "cambio", "antes": 47, "signo": "+", "n": 30}, SABER)
    comprobar("F1 tenia 47 y le dan 30: anadir, y calcula de diez en diez",
              (r["pieza"]["id"], r["resultado"]["pieza"]["id"], r["valor"]),
              ("anadir", "sumar_de_diez_en_diez", 77))
    r = motor.aplicar("paso", {"tipo": "cambio", "antes": 52, "signo": "-", "n": 29}, SABER)
    comprobar("F2 tenia 52 y se van 29: quitar, y calcula compensando",
              (r["pieza"]["id"], r["resultado"]["pieza"]["id"], r["valor"]),
              ("quitar", "restar_compensando", 23))
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
