# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 7.5 - RESTAR POR COLUMNAS (y el intercambio de una decena).

Lo que esta unidad tiene que dejar claro:
  - Se resta columna a columna, empezando por la derecha (como en la suma, 7.3).
  - SI LAS UNIDADES DE ARRIBA NO LLEGAN, NO SE DA LA VUELTA A LA RESTA.  Ese es EL error mas
    comun de la resta, y el que hay que matar (5 - 2 = 3 en vez de cambiando).
  - Lo que se hace es CAMBIAR una decena por diez unidades.  NO es un prestamo: no se devuelve
    nada.  Y el numero sigue valiendo lo mismo (60 + 12 = 72).
  - Al cambiarla, la columna de las decenas BAJA de 7 a 6.  Si se olvida, sale diez de mas.
  - Cada resta de columna se hace con EL MECANISMO (7.4), no de memoria.
  - Se verifica por la vuelta: la suma deshace la resta (con las columnas de la 7.3).
  - Y las DOS formas (con y sin intercambio) son la misma cosa salvo un paso.

LA PRUEBA DE HIERRO (F): TODAS las parejas (a, b) con a de 0 a 100 y b de 0 a a dan lo mismo que
la resta (5.4), y su vuelta SIEMPRE cuadra.  Si una sola falla, la unidad no esta.
"""

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
import motor  # noqa: E402
import _hierro  # noqa: E402

# Las parejas (a, b) con b <= a <= 100: TODAS con --hierro; fronteras + muestra fija, si no.
PAREJAS = _hierro.parejas(100, lambda a, b: b <= a, extra=[(100, 1), (100, 99), (10, 1), (72, 45), (43, 17)])

BIEN = 0
MAL = 0


def comprobar(nombre, obtenido, esperado):
    global BIEN, MAL
    if obtenido == esperado:
        BIEN += 1
        print("  bien    %s" % nombre)
    else:
        MAL += 1
        print("  FALLA   %s\n          esperado=%r  obtenido=%r" % (nombre, esperado, obtenido))


SABER = motor.cargar_conocimiento()
PALABRA = SABER["secuencia_de_conteo"]["palabras"]

print("=" * 78)
print("UNIDAD 7.5 - RESTAR POR COLUMNAS")
print("=" * 78)

# ------------------------------------------------------------------ A: lo basico
print("\nA - LO BASICO")
r = motor.decidir_7_5_columnas("72", "45", SABER)
comprobar("A1 conclusion", r["conclusion"], "se_puede")
comprobar("A2 hay intercambio", r["hay_intercambio"], True)
comprobar("A3 7 decenas y 2 unidades", (r["dec_a"], r["uni_a"]), (7, 2))
comprobar("A4 tras cambiarla: 6 decenas y 12 unidades", (r["dec_a_despues"], r["uni_a_despues"]),
          (6, 12))
comprobar("A5 el cambio no cambia el numero", r["intercambio_vale_igual"], True)
comprobar("A6 la resta de las unidades", r["resta_unidades"], "12 - 5 = 7")
comprobar("A7 la resta de las decenas (con la decena ya bajada)", r["resta_decenas"], "6 - 4 = 2")
comprobar("A8 el resultado", r["expresion"], "setenta y dos - cuarenta y cinco = veintisiete")
comprobar("A9 con cifras", r["expresion_cifras"], "72 - 45 = 27")
comprobar("A10 y la vuelta cuadra", r["verificacion"], True)

r = motor.decidir_7_5_columnas("58", "27", SABER)
comprobar("A11 sin intercambio: no hace falta cambiar nada", r["hay_intercambio"], False)
comprobar("A12 y sale 31", r["expresion"], "cincuenta y ocho - veintisiete = treinta y uno")

r = motor.decidir_7_5_columnas("40", "18", SABER)
comprobar("A13 40 - 18 = 22", r["expresion"], "cuarenta - dieciocho = veintidos")

# ------------------------------------------------------------------ B: los errores
print("\nB - LO QUE NO SE PUEDE (y lo dice, no lo inventa)")
r = motor.decidir_7_5_columnas("silla_1", "cuatro", SABER)
comprobar("B1 un objeto no es un numero", r["conclusion"], "no_es_un_numero")

r = motor.decidir_7_5_columnas("45", "72", SABER)
comprobar("B2 quitar mas de lo que hay: no hay resta negativa", r["conclusion"], "no_hay_bastantes")

r = motor.decidir_7_5_columnas("150", "40", SABER)
# ANTES (7.5): 150 - 40 -> no_alcanza (la resta por columnas llegaba a cien).
# MEJORA 7.6 (5 oct 2026): con la columna de las CENTENAS ya se puede: 110.
comprobar("B3 (MEJORA 7.6) 150 - 40 ya se resta: 110", r.get("resta"), 110)
r = motor.decidir_7_5_columnas("1500", "40", SABER)
comprobar("B3b (7.6) pasar de MIL: no alcanza", r["conclusion"], "no_alcanza")

# ------------------------------------------------------------------ C: LOS TRES ERRORES TIPICOS
print("\nC - LOS TRES ERRORES TIPICOS DE LA RESTA POR COLUMNAS (los documentados)")
# 43 - 17: el clasico.  34 = dar la vuelta a la resta; 36 = olvidar bajar la decena.
r = motor.decidir_7_5_columnas("43", "17", SABER)
comprobar("C1 43 - 17 no da 34 (no se da la vuelta a la resta)", r["resta"], 26)
comprobar("C2 43 - 17 no da 36 (la decena BAJA de 4 a 3)", r["dec_a_despues"], 3)
comprobar("C3 43 - 17 = 26", r["expresion_cifras"], "43 - 17 = 26")

r = motor.decidir_7_5_columnas("52", "27", SABER)
comprobar("C4 52 - 27 = 25", r["expresion_cifras"], "52 - 27 = 25")

r = motor.decidir_7_5_columnas("72", "45", SABER)
comprobar("C5 y no se queda en 5 - 2 = 3 (el error de dar la vuelta)",
          "5 - 2" not in r["resta_unidades"], True)

# ------------------------------------------------------------------ D: la vuelta
print("\nD - LA VERIFICACION (la suma deshace la resta)")
r = motor.decidir_7_5_columnas("72", "45", SABER)
comprobar("D1 la vuelta usa las columnas de la 7.3", r["vuelta"]["conclusion"], "se_puede")
comprobar("D2 y da el numero de partida", r["vuelta"]["total_valor"], 72)
comprobar("D3 la verificacion sale SI", r["verificacion"], True)

# ------------------------------------------------------------------ E: coherencia
print("\nE - COHERENCIA CON LO QUE YA SABIA (si no, hay dos verdades)")
malas_e = 0
for a, b in PAREJAS:
    if a >= 1:
        rc = motor.decidir_7_5_columnas(str(a), str(b), SABER)
        rn = motor.decidir_5_4_restar_numeros(str(a), str(b), SABER)
        if rc["resta"] != rn.get("resultado_valor"):
            malas_e += 1
            if malas_e < 4:
                print("    %d - %d: columnas=%s restar_numeros=%s"
                      % (a, b, rc["resta"], rn.get("resultado_valor")))
comprobar("E1 las columnas y restar_numeros (5.4) dan lo MISMO (%d parejas)" % len(PAREJAS), malas_e, 0)

malas_e2 = 0
for a in range(1, 11):
    for b in range(0, a + 1):
        rc = motor.decidir_7_5_columnas(str(a), str(b), SABER)
        rd = motor.decidir_7_4_resta_dedos(str(a), str(b), SABER)
        if rc["resta"] != rd["quedan"]:
            malas_e2 += 1
comprobar("E2 y con los dedos (7.4) tambien, cuando caben", malas_e2, 0)

# ------------------------------------------------------------------ F: LA PRUEBA DE HIERRO
print("\nF - LA PRUEBA DE HIERRO (parejas hasta cien: %s)" % _hierro.modo())
probadas = 0
malas = 0
sin_vuelta = 0
sin_intercambio = 0
for a, b in PAREJAS:
    if True:
        r = motor.decidir_7_5_columnas(str(a), str(b), SABER)
        probadas += 1
        if r["conclusion"] != "se_puede":
            malas += 1
            if malas < 4:
                print("    %d - %d: conclusion=%s" % (a, b, r["conclusion"]))
            continue
        if r["resta"] != a - b:
            malas += 1
            if malas < 4:
                print("    %d - %d: resta=%s (deberia %d)" % (a, b, r["resta"], a - b))
        elif not r["intercambio_vale_igual"]:
            malas += 1
        elif not r["verificacion"]:
            sin_vuelta += 1
            if sin_vuelta < 4:
                print("    %d - %d: la vuelta no cuadra" % (a, b))
        if r["hay_intercambio"]:
            sin_intercambio += 1
comprobar("F1 las %d parejas dan lo mismo por columnas que restando" % probadas, malas, 0)
comprobar("F2 y se recorrieron todas las previstas (%s)" % _hierro.modo(), probadas, len(PAREJAS))
comprobar("F3 ninguna se queda sin poder comprobarse por la vuelta", sin_vuelta, 0)
comprobar("F4 y hay intercambio en muchisimas (no se esta esquivando)",
          sin_intercambio > len(PAREJAS) // 3, True)

print("\n" + "=" * 78)
print("UNIDAD 7.5: %d/%d correctos" % (BIEN, BIEN + MAL))
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
print("=" * 78)
sys.exit(1 if MAL else 0)
