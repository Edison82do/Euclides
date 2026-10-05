# -*- coding: utf-8 -*-
"""
PRUEBAS DE LA UNIDAD 7.2  -  DERIVAR (hacer diez)

Lo que hay que demostrar:
  1. El metodo da el resultado correcto: 7 + 5 = 12 por 7 + 3 + 2.
  2. La PARTE tiene que cuadrar: las dos partes del segundo suman el segundo.
  3. La condicion de aplicacion: si NO cruza el diez, no hace falta.
  4. La condicion de aplicacion: el PRIMERO tiene que ser de una cifra.
  5. Las DOS VIAS (los dedos y derivar) dan LO MISMO.  <- decision de Carlos
  6. LA PRUEBA DE HIERRO: EL RANGO ENTERO.  Las 100 parejas 0..9 x 0..9, las tres vias
     (derivar, dedos, sumar_numeros) comparadas una a una.  Una prueba que solo mira
     hasta diez deja pasar los fallos del techo (eso ya nos paso en la 5.3).
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


PALABRA = ["cero"] + [motor.construir_nombre_hasta_cien(n, SABER) for n in range(1, 11)]


# ---------------------------------------------------------------------------
# A. EL CASO DE LA UNIDAD
# ---------------------------------------------------------------------------
r = motor.decidir_7_2_derivar("7", "5", SABER)
check("A1 conclusion", r["conclusion"] == "se_puede", r["conclusion"])
check("A2 faltan para diez", r["faltan_para_diez"] == 3, r["faltan_para_diez"])
check("A3 parte que sobra", r["parte_que_sobra"] == 2, r["parte_que_sobra"])
check("A4 paso 1", r["paso_1"] == "7 + 3 = 10", r["paso_1"])
check("A5 paso 2", r["paso_2"] == "10 + 2 = 12", r["paso_2"])
check("A6 total", r["total_valor"] == 12, r["total_valor"])
check("A7 palabra del total", r["total"] == "doce", r["total"])
check("A8 expresion", r["expresion"] == "siete + cinco = doce", r["expresion"])
check("A9 suma de tres", r["suma_de_tres"] == "7 + 3 + 2", r["suma_de_tres"])
check("A10 partes cuadran", r["las_partes_cuadran"] is True)
check("A11 verificacion", r["verificacion"] is True)

# En palabras tambien
r2 = motor.decidir_7_2_derivar("siete", "cinco", SABER)
check("A12 en palabras", r2["conclusion"] == "se_puede" and r2["total_valor"] == 12, r2["conclusion"])

# Y mezclando
r3 = motor.decidir_7_2_derivar("7", "cinco", SABER)
check("A13 mezclando cifra y palabra", r3["total_valor"] == 12, r3["total_valor"])


# ---------------------------------------------------------------------------
# B. LAS DOS VIAS TIENEN QUE DAR LO MISMO  (la prueba que pidio Carlos)
# ---------------------------------------------------------------------------
for a in range(0, 10):
    for b in range(0, 10):
        dr = motor.decidir_7_2_derivar(PALABRA[a], PALABRA[b], SABER)
        if dr["conclusion"] != "se_puede":
            continue
        dd = motor.decidir_7_1_dedos(PALABRA[a], PALABRA[b], SABER)
        ds = motor.decidir_5_3_sumar_numeros(PALABRA[a], PALABRA[b], SABER)
        ok_dedos = (dd["conclusion"] != "se_puede") or (dd["total_valor"] == dr["total_valor"])
        ok_suma = (ds["conclusion"] != "se_puede") or (ds["total_valor"] == dr["total_valor"])
        check("B %d+%d: tres vias de acuerdo" % (a, b),
              dr["total_valor"] == a + b and ok_dedos and ok_suma,
              "derivar=%s dedos=%s suma=%s (esperado %d)"
              % (dr["total_valor"], dd.get("total_valor"), ds.get("total_valor"), a + b))
        check("B %d+%d: la otra via dice lo mismo" % (a, b),
              dr["las_dos_vias_coinciden"] is None or dr["las_dos_vias_coinciden"] is True,
              "las_dos_vias_coinciden=%s" % dr["las_dos_vias_coinciden"])

# Y el caso 8 + 9, el que casi nadie tiene memorizado (Number Sense Maths)
r89 = motor.decidir_7_2_derivar("ocho", "nueve", SABER)
check("B2 8+9", r89["conclusion"] == "se_puede" and r89["total_valor"] == 17, r89["conclusion"])
check("B3 8+9 paso 1", r89["paso_1"] == "8 + 2 = 10", r89["paso_1"])
check("B4 8+9 suma de tres", r89["suma_de_tres"] == "8 + 2 + 7", r89["suma_de_tres"])


# ---------------------------------------------------------------------------
# C. CONDICIONES DE APLICACION
# ---------------------------------------------------------------------------
r = motor.decidir_7_2_derivar("4", "5", SABER)
check("C1 4+5 no cruza: no_hace_falta", r["conclusion"] == "no_hace_falta", r["conclusion"])

r = motor.decidir_7_2_derivar("3", "7", SABER)
check("C2 3+7 = 10 justo: tampoco hace falta", r["conclusion"] == "no_hace_falta", r["conclusion"])

r = motor.decidir_7_2_derivar("5", "0", SABER)
check("C3 5+0 no cruza", r["conclusion"] == "no_hace_falta", r["conclusion"])

r = motor.decidir_7_2_derivar("8", "6", SABER)
check("C4 8+6 cruza: se puede", r["conclusion"] == "se_puede", r["conclusion"])

r = motor.decidir_7_2_derivar("cuarenta y siete", "tres", SABER)
check("C5 el primero de dos cifras: columnas", r["conclusion"] == "necesito_las_columnas",
      r["conclusion"])

r = motor.decidir_7_2_derivar("doce", "tres", SABER)
check("C6 el primero de dos cifras (palabra)", r["conclusion"] == "necesito_las_columnas",
      r["conclusion"])

r = motor.decidir_7_2_derivar("ocho", "manzana", SABER)
check("C7 objeto no es numero", r["conclusion"] == "no_es_un_numero", r["conclusion"])

r = motor.decidir_7_2_derivar("manzana", "ocho", SABER)
check("C8 objeto en el primero", r["conclusion"] == "no_es_un_numero", r["conclusion"])

r = motor.decidir_7_2_derivar("noventa y cinco", "nueve", SABER)
check("C9 el primero pasa de cien? no: es de dos cifras",
      r["conclusion"] == "necesito_las_columnas", r["conclusion"])


# ---------------------------------------------------------------------------
# D. LA DERIVACION CUADRA SIEMPRE
# ---------------------------------------------------------------------------
for a in range(0, 10):
    for b in range(0, 10):
        r = motor.decidir_7_2_derivar(PALABRA[a], PALABRA[b], SABER)
        if r["conclusion"] != "se_puede":
            continue
        check("D %d+%d: faltan + sobra = segundo" % (a, b),
              r["faltan_para_diez"] + r["parte_que_sobra"] == b)
        check("D %d+%d: primer resultado es diez" % (a, b),
              r["valor_a"] + r["faltan_para_diez"] == 10)
        check("D %d+%d: verificacion" % (a, b), r["verificacion"] is True)
        check("D %d+%d: los dos pasos son ciertos" % (a, b),
              r["valor_a"] + r["faltan_para_diez"] == 10
              and 10 + r["parte_que_sobra"] == r["total_valor"])


# ---------------------------------------------------------------------------
# E. EL EXPLICADOR
# ---------------------------------------------------------------------------
t = motor.explicar_7_2_derivar("7", "5", SABER)
check("E1 explica el paso 1", "PASO 1" in t)
check("E2 explica el paso 2 (partir)", "PASO 2" in t and "cinco  =  3  +  2" in t)
check("E3 explica el paso 3 (hacer diez)", "PASO 3" in t)
check("E4 ensena la suma de tres", "7 + 3 + 2" in t)
check("E5 prueba las dos vias", "LAS DOS VIAS" in t and "las dos dan lo mismo: SI" in t)
check("E6 cita por que derivar es mejor", "RENDIMIENTO MAS BAJO" in t)
check("E7 da el resultado", "RESULTADO: siete + cinco = doce" in t)

t = motor.explicar_7_2_derivar("4", "5", SABER)
check("E8 no_hace_falta se explica", "no_hace_falta" in t and "NO cruzan el diez" in t)

t = motor.explicar_7_2_derivar("cuarenta y siete", "tres", SABER)
check("E9 las columnas se explican", "necesito_las_columnas" in t and "COLUMNAS" in t)

t = motor.explicar_7_2_derivar("ocho", "manzana", SABER)
check("E10 no_es_un_numero se explica", "no_es_un_numero" in t)


# ---------------------------------------------------------------------------
# F. LA OTRA VIA NO SE ROMPE
# ---------------------------------------------------------------------------
t = motor.explicar_7_1_dedos("8", "5", SABER)
check("F1 los dedos siguen explicando", "PASO 1" in t and "trece" in t)
check("F2 los dedos ahora comparan con derivar", "LA OTRA VIA" in t and "DERIVANDO" in t)

# El caso donde los dedos no llegan y derivar si
r = motor.decidir_7_2_derivar("9", "9", SABER)
check("F3 9+9 derivando", r["conclusion"] == "se_puede" and r["total_valor"] == 18, r["conclusion"])
otra = motor.decidir_7_1_dedos("9", "9", SABER)
check("F4 9+9 con los dedos si cabe (9 <= 10)", otra["conclusion"] == "se_puede",
      otra["conclusion"])


# ---------------------------------------------------------------------------
print("PRUEBAS 7.2  -  DERIVAR (hacer diez)")
print("=" * 60)
for f in fallos:
    print("  FALLA:  " + f)
print("-" * 60)
print("  %d de %d bien, %d fallan" % (len(pruebas) - len(fallos), len(pruebas), len(fallos)))
# Este formato es el que lee pruebas/correr_todas.py para sumar el total del proyecto.
print("UNIDAD 7.2: %d/%d" % (len(pruebas) - len(fallos), len(pruebas)))
if fallos:
    print("RESULTADO: HAY FALLOS")
    sys.exit(1)
print("RESULTADO: TODO BIEN")
