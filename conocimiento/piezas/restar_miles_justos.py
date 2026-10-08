# -*- coding: utf-8 -*-
"""Pieza de calculo: RESTAR MILES JUSTOS (paso N.4; NCETM 1.26, punto 4).  623 000 - 278 000: 623 mil menos
278 mil = 345 mil.  El mil se cuenta como UNA cosa."""

PIEZA = {
    "id": "restar_miles_justos",
    "nombre": "contar miles hacia atras",
    "unidad": "N.4",
    "responde": "restar",
    "rapidez": 3,
    "que_hace": "si los dos son miles justos, se restan los miles como si fueran cosas",
    "condiciones": [
        ("los_dos_son_miles_justos", "no son los dos miles justos (345 000, 2 000...)"),
        ("el_de_abajo_no_es_mayor", "se quitaria mas de lo que hay (no hay restas negativas, 5.4)"),
        ("pocos_miles_para_contarlos", "son mas de 999 miles (y no son millones justos): contarlos uno a uno serian miles de pasos (N.6)"),
    ],
    "usa": [],
}


def _cosas(u, a, b):
    """Los miles como cosas; y si los dos son millones justos, los MILLONES como cosas (N.6; NCETM 1.30, punto 1)."""
    if all(len(u.cifras_de(x)) >= 7 and u.cifras_de(x)[:6] == [0, 0, 0, 0, 0, 0] for x in (a, b)):
        return 6, "millones"
    return 3, "mil"


def _n(k, nombre):
    return "%d %s" % (k, "millon" if nombre == "millones" and k == 1 else nombre)


def hacer(s, u):
    ceros, nombre = _cosas(u, s["a"], s["b"])
    ma, mb = u.escribir_cifras(u.cifras_de(s["a"])[ceros:]), u.escribir_cifras(u.cifras_de(s["b"])[ceros:])
    m = u.leer(u.contar_hasta(u.decir(mb), u.decir(ma)))   # de mb a ma, contando hacia arriba (P.6)
    total = u.escribir_cifras([0 for _ in range(ceros)] + u.cifras_de(m)) if m else 0
    adelante = u.sumar_por_columnas(m, mb)
    return {"valor": total, "metodo": "contar %s (%s)" % ("millones" if ceros == 6 else "miles", "N.6" if ceros == 6 else "N.4"),
            "cuenta": "%d - %d: %s - %s = %s (%d - %d = %d) = %d"
                      % (s["a"], s["b"], _n(ma, nombre), _n(mb, nombre), _n(m, nombre), ma, mb, m, total),
            "vuelta": "%s + %s = %s" % (_n(m, nombre), _n(mb, nombre), _n(adelante, nombre)), "vuelta_ok": adelante == ma}
