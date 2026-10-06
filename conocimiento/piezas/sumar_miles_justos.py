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


def _miles(u, n):
    return u.escribir_cifras(u.cifras_de(n)[3:])          # 345000 -> 345 (se tapan las tres cifras de la derecha)


def hacer(s, u):
    ma, mb = _miles(u, s["a"]), _miles(u, s["b"])
    m = u.sumar_por_columnas(ma, mb)                       # los miles, como cosas (el mecanismo)
    total = u.escribir_cifras([0, 0, 0] + u.cifras_de(m))
    atras = u.sumar_por_columnas(mb, ma)                   # la vuelta: en el otro orden
    return {"valor": total, "metodo": "contar miles (N.4)",
            "cuenta": "%d + %d: %d mil + %d mil = %d mil (%d + %d = %d) = %d"
                      % (s["a"], s["b"], ma, mb, m, ma, mb, m, total),
            "vuelta": "en el otro orden: %d mil + %d mil = %d mil" % (mb, ma, atras), "vuelta_ok": atras == m}
