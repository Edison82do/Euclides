# -*- coding: utf-8 -*-
"""
PRUEBAS DE LA UNIDAD 6.2  -  AGRUPAR DE DIEZ EN DIEZ (el diez como UNA cosa)

Lo que hay que demostrar:
  1. El agrupamiento es correcto: 13 objetos -> 1 decena y 3 unidades.
  2. El reparto CUADRA siempre: decenas x 10 + unidades == numero de objetos.
  3. Las UNIDADES nunca llegan a diez (si llegaran, habria otra decena).
  4. El ORDEN no cambia el valor (lo dice Oak): agrupar al reves da lo mismo.
  5. Las condiciones de aplicacion: menos de diez -> no_hay_decena; mas de MIL -> no_alcanza (6.7).
  6. LA PRUEBA DE HIERRO: EL RANGO ENTERO.  Las 1001 cantidades de 0 a 1000, una a una (6.7).
     (Una prueba que solo mira un par de casos deja pasar los fallos del rango, como paso en la 5.3.)
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

import motor  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _hierro  # noqa: E402

SABER = motor.cargar_conocimiento()

fallos = []
pruebas = []


def check(nombre, cond, detalle=""):
    pruebas.append(nombre)
    if not cond:
        fallos.append("%s  %s" % (nombre, detalle))


def escena_de_n(n):
    """Una coleccion de n objetos distintos: o1, o2, ... on."""
    return motor.escena_cantidad(",".join("o%d" % i for i in range(1, n + 1)), SABER)


# ---------------------------------------------------------------------------
# A. EL CASO DE LA UNIDAD
# ---------------------------------------------------------------------------
r = motor.decidir_6_2_agrupar(escena_de_n(13), SABER)
check("A1 conclusion", r["conclusion"] == "se_puede", r["conclusion"])
check("A2 objetos", r["cuantos_objetos"] == 13, r["cuantos_objetos"])
check("A3 decenas", r["decenas"] == 1, r["decenas"])
check("A4 unidades", r["unidades"] == 3, r["unidades"])
check("A5 como se dice", r["como_se_dice"] == "una decena y tres", r["como_se_dice"])
check("A6 palabra del total", r["palabra_total"] == "trece", r["palabra_total"])
check("A7 reparto cuadra", r["reparto_cuadra"] is True)
check("A8 el orden da igual", r["el_orden_da_igual"] is True)
check("A9 hay 1 monton", len(r["montones"]) == 1, len(r["montones"]))
check("A10 el monton tiene 10", len(r["montones"][0]) == 10, len(r["montones"][0]))
check("A11 quedan 3 sueltos", len(r["sueltos"]) == 3, len(r["sueltos"]))

# Ojo con el genero: "una decena", no "uno decena"
check("A12 la decena es femenina", "uno decena" not in r["como_se_dice"], r["como_se_dice"])

r24 = motor.decidir_6_2_agrupar(escena_de_n(24), SABER)
check("A13 24 -> dos decenas y cuatro", r24["como_se_dice"] == "dos decenas y cuatro", r24["como_se_dice"])

r10 = motor.decidir_6_2_agrupar(escena_de_n(10), SABER)
check("A14 10 -> una decena (justa)", r10["como_se_dice"] == "una decena", r10["como_se_dice"])
check("A15 10 -> 0 unidades", r10["unidades"] == 0, r10["unidades"])

r20 = motor.decidir_6_2_agrupar(escena_de_n(20), SABER)
check("A16 20 -> dos decenas", r20["como_se_dice"] == "dos decenas", r20["como_se_dice"])

r100 = motor.decidir_6_2_agrupar(escena_de_n(100), SABER)
check("A17 100 -> diez decenas", r100["decenas"] == 10, r100["decenas"])
check("A18 100 -> 0 unidades", r100["unidades"] == 0, r100["unidades"])
check("A19 100 -> palabra cien", r100["palabra_total"] == "cien", r100["palabra_total"])


# ---------------------------------------------------------------------------
# B. LA PRUEBA DE HIERRO: EL RANGO ENTERO  (las 101 cantidades)
# ---------------------------------------------------------------------------
_H = _hierro.Agregado()
NUMEROS = _hierro.numeros(0, 1000)
for n in NUMEROS:  # 6.7: el rango sube a MIL
    r = motor.decidir_6_2_agrupar(escena_de_n(n), SABER)
    if n == 0:
        # El vacio es CERO, no "no hay decena" (unidad 3.2).  No hay decenas NI unidades.
        _H.check("B 0: el vacio es cero", r["conclusion"] == "se_puede" and r["como_se_dice"] == "cero",
              "%s / %s" % (r["conclusion"], r.get("como_se_dice")))
        continue
    if n < 10:
        _H.check("B %d: menos de diez no hay decena" % n, r["conclusion"] == "no_hay_decena",
              "%d -> %s" % (n, r["conclusion"]))
        continue
    _H.check("B %d: se puede" % n, r["conclusion"] == "se_puede", "%d -> %s" % (n, r["conclusion"]))
    _H.check("B %d: decenas correctas" % n, r["decenas"] == n // 10, "%d -> %d" % (n, r["decenas"]))
    _H.check("B %d: unidades correctas" % n, r["unidades"] == n % 10, "%d -> %d" % (n, r["unidades"]))
    _H.check("B %d: las unidades nunca llegan a diez" % n, r["unidades"] < 10, r["unidades"])
    _H.check("B %d: el reparto cuadra" % n, r["decenas"] * 10 + r["unidades"] == n)
    _H.check("B %d: el orden da igual" % n, r["el_orden_da_igual"] is True)
    _H.check("B %d: el numero de montones" % n, len(r["montones"]) == n // 10, len(r["montones"]))
    _H.check("B %d: los montones son de diez" % n, all(len(m) == 10 for m in r["montones"]))
    _H.check("B %d: los sueltos son las unidades" % n, len(r["sueltos"]) == n % 10)
    _H.check("B %d: cada objeto esta UNA vez" % n,
          sorted([x["id"] for m in r["montones"] for x in m] + [x["id"] for x in r["sueltos"]])
          == sorted(x["id"] for x in escena_de_n(n)))

_H.volcar(check, "B HIERRO (%d cantidades, %s):" % (len(NUMEROS), _hierro.modo()))

# El techo de verdad
# UNIDAD 6.7: el techo subio de cien a MIL; 101 ya se puede.
r = motor.decidir_6_2_agrupar(escena_de_n(1001), SABER)
check("B101: mas de mil -> no_alcanza", r["conclusion"] == "no_alcanza", r["conclusion"])


# ---------------------------------------------------------------------------
# C. EL ERROR TIPICO QUE DOCUMENTA OAK
# ---------------------------------------------------------------------------
t = motor.explicar_6_2_agrupar(escena_de_n(23), SABER)
check("C1 el explicador avisa del error tipico", "ERROR TIPICO" in t)
check("C2 dice que las decenas van de diez en diez", "de DIEZ EN DIEZ" in t)
check("C3 dice que las unidades van de uno en uno", "DE UNO EN UNO" in t.upper())
check("C4 dice que se cuentan primero las decenas", "PRIMERO LAS DECENAS" in t)
check("C5 ensena los montones", "MONTON 1" in t and "MONTON 2" in t)
check("C6 ensena los sueltos", "SUELTOS" in t)
check("C7 dice el resultado", "RESULTADO: dos decenas y tres" in t)
check("C8 nombra el unitising", "unitising" in t)
check("C9 conecta con el valor posicional", "VALOR POSICIONAL" in t)
check("C10 conecta con multiplicar", "paso a multiplicar" in t)

t = motor.explicar_6_2_agrupar(escena_de_n(7), SABER)
check("C11 menos de diez se explica", "no_hay_decena" in t and "hacen falta DIEZ" in t)
check("C12 no hay media decena", "media decena" in t)

t = motor.explicar_6_2_agrupar(escena_de_n(1001), SABER)  # 6.7: el techo es MIL
check("C13 el techo se explica", "no_alcanza" in t)


# ---------------------------------------------------------------------------
# D. NO SE MEZCLA CON LO DE ANTES
# ---------------------------------------------------------------------------
# 'cuantos' sigue contando de uno en uno (la 6.2 es OTRA cosa: agrupar)
r = motor.decidir_2_3_cuantos(escena_de_n(13), SABER)
check("D1 cuantos sigue dando la cantidad", r.get("cantidad") == "trece", r.get("cantidad"))
# ...pero solo llega hasta cien
r = motor.decidir_2_3_cuantos(escena_de_n(1001), SABER)  # 6.7: el techo es MIL
check("D2 cuantos sigue teniendo techo", r["conclusion"] == "no_alcanza_la_secuencia", r["conclusion"])
# Y agrupar NO es contar: con trece, agrupar dice "una decena y tres", no "trece"
r = motor.decidir_6_2_agrupar(escena_de_n(13), SABER)
check("D3 agrupar no es contar", r["como_se_dice"] != r["palabra_total"], r["como_se_dice"])
# Las cifras de dos digitos siguen sin leerse (unidad 6.3, pendiente)
try:
    motor.escena_cantidad("47", SABER)
    check("D4 el 47 sigue sin leerse", False, "no salto la excepcion")
except motor.EntradaDelGrupoEquivocado:
    check("D4 el 47 sigue sin leerse (dice que no)", True)


# ---------------------------------------------------------------------------
print("PRUEBAS 6.2  -  AGRUPAR DE DIEZ EN DIEZ")
print("=" * 60)
for f in fallos:
    print("  FALLA:  " + f)
print("-" * 60)
print("  %d de %d bien, %d fallan" % (len(pruebas) - len(fallos), len(pruebas), len(fallos)))
print("UNIDAD 6.2: %d/%d" % (len(pruebas) - len(fallos), len(pruebas)))
if fallos:
    print("RESULTADO: HAY FALLOS")
    sys.exit(1)
print("RESULTADO: TODO BIEN")
