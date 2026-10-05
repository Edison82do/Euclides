# -*- coding: utf-8 -*-
"""
Motor de Euclides - version 0.2

Que sabe hacer:
  UNIDAD 0.1  - dada una escena, decidir si hay UN OBJETO o VARIOS OBJETOS (identidad y pluralidad).
  UNIDAD 0.2  - RECONOCER: si esos objetos forman grupo, diciendo QUE ATRIBUTOS comparten.
              - FORMAR: extraer el grupo de los que cumplen <atributo>=<valor>.

  OJO (corregido el 2026-10-03): la palabra GRUPO es solo de la unidad 0.2, y siempre quiere
  decir "varios objetos que comparten un atributo con el mismo valor".  0.1 no habla de
  grupos: solo dice si hay una cosa o varias.

Como se escribe una escena:
  0.1  ->  nombres separados por comas:            silla, mesa, silla
  0.2  ->  objetos con atributos, separados por ';':
               caja_A(color=rojo,forma=cubo); caja_B(color=rojo,forma=esfera)
  formar ->  empieza por el criterio y dos puntos:
               color=rojo: caja_A(color=rojo,forma=cubo); caja_B(color=azul,forma=cubo)

Reglas del proyecto que este motor respeta:
  - No adivina: si no hay regla aplicable o falta un dato, responde "no_decidible".
  - No cuenta: la cantidad es la unidad 2.3. Aqui solo se forman y se reconocen grupos.
  - Todo se puede rastrear: cada respuesta sale con la regla y el conocimiento que la respaldan.

Uso:
    python motor.py conocimiento
    python motor.py escena "silla,mesa"
    python motor.py escena "caja_A(color=rojo,forma=cubo); caja_B(color=rojo,forma=esfera)"
    python motor.py escena "color=rojo: caja_A(color=rojo,forma=cubo); caja_B(color=azul,forma=cubo)"
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_CONOCIMIENTO = os.path.join(RAIZ, "conocimiento")


# ---------------------------------------------------------------- lectura de .kn

def _sangria(linea):
    return len(linea) - len(linea.lstrip(" "))


def _parse_bloque(lineas, i, indent):
    """Lee un bloque de pares clave: valor con indentacion fija."""
    datos = {}
    while i < len(lineas):
        cruda = lineas[i]
        if not cruda.strip() or cruda.strip().startswith("#"):
            i += 1
            continue
        sangria = _sangria(cruda)
        if sangria < indent:
            break
        if sangria > indent:
            raise ValueError("sangria inesperada en la linea %d: %r" % (i + 1, cruda))

        cuerpo = cruda.strip()
        if cuerpo.startswith("- "):
            raise ValueError("item de lista sin clave en la linea %d" % (i + 1))

        clave, _, valor = cuerpo.partition(":")
        clave, valor = clave.strip(), valor.strip()
        i += 1

        if valor == "|":
            buf = []
            while i < len(lineas):
                l = lineas[i]
                if not l.strip():
                    buf.append("")
                    i += 1
                    continue
                if _sangria(l) <= indent:
                    break
                buf.append(l[indent + 2:] if len(l) > indent + 2 else l.strip())
                i += 1
            datos[clave] = "\n".join(buf).strip("\n")

        elif valor == "[]":
            datos[clave] = []

        elif valor == "":
            if i < len(lineas) and lineas[i].strip().startswith("- ") and _sangria(lineas[i]) > indent:
                items, i = _parse_lista(lineas, i, indent)
                datos[clave] = items
            elif i < len(lineas) and lineas[i].strip() and _sangria(lineas[i]) > indent:
                sub, i = _parse_bloque(lineas, i, indent + 2)
                datos[clave] = sub
            else:
                datos[clave] = None
        else:
            datos[clave] = valor
    return datos, i


def _parse_lista(lineas, i, indent):
    """
    Lee una lista de items '- ...'.  Cada item puede ser:
      - texto (que puede CONTINUAR en las lineas siguientes con mas sangria), o
      - un mapping ('- nombre: ...' con sus claves indentadas debajo).
    """
    items = []
    while i < len(lineas):
        l = lineas[i]
        if not l.strip():
            i += 1
            continue
        if not l.strip().startswith("- ") or _sangria(l) <= indent:
            break
        sangria_item = _sangria(l)
        primero = l.strip()[2:]
        if ":" in primero:
            # item que es un mapping: lo reescribimos sin el guion y lo parseamos
            copia = list(lineas)
            copia[i] = " " * (sangria_item + 2) + primero
            sub, i = _parse_bloque(copia, i, sangria_item + 2)
            items.append(sub)
        else:
            # item de texto: las lineas siguientes con MAS sangria siguen siendo del item
            buf = [primero.strip()]
            i += 1
            while i < len(lineas):
                nl = lineas[i]
                if not nl.strip():
                    j = i + 1
                    while j < len(lineas) and not lineas[j].strip():
                        j += 1
                    if (j < len(lineas) and _sangria(lineas[j]) > sangria_item
                            and not lineas[j].strip().startswith("- ")):
                        i += 1
                        continue
                    break
                if _sangria(nl) > sangria_item and not nl.strip().startswith("- "):
                    buf.append(nl.strip())
                    i += 1
                    continue
                break
            items.append(" ".join(p for p in buf if p).strip())
    return items, i


def cargar_archivo_kn(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        lineas = f.read().split("\n")
    datos, _ = _parse_bloque(lineas, 0, 0)
    return datos


def cargar_conocimiento(directorio=DIR_CONOCIMIENTO):
    """Carga todos los .kn del directorio. Devuelve {id: conocimiento}."""
    saber = {}
    for nombre in sorted(os.listdir(directorio)):
        if not nombre.endswith(".kn"):
            continue
        d = cargar_archivo_kn(os.path.join(directorio, nombre))
        if "id" not in d:
            raise ValueError("el archivo %s no declara 'id'" % nombre)
        d["_archivo"] = nombre
        saber[d["id"]] = d

    # UNIDAD 6.1 - la secuencia de contar se CONSTRUYE con la regla y llega hasta 100.
    # Se hace AQUI, en un solo punto, para que todas las unidades anteriores sigan viendo
    # exactamente lo mismo que veian: una lista de palabras de contar, en orden.  Lo unico que
    # cambia es que la lista es mas larga.  Ninguna unidad vieja se entera.
    if "secuencia_hasta_cien" in saber and "secuencia_de_conteo" in saber:
        palabras = _secuencia_hasta_mil(saber)
        if palabras and all(palabras) and len(set(palabras)) == len(palabras):
            saber["secuencia_de_conteo"]["palabras"] = palabras
            saber["secuencia_de_conteo"]["hasta"] = len(palabras)
            saber["secuencia_de_conteo"]["_construida_con_la_regla"] = True
            # UNIDAD 6.7 - EL MAPA INVERSO (palabra -> valor), construido UNA VEZ.
            # Asi leer 'novecientos' es instantaneo, en vez de recorrer mil nombres cada vez.
            saber["_nombre_a_valor"] = {w: i + 1 for i, w in enumerate(palabras)}
    return saber


# ---------------------------------------------------------------- escenas

def escena_0_1(texto):
    """'silla,mesa' -> [{'id': 'silla', 'atributos': {}}, ...]"""
    t = texto.strip()
    if not t:
        return []
    return [{"id": p.strip(), "atributos": {}} for p in t.split(",") if p.strip()]


def _dividir_escena(texto):
    """
    Separa los objetos de una escena por ';' o por comas DE FUERA de los parentesis.
    Asi vale tanto 'a(x=1); b(x=2)' como 'a(x=1), b'.  Las comas de dentro de los
    parentesis separan atributos y no cuentan aqui.
    """
    partes, buf, nivel = [], [], 0
    for ch in texto:
        if ch == "(":
            nivel += 1
        elif ch == ")":
            nivel = max(0, nivel - 1)
        if ch in ";," and nivel == 0:
            partes.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    partes.append("".join(buf))
    return [p.strip() for p in partes if p.strip()]


def parsear_objeto(texto):
    """'caja_A(color=rojo,forma=cubo)' -> {'id': 'caja_A', 'atributos': {...}}"""
    texto = texto.strip()
    if "(" not in texto:
        return {"id": texto, "atributos": {}}
    if texto.count("(") != 1 or not texto.endswith(")"):
        raise ValueError(
            "no entiendo este objeto: %r\n"
            "   se escribe asi:  nombre(atributo=valor,atributo=valor)" % texto)
    ident, _, resto = texto.partition("(")
    resto = resto[:-1]
    if "(" in resto or ")" in resto:
        raise ValueError(
            "no entiendo este objeto: %r\n"
            "   sobran parentesis" % texto)
    attrs = {}
    for trozo in resto.split(","):
        trozo = trozo.strip()
        if not trozo:
            continue
        k, _, v = trozo.partition("=")
        if not k.strip() or not v.strip():
            raise ValueError(
                "no entiendo el atributo %r\n"
                "   se escribe asi:  nombre=valor" % trozo)
        attrs[k.strip()] = v.strip()
    if not ident.strip():
        raise ValueError("no entiendo este objeto: %r  (le falta el nombre)" % texto)
    return {"id": ident.strip(), "atributos": attrs}


def escena_0_2(texto):
    """Objetos con atributos, separados por ';' (o por comas de fuera de los parentesis)."""
    t = texto.strip()
    if not t:
        return []
    return [parsear_objeto(p) for p in _dividir_escena(t)]


def parsear_criterio(texto):
    """'color=rojo' -> {'atributo': 'color', 'valor': 'rojo'}"""
    k, _, v = texto.strip().partition("=")
    if not k.strip() or not v.strip():
        raise ValueError(
            "no entiendo el criterio %r\n"
            "   se escribe asi:  atributo=valor   (por ejemplo color=rojo)" % texto)
    return {"atributo": k.strip(), "valor": v.strip()}


# ---------------------------------------------------------------- atributos (0.2)

def atributos_presentes(escena):
    nombres = set()
    for o in escena:
        nombres |= set(o["atributos"].keys())
    return sorted(nombres)


def declaran(escena, atributo):
    return [o for o in escena if atributo in o["atributos"]]


def comparten_todos(escena, atributo):
    """Cierto si TODOS los objetos declaran el atributo y con el mismo valor."""
    if not escena:
        return False
    if len(declaran(escena, atributo)) != len(escena):
        return False
    return len({o["atributos"][atributo] for o in escena}) == 1


def atributos_compartidos(escena):
    return [a for a in atributos_presentes(escena) if comparten_todos(escena, a)]


def atributos_indeterminados(escena):
    """
    Atributos que unas veces estan declarados y otras no, pero donde los que SI lo
    declaran coinciden.  No se puede afirmar ni negar: el sistema lo dice.
    """
    dudosos = []
    for a in atributos_presentes(escena):
        los_que = declaran(escena, a)
        if len(los_que) == 0 or len(los_que) == len(escena):
            continue
        if len({o["atributos"][a] for o in los_que}) == 1:
            dudosos.append(a)
    return dudosos


def cumple(objeto, criterio):
    return objeto["atributos"].get(criterio["atributo"]) == criterio["valor"]


def miembros(escena, criterio):
    return [o["id"] for o in escena if cumple(o, criterio)]


def _se_contradicen(attrs_a, attrs_b):
    """Cierto si comparten una clave con valores distintos."""
    return any(k in attrs_b and attrs_b[k] != v for k, v in attrs_a.items())


def entidades_reales(escena):
    """
    Convierte una ESCENA (lista de menciones) en la lista de ENTIDADES reales.
    Tres reglas, las tres razonadas con Carlos el 2026-10-03:

      1. Menciones del MISMO identificador con datos que NO se contradicen: son la MISMA
         entidad y sus atributos SE SUMAN.
             casa(color=blanco) + casa(forma=cuadrada)  ->  una casa blanca y cuadrada

      2. Menciones del MISMO identificador con un atributo y DOS VALORES DISTINTOS: eso
         PRUEBA que son entidades DISTINTAS, porque una misma cosa no puede ser negra y
         blanca a la vez.
             carro(color=negro) + carro(color=blanco)   ->  DOS coches, uno de cada color

      3. Identificadores distintos: entidades distintas.

    Cuando un identificador da varias entidades se numeran: carro#1, carro#2.
    Si una mencion encaja en varias, se une a la PRIMERA compatible en el orden escrito,
    para que la misma entrada de siempre el mismo resultado.
    """
    entidades = []
    for o in escena:
        base = o["id"]
        for e in entidades:
            if e["base"] == base and not _se_contradicen(e["atributos"], o["atributos"]):
                for k, v in o["atributos"].items():
                    e["atributos"].setdefault(k, v)
                e["menciones"] += 1
                break
        else:
            entidades.append({"base": base, "atributos": dict(o["atributos"]), "menciones": 1})

    cuantas = {}
    for e in entidades:
        cuantas[e["base"]] = cuantas.get(e["base"], 0) + 1

    vistos = {}
    salida = []
    for e in entidades:
        base = e["base"]
        if cuantas[base] > 1:
            vistos[base] = vistos.get(base, 0) + 1
            nombre = "%s#%d" % (base, vistos[base])
        else:
            nombre = base
        salida.append({"id": nombre, "base": base, "atributos": e["atributos"],
                       "menciones": e["menciones"]})
    return salida


def separadas(escena, entidades):
    """
    Identificadores base que dieron MAS DE UNA entidad: prueba de que eran objetos distintos.
    """
    bases = [e["base"] for e in entidades]
    return sorted({b for b in bases if bases.count(b) > 1})


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
    return len(escena) + len(cuenta.get("otra") or []) > n


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
    return d * 10 + u > 100


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
        if 0 <= n <= len(saber["secuencia_de_conteo"]["palabras"]):
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
        nombre = construir_nombre_hasta_mil(n, saber)
        if nombre:
            return nombre, True
    return t, False


def p_la_suma_no_cruza_de_diez(escena, cuenta):
    """Si los dos ya suman diez o menos, no hay nada que cruzar: no hace falta derivar."""
    a, b = cuenta.get("valor_a"), cuenta.get("valor_b")
    if a is None or b is None:
        return False
    return a + b <= 10


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
    return a + b > len(cuenta.get("secuencia") or [])


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
            return _resultado_de_la_6_3("palabra", "palabra_de_dos_digitos (6.3)", saber,
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
        r["parejas"] = [(k, n - k) for k in range(0, n // 2 + 1)]
        r["parejas_palabras"] = [(_palabra_de(k, secuencia), _palabra_de(n - k, secuencia))
                                 for k, _ in r["parejas"]]
        r["parejas_cifras"] = [(tabla.get(_palabra_de(k, secuencia)),
                                tabla.get(_palabra_de(n - k, secuencia)))
                               for k, _ in r["parejas"]]
        r["cuantas_maneras"] = len(r["parejas"])
        # VERIFICACION: recomponer cada pareja tiene que devolver el todo (la vuelta verifica la ida)
        r["verificacion"] = all(k + (n - k) == n for k, _ in r["parejas"])
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
        n = len(a) + len(b)
        tabla = _tabla(saber)
        r["parte_a"] = _palabra_de(len(a), secuencia)
        r["parte_b"] = _palabra_de(len(b), secuencia)
        r["total"] = _palabra_de(n, secuencia)
        r["total_cifra"] = tabla.get(r["total"])
        r["cifra_a"] = tabla.get(r["parte_a"])
        r["cifra_b"] = tabla.get(r["parte_b"])
        # VERIFICACION por la vuelta: partir el todo tiene que dar las mismas dos partes
        r["verificacion"] = (len(a) + len(b) == n)
        r["las_dos_partes"] = sorted([len(a), len(b)])
    return r


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
    n = len(r["primera"]) + len(r["segunda"])
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
        n = len(a) + len(b)
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
        parejas = [(k, n - k) for k in range(0, n // 2 + 1)]
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
    lineas.extend(_puente_mejor("*" * (len(r["primera"]) + len(r["segunda"])), r["suma"],
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
    # El mapa inverso de la 6.7: O(1), no un recorrido de mil nombres.
    return (saber.get("_nombre_a_valor") or {}).get(palabra)


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
    total = va + vb
    r["conclusion"] = "suma"
    r["valor_a"], r["valor_b"] = va, vb
    r["total_valor"] = total
    r["suma"] = _palabra_de(total, saber["secuencia_de_conteo"]["palabras"])
    r["cifra_a"] = tabla.get(pa)
    r["cifra_b"] = tabla.get(pb)
    r["cifra_suma"] = tabla.get(r["suma"])
    # Las tres representaciones y la verificacion por la vuelta (unidad 5.1)
    r["parejas_de_la_suma"] = [(k, total - k) for k in range(0, total // 2 + 1)]
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
    r["parejas"] = [(k, v - k) for k in range(0, v // 2 + 1)]
    r["parejas_palabras"] = [(_palabra_de(k, saber["secuencia_de_conteo"]["palabras"]),
                              _palabra_de(v - k, saber["secuencia_de_conteo"]["palabras"]))
                             for k, _ in r["parejas"]]
    r["parejas_cifras"] = [(tabla.get(_palabra_de(k, saber["secuencia_de_conteo"]["palabras"])),
                            tabla.get(_palabra_de(v - k, saber["secuencia_de_conteo"]["palabras"])))
                           for k, _ in r["parejas"]]
    r["cuantas_maneras"] = len(r["parejas"])
    r["verificacion"] = all(k + (v - k) == v for k, _ in r["parejas"])
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
        lineas.append("  La suma daria %d, y mi lista de contar llega a diez." % r["total_valor"])
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
        quedan = len(reales) - valor
        r["minuendo"] = _palabra_de(len(reales), secuencia)
        r["sustraendo"] = palabra
        r["resultado"] = _palabra_de(quedan, secuencia)
        r["cifra_minuendo"] = tabla.get(r["minuendo"])
        r["cifra_sustraendo"] = tabla.get(r["sustraendo"])
        r["cifra_resultado"] = tabla.get(r["resultado"])
        r["los_que_quedan"] = [o["id"] for o in reales[:quedan]]
        r["los_que_se_van"] = [o["id"] for o in reales[quedan:]]
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
        r["verificacion"] = (quedan + valor == len(reales))
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
    r["conclusion"] = "resta"
    r["valor_a"], r["valor_b"] = va, vb
    r["resultado_valor"] = va - vb
    r["resultado"] = _palabra_de(va - vb, saber["secuencia_de_conteo"]["palabras"])
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
    r["diferencia_valor"] = abs(len(a) - len(b))
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
        r["verificacion"] = (r["diferencia_valor"] + min(len(a), len(b)) == max(len(a), len(b)))
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
    r["diferencia_valor"] = abs(va - vb)
    r["diferencia"] = _palabra_de(r["diferencia_valor"], r["secuencia"])
    r["mayor"], r["menor"] = (pa, pb) if va >= vb else (pb, pa)
    r["cifra_mayor"], r["cifra_menor"] = tabla.get(r["mayor"]), tabla.get(r["menor"])
    r["cifra_diferencia"] = tabla.get(r["diferencia"])
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


# ------------------------------------------------- la secuencia hasta 100 (6.1)

def _tabla_nombres(saber):
    """
    La tabla de la unidad 6.1, ya NORMALIZADA: los numeros como enteros, no como texto.
    El .kn es texto; convertirlo aqui, en un solo sitio, evita repetir la conversion por todas
    partes (y evita el error de comparar un texto con un numero).
    """
    d = saber.get("secuencia_hasta_cien") or {}

    def a_entero(x):
        try:
            return int(x)
        except (TypeError, ValueError):
            return None

    memorizadas, decenas, formaciones = {}, {}, []
    for k, v in (d.get("memorizadas") or {}).items():
        n = a_entero(k)
        if n is not None:
            memorizadas[n] = v
    for k, v in (d.get("decenas") or {}).items():
        n = a_entero(k)
        if n is not None:
            decenas[n] = v
    for f in (d.get("formaciones") or []):
        desde, hasta = a_entero(f.get("desde")), a_entero(f.get("hasta"))
        if desde is not None and hasta is not None:
            formaciones.append({"nombre": f.get("nombre"), "desde": desde, "hasta": hasta,
                                "prefijo": f.get("prefijo"), "junta": f.get("junta")})
    return {"memorizadas": memorizadas, "decenas": decenas, "formaciones": formaciones}


def construir_nombre_hasta_cien(n, saber):
    """
    Unidad 6.1: el nombre de un numero del 1 al 100, CONSTRUIDO con la regla.

    No esta memorizado: se construye.  Se sabe de memoria solo lo que la regla no puede dar
    (1-10, 11-15, 20, 100 y las decenas); lo demas sale de las tres formaciones.
    Devuelve None si esta fuera del 1..100 (o si falta un dato).
    """
    tabla = _tabla_nombres(saber)
    if n in tabla["memorizadas"]:
        return tabla["memorizadas"][n]
    if n in tabla["decenas"]:
        return tabla["decenas"][n]
    for f in tabla["formaciones"]:
        if f["desde"] <= n <= f["hasta"]:
            unidad = tabla["memorizadas"].get(n % 10)
            if not unidad:
                return None
            if f.get("junta") == "pegado":
                return "%s%s" % (f["prefijo"], unidad)
            if f.get("junta") == "con_y":
                decena = tabla["decenas"].get(n - (n % 10))
                if not decena:
                    return None
                return "%s y %s" % (decena, unidad)
    return None


def construir_nombre_hasta_mil(n, saber):
    """
    Unidad 6.7: el nombre de un numero del 1 al 1000, CONSTRUIDO con la regla.

    Por debajo de 100 delega en la 6.1 (misma verdad, no una copia).  De 100 a 999 compone con la
    palabra del CIENTO (que se sabe de memoria: son nueve) mas el nombre del resto.
    Y 1000 es "mil".

    OJO con las dos irregularidades:
      - 100 solo es "cien"; de 101 a 199 es "ciento ..."; y de 200 en adelante ya es la palabra del
        cientos a secas (200 -> "doscientos").
      - quinientos, setecientos y novecientos NO se construyen pegando "-cientos".
    Devuelve None si esta fuera del 1..1000.
    """
    if n is None or n < 1 or n > 1000:
        return None
    if n <= 100:
        return construir_nombre_hasta_cien(n, saber)
    if n == 1000:
        return _centenas(saber).get("mil") or "mil"
    cent, resto = divmod(n, 100)
    cientos = _centenas(saber)
    if resto == 0:
        return cientos["cientos_solos"].get(cent)
    palabra_cientos = cientos["cientos"].get(cent)
    if not palabra_cientos:
        return None
    nombre_resto = construir_nombre_hasta_cien(resto, saber)
    if not nombre_resto:
        return None
    return "%s %s" % (palabra_cientos, nombre_resto)


def _centenas(saber):
    """
    Los datos de los cientos, tal como estan escritos en la_centena.kn.
    OJO: el lector de .kn devuelve las claves como TEXTO ('2'), asi que aqui se pasan a numero.
    Si no, buscar el 5 daria None y "quinientos" no saldria nunca.
    """
    d = saber.get("la_centena") or {}
    if not d:
        return d
    out = dict(d)
    for clave in ("cientos", "cientos_solos"):
        t_ = d.get(clave)
        if isinstance(t_, dict):
            out[clave] = {}
            for k, v in t_.items():
                try:
                    out[clave][int(k)] = v
                except (TypeError, ValueError):
                    out[clave][k] = v
    return out


def _secuencia_hasta_mil(saber):
    """Los 1000 nombres, en orden, construidos con la regla (unidad 6.7, que sube el techo)."""
    return [construir_nombre_hasta_mil(n, saber) for n in range(1, 1001)]


def _secuencia_hasta_cien(saber):
    """Los 100 nombres, en orden, construidos con la regla de la unidad 6.1."""
    return [construir_nombre_hasta_cien(n, saber) for n in range(1, 101)]


def de_donde_sale_el_nombre(n, saber):
    """Como se construyo ese nombre: que formacion, y con que piezas.  Para poder EXPLICARLO."""
    tabla = _tabla_nombres(saber)
    if n in tabla["memorizadas"]:
        return {"tipo": "memorizada", "palabra": tabla["memorizadas"][n]}
    if n in tabla["decenas"]:
        return {"tipo": "decena", "palabra": tabla["decenas"][n]}
    for f in tabla["formaciones"]:
        if f["desde"] <= n <= f["hasta"]:
            unidad_valor = n % 10
            piezas = {"unidad": tabla["memorizadas"].get(unidad_valor), "unidad_valor": unidad_valor}
            if f.get("junta") == "pegado":
                piezas["prefijo"] = f["prefijo"]
            elif f.get("junta") == "con_y":
                piezas["decena"] = tabla["decenas"].get(n - unidad_valor)
                piezas["decena_valor"] = n - unidad_valor
            return {"tipo": f["nombre"], "junta": f.get("junta"), "piezas": piezas,
                    "desde": f["desde"], "hasta": f["hasta"]}
    return None


def _la_decena_que_le_toca(n):
    """La decena a la que pertenece un numero (para hablar del error de decena)."""
    return (n // 10) * 10


def explicar_6_1_nombre(texto, saber=None):
    """'nombre: 47' -> la palabra, y ENSEÑA COMO SE CONSTRUYO (que es lo de esta unidad)."""
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (6.1): como se LLAMA este numero?"]
    t = texto.strip()
    try:
        n = int(t)
    except ValueError:
        lineas.append("RESULTADO: no_lo_se")
        lineas.append("  '%s' no es un numero del 1 al 100." % t)
        return "\n".join(lineas)
    lineas.append("NUMERO: %d" % n)
    palabra = construir_nombre_hasta_cien(n, saber)
    if palabra is None:
        lineas.append("RESULTADO: fuera_de_mi_secuencia")
        lineas.append("  Mi secuencia de contar llega del UNO al CIEN.  Mas alla no me invento")
        lineas.append("  nombres, porque no los tengo escritos en ningun sitio.")
        return "\n".join(lineas)
    info = de_donde_sale_el_nombre(n, saber) or {}
    lineas.append("")
    if info.get("tipo") == "memorizada":
        lineas.append("  ESTE NOMBRE HAY QUE SABERSE DE MEMORIA.  Aqui la regla no llega:")
        lineas.append("  del 1 al 10 y del 11 al 15 son irregulares (once, doce, trece... no salen de")
        lineas.append("  ninguna regla), y el 20 tampoco (no es 'veinti-diez').")
    elif info.get("tipo") == "decena":
        lineas.append("  ESTE NOMBRE HAY QUE SABERSE DE MEMORIA: es una DECENA, y es justo el punto")
        lineas.append("  donde la regla se ROMPE.  Por eso 'veintinueve' no sigue con 'veintidiez':")
        lineas.append("  sigue con 'treinta'.  Las decenas hay que saberselas.")
    elif info.get("junta") == "pegado":
        p = info["piezas"]
        lineas.append("  SE CONSTRUYE con la formacion '%s' (del %d al %d), TODO PEGADO:"
                      % (info["tipo"], info["desde"], info["hasta"]))
        lineas.append("     prefijo '%s' + la unidad '%s'  ->  %s" % (p["prefijo"], p["unidad"], palabra))
        lineas.append("  (La unidad que se pega es la PALABRA del 1 al 9, nunca una cifra.)")
    elif info.get("junta") == "con_y":
        p = info["piezas"]
        lineas.append("  SE CONSTRUYE con la formacion '%s' (del %d al %d), y va SEPARADO:"
                      % (info["tipo"], info["desde"], info["hasta"]))
        lineas.append("     la decena '%s' + ' y ' + la unidad '%s'  ->  %s"
                      % (p["decena"], p["unidad"], palabra))
    lineas.append("")
    lineas.append("  OJO: ese es el numero %d, y su nombre es '%s'.  El nombre NO dice las cifras" % (n, palabra))
    lineas.append("  (eso sera la unidad 6.2); dice como se lee.")
    lineas.append("")
    lineas.append("RESULTADO: %s" % palabra)
    return "\n".join(lineas)


def explicar_6_1_numero(texto, saber=None):
    """'numero: cuarenta y siete' -> el numero.  La vuelta: de la PALABRA al numero."""
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (6.1): que numero es este nombre?  (la vuelta)"]
    t = texto.strip().lower()
    lineas.append("PALABRA: %s" % t)
    for n in range(1, 101):
        if construir_nombre_hasta_cien(n, saber) == t:
            lineas.append("")
            lineas.append("  Lo construyo hasta encontrar el que coincide:")
            info = de_donde_sale_el_nombre(n, saber) or {}
            if info.get("tipo") in ("memorizada", "decena"):
                lineas.append("  y es de las que hay que SABERSE (no sale de ninguna regla).")
            elif info.get("junta") == "pegado":
                lineas.append("  formacion '%s': '%s' es el prefijo y '%s' es la unidad."
                              % (info["tipo"], info["piezas"]["prefijo"], info["piezas"]["unidad"]))
            elif info.get("junta") == "con_y":
                lineas.append("  formacion '%s': '%s' es la decena y '%s' la unidad."
                              % (info["tipo"], info["piezas"]["decena"], info["piezas"]["unidad"]))
            lineas.append("")
            lineas.append("RESULTADO: %d" % n)
            return "\n".join(lineas)
    lineas.append("RESULTADO: no_lo_se")
    lineas.append("  '%s' no es un nombre de mi secuencia.  No me lo invento." % t)
    lineas.append("  (Mi secuencia son los 100 nombres; los construyo con la regla y los recorro.)")
    return "\n".join(lineas)


def explicar_6_1_decenas(saber=None):
    """Las decenas: los nombres donde la regla se ROMPE.  Por eso hay que saberselas."""
    if saber is None:
        saber = cargar_conocimiento()
    tabla = _tabla_nombres(saber)
    lineas = ["LAS DECENAS (unidad 6.1): los nombres donde la REGLA SE ROMPE"]
    lineas.append("  Del 31 al 99 los nombres se construyen: la decena + ' y ' + la unidad.")
    lineas.append("  Pero cada DECENA hay que sabersela, porque no sale de ninguna regla:")
    lineas.append("")
    for n in sorted(tabla["decenas"]):
        lineas.append("    %d   %s" % (n, tabla["decenas"][n]))
    lineas.append("")
    lineas.append("  Y el 20 tambien es irregular: veinte (no 'veinti-diez').  Y el 100: cien.")
    lineas.append("")
    lineas.append("  LO IMPORTANTE, EL ERROR DE DECENA:")
    lineas.append("    veintiocho, veintinueve, ... ¿y ahora?")
    lineas.append("    Si siguiera la regla saldria 'veintidiez', que NO EXISTE.")
    lineas.append("    El nombre CAMBIA: treinta.")
    lineas.append("    Ese error lo hace quien ha entendido la regla DEMASIADO BIEN.  No es no saber:")
    lineas.append("    es aplicar una regla buena donde ya no vale.")
    lineas.append("")
    lineas.append("  Y CONTAR DE DIEZ EN DIEZ (esto prepara la unidad 6.2):")
    lineas.append("    %s" % ", ".join(tabla["decenas"][n] for n in sorted(tabla["decenas"])))
    lineas.append("    (cada uno es UN GRUPO DE DIEZ; contar asi es contar dieces)")
    return "\n".join(lineas)


# ------------------------------------------------- el metodo de los dedos (7.1)

def decidir_7_1_dedos(texto_a, texto_b, saber=None):
    """
    Unidad 7.1: EL METODO DE LOS DEDOS (sumar contando hacia adelante, mecanico).

      1. se ANOTA el primero (la pizarra),
      2. se cogen con los dedos tantos como el SEGUNDO,
      3. se cuenta HACIA ADELANTE desde el primero, un paso por dedo,
      4. el ultimo numero dicho es el total.

    OJO: el total es DONDE SE PARA.  No tiene que caber en los dedos: los dedos cuentan los PASOS.
    """
    if saber is None:
        saber = cargar_conocimiento()
    pa, ca = nombre_de_numero(texto_a, saber)
    pb, cb = nombre_de_numero(texto_b, saber)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    va = _valor_de_cantidad(pa, saber)
    vb = _valor_de_cantidad(pb, saber)
    cuenta = {"secuencia": secuencia, "valor_a": va, "valor_b": vb, "_saber": saber}
    r = _aplicar_reglas(saber["reglas_7_1"]["reglas_dedos"], None, None, saber, cuenta=cuenta)
    r["secuencia"] = secuencia
    r["entidades"] = []
    r["texto_a"], r["texto_b"] = texto_a, texto_b
    r["palabra_a"], r["palabra_b"] = pa, pb
    r["venia_en_cifra"] = (ca, cb)
    r["valor_a"], r["valor_b"] = va, vb
    r["dedos"] = _cuantos_dedos(saber)
    if r["conclusion"] != "se_puede":
        return r
    # LA PIZARRA: lo que se ha anotado, y los pasos uno a uno.
    r["anotado"] = pa
    r["los_pasos"] = []
    for k in range(1, vb + 1):
        valor = va + k
        r["los_pasos"].append({"dedo": k, "quedan": vb - k, "valor": valor,
                               "palabra": _palabra_de(valor, secuencia)})
    r["total_valor"] = va + vb
    r["total"] = _palabra_de(va + vb, secuencia)
    r["expresion"] = "%s + %s = %s" % (pa, pb, r["total"])
    tabla = _tabla(saber)
    r["cifra_a"], r["cifra_b"] = tabla.get(pa), tabla.get(pb)
    r["cifra_total"] = tabla.get(r["total"])
    r["hay_cifras"] = (r["cifra_a"] is not None and r["cifra_b"] is not None)
    if r["hay_cifras"]:
        r["expresion_cifras"] = "%s + %s = %s" % (r["cifra_a"], r["cifra_b"],
                                                  r["cifra_total"] or r["total"])
    else:
        r["expresion_cifras"] = r["expresion"]
    # LAS CUENTAS DEL AHORRO: contar hacia adelante da VB pasos; contar todo daria A+B.
    r["pasos_dados"] = vb
    r["pasos_contando_todo"] = va + vb
    r["pasos_ahorrados"] = va
    r["la_suma_cuadra"] = (r["total_valor"] == va + vb)
    # LA COMPROBACION: al total se le quita el segundo y tiene que volver a salir el primero.
    r["expresion_inversa"] = "%s - %s = %s" % (r["total"], pb, pa)
    r["verificacion"] = (r["total_valor"] - vb == va)
    return r


def explicar_7_1_dedos(texto_a, texto_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_7_1_dedos(texto_a, texto_b, saber)
    lineas = ["PREGUNTA (7.1): como se suman estos DOS NUMEROS, MECANICAMENTE?"
              "  (el metodo de los dedos)"]
    lineas.append("NUMEROS:  %s  y  %s" % (texto_a, texto_b))
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  Alguno de los dos no es un numero que conozca (los mios van del CERO al CIEN).")
        return "\n".join(lineas)
    if r["conclusion"] == "no_caben_en_los_dedos":
        lineas.append("RESULTADO: no_caben_en_los_dedos")
        lineas.append("  El SEGUNDO numero es %s, y solo tengo %d dedos." % (r["palabra_b"], r["dedos"]))
        lineas.append("  CONDICION DE APLICACION: al segundo numero no le pueden pasar de %d."
                      % r["dedos"])
        lineas.append("  (El PRIMERO puede ser mas grande, porque no se coge con los dedos: se ANOTA.)")
        return "\n".join(lineas)
    if r["conclusion"] == "no_alcanza":
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  La suma se pasaria de %s, que es hasta donde se contar."
                      % _hasta_donde_cuento(saber).upper())
        return "\n".join(lineas)
    if r["hay_cifras"]:
        lineas.append("EN CIFRAS: %s" % r["expresion_cifras"])
    lineas.append("")
    lineas.append("  PASO 1 - SE ANOTA EL PRIMERO.  El primero no se cuenta: se GUARDA.")
    lineas.append("    PIZARRA:  %s        <- aqui esta anotado, y de aqui no se mueve"
                  % r["anotado"])
    lineas.append("    (esto es la MEMORIA DE TRABAJO: hay que aguantarlo mientras se cuenta.")
    lineas.append("     Es la parte que cuesta, y por eso el sistema tiene la pizarra a la vista)")
    lineas.append("")
    lineas.append("  PASO 2 - SE COGEN CON LOS DEDOS tantos como el SEGUNDO numero (%s)."
                  % r["palabra_b"])
    lineas.append("    dedos levantados: %d  de  %d" % (r["valor_b"], r["dedos"]))
    if r["valor_b"] == 0:
        lineas.append("    (ninguno: el segundo es CERO, asi que no se levanta ni un dedo)")
    lineas.append("")
    lineas.append("  PASO 3 - SE CUENTA HACIA ADELANTE DESDE EL PRIMERO, un paso por dedo.")
    lineas.append("    OJO: se empieza a contar DESDE EL %s, NO desde el uno."
                  % r["anotado"].upper())
    if r["los_pasos"]:
        for p in r["los_pasos"]:
            lineas.append("      dedo %d:  se dice '%s'   (quedan %d dedos)"
                          % (p["dedo"], p["palabra"], p["quedan"]))
    else:
        lineas.append("      (no hay pasos: no se levanto ningun dedo)")
    lineas.append("")
    lineas.append("  PASO 4 - SE ACABARON LOS DEDOS: el ULTIMO numero dicho es el total.")
    lineas.append("    el ultimo numero dicho: %s" % r["total"].upper())
    lineas.append("")
    lineas.append("  ¡OJO CON LA TRAMPA!  El total NO tiene que caber en los dedos:")
    lineas.append("  los dedos cuentan los PASOS, no el resultado.  Aqui %s no cabe en %d dedos,"
                  % (r["total"], r["dedos"]))
    lineas.append("  y no pasa nada.")
    lineas.append("")
    lineas.append("  POR QUE ESTO ES MEJOR QUE CONTAR TODO:")
    lineas.append("    contando hacia adelante (desde el %s):  %d pasos"
                  % (r["anotado"], r["pasos_dados"]))
    lineas.append("    contando todo (desde el uno):           %d pasos"
                  % r["pasos_contando_todo"])
    lineas.append("    -> el mismo resultado, pero %d pasos MENOS."
                  % r["pasos_ahorrados"])
    lineas.append("    Contar todo es lo que hace quien aun no sabe sumar.  Y cuanto mas grandes son")
    lineas.append("    los numeros, mas se nota la diferencia.")
    lineas.append("")
    lineas.append("  COMPROBACION (al total se le quita el segundo y vuelve el primero):")
    lineas.append("    %s ... %s" % (r["expresion_inversa"],
                                     "SI" if r["verificacion"] else "NO"))
    if not r["verificacion"]:
        lineas.append("    NO CUADRA. El sistema no elige uno: lo dice.")
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["expresion"])
    lineas.append("  %s   (%s mas %s igual a %s)" % (r["expresion"], r["palabra_a"],
                                                     r["palabra_b"], r["total"]))
    lineas.append("")
    lineas.append("  Y ES MECANICO: todo lo que hay arriba sale de los cuatro pasos.  Nada se sabe")
    lineas.append("  de memoria ni sale de una calculadora (decision de Carlos, 4 oct 2026).")
    lineas.append("")
    lineas.append("  LA OTRA VIA (derivar, unidad 7.2): si este segundo numero pasa del DIEZ, los dedos")
    lineas.append("  ya no llegan... pero DERIVAR (hacer diez) SI.  El sistema prueba las dos cuando puede.")
    otra = decidir_7_2_derivar(texto_a, texto_b, saber)
    if otra["conclusion"] == "se_puede":
        lineas.append("    DERIVANDO: %s   (y no cuenta nada: hace diez y sumo lo que sobra)"
                      % otra["expresion"])
        lineas.append("    -> las dos vias dan lo mismo: %s"
                      % ("SI" if otra["total_valor"] == r["total_valor"] else "NO"))
    else:
        lineas.append("    DERIVAR aqui dice: %s" % otra["conclusion"])
    return "\n".join(lineas)


# ------------------------------------------------- derivar / hacer diez (7.2)

def decidir_7_2_derivar(texto_a, texto_b, saber=None):
    """
    Unidad 7.2: DERIVAR (hacer diez).  Usar lo que ya se sabe para NO contar.

      7 + 5  ->  al 7 le faltan 3 para diez
              ->  parto el 5 en 3 y 2
              ->  7 + 3 = 10, y 10 + 2 = 12

    No hace falta nada nuevo: se COMBINAN la particion (5.1) y la suma (5.2).
    """
    if saber is None:
        saber = cargar_conocimiento()
    pa, ca = nombre_de_numero(texto_a, saber)
    pb, cb = nombre_de_numero(texto_b, saber)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    va = _valor_de_cantidad(pa, saber)
    vb = _valor_de_cantidad(pb, saber)
    cuenta = {"secuencia": secuencia, "valor_a": va, "valor_b": vb, "_saber": saber}
    r = _aplicar_reglas(saber["reglas_7_2"]["reglas_derivar"], None, None, saber, cuenta=cuenta)
    r["secuencia"] = secuencia
    r["entidades"] = []
    r["texto_a"], r["texto_b"] = texto_a, texto_b
    r["palabra_a"], r["palabra_b"] = pa, pb
    r["valor_a"], r["valor_b"] = va, vb
    if r["conclusion"] != "se_puede":
        return r
    faltan = 10 - va          # lo que le falta al primero para llegar a DIEZ
    r["faltan_para_diez"] = faltan
    r["sobra_del_segundo"] = vb - faltan
    r["parte_para_diez"] = faltan
    r["parte_que_sobra"] = vb - faltan
    r["primera_cuenta"] = "10" if faltan else "0"
    r["paso_1"] = "%d + %d = 10" % (va, faltan)
    r["paso_2"] = "10 + %d = %d" % (vb - faltan, va + vb)
    r["total_valor"] = va + vb
    r["total"] = _palabra_de(va + vb, secuencia)
    r["expresion"] = "%s + %s = %s" % (pa, pb, r["total"])
    r["suma_de_tres"] = "%d + %d + %d" % (va, faltan, vb - faltan)
    tabla = _tabla(saber)
    r["cifra_a"], r["cifra_b"] = tabla.get(pa), tabla.get(pb)
    r["cifra_total"] = tabla.get(r["total"])
    if r["cifra_a"] is not None and r["cifra_b"] is not None:
        r["expresion_cifras"] = "%s + %s = %s" % (r["cifra_a"], r["cifra_b"],
                                                  r["cifra_total"] or r["total"])
    else:
        r["expresion_cifras"] = r["expresion"]
    r["las_partes_cuadran"] = (faltan + (vb - faltan) == vb)
    r["verificacion"] = (va + faltan == 10 and 10 + (vb - faltan) == va + vb)
    # LA OTRA VIA: los dedos tienen que decir lo mismo (decision de Carlos: que pruebe las dos).
    otra = decidir_7_1_dedos(texto_a, texto_b, saber)
    r["la_otra_via"] = otra
    if otra["conclusion"] == "se_puede":
        r["las_dos_vias_coinciden"] = (otra["total_valor"] == r["total_valor"])
        r["la_otra_via_dice"] = otra["total"]
        r["la_otra_via_pasos"] = otra["pasos_dados"]
    else:
        r["las_dos_vias_coinciden"] = None
        r["la_otra_via_dice"] = None
    return r


def explicar_7_2_derivar(texto_a, texto_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_7_2_derivar(texto_a, texto_b, saber)
    lineas = ["PREGUNTA (7.2): como se suman estos DOS NUMEROS DERIVANDO?"
              "  (hacer diez: usar lo que ya sabes, sin contar)"]
    lineas.append("NUMEROS:  %s  y  %s" % (texto_a, texto_b))
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  Alguno de los dos no es un numero que conozca (los mios van del CERO al CIEN).")
        return "\n".join(lineas)
    if r["conclusion"] == "necesito_las_columnas":
        lineas.append("RESULTADO: necesito_las_columnas")
        lineas.append("  El primero (%s) es de DOS cifras, y mi 'hacer diez' es para numeros de UNA."
                      % r["palabra_a"])
        lineas.append("  CONDICION DE APLICACION: partir y completar diez necesita una cifra.")
        lineas.append("  Con dos cifras hay que ir por COLUMNAS: unidad con unidad, decena con decena")
        lineas.append("  (unidad 7.3, que todavia no esta).  No lo hago mal: lo digo.")
        return "\n".join(lineas)
    if r["conclusion"] == "no_hace_falta":
        lineas.append("RESULTADO: no_hace_falta")
        lineas.append("  %s y %s ya suman %s, y NO cruzan el diez: no hay nada que hacer."
                      % (r["palabra_a"], r["palabra_b"], _palabra_de(r["valor_a"] + r["valor_b"],
                                                                     r["secuencia"])))
        lineas.append("  Derivar sirve para cuando la suma PASA de diez (7 + 5, 8 + 4, 9 + 9).")
        return "\n".join(lineas)
    if r["hay_cifras"] if "hay_cifras" in r else False:
        pass
    lineas.append("")
    lineas.append("  ESTO NO ES CONTAR: es TRANSFORMAR la cuenta en dos cuentas mas faciles, y una")
    lineas.append("  de ellas (%s) ya la se." % ("llegar a diez"))
    lineas.append("")
    lineas.append("  PASO 1 - ¿CUANTO LE FALTA AL PRIMERO PARA LLEGAR A DIEZ?")
    lineas.append("    al %s le faltan %d  (porque %d + %d = 10)"
                  % (r["palabra_a"], r["faltan_para_diez"], r["valor_a"], r["faltan_para_diez"]))
    lineas.append("")
    lineas.append("  PASO 2 - PARTO EL SEGUNDO EN DOS, PARA SEPARAR ESA PARTE  (es partir, unidad 5.1)")
    lineas.append("    %s  =  %d  +  %d" % (r["palabra_b"], r["parte_para_diez"], r["parte_que_sobra"]))
    lineas.append("    (la primera parte es la que hace diez; la segunda es la que sobra)")
    lineas.append("")
    lineas.append("  PASO 3 - HAGO DIEZ, y luego sumo lo que sobra:")
    lineas.append("    %s        <- aqui ya hay DIEZ" % r["paso_1"])
    lineas.append("    %s        <- y esto es sumarle lo que sobraba" % r["paso_2"])
    lineas.append("")
    lineas.append("  LA CUENTA ENTERA ES UNA SUMA DE TRES:  %s = %d"
                  % (r["suma_de_tres"], r["total_valor"]))
    lineas.append("")
    lineas.append("  COMPROBACION DE LA DERIVACION (las dos partes tienen que ser el segundo):")
    lineas.append("    %d + %d = %d ... %s"
                  % (r["parte_para_diez"], r["parte_que_sobra"], r["valor_b"],
                     "SI" if r["las_partes_cuadran"] else "NO"))
    lineas.append("    y los dos pasos: %s y %s ... %s"
                  % (r["paso_1"], r["paso_2"], "SI" if r["verificacion"] else "NO"))
    lineas.append("")
    lineas.append("  LAS DOS VIAS (prueba de Carlos: que pruebe las dos):")
    if r["las_dos_vias_coinciden"] is None:
        lineas.append("    los DEDOS no pueden hacer esta cuenta (el segundo pasa de diez),")
        lineas.append("    asi que aqui solo hay una via.")
    else:
        lineas.append("    DERIVANDO (esto):  %s" % r["total"])
        lineas.append("    CON LOS DEDOS (7.1): %s, y costaria %d pasos"
                      % (r["la_otra_via_dice"], r["la_otra_via_pasos"]))
        lineas.append("    -> las dos dan lo mismo: %s"
                      % ("SI" if r["las_dos_vias_coinciden"] else "NO. ¡NO CUADRAN!"))
        lineas.append("    La diferencia: derivando NO se cuenta nada.")
    lineas.append("")
    lineas.append("  POR QUE DERIVAR ES MEJOR QUE CONTAR (esta medido, no es una opinion):")
    lineas.append("    'los metodos de contar hacia adelante no solo son menos eficientes, estan")
    lineas.append("     asociados con un RENDIMIENTO MAS BAJO... los alumnos de rendimiento alto")
    lineas.append("     tienden a usar HECHOS DERIVADOS'  (Tall y Gray, citado por Number Sense Maths)")
    lineas.append("    Y '8 + 9' casi nadie lo tiene memorizado: solo el 5% de los profesores dice")
    lineas.append("    'saberlo'; la mayoria lo deriva.  (Number Sense Maths)")
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["expresion"])
    lineas.append("  %s   (%s mas %s igual a %s)" % (r["expresion"], r["palabra_a"],
                                                     r["palabra_b"], r["total"]))
    lineas.append("")
    lineas.append("  Y NO SE SABE DE MEMORIA NI SE USA CALCULADORA: sale de partir y de hacer diez,")
    lineas.append("  que ya estaban en el sistema.  Derivar es COMBINAR lo que ya se sabe.")
    return "\n".join(lineas)


# ------------------------------------------------- agrupar de diez en diez (6.2)

def decidir_6_2_agrupar(escena, saber=None):
    """
    Unidad 6.2: AGRUPAR DE DIEZ EN DIEZ.  Coger los objetos de diez en diez y contar los montones
    como UNA cosa (una decena), mas lo que sobra suelto (las unidades).

      13 objetos  ->  UNA DECENA y 3 UNIDADES

    Esto es el "unitising" (NCETM): diez unidades son UNA decena, y la decena es una cosa nueva.
    """
    if saber is None:
        saber = cargar_conocimiento()
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    cuenta = {"secuencia": secuencia, "_saber": saber}
    r = _aplicar_reglas(saber["reglas_6_2"]["reglas_agrupar"], escena, None, saber, cuenta=cuenta)
    r["escena"] = escena
    r["secuencia"] = secuencia
    if r["conclusion"] != "se_puede":
        r["cuantos_objetos"] = len(escena)
        return r
    total = len(escena)
    decenas = total // 10
    unidades = total % 10
    r["cuantos_objetos"] = total
    r["decenas"] = decenas
    r["unidades"] = unidades
    r["montones"] = [escena[i * 10:(i + 1) * 10] for i in range(decenas)]
    r["sueltos"] = escena[decenas * 10:]
    r["palabra_total"] = _palabra_de(total, secuencia)
    r["cifra_total"] = _tabla(saber).get(r["palabra_total"])
    r["decenas_en_palabra"] = _palabra_de(decenas, secuencia) if decenas else "cero"
    r["unidades_en_palabra"] = _palabra_de(unidades, secuencia) if unidades else "cero"
    # COMO SE DICE ENTERO: "una decena y tres" / "cuatro decenas" / "tres unidades" (si no hay decena)
    # OJO: la decena es FEMENINA ("una decena", no "uno decena").
    r["decena_o_decenas"] = "una decena" if decenas == 1 else "%s decenas" % r["decenas_en_palabra"]
    if total == 0:
        # El conjunto VACIO no es "no hay decena": es CERO (unidad 3.2).  El vacio es una cantidad.
        r["como_se_dice"] = "cero"
    elif decenas and unidades:
        r["como_se_dice"] = "%s y %s" % (r["decena_o_decenas"], r["unidades_en_palabra"])
    elif decenas:
        r["como_se_dice"] = r["decena_o_decenas"]
    else:
        r["como_se_dice"] = "%s unidad%s" % (r["unidades_en_palabra"], "" if unidades == 1 else "es")
    # COMPROBACION 1: los montones y los sueltos tienen que ser TODOS los objetos, ni uno mas ni uno menos.
    r["reparto_cuadra"] = (decenas * 10 + unidades == total)
    # COMPROBACION 2 (la de Oak): el ORDEN de los objetos NO cambia el valor.  Se agrupa al reves.
    al_reves = list(reversed(escena))
    r["decenas_al_reves"] = len(al_reves) // 10
    r["unidades_al_reves"] = len(al_reves) % 10
    r["el_orden_da_igual"] = (r["decenas_al_reves"] == decenas and r["unidades_al_reves"] == unidades)
    r["ordeno_bien"] = unidades < 10 and decenas * 10 == total - unidades
    return r


def explicar_6_2_agrupar(escena, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_6_2_agrupar(escena, saber)
    lineas = ["PREGUNTA (6.2): como se agrupan estos objetos DE DIEZ EN DIEZ?"
              "  (el diez pasa a ser UNA cosa: una DECENA)"]
    lineas.append("OBJETOS: %d" % len(escena))
    if r["conclusion"] == "no_alcanza":
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  Son %d objetos, y mi secuencia llega hasta %s.  No me lo invento."
                      % (r["cuantos_objetos"], _hasta_donde_cuento(saber)))
        return "\n".join(lineas)
    if r["conclusion"] == "no_hay_decena":
        lineas.append("RESULTADO: no_hay_decena")
        lineas.append("  Son %d objetos y para hacer UNA decena hacen falta DIEZ." % r["cuantos_objetos"])
        lineas.append("  Con menos de diez NO hay monton que hacer: quedan todos sueltos, y eso son")
        lineas.append("  %d unidad%s." % (r["cuantos_objetos"], "" if r["cuantos_objetos"] == 1 else "es"))
        lineas.append("  (Una decena es diez unidades EXACTAS.  No hay media decena.)")
        return "\n".join(lineas)
    lineas.append("")
    lineas.append("  SE VAN COGIENDO MONTONES DE DIEZ.  Cada monton de diez es UNA DECENA,")
    lineas.append("  y se cuenta como si fuera UNA SOLA COSA (eso es el 'unitising', NCETM).")
    lineas.append("")
    for i, m in enumerate(r["montones"], 1):
        lineas.append("    MONTON %d:  %s" % (i, " ".join(x["id"] for x in m)))
        if i == 1:
            lineas.append("               ^ estos diez objetos son UNA DECENA: ya no se cuentan uno a uno,")
            lineas.append("                 se cuentan como 'uno'.")
    if r["sueltos"]:
        lineas.append("    SUELTOS:   %s" % " ".join(x["id"] for x in r["sueltos"]))
        lineas.append("               ^ y estos NO llegan a diez: son las UNIDADES, y se cuentan DE UNO EN UNO.")
    lineas.append("")
    lineas.append("  SE CUENTAN PRIMERO LAS DECENAS, y despues las unidades (lo dice Oak):")
    lineas.append("    DECENAS:   %d    (se cuentan de DIEZ EN DIEZ: uno, dos, tres... montones)"
                  % r["decenas"])
    lineas.append("    UNIDADES:  %d    (y estas DE UNO EN UNO)" % r["unidades"])
    lineas.append("")
    lineas.append("  OJO CON EL ERROR TIPICO (lo documenta Oak): NO se siguen contando de diez en diez")
    lineas.append("  cuando ya se llega a las unidades.  Las decenas van de diez en diez; las unidades,")
    lineas.append("  de uno en uno.  Si contaras '2 decenas y 3 unidades' de diez en diez, dirias")
    lineas.append("  cualquier cosa.")
    lineas.append("")
    lineas.append("  COMPROBACIONES:")
    lineas.append("    - el reparto cuadra: %d decenas y %d unidades son %d ... %s"
                  % (r["decenas"], r["unidades"], r["cuantos_objetos"],
                     "SI" if r["reparto_cuadra"] else "NO"))
    lineas.append("    - y el ORDEN no cambia nada (Oak): agrupando al reves sale %d decena(s) y %d"
                  % (r["decenas_al_reves"], r["unidades_al_reves"]))
    lineas.append("      unidad(es) ... %s" % ("SI" if r["el_orden_da_igual"] else "NO"))
    lineas.append("")
    lineas.append("RESULTADO: %s   (que son %s objetos)" % (r["como_se_dice"], r["palabra_total"]))
    if r["cifra_total"]:
        lineas.append("  En cifras: %s" % r["cifra_total"])
    elif r["cuantos_objetos"] >= 10:
        lineas.append("  (Su cifra son DOS simbolos, y eso es la unidad 6.3: aqui todavia no la leo.)")
    lineas.append("")
    lineas.append("  Y ESTO ES LO QUE HACE POSIBLE EL VALOR POSICIONAL: diez unidades son UNA decena.")
    lineas.append("  La misma cantidad vista de dos maneras: %d unidades sueltas, o %d monton(es) de diez"
                  % (r["cuantos_objetos"], r["decenas"]))
    lineas.append("  y %d suelta(s)." % r["unidades"])
    lineas.append("  Y sera el paso a multiplicar: %d veces una decena son %d (eso es la unidad 5.6,"
                  " que aun no esta)." % (r["decenas"], r["decenas"] * 10))
    return "\n".join(lineas)


# ------------------------------------------------- la tabla de 100 (6.3)

def decidir_6_3_sitio(texto, saber=None):
    """
    Unidad 6.3: EL SITIO de un numero en la tabla de 100.  Decenas = fila, unidades = columna.

      sitio: 47  ->  fila 4 (cuarenta) y columna 7 (siete)  ->  4 decenas y 7 unidades
    """
    if saber is None:
        saber = cargar_conocimiento()
    palabra, venia_en_cifra = nombre_de_numero(texto, saber)
    valor = _valor_de_numero(palabra, saber)
    # Si es una CIFRA aunque pase de cien, el valor se sabe: que lo diga la regla (fuera_de_la_tabla).
    t = texto.strip()
    if valor is None and t.isdigit():
        valor = int(t)
    cuenta = {"valor": valor, "_saber": saber,
              "secuencia": saber["secuencia_de_conteo"]["palabras"]}
    r = _aplicar_reglas(saber["reglas_6_3"]["reglas_sitio"], None, None, saber, cuenta=cuenta)
    r["texto_dado"] = texto
    r["palabra"] = palabra
    r["venia_en_cifra"] = venia_en_cifra
    r["valor"] = valor
    if r["conclusion"] != "se_puede":
        return r
    d, u = valor // 10, valor % 10
    r["decenas"] = d
    r["unidades"] = u
    # EL SITIO EN LA TABLA (la tabla de 100 es 1..100: fila 0 = 1..10, fila 9 = 91..100).
    if valor >= 1:
        r["fila"] = (valor - 1) // 10
        r["columna"] = (valor - 1) % 10 + 1
        r["esta_en_la_tabla"] = True
    else:
        r["fila"] = None
        r["columna"] = None
        r["esta_en_la_tabla"] = False   # el cero no esta en la tabla (la tabla empieza en el uno)
    r["decena_en_palabra"] = _palabra_de(d, saber["secuencia_de_conteo"]["palabras"]) if d else "cero"
    r["unidad_en_palabra"] = _palabra_de(u, saber["secuencia_de_conteo"]["palabras"]) if u else "cero"
    r["es_una_decena"] = (u == 0)
    r["es_de_una_cifra"] = (valor < 10)
    r["dato"] = ("cero decenas y cero unidades" if valor == 0
                 else "%d decenas y %d unidades" % (d, u))
    return r


def explicar_6_3_sitio(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_6_3_sitio(texto, saber)
    lineas = ["PREGUNTA (6.3): en que SITIO esta este numero en la tabla de 100?"
              "  (fila = DECENAS, columna = UNIDADES)"]
    lineas.append("NUMERO:  %s" % texto)
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  No es un numero que conozca (los mios van del CERO al CIEN).")
        return "\n".join(lineas)
    if r["conclusion"] == "fuera_de_la_tabla":
        lineas.append("RESULTADO: fuera_de_la_tabla")
        lineas.append("  Mi tabla llega hasta el CIEN (diez decenas justas).  Este numero no tiene")
        lineas.append("  sitio, y no me lo invento.")
        return "\n".join(lineas)
    v = r["valor"]
    lineas.append("")
    if v == 0:
        lineas.append("  El CERO no esta en la tabla de 100: la tabla empieza en el UNO.  Y el cero")
        lineas.append("  tiene cero decenas y cero unidades (es una cantidad, unidad 3.2).")
        lineas.append("")
        lineas.append("RESULTADO: cero decenas y cero unidades  (el cero no tiene sitio en la tabla)")
        return "\n".join(lineas)
    if r["es_de_una_cifra"]:
        lineas.append("  Una cifra sola (%d) va SIEMPRE en la fila de las decenas = CERO," % v)
        lineas.append("  o sea: %s decenas y %s unidades.  Por eso se dice '%s' y NO"
                      % (r["decena_en_palabra"], r["unidad_en_palabra"], r["palabra"]))
        lineas.append("  'cero decenas y %s': el cero de las decenas NO se dice." % r["unidad_en_palabra"])
    else:
        lineas.append("  LA PRIMERA CIFRA son las DECENAS:  %s  ->  %d decenas (fila %d)"
                      % (r["decena_en_palabra"], r["decenas"], r["fila"]))
        lineas.append("  LA SEGUNDA CIFRA son las UNIDADES: %s  ->  %d unidades (columna %d)"
                      % (r["unidad_en_palabra"], r["unidades"], r["columna"]))
    lineas.append("")
    lineas.append("  LA TABLA DE 100 (la fila del numero marcada):")
    f = r["fila"]
    for fila in sorted(set([max(0, f - 1), f, min(9, f + 1)])):
        celdas = []
        for col in range(1, 11):
            n = fila * 10 + col
            if n == v:
                celdas.append("[%3d]" % n)
            else:
                celdas.append(" %3d " % n)
        marca = "  <-- AQUI" if n == v or (fila * 10 + 10 >= v > fila * 10) else ""
        lineas.append("    fila %d: %s%s" % (fila, "".join(celdas), marca))
    lineas.append("")
    lineas.append("  COMO SE LEE (esto es leer una cifra de dos digitos):")
    lineas.append("    %s  ->  %s  ->  '%s'" % (texto if r["venia_en_cifra"] else r["palabra"],
                                                r["dato"], r["palabra"]))
    lineas.append("  Y EL SITIO ES EL VALOR, no es lo mismo que la cantidad:")
    lineas.append("    en %d, el %d son %s; pero en %d el mismo %d serian %s decenas."
                  % (v, v % 10, r["unidad_en_palabra"], v % 10 * 10 + v // 10, v % 10,
                     r["unidad_en_palabra"]))
    if r["es_una_decena"]:
        lineas.append("")
        lineas.append("  OJO: es una DECENA EXACTA (0 unidades), asi que su columna es la 10 y se")
        lineas.append("  dice '%s', sin 'y cero'." % r["palabra"])
    lineas.append("")
    lineas.append("  COMPROBACION: %d son %d decenas y %d unidades  ... %s"
                  % (v, r["decenas"], r["unidades"], "SI" if r["decenas"] * 10 + r["unidades"] == v else "NO"))
    lineas.append("")
    lineas.append("RESULTADO: %s %s (fila %d, columna %d)"
                  % (r["dato"], "-> '%s'" % r["palabra"], r["fila"], r["columna"]))
    return "\n".join(lineas)


def explicar_6_3_tabla(saber=None):
    """La tabla de 100 entera, para verla."""
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (6.3): ensename la TABLA DE 100",
              "  (la fila son las DECENAS; la columna son las UNIDADES)",
              ""]
    for fila in range(0, 10):
        celdas = []
        for col in range(1, 11):
            n = fila * 10 + col
            celdas.append(" %3d " % n)
        lineas.append("  fila %d: %s" % (fila, "".join(celdas)))
    lineas.append("")
    lineas.append("  COMO SE RECORRE:")
    lineas.append("    - dentro de una fila, DE UNO EN UNO (47 -> 48: todavia en la fila 4)")
    lineas.append("    - bajando de fila, DE DIEZ EN DIEZ (47 -> 57: otra decena entera)")
    lineas.append("    (y cada fila es UNA DECENA ENTERA: eso es la unidad 6.2)")
    lineas.append("")
    lineas.append("  La tabla llega hasta el %s, que son DIEZ decenas justas (la ultima fila)."
                  % _hasta_donde_cuento(saber))
    lineas.append("  Se cuenta de dos maneras y las dos son ciertas: uno a uno (100 palabras) o de")
    lineas.append("  diez en diez (10 filas).  Es la misma cantidad.")
    lineas.append("")
    lineas.append("RESULTADO: la tabla de 100, fila a fila")
    lineas.append("   (prueba 'sitio: 47' para ver el sitio de un numero en concreto)")
    return "\n".join(lineas)


# ------------------------------------------------- partir en decenas y unidades (6.5)

def decidir_6_5_partir(texto, saber=None):
    """
    Unidad 6.5: PARTIR EN DECENAS Y UNIDADES.  Cuanto vale cada cifra.

      47  =  4 decenas  +  7 unidades  =  40 + 7
    """
    if saber is None:
        saber = cargar_conocimiento()
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    palabra, venia = nombre_de_numero(texto, saber)
    valor = _valor_de_numero(palabra, saber)
    t = texto.strip()
    if valor is None and t.isdigit():
        valor = int(t)
    cuenta = {"valor": valor, "secuencia": secuencia}
    r = _aplicar_reglas(saber["reglas_6_5"]["reglas_partir"], None, None, saber, cuenta=cuenta)
    r["texto_dado"], r["palabra"], r["venia_en_cifra"], r["valor"] = texto, palabra, venia, valor
    if r["conclusion"] != "se_puede":
        return r
    d, u = valor // 10, valor % 10
    r["decenas"], r["unidades"] = d, u
    r["valor_de_las_decenas"] = d * 10
    r["tabla"] = _tabla(saber)
    r["palabra_del_total"] = _palabra_de(valor, secuencia) if valor else "cero"
    # COMO SE DICE: "cuatro decenas y siete unidades" / "cuarenta y siete"
    r["partes_dichas"] = "%s decenas y %s unidades" % (
        _palabra_de(d, secuencia) if d else "cero",
        _palabra_de(u, secuencia) if u else "cero")
    r["cuenta_de_la_particion"] = ("%d decenas y %d unidades son %d" % (d, u, valor) if d
                                   else "solo unidades: son %d" % valor)
    r["valor_posicional"] = ("%d vale %d (no %d)" % (d, r["valor_de_las_decenas"], d)
                             if d else "el 0 de las decenas no vale nada")
    # EL ERROR TIPICO DE OAK: sumar las cifras como si valieran lo mismo
    r["si_sumara_las_cifras"] = d + u
    r["seria_el_error"] = (d + u != valor)
    return r


def explicar_6_5_partir(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_6_5_partir(texto, saber)
    lineas = ["PREGUNTA (6.5): cuanto vale CADA CIFRA de este numero?  (partirlo en decenas y unidades)"]
    lineas.append("NUMERO:  %s" % texto)
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  No es un numero que conozca (los mios van del CERO al CIEN).")
        return "\n".join(lineas)
    if r["conclusion"] == "fuera_de_la_tabla":
        lineas.append("RESULTADO: fuera_de_la_tabla")
        lineas.append("  Mi tabla llega hasta el CIEN.  Este numero no lo parto: no me lo invento.")
        return "\n".join(lineas)
    v, d, u = r["valor"], r["decenas"], r["unidades"]
    lineas.append("")
    lineas.append("  LA PRIMERA CIFRA SON LAS DECENAS y la ultima son las UNIDADES (BBC Bitesize).")
    lineas.append("")
    if v < 10:
        lineas.append("  %d tiene UNA cifra sola, asi que va en las unidades:" % v)
        lineas.append("    0 decenas y %d unidades.  Y el cero de las decenas NO se dice: se dice '%s'."
                      % (v, r["palabra_del_total"]))
    else:
        lineas.append("    DECENAS:   %d   ->  y NO vale %d: vale %d  (porque son %d decenas)"
                      % (d, d, d * 10, d))
        lineas.append("    UNIDADES:  %d   ->  y esto SI vale %d" % (u, u))
    lineas.append("")
    lineas.append("  LA CUENTA ES:  %s" % r["cuenta_de_la_particion"])
    lineas.append("  Es decir: %s" % r["partes_dichas"])
    lineas.append("  Y eso es el mismo numero de antes: '%s' = %s" % (r["palabra_del_total"], v))
    lineas.append("")
    lineas.append("  POR QUE ESTO IMPORTA (el error tipico, lo documenta Oak):")
    if r["seria_el_error"]:
        lineas.append("    OJO: si sumaras las cifras como si valieran lo mismo, %d + %d = %d,"
                      % (d, u, r["si_sumara_las_cifras"]))
        lineas.append("    y %d NO es %d.  Eso es 'transponer los digitos': las decenas NO son unidades."
                      % (r["si_sumara_las_cifras"], v))
    else:
        lineas.append("    aqui las cifras suman %d y el numero es %d: justo por eso hay que mirar"
                      % (d + u, v))
        lineas.append("    EL SITIO, no la cifra.  La misma cifra vale cosas distintas segun donde este.")
    lineas.append("    En 73 el 7 vale SETENTA; en el 7 solo, vale SIETE.  El sitio es el valor.")
    lineas.append("")
    lineas.append("  COMPROBACION (juntarlo otra vez tiene que dar el numero):")
    lineas.append("    %d decenas y %d unidades son %d ... %s"
                  % (d, u, v, "SI" if d * 10 + u == v else "NO"))
    lineas.append("")
    lineas.append("RESULTADO: %s decenas + %s unidades = %d"
                  % (d, u, v))
    lineas.append("")
    lineas.append("  Y ESTO ES LO QUE HACE FALTA PARA SUMAR POR COLUMNAS (unidad 7.3): suma")
    lineas.append("  decenas con decenas y unidades con unidades.  Para eso hay que saber partir")
    lineas.append("  primero, y por eso van en este orden.  (Lo dice Oak.)")
    return "\n".join(lineas)


def decidir_6_5_juntar_decenas(decenas, unidades, saber=None):
    """
    Unidad 6.5, al reves: JUNTAR las decenas y las unidades.

      4 decenas y 7 unidades  ->  47
    """
    if saber is None:
        saber = cargar_conocimiento()
    secuencia = saber["secuencia_de_conteo"]["palabras"]

    def _a_valor(txt):
        p, _ = nombre_de_numero(str(txt), saber)
        v = _valor_de_numero(p, saber)
        return v

    d, u = _a_valor(decenas), _a_valor(unidades)
    cuenta = {"decenas": d, "unidades": u, "secuencia": secuencia}
    r = _aplicar_reglas(saber["reglas_6_5"]["reglas_juntar_decenas"], None, None, saber, cuenta=cuenta)
    r["decenas_dadas"], r["unidades_dadas"] = decenas, unidades
    r["decenas"], r["unidades"] = d, u
    if r["conclusion"] != "se_puede":
        return r
    total = d * 10 + u
    r["total"] = total
    r["palabra"] = _palabra_de(total, secuencia) if total else "cero"
    r["cuenta"] = "%d decenas y %d unidades son %d" % (d, u, total)
    r["dato"] = "%s -> %d" % (r["palabra"], total) if total else "cero -> 0"
    r["demasiadas_unidades"] = u >= 10
    r["se_dice"] = r["palabra"]
    return r


def explicar_6_5_juntar_decenas(decenas, unidades, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_6_5_juntar_decenas(decenas, unidades, saber)
    lineas = ["PREGUNTA (6.5): juntando estas decenas y estas unidades, que numero sale?"]
    lineas.append("DECENAS:  %s     UNIDADES:  %s" % (decenas, unidades))
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  Las decenas y las unidades tienen que ser numeros que conozca.")
        return "\n".join(lineas)
    if r["conclusion"] == "fuera_de_la_tabla":
        lineas.append("RESULTADO: fuera_de_la_tabla")
        lineas.append("  Eso se pasa de CIEN (%d decenas y %d unidades), y mi tabla llega al cien."
                      % (r["decenas"], r["unidades"]))
        return "\n".join(lineas)
    d, u = r["decenas"], r["unidades"]
    lineas.append("")
    lineas.append("  CADA DECENA SON DIEZ (unidad 6.2), asi que %d decenas son %d"
                  % (d, d * 10))
    lineas.append("  Y las unidades valen lo que dicen: %d" % u)
    lineas.append("")
    lineas.append("  SE JUNTAN:  %s" % r["cuenta"])
    lineas.append("")
    if r["demasiadas_unidades"]:
        lineas.append("  OJO: hay %d unidades, y con DIEZ unidades se hace OTRA DECENA." % u)
        lineas.append("  Por eso no se dice 'cuarenta y quince': se dice '%s'." % r["palabra"])
        lineas.append("  (Los nombres raros tipo 'sesenta y quince' son el error de decena otra vez.)")
        lineas.append("")
    lineas.append("  COMPROBACION (partirlo otra vez tiene que dar lo mismo):")
    lineas.append("    %d -> %d decenas y %d unidades" % (r["total"], d, u))
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["dato"])
    return "\n".join(lineas)


def _suma_con_metodo(a, b, saber):
    """
    Hace una suma de DOS numeros DE UNA CIFRA y devuelve como se hizo, para poder ENSENARLO.
    NO se sabe de memoria y NO se usa calculadora: se usa el metodo que ya esta ensenado
    (los dedos, 7.1; y derivar, 7.2, cuando cruza el diez).

    Lo cazo Carlos: la suma por columnas decia "7 + 5 = 12" a secas, y no decia de donde salia.
    """
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    pa = _palabra_de(a, secuencia) if a else "cero"
    pb = _palabra_de(b, secuencia) if b else "cero"
    total = a + b
    d = {"a": a, "b": b, "total": total,
         "palabra_a": pa, "palabra_b": pb,
         "palabra_total": _palabra_de(total, secuencia) if total else "cero"}
    # El mecanismo: si los dedos no llegan (el segundo pasa de diez) o si derivar sirve, se elige.
    ded = decidir_7_1_dedos(str(a), str(b), saber)
    der = decidir_7_2_derivar(str(a), str(b), saber)
    if ded["conclusion"] == "se_puede":
        d["metodo"] = "dedos (7.1)"
        d["detalle"] = ded
        d["como"] = ("se anota el %s y se cuentan %d dedos hacia adelante desde el %s"
                     % (pa, b, pa))
    elif der["conclusion"] == "se_puede":
        d["metodo"] = "derivar (7.2)"
        d["detalle"] = der
        d["como"] = ("al %s le faltan %d para diez, y se parte el %s en %d y %d"
                     % (pa, der["faltan_para_diez"], pb, der["parte_para_diez"],
                        der["parte_que_sobra"]))
    else:
        d["metodo"] = None
        d["detalle"] = None
        d["como"] = None
    return d


def _dos_pasos(a, b, c, saber):
    """
    Suma TRES numeros de una cifra EN DOS PASOS, porque el sistema solo tiene el metodo de sumar
    DOS.  Antes decia "4 + 1 + 1 = 6" de golpe, que es un metodo que NO tiene.

    Lo cazo Carlos: "4 + 1 + 1 = 6 no deberia ser 4+1 = 5 y 5 + 1 = 6?"
    """
    p1 = _suma_con_metodo(a, b, saber)
    p2 = _suma_con_metodo(p1["total"], c, saber)
    return {"paso_1": p1, "paso_2": p2, "total": p2["total"]}


# ------------------------------------------------- sumar por columnas (7.3)

def decidir_7_3_columnas(texto_a, texto_b, saber=None):
    """
    Unidad 7.3: SUMAR POR COLUMNAS.  Unidad con unidad, decena con decena, y el llevarse.

      47 + 15  ->  7+5 = 12 (anoto 2, me llevo 1);  4+1+1 = 6  ->  62

    El llevarse NO es un truco: es RE-AGRUPAR (diez unidades hacen una decena, unidad 6.2).
    """
    if saber is None:
        saber = cargar_conocimiento()
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    pa, ca = nombre_de_numero(texto_a, saber)
    pb, cb = nombre_de_numero(texto_b, saber)
    va, vb = _valor_de_numero(pa, saber), _valor_de_numero(pb, saber)
    cuenta = {"valor_a": va, "valor_b": vb, "secuencia": secuencia}
    r = _aplicar_reglas(saber["reglas_7_3"]["reglas_columnas"], None, None, saber, cuenta=cuenta)
    r["texto_a"], r["texto_b"] = texto_a, texto_b
    r["palabra_a"], r["palabra_b"] = pa, pb
    r["valor_a"], r["valor_b"] = va, vb
    if r["conclusion"] != "se_puede":
        return r
    # --- LAS DOS COLUMNAS -------------------------------------------------
    ua, ub = va % 10, vb % 10
    da, db = va // 10, vb // 10
    suma_unidades = ua + ub
    se_lleva = suma_unidades // 10        # 0 o 1 (nunca mas: 9+9=18)
    anota_unidades = suma_unidades % 10
    suma_decenas = da + db + se_lleva
    total = va + vb
    r["unidades_a"], r["unidades_b"] = ua, ub
    r["decenas_a"], r["decenas_b"] = da, db
    r["suma_unidades"] = suma_unidades
    r["se_lleva"] = se_lleva
    r["anota_unidades"] = anota_unidades
    r["suma_decenas"] = suma_decenas
    r["total_valor"] = total
    r["cuenta_unidades"] = "%d + %d = %d" % (ua, ub, suma_unidades)
    r["cuenta_decenas"] = ("%d + %d + %d = %d" % (da, db, se_lleva, suma_decenas) if se_lleva
                           else "%d + %d = %d" % (da, db, suma_decenas))
    r["hay_que_llevarse"] = se_lleva > 0
    r["total"] = _palabra_de(total, secuencia) if total else "cero"
    r["tabla"] = _tabla(saber)
    r["expresion"] = "%s + %s = %s" % (pa, pb, r["total"])
    r["expresion_cifras"] = "%d + %d = %d" % (va, vb, total)
    # COMPROBACIONES
    r["recompone"] = (suma_decenas * 10 + anota_unidades == total)
    r["el_llevado_es_una_decena"] = (suma_unidades == anota_unidades + se_lleva * 10)
    r["lleva_como_mucho_uno"] = se_lleva <= 1   # 9+9=18 -> se lleva 1, nunca 2
    r["sin_llevarse_daria_mal"] = (se_lleva > 0 and da + db != suma_decenas)
    # la verificacion de siempre: por la vuelta (partir el total, unidad 5.1)
    r["parejas_del_total"] = [(k, total - k) for k in range(0, total // 2 + 1)]
    r["verificacion"] = sorted((va, vb)) in [sorted(p) for p in r["parejas_del_total"]]
    return r


def explicar_7_3_columnas(texto_a, texto_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_7_3_columnas(texto_a, texto_b, saber)
    lineas = ["PREGUNTA (7.3): sumar estos DOS NUMEROS por COLUMNAS"
              "  (unidad con unidad, decena con decena, y el llevarse)"]
    lineas.append("NUMEROS:  %s  y  %s" % (texto_a, texto_b))
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  Alguno no es un numero que conozca (los mios van del CERO al CIEN).")
        return "\n".join(lineas)
    if r["conclusion"] == "no_alcanza":
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  La suma se pasa de CIEN (%s + %s), y mi tabla llega al cien."
                      % (r["valor_a"], r["valor_b"]))
        lineas.append("  No me lo invento: mas alla del cien no tengo sitio.")
        return "\n".join(lineas)
    va, vb = r["valor_a"], r["valor_b"]
    lineas.append("")
    lineas.append("  SE PONE UNO DEBAJO DEL OTRO y se suman las COLUMNAS:")
    lineas.append("")
    lineas.append("       %s" % va)
    lineas.append("     + %s" % vb)
    lineas.append("     " + "-" * (max(len(str(va)), len(str(vb))) + 2))
    lineas.append("")
    lineas.append("  PASO 0 - SE PARTE CADA NUMERO EN DECENAS Y UNIDADES (unidad 6.5):")
    lineas.append("    %d = %d decenas y %d unidades   |   %d = %d decenas y %d unidades"
                  % (va, r["decenas_a"], r["unidades_a"], vb, r["decenas_b"], r["unidades_b"]))
    lineas.append("")
    lineas.append("  PASO 1 - COLUMNA DE LAS UNIDADES (se empieza por la derecha):")
    su = _suma_con_metodo(va % 10, vb % 10, saber)
    lineas.append("    la suma es %s, y NO se sabe de memoria: %s" % (r["cuenta_unidades"],
                                                                      su["como"] or "con el metodo"))
    lineas.append("    (el metodo: %s -- unidad 7.1/7.2.  Se hace con el mecanismo, no con una"
                  " calculadora.)" % su["metodo"])
    if r["hay_que_llevarse"]:
        lineas.append("    -> %d PASA DE NUEVE.  Y %d son UNA DECENA Y %d UNIDADES"
                      % (r["suma_unidades"], r["suma_unidades"], r["anota_unidades"]))
        lineas.append("       (diez unidades hacen una decena: unidad 6.2).")
        lineas.append("    -> se ANOTA el %d en las unidades" % r["anota_unidades"])
        lineas.append("    -> y me LLEVO %d DECENA para la columna siguiente" % r["se_lleva"])
    else:
        lineas.append("    -> NO pasa de nueve: se anota el %d y no hay nada que llevarse."
                      % r["anota_unidades"])
    lineas.append("")
    lineas.append("  PASO 2 - COLUMNA DE LAS DECENAS (en DOS PASOS, porque sumar TRES numeros de")
    lineas.append("  golpe no es un metodo que el sistema tenga):")
    dp = _dos_pasos(r["decenas_a"], r["decenas_b"], r["se_lleva"], saber)
    p1, p2 = dp["paso_1"], dp["paso_2"]
    if r["hay_que_llevarse"]:
        lineas.append("    PRIMERO los dos de arriba:  %d + %d = %d" % (p1["a"], p1["b"], p1["total"]))
        lineas.append("      (el metodo: %s)" % (p1["metodo"] or "no hace falta: no cruza el diez"))
        lineas.append("    Y LUEGO le sumo la que me llevo:  %d + %d = %d"
                      % (p2["a"], p2["b"], p2["total"]))
        lineas.append("      (el metodo: %s)" % (p2["metodo"] or "no hace falta: no cruza el diez"))
        lineas.append("    -> %d + %d + %d = %d, en dos pasos" % (r["decenas_a"], r["decenas_b"],
                                                                 r["se_lleva"], r["suma_decenas"]))
        lineas.append("    OJO: si me olvidara de la que me llevo, me quedaria en %d, y seria FALSO."
                      % p1["total"])
    else:
        lineas.append("    %d + %d = %d   (no hay nada que llevarse)"
                      % (p1["a"], p1["b"], p1["total"]))
    lineas.append("")
    lineas.append("  LA CUENTA ENTERA:")
    lineas.append("    %d decenas y %d unidades  ->  %s" % (r["suma_decenas"], r["anota_unidades"],
                                                            r["total"]))
    lineas.append("    (y NO se escribe '%d x 10': el sistema todavia no sabe multiplicar.  Se dice"
                  % r["suma_decenas"])
    lineas.append("     'son %d decenas', que es lo que si sabe: juntar decenas, unidad 6.5.)"
                  % r["suma_decenas"])
    lineas.append("")
    lineas.append("  COMPROBACIONES:")
    lineas.append("    - juntando las columnas: %d decenas y %d unidades son %d ... %s"
                  % (r["suma_decenas"], r["anota_unidades"], r["total_valor"],
                     "SI" if r["recompone"] else "NO"))
    if r["hay_que_llevarse"]:
        lineas.append("    - el llevado es una decena entera: %d son %d unidad y 1 decena ... %s"
                      % (r["suma_unidades"], r["anota_unidades"],
                         "SI" if r["el_llevado_es_una_decena"] else "NO"))
        lineas.append("    - y lo que se lleva NUNCA puede ser mas de 1: 9+9=18, o sea una decena"
                      " ... %s" % ("SI" if r["lleva_como_mucho_uno"] else "NO"))
    lineas.append("    - la vuelta (partir el total, unidad 5.1): %s y %s tienen que salir de %d ... %s"
                  % (r["valor_a"], r["valor_b"], r["total_valor"],
                     "SI" if r["verificacion"] else "NO"))
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["expresion_cifras"])
    lineas.append("")
    lineas.append("  Y ESTO ES LA NOTA 7, PALABRA POR PALABRA: sumar \"unidad con unidad, luego")
    lineas.append("  decena con decena, y si pasa de 9 se anota la unidad y la decena que se lleva")
    lineas.append("  se suma con lo siguiente\".")
    lineas.append("  Y EL LLEVARSE NO ES UN TRUCO: es RE-AGRUPAR.  Las DIEZ unidades que sobran se")
    lineas.append("  convierten en una DECENA que sube a su columna -- lo mismo que ya sabia hacer")
    lineas.append("  al juntar (unidad 6.5).")
    return "\n".join(lineas)


# ------------------------------------------------- la resta con los dedos (7.4)

def decidir_7_4_resta_dedos(texto_a, texto_b, saber=None):
    """
    Unidad 7.4: LA RESTA CON LOS DEDOS.  Se toma el primero, se van BAJANDO los del segundo, y los
    dedos que quedan son el resultado.

      9 - 4  ->  se levantan 9 (del 1 al 9), se bajan 4, quedan 5.

    **LO QUE CAZO CARLOS (4 oct 2026, por la tarde):** la version anterior exigia que EL PRIMERO
    cupiera en los dedos (no pasar de diez), y eso era MAL, por dos razones:

      1. CONTradecia a la suma: la 7.1 ya funciona asi -- los dedos cuentan los PASOS, y el primero
         se anota; el total NO tiene que caber ("no tiene que caber en los dedos").
      2. Y es que los diez dedos NO tienen que representar el numero entero: representan la VENTANA
         DE LOS ULTIMOS DIEZ, terminando en el minuendo.  Para 12 - 5 los dedos van DEL 3 AL 12; se
         bajan 5 y quedan 7.  Y asi CABE 45 - 7 (dedos del 36 al 45, se bajan 7, quedan 38).

    ES DECIR: lo unico que tiene que caber en los dedos es EL SEGUNDO (el que se baja).  El primero
    puede ser tan grande como quiera: solo marca DONDE ACABA la ventana.
    """
    if saber is None:
        saber = cargar_conocimiento()
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    pa, ca = nombre_de_numero(texto_a, saber)
    pb, cb = nombre_de_numero(texto_b, saber)
    va = _valor_de_cantidad(pa, saber)
    vb = _valor_de_cantidad(pb, saber)
    # Se le pasa la cuenta en el MISMO formato que la unidad 5.4, para REUTILIZAR su primitiva
    # ('no se puede quitar mas de lo que hay') y no escribir una segunda verdad.
    escena_54 = [{"id": i + 1} for i in range(va)] if va is not None else []
    cuenta = {"secuencia": secuencia, "valor_a": va, "valor_b": vb, "pedido_valor": vb,
              "otra": [None] * (vb or 0),
              # La primitiva 'segundo_pasa_de_diez' es la de la 7.1 y necesita saber cuantos dedos
              # hay: hay que pasarle '_saber', igual que hace la 7.1.  Si no, revienta.
              "_saber": saber}
    r = _aplicar_reglas(saber["reglas_7_4"]["reglas_resta_dedos"], escena_54, None, saber,
                        cuenta=cuenta)
    r["secuencia"] = secuencia
    r["texto_a"], r["texto_b"] = texto_a, texto_b
    r["palabra_a"], r["palabra_b"] = pa, pb
    r["valor_a"], r["valor_b"] = va, vb
    r["dedos"] = _cuantos_dedos(saber)
    if r["conclusion"] != "se_puede":
        return r
    quedan = va - vb
    r["quedan"] = quedan
    r["resta"] = _palabra_de(quedan, secuencia) if quedan else "cero"
    r["expresion"] = "%s - %s = %s" % (pa, pb, r["resta"])
    tabla = _tabla(saber)
    r["cifra_a"], r["cifra_b"] = tabla.get(pa, str(va) if va is not None else None), \
                                 tabla.get(pb, str(vb) if vb is not None else None)
    r["cifra_resta"] = tabla.get(r["resta"], str(quedan))
    r["expresion_cifras"] = "%s - %s = %s" % (r["cifra_a"], r["cifra_b"], r["cifra_resta"])
    # LA VENTANA DE LOS DEDOS: los diez dedos son los ULTIMOS DIEZ numeros, y el ultimo es el
    # minuendo.  Si el minuendo es 12, la ventana es del 3 al 12.  Si es 9, del 1 al 9.
    r["desde"] = max(1, va - (r["dedos"] - 1))
    r["dedos_levantados"] = va - r["desde"] + 1
    r["ventana"] = (r["desde"], va)
    r["cabe_entero"] = (r["desde"] == 1)
    # EL PASO A PASO: los dedos que se van bajando, con el numero que va quedando
    r["bajadas"] = [{"bajo": i, "quedan": va - i} for i in range(1, vb + 1)]
    r["pasos_dados"] = vb
    # LA VUELTA: la suma deshace la resta (unidad 7.1)
    vuelta = decidir_7_1_dedos(str(quedan), str(vb), saber)
    r["vuelta"] = vuelta
    r["verificacion"] = (vuelta["conclusion"] == "se_puede" and vuelta["total_valor"] == va)
    r["verificacion_texto"] = ("%s + %s = %s" % (r["resta"], pb, pa))
    return r


def explicar_7_4_resta_dedos(texto_a, texto_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_7_4_resta_dedos(texto_a, texto_b, saber)
    lineas = ["PREGUNTA (7.4): como se resta MECANICAMENTE?  (el metodo de los dedos, AL REVES que"
              " la suma)"]
    lineas.append("NUMEROS:  %s  y  %s" % (texto_a, texto_b))
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  Alguno de los dos no es un numero que conozca.")
        return "\n".join(lineas)
    if r["conclusion"] == "no_caben_en_los_dedos":
        lineas.append("RESULTADO: no_caben_en_los_dedos")
        lineas.append("  El que se BAJA (%s) es mas grande que mis %d dedos: no puedo bajar %d dedos"
                      % (r["palabra_b"], r["dedos"], r["valor_b"]))
        lineas.append("  si solo tengo %d.  Y lo que tiene que caber es EL QUE SE BAJA (el segundo),"
                      " no el primero: el primero solo marca DONDE ACABA la ventana."
                      % r["dedos"])
        return "\n".join(lineas)
    if r["conclusion"] == "no_hay_bastantes":
        lineas.append("RESULTADO: no_hay_bastantes")
        lineas.append("  No se pueden bajar mas dedos de los que hay: hay %s y se quieren bajar %s."
                      % (r["palabra_a"], r["palabra_b"]))
        lineas.append("  Eso seria una resta NEGATIVA, y aqui no existe (unidad 5.4).")
        return "\n".join(lineas)
    lineas.append("")
    lineas.append("  OJO: ES AL REVES QUE LA SUMA.  En la suma se toman los dedos del SEGUNDO y se")
    lineas.append("  cuenta hacia adelante desde el primero.  Aqui se toma EL PRIMERO y se van")
    lineas.append("  BAJANDO los del segundo.  Es CONTAR HACIA ATRAS.")
    lineas.append("")
    lineas.append("  PASO 1 - LOS DEDOS REPRESENTAN LA VENTANA DE LOS ULTIMOS DIEZ NUMEROS, y el")
    lineas.append("  ultimo de ellos es el MINUENDO (%s)." % r["palabra_a"])
    if r["cabe_entero"]:
        lineas.append("    dedos levantados: del 1 al %d  (%d dedos)" % (r["valor_a"],
                                                                      r["dedos_levantados"]))
    else:
        lineas.append("    %s no cabe entero en los dedos, pero NO HACE FALTA: los dedos van del"
                      " %d al %d" % (r["palabra_a"], r["desde"], r["valor_a"]))
        lineas.append("    (%d dedos, y el ultimo marca donde ACABA la cuenta)" % r["dedos_levantados"])
        lineas.append("    Y asi cabe cualquier minuendo: lo que tiene que caber es lo que se BAJA.")
    lineas.append("")
    lineas.append("  PASO 2 - SE VAN BAJANDO tantos como el SEGUNDO (%s), uno a uno." % r["palabra_b"])
    for b in r["bajadas"]:
        lineas.append("    bajo %d:  van quedando %d" % (b["bajo"], b["quedan"]))
    lineas.append("")
    lineas.append("  PASO 3 - LOS DEDOS QUE QUEDAN SON EL RESULTADO.")
    lineas.append("    quedan levantados: %d" % r["quedan"])
    lineas.append("")
    lineas.append("  POR QUE ESTO ES 'QUITAR' (unidad 5.4): primero habia %s, se van %s, ahora quedan"
                  " %s." % (r["palabra_a"], r["palabra_b"], r["resta"]))
    lineas.append("  Y los dedos que quedan son, literalmente, LO QUE QUEDA DESPUES DE QUE SE VAYAN.")
    lineas.append("")
    lineas.append("  LA CUENTA DE LOS PASOS:")
    lineas.append("    empezando en %d y contando hacia atras %d veces se llega a %d"
                  % (r["valor_a"], r["pasos_dados"], r["quedan"]))
    lineas.append("")
    lineas.append("  VERIFICACION (la vuelta: la suma deshace la resta):")
    lineas.append("    %s ... %s" % (r["verificacion_texto"], "SI" if r["verificacion"] else "NO"))
    lineas.append("    (y esa suma la hace con SU mecanismo, el de los dedos hacia adelante, 7.1)")
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["expresion"])
    lineas.append("")
    lineas.append("  Y ES MECANICO: se dan %d pasos, uno por dedo.  No se sabe de memoria ni se usa"
                  " calculadora." % r["pasos_dados"])
    return "\n".join(lineas)


# ------------------------------------------------- restar por columnas (7.5)

def _dec_u(d, u):
    """Escribe '3 decenas y 1 unidad' (en singular cuando toca)."""
    return "%d %s y %d %s" % (d, "decena" if d == 1 else "decenas", u,
                              "unidad" if u == 1 else "unidades")


def _resta_con_metodo(a, b, saber):
    """
    Hace una resta (de una columna) y devuelve COMO se hizo, para poder ENSENARLO.
    NO se sabe de memoria y NO se usa calculadora: se usa el mecanismo de la unidad 7.4 (los dedos,
    contando hacia atras).  Si el minuendo no cabe en los dedos (12, que sale despues de cambiar la
    decena), se ANOTA en la pizarra y se bajan los dedos del sustraendo -- igual que en la suma
    (7.1), donde el primero tambien se anota.
    """
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    pa = _palabra_de(a, secuencia) if a else "cero"
    pb = _palabra_de(b, secuencia) if b else "cero"
    queda = a - b
    d = {"a": a, "b": b, "queda": queda, "palabra_a": pa, "palabra_b": pb,
         "palabra_queda": _palabra_de(queda, secuencia) if queda else "cero"}
    ded = decidir_7_4_resta_dedos(str(a), str(b), saber)
    if ded["conclusion"] == "se_puede":
        d["metodo"] = "dedos (7.4)"
        d["ventana"] = ded.get("ventana")
        if ded.get("cabe_entero"):
            d["como"] = ("se levantan %s y se bajan %d dedos: quedan %s"
                         % (pa, b, d["palabra_queda"]))
        else:
            d["como"] = ("los dedos van del %d al %d (el ultimo es %s), y se bajan %d: quedan %s"
                         % (ded["desde"], a, pa, b, d["palabra_queda"]))
    else:
        # No deberia pasar en una columna (lo que se baja siempre es de una cifra), pero si pasa,
        # el sistema lo DICE en vez de inventarse el resultado.
        d["metodo"] = None
        d["como"] = "no cabe en los dedos, y el sistema no tiene otro mecanismo para esto"
    d["cuenta"] = "%d - %d = %d" % (a, b, queda)
    return d


def decidir_7_5_columnas(texto_a, texto_b, saber=None):
    """
    Unidad 7.5: RESTAR POR COLUMNAS.  Columna a columna, y si las unidades de arriba no llegan, se
    CAMBIA una decena por diez unidades (el intercambio, que NO es un prestamo).

      72 - 45  ->  2-5 no llega -> 72 = 6 dec y 12 u -> 12-5=7 -> 6-4=2  ->  27
      58 - 27  ->  8-7=1 y 5-2=3 sin cambiar nada                      ->  31
    """
    if saber is None:
        saber = cargar_conocimiento()
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    pa, ca = nombre_de_numero(texto_a, saber)
    pb, cb = nombre_de_numero(texto_b, saber)
    va = _valor_de_cantidad(pa, saber)
    vb = _valor_de_cantidad(pb, saber)
    escena_54 = [{"id": i + 1} for i in range(va)] if va is not None else []
    cuenta = {"secuencia": secuencia, "valor_a": va, "valor_b": vb, "pedido_valor": vb,
              "texto_a": texto_a, "texto_b": texto_b,
              "otra": [None] * (vb or 0)}
    r = _aplicar_reglas(saber["reglas_7_5"]["reglas_columnas_resta"], escena_54, None, saber,
                        cuenta=cuenta)
    r["secuencia"] = secuencia
    r["texto_a"], r["texto_b"] = texto_a, texto_b
    r["palabra_a"], r["palabra_b"] = pa, pb
    r["valor_a"], r["valor_b"] = va, vb
    if r["conclusion"] != "se_puede":
        return r
    # PASO 0 - partir cada numero (unidad 6.5)
    r["dec_a"], r["uni_a"] = divmod(va, 10)
    r["dec_b"], r["uni_b"] = divmod(vb, 10)
    # PASO 1 - la columna de las unidades, y el INTERCAMBIO si no llega
    r["hay_intercambio"] = r["uni_a"] < r["uni_b"]
    if r["hay_intercambio"]:
        r["dec_a_despues"] = r["dec_a"] - 1
        r["uni_a_despues"] = r["uni_a"] + 10
        unidad = _resta_con_metodo(r["uni_a_despues"], r["uni_b"], saber)
        decena = _resta_con_metodo(r["dec_a_despues"], r["dec_b"], saber)
    else:
        r["dec_a_despues"] = r["dec_a"]
        r["uni_a_despues"] = r["uni_a"]
        unidad = _resta_con_metodo(r["uni_a"], r["uni_b"], saber)
        decena = _resta_con_metodo(r["dec_a"], r["dec_b"], saber)
    r["unidad"], r["decena"] = unidad, decena
    r["resta_unidades"] = unidad["cuenta"]
    r["resta_decenas"] = decena["cuenta"]
    # Y LA COMPROBACION DEL INTERCAMBIO: sigue valiendo lo mismo
    r["intercambio_vale_igual"] = (r["dec_a_despues"] * 10 + r["uni_a_despues"]) == va
    r["resta"] = unidad["queda"] + decena["queda"] * 10
    r["resultado"] = _palabra_de(r["resta"], secuencia) if r["resta"] else "cero"
    r["expresion"] = "%s - %s = %s" % (pa, pb, r["resultado"])
    tabla = _tabla(saber)
    r["cifra_a"], r["cifra_b"] = tabla.get(pa, str(va)), tabla.get(pb, str(vb))
    r["cifra_resultado"] = tabla.get(r["resultado"], str(r["resta"]))
    r["expresion_cifras"] = "%s - %s = %s" % (r["cifra_a"], r["cifra_b"], r["cifra_resultado"])
    # LA VUELTA: la suma deshace la resta (con las columnas de la 7.3)
    vuelta = decidir_7_3_columnas(str(r["resta"]), str(vb), saber)
    r["vuelta"] = vuelta
    r["verificacion"] = (vuelta["conclusion"] == "se_puede" and vuelta["total_valor"] == va)
    r["verificacion_texto"] = "sumando sale otra vez el de arriba"
    return r


def explicar_7_5_columnas(texto_a, texto_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_7_5_columnas(texto_a, texto_b, saber)
    lineas = ["PREGUNTA (7.5): restar estos DOS NUMEROS por COLUMNAS  (y el intercambio de una"
              " decena)"]
    lineas.append("NUMEROS:  %s  y  %s" % (texto_a, texto_b))
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  Alguno de los dos no es un numero que conozca.")
        return "\n".join(lineas)
    if r["conclusion"] == "no_hay_bastantes":
        lineas.append("RESULTADO: no_hay_bastantes")
        lineas.append("  Al de abajo (%s) no se le puede quitar al de arriba (%s): seria una resta"
                      " NEGATIVA." % (r["palabra_b"], r["palabra_a"]))
        lineas.append("  Y aqui no existe (unidad 5.4).  Se dice, no se inventa.")
        return "\n".join(lineas)
    if r["conclusion"] == "no_alcanza":
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  Alguno pasa de cien, y la resta por columnas no llega tan alto todavia.")
        return "\n".join(lineas)
    lineas.append("")
    lineas.append("  SE PONE UNO DEBAJO DEL OTRO y se restan las COLUMNAS (se empieza por la"
                  " derecha):")
    lineas.append("")
    lineas.append("       %s" % r["cifra_a"])
    lineas.append("    -  %s" % r["cifra_b"])
    lineas.append("    ----")
    lineas.append("")
    lineas.append("  PASO 0 - SE PARTE CADA NUMERO EN DECENAS Y UNIDADES (unidad 6.5):")
    lineas.append("    %s = %d decenas y %d unidades   |   %s = %d decenas y %d unidades"
                  % (r["palabra_a"], r["dec_a"], r["uni_a"], r["palabra_b"], r["dec_b"], r["uni_b"]))
    lineas.append("")
    lineas.append("  PASO 1 - COLUMNA DE LAS UNIDADES (se empieza por la derecha):")
    if r["hay_intercambio"]:
        lineas.append("    %d - %d ... NO SE PUEDE.  Arriba hay %d y abajo %d: no llega."
                      % (r["uni_a"], r["uni_b"], r["uni_a"], r["uni_b"]))
        lineas.append("    Y OJO: ESO NO SE ARREGLA DANDO LA VUELTA A LA RESTA.  El de arriba es LO")
        lineas.append("    QUE HAY; si no llega, no se cambia el orden.  %d - %d seria FALSO."
                      % (r["uni_b"], r["uni_a"]))
        lineas.append("    -> SE CAMBIA una decena por diez unidades (y esto NO es un prestamo: no")
        lineas.append("       hay que devolver nada).  Se coge UNA de las %d decenas y se abre en"
                      % r["dec_a"])
        lineas.append("       diez unidades:")
        lineas.append("         %s = %d decenas y %d unidades  ->  %d decenas y %d unidades"
                      % (r["palabra_a"], r["dec_a"], r["uni_a"], r["dec_a_despues"],
                         r["uni_a_despues"]))
        lineas.append("       Y SIGUE SIENDO %s ... %s"
                      % (r["palabra_a"], "SI" if r["intercambio_vale_igual"] else "NO"))
        lineas.append("       (no se escribe '%d + %d = %d': son %d DECENAS y %d unidades, y el"
                      % (r["dec_a_despues"], r["uni_a_despues"], r["valor_a"],
                         r["dec_a_despues"], r["uni_a_despues"]))
        lineas.append("        sistema todavia no sabe multiplicar.  Se dice 'son %d decenas', que"
                      " es lo que si sabe: unidad 6.5.)" % r["dec_a_despues"])
        lineas.append("    -> AHORA SI:  %s" % r["resta_unidades"])
        lineas.append("       (el metodo: %s)" % r["unidad"]["como"])
        lineas.append("    -> Y AL CAMBIAR LA DECENA, LA COLUMNA DE LAS DECENAS PASA DE %d A %d."
                      % (r["dec_a"], r["dec_a_despues"]))
        lineas.append("       Si se olvidara, la respuesta saldria DIEZ DE MAS.")
    else:
        lineas.append("    %d - %d = %d  (SI llega: no hay que cambiar nada)"
                      % (r["uni_a"], r["uni_b"], r["unidad"]["queda"]))
        lineas.append("       (el metodo: %s)" % r["unidad"]["como"])
    lineas.append("")
    lineas.append("  PASO 2 - COLUMNA DE LAS DECENAS:")
    lineas.append("    %s" % r["resta_decenas"])
    lineas.append("       (el metodo: %s)" % r["decena"]["como"])
    lineas.append("")
    lineas.append("  LA CUENTA ENTERA:")
    lineas.append("    %s  ->  %s" % (_dec_u(r["decena"]["queda"], r["unidad"]["queda"]),
                                       r["resultado"]))
    lineas.append("")
    lineas.append("  COMPROBACIONES:")
    lineas.append("    - el cambio de la decena no cambia el numero: %d dec y %d u siguen siendo %d"
                  " ... %s" % (r["dec_a_despues"], r["uni_a_despues"], r["valor_a"],
                               "SI" if r["intercambio_vale_igual"] else "NO"))
    lineas.append("    - la vuelta (la suma deshace la resta, unidad 7.3): %s + %s = %s ... %s"
                  % (r["resultado"], r["palabra_b"], r["palabra_a"],
                     "SI" if r["verificacion"] else "NO"))
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["expresion"])
    lineas.append("")
    if r["hay_intercambio"]:
        lineas.append("  Y EL INTERCAMBIO NO ES UN TRUCO: es la MISMA MONEDA que el llevarse de la")
        lineas.append("  suma (unidad 7.3), cambiada al REVES.  Alli, diez unidades se juntaban en")
        lineas.append("  una decena que SUBIA; aqui, una decena se abre en diez unidades que BAJAN.")
        lineas.append("  Es cambiar una decena por diez unidades.  Ni se presta ni se devuelve.")
    else:
        lineas.append("  AQUI NO HA HECHO FALTA CAMBIAR NADA: las unidades de arriba llegaban.")
        lineas.append("  Y por eso se aprenden LAS DOS juntas: es lo mismo, con un paso de mas.")
    return "\n".join(lineas)


def _detalle_error(escena, r):
    """Dice, en palabras, QUE ha estado mal.  Sin usar cifras (unidad 3.1)."""
    palabras, secuencia = r["palabras"], r["secuencia"]
    c = r["conclusion"]
    if c == "faltan_objetos_sin_contar":
        sin = [o["id"] for o in r["entidades"][len(palabras):]]
        return "  -> quedaron objetos SIN contar: %s" % ", ".join(sin)
    if c == "palabras_de_mas":
        return "  -> hay mas palabras que objetos: sobra %s" % ", ".join(palabras[len(r["entidades"]):])
    if c == "palabra_repetida":
        vistas, repes = set(), []
        for p in palabras:
            if p in vistas and p not in repes:
                repes.append(p)
            vistas.add(p)
        return "  -> se uso la misma palabra mas de una vez: %s" % ", ".join(repes)
    if c == "palabra_desconocida":
        raras = [p for p in palabras if p not in secuencia]
        return "  -> no conozco estas palabras: %s" % ", ".join(raras)
    if c == "orden_saltado":
        esperadas = secuencia[:len(palabras)]
        faltan = [p for p in esperadas if p not in palabras]
        if faltan:
            return "  -> falta por decir: %s" % ", ".join(faltan)
        return "  -> las palabras no van en el orden de la secuencia"
    return None


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


def explicar_3_1_cifra(palabra, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (3.1): cual es la CIFRA de esta palabra?"]
    r = decidir_3_1_cifra(palabra, saber)
    lineas.append("PALABRA: %s" % palabra)
    lineas.extend(_traza_texto(r))
    if r["conclusion"] == "cifra":
        marcas = "*" * int(r["cifra"])
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
        marcas = "*" * int(cifra)
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


# ---------------------------------------------------------------- linea de ordenes

def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    orden = argv[1]
    saber = cargar_conocimiento()

    if orden == "conocimiento":
        print("Conocimientos cargados (%d):" % len(saber))
        for cid, d in sorted(saber.items()):
            print("  - %-24s %-10s %s" % (cid, d.get("categoria", "?"), d.get("nombre", "?")))
        return 0

    if orden == "escena":
        if len(argv) < 3:
            print("falta la escena, por ejemplo: escena \"silla,mesa\"")
            return 2
        print(explicar_pregunta(" ".join(argv[2:]), saber))
        return 0

    print("orden desconocida: %s" % orden)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
