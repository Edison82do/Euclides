# -*- coding: utf-8 -*-
"""
Euclides - Nivel 4 - relaciones (4.1, 4.2).

Este archivo es UNA PARTE del motor.  No se importa suelto: lo carga sistema/motor.py,
que junta todas las partes en un solo espacio de nombres (por eso aqui se usan funciones
definidas en otras partes sin importarlas).  Ver sistema/partes/__init__.py.
"""

import os  # noqa: F401
import sys  # noqa: F401

# ------------------------------------------------------- comparar (4.1)

def _tamanos(r):
    """Los tamanos que aparecen en las dos colecciones, si es que aparece alguno."""
    vistos = set()
    for o in list(r["primera"]) + list(r["segunda"]):
        t = o["atributos"].get("tamano")
        if t:
            vistos.add(t)
    return sorted(vistos)


def explicar_4_1_comparar(escena_a, escena_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (4.1): compara estas DOS colecciones (cual tiene mas?)"]
    r = decidir_4_1_comparar(escena_a, escena_b, saber)
    lineas.append("PRIMERA COLECCION:")
    lineas.extend(_cabecera(r["primera"]))
    lineas.append("SEGUNDA COLECCION:")
    lineas.extend(_cabecera(r["segunda"]))
    if r["conclusion"] == "no_alcanza":
        lineas.append("")
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  Alguna de las dos tiene mas objetos de los que se contar (mi lista llega a")
        lineas.append("  diez). Lo digo en vez de inventarme la comparacion.")
        return "\n".join(lineas)
    lineas.extend(_traza_texto(r))
    lineas.append("")
    lineas.append("  CAMINO 1, EMPAREJAR (uno a uno, SIN contar):")
    for x, y in r["emparejadas"]:
        lineas.append("    %-12s -- %s" % (x, y))
    for x in r["sobra_primera"]:
        lineas.append("    %-12s -- (no tiene pareja)" % x)
    for y in r["sobra_segunda"]:
        lineas.append("    %-12s -- (no tiene pareja)" % y)
    if not r["emparejadas"] and not r["sobra_primera"] and not r["sobra_segunda"]:
        lineas.append("    (las dos estan vacias: no hay nada que emparejar)")
    lineas.append("")
    lineas.append("  CAMINO 2, CONTAR (la verificacion):")
    lineas.append("    primera: %d -> %s" % (len(r["primera"]), r["cantidad_primera"]))
    lineas.append("    segunda: %d -> %s" % (len(r["segunda"]), r["cantidad_segunda"]))
    lineas.append("    los dos caminos dicen lo mismo: %s" % ("SI" if r["verificacion"] else "NO"))
    if not r["verificacion"]:
        lineas.append("    NO CUADRAN. El sistema no elige uno: lo dice.")
    tamanos = _tamanos(r)
    if len(tamanos) > 1:
        lineas.append("")
        lineas.append("  OJO AL TAMANO: hay objetos %s." % " y ".join(tamanos))
        lineas.append("  El tamano NO cuenta: dos cosas grandes NO son mas que tres pequenas.")
        lineas.append("  La cantidad son las COSAS, no lo que ocupan.")
    lineas.append("")
    if r["conclusion"] == "tantos_como":
        lineas.append("RESULTADO: tantos_como")
        lineas.append("  Las dos tienen lo mismo: %s.  Ni mas ni menos." % r["cantidad_primera"])
    elif r["conclusion"] == "mas":
        lineas.append("RESULTADO: mas")
        lineas.append("  La PRIMERA tiene mas: %s contra %s."
                      % (r["cantidad_primera"], r["cantidad_segunda"]))
    else:
        lineas.append("RESULTADO: menos")
        lineas.append("  La PRIMERA tiene menos: %s contra %s."
                      % (r["cantidad_primera"], r["cantidad_segunda"]))
    lineas.append("  (Se dice con palabras: los simbolos >, <, = van entre CIFRAS, y son la 4.2.)")
    return "\n".join(lineas)


def _a_cifra(texto, saber):
    """
    Unidad 6.3: traduce lo que le den a la CIFRA del numero, sea cifra (47) o palabra (cuarenta y
    siete).  Es el traductor comun de las ordenes que trabajan con numeros, para que NO haya dos
    verdades: si el lector sabe leer 47, lo sabe en todas las ordenes.
    Devuelve el texto tal cual si no es un numero que conozca (asi las reglas diran cifra_desconocida).
    """
    t = texto.strip()
    n = _cifra_a_numero(t, saber)
    if n is not None:
        return str(n)
    v = _valor_de_numero(t.lower(), saber)
    if v is not None:
        return str(v)
    return texto


def decidir_4_2_comparar_cifras(cifra_a, cifra_b, saber=None):
    """
    Unidad 4.2: comparar dos CIFRAS.  La respuesta es el SIMBOLO: >, < o =.

    De donde sale: en la secuencia de numeros (3.3), EL QUE VIENE DESPUES ES EL MAYOR.  Y eso cuadra
    con las cantidades (4.1): si 3 > 2, es porque tres cosas son mas que dos.
    """
    if saber is None:
        saber = cargar_conocimiento()
    tabla = _tabla(saber)
    inversa = {v: k for k, v in tabla.items()}
    # Unidad 5.3 / 6.3: un numero se dice con CIFRA o con PALABRA, y las dos valen (tambien de dos
    # cifras).  ('manzana' no se traduce: dara cifra_desconocida.)
    cifra_a = _a_cifra(cifra_a, saber)
    cifra_b = _a_cifra(cifra_b, saber)
    numeros = list(saber["secuencia_de_numeros"]["numeros"])
    cuenta = {"secuencia": saber["secuencia_de_conteo"]["palabras"], "numeros": numeros,
              "tabla_inversa": inversa, "otra_cifra": cifra_b}
    r = _aplicar_reglas(saber["reglas_4_2"]["reglas_comparar_cifras"], None, None, saber,
                        cuenta=cuenta, palabra=cifra_a)
    r["cifra_a"], r["cifra_b"] = cifra_a, cifra_b
    r["numeros"] = numeros
    r["simbolos"] = {">": "mayor que", "<": "menor que", "=": "igual a"}
    if r["conclusion"] in ("mayor", "menor", "iguales"):
        r["simbolo"] = {"mayor": ">", "menor": "<", "iguales": "="}[r["conclusion"]]
        r["palabra_a"] = nombre_de_numero(cifra_a, saber)[0]
        r["palabra_b"] = nombre_de_numero(cifra_b, saber)[0]
        r["sitio_a"] = _sitio_cifra(cifra_a, cuenta)
        r["sitio_b"] = _sitio_cifra(cifra_b, cuenta)
        r["cantidad_a"] = "%d" % (r["sitio_a"])
        r["cantidad_b"] = "%d" % (r["sitio_b"])
        # COHERENCIA con las cantidades (unidad 4.1): el simbolo tiene que cuadrar con la cuenta
        r["por_cantidad"] = ("mayor" if r["sitio_a"] > r["sitio_b"]
                             else "menor" if r["sitio_a"] < r["sitio_b"] else "iguales")
        r["cuadra"] = (r["por_cantidad"] == r["conclusion"])
    return r


def explicar_4_2_comparar_cifras(cifra_a, cifra_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (4.2): compara estos DOS NUMEROS (cifras)"]
    r = decidir_4_2_comparar_cifras(cifra_a, cifra_b, saber)
    lineas.append("NUMEROS:  %s  y  %s" % (cifra_a, cifra_b))
    lineas.extend(_traza_texto(r))
    if r["conclusion"] == "cifra_desconocida":
        lineas.append("RESULTADO: cifra_desconocida")
        lineas.append("  Alguna de las dos no es una cifra que conozco (del 0 al 9), y no me la")
        lineas.append("  invento.  (El 10 son dos simbolos: eso es el Sistema Decimal.)")
        return "\n".join(lineas)
    lineas.append("")
    lineas.append("  LAS TRES MANERAS DE DECIRLO:")
    lineas.append("    cifras:     %s  y  %s" % (r["cifra_a"], r["cifra_b"]))
    lineas.append("    palabras:   %s  y  %s" % (r["palabra_a"], r["palabra_b"]))
    lineas.append("    cantidad:   %s cosas  y  %s cosas" % (r["cantidad_a"], r["cantidad_b"]))
    lineas.append("")
    lineas.append("  DE DONDE SALE (el orden de la secuencia de numeros, unidad 3.3):")
    lineas.append("    %s" % ", ".join(r["numeros"]))
    lineas.append("    el '%s' esta en el sitio %d y el '%s' en el sitio %d: el que viene DESPUES"
                  % (r["palabra_a"], r["sitio_a"], r["palabra_b"], r["sitio_b"]))
    lineas.append("    es el MAYOR.")
    lineas.append("")
    lineas.append("  Y CUADRA CON LAS CANTIDADES (unidad 4.1): %s cosas frente a %s cosas."
                  % (r["cantidad_a"], r["cantidad_b"]))
    lineas.append("    los dos caminos dicen lo mismo: %s" % ("SI" if r["cuadra"] else "NO"))
    if not r["cuadra"]:
        lineas.append("    NO CUADRAN. El sistema no elige uno: lo dice.")
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["simbolo"])
    lineas.append("  %s %s %s   (%s es %s %s)"
                  % (r["cifra_a"], r["simbolo"], r["cifra_b"], r["palabra_a"],
                     r["simbolos"][r["simbolo"]], r["palabra_b"]))
    if r["conclusion"] in ("mayor", "menor"):
        lineas.append("  La boca del simbolo (%s) mira al numero MAYOR, que es el %s."
                      % (r["simbolo"], r["cifra_a"] if r["conclusion"] == "mayor" else r["cifra_b"]))
    lineas.append("  (Los simbolos van entre CIFRAS.  Entre CANTIDADES se dice con palabras:")
    lineas.append("   mas, menos, tantos_como; eso es la unidad 4.1.)")
    return "\n".join(lineas)


def _puente_mejor(marcas, palabra, cifra):
    """Como _puente, pero si la cifra no la tiene, lo DICE en vez de inventarla.
    (La cifra del diez no existe: son dos simbolos.  Unidad 3.4.)"""
    if cifra is None:
        return ["  PUENTE (las representaciones que SI tengo):",
                "    cantidad:  %s" % marcas,
                "    palabra:   %s" % palabra,
                "    cifra:     (no la tengo: el diez son DOS simbolos)"]
    return _puente(marcas, palabra, cifra)


def decidir_5_1_descomponer(escena, saber=None):
    """
    Unidad 5.1: partir una coleccion en DOS partes, TODAS las maneras.

    Dos reglas de forma, las dos de la investigacion:
      - NO se repite el orden: (2,3) y (3,2) son LA MISMA pareja (conmutatividad; y la unidad 2.5 ya
        enseno que el orden no importa).  Asi que solo se listan las parejas con k <= n-k.
      - El CERO es una parte valida ('cero y cinco'), pero el cero como TODO no se parte.
    """
    if saber is None:
        saber = cargar_conocimiento()
    reales = entidades_reales(escena)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    cuenta = {"secuencia": secuencia}
    r = _aplicar_reglas(saber["reglas_5_1"]["reglas_descomponer"], reales, None, saber, cuenta=cuenta)
    r["entidades"] = reales
    r["secuencia"] = secuencia
    if r["conclusion"] == "parejas":
        n = len(reales)
        tabla = _tabla(saber)
        r["total"] = _palabra_de(n, secuencia)
        # OJO: la cifra del DIEZ no existe (son dos simbolos, Sistema Decimal).  Si el todo es diez,
        # el sistema da la palabra y dice que la cifra no la tiene (igual que en la 3.4).
        r["total_cifra"] = tabla.get(r["total"])
        r["parejas"] = parejas_que_suman(n, saber)        # mecanismo.py
        r["parejas_palabras"] = [(_palabra_de(k, secuencia), _palabra_de(m, secuencia))
                                 for k, m in r["parejas"]]
        r["parejas_cifras"] = [(tabla.get(_palabra_de(k, secuencia)),
                                tabla.get(_palabra_de(m, secuencia)))
                               for k, m in r["parejas"]]
        r["cuantas_maneras"] = len(r["parejas"])
        # VERIFICACION: recomponer cada pareja tiene que devolver el todo (la vuelta verifica la ida)
        r["verificacion"] = all(leer(contar_adelante(decir(k, saber), decir(m, saber), saber,
                                                     con_dedos=False)["resultado"], saber) == n
                                for k, m in r["parejas"])
    return r


def decidir_5_1_componer(escena_a, escena_b, saber=None):
    """Unidad 5.1: juntar dos colecciones y decir el TODO."""
    if saber is None:
        saber = cargar_conocimiento()
    a = entidades_reales(escena_a)
    b = entidades_reales(escena_b)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    cuenta = {"secuencia": secuencia, "otra": b}
    r = _aplicar_reglas(saber["reglas_5_1"]["reglas_componer"], a, None, saber, cuenta=cuenta)
    r["primera"] = a
    r["segunda"] = b
    r["secuencia"] = secuencia
    if r["conclusion"] == "junto":
        n = contar_todo(a, b)              # se juntan y se cuentan TODOS
        tabla = _tabla(saber)
        r["parte_a"] = _palabra_de(len(a), secuencia)
        r["parte_b"] = _palabra_de(len(b), secuencia)
        r["total"] = _palabra_de(n, secuencia)
        r["total_cifra"] = tabla.get(r["total"])
        r["cifra_a"] = tabla.get(r["parte_a"])
        r["cifra_b"] = tabla.get(r["parte_b"])
        # VERIFICACION por la vuelta: partir el todo tiene que dar las mismas dos partes
        r["verificacion"] = (len(a), len(b)) in parejas_que_suman(n, saber) or \
            (len(b), len(a)) in parejas_que_suman(n, saber)
        r["las_dos_partes"] = sorted([len(a), len(b)])
    return r
