# -*- coding: utf-8 -*-
"""
LAS MUESTRAS: que numeros recorren las pruebas grandes.

DECISION DE CARLOS (5 oct 2026): NO se prueban todas las combinaciones de numeros.  Con una buena
muestra basta.  (El modo "--hierro", que recorria el rango entero, se quito.)

POR QUE UNA MUESTRA BASTA:
  El mecanismo del sistema (contar, dedos, columnas) hace LO MISMO con 347 que con 348: lo que
  cambia su camino son las FRONTERAS (el cero, el nueve, el diez, pasar de una decena a otra,
  llevarse, cambiar a traves de un cero, el techo).  Asi que la muestra rapida coge TODAS las
  fronteras + todos los numeros pequenos + una muestra fija al azar (siempre la misma, para que
  un fallo se pueda repetir).

UNA PRUEBA = UNA AFIRMACION.  Una prueba con muestra es UNA afirmacion sobre todo el rango
("todas las sumas dan bien"), y cuenta como UNA, diga cuantos casos ha recorrido.  Antes se
contaba cada caso por separado y salian 57.000 "pruebas" que eran, en verdad, unas 1.000.
"""
import os
import random


_FRONTERA_UNIDADES = (0, 1, 2, 5, 8, 9)


def numeros(desde, hasta, extra=()):
    """Los numeros a recorrer entre desde y hasta (incluidos)."""
    s = set(range(desde, min(hasta, 20) + 1))                       # los pequenos, todos
    for n in range(desde, hasta + 1):
        c = str(n)
        if all(int(x) in _FRONTERA_UNIDADES for x in c):             # cifras de frontera
            s.add(n)
        if n % 100 in (0, 1, 99) or n % 10 == 0 and n % 100 in (10, 90):
            s.add(n)
    azar = random.Random(20261005)
    s |= set(azar.sample(range(desde, hasta + 1), min(60, hasta - desde + 1)))
    s |= {x for x in extra if desde <= x <= hasta}
    s |= {desde, hasta}
    return sorted(s)


def parejas(hasta_a, cond, cuantas_al_azar=300, extra=()):
    """Parejas (a, b) con a, b en 0..hasta_a que cumplen cond(a, b).
    Rapido: todas las combinaciones de numeros de FRONTERA (cifras 0, 1 y 9, y del 0 al 12)
    + 'cuantas_al_azar' parejas al azar (siempre las mismas)."""
    base = set(range(0, min(hasta_a, 12) + 1))
    base |= {n for n in range(0, hasta_a + 1) if all(x in "019" for x in str(n))}
    base |= {5, 50, 55, 500, 555} & set(range(0, hasta_a + 1))
    ps = {(a, b) for a in base for b in base if cond(a, b)}
    azar = random.Random(51)
    intentos = 0
    while cuantas_al_azar > 0 and intentos < 100000:
        intentos += 1
        a, b = azar.randint(0, hasta_a), azar.randint(0, hasta_a)
        if cond(a, b) and (a, b) not in ps:
            ps.add((a, b))
            cuantas_al_azar -= 1
    ps |= {p for p in extra if cond(*p)}
    return sorted(ps)


def modo():
    return "muestra: fronteras + azar fijo"


class Agregado:
    """Para las pruebas de hierro escritas con check(nombre, cond) dentro de un bucle: en vez de
    contar cada caso, junta los fallos por AFIRMACION ('B n: decenas') y al final hace UN check por
    afirmacion, diciendo cuantos casos recorrio y cuales fallaron (los tres primeros)."""

    def __init__(self):
        self.claves = {}
        self.casos = 0

    def check(self, nombre, cond, detalle=""):
        import re
        clave = re.sub(r"-?\d+", "n", nombre)
        self.claves.setdefault(clave, [])
        if not cond:
            self.claves[clave].append("%s %s" % (nombre, detalle))

    def volcar(self, check, prefijo):
        for clave, fallos in self.claves.items():
            check("%s %s" % (prefijo, clave), not fallos, "; ".join(fallos[:3]))
