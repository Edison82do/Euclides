# -*- coding: utf-8 -*-
"""
PRUEBAS DE LA AYUDA  -  que no se quede atras

POR QUE ESTAS PRUEBAS EXISTEN:
  La ayuda que se ve escribiendo "ayuda" se quedo CONGELADA en la unidad 3.1 durante varias
  unidades.  Habia DOS textos (el docstring del fichero y una constante AYUDA) y solo se
  actualizaba uno.  Lo cazo Carlos: "cuando escribo ayuda solo llega a la unidad 3.1".

  Arreglado de raiz: AYUDA es EL MISMO texto que la cabecera (el docstring).  Y estas pruebas
  vigilan que la ayuda no se vuelva a quedar atras: si el sistema sabe hacer algo, la ayuda lo
  tiene que decir.

Lo que hay que demostrar:
  1. La ayuda es UNA SOLA VERDAD (la constante sale del docstring).
  2. La ayuda menciona TODAS las unidades.
  3. La ayuda menciona TODAS las ordenes que el probador entiende de verdad.
  4. Y no se quedo ningun texto de ayuda viejo por ahi.
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, RAIZ)

import probar  # noqa: E402

fallos = []
pruebas = []


def check(nombre, cond, detalle=""):
    pruebas.append(nombre)
    if not cond:
        fallos.append("%s  %s" % (nombre, detalle))


AYUDA = probar.AYUDA

# ---------------------------------------------------------------------------
# A. UNA SOLA VERDAD
# ---------------------------------------------------------------------------
check("A1 la ayuda es el docstring (una sola verdad)", probar.__doc__ in AYUDA or
      AYUDA.strip().startswith(probar.__doc__.strip()[:60]), AYUDA[:80])
check("A2 la ayuda no esta vacia", len(AYUDA) > 2000, len(AYUDA))

fuente = io.open(os.path.join(RAIZ, "probar.py"), encoding="utf-8").read()
n = fuente.count("Escribe una pregunta y pulsa Enter")
check("A3 no hay un segundo texto de ayuda suelto", n <= 1, "aparece %d veces" % n)

# ---------------------------------------------------------------------------
# B. TODAS LAS UNIDADES EN LA AYUDA
# ---------------------------------------------------------------------------
# Las unidades que el sistema sabe hacer, puestas a mano AQUI a proposito: si se anyade una unidad
# nueva, esta lista se toca y la prueba obliga a tocar la ayuda.
DEBE_ESTAR = [
    "0.1", "0.2", "0.3",          # objetos y grupos
    "1.0",                        # subitizar
    "2.1", "2.2", "2.3", "2.4", "2.5", "2.6",   # contar
    "3.1", "3.2", "3.3", "3.4",   # simbolos, el cero, las dos listas, el puente
    "4.1", "4.2",                 # comparar
    "5.1", "5.2", "5.3", "5.4", "5.5",   # operaciones
    "6.1", "6.2", "6.3", "6.5", "6.7",   # la secuencia, las decenas, la tabla, partir, la centena
    "7.1", "7.2", "7.3", "7.4", "7.5", "7.6",   # dedos, derivar, columnas (suma, resta, centenas)
    "R.1",                        # el resolvedor
]
for u in DEBE_ESTAR:
    check("B la ayuda menciona la unidad %s" % u, u in AYUDA)

# ---------------------------------------------------------------------------
# C. TODAS LAS ORDENES QUE EL PROBADOR ENTIENDE
# ---------------------------------------------------------------------------
# Las ordenes de verdad: las que el despacho de probar.py reconoce con startswith o ==.
ORDENES = [
    "subitizar", "contar", "revisar", "siguiente", "anterior", "recitar",
    "revisar_secuencia", "cuantos", "dame", "tiene", "orden", "conteo",
    "misma_cantidad", "cifra", "palabra", "cifra_de", "puente", "caminos",
    "comparar", "comparar_cifras", "descomponer", "componer", "sumar", "anadir",
    "sumar_numeros", "comparar_numeros", "descomponer_numero", "quitar",
    "restar_numeros", "diferencia", "diferencia_numeros", "dedos", "derivar",
    "nombre", "numero", "decenas", "agrupar", "sitio", "tabla", "partir",
    "juntar_decenas", "columnas", "pertenece", "casos", "ayuda", "salir", "listas",
    "centena", "problema", "piezas", "memoria", "aprender", "olvidar", "calcular", "verdad", "ecuacion", "hueco", "de 5 en 5", "par:", "filas de", "columnas de", "grupos de", "3 x 4", "tabla del", "mitad:", "aprender: tablas", "en grupos de", "12 entre 3", "12 : 3", "3 x ? = 12", "? : 3 = 4", "tabla del 4", "tabla del 8", "divisible:", "tabla del 3", "tabla del 6", "tabla del 9", "tabla del 7", "12 x 6", "3 x 4 - 5 = c", "3 x n + 2 = 14", "redondear", "247 a la centena", "estimar", "razonable", "negativo", "intervalo", "recta:", "veces: 4 veces 6", "cuantas veces", "area: rectangulo 5 x 3", "perimetro: cuadrado de 6", "3 x 2/5", "3 x 1 2/5", "dinero: $3.45", "cambio: pago $10", "decimal: 2.35", "comparar: 0.5 y 0.45", "decimal: 2.3", "2.7 + 1.5", "mixto: 2 3/4", "recta: 7/4", "corta: 305 : 5", "corta: 347 x 6", "23 x 100", "47 : 10", "comprobar: 17 : 5", "Cuantos sobran", "tabla del 12", "divisible: 84 entre 12", "millar: 3045", "comparar: 3456 y 3465", "2/7 + 3/7", "1 - 3/8", "recta: 3/4", "3/4 de 12", "fraccion: 1/4", "1/4 de 12",
    "25 x 7 x 4", "volumen: caja 5 x 3 x 2", "volumen: cubo de 3", "volumen: 5 x 3 x ? = 60", "verdad: 2 x 3 x 4",
    "partes: 37, 25, 63; todo: ?", "todo: 100; partes: 37, ?, 25", "perimetro: 30; lados", "4 partes iguales",
]
for o in ORDENES:
    check("C la ayuda menciona la orden '%s'" % o, o in AYUDA)

# ---------------------------------------------------------------------------
# D. Y LA AYUDA ES LO QUE SALE AL PEDIRLA
# ---------------------------------------------------------------------------
# Interactivo: 'ayuda' tiene que dar exactamente esto.
# Y como argumento tambien (antes lo tomaba por una ESCENA y decia 'un_objeto').
import subprocess  # noqa: E402

r = subprocess.run([sys.executable, os.path.join(RAIZ, "probar.py"), "ayuda"],
                   cwd=RAIZ, capture_output=True, text=True)
check("D1 'probar.py ayuda' da la ayuda", "QUE SE PUEDE ESCRIBIR" in r.stdout, r.stdout[:80])
check("D2 y NO contesta 'un_objeto'", "un_objeto" not in r.stdout)

r = subprocess.run([sys.executable, os.path.join(RAIZ, "probar.py")],
                   cwd=RAIZ, capture_output=True, text=True, input="ayuda\nsalir\n")
check("D3 en interactivo tambien", "QUE SE PUEDE ESCRIBIR" in r.stdout)
check("D4 y llega hasta la ultima unidad (7.6)", "7.6" in r.stdout)

# ---------------------------------------------------------------------------
print("PRUEBAS DE LA AYUDA")
print("=" * 60)
for f in fallos[:20]:
    print("  FALLA:  " + f)
if len(fallos) > 20:
    print("  ... y %d mas" % (len(fallos) - 20))
print("-" * 60)
print("  %d de %d bien, %d fallan" % (len(pruebas) - len(fallos), len(pruebas), len(fallos)))
print("TOTAL: %d/%d" % (len(pruebas) - len(fallos), len(pruebas)))
if fallos:
    print("RESULTADO: HAY FALLOS")
    sys.exit(1)
print("RESULTADO: TODO BIEN")
