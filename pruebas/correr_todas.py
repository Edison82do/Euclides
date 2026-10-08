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
  python pruebas/correr_todas.py --parte 1/2  la mitad de los archivos; luego --parte 2/2 (con los casos)

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
    # --parte k/n: solo una parte de los archivos (para maquinas lentas o con limite de tiempo: se corren las
    # n partes una detras de otra y entre todas son la bateria entera).  Los casos van en la ultima parte.
    parte = None
    if "--parte" in sys.argv:
        k, _, n = sys.argv[sys.argv.index("--parte") + 1].partition("/")
        parte = (int(k), int(n))
        archivos = archivos[parte[0] - 1::parte[1]]
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
    # Los casos de Carlos van partidos en TROZOS, como un trabajo mas de la cola (7 oct 2026, tarde: los casos
    # en un solo proceso aparte eran lo que mas tardaba y competian con las pruebas).  Y primero lo que mas
    # tarda (los trozos y los archivos grandes): asi los dos trabajadores acaban a la vez.
    t_casos = time.time()
    trozos = ["casos:%d/%d" % (k, _TROZOS) for k in range(_TROZOS)] if not parte or parte[0] == parte[1] else []
    archivos = trozos + sorted(archivos, key=lambda f: -os.path.getsize(os.path.join(DIR_PRUEBAS, f)))
    casos_out, casos_err, casos_mal = [], [], False
    if separados:
        resultados = ((n,) + _separado(n, entorno) for n in archivos)
    else:
        import multiprocessing
        trabajadores = max(1, min(2, (os.cpu_count() or 1)))
        pool = multiprocessing.get_context("fork").Pool(trabajadores) if trabajadores > 1 else None
        resultados = pool.imap(_trabajo, archivos) if pool else map(_trabajo, archivos)
    for nombre, r, seg in resultados:
        if nombre.startswith("casos:"):
            casos_out.append(r.stdout)
            casos_err.append(r.stderr)
            casos_mal = casos_mal or r.returncode != 0
            continue
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
    if not separados and pool:
        pool.close()
        pool.join()
    # Los casos de Carlos corren por la OTRA via (la del probador): si se desincroniza, ROJO.
    r = _Resultado("\n".join(casos_out), "\n".join(casos_err), 1 if casos_mal else 0)
    log.write("\n# probar.py --casos\n" + r.stdout + r.stderr)
    cuentas = re.findall(r"mis casos: (\d+) bien, (\d+) fallan", r.stdout)
    if not trozos:
        casos, casos_mal = "(en la ultima parte)", False
    elif len(cuentas) == _TROZOS:
        b_c = sum(int(x[0]) for x in cuentas)
        casos = "%d/%d" % (b_c, b_c + sum(int(x[1]) for x in cuentas))
    else:
        casos, casos_mal = "?", True
    mal = casos_mal
    print("  %-6s %-18s %9s   %5.1fs" % ("FALLA" if mal else "bien", "mis_casos.txt", casos,
                                         time.time() - t_casos))
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
          % (bien_total, total_total, casos, len(archivos) - len(trozos), time.time() - t0))
    print("(la salida entera de cada archivo esta en pruebas/ultima_salida.txt)")
    for f in fallos:
        print("  FALLA: %s" % f)
    if fallos:
        print("RESULTADO GLOBAL: ROJO")
        return 1
    print("RESULTADO GLOBAL: VERDE")
    return 0


_TROZOS = 4


def _trabajo(nombre):
    """Un archivo de pruebas en un trabajador (su propio proceso, con el motor cargado una vez).
    'casos:k/n' es un trozo de mis_casos.txt, que corre por la via del probador (probar.py --casos)."""
    t = time.time()
    if nombre.startswith("casos:"):
        r = subprocess.run([sys.executable, os.path.join(RAIZ, "probar.py"), "--casos", "--trozo", nombre[6:]],
                           cwd=RAIZ, capture_output=True, text=True,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        return nombre, r, time.time() - t
    antes = dict(os.environ)
    r = _correr_aqui(os.path.join(DIR_PRUEBAS, nombre))
    os.environ.clear()
    os.environ.update(antes)
    return nombre, r, time.time() - t


def _separado(nombre, entorno):
    if nombre.startswith("casos:"):
        _, r, seg = _trabajo(nombre)
        return r, seg
    t = time.time()
    r = subprocess.run([sys.executable, os.path.join(DIR_PRUEBAS, nombre)], cwd=RAIZ,
                       capture_output=True, text=True, env=entorno)
    return r, time.time() - t


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
