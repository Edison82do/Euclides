# -*- coding: utf-8 -*-
"""
Euclides - Las primitivas (condiciones de las reglas) y su tabla PRIMITIVAS.

Este archivo es UNA PARTE del motor.  No se importa suelto: lo carga sistema/motor.py,
que junta todas las partes en un solo espacio de nombres (por eso aqui se usan funciones
definidas en otras partes sin importarlas).  Ver sistema/partes/__init__.py.
"""

import os  # noqa: F401
import sys  # noqa: F401

# ---------------------------------------------------------------- primitivas

def p_escena_vacia(escena, criterio=None):
    return len(escena) == 0


def p_varios_distintos(escena, criterio=None):
    """Cierto si en la escena hay dos o mas identificadores distintos."""
    return len({o["id"] for o in escena}) >= 2


def p_un_solo_distinto(escena, criterio=None):
    """Cierto si todas las referencias de la escena son de la misma entidad."""
    return len({o["id"] for o in escena}) <= 1


def p_menos_de_dos_entidades(escena, criterio=None):
    return len({o["id"] for o in escena}) < 2


def p_algun_atributo_indeterminado(escena, criterio=None):
    return len(atributos_indeterminados(escena)) > 0


def p_hay_atributo_compartido_por_todos(escena, criterio=None):
    return len(atributos_compartidos(escena)) > 0


def p_sin_atributo_compartido_por_todos(escena, criterio=None):
    return len(atributos_compartidos(escena)) == 0


def p_alguno_sin_el_atributo(escena, criterio=None):
    return any(criterio["atributo"] not in o["atributos"] for o in escena)


def p_hay_alguno_que_cumple(escena, criterio=None):
    return any(cumple(o, criterio) for o in escena)


def p_el_objeto_no_cumple(escena, criterio=None):
    """Cierto si el objeto declara el atributo pero con OTRO valor."""
    return any(criterio["atributo"] in o["atributos"] and not cumple(o, criterio) for o in escena)


def p_ninguno_cumple(escena, criterio=None):
    return not any(cumple(o, criterio) for o in escena)


# ---------------------------------------------------------------- subitizing (1.0)

def normalizar_patron(texto):
    """
    Convierte lo escrito en una figura de 3 filas x 3 columnas.
    Acepta 'x', 'X', 'o', '*' como elemento, y '.', '-', '_' como hueco.
    Devuelve las tres filas unidas por '/'.
    """
    t = texto.strip().replace(" ", "")
    filas = [f for f in t.split("/") if f != ""]
    if len(filas) != 3:
        raise ValueError(
            "no entiendo esta figura: %r\n"
            "   se escribe con TRES filas separadas por /  ->  x.x/.../x.x\n"
            "   (x = elemento, . = hueco)" % texto)
    normal = []
    for f in filas:
        fila = "".join("x" if c not in ".-_" else "." for c in f.lower())
        if len(fila) != 3:
            raise ValueError(
                "no entiendo esta figura: %r\n"
                "   cada fila tiene que tener TRES huecos  ->  x.x/.../x.x" % texto)
        normal.append(fila)
    return "/".join(normal)


def buscar_patron(patron_normalizado, saber):
    """Devuelve el patron declarado en la tabla, o None si no esta."""
    for p in saber["patrones"]["patrones"]:
        if normalizar_patron(p["patron"]) == patron_normalizado:
            return p
    return None


def p_el_patron_esta_declarado(patron):
    return patron is not None and patron.get("declarado") is not None


def p_el_patron_no_esta_declarado(patron):
    return not p_el_patron_esta_declarado(patron)


# ---------------------------------------------------------------- contar (2.1)

def p_faltan_palabras(escena, cuenta):
    return len(escena) > len(cuenta["secuencia"])


def p_hay_palabras_suficientes(escena, cuenta):
    return len(escena) <= len(cuenta["secuencia"])


def p_menos_palabras_que_objetos(escena, cuenta):
    return len(cuenta["palabras"]) < len(escena)


def p_mas_palabras_que_objetos(escena, cuenta):
    return len(cuenta["palabras"]) > len(escena)


def p_hay_palabra_repetida(cuenta):
    p = cuenta["palabras"]
    return len(set(p)) != len(p)


def p_hay_palabra_desconocida(cuenta):
    return any(p not in cuenta["secuencia"] for p in cuenta["palabras"])


def p_no_es_el_principio(cuenta):
    p = cuenta["palabras"]
    return p != cuenta["secuencia"][:len(p)]


def p_es_el_principio(cuenta):
    p = cuenta["palabras"]
    return p == cuenta["secuencia"][:len(p)]


# ---------------------------------------------------- orden estable de la lista (2.2)

def p_la_palabra_no_esta(palabra, cuenta):
    return palabra not in cuenta["secuencia"]


def p_la_palabra_esta(palabra, cuenta):
    return palabra in cuenta["secuencia"]


def _sitio(palabra, cuenta):
    return cuenta["secuencia"].index(palabra)


def p_es_la_ultima(palabra, cuenta):
    return _sitio(palabra, cuenta) == len(cuenta["secuencia"]) - 1


def p_hay_siguiente(palabra, cuenta):
    return _sitio(palabra, cuenta) < len(cuenta["secuencia"]) - 1


def p_es_la_primera(palabra, cuenta):
    return _sitio(palabra, cuenta) == 0


def p_hay_anterior(palabra, cuenta):
    return _sitio(palabra, cuenta) > 0


# ---------------------------------------------------- cardinalidad (2.4)

def p_la_cantidad_es_la_palabra(escena, palabra, cuenta):
    """La cantidad del conjunto (la ultima palabra del recuento) es esa palabra?"""
    sec = cuenta["secuencia"]
    if not escena or len(escena) > len(sec):
        return False
    return sec[len(escena) - 1] == palabra


def p_la_cantidad_no_es_la_palabra(escena, palabra, cuenta):
    return not p_la_cantidad_es_la_palabra(escena, palabra, cuenta)


def p_faltan_objetos(escena, palabra, cuenta):
    """En el monton hay MENOS objetos que la cantidad pedida?"""
    sec = cuenta["secuencia"]
    if palabra not in sec:
        return False
    return len(escena) < sec.index(palabra) + 1


def p_hay_bastantes(escena, palabra, cuenta):
    """Hay bastantes objetos en el monton para dar esa cantidad?"""
    sec = cuenta["secuencia"]
    if palabra not in sec:
        return False
    return len(escena) >= sec.index(palabra) + 1


# ---------------------------------------------------- recorrido del conteo (2.5)

def p_hay_repetido_en_el_recorrido(escena):
    """En el RECORRIDO se conto el mismo objeto dos veces?  (Aqui NO se fusiona: la repeticion
    es justo el error que buscamos.)"""
    ids = [o["id"] for o in escena]
    return len(set(ids)) != len(ids)


# ---------------------------------------------------- abstraccion (2.6)

def p_alguna_esta_vacia(escena, cuenta):
    return not escena or not (cuenta.get("otra") or [])


def p_alguna_pasa_de_diez(escena, cuenta):
    n = len(cuenta["secuencia"])
    return len(escena) > n or len(cuenta.get("otra") or []) > n


def p_alguna_pasa_de_una_decena(escena, cuenta):
    """Unidad 7.3 (aviso): si alguno de los montones pasa de DIEZ, la suma ya es de DOS CIFRAS y el
    sistema no tiene metodo para eso: el metodo son las COLUMNAS.  Se DICE, no se finge."""
    return len(escena) > 10 or len(cuenta.get("otra") or []) > 10


def p_numero_de_dos_cifras(escena, cuenta):
    """Para sumar NUMEROS (5.3): si alguno pasa de nueve, hacen falta las columnas (7.3)."""
    a, b = cuenta.get("valor_a"), cuenta.get("valor_b")
    if a is None or b is None:
        return False
    return a > 9 or b > 9


def p_misma_cantidad(escena, cuenta):
    otra = cuenta.get("otra") or []
    return bool(escena) and bool(otra) and len(escena) == len(otra)


def p_distinta_cantidad(escena, cuenta):
    otra = cuenta.get("otra") or []
    return bool(escena) and bool(otra) and len(escena) != len(otra)


# ---------------------------------------------------- simbolos / cifras (3.1)

def _tabla(saber):
    """{palabra: cifra} leida del conocimiento 'simbolos'.  No se inventa: se lee."""
    return {d["palabra"]: d["cifra"] for d in saber["simbolos"]["simbolos"]}


def p_la_cifra_no_esta(palabra, cuenta):
    return palabra not in (cuenta.get("simbolos") or {}).values()


def p_la_cifra_esta(palabra, cuenta):
    return palabra in (cuenta.get("simbolos") or {}).values()


def p_hay_simbolo(palabra, cuenta):
    return palabra in (cuenta.get("simbolos") or {})


def p_no_hay_simbolo(palabra, cuenta):
    return palabra not in (cuenta.get("simbolos") or {})


def _palabra_de_la_cantidad(escena, cuenta):
    """La cantidad de la coleccion.  Un conjunto VACIO tiene cantidad CERO (unidad 3.2)."""
    sec = cuenta["secuencia"]
    if not escena:
        return "cero"
    if len(escena) > len(sec):
        return None
    return sec[len(escena) - 1]


def p_hay_cifra_para_la_cantidad(escena, cuenta):
    """Unidad 6.3: la cifra de una cantidad ya vale hasta CIEN (antes solo hasta nueve, porque
    el sistema no sabia escribir cifras de dos digitos)."""
    p = _palabra_de_la_cantidad(escena, cuenta)
    if p is None:
        return False
    if p in (cuenta.get("simbolos") or {}):
        return True
    return p in (cuenta.get("secuencia") or [])


def p_no_hay_cifra_para_la_cantidad(escena, cuenta):
    return not p_hay_cifra_para_la_cantidad(escena, cuenta)


# ---------------------------------------------------- secuencia de numeros (3.3)

def _numeros(cuenta):
    return cuenta.get("numeros") or []


def p_el_numero_no_esta(palabra, cuenta):
    return palabra not in _numeros(cuenta)


def p_el_numero_esta(palabra, cuenta):
    return palabra in _numeros(cuenta)


def _sitio_num(palabra, cuenta):
    """El sitio de la palabra en la secuencia de numeros, o None si no esta.
    Devuelve None en vez de reventar: una condicion debe poder DECIR QUE NO, no romperse."""
    return _numeros(cuenta).index(palabra) if palabra in _numeros(cuenta) else None


def p_es_el_primer_numero(palabra, cuenta):
    return _sitio_num(palabra, cuenta) == 0


def p_es_el_ultimo_numero(palabra, cuenta):
    return _sitio_num(palabra, cuenta) == len(_numeros(cuenta)) - 1


def p_hay_numero_anterior(palabra, cuenta):
    sitio = _sitio_num(palabra, cuenta)
    return sitio is not None and sitio > 0


def p_hay_numero_siguiente(palabra, cuenta):
    sitio = _sitio_num(palabra, cuenta)
    return sitio is not None and sitio < len(_numeros(cuenta)) - 1


def p_no_esta_en_ninguna_lista(palabra, cuenta):
    """Ni en la secuencia de numeros, ni en la lista de contar: no es nada que conozca."""
    return palabra not in _numeros(cuenta) and palabra not in (cuenta.get("secuencia") or [])


# ---------------------------------------------------- comparar cantidades (4.1)

def p_cuenta_no_alcanza(escena, cuenta):
    """Alguna de las dos colecciones pasa de lo que se contar (diez)."""
    n = len(cuenta["secuencia"])
    return len(escena) > n or len(cuenta.get("otra") or []) > n


def p_las_dos_iguales(escena, cuenta):
    """Misma cantidad de cosas.  Vale tambien con dos colecciones VACIAS (cero y cero)."""
    return len(escena) == len(cuenta.get("otra") or [])


def p_la_primera_tiene_mas(escena, cuenta):
    return len(escena) > len(cuenta.get("otra") or [])


def p_la_primera_tiene_menos(escena, cuenta):
    return len(escena) < len(cuenta.get("otra") or [])


# ---------------------------------------------------- relaciones entre numeros (4.2)

def _sitio_cifra(cifra, cuenta):
    """El sitio (el VALOR) de una CIFRA, o None si no es una cifra valida.

    Unidad 6.3: antes esto solo valia para las cifras del 0 al 9, porque el sistema no sabia leer
    cifras de dos digitos.  Ahora vale hasta cien.  Para el 0..9 el valor y el sitio en la lista de
    numeros coinciden, asi que nada de lo anterior cambia."""
    if cifra is None:
        return None
    inv = cuenta.get("tabla_inversa") or {}
    if cifra in inv:
        return _sitio_num(inv[cifra], cuenta)
    t = str(cifra).strip()
    if t.isdigit():
        n = int(t)
        if 0 <= n <= len(cuenta.get("secuencia") or []):
            return n
    return None


def p_cifra_no_conocida(palabra, cuenta):
    """OJO: mira LAS DOS cifras.  Una condicion que habla de dos cosas tiene que mirar las dos;
    si solo mirara la primera, 'comparar_cifras: 3 / tres' se quedaria sin ninguna regla aplicable.

    Unidad 6.3: ahora vale cualquier cifra hasta cien (47, 100), no solo del 0 al 9."""
    return _sitio_cifra(palabra, cuenta) is None or _sitio_cifra(cuenta.get("otra_cifra"), cuenta) is None


def p_cifras_iguales(palabra, cuenta):
    a = _sitio_cifra(palabra, cuenta)
    b = _sitio_cifra(cuenta.get("otra_cifra"), cuenta)
    return a is not None and b is not None and a == b


def p_cifra_mayor(palabra, cuenta):
    """La primera viene DESPUES en la secuencia de numeros -> es la mayor."""
    a = _sitio_cifra(palabra, cuenta)
    b = _sitio_cifra(cuenta.get("otra_cifra"), cuenta)
    return a is not None and b is not None and a > b


def p_cifra_menor(palabra, cuenta):
    a = _sitio_cifra(palabra, cuenta)
    b = _sitio_cifra(cuenta.get("otra_cifra"), cuenta)
    return a is not None and b is not None and a < b


# ------------------------------------------------- componer y descomponer (5.1)

def p_hay_algo(escena, cuenta):
    return len(escena) >= 1


def p_juntar_pasa_de_diez(escena, cuenta):
    n = len(cuenta["secuencia"])
    return contar_todo(escena, cuenta.get("otra") or []) > n     # se juntan y se cuentan


def p_siempre(escena, cuenta):
    """Sirve para la regla final: 'en cualquier otro caso'.  Explicita, para que se vea."""
    return True


# ------------------------------------------------------------ la resta (5.4)

def p_pedido_no_es_numero(escena, cuenta):
    """Lo que se pide quitar no es un numero que el sistema conozca."""
    return cuenta.get("pedido_valor") is None


def p_quiere_quitar_de_mas(escena, cuenta):
    """LA CONDICION DE APLICACION DE LA RESTA: no se puede quitar mas de lo que hay.
    (Un numero negativo es otra cosa, y no esta en este sistema.)"""
    v = cuenta.get("pedido_valor")
    return v is not None and len(escena) < v


def p_no_alcanza_a_contar(escena, cuenta):
    """No hay PALABRA para contar tantos objetos: la lista de contar solo llega hasta su ultima
    palabra.  Antes de contar, hay que poder contar."""
    return len(escena) > len(cuenta.get("secuencia") or [])


def p_no_llega_a_diez(escena, cuenta):
    """Para hacer UNA decena hacen falta DIEZ objetos.  Con menos, no hay monton que hacer (6.2)."""
    return 0 < len(escena) < 10


def p_fuera_de_la_tabla(escena, cuenta):
    """El numero no tiene sitio en la tabla de 100 (6.3)."""
    v = cuenta.get("valor")
    return v is not None and v > 100


def p_el_numero_solo_no_existe(escena, cuenta):
    """Para las ordenes que reciben UN solo numero (sitio, 6.3): no es un numero que conozca."""
    return cuenta.get("valor") is None


def p_decenas_o_unidades_negativas(escena, cuenta):
    """Para juntar decenas y unidades (6.5): ninguna puede ser negativa."""
    d, u = cuenta.get("decenas"), cuenta.get("unidades")
    if d is None or u is None:
        return True
    return d < 0 or u < 0


def p_junta_pasa_de_cien(escena, cuenta):
    """Juntar esas decenas y unidades se pasa de cien (6.5)."""
    d, u = cuenta.get("decenas"), cuenta.get("unidades")
    if d is None or u is None:
        return False
    s = _saber_de(cuenta)
    t = juntar_decenas(d, u, s)
    return t is None or viene_despues(decir(t, s), "cien", s)


def p_alguna_pasa_de_cien(escena, cuenta):
    """Para restar por columnas (7.5): ninguno de los dos puede pasar de cien.
    OJO: mira TAMBIEN el texto, porque una cifra como 150 ES un numero (aunque el sistema todavia
    no sepa leerla): lo que pasa es que se sale de la tabla.  Decir 'no_es_un_numero' ahi seria
    mentira: es un numero, y lo que pasa es que no alcanza."""
    for texto in (cuenta.get("texto_a"), cuenta.get("texto_b")):
        if isinstance(texto, str) and texto.strip().isdigit() and int(texto.strip()) > 100:
            return True
    a, b = cuenta.get("valor_a"), cuenta.get("valor_b")
    return (a is not None and a > 100) or (b is not None and b > 100)


def p_primer_numero_pasa_de_diez(escena, cuenta):
    """Los dedos son los que hay: el PRIMERO no puede pasar de diez (unidad 7.4, la resta)."""
    a = cuenta.get("valor_a")
    return a is not None and a > 10


def _hasta_donde_cuento(saber):
    """Hasta que numero sabe contar el sistema (la ultima palabra de la secuencia)."""
    return saber["secuencia_de_conteo"]["palabras"][-1]


def _palabra_de(n, secuencia):
    """La palabra de una cantidad (0 -> 'cero')."""
    return secuencia[n - 1] if n > 0 else "cero"


# ------------------------------------------- las tres entradas (unidad 5.3)

def _tabla_inversa(saber):
    """{cifra: palabra}, leida del conocimiento (no se calcula)."""
    return {v: k for k, v in _tabla(saber).items()}


def clasificar_nombre(nombre, saber):
    """De que GRUPO es este texto:
         'cifra'    -> es un numero escrito con CIFRAS     (3, 47, 100)
         'palabra'  -> es la palabra de un numero          (tres, cuarenta y siete)
         'cantidad' -> cualquier otra cosa: un OBJETO      (a, b, casa, silla_1)
    Unidad 5.3: los tres grupos estan separados, y las ordenes declaran cual esperan."""
    if nombre in _tabla_inversa(saber):
        return "cifra"
    if nombre in _tabla(saber):
        return "palabra"
    # Una cifra ESCRITA CON DIGITOS es un NUMERO, aunque el sistema todavia no sepa leerla
    # (47, 100: eso es la unidad 6.3).  Lo que NO puede ser nunca es el nombre de un objeto.
    # OJO: 'silla_1' NO es todo digitos, asi que sigue siendo un objeto.
    if nombre.isdigit():
        return "cifra"
    return "cantidad"


class EntradaDelGrupoEquivocado(ValueError):
    """Se ha dado un numero donde van objetos (o al reves).  Unidad 5.3."""


def escena_cantidad(texto, saber):
    """
    Como escena_0_2, pero para las ordenes DE CANTIDADES: COMPRUEBA que los nombres sean de objetos
    y no numeros.  Unidad 5.3: un objeto no se puede llamar como un numero.

    Antes de esto, 'sumar: 3 / 2' tomaba '3' y '2' por dos OBJETOS y contestaba '1 + 1 = 2' con toda
    seguridad: una respuesta creible y falsa.  Ahora lo DICE.  (Lo cazo Carlos.)
    """
    escena = escena_0_2(texto)
    malos = [(o["id"], clasificar_nombre(o["id"], saber)) for o in escena
             if clasificar_nombre(o["id"], saber) != "cantidad"]
    if malos:
        lineas = ["los nombres de objeto y los numeros estan en GRUPOS SEPARADOS:",
                  "  cantidad -> a, b, c    |    cifra -> 3 (o 47)    |    palabra -> tres"]
        for n, g in malos:
            if g == "cifra" and n not in _tabla_inversa(saber):
                # Es una cifra (tiene digitos) pero el sistema TODAVIA NO SABE leerla: 47, 100.
                # Se dice claro en vez de tomarla por un objeto y contestar cualquier cosa.
                lineas.append("  '%s' es un NUMERO escrito con cifras, y YO TODAVIA NO SE LEER cifras"
                              " de mas de un digito" % n)
                lineas.append("     (eso es la unidad 6.3, que aun no esta).  Escríbemelo con"
                              " palabras: 'cuarenta y siete'.")
            elif g == "cifra":
                lineas.append("  '%s' es una CIFRA (el numero %s), y no es el nombre de un objeto." % (n, n))
            else:
                lineas.append("  '%s' es la PALABRA del numero '%s', y no es el nombre de un objeto." % (n, n))
        lineas.append("")
        lineas.append("Esta orden maneja CANTIDADES (cosas).  Si querias el NUMERO, la orden es otra:")
        lineas.append("   siguiente: / anterior: / recitar: / comparar_numeros: / sumar_numeros: /")
        lineas.append("   descomponer_numero: / cifra: / palabra:")
        lineas.append("Y si son objetos de verdad, dales un nombre que no sea un numero:")
        lineas.append("   silla_1, silla_2, silla_3   (no '1', '2', '3')")
        raise EntradaDelGrupoEquivocado("\n".join(lineas))
    return escena


def _cifra_a_numero(texto, saber):
    """Unidad 6.3: si el texto es una CIFRA escrita con digitos (0..100), devuelve el numero.
    Si no lo es, devuelve None.  Antes de la 6.3, una cifra solo valia si era de UN digito."""
    t = texto.strip()
    if t.isdigit():
        n = int(t)
        if 0 <= n <= numero_maximo(saber):              # N.4: hasta el numero maximo (un millon)
            return n
    return None


def nombre_de_numero(texto, saber):
    """
    Para las ordenes DE NUMEROS: acepta la CIFRA o la PALABRA, porque son EL MISMO NUMERO (3.4).
    Devuelve (palabra, venia_en_cifra).

    UNIDAD 6.3: y ahora TAMBIEN lee cifras de DOS digitos.  '47' -> 'cuarenta y siete'.
    Este es el UNICO sitio donde se lee una cifra: si el lector cambia, cambia en todas las
    ordenes a la vez (una sola verdad).
    """
    t = texto.strip().lower()
    inversa = _tabla_inversa(saber)
    if t in inversa:
        return inversa[t], True
    n = _cifra_a_numero(t, saber)
    if n is not None:
        nombre = construir_nombre_hasta_diez_mil(n, saber) or decir(n, saber)    # N.4: y por la estructura
        if nombre:
            return nombre, True
    return t, False


_SABER_DE_LA_SECUENCIA = {}


def _saber_de(cuenta):
    """El 'saber' que necesita el mecanismo.  Si la cuenta no lo trae, se arma con su secuencia."""
    if cuenta.get("_saber"):
        return cuenta["_saber"]
    sec = cuenta.get("secuencia") or []
    clave = id(sec)
    if clave not in _SABER_DE_LA_SECUENCIA:
        _SABER_DE_LA_SECUENCIA[clave] = {"secuencia_de_conteo": {"palabras": list(sec)}}
    return _SABER_DE_LA_SECUENCIA[clave]


def p_la_suma_no_cruza_de_diez(escena, cuenta):
    """Si los dos ya suman diez o menos, no hay nada que cruzar: no hace falta derivar.
    (Mecanico: se cuenta con los dedos y se mira si la palabra viene despues de 'diez'.)"""
    a, b = cuenta.get("valor_a"), cuenta.get("valor_b")
    if a is None or b is None:
        return False
    s = _saber_de(cuenta)
    c = contar_adelante(decir(a, s), decir(b, s), s)
    if c["conclusion"] != "se_puede":
        return False
    return not viene_despues(c["resultado"], "diez", s)


def p_primer_numero_es_de_dos_cifras(escena, cuenta):
    """Para partir y completar diez hacen falta numeros de UNA cifra.  Con dos cifras, columnas."""
    a = cuenta.get("valor_a")
    return a is not None and a > 9


# ------------------------------------------------- los dedos (7.1)

def p_entrada_no_es_numero(escena, cuenta):
    """Alguno de los dos numeros no es un numero que el sistema conozca."""
    return cuenta.get("valor_a") is None or cuenta.get("valor_b") is None


def _cuantos_dedos(saber):
    """Cuantos dedos tiene el sistema.  Es un dato, no un numero escrito en el codigo."""
    return int(saber["reglas_7_1"].get("dedos") or 10)


def p_segundo_pasa_de_diez(escena, cuenta):
    """CONDICION DE APLICACION: no se pueden coger mas dedos de los que hay."""
    v = cuenta.get("valor_b")
    return v is not None and v > _cuantos_dedos(cuenta.get("_saber") or {})


def p_total_pasa_de_cien(escena, cuenta):
    """El total se pasaria de la secuencia de contar."""
    a, b = cuenta.get("valor_a"), cuenta.get("valor_b")
    if a is None or b is None:
        return False
    # Mecanico: se suma por columnas y se mira si el total tiene palabra en la lista.
    return sumar_por_columnas(a, b, _saber_de(cuenta)) is None


# ------------------------------------------------- la centena (6.7) y las columnas de tres (7.6)
# OJO: los techos se escriben con len(secuencia), NUNCA con el numero a mano (carne de errores).

def _techo(cuenta):
    return len(cuenta.get("secuencia") or [])


def p_entrada_no_es_un_numero(escena, cuenta):
    """Para las ordenes de UN numero (6.7): no es un numero que se pueda leer."""
    return cuenta.get("valor") is None


def p_numero_pasa_de_mil(escena, cuenta):
    """El numero se sale de la secuencia de contar (hoy llega a mil)."""
    v = cuenta.get("valor")
    return v is not None and v > _techo(cuenta)


def p_es_de_la_centena(escena, cuenta):
    """El numero pasa de cien (se sale de la tabla de 100) pero no del techo: es de la 6.7."""
    v = cuenta.get("valor")
    return v is not None and 100 < v <= _techo(cuenta)


def p_junta_pasa_del_techo(escena, cuenta):
    """Juntar esas decenas y unidades se sale de la secuencia de contar (6.5 con la 6.7)."""
    d, u = cuenta.get("decenas"), cuenta.get("unidades")
    if d is None or u is None:
        return False
    return juntar_decenas(d, u, _saber_de(cuenta)) is None     # no hay palabra: se sale


def p_alguna_pasa_del_techo(escena, cuenta):
    """Restar por columnas (7.6): ninguno de los dos puede salirse de la secuencia.
    Mira tambien el TEXTO: '1500' es un numero aunque no se pueda leer (no_alcanza, no
    no_es_un_numero)."""
    techo = _techo(cuenta)
    if cuenta.get("_saber"):                       # N.4: las columnas llegan a lo que se sabe escribir (un millon)
        techo = numero_maximo(cuenta["_saber"])
    for texto in (cuenta.get("texto_a"), cuenta.get("texto_b")):
        if isinstance(texto, str) and texto.strip().isdigit() and int(texto.strip()) > techo:
            return True
    a, b = cuenta.get("valor_a"), cuenta.get("valor_b")
    return (a is not None and a > techo) or (b is not None and b > techo)


def p_quiere_quitar_mas_de_lo_que_hay(escena, cuenta):
    """CONDICION DE LA RESTA (5.4), con numeros: no se puede quitar mas de lo que hay."""
    a, b = cuenta.get("valor_a"), cuenta.get("valor_b")
    return a is not None and b is not None and b > a


PRIMITIVAS = {
    "escena_vacia": p_escena_vacia,
    "varios_distintos": p_varios_distintos,
    "un_solo_distinto": p_un_solo_distinto,
    "menos_de_dos_entidades": p_menos_de_dos_entidades,
    "algun_atributo_indeterminado": p_algun_atributo_indeterminado,
    "hay_atributo_compartido_por_todos": p_hay_atributo_compartido_por_todos,
    "sin_atributo_compartido_por_todos": p_sin_atributo_compartido_por_todos,
    "alguno_sin_el_atributo": p_alguno_sin_el_atributo,
    "objeto_sin_el_atributo": p_alguno_sin_el_atributo,
    "el_objeto_cumple": p_hay_alguno_que_cumple,
    "el_objeto_no_cumple": p_el_objeto_no_cumple,
    "hay_alguno_que_cumple": p_hay_alguno_que_cumple,
    "ninguno_cumple": p_ninguno_cumple,
    "el_patron_esta_declarado": p_el_patron_esta_declarado,
    "el_patron_no_esta_declarado": p_el_patron_no_esta_declarado,
    "faltan_palabras": p_faltan_palabras,
    "hay_palabras_suficientes": p_hay_palabras_suficientes,
    "menos_palabras_que_objetos": p_menos_palabras_que_objetos,
    "mas_palabras_que_objetos": p_mas_palabras_que_objetos,
    "hay_palabra_repetida": p_hay_palabra_repetida,
    "hay_palabra_desconocida": p_hay_palabra_desconocida,
    "no_es_el_principio": p_no_es_el_principio,
    "es_el_principio": p_es_el_principio,
    "la_palabra_no_esta": p_la_palabra_no_esta,
    "la_palabra_esta": p_la_palabra_esta,
    "es_la_ultima": p_es_la_ultima,
    "hay_siguiente": p_hay_siguiente,
    "es_la_primera": p_es_la_primera,
    "hay_anterior": p_hay_anterior,
    "la_cantidad_es_la_palabra": p_la_cantidad_es_la_palabra,
    "la_cantidad_no_es_la_palabra": p_la_cantidad_no_es_la_palabra,
    "faltan_objetos": p_faltan_objetos,
    "hay_bastantes": p_hay_bastantes,
    "hay_repetido_en_el_recorrido": p_hay_repetido_en_el_recorrido,
    "alguna_esta_vacia": p_alguna_esta_vacia,
    "alguna_pasa_de_diez": p_alguna_pasa_de_diez,
    "misma_cantidad": p_misma_cantidad,
    "distinta_cantidad": p_distinta_cantidad,
    "la_cifra_no_esta": p_la_cifra_no_esta,
    "la_cifra_esta": p_la_cifra_esta,
    "hay_simbolo": p_hay_simbolo,
    "no_hay_simbolo": p_no_hay_simbolo,
    "hay_cifra_para_la_cantidad": p_hay_cifra_para_la_cantidad,
    "no_hay_cifra_para_la_cantidad": p_no_hay_cifra_para_la_cantidad,
    "el_numero_no_esta": p_el_numero_no_esta,
    "el_numero_esta": p_el_numero_esta,
    "es_el_primer_numero": p_es_el_primer_numero,
    "es_el_ultimo_numero": p_es_el_ultimo_numero,
    "hay_numero_anterior": p_hay_numero_anterior,
    "hay_numero_siguiente": p_hay_numero_siguiente,
    "no_esta_en_ninguna_lista": p_no_esta_en_ninguna_lista,
    "cuenta_no_alcanza": p_cuenta_no_alcanza,
    "las_dos_iguales": p_las_dos_iguales,
    "la_primera_tiene_mas": p_la_primera_tiene_mas,
    "la_primera_tiene_menos": p_la_primera_tiene_menos,
    "cifra_no_conocida": p_cifra_no_conocida,
    "cifras_iguales": p_cifras_iguales,
    "cifra_mayor": p_cifra_mayor,
    "cifra_menor": p_cifra_menor,
    "hay_algo": p_hay_algo,
    "juntar_pasa_de_diez": p_juntar_pasa_de_diez,
    "siempre": p_siempre,
    "pedido_no_es_numero": p_pedido_no_es_numero,
    "quiere_quitar_de_mas": p_quiere_quitar_de_mas,
    "no_alcanza_a_contar": p_no_alcanza_a_contar,
    "entrada_no_es_numero": p_entrada_no_es_numero,
    "segundo_pasa_de_diez": p_segundo_pasa_de_diez,
    "total_pasa_de_cien": p_total_pasa_de_cien,
    "la_suma_no_cruza_de_diez": p_la_suma_no_cruza_de_diez,
    "primer_numero_es_de_dos_cifras": p_primer_numero_es_de_dos_cifras,
    "no_llega_a_diez": p_no_llega_a_diez,
    "no_alcanza_la_secuencia": p_no_alcanza_a_contar,
    "fuera_de_la_tabla": p_fuera_de_la_tabla,
    "el_numero_solo_no_existe": p_el_numero_solo_no_existe,
    "decenas_o_unidades_negativas": p_decenas_o_unidades_negativas,
    "junta_pasa_de_cien": p_junta_pasa_de_cien,
    "alguna_pasa_de_una_decena": p_alguna_pasa_de_una_decena,
    "numero_de_dos_cifras": p_numero_de_dos_cifras,
    "primer_numero_pasa_de_diez": p_primer_numero_pasa_de_diez,
    "pasa_de_cien": p_alguna_pasa_de_cien,
    # 6.7 y 7.6
    "entrada_no_es_un_numero": p_entrada_no_es_un_numero,
    "numero_pasa_de_mil": p_numero_pasa_de_mil,
    "es_de_la_centena": p_es_de_la_centena,
    "junta_pasa_del_techo": p_junta_pasa_del_techo,
    "alguna_pasa_del_techo": p_alguna_pasa_del_techo,
    "quiere_quitar_mas_de_lo_que_hay": p_quiere_quitar_mas_de_lo_que_hay,
}


def evaluar_condicion(texto, escena, criterio=None, patron=None, cuenta=None, palabra=None):
    """
    Evalua 'nombre(...)'.  Los argumentos van NOMBRADOS: escena, criterio, patron, cuenta o palabra,
    para que la regla diga de que esta hablando.
    """
    if not texto.endswith(")"):
        raise ValueError("condicion no reconocida: %r" % texto)
    nombre, _, args = texto[:-1].partition("(")
    nombre = nombre.strip()
    if nombre not in PRIMITIVAS:
        raise ValueError("primitiva desconocida: %r" % nombre)
    valores = []
    for a in [x.strip() for x in args.split(",") if x.strip()]:
        if a == "escena":
            valores.append(escena)
        elif a == "criterio":
            valores.append(criterio)
        elif a == "patron":
            valores.append(patron)
        elif a == "cuenta":
            valores.append(cuenta)
        elif a == "palabra":
            valores.append(palabra)
        else:
            raise ValueError("argumento desconocido en la condicion: %r" % a)
    return PRIMITIVAS[nombre](*valores), nombre
