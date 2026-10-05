# -*- coding: utf-8 -*-
"""
Euclides - El motor de decision: aplicar reglas en orden; unidades 0.x, 1.0 y 2.1.

Este archivo es UNA PARTE del motor.  No se importa suelto: lo carga sistema/motor.py,
que junta todas las partes en un solo espacio de nombres (por eso aqui se usan funciones
definidas en otras partes sin importarlas).  Ver sistema/partes/__init__.py.
"""

import os  # noqa: F401
import sys  # noqa: F401

# ---------------------------------------------------------------- decision

def _aplicar_reglas(reglas, escena, criterio, saber, patron=None, cuenta=None, palabra=None):
    traza = []
    for regla in reglas:
        resultados = []
        for cond in regla["condiciones"]:
            valor, _ = evaluar_condicion(cond, escena, criterio, patron, cuenta, palabra)
            resultados.append((cond, valor))
        traza.append({"regla": regla["nombre"], "condiciones": resultados})
        if all(v for _, v in resultados):
            just = saber.get(regla["justificacion"], {})
            return {
                "conclusion": regla["conclusion"],
                "regla": regla["nombre"],
                "justificacion": {
                    "id": regla["justificacion"],
                    "nombre": just.get("nombre", "?"),
                    "categoria": just.get("categoria", "?"),
                },
                "traza": traza,
            }
    raise ValueError("ninguna regla aplicable")


def decidir(escena, saber=None):
    """Unidad 0.1: objeto individual o grupo."""
    if saber is None:
        saber = cargar_conocimiento()
    return _aplicar_reglas(saber["reglas_0_1"]["reglas"], escena, None, saber)


def _pluralidad(escena):
    """Lo que la unidad 0.1 sabe de esta escena: nada, un objeto o varios."""
    if not escena:
        return "nada"
    if len({o["id"] for o in escena}) < 2:
        return "un_objeto"
    return "varios_objetos"


def decidir_0_2_reconocer(escena, saber=None):
    """Unidad 0.2, reconocer: forman grupo? que comparten?"""
    if saber is None:
        saber = cargar_conocimiento()
    reales = entidades_reales(escena)
    r = _aplicar_reglas(saber["reglas_0_2"]["reglas_reconocer"], reales, None, saber)
    r["entidades"] = reales
    r["separadas"] = separadas(escena, reales)
    r["atributos_compartidos"] = atributos_compartidos(reales)
    r["atributos_indeterminados"] = atributos_indeterminados(reales)
    # 0.2 NO oculta lo que 0.1 ya sabe: la respuesta lleva las dos partes.
    r["pluralidad"] = _pluralidad(reales)
    return r


def decidir_0_2_formar(escena, criterio, saber=None):
    """Unidad 0.2, formar: el grupo de los que cumplen el criterio."""
    if saber is None:
        saber = cargar_conocimiento()
    reales = entidades_reales(escena)
    r = _aplicar_reglas(saber["reglas_0_2"]["reglas_formar"], reales, criterio, saber)
    r["entidades"] = reales
    r["separadas"] = separadas(escena, reales)
    r["criterio"] = criterio
    r["miembros"] = miembros(reales, criterio)
    r["pluralidad"] = _pluralidad(reales)
    return r


def decidir_0_3_pertenencia(escena, criterio, saber=None):
    """
    Unidad 0.3, pertenencia: para cada entidad de la escena, decide si pertenece al grupo
    del criterio.  Devuelve una lista de resultados (uno por entidad).
    """
    if saber is None:
        saber = cargar_conocimiento()
    reales = entidades_reales(escena)
    resultados = []
    for o in reales:
        r = _aplicar_reglas(saber["reglas_0_3"]["reglas"], [o], criterio, saber)
        r["objeto"] = o
        r["criterio"] = criterio
        resultados.append(r)
    return resultados


def decidir_1_0_subitizar(texto_patron, saber=None):
    """
    Unidad 1.0, subitizing: reconocer la cantidad de un grupo pequeno DE UN VISTAZO.
    Si la figura no esta en la tabla de patrones, NO se cuenta: se dice no_reconocido.
    """
    if saber is None:
        saber = cargar_conocimiento()
    normalizado = normalizar_patron(texto_patron)
    encontrado = buscar_patron(normalizado, saber)
    paquete = {"texto": normalizado, "declarado": encontrado}
    r = _aplicar_reglas(saber["reglas_1_0"]["reglas"], [], None, saber, patron=paquete)
    r["patron"] = normalizado
    r["etiqueta"] = encontrado["etiqueta"] if encontrado else None
    r["nombre_patron"] = encontrado["nombre"] if encontrado else None
    return r


def decidir_2_1_contar(escena, saber=None):
    """
    Unidad 2.1, trabajo A: emparejar una palabra con cada objeto, en orden.
    OJO: primero se resuelven las ENTIDADES reales (unidad 0.1): repetir el mismo nombre no
    crea dos objetos, asi que tampoco da dos palabras.
    Si hay mas objetos que palabras conoce el sistema, NO se inventa las que faltan.
    """
    if saber is None:
        saber = cargar_conocimiento()
    reales = entidades_reales(escena)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    cuenta = {"secuencia": secuencia, "palabras": []}
    r = _aplicar_reglas(saber["reglas_2_1"]["reglas_contar"], reales, None, saber, cuenta=cuenta)
    r["secuencia"] = secuencia
    r["entidades"] = reales
    if r["conclusion"] == "emparejado":
        r["emparejamiento"] = [(o["id"], secuencia[i]) for i, o in enumerate(reales)]
    return r


def decidir_2_1_revisar(escena, palabras, saber=None):
    """
    Unidad 2.1, trabajo B: revisar una cuenta hecha por otro y decir que error tiene, si lo tiene.
    """
    if saber is None:
        saber = cargar_conocimiento()
    reales = entidades_reales(escena)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    cuenta = {"secuencia": secuencia, "palabras": list(palabras)}
    r = _aplicar_reglas(saber["reglas_2_1"]["reglas_revisar"], reales, None, saber, cuenta=cuenta)
    r["secuencia"] = secuencia
    r["palabras"] = list(palabras)
    r["entidades"] = reales
    return r
