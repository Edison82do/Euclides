# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.2: LAS TABLAS DEL 2, 5 Y 10; LA CONMUTATIVA; DOBLES Y MITADES (NCETM 2.3-2.5).
El plan y sus trampas: diario/2026-10-05-paso-M2-tablas.md
Python (a * b) solo aparece aqui como TESTIGO externo.
"""
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
TMP = tempfile.mkdtemp(prefix="tablas_")
RUTA = os.path.join(TMP, "hechos.txt")
os.environ["EUCLIDES_MEMORIA"] = RUTA      # memoria vacia
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
print("PASO M.2 - LAS TABLAS DEL 2, 5 Y 10  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - CADA PIEZA DONDE LE TOCA")
    comprobar("A1 0 x 8 y 8 x 1: sin calcular (NCETM 2.4)", (P(0, 8)[:2], P(8, 1)[:2]),
              ((0, "multiplicar_por_cero_o_uno"), (8, "multiplicar_por_cero_o_uno")))
    comprobar("A2 2 x 9 y 9 x 2: el doble de 9 (NCETM 2.5)", (P(2, 9)[:2], P(9, 2)[:2]),
              ((18, "multiplicar_con_dobles"), (18, "multiplicar_con_dobles")))
    v, p, r = P(5, 7)
    comprobar("A3 5 x 7: la otra lectura, 7 grupos de 5, con la tabla del 5", (v, p, r["resultado"]["pasos"][-1]),
              (35, "multiplicar_dando_la_vuelta", "35"))
    comprobar("A4 7 x 5: ya son grupos de 5, no hace falta dar la vuelta", P(7, 5)[:2], (35, "multiplicar_grupos_iguales"))
    comprobar("A5 3 x 4: ni 2, ni 5, ni 10 -> grupo a grupo", P(3, 4)[:2], (12, "multiplicar_grupos_iguales"))

    print("\nB - LAS TABLAS (NCETM 2.3 y 2.4)")
    for n in (2, 5, 10):
        t = motor.explicar_pregunta("tabla del %d" % n, SABER)
        esperado = ", ".join(str(n * k) for k in range(0, 11))
        comprobar("B tabla del %d: 0 ... %d, cada uno el anterior mas %d" % (n, 10 * n, n),
                  t.strip().splitlines()[-1], "RESULTADO: " + esperado)
    comprobar("B4 tabla del 7: todavia no (en M.2 era la del 3; llegan en orden)", motor.explicar_pregunta("tabla del 7", SABER).strip().splitlines()[-1],
              "RESULTADO: todavia_no")

    print("\nC - LA CONMUTATIVA EN EL = (E.0)")
    r = motor.decidir_igualdad("3 x 4 = 4 x 3", SABER)
    comprobar("C1 3 x 4 = 4 x 3: VERDADERO sin calcular", (r["valor"], r["pieza"]["id"]), ("verdadero", "igual_dando_la_vuelta"))
    r = motor.decidir_igualdad("3 x 4 = 3 + 4", SABER)
    comprobar("C2 3 x 4 = 3 + 4: FALSO (12 y 7)", r["valor"], "falso")
    r = motor.decidir_igualdad("6 x 5 = 30", SABER)
    comprobar("C3 6 x 5 = 30: VERDADERO", r["valor"], "verdadero")

    print("\nD - LA MITAD (lo contrario del doble)")
    comprobar("D1 mitad de 14 = 7, comprobada con el doble", (motor.mitad(14, SABER)["valor"], motor.mitad(14, SABER)["comprobacion"]), (7, True))
    comprobar("D2 mitad de 7: impar", motor.mitad(7, SABER)["conclusion"], "impar")
    comprobar("D3 mitad de 40: todavia no (eso es repartir, M.3)", motor.mitad(40, SABER)["conclusion"], "todavia_no")
    fallos = [n for n in range(0, 21) if (motor.mitad(n, SABER).get("valor") if n % 2 == 0 else "impar")
              != (n // 2 if n % 2 == 0 else motor.mitad(n, SABER)["conclusion"])]
    comprobar("D4 las mitades de 0 a 20", fallos, [])

    print("\nE - APRENDER LAS TABLAS (la memoria se gana)")
    a = motor.aprender("tablas", SABER)
    comprobar("E1 aprende las tablas ensenadas (2, 5, 10; desde M.4 tambien 4 y 8) en las dos lecturas, sin rechazar ninguna",
              (len(a["nuevos"]), a["rechazados"]),
              (len({(k, t) for t in motor.TABLAS_ENSENADAS for k in range(11)} | {(t, k) for t in motor.TABLAS_ENSENADAS for k in range(11)}), []))
    h = motor.cargar_memoria()["6 x 5"]
    comprobar("E2 6 x 5 = 30, comprobado con la otra lectura (5 grupos de 6)", (h["valor"], "5 grupos de 6" in h["comprobado"]), (30, True))
    comprobar("E3 6 x 5 ahora de memoria", P(6, 5)[:2], (30, "recordar_producto"))
    comprobar("E4 7 x 7 no esta en las tablas aprendidas: se calcula", P(7, 7)[1], "multiplicar_grupos_iguales")
    comprobar("E5 sin memoria, 6 x 5 se calcula", P(6, 5, sin_memoria=True)[1] != "recordar_producto", True)
    with open(RUTA, encoding="utf-8") as f:
        txt = f.read()
    with open(RUTA, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt.replace("6 x 5 = 30 |", "6 x 5 = 31 |"))
    v, p, r = P(6, 5)
    comprobar("E6 un recuerdo falso (6 x 5 = 31) no se usa: se calcula y da 30", (v, p != "recordar_producto"), (30, True))

    print("\nF - CONTRA EL TESTIGO")
    motor.olvidar_todo()
    fallos = [(a, b) for a in range(0, 11) for b in range(0, 11) if P(a, b)[0] != a * b]
    comprobar("F1 las 121 de 0 a 10 por 0 a 10, con todas las piezas", fallos[:3], [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
