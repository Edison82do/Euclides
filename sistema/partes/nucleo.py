# -*- coding: utf-8 -*-
"""
Euclides - Nucleo: lectura de los .kn, escenas y atributos (0.1, 0.2).

Este archivo es UNA PARTE del motor.  No se importa suelto: lo carga sistema/motor.py,
que junta todas las partes en un solo espacio de nombres (por eso aqui se usan funciones
definidas en otras partes sin importarlas).  Ver sistema/partes/__init__.py.
"""

import os  # noqa: F401
import sys  # noqa: F401


# RAIZ del proyecto: sistema/partes/ -> sistema/ -> E:\Euclides
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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


_CACHE_SABER = {}


def cargar_conocimiento(directorio=DIR_CONOCIMIENTO):
    """Carga todos los .kn del directorio. Devuelve {id: conocimiento}.

    Se lee UNA vez y se guarda: muchas funciones se llaman sin 'saber' y antes cada llamada volvia a
    leer los 68 archivos del disco (en una prueba, 1.632 aperturas = 3,4 s).  Si cualquier .kn
    cambia (fecha o tamano), se vuelve a leer, asi que editar un .kn sigue funcionando al momento."""
    try:
        firma = tuple(sorted((e.name, e.stat().st_mtime_ns, e.stat().st_size)
                             for e in os.scandir(directorio) if e.name.endswith(".kn")))
    except OSError:
        firma = None
    guardado = _CACHE_SABER.get(directorio)
    if firma is not None and guardado and guardado[0] == firma:
        return guardado[1]
    saber = _cargar_de_disco(directorio)
    if firma is not None:
        _CACHE_SABER[directorio] = (firma, saber)
    return saber


def _cargar_de_disco(directorio):
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
        # PASO N.3 (4.o, NCETM 1.22): con el millar la lista llega a DIEZ MIL, con la misma regla.
        if "el_millar" in saber:
            palabras = _secuencia_hasta_diez_mil(saber)
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
    por_base = {}     # (solo para no recorrer TODAS las entidades por cada mencion: mismo resultado)
    for o in escena:
        base = o["id"]
        for e in por_base.get(base, ()):
            if not _se_contradicen(e["atributos"], o["atributos"]):
                for k, v in o["atributos"].items():
                    e["atributos"].setdefault(k, v)
                e["menciones"] += 1
                break
        else:
            nueva = {"base": base, "atributos": dict(o["atributos"]), "menciones": 1}
            entidades.append(nueva)
            por_base.setdefault(base, []).append(nueva)

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
