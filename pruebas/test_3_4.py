# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 3.4 - EL PUENTE (cantidad, palabra, cifra).

Lo que esta unidad tiene que dejar claro:
  - Lo mismo se dice de TRES maneras: cantidad (los objetos), palabra (como se dice), cifra (como
    se escribe).  Y hay SEIS caminos entre ellas (tres pares, cada uno en los dos sentidos).
  - El camino que faltaba es CIFRA -> CANTIDAD (dame: <monton> / 3), y se aprende aqui.
  - Hay DOS caminos para saber cuantos hay, y NO son iguales:
        EL LARGO: contar (una palabra por objeto).  Vale hasta diez.
        EL CORTO: de un vistazo (subitizing).  Solo grupos pequenos y reconocibles.
  - Y el sistema DICE por cual ha ido.

Se corre asi:   py -3 pruebas/test_3_4.py
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

from motor import (cargar_conocimiento, decidir_1_0_subitizar, decidir_2_4_dame,  # noqa: E402
                   decidir_2_4_tiene, decidir_3_1_cifra, decidir_3_1_cifra_de,
                   decidir_3_1_palabra, decidir_3_4_puente, escena_0_2, explicar_pregunta)

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


def main():
    saber = cargar_conocimiento()

    # ------------------------------------------------------------------ los seis caminos
    print("=" * 76)
    print("A) LOS SEIS CAMINOS (los tres pares, en los dos sentidos)")
    print("=" * 76)
    tres = escena_0_2("a,b,c")
    # 1. cantidad -> palabra
    r = decidir_2_4_tiene(tres, "tres", saber)
    comprobar("C1 cantidad -> palabra  (tiene: a,b,c / tres)", r["conclusion"], "si")
    # 2. palabra -> cantidad
    r = decidir_2_4_dame(escena_0_2("a,b,c,d"), "tres", saber)
    comprobar("C2 palabra -> cantidad   (dame: a,b,c,d / tres)", r["conclusion"], "cogido")
    # 3. cantidad -> cifra
    r = decidir_3_1_cifra_de(tres, saber)
    comprobar("C3 cantidad -> cifra     (cifra_de: a,b,c)", r.get("cifra"), "3")
    # 4. cifra -> cantidad  (ESTE ES EL NUEVO)
    r = decidir_2_4_dame(escena_0_2("a,b,c,d"), "3", saber)
    comprobar("C4 cifra -> cantidad     (dame: a,b,c,d / 3)  <- EL NUEVO", r["conclusion"], "cogido")
    comprobar("C4b y coge TRES, no otra cosa", len(r["cogidos"]), 3)
    comprobar("C4c y sabe que se lo pidieron con cifra", r["entrada_cifra"], True)
    # 5. palabra -> cifra
    r = decidir_3_1_cifra("tres", saber)
    comprobar("C5 palabra -> cifra      (cifra: tres)", r.get("cifra"), "3")
    # 6. cifra -> palabra
    r = decidir_3_1_palabra("3", saber)
    comprobar("C6 cifra -> palabra      (palabra: 3)", r.get("palabra"), "tres")
    print("")

    # ------------------------------------------------------------------ el puente
    print("=" * 76)
    print("B) EL PUENTE DE UNA COLECCION (el camino largo: contar)")
    print("=" * 76)
    r = decidir_3_4_puente(escena_0_2("silla_1,silla_2"), saber)
    comprobar("P1 la cantidad es 'dos'", r.get("cantidad"), "dos")
    comprobar("P2 la cifra es '2'", r.get("cifra"), "2")
    r = decidir_3_4_puente([], saber)
    comprobar("P3 una coleccion vacia es CERO (no 'no se puede decidir')", r["conclusion"], "vacia")
    r = decidir_3_4_puente(escena_0_2(",".join("o%d" % i for i in range(1, 10002))), saber)   # N.3: diez mil
    # UNIDAD 6.1: once objetos YA se cuentan; por eso ahora el limite esta en cien.
    comprobar("P4 TRAMPA: con mas de DIEZ MIL objetos no le alcanza -> lo dice",
              r["conclusion"], "no_alcanza")
    r = decidir_3_4_puente(escena_0_2(",".join("o%d" % (i + 1) for i in range(11))), saber)
    comprobar("P4b (MEJORA 6.1): once objetos -> la palabra SI, pero la cifra no existe",
              r["conclusion"], "puente_sin_cifra")
    print("")

    # ------------------------------------------------------------------ el camino corto
    print("=" * 76)
    print("C) EL CAMINO CORTO (de un vistazo), ahora conectado con la cifra")
    print("=" * 76)
    r = decidir_1_0_subitizar("x.x/.../x.x", saber)
    comprobar("S1 reconoce el patron de las esquinas", r["conclusion"], "reconocido")
    comprobar("S2 y dice que son CUATRO", r.get("etiqueta"), "cuatro")
    comprobar("S3 Y NO HA CONTADO (es el camino corto)", r["etiqueta"] != "tres", True)
    r = decidir_1_0_subitizar("x../xx./x.x", saber)
    comprobar("S4 TRAMPA: un dibujo que no reconoce -> no_reconocido (y NO cuenta)",
              r["conclusion"], "no_reconocido")
    print("")

    # ------------------------------------------------------------------ los dos caminos coinciden
    print("=" * 76)
    print("D) LOS DOS CAMINOS TIENEN QUE COINCIDIR")
    print("=" * 76)
    # El camino CORTO dice: el dibujo de las esquinas son cuatro.
    corto = decidir_1_0_subitizar("x.x/.../x.x", saber)["etiqueta"]
    # El camino LARGO dice: cuatro objetos contados son cuatro.
    largo = decidir_3_4_puente(escena_0_2("p,q,r,s"), saber)["cantidad"]
    comprobar("D1 el camino corto y el largo dan LA MISMA palabra", corto, largo)
    # Y las dos llegan a la misma cifra (dos formas distintas de decir lo mismo).
    cifra_corta = decidir_3_1_cifra(corto, saber).get("cifra")
    cifra_larga = decidir_3_4_puente(escena_0_2("p,q,r,s"), saber)["cifra"]
    comprobar("D2 y a la misma CIFRA", cifra_corta, cifra_larga)
    comprobar("D3 esa cifra es 4", cifra_corta, "4")
    print("")

    # ------------------------------------------------------------------ trampas del camino 4
    print("=" * 76)
    print("E) TRAMPAS DEL CAMINO NUEVO (cifra -> cantidad)")
    print("=" * 76)
    r = decidir_2_4_dame(escena_0_2("a,b"), "3", saber)
    comprobar("E1 TRAMPA: pedir 3 con solo 2 en el monton -> no_hay_bastantes",
              r["conclusion"], "no_hay_bastantes")
    r = decidir_2_4_dame(escena_0_2("a,b,c,d"), "10", saber)
    comprobar("E2 TRAMPA: el 10 son dos simbolos -> palabra_desconocida",
              r["conclusion"], "palabra_desconocida")
    r = decidir_2_4_dame(escena_0_2(",".join("o%d" % i for i in range(1, 11))), "9", saber)
    comprobar("E3 la cifra 9 si existe y se puede pedir (con diez en el monton)",
              r["conclusion"], "cogido")
    comprobar("E3b y coge NUEVE", len(r["cogidos"]), 9)
    r = decidir_2_4_dame(escena_0_2("a,b,c,d"), "0", saber)
    comprobar("E4 TRAMPA: pedir CERO objetos -> dar es coger, y el vacio no se coge",
              r["conclusion"], "cero_no_se_coge")
    print("")

    # ------------------------------------------------------------------ robustez
    print("=" * 76)
    print("F) ROBUSTEZ: contesta a todo, no revienta")
    print("=" * 76)
    for q in ["puente:", "puente: a", "puente: a,b,c,d,e,f,g,h,i,j",
              "dame: a,b / 3", "dame: a,b / 10", "caminos", "subitizar: xxx/xxx/xxx",
              "puente: casa(color=rojo), casa(forma=cuadrado), carro"]:
        salida = explicar_pregunta(q, saber)
        comprobar("F '%s'" % q[:40], ("RESULTADO:" in salida or "NO ENTIENDO" in salida), True)
    print("")

    print("=" * 76)
    print("UNIDAD 3.4: %d/%d correctos" % (BIEN[0], TOTAL[0]))
    print("=" * 76)
    return 0 if BIEN[0] == TOTAL[0] else 1


if __name__ == "__main__":
    sys.exit(main())
