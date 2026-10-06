# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 3.3 - LA SECUENCIA DE NUMEROS (y las dos listas).

Lo que esta unidad tiene que dejar claro:
  - HAY DOS LISTAS, y son cosas distintas:
       LA LISTA DE CONTAR    : uno, dos, tres ... diez      (para contar cosas; empieza en el objeto)
       LA SECUENCIA DE NUMEROS: cero, uno, dos ... nueve    (el orden de los numeros; lleva el cero)
  - Y SON COHERENTES: si "cuantos" de una coleccion vacia es CERO, entonces el cero TIENE que estar
    en la lista.  Eso es el FALLO que cazo Carlos, y aqui queda vigilado.

Se corre asi:   py -3 pruebas/test_3_3.py
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

from motor import (cargar_conocimiento, decidir_2_3_cuantos,  # noqa: E402
                   decidir_3_3_anterior, decidir_3_3_dos_listas, decidir_3_3_siguiente,
                   explicar_pregunta)

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


def correr_flechas(casos, funcion, saber, etiqueta):
    print("=" * 76)
    print(etiqueta)
    print("=" * 76)
    for titulo, palabra, esperado in casos:
        r = funcion(palabra, saber)
        obtenido = r.get("siguiente") or r.get("anterior") or r["conclusion"]
        comprobar(titulo, obtenido, esperado)
    print("")


def main():
    saber = cargar_conocimiento()

    # ------------------------------------------------------------------ ejemplos
    print("=" * 76)
    print("A) EJEMPLOS: los dos casos de siempre, ahora sobre la secuencia de numeros")
    print("=" * 76)
    comprobar("E1 despues de tres va cuatro", decidir_3_3_siguiente("tres", saber).get("siguiente"), "cuatro")
    comprobar("E2 antes de tres va dos", decidir_3_3_anterior("tres", saber).get("anterior"), "dos")
    print("")

    # ------------------------------------------------------------------ dominio
    correr_flechas([
        ("D1 despues del cero va uno (el cero SI esta en los numeros)", "cero", "uno"),
        ("D2 despues de cinco va seis (lo normal sigue igual)", "cinco", "seis"),
        ("D3 TRAMPA: despues de nueve NO hay nada (es el ultimo)", "nueve", "no_lo_se"),
        ("D4 'diez' no tiene sitio en los numeros -> sin_numero", "diez", "sin_numero"),
        ("D5 (MEJORA 6.1): 'once' ya SI esta en la lista de CONTAR, pero no en la de NUMEROS",
         "once", "sin_numero"),
        ("D6 TRAMPA: 'manzana' tampoco", "manzana", "palabra_desconocida"),
    ], decidir_3_3_siguiente, saber,
        "B) SIGUIENTE: el cero, el final y las trampas")

    correr_flechas([
        ("D9 antes de cinco va cuatro", "cinco", "cuatro"),
        ("D10 ARREGLO DEL FALLO: antes de uno esta el CERO", "uno", "cero"),
        ("D11 TRAMPA: antes del cero -> no_lo_se (es el primero)", "cero", "no_lo_se"),
        ("D12 TRAMPA: 'diez' -> sin_numero (esta en la de contar, no en la de numeros)", "diez", "sin_numero"),
        ("D13 TRAMPA: 'casa' no es un numero", "casa", "palabra_desconocida"),
    ], decidir_3_3_anterior, saber, "C) ANTERIOR (mas casos)")

    # ------------------------------------------------------------------ las dos listas
    print("=" * 76)
    print("D) LAS DOS LISTAS, y su relacion")
    print("=" * 76)
    d = decidir_3_3_dos_listas(saber)
    comprobar("D13 la lista de contar empieza en 'uno'", d["conteo"][0], "uno")
    comprobar("D14 la secuencia de numeros empieza en 'cero'", d["numeros"][0], "cero")
    comprobar("D15 la lista de contar NO tiene el cero", "cero" in d["conteo"], False)
    comprobar("D16 la secuencia de numeros SI tiene el cero", "cero" in d["numeros"], True)
    comprobar("D17 (N.3) la lista de CONTAR llega a 'diez mil' (antes: cien, luego mil)",
              d["conteo"][-1], "diez mil")
    comprobar("D18 la secuencia de numeros acaba en 'nueve' (diez no tiene cifra)", d["numeros"][-1], "nueve")
    # UNIDAD 6.1: antes la lista de contar acababa en 'diez' y los numeros eran "el cero + la de
    # contar sin el diez".  Al llegar el conteo a cien, esa relacion SE ROMPE (y debe romperse:
    # son dos cosas distintas, y ahora se ve).
    comprobar("D19 (6.1) contar y numeros YA NO COINCIDEN: los numeros son el cero..nueve",
              d["numeros"], ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete",
                             "ocho", "nueve"])
    comprobar("D19b la de contar empieza en 'uno' y la de numeros en 'cero'",
              (d["conteo"][0], d["numeros"][0]), ("uno", "cero"))
    print("")

    # ------------------------------------------------------------------ LA COHERENCIA (el fallo)
    print("=" * 76)
    print("E) LA COHERENCIA: la incoherencia que cazo Carlos, vigilada")
    print("=" * 76)
    r_cuantos = decidir_2_3_cuantos([], saber)
    comprobar("E1 'cuantos' de una coleccion vacia es CERO", r_cuantos.get("cantidad"), "cero")
    comprobar("E2 y ese 'cero' TIENE que estar en la secuencia de numeros",
              r_cuantos.get("cantidad") in d["numeros"], True)
    comprobar("E3 y el cero NO puede estar en la lista de contar (contar empieza en uno)",
              r_cuantos.get("cantidad") in d["conteo"], False)
    r_ant = decidir_3_3_anterior("uno", saber)
    comprobar("E4 'antes de uno' es CERO, no 'no hay nada' (esto era el fallo)", r_ant.get("anterior"), "cero")
    print("")

    # ------------------------------------------------------------------ robustez
    print("=" * 76)
    print("F) ROBUSTEZ: no revienta con nada raro")
    print("=" * 76)
    for palabra in ["", "  ", "CERO", "Uno", "123", "cero ", "0"]:
        salida = explicar_pregunta("anterior: %s" % palabra, saber)
        comprobar("F '%s' -> contesta, no revienta" % palabra,
                  ("RESULTADO:" in salida or "NO ENTIENDO" in salida), True)
    print("")

    print("=" * 76)
    print("UNIDAD 3.3: %d/%d correctos" % (BIEN[0], TOTAL[0]))
    print("=" * 76)
    return 0 if BIEN[0] == TOTAL[0] else 1


if __name__ == "__main__":
    sys.exit(main())
