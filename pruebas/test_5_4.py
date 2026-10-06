# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 5.4 - LA RESTA COMO QUITAR (reduccion).

Lo que esta unidad tiene que dejar claro:
  - Restar es QUITAR: el monton DISMINUYE.  La historia es 'primero, luego, ahora'.
  - Y QUITAR NO ES PARTIR (5.1): aqui los que se van SE VAN.
  - El signo - y los terminos: MINUENDO, SUSTRAENDO, RESULTADO.
  - LA CONDICION DE APLICACION: no se puede quitar mas de lo que hay.
  - LA VUELTA VERIFICA: lo que queda + lo que se fue = el minuendo (la suma, unidad 5.2).

LA PRUEBA DE HIERRO (I): toda resta posible se comprueba SUMANDO (cruzando las dos unidades).
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
    """La escena ya leida de n objetos (es lo que el motor espera, no el texto)."""
    return motor.escena_cantidad(coleccion(n), SABER)

print("=" * 78)
print("UNIDAD 5.4 - LA RESTA COMO QUITAR")
print("=" * 78)

# ---------------------------------------------------------------- A) lo basico
print("\nA) LO BASICO Y LOS TERMINOS")
r = motor.decidir_5_4_quitar(esc(5), "dos", SABER)
comprobar("A1 concluye 'quedan'", r["conclusion"], "quedan")
comprobar("A2 el minuendo es cinco", r["minuendo"], "cinco")
comprobar("A3 el sustraendo es dos", r["sustraendo"], "dos")
comprobar("A4 el resultado es tres", r["resultado"], "tres")
comprobar("A5 la expresion es 5 - 2 = 3", r["expresion"], "5 - 2 = 3")
comprobar("A6 se van los DOS ultimos", r["los_que_se_van"], ["o4", "o5"])
comprobar("A7 quedan los TRES primeros", r["los_que_quedan"], ["o1", "o2", "o3"])

r = motor.decidir_5_4_quitar(esc(9), "4", SABER)
comprobar("A8 la cifra tambien vale como sustraendo 9-4", r["expresion"], "9 - 4 = 5")
r = motor.decidir_5_4_quitar(esc(4), "cuatro", SABER)
comprobar("A9 quitar TODO deja cero: 4 - 4 = 0", r["expresion"], "4 - 4 = 0")
comprobar("A10 y el resultado es la palabra cero", r["resultado"], "cero")
r = motor.decidir_5_4_quitar(esc(3), "cero", SABER)
comprobar("A11 quitar CERO no quita nada: 3 - 0 = 3", r["expresion"], "3 - 0 = 3")
comprobar("A12 y no se va nadie", r["los_que_se_van"], [])

# ------------------------------------------------- B) la condicion de aplicacion
print("\nB) LA CONDICION DE APLICACION: NO SE PUEDE QUITAR MAS DE LO QUE HAY")
r = motor.decidir_5_4_quitar(esc(2), "tres", SABER)
comprobar("B1 de dos no se quitan tres", r["conclusion"], "no_hay_bastantes")
r = motor.decidir_5_4_quitar(esc(2), "3", SABER)
comprobar("B2 lo mismo con la cifra", r["conclusion"], "no_hay_bastantes")
r = motor.decidir_5_4_quitar(esc(0), "uno", SABER)
comprobar("B3 de nada no se quita uno", r["conclusion"], "no_hay_bastantes")
r = motor.decidir_5_4_quitar(esc(2), "dos", SABER)
comprobar("B4 quitar TODO si se puede (justo lo que hay)", r["conclusion"], "quedan")

# --------------------------------------------------------- C) restar_numeros
print("\nC) RESTAR DOS NUMEROS (sin objetos)")
r = motor.decidir_5_4_restar_numeros("5", "2", SABER)
comprobar("C1 5 - 2 = 3", r["expresion"], "5 - 2 = 3")
r = motor.decidir_5_4_restar_numeros("nueve", "tres", SABER)
comprobar("C2 las palabras valen: nueve - tres = 6", r["expresion"], "9 - 3 = 6")
r = motor.decidir_5_4_restar_numeros("2", "5", SABER)
comprobar("C3 restar mas de lo que hay -> no_hay_bastantes", r["conclusion"], "no_hay_bastantes")
r = motor.decidir_5_4_restar_numeros("5", "manzana", SABER)
comprobar("C4 un objeto no es un numero", r["conclusion"], "no_es_un_numero")
r = motor.decidir_5_4_restar_numeros("7", "7", SABER)
comprobar("C5 7 - 7 = 0", r["expresion"], "7 - 7 = 0")
r = motor.decidir_5_4_restar_numeros("7", "cero", SABER)
comprobar("C6 7 - 0 = 7", r["expresion"], "7 - 0 = 7")

# ------------------------------------------- D) los grupos no se mezclan (5.3)
print("\nD) LOS GRUPOS SEPARADOS (unidad 5.3)")
try:
    motor.escena_cantidad("3", SABER)
    comprobar("D1 un numero no es un objeto", "dejo_pasar", "grupo_equivocado")
except motor.EntradaDelGrupoEquivocado:
    comprobar("D1 un numero no es un objeto", "grupo_equivocado", "grupo_equivocado")
comprobar("D2 el pedido SI es un numero (cifra o palabra)",
          motor.decidir_5_4_quitar(esc(5), "2", SABER)["conclusion"], "quedan")

# ------------------------------------------------------------- E) robustez
print("\nE) ROBUSTEZ Y LO QUE NO ENTIENDE")
r = motor.decidir_5_4_quitar(esc(3), "muchos", SABER)
comprobar("E1 'muchos' no es un numero", r["conclusion"], "no_es_un_numero")
comprobar("E2 y lo dice, no lo inventa", r["conclusion"] != "quedan", True)
r = motor.decidir_5_4_quitar(esc(0), "cero", SABER)
comprobar("E3 de nada, quitar cero: quedan cero", r["expresion"], "0 - 0 = 0")

# ==================================================== LA PRUEBA DE HIERRO (I)
print("\n" + "=" * 78)
print("I) PRUEBA DE HIERRO: toda resta se comprueba SUMANDO (la vuelta, unidad 5.2)")
print("=" * 78)
malas = 0
probadas = 0
sin_suma = 0
for a in range(1, 10):
    for b in range(0, a + 1):
        rr = motor.decidir_5_4_quitar(esc(a), motor._palabra_de(b, SABER["secuencia_de_conteo"]["palabras"]), SABER)
        if rr["conclusion"] != "quedan":
            malas += 1
            continue
        probadas += 1
        if not rr["verificacion"]:
            malas += 1
            print("    NO CUADRA la cuenta: %s" % rr["expresion"])
        if rr["verificacion_con_la_suma"] is None:
            sin_suma += 1
            print("    (sin suma escrita: %s)" % rr["expresion"])
        elif not rr["verificacion_con_la_suma"]:
            malas += 1
            print("    NO CUADRA la vuelta: %s  ->  %s" % (rr["expresion"], rr["expresion_inversa"]))
comprobar("I1 las %d restas posibles se verifican por la vuelta" % probadas, malas, 0)
comprobar("I2 y son 54 (a en 1..9, b de 0 a a)", probadas, 54)
comprobar("I3 ninguna se quedo sin poder comprobarse con la suma", sin_suma, 0)

# El diez de minuendo: la cuenta cuadra, pero la suma ESCRITA no llega (la secuencia de
# numeros acaba en nueve).  Es un limite conocido, y el sistema lo DICE.
r = motor.decidir_5_4_quitar(esc(10), "dos", SABER)
comprobar("I4 con diez de minuendo: 10 - 2 = 8", r["expresion"], "diez - 2 = 8")
comprobar("I5 la cuenta cuadra igual", r["verificacion"], True)
comprobar("I6 y la suma escrita SI llega (da 'diez', que es una palabra)",
          r["verificacion_con_la_suma"], True)

# El limite de verdad: NO SE PUEDE CONTAR MAS DE LO QUE LLEGA LA SECUENCIA.  Con doce objetos el
# sistema ya NO tiene problema (unidad 6.1: la secuencia llega a cien); el limite esta en cien.
r = motor.decidir_5_4_quitar(esc(12), "dos", SABER)
comprobar("I7 (MEJORA 6.1) con doce objetos YA se puede contar: 12 - 2 = 10",
          r["expresion"], "doce - 2 = diez")
r = motor.decidir_5_4_quitar(esc(10001), "dos", SABER)
comprobar("I7b TRAMPA: con mas de DIEZ MIL objetos si lo dice (N.3)", r["conclusion"], "no_alcanza")
r = motor.decidir_5_4_quitar(esc(10), "dos", SABER)
comprobar("I8 diez si (es la ultima palabra): 10 - 2 = 8", r["expresion"], "diez - 2 = 8")
comprobar("I9 y la vuelta cuadra", r["verificacion_con_la_suma"], True)

# Y LO MISMO EN LAS OTRAS UNIDADES que cuentan: mas de lo que llega la secuencia no debe reventar.
print("\nI-bis) MAS DE DIEZ OBJETOS EN LAS UNIDADES QUE CUENTAN (que no reviente)")
casos = [
    ("cuantos:", lambda: motor.explicar_2_3_cuantos(esc(10001), SABER), "no"),
    ("descomponer:", lambda: motor.explicar_5_1_descomponer(esc(10001), SABER), "no"),
    ("sumar:", lambda: motor.explicar_5_2_sumar(esc(10001), esc(2), SABER), "no"),
    ("comparar:", lambda: motor.explicar_4_1_comparar(esc(10001), esc(2), SABER), "no"),
]
for nombre, fn, _ in casos:
    try:
        texto = fn()
        ok = "no_alcanza" in texto or "no_alcanza_a_contar" in texto or "no se contar" in texto
        comprobar("I-bis %s con 12 objetos lo dice (no revienta)" % nombre, ok, True)
    except Exception as e:
        comprobar("I-bis %s con 12 objetos lo dice (no revienta)" % nombre,
                  "REVENTO: %s: %s" % (type(e).__name__, e), True)

# Y la prueba cruzada final: la resta y la suma son la una la vuelta de la otra.
print("\nJ) LA SUMA Y LA RESTA SON LA UNA LA VUELTA DE LA OTRA")
malas = 0
for a in range(0, 10):
    for b in range(0, 10 - a):
        suma = motor.decidir_5_3_sumar_numeros(str(a), str(b), SABER)
        if suma["conclusion"] != "suma":
            continue
        resta = motor.decidir_5_4_restar_numeros(str(a + b), str(b), SABER)
        if resta["conclusion"] != "resta":
            malas += 1
            print("    %d + %d = %d  pero la resta no sale" % (a, b, a + b))
            continue
        if resta["resultado_valor"] != a:
            malas += 1
            print("    %d + %d = %d  y  %s (esperaba %d)" % (a, b, a + b, resta["expresion"], a))
comprobar("J1 (a + b) - b vuelve a dar a, en las 55 parejas", malas, 0)

print("\n" + "=" * 78)
print("UNIDAD 5.4: %d/%d correctos" % (BIEN, BIEN + MAL))
print("=" * 78)
sys.exit(1 if MAL else 0)
