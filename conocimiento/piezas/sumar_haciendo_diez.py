# -*- coding: utf-8 -*-
"""Pieza de calculo: SUMAR HACIENDO DIEZ (unidad 7.2).  8 + 5 -> al 8 le faltan 2; 5 = 2 + 3;
10 + 3 = 13.  No cuenta: COMBINA lo que ya sabe.  Es un hecho DERIVADO (la tercera etapa de las
estrategias de los ninos), asi que va antes que contar con los dedos."""

PIEZA = {
    "id": "sumar_haciendo_diez",
    "nombre": "hacer diez",
    "unidad": "7.2",
    "responde": "sumar",
    "rapidez": 10,
    "que_hace": "completa el diez con una parte del segundo y suma lo que sobra",
    "condiciones": [
        ("los_dos_son_de_una_cifra", "no son los dos de una cifra (hacer diez es para una cifra)"),
        ("la_suma_cruza_el_diez", "no cruza el diez: no hay diez que hacer"),
    ],
    "usa": ["7.2"],
}


def hacer(s, u):
    r = u.leccion("7.2")(u.decir(s["a"]), u.decir(s["b"]), u.saber)
    vuelta = u.contar_atras(r["total"], u.decir(s["b"]))
    return {"valor": r["total_valor"], "metodo": "hacer diez (7.2)",
            "cuenta": "%d + %d = %d  (al %d le faltan %d para diez; %d + %d = 10; 10 + %d = %d)"
            % (s["a"], s["b"], r["total_valor"], s["a"], r["faltan_para_diez"], s["a"],
               r["faltan_para_diez"], r["parte_que_sobra"], r["total_valor"]),
            "vuelta": "%s - %s = %s" % (r["total"], u.decir(s["b"]), vuelta.get("resultado")),
            "vuelta_ok": vuelta.get("resultado") == u.decir(s["a"])}
