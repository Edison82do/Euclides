# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 7.1 - EL METODO DE LOS DEDOS (sumar contando hacia adelante).

Lo que esta unidad tiene que dejar claro:
  - Se ANOTA el primero (la pizarra / memoria de trabajo).
  - Se cogen con los dedos tantos como el SEGUNDO.
  - Se cuenta HACIA ADELANTE desde el primero, un paso por dedo.
  - El ULTIMO numero dicho es el total (y no tiene que caber en los dedos).
  - El segundo no puede pasar de diez (no hay mas dedos).
  - Y es MECANICO: nada de memoria ni de calculadora (decision de Carlos, 4 oct 2026).

LA PRUEBA DE HIERRO (F): las 100 parejas de un digito con un digito dan lo MISMO por los dedos
que por la suma (unidad 5.3).  Dos caminos, un solo resultado.
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
print("UNIDAD 7.1 - EL METODO DE LOS DEDOS")
print("=" * 78)

# --------------------------------------------------------- A) el metodo, paso a paso
print("\nA) EL METODO CON 8 + 5 (el caso de Carlos)")
r = motor.decidir_7_1_dedos("8", "5", SABER)
comprobar("A1 concluye 'se_puede'", r["conclusion"], "se_puede")
comprobar("A2 el PRIMERO se anota (la pizarra)", r["anotado"], "ocho")
comprobar("A3 se levantan 5 dedos (los del SEGUNDO)", r["valor_b"], 5)
comprobar("A4 hay 5 pasos, uno por dedo", len(r["los_pasos"]), 5)
comprobar("A5 los pasos dicen 9,10,11,12,13",
          [x["palabra"] for x in r["los_pasos"]],
          ["nueve", "diez", "once", "doce", "trece"])
comprobar("A6 y van quedando dedos: 4,3,2,1,0",
          [x["quedan"] for x in r["los_pasos"]], [4, 3, 2, 1, 0])
comprobar("A7 el total es el ULTIMO numero dicho", r["total"], "trece")
comprobar("A8 el total NO cabe en los dedos (y no importa)", r["total_valor"] > r["dedos"], True)
comprobar("A9 la expresion en cifras", r["expresion_cifras"], "8 + 5 = trece")

# --------------------------------------------------------- B) los bordes
print("\nB) LOS BORDES")
r = motor.decidir_7_1_dedos("5", "0", SABER)
comprobar("B1 sumar CERO: no se levanta ningun dedo", len(r["los_pasos"]), 0)
comprobar("B2 y el total es el primero", r["total"], "cinco")
r = motor.decidir_7_1_dedos("0", "3", SABER)
comprobar("B3 cero mas tres: se cuenta desde el CERO", r["total"], "tres")
comprobar("B4 y son 3 pasos", len(r["los_pasos"]), 3)
r = motor.decidir_7_1_dedos("0", "0", SABER)
comprobar("B5 cero mas cero es cero", r["total"], "cero")
r = motor.decidir_7_1_dedos("9", "9", SABER)
comprobar("B6 nueve mas nueve son dieciocho (con 9 dedos, no 10)", r["total"], "dieciocho")
comprobar("B7 y son 9 pasos", len(r["los_pasos"]), 9)
r = motor.decidir_7_1_dedos("cuarenta y siete", "tres", SABER)
comprobar("B8 el PRIMERO puede ser grande: 47 + 3 = 50", r["total"], "cincuenta")
comprobar("B9 y solo se dan 3 pasos (no 50)", len(r["los_pasos"]), 3)

# --------------------------------------------------------- C) las condiciones
print("\nC) LAS CONDICIONES DE APLICACION")
r = motor.decidir_7_1_dedos("ocho", "doce", SABER)
comprobar("C1 el segundo pasa de diez -> no_caben_en_los_dedos",
          r["conclusion"], "no_caben_en_los_dedos")
r = motor.decidir_7_1_dedos("ocho", "once", SABER)
comprobar("C2 once dedos tampoco caben", r["conclusion"], "no_caben_en_los_dedos")
r = motor.decidir_7_1_dedos("ocho", "diez", SABER)
comprobar("C3 diez dedos SI caben (justo)", r["conclusion"], "se_puede")
comprobar("C4 y el total es dieciocho", r["total"], "dieciocho")
# UNIDAD 6.7: el techo subio de cien a MIL.  (Antes este caso era 95+9=104.)
r = motor.decidir_7_1_dedos("novecientos noventa y cinco", "nueve", SABER)
comprobar("C5 el total pasa de MIL -> no_alcanza", r["conclusion"], "no_alcanza")
r = motor.decidir_7_1_dedos("noventa y cinco", "nueve", SABER)
comprobar("C5b (MEJORA 6.7): 95+9=104 YA se puede, porque el techo es mil",
          r["conclusion"], "se_puede")
r = motor.decidir_7_1_dedos("ocho", "manzana", SABER)
comprobar("C6 'manzana' no es un numero", r["conclusion"], "no_es_un_numero")

# --------------------------------------------------------- D) el ahorro de pasos
print("\nD) POR QUE ES MEJOR QUE CONTAR TODO (lo que ensena el metodo)")
r = motor.decidir_7_1_dedos("8", "5", SABER)
comprobar("D1 contando hacia adelante: 5 pasos", r["pasos_dados"], 5)
comprobar("D2 contando todo: 13 pasos", r["pasos_contando_todo"], 13)
comprobar("D3 el ahorro son 8 pasos", r["pasos_ahorrados"], 8)
r = motor.decidir_7_1_dedos("1", "1", SABER)
comprobar("D4 con 1 + 1 el ahorro es 1 paso (poco)", r["pasos_ahorrados"], 1)
r = motor.decidir_7_1_dedos("9", "9", SABER)
comprobar("D5 con 9 + 9 el ahorro es 9 pasos (mucho)", r["pasos_ahorrados"], 9)

# --------------------------------------------------------- E) la verificacion
print("\nE) LA COMPROBACION (la vuelta)")
r = motor.decidir_7_1_dedos("8", "5", SABER)
comprobar("E1 la vuelta se escribe", r["expresion_inversa"], "trece - cinco = ocho")
comprobar("E2 y cuadra", r["verificacion"], True)
comprobar("E3 y la suma cuadra por dentro", r["la_suma_cuadra"], True)

# ==================================================== LA PRUEBA DE HIERRO (F)
print("\n" + "=" * 78)
print("F) PRUEBA DE HIERRO: las 100 parejas dan lo mismo por los DEDOS que por la SUMA")
print("=" * 78)
malas = 0
probadas = 0
sin_suma = 0
for a in range(0, 10):
    for b in range(0, 10):
        dedos = motor.decidir_7_1_dedos(str(a), str(b), SABER)
        if dedos["conclusion"] != "se_puede":
            malas += 1
            print("    %d + %d: los dedos dicen %s" % (a, b, dedos["conclusion"]))
            continue
        suma = motor.decidir_5_3_sumar_numeros(str(a), str(b), SABER)
        if suma["conclusion"] != "suma":
            sin_suma += 1
            continue
        probadas += 1
        if dedos["total_valor"] != a + b:
            malas += 1
            print("    %d + %d: los dedos dicen %d" % (a, b, dedos["total_valor"]))
        elif dedos["total"] != suma["suma"]:
            malas += 1
            print("    %d + %d: los dedos dicen '%s' y la suma dice '%s'"
                  % (a, b, dedos["total"], suma["suma"]))
        elif not dedos["verificacion"]:
            malas += 1
            print("    %d + %d: no cuadra la vuelta" % (a, b))
comprobar("F1 las %d parejas dan el MISMO resultado por los dedos y por la suma" % probadas, malas, 0)
comprobar("F2 y son 100 (a y b de 0 a 9)", probadas, 100)
comprobar("F3 ninguna se quedo sin poder comprobarse con la suma", sin_suma, 0)

print("\n" + "=" * 78)
print("UNIDAD 7.1: %d/%d correctos" % (BIEN, BIEN + MAL))
print("=" * 78)
sys.exit(1 if MAL else 0)
