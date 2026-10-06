# -*- coding: utf-8 -*-
"""
Euclides - Los explicadores: lo que se le ensena a quien pregunta.

Este archivo es UNA PARTE del motor.  No se importa suelto: lo carga sistema/motor.py,
que junta todas las partes en un solo espacio de nombres (por eso aqui se usan funciones
definidas en otras partes sin importarlas).  Ver sistema/partes/__init__.py.
"""

import os  # noqa: F401
import re  # noqa: F401
import sys  # noqa: F401

# ---------------------------------------------------------------- explicacion

def _cabecera(escena):
    lineas = []
    for o in escena:
        if o["atributos"]:
            attrs = ", ".join("%s=%s" % (k, v) for k, v in o["atributos"].items())
            lineas.append("    %s  [%s]" % (o["id"], attrs))
        else:
            lineas.append("    %s" % o["id"])
    return lineas or ["    (vacia)"]


def _cabecera_emparejamiento(pares):
    """'objeto -> palabra' alineado, con ancho segun el nombre mas largo."""
    if not pares:
        return ["    (nada)"]
    ancho = max(max(len(o) for o, _ in pares), 10)
    return ["    %-*s -> %s" % (ancho, o, p) for o, p in pares]


def _traza_texto(r):
    lineas = ["  reglas probadas, en orden:"]
    for paso in r["traza"]:
        detalle = ", ".join("%s -> %s" % (c, "cierto" if v else "falso") for c, v in paso["condiciones"])
        lineas.append("    - %s : %s" % (paso["regla"], detalle))
    return lineas


def _pie(lineas, r, etiqueta="RESULTADO"):
    lineas.append("%s: %s" % (etiqueta, r["conclusion"]))
    lineas.append("  lo decide la regla '%s'" % r["regla"])
    j = r["justificacion"]
    lineas.append("  respaldado por el conocimiento '%s' (%s) [%s]" % (j["id"], j["nombre"], j["categoria"]))
    return lineas


_PLURALIDAD_TEXTO = {
    "nada": "no hay ninguna entidad",
    "un_objeto": "es UN OBJETO",
    "varios_objetos": "son VARIOS OBJETOS",
}


def explicar(escena, saber=None):
    """Explicacion de la unidad 0.1."""
    if saber is None:
        saber = cargar_conocimiento()
    ids = [o["id"] for o in escena]
    distintas = sorted({o["id"] for o in escena})
    lineas = ["PREGUNTA (0.1): hay UN OBJETO o VARIOS OBJETOS?"]
    lineas.append("ESCENA: %s" % (", ".join(ids) if ids else "(vacia)"))
    lineas.append("  identificadores distintos: %s" % (", ".join(distintas) if distintas else "ninguno"))
    try:
        r = decidir(escena, saber)
    except ValueError as e:
        lineas.append("RESULTADO: no_decidible  (%s)" % e)
        lineas.append("  el sistema no inventa: sin regla aplicable, no responde.")
        return "\n".join(lineas)
    lineas.extend(_traza_texto(r))
    return "\n".join(_pie(lineas, r))


def _nota_entidades(escena, r):
    """
    Avisa de lo que ha pasado con las menciones repetidas del mismo nombre:
      - se han UNIDO (misma cosa, los datos se suman), o
      - se han SEPARADO (un atributo con dos valores distintos PRUEBA que son objetos distintos).
    """
    lineas = []
    entidades = r["entidades"]
    sep = r.get("separadas") or []
    if sep:
        lineas.append("  AVISO: un mismo nombre con datos que NO pueden ser la misma cosa:")
        for o in escena:
            if o["id"] in sep:
                attrs = ", ".join("%s=%s" % (k, v) for k, v in o["atributos"].items()) or "sin atributos"
                lineas.append("    %s  [%s]" % (o["id"], attrs))
        lineas.append("  -> eso PRUEBA que son objetos DISTINTOS. Quedan asi: %s"
                      % ", ".join(e["id"] for e in entidades if e["base"] in sep))
        return lineas
    if len(entidades) < len(escena):
        lineas.append("  (las menciones del mismo objeto se unen: es la misma cosa, y sus datos se suman)")
        lineas.append("  ENTIDADES:")
        lineas.extend(_cabecera(entidades))
    return lineas


def explicar_0_2_reconocer(escena, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (0.2): forman GRUPO estos objetos?"]
    lineas.append("ESCENA:")
    lineas.extend(_cabecera(escena))
    try:
        r = decidir_0_2_reconocer(escena, saber)
    except ValueError as e:
        lineas.append("NO SE PUEDE DECIDIR: %s" % e)
        return "\n".join(lineas)

    reales = r["entidades"]
    lineas.extend(_nota_entidades(escena, r))

    # Primero lo que ya sabe la unidad 0.1, y luego lo que decide la 0.2.
    lineas.append("PLURALIDAD (0.1): %s" % _PLURALIDAD_TEXTO[r["pluralidad"]])
    lineas.extend(_traza_texto(r))
    if r["atributos_indeterminados"] and r["conclusion"] == "no_decidible":
        lineas.append("  atributos que NO se saben: %s" % ", ".join(r["atributos_indeterminados"]))
    if r["conclusion"] == "grupo_atributo":
        lineas.append("  atributos que comparten TODOS: %s" % ", ".join(r["atributos_compartidos"]))
    return "\n".join(_pie(lineas, r, etiqueta="ATRIBUTOS (0.2)"))


def explicar_0_2_formar(escena, criterio, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    crit = "%s=%s" % (criterio["atributo"], criterio["valor"])
    lineas = ["PREGUNTA (0.2): dame el GRUPO de %s" % crit]
    lineas.append("ESCENA:")
    lineas.extend(_cabecera(escena))
    try:
        r = decidir_0_2_formar(escena, criterio, saber)
    except ValueError as e:
        lineas.append("NO SE PUEDE DECIDIR: %s" % e)
        return "\n".join(lineas)

    reales = r["entidades"]
    lineas.extend(_nota_entidades(escena, r))

    lineas.append("PLURALIDAD (0.1): %s" % _PLURALIDAD_TEXTO[r["pluralidad"]])
    lineas.extend(_traza_texto(r))
    if r["conclusion"] == "grupo_formado":
        lineas.append("  miembros del grupo: %s" % ", ".join(r["miembros"]))
    return "\n".join(_pie(lineas, r, etiqueta="ATRIBUTOS (0.2)"))


def explicar_0_3_pertenencia(escena, criterio, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    crit = "%s=%s" % (criterio["atributo"], criterio["valor"])
    lineas = ["PREGUNTA (0.3): quien PERTENECE al grupo de %s ?" % crit]
    lineas.append("OBJETOS:")
    lineas.extend(_cabecera(escena))
    if not escena:
        lineas.append("RESULTADO: no hay ningun objeto del que preguntar.")
        return "\n".join(lineas)

    resultados = decidir_0_3_pertenencia(escena, criterio, saber)
    for r in resultados:
        o = r["objeto"]
        aviso = ""
        if r["conclusion"] == "no_decidible" and criterio["atributo"] not in o["atributos"]:
            aviso = "  (no se sabe su %s)" % criterio["atributo"]
        lineas.append("  %-10s -> %s%s" % (o["id"], r["conclusion"].upper(), aviso))

    if len(resultados) == 1:
        r = resultados[0]
        lineas.append("")
        lineas.extend(_traza_texto(r))
        return "\n".join(_pie(lineas, r, etiqueta="RESULTADO"))

    lineas.append("")
    lineas.append("  (recordatorio: no_pertenece y no_decidible NO son lo mismo)")
    return "\n".join(lineas)


def _dibujo_patron(normalizado):
    return ["    " + " ".join(fila) for fila in normalizado.split("/")]


def explicar_1_0_subitizar(texto_patron, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (1.0): cuantos elementos hay aqui?  (de un vistazo, SIN contar)"]
    try:
        r = decidir_1_0_subitizar(texto_patron, saber)
    except ValueError as e:
        return "NO ENTIENDO ESTO: %s" % e

    lineas.append("FIGURA:")
    lineas.extend(_dibujo_patron(r["patron"]))
    lineas.extend(_traza_texto(r))
    if r["conclusion"] == "reconocido":
        lineas.append("  es el patron '%s'  ->  %s" % (r["nombre_patron"], r["etiqueta"].upper()))
        lineas.append("")
        lineas.append("  CAMINO: DE UN VISTAZO (el corto).  NO he contado: he reconocido el dibujo.")
        cifra = _tabla(saber).get(r["etiqueta"])
        if cifra:
            lineas.extend(_puente("(las del dibujo)", r["etiqueta"], cifra))
            lineas.append("")
            lineas.append("RESULTADO: %s" % r["etiqueta"].upper())
            lineas.append("  su CIFRA es: %s   (unidad 3.4: el camino corto tambien llega a la cifra)"
                          % cifra)
            return "\n".join(lineas)
        return "\n".join(_pie(lineas, r, etiqueta="RESULTADO"))
    lineas.append("RESULTADO: no_reconocido")
    lineas.append("  No lo reconozco de un vistazo, y NO lo cuento: contar es la unidad 2.3.")
    lineas.append("  El camino corto solo llega hasta donde llega el ojo (grupos pequenos y con una")
    lineas.append("  disposicion reconocible).  Para todo lo demas, el camino largo: CONTAR.")
    lineas.append("  El sistema no adivina: si no lo reconoce, lo dice.")
    return "\n".join(lineas)


def explicar_3_4_puente(escena, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (3.4): dime esta coleccion de las TRES maneras"]
    r = decidir_3_4_puente(escena, saber)
    lineas.append("COLECCION:")
    lineas.extend(_cabecera(r["entidades"]))
    if r["conclusion"] == "puente":
        n = len(r["entidades"])
        lineas.append("")
        lineas.append("  CAMINO: CONTAR (el largo).  Una palabra por objeto, en orden:")
        for i, o in enumerate(r["entidades"]):
            lineas.append("    %-10s -> %s" % (o["id"], r["secuencia"][i]))
        lineas.append("")
        lineas.extend(_puente("*" * n, r["cantidad"], r["cifra"]))
        lineas.append("")
        lineas.append("RESULTADO: %s" % r["cifra"])
        lineas.append("  la cantidad es '%s' y su cifra es '%s'; son lo mismo dicho de dos maneras."
                      % (r["cantidad"], r["cifra"]))
        lineas.append("  (El conteo es lo que une las tres: por eso se ensena el recuento.)")
        lineas.append("  lo decide la regla '%s'" % r["regla"])
        lineas.append("  respaldado por el conocimiento 'puente' [FIJADO]")
        return "\n".join(lineas)
    if r["conclusion"] == "puente_sin_cifra":
        n = len(r["entidades"])
        lineas.append("")
        lineas.append("  CAMINO: CONTAR (el largo).  Una palabra por objeto, en orden:")
        for i, o in enumerate(r["entidades"]):
            lineas.append("    %-10s -> %s" % (o["id"], r["secuencia"][i]))
        lineas.append("")
        lineas.append("  PUENTE (las representaciones que SI tengo):")
        lineas.append("    cantidad:  %s" % ("*" * n))
        lineas.append("    palabra:   %s" % r["cantidad"])
        lineas.append("    cifra:     (no la tengo)")
        lineas.append("")
        lineas.append("RESULTADO: %s" % r["cantidad"])
        lineas.append("  La CANTIDAD es '%s' y su PALABRA es '%s', pero su CIFRA no la tengo:"
                      % (r["cantidad"], r["cantidad"]))
        lineas.append("  el diez son DOS simbolos (1 y 0), y eso es el Sistema Decimal.")
        lineas.append("  Doy las dos representaciones que tengo en vez de inventarme la tercera.")
        return "\n".join(lineas)
    if r["conclusion"] == "vacia":
        lineas.extend(_puente("(nada)", "cero", "0"))
        lineas.append("")
        lineas.append("RESULTADO: 0")
        lineas.append("  La coleccion esta vacia: cantidad cero, palabra 'cero', cifra 0.")
        return "\n".join(lineas)
    lineas.append("RESULTADO: no_alcanza")
    lineas.append("  Esta coleccion tiene mas objetos de los que se contar (mi lista llega a diez).")
    lineas.append("  Lo digo en vez de inventarme el numero.")
    return "\n".join(lineas)


def explicar_3_4_caminos(saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (3.4): que caminos hay entre cantidad, palabra y cifra?", ""]
    lineas.append("  LAS TRES REPRESENTACIONES de lo mismo:")
    lineas.append("    cantidad:  * * *        (los objetos)")
    lineas.append("    palabra:   tres         (como se dice al contar)")
    lineas.append("    cifra:     3            (como se escribe)")
    lineas.append("")
    lineas.append("  Y LOS SEIS CAMINOS (tres pares, cada uno en los dos sentidos):")
    for linea in [
        "    1. cantidad -> palabra    cuantos: a,b,c                 -> tres",
        "    2. palabra  -> cantidad   dame: a,b,c,d / tres          -> coge tres",
        "    3. cantidad -> cifra      cifra_de: a,b,c               -> 3",
        "    4. cifra    -> cantidad   dame: a,b,c,d / 3             -> coge tres",
        "    5. palabra  -> cifra      cifra: tres                   -> 3",
        "    6. cifra    -> palabra    palabra: 3                    -> tres",
    ]:
        lineas.append(linea)
    lineas.append("")
    lineas.append("RESULTADO: los_seis_caminos")
    lineas.append("  EL ORDEN EN QUE SE APRENDEN no es invento nuestro (Benoit, Lehalle & Jouen 2013):")
    lineas.append("  primero palabra<->conjunto, despues cifra<->conjunto, y POR ULTIMO palabra<->cifra.")
    lineas.append("  El camino 4 (cifra->cantidad) es el que faltaba, y se aprende en esta unidad.")
    lineas.append("  respaldado por el conocimiento 'puente' [FIJADO]")
    return "\n".join(lineas)


def explicar_2_1_contar(escena, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (2.1): empareja UNA palabra con CADA objeto, en orden"]
    r = decidir_2_1_contar(escena, saber)
    lineas.append("COLECCION:")
    lineas.extend(_cabecera(r["entidades"]))
    if not escena:
        lineas.append("RESULTADO: no_decidible  (no hay nada que contar)")
        return "\n".join(lineas)

    if len(r["entidades"]) < len(escena):
        lineas.append("  (los nombres repetidos son el MISMO objeto: no dan dos palabras)")
    lineas.extend(_traza_texto(r))
    if r["conclusion"] == "emparejado":
        lineas.append("  EMPAREJAMIENTO (una palabra por objeto, ninguna repetida):")
        lineas.extend(_cabecera_emparejamiento(r["emparejamiento"]))
        return "\n".join(_pie(lineas, r, etiqueta="RESULTADO"))
    if r["conclusion"] == "no_alcanza_la_secuencia":
        lineas.append("RESULTADO: no_alcanza_la_secuencia")
        lineas.append("  Hay mas objetos que palabras conozco, y NO me invento las que faltan.")
        lineas.append("  (Aprender mas palabras de la secuencia es la unidad 2.2.)")
        return "\n".join(lineas)
    return "\n".join(_pie(lineas, r, etiqueta="RESULTADO"))


def explicar_2_1_revisar(escena, palabras, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (2.1): esta bien hecha esta cuenta?  (y si no, que error tiene)"]
    r = decidir_2_1_revisar(escena, palabras, saber)
    lineas.append("COLECCION:")
    lineas.extend(_cabecera(r["entidades"]))
    lineas.append("CUENTA PROPUESTA: %s" % (", ".join(palabras) if palabras else "(ninguna palabra)"))
    lineas.extend(_traza_texto(r))
    detalle = _detalle_error(escena, r)
    if detalle:
        lineas.append(detalle)
    return "\n".join(_pie(lineas, r, etiqueta="RESULTADO"))


def explicar_2_2_recitar(palabra, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (2.2): recita la lista desde '%s' hasta donde sepas" % palabra]
    r = decidir_2_2_recitar(palabra, saber)
    lineas.extend(_traza_texto(r))
    if r["conclusion"] == "recitado":
        lineas.append("RECITADO: %s" % ", ".join(r["tramo"]))
        if r["llega_al_final"]:
            lineas.append("  Llego hasta el final de lo que se: no hay mas palabras despues de '%s'."
                          % r["secuencia"][-1])
        return "\n".join(_pie(lineas, r, etiqueta="RESULTADO"))
    lineas.append("RESULTADO: palabra_desconocida")
    if palabra == "cero":
        lineas.append("  'cero' SI esta en la secuencia de NUMEROS (y es el primero), pero RECITAR es")
        lineas.append("  la lista de CONTAR, que empieza en 'uno': no se cuenta desde cero.")
    else:
        lineas.append("  '%s' no esta en mi lista, y no me la invento." % palabra)
    return "\n".join(lineas)


def explicar_2_2_revisar(palabras, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (2.2): esta bien dicha esta recitacion?"]
    r = decidir_2_2_revisar(palabras, saber)
    lineas.append("RECITACION PROPUESTA: %s" % (", ".join(palabras) if palabras else "(nada)"))
    lineas.extend(_traza_texto(r))
    detalle = _detalle_error(None, r)
    if detalle:
        lineas.append(detalle)
    return "\n".join(_pie(lineas, r, etiqueta="RESULTADO"))


def explicar_2_3_cuantos(escena, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (2.3): cuenta estos objetos y dime CUANTOS HAY"]
    r = decidir_2_3_cuantos(escena, saber)
    lineas.append("COLECCION:")
    lineas.extend(_cabecera(r["entidades"]))
    if not escena:
        lineas.append("  (la coleccion esta VACIA: no hay ningun objeto)")
        lineas.append("")
        lineas.append("RESULTADO: cero")
        lineas.append("  la cantidad de un conjunto vacio es CERO, y su cifra es 0.")
        lineas.append("  (OJO: esto NO es 'no se sabe'. Es una cantidad: ninguno.)")
        return "\n".join(lineas)

    if len(r["entidades"]) < len(escena):
        lineas.append("  (los nombres repetidos son el MISMO objeto: no se cuentan dos veces)")
    lineas.extend(_traza_texto(r))
    if r["conclusion"] == "hay_cantidad":
        lineas.append("  RECUENTO (una palabra por objeto, en orden):")
        lineas.extend(_cabecera_emparejamiento(r["emparejamiento"]))
        lineas.append("")
        lineas.append("  la ULTIMA palabra del recuento es: %s" % r["cantidad"])
        lineas.append("  (OJO: esto es la REGLA DE LA ULTIMA PALABRA, no el principio de"
                      " cardinalidad; ese es la unidad 2.4.)")
        lineas.append("")
        lineas.append("RESULTADO: %s" % r["cantidad"])
        lineas.append("  respaldado por el conocimiento 'cuantos_hay' [FIJADO]")
        return "\n".join(lineas)
    if r["conclusion"] == "no_alcanza_la_secuencia":
        lineas.append("RESULTADO: no_alcanza_la_secuencia")
        lineas.append("  Hay mas objetos que palabras conozco: NO me invento la cantidad.")
        return "\n".join(lineas)
    return "\n".join(_pie(lineas, r, etiqueta="RESULTADO"))


def explicar_2_4_dame(escena, palabra, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (2.4): de este monton, dame esta cantidad  (Give-N: de la palabra al conjunto)"]
    r = decidir_2_4_dame(escena, palabra, saber)
    lineas.append("MONTON (lo que me dan, no me lo invento):")
    lineas.extend(_cabecera(r["monton"]))
    if r["entrada_cifra"]:
        lineas.append("CANTIDAD QUE ME PIDEN: %s   (me lo pides con una CIFRA; su palabra es '%s')"
                      % (palabra, r["palabra"]))
        lineas.append("  camino 4 del puente (cifra -> cantidad), unidad 3.4")
    else:
        lineas.append("CANTIDAD QUE ME PIDEN: %s" % palabra)
    if r["conclusion"] == "cero_no_se_coge":
        lineas.append("RESULTADO: cero_no_se_coge")
        lineas.append("  Me pides CERO objetos.  El cero es una cantidad (unidad 3.2), pero no es una")
        lineas.append("  cantidad que se pueda COGER: dar es coger, y el vacio no se coge.")
        lineas.append("  La pregunta no tiene tarea.  Lo digo en vez de inventarme una respuesta.")
        return "\n".join(lineas)
    lineas.extend(_traza_texto(r))
    if r["conclusion"] == "cogido":
        lineas.append("  COJO (%d objetos):" % len(r["cogidos"]))
        lineas.extend(_cabecera_emparejamiento(
            [(oid, r["secuencia"][i]) for i, oid in enumerate(r["cogidos"])]))
        lineas.append("  (cojo los PRIMEROS del monton, en el orden en que me los das)")
        if r["dejados"]:
            lineas.append("  DEJO (no me los llevo): %s" % ", ".join(r["dejados"]))
        lineas.append("")
        lineas.append("  VERIFICACION (cuento lo que he cogido): la ultima palabra es '%s'"
                      % r["cantidad"])
        lineas.append("  cuadra con lo pedido: %s" % ("SI" if r["verificacion"] else "NO"))
        lineas.append("  (Soy un COUNTER, no un GRABBER: no agarro un punado, cuento.)")
        return "\n".join(_pie(lineas, r, etiqueta="RESULTADO"))
    if r["conclusion"] == "no_hay_bastantes":
        lineas.append("RESULTADO: no_hay_bastantes")
        lineas.append("  En el monton hay menos objetos que los que me pides, y NO me invento los"
                      " que faltan.")
        lineas.append("  (El sistema no tiene objetos propios: solo puede dar de lo que le dan.)")
        return "\n".join(lineas)
    if r["conclusion"] == "no_decidible":
        lineas.append("RESULTADO: no_decidible")
        lineas.append("  El monton esta vacio: no tengo de donde coger.")
        return "\n".join(lineas)
    lineas.append("RESULTADO: palabra_desconocida")
    lineas.append("  '%s' no esta en mi lista, y no me la invento." % palabra)
    return "\n".join(lineas)


def explicar_2_4_tiene(escena, palabra, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (2.4): este conjunto tiene esa cantidad?  ('tiene N?')"]
    r = decidir_2_4_tiene(escena, palabra, saber)
    lineas.append("COLECCION:")
    lineas.extend(_cabecera(r["entidades"]))
    lineas.append("CANTIDAD QUE SE PREGUNTA: %s" % palabra)
    lineas.extend(_traza_texto(r))
    if r["conclusion"] in ("si", "no"):
        lineas.append("  cuento el conjunto y la ultima palabra es: %s" % r["cantidad"])
        lineas.append("  RESULTADO: %s" % ("SI, tiene %s" % palabra if r["conclusion"] == "si"
                                           else "NO, no tiene %s: tiene %s" % (palabra, r["cantidad"])))
    elif r["conclusion"] == "no_decidible":
        lineas.append("RESULTADO: no_decidible  (la coleccion esta vacia)")
    elif r["conclusion"] == "no_alcanza_la_secuencia":
        lineas.append("RESULTADO: no_alcanza_la_secuencia")
        lineas.append("  Hay mas objetos que palabras conozco: no puedo decidirlo.")
    else:
        lineas.append("RESULTADO: palabra_desconocida")
        lineas.append("  '%s' no esta en mi lista, y no me la invento." % palabra)
    if r["conclusion"] in ("si", "no", "no_decidible", "no_alcanza_la_secuencia"):
        lineas.append("  respaldado por el conocimiento 'cardinalidad' (Cardinalidad) [FIJADO]")
    return "\n".join(lineas)


def explicar_2_5_orden(escena, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (2.5): cuenta esta coleccion de dos maneras y dime si sale lo mismo"]
    r = decidir_2_5_orden(escena, saber)
    lineas.append("COLECCION:")
    lineas.extend(_cabecera(r["entidades"]))
    if not escena:
        lineas.append("RESULTADO: no_decidible  (no hay nada que contar)")
        return "\n".join(lineas)
    lineas.extend(_traza_texto(r))
    if r["conclusion"] == "coinciden":
        lineas.append("  ORDEN 1 (como me lo das):")
        lineas.extend(_cabecera_emparejamiento(r["derecho"]))
        lineas.append("     -> la ultima palabra es %s" % r["cantidad_derecho"])
        lineas.append("  ORDEN 2 (al reves):")
        lineas.extend(_cabecera_emparejamiento(r["reves"]))
        lineas.append("     -> la ultima palabra es %s" % r["cantidad_reves"])
        lineas.append("")
        lineas.append("  COINCIDEN: %s   (el orden de los OBJETOS no importa: es una regla"
                      " CONVENCIONAL, no logica)" % ("SI" if r["coinciden"] else "NO"))
        lineas.append("  (Las PALABRAS si van siempre en el mismo orden: esa regla si es logica.)")
        return "\n".join(_pie(lineas, r, etiqueta="RESULTADO"))
    if r["conclusion"] == "no_alcanza_la_secuencia":
        lineas.append("RESULTADO: no_alcanza_la_secuencia")
        lineas.append("  Hay mas objetos que palabras conozco: no puedo decidirlo.")
        return "\n".join(lineas)
    return "\n".join(_pie(lineas, r, etiqueta="RESULTADO"))


def explicar_2_5_conteo(recorrido, palabras, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (2.5): este RECORRIDO de conteo, esta bien hecho?"]
    r = decidir_2_5_conteo(recorrido, palabras, saber)
    if not recorrido:
        lineas.append("RESULTADO: no_decidible  (no hay nada en el recorrido)")
        return "\n".join(lineas)
    lineas.append("RECORRIDO (por donde fue contando, en orden):")
    lineas.extend(_cabecera(r["entidades"]))
    lineas.append("PALABRAS QUE DIJO: %s" % (", ".join(palabras) if palabras else "(ninguna)"))
    lineas.extend(_traza_texto(r))
    if r["conclusion"] == "valido":
        lineas.append("  EMPAREJAMIENTO:")
        lineas.extend(_cabecera_emparejamiento(r["emparejamiento"]))
        lineas.append("")
        lineas.append("  RESULTADO: el conteo es VALIDO.  Empezar por donde quiera es una regla"
                      " CONVENCIONAL: no cambia la cantidad.")
    elif r["conclusion"] == "objeto_repetido":
        lineas.append("  RESULTADO: el conteo NO es valido.")
        lineas.append("  Se conto dos veces el mismo objeto: eso rompe la correspondencia uno a uno,"
                      " que es una regla LOGICA.")
        lineas.append("  (Aunque el total cuadre, la ultima palabra ya no vale: es una"
                      " 'compensacion'.)")
    else:
        detalle = _detalle_error(None, r)
        if detalle:
            lineas.append(detalle)
        lineas.append("  RESULTADO: el conteo NO es valido.")
        lineas.append("  (Cuando el 1-a-1 o el orden de las palabras se rompen, la ultima palabra"
                      " no representa la cantidad.)")
    return "\n".join(_pie(lineas, r, etiqueta="RESULTADO"))


def explicar_2_6_misma_cantidad(izquierda, derecha, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (2.6): estas dos colecciones, tienen la misma cantidad?"
              "  (aunque sean cosas distintas)"]
    r = decidir_2_6_misma_cantidad(izquierda, derecha, saber)
    lineas.append("COLECCION 1:")
    lineas.extend(_cabecera(r["izquierda"]))
    lineas.append("COLECCION 2:")
    lineas.extend(_cabecera(r["derecha"]))
    lineas.extend(_traza_texto(r))
    if r["conclusion"] in ("si", "no"):
        lineas.append("  CUENTO LA 1: la ultima palabra es %s" % r["cantidad_izquierda"])
        lineas.append("  CUENTO LA 2: la ultima palabra es %s" % r["cantidad_derecha"])
        lineas.append("")
        lineas.append("  RESULTADO: %s"
                      % ("SI, las dos tienen la misma cantidad" if r["conclusion"] == "si"
                         else "NO, no tienen la misma cantidad"))
        lineas.append("  (La cantidad NO depende de QUE SEAN las cosas: por eso se pueden comparar"
                      " una silla con un sonido.)")
    elif r["conclusion"] == "no_decidible":
        lineas.append("RESULTADO: no_decidible  (alguna de las dos esta vacia)")
    elif r["conclusion"] == "no_alcanza_la_secuencia":
        lineas.append("RESULTADO: no_alcanza_la_secuencia")
        lineas.append("  Hay mas objetos que palabras conozco: no puedo decidirlo.")
    return "\n".join(_pie(lineas, r, etiqueta="RESULTADO"))


def _puente(cantidad_marcas, palabra, cifra):
    return ["  PUENTE (tres representaciones de lo mismo):",
            "    cantidad:  %s" % cantidad_marcas,
            "    palabra:   %s" % palabra,
            "    cifra:     %s" % cifra]


def _marcas(n):
    """La cantidad dibujada con marcas.  Hasta cien se dibujan una a una (como siempre); con mas,
    una fila de 247 asteriscos no ensena nada, asi que se DICE cuantas son (6.7)."""
    if n <= 100:
        return "*" * n
    return "(%d marcas: demasiadas para dibujarlas una a una)" % n


def explicar_3_1_cifra(palabra, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (3.1): cual es la CIFRA de esta palabra?"]
    r = decidir_3_1_cifra(palabra, saber)
    lineas.append("PALABRA: %s" % palabra)
    lineas.extend(_traza_texto(r))
    if r["conclusion"] == "cifra":
        marcas = _marcas(int(r["cifra"]))
        lineas.extend(_puente(marcas if marcas else "(nada)", palabra, r["cifra"]))
        lineas.append("")
        lineas.append("RESULTADO: %s" % r["cifra"])
        lineas.append("  (OJO: %s es un SIMBOLO. No es la cantidad ni la palabra: es una marca que"
                      " la representa.)" % r["cifra"])
        return "\n".join(lineas)
    if r["conclusion"] == "sin_cifra":
        lineas.append("RESULTADO: sin_cifra")
        lineas.append("  '%s' es una palabra que conozco, pero su cifra son DOS simbolos juntos."
                      % palabra)
        lineas.append("  En esta unidad solo estan las cifras del 1 al 9. No me la invento.")
        return "\n".join(lineas)
    lineas.append("RESULTADO: palabra_desconocida")
    lineas.append("  '%s' no esta en mi lista, y no me la invento." % palabra)
    return "\n".join(lineas)


def explicar_3_1_palabra(cifra, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (3.1): que PALABRA es esta cifra?"]
    r = decidir_3_1_palabra(cifra, saber)
    lineas.append("CIFRA: %s" % cifra)
    lineas.extend(_traza_texto(r))
    if r["conclusion"] == "palabra":
        marcas = _marcas(int(cifra))
        lineas.extend(_puente(marcas if marcas else "(nada)", r["palabra"], cifra))
        lineas.append("")
        lineas.append("RESULTADO: %s" % r["palabra"])
        return "\n".join(lineas)
    lineas.append("RESULTADO: cifra_desconocida")
    lineas.append("  '%s' no es una de las cifras que conozco (del 1 al 9), y no me la invento."
                  % cifra)
    return "\n".join(lineas)


def explicar_3_1_cifra_de(escena, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (3.1): de esta coleccion, cual es su CIFRA?"]
    r = decidir_3_1_cifra_de(escena, saber)
    lineas.append("COLECCION:")
    lineas.extend(_cabecera(r["entidades"]))
    if not escena:
        lineas.extend(_puente("(nada)", "cero", "0"))
        lineas.append("")
        lineas.append("RESULTADO: 0")
        lineas.append("  La coleccion esta vacia: su cantidad es cero y su cifra 0.")
        lineas.append("  (No es 'no se sabe': es una cantidad.)")
        return "\n".join(lineas)
    lineas.extend(_traza_texto(r))
    if r["conclusion"] == "cifra":
        marcas = "*" * len(r["entidades"])
        lineas.extend(_puente(marcas, r["cantidad"], r["cifra"]))
        lineas.append("")
        lineas.append("RESULTADO: %s" % r["cifra"])
        lineas.append("  (camino completo: de la CANTIDAD a la PALABRA, y de la palabra a la CIFRA.)")
        return "\n".join(_pie(lineas, r, etiqueta="RESULTADO"))
    if r["conclusion"] == "no_alcanza_las_cifras":
        lineas.append("RESULTADO: no_alcanza_las_cifras")
        lineas.append("  La cantidad de esta coleccion no tiene cifra entre las que conozco"
                      " (del 1 al 9). Lo digo en vez de inventarmela.")
        return "\n".join(lineas)
    return "\n".join(_pie(lineas, r, etiqueta="RESULTADO"))


def _linea_numeros(r):
    return "  EN LA SECUENCIA DE NUMEROS: %s" % ", ".join(r["numeros"])


def explicar_3_3_siguiente(palabra, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (3.3): que NUMERO va despues de '%s'?" % palabra]
    r = decidir_3_3_siguiente(palabra, saber)
    lineas.extend(_traza_texto(r))
    if r["conclusion"] == "hay_siguiente":
        lineas.append("RESULTADO: %s" % r["siguiente"])
        lineas.append(_linea_numeros(r))
        lineas.append("  respaldado por el conocimiento 'secuencia_de_numeros' [FIJADO]")
        return "\n".join(lineas)
    if r["conclusion"] == "no_lo_se":
        lineas.append("RESULTADO: no_lo_se")
        lineas.append("  '%s' es el ULTIMO numero de la secuencia." % palabra)
        lineas.append("  (El 'diez' no tiene sitio aqui: su cifra son DOS simbolos.)")
        return "\n".join(lineas)
    if r["conclusion"] == "sin_numero":
        lineas.append("RESULTADO: sin_numero")
        lineas.append("  '%s' es una palabra de la lista de CONTAR, pero no tiene sitio en la"
                      " secuencia de NUMEROS." % palabra)
        lineas.append("  (El 'diez' no tiene cifra: son dos simbolos, y eso es el Sistema Decimal.)")
        return "\n".join(lineas)
    lineas.append("RESULTADO: palabra_desconocida")
    lineas.append("  '%s' no esta en ninguna de mis dos listas, y no me lo invento." % palabra)
    return "\n".join(lineas)


def explicar_3_3_anterior(palabra, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (3.3): que NUMERO va antes de '%s'?" % palabra]
    r = decidir_3_3_anterior(palabra, saber)
    lineas.extend(_traza_texto(r))
    if r["conclusion"] == "hay_anterior":
        lineas.append("RESULTADO: %s" % r["anterior"])
        lineas.append(_linea_numeros(r))
        if palabra == "uno":
            lineas.append("  (OJO: esto es la secuencia de NUMEROS. En la lista de CONTAR, el uno"
                          " es el primero: contar arranca en el primer objeto, no en el cero.)")
        return "\n".join(lineas)
    if r["conclusion"] == "no_lo_se":
        lineas.append("RESULTADO: no_lo_se")
        lineas.append("  '%s' es el PRIMER numero de la secuencia: antes no hay nada." % palabra)
        return "\n".join(lineas)
    if r["conclusion"] == "sin_numero":
        lineas.append("RESULTADO: sin_numero")
        lineas.append("  '%s' es una palabra de la lista de CONTAR, pero no tiene sitio en la"
                      " secuencia de NUMEROS." % palabra)
        return "\n".join(lineas)
    lineas.append("RESULTADO: palabra_desconocida")
    lineas.append("  '%s' no esta en ninguna de mis dos listas, y no me lo invento." % palabra)
    return "\n".join(lineas)


def explicar_3_3_listas(saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    d = decidir_3_3_dos_listas(saber)
    lineas = ["PREGUNTA (3.3): ensename las dos listas y en que se diferencian", ""]
    lineas.append("  LA LISTA DE CONTAR (para contar cosas; empieza en el primer objeto):")
    lineas.append("    %s" % ", ".join(d["conteo"]))
    lineas.append("  LA SECUENCIA DE NUMEROS (el orden de los numeros; lleva el cero delante):")
    lineas.append("    %s" % ", ".join(d["numeros"]))
    lineas.append("")
    lineas.append("  DIFERENCIA: la lista de contar es la secuencia de numeros SIN el cero, y sin el")
    lineas.append("  'diez' (que no tiene cifra).  Contar cosas empieza en 'uno'; los numeros empiezan")
    lineas.append("  en 'cero'.")
    lineas.append("  respaldado por el conocimiento 'secuencia_de_numeros' [FIJADO]")
    return "\n".join(lineas)


def explicar_pregunta(texto, saber=None):
    """
    Despacha segun lo que se escriba:
      'color=rojo: a(...); b(...)'   -> 0.2 formar
      'a(color=rojo); b(color=rojo)' -> 0.2 reconocer
      'silla,mesa'                   -> 0.1

    Si no se entiende lo escrito, lo dice.  Nunca revienta: un fallo con traceback no
    ensena nada a quien esta probando, y el sistema tiene que saber decir "no entiendo".
    """
    if saber is None:
        saber = cargar_conocimiento()
    t = texto.strip()
    try:
        if t.lower().strip() in ("piezas", "mapa"):
            return explicar_piezas(saber)
        if t.lower().startswith("divisible"):
            return explicar_divisible(t[len("divisible"):].lstrip(":").strip(), saber)
        if t.lower().startswith("tabla del"):
            return explicar_tabla(t, saber)
        if t.lower().startswith("mitad"):
            return explicar_mitad(t[len("mitad"):].lstrip(":").strip(), saber)
        if es_division(t):
            return explicar_dividir(t, saber)
        if es_multiplicacion(t):
            return explicar_multiplicar(t, saber)
        if re.match(r"^(filas:\s*)?\d+\s+(filas?|columnas?)\s+de\s+\d+", t.lower()):
            return explicar_filas(re.sub(r"^filas:\s*", "", t.lower()), saber)
        if re.match(r"^de\s+\d+\s+en\s+\d+", t.lower()):
            return explicar_saltos(t, saber)
        if t.lower().startswith("redondear"):
            return explicar_redondear(t[len("redondear"):].lstrip(":").strip(), saber)
        if t.lower().startswith("par:") or t.lower().startswith("par "):
            return explicar_paridad(t[3:].lstrip(":").strip(), saber)
        if t.lower().startswith("ecuacion") or t.lower().startswith("hueco"):
            resto = t.split(":", 1)[1] if ":" in t else t
            if es_ecuacion_con_letra(resto):
                return explicar_ecuacion_letra(resto, saber)
            return explicar_ecuacion(resto, saber)
        if es_ecuacion_con_letra(t):
            return explicar_ecuacion_letra(t, saber)
        if t.lower().startswith("verdad"):
            resto = t.split(":", 1)[1] if ":" in t else t[len("verdad"):]
            return explicar_igualdad(resto, saber)
        if t.lower().startswith("calcular"):
            return explicar_calculo(t[len("calcular"):].strip(), saber)
        if t.lower().strip() == "memoria":
            return explicar_memoria(saber)
        if t.lower().startswith("aprender"):
            resto = t[len("aprender"):].strip().lstrip(":").strip()
            return explicar_aprender(resto, saber)
        if t.lower().startswith("olvidar"):
            resto = t[len("olvidar"):].strip().lstrip(":").strip().lower()
            if resto != "todo":
                return "NO ENTIENDO ESTO: se escribe  olvidar: todo   (borra la memoria de hechos)"
            olvidar_todo()
            return "PREGUNTA: olvidar todo lo que se de memoria\n\nRESULTADO: olvidado (vuelvo a calcularlo todo)"
        if t.lower().startswith("problema"):
            resto = t[len("problema"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            if not resto:
                return ("NO ENTIENDO ESTO: dame el enunciado.\n"
                        "   se escribe asi:  problema: Ana tiene 5 manzanas. Le dan 3. Cuantas tiene ahora?")
            if es_problema_por(resto, saber):
                return explicar_R2_problema(resto, saber)
            return explicar_R1_problema(resto, saber)
        if t.lower().startswith("cifra_de"):
            resto = t[len("cifra_de"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            return explicar_3_1_cifra_de(escena_cantidad(resto, saber), saber)
        if t.lower().startswith("cifra"):
            resto = t[len("cifra"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            return explicar_3_1_cifra(resto.lower(), saber)
        if t.lower().startswith("palabra"):
            resto = t[len("palabra"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            return explicar_3_1_palabra(resto, saber)
        if t.lower().startswith("misma_cantidad"):
            resto = t[len("misma_cantidad"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, _, der = resto.partition("/")
            return explicar_2_6_misma_cantidad(escena_cantidad(izq, saber), escena_cantidad(der, saber), saber)
        if t.lower().startswith("orden"):
            resto = t[len("orden"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            return explicar_2_5_orden(escena_cantidad(resto, saber), saber)
        if t.lower().startswith("conteo"):
            resto = t[len("conteo"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, _, der = resto.partition("/")
            return explicar_2_5_conteo(escena_cantidad(izq, saber),
                                       [p.strip().lower() for p in der.split(",") if p.strip()],
                                       saber)
        if t.lower().startswith("dame"):
            resto = t[len("dame"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            if "/" not in resto:
                return ("NO ENTIENDO ESTO: dame necesita un MONTON del que coger.\n"
                        "   se escribe asi:  dame: <monton> / <cantidad>\n"
                        "   ejemplo:         dame: silla_1, silla_2, mesa / tres\n\n"
                        "El sistema no tiene objetos propios: no se inventa de donde coger.")
            izq, _, der = resto.partition("/")
            return explicar_2_4_dame(escena_cantidad(izq, saber), der.strip().lower(), saber)
        if t.lower().startswith("tiene"):
            resto = t[len("tiene"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, _, der = resto.partition("/")
            return explicar_2_4_tiene(escena_cantidad(izq, saber), der.strip().lower(), saber)
        if t.lower().startswith("listas"):
            return explicar_3_3_listas(saber)
        if t.lower().startswith("nombre"):
            resto = t[len("nombre"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            if not resto:
                return ("NO ENTIENDO ESTO: dime un numero del 1 al 100.\n"
                        "   se escribe asi:  nombre: 47")
            return explicar_6_1_nombre(resto, saber)
        if t.lower().startswith("numero"):
            resto = t[len("numero"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            if not resto:
                return ("NO ENTIENDO ESTO: dime un nombre de numero.\n"
                        "   se escribe asi:  numero: cuarenta y siete")
            return explicar_6_1_numero(resto, saber)
        if t.lower().startswith("columnas"):
            resto = t[len("columnas"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            # Unidad 7.5: 'columnas: 72 - 45' es la RESTA por columnas (y el intercambio).
            if "-" in resto or "menos" in resto.lower():
                sep = "-" if "-" in resto else "menos"
                izq, s, der = resto.partition(sep)
                if not s:
                    return ("NO ENTIENDO ESTO: restar por columnas quita DOS numeros.\n"
                            "   se escribe asi:  columnas: 72 - 45")
                return explicar_7_5_columnas(izq.strip(), der.strip(), saber)
            sep = "+" if "+" in resto else "/"
            izq, s, der = resto.partition(sep)
            if not s:
                return ("NO ENTIENDO ESTO: columnas suma o resta DOS numeros.\n"
                        "   se escribe asi:  columnas: 47 + 15   o   columnas: 72 - 45")
            return explicar_7_3_columnas(izq.strip(), der.strip(), saber)
        if t.lower().startswith("partir"):
            resto = t[len("partir"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            if not resto:
                return "NO ENTIENDO ESTO: dime un numero.\n   se escribe asi:  partir: 47"
            return explicar_6_5_partir(resto, saber)
        if t.lower().startswith("juntar_decenas"):
            resto = t[len("juntar_decenas"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, _, der = resto.partition("/")
            if izq.strip() == "" or der.strip() == "":
                return ("NO ENTIENDO ESTO: dime las decenas, una barra, y las unidades.\n"
                        "   se escribe asi:  juntar_decenas: 4 / 7")
            return explicar_6_5_juntar_decenas(izq.strip(), der.strip(), saber)
        if t.lower().strip() == "tabla":
            return explicar_6_3_tabla(saber)
        if t.lower().strip() in ("centena", "centenas"):
            return explicar_6_7_escalera(saber)
        if t.lower().startswith("centena"):
            resto = t[len("centena"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            if not resto:
                return "NO ENTIENDO ESTO: dime un numero.\n   se escribe asi:  centena: 247"
            return explicar_6_7_centena(resto, saber)
        if t.lower().startswith("sitio"):
            resto = t[len("sitio"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            if not resto:
                return "NO ENTIENDO ESTO: dime un numero.\n   se escribe asi:  sitio: 47"
            return explicar_6_3_sitio(resto, saber)
        if t.lower().startswith("agrupar"):
            resto = t[len("agrupar"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            return explicar_6_2_agrupar(escena_cantidad(resto, saber), saber)
        if t.lower().startswith("derivar"):
            resto = t[len("derivar"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            sep = "+" if "+" in resto else "/"
            izq, s, der = resto.partition(sep)
            if not s:
                return ("NO ENTIENDO ESTO: derivar suma DOS numeros.\n"
                        "   se escribe asi:  derivar: 7 + 5")
            return explicar_7_2_derivar(izq.strip(), der.strip(), saber)
        if t.lower().startswith("dedos"):
            resto = t[len("dedos"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            # Unidad 7.4: 'dedos: 9 - 4' es la RESTA con los dedos (se baja el segundo).
            # 'dedos: 8 + 5' es la SUMA (se cuentan los dedos del segundo hacia adelante).
            if "-" in resto or "menos" in resto.lower():
                sep = "-" if "-" in resto else "menos"
                izq, s, der = resto.partition(sep)
                if not s:
                    return ("NO ENTIENDO ESTO: la resta con los dedos quita DOS numeros.\n"
                            "   se escribe asi:  dedos: 9 - 4")
                return explicar_7_4_resta_dedos(izq.strip(), der.strip(), saber)
            sep = "+" if "+" in resto else "/"
            izq, s, der = resto.partition(sep)
            if not s:
                return ("NO ENTIENDO ESTO: el metodo de los dedos suma o resta DOS numeros.\n"
                        "   se escribe asi:  dedos: 8 + 5   o   dedos: 9 - 4")
            return explicar_7_1_dedos(izq.strip(), der.strip(), saber)
        if t.lower().startswith("decenas"):
            return explicar_6_1_decenas(saber)
        if t.lower().startswith("diferencia_numeros"):
            resto = t[len("diferencia_numeros"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, sep, der = resto.partition("/")
            if not sep:
                return ("NO ENTIENDO ESTO: para la diferencia hacen falta DOS numeros.\n"
                        "   se escribe asi:  diferencia_numeros: 5 / 3")
            return explicar_5_5_diferencia_numeros(izq.strip(), der.strip(), saber)
        if t.lower().startswith("diferencia"):
            resto = t[len("diferencia"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, sep, der = resto.partition("/")
            if not sep:
                return ("NO ENTIENDO ESTO: la diferencia necesita DOS colecciones.\n"
                        "   se escribe asi:  diferencia: <una coleccion> / <otra coleccion>\n"
                        "   ejemplo:         diferencia: a,b,c,d,e / a,b,c\n\n"
                        "Con una sola no hay hueco que mirar.")
            return explicar_5_5_diferencia(escena_cantidad(izq, saber),
                                           escena_cantidad(der, saber), saber)
        if t.lower().startswith("restar_numeros"):
            resto = t[len("restar_numeros"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            sep = "-" if "-" in resto else "/"
            izq, s, der = resto.partition(sep)
            if not s:
                return ("NO ENTIENDO ESTO: para restar numeros hacen falta DOS numeros.\n"
                        "   se escribe asi:  restar_numeros: 5 - 2\n\n"
                        "Con uno solo no hay nada que quitar.")
            return explicar_5_4_restar_numeros(izq.strip(), der.strip(), saber)
        if t.lower().startswith("quitar"):
            resto = t[len("quitar"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, sep, der = resto.partition("/")
            if not sep:
                return ("NO ENTIENDO ESTO: quitar necesita un MONTON y UNA CANTIDAD.\n"
                        "   se escribe asi:  quitar: <monton> / <cuantos>\n"
                        "   ejemplo:         quitar: a,b,c,d,e / dos\n\n"
                        "El sistema no tiene objetos propios: no se inventa de donde quitar.")
            return explicar_5_4_quitar(escena_cantidad(izq, saber), der.strip(), saber)
        if t.lower().startswith("sumar_numeros"):
            resto = t[len("sumar_numeros"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            sep = "+" if "+" in resto else "/"
            izq, s, der = resto.partition(sep)
            if not s:
                return ("NO ENTIENDO ESTO: para sumar numeros hacen falta DOS numeros.\n"
                        "   se escribe asi:  sumar_numeros: 3 + 2\n\n"
                        "Con uno solo no hay nada que juntar.")
            return explicar_5_3_sumar_numeros(izq.strip(), der.strip(), saber)
        if t.lower().startswith("sumar"):
            resto = t[len("sumar"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, sep, der = resto.partition("/")
            if not sep:
                return ("NO ENTIENDO ESTO: para sumar hacen falta DOS cantidades.\n"
                        "   se escribe asi:  sumar: <coleccion> / <coleccion>\n"
                        "   ejemplo:         sumar: a,b,c / d,e\n\n"
                        "Con una sola cantidad no hay nada que juntar.")
            return explicar_5_2_sumar(escena_cantidad(izq, saber), escena_cantidad(der, saber), saber)
        if t.lower().startswith("anadir"):
            resto = t[len("anadir"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, sep, der = resto.partition("/")
            if not sep:
                return ("NO ENTIENDO ESTO: para anadir hacen falta DOS cantidades.\n"
                        "   se escribe asi:  anadir: <coleccion> / <lo que se anade>\n"
                        "   ejemplo:         anadir: a,b,c / d,e\n\n"
                        "Si no hay nada que anadir, el monton no crece.")
            return explicar_5_2_anadir(escena_cantidad(izq, saber), escena_cantidad(der, saber), saber)
        if t.lower().startswith("descomponer_numero"):
            resto = t[len("descomponer_numero"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            return explicar_5_3_descomponer_numero(resto, saber)
        if t.lower().startswith("descomponer"):
            resto = t[len("descomponer"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            return explicar_5_1_descomponer(escena_cantidad(resto, saber), saber)
        if t.lower().startswith("componer"):
            resto = t[len("componer"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, sep, der = resto.partition("/")
            if not sep:
                return ("NO ENTIENDO ESTO: componer necesita DOS partes.\n"
                        "   se escribe asi:  componer: <coleccion> / <coleccion>\n"
                        "   ejemplo:         componer: a,b / c,d,e\n\n"
                        "Para juntar hacen falta DOS partes (las partes son lo que se junta).")
            return explicar_5_1_componer(escena_cantidad(izq, saber), escena_cantidad(der, saber), saber)
        if t.lower().startswith("comparar_cifras") or t.lower().startswith("comparar_numeros"):
            resto = t[len("comparar_numeros"):].strip() if t.lower().startswith("comparar_numeros") else t[len("comparar_cifras"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, sep, der = resto.partition("/")
            if not sep:
                return ("NO ENTIENDO ESTO: comparar_cifras necesita DOS numeros.\n"
                        "   se escribe asi:  comparar_cifras: 3 / 2\n\n"
                        "Comparar es comparar DOS cosas: con una sola no hay nada que decidir.")
            return explicar_4_2_comparar_cifras(izq.strip(), der.strip(), saber)
        if t.lower().startswith("comparar"):
            resto = t[len("comparar"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, sep, der = resto.partition("/")
            if not sep:
                return ("NO ENTIENDO ESTO: comparar necesita DOS colecciones.\n"
                        "   se escribe asi:  comparar: <coleccion> / <coleccion>\n"
                        "   ejemplo:         comparar: a,b,c / d,e\n\n"
                        "Comparar es comparar DOS cosas: con una sola no hay nada que decidir.")
            return explicar_4_1_comparar(escena_cantidad(izq, saber), escena_cantidad(der, saber), saber)
        if t.lower().startswith("caminos"):
            return explicar_3_4_caminos(saber)
        if t.lower().startswith("puente"):
            resto = t[len("puente"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            return explicar_3_4_puente(escena_cantidad(resto, saber), saber)
        if t.lower().startswith("cuantos"):
            resto = t[len("cuantos"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            return explicar_2_3_cuantos(escena_cantidad(resto, saber), saber)
        if t.lower().startswith("revisar_secuencia"):
            resto = t[len("revisar_secuencia"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            palabras = [nombre_de_numero(p, saber)[0] for p in resto.split(",") if p.strip()]
            return explicar_2_2_revisar(palabras, saber)
        if t.lower().startswith("recitar"):
            resto = t[len("recitar"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            return explicar_2_2_recitar(resto, saber)
        if t.lower().startswith("siguiente"):
            resto = t[len("siguiente"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            return explicar_3_3_siguiente(resto, saber)
        if t.lower().startswith("anterior"):
            resto = t[len("anterior"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            return explicar_3_3_anterior(resto, saber)
        if t.lower().startswith("revisar"):
            resto = t[len("revisar"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, _, der = resto.partition("/")
            objetos = escena_cantidad(izq, saber)
            palabras = [p.strip().lower() for p in der.split(",") if p.strip()]
            return explicar_2_1_revisar(objetos, palabras, saber)
        if t.lower().startswith("contar"):
            resto = t[len("contar"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            return explicar_2_1_contar(escena_cantidad(resto, saber), saber)
        if t.lower().startswith("subitizar"):
            resto = t[len("subitizar"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            return explicar_1_0_subitizar(resto, saber)
        if t.lower().startswith("pertenece"):
            resto = t[len("pertenece"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, _, der = resto.partition(":")
            return explicar_0_3_pertenencia(escena_cantidad(der, saber), parsear_criterio(izq), saber)
        if ":" in t and "=" in t.split(":", 1)[0] and "(" not in t.split(":", 1)[0]:
            izq, _, der = t.partition(":")
            return explicar_0_2_formar(escena_cantidad(der, saber), parsear_criterio(izq), saber)
        if "(" in t or ";" in t:
            return explicar_0_2_reconocer(escena_cantidad(t, saber), saber)
        return explicar(escena_0_1(t), saber)
    except Exception as e:  # NUNCA un traceback delante de quien prueba
        if not isinstance(e, ValueError):
            return ("NO ENTIENDO ESTO: se ha roto algo por dentro (%s: %s).\n\n"
                    "El sistema no deberia reventar nunca: lo siento, apuntalo.\n"
                    % (type(e).__name__, e))
        return ("NO ENTIENDO ESTO: %s\n\n"
                "FORMAS QUE SI ENTIENDO:\n"
                "  0.1  un objeto o varios  silla,mesa\n"
                "  0.2  forman grupo?       a(color=rojo,forma=cubo); b(color=azul,forma=cubo)\n"
                "  0.2  dame el grupo de... color=rojo: a(color=rojo); b(color=azul)\n"
                "  0.3  pertenece           pertenece color=rojo: taza(color=rojo)\n"
                "  1.0  subitizar          subitizar: x.x/.../x.x\n"
                "  2.1  contar             contar: a, b, c\n"
                "  2.1  revisar            revisar: a,b,c / uno,dos,tres\n"
                "  2.2  siguiente          siguiente: tres\n"
                "  2.2  anterior           anterior: tres\n"
                "  2.2  recitar            recitar: ocho\n"
                "  2.2  revisar_secuencia  revisar_secuencia: uno,dos,cuatro\n"
                "  3.3  listas            listas                 (las dos listas y su diferencia)\n"
                "  3.4  caminos           caminos                (los seis caminos del puente)\n"
                "  3.4  puente            puente: a,b,c          (la coleccion de las tres maneras)\n"
                "  4.1  comparar          comparar: a,b,c / d,e   (mas / menos / tantos_como)\n"
                "  4.2  comparar_cifras   comparar_cifras: 3 / 2  (> < =, la boca mira al mayor)\n"
                "  5.1  descomponer       descomponer: a,b,c,d,e  (todas las maneras de partir en dos)\n"
                "  5.1  componer          componer: a,b / c,d,e   (juntar las partes)\n"
                "  5.2  sumar             sumar: a,b,c / d,e      (agregacion: el signo + y el =)\n"
                "  5.2  anadir            anadir: a,b,c / d,e     (aumentacion: el monton crece)\n"
                "  5.3  sumar_numeros     sumar_numeros: 3 + 2   (numeros, sin objetos)\n"
                "  5.3  descomponer_numero descomponer_numero: 5 (partir un numero)\n"
                "  5.3  comparar_numeros  comparar_numeros: dos / 3 (cifra o palabra)\n"
                "  5.4  quitar            quitar: a,b,c,d,e / dos (resta: quitar de un monton)\n"
                "  5.4  restar_numeros    restar_numeros: 5 - 2  (numeros, sin objetos)\n"
                "  5.5  diferencia        diferencia: a,b,c,d,e / a,b,c (el HUECO entre las dos)\n"
                "  5.5  diferencia_numeros diferencia_numeros: 5 / 3\n"
                "  6.1  nombre             nombre: 47  (y ENSENA como se construyo el nombre)\n"
                "  6.1  numero             numero: cuarenta y siete  (la vuelta)\n"
                "  6.1  decenas            las decenas y el error de decena\n"
                "  7.1  dedos              dedos: 8 + 5  (el METODO de sumar: se anota el primero,\n"
                "                          se cuentan los dedos del segundo y se sigue desde el primero)\n"
                "  2.3  cuantos           cuantos: silla_1, silla_2, silla_3\n"
                "  2.4  dame              dame: a,b,c,d,e / tres\n"
                "  2.4  tiene             tiene: a,b,c / tres\n"
                "  2.5  orden             orden: a,b,c\n"
                "  2.5  conteo            conteo: c,a,b / uno,dos,tres\n"
                "  2.6  misma_cantidad    misma_cantidad: silla_1,silla_2 / sonido_1,sonido_2\n"
                "  3.1  cifra             cifra: tres           (palabra -> cifra)\n"
                "  3.1  palabra           palabra: 3            (cifra   -> palabra)\n"
                "  3.1  cifra_de          cifra_de: a,b,c       (cantidad -> cifra)\n\n"
                "El sistema no adivina: si no entiende, lo dice." % e)
