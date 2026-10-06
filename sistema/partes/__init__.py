# -*- coding: utf-8 -*-
"""
LAS PARTES DEL MOTOR DE EUCLIDES  (partido el 5 de octubre de 2026)

Hasta la unidad 7.5 el motor era UN solo archivo (sistema/motor.py, ~5.400 lineas).  Se partio
por NIVELES para que cada unidad nueva se escriba en su sitio y se pueda leer sin perderse.

    nucleo.py       lectura de los .kn, escenas, atributos            (0.1, 0.2)
    primitivas.py   las condiciones de las reglas + la tabla PRIMITIVAS
    mecanismo.py    COMO CALCULA SIN CALCULADORA: recitar, levantar dedos, leer cifras
    decision.py     aplicar las reglas en orden; unidades 0.x, 1.0, 2.1
    nivel_2.py      conteo                                            (2.2 - 2.6)
    nivel_3.py      numeros                                           (3.1 - 3.4)
    nivel_4.py      relaciones                                        (4.1, 4.2)
    nivel_5.py      operaciones                                       (5.1 - 5.5)
    nivel_6.py      valor posicional                                  (6.1 - 6.7)
    nivel_7.py      metodos de calculo                                (7.1 - 7.6)
    explicacion.py  los explicadores (lo que se le ensena a quien pregunta)
    piezas.py       el MOTOR DE PIEZAS: carga conocimiento/piezas/, prueba, descarta, aplica
    memoria.py      la MEMORIA de hechos, GANADA: aprender, recordar, olvidar (paso 3)
    resolver.py     el RESOLVEDOR: leer, montar la situacion, pedir pasos a las piezas (R.1)

COMO FUNCIONA (y por que asi):
  Las funciones de una parte llaman a funciones de otras (la 5.3 usa las columnas de la 7.3, la
  7.5 usa la resta de la 5.4...).  Con imports normales eso son importaciones circulares.  Asi
  que juntar() carga TODAS las partes y despues les da a todas EL MISMO espacio de nombres: el
  comportamiento es EXACTAMENTE el de antes (un solo archivo), pero el codigo vive en piezas.

REGLA: un nombre se define en UNA sola parte.  juntar() lo comprueba y se niega a arrancar si
dos partes definen lo mismo (serian dos verdades: la que gane dependeria del orden de carga).
"""

import importlib

ORDEN = ["nucleo", "primitivas", "mecanismo", "decision", "nivel_2", "nivel_3", "nivel_4", "nivel_5",
         "nivel_6", "nivel_7", "explicacion", "piezas", "memoria", "igualdad", "ecuaciones", "saltos", "filas", "multiplicar", "dividir", "resolver", "resolver_r2"]

_IGNORAR = {"os", "sys", "__builtins__", "__cached__", "__doc__", "__file__", "__loader__",
            "__name__", "__package__", "__spec__"}


def juntar():
    """Carga las partes y las une en un solo espacio de nombres.  Devuelve ese espacio."""
    modulos = []
    for nombre in ORDEN:
        try:
            modulos.append(importlib.import_module(__name__ + "." + nombre))
        except ModuleNotFoundError as e:
            if e.name == __name__ + "." + nombre:
                continue          # una parte que todavia no existe
            raise
    espacio = {}
    donde = {}
    for m in modulos:
        for k, v in vars(m).items():
            if k in _IGNORAR:
                continue
            if k in espacio and espacio[k] is not v:
                raise ImportError("'%s' esta definido en DOS partes (%s y %s): dos verdades"
                                  % (k, donde[k], m.__name__))
            espacio[k] = v
            donde[k] = m.__name__
    for m in modulos:
        vars(m).update(espacio)
    espacio["_DONDE_ESTA"] = donde
    return espacio
