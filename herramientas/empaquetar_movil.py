# -*- coding: utf-8 -*-
"""
Empaqueta Euclides en UN SOLO ARCHIVO .py, para poder ejecutarlo en un movil
(Pydroid 3 en Android, Pythonista, Termux, o cualquier Python 3).

No toca nada del proyecto: lee motor.py, probar.py, mis_casos.txt y los .kn, los
embebe como texto y genera un lanzador que, al ejecutarse, los escribe en una
carpeta temporal y corre el probador tal cual.

Uso:  py -3 herramientas/empaquetar_movil.py
Salida:  movil/euclides_movil.py
"""

import os
import sys
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_MOVIL = os.path.join(RAIZ, "movil")

PLANTILLA = '''# -*- coding: utf-8 -*-
"""
EUCLIDES - version movil, en UN SOLO ARCHIVO.

Generado automaticamente por herramientas/empaquetar_movil.py. No editar a mano.

Que es: el sistema deterministico de conocimiento matematico de Carlos, para
llevarlo en el bolsillo. No tiene dependencias: solo Python 3.

Como usarlo en Android (lo mas facil):
  1. Instala "Pydroid 3" desde Play Store (gratis).
  2. Abre este archivo con Pydroid 3.
  3. Pulsa el boton de PLAY (el triangulo).
  4. Escribe preguntas y pulsa Enter.

En Termux:
  pkg install python
  python euclides_movil.py

Al arrancar se descomprime solo en una carpeta temporal y corre el probador.
"""

import os
import runpy
import sys
import tempfile

# El motor: desde el 5 oct 2026 son VARIOS archivos (sistema/motor.py + sistema/partes/*.py)
SISTEMA = {sistema!r}

PROBAR = {probar!r}

MIS_CASOS = {casos!r}

ARCHIVOS_KN = {kn!r}


def extraer(destino):
    os.makedirs(os.path.join(destino, "sistema", "partes"), exist_ok=True)
    os.makedirs(os.path.join(destino, "conocimiento"), exist_ok=True)

    for rel, contenido in SISTEMA.items():
        with open(os.path.join(destino, "sistema", *rel.split("/")), "w", encoding="utf-8") as f:
            f.write(contenido)
    with open(os.path.join(destino, "probar.py"), "w", encoding="utf-8") as f:
        f.write(PROBAR)
    with open(os.path.join(destino, "mis_casos.txt"), "w", encoding="utf-8") as f:
        f.write(MIS_CASOS)
    for nombre, contenido in ARCHIVOS_KN.items():
        with open(os.path.join(destino, "conocimiento", nombre), "w", encoding="utf-8") as f:
            f.write(contenido)


def main():
    try:
        destino = tempfile.mkdtemp(prefix="euclides_")
    except Exception:
        destino = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_euclides_tmp")
        os.makedirs(destino, exist_ok=True)

    extraer(destino)

    lanzador = os.path.join(destino, "probar.py")
    # los argumentos que le hayan pasado a este archivo (--casos, o una pregunta)
    sys.argv = [lanzador] + sys.argv[1:]

    print()
    print("EUCLIDES - sistema deterministico de conocimiento matematico")
    print("El sistema no adivina: si no entiende algo, lo dice.")
    print("Escribe 'ayuda' para ver que sabe hacer, y 'salir' para terminar.")
    print()

    try:
        runpy.run_path(lanzador, run_name="__main__")
    except SystemExit:
        pass
    except KeyboardInterrupt:
        print()
        print("Hasta luego.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


def leer(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()


def main():
    dir_sis = os.path.join(RAIZ, "sistema")
    sistema = {}
    for base, dirs, ficheros in os.walk(dir_sis):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for nombre in sorted(ficheros):
            if nombre.endswith(".py"):
                completo = os.path.join(base, nombre)
                sistema[os.path.relpath(completo, dir_sis).replace(os.sep, "/")] = leer(completo)
    probar = leer(os.path.join(RAIZ, "probar.py"))
    casos = leer(os.path.join(RAIZ, "mis_casos.txt"))

    dir_kn = os.path.join(RAIZ, "conocimiento")
    kn = {}
    for nombre in sorted(os.listdir(dir_kn)):
        if nombre.endswith(".kn"):
            kn[nombre] = leer(os.path.join(dir_kn, nombre))

    codigo = PLANTILLA.format(sistema=sistema, probar=probar, casos=casos, kn=kn)
    # que compile es la primera prueba
    compile(codigo, "euclides_movil.py", "exec")

    os.makedirs(DIR_MOVIL, exist_ok=True)
    ruta_py = os.path.join(DIR_MOVIL, "euclides_movil.py")
    with open(ruta_py, "w", encoding="utf-8") as f:
        f.write(codigo)

    # y tambien el proyecto entero, en un zip
    ruta_zip = os.path.join(DIR_MOVIL, "Euclides_codigo.zip")
    with zipfile.ZipFile(ruta_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _, ficheros in os.walk(RAIZ):
            if os.path.join(RAIZ, "movil") in base or os.path.join(RAIZ, ".git") in base:
                continue
            for nombre in ficheros:
                if nombre.endswith((".pyc",)):
                    continue
                completo = os.path.join(base, nombre)
                z.write(completo, os.path.relpath(completo, RAIZ))

    print("OK: %s  (%d KB, %d .kn embebidos)" % (ruta_py, len(codigo.encode("utf-8")) // 1024, len(kn)))
    print("OK: %s  (%d KB)" % (ruta_zip, os.path.getsize(ruta_zip) // 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
