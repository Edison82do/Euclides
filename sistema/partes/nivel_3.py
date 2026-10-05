# -*- coding: utf-8 -*-
"""
Euclides - Nivel 3 - numeros (3.1 a 3.4).

Este archivo es UNA PARTE del motor.  No se importa suelto: lo carga sistema/motor.py,
que junta todas las partes en un solo espacio de nombres (por eso aqui se usan funciones
definidas en otras partes sin importarlas).  Ver sistema/partes/__init__.py.
"""

import os  # noqa: F401
import sys  # noqa: F401

# ------------------------------------------------- simbolos (3.1)

def _resultado_de_la_6_3(conclusion, regla, saber, **campos):
    """
    Resultado con la traza puesta a mano, para las lecturas de DOS cifras de la unidad 6.3.
    El resto de las ordenes pasan por _aplicar_reglas; estas dos (cifra y palabra de dos digitos)
    son un atajo y tienen que dejar la traza igual de clara (regla 13: toda respuesta se rastrea
    a una regla escrita y a un dato escrito).
    """
    j = saber.get("la_tabla_de_cien") or {}
    d = {
        "conclusion": conclusion,
        "regla": regla,
        "justificacion": {
            "id": "la_tabla_de_cien",
            "nombre": j.get("nombre", "la tabla de 100"),
            "categoria": j.get("categoria", "FIJADO"),
        },
        "traza": [{"regla": regla,
                   "condiciones": [("el numero tiene DOS cifras (unidad 6.3)", True)]}],
    }
    # UNIDAD 6.7: con TRES cifras la traza lo dice (antes decia "DOS cifras" tambien para 247).
    if "tres_cifras" in regla:
        c = saber.get("la_centena") or {}
        d["justificacion"] = {"id": "la_centena", "nombre": c.get("nombre", "la centena"),
                              "categoria": c.get("categoria", "FIJADO")}
        d["traza"] = [{"regla": regla,
                       "condiciones": [("el numero tiene TRES cifras o mas (unidad 6.7)", True)]}]
    d.update(campos)
    return d


def decidir_3_1_cifra(palabra, saber=None):
    """De la PALABRA a la CIFRA.  'tres' -> 3

    UNIDAD 6.3: ahora tambien vale una palabra de DOS cifras.  'cuarenta y siete' -> '47'.
    (Antes de la 6.3 esto decia palabra_desconocida, porque la tabla es de un digito.)"""
    if saber is None:
        saber = cargar_conocimiento()
    tabla = _tabla(saber)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    v = _valor_de_numero(palabra, saber)
    if v is not None and v > 9:
        # Es la palabra de un numero de dos cifras: el sistema YA sabe leerla (6.3).
        return _resultado_de_la_6_3("cifra", "cifra_de_dos_digitos (6.3)", saber,
                                    cifra=str(v), palabra=palabra, valor=v,
                                    secuencia=secuencia, tabla=tabla)
    cuenta = {"secuencia": secuencia, "simbolos": tabla}
    r = _aplicar_reglas(saber["reglas_3_1"]["reglas_cifra"], None, None, saber,
                        cuenta=cuenta, palabra=palabra)
    r["palabra"] = palabra
    r["secuencia"] = secuencia
    r["tabla"] = tabla
    if r["conclusion"] == "cifra":
        r["cifra"] = tabla[palabra]
    return r


def decidir_3_1_palabra(cifra, saber=None):
    """De la CIFRA a la PALABRA.  3 -> 'tres'

    UNIDAD 6.3: ahora tambien vale una cifra de DOS digitos.  '47' -> 'cuarenta y siete'."""
    if saber is None:
        saber = cargar_conocimiento()
    tabla = _tabla(saber)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    n = _cifra_a_numero(cifra, saber)
    if n is not None and n > 9:
        # Cifra de DOS O TRES digitos: el nombre se CONSTRUYE con la regla (6.1 y 6.7).
        nombre = construir_nombre_hasta_mil(n, saber)
        if nombre:
            regla_ = ("palabra_de_tres_cifras (6.7)" if n > 99 else "palabra_de_dos_digitos (6.3)")
            return _resultado_de_la_6_3("palabra", regla_, saber,
                                        palabra=nombre, cifra_dada=cifra, valor=n,
                                        secuencia=secuencia, tabla=tabla)
    cuenta = {"secuencia": secuencia, "simbolos": tabla}
    r = _aplicar_reglas(saber["reglas_3_1"]["reglas_palabra"], None, None, saber,
                        cuenta=cuenta, palabra=cifra)
    r["cifra_dada"] = cifra
    r["secuencia"] = secuencia
    r["tabla"] = tabla
    if r["conclusion"] == "palabra":
        r["palabra"] = {v: k for k, v in tabla.items()}[cifra]
    return r


def decidir_3_1_cifra_de(escena, saber=None):
    """De la CANTIDAD a la CIFRA: cuenta la coleccion y da su cifra."""
    if saber is None:
        saber = cargar_conocimiento()
    reales = entidades_reales(escena)
    tabla = _tabla(saber)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    cuenta = {"secuencia": secuencia, "simbolos": tabla}
    r = _aplicar_reglas(saber["reglas_3_1"]["reglas_cifra_de"], reales, None, saber, cuenta=cuenta)
    r["secuencia"] = secuencia
    r["tabla"] = tabla
    r["entidades"] = reales
    if r["conclusion"] == "cifra":
        r["cantidad"] = _palabra_de_la_cantidad(reales, cuenta)
        # Unidad 6.3: si la cantidad pasa de nueve, su cifra tiene DOS digitos y se escribe igual.
        r["cifra"] = tabla.get(r["cantidad"])
        if r["cifra"] is None and r["cantidad"] in secuencia:
            r["cifra"] = str(secuencia.index(r["cantidad"]) + 1)
    return r


# ------------------------------------------------- secuencia de numeros (3.3)

def decidir_3_3_siguiente(palabra, saber=None):
    """Que NUMERO va despues.  Aqui SI esta el cero (a diferencia de la lista de contar)."""
    if saber is None:
        saber = cargar_conocimiento()
    palabra = nombre_de_numero(palabra, saber)[0]   # unidad 5.3: cifra o palabra, da igual
    numeros = list(saber["secuencia_de_numeros"]["numeros"])
    cuenta = {"secuencia": saber["secuencia_de_conteo"]["palabras"], "numeros": numeros}
    r = _aplicar_reglas(saber["reglas_3_3"]["reglas_siguiente_numero"], None, None, saber,
                        cuenta=cuenta, palabra=palabra)
    r["palabra"] = palabra
    r["numeros"] = numeros
    if r["conclusion"] == "hay_siguiente":
        r["siguiente"] = numeros[numeros.index(palabra) + 1]
    return r


def decidir_3_3_anterior(palabra, saber=None):
    """Que NUMERO va antes.  El cero es el primero de la secuencia de numeros (no de la de contar)."""
    if saber is None:
        saber = cargar_conocimiento()
    palabra = nombre_de_numero(palabra, saber)[0]
    numeros = list(saber["secuencia_de_numeros"]["numeros"])
    cuenta = {"secuencia": saber["secuencia_de_conteo"]["palabras"], "numeros": numeros}
    r = _aplicar_reglas(saber["reglas_3_3"]["reglas_anterior_numero"], None, None, saber,
                        cuenta=cuenta, palabra=palabra)
    r["palabra"] = palabra
    r["numeros"] = numeros
    if r["conclusion"] == "hay_anterior":
        r["anterior"] = numeros[numeros.index(palabra) - 1]
    return r


def decidir_3_3_dos_listas(saber=None):
    """Las dos listas, y en que se diferencian.  Sin reglas: es un dato."""
    if saber is None:
        saber = cargar_conocimiento()
    return {"conteo": list(saber["secuencia_de_conteo"]["palabras"]),
            "numeros": list(saber["secuencia_de_numeros"]["numeros"])}


def decidir_3_4_puente(escena, saber=None):
    """Unidad 3.4: la misma coleccion de las tres maneras (cantidad, palabra, cifra), por conteo."""
    if saber is None:
        saber = cargar_conocimiento()
    reales = entidades_reales(escena)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    cuenta = {"secuencia": secuencia}
    r = _aplicar_reglas(saber["reglas_3_4"]["reglas_puente"], reales, None, saber, cuenta=cuenta)
    r["secuencia"] = secuencia
    r["entidades"] = reales
    if r["conclusion"] == "puente":
        r["cantidad"] = secuencia[len(reales) - 1]
        tabla = _tabla(saber)
        if r["cantidad"] in tabla:
            r["cifra"] = tabla[r["cantidad"]]
        else:
            # Unidad 3.4: se puede CONTAR hasta diez, pero la CIFRA solo llega a nueve.
            # El diez son dos simbolos, y eso es el Sistema Decimal (unidad siguiente).
            # El puente da las dos representaciones que tiene y DICE que la tercera no la tiene.
            r["conclusion"] = "puente_sin_cifra"
    return r


def decidir_4_1_comparar(escena_a, escena_b, saber=None):
    """
    Unidad 4.1: comparar DOS COLECCIONES.  Se dice con palabras: mas, menos, tantos_como.

    El sistema decide EMPAREJANDO (uno a uno, sin contar) y luego VERIFICA CONTANDO.  Los dos
    caminos tienen que decir lo mismo; si no, el sistema lo diria en vez de elegir uno.
    """
    if saber is None:
        saber = cargar_conocimiento()
    a = entidades_reales(escena_a)
    b = entidades_reales(escena_b)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    cuenta = {"secuencia": secuencia, "otra": b}
    r = _aplicar_reglas(saber["reglas_4_1"]["reglas_comparar"], a, None, saber, cuenta=cuenta)
    r["primera"] = a
    r["segunda"] = b
    r["secuencia"] = secuencia
    # EL EMPAREJAMIENTO: un objeto con un objeto (esto no necesita contar)
    n = min(len(a), len(b))
    r["emparejadas"] = [(a[i]["id"], b[i]["id"]) for i in range(n)]
    r["sobra_primera"] = [o["id"] for o in a[n:]]
    r["sobra_segunda"] = [o["id"] for o in b[n:]]
    # LA VERIFICACION: contar las dos y comparar (unidad 2.3)
    if r["conclusion"] in ("mas", "menos", "tantos_como"):
        r["cantidad_primera"] = secuencia[len(a) - 1] if a else "cero"
        r["cantidad_segunda"] = secuencia[len(b) - 1] if b else "cero"
        r["por_conteo"] = ("mas" if len(a) > len(b)
                           else "menos" if len(a) < len(b) else "tantos_como")
        r["verificacion"] = (r["por_conteo"] == r["conclusion"])
    return r
