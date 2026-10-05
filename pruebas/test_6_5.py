# -*- coding: utf-8 -*-
"""
PRUEBAS DE LA UNIDAD 6.5  -  PARTIR EN DECENAS Y UNIDADES

Lo que hay que demostrar:
  1. La particion es correcta: 47 = 4 decenas + 7 unidades = 40 + 7.
  2. CADA CIFRA VALE POR SU SITIO: en 47 el 4 vale 40, no 4  (el error tipico de Oak).
  3. Y al reves: juntar 4 decenas y 7 unidades da 47.
  4. Los numeros raros NO se dicen raro: 3 decenas y 12 unidades son CUARENTA Y DOS, no
     "treinta y doce" (el error que documenta NZ Maths).
  5. LA PRUEBA DE HIERRO: EL RANGO ENTERO.  Las 101 cantidades de 0 a 100, una a una.
  6. LA COHERENCIA con la 6.3: partir y sitio tienen que dar las MISMAS decenas y unidades.
     (Una sola verdad: si el sistema sabe el sitio de 47, sabe partirlo igual.)
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


NOMBRE = {n: (motor.construir_nombre_hasta_cien(n, SABER) or "cero") for n in range(0, 101)}


# ---------------------------------------------------------------------------
# A. EL CASO DE LA UNIDAD
# ---------------------------------------------------------------------------
r = motor.decidir_6_5_partir("47", SABER)
check("A1 conclusion", r["conclusion"] == "se_puede", r["conclusion"])
check("A2 decenas", r["decenas"] == 4, r["decenas"])
check("A3 unidades", r["unidades"] == 7, r["unidades"])
check("A4 el valor de las decenas", r["valor_de_las_decenas"] == 40, r["valor_de_las_decenas"])
check("A5 la cuenta", r["cuenta_de_la_particion"] == "4 decenas y 7 unidades son 47", r["cuenta_de_la_particion"])
check("A6 la palabra del total", r["palabra_del_total"] == "cuarenta y siete", r["palabra_del_total"])
check("A7 el 4 NO vale 4", "vale 40" in r["valor_posicional"], r["valor_posicional"])
check("A8 detecta el error de sumar cifras", r["si_sumara_las_cifras"] == 11)

# En palabras tambien
r = motor.decidir_6_5_partir("cuarenta y siete", SABER)
check("A9 con palabras", r["conclusion"] == "se_puede" and r["decenas"] == 4, r["conclusion"])

# El reverso
r = motor.decidir_6_5_juntar_decenas("4", "7", SABER)
check("A10 juntar 4 y 7", r["conclusion"] == "se_puede" and r["total"] == 47, r["total"])
check("A11 su palabra", r["palabra"] == "cuarenta y siete", r["palabra"])
check("A12 su cuenta", r["cuenta"] == "4 decenas y 7 unidades son 47", r["cuenta"])


# ---------------------------------------------------------------------------
# B. LA PRUEBA DE HIERRO: EL RANGO ENTERO (las 101 cantidades)
# ---------------------------------------------------------------------------
for n in range(0, 101):
    r = motor.decidir_6_5_partir(str(n), SABER)
    check("B %d: se parte" % n, r["conclusion"] == "se_puede", r["conclusion"])
    check("B %d: decenas" % n, r["decenas"] == n // 10, "%d -> %d" % (n, r["decenas"]))
    check("B %d: unidades" % n, r["unidades"] == n % 10, "%d -> %d" % (n, r["unidades"]))
    check("B %d: el valor de las decenas" % n, r["valor_de_las_decenas"] == (n // 10) * 10)
    # juntarlo otra vez da el numero (la vuelta)
    check("B %d: se recompone" % n, r["decenas"] * 10 + r["unidades"] == n)
    esperada = ("%d decenas y %d unidades son %d" % (n // 10, n % 10, n) if n >= 10
                else "solo unidades: son %d" % n)
    check("B %d: la cuenta cuadra" % n, r["cuenta_de_la_particion"] == esperada,
          r["cuenta_de_la_particion"])
    # y por la puerta de juntar_decenas, con las MISMAS partes, sale el mismo numero
    j = motor.decidir_6_5_juntar_decenas(str(r["decenas"]), str(r["unidades"]), SABER)
    check("B %d: juntando sus partes da el mismo" % n, j["conclusion"] == "se_puede" and j["total"] == n,
          "%d -> %s" % (n, j.get("total")))
    check("B %d: y se llama igual" % n, j["palabra"] == NOMBRE[n], "%s / %s" % (j["palabra"], NOMBRE[n]))

# Fuera de la tabla
for malo in ("101", "200"):
    r = motor.decidir_6_5_partir(malo, SABER)
    check("B fuera: %s" % malo, r["conclusion"] == "fuera_de_la_tabla", r["conclusion"])
r = motor.decidir_6_5_partir("manzana", SABER)
check("B no es numero", r["conclusion"] == "no_es_un_numero", r["conclusion"])
r = motor.decidir_6_5_juntar_decenas("11", "0", SABER)
check("B juntar 11 decenas pasa de cien", r["conclusion"] == "fuera_de_la_tabla", r["conclusion"])


# ---------------------------------------------------------------------------
# C. LOS NUMEROS RAROS NO SE DICEN RARO  (el error que documenta NZ Maths)
# ---------------------------------------------------------------------------
# 3 decenas y 12 unidades son 42, y se dice "cuarenta y dos", NO "treinta y doce".
r = motor.decidir_6_5_juntar_decenas("3", "12", SABER)
check("C1 3 decenas y 12 unidades son 42", r["total"] == 42, r["total"])
check("C2 y se dice cuarenta y dos", r["palabra"] == "cuarenta y dos", r["palabra"])
check("C3 NO se dice treinta y doce", "treinta y doce" not in r["palabra"], r["palabra"])
check("C4 avisa de las unidades de mas", r["demasiadas_unidades"] is True)

# ...pero 4 decenas y 7 unidades si son las de verdad
r = motor.decidir_6_5_juntar_decenas("4", "7", SABER)
check("C5 4 y 7 son la particion normal", r["demasiadas_unidades"] is False)

t = motor.explicar_6_5_juntar_decenas("3", "12", SABER)
check("C6 el explicador avisa", "DIEZ unidades se hace OTRA DECENA" in t)
check("C7 y da el nombre bueno", "se dice 'cuarenta y dos'" in t)


# ---------------------------------------------------------------------------
# D. LA COHERENCIA CON LA 6.3  (una sola verdad)
# ---------------------------------------------------------------------------
for n in (0, 7, 10, 25, 47, 60, 99, 100):
    p = motor.decidir_6_5_partir(str(n), SABER)
    s = motor.decidir_6_3_sitio(str(n), SABER)
    check("D %d: partir y sitio dan las MISMAS decenas" % n,
          p["decenas"] == s["decenas"], "%d / %d" % (p["decenas"], s["decenas"]))
    check("D %d: partir y sitio dan las MISMAS unidades" % n,
          p["unidades"] == s["unidades"], "%d / %d" % (p["unidades"], s["unidades"]))


# ---------------------------------------------------------------------------
# E. EL ERROR TIPICO DE OAK (transponer los digitos)
# ---------------------------------------------------------------------------
t = motor.explicar_6_5_partir("47", SABER)
check("E1 avisa del error tipico", "error tipico" in t.lower() or "ERROR TIPICO" in t.upper())
check("E2 dice que 4+7=11 no es 47", "4 + 7 = 11" in t and "11 NO es 47" in t)
check("E3 nombra el transponer", "transponer los digitos" in t)
check("E4 ensena el valor posicional del 7", "SETENTA" in t)
check("E5 dice que es el requisito de las columnas", "COLUMNAS" in t)
check("E6 da el resultado", "RESULTADO: 4 decenas + 7 unidades = 47" in t)

t = motor.explicar_6_5_partir("7", SABER)
check("E7 una cifra sola: cero decenas", "0 decenas y 7 unidades" in t)
check("E8 y el cero de las decenas no se dice", "NO se dice" in t)

t = motor.explicar_6_5_partir("101", SABER)
check("E9 el techo se explica", "fuera_de_la_tabla" in t)


# ---------------------------------------------------------------------------
# F. NO SE MEZCLA CON LO DE ANTES
# ---------------------------------------------------------------------------
# 'descomponer_numero' (5.3) sigue partiendo en DOS PARTES QUE SUMAN (otra cosa)
r = motor.decidir_5_3_descomponer_numero("5", SABER)
check("F1 descomponer_numero sigue siendo otra cosa (5 = 0+5, 1+4, 2+3)",
      r["conclusion"] == "parejas" and r["parejas"] == [(0, 5), (1, 4), (2, 3)],
      "%s / %s" % (r["conclusion"], r.get("parejas")))
# y 'derivar' sigue pidiendo las columnas con dos cifras
check("F2 derivar sigue diciendo necesito_las_columnas",
      motor.decidir_7_2_derivar("47", "3", SABER)["conclusion"] == "necesito_las_columnas")


# ---------------------------------------------------------------------------
print("PRUEBAS 6.5  -  PARTIR EN DECENAS Y UNIDADES")
print("=" * 60)
for f in fallos[:20]:
    print("  FALLA:  " + f)
if len(fallos) > 20:
    print("  ... y %d mas" % (len(fallos) - 20))
print("-" * 60)
print("  %d de %d bien, %d fallan" % (len(pruebas) - len(fallos), len(pruebas), len(fallos)))
print("UNIDAD 6.5: %d/%d" % (len(pruebas) - len(fallos), len(pruebas)))
if fallos:
    print("RESULTADO: HAY FALLOS")
    sys.exit(1)
print("RESULTADO: TODO BIEN")
