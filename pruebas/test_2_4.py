# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 2.4 - CARDINALIDAD (la ultima palabra ES la cantidad del conjunto).

Lo que esta unidad tiene que dejar claro:
  - GIVE-N: de la palabra al conjunto.  Saber RECONOCER una cantidad no es saber PRODUCIRLA.
    ("Dame tres" es mas dificil que "cuantos hay?", y por eso es la prueba que distingue.)
  - EL MONTON LO DA QUIEN PREGUNTA.  El sistema NO TIENE UN MUNDO: no crea objetos, elige de los
    que le dan.  (Agujero cazado por Carlos: la primera version se fabricaba los objetos.)
  - Si en el monton hay MENOS de los pedidos, NO se los inventa: dice que no hay bastantes.
  - Siempre se verifica: cuenta lo cogido y comprueba que cuadra.
  - Y "tiene N?": cuenta el conjunto y confirma o RECHAZA.

  A) CASOS DE EJEMPLO  - los del conocimiento.
  B) CASOS DE DOMINIO  - no programados, con trampas.
  C) ROBUSTEZ          - lo mal escrito se dice, no revienta.

Uso:  python pruebas/test_2_4.py
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _hierro  # noqa: E402

from motor import (cargar_conocimiento, decidir_2_3_cuantos, decidir_2_4_dame,  # noqa: E402
                   decidir_2_4_tiene, escena_0_2, explicar_pregunta)


# (titulo, monton, palabra, conclusion esperada, cuantos cogidos)
EJEMPLOS_DAME = [
    ("E1 de cinco, dame tres -> coge 3 y deja 2", "a,b,c,d,e", "tres", "cogido", 3),
]

DOMINIO_DAME = [
    ("D1 de uno, dame uno -> coge el unico", "a", "uno", "cogido", 1),

    ("D2 de diez, dame diez -> coge los diez", "a,b,c,d,e,f,g,h,i,j", "diez", "cogido", 10),

    ("D3 de tres, dame uno -> coge 1 y deja 2", "a,b,c", "uno", "cogido", 1),

    ("D4 justo los que pide: de tres, dame tres", "a,b,c", "tres", "cogido", 3),

    ("D5 TRAMPA: de dos NO puede dar tres -> no_hay_bastantes",
     "a,b", "tres", "no_hay_bastantes", None),

    ("D6 TRAMPA: de cuatro NO puede dar diez -> no_hay_bastantes",
     "a,b,c,d", "diez", "no_hay_bastantes", None),

    ("D7 (MEJORA 6.1): 'once' ya SI es palabra valida; pero de TRES objetos no se cogen once",
     "a,b,c", "once", "no_hay_bastantes", None),

    ("D7b TRAMPA: una palabra que no esta en la lista -> palabra_desconocida",
     "a,b,c", "pepito", "palabra_desconocida", None),

    ("D8 TRAMPA: monton vacio -> no tengo de donde coger", "", "tres", "no_decidible", None),

    ("D9 TRAMPA: el monton con nombres repetidos cuenta una sola vez",
     "a,a,a,b", "dos", "cogido", 2),
]

# (titulo, coleccion, palabra, conclusion esperada)
EJEMPLOS_TIENE = [
    ("E2 a,b,c tiene tres -> si", "a,b,c", "tres", "si"),
]

DOMINIO_TIENE = [
    ("D10 TRAMPA: a,b,c tiene cinco -> NO (y dice que tiene tres)",
     "a,b,c", "cinco", "no"),

    ("D11 a,b,c,d tiene cuatro -> si", "a,b,c,d", "cuatro", "si"),

    ("D12 TRAMPA (la prueba de Carlos): la casa repetida no cuenta doble -> tiene tres",
     "casa(color=blanco), casa, perro, casa(forma=cuadrado), carro", "tres", "si"),

    ("D13 TRAMPA: el mismo conjunto NO tiene cinco",
     "casa(color=blanco), casa, perro, casa(forma=cuadrado), carro", "cinco", "no"),

    ("D14 TRAMPA: mas de MIL objetos -> no puede decidirlo (6.7)",
     ",".join("o%d" % (i + 1) for i in range(1001)), "cinco", "no_alcanza_la_secuencia"),

    ("D14b (MEJORA 6.1): ONCE objetos ya SI se pueden decidir... y tienen ONCE, no cinco",
     ",".join("o%d" % (i + 1) for i in range(11)), "cinco", "no"),

    ("D15 (MEJORA 6.1): 'once' ya SI es palabra valida; pero tres objetos no tienen once",
     "a,b,c", "once", "no"),

    ("D15b TRAMPA: una palabra que no esta en la lista",
     "a,b,c", "pepito", "palabra_desconocida"),

    ("D16 un solo objeto tiene uno -> si", "cosa", "uno", "si"),
]


def correr_dame(saber):
    print("=" * 76)
    print("A/B) GIVE-N: 'dame: <monton> / N'  (de la palabra al conjunto, cogiendo del monton)")
    print("=" * 76)
    bien = 0
    casos = EJEMPLOS_DAME + DOMINIO_DAME
    for titulo, monton, palabra, concl_esp, n_esp in casos:
        r = decidir_2_4_dame(escena_0_2(monton), palabra, saber)
        ok = (r["conclusion"] == concl_esp
              and (n_esp is None or len(r.get("cogidos", [])) == n_esp)
              and (r["conclusion"] != "cogido" or r.get("verificacion")))
        bien += ok
        print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
        if not ok:
            print("       esperado=%s n=%s  obtenido=%s n=%s verif=%s"
                  % (concl_esp, n_esp, r["conclusion"], len(r.get("cogidos", [])),
                     r.get("verificacion")))
    print("-- %d/%d correctos\n" % (bien, len(casos)))
    return bien, len(casos)


def correr_tiene(saber):
    print("=" * 76)
    print("A/B) 'TIENE N?': cuenta y confirma o rechaza")
    print("=" * 76)
    bien = 0
    casos = EJEMPLOS_TIENE + DOMINIO_TIENE
    for titulo, coleccion, palabra, concl_esp in casos:
        r = decidir_2_4_tiene(escena_0_2(coleccion), palabra, saber)
        ok = r["conclusion"] == concl_esp
        bien += ok
        print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
        if not ok:
            print("       esperado=%s  obtenido=%s" % (concl_esp, r["conclusion"]))
    print("-- %d/%d correctos\n" % (bien, len(casos)))
    return bien, len(casos)


def correr_coherencia(saber):
    """
    La prueba de fuego del principio: de un monton de diez, para CADA cantidad, coger la cantidad
    pedida y volver a contarla tiene que devolver la misma palabra.
    """
    print("=" * 76)
    print("C) COHERENCIA: de un monton de CIEN, 'dame N' y contar lo cogido tiene que dar N")
    print("=" * 76)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    # UNIDAD 6.7: la secuencia llega a MIL, asi que el monton tiene que llegar tambien.
    # (Antes de la 6.1 era de diez; con la 6.1, de cien; ahora, de mil.)
    monton = escena_0_2(",".join("cosa%d" % i for i in range(1, 1001)))
    # UNA afirmacion ("para toda N, dame N y contar lo cogido da N"), recorrida sobre las
    # cantidades de _hierro (todas con --hierro).  Antes contaba 1000 pruebas e imprimia 1000 lineas.
    cantidades = _hierro.numeros(1, len(secuencia))
    malas = []
    for n in cantidades:
        palabra = secuencia[n - 1]
        r = decidir_2_4_dame(monton, palabra, saber)
        rc = decidir_2_3_cuantos(escena_0_2(",".join(r["cogidos"])), saber)
        if not (r["conclusion"] == "cogido" and rc.get("cantidad") == palabra):
            malas.append(palabra)
    ok = not malas
    print("%-6s dame N y contar lo cogido da N  (%d cantidades, %s)%s"
          % ("OK" if ok else "FALLA", len(cantidades), _hierro.modo(),
             "" if ok else "  fallan: %s" % malas[:5]))
    print()
    return (1 if ok else 0), 1


def correr_robustez(saber):
    print("=" * 76)
    print("D) ROBUSTEZ - lo escrito mal se dice, no revienta")
    print("=" * 76)
    entradas = ["dame:", "dame: ", "dame: a,b /", "dame: / tres", "dame: a,b",
                "tiene: a,b,c /", "tiene: / tres", "tiene: caja(colorrojo) / tres"]
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
    a = correr_dame(saber)
    b = correr_tiene(saber)
    c = correr_coherencia(saber)
    d = correr_robustez(saber)

    print("=" * 76)
    print("TRAZA DEL CASO PRINCIPAL (dame desde un monton, y sin monton)")
    print("=" * 76)
    print(explicar_pregunta("dame: a,b,c,d,e / tres", saber))
    print()
    print(explicar_pregunta("dame: tres", saber))
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
