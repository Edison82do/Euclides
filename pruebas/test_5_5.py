# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 5.5 - LA DIFERENCIA (la tercera estructura de la resta).

Lo que esta unidad tiene que dejar claro:
  - La diferencia es el HUECO entre dos cantidades.
  - AQUI NO SE QUITA NADA: los dos montones siguen enteros.
  - El MISMO numero responde a 'cuantos mas' y a 'cuantos menos'.
  - Se escribe de DOS maneras: restando y contando hacia adelante.
  - Si son iguales, la diferencia es CERO (y el cero es una cantidad).
  - No hay 'todo' (a diferencia de quitar y de partir).

LA PRUEBA DE HIERRO (K): LAS TRES ESTRUCTURAS DE LA RESTA DAN EL MISMO NUMERO.
  quitar (5.4):     de 5 se van 2  -> quedan 3
  partir (5.1):     5 se parte en 2 y 3
  diferencia (5.5): el hueco entre 5 y 2 es 3
  Las tres son 5 - 2 = 3, y las tres historias son distintas.
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


def coleccion(n, base="o"):
    return ",".join("%s%d" % (base, i + 1) for i in range(n))


SABER = motor.cargar_conocimiento()


def esc(n):
    return motor.escena_cantidad(coleccion(n), SABER)


def palabra(n):
    return motor._palabra_de(n, SABER["secuencia_de_conteo"]["palabras"])


print("=" * 78)
print("UNIDAD 5.5 - LA DIFERENCIA")
print("=" * 78)

# ---------------------------------------------------------------- A) lo basico
print("\nA) LO BASICO")
r = motor.decidir_5_5_diferencia(esc(5), esc(3), SABER)
comprobar("A1 concluye 'hay_diferencia'", r["conclusion"], "hay_diferencia")
comprobar("A2 la diferencia es 2", r["diferencia_valor"], 2)
comprobar("A3 y en palabra: dos", r["diferencia"], "dos")
comprobar("A4 se escribe 5 - 3 = 2", r["expresion"], "5 - 3 = 2")
comprobar("A5 la primera tiene mas", r["tiene_mas"], "la primera")
comprobar("A6 quedan 2 SIN PAREJA de la primera", r["sobra_primera"], ["o4", "o5"])
comprobar("A7 y ninguna de la segunda", r["sobra_segunda"], [])
comprobar("A8 hay 3 emparejados", len(r["emparejadas"]), 3)

# El mismo numero desde los dos lados
r = motor.decidir_5_5_diferencia(esc(3), esc(5), SABER)
comprobar("A9 A6 el orden no cambia la diferencia", r["diferencia_valor"], 2)
comprobar("A10 ahora la segunda tiene mas", r["tiene_mas"], "la segunda")
comprobar("A11 y sin embargo el numero es el MISMO", r["cuantos_mas"], "dos")

# ------------------------------------------------------- B) no se quita nada
print("\nB) AQUI NO SE QUITA NADA (es la clave de la diferencia)")
r = motor.decidir_5_5_diferencia(esc(5), esc(3), SABER)
comprobar("B1 la primera sigue con sus CINCO objetos", len(r["primera"]), 5)
comprobar("B2 la segunda sigue con sus TRES objetos", len(r["segunda"]), 3)
comprobar("B3 no hay ninguna clave de 'lo que queda'", "resultado" in r, False)
comprobar("B4 los emparejados siguen todos enteros", len(r["emparejadas"]) + len(r["sobra_primera"]), 5)

# ------------------------------------------------------------- C) el cero
print("\nC) SI SON IGUALES, LA DIFERENCIA ES CERO")
r = motor.decidir_5_5_diferencia(esc(3), esc(3), SABER)
comprobar("C1 concluye 'tantos_como'", r["conclusion"], "tantos_como")
comprobar("C2 la diferencia es cero", r["diferencia_valor"], 0)
comprobar("C3 y en palabra: cero", r["diferencia"], "cero")
r = motor.decidir_5_5_diferencia(esc(0), esc(0), SABER)
comprobar("C4 dos vacias: la diferencia es cero", r["diferencia_valor"], 0)
r = motor.decidir_5_5_diferencia(esc(0), esc(4), SABER)
comprobar("C5 nada contra cuatro: la diferencia es cuatro", r["diferencia_valor"], 4)

# ------------------------------------------------------- D) el techo
print("\nD) EL TECHO: NO SE PUEDE CONTAR MAS DE MIL (unidad 6.7)")
r = motor.decidir_5_5_diferencia(esc(12), esc(3), SABER)
# UNIDAD 6.1: doce objetos YA se cuentan.
# UNIDAD 6.7 (LA CENTENA): el limite subio de cien a MIL.  Antes esta prueba decia
# 101 y esperaba no_alcanza; ahora 101 SI se puede, y el techo esta en 1000.
r = motor.decidir_5_5_diferencia(esc(10001), esc(3), SABER)
comprobar("D1 TRAMPA: mas de diez mil objetos (N.3): lo dice", r["conclusion"], "no_alcanza")
r = motor.decidir_5_5_diferencia(esc(3), esc(10001), SABER)
comprobar("D2 TRAMPA: y tambien si es la segunda", r["conclusion"], "no_alcanza")
r = motor.decidir_5_5_diferencia(esc(12), esc(3), SABER)
comprobar("D2b (MEJORA 6.1): doce contra tres ya SI: la diferencia es 9",
          r["diferencia_valor"], 9)
r = motor.decidir_5_5_diferencia(esc(10), esc(3), SABER)
comprobar("D3 diez si (es la ultima palabra): 10 - 3 = 7", r["expresion"], "diez - 3 = 7")

# --------------------------------------------------- E) la diferencia de numeros
print("\nE) LA DIFERENCIA ENTRE DOS NUMEROS")
r = motor.decidir_5_5_diferencia_numeros("5", "3", SABER)
comprobar("E1 5 - 3 = 2", r["expresion"], "5 - 3 = 2")
r = motor.decidir_5_5_diferencia_numeros("3", "5", SABER)
comprobar("E2 al reves da el MISMO numero", r["diferencia_valor"], 2)
r = motor.decidir_5_5_diferencia_numeros("nueve", "cuatro", SABER)
comprobar("E3 las palabras valen: 9 - 4 = 5", r["expresion"], "9 - 4 = 5")
r = motor.decidir_5_5_diferencia_numeros("4", "4", SABER)
comprobar("E4 iguales: cero", r["diferencia_valor"], 0)
r = motor.decidir_5_5_diferencia_numeros("5", "manzana", SABER)
comprobar("E5 un objeto no es un numero", r["conclusion"], "no_es_un_numero")

# ------------------------------------------------------------- F) robustez
print("\nF) ROBUSTEZ")
r = motor.decidir_5_5_diferencia(esc(0), esc(0), SABER)
comprobar("F1 dos colecciones vacias no revientan", r["conclusion"], "tantos_como")
r = motor.decidir_5_5_diferencia(esc(1), esc(0), SABER)
comprobar("F2 uno contra nada: la diferencia es uno", r["diferencia_valor"], 1)

# ------------------------------------------- G) cuadra con la unidad 4.1
print("\nG) LA DIFERENCIA Y EL COMPARAR DICEN LO MISMO (unidad 4.1)")
# OJO: las conclusiones se llaman distinto A PROPOSITO.  4.1 dice la PALABRA (mas/menos/
# tantos_como); 5.5 dice el NUMERO.  Lo que tiene que cuadrar es el SENTIDO.
malas = 0
for a in range(0, 8):
    for b in range(0, 8):
        comp = motor.decidir_4_1_comparar(esc(a), esc(b), SABER)
        dif = motor.decidir_5_5_diferencia(esc(a), esc(b), SABER)
        sentido_comp = comp["conclusion"]          # mas / menos / tantos_como
        if a == b:
            sentido_dif = "tantos_como"
        elif a > b:
            sentido_dif = "mas"
        else:
            sentido_dif = "menos"
        if sentido_comp != sentido_dif or dif["diferencia_valor"] != abs(a - b):
            malas += 1
            print("    %d vs %d: comparar dice %s, la cuenta dice %d y la diferencia %d"
                  % (a, b, sentido_comp, abs(a - b), dif["diferencia_valor"]))
comprobar("G1 las 64 parejas (0..7) coinciden en quien tiene mas Y en cuanto", malas, 0)

# ==================================================== LA PRUEBA DE HIERRO (K)
print("\n" + "=" * 78)
print("K) PRUEBA DE HIERRO: LAS TRES ESTRUCTURAS DE LA RESTA DAN EL MISMO NUMERO")
print("   quitar (5.4)  |  partir (5.1)  |  diferencia (5.5)")
print("=" * 78)
malas = 0
probadas = 0
for m in range(1, 11):
    for s in range(0, m + 1):
        # 1) QUITAR: de m se van s -> quedan m - s
        q = motor.decidir_5_4_quitar(esc(m), palabra(s), SABER)
        if q["conclusion"] != "quedan":
            malas += 1
            print("    quitar %d/%d: %s" % (m, s, q["conclusion"]))
            continue
        r_q = motor._valor_de_cantidad(q["resultado"], SABER)
        # 2) DIFERENCIA: el hueco entre m y s -> m - s
        d = motor.decidir_5_5_diferencia(esc(m), esc(s), SABER)
        if d["conclusion"] == "no_alcanza":
            malas += 1
            print("    diferencia %d/%d: no_alcanza" % (m, s))
            continue
        r_d = d["diferencia_valor"]
        # 3) PARTIR: m se parte en dos, y una de las maneras tiene que ser (s, m-s)
        p = motor.decidir_5_1_descomponer(esc(m), SABER)
        pareja = (min(s, m - s), max(s, m - s))
        if pareja not in p["parejas"]:
            malas += 1
            print("    partir %d: no esta la pareja %s (tiene %s)" % (m, pareja, p["parejas"]))
            continue
        probadas += 1
        if not (r_q == r_d == (m - s)):
            malas += 1
            print("    NO CUADRAN las tres: m=%d s=%d -> quitar=%s diferencia=%s esperado=%d"
                  % (m, s, r_q, r_d, m - s))
comprobar("K1 las %d parejas dan el MISMO numero por las TRES estructuras" % probadas, malas, 0)
comprobar("K2 y son 65 (m de 1 a 10, s de 0 a m)", probadas, 65)

# Y la otra cara: la MISMA expresion 'm - s = r' con tres historias distintas.
print("\nL) LA MISMA EXPRESION, TRES HISTORIAS (con 5 y 2)")
q = motor.decidir_5_4_quitar(esc(5), "dos", SABER)
d = motor.decidir_5_5_diferencia(esc(5), esc(2), SABER)
p = motor.decidir_5_1_descomponer(esc(5), SABER)
comprobar("L1 quitar dice 5 - 2 = 3", q["expresion"], "5 - 2 = 3")
comprobar("L2 diferencia dice 5 - 2 = 3", d["expresion"], "5 - 2 = 3")
comprobar("L3 y partir tambien tiene la pareja (2,3)", (2, 3) in p["parejas"], True)
comprobar("L4 pero quitar habla de 'quedan'", "resultado" in q, True)
comprobar("L5 y la diferencia NO (no se quita nada)", "resultado" in d, False)

print("\n" + "=" * 78)
print("UNIDAD 5.5: %d/%d correctos" % (BIEN, BIEN + MAL))
print("=" * 78)
sys.exit(1 if MAL else 0)
