# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 2.6 - ABSTRACCION (se puede contar cualquier cosa).

Lo que esta unidad tiene que dejar claro:
  - La cantidad NO depende de QUE SEAN las cosas: dos colecciones de cosas completamente distintas
    pueden tener la misma cantidad.
  - No hace falta que las cosas sean iguales ni que compartan atributos para contar un conjunto.
  - Y "silla, silla, silla" es UNA silla (regla de identidad de la 0.1): para tener tres sillas hay
    que darles nombres distintos.  OJO CON ESTO EN LAS PRUEBAS.

  A) CASOS DE EJEMPLO  - los del conocimiento.
  B) CASOS DE DOMINIO  - no programados, con trampas.
  C) ROBUSTEZ          - lo mal escrito se dice, no revienta.

Uso:  python pruebas/test_2_6.py
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

from motor import (cargar_conocimiento, decidir_2_3_cuantos,  # noqa: E402
                   decidir_2_6_misma_cantidad, escena_0_2, explicar_pregunta)


# (titulo, coleccion 1, coleccion 2, conclusion esperada)
EJEMPLOS = [
    ("E1 tres sillas y tres sonidos -> la misma cantidad",
     "silla_1,silla_2,silla_3", "sonido_1,sonido_2,sonido_3", "si"),
]

DOMINIO = [
    ("D1 cosas totalmente distintas, misma cantidad -> si",
     "casa(color=rojo),perro", "idea,salto", "si"),

    ("D2 distinta cantidad -> no", "a_1,a_2", "b_1,b_2,b_3", "no"),

    ("D3 TRAMPA: 'silla,silla,silla' es UNA silla (identidad de 0.1) -> no es lo mismo que tres",
     "silla,silla,silla", "sonido_1,sonido_2,sonido_3", "no"),

    ("D4 TRAMPA: coleccion mezclada sin NINGUN atributo comun -> tiene cantidad igualmente",
     "silla_1,perro_1,idea_1", "x_1,x_2,x_3", "si"),

    ("D5 un objeto y un objeto -> si", "cosa", "otra_cosa", "si"),

    ("D6 diez y diez -> si", "a_1,a_2,a_3,a_4,a_5,a_6,a_7,a_8,a_9,a_10",
     "b_1,b_2,b_3,b_4,b_5,b_6,b_7,b_8,b_9,b_10", "si"),

    ("D7 TRAMPA: una vacia -> no_decidible", "a_1,a_2", "", "no_decidible"),

    # UNIDAD 6.1: el techo dejo de estar en diez.  Ahora hacen falta mas de cien.
    ("D8 TRAMPA: mas de cien en una -> no_alcanza_la_secuencia",
     ",".join("a_%d" % (i + 1) for i in range(1001)),
     "b_1,b_2", "no_alcanza_la_secuencia"),

    ("D8b (MEJORA 6.1): once contra dos ya SI se decide (antes no se podia contar)",
     ",".join("a_%d" % (i + 1) for i in range(11)),
     "b_1,b_2", "no"),

    ("D9 TRAMPA: la casa repetida con datos que no chocan es UNA casa -> 2 contra 3 da NO",
     "casa(color=rojo),casa(forma=cuadrado),perro", "x_1,x_2,x_3", "no"),
]


def correr(saber):
    print("=" * 76)
    print("A/B) MISMA CANTIDAD: dos colecciones de cosas distintas")
    print("=" * 76)
    bien = 0
    casos = EJEMPLOS + DOMINIO
    for titulo, c1, c2, concl_esp in casos:
        r = decidir_2_6_misma_cantidad(escena_0_2(c1), escena_0_2(c2), saber)
        ok = r["conclusion"] == concl_esp
        bien += ok
        print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
        if not ok:
            print("       esperado=%s  obtenido=%s  (%d vs %d)"
                  % (concl_esp, r["conclusion"], len(r["izquierda"]), len(r["derecha"])))
    print("-- %d/%d correctos\n" % (bien, len(casos)))
    return bien, len(casos)


def correr_tipos(saber):
    """
    La prueba de fondo de la abstraccion: contar cosas de CUALQUIER tipo (y mezcladas) da cantidad.
    - objetos, sonidos, saltos, ideas, y una mezcla de todo.
    """
    print("=" * 76)
    print("C) CUALQUIER COSA SE CUENTA: objetos, sonidos, saltos, ideas y mezclas")
    print("=" * 76)
    pruebas = [
        ("tres objetos", "silla_1,silla_2,silla_3", "tres"),
        ("tres sonidos", "sonido_1,sonido_2,sonido_3", "tres"),
        ("tres saltos", "salto_1,salto_2,salto_3", "tres"),
        ("tres ideas", "idea_1,idea_2,idea_3", "tres"),
        ("una mezcla de todo", "silla_1,sonido_1,salto_1,idea_1", "cuatro"),
        ("cosas abstractas y sin atributos", "amor,tiempo,silencio", "tres"),
    ]
    bien = 0
    for titulo, coleccion, esperado in pruebas:
        r = decidir_2_3_cuantos(escena_0_2(coleccion), saber)
        ok = r.get("cantidad") == esperado
        bien += ok
        print("%-6s %-36s -> %s" % ("OK" if ok else "FALLA", titulo, r.get("cantidad")))
    print("-- %d/%d correctos\n" % (bien, len(pruebas)))
    return bien, len(pruebas)


def correr_robustez(saber):
    print("=" * 76)
    print("D) ROBUSTEZ - lo escrito mal se dice, no revienta")
    print("=" * 76)
    entradas = ["misma_cantidad:", "misma_cantidad: a,b", "misma_cantidad: / ", "misma_cantidad: / a",
                "misma_cantidad: a,b /", "misma_cantidad: caja(colorrojo) / a"]
    bien = 0
    for e in entradas:
        try:
            salida = explicar_pregunta(e, saber)
            ok = isinstance(salida, str) and salida.strip() != ""
            bien += ok
            print("%-6s %r -> %s" % ("OK" if ok else "FALLA", e, salida.splitlines()[0][:50]))
        except Exception as ex:
            print("FALLA  reviento con %r -> %r" % (e, ex))
    print("-- %d/%d correctos\n" % (bien, len(entradas)))
    return bien, len(entradas)


def main():
    saber = cargar_conocimiento()
    a = correr(saber)
    c = correr_tipos(saber)
    d = correr_robustez(saber)

    print("=" * 76)
    print("TRAZA DEL CASO PRINCIPAL (tres sillas contra tres sonidos)")
    print("=" * 76)
    print(explicar_pregunta("misma_cantidad: silla_1,silla_2,silla_3 / sonido_1,sonido_2,sonido_3",
                            saber))
    print()

    ok = a[0] + c[0] + d[0]
    total = a[1] + c[1] + d[1]
    print("TOTAL: %d/%d" % (ok, total))
    if ok != total:
        print("RESULTADO: ROJO")
        return 1
    print("RESULTADO: VERDE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
