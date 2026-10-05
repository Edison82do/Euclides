# -*- coding: utf-8 -*-
"""
Euclides - Nivel 2 - conteo (2.2 a 2.6).

Este archivo es UNA PARTE del motor.  No se importa suelto: lo carga sistema/motor.py,
que junta todas las partes en un solo espacio de nombres (por eso aqui se usan funciones
definidas en otras partes sin importarlas).  Ver sistema/partes/__init__.py.
"""

import os  # noqa: F401
import sys  # noqa: F401

# ------------------------------------------------- orden de la lista (2.2)

def decidir_2_2_recitar(palabra, saber=None):
    """La lista DESDE esa palabra hasta donde el sistema sabe.  Se dice donde acaba."""
    if saber is None:
        saber = cargar_conocimiento()
    palabra = nombre_de_numero(palabra, saber)[0]   # unidad 5.3: cifra o palabra, da igual
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    cuenta = {"secuencia": secuencia}
    r = _aplicar_reglas(saber["reglas_2_2"]["reglas_recitar"], None, None, saber,
                        cuenta=cuenta, palabra=palabra)
    r["palabra"] = palabra
    r["secuencia"] = secuencia
    if r["conclusion"] == "recitado":
        tramo = secuencia[secuencia.index(palabra):]
        r["tramo"] = tramo
        r["llega_al_final"] = tramo[-1] == secuencia[-1]
    return r


def decidir_2_2_revisar(palabras, saber=None):
    """
    Revisar una recitacion hecha por otro: reutiliza TAL CUAL las primitivas de la 2.1
    (hay_palabra_desconocida, no_es_el_principio, es_el_principio).
    """
    if saber is None:
        saber = cargar_conocimiento()
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    cuenta = {"secuencia": secuencia, "palabras": list(palabras)}
    r = _aplicar_reglas(saber["reglas_2_2"]["reglas_revisar_secuencia"], None, None, saber, cuenta=cuenta)
    r["secuencia"] = secuencia
    r["palabras"] = list(palabras)
    r["entidades"] = []
    return r


# ------------------------------------------------- cuantos hay (2.3)

def decidir_2_3_cuantos(escena, saber=None):
    """
    Unidad 2.3: contar la coleccion y decir CUANTOS HAY (la ultima palabra del recuento).
    Reutiliza el emparejamiento de la 2.1 y sus mismas primitivas.
    """
    if saber is None:
        saber = cargar_conocimiento()
    reales = entidades_reales(escena)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    cuenta = {"secuencia": secuencia, "palabras": []}
    r = _aplicar_reglas(saber["reglas_2_3"]["reglas_cuantos"], reales, None, saber, cuenta=cuenta)
    r["secuencia"] = secuencia
    r["entidades"] = reales
    if r["conclusion"] == "cero":
        r["cantidad"] = "cero"
        r["cifra"] = "0"
    elif r["conclusion"] == "hay_cantidad":
        r["emparejamiento"] = [(o["id"], secuencia[i]) for i, o in enumerate(reales)]
        r["cantidad"] = secuencia[len(reales) - 1]
        r["cifra"] = _tabla(saber).get(r["cantidad"])
    return r


# ------------------------------------------------- cardinalidad (2.4)

def decidir_2_4_dame(escena, palabra, saber=None):
    """
    Unidad 2.4, Give-N: de un MONTON que da quien pregunta, coger esa cantidad (word-to-set).
    El sistema no crea objetos: elige de los que le dan.  Y SIEMPRE se verifica contando.

    Unidad 3.4: la cantidad tambien se puede pedir con una CIFRA ('dame: a,b,c / 3').  Es el sexto
    camino del puente (cifra -> cantidad); se traduce la cifra a su palabra y se sigue igual.
    """
    if saber is None:
        saber = cargar_conocimiento()
    reales = entidades_reales(escena)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    tabla = _tabla(saber)
    invertida = {v: k for k, v in tabla.items()}
    entrada_cifra = palabra in invertida and palabra not in secuencia
    if entrada_cifra:
        palabra = invertida[palabra]
    if palabra == "cero":
        # Unidad 3.4: "dame cero objetos" no es coger nada.  Dar es coger, y no se coge el vacio.
        # Es una pregunta sin tarea: el cero es una cantidad, pero no una cantidad QUE SE COGE.
        return {"conclusion": "cero_no_se_coge", "palabra": palabra, "entrada_cifra": entrada_cifra,
                "monton": reales, "secuencia": secuencia, "regla": "dame_cero_no_se_coge",
                "justificacion": "el_cero", "condiciones_probadas": []}
    cuenta = {"secuencia": secuencia}
    r = _aplicar_reglas(saber["reglas_2_4"]["reglas_dame"], reales, None, saber,
                        cuenta=cuenta, palabra=palabra)
    r["palabra"] = palabra
    r["entrada_cifra"] = entrada_cifra
    r["secuencia"] = secuencia
    r["monton"] = reales
    if r["conclusion"] == "cogido":
        n = secuencia.index(palabra) + 1
        r["cogidos"] = [o["id"] for o in reales[:n]]
        r["dejados"] = [o["id"] for o in reales[n:]]
        # verificacion: contar lo cogido y comprobar que sale lo pedido
        r["verificacion"] = secuencia[len(r["cogidos"]) - 1] == palabra
        r["cantidad"] = secuencia[len(r["cogidos"]) - 1]
    return r


def decidir_2_4_tiene(escena, palabra, saber=None):
    """Unidad 2.4: 'este conjunto tiene esa cantidad?'  Cuenta y confirma o rechaza."""
    if saber is None:
        saber = cargar_conocimiento()
    reales = entidades_reales(escena)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    cuenta = {"secuencia": secuencia}
    r = _aplicar_reglas(saber["reglas_2_4"]["reglas_tiene"], reales, None, saber,
                        cuenta=cuenta, palabra=palabra)
    r["palabra"] = palabra
    r["secuencia"] = secuencia
    r["entidades"] = reales
    if r["conclusion"] in ("si", "no"):
        r["cantidad"] = secuencia[len(reales) - 1]
    return r


# ------------------------------------------------- orden y recorrido (2.5)

def decidir_2_5_orden(escena, saber=None):
    """Cuenta la coleccion de dos maneras y comprueba que la cantidad es la misma."""
    if saber is None:
        saber = cargar_conocimiento()
    reales = entidades_reales(escena)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    cuenta = {"secuencia": secuencia}
    r = _aplicar_reglas(saber["reglas_2_5"]["reglas_orden"], reales, None, saber, cuenta=cuenta)
    r["secuencia"] = secuencia
    r["entidades"] = reales
    if r["conclusion"] == "coinciden":
        r["derecho"] = [(o["id"], secuencia[i]) for i, o in enumerate(reales)]
        r["reves"] = [(o["id"], secuencia[i]) for i, o in enumerate(reversed(reales))]
        r["cantidad_derecho"] = secuencia[len(reales) - 1]
        r["cantidad_reves"] = secuencia[len(reales) - 1]
        r["coinciden"] = r["cantidad_derecho"] == r["cantidad_reves"]
    return r


def decidir_2_5_conteo(recorrido, palabras, saber=None):
    """
    Unidad 2.5: juzgar un RECORRIDO de conteo hecho por otro.
    Aqui se ve la diferencia entre las dos clases de reglas:
      - PSEUDOERROR: recorrer los objetos en orden raro -> VALIDO (regla convencional).
      - COMPENSACION: saltarse uno y contar otro dos veces -> INVALIDO (regla logica rota).
    NO se pasa por entidades_reales: si un objeto se repite en el recorrido, eso ES el error.
    """
    if saber is None:
        saber = cargar_conocimiento()
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    cuenta = {"secuencia": secuencia, "palabras": list(palabras)}
    r = _aplicar_reglas(saber["reglas_2_5"]["reglas_conteo"], recorrido, None, saber, cuenta=cuenta)
    r["secuencia"] = secuencia
    r["palabras"] = list(palabras)
    r["recorrido"] = recorrido
    r["entidades"] = recorrido
    if r["conclusion"] == "valido":
        r["emparejamiento"] = [(o["id"], palabras[i]) for i, o in enumerate(recorrido)]
        r["cantidad"] = palabras[len(recorrido) - 1]
    return r


# ------------------------------------------------- abstraccion (2.6)

def decidir_2_6_misma_cantidad(izquierda, derecha, saber=None):
    """
    Unidad 2.6: dos colecciones, ?tienen la misma cantidad?  Aunque sean cosas totalmente distintas.
    La segunda coleccion viaja en cuenta['otra'].
    """
    if saber is None:
        saber = cargar_conocimiento()
    reales1 = entidades_reales(izquierda)
    reales2 = entidades_reales(derecha)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    cuenta = {"secuencia": secuencia, "otra": reales2}
    r = _aplicar_reglas(saber["reglas_2_6"]["reglas_misma_cantidad"], reales1, None, saber,
                        cuenta=cuenta)
    r["secuencia"] = secuencia
    r["izquierda"] = reales1
    r["derecha"] = reales2
    if r["conclusion"] in ("si", "no"):
        r["cantidad_izquierda"] = secuencia[len(reales1) - 1]
        r["cantidad_derecha"] = secuencia[len(reales2) - 1]
    return r
