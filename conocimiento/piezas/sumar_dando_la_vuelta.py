# -*- coding: utf-8 -*-
"""Pieza de calculo: DAR LA VUELTA (paso P.5; Common Core 1.OA.B.3, la propiedad conmutativa).
Juntar 3 y 47 es lo mismo que juntar 47 y 3: el orden no importa al JUNTAR.  Asi que se empieza por
el GRANDE y se cuenta el pequeno (la estrategia 'contar desde el mayor' de los ninos).
OJO: solo para sumar.  Quitar no se puede dar la vuelta (8 - 3 no es 3 - 8)."""

PIEZA = {
    "id": "sumar_dando_la_vuelta",
    "nombre": "dar la vuelta (empezar por el grande)",
    "unidad": "P.5",
    "responde": "sumar",
    "rapidez": 15,
    "que_hace": "si el primero es el pequeno, empiezo por el grande: 3 + 47 = 47 + 3",
    "condiciones": [
        ("el_primero_es_menor", "ya empieza por el grande (o son iguales): no hay vuelta que dar"),
        ("el_primero_es_corto", "el primero no cabe en los dedos ni son decenas justas: darle la vuelta no ayuda"),
    ],
    "usa": ["sumar_de_diez_en_diez", "sumar_con_dedos"],
}


def hacer(s, u):
    probados = []
    for metodo in ("sumar_de_diez_en_diez", "sumar_con_dedos"):
        try:
            r = u.usar(metodo, a=s["b"], b=s["a"])        # LA VUELTA: el grande primero
        except RuntimeError:                             # usar algo no declarado: eso es un fallo de verdad
            raise
        except Exception as e:                           # ese metodo no encaja: el siguiente
            probados.append("%s: %s" % (metodo, e))
            continue
        res = r["resultado"]
        return {"valor": r["valor"], "metodo": "dar la vuelta (P.5) y %s" % res["metodo"],
                "cuenta": "%d + %d = %d + %d  (juntar %d y %d es lo mismo que juntar %d y %d: "
                          "empiezo por el grande);  %s"
                          % (s["a"], s["b"], s["b"], s["a"], s["a"], s["b"], s["b"], s["a"], res["cuenta"]),
                "vuelta": res["vuelta"], "vuelta_ok": res["vuelta_ok"]}
    raise ValueError("dandole la vuelta tampoco hay un metodo corto (%s)" % "; ".join(probados))
