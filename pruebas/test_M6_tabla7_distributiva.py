# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.6: LA TABLA DEL 7 Y LA DISTRIBUTIVA (NCETM 2.9, 2.10; 3.OA.B.5, 3.OA.C.7).
El plan y sus trampas: diario/2026-10-06-paso-M6-tabla-7-distributiva.md
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
TMP = tempfile.mkdtemp(prefix="m6_")
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


def P(a, b, **k):
    s = {"a": a, "b": b}
    s.update(k)
    r = motor.aplicar("multiplicar", s, SABER)
    return r.get("valor"), r.get("pieza", {}).get("id"), r


print("=" * 78)
print("PASO M.6 - LA TABLA DEL 7 Y LA DISTRIBUTIVA  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LA TABLA DEL 7 (7 = 5 + 2)")
    t = motor.explicar_pregunta("tabla del 7", SABER)
    comprobar("A1 tabla del 7: 0 ... 70, cada fila 5 x k + 2 x k",
              (t.strip().splitlines()[-1], "8 x 7 =  8 x 5 +  8 x 2 = 40 + 16 = 56" in t),
              ("RESULTADO: " + ", ".join(str(7 * k) for k in range(11)), True))
    comprobar("A2 tabla del 11: todavia no (NCETM 2.11, 4.o)",
              motor.explicar_pregunta("tabla del 11", SABER).strip().splitlines()[-1], "RESULTADO: todavia_no")

    print("\nB - LA DISTRIBUTIVA: PARTIR UN FACTOR (solo con hechos que ya se saben)")
    comprobar("B1 sin memoria no se puede partir: 8 x 7 se calcula de otra manera", P(8, 7)[1] != "multiplicar_partiendo", True)
    a = motor.aprender("tablas", SABER)
    comprobar("B2 aprender: tablas -> todas hasta 10 x 10 (3.OA.C.7), sin rechazar ninguna", a["rechazados"], [])
    h = motor.cargar_memoria()
    faltan = [(x, y) for x in range(0, 11) for y in range(0, 11)
              if "%d x %d" % (x, y) not in h and not (x in (0, 1) and y in (0, 1))]
    comprobar("B3 en la memoria estan todos los productos hasta 10 x 10 (menos 0/1 x 0/1, que salen sin calcular)",
              faltan, [])
    comprobar("B4 7 x 7 se aprendio PARTIENDO (7 = 5 + 2)", h["7 x 7"]["como"], "partiendo (M.6)")
    r = motor.aplicar("multiplicar", {"a": 8, "b": 7, "sin_memoria": True}, SABER)
    comprobar("B5 8 x 7 sin recordarlo pero partiendo: 8 x 5 + 8 x 2 = 40 + 16 (el ejemplo de 3.OA.B.5)",
              (r["valor"], r["pieza"]["id"] in ("multiplicar_partiendo", "multiplicar_doblando")), (56, True))
    v, p, r = P(12, 6)
    comprobar("B6 MAS ALLA de las tablas: 12 x 6 = 10 x 6 + 2 x 6 = 72", (v, p, "60 + 12 = 72" in r["resultado"]["cuenta"]),
              (72, "multiplicar_partiendo", True))
    fallos = [(x, y) for x in range(11, 21) for y in range(0, 11) if P(x, y)[0] != x * y]
    comprobar("B7 de 11 a 20 por 0 a 10 contra el testigo", fallos[:3], [])

    print("\nC - LOS PATRONES (NCETM 2.9)")
    t = motor.explicar_pregunta("7 x 9", SABER)
    comprobar("C1 impar x impar -> impar", "impar x impar -> el producto es IMPAR" in t, True)
    t = motor.explicar_pregunta("6 x 7", SABER)
    comprobar("C2 par x impar -> par", "par x impar -> el producto es PAR" in t, True)
    t = motor.explicar_pregunta("6 x 6", SABER)
    comprobar("C3 6 x 6: NUMERO CUADRADO", "36 es un NUMERO CUADRADO" in t, True)
    comprobar("C4 la division no es conmutativa: 12 : 3 = 3 : 12 no es verdad",
              motor.decidir_igualdad("12 : 3 = 3 : 12", SABER).get("valor") != "verdadero", True)

    print("\nD - DIVISIBLE ENTRE CUALQUIERA (dividiendo con lo que se)")
    comprobar("D1 49 entre 7: si; 50 entre 7: no", (motor.decidir_divisible(49, 7, SABER)["valor"],
                                                     motor.decidir_divisible(50, 7, SABER)["valor"]), (True, False))
    fallos = [(n, d) for n in range(0, 101) for d in (5, 7, 10) if motor.decidir_divisible(n, d, SABER)["valor"] != (n % d == 0)]
    comprobar("D2 de 0 a 100 entre 5, 7 y 10 contra el testigo", fallos[:3], [])

    print("\nE - TODO 0..10 x 0..10 CONTRA EL TESTIGO")
    fallos = [(x, y) for x in range(0, 11) for y in range(0, 11) if P(x, y)[0] != x * y]
    comprobar("E1 las 121", fallos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
