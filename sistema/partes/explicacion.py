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


# explicar_pregunta (la puerta de entrada) vive desde U.4 en puertas.py: UNA tabla de puertas, la misma para
# lo que se ensena y para la respuesta corta del probador.
