# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 5.3 - LAS TRES ENTRADAS (cantidad, cifra, palabra).

Lo que esta unidad tiene que dejar claro:
  - Lo que se escribe pertenece a UN GRUPO: cantidad (a,b,c), cifra (3) o palabra (tres).
  - UN OBJETO NO SE PUEDE LLAMAR COMO UN NUMERO.  Antes, 'sumar: 3 / 2' tomaba '3' y '2' por dos
    OBJETOS y contestaba '1 + 1 = 2' con toda seguridad: una respuesta creible y FALSA.  Lo cazo
    Carlos.  Ahora lo DICE.
  - Las ordenes de NUMEROS aceptan LA CIFRA O LA PALABRA (son el mismo numero): siguiente, anterior,
    recitar, comparar_numeros.
  - Y se puede OPERAR CON NUMEROS sin objetos: sumar_numeros, descomponer_numero.

Se corre asi:   py -3 pruebas/test_5_3.py
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

from motor import (EntradaDelGrupoEquivocado, cargar_conocimiento,  # noqa: E402
                   clasificar_nombre, decidir_2_2_recitar, decidir_3_3_anterior,
                   decidir_3_3_siguiente, decidir_4_2_comparar_cifras, decidir_5_1_componer,
                   decidir_5_2_sumar, decidir_5_3_descomponer_numero, decidir_5_3_sumar_numeros,
                   escena_0_2, escena_cantidad, explicar_pregunta)

BIEN = [0]
TOTAL = [0]

NOMBRES = ["o%d" % i for i in range(1, 12)]


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

    # ------------------------------------------------------------------ los tres grupos
    print("=" * 76)
    print("A) LOS TRES GRUPOS")
    print("=" * 76)
    comprobar("A1 'a' es una CANTIDAD (un objeto)", clasificar_nombre("a", saber), "cantidad")
    comprobar("A2 'silla_1' tambien", clasificar_nombre("silla_1", saber), "cantidad")
    comprobar("A3 '3' es una CIFRA", clasificar_nombre("3", saber), "cifra")
    comprobar("A4 '0' tambien", clasificar_nombre("0", saber), "cifra")
    comprobar("A5 'tres' es una PALABRA de numero", clasificar_nombre("tres", saber), "palabra")
    comprobar("A6 'cero' tambien", clasificar_nombre("cero", saber), "palabra")
    comprobar("A7 y 'casa' es una cantidad (no es ningun numero)",
              clasificar_nombre("casa", saber), "cantidad")
    print("")

    # ------------------------------------------------------------------ EL FALLO GRAVE
    print("=" * 76)
    print("B) EL FALLO GRAVE, ARREGLADO: un objeto no se llama como un numero")
    print("=" * 76)
    for texto, malo in [("a,b,c", None), ("silla_1,silla_2", None), ("3,2", "3"), ("dos,tres", "dos")]:
        try:
            escena_cantidad(texto, saber)
            comprobar("B '%s' -> se acepta (son objetos)" % texto, malo, None)
        except EntradaDelGrupoEquivocado:
            comprobar("B '%s' -> se RECHAZA (es un numero)" % texto, malo, texto.split(",")[0])
    salida = explicar_pregunta("sumar: 3 / 2", saber)
    comprobar("B3 sumar: 3 / 2 ya NO contesta '1 + 1 = 2'", "1 + 1 = 2" in salida, False)
    comprobar("B4 y dice claramente que '3' es una cifra", "'3' es una CIFRA" in salida, True)
    comprobar("B5 y sugiere las ordenes de numeros", "sumar_numeros:" in salida, True)
    salida = explicar_pregunta("descomponer: 5", saber)
    comprobar("B6 descomponer: 5 tampoco da '1 maneras'", "1 maneras" in salida, False)
    salida = explicar_pregunta("comparar: 3 / 2", saber)
    comprobar("B7 comparar: 3 / 2 tampoco dice 'tantos_como' falso",
              "RESULTADO: tantos_como" in salida, False)
    print("")

    # ------------------------------------------------------------------ el puente en las ordenes de numeros
    print("=" * 76)
    print("C) EL PUENTE EN LAS ORDENES DE NUMEROS (cifra o palabra, da igual)")
    print("=" * 76)
    comprobar("C1 siguiente: 3 = siguiente: tres",
              (decidir_3_3_siguiente("3", saber).get("siguiente"),
               decidir_3_3_siguiente("tres", saber).get("siguiente")), ("cuatro", "cuatro"))
    comprobar("C2 anterior: 3 = anterior: tres",
              (decidir_3_3_anterior("3", saber).get("anterior"),
               decidir_3_3_anterior("tres", saber).get("anterior")), ("dos", "dos"))
    comprobar("C3 recitar: 3 funciona", decidir_2_2_recitar("3", saber).get("tramo")[:2],
              ["tres", "cuatro"])
    comprobar("C4 comparar numeros con palabra y cifra mezcladas: dos y 3",
              decidir_4_2_comparar_cifras("dos", "3", saber).get("simbolo"), "<")
    comprobar("C5 y al reves: 3 y dos", decidir_4_2_comparar_cifras("3", "dos", saber).get("simbolo"), ">")
    salida = explicar_pregunta("revisar_secuencia: 1,dos,3", saber)
    comprobar("C6 revisar_secuencia acepta cifras", "RESULTADO: correcta" in salida, True)
    print("")

    # ------------------------------------------------------------------ operar con numeros
    print("=" * 76)
    print("D) OPERAR CON NUMEROS (sin objetos de por medio)")
    print("=" * 76)
    comprobar("D1 sumar_numeros: 3 + 2", decidir_5_3_sumar_numeros("3", "2", saber).get("expresion"),
              "3 + 2 = 5")
    comprobar("D2 con palabras: dos + tres", decidir_5_3_sumar_numeros("dos", "tres", saber).get("expresion"),
              "2 + 3 = 5")
    comprobar("D3 mezclando: 3 + dos", decidir_5_3_sumar_numeros("3", "dos", saber).get("expresion"),
              "3 + 2 = 5")
    comprobar("D4 con el cero: 0 + 4", decidir_5_3_sumar_numeros("0", "4", saber).get("expresion"),
              "0 + 4 = 4")
    comprobar("D5 en el limite: 6 + 4", decidir_5_3_sumar_numeros("6", "4", saber).get("expresion"),
              "6 + 4 = diez")
    # UNIDAD 7.1: el techo de sumar_numeros estaba escrito "10" a mano y se quedo corto al
    # llegar la secuencia a 100.  Ahora 7 + 5 = doce SI se puede; el techo esta en cien.
    comprobar("D6 (MEJORA 7.1): 7 + 5 ya SI suma -> doce",
              decidir_5_3_sumar_numeros("7", "5", saber).get("suma"), "doce")
    # Y el techo viejo tampoco estorba ya: 9 + 9 (que antes no se podia) ahora si.
    comprobar("D6b (MEJORA 7.1): 9 + 9 = dieciocho (antes el techo era diez)",
              decidir_5_3_sumar_numeros("9", "9", saber).get("suma"), "dieciocho")
    # UNIDAD 6.7: el techo subio de cien a MIL.  (Antes: noventa + noventa = 180 no alcanzaba.)
    # antes (N.4): novecientos mil + novecientos mil -> no_alcanza.  N.6: el techo es diez millones
    comprobar("D6c MEJORA N.6: nueve millones + dos millones pasa de DIEZ MILLONES -> no_alcanza",
              decidir_5_3_sumar_numeros("nueve millones", "dos millones", saber)["conclusion"],
              "no_alcanza")
    comprobar("D6d (MEJORA 6.7): noventa + noventa YA SI suma -> ciento ochenta",
              decidir_5_3_sumar_numeros("noventa", "noventa", saber).get("suma"),
              "ciento ochenta")
    comprobar("D7 TRAMPA: 'manzana' no es un numero",
              decidir_5_3_sumar_numeros("manzana", "2", saber)["conclusion"], "no_es_un_numero")
    r = decidir_5_3_descomponer_numero("5", saber)
    comprobar("D8 descomponer_numero: 5 -> 3 maneras", r.get("cuantas_maneras"), 3)
    comprobar("D9 y son las de siempre: 0+5, 1+4, 2+3", r.get("parejas"), [(0, 5), (1, 4), (2, 3)])
    comprobar("D10 con palabra: descomponer_numero: cinco",
              decidir_5_3_descomponer_numero("cinco", saber).get("cuantas_maneras"), 3)
    comprobar("D11 TRAMPA: el cero no se parte",
              decidir_5_3_descomponer_numero("0", saber)["conclusion"], "el_cero_no_se_parte")
    print("")

    # ------------------------------------------------------------------ PRUEBA DE HIERRO
    print("=" * 76)
    print("E) LA PRUEBA DE HIERRO: sumar numeros y sumar cantidades dan LO MISMO")
    print("=" * 76)
    malas = 0
    probadas = 0
    for a in range(0, 10):
        for b in range(0, 10 - a):
            con_numeros = decidir_5_3_sumar_numeros(str(a), str(b), saber)
            con_objetos = decidir_5_2_sumar(coleccion(a), coleccion(b), saber)
            con_partes = decidir_5_1_componer(coleccion(a), coleccion(b), saber)
            probadas += 1
            if not (con_numeros.get("suma") == con_objetos.get("suma") == con_partes.get("total")):
                malas += 1
                print("       NO CUADRA: %d+%d -> numeros=%s  objetos=%s  partes=%s"
                      % (a, b, con_numeros.get("suma"), con_objetos.get("suma"),
                         con_partes.get("total")))
    comprobar("E1 las %d parejas dan lo mismo por los TRES caminos" % probadas, malas, 0)
    comprobar("E2 y son 55 (a,b<=9 y a+b<=9)", probadas, 55)
    # La suma que da diez: con NUMEROS tambien (5+5), aunque su cifra no exista.
    r = decidir_5_3_sumar_numeros("5", "5", saber)
    comprobar("E2b 5 + 5 = diez (y avisa de que la cifra no la tiene)",
              (r.get("expresion"), r.get("total_sin_cifra")), ("5 + 5 = diez", True))
    # Y las dos maneras de decir el numero dan la misma suma
    malas2 = 0
    for n in range(0, 6):
        for m in range(0, 6 - n):
            cifra = decidir_5_3_sumar_numeros(str(n), str(m), saber).get("suma")
            palabra = decidir_5_3_sumar_numeros(
                ["cero", "uno", "dos", "tres", "cuatro", "cinco"][n],
                ["cero", "uno", "dos", "tres", "cuatro", "cinco"][m], saber).get("suma")
            if cifra != palabra:
                malas2 += 1
    comprobar("E3 da igual escribirlo con cifra o con palabra", malas2, 0)
    print("")

    # ------------------------------------------------------------------ el limite, bien puesto
    print("=" * 76)
    print("F) LO QUE SIGUE FUNCIONANDO IGUAL (no se ha roto nada)")
    print("=" * 76)
    comprobar("F1 cuantos: con objetos de verdad", "RESULTADO: tres" in
              explicar_pregunta("cuantos: silla_1, silla_2, silla_3", saber), True)
    comprobar("F2 sumar: con colecciones de verdad", "RESULTADO: 3 + 2 = 5" in
              explicar_pregunta("sumar: a,b,c / d,e", saber), True)
    comprobar("F3 y cifra: sigue igual", "RESULTADO: 3" in
              explicar_pregunta("cifra: tres", saber), True)
    comprobar("F4 y palabra: sigue igual", "RESULTADO: tres" in
              explicar_pregunta("palabra: 3", saber), True)
    print("")

    # ------------------------------------------------------------------ robustez
    print("=" * 76)
    print("G) ROBUSTEZ: contesta a todo, NUNCA revienta")
    print("=" * 76)
    for q in ["sumar_numeros: 3", "sumar_numeros: / ", "sumar_numeros: 3 + ", "sumar_numeros: + 3",
              "descomponer_numero:", "descomponer_numero: manzana", "siguiente: manzana",
              "comparar_numeros: 3 / manzana", "sumar: 3 / 2", "cuantos: 3",
              "descomponer: 5", "sumar: dos / tres", "anadir: 1 / 2"]:
        salida = explicar_pregunta(q, saber)
        comprobar("G '%s'" % q[:36],
                  ("RESULTADO:" in salida or "NO ENTIENDO" in salida), True)
    print("")

    print("=" * 76)
    print("UNIDAD 5.3: %d/%d correctos" % (BIEN[0], TOTAL[0]))
    print("=" * 76)
    return 0 if BIEN[0] == TOTAL[0] else 1


if __name__ == "__main__":
    sys.exit(main())
