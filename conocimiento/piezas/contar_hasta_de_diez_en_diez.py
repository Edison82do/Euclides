# -*- coding: utf-8 -*-
"""Pieza de CONTAR HASTA (paso N.1; Common Core 2.NBT.B.8): de 47 a 77 no se cuentan 30 pasos de uno
en uno: las unidades son iguales, asi que se SALTA de diez en diez (57, 67, 77) y se cuentan los
saltos: 3 saltos de diez = 30.  (Lo que quedo pendiente en E.1 con 47 + ? = 77.)"""

PIEZA = {
    "id": "contar_hasta_de_diez_en_diez",
    "nombre": "saltar de diez en diez hasta el otro",
    "unidad": "N.1",
    "responde": "contar_hasta",
    "rapidez": 5,
    "que_hace": "si las unidades son iguales, salta de diez en diez y cuenta los saltos",
    "condiciones": [
        ("el_segundo_no_es_menor", "el segundo es menor: contando hacia adelante no se llega"),
        ("se_llega_saltando_de_diez", "las unidades no son iguales (o hay mas de nueve saltos): no se llega saltando de diez"),
    ],
    "usa": [],
}


def hacer(s, u):
    v, saltos, camino = s["a"], "cero", []
    while v != s["b"]:
        v = u.subir_una_decena(v)
        saltos = u.siguiente(saltos)
        camino.append(str(v))
    total = u.escribir_cifras([0, u.leer(saltos)])           # tres saltos de diez: 3 decenas = 30
    w, marca = s["b"], "cero"
    while marca != saltos:                                   # la vuelta: los saltos hacia atras
        w = u.bajar_una_decena(w)
        marca = u.siguiente(marca)
    return {"valor": total, "metodo": "saltar de diez en diez (N.1)",
            "cuenta": "de %d a %d: %s -> %s saltos de diez = %d" % (s["a"], s["b"], ", ".join(camino) or "nada",
                                                                  saltos, total),
            "vuelta": "%d - %d = %d (los saltos hacia atras)" % (s["b"], total, w),
            "vuelta_ok": w == s["a"]}
