# -*- coding: utf-8 -*-
"""Pieza de calculo: SUMAR MILES JUSTOS (paso N.4; NCETM 1.26, punto 4: 'lo que sirve para calcular hasta
1000 sirve para los multiplos de 1000 hasta un millon').  345 000 + 278 000: son 345 MIL y 278 MIL;
345 + 278 = 623, asi que 623 MIL.  El mil se cuenta como UNA cosa (como la decena, la centena, el millar)."""

PIEZA = {
    "id": "sumar_miles_justos",
    "nombre": "contar miles (como cosas)",
    "unidad": "N.4",
    "responde": "sumar",
    "rapidez": 3,
    "que_hace": "si los dos son miles justos (345 000, 278 000), se suman los miles como si fueran cosas",
    "condiciones": [
        ("los_dos_son_miles_justos", "no son los dos miles justos (345 000, 2 000...)"),
        ("el_total_tiene_nombre", "el total se pasa de lo que se"),
    ],
    "usa": [],
}


def _cosas(u, a, b):
    """Los miles como cosas; y si los dos son millones justos, los MILLONES como cosas (N.6; NCETM 1.30, punto 1:
    2 millones + 3 millones = 5 millones)."""
    if all(len(u.cifras_de(x)) >= 7 and u.cifras_de(x)[:6] == [0, 0, 0, 0, 0, 0] for x in (a, b)):
        return 6, "millones"
    return 3, "mil"


def _n(k, nombre):
    return "%d %s" % (k, "millon" if nombre == "millones" and k == 1 else nombre)


def hacer(s, u):
    ceros, nombre = _cosas(u, s["a"], s["b"])
    ma, mb = u.escribir_cifras(u.cifras_de(s["a"])[ceros:]), u.escribir_cifras(u.cifras_de(s["b"])[ceros:])
    m = u.sumar_por_columnas(ma, mb)                       # las cosas, como cosas (el mecanismo)
    total = u.escribir_cifras([0 for _ in range(ceros)] + u.cifras_de(m))
    atras = u.sumar_por_columnas(mb, ma)                   # la vuelta: en el otro orden
    return {"valor": total, "metodo": "contar %s (%s)" % ("millones" if ceros == 6 else "miles", "N.6" if ceros == 6 else "N.4"),
            "cuenta": "%d + %d: %s + %s = %s (%d + %d = %d) = %d"
                      % (s["a"], s["b"], _n(ma, nombre), _n(mb, nombre), _n(m, nombre), ma, mb, m, total),
            "vuelta": "en el otro orden: %s + %s = %s" % (_n(mb, nombre), _n(ma, nombre), _n(atras, nombre)),
            "vuelta_ok": atras == m}
