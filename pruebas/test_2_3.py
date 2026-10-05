# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 2.3 - CUANTOS HAY (contar la coleccion y dar la cantidad).

Lo que esta unidad tiene que dejar claro:
  - La respuesta es LA ULTIMA PALABRA del recuento.
  - NO se cuenta dos veces (el error clasico de los ninos al oir "cuantos hay?").
  - Si hay mas objetos que palabras conoce el sistema, NO se inventa la cantidad.
  - Repetir el mismo nombre NO cuenta dos veces (identidad de la 0.1).
  - Y todo vale tanto con nombres pelados como con atributos (la leccion del fallo de la 2.1).

  A) CASOS DE EJEMPLO  - los del conocimiento.
  B) CASOS DE DOMINIO  - no programados, con trampas.
  C) ROBUSTEZ          - lo mal escrito se dice, no revienta.

Uso:  python pruebas/test_2_3.py
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

from motor import cargar_conocimiento, decidir_2_3_cuantos, escena_0_2, explicar_pregunta  # noqa: E402


# (titulo, coleccion, conclusion esperada, cantidad esperada)
EJEMPLOS = [
    ("E1 tres objetos -> tres", "a,b,c", "hay_cantidad", "tres"),
]

DOMINIO = [
    ("D1 un solo objeto -> uno", "cosa", "hay_cantidad", "uno"),
    ("D2 cinco objetos -> cinco", "a,b,c,d,e", "hay_cantidad", "cinco"),
    ("D3 diez objetos -> diez (el maximo que conozco)", "a,b,c,d,e,f,g,h,i,j", "hay_cantidad", "diez"),

    # UNIDAD 6.1: la secuencia llega a cien, asi que el techo deja de estar en diez.
    ("D4 TRAMPA: mas de cien objetos -> no se inventa la cantidad",
     ",".join("o%d" % (i + 1) for i in range(1001)), "no_alcanza_la_secuencia", None),

    ("D4b (MEJORA 6.1): ONCE objetos ya SI se cuentan -> once",
     ",".join("o%d" % (i + 1) for i in range(11)), "hay_cantidad", "once"),

    ("D5 TRAMPA (la prueba de Carlos): el nombre repetido NO cuenta doble -> tres",
     "casa(color=blanco), casa, perro, casa(forma=cuadrado), carro", "hay_cantidad", "tres"),

    ("D6 TRAMPA: el mismo nombre cinco veces -> UN objeto -> uno",
     "a,a,a,a,a", "hay_cantidad", "uno"),

    ("D7 TRAMPA: dos casas que SI se contradicen son DOS -> tres en total",
     "casa(color=blanco), casa(color=rojo), carro", "hay_cantidad", "tres"),

    ("D8 la coleccion entera con atributos, bien contada",
     "silla(color=azul), mesa(color=rojo), plato(forma=redondo), vaso", "hay_cantidad", "cuatro"),
]


def correr(casos, saber, etiqueta):
    print("=" * 76)
    print(etiqueta)
    print("=" * 76)
    bien = 0
    for titulo, coleccion, concl_esp, cant_esp in casos:
        r = decidir_2_3_cuantos(escena_0_2(coleccion), saber)
        ok = r["conclusion"] == concl_esp and (cant_esp is None or r.get("cantidad") == cant_esp)
        bien += ok
        print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
        if not ok:
            print("       esperado=%s %s" % (concl_esp, cant_esp))
            print("       obtenido=%s %s" % (r["conclusion"], r.get("cantidad")))
    print("-- %d/%d correctos\n" % (bien, len(casos)))
    return bien, len(casos)


def correr_vacio(saber):
    print("=" * 76)
    print("C) Una coleccion VACIA tiene cantidad CERO (unidad 3.2)")
    print("=" * 76)
    r = decidir_2_3_cuantos([], saber)
    ok = r["conclusion"] == "cero"
    print("%-6s cuantos: (nada) -> %s" % ("OK" if ok else "FALLA", r["conclusion"]))
    print("-- %d/1 correctos\n" % ok)
    return ok, 1


def correr_robustez(saber):
    print("=" * 76)
    print("D) ROBUSTEZ - lo escrito mal se dice, no revienta")
    print("=" * 76)
    entradas = ["cuantos: ", "cuantos:", "cuantos: caja(colorrojo)", "cuantos: caja(color=)"]
    bien = 0
    for e in entradas:
        try:
            salida = explicar_pregunta(e, saber)
            ok = isinstance(salida, str) and salida.strip() != ""
            bien += ok
            print("%-6s %r -> %s" % ("OK" if ok else "FALLA", e, salida.splitlines()[0][:56]))
        except Exception as ex:
            print("FALLA  reviento con %r -> %r" % (e, ex))
    print("-- %d/%d correctos\n" % (bien, len(entradas)))
    return bien, len(entradas)


def main():
    saber = cargar_conocimiento()
    a = correr(EJEMPLOS, saber, "A) CUANTOS HAY - casos de ejemplo")
    b = correr(DOMINIO, saber, "B) CUANTOS HAY - prueba de dominio (no programados)")
    c = correr_vacio(saber)
    d = correr_robustez(saber)

    print("=" * 76)
    print("TRAZA DEL CASO DE CARLOS (D5: casa blanca + casa cuadrada es UNA casa)")
    print("=" * 76)
    print(explicar_pregunta(
        "cuantos: casa(color=blanco), casa, perro, casa(forma=cuadrado), carro", saber))
    print()

    ok = a[0] + b[0] + c[0] + d[0]
    total = a[1] + b[1] + c[1] + d[1]
    print("TOTAL: %d/%d" % (ok, total))
    if ok != total:
        print("RESULTADO: ROJO")
        return 1
    print("RESULTADO: VERDE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
