# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 5.2 - LA SUMA.

Lo que esta unidad tiene que dejar claro:
  - Sumar es JUNTAR.  El signo + se lee 'mas'; el signo = se lee 'igual a'.
  - El = significa EQUIVALENCIA (que las dos cosas son lo mismo), NO 'pon el resultado'.
  - Los terminos: SUMANDOS (los que se juntan) y SUMA (el resultado).
  - Hay DOS estructuras: AGREGACION (juntar dos montones que ya estan) y AUMENTACION (el monton crece).
  - Y LA VUELTA VERIFICA: partiendo la suma tiene que salir la pareja de los sumandos (unidad 5.1).

Se corre asi:   py -3 pruebas/test_5_2.py
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

from motor import (cargar_conocimiento, decidir_5_1_componer, decidir_5_2_anadir,  # noqa: E402
                   decidir_5_2_sumar, escena_0_2, explicar_pregunta)

BIEN = [0]
TOTAL = [0]

# UNIDAD 6.1: la secuencia llega a 100; hacen falta nombres de sobra para probar "pasa de cien".
NOMBRES = ["o%d" % i for i in range(1, 121)]


def comprobar(titulo, obtenido, esperado):
    ok = obtenido == esperado
    BIEN[0] += ok
    TOTAL[0] += 1
    print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
    if not ok:
        print("       esperado=%s  obtenido=%s" % (esperado, obtenido))
    return ok


def coleccion(n):
    return escena_0_2(",".join(NOMBRES[:n]))


def main():
    saber = cargar_conocimiento()

    # ------------------------------------------------------------------ la cuenta
    print("=" * 76)
    print("A) SUMAR: el signo + y el signo =")
    print("=" * 76)
    r = decidir_5_2_sumar(coleccion(3), coleccion(2), saber)
    comprobar("A1 tres mas dos es cinco", r.get("expresion"), "3 + 2 = 5")
    comprobar("A2 los SUMANDOS son tres y dos", (r.get("sumando_a"), r.get("sumando_b")),
              ("tres", "dos"))
    comprobar("A3 la SUMA es cinco", r.get("suma"), "cinco")
    comprobar("A4 TRAMPA: da igual el orden, la SUMA es la misma (conmutatividad)",
              (decidir_5_2_sumar(coleccion(2), coleccion(3), saber).get("suma"),
               decidir_5_2_sumar(coleccion(2), coleccion(3), saber).get("expresion")),
              ("cinco", "2 + 3 = 5"))
    comprobar("A4b y respeta el orden que le das (no reordena por su cuenta)",
              decidir_5_2_sumar(coleccion(3), coleccion(2), saber).get("expresion"), "3 + 2 = 5")
    r = decidir_5_2_sumar(coleccion(0), coleccion(4), saber)
    comprobar("A5 con una parte vacia: 0 + 4 = 4", r.get("expresion"), "0 + 4 = 4")
    print("")

    # ------------------------------------------------------------------ las dos estructuras
    print("=" * 76)
    print("B) LAS DOS ESTRUCTURAS DE LA SUMA (mismo numero, distinta historia)")
    print("=" * 76)
    ag = decidir_5_2_sumar(coleccion(3), coleccion(2), saber)
    au = decidir_5_2_anadir(coleccion(3), coleccion(2), saber)
    comprobar("B1 agregacion: el resultado es 5", ag.get("suma"), "cinco")
    comprobar("B2 aumentacion: el resultado tambien es 5", au.get("suma"), "cinco")
    comprobar("B3 las dos dan la MISMA expresion", ag.get("expresion"), au.get("expresion"))
    comprobar("B4 pero son estructuras distintas", ag["conclusion"] != au["conclusion"], True)
    salida = explicar_pregunta("sumar: a,b,c / d,e", saber)
    comprobar("B5 la agregacion se llama AGREGACION", "ESTRUCTURA: AGREGACION" in salida, True)
    salida = explicar_pregunta("anadir: a,b,c / d,e", saber)
    comprobar("B6 la aumentacion se llama AUMENTACION", "ESTRUCTURA: AUMENTACION" in salida, True)
    comprobar("B7 y cuenta la historia primero/luego/ahora",
              "PRIMERO: habia tres" in salida and "AHORA: hay cinco" in salida, True)
    print("")

    # ------------------------------------------------------------------ el igual
    print("=" * 76)
    print("C) EL SIGNO = ES EQUIVALENCIA, NO 'PON EL RESULTADO'")
    print("=" * 76)
    salida = explicar_pregunta("sumar: a,b,c / d,e", saber)
    comprobar("C1 el sistema lo dice claramente", "NO es 'haz la cuenta y pon el resultado'" in salida, True)
    comprobar("C2 y da el ejemplo al reves (5 = 3 + 2)", "5 = 3 + 2 es igual de cierto" in salida, True)
    comprobar("C3 dice que el + significa juntar", "significa JUNTAR" in salida, True)
    print("")

    # ------------------------------------------------------------------ la vuelta verifica
    print("=" * 76)
    print("D) LA VERIFICACION: la vuelta (unidad 5.1)")
    print("=" * 76)
    r = decidir_5_2_sumar(coleccion(3), coleccion(2), saber)
    comprobar("D1 el sistema comprueba que la pareja esta al partir", r.get("verificacion"), True)
    comprobar("D2 y las parejas de cinco son las de la 5.1", r.get("parejas_de_la_suma"),
              [(0, 5), (1, 4), (2, 3)])
    salida = explicar_pregunta("sumar: a,b,c / d,e", saber)
    comprobar("D3 y lo ENSENA en la salida", "VERIFICACION (por la vuelta" in salida, True)
    comprobar("D4 diciendo que la pareja 'tres y dos' esta entre ellas",
              "esta entre ellas: SI" in salida, True)
    print("")

    # ------------------------------------------------------------------ PRUEBA DE HIERRO
    print("=" * 76)
    print("E) LA PRUEBA DE HIERRO: la suma y el componer (5.1) dan LO MISMO")
    print("=" * 76)
    malas = 0
    probadas = 0
    for a in range(0, 11):
        for b in range(0, 11 - a):
            s = decidir_5_2_sumar(coleccion(a), coleccion(b), saber)
            c = decidir_5_1_componer(coleccion(a), coleccion(b), saber)
            probadas += 1
            if s.get("suma") != c.get("total"):
                malas += 1
                print("       NO CUADRA: %d + %d -> suma=%s  componer=%s"
                      % (a, b, s.get("suma"), c.get("total")))
    comprobar("E1 las %d sumas (a+b<=10) coinciden con el componer" % probadas, malas, 0)
    comprobar("E2 y son 66 sumas probadas", probadas, 66)
    # Y todas verifican por la vuelta
    malas_v = 0
    for a in range(0, 11):
        for b in range(0, 11 - a):
            if not decidir_5_2_sumar(coleccion(a), coleccion(b), saber).get("verificacion"):
                malas_v += 1
    comprobar("E3 y las 66 verifican por la vuelta", malas_v, 0)
    # Y la expresion con cifras es correcta (salvo cuando la suma es diez, que no tiene cifra)
    malas_e = 0
    for a in range(0, 10):
        for b in range(0, 10 - a):
            r = decidir_5_2_sumar(coleccion(a), coleccion(b), saber)
            if r.get("expresion") != "%d + %d = %d" % (a, b, a + b):
                malas_e += 1
                print("       expresion mal: %s" % r.get("expresion"))
    comprobar("E4 las 55 expresiones con cifras (a+b<=9) son exactas", malas_e, 0)
    r = decidir_5_2_sumar(coleccion(3), coleccion(7), saber)
    comprobar("E5 con suma diez: se da la palabra y se avisa", r.get("total_sin_cifra"), True)
    comprobar("E6 y la expresion no miente", r.get("expresion"), "3 + 7 = diez")
    print("")

    # ------------------------------------------------------------------ condiciones y trampas
    print("=" * 76)
    print("F) CONDICIONES DE APLICACION Y TRAMPAS")
    print("=" * 76)
    r = decidir_5_2_sumar(coleccion(6), coleccion(6), saber)
    # UNIDAD 6.1: seis y seis SON doce, y doce ya se cuenta; el limite esta en cien.
    comprobar("F1 (MEJORA 6.1): seis y seis ya SI suman -> doce", r.get("suma"), "doce")
    # UNIDAD 6.7: el techo subio a MIL; 60+60 ya se puede.
    # (con nombres GENERADOS: la lista fija de arriba es corta)
    r = decidir_5_2_anadir(escena_0_2(",".join("o%d" % (i + 1) for i in range(600))), escena_0_2(",".join("o%d" % (i + 1) for i in range(600))), saber)
    comprobar("F2 TRAMPA: seiscientos y seiscientos (1200) pasa de MIL -> no_alcanza",
              r["conclusion"], "no_alcanza")
    salida = explicar_pregunta("sumar: a,b,c", saber)
    comprobar("F3 sin la barra -> NO ENTIENDO (hacen falta DOS)", "NO ENTIENDO" in salida, True)
    salida = explicar_pregunta("anadir: a,b,c", saber)
    comprobar("F4 lo mismo al anadir", "NO ENTIENDO" in salida, True)
    salida = explicar_pregunta("sumar: a,b,c,d,e,f / g,h,i,j", saber)
    comprobar("F5 pero seis y cuatro SI se suman (son diez)", "RESULTADO: 6 + 4 = diez" in salida, True)
    print("")

    # ------------------------------------------------------------------ identidad (0.1)
    print("=" * 76)
    print("G) PASA POR LA IDENTIDAD (unidad 0.1)")
    print("=" * 76)
    r = decidir_5_2_sumar(escena_0_2("casa(color=rojo), casa(forma=cuadrado), carro"),
                          escena_0_2("moto"), saber)
    comprobar("G1 la casa repetida es UNA: 2 + 1 = 3", r.get("expresion"), "2 + 1 = 3")
    print("")

    # ------------------------------------------------------------------ robustez
    print("=" * 76)
    print("H) ROBUSTEZ: contesta a todo, no revienta")
    print("=" * 76)
    for q in ["sumar: / ", "sumar: a / b", "sumar: / a,b", "sumar: a,b / ",
              "sumar:a,b/c,d", "anadir: / ", "anadir: a,b / c",
              "sumar: a,b,c,d,e,f,g,h,i,j,k / l"]:
        salida = explicar_pregunta(q, saber)
        comprobar("H '%s'" % q[:38], ("RESULTADO:" in salida or "NO ENTIENDO" in salida), True)
    print("")

    print("=" * 76)
    print("UNIDAD 5.2: %d/%d correctos" % (BIEN[0], TOTAL[0]))
    print("=" * 76)
    return 0 if BIEN[0] == TOTAL[0] else 1


if __name__ == "__main__":
    sys.exit(main())
