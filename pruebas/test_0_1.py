# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 0.1 - un objeto o varios objetos.

Aviso (corregido el 2026-10-03): esta unidad NO decide "grupos". Solo dice si hay una cosa o
varias. La palabra GRUPO es de la unidad 0.2 (varios objetos que comparten un atributo).

Hay dos clases de casos:
  A) CASOS DE EJEMPLO  - los que estan escritos en el conocimiento.
  B) CASOS DE DOMINIO  - NO programados en el conocimiento: casos nuevos que el
     sistema tiene que resolver con lo que ya sabe.  Es la prueba de dominio de la
     unidad.  Al menos uno es una TRAMPA sacada del carne de errores.

Uso:  python pruebas/test_0_1.py
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

from motor import cargar_conocimiento, decidir, explicar  # noqa: E402


def ref(ident, nombre=None):
    return {"id": ident, "nombre": nombre or ident}


# ------------------------------------------------------------------ clase A
# Los ejemplos que ya estan declarados en el conocimiento.
CASOS_EJEMPLO = [
    ("A1 escena con una sola entidad", [ref("silla")], "un_objeto"),
    ("A2 escena con dos entidades distintas", [ref("silla"), ref("mesa")], "varios_objetos"),
    ("A3 la misma silla senalada dos veces",
     [ref("silla"), ref("silla")], "un_objeto"),
]

# ------------------------------------------------------------------ clase B
# Casos NUEVOS, no escritos en el conocimiento.  Prueba de dominio de la unidad.
CASOS_DOMINIO = [
    ("B1 una taza sola", [ref("taza_X")], "un_objeto"),

    # TRAMPA 1: tres referencias al MISMO objeto.  No es un grupo.
    ("B2 TRAMPA: la misma taza senalada tres veces",
     [ref("taza_X"), ref("taza_X"), ref("taza_X")], "un_objeto"),

    # TRAMPA 2: dos objetos DISTINTOS que se llaman igual.  Si es un grupo.
    ("B3 TRAMPA: dos sillas distintas con el mismo nombre visible",
     [ref("silla_A", "silla"), ref("silla_B", "silla")], "varios_objetos"),

    ("B4 tres objetos distintos", [ref("libro_L"), ref("lapiz_P"), ref("vaso_V")], "varios_objetos"),

    ("B5 escena sin entidades", [], "no_decidible"),
]


def correr(casos, saber, etiqueta):
    print("=" * 72)
    print(etiqueta)
    print("=" * 72)
    bien = 0
    for titulo, escena, esperado in casos:
        try:
            r = decidir(escena, saber)
            obtenido = r["conclusion"]
        except ValueError:
            obtenido = "no_decidible"
        ok = obtenido == esperado
        bien += ok
        print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
        print("       esperado=%s  obtenido=%s" % (esperado, obtenido))
        if not ok:
            print(explicar(escena, saber))
    print("-- %d/%d correctos\n" % (bien, len(casos)))
    return bien, len(casos)


def main():
    saber = cargar_conocimiento()
    a = correr(CASOS_EJEMPLO, saber, "A) CASOS DE EJEMPLO (los que ya estan en el conocimiento)")
    b = correr(CASOS_DOMINIO, saber, "B) PRUEBA DE DOMINIO (casos no programados)")

    print("=" * 72)
    print("TRAZA DE LA TRAMPA PRINCIPAL (B3: dos sillas distintas con el mismo nombre)")
    print("=" * 72)
    print(explicar([ref("silla_A", "silla"), ref("silla_B", "silla")], saber))
    print()

    total_ok, total = a[0] + b[0], a[1] + b[1]
    print("TOTAL: %d/%d" % (total_ok, total))
    if total_ok != total:
        print("RESULTADO: ROJO")
        return 1
    print("RESULTADO: VERDE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
