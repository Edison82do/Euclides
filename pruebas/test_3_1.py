# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 3.1 - LOS SIMBOLOS (las cifras 1..9).

Lo que esta unidad tiene que dejar claro:
  - Son TRES representaciones de lo mismo: CANTIDAD, PALABRA y CIFRA.
  - La cifra es un SIMBOLO: una marca que representa, no la cantidad.
  - Se pasa en los dos sentidos: palabra -> cifra y cifra -> palabra, y de la cantidad a la cifra.
  - Donde acaba: el 1 al 9.  "diez" tiene cifra, pero son DOS simbolos: aqui no esta, y se dice.
  - 6 y 9 son DOS simbolos distintos (que uno parezca el otro girado no los hace el mismo).

  A) CASOS DE EJEMPLO  - los del conocimiento.
  B) CASOS DE DOMINIO  - no programados, con trampas.
  C) COBERTURA         - los nueve pares, y la ida y vuelta de cada uno.
  D) ROBUSTEZ          - lo mal escrito se dice, no revienta.

Uso:  python pruebas/test_3_1.py
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

from motor import (cargar_conocimiento, decidir_3_1_cifra,  # noqa: E402
                   decidir_3_1_cifra_de, decidir_3_1_palabra, escena_0_2, explicar_pregunta)


# (titulo, palabra, conclusion esperada, cifra esperada)
EJEMPLOS_CIFRA = [
    ("E1 la cifra de 'tres' es 3", "tres", "cifra", "3"),
]

DOMINIO_CIFRA = [
    ("D1 MEJORA 6.3: 'diez' YA tiene cifra de dos digitos (antes: sin_cifra)",
     "diez", "cifra", "10"),

    ("D2 TRAMPA: 'manzana' no es una palabra de la lista",
     "manzana", "palabra_desconocida", None),

    ("D3 TRAMPA: '6' no es una palabra (es una cifra)", "6", "palabra_desconocida", None),
]

# (titulo, cifra, conclusion esperada, palabra esperada)
EJEMPLOS_PALABRA = [
    ("E2 la palabra de la cifra 3 es 'tres'", "3", "palabra", "tres"),
]

DOMINIO_PALABRA = [
    ("D4 el 0 ya es una cifra: es el cero (unidad 3.2)", "0", "palabra", "cero"),
    ("D5 MEJORA 6.3: la cifra 10 YA se lee (antes: dos simbolos)", "10", "palabra", "diez"),
    ("D6 TRAMPA: 'tres' no es una cifra", "tres", "cifra_desconocida", None),
]

# (titulo, coleccion, conclusion esperada, cifra esperada)
DOMINIO_CIFRA_DE = [
    ("D7 un objeto -> 1", "cosa", "cifra", "1"),
    ("D8 nueve objetos -> 9", "a,b,c,d,e,f,g,h,i", "cifra", "9"),
    ("D9 MEJORA 6.3: diez objetos YA tienen cifra (antes: no_alcanza_las_cifras)",
     "a,b,c,d,e,f,g,h,i,j", "cifra", "10"),
    ("D10 TRAMPA: una coleccion vacia tiene cifra 0 (unidad 3.2)", "", "cifra", "0"),
    ("D11 TRAMPA (la prueba de Carlos): la casa repetida es UNA casa -> 3",
     "casa(color=blanco), casa, perro, casa(forma=cuadrado), carro", "cifra", "3"),
]


def correr_cifra(saber):
    print("=" * 76)
    print("A/B) PALABRA -> CIFRA")
    print("=" * 76)
    bien = 0
    casos = EJEMPLOS_CIFRA + DOMINIO_CIFRA
    for titulo, palabra, concl_esp, cif_esp in casos:
        r = decidir_3_1_cifra(palabra, saber)
        ok = r["conclusion"] == concl_esp and (cif_esp is None or r.get("cifra") == cif_esp)
        bien += ok
        print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
        if not ok:
            print("       esperado=%s %s  obtenido=%s %s"
                  % (concl_esp, cif_esp, r["conclusion"], r.get("cifra")))
    print("-- %d/%d correctos\n" % (bien, len(casos)))
    return bien, len(casos)


def correr_palabra(saber):
    print("=" * 76)
    print("A/B) CIFRA -> PALABRA")
    print("=" * 76)
    bien = 0
    casos = EJEMPLOS_PALABRA + DOMINIO_PALABRA
    for titulo, cifra, concl_esp, pal_esp in casos:
        r = decidir_3_1_palabra(cifra, saber)
        ok = r["conclusion"] == concl_esp and (pal_esp is None or r.get("palabra") == pal_esp)
        bien += ok
        print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
        if not ok:
            print("       esperado=%s %s  obtenido=%s %s"
                  % (concl_esp, pal_esp, r["conclusion"], r.get("palabra")))
    print("-- %d/%d correctos\n" % (bien, len(casos)))
    return bien, len(casos)


def correr_cifra_de(saber):
    print("=" * 76)
    print("C) CANTIDAD -> CIFRA")
    print("=" * 76)
    bien = 0
    for titulo, coleccion, concl_esp, cif_esp in DOMINIO_CIFRA_DE:
        r = decidir_3_1_cifra_de(escena_0_2(coleccion), saber)
        ok = r["conclusion"] == concl_esp and (cif_esp is None or r.get("cifra") == cif_esp)
        bien += ok
        print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
        if not ok:
            print("       esperado=%s %s  obtenido=%s %s"
                  % (concl_esp, cif_esp, r["conclusion"], r.get("cifra")))
    print("-- %d/%d correctos\n" % (bien, len(DOMINIO_CIFRA_DE)))
    return bien, len(DOMINIO_CIFRA_DE)


def correr_cobertura(saber):
    """
    Los NUEVE pares, y la ida y vuelta de cada uno: palabra -> cifra -> palabra tiene que volver
    al mismo sitio.  Y las nueve cifras tienen que ser DISTINTAS entre si.
    """
    print("=" * 76)
    print("C) COBERTURA: los nueve pares, y la ida y vuelta de cada uno")
    print("=" * 76)
    palabras = ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve"]
    bien = 0
    cifras_vistas = []
    for i, p in enumerate(palabras, 1):
        rc = decidir_3_1_cifra(p, saber)
        cifra = rc.get("cifra")
        rp = decidir_3_1_palabra(cifra, saber) if cifra else {}
        vuelta = rp.get("palabra")
        ok = cifra == str(i) and vuelta == p
        bien += ok
        cifras_vistas.append(cifra)
        print("%-6s %-7s -> %-2s -> %-7s" % ("OK" if ok else "FALLA", p, cifra, vuelta))
    # las nueve cifras tienen que ser distintas
    distintas = len(set(cifras_vistas)) == 9
    bien += distintas
    print("%-6s las nueve cifras son distintas entre si" % ("OK" if distintas else "FALLA"))
    print("-- %d/%d correctos\n" % (bien, 10))
    return bien, 10


def correr_robustez(saber):
    print("=" * 76)
    print("D) ROBUSTEZ - lo escrito mal se dice, no revienta")
    print("=" * 76)
    entradas = ["cifra:", "cifra: ", "palabra:", "palabra: ", "cifra_de:", "cifra_de: ",
                "cifra:  ", "palabra: abc"]
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
    a1 = correr_cifra(saber)
    a2 = correr_palabra(saber)
    c1 = correr_cifra_de(saber)
    c2 = correr_cobertura(saber)
    d = correr_robustez(saber)

    print("=" * 76)
    print("TRAZA DEL PUENTE COMPLETO (cantidad -> palabra -> cifra)")
    print("=" * 76)
    print(explicar_pregunta("cifra_de: a,b,c", saber))
    print()

    ok = a1[0] + a2[0] + c1[0] + c2[0] + d[0]
    total = a1[1] + a2[1] + c1[1] + c2[1] + d[1]
    print("TOTAL: %d/%d" % (ok, total))
    if ok != total:
        print("RESULTADO: ROJO")
        return 1
    print("RESULTADO: VERDE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
