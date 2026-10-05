# -*- coding: utf-8 -*-
"""
Corre TODAS las pruebas del proyecto, de una vez.

Regla del metodo: si algo viejo se rompe, se arregla antes de seguir.  Por eso
nunca se corre solo la prueba de hoy: se corren todas.

Uso:  python pruebas/correr_todas.py
"""

import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_PRUEBAS = os.path.join(RAIZ, "pruebas")


def main():
    archivos = sorted(
        f for f in os.listdir(DIR_PRUEBAS)
        if f.startswith("test_") and f.endswith(".py")
    )
    if not archivos:
        print("no hay pruebas todavia")
        return 1

    fallos = []
    bien_total = 0
    mal_total = 0
    for nombre in archivos:
        print("\n" + "#" * 72)
        print("# %s" % nombre)
        print("#" * 72)
        r = subprocess.run(
            [sys.executable, os.path.join(DIR_PRUEBAS, nombre)],
            cwd=RAIZ, capture_output=True, text=True,
        )
        print(r.stdout, end="")
        if r.stderr:
            print(r.stderr, end="", file=sys.stderr)
        if r.returncode != 0:
            fallos.append(nombre)
        # El total del archivo: cada prueba lo dice de una forma ("TOTAL: 8/8" o
        # "UNIDAD 5.4: 41/41").  Se coge la ULTIMA, que es la del final.
        encontrados = re.findall(r"(?:^|\n)(?:TOTAL|UNIDAD [0-9.]+):\s*(\d+)/(\d+)", r.stdout)
        if encontrados:
            b, t = encontrados[-1]
            bien_total += int(b)
            mal_total += int(t)
            # Un archivo que dice "8/10" esta en rojo aunque salga con exito.
            if int(b) != int(t):
                fallos.append("%s (dice %s/%s: pruebas en rojo dentro del archivo)" % (nombre, b, t))
        else:
            # ESTO NO ES UN AVISO: si un archivo no dice su total, el recuento global puede
            # dar VERDE con el archivo entero fuera de cuenta.  Ya paso (unidad 7.2: 255
            # pruebas no se contaban y el total seguia diciendo VERDE).  Es un FALLO.
            print("  FALLA: %s no dice su total (TOTAL: n/m o UNIDAD x.y: n/m)" % nombre)
            fallos.append("%s (no dice su total: no se puede contar)" % nombre)

    # Los casos de Carlos corren por la OTRA via (la del probador).  Si esa via y el motor se
    # desincronizan, esto se pone ROJO.  Ya paso una vez (unidad 3.3): el probador tenia su
    # propio despacho y se quedo atras.  Por eso se corre aqui tambien.
    print("\n" + "#" * 72)
    print("# probar.py --casos  (los casos, por la via del probador)")
    print("#" * 72)
    r = subprocess.run([sys.executable, os.path.join(RAIZ, "probar.py"), "--casos"], cwd=RAIZ)
    if r.returncode != 0:
        fallos.append("probar.py --casos")

    print("\n" + "=" * 72)
    print("TOTAL DEL PROYECTO: %d/%d pruebas de unidad" % (bien_total, mal_total))
    print("PRUEBAS: %d archivo(s) + los casos, %d con fallos" % (len(archivos), len(fallos)))
    for f in fallos:
        print("  FALLA: %s" % f)
    if fallos:
        print("RESULTADO GLOBAL: ROJO")
        return 1
    print("RESULTADO GLOBAL: VERDE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
