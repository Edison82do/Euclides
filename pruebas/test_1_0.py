# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 1.0 - SUBITIZING (reconocer una cantidad de un vistazo).

Lo que esta unidad tiene que dejar claro:
  - reconocer NO es contar.  Si la figura no esta en la tabla de patrones, el sistema NO la
    cuenta: dice "no_reconocido".  Esa es la prueba de fuego de la unidad.
  - la DISPOSICION es lo que hace reconocible un grupo.  Una disposicion no canonica de 4
    elementos NO se reconoce (y no se cuenta).
  - la misma cantidad en dos disposiciones distintas sigue siendo la misma cantidad.

  A) CASOS DE EJEMPLO  - los del conocimiento.
  B) CASOS DE DOMINIO  - no programados, con trampas.
  C) ROBUSTEZ          - lo mal escrito se dice, no revienta.

Uso:  python pruebas/test_1_0.py
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

from motor import (cargar_conocimiento, decidir_1_0_subitizar,  # noqa: E402
                   explicar_1_0_subitizar, explicar_pregunta)


# (titulo, figura, conclusion esperada, etiqueta esperada)
EJEMPLOS = [
    ("E1 un punto", ".../.x./...", "reconocido", "uno"),
    ("E2 cuatro en las esquinas (como un dado)", "x.x/.../x.x", "reconocido", "cuatro"),
]

DOMINIO = [
    ("D1 TRAMPA: 4 elementos en una disposicion NO conocida -> no lo reconoce, y NO lo cuenta",
     "x../xx./x.x", "no_reconocido", None),

    ("D2 la MISMA cantidad en otra disposicion declarada: sigue siendo cuatro",
     "xx./xx./...", "reconocido", "cuatro"),

    ("D3 nueve elementos: no se reconoce de un vistazo",
     "xxx/xxx/xxx", "no_reconocido", None),

    ("D4 tres en diagonal (patron declarado)",
     "x../.x./..x", "reconocido", "tres"),

    ("D5 TRAMPA: dos elementos, pero en una disposicion que no esta en la tabla",
     "x.x/.../...", "no_reconocido", None),

    ("D6 cinco, como en el dado",
     "x.x/.x./x.x", "reconocido", "cinco"),

    ("D7 TRAMPA: seis, como en el dado; SI se reconoce aunque sean mas de cuatro",
     "x.x/x.x/x.x", "reconocido", "seis"),
]


def correr(casos, saber, etiqueta):
    print("=" * 76)
    print(etiqueta)
    print("=" * 76)
    bien = 0
    for titulo, figura, concl_esp, etiq_esp in casos:
        r = decidir_1_0_subitizar(figura, saber)
        concl, etiq = r["conclusion"], r["etiqueta"]
        ok = concl == concl_esp and etiq == etiq_esp
        bien += ok
        print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
        if not ok:
            print("       esperado=%s/%s  obtenido=%s/%s" % (concl_esp, etiq_esp, concl, etiq))
            print(explicar_1_0_subitizar(figura, saber))
    print("-- %d/%d correctos\n" % (bien, len(casos)))
    return bien, len(casos)


def correr_robustez(saber):
    print("=" * 76)
    print("C) ROBUSTEZ - figura mal escrita: se dice, no revienta")
    print("=" * 76)
    entradas = [
        "subitizar: x.x/...",
        "subitizar: x.x/..../x.x",
        "subitizar: xx/xx/..",
        "subitizar: ",
    ]
    bien = 0
    for e in entradas:
        try:
            salida = explicar_pregunta(e, saber)
            if isinstance(salida, str) and (salida.startswith("NO ENTIENDO") or salida.startswith("RESULTADO: no_reconocido")):
                bien += 1
                print("OK     se dice que no -> %r" % e)
            else:
                print("FALLA  deberia decir 'no' -> %r" % e)
                print("       dijo: %s" % (salida.splitlines()[0] if salida else "nada"))
        except Exception as ex:
            print("FALLA  reviento con %r -> %r" % (e, ex))
    print("-- %d/%d correctos\n" % (bien, len(entradas)))
    return bien, len(entradas)


def main():
    saber = cargar_conocimiento()
    a = correr(EJEMPLOS, saber, "A) SUBITIZING - casos de ejemplo")
    b = correr(DOMINIO, saber, "B) SUBITIZING - prueba de dominio (no programados)")
    rb = correr_robustez(saber)

    print("=" * 76)
    print("TRAZA DE LA TRAMPA PRINCIPAL (D1: 4 elementos que NO se reconocen y NO se cuentan)")
    print("=" * 76)
    print(explicar_1_0_subitizar("x../xx./x.x", saber))
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
