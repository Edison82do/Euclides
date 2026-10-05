# -*- coding: utf-8 -*-
"""
PRUEBAS DE LA UNIDAD 6.3  -  LA TABLA DE 100 (leer cifras de dos digitos)

Lo que hay que demostrar:
  1. El sistema LEE una cifra de dos digitos: 47 -> cuarenta y siete.
  2. Y la vuelve a escribir: cuarenta y siete -> 47.
  3. El SITIO: fila = decenas, columna = unidades; la tabla es 1..100.
  4. Las condiciones de aplicacion: fuera de la tabla (>100), y lo que no es un numero.
  5. LA PRUEBA DE HIERRO: EL RANGO ENTERO.  Las 101 cifras de 0 a 100, una a una.
  6. LA PRUEBA DE LA COHERENCIA (lo que pidio Carlos): el MISMO numero tiene que leerse igual
     por TODAS las puertas.  Una sola verdad: si el lector sabe leer 47, lo sabe en todas las
     ordenes.  (Antes de esta unidad habia cuatro puertas que decian que no.)
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


def escena_de_n(n):
    return motor.escena_cantidad(",".join("o%d" % i for i in range(1, n + 1)), SABER)


# ---------------------------------------------------------------------------
# A. EL CASO DE LA UNIDAD
# ---------------------------------------------------------------------------
r = motor.decidir_3_1_palabra("47", SABER)
check("A1 47 -> palabra", r["conclusion"] == "palabra" and r["palabra"] == "cuarenta y siete",
      "%s / %s" % (r["conclusion"], r.get("palabra")))
r = motor.decidir_3_1_cifra("cuarenta y siete", SABER)
check("A2 cuarenta y siete -> cifra 47", r["conclusion"] == "cifra" and r["cifra"] == "47",
      "%s / %s" % (r["conclusion"], r.get("cifra")))

s = motor.decidir_6_3_sitio("47", SABER)
check("A3 sitio conclusion", s["conclusion"] == "se_puede", s["conclusion"])
check("A4 sitio decenas", s["decenas"] == 4, s["decenas"])
check("A5 sitio unidades", s["unidades"] == 7, s["unidades"])
check("A6 sitio fila", s["fila"] == 4, s["fila"])
check("A7 sitio columna", s["columna"] == 7, s["columna"])
check("A8 sitio dato", s["dato"] == "4 decenas y 7 unidades", s["dato"])

# Y las decenas exactas: el 10 esta al FINAL de la fila 0, no en la fila 1
s = motor.decidir_6_3_sitio("10", SABER)
check("A9 el 10: 1 decena y 0 unidades", s["decenas"] == 1 and s["unidades"] == 0)
check("A10 el 10 esta en la fila 0, columna 10", s["fila"] == 0 and s["columna"] == 10,
      "fila %s columna %s" % (s["fila"], s["columna"]))
s = motor.decidir_6_3_sitio("100", SABER)
check("A11 el 100: diez decenas", s["decenas"] == 10 and s["unidades"] == 0)
check("A12 el 100 esta en la fila 9, columna 10", s["fila"] == 9 and s["columna"] == 10,
      "fila %s columna %s" % (s["fila"], s["columna"]))
check("A13 el 100 se llama cien", s["palabra"] == "cien", s["palabra"])

# Con palabra tambien
s = motor.decidir_6_3_sitio("cuarenta y siete", SABER)
check("A14 el sitio tambien con palabra", s["conclusion"] == "se_puede" and s["decenas"] == 4)


# ---------------------------------------------------------------------------
# B. LA PRUEBA DE HIERRO: EL RANGO ENTERO (las 101 cifras)
# ---------------------------------------------------------------------------
for n in range(0, 101):
    # 1) cifra -> palabra
    r = motor.decidir_3_1_palabra(str(n), SABER)
    check("B %d: cifra -> palabra" % n,
          r["conclusion"] == "palabra" and r["palabra"] == NOMBRE[n],
          "%d -> %s / %s" % (n, r["conclusion"], r.get("palabra")))
    # 2) palabra -> cifra (la vuelta)
    r = motor.decidir_3_1_cifra(NOMBRE[n], SABER)
    check("B %d: palabra -> cifra (la vuelta)" % n,
          r["conclusion"] == "cifra" and r["cifra"] == str(n),
          "%s -> %s / %s" % (NOMBRE[n], r["conclusion"], r.get("cifra")))
    # 3) el sitio
    s = motor.decidir_6_3_sitio(str(n), SABER)
    check("B %d: el sitio se puede" % n, s["conclusion"] == "se_puede", s["conclusion"])
    check("B %d: decenas" % n, s["decenas"] == n // 10, "%d -> %d" % (n, s["decenas"]))
    check("B %d: unidades" % n, s["unidades"] == n % 10, "%d -> %d" % (n, s["unidades"]))
    check("B %d: el numero se recompone" % n, s["decenas"] * 10 + s["unidades"] == n)
    if n >= 1:
        check("B %d: fila" % n, s["fila"] == (n - 1) // 10, "%d -> %d" % (n, s["fila"]))
        check("B %d: columna" % n, s["columna"] == (n - 1) % 10 + 1, "%d -> %d" % (n, s["columna"]))
        # la fila y la columna tienen que dar el numero  (fila*10 + columna = n)
        check("B %d: fila*10 + columna cuadra" % n, s["fila"] * 10 + s["columna"] == n,
              "%d -> %d" % (n, s["fila"] * 10 + s["columna"]))

# Fuera de la tabla
for malo in ("101", "200", "999"):
    s = motor.decidir_6_3_sitio(malo, SABER)
    check("B fuera: %s" % malo, s["conclusion"] == "fuera_de_la_tabla", s["conclusion"])
s = motor.decidir_6_3_sitio("manzana", SABER)
check("B no es numero", s["conclusion"] == "no_es_un_numero", s["conclusion"])
s = motor.decidir_6_3_sitio("0", SABER)
check("B el cero no esta en la tabla", s["conclusion"] == "se_puede" and s["esta_en_la_tabla"] is False)


# ---------------------------------------------------------------------------
# C. LA COHERENCIA: EL MISMO NUMERO POR TODAS LAS PUERTAS  (lo que pidio Carlos)
# ---------------------------------------------------------------------------
# Si el lector sabe leer 47, lo tiene que saber en TODAS las ordenes.  Antes de la 6.3 habia
# cuatro puertas que decian que no (cifra_de, comparar_cifras, comparar_numeros, dedos).
for n in (10, 11, 25, 47, 60, 99, 100):
    # puerta 1: nombre:
    p1 = motor.construir_nombre_hasta_cien(n, SABER)
    # puerta 2: palabra: (cifra -> palabra)
    p2 = motor.decidir_3_1_palabra(str(n), SABER).get("palabra")
    # puerta 3: sitio: (el numero leido)
    s = motor.decidir_6_3_sitio(str(n), SABER)
    p3 = s.get("palabra")
    # puerta 4: comparar_cifras (se lee el numero para compararlo)
    c = motor.decidir_4_2_comparar_cifras(str(n), "0", SABER)
    p4 = c.get("palabra_a")
    check("C %d: las puertas leen LO MISMO" % n, p1 == p2 == p3 == p4,
          "nombre=%s palabra=%s sitio=%s comparar=%s" % (p1, p2, p3, p4))
    # y la vuelta: cifra: de esa palabra tiene que dar el numero otra vez
    v = motor.decidir_3_1_cifra(p1, SABER).get("cifra")
    check("C %d: la vuelta da el numero" % n, v == str(n), "%s -> %s" % (p1, v))

# La cifra de una cantidad de dos cifras (puerta 5: cifra_de)
for n in (10, 47, 100):
    r = motor.decidir_3_1_cifra_de(escena_de_n(n), SABER)
    check("C %d: cifra_de YA lee la cantidad" % n,
          r["conclusion"] == "cifra" and r["cifra"] == str(n),
          "%d -> %s / %s" % (n, r["conclusion"], r.get("cifra")))

# Y los dedos con una cifra de dos digitos (puerta 6)
r = motor.decidir_7_1_dedos("47", "3", SABER)
check("C dedos: 47 + 3 YA funciona", r["conclusion"] == "se_puede" and r["total_valor"] == 50,
      "%s / %s" % (r["conclusion"], r.get("total_valor")))

# Y lo que NO cambio (el limite esta bien puesto)
check("C derivar sigue siendo de una cifra",
      motor.decidir_7_2_derivar("47", "3", SABER)["conclusion"] == "necesito_las_columnas")
check("C los numeros de la 3.3 siguen siendo 0..9",
      motor.decidir_3_3_siguiente("cuarenta y siete", SABER)["conclusion"] == "sin_numero")
check("C recitar 47 si (es la lista de contar)",
      motor.decidir_2_2_recitar("cuarenta y siete", SABER)["conclusion"] == "recitado")
check("C cuantos sigue siendo de CANTIDADES (47 no es un objeto)",
      True)   # se comprueba en el D de abajo con la excepcion


# ---------------------------------------------------------------------------
# D. EL EXPLICADOR Y LAS ORDENES DE CANTIDAD
# ---------------------------------------------------------------------------
t = motor.explicar_6_3_sitio("47", SABER)
check("D1 ensena el sitio", "fila 4" in t or "fila 4" in t)
check("D2 ensena la tabla", "LA TABLA DE 100" in t)
check("D3 ensena a leerlo", "cuarenta y siete" in t)
check("D4 ensena que el sitio es el valor", "EL SITIO ES EL VALOR" in t)
check("D5 comprobacion", "COMPROBACION: 47 son 4 decenas y 7 unidades" in t)

t = motor.explicar_6_3_tabla(SABER)
check("D6 la tabla entera", "fila 9" in t and "100" in t)
check("D7 dice como se recorre", "DE DIEZ EN DIEZ" in t and "DE UNO EN UNO" in t)

try:
    motor.escena_cantidad("47", SABER)
    check("D8 '47' NO es un nombre de objeto", False, "no salto la excepcion")
except motor.EntradaDelGrupoEquivocado:
    check("D8 '47' NO es un nombre de objeto (lo dice)", True)

# Y un objeto con digitos sigue siendo un objeto
e = motor.escena_cantidad("silla_1, silla_2", SABER)
check("D9 'silla_1' SI es un objeto", len(e) == 2, len(e))


# ---------------------------------------------------------------------------
print("PRUEBAS 6.3  -  LA TABLA DE 100")
print("=" * 60)
for f in fallos[:20]:
    print("  FALLA:  " + f)
if len(fallos) > 20:
    print("  ... y %d mas" % (len(fallos) - 20))
print("-" * 60)
print("  %d de %d bien, %d fallan" % (len(pruebas) - len(fallos), len(pruebas), len(fallos)))
print("UNIDAD 6.3: %d/%d" % (len(pruebas) - len(fallos), len(pruebas)))
if fallos:
    print("RESULTADO: HAY FALLOS")
    sys.exit(1)
print("RESULTADO: TODO BIEN")
