# -*- coding: utf-8 -*-
"""Pieza de la BALANZA (paso P.7; NCETM 1.29, puntos 3 y 6): DOS RESTAS, sin calcular los lados.
   74 - 28 = 75 - ?   el minuendo SUBE 1, asi que el sustraendo tambien tiene que subir 1: 29.
   (La trampa: 27, que es compensar como en la SUMA.  En la resta los dos se mueven HACIA EL MISMO LADO.)
   50 - 19 = ? - 20   el sustraendo sube 1, el minuendo tambien: 51."""

PIEZA = {
    "id": "balanza_misma_diferencia",
    "nombre": "la misma diferencia (en la resta, los dos igual)",
    "unidad": "P.7",
    "responde": "balanza",
    "rapidez": 5,
    "que_hace": "mira cuanto cambia el numero conocido y mueve el hueco LO MISMO y HACIA EL MISMO LADO",
    "condiciones": [
        ("los_dos_lados_son_restas_con_un_cambio_facil",
         "no son dos restas con un cambio facil (en los dedos, o decenas/centenas justas)"),
    ],
    "usa": ["restar_por_columnas", "sumar", "restar"],
}


def hacer(s, u):
    c, h = s["completo"], s["con_hueco"]
    if h["b"] == "?":
        p, q, mover, papel, otro = c["a"], h["a"], c["b"], "el minuendo", "el sustraendo"
    else:
        p, q, mover, papel, otro = c["b"], h["b"], c["a"], "el sustraendo", "el minuendo"
    if p == q:
        v, frase = mover, "%s no cambia, %s tampoco" % (papel, otro)
    elif u.viene_despues(u.decir(q), u.decir(p)):
        d = u.usar("restar_por_columnas", a=q, b=p)["valor"]
        v = u.usar("sumar", a=mover, b=d)["valor"]
        frase = "%s SUBE %d (%d -> %d); para que la diferencia no cambie, %s tambien sube %d: %d + %d = %d" \
                % (papel, d, p, q, otro, d, mover, d, v)
    else:
        d = u.usar("restar_por_columnas", a=p, b=q)["valor"]
        if u.viene_despues(u.decir(d), u.decir(mover)):
            raise ValueError("no hay numero: a %d no le puedo quitar %d" % (mover, d))
        v = u.usar("restar", a=mover, b=d)["valor"]
        frase = "%s BAJA %d (%d -> %d); para que la diferencia no cambie, %s tambien baja %d: %d - %d = %d" \
                % (papel, d, p, q, otro, d, mover, d, v)
    # LA VUELTA: se calculan los dos platos, con el numero en el hueco
    a2, b2 = (h["a"], v) if h["b"] == "?" else (v, h["b"])
    if u.viene_despues(u.decir(b2), u.decir(a2)):
        raise ValueError("no hay numero: la resta del otro plato quitaria mas de lo que hay")
    vc = u.usar("restar", a=c["a"], b=c["b"])["valor"]
    vh = u.usar("restar", a=a2, b=b2)["valor"]
    return {"valor": v, "metodo": "la misma diferencia (P.7)",
            "cuenta": "%s  (sin calcular los lados; NCETM 1.29: en la resta los dos se mueven HACIA EL MISMO LADO)" % frase,
            "vuelta": "%d - %d = %d;  %d - %d = %d" % (c["a"], c["b"], vc, a2, b2, vh),
            "vuelta_ok": vc == vh}
