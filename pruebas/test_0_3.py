# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 0.3 - PERTENENCIA a un grupo.

Lo que esta unidad tiene que dejar claro:
  - pertenece / no_pertenece / no_decidible son TRES respuestas, no dos.
  - "no pertenece" (tiene el atributo con otro valor) NO es lo mismo que "no se sabe"
    (no le esta declarado el atributo).
  - la pertenencia depende del criterio: el mismo objeto puede pertenecer a varios grupos.

  A) CASOS DE EJEMPLO  - los del conocimiento.
  B) CASOS DE DOMINIO  - no programados, con trampas.

Uso:  python pruebas/test_0_3.py
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

from motor import (cargar_conocimiento, decidir_0_3_pertenencia,  # noqa: E402
                   escena_0_2, parsear_criterio, explicar_0_3_pertenencia, explicar_pregunta)


# (titulo, escena, criterio, [conclusion esperada por objeto])
EJEMPLOS = [
    ("E1 una taza roja SI pertenece a los rojos",
     "taza(color=rojo)", "color=rojo", ["pertenece"]),
    ("E2 un plato azul NO pertenece a los rojos",
     "plato(color=azul)", "color=rojo", ["no_pertenece"]),
]

DOMINIO = [
    ("D1 TRAMPA: al objeto no le esta declarado el color -> NO SE SABE (no es 'no pertenece')",
     "vaso(forma=cubo)", "color=rojo", ["no_decidible"]),

    ("D2 TRAMPA: el MISMO objeto pertenece a DOS grupos distintos, segun el criterio",
     "triangulo(color=verde,forma=triangulo)", "color=verde", ["pertenece"]),

    ("D3 el mismo objeto, el otro criterio",
     "triangulo(color=verde,forma=triangulo)", "forma=triangulo", ["pertenece"]),

    ("D4 TRAMPA: color=rojo contra tono=rojo (el valor no es el atributo)",
     "caja(tono=rojo)", "color=rojo", ["no_decidible"]),

    ("D5 un mismo nombre con dos colores distintos son DOS objetos: cada uno con lo suyo",
     "casa(color=rojo); casa(color=azul)", "color=rojo", ["pertenece", "no_pertenece"]),

    ("D6 tres objetos: pertenece, no pertenece y no se sabe, cada uno en su sitio",
     "taza(color=rojo); plato(color=azul); vaso(forma=cubo)", "color=rojo",
     ["pertenece", "no_pertenece", "no_decidible"]),

    ("D7 TRAMPA: valor distinto en el mismo atributo -> NO pertenece (no 'no se sabe')",
     "cubo(color=verde)", "color=rojo", ["no_pertenece"]),

    ("D8 el caso de Carlos: el mismo nombre con dos colores son dos objetos, cada uno con su veredicto",
     "carro(color=negro); carro(color=blanco)", "color=negro",
     ["pertenece", "no_pertenece"]),

    ("D9 el mismo nombre repetido SIN nada que lo distinga: sigue siendo un solo objeto",
     "carro(color=negro); carro(color=negro)", "color=negro", ["pertenece"]),
]


def correr(casos, saber, etiqueta):
    print("=" * 76)
    print(etiqueta)
    print("=" * 76)
    bien = 0
    for titulo, texto, crit_txt, esperado in casos:
        escena = escena_0_2(texto)
        criterio = parsear_criterio(crit_txt)
        rs = decidir_0_3_pertenencia(escena, criterio, saber)
        obtenido = [r["conclusion"] for r in rs]
        ok = obtenido == esperado
        bien += ok
        print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
        if not ok:
            print("       esperado=%s  obtenido=%s" % (esperado, obtenido))
            print(explicar_0_3_pertenencia(escena, criterio, saber))
    print("-- %d/%d correctos\n" % (bien, len(casos)))
    return bien, len(casos)


def correr_robustez(saber):
    """Lo mal escrito se dice, no revienta.  Vale tambien para la unidad 0.3."""
    print("=" * 76)
    print("C) ROBUSTEZ - pertenencia mal escrita: se dice, no revienta")
    print("=" * 76)
    entradas = [
        "pertenece :",
        "pertenece colorrojo: taza(color=rojo)",
        "pertenece color=rojo: taza(colorrojo)",
        "pertenece =rojo: taza(color=rojo)",
    ]
    bien = 0
    for e in entradas:
        try:
            salida = explicar_pregunta(e, saber)
            if isinstance(salida, str) and salida.startswith("NO ENTIENDO"):
                bien += 1
                print("OK     se dice 'NO ENTIENDO' -> %r" % e)
            else:
                print("FALLA  deberia decir 'NO ENTIENDO' -> %r" % e)
                print("       dijo: %s" % (salida.splitlines()[0] if salida else "nada"))
        except Exception as ex:
            print("FALLA  reviento con %r -> %r" % (e, ex))
    print("-- %d/%d correctos\n" % (bien, len(entradas)))
    return bien, len(entradas)


def main():
    saber = cargar_conocimiento()
    a = correr(EJEMPLOS, saber, "A) PERTENENCIA - casos de ejemplo")
    b = correr(DOMINIO, saber, "B) PERTENENCIA - prueba de dominio (no programados)")
    rb = correr_robustez(saber)

    print("=" * 76)
    print("TRAZA DE LA TRAMPA PRINCIPAL (D1: no se sabe, que NO es lo mismo que no pertenecer)")
    print("=" * 76)
    print(explicar_0_3_pertenencia(escena_0_2("vaso(forma=cubo)"), parsear_criterio("color=rojo"), saber))
    print()

    ok = a[0] + b[0] + rb[0]
    total = a[1] + b[1] + rb[1]
    print("TOTAL: %d/%d" % (ok, total))
    if ok != total:
        print("RESULTADO: ROJO")
        return 1
    print("RESULTADO: VERDE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
