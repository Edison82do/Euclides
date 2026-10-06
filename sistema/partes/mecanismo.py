# -*- coding: utf-8 -*-
"""
Euclides - EL MECANISMO: como calcula el sistema SIN calculadora (decision de Carlos, 4 oct 2026:
"este sistema debe hacerlo mecanicamente hasta nuevo aviso").

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

LO UNICO QUE SABE HACER LA MAQUINA, de verdad, son tres cosas de nino pequeno:
  1. RECITAR: dada una palabra de la lista de contar, decir la SIGUIENTE (o la ANTERIOR).
     La lista es cero, uno, dos ... mil, construida con las reglas de la 6.1 y la 6.7.
  2. LEVANTAR DEDOS: un dedo por cada palabra recitada desde 'uno'.  Hay DIEZ dedos con nombre;
     si se acaban antes de llegar, no caben.
  3. LEER Y ESCRIBIR CIFRAS: el valor de una palabra es su SITIO en la lista (eso es el principio
     cardinal, 2.4) y una cifra escrita se lee simbolo a simbolo (3.1 / 6.3).
Con eso, y SOLO con eso, se construye todo lo demas:
  - sumar con los dedos (7.1): anoto el primero, levanto los dedos del segundo, y por cada dedo
    que bajo digo la palabra SIGUIENTE.  Donde me paro es el total.
  - restar con los dedos (7.4): igual, pero diciendo la ANTERIOR.
  - hacer diez (7.2): cuento cuantos le faltan al primero para 'diez', parto el segundo...
  - las columnas (7.3 / 7.5 / 7.6): cada columna es una cuenta de dedos; "pasa de nueve" es que la
    palabra viene DESPUES de 'nueve' en la lista; lo que se anota es lo que hay que contar desde
    'diez' hasta ahi.
En NINGUN sitio del camino de la respuesta hay un "a + b" de Python.  Python se usa para leer
(el sitio de una palabra) y para las COMPROBACIONES de las pruebas, que son el testigo externo.
"""

import os  # noqa: F401
import sys  # noqa: F401

DEDOS_CON_NOMBRE = ("menique izquierdo", "anular izquierdo", "corazon izquierdo",
                    "indice izquierdo", "pulgar izquierdo", "pulgar derecho", "indice derecho",
                    "corazon derecho", "anular derecho", "menique derecho")


def lista_de_contar(saber):
    """cero, uno, dos ... mil.  Construida una vez (la lista es la de la 6.1/6.7, con el cero de 3.2)."""
    if "_lista_con_cero" not in saber:
        lista = ["cero"] + list(saber["secuencia_de_conteo"]["palabras"])
        saber["_lista_con_cero"] = lista
        saber["_sitio_en_la_lista"] = {w: i for i, w in enumerate(lista)}
    return saber["_lista_con_cero"]


def techo(saber):
    """La ULTIMA palabra de la lista: hasta donde se contar (cien en la 6.1, mil en la 6.7, diez mil en
    la N.3).  Los mensajes de 'no me alcanza' la dicen de aqui, no escrita a mano."""
    return lista_de_contar(saber)[-1]


def leer(palabra, saber):
    """El VALOR de una palabra es su SITIO en la lista (principio cardinal).  Solo lectura."""
    lista_de_contar(saber)
    return saber["_sitio_en_la_lista"].get(palabra)


def decir(valor, saber):
    """La palabra que esta en ese sitio de la lista (lo contrario de leer)."""
    lista = lista_de_contar(saber)
    return lista[valor] if valor is not None and 0 <= valor < len(lista) else None


def siguiente(palabra, saber):
    lista = lista_de_contar(saber)
    i = saber["_sitio_en_la_lista"].get(palabra)
    return lista[i + 1] if i is not None and i + 1 < len(lista) else None


def anterior(palabra, saber):
    lista = lista_de_contar(saber)
    i = saber["_sitio_en_la_lista"].get(palabra)
    return lista[i - 1] if i is not None and i > 0 else None


def viene_despues(p, q, saber):
    """p es MAYOR que q: en la lista viene despues (unidad 4.2)."""
    lista_de_contar(saber)
    s = saber["_sitio_en_la_lista"]
    return s[p] > s[q]


def levantar_dedos(palabra, saber):
    """Se recita desde 'uno' hasta 'palabra' levantando un dedo por palabra.
    Devuelve [(dedo, palabra_dicha), ...] o None si se acaban los dedos antes de llegar."""
    if palabra == "cero":
        return []
    levantados = []
    dicha = "uno"
    for dedo in DEDOS_CON_NOMBRE:
        levantados.append((dedo, dicha))
        if dicha == palabra:
            return levantados
        dicha = siguiente(dicha, saber)
        if dicha is None:
            return None
    return None                       # se acabaron los dedos y no se llego


def _contar(desde, cuantos, saber, paso, con_dedos=True):
    """El corazon del mecanismo: desde 'desde', dar 'cuantos' pasos (siguiente o anterior).
    Con dedos: un dedo por paso (maximo diez).  Sin dedos: se lleva la cuenta recitando
    uno, dos, tres... a la vez (como cuando se cuenta con marcas)."""
    if con_dedos:
        dedos = levantar_dedos(cuantos, saber)
        if dedos is None:
            return {"conclusion": "no_caben_en_los_dedos"}
    else:
        dedos = []
        marca = "uno"
        while cuantos != "cero":
            dedos.append(("marca", marca))
            if marca == cuantos:
                break
            marca = siguiente(marca, saber)
            if marca is None:
                return {"conclusion": "no_alcanza"}
    actual = desde
    pasos = []
    for dedo, nombre in dedos:        # se baja un dedo y se dice la palabra de al lado
        nueva = paso(actual, saber)
        if nueva is None:
            return {"conclusion": "no_alcanza" if paso is siguiente else "no_hay_bastantes",
                    "pasos": pasos}
        actual = nueva
        pasos.append({"dedo": dedo, "dedo_numero": nombre, "dice": actual})
    return {"conclusion": "se_puede", "resultado": actual, "pasos": pasos,
            "dedos": [d for d, _ in dedos]}


def contar_adelante(desde, cuantos, saber, con_dedos=True):
    return _contar(desde, cuantos, saber, siguiente, con_dedos)


def contar_atras(desde, cuantos, saber, con_dedos=True):
    return _contar(desde, cuantos, saber, anterior, con_dedos)


def contar_hasta(desde, hasta, saber):
    """Cuantos pasos hay de 'desde' a 'hasta' contando hacia adelante (5.5: el hueco).
    Devuelve la PALABRA de los pasos ('cero' si son iguales), o None si 'hasta' va antes."""
    if desde == hasta:
        return "cero"
    if not viene_despues(hasta, desde, saber):
        return None
    marca = "cero"
    actual = desde
    while actual != hasta:
        actual = siguiente(actual, saber)
        marca = siguiente(marca, saber)
    return marca


def cifras_de(valor):
    """Las cifras de un numero ESCRITO, de derecha a izquierda (unidades primero).
    Es LEER la cifra simbolo a simbolo, no calcular: 247 -> [7, 4, 2]."""
    return [int(c) for c in reversed(str(valor))]


def escribir_cifras(cifras):
    """Lo contrario: las cifras por sitio (unidades primero) se ESCRIBEN una al lado de otra."""
    texto = "".join(str(c) for c in reversed(cifras)).lstrip("0")
    return int(texto) if texto else 0


def subir_una_decena(valor, saber):
    """SALTAR DE DIEZ EN DIEZ (paso 4): 47 -> 57.  Es ESCRIBIR, no contar: la cifra de las decenas
    pasa a la siguiente; si era un nueve se vuelve cero y la de al lado sube (como en el
    cuentakilometros).  None si se sale de la lista."""
    return _subir_en_el_sitio(valor, 1, saber)


def subir_una_centena(valor, saber):
    """SALTAR DE CIEN EN CIEN (paso N.1; 2.NBT.B.8): 250 -> 350, escribiendo la cifra de las centenas."""
    return _subir_en_el_sitio(valor, 2, saber)


def saltar(desde, de, saber):
    """Un SALTO de 'de' (dos, cinco, diez, cien) desde 'desde' (paso N.1; 2.NBT.A.2).
    De dos y de cinco: se recita en voz baja con los dedos y se dice el ultimo.  De diez y de cien:
    se ESCRIBE la cifra del sitio (sin contar diez ni cien pasos).  None si se sale de la lista."""
    if de == "diez":
        return subir_una_decena(desde, saber)
    if de == "cien":
        return subir_una_centena(desde, saber)
    if de == "mil":                                   # paso N.3: de mil en mil, la cifra de los millares
        return _subir_en_el_sitio(desde, 3, saber)
    p = decir(desde, saber)
    for _ in levantar_dedos(de, saber) or []:
        p = siguiente(p, saber)
        if p is None:
            return None
    return leer(p, saber)


def _subir_en_el_sitio(valor, i, saber):
    cif = cifras_de(valor)
    while True:
        while len(cif) <= i:
            cif.append(0)
        if cif[i] != 9:
            cif[i] = leer(siguiente(decir(cif[i], saber), saber), saber)
            break
        cif[i] = 0
        i = i + 1
    total = escribir_cifras(cif)
    return total if decir(total, saber) is not None else None


def bajar_una_decena(valor, saber):
    """Lo contrario: 77 -> 67.  Si la cifra de las decenas es un cero, se vuelve nueve y la de al
    lado baja (como al restar a traves de un cero).  None si no hay una decena que quitar."""
    cif = cifras_de(valor)
    i = 1
    while True:
        if len(cif) <= i:
            return None
        if cif[i] != 0:
            cif[i] = leer(anterior(decir(cif[i], saber), saber), saber)
            return escribir_cifras(cif)
        cif[i] = 9
        i = i + 1


# ------------------------------------------------- piezas compuestas (todas con lo de arriba)

def coleccion_de(palabra, saber):
    """Una coleccion de tantas marcas como dice la palabra: se recita desde 'uno' poniendo una
    marca por palabra (como hacer palotes).  Para cuando una regla necesita 'un monton de N'."""
    marcas = []
    if palabra in (None, "cero"):
        return marcas
    m = "uno"
    while m is not None:
        marcas.append({"id": m})
        if m == palabra:
            return marcas
        m = siguiente(m, saber)
    return marcas


def contar_todo(*colecciones):
    """Se juntan las colecciones y se cuentan TODAS juntas (la estrategia 'contar todo', 5.2)."""
    junta = []
    for c in colecciones:
        junta.extend(c)
    return len(junta)


def _rellenar(cifras, n):
    cifras = list(cifras)
    while len(cifras) < n:
        cifras.append(0)
    return cifras


def sumar_por_columnas(a, b, saber):
    """La suma por columnas, sin explicacion (para las CONDICIONES: 'se pasaria del techo?').
    Cada columna con los dedos; si pasa de nueve se anota lo que hay desde 'diez' y se lleva uno.
    Devuelve el total, o None si no hay palabra para el (se sale de la lista)."""
    ca, cb = cifras_de(a), cifras_de(b)
    n = max(len(ca), len(cb))
    ca, cb = _rellenar(ca, n), _rellenar(cb, n)
    lleva = False
    res = []
    for x, y in zip(ca, cb):
        s = contar_adelante(decir(x, saber), decir(y, saber), saber)["resultado"]
        if lleva:
            s = siguiente(s, saber)
        if viene_despues(s, "nueve", saber):
            res.append(leer(contar_hasta("diez", s, saber), saber))
            lleva = True
        else:
            res.append(leer(s, saber))
            lleva = False
    if lleva:
        res.append(1)
    total = escribir_cifras(res)
    return total if decir(total, saber) is not None else None


def juntar_decenas(d, u, saber):
    """d decenas y u unidades: la cifra de las decenas con un cero detras (4 -> 40) y desde ahi se
    cuentan las unidades una a una.  Devuelve el numero, o None si se sale de la lista."""
    base = escribir_cifras([0] + cifras_de(d))
    if decir(base, saber) is None:
        return None
    c = contar_adelante(decir(base, saber), decir(u, saber), saber, con_dedos=False)
    return leer(c["resultado"], saber) if c["conclusion"] == "se_puede" else None


def parejas_que_suman(total, saber):
    """Todas las maneras de partir 'total' en DOS (sin repetir el orden), mecanicas: una parte va
    subiendo desde cero, la otra es lo que queda contando hacia atras; se para cuando se cruzan."""
    pt = decir(total, saber)
    out = []
    k = "cero"
    while k is not None:
        m = contar_atras(pt, k, saber, con_dedos=False).get("resultado")
        if m is None or viene_despues(k, m, saber):
            break
        out.append((leer(k, saber), leer(m, saber)))
        if k == m:
            break
        k = siguiente(k, saber)
    return out
