# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 4.2 - COMPARAR NUMEROS (cifras).

Lo que esta unidad tiene que dejar claro:
  - Dos CIFRAS se relacionan con un SIMBOLO: > (mayor que), < (menor que), = (igual a).
  - De donde sale: EN LA SECUENCIA DE NUMEROS, EL QUE VIENE DESPUES ES EL MAYOR (unidad 3.3).
  - Y CUADRA CON LAS CANTIDADES (unidad 4.1): 3 > 2 porque tres cosas son mas que dos.
  - Los simbolos van SOLO entre CIFRAS; las cantidades se dicen con palabras.

Se corre asi:   py -3 pruebas/test_4_2.py
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

from motor import (cargar_conocimiento, decidir_4_1_comparar, decidir_4_2_comparar_cifras,  # noqa: E402
                   escena_0_2, explicar_pregunta)

BIEN = [0]
TOTAL = [0]

# Nombres de objeto para construir colecciones de un tamano dado (los uso YO, en la prueba).
NOMBRES = ["o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8", "o9", "o10"]


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

    # ------------------------------------------------------------------ los tres simbolos
    print("=" * 76)
    print("A) LOS TRES SIMBOLOS")
    print("=" * 76)
    comprobar("A1 3 > 2", decidir_4_2_comparar_cifras("3", "2", saber).get("simbolo"), ">")
    comprobar("A2 2 < 3", decidir_4_2_comparar_cifras("2", "3", saber).get("simbolo"), "<")
    comprobar("A3 4 = 4", decidir_4_2_comparar_cifras("4", "4", saber).get("simbolo"), "=")
    comprobar("A4 el cero tambien: 0 < 1", decidir_4_2_comparar_cifras("0", "1", saber).get("simbolo"), "<")
    comprobar("A5 9 > 7 (numeros grandes)", decidir_4_2_comparar_cifras("9", "7", saber).get("simbolo"), ">")
    print("")

    # ------------------------------------------------------------------ de donde sale
    print("=" * 76)
    print("B) DE DONDE SALE: el sitio en la secuencia de numeros")
    print("=" * 76)
    r = decidir_4_2_comparar_cifras("3", "2", saber)
    comprobar("B1 el 'tres' esta en el sitio 3", r.get("sitio_a"), 3)
    comprobar("B2 el 'dos' esta en el sitio 2", r.get("sitio_b"), 2)
    comprobar("B3 el que viene DESPUES es el mayor", r.get("sitio_a") > r.get("sitio_b"), True)
    comprobar("B4 y la palabra de la cifra 3 es 'tres'", r.get("palabra_a"), "tres")
    r = decidir_4_2_comparar_cifras("2", "5", saber)
    comprobar("B5 2 < 5 porque el cinco viene despues", (r.get("sitio_a"), r.get("sitio_b")), (2, 5))
    print("")

    # ------------------------------------------------------------------ COHERENCIA con 4.1
    print("=" * 76)
    print("C) LA PRUEBA DE HIERRO: TODAS las parejas cuadran con las CANTIDADES (4.1)")
    print("=" * 76)
    malas = 0
    probadas = 0
    for a in range(0, 10):
        for b in range(0, 10):
            r = decidir_4_2_comparar_cifras(str(a), str(b), saber)
            # lo que dice el SIMBOLO (4.2)
            por_simbolo = r.get("conclusion")
            # lo que dicen las CANTIDADES de verdad (4.1), con colecciones de objetos reales
            por_cantidad = decidir_4_1_comparar(coleccion(a), coleccion(b), saber)["conclusion"]
            equivalencia = {"mayor": "mas", "menor": "menos", "iguales": "tantos_como"}
            probadas += 1
            if equivalencia[por_simbolo] != por_cantidad:
                malas += 1
                print("       NO CUADRA: %d vs %d -> simbolo=%s  cantidad=%s"
                      % (a, b, por_simbolo, por_cantidad))
    comprobar("C1 las %d parejas de cifras (0..9) cuadran con las cantidades" % probadas, malas, 0)
    comprobar("C2 y son 100 parejas probadas", probadas, 100)
    r = decidir_4_2_comparar_cifras("7", "2", saber)
    comprobar("C3 el sistema lo declara: 'cuadra' = True", r.get("cuadra"), True)
    print("")

    # ------------------------------------------------------------------ la boca del simbolo
    print("=" * 76)
    print("D) LA BOCA DEL SIMBOLO MIRA AL MAYOR")
    print("=" * 76)
    salida = explicar_pregunta("comparar_cifras: 3 / 2", saber)
    comprobar("D1 lo dice: la boca mira al 3", "mira al numero MAYOR, que es el 3" in salida, True)
    salida = explicar_pregunta("comparar_cifras: 2 / 3", saber)
    comprobar("D2 y al reves, mira al 3", "mira al numero MAYOR, que es el 3" in salida, True)
    comprobar("D3 la lectura en palabras va con el simbolo", "2 < 3" in salida and "menor que" in salida, True)
    print("")

    # ------------------------------------------------------------------ trampas
    print("=" * 76)
    print("E) TRAMPAS")
    print("=" * 76)
    r = decidir_4_2_comparar_cifras("10", "2", saber)
    comprobar("E1 MEJORA 6.3: el 10 YA se compara (diez es mayor que dos)",
              r["conclusion"], "mayor")
    r = decidir_4_2_comparar_cifras("3", "tres", saber)
    comprobar("E2 MEJORA (5.3): 'tres' y 3 son EL MISMO numero -> =", r["conclusion"], "iguales")
    r = decidir_4_2_comparar_cifras("3", "manzana", saber)
    comprobar("E3 TRAMPA: 'manzana' tampoco", r["conclusion"], "cifra_desconocida")
    salida = explicar_pregunta("comparar_cifras: 3", saber)
    comprobar("E4 sin la barra -> NO ENTIENDO (comparar son DOS)", "NO ENTIENDO" in salida, True)
    print("")

    # ------------------------------------------------------------------ simbolos vs palabras
    print("=" * 76)
    print("F) SIMBOLOS CON CIFRAS, PALABRAS CON CANTIDADES (no se mezclan)")
    print("=" * 76)
    salida = explicar_pregunta("comparar_cifras: 3 / 2", saber)
    comprobar("F1 con cifras: sale el SIMBOLO >", "RESULTADO: >" in salida, True)
    salida = explicar_pregunta("comparar: a,b,c / d,e", saber)
    comprobar("F2 con cantidades: sale la PALABRA 'mas'", "RESULTADO: mas" in salida, True)
    comprobar("F3 y la 4.2 recuerda que los simbolos son de cifras",
              "van entre CIFRAS" in salida, True)
    print("")

    # ------------------------------------------------------------------ robustez
    print("=" * 76)
    print("G) ROBUSTEZ: contesta a todo, no revienta")
    print("=" * 76)
    for q in ["comparar_cifras: 0 / 0", "comparar_cifras: 9 / 0", "comparar_cifras: / ",
              "comparar_cifras: a / b", "comparar_cifras: 1.5 / 2", "comparar_cifras: -1 / 2"]:
        salida = explicar_pregunta(q, saber)
        comprobar("G '%s'" % q, ("RESULTADO:" in salida or "NO ENTIENDO" in salida), True)
    print("")

    print("=" * 76)
    print("UNIDAD 4.2: %d/%d correctos" % (BIEN[0], TOTAL[0]))
    print("=" * 76)
    return 0 if BIEN[0] == TOTAL[0] else 1


if __name__ == "__main__":
    sys.exit(main())
