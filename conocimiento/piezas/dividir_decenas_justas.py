# -*- coding: utf-8 -*-
"""Pieza de DIVIDIR (paso M.9; NCETM 2.13, punto 6): si el dividendo se hace DIEZ VECES mayor, el cociente
tambien.  120 : 4: 12 : 4 = 3 (porque 3 x 4 = 12, de memoria) y 120 es diez veces 12, asi que el cociente
es diez veces 3 = 30.  Hecho derivado: solo si la division pequena esta en las tablas que se saben."""

PIEZA = {
    "id": "dividir_decenas_justas",
    "nombre": "decenas justas: la division pequena, diez veces",
    "unidad": "M.9",
    "responde": "dividir",
    "rapidez": 3,
    "que_hace": "quita el cero del dividendo, divide con la tabla que se sabe, y sube las cifras del cociente",
    "condiciones": [
        ("el_dividendo_acaba_en_cero", "el dividendo no acaba en cero (o el divisor es 0, 1, 10 o 100)"),
    ],
    "usa": [],
}


def hacer(s, u):
    t, d = s["total"], s["divisor"]
    pequeno = u.escribir_cifras(u.cifras_de(t)[1:])          # 120 -> 12 (se tapa el cero)
    q = "cero"
    while True:
        h = u.recuerdo("%d x %d" % (u.leer(q), d)) or u.recuerdo("%d x %d" % (d, u.leer(q)))
        if h and h["valor"] == pequeno:
            break
        if q == "doce":
            raise ValueError("%d : %d no esta en las tablas que me se" % (pequeno, d))
        q = u.siguiente(q)
    qq = u.leer(q)
    v = u.escribir_cifras([0] + u.cifras_de(qq)) if qq else 0
    return {"valor": v, "resto": 0, "metodo": "decenas justas (M.9)",
            "cuenta": "%d : %d = %d (porque %d x %d = %d, lo se); %d es DIEZ veces %d, asi que el cociente tambien: %d"
                      % (pequeno, d, qq, qq, d, pequeno, t, pequeno, v),
            "vuelta": "%d x %d = %d, y diez veces: %d" % (qq, d, pequeno, t),
            "vuelta_ok": u.escribir_cifras([0] + u.cifras_de(pequeno)) == t}
