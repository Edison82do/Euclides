# -*- coding: utf-8 -*-
"""
PRUEBA: EL SISTEMA NO USA CALCULADORA (paso 1 del plan, 5 oct 2026)

Lee el CODIGO de todas las piezas del motor (sistema/partes/*.py) y busca cuentas de Python
(+, -, *, /, //, %, **).  Ninguna puede estar en el camino de una respuesta: las cuentas se
hacen con el MECANISMO (mecanismo.py: recitar, dedos, leer y escribir cifras).

No cuenta como cuenta:
  - unir textos o listas ("a" + "b", [1] + [2]);
  - moverse por una lista (i + 1, len(x) - 1, lista[i + 1]): eso es recitar, ir a la de al lado.
Y hay una LISTA BLANCA, con su porque, de los sitios donde una operacion de Python no es
matematica del sistema (leer archivos, maquetar el texto, numerar carro#1 / carro#2).

Si alguien mete un 'a + b' en un sitio nuevo, esta prueba se pone ROJA y dice donde.
"""
import ast
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTES = os.path.join(RAIZ, "sistema", "partes")
PIEZAS = os.path.join(RAIZ, "conocimiento", "piezas")     # las piezas tampoco: SIN lista blanca

LISTA_BLANCA = {
    ("__init__.py", "juntar"): "nombres de modulos (texto)",
    ("nivel_4.py", "_tamanos"): "une dos LISTAS de objetos",
    ("nivel_6.py", "decidir_6_7_centena"): "une textos ('2 centenas' + ' y ' ...)",
    ("nivel_7.py", "explicar_7_3_columnas"): "ancho de la columna al DIBUJAR la cuenta",
    ("nivel_7.py", "explicar_7_6_columnas"): "ancho de la columna al DIBUJAR la cuenta",
    ("nucleo.py", "_sangria"): "leer los .kn: cuantos espacios tiene una linea",
    ("nucleo.py", "_parse_lista"): "leer los .kn: sangria",
    ("nucleo.py", "entidades_reales"): "numerar objetos repetidos: carro#1, carro#2 (etiquetas)",
    ("resolver.py", "_formas"): "construir los patrones de lectura (texto)",
    ("resolver.py", "compilar"): "construir los patrones de lectura (texto)",
    ("resolver.py", "_montar"): "mensajes de 'no entiendo' (texto)",
    ("resolver.py", "quien_es"): "mensajes de 'no entiendo' (texto)",
    ("piezas.py", "cargar_piezas"): "el RELOJ: mirar los archivos como mucho una vez por segundo",
}
OPS = (ast.Add, ast.Sub, ast.Mult, ast.FloorDiv, ast.Mod, ast.Div, ast.Pow)


def _es_texto(n):
    return isinstance(n, ast.JoinedStr) or (isinstance(n, ast.Constant) and isinstance(n.value, str))


def _es_secuencia(n):
    return isinstance(n, (ast.List, ast.ListComp, ast.Tuple))


def _es_paso(n):
    def pos(x):
        return isinstance(x, ast.Name) or (isinstance(x, ast.Call) and (
            (isinstance(x.func, ast.Name) and x.func.id == "len") or
            (isinstance(x.func, ast.Attribute) and x.func.attr == "index")))

    def poco(x):
        return isinstance(x, ast.Constant) and isinstance(x.value, int) and x.value in (1, 2, 6)
    return isinstance(n.op, (ast.Add, ast.Sub)) and ((pos(n.left) and poco(n.right)) or
                                                     (poco(n.left) and pos(n.right)))


hallazgos = []
blancas_usadas = set()
ARCHIVOS = [(PARTES, f) for f in sorted(os.listdir(PARTES))] + \
    [(PIEZAS, f) for f in sorted(os.listdir(PIEZAS))]
for carpeta, f in ARCHIVOS:
    if not f.endswith(".py"):
        continue
    src = open(os.path.join(carpeta, f), encoding="utf-8").read()
    arbol = ast.parse(src)
    padres = {}
    for p in ast.walk(arbol):
        for c in ast.iter_child_nodes(p):
            padres[c] = p
    for fn in ast.walk(arbol):
        if not isinstance(fn, (ast.FunctionDef, ast.Lambda)):
            continue
        for n in ast.walk(fn):
            if not (isinstance(n, ast.BinOp) and isinstance(n.op, OPS)):
                continue
            if _es_texto(n.left) or _es_texto(n.right) or _es_secuencia(n.left) or \
                    _es_secuencia(n.right) or _es_paso(n):
                continue
            p, dentro = padres.get(n), False
            while p is not None and p is not fn:
                if isinstance(p, (ast.Subscript, ast.Slice)):
                    dentro = True
                    break
                p = padres.get(p)
            if dentro:
                continue
            nombre_fn = getattr(fn, "name", "<lambda>")
            if carpeta == PARTES and (f, nombre_fn) in LISTA_BLANCA:
                blancas_usadas.add((f, nombre_fn))
                continue
            hallazgos.append("%s :: %s (linea %d): %s"
                             % (f, nombre_fn, n.lineno, ast.get_source_segment(src, n)[:70]))

bien = mal = 0
print("PRUEBA: EL SISTEMA NO USA CALCULADORA")
print("=" * 60)
if hallazgos:
    mal += 1
    print("  FALLA  hay cuentas de Python fuera del mecanismo:")
    for h in hallazgos:
        print("         " + h)
else:
    bien += 1
    print("  bien   ninguna cuenta de Python en el camino de las respuestas")
sobran = set(LISTA_BLANCA) - blancas_usadas
if sobran:
    mal += 1
    print("  FALLA  la lista blanca tiene entradas que ya no hacen falta (quitarlas): %s" % sorted(sobran))
else:
    bien += 1
    print("  bien   la lista blanca es la justa (%d sitios, todos de texto o de leer archivos)"
          % len(LISTA_BLANCA))
print("TOTAL: %d/%d" % (bien, bien + mal))
sys.exit(1 if mal else 0)
