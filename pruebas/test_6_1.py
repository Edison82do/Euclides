# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 6.1 - LA SECUENCIA HASTA 100 (la regla y sus excepciones).

Lo que esta unidad tiene que dejar claro:
  - La secuencia de contar llega del UNO al CIEN.
  - Los nombres NO estan memorizados: se CONSTRUYEN con tres formaciones.
  - Solo hay que saberse unas pocas (1-10, 11-15, 20, 100 y las decenas).
  - El ERROR DE DECENA: donde la regla se rompe (29 -> treinta, no 'veintidiez').

LA PRUEBA DE HIERRO: construir el nombre de los 100 y volver (nombre -> numero) tiene que dar el
mismo numero, sin colisiones.  Y ademas, una lista ESCRITA A MANO de los nombres que importan.
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
SEC = SABER["secuencia_de_conteo"]["palabras"]


def nombre(n):
    return motor.construir_nombre_hasta_cien(n, SABER)


print("=" * 78)
print("UNIDAD 6.1 - LA SECUENCIA DE CONTAR HASTA 100")
print("=" * 78)

# ------------------------------------------------- A) la secuencia, escrita a mano
print("\nA) LOS NOMBRES QUE IMPORTAN (escritos A MANO, no copiados del sistema)")
A_MANO = [
    (1, "uno"), (2, "dos"), (9, "nueve"), (10, "diez"),
    (11, "once"), (12, "doce"), (13, "trece"), (14, "catorce"), (15, "quince"),
    (16, "dieciseis"), (17, "diecisiete"), (18, "dieciocho"), (19, "diecinueve"),
    (20, "veinte"), (21, "veintiuno"), (22, "veintidos"), (25, "veinticinco"),
    (28, "veintiocho"), (29, "veintinueve"),
    (30, "treinta"), (31, "treinta y uno"), (35, "treinta y cinco"),
    (40, "cuarenta"), (44, "cuarenta y cuatro"),
    (50, "cincuenta"), (60, "sesenta"), (66, "sesenta y seis"),
    (70, "setenta"), (77, "setenta y siete"),
    (80, "ochenta"), (88, "ochenta y ocho"),
    (90, "noventa"), (99, "noventa y nueve"), (100, "cien"),
]
for n, esperado in A_MANO:
    comprobar("A el %d se llama '%s'" % (n, esperado), nombre(n), esperado)

# --------------------------------------------------------------- B) la regla
print("\nB) LAS TRES FORMACIONES (como se construye, no como se memoriza)")
for n, formacion in [(16, "dieci"), (17, "dieci"), (18, "dieci"), (19, "dieci"),
                     (21, "veinti"), (22, "veinti"), (26, "veinti"), (29, "veinti"),
                     (31, "decena_y_unidad"), (45, "decena_y_unidad"), (98, "decena_y_unidad")]:
    info = motor.de_donde_sale_el_nombre(n, SABER)
    comprobar("B el %d se CONSTRUYE con '%s'" % (n, formacion), info["tipo"], formacion)

for n in [1, 7, 10, 11, 15, 20, 30, 50, 90, 100]:
    info = motor.de_donde_sale_el_nombre(n, SABER)
    comprobar("B el %d NO se construye: hay que SABERLO (%s)" % (n, info["tipo"]),
              info["tipo"] in ("memorizada", "decena"), True)

# El pegote: la unidad que se pega es la PALABRA, no la cifra.
info = motor.de_donde_sale_el_nombre(26, SABER)
comprobar("B en 'veintiseis' lo que se pega es la PALABRA 'seis'", info["piezas"]["unidad"], "seis")

# ------------------------------------------------------- C) la vuelta
print("\nC) LA VUELTA: del nombre al numero")
for palabra, esperado in [("cuarenta y siete", 47), ("veintidos", 22), ("cien", 100),
                          ("uno", 1), ("treinta", 30), ("noventa y nueve", 99)]:
    r = motor.explicar_6_1_numero(palabra, SABER)
    comprobar("C '%s' es el %d" % (palabra, esperado),
              "RESULTADO: %d" % esperado in r, True)
comprobar("C 'pepito' no es un nombre -> lo dice",
          "no_lo_se" in motor.explicar_6_1_numero("pepito", SABER), True)

# ------------------------------------------------------ D) los saltos de decena
print("\nD) EL ERROR DE DECENA (donde la regla se rompe)")
comprobar("D 20 NO es 'veintidiez'", nombre(20), "veinte")
comprobar("D 30 NO es 'veintidiez'", nombre(30), "treinta")
comprobar("D despues de veintinueve viene treinta",
          (nombre(29), nombre(30)), ("veintinueve", "treinta"))
comprobar("D despues de treinta y nueve viene cuarenta",
          (nombre(39), nombre(40)), ("treinta y nueve", "cuarenta"))
comprobar("D despues de noventa y nueve viene cien",
          (nombre(99), nombre(100)), ("noventa y nueve", "cien"))
comprobar("D y NO existe ningun nombre que empiece por 'veintidiez'",
          any("veintidiez" in (p or "") for p in SEC), False)

# ----------------------------------------------------------- E) el techo
print("\nE) EL TECHO: hasta cien")
comprobar("E el 100 si se llama", nombre(100), "cien")
comprobar("E el 101 NO: fuera_de_mi_secuencia",
          motor.construir_nombre_hasta_cien(101, SABER), None)
comprobar("E y el 0 tampoco (la secuencia de contar empieza en uno)",
          motor.construir_nombre_hasta_cien(0, SABER), None)
# UNIDAD 6.7 (LA CENTENA): la lista subio de 100 a MIL nombres.
comprobar("E la lista tiene 1000 palabras (subio de 100 en la 6.7)", len(SEC), 1000)
comprobar("E y son todas distintas (no hay dos iguales)", len(set(SEC)), 1000)

# ============================================ LA PRUEBA DE HIERRO (F)
print("\n" + "=" * 78)
print("F) PRUEBA DE HIERRO: los 100, ida y vuelta")
print("=" * 78)
malas = 0
for n in range(1, 101):
    p = nombre(n)
    if not p:
        malas += 1
        print("    el %d no tiene nombre" % n)
        continue
    # volver: buscar el numero a partir del nombre
    vuelta = None
    for k in range(1, 101):
        if nombre(k) == p:
            vuelta = k
            break
    if vuelta != n:
        malas += 1
        print("    el %d dice '%s' y la vuelta da %s" % (n, p, vuelta))
comprobar("F1 los 100 nombres van y vuelven sin colisiones", malas, 0)

print("\n" + "=" * 78)
print("UNIDAD 6.1: %d/%d correctos" % (BIEN, BIEN + MAL))
print("=" * 78)
sys.exit(1 if MAL else 0)
