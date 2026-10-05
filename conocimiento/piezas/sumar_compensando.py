# -*- coding: utf-8 -*-
"""Pieza de calculo: SUMAR COMPENSANDO (paso 4).  29 + 14: al 29 le falta UNO para 30; ese uno
se le quita al 14 (queda 13), y 30 + 13 se hace de diez en diez: 43.  Lo que se da a uno se le
quita al otro: el total no cambia (la compensacion de la investigacion: "make a ten / bridge
through ten" con decenas)."""

PIEZA = {
    "id": "sumar_compensando",
    "nombre": "compensar (redondear y devolver)",
    "unidad": "P.4",
    "responde": "sumar",
    "rapidez": 6,
    "que_hace": "si uno acaba en nueve (29), le paso UNO del otro y queda una decena justa",
    "condiciones": [
        ("uno_acaba_en_nueve", "ninguno es de dos cifras acabado en nueve (19, 29 ... 89)"),
        ("ninguno_es_cero", "uno es cero: no hay nada que pasar de uno a otro"),
        ("el_total_tiene_nombre", "el total se pasa de mil"),
    ],
    "usa": ["sumar_de_diez_en_diez"],
}


def _acaba_en_nueve(n, u):
    c = u.cifras_de(n)
    return len(c) == 2 and c[0] == 9 and c[1] != 9


def hacer(s, u):
    x, otro = (s["a"], s["b"]) if _acaba_en_nueve(s["a"], u) else (s["b"], s["a"])
    redondo = u.leer(u.siguiente(u.decir(x)))         # 29 -> 30: le doy uno
    resto = u.leer(u.anterior(u.decir(otro)))         # 14 -> 13: se lo quito al otro
    r = u.usar("sumar_de_diez_en_diez", a=resto, b=redondo)
    v = r["valor"]
    # LA VUELTA, contando hacia atras desde el total: tiene que salir el primero
    vuelta = u.contar_atras(u.decir(v), u.decir(s["b"]), con_dedos=False)
    return {"valor": v, "metodo": "compensar (P.4)",
            "cuenta": "%d + %d = %d  (al %d le doy uno del %d: %d + %d; %s)"
            % (s["a"], s["b"], v, x, otro, redondo, resto, r["resultado"]["cuenta"]),
            "vuelta": "%s - %s = %s" % (u.decir(v), u.decir(s["b"]), vuelta.get("resultado")),
            "vuelta_ok": vuelta.get("resultado") == u.decir(s["a"])}
