# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 4.1 - COMPARAR CANTIDADES.

Lo que esta unidad tiene que dejar claro:
  - Comparar DOS COLECCIONES se dice con PALABRAS: mas, menos, tantos_como.  NO con simbolos.
    (Los simbolos >, <, = van entre CIFRAS, y eso es la 4.2.)
  - Se decide EMPAREJANDO (correspondencia uno a uno, sin contar) y se VERIFICA CONTANDO.
  - El TAMANO de los objetos NO cuenta: la cantidad son las cosas, no lo que ocupan.

Se corre asi:   py -3 pruebas/test_4_1.py
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

from motor import decidir_4_1_comparar, escena_0_2, explicar_pregunta  # noqa: E402

BIEN = [0]
TOTAL = [0]


def comprobar(titulo, obtenido, esperado):
    ok = obtenido == esperado
    BIEN[0] += ok
    TOTAL[0] += 1
    print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
    if not ok:
        print("       esperado=%s  obtenido=%s" % (esperado, obtenido))
    return ok


def comp(a, b, saber):
    return decidir_4_1_comparar(escena_0_2(a), escena_0_2(b), saber)


def main():
    saber = None  # cada llamada carga el conocimiento

    # ------------------------------------------------------------------ los tres resultados
    print("=" * 76)
    print("A) LOS TRES RESULTADOS (en palabras: mas, menos, tantos_como)")
    print("=" * 76)
    comprobar("A1 la primera tiene MAS", comp("a,b,c", "d,e", saber)["conclusion"], "mas")
    comprobar("A2 la primera tiene MENOS", comp("a,b", "c,d,e", saber)["conclusion"], "menos")
    comprobar("A3 las dos TANTOS COMO (lo mismo)", comp("a,b", "c,d", saber)["conclusion"], "tantos_como")
    comprobar("A4 con una sola -> no se puede comparar",
              comp("a,b", "", saber)["conclusion"], "mas")
    print("")

    # ------------------------------------------------------------------ el emparejamiento
    print("=" * 76)
    print("B) EL EMPAREJAMIENTO (uno a uno, sin contar) y la VERIFICACION contando")
    print("=" * 76)
    r = comp("a,b,c", "d,e", saber)
    comprobar("B1 empareja a--d y b--e", r["emparejadas"], [("a", "d"), ("b", "e")])
    comprobar("B2 y sobra 'c' de la primera", r["sobra_primera"], ["c"])
    comprobar("B3 no sobra nada de la segunda", r["sobra_segunda"], [])
    comprobar("B4 el conteo confirma: 3 y 2", (r["cantidad_primera"], r["cantidad_segunda"]),
              ("tres", "dos"))
    comprobar("B5 los dos caminos COINCIDEN (verificacion)", r["verificacion"], True)
    r = comp("a,b", "c,d,e", saber)
    comprobar("B6 al reves: sobra de la SEGUNDA", r["sobra_segunda"], ["e"])
    comprobar("B7 y su verificacion tambien cuadra", r["verificacion"], True)
    r = comp("a,b", "c,d", saber)
    comprobar("B8 las dos iguales: no sobra nada", (r["sobra_primera"], r["sobra_segunda"]), ([], []))
    print("")

    # ------------------------------------------------------------------ EL TAMANO NO CUENTA
    print("=" * 76)
    print("C) LA TRAMPA DE LA UNIDAD: el TAMANO de los objetos NO cuenta")
    print("=" * 76)
    r = comp("g1(tamano=grande), g2(tamano=grande)",
             "p1(tamano=pequeno), p2(tamano=pequeno), p3(tamano=pequeno)", saber)
    comprobar("C1 dos objetos GRANDES tienen MENOS que tres pequenos", r["conclusion"], "menos")
    comprobar("C2 (el sistema mira la cantidad, no el tamano)", r["cantidad_primera"], "dos")
    r = comp("g1(tamano=grande), g2(tamano=grande), g3(tamano=grande)",
             "p1(tamano=pequeno)", saber)
    comprobar("C3 TRAMPA: tres grandes tienen MAS que uno pequeno", r["conclusion"], "mas")
    salida = explicar_pregunta(
        "comparar: g1(tamano=grande) / p1(tamano=pequeno), p2(tamano=pequeno)", saber)
    comprobar("C4 y el sistema LO DICE (avisa del tamano)", "OJO AL TAMANO" in salida, True)
    print("")

    # ------------------------------------------------------------------ con la identidad (0.1)
    print("=" * 76)
    print("D) PASA POR LA IDENTIDAD (unidad 0.1): el mismo nombre es UNA cosa")
    print("=" * 76)
    r = comp("casa(color=rojo), casa(forma=cuadrado), carro", "x,y", saber)
    comprobar("D1 la casa repetida es UNA (2 objetos, no 3)", len(r["primera"]), 2)
    comprobar("D2 y entonces las dos son TANTOS COMO", r["conclusion"], "tantos_como")
    print("")

    # ------------------------------------------------------------------ el cero (3.2)
    print("=" * 76)
    print("E) EL CERO TAMBIEN SE COMPARA (unidad 3.2)")
    print("=" * 76)
    r = comp("", "", saber)
    comprobar("E1 dos colecciones VACIAS son TANTOS COMO (cero y cero)", r["conclusion"], "tantos_como")
    comprobar("E2 y las dos cantidades son 'cero'",
              (r["cantidad_primera"], r["cantidad_segunda"]), ("cero", "cero"))
    r = comp("", "a", saber)
    comprobar("E3 vacia contra una cosa: tiene MENOS", r["conclusion"], "menos")
    r = comp("a", "", saber)
    comprobar("E4 una cosa contra vacia: tiene MAS", r["conclusion"], "mas")
    print("")

    # ------------------------------------------------------------------ limites
    print("=" * 76)
    print("F) LIMITES DECLARADOS")
    print("=" * 76)
    r = comp(",".join("o%d" % i for i in range(1, 10002)), "a,b", saber)   # N.3: diez mil
    # UNIDAD 6.1: once objetos YA se cuentan; ahora el limite esta en cien.
    comprobar("F1 TRAMPA: con mas de DIEZ MIL objetos no le alcanza -> lo dice",
              r["conclusion"], "no_alcanza")
    r = decidir_4_1_comparar(escena_0_2(",".join("o%d" % (i + 1) for i in range(11))),
                             escena_0_2("a,b"), saber)
    comprobar("F1b (MEJORA 6.1): once contra dos ya SI se compara -> mas",
              r["conclusion"], "mas")
    salida = explicar_pregunta("comparar: a,b,c", saber)
    comprobar("F2 una sola coleccion -> NO ENTIENDO (comparar son DOS)", "NO ENTIENDO" in salida, True)
    salida = explicar_pregunta("comparar: a,b,c / d,e", saber)
    comprobar("F3 NO usa simbolos: la RESPUESTA es la palabra 'mas'",
              "RESULTADO: mas" in salida, True)
    comprobar("F3b y la cantidad tambien la dice con palabras", "tres contra dos" in salida, True)
    comprobar("F4 y explica que los simbolos son de la 4.2", "4.2" in salida, True)
    print("")

    # ------------------------------------------------------------------ robustez
    print("=" * 76)
    print("G) ROBUSTEZ: contesta a todo, no revienta")
    print("=" * 76)
    for q in ["comparar: / ", "comparar: a / b", "comparar: / a,b", "comparar: a,b / ",
              "comparar:a,b/c,d", "comparar: casa(color=rojo), casa / x,y"]:
        salida = explicar_pregunta(q, saber)
        comprobar("G '%s'" % q[:38], ("RESULTADO:" in salida or "NO ENTIENDO" in salida), True)
    print("")

    print("=" * 76)
    print("UNIDAD 4.1: %d/%d correctos" % (BIEN[0], TOTAL[0]))
    print("=" * 76)
    return 0 if BIEN[0] == TOTAL[0] else 1


if __name__ == "__main__":
    sys.exit(main())
