# -*- coding: utf-8 -*-
"""
Corre TODAS las pruebas del proyecto, de una vez.

Uso:
  python pruebas/correr_todas.py            todas las pruebas (unos segundos).  Las pruebas grandes
                                            recorren una MUESTRA: las fronteras y unos cuantos al azar
                                            fijo (decision de Carlos: no todas las combinaciones)
  python pruebas/correr_todas.py --todo     ademas de lo de siempre, imprime la salida entera de
                                            cada archivo
  python pruebas/correr_todas.py --separados  cada archivo en su propio proceso (mas lento)

Regla del metodo: si algo viejo se rompe, se arregla antes de seguir.  Por eso nunca se corre
solo la prueba de hoy: se corren todas.

LO QUE SE VE: una linea por archivo, y la salida ENTERA de cualquier archivo que falle (nada de un
fallo escondido detras de un filtro).  La salida entera de TODO queda siempre en
pruebas/ultima_salida.txt, para leerla cuando haga falta.

UNA PRUEBA = UNA AFIRMACION.  Una prueba de hierro cuenta como UNA, recorra 10 casos o 50.000
(ver _muestras.py).  Un archivo que no dice su total, o que dice 8/10, es un FALLO.
"""

import os
import re
import subprocess
import sys
import time

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_PRUEBAS = os.path.join(RAIZ, "pruebas")
SALIDA = os.path.join(DIR_PRUEBAS, "ultima_salida.txt")


def main():
    todo = "--todo" in sys.argv
    entorno = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    archivos = sorted(f for f in os.listdir(DIR_PRUEBAS) if f.startswith("test_") and f.endswith(".py"))
    if not archivos:
        print("no hay pruebas todavia")
        return 1
    print("PRUEBAS DE EUCLIDES  (las grandes recorren una muestra: fronteras + azar fijo)")
    print("-" * 72)
    fallos = []
    bien_total = total_total = 0
    log = io_abrir()
    t0 = time.time()
    os.environ.update(entorno)
    separados = "--separados" in sys.argv
    for nombre in archivos:
        t = time.time()
        if separados:
            r = subprocess.run([sys.executable, os.path.join(DIR_PRUEBAS, nombre)], cwd=RAIZ,
                               capture_output=True, text=True, env=entorno)
        else:
            antes = dict(os.environ)
            r = _correr_aqui(os.path.join(DIR_PRUEBAS, nombre))
            os.environ.clear()
            os.environ.update(antes)
        seg = time.time() - t
        log.write("\n" + "#" * 72 + "\n# %s\n" % nombre + "#" * 72 + "\n" + r.stdout + r.stderr)
        mal = r.returncode != 0
        encontrados = re.findall(r"(?:^|\n)(?:TOTAL|UNIDAD [0-9A-Z.]+):\s*(\d+)/(\d+)", r.stdout)
        if encontrados:
            b, tt = int(encontrados[-1][0]), int(encontrados[-1][1])
            bien_total += b
            total_total += tt
            if b != tt:
                mal = True
            cuenta = "%d/%d" % (b, tt)
        else:
            mal = True
            cuenta = "SIN TOTAL"
        print("  %-6s %-18s %9s   %5.1fs" % ("FALLA" if mal else "bien", nombre, cuenta, seg))
        if mal:
            fallos.append(nombre)
        if mal or todo:
            print(r.stdout + r.stderr)
    # Los casos de Carlos corren por la OTRA via (la del probador): si se desincroniza, ROJO.
    t = time.time()
    r = subprocess.run([sys.executable, os.path.join(RAIZ, "probar.py"), "--casos"], cwd=RAIZ,
                       capture_output=True, text=True, env=entorno)
    log.write("\n# probar.py --casos\n" + r.stdout + r.stderr)
    m = re.search(r"mis casos: (\d+) bien, (\d+) fallan", r.stdout)
    casos = "%s/%d" % (m.group(1), int(m.group(1)) + int(m.group(2))) if m else "?"
    mal = r.returncode != 0
    print("  %-6s %-18s %9s   %5.1fs" % ("FALLA" if mal else "bien", "mis_casos.txt", casos,
                                         time.time() - t))
    if mal:
        fallos.append("probar.py --casos")
        # de los casos solo se ensenan los que FALLAN (con su explicacion); todo lo demas esta en
        # pruebas/ultima_salida.txt
        trozos = r.stdout.split("\n  [")
        print("\n".join("  [" + t for t in trozos[1:] if t.startswith("FALLA")))
        print(r.stderr)
    log.close()
    print("-" * 72)
    print("TOTAL DEL PROYECTO: %d/%d afirmaciones  +  %s casos   (%d archivos, %.0f s)"
          % (bien_total, total_total, casos, len(archivos), time.time() - t0))
    print("(la salida entera de cada archivo esta en pruebas/ultima_salida.txt)")
    for f in fallos:
        print("  FALLA: %s" % f)
    if fallos:
        print("RESULTADO GLOBAL: ROJO")
        return 1
    print("RESULTADO GLOBAL: VERDE")
    return 0


class _Resultado:
    def __init__(self, stdout, stderr, returncode):
        self.stdout, self.stderr, self.returncode = stdout, stderr, returncode


def _correr_aqui(ruta):
    """Corre un archivo de pruebas DENTRO de este mismo proceso (el motor se carga una sola vez;
    asi tarda la mitad).  Es igual que lanzarlo aparte: se captura lo que imprime y como sale.
    Con --separados se lanza cada archivo en su propio proceso, como antes."""
    import contextlib
    import io
    import runpy
    import traceback
    salida, errores = io.StringIO(), io.StringIO()
    codigo = 0
    argv = sys.argv
    sys.argv = [ruta]
    cwd = os.getcwd()
    os.chdir(RAIZ)
    try:
        with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(errores):
            try:
                runpy.run_path(ruta, run_name="__main__")
            except SystemExit as e:
                codigo = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
            except Exception:
                traceback.print_exc()
                codigo = 1
    finally:
        sys.argv = argv
        os.chdir(cwd)
    return _Resultado(salida.getvalue(), errores.getvalue(), codigo)


def io_abrir():
    import io
    return io.open(SALIDA, "w", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
