# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 6.7 - LA CENTENA (diez decenas son una centena, y la escalera sigue).

Lo que esta unidad tiene que dejar claro (la_centena.kn y reglas_6_7.kn):
  - La escalera: 10 unidades = 1 decena, 10 decenas = 1 centena, 10 centenas = 1 unidad de mil.
  - Un numero de tres cifras son centenas, decenas y unidades; la POSICION dice el valor.
  - El cero como MARCADOR de posicion, y el error tipico: "204 no tiene decenas" (tiene 20).
  - Los nombres de tres cifras se CONSTRUYEN (los cientos de memoria + el resto de la 6.1), con
    sus irregulares (quinientos, setecientos, novecientos) y el cien/ciento.
  - Nada de "x 100": se dice "2 centenas" (no hay multiplicacion todavia).
  - UNA SOLA VERDAD: centena:, sitio:, partir:, nombre:, numero:, palabra: y cifra: dicen lo mismo
    del mismo numero, y el probador dice lo mismo que el explicador.

LA PRUEBA DE HIERRO (B): los 1001 numeros de 0 a 1000, uno a uno, por todas las puertas.
"""

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, RAIZ)
import motor  # noqa: E402
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


def resultado(texto):
    """La ultima linea RESULTADO de lo que ve quien prueba."""
    lineas = [l for l in motor.explicar_pregunta(texto, SABER).splitlines() if l.startswith("RESULTADO")]
    return lineas[-1] if lineas else None


SABER = motor.cargar_conocimiento()

print("=" * 78)
print("UNIDAD 6.7 - LA CENTENA")
print("=" * 78)

# ------------------------------------------------------------------ A: lo basico
print("\nA - LO BASICO")
r = motor.decidir_6_7_centena("247", SABER)
comprobar("A1 247 son 2 centenas, 4 decenas y 7 unidades", r["dato"], "2 centenas, 4 decenas y 7 unidades")
comprobar("A2 el 2 vale doscientos", r["valores"][2]["vale_en_palabra"], "doscientos")
comprobar("A3 el 4 vale cuarenta", r["valores"][1]["vale_en_palabra"], "cuarenta")
comprobar("A4 y el nombre es doscientos cuarenta y siete", r["palabra"], "doscientos cuarenta y siete")
r = motor.decidir_6_7_centena("204", SABER)
comprobar("A5 TRAMPA (NZ Maths): 204 tiene VEINTE decenas en total", r["decenas_en_total"], 20)
comprobar("A6 y la cifra de las decenas (las sueltas) es 0", r["decenas"], 0)
comprobar("A7 el cero es marcador de posicion de las decenas", r["ceros_de_relleno"], ["decenas"])
r = motor.decidir_6_7_centena("1000", SABER)
comprobar("A8 1000 es 1 unidad de mil", r["unidades_de_mil"], 1)
comprobar("A9 y se llama mil", r["palabra"], "mil")
r = motor.decidir_6_7_centena("doscientos cuarenta y siete", SABER)
comprobar("A10 con palabras tambien", r["valor"], 247)
for n, p in ((500, "quinientos"), (700, "setecientos"), (900, "novecientos"),
             (100, "cien"), (101, "ciento uno"), (120, "ciento veinte"), (200, "doscientos")):
    comprobar("A11 nombre de %d: %s (irregulares y cien/ciento)" % (n, p),
              motor.decidir_6_1_nombre(str(n), SABER).get("palabra"), p)

# ------------------------------------------------------------------ B: la prueba de hierro
print("\nB - LA PRUEBA DE HIERRO: los 1001 numeros de 0 a 1000, por todas las puertas")
malos = {"recompone": 0, "nombre": 0, "vuelta": 0, "palabra_3_1": 0, "cifra_3_1": 0,
         "sitio": 0, "partir": 0, "probador": 0}
for n in range(0, 1001):
    c = motor.decidir_6_7_centena(str(n), SABER)
    if c["conclusion"] != "se_puede" or not c["recompone"]:
        malos["recompone"] += 1
        continue
    if n > 0:
        nom = motor.decidir_6_1_nombre(str(n), SABER).get("palabra")
        if nom != c["palabra"]:
            malos["nombre"] += 1
        if motor.decidir_6_1_numero(nom, SABER).get("valor") != n:
            malos["vuelta"] += 1
        pal = motor.decidir_3_1_palabra(str(n), SABER)
        if pal.get("palabra") != c["palabra"]:
            malos["palabra_3_1"] += 1
        cif = motor.decidir_3_1_cifra(c["palabra"], SABER)
        if str(cif.get("cifra")) != str(n):
            malos["cifra_3_1"] += 1
    if n > 100:
        s = motor.decidir_6_3_sitio(str(n), SABER)
        if s.get("dato") != c["dato"]:
            malos["sitio"] += 1
        p = motor.decidir_6_5_partir(str(n), SABER)
        if p.get("como_se_parte") != c["como_se_parte"]:
            malos["partir"] += 1
    if n % 37 == 0 and n > 0:    # el probador y el explicador (lo que se VE) dicen lo mismo
        obtenido, _ = probar.preguntar("nombre: %d" % n, SABER)
        if obtenido != c["palabra"] or resultado("nombre: %d" % n) != "RESULTADO: %s" % c["palabra"]:
            malos["probador"] += 1
for k, v in malos.items():
    comprobar("B %-12s 0 numeros discrepan" % k, v, 0)

# ------------------------------------------------------------------ C: condiciones
print("\nC - LAS CONDICIONES DE APLICACION")
comprobar("C1 1001 pasa de mil: no_alcanza", motor.decidir_6_7_centena("1001", SABER)["conclusion"], "no_alcanza")
comprobar("C2 manzana no es un numero", motor.decidir_6_7_centena("manzana", SABER)["conclusion"], "no_es_un_numero")
comprobar("C3 sitio de 1001: no_alcanza", motor.decidir_6_3_sitio("1001", SABER)["conclusion"], "no_alcanza")
comprobar("C4 y el 100 SIGUE en la tabla de 100 (6.3 no cambia)",
          motor.decidir_6_3_sitio("100", SABER)["dato"], "10 decenas y 0 unidades")
comprobar("C5 nombre de 1001: fuera_de_mi_secuencia",
          motor.decidir_6_1_nombre("1001", SABER)["conclusion"], "fuera_de_mi_secuencia")
comprobar("C6 numero 'cincocientos': no_lo_se (no se inventa)",
          motor.decidir_6_1_numero("cincocientos", SABER)["conclusion"], "no_lo_se")

# ------------------------------------------------------------------ D: lo que se ensena
print("\nD - LO QUE SE ENSENA (y lo que NO se dice)")
t = motor.explicar_pregunta("centena: 204", SABER)
comprobar("D1 204: explica el cero como MARCADOR", "MARCADOR DE POSICION" in t, True)
comprobar("D2 204: explica las 20 decenas", "hay 20 DECENAS" in t, True)
comprobar("D3 no escribe 'x 100' como cuenta (no sabe multiplicar)", "= 2 x 100" in t or "2x100" in t, False)
t = motor.explicar_pregunta("centena", SABER)
comprobar("D4 'centena' sola da la escalera", resultado("centena"), "RESULTADO: la_escalera")
comprobar("D5 la escalera se comprueba con la 6.5 (10 decenas son cien)", "-> cien ... SI" in t, True)
t = motor.explicar_pregunta("palabra: 247", SABER)
comprobar("D6 palabra: 247 ya no dice 'DOS cifras'", "DOS cifras" in t, False)
comprobar("D7 y no dibuja 247 asteriscos", "*" * 101 in t, False)
t = motor.explicar_pregunta("nombre: 247", SABER)
comprobar("D8 nombre: 247 ensena las dos piezas", "doscientos" in t and "cuarenta y siete" in t
          and "SE CONSTRUYE" in t, True)

print("\n" + "=" * 78)
print("UNIDAD 6.7: %d/%d correctos" % (BIEN, BIEN + MAL))
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
print("=" * 78)
sys.exit(1 if MAL else 0)
