# -*- coding: utf-8 -*-
"""Pieza de calculo: SUMAR CENTENAS JUSTAS (paso N.3; NCETM 1.22, punto 2: 'al sumar multiplos de 100, el
resultado es siempre un multiplo de 100').  300 + 800: son 3 centenas y 8 centenas; 3 + 8 = 11, asi que
11 centenas: 1100.  Es el 'unitising' de siempre (6.2, la centena 6.7): la centena se cuenta como UNA cosa."""

PIEZA = {
    "id": "sumar_centenas_justas",
    "nombre": "contar centenas (como cosas)",
    "unidad": "N.3",
    "responde": "sumar",
    "rapidez": 4,
    "que_hace": "si los dos son centenas justas (300, 800...), se suman las centenas como si fueran cosas",
    "condiciones": [
        ("los_dos_son_centenas_justas", "no son los dos centenas justas (300, 800, 2500...)"),
        ("el_total_tiene_nombre", "el total se pasa de mi lista"),
    ],
    "usa": [],
}


def _centenas(u, n):
    return u.escribir_cifras(u.cifras_de(n)[2:])          # 2500 -> 25 (se tapan decenas y unidades)


def hacer(s, u):
    ca, cb = _centenas(u, s["a"]), _centenas(u, s["b"])
    c = u.sumar_por_columnas(ca, cb)                       # las centenas, como cosas (el mecanismo)
    total = u.escribir_cifras([0, 0] + u.cifras_de(c))    # 11 centenas -> 1100
    atras = u.leer(u.contar_hasta(u.decir(cb), u.decir(c)))  # la vuelta: de cb a c, contando hacia arriba
    return {"valor": total, "metodo": "contar centenas (N.3)",
            "cuenta": "%d + %d: %d centenas + %d centenas = %d centenas (%d + %d = %d, por columnas) = %d"
                      % (s["a"], s["b"], ca, cb, c, ca, cb, c, total),
            "vuelta": "%d - %d: %d centenas - %d centenas = %d centenas" % (total, s["b"], c, cb, atras),
            "vuelta_ok": atras == ca}
