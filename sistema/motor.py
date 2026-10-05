# -*- coding: utf-8 -*-
"""
Motor de Euclides - sistema determinista de conocimiento matematico.

Que sabe hacer: lo que dicen PROGRESO.md y la ayuda del probador (python probar.py, "ayuda").
Desde el nivel 0 (objetos y grupos) hasta el 7 (metodos de calculo por columnas), y el
resolvedor de problemas (R.1).

Donde esta el codigo: en sistema/partes/, una pieza por nivel (ver partes/__init__.py).  Este
archivo es la FACHADA: junta las piezas, y `import motor` sigue dando acceso a todo.

Reglas del proyecto que este motor respeta:
  - No adivina: si no hay regla aplicable o falta un dato, lo dice.
  - Todo se puede rastrear: cada respuesta sale con la regla y el conocimiento que la respaldan.
  - Nada de cajas negras: cada cuenta sale de un METODO ensenado (dedos, derivar, columnas).

Uso:
    python motor.py conocimiento
    python motor.py partes
    python motor.py escena "silla,mesa"
"""


# ----------------------------------------------------------------------------------------------
# DESDE EL 5 DE OCTUBRE DE 2026 EL MOTOR ESTA PARTIDO EN PIEZAS (sistema/partes/).
# Este archivo es la FACHADA: carga todas las partes y las junta en UN SOLO espacio de nombres,
# de modo que `import motor` y `from motor import X` siguen funcionando exactamente igual.
# Donde esta cada cosa:  ver sistema/partes/__init__.py  (y `python motor.py partes`).
# ----------------------------------------------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from partes import juntar as _juntar  # noqa: E402

_ESPACIO = _juntar()
globals().update({k: v for k, v in _ESPACIO.items() if k not in ('__doc__',)})


# ---------------------------------------------------------------- linea de ordenes

def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    orden = argv[1]
    saber = cargar_conocimiento()

    if orden == "conocimiento":
        print("Conocimientos cargados (%d):" % len(saber))
        for cid, d in sorted(saber.items()):
            print("  - %-24s %-10s %s" % (cid, d.get("categoria", "?"), d.get("nombre", "?")))
        return 0

    if orden == "partes":
        print("Donde esta cada cosa del motor (sistema/partes/):")
        por_parte = {}
        for nombre, parte in sorted(_ESPACIO["_DONDE_ESTA"].items()):
            por_parte.setdefault(parte, []).append(nombre)
        for parte, nombres in por_parte.items():
            print("  %-22s %4d nombres" % (parte, len(nombres)))
        return 0

    if orden == "escena":
        if len(argv) < 3:
            print("falta la escena, por ejemplo: escena \"silla,mesa\"")
            return 2
        print(explicar_pregunta(" ".join(argv[2:]), saber))
        return 0

    print("orden desconocida: %s" % orden)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
