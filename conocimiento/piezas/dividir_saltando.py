# -*- coding: utf-8 -*-
"""Pieza de DIVIDIR (paso M.3; NCETM 2.6, puntos 1 a 3): CONTAR DE DIVISOR EN DIVISOR hasta el total y
contar los saltos.  Agrupar 12 en grupos de 3: 3, 6, 9, 12 -> 4 grupos.  Repartir 12 entre 3: cada
ronda da uno a cada uno (3), y 3, 6, 9, 12 son 4 rondas -> 4 para cada uno.  Lo que no llega para
otro salto es el RESTO."""

PIEZA = {
    "id": "dividir_saltando",
    "nombre": "contar de divisor en divisor",
    "unidad": "M.3",
    "responde": "dividir",
    "rapidez": 20,
    "que_hace": "salta de divisor en divisor hasta el total; los saltos son el cociente, lo que falta el resto",
    "condiciones": [
        ("el_divisor_no_es_cero", "el divisor es cero: no se puede repartir entre nadie (y los grupos de cero nunca se llenan)"),
    ],
    "usa": [],
}


def _saltar(v, d, u):
    if u.decir(d) in ("dos", "cinco", "diez", "cien"):
        return u.saltar(v, u.decir(d))
    r = u.contar_adelante(u.decir(v), u.decir(d), con_dedos=False)
    return u.leer(r["resultado"]) if r.get("resultado") else None


def hacer(s, u):
    t, d = s["total"], s["divisor"]
    v, saltos, camino = 0, "cero", []
    while True:
        nuevo = _saltar(v, d, u)
        if nuevo is None or u.viene_despues(u.decir(nuevo), u.decir(t)):
            break
        v = nuevo
        saltos = u.siguiente(saltos)
        camino.append(str(v))
    resto = u.leer(u.contar_hasta(u.decir(v), u.decir(t)))
    q = u.leer(saltos)
    return {"valor": q, "resto": resto, "metodo": "contar de %d en %d (M.3)" % (d, d),
            "cuenta": "de %d en %d: %s -> %d saltos%s"
                      % (d, d, ", ".join(camino) or "(no llega ni a un salto)", q,
                         ("; sobra 1 (no llega a otro salto)" if resto == 1 else "; sobran %d (no llegan a otro salto)" % resto)
                         if resto else ", justo"),
            "vuelta": "", "vuelta_ok": True}
