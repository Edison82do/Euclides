# -*- coding: utf-8 -*-
"""
PRUEBAS DE LA FASE U.4 DEL PLAN U: UNA SOLA TABLA DE PUERTAS.
El plan y sus trampas: diario/2026-10-08-paso-U4-una-sola-tabla-de-puertas.md
Pocas y representativas (decision de Carlos para lo nuevo).  Python solo es TESTIGO.
"""
import os
import sys
import tempfile
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)
TMP = tempfile.mkdtemp(prefix="u4_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria propia (vacia)
import motor  # noqa: E402
import probar  # noqa: E402
import comparar_puertas  # noqa: E402

BIEN = MAL = 0
SABER = motor.cargar_conocimiento()


def comprobar(nombre, obtenido, esperado):
    global BIEN, MAL
    if obtenido == esperado:
        BIEN += 1
        print("  BIEN    %s" % nombre)
    else:
        MAL += 1
        print("  FALLA   %s\n          obtenido: %r\n          esperado: %r" % (nombre, obtenido, esperado))


def P(t):
    return probar.preguntar(t, SABER)[0]


def X(t):
    return motor.explicar_pregunta(t, SABER)


def main():
    print("A - UNA SOLA TABLA (las dos salidas recorren la misma)")
    comprobar("A1 explicar_pregunta vive en UNA parte (puertas.py)", motor._DONDE_ESTA["explicar_pregunta"],
              "partes.puertas")
    src = open(os.path.join(RAIZ, "probar.py"), encoding="utf-8").read()
    comprobar("A2 probar.py ya no tiene su segunda cadena de puertas",
              ("_preguntar_por_las_puertas" in src, "motor.responder_pregunta(texto, saber)" in src), (False, True))
    comprobar("A3 las puertas que solo tenia una cadena estan en las dos: listas",
              (P("listas"), X("listas").startswith("PREGUNTA") or "lista" in X("listas").lower()), ("las_listas", True))
    # en una muestra de mis_casos (uno de cada 12): si el explicador dice que decidio el resolvedor, la respuesta corta
    # es la del resolvedor; si no, la de la puerta (las dos salidas deciden con la MISMA regla)
    casos = probar.leer_casos(os.path.join(RAIZ, "mis_casos.txt"))[::12]
    mal = []
    for c in casos:
        t = c["texto"]
        if not t or t.lower().startswith(("aprender", "olvidar")):
            continue
        e = X(t)
        a = P(t)
        if e.startswith("(la puerta vieja decia"):
            cuerpo = motor._pu_cuerpo(t) if motor._pu_simbolica(motor._pu_cuerpo(t)) else t
            if a != motor._pu_r_resolver(cuerpo, SABER)[0]:
                mal.append(t)
        elif not motor.es_orden_resolver(t):
            puerta = motor._pu_elegir_puerta(t.strip(), SABER, motor._pu_simbolica(t.strip()))
            if puerta["nombre"] != "simbolica" and a != motor._pu_responder_puerta(puerta, t.strip(), SABER)[0]:
                mal.append(t)
    comprobar("A4 en %d casos de mis_casos las dos salidas eligen lo mismo" % len(casos), mal, [])

    print("\nB - EL DIAGNOSTICO (lo que decia antes)")
    for q, esperado in (("1/2 x n = 3", "n = 6"),                      # E.5 leia 1/2 como 1 : 2 -> no_sale
                        ("n + 1/2 = 3/4", "n = 1/4"),
                        ("n : 3 = 1/2", "n = 3/2"),
                        ("a + b = 9; a : b = 2", "a = 6, b = 3"),      # lo cogia la puerta de los OBJETOS (0.2)
                        ("2 x (n + 3) = 2 x n + 6", "cualquiera"),      # todavia_no
                        ("a + b = a + b + 1", "ninguna")):              # todavia_no
        comprobar("B %s -> %s" % (q, esperado), P(q), esperado)
    comprobar("B la explicacion dice que la puerta vieja no llegaba y cual era",
              X("1/2 x n = 3").startswith("(la puerta vieja decia") or "resolvedor" in X("1/2 x n = 3"), True)

    print("\nC - LA REGLA DE LA RED: nada viejo cambia; el ano se respeta")
    comprobar("C1 2 x 3 - 4 x 5 sigue todavia_no (el ano: se baja de cero)", P("2 x 3 - 4 x 5"), "todavia_no")
    comprobar("C1b 12 : 3 + 1: desde M.22 (2.28) es del ano: lo coge el resolvedor", P("12 : 3 + 1"), "5")
    comprobar("C2 ecuacion: 3 x ? = 13 sigue no_entero", P("ecuacion: 3 x ? = 13"), "no_entero")
    comprobar("C3 3 x n = 13 sigue no_sale (no hay entero)...", P("3 x n = 13"), "no_sale")
    comprobar("C4 ... y la explicacion ensena tambien lo del resolvedor (13/3)", "n = 13/3" in X("3 x n = 13"), True)
    comprobar("C5 8 : 0 sigue no_se_puede", P("8 : 0"), "no_se_puede")
    comprobar("C6 (a + 5) x 2 = 26 sigue por E.5 (8)", (P("(a + 5) x 2 = 26"), motor.puerta_de("(a + 5) x 2 = 26", SABER)),
              ("8", "letra"))
    comprobar("C7 a + b = 10; a - b = 12 sigue ninguna (con numeros para contar)...", P("a + b = 10; a - b = 12"),
              "ninguna")
    comprobar("C8 ... y ensena que con negativos si hay (a = 11, b = -1)", "a = 11, b = -1" in X("a + b = 10; a - b = 12"),
              True)
    comprobar("C9 0 x n = 5: E.5 decia no_sale; se contradice: ninguna", P("0 x n = 5"), "ninguna")

    print("\nD - IDENTIDADES Y CONTRADICCIONES (desarrollar con la distributiva)")
    for q, esperado in (("4 x (n + 2) - 8 = 4 x n", "cualquiera"),
                        ("2 x (a + b) = 2 x a + 2 x b", "cualquiera"),               # dos letras
                        ("(n + 1) x (n + 1) = n x n + 2 x n + 1", "cualquiera"),     # no lineal
                        ("0 x n = 0", "cualquiera"),
                        ("5 x (a - 1) = 5 x a - 3", "ninguna"),
                        ("n : n = 1", "todavia_no"),                                  # una letra divide: no se desarrolla
                        ("a + b = 10; 2 x (a + b + c) = 2 x a + 2 x b + 2 x c", "todavia_no")):  # c puede ser cualquiera
        comprobar("D %s -> %s" % (q, esperado), P(q), esperado)
    comprobar("D una identidad en un sistema no dice nada: quedan las 11 parejas de a + b = 10",
              P("a + b = 10; 2 x (a + b) = 2 x a + 2 x b").count(";"), 10)
    comprobar("D la explicacion lo dice", "los dos lados son LO MISMO" in X("4 x (n + 2) - 8 = 4 x n"), True)

    print("\nE - E.5, TRADUCTOR AL MODELO (lee con el lector unico)")
    comprobar("E1 x/2 + 1 = 3 sigue por E.5", (P("x/2 + 1 = 3"), motor.puerta_de("x/2 + 1 = 3", SABER)), ("4", "letra"))
    comprobar("E2 con fracciones ya no es de E.5", motor.puerta_de("1/2 x n = 3", SABER) != "letra", True)
    comprobar("E3 '2n' no es de E.5 (por sin escribir): lo resuelve el resolvedor", P("2n = 6"), "n = 3")
    comprobar("E4 n = 12/3: la fraccion en su forma mas simple", P("n = 12/3"), "n = 4")

    print("\nF - RESPUESTAS FALSAS DE PUERTAS VIEJAS (las encontro comparar)")
    comprobar("F1 calcular: 1/2 + 0.25 (decia 2: leia '2 + 0')", P("calcular: 1/2 + 0.25"), "3/4")
    comprobar("F2 ecuacion: 0.5 + ? = 12 (decia 7)", P("ecuacion: 0.5 + ? = 12"), "el hueco = 11.5")
    comprobar("F3 ecuacion: -2 x ? = 12 (decia 6)", P("ecuacion: -2 x ? = 12"), "el hueco = -6")
    comprobar("F4 ecuacion: ? : 0 = 3 sigue imposible (el resolvedor: ninguna; antes no_cuadra)",
              (P("ecuacion: ? : 0 = 3"), motor._pu_r_resolver("? : 0 = 3", SABER)[0]), ("imposible", "ninguna"))
    v, explicadas, distintas = comparar_puertas.comparar(SABER, ensenar=False)
    comprobar("F5 comparar: en %d casos simbolicos de mis_casos y mis_pruebas, ninguna diferencia sin explicar" % v,
              [(a, l, t) for a, l, t, _, _, _ in distintas], [])

    print("\nG - LA REGLA DE PRUDENCIA CON PALABRAS")
    camion = "resolver: Un camion lleva 12 cajas. Cada caja pesa 96 kilos. Cuanto pesan las cajas?"
    comprobar("G1 'cada caja pesa' y 'las cajas pesan' (decia 96 kilos): no entiendo", P(camion), "no_entiendo")
    comprobar("G2 ... y dice que numero y que frase", "el 12 de 'un camion lleva 12 cajas'" in X(camion), True)
    comprobar("G3 al reves (decia 96 kilos): no entiendo",
              P("resolver: Un camion lleva 12 cajas. Las cajas pesan 96 kilos. Cuanto pesa cada caja?"), "no_entiendo")
    gaste = "resolver: Tengo 50 pesos. Gaste la mitad. Cuanto me queda?"
    comprobar("G4 'gaste la mitad' no se entiende y se ignoraba (decia 50 pesos): no entiendo", P(gaste), "no_entiendo")
    comprobar("G5 ... diciendo la frase", "'gaste la mitad'" in X(gaste), True)
    comprobar("G6 con 'gasto' (vocabulario) sale", P("resolver: Tengo 50 pesos. Gasto la mitad. Cuanto me queda?"),
              "25 pesos")
    comprobar("G7 lo que sobra de verdad (la edad) sigue sobrando",
              P("resolver: Ana tiene 9 anos. Luis tiene 6 canicas y Pedro 4. Cuantas canicas tienen Luis y Pedro?"),
              "10 canicas")
    comprobar("G8 lo de otro dueno sigue sobrando (los caramelos de Ana)",
              P("problema: Ana tiene 6 caramelos y Luis tiene 4. Ana le da 2 a Luis. Cuantos tiene Luis?"),
              "6 caramelos")

    print("\nH - 20 PROBLEMAS SIMBOLICOS NUEVOS (sin 'resolver:'; los que salen, contra el testigo)")
    veinte = (("5 x n - 7 = 2 x n + 8", "n = 5"), ("3 x (x - 2) = x + 10", "x = 8"), ("y/4 + 3 = y/2 - 1", "y = 16"),
              ("0.5 x m + 1.25 = 3", "m = 3.5"), ("-3 x k + 4 = 19", "k = -5"), ("2/3 x p = 3/4", "p = 9/8"),
              ("a + b = 17; a - b = 5", "a = 11, b = 6"), ("2 x a + 3 x b = 23; a - b = 4", "a = 7, b = 3"),
              ("x + y + z = 12; x - y = 1; y - z = 1", "x = 5, y = 4, z = 3"),
              ("a + b + c = 30; a = 2 x b; c = b + 2", "a = 14, b = 7, c = 9"),
              ("p + q = 1.5; p - q = 0.25", "p = 0.875, q = 0.625"), ("x + y = -2; x - y = 6", "x = 2, y = -4"),
              ("n x n = 81", "n = 9"), ("n x (n + 1) = 56", "n = 7"), ("a x b = 18; a + b = 9", "a = 3, b = 6; a = 6, b = 3"),
              ("4 x (n + 2) - 8 = 4 x n", "cualquiera"), ("5 x (a - 1) = 5 x a - 3", "ninguna"),
              ("(x + 2) x (x + 2) = x x x + 4 x x + 4", "cualquiera"), ("3 x n + 1/2 = n + 2.5", "n = 1"),
              ("a + b = 8; 3 x a + 3 x b = 20", "ninguna"))
    mal = [(q, P(q)) for q, e in veinte if P(q) != e]
    comprobar("H %d/20 salen bien" % (20 - len(mal)), mal, [])

    print("\nI - EL TIEMPO (cada pregunta por debajo de 3 s)")
    lentas = []
    for q in ("x + y + z = 12; x - y = 1; y - z = 1", "n x (n + 1) = 56", "(x + 2) x (x + 2) = x x x + 4 x x + 4", camion):
        t0 = time.time()
        P(q)
        X(q)
        if time.time() - t0 > 3:
            lentas.append(q)
    comprobar("I nada tarda mas de 3 s", lentas, [])

    print("\nTOTAL: %d/%d" % (BIEN, BIEN + MAL))
    return 0 if MAL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
