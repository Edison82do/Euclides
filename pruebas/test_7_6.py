# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 7.6 - SUMAR Y RESTAR POR COLUMNAS CON LA CENTENA (la NOTA 7 entera).

Lo que esta unidad tiene que dejar claro (columnas_con_centenas.kn y reglas_7_6.kn):
  - El metodo es EL MISMO de la 7.3 y la 7.5, con una columna mas: unidades, decenas, CENTENAS.
  - El llevarse es re-agrupar en CUALQUIER columna (diez decenas suben como una centena), nunca
    pasa de 1, y una columna de tres numeros se suma en DOS pasos.
  - El intercambio sube de escalon (una centena por diez decenas) y RESTAR A TRAVES DE UN CERO
    se hace escalon a escalon: 500 - 247 -> 4 c, 9 d, 10 u.  El numero sigue valiendo lo mismo.
  - NINGUNA cuenta es una caja negra: cada columna sale de un METODO (dedos 7.1 / 7.4).
  - Lo que la 7.3 y la 7.5 ya hacian (hasta cien) sale EXACTAMENTE igual.
  - La vuelta verifica: la suma se comprueba restando y la resta sumando.

LA PRUEBA DE HIERRO (E): miles de parejas repartidas por todo el rango hasta mil, y TODAS las
restas de un numero con ceros intercalados (100, 200, ..., 1000, 101, 205...).
"""

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, RAIZ)
sys.path.insert(0, AQUI)
import motor  # noqa: E402
import _muestras  # noqa: E402
import random  # noqa: E402
import probar  # noqa: E402

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
col = motor.decidir_7_6_columnas

print("=" * 78)
print("UNIDAD 7.6 - COLUMNAS CON LA CENTENA")
print("=" * 78)

# ------------------------------------------------------------------ A: la suma
print("\nA - LA SUMA")
r = col("247", "+", "385", SABER)
comprobar("A1 247 + 385 = 632", r["total_valor"], 632)
comprobar("A2 se lleva a las decenas y a las centenas", [p.get("se_lleva") for p in r["pasos"]], [1, 1, 0])
comprobar("A3 la columna con lo que se lleva va en DOS pasos", r["pasos"][1]["paso_2"] is not None, True)
comprobar("A4 la vuelta (632 - 385) da 247", r["verificacion"], True)
r = col("999", "+", "1", SABER)
comprobar("A5 999 + 1 = 1000 (tres llevadas: sale la unidad de mil)", r["total_valor"], 1000)
comprobar("A6 y la ultima columna es solo lo que se lleva", r["pasos"][-1].get("solo_lo_que_se_lleva"), 1)
r = motor.decidir_7_3_columnas("99", "99", SABER)
comprobar("A7 99 + 99 por 'columnas:' llega a la 7.6 (el total pasa de cien)", r.get("unidad"), "7.6")
comprobar("A8 y da 198", r["total_valor"], 198)

# ------------------------------------------------------------------ B: la resta
print("\nB - LA RESTA")
r = col("500", "-", "247", SABER)
comprobar("B1 500 - 247 = 253", r["total_valor"], 253)
comprobar("B2 A TRAVES DE UN CERO (dos cambios seguidos en la columna de las unidades)",
          len(r["pasos"][0]["cambios"]), 2)
comprobar("B3 despues de los cambios arriba queda 4 c, 9 d, 10 u", r["pasos"][0]["cambios"][-1]["queda"], [10, 9, 4])
comprobar("B4 y cada cambio sigue valiendo 500", all(c["sigue_valiendo"] for c in r["pasos"][0]["cambios"]), True)
comprobar("B5 TRAMPA: dar la vuelta daria 347 (y no es)", r["si_diera_la_vuelta"], 347)
comprobar("B6 la vuelta (253 + 247) da 500", r["verificacion"], True)
r = col("1000", "-", "1", SABER)
comprobar("B7 1000 - 1 = 999 (tres cambios seguidos)", (r["total_valor"], len(r["pasos"][0]["cambios"])), (999, 3))
r = col("720", "-", "180", SABER)
comprobar("B8 720 - 180 = 540 (NZ Maths: 720 visto como 6 c y 12 d)", r["total_valor"], 540)
comprobar("B9 ... y arriba queda 6 centenas y 12 decenas", r["arriba_despues"][1:], [12, 6])
r = motor.decidir_7_5_columnas("150", "40", SABER)
comprobar("B10 150 - 40 por 'columnas:' llega a la 7.6", (r.get("unidad"), r["total_valor"]), ("7.6", 110))

# ------------------------------------------------------------------ C: condiciones
print("\nC - LAS CONDICIONES DE APLICACION")
comprobar("C1 900 + 200 pasa de mil: no_alcanza", col("900", "+", "200", SABER)["conclusion"], "no_alcanza")
comprobar("C2 300 - 301: no_hay_bastantes", col("300", "-", "301", SABER)["conclusion"], "no_hay_bastantes")
comprobar("C3 1500 - 40: no_alcanza (es un numero, pero pasa de mil)", col("1500", "-", "40", SABER)["conclusion"], "no_alcanza")
comprobar("C4 silla - 3: no_es_un_numero", col("silla", "-", "3", SABER)["conclusion"], "no_es_un_numero")
comprobar("C5 la regla que decide se puede rastrear", col("900", "+", "200", SABER)["regla"], "c6_no_alcanza")

# ------------------------------------------------------------------ D: lo de antes no cambia
print("\nD - LO QUE LA 7.3 Y LA 7.5 YA HACIAN SALE IGUAL (hasta cien)")
SUMAS_100 = _muestras.parejas(100, lambda a, b: a + b <= 100, extra=[(0, 100), (100, 0), (50, 50)])
RESTAS_100 = _muestras.parejas(100, lambda a, b: b <= a, extra=[(100, 1), (100, 100)])
cambios = sum(1 for a, b in SUMAS_100
              if motor.decidir_7_3_columnas(str(a), str(b), SABER).get("unidad") == "7.6")
comprobar("D1 ninguna suma con total <= 100 se va a la 7.6 (%d parejas)" % len(SUMAS_100), cambios, 0)
cambios = sum(1 for a, b in RESTAS_100
              if motor.decidir_7_5_columnas(str(a), str(b), SABER).get("unidad") == "7.6")
comprobar("D2 ninguna resta con el de arriba <= 100 se va a la 7.6 (%d parejas)" % len(RESTAS_100), cambios, 0)
# y la 7.6 dice LO MISMO que la 7.3 / 7.5 donde las dos saben
dif = 0
for a, b in SUMAS_100:
    if col(str(a), "+", str(b), SABER)["total_valor"] != motor.decidir_7_3_columnas(str(a), str(b), SABER)["total_valor"]:
        dif += 1
for a, b in RESTAS_100:
    if col(str(a), "-", str(b), SABER)["total_valor"] != motor.decidir_7_5_columnas(str(a), str(b), SABER)["resta"]:
        dif += 1
comprobar("D3 donde las dos saben, la 7.6 y la 7.3/7.5 dan lo mismo", dif, 0)

# ------------------------------------------------------------------ E: la prueba de hierro
print("\nE - LA PRUEBA DE HIERRO (hasta mil)")
probadas = malas = sin_vuelta = caja_negra = lleva_mas_de_uno = 0
for a, b in _muestras.parejas(1000, lambda a, b: a + b <= 1000, cuantas_al_azar=500,
                            extra=[(999, 1), (500, 500), (1, 999), (455, 545)]):
    if True:
        r = col(str(a), "+", str(b), SABER)
        probadas += 1
        if r["conclusion"] != "se_puede" or r["total_valor"] != a + b:
            malas += 1
        if not r["verificacion"]:
            sin_vuelta += 1
        if "?" in r["metodos_usados"]:
            caja_negra += 1
        if any((p.get("se_lleva") or 0) > 1 for p in r["pasos"]):
            lleva_mas_de_uno += 1
comprobar("E1 las %d sumas dan bien" % probadas, malas, 0)
comprobar("E2 todas se comprueban por la vuelta", sin_vuelta, 0)
comprobar("E3 ninguna columna sin metodo (cero cajas negras)", caja_negra, 0)
comprobar("E4 lo que se lleva nunca pasa de 1", lleva_mas_de_uno, 0)
comprobar("E5 y se recorrio el rango (%s): %d sumas" % (_muestras.modo(), probadas), probadas > 1000, True)
probadas = malas = sin_vuelta = caja_negra = por_cero = 0
# las restas: las parejas de siempre + TODAS las de arriba con un CERO dentro (100, 205, 1000...)
# contra una muestra de abajo, que es donde vive el cambio a traves de un cero
con_ceros = [n for n in range(100, 1001) if "0" in str(n)]
azar = random.Random(7)
RESTAS = set(_muestras.parejas(1000, lambda a, b: b <= a, cuantas_al_azar=500))
for a in con_ceros:
    abajos = range(0, a + 1) if False else \
        {0, 1, 9, 10, 11, 99, 100, a - 1, a} | {azar.randint(0, a) for _ in range(4)}
    RESTAS |= {(a, b) for b in abajos if 0 <= b <= a}
for a, b in sorted(RESTAS):
    if True:
        r = col(str(a), "-", str(b), SABER)
        probadas += 1
        if r["conclusion"] != "se_puede" or r["total_valor"] != a - b:
            malas += 1
        if not r["verificacion"]:
            sin_vuelta += 1
        if "?" in r["metodos_usados"]:
            caja_negra += 1
        if r["a_traves_de_un_cero"]:
            por_cero += 1
comprobar("E6 las %d restas dan bien" % probadas, malas, 0)
comprobar("E7 todas se comprueban por la vuelta", sin_vuelta, 0)
comprobar("E8 ninguna columna sin metodo (cero cajas negras)", caja_negra, 0)
comprobar("E9 y hay muchisimas A TRAVES DE UN CERO (%d)" % por_cero, por_cero > 300, True)

# ------------------------------------------------------------------ F: una sola verdad
print("\nF - UNA SOLA VERDAD (todas las puertas que suman o restan)")
for a, b in ((247, 385), (99, 99), (500, 247), (50, 27), (1000, 1)):
    if a + b <= 1000:
        s, _ = probar.preguntar("sumar_numeros: %d + %d" % (a, b), SABER)
        c, _ = probar.preguntar("columnas: %d + %d" % (a, b), SABER)
        comprobar("F sumar_numeros y columnas dicen lo mismo de %d + %d" % (a, b), s, c)
    if b <= a:
        s, _ = probar.preguntar("restar_numeros: %d - %d" % (a, b), SABER)
        c, _ = probar.preguntar("columnas: %d - %d" % (a, b), SABER)
        comprobar("F restar_numeros y columnas dicen lo mismo de %d - %d" % (a, b), s, c)
t = motor.explicar_pregunta("restar_numeros: 50 - 27", SABER)
comprobar("F ya no sale 'None - None' (fallo arreglado el 5 oct 2026)", "None" in t, False)
d = motor.decidir_5_5_diferencia_numeros("300", "47", SABER)
comprobar("F la diferencia de 300 y 47 se mide por columnas: 253", (d["diferencia_valor"], d["expresion"]),
          (253, "300 - 47 = 253"))
t = motor.explicar_pregunta("sumar_numeros: novecientos + novecientos", SABER)
comprobar("F 900 + 900 dice no_alcanza (antes reventaba con KeyError)", "RESULTADO: no_alcanza" in t, True)

print("\n" + "=" * 78)
print("UNIDAD 7.6: %d/%d correctos" % (BIEN, BIEN + MAL))
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
print("=" * 78)
sys.exit(1 if MAL else 0)
