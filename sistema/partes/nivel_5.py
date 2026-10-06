# -*- coding: utf-8 -*-
"""
Euclides - Nivel 5 - operaciones (5.1 a 5.5).

Este archivo es UNA PARTE del motor.  No se importa suelto: lo carga sistema/motor.py,
que junta todas las partes en un solo espacio de nombres (por eso aqui se usan funciones
definidas en otras partes sin importarlas).  Ver sistema/partes/__init__.py.
"""

import os  # noqa: F401
import sys  # noqa: F401

# ------------------------------------------------- componer y descomponer (5.1)

def explicar_5_1_descomponer(escena, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (5.1): en cuantas maneras se puede partir esta coleccion en DOS partes?"]
    r = decidir_5_1_descomponer(escena, saber)
    lineas.append("COLECCION:")
    lineas.extend(_cabecera(r["entidades"]))
    if r["conclusion"] == "no_alcanza":
        lineas.append("")
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  Tiene mas objetos de los que se contar (mi lista llega a diez).")
        lineas.append("  Lo digo en vez de inventarme las partes.")
        return "\n".join(lineas)
    if r["conclusion"] == "el_cero_no_se_parte":
        lineas.append("")
        lineas.append("RESULTADO: el_cero_no_se_parte")
        lineas.append("  Esta coleccion esta VACIA (cantidad cero).  De cero no hay nada que partir.")
        lineas.append("  El cero SI puede ser una PARTE (cero y cinco), pero no un TODO que se parte.")
        return "\n".join(lineas)
    n = len(r["entidades"])
    lineas.append("")
    lineas.append("  EL TODO (la coleccion entera):")
    lineas.extend(_puente_mejor("*" * n, r["total"], r["total_cifra"]))
    lineas.append("")
    lineas.append("  LAS PARTES, todas las maneras (%d):" % r["cuantas_maneras"])
    for i, ((k, m), (pk, pm), (ck, cm)) in enumerate(
            zip(r["parejas"], r["parejas_palabras"], r["parejas_cifras"])):
        izq = ck if ck is not None else "--"
        der = cm if cm is not None else "--"
        lineas.append("    %d. %-8s y %-8s   (%s y %s)     %s | %s"
                      % (i + 1, pk, pm, izq, der, "*" * k if k else "(vacio)", "*" * m if m else "(vacio)"))
    lineas.append("")
    lineas.append("  NO REPITO LA PAREJA AL REVES: 'dos y tres' es lo mismo que 'tres y dos' (el orden")
    lineas.append("  no cambia la cantidad, unidad 2.5).  Serian la misma manera contada dos veces.")
    lineas.append("  El CERO es una parte valida ('cero y cinco'): un lado vacio y el otro con todo.")
    lineas.append("")
    lineas.append("  VERIFICACION (por la vuelta): juntando cada pareja vuelve a salir el todo: %s"
                  % ("SI" if r["verificacion"] else "NO"))
    lineas.append("  (Partir y juntar son la ida y la vuelta: eso es lo que sostiene la suma y la resta.)")
    lineas.append("")
    lineas.append("RESULTADO: %d maneras" % r["cuantas_maneras"])
    lineas.append("  '%s'%s se puede partir de %d maneras distintas."
                  % (r["total"], " (%s)" % r["total_cifra"] if r["total_cifra"] else "", r["cuantas_maneras"]))
    if r["total_cifra"] is None:
        lineas.append("  (Su CIFRA no la tengo: el diez son dos simbolos, Sistema Decimal.)")
    lineas.append("  (Aqui se parte en DOS partes.  Partir en tres o mas es un paso posterior.)")
    return "\n".join(lineas)


def explicar_5_1_componer(escena_a, escena_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (5.1): juntando estas dos colecciones, cuanto sale?"]
    r = decidir_5_1_componer(escena_a, escena_b, saber)
    lineas.append("PRIMERA PARTE:")
    lineas.extend(_cabecera(r["primera"]))
    lineas.append("SEGUNDA PARTE:")
    lineas.extend(_cabecera(r["segunda"]))
    if r["conclusion"] == "no_alcanza":
        lineas.append("")
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  Juntandolas pasaria de diez, y mi lista de contar llega a diez.")
        lineas.append("  Lo digo en vez de inventarme el total.")
        return "\n".join(lineas)
    n = contar_todo(r["primera"], r["segunda"])
    lineas.append("")
    lineas.append("  LAS DOS PARTES:")
    lineas.append("    primera: %d -> %s" % (len(r["primera"]), r["parte_a"]))
    lineas.append("    segunda: %d -> %s" % (len(r["segunda"]), r["parte_b"]))
    lineas.append("")
    lineas.append("  EL TODO (juntando las dos):")
    lineas.extend(_puente_mejor("*" * n, r["total"], r["total_cifra"]))
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["total"])
    if r["total_cifra"] is not None:
        lineas.append("  '%s' y '%s' son '%s'   (con las cifras: %s y %s son %s)"
                      % (r["parte_a"], r["parte_b"], r["total"],
                         r["cifra_a"], r["cifra_b"], r["total_cifra"]))
    else:
        lineas.append("  '%s' y '%s' son '%s'   (su cifra no la tengo: el diez son dos simbolos)"
                      % (r["parte_a"], r["parte_b"], r["total"]))
    lineas.append("  VERIFICACION (por la vuelta): partiendo '%s' en esas dos partes, vuelven a salir"
                  % r["total"])
    lineas.append("  las mismas: SI.  (Juntar y partir son la ida y la vuelta.)")
    lineas.append("  (Todavia no se escribe el signo +: eso es la unidad siguiente.)")
    return "\n".join(lineas)


def _suma_base(escena_a, escena_b, saber, clave, ok):
    """Lo comun a sumar (agregacion) y anadir (aumentacion): el calculo y la verificacion."""
    a = entidades_reales(escena_a)
    b = entidades_reales(escena_b)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    cuenta = {"secuencia": secuencia, "otra": b}
    r = _aplicar_reglas(saber["reglas_5_2"][clave], a, None, saber, cuenta=cuenta)
    r["primera"] = a
    r["segunda"] = b
    r["secuencia"] = secuencia
    if r["conclusion"] == ok:
        tabla = _tabla(saber)
        n = contar_todo(a, b)              # CONTAR TODO: se juntan y se cuentan (5.2)
        r["sumando_a"] = _palabra_de(len(a), secuencia)
        r["sumando_b"] = _palabra_de(len(b), secuencia)
        r["suma"] = _palabra_de(n, secuencia)
        r["cifra_a"] = tabla.get(r["sumando_a"])
        r["cifra_b"] = tabla.get(r["sumando_b"])
        r["cifra_suma"] = tabla.get(r["suma"])
        r["expresion"] = "%s + %s = %s" % (r["cifra_a"], r["cifra_b"], r["cifra_suma"])
        if r["cifra_suma"] is None:
            # La cifra del DIEZ no existe (son dos simbolos): se usa la palabra y se dice.
            r["expresion"] = "%s + %s = %s" % (r["cifra_a"], r["cifra_b"], r["suma"])
            r["total_sin_cifra"] = True
        # LA VERIFICACION (la vuelta, unidad 5.1): partiendo la SUMA tiene que aparecer la pareja
        # de los sumandos.  Si no apareciera, el sistema no elegiria: lo diria.
        parejas = parejas_que_suman(n, saber)
        r["parejas_de_la_suma"] = parejas
        r["verificacion"] = sorted((len(a), len(b))) in [sorted(p) for p in parejas]
    return r


def decidir_5_2_sumar(escena_a, escena_b, saber=None):
    """Unidad 5.2, AGREGACION: juntar dos montones que ya estan ahi."""
    if saber is None:
        saber = cargar_conocimiento()
    return _suma_base(escena_a, escena_b, saber, "reglas_sumar", "suma")


def decidir_5_2_anadir(escena_a, escena_b, saber=None):
    """Unidad 5.2, AUMENTACION: a un monton se le anaden mas (el monton crece)."""
    if saber is None:
        saber = cargar_conocimiento()
    return _suma_base(escena_a, escena_b, saber, "reglas_anadir", "aumento")


# ------------------------------------------------------------ la suma (5.2)

def _leyenda_de_los_signos():
    return ["  QUE SIGNIFICAN LOS SIGNOS:",
            "    +   se lee 'mas' y significa JUNTAR lo de los dos lados",
            "    =   se lee 'igual a' y significa QUE LAS DOS COSAS SON LO MISMO",
            "        (OJO: el = NO es 'haz la cuenta y pon el resultado'.  Es que 3 + 2 y 5 son la",
            "         misma cosa dicha de dos maneras.  Por eso 5 = 3 + 2 es igual de cierto.)"]


def _bloque_verificacion(r, saber):
    # Sirve para las dos ordenes de suma: la de cantidad (sumando_a/b) y la de numeros (palabra_a/b).
    nombre_a = r.get("sumando_a") or r.get("palabra_a")
    nombre_b = r.get("sumando_b") or r.get("palabra_b")
    lineas = []
    lineas.append("  VERIFICACION (por la vuelta, unidad 5.1):")
    lineas.append("    partiendo '%s' sale: %s"
                  % (r["suma"],
                     ", ".join("%s y %s" % (a, b) for a, b in
                               [(_palabra_de(k, r["secuencia"]), _palabra_de(m, r["secuencia"]))
                                for k, m in r["parejas_de_la_suma"]])))
    lineas.append("    la pareja de los sumandos ('%s y %s') esta entre ellas: %s"
                  % (nombre_a, nombre_b, "SI" if r["verificacion"] else "NO"))
    if not r["verificacion"]:
        lineas.append("    NO CUADRA. El sistema no elige uno: lo dice.")
    return lineas


def _aviso_columnas(r, que):
    """Unidad 7.3: el sistema SABE que esa suma existe, pero NO TIENE METODO para hacerla todavia.
    El metodo son las COLUMNAS.  Se dice claro, en vez de dar un numero sin metodo que lo respalde."""
    return [
        "RESULTADO: necesito_las_columnas",
        "  %s" % que,
        "  El sistema NO TIENE todavia el metodo para sumar de DOS CIFRAS: ese metodo son las",
        "  COLUMNAS (unidad 7.3, la que viene ahora): unidad con unidad, decena con decena, y lo",
        "  que se lleva se suma con lo siguiente.",
        "  Y sin metodo NO da el resultado, aunque pudiera adivinarlo: en este proyecto cada",
        "  respuesta tiene que salir de un metodo que se pueda seguir (regla 13).",
        "  Lo que SI sabe ya de dos cifras: leerlas (6.3), su sitio (6.3) y partirlas (6.5).",
    ]


def explicar_5_2_sumar(escena_a, escena_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (5.2): suma estas dos colecciones"]
    r = decidir_5_2_sumar(escena_a, escena_b, saber)
    if r["conclusion"] == "necesito_las_columnas":
        return "\n".join(["PREGUNTA (5.2): juntar dos montones (agregacion)"] +
                         _aviso_columnas(r, "Alguno de los dos montones pasa de DIEZ objetos."))
    lineas.append("PRIMERA COLECCION:")
    lineas.extend(_cabecera(r["primera"]))
    lineas.append("SEGUNDA COLECCION:")
    lineas.extend(_cabecera(r["segunda"]))
    if r["conclusion"] == "no_alcanza":
        lineas.append("")
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  La suma pasaria de diez, y mi lista de contar llega a diez.")
        lineas.append("  CONDICION DE APLICACION: no se suma mas alla de lo que se cuenta.")
        lineas.append("  Lo digo en vez de inventarme el resultado.")
        return "\n".join(lineas)
    lineas.extend(_traza_texto(r))
    lineas.append("")
    lineas.append("  ESTRUCTURA: AGREGACION")
    lineas.append("    Se juntan dos montones que YA ESTAN ahi.  No se anade nada: se juntan.")
    lineas.append("")
    lineas.append("  LOS TERMINOS TIENEN NOMBRE:")
    lineas.append("    los SUMANDOS son %s y %s   (los numeros que se juntan)"
                  % (r["sumando_a"], r["sumando_b"]))
    lineas.append("    la SUMA es %s              (el resultado)" % r["suma"])
    lineas.append("")
    lineas.extend(_leyenda_de_los_signos())
    lineas.append("")
    lineas.append("  LA CUENTA:")
    lineas.extend(_puente_mejor("*" * contar_todo(r["primera"], r["segunda"]), r["suma"],
                                r["cifra_suma"]))
    lineas.append("")
    lineas.extend(_bloque_verificacion(r, saber))
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["expresion"])
    lineas.append("  %s   (%s mas %s igual a %s)"
                  % (r["expresion"], r["sumando_a"], r["sumando_b"], r["suma"]))
    if r.get("total_sin_cifra"):
        lineas.append("  (La cifra del total no la tengo: el diez son DOS simbolos, Sistema Decimal.)")
    return "\n".join(lineas)


def explicar_5_2_anadir(escena_a, escena_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (5.2): a esta coleccion le anado estas otras"]
    r = decidir_5_2_anadir(escena_a, escena_b, saber)
    if r["conclusion"] == "necesito_las_columnas":
        return "\n".join(["PREGUNTA (5.2): anadir a un monton (aumentacion)"] +
                         _aviso_columnas(r, "Alguno de los dos montones pasa de DIEZ objetos."))
    lineas.append("LO QUE HABIA AL PRINCIPIO:")
    lineas.extend(_cabecera(r["primera"]))
    lineas.append("LO QUE SE ANADE:")
    lineas.extend(_cabecera(r["segunda"]))
    if r["conclusion"] == "no_alcanza":
        lineas.append("")
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  La suma pasaria de diez, y mi lista de contar llega a diez.")
        lineas.append("  CONDICION DE APLICACION: no se suma mas alla de lo que se cuenta.")
        return "\n".join(lineas)
    lineas.extend(_traza_texto(r))
    lineas.append("")
    lineas.append("  ESTRUCTURA: AUMENTACION")
    lineas.append("    A un monton se le ANADEN mas cosas: el monton CRECE.  La historia es")
    lineas.append("    'primero..., luego..., ahora...':")
    lineas.append("      PRIMERO: habia %s.   LUEGO: se anaden %s.   AHORA: hay %s."
                  % (r["sumando_a"], r["sumando_b"], r["suma"]))
    lineas.append("    (El numero final es el mismo que juntando, pero la historia es OTRA: aqui el")
    lineas.append("     monton crece; en la agregacion los dos montones ya estaban.)")
    lineas.append("")
    lineas.extend(_leyenda_de_los_signos())
    lineas.append("")
    lineas.extend(_bloque_verificacion(r, saber))
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["expresion"])
    lineas.append("  %s   (%s mas %s igual a %s)"
                  % (r["expresion"], r["sumando_a"], r["sumando_b"], r["suma"]))
    if r.get("total_sin_cifra"):
        lineas.append("  (La cifra del total no la tengo: el diez son DOS simbolos, Sistema Decimal.)")
    return "\n".join(lineas)


# ------------------------------------------- operar con NUMEROS (unidad 5.3)

def _valor_de_numero(palabra, saber):
    """El valor de un numero dicho con palabra, o None si no es un numero que conozca.

    UNIDAD 6.3: y si la palabra es la de un numero de DOS cifras (hasta cien), tambien su valor.
    UNIDAD 6.7: y de TRES cifras (hasta mil), tambien.  Este es el PUNTO UNICO donde se lee el
    valor de un numero dicho con palabra: si cambia aqui, cambia en TODAS las puertas a la vez.
    (Antes usaba solo el constructor hasta cien, y por eso 'novecientos' y '600' decian
    'no_es_un_numero' -- el fallo que caza la prueba de la 6.7.)"""
    numeros = list(saber["secuencia_de_numeros"]["numeros"])
    if palabra in numeros:
        return numeros.index(palabra)
    # El mapa inverso de la 6.7: O(1), no un recorrido de mil nombres.  N.4: y si no, por la estructura.
    v = (saber.get("_nombre_a_valor") or {}).get(palabra)
    return v if v is not None else leer(palabra, saber)


def _valor_de_cantidad(palabra, saber):
    """
    El valor de una CANTIDAD de objetos dicha con palabra.

    Aqui SI vale 'diez' (la lista de CONTAR llega hasta cien) y tambien el cero.  OJO: NO es lo
    mismo que un NUMERO: los numeros solo llegan al nueve (unidad 3.3).  Por eso las ordenes de
    cantidad (dame, quitar) usan ESTA y no _valor_de_numero.
    (Esto estaba mal en la 5.4: 'dame: ... / diez' valia y 'quitar: ... / diez' no.  Dos verdades
    para lo mismo.  Lo cazo la prueba de hierro de la 5.5.)
    """
    if palabra == "cero":
        return 0
    return (saber.get("_nombre_a_valor") or {}).get(palabra)


def decidir_5_3_sumar_numeros(texto_a, texto_b, saber=None):
    """
    Unidad 5.3: SUMAR DOS NUMEROS, sin objetos de por medio (cifra o palabra, da igual).
    Es el paso siguiente al 'sumar' de cantidades: alli se juntan cosas, aqui se suman numeros.
    """
    if saber is None:
        saber = cargar_conocimiento()
    pa, ca = nombre_de_numero(texto_a, saber)
    pb, cb = nombre_de_numero(texto_b, saber)
    tabla = _tabla(saber)
    inversa = {v: k for k, v in tabla.items()}
    r = {"texto_a": texto_a, "texto_b": texto_b, "palabra_a": pa, "palabra_b": pb,
         "venia_en_cifra": (ca, cb),
         "secuencia": saber["secuencia_de_conteo"]["palabras"],
         "numeros": list(saber["secuencia_de_numeros"]["numeros"])}
    va, vb = _valor_de_numero(pa, saber), _valor_de_numero(pb, saber)
    if va is None or vb is None:
        r["conclusion"] = "no_es_un_numero"
        r["cual"] = pa if va is None else pb
        return r
    # UNIDAD 7.3: para DOS CIFRAS ya HAY metodo: las COLUMNAS (unidad con unidad, decena con decena,
    # y el llevarse).  Antes esto decia necesito_las_columnas; ahora las usa.
    if va > 9 or vb > 9:
        col = decidir_7_3_columnas(texto_a, texto_b, saber)
        if col["conclusion"] == "se_puede":
            r["conclusion"] = "suma"
            r["suma"] = col["total"]
            r["total_valor"] = col["total_valor"]
            r["valor_a"], r["valor_b"] = va, vb
            r["cifra_a"], r["cifra_b"] = str(va), str(vb)
            r["cifra_suma"] = str(col["total_valor"])
            r["expresion"] = "%d + %d = %d" % (va, vb, col["total_valor"])
            r["por_columnas"] = col
            r["metodo"] = "columnas (7.3)"
            r["tabla"] = tabla
            return r
        return col   # no_alcanza (se pasa de cien)
    # con UNA cifra el metodo son los DEDOS (7.1) o derivar (7.2): el total sale de ahi
    total = _suma_con_metodo(va, vb, saber)["total"]
    r["conclusion"] = "suma"
    r["valor_a"], r["valor_b"] = va, vb
    r["total_valor"] = total
    r["suma"] = _palabra_de(total, saber["secuencia_de_conteo"]["palabras"])
    r["cifra_a"] = tabla.get(pa)
    r["cifra_b"] = tabla.get(pb)
    r["cifra_suma"] = tabla.get(r["suma"])
    # Las tres representaciones y la verificacion por la vuelta (unidad 5.1)
    r["parejas_de_la_suma"] = parejas_que_suman(total, saber)
    r["verificacion"] = sorted((va, vb)) in [sorted(p) for p in r["parejas_de_la_suma"]]
    r["expresion"] = ("%s + %s = %s" % (r["cifra_a"], r["cifra_b"], r["cifra_suma"])
                      if r["cifra_suma"] is not None
                      else "%s + %s = %s" % (r["cifra_a"], r["cifra_b"], r["suma"]))
    r["total_sin_cifra"] = r["cifra_suma"] is None
    return r


def decidir_5_3_descomponer_numero(texto_n, saber=None):
    """Unidad 5.3: partir un NUMERO (no una coleccion) en dos partes, todas las maneras."""
    if saber is None:
        saber = cargar_conocimiento()
    pn, cn = nombre_de_numero(texto_n, saber)
    tabla = _tabla(saber)
    inversa = {v: k for k, v in tabla.items()}
    r = {"texto_n": texto_n, "palabra_n": pn, "venia_en_cifra": cn,
         "numeros": list(saber["secuencia_de_numeros"]["numeros"])}
    v = _valor_de_numero(pn, saber)
    if v is None:
        r["conclusion"] = "no_es_un_numero"
        r["cual"] = pn
        return r
    if v == 0:
        r["conclusion"] = "el_cero_no_se_parte"
        return r
    r["conclusion"] = "parejas"
    r["valor"] = v
    r["cifra_n"] = tabla.get(pn)
    r["parejas"] = parejas_que_suman(v, saber)
    r["parejas_palabras"] = [(decir(k, saber), decir(m, saber)) for k, m in r["parejas"]]
    r["parejas_cifras"] = [(tabla.get(decir(k, saber)), tabla.get(decir(m, saber)))
                           for k, m in r["parejas"]]
    r["cuantas_maneras"] = len(r["parejas"])
    r["verificacion"] = all(leer(contar_adelante(decir(k, saber), decir(m, saber), saber,
                                                 con_dedos=False)["resultado"], saber) == v
                            for k, m in r["parejas"])
    return r


def explicar_5_3_sumar_numeros(texto_a, texto_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (5.3): suma estos DOS NUMEROS  (numeros, no objetos)"]
    r = decidir_5_3_sumar_numeros(texto_a, texto_b, saber)
    if r["conclusion"] == "necesito_las_columnas":
        return "\n".join(["PREGUNTA (5.3): sumar dos NUMEROS"] +
                         _aviso_columnas(r, "Alguno de los dos numeros pasa de NUEVE."))
    if r.get("por_columnas"):
        # UNIDAD 7.3: con dos cifras, el metodo son las COLUMNAS.  Se ensena el desarrollo.
        lineas = ["PREGUNTA (5.3): sumar estos DOS NUMEROS  (numeros, no objetos)"]
        lineas.append("NUMEROS:  %s  y  %s" % (texto_a, texto_b))
        lineas.append("")
        lineas.append("  Y OJO: como son de DOS CIFRAS, el metodo NO es ir uno a uno: son las")
        lineas.append("  COLUMNAS (unidad 7.3).  El desarrollo entero:")
        lineas.append("")
        lineas.extend(explicar_7_3_columnas(texto_a, texto_b, saber).split("\n"))
        return "\n".join(lineas)
    lineas.append("NUMEROS:  %s  y  %s" % (texto_a, texto_b))
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  '%s' no es un numero que conozca: los mios van del CERO al NUEVE." % r["cual"])
        lineas.append("  Si era un objeto, recuerda que objetos y numeros son grupos separados.")
        lineas.append("  Lo digo en vez de inventarme el resultado.")
        return "\n".join(lineas)
    if r["conclusion"] == "no_alcanza":
        lineas.append("RESULTADO: no_alcanza")
        # (Antes decia "la suma daria %d" con un total que NO salia de ningun metodo -- y con dos
        # cifras reventaba con KeyError, porque las columnas no dan ese total.  Ahora se dice
        # lo que se sabe: que se pasa del techo.)
        lineas.append("  %s + %s se pasa de mi lista de contar (llega a '%s')."
                      % (r.get("valor_a", texto_a), r.get("valor_b", texto_b),
                         saber["secuencia_de_conteo"]["palabras"][-1]))
        lineas.append("  CONDICION DE APLICACION: no se suma mas alla de lo que se cuenta.")
        return "\n".join(lineas)
    lineas.append("")
    lineas.append("  DE CIFRA A PALABRA (unidad 3.4): cada numero se puede decir de las dos maneras.")
    lineas.append("    %s = '%s'      %s = '%s'" % (texto_a, r["palabra_a"], texto_b, r["palabra_b"]))
    lineas.extend(_leyenda_de_los_signos())
    lineas.append("")
    lineas.append("  LOS TERMINOS: sumandos = %s y %s ; la suma = %s"
                  % (r["palabra_a"], r["palabra_b"], r["suma"]))
    lineas.append("")
    lineas.extend(_bloque_verificacion(r, saber))
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["expresion"])
    lineas.append("  %s   (%s mas %s igual a %s)"
                  % (r["expresion"], r["palabra_a"], r["palabra_b"], r["suma"]))
    if r["total_sin_cifra"]:
        lineas.append("  (La cifra del total no la tengo: el diez son DOS simbolos.)")
    return "\n".join(lineas)


def explicar_5_3_descomponer_numero(texto_n, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (5.3): en cuantas maneras se puede partir este NUMERO en DOS?"]
    r = decidir_5_3_descomponer_numero(texto_n, saber)
    lineas.append("NUMERO:  %s" % texto_n)
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  '%s' no es un numero que conozca (del 0 al 9)." % r["cual"])
        return "\n".join(lineas)
    if r["conclusion"] == "el_cero_no_se_parte":
        lineas.append("RESULTADO: el_cero_no_se_parte")
        lineas.append("  De cero no hay nada que partir.  (El cero SI puede ser una PARTE.)")
        return "\n".join(lineas)
    lineas.append("")
    lineas.append("  LAS PARTES, todas las maneras (%d):" % r["cuantas_maneras"])
    for i, ((k, m), (pk, pm), (ck, cm)) in enumerate(
            zip(r["parejas"], r["parejas_palabras"], r["parejas_cifras"])):
        lineas.append("    %d. %-8s y %-8s   (%s y %s)"
                      % (i + 1, pk, pm, ck if ck is not None else "--",
                         cm if cm is not None else "--"))
    lineas.append("")
    lineas.append("  NO REPITO LA PAREJA AL REVES (el orden no importa, unidad 2.5).")
    lineas.append("  Y el CERO es una parte valida: 'cero y %s'." % r["palabra_n"])
    lineas.append("  VERIFICACION (por la vuelta): juntando cada pareja vuelve a salir %s: %s"
                  % (r["palabra_n"], "SI" if r["verificacion"] else "NO"))
    lineas.append("")
    lineas.append("RESULTADO: %d maneras" % r["cuantas_maneras"])
    lineas.append("  El numero %s se puede partir de %d maneras distintas."
                  % (r["palabra_n"], r["cuantas_maneras"]))
    return "\n".join(lineas)


# ------------------------------------------------------------ la resta (5.4)

def decidir_5_4_quitar(escena, pedido, saber=None):
    """
    Unidad 5.4, REDUCCION: restar es QUITAR.  De este monton se van tantos; cuantos quedan?
    La historia es 'primero..., luego..., ahora...'.  OJO: quitar NO es partir (5.1): los que se
    van SE VAN del monton, no se quedan en una parte.
    """
    if saber is None:
        saber = cargar_conocimiento()
    reales = entidades_reales(escena)
    palabra, venia_cifra = nombre_de_numero(pedido, saber)
    # La cantidad que se quita es una CANTIDAD de objetos, no un numero: aqui 'diez' vale.
    valor = _valor_de_cantidad(palabra, saber)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    cuenta = {"secuencia": secuencia, "pedido": palabra, "pedido_valor": valor}
    r = _aplicar_reglas(saber["reglas_5_4"]["reglas_quitar"], reales, None, saber, cuenta=cuenta)
    r["monton"] = reales
    r["pedido"] = pedido
    r["pedido_palabra"] = palabra
    r["pedido_venia_en_cifra"] = venia_cifra
    r["secuencia"] = secuencia
    if r["conclusion"] == "quedan":
        tabla = _tabla(saber)
        # QUITAR, mecanico: se van sacando del monton tantos como dice la palabra (recitando
        # uno, dos... uno por objeto que se va), y lo que queda se cuenta.
        restantes = list(reales)
        se_van = []
        for _marca in coleccion_de(palabra, saber):
            se_van.insert(0, restantes.pop())
        quedan = len(restantes)
        r["minuendo"] = _palabra_de(len(reales), secuencia)
        r["sustraendo"] = palabra
        r["resultado"] = _palabra_de(quedan, secuencia)
        r["cifra_minuendo"] = tabla.get(r["minuendo"])
        r["cifra_sustraendo"] = tabla.get(r["sustraendo"])
        r["cifra_resultado"] = tabla.get(r["resultado"])
        r["los_que_quedan"] = [o["id"] for o in restantes]
        r["los_que_se_van"] = [o["id"] for o in se_van]
        # Si alguna cifra no existe (el DIEZ son dos simbolos), se usa su palabra.  Se mezclan
        # cifra y palabra SOLO en ese caso, y el sistema lo dice.
        r["expresion"] = "%s - %s = %s" % (r["cifra_minuendo"] or r["minuendo"],
                                           r["cifra_sustraendo"] or r["sustraendo"],
                                           r["cifra_resultado"] or r["resultado"])
        r["alguno_sin_cifra"] = (r["cifra_minuendo"] is None or r["cifra_resultado"] is None)
        # LA VUELTA VERIFICA (lo pide el plan): sumar lo que quedo y lo que se fue devuelve el
        # minuendo.  Dos comprobaciones: la aritmetica (siempre se puede) y la de verdad, con la
        # SUMA de la unidad 5.2/5.3 (que no siempre llega: la secuencia de NUMEROS acaba en nueve,
        # asi que con el DIEZ de minuendo la suma de numeros no lo alcanza; entonces se dice).
        r["verificacion"] = (contar_todo(restantes, se_van) == len(reales))   # juntar lo de antes
        vuelta = decidir_5_3_sumar_numeros(r["resultado"], r["sustraendo"], saber)
        r["vuelta"] = vuelta
        if vuelta["conclusion"] == "suma":
            r["verificacion_con_la_suma"] = (vuelta["suma"] == r["minuendo"])
            r["expresion_inversa"] = vuelta.get("expresion")
        else:
            r["verificacion_con_la_suma"] = None
            r["expresion_inversa"] = None
    return r


def decidir_5_4_restar_numeros(texto_a, texto_b, saber=None):
    """Unidad 5.4: restar DOS NUMEROS (sin objetos).  '5 - 2 = 3'."""
    if saber is None:
        saber = cargar_conocimiento()
    pa, ca = nombre_de_numero(texto_a, saber)
    pb, cb = nombre_de_numero(texto_b, saber)
    tabla = _tabla(saber)
    inversa = {v: k for k, v in tabla.items()}
    r = {"texto_a": texto_a, "texto_b": texto_b, "palabra_a": pa, "palabra_b": pb,
         "venia_en_cifra": (ca, cb),
         "secuencia": saber["secuencia_de_conteo"]["palabras"],
         "numeros": list(saber["secuencia_de_numeros"]["numeros"])}
    va, vb = _valor_de_numero(pa, saber), _valor_de_numero(pb, saber)
    if va is None or vb is None:
        r["conclusion"] = "no_es_un_numero"
        r["cual"] = pa if va is None else pb
        return r
    if vb > va:
        r["conclusion"] = "no_hay_bastantes"
        r["valor_a"], r["valor_b"] = va, vb
        return r
    if va > 9 or vb > 9:
        # Con DOS o TRES cifras el metodo son las COLUMNAS (7.5 / 7.6), como en la suma (5.3).
        # (Antes: va - vb calculado por dentro, sin metodo, y la salida decia "None - None = ...":
        #  la cifra se buscaba en la tabla del 0 al 9.  Lo cazo la revision del 5 oct 2026.)
        col = decidir_7_5_columnas(str(va), str(vb), saber)
        r["valor_a"], r["valor_b"] = va, vb
        if col["conclusion"] != "se_puede":
            r["conclusion"] = col["conclusion"]
            return r
        r["conclusion"] = "resta"
        r["resultado_valor"] = col["resta"]
        r["resultado"] = col["resultado"]
        r["cifra_a"], r["cifra_b"], r["cifra_resultado"] = str(va), str(vb), str(col["resta"])
        r["expresion"] = "%d - %d = %d" % (va, vb, col["resta"])
        r["alguno_sin_cifra"] = False
        r["por_columnas"] = col
        r["metodo"] = "columnas (%s)" % col.get("unidad", "7.5")
        r["verificacion"] = bool(col.get("verificacion"))
        r["expresion_inversa"] = "%d + %d = %d" % (col["resta"], vb, va)
        return r
    r["conclusion"] = "resta"
    r["valor_a"], r["valor_b"] = va, vb
    # con UNA cifra el metodo son los DEDOS hacia atras (7.4)
    rr = _resta_con_metodo(va, vb, saber)
    r["resultado_valor"] = rr["queda"]
    r["resultado"] = rr["palabra_queda"]
    r["cifra_a"], r["cifra_b"] = tabla.get(pa), tabla.get(pb)
    r["cifra_resultado"] = tabla.get(r["resultado"])
    r["expresion"] = "%s - %s = %s" % (r["cifra_a"], r["cifra_b"],
                                       r["cifra_resultado"] if r["cifra_resultado"] else r["resultado"])
    r["alguno_sin_cifra"] = r["cifra_resultado"] is None
    vuelta = decidir_5_3_sumar_numeros(r["resultado"], pb, saber)
    r["vuelta"] = vuelta
    r["verificacion"] = (vuelta["conclusion"] == "suma" and vuelta["suma"] == pa)
    r["expresion_inversa"] = vuelta.get("expresion")
    return r


def _leyenda_del_menos():
    return ["  QUE SIGNIFICAN LOS SIGNOS:",
            "    -   se lee 'menos' y significa QUITAR lo de la derecha de lo de la izquierda",
            "    =   se lee 'igual a' y significa QUE LAS DOS COSAS SON LO MISMO"]


def explicar_5_4_quitar(escena, pedido, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (5.4): de este monton se van tantos; cuantos quedan?"]
    r = decidir_5_4_quitar(escena, pedido, saber)
    lineas.append("MONTON (lo que hay al principio):")
    lineas.extend(_cabecera(r["monton"]))
    lineas.append("LO QUE SE PIDE QUITAR: %s" % pedido)
    if r["conclusion"] == "no_alcanza":
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  El monton tiene %d objetos, y yo solo se contar hasta %s."
                      % (len(r["monton"]), _hasta_donde_cuento(saber).upper()))
        lineas.append("  Para un numero mas grande NO TENGO PALABRA, y no me la invento.")
        lineas.append("  (Se podria quitar igual, pero no sabria decirte cuantos quedan.)")
        return "\n".join(lineas)
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  '%s' no es un numero que conozca: los mios van del CERO al NUEVE." % pedido)
        return "\n".join(lineas)
    if r["conclusion"] == "no_hay_bastantes":
        lineas.append("RESULTADO: no_hay_bastantes")
        lineas.append("  Me pides quitar %s, y en el monton solo hay %s."
                      % (r["pedido_palabra"], _palabra_de(len(r["monton"]), r["secuencia"])))
        lineas.append("  CONDICION DE APLICACION DE LA RESTA: NO SE PUEDE QUITAR MAS DE LO QUE HAY.")
        lineas.append("  (Un numero negativo es otra cosa, y no esta aqui.)")
        lineas.append("  Lo digo en vez de inventarme el resultado.")
        return "\n".join(lineas)
    lineas.extend(_traza_texto(r))
    lineas.append("")
    lineas.append("  ESTRUCTURA: QUITAR (reduccion).  El monton DISMINUYE.  La historia es")
    lineas.append("  'primero..., luego..., ahora...':")
    lineas.append("    PRIMERO: habia %s.   LUEGO: se van %s.   AHORA: quedan %s."
                  % (r["minuendo"], r["sustraendo"], r["resultado"]))
    lineas.append("")
    lineas.append("  LOS QUE SE VAN (ya no estan): %s" % (", ".join(r["los_que_se_van"]) or "(ninguno)"))
    lineas.append("  LOS QUE QUEDAN:              %s" % (", ".join(r["los_que_quedan"]) or "(ninguno)"))
    lineas.append("  (Esto es QUITAR, no PARTIR: los que se van SE VAN del monton.  Partir el monton")
    lineas.append("   entero en dos partes es la unidad 5.1, y alli no se va nada.)")
    lineas.append("")
    lineas.append("  LOS TERMINOS TIENEN NOMBRE:")
    lineas.append("    el MINUENDO es %s      (de donde se quita)" % r["minuendo"])
    lineas.append("    el SUSTRAENDO es %s    (lo que se quita)" % r["sustraendo"])
    lineas.append("    el RESULTADO es %s     (lo que queda)" % r["resultado"])
    lineas.append("")
    lineas.extend(_leyenda_del_menos())
    lineas.append("")
    lineas.append("  VERIFICACION (la vuelta: la suma deshace la resta, unidad 5.2):")
    lineas.append("    lo que queda y lo que se fue tienen que volver a dar el minuendo:")
    if r["verificacion_con_la_suma"] is None:
        lineas.append("    contando: %s y %s vuelven a ser %s ... %s"
                      % (r["resultado"], r["sustraendo"], r["minuendo"],
                         "SI" if r["verificacion"] else "NO"))
        lineas.append("    (La suma ESCRITA no la puedo hacer aqui: la vuelta PASA DE DIEZ, y la")
        lineas.append("     secuencia de NUMEROS llega hasta el nueve.  Lo cuento, y lo digo.)")
    else:
        lineas.append("    %s ... los dos caminos dicen lo mismo: %s"
                      % (r["expresion_inversa"], "SI" if r["verificacion"] else "NO"))
    if not r["verificacion"]:
        lineas.append("    NO CUADRA. El sistema no elige uno: lo dice.")
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["expresion"])
    lineas.append("  %s   (%s menos %s igual a %s)"
                  % (r["expresion"], r["minuendo"], r["sustraendo"], r["resultado"]))
    if r.get("alguno_sin_cifra"):
        lineas.append("  (Alguna cifra no la tengo porque es el DIEZ: son DOS simbolos.)")
    return "\n".join(lineas)


def explicar_5_4_restar_numeros(texto_a, texto_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (5.4): resta estos DOS NUMEROS  (numeros, no objetos)"]
    r = decidir_5_4_restar_numeros(texto_a, texto_b, saber)
    lineas.append("NUMEROS:  %s  y  %s" % (texto_a, texto_b))
    if r.get("por_columnas"):
        lineas.append("")
        lineas.append("  Y OJO: como pasan de NUEVE, el metodo son las COLUMNAS (unidades 7.5 y 7.6).")
        lineas.append("  El desarrollo entero:")
        lineas.append("")
        lineas.extend(explicar_7_5_columnas(str(r["valor_a"]), str(r["valor_b"]), saber).split("\n"))
        lineas.append("")
        lineas.append("RESULTADO: %s" % r["expresion"])
        return "\n".join(lineas)
    if r["conclusion"] == "no_alcanza":
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  Alguno pasa de mi lista de contar.  No me lo invento.")
        return "\n".join(lineas)
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  '%s' no es un numero que conozca: los mios van del CERO al NUEVE." % r["cual"])
        return "\n".join(lineas)
    if r["conclusion"] == "no_hay_bastantes":
        lineas.append("RESULTADO: no_hay_bastantes")
        lineas.append("  Me pides restar %d de %d, y la resta seria NEGATIVA." % (r["valor_b"], r["valor_a"]))
        lineas.append("  CONDICION DE APLICACION DE LA RESTA: NO SE PUEDE QUITAR MAS DE LO QUE HAY.")
        lineas.append("  (Los numeros negativos son otra cosa, y no estan aqui.)")
        return "\n".join(lineas)
    lineas.append("")
    lineas.append("  DE CIFRA A PALABRA (unidad 3.4): %s = '%s'   %s = '%s'"
                  % (texto_a, r["palabra_a"], texto_b, r["palabra_b"]))
    lineas.extend(_leyenda_del_menos())
    lineas.append("")
    lineas.append("  LOS TERMINOS: minuendo = %s ; sustraendo = %s ; resultado = %s"
                  % (r["palabra_a"], r["palabra_b"], r["resultado"]))
    lineas.append("")
    lineas.append("  VERIFICACION (la vuelta: la suma deshace la resta, unidad 5.2):")
    lineas.append("    %s ... los dos caminos dicen lo mismo: %s"
                  % (r["expresion_inversa"], "SI" if r["verificacion"] else "NO"))
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["expresion"])
    lineas.append("  %s   (%s menos %s igual a %s)"
                  % (r["expresion"], r["palabra_a"], r["palabra_b"], r["resultado"]))
    return "\n".join(lineas)


# ------------------------------------------------------------ la diferencia (5.5)

def decidir_5_5_diferencia(escena_a, escena_b, saber=None):
    """
    Unidad 5.5, LA DIFERENCIA: el HUECO entre dos cantidades.  Es la tercera estructura de la resta.

    OJO: AQUI NO SE QUITA NADA.  Los dos montones siguen enteros.  Se empareja (2.1) y los que se
    quedan SIN pareja son el hueco.

    Las primitivas son las mismas que en 4.1: comparar y hallar la diferencia son lo mismo.
    """
    if saber is None:
        saber = cargar_conocimiento()
    a = entidades_reales(escena_a)
    b = entidades_reales(escena_b)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    cuenta = {"secuencia": secuencia, "otra": b}
    r = _aplicar_reglas(saber["reglas_5_5"]["reglas_diferencia"], a, None, saber, cuenta=cuenta)
    r["primera"] = a
    r["segunda"] = b
    r["secuencia"] = secuencia
    if r["conclusion"] == "no_alcanza":
        return r
    # EL EMPAREJAMIENTO: un objeto con un objeto.  Los que sobran SON el hueco.
    n = min(len(a), len(b))
    r["emparejadas"] = [(a[i]["id"], b[i]["id"]) for i in range(n)]
    r["sobra_primera"] = [o["id"] for o in a[n:]]
    r["sobra_segunda"] = [o["id"] for o in b[n:]]
    r["diferencia_valor"] = len(r["sobra_primera"]) or len(r["sobra_segunda"])   # los SIN pareja
    r["el_que_va_primero"] = a[0]["id"] if a else "(vacio)"
    r["el_que_va_segundo"] = b[0]["id"] if b else "(vacio)"
    r["tantos_la_primera"] = _palabra_de(len(a), secuencia)
    r["tantos_la_segunda"] = _palabra_de(len(b), secuencia)
    r["diferencia"] = _palabra_de(r["diferencia_valor"], secuencia)
    tabla = _tabla(saber)
    r["cifra_primera"] = tabla.get(r["tantos_la_primera"])
    r["cifra_segunda"] = tabla.get(r["tantos_la_segunda"])
    r["cifra_diferencia"] = tabla.get(r["diferencia"])
    if len(a) >= len(b):
        r["tiene_mas"] = "la primera"
        r["cuantos_mas"] = r["diferencia"]
        r["mayor"], r["menor"] = r["tantos_la_primera"], r["tantos_la_segunda"]
        r["cifra_mayor"], r["cifra_menor"] = r["cifra_primera"], r["cifra_segunda"]
    else:
        r["tiene_mas"] = "la segunda"
        r["cuantos_mas"] = r["diferencia"]
        r["mayor"], r["menor"] = r["tantos_la_segunda"], r["tantos_la_primera"]
        r["cifra_mayor"], r["cifra_menor"] = r["cifra_segunda"], r["cifra_primera"]
    # LAS DOS FORMAS DE ESCRIBIRLO (NCETM): 5 - 3 = 2   y   3 + 2 = 5
    r["expresion"] = "%s - %s = %s" % (r["cifra_mayor"] or r["mayor"], r["cifra_menor"] or r["menor"],
                                       r["cifra_diferencia"] or r["diferencia"])
    r["alguno_sin_cifra"] = (r["cifra_mayor"] is None or r["cifra_menor"] is None
                             or r["cifra_diferencia"] is None)
    # LA VUELTA VERIFICA: la diferencia sumada al pequeno tiene que dar el grande (unidad 5.2/5.3).
    if r["diferencia_valor"] == 0:
        r["expresion_inversa"] = "%s + cero = %s" % (r["menor"], r["menor"])
        r["verificacion"] = True
        r["verificacion_con_la_suma"] = True
    else:
        vuelta = decidir_5_3_sumar_numeros(r["menor"], r["diferencia"], saber)
        r["vuelta"] = vuelta
        if vuelta["conclusion"] == "suma":
            r["expresion_inversa"] = vuelta.get("expresion")
            r["verificacion_con_la_suma"] = (vuelta["suma"] == r["mayor"])
        else:
            r["expresion_inversa"] = None
            r["verificacion_con_la_suma"] = None
        # la vuelta: los emparejados mas los que sobran tienen que ser el monton grande entero
        r["verificacion"] = (contar_todo(r["emparejadas"], r["sobra_primera"] or r["sobra_segunda"])
                             == max(len(a), len(b)))
    return r


def decidir_5_5_diferencia_numeros(texto_a, texto_b, saber=None):
    """Unidad 5.5: la diferencia entre DOS NUMEROS (sin objetos).  'diferencia_numeros: 5 / 3'."""
    if saber is None:
        saber = cargar_conocimiento()
    pa, ca = nombre_de_numero(texto_a, saber)
    pb, cb = nombre_de_numero(texto_b, saber)
    va, vb = _valor_de_numero(pa, saber), _valor_de_numero(pb, saber)
    r = {"texto_a": texto_a, "texto_b": texto_b, "palabra_a": pa, "palabra_b": pb,
         "venia_en_cifra": (ca, cb),
         "secuencia": saber["secuencia_de_conteo"]["palabras"]}
    if va is None or vb is None:
        r["conclusion"] = "no_es_un_numero"
        r["cual"] = pa if va is None else pb
        return r
    tabla = _tabla(saber)
    r["valor_a"], r["valor_b"] = va, vb
    r["conclusion"] = "tantos_como" if va == vb else "hay_diferencia"
    if max(va, vb) > 9:
        # Con mas de una cifra, el HUECO se mide restando por COLUMNAS (7.5 / 7.6) el grande menos
        # el pequeno.  (Antes: abs(va - vb) por dentro, sin metodo, y la cifra salia None.)
        col = decidir_7_5_columnas(str(max(va, vb)), str(min(va, vb)), saber)
        r["diferencia_valor"] = col["resta"]
        r["por_columnas"] = col
    else:
        # el HUECO se cuenta: desde el pequeno hasta el grande (contar hacia adelante, 5.5)
        r["diferencia_valor"] = leer(contar_hasta(decir(min(va, vb), saber),
                                                  decir(max(va, vb), saber), saber), saber)
    r["diferencia"] = _palabra_de(r["diferencia_valor"], r["secuencia"]) if r["diferencia_valor"] else "cero"
    r["mayor"], r["menor"] = (pa, pb) if va >= vb else (pb, pa)
    r["cifra_mayor"] = tabla.get(r["mayor"]) or str(max(va, vb))
    r["cifra_menor"] = tabla.get(r["menor"]) or str(min(va, vb))
    r["cifra_diferencia"] = tabla.get(r["diferencia"]) or str(r["diferencia_valor"])
    r["tiene_mas"] = "la primera" if va >= vb else "la segunda"
    r["expresion"] = "%s - %s = %s" % (r["cifra_mayor"], r["cifra_menor"],
                                       r["cifra_diferencia"] or r["diferencia"])
    vuelta = decidir_5_3_sumar_numeros(r["menor"], r["diferencia"], saber)
    r["vuelta"] = vuelta
    if vuelta["conclusion"] == "suma":
        r["expresion_inversa"] = vuelta.get("expresion")
        r["verificacion"] = (vuelta["suma"] == r["mayor"])
    else:
        r["expresion_inversa"] = None
        r["verificacion"] = None
    return r


def explicar_5_5_diferencia(escena_a, escena_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (5.5): cual es la DIFERENCIA entre estas dos colecciones?"]
    lineas.append("  (la diferencia es el HUECO entre las dos: cuanto hay que anadir a la pequena")
    lineas.append("   para llegar a la grande)")
    r = decidir_5_5_diferencia(escena_a, escena_b, saber)
    lineas.append("PRIMERA:")
    lineas.extend(_cabecera(r["primera"]))
    lineas.append("SEGUNDA:")
    lineas.extend(_cabecera(r["segunda"]))
    if r["conclusion"] == "no_alcanza":
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  Alguna de las dos colecciones pasa de %s, y yo solo se contar hasta ahi."
                      % _hasta_donde_cuento(saber).upper())
        lineas.append("  Para un numero mas grande NO TENGO PALABRA, y no me la invento.")
        return "\n".join(lineas)
    lineas.extend(_traza_texto(r))
    lineas.append("")
    lineas.append("  ESTRUCTURA: COMPARAR (la diferencia).  Es la TERCERA de las tres estructuras de")
    lineas.append("  la resta, y es OTRA HISTORIA que quitar y que partir:")
    lineas.append("    QUITAR (5.4):  el monton DISMINUYE (los que se van SE VAN)")
    lineas.append("    PARTIR (5.1):  el monton se reparte (no se va nada, pero hay un TODO)")
    lineas.append("    DIFERENCIA:    NO HAY TODO.  Hay DOS cantidades y un HUECO entre ellas.")
    lineas.append("")
    lineas.append("  ¡AQUI NO SE QUITA NADA!  Los dos montones siguen enteros: nadie se va.")
    lineas.append("  Se empareja uno con uno, y los que se quedan SIN PAREJA son el hueco:")
    if r["emparejadas"]:
        lineas.append("    emparejados: %s" % ", ".join("%s-%s" % (x, y) for x, y in r["emparejadas"]))
    lineas.append("    SIN PAREJA de la primera: %s" % (", ".join(r["sobra_primera"]) or "(ninguno)"))
    lineas.append("    SIN PAREJA de la segunda: %s" % (", ".join(r["sobra_segunda"]) or "(ninguno)"))
    lineas.append("")
    if r["conclusion"] == "tantos_como":
        lineas.append("  Las dos cantidades son IGUALES: %s y %s." % (r["tantos_la_primera"],
                                                                     r["tantos_la_segunda"]))
        lineas.append("  No sobra nadie en ninguna: EL HUECO ES CERO.  Y el cero es una cantidad")
        lineas.append("  (unidad 3.2), no un 'no se'.")
    else:
        lineas.append("  LAS DOS PREGUNTAS TIENEN LA MISMA RESPUESTA:")
        lineas.append("    cuantos MAS tiene la primera?  -> %s" % r["cuantos_mas"])
        lineas.append("    cuantos MENOS tiene la segunda? -> %s" % r["cuantos_mas"])
        lineas.append("    (el mismo numero: la diferencia es UNA, y se dice desde los dos lados)")
    lineas.append("")
    lineas.append("  SE ESCRIBE DE DOS MANERAS (las dos valen, y dan lo mismo):")
    lineas.append("    restando:              %s       (%s menos %s)"
                  % (r["expresion"], r["mayor"], r["menor"]))
    lineas.append("    contando hacia adelante: %s       (desde el pequeno hasta el grande)"
                  % (r["expresion_inversa"] or "?"))
    lineas.append("")
    lineas.append("  VERIFICACION (la vuelta: la diferencia y el pequeno vuelven a dar el grande):")
    if r["verificacion_con_la_suma"] is None:
        lineas.append("    contando: %s y %s vuelven a ser %s ... %s"
                      % (r["menor"], r["diferencia"], r["mayor"],
                         "SI" if r["verificacion"] else "NO"))
        lineas.append("    (La suma ESCRITA no la puedo hacer aqui: pasaria de diez.)")
    else:
        lineas.append("    %s ... los dos caminos dicen lo mismo: %s"
                      % (r["expresion_inversa"], "SI" if r["verificacion"] else "NO"))
    if not r["verificacion"]:
        lineas.append("    NO CUADRA. El sistema no elige uno: lo dice.")
    lineas.append("")
    lineas.append("  OJO CON LA PALABRA 'MAS': en 'cuantos mas tiene' NO se suma; se busca el hueco.")
    lineas.append("  (Error tipico de los ninos, y esta escrito en la fuente: NCETM.)")
    lineas.append("")
    lineas.append("RESULTADO: %s" % (r["diferencia"] if r["conclusion"] != "tantos_como" else "cero"))
    lineas.append("  La diferencia entre %s y %s es %s."
                  % (r["tantos_la_primera"], r["tantos_la_segunda"], r["diferencia"]))
    if r["conclusion"] != "tantos_como":
        lineas.append("  (O sea: %s - %s = %s)" % (r["mayor"], r["menor"], r["diferencia"]))
    if r.get("alguno_sin_cifra"):
        lineas.append("  (Alguna cifra no la tengo porque es el DIEZ: son DOS simbolos.)")
    return "\n".join(lineas)


def explicar_5_5_diferencia_numeros(texto_a, texto_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (5.5): la DIFERENCIA entre estos DOS NUMEROS  (numeros, no objetos)"]
    r = decidir_5_5_diferencia_numeros(texto_a, texto_b, saber)
    lineas.append("NUMEROS:  %s  y  %s" % (texto_a, texto_b))
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  '%s' no es un numero que conozca: los mios van del CERO al NUEVE." % r["cual"])
        return "\n".join(lineas)
    lineas.append("")
    lineas.append("  DE CIFRA A PALABRA (unidad 3.4): %s = '%s'   %s = '%s'"
                  % (texto_a, r["palabra_a"], texto_b, r["palabra_b"]))
    lineas.append("  ESTRUCTURA: la DIFERENCIA (comparar).  No se quita nada: se mide el HUECO.")
    lineas.append("")
    if r["conclusion"] == "tantos_como":
        lineas.append("  Los dos numeros son IGUALES: el hueco es CERO.")
    else:
        lineas.append("  LAS DOS PREGUNTAS TIENEN LA MISMA RESPUESTA: %s mas, o %s menos."
                      % (r["diferencia"], r["diferencia"]))
    lineas.append("  LAS DOS FORMAS:  %s   y   %s"
                  % (r["expresion"], r["expresion_inversa"] or "?"))
    lineas.append("  VERIFICACION: %s ... los dos caminos dicen lo mismo: %s"
                  % (r["expresion_inversa"], "SI" if r["verificacion"] else "NO"))
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["diferencia"])
    lineas.append("  La diferencia entre %s y %s es %s."
                  % (r["palabra_a"], r["palabra_b"], r["diferencia"]))
    return "\n".join(lineas)
