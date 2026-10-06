# -*- coding: utf-8 -*-
"""
PRUEBAS DE LA UNIDAD 7.3  -  SUMAR POR COLUMNAS

Lo que hay que demostrar:
  1. El metodo da el resultado: 47 + 15 = 62 (7+5=12 -> anoto 2, me llevo 1; 4+1+1=6).
  2. LAS COLUMNAS CUADRAN: decenas x 10 + unidades = total, SIEMPRE.
  3. EL LLEVADO ES UNA DECENA ENTERA: 12 = 2 + 1x10 (no un truco).
  4. LO QUE SE LLEVA NUNCA PASA DE 1 (9+9=18, o sea una decena).
  5. Olvidarse de lo que se lleva da un numero FALSO: el sistema lo sabe y lo dice.
  6. LA PRUEBA DE HIERRO: EL RANGO ENTERO.  TODAS las parejas (a,b) con a+b <= 100.
  7. LA COHERENCIA: sumar_numeros (5.3) con dos cifras tiene que dar LO MISMO que columnas:.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

import motor  # noqa: E402

SABER = motor.cargar_conocimiento()

fallos = []
pruebas = []


def check(nombre, cond, detalle=""):
    pruebas.append(nombre)
    if not cond:
        fallos.append("%s  %s" % (nombre, detalle))


# ---------------------------------------------------------------------------
# A. EL CASO DE LA UNIDAD
# ---------------------------------------------------------------------------
r = motor.decidir_7_3_columnas("47", "15", SABER)
check("A1 conclusion", r["conclusion"] == "se_puede", r["conclusion"])
check("A2 total", r["total_valor"] == 62, r["total_valor"])
check("A3 suma de unidades", r["suma_unidades"] == 12, r["suma_unidades"])
check("A4 se lleva 1", r["se_lleva"] == 1, r["se_lleva"])
check("A5 anota 2 unidades", r["anota_unidades"] == 2, r["anota_unidades"])
check("A6 decenas: 4+1+1", r["suma_decenas"] == 6, r["suma_decenas"])
check("A7 la cuenta de unidades", r["cuenta_unidades"] == "7 + 5 = 12", r["cuenta_unidades"])
check("A8 la cuenta de decenas", r["cuenta_decenas"] == "4 + 1 + 1 = 6", r["cuenta_decenas"])
check("A9 hay que llevarse", r["hay_que_llevarse"] is True)
check("A10 el llevado es una decena", r["el_llevado_es_una_decena"] is True)
check("A11 la expresion", r["expresion_cifras"] == "47 + 15 = 62", r["expresion_cifras"])
check("A12 la palabra del total", r["total"] == "sesenta y dos", r["total"])
check("A13 verificacion por la vuelta", r["verificacion"] is True)

# Sin llevarse
r = motor.decidir_7_3_columnas("5", "3", SABER)
check("A14 5+3 sin llevarse", r["hay_que_llevarse"] is False and r["total_valor"] == 8)
check("A15 su cuenta de decenas no lleva", r["cuenta_decenas"] == "0 + 0 = 0", r["cuenta_decenas"])

r = motor.decidir_7_3_columnas("32", "15", SABER)
check("A16 32+15 = 47", r["total_valor"] == 47, r["total_valor"])
check("A17 2+5=7 no pasa de nueve", r["hay_que_llevarse"] is False)

# El peor caso del llevarse
r = motor.decidir_7_3_columnas("9", "9", SABER)
check("A18 9+9=18", r["total_valor"] == 18, r["total_valor"])
check("A19 se lleva 1 (no 2)", r["se_lleva"] == 1, r["se_lleva"])

# Con palabras
r = motor.decidir_7_3_columnas("cuarenta y siete", "quince", SABER)
check("A20 con palabras", r["conclusion"] == "se_puede" and r["total_valor"] == 62, r["conclusion"])


# ---------------------------------------------------------------------------
# B. LA PRUEBA DE HIERRO: EL RANGO ENTERO  (todas las parejas con suma <= 100)
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _muestras  # noqa: E402
PAREJAS = _muestras.parejas(100, lambda a, b: a + b <= 100,
                          extra=[(0, 100), (100, 0), (50, 50), (99, 1), (1, 99), (45, 55)])
n_parejas = len(PAREJAS)
malas = {"se puede": [], "el total": [], "las columnas cuadran": [], "el llevado es una decena": [],
         "se lleva 0 o 1": [], "olvidar el llevado daria falso": [], "la vuelta": []}
for a, b in PAREJAS:
    r = motor.decidir_7_3_columnas(str(a), str(b), SABER)
    if r["conclusion"] != "se_puede":
        malas["se puede"].append((a, b))
        continue
    if r["total_valor"] != a + b:
        malas["el total"].append((a, b, r["total_valor"]))
    if r["suma_decenas"] * 10 + r["anota_unidades"] != a + b:
        malas["las columnas cuadran"].append((a, b))
    if r["suma_unidades"] != r["anota_unidades"] + r["se_lleva"] * 10:
        malas["el llevado es una decena"].append((a, b))
    if r["se_lleva"] not in (0, 1):
        malas["se lleva 0 o 1"].append((a, b))
    if r["se_lleva"] and r["sin_llevarse_daria_mal"] is not True:
        malas["olvidar el llevado daria falso"].append((a, b))
    if r["verificacion"] is not True:
        malas["la vuelta"].append((a, b))
for k, v in malas.items():
    check("B HIERRO (%d parejas, %s): %s" % (n_parejas, _muestras.modo(), k), not v, v[:3])

# Y por encima de MIL, lo dice  (UNIDAD 6.7: el techo subio de cien a mil;
# antes esta lista era 60+50, 99+9, 100+1 y 55+55, que ahora SI se pueden)
# PASO N.3: el techo es DIEZ MIL (600+500, 999+9, 1000+1 y 550+550 ya SI se pueden).
for a, b in ((6000, 5000), (9999, 9), (10000, 1), (5500, 5500)):
    r = motor.decidir_7_3_columnas(str(a), str(b), SABER)
    check("B %d+%d pasa de DIEZ MIL -> no_alcanza" % (a, b), r["conclusion"] == "no_alcanza",
          r["conclusion"])

r = motor.decidir_7_3_columnas("manzana", "3", SABER)
check("B objeto no es numero", r["conclusion"] == "no_es_un_numero", r["conclusion"])


# ---------------------------------------------------------------------------
# C. LA COHERENCIA: sumar_numeros usa las columnas
# ---------------------------------------------------------------------------
for a, b in ((47, 15), (32, 15), (28, 15), (9, 9), (90, 5), (5, 3), (60, 40), (99, 1)):
    col = motor.decidir_7_3_columnas(str(a), str(b), SABER)
    sn = motor.decidir_5_3_sumar_numeros(str(a), str(b), SABER)
    check("C %d+%d: sumar_numeros da lo mismo" % (a, b),
          sn["total_valor"] == col["total_valor"], "%s / %s" % (sn.get("total_valor"),
                                                                col["total_valor"]))
    check("C %d+%d: y usa las columnas" % (a, b),
          bool(sn.get("por_columnas")) or (a <= 9 and b <= 9), str(sn.get("metodo")))
    check("C %d+%d: misma palabra" % (a, b), sn["suma"] == col["total"],
          "%s / %s" % (sn["suma"], col["total"]))


# ---------------------------------------------------------------------------
# D. EL EXPLICADOR
# ---------------------------------------------------------------------------
t = motor.explicar_7_3_columnas("47", "15", SABER)
check("D1 ensena las columnas", "PASO 1" in t and "PASO 2" in t)
check("D2 ensena el llevarse", "LLEVO 1 DECENA" in t.upper())
check("D3 avisa de olvidarse", "seria FALSO" in t)
check("D4 dice que el llevado es una decena", "UNA DECENA Y 2 UNIDADES" in t)
check("D5 dice lo que se lleva nunca es mas de 1", "NUNCA PUEDE SER MAS DE 1" in t.upper())
check("D6 cita la nota 7 de Carlos", "unidad con unidad" in t)
check("D7 dice que el llevarse es re-agrupar", "RE-AGRUPAR" in t)
check("D8 el resultado", "RESULTADO: 47 + 15 = 62" in t)

t = motor.explicar_7_3_columnas("5", "3", SABER)
check("D9 sin llevarse lo dice", "no hay nada que llevarse" in t)

# 6.7: 60+50 = 110 YA se puede; el techo es MIL.
t = motor.explicar_7_3_columnas("6000", "5000", SABER)
check("D10 el techo se explica (N.3: el techo es DIEZ MIL)", "no_alcanza" in t)


# ---------------------------------------------------------------------------
# E. NO SE ROMPIO NADA DE ANTES
# ---------------------------------------------------------------------------
# derivar (7.2) sigue siendo de UNA cifra
check("E1 derivar sigue pidiendo las columnas",
      motor.decidir_7_2_derivar("47", "3", SABER)["conclusion"] == "necesito_las_columnas")
# los dedos (7.1) siguen igual
check("E2 los dedos siguen con una cifra",
      motor.decidir_7_1_dedos("8", "5", SABER)["conclusion"] == "se_puede")
# partir (6.5) sigue igual
check("E3 partir sigue igual", motor.decidir_6_5_partir("47", SABER)["decenas"] == 4)
# y las sumas de una cifra siguen dandose directamente (no por columnas)
r = motor.decidir_5_3_sumar_numeros("3", "2", SABER)
check("E4 3+2 sigue siendo directo", r["conclusion"] == "suma" and not r.get("por_columnas"))
check("E5 9+9 sigue funcionando", motor.decidir_5_3_sumar_numeros("9", "9", SABER)["suma"]
      == "dieciocho")


# ---------------------------------------------------------------------------
print("PRUEBAS 7.3  -  SUMAR POR COLUMNAS")
print("=" * 60)
for f in fallos[:20]:
    print("  FALLA:  " + f)
if len(fallos) > 20:
    print("  ... y %d mas" % (len(fallos) - 20))
print("-" * 60)
print("  %d de %d bien, %d fallan  (%d parejas recorridas)"
      % (len(pruebas) - len(fallos), len(pruebas), len(fallos), n_parejas))
print("UNIDAD 7.3: %d/%d" % (len(pruebas) - len(fallos), len(pruebas)))
if fallos:
    print("RESULTADO: HAY FALLOS")
    sys.exit(1)
print("RESULTADO: TODO BIEN")
