# -*- coding: utf-8 -*-
"""
Euclides - EL MECANISMO: como calcula el sistema SIN calculadora (decision de Carlos, 4 oct 2026:
"este sistema debe hacerlo mecanicamente hasta nuevo aviso").

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

LO UNICO QUE SABE HACER LA MAQUINA, de verdad, son tres cosas de nino pequeno:
  1. RECITAR: dada una palabra de la lista de contar, decir la SIGUIENTE (o la ANTERIOR).
     La lista es cero, uno, dos ... mil, construida con las reglas de la 6.1 y la 6.7.
  2. LEVANTAR DEDOS: un dedo por cada palabra recitada desde 'uno'.  Hay DIEZ dedos con nombre;
     si se acaban antes de llegar, no caben.
  3. LEER Y ESCRIBIR CIFRAS: el valor de una palabra es su SITIO en la lista (eso es el principio
     cardinal, 2.4) y una cifra escrita se lee simbolo a simbolo (3.1 / 6.3).
Con eso, y SOLO con eso, se construye todo lo demas:
  - sumar con los dedos (7.1): anoto el primero, levanto los dedos del segundo, y por cada dedo
    que bajo digo la palabra SIGUIENTE.  Donde me paro es el total.
  - restar con los dedos (7.4): igual, pero diciendo la ANTERIOR.
  - hacer diez (7.2): cuento cuantos le faltan al primero para 'diez', parto el segundo...
  - las columnas (7.3 / 7.5 / 7.6): cada columna es una cuenta de dedos; "pasa de nueve" es que la
    palabra viene DESPUES de 'nueve' en la lista; lo que se anota es lo que hay que contar desde
    'diez' hasta ahi.
En NINGUN sitio del camino de la respuesta hay un "a + b" de Python.  Python se usa para leer
(el sitio de una palabra) y para las COMPROBACIONES de las pruebas, que son el testigo externo.
"""

import os  # noqa: F401
import sys  # noqa: F401

DEDOS_CON_NOMBRE = ("menique izquierdo", "anular izquierdo", "corazon izquierdo",
                    "indice izquierdo", "pulgar izquierdo", "pulgar derecho", "indice derecho",
                    "corazon derecho", "anular derecho", "menique derecho")


def lista_de_contar(saber):
    """cero, uno, dos ... mil.  Construida una vez (la lista es la de la 6.1/6.7, con el cero de 3.2)."""
    if "_lista_con_cero" not in saber:
        lista = ["cero"] + list(saber["secuencia_de_conteo"]["palabras"])
        saber["_lista_con_cero"] = lista
        saber["_sitio_en_la_lista"] = {w: i for i, w in enumerate(lista)}
    return saber["_lista_con_cero"]


def leer(palabra, saber):
    """El VALOR de una palabra es su SITIO en la lista (principio cardinal).  Solo lectura."""
    lista_de_contar(saber)
    return saber["_sitio_en_la_lista"].get(palabra)


def decir(valor, saber):
    """La palabra que esta en ese sitio de la lista (lo contrario de leer)."""
    lista = lista_de_contar(saber)
    return lista[valor] if valor is not None and 0 <= valor < len(lista) else None


def siguiente(palabra, saber):
    lista = lista_de_contar(saber)
    i = saber["_sitio_en_la_lista"].get(palabra)
    return lista[i + 1] if i is not None and i + 1 < len(lista) else None


def anterior(palabra, saber):
    lista = lista_de_contar(saber)
    i = saber["_sitio_en_la_lista"].get(palabra)
    return lista[i - 1] if i is not None and i > 0 else None


def viene_despues(p, q, saber):
    """p es MAYOR que q: en la lista viene despues (unidad 4.2)."""
    lista_de_contar(saber)
    s = saber["_sitio_en_la_lista"]
    return s[p] > s[q]


def levantar_dedos(palabra, saber):
    """Se recita desde 'uno' hasta 'palabra' levantando un dedo por palabra.
    Devuelve [(dedo, palabra_dicha), ...] o None si se acaban los dedos antes de llegar."""
    if palabra == "cero":
        return []
    levantados = []
    dicha = "uno"
    for dedo in DEDOS_CON_NOMBRE:
        levantados.append((dedo, dicha))
        if dicha == palabra:
            return levantados
        dicha = siguiente(dicha, saber)
        if dicha is None:
            return None
    return None                       # se acabaron los dedos y no se llego


def _contar(desde, cuantos, saber, paso, con_dedos=True):
    """El corazon del mecanismo: desde 'desde', dar 'cuantos' pasos (siguiente o anterior).
    Con dedos: un dedo por paso (maximo diez).  Sin dedos: se lleva la cuenta recitando
    uno, dos, tres... a la vez (como cuando se cuenta con marcas)."""
    if con_dedos:
        dedos = levantar_dedos(cuantos, saber)
        if dedos is None:
            return {"conclusion": "no_caben_en_los_dedos"}
    else:
        dedos = []
        marca = "uno"
        while cuantos != "cero":
            dedos.append(("marca", marca))
            if marca == cuantos:
                break
            marca = siguiente(marca, saber)
            if marca is None:
                return {"conclusion": "no_alcanza"}
    actual = desde
    pasos = []
    for dedo, nombre in dedos:        # se baja un dedo y se dice la palabra de al lado
        nueva = paso(actual, saber)
        if nueva is None:
            return {"conclusion": "no_alcanza" if paso is siguiente else "no_hay_bastantes",
                    "pasos": pasos}
        actual = nueva
        pasos.append({"dedo": dedo, "dedo_numero": nombre, "dice": actual})
    return {"conclusion": "se_puede", "resultado": actual, "pasos": pasos,
            "dedos": [d for d, _ in dedos]}


def contar_adelante(desde, cuantos, saber, con_dedos=True):
    return _contar(desde, cuantos, saber, siguiente, con_dedos)


def contar_atras(desde, cuantos, saber, con_dedos=True):
    return _contar(desde, cuantos, saber, anterior, con_dedos)


def contar_hasta(desde, hasta, saber):
    """Cuantos pasos hay de 'desde' a 'hasta' contando hacia adelante (5.5: el hueco).
    Devuelve la PALABRA de los pasos ('cero' si son iguales), o None si 'hasta' va antes."""
    if desde == hasta:
        return "cero"
    if not viene_despues(hasta, desde, saber):
        return None
    marca = "cero"
    actual = desde
    while actual != hasta:
        actual = siguiente(actual, saber)
        marca = siguiente(marca, saber)
    return marca


def cifras_de(valor):
    """Las cifras de un numero ESCRITO, de derecha a izquierda (unidades primero).
    Es LEER la cifra simbolo a simbolo, no calcular: 247 -> [7, 4, 2]."""
    return [int(c) for c in reversed(str(valor))]


def escribir_cifras(cifras):
    """Lo contrario: las cifras por sitio (unidades primero) se ESCRIBEN una al lado de otra."""
    texto = "".join(str(c) for c in reversed(cifras)).lstrip("0")
    return int(texto) if texto else 0
