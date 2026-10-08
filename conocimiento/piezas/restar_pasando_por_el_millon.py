# -*- coding: utf-8 -*-
"""Pieza de calculo: RESTAR PASANDO POR EL MILLON (paso N.6; NCETM 1.30, punto 4).  Contar hacia arriba (P.6) con
millones: 1 002 000 - 997 000: de 997 000 al millon, 3 000 (por las cifras); del millon a 1 002 000, 2 000
(se tapan los millones); 3 000 + 2 000 = 5 000.  Como la diferencia en la recta, saltando al redondo."""

PIEZA = {
    "id": "restar_pasando_por_el_millon",
    "nombre": "contar hacia arriba pasando por el millon",
    "unidad": "N.6",
    "responde": "restar",
    "rapidez": 2,
    "que_hace": "si lo que se quita esta justo debajo de un millon justo y lo que habia justo encima: hasta el millon y desde el millon",
    "condiciones": [
        ("el_de_abajo_no_es_mayor", "se quitaria mas de lo que hay (no hay restas negativas, 5.4)"),
        ("la_resta_pasa_por_un_millon_justo",
         "lo que se quita no esta justo debajo de un millon justo, o lo que habia no esta en el millon siguiente"),
    ],
    "usa": [],                       # suma por columnas con el mecanismo (si usara 'sumar' habria una vuelta en el mapa)
}


def hacer(s, u):
    a, b = s["a"], s["b"]
    hasta = u.lo_que_falta_para_el_redondo(b, 6)                      # de 997000 al millon: 3000
    ca = u.cifras_de(a)
    desde = u.escribir_cifras(ca[:6])                                 # del millon a 1002000: se tapan los millones
    redondo = u.escribir_cifras([0, 0, 0, 0, 0, 0] + ca[6:])
    diferencia = u.sumar_por_columnas(hasta, desde)                   # 3000 + 2000
    # LA VUELTA: lo que se quito + la diferencia tiene que dar lo que habia (por columnas, en el otro orden)
    atras = u.sumar_por_columnas(diferencia, b)
    return {"valor": diferencia, "metodo": "pasar por el millon (N.6)",
            "cuenta": "%d - %d: de %d a %d hay %d (cada cifra hasta nueve, la ultima hasta diez); de %d a %d hay %d; "
                      "%d + %d = %d" % (a, b, b, redondo, hasta, redondo, a, desde, hasta, desde, diferencia),
            "vuelta": "%d + %d = %s" % (b, diferencia, atras), "vuelta_ok": atras == a}
