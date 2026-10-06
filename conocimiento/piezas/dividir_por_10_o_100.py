# -*- coding: utf-8 -*-
"""Pieza de DIVIDIR ENTRE 10 O ENTRE 100 (paso M.9; NCETM 2.13, puntos 2, 4 y 5).  Entre 10, CADA CIFRA BAJA
UN SITIO: las decenas se vuelven unidades.  Lo que habia en las unidades no cabe en un grupo de diez: es el
RESTO (47 : 10 = 4 resto 7: cuatro decenas, y siete sueltas).  Entre 100, dos sitios."""

PIEZA = {
    "id": "dividir_por_10_o_100",
    "nombre": "entre 10 o 100: las cifras bajan de sitio",
    "unidad": "M.9",
    "responde": "dividir",
    "rapidez": 2,
    "que_hace": "entre 10 cada cifra baja un sitio (las unidades sobran); entre 100, dos",
    "condiciones": [
        ("el_divisor_es_10_o_100", "el divisor no es 10 ni 100"),
    ],
    "usa": [],
}


def hacer(s, u):
    t, d = s["total"], s["divisor"]
    cif = u.cifras_de(t)
    caen = 1 if d == 10 else 2
    while len(cif) <= caen:
        cif.append(0)
    q = u.escribir_cifras(cif[caen:])
    resto = u.escribir_cifras(cif[:caen])
    # LA VUELTA: el cociente con sus cifras subidas, mas el resto
    sube = [0] if d == 10 else [0, 0]
    sube.extend(u.cifras_de(q))
    subido = u.escribir_cifras(sube) if q else 0
    vuelta = u.sumar_por_columnas(subido, resto) if resto else subido
    que = "decenas" if d == 10 else "centenas"
    return {"valor": q, "resto": resto, "metodo": "las cifras bajan de sitio (M.9)",
            "cuenta": "%d : %d: en %d hay %d %s (se tapan %s); %s"
                      % (t, d, t, q, que, "las unidades" if d == 10 else "las decenas y las unidades",
                         "sobran %d" % resto if resto else "no sobra nada"),
            "vuelta": "%d x %d%s = %d" % (q, d, " + %d" % resto if resto else "", vuelta), "vuelta_ok": vuelta == t}
