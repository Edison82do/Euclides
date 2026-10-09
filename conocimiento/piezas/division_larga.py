# -*- coding: utf-8 -*-
"""Pieza de DIVIDIR (paso M.18; NCETM 2.24, punto 2; Common Core 5.NBT.B.6, 6.NS.B.2): LA DIVISION LARGA, entre un
divisor de DOS cifras, cuando el cociente es de 10 o mas.  Primero la LISTA DE LOS MULTIPLOS del divisor (sumandolo una
y otra vez: no hace falta saberse la tabla del 24).  De IZQUIERDA a derecha: se toman cifras hasta que cabe el divisor;
en cada paso el multiplo mas grande que cabe, la RESTA debajo, y se BAJA la cifra siguiente; si el divisor no cabe,
un 0 en el cociente (2448 : 24 = 102, no 12).  Lo que queda al final es el resto.
           356
         -----
    24 | 8544
         72          85 centenas : 24 -> 3 centenas (72), sobran 13
         --
         134         bajo el 4: 134 decenas : 24 -> 5 decenas (120), sobran 14
         120
         ---
          144        bajo el 4: 144 unidades : 24 -> 6 (144), no sobra nada
          144
          ---
            0
LA VUELTA (con la operacion contraria): el cociente por el divisor, mas el resto, da el dividendo; y el resto es menor
que el divisor."""

PIEZA = {
    "id": "division_larga",
    "nombre": "la division larga (la lista de multiplos, restar y bajar)",
    "unidad": "M.18",
    "responde": "dividir",
    "rapidez": 9.5,
    "que_hace": "con la lista de multiplos del divisor: en cada sitio el que cabe, la resta debajo y se baja la cifra siguiente",
    "condiciones": [
        ("el_divisor_es_de_dos_cifras_y_el_cociente_pasa_de_nueve",
         "el divisor no es de dos cifras o el cociente no llega a 10 (eso se hace contando de divisor en divisor)"),
    ],
    "usa": ["sumar", "restar", "multiplicar"],
}

_SITIO = ("unidades", "decenas", "centenas", "millares", "decenas de millar", "centenas de millar", "millones")
_UNO = {"unidades": "unidad", "decenas": "decena", "centenas": "centena", "millares": "millar",
        "decenas de millar": "decena de millar", "centenas de millar": "centena de millar", "millones": "millon"}


def _n(n, sitio):
    return "%d %s" % (n, _UNO[sitio] if n == 1 else sitio)


def _cabe(u, lista, d, actual):
    """El multiplo mas grande del divisor que cabe en 'actual' (comparando con el mecanismo).  (veces, multiplo).
    La LISTA DE LOS MULTIPLOS (1 x d, 2 x d ... 9 x d) se va escribiendo cuando hace falta, sumando d al ultimo
    (por columnas, con el mecanismo): no hace falta saberse la tabla del 24."""
    q, p = 0, 0
    for k, veces in enumerate(("uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve")):
        if k == len(lista):
            lista.append(u.sumar_por_columnas(lista[-1], d) if lista else d)
        m = lista[k]
        if m != actual and u.viene_despues(u.decir(m), u.decir(actual)):
            break
        q, p = u.leer(veces), m
    return q, p


def hacer(s, u):
    t, d = s["total"], s["divisor"]
    lista = []
    cif = list(reversed(u.cifras_de(t)))                     # de IZQUIERDA a derecha
    sitios = list(reversed(_SITIO[:len(cif)]))
    cociente, pasos, filas, actual = [], [], [], 0
    for i, (c, sitio) in enumerate(zip(cif, sitios)):
        cs = [c]
        cs.extend(u.cifras_de(actual) if actual else [])
        bajado = bool(cociente)
        actual = u.escribir_cifras(cs)
        q, p = _cabe(u, lista, d, actual)
        if not q and not cociente:
            pasos.append("%s : %d no cabe ni una vez: tomo la cifra siguiente" % (_n(actual, sitio), d))
            continue
        resto = 0 if p == actual else (u.usar("restar", a=actual, b=p)["valor"] if q else actual)
        if q:
            pasos.append("%s%s : %d -> %s (%d x %d = %d), %d - %d = %d"
                         % ("bajo el %d: " % c if bajado else "", _n(actual, sitio), d, _n(q, sitio), q, d, p, actual,
                            p, resto))
        else:
            pasos.append("bajo el %d: %s : %d no cabe: un 0 en el cociente (en las %s)"
                         % (c, _n(actual, sitio), d, sitio))
        filas.append((i, actual, p, resto, bajado))
        cociente.append(q)
        actual = resto
    q_total = u.escribir_cifras(list(reversed(cociente)))
    # el dibujo de la larga (se mira lo escrito, no se calcula)
    T = str(t)
    margen = "%d | " % d
    ancho = len("%s%s" % (margen, T))
    dibujo = [str(q_total).rjust(ancho), "".join("-" for _ in T).rjust(ancho), "%s%s" % (margen, T)]
    for i, antes, p, resto, bajado in filas:
        w = len("%s%s" % (margen, T[:i + 1]))
        if bajado:
            dibujo.append(str(antes).rjust(w))
        dibujo.extend([str(p).rjust(w), "".join("-" for _ in str(antes)).rjust(w)])
    dibujo.append(str(actual).rjust(ancho))
    # LA VUELTA: cociente x divisor + resto = dividendo, y el resto menor que el divisor
    m = u.usar("multiplicar", a=q_total, b=d)["valor"]
    vuelta = u.usar("sumar", a=m, b=actual)["valor"] if actual else m
    menor = actual != d and not u.viene_despues(u.decir(actual), u.decir(d))
    if actual:
        pasos.append("al final sobra%s %d: es el RESTO" % ("" if actual == 1 else "n", actual))
    return {"valor": q_total, "resto": actual, "metodo": "la division larga (M.18; NCETM 2.24)",
            "cuenta": "%s; los multiplos de %d que escribo: %s; %s" % ("; ".join(dibujo), d, ", ".join(str(x) for x in lista),
                                                          "; ".join(pasos)),
            "dibujo": dibujo,
            "vuelta": "%d x %d%s = %d%s" % (q_total, d, " + %d" % actual if actual else "", vuelta,
                                            "" if menor else " (y el resto no es menor que %d)" % d),
            "vuelta_ok": vuelta == t and menor,
            "vuelta_explicada": "con la operacion contraria: el cociente por %d%s vuelve a dar %d"
                                % (d, ", mas el resto," if actual else "", t)}
