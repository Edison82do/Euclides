# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 7.4 - LA RESTA CON LOS DEDOS (tomar el primero, ir bajando el segundo).

Lo que esta unidad tiene que dejar claro (la nota de Carlos, 4 oct 2026):
  - Se TOMA EL PRIMERO con los dedos (no el segundo: eso es la suma).
  - Se van BAJANDO tantos como el SEGUNDO, uno a uno: CONTAR HACIA ATRAS.
  - Los dedos que QUEDAN son el resultado.
  - Es el MECANISMO de "quitar" (unidad 5.4): los dedos que quedan son lo que queda.
  - No se pueden bajar mas dedos de los que hay (no hay resta negativa).
  - El PRIMERO no puede pasar de diez (son los dedos que hay).
  - Se VERIFICA por la vuelta: la suma deshace la resta, y esa suma la hace con su mecanismo (7.1).
  - Y es MECANICO: se dan tantos pasos como el segundo.  Nada de memoria ni calculadora.

LA PRUEBA DE HIERRO (F): TODAS las parejas (a, b) con a de 0 a 10 y b de 0 a a dan lo mismo por los
dedos que por la resta (unidad 5.4) -- y su vuelta SIEMPRE cuadra.  Si una sola falla, la unidad no
esta.
"""

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
import motor  # noqa: E402

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


def p(n):
    return PALABRA[n - 1] if n > 0 else "cero"


print("=" * 78)
print("UNIDAD 7.4 - LA RESTA CON LOS DEDOS")
print("=" * 78)

# ------------------------------------------------------------------ A: lo basico
print("\nA - LO BASICO (la nota de Carlos)")
r = motor.decidir_7_4_resta_dedos("9", "4", SABER)
comprobar("A1 conclusion", r["conclusion"], "se_puede")
comprobar("A2 quedan 5", r["quedan"], 5)
comprobar("A3 el resultado con palabras", r["expresion"], "nueve - cuatro = cinco")
comprobar("A4 con cifras", r["expresion_cifras"], "9 - 4 = 5")
comprobar("A5 se dan 4 pasos (uno por dedo)", r["pasos_dados"], 4)

r = motor.decidir_7_4_resta_dedos("cinco", "dos", SABER)
comprobar("A6 con palabras por los dos lados", r["expresion"], "cinco - dos = tres")

r = motor.decidir_7_4_resta_dedos("diez", "siete", SABER)
comprobar("A7 diez menos siete", r["quedan"], 3)

# ------------------------------------------------------------------ B: los errores
print("\nB - LO QUE NO SE PUEDE (y lo dice, no lo inventa)")
r = motor.decidir_7_4_resta_dedos("silla_1", "cuatro", SABER)
comprobar("B1 un objeto no es un numero", r["conclusion"], "no_es_un_numero")

r = motor.decidir_7_4_resta_dedos("45", "7", SABER)
comprobar("B2 el PRIMERO SI puede pasar de diez (lo cazo Carlos)", r["conclusion"], "se_puede")
comprobar("B2b 45 - 7 = 38", r["quedan"], 38)
comprobar("B2c los dedos van del 36 al 45 (la ventana)", r["ventana"], (36, 45))

r = motor.decidir_7_4_resta_dedos("45", "12", SABER)
comprobar("B2d lo que tiene que caber es EL SEGUNDO (el que se baja)", r["conclusion"],
          "no_caben_en_los_dedos")

r = motor.decidir_7_4_resta_dedos("12", "5", SABER)
comprobar("B2e el ejemplo de Carlos: 12 - 5, dedos del 3 al 12", r["ventana"], (3, 12))
comprobar("B2f y quedan 7", r["quedan"], 7)

r = motor.decidir_7_4_resta_dedos("4", "9", SABER)
comprobar("B3 no se pueden bajar mas dedos de los que hay", r["conclusion"], "no_hay_bastantes")

# ------------------------------------------------------------------ C: la mecanica
print("\nC - LA MECANICA (que de verdad se baje uno a uno)")
r = motor.decidir_7_4_resta_dedos("10", "3", SABER)
comprobar("C1 se bajan 3 dedos", [b["bajo"] for b in r["bajadas"]], [1, 2, 3])
comprobar("C2 y van quedando 9, 8, 7", [b["quedan"] for b in r["bajadas"]], [9, 8, 7])
comprobar("C3 empieza en el PRIMERO", r["valor_a"], 10)
comprobar("C4 y no en el segundo (eso seria la suma)", r["bajadas"][0]["quedan"], 9)

r = motor.decidir_7_4_resta_dedos("9", "9", SABER)
comprobar("C5 quitar todo deja cero", r["expresion"], "nueve - nueve = cero")
comprobar("C6 y da cero, no vacio", r["quedan"], 0)

# ------------------------------------------------------------------ D: la vuelta
print("\nD - LA VERIFICACION (la suma deshace la resta)")
r = motor.decidir_7_4_resta_dedos("9", "4", SABER)
comprobar("D1 la vuelta es el mecanismo de la 7.1", r["vuelta"]["conclusion"], "se_puede")
comprobar("D2 y da el numero de partida", r["vuelta"]["total_valor"], 9)
comprobar("D3 la verificacion sale SI", r["verificacion"], True)
comprobar("D4 y se escribe", r["verificacion_texto"], "cinco + cuatro = nueve")

def coleccion(n, base="o"):
    return ",".join("%s%d" % (base, i + 1) for i in range(n))


def esc(n):
    return motor.escena_cantidad(coleccion(n), SABER)


# ------------------------------------------------------------------ E: coherencia
print("\nE - COHERENCIA CON LO QUE YA SABIA (si no, hay dos verdades)")
malas_e = 0
for a in range(1, 11):
    for b in range(0, a + 1):
        rd = motor.decidir_7_4_resta_dedos(str(a), str(b), SABER)
        quitar = motor.decidir_5_4_quitar(esc(a), str(b), SABER)
        if str(rd["resta"]) != quitar["resultado"]:
            malas_e += 1
            print("    %d - %d: dedos=%s quitar=%s" % (a, b, rd["resta"], quitar["resultado"]))
comprobar("E1 los dedos y 'quitar' (5.4) dan lo MISMO en todas las parejas", malas_e, 0)

malas_e2 = 0
for a in range(1, 11):
    for b in range(0, a + 1):
        rd = motor.decidir_7_4_resta_dedos(str(a), str(b), SABER)
        rn = motor.decidir_5_4_restar_numeros(str(a), str(b), SABER)
        if rd["quedan"] != rn.get("resultado_valor"):
            malas_e2 += 1
comprobar("E2 y con restar_numeros (5.5) tambien", malas_e2, 0)

# ------------------------------------------------------------------ F: LA PRUEBA DE HIERRO
print("\nF - LA PRUEBA DE HIERRO (todas las parejas de los dedos)")
probadas = 0
malas = 0
sin_vuelta = 0
for a in range(0, 101):
    for b in range(0, min(a, 10) + 1):
        r = motor.decidir_7_4_resta_dedos(str(a), str(b), SABER)
        probadas += 1
        if r["conclusion"] != "se_puede":
            malas += 1
            print("    %d - %d: conclusion=%s" % (a, b, r["conclusion"]))
            continue
        if r["dedos_levantados"] > 10:
            malas += 1
            print("    %d - %d: %d dedos levantados (son 10)" % (a, b, r["dedos_levantados"]))
        elif r["ventana"][1] != a:
            malas += 1
            print("    %d - %d: la ventana no acaba en el minuendo" % (a, b))
        elif b > 0 and r["bajadas"][-1]["quedan"] != a - b:
            malas += 1
            print("    %d - %d: las bajadas no llegan a %d" % (a, b, a - b))
        elif not r["verificacion"]:
            sin_vuelta += 1
            print("    %d - %d: la vuelta no cuadra" % (a, b))
comprobar("F1 las %d parejas dan lo mismo por los dedos que restando" % probadas, malas, 0)
comprobar("F2 y son 1056 (a de 0 a 100, b de 0 a min(a, 10))", probadas, 1056)
comprobar("F3 ninguna se queda sin poder comprobarse por la vuelta", sin_vuelta, 0)

print("\n" + "=" * 78)
print("UNIDAD 7.4: %d/%d correctos" % (BIEN, BIEN + MAL))
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
print("=" * 78)
sys.exit(1 if MAL else 0)
