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
    "usa": ["sumar", "restar"],
}

# PASO N.4 (arreglo, 7 oct): con divisores de VARIAS cifras ya no se cuenta de uno en uno (un humano no
# cuenta 243225 pasos para dar un salto): cada salto es una SUMA (+ el divisor) y el resto una RESTA.
# Con un divisor que pasa de las tablas (mas de doce), mas de cien saltos ya es la division larga
# (6.o, NCETM 2.24): todavia no.  PASO M.18: entre DOS cifras ya se hace la division larga (pieza division_larga);
# aqui solo llegan con muchos saltos los divisores de TRES cifras o mas, y esos siguen todavia no.
_MAX_SALTOS_GRANDES = "cien"
_MAX_SALTOS = "mil"


def _grande(d, u):
    return u.viene_despues(u.decir(d), "doce")


def _saltar(v, d, u):
    if u.decir(d) in ("dos", "cinco", "diez", "cien"):
        return u.saltar(v, u.decir(d))
    if _grande(d, u):
        try:
            r = u.usar("sumar", a=v, b=d)["valor"]
        except Exception:                                # el salto se sale de mi lista
            return None
        return r if u.decir(r) is not None else None
    r = u.contar_adelante(u.decir(v), u.decir(d), con_dedos=False)
    return u.leer(r["resultado"]) if r.get("resultado") else None


def hacer(s, u):
    t, d = s["total"], s["divisor"]
    v, saltos, camino = 0, "cero", []
    while True:
        nuevo = _saltar(v, d, u)
        if nuevo is None or u.viene_despues(u.decir(nuevo), u.decir(t)):
            break
        if _grande(d, u) and saltos == _MAX_SALTOS_GRANDES:
            if len(u.cifras_de(d)) > 2:
                raise ValueError("son mas de cien saltos de %d: dividir entre tres cifras todavia no (la division "
                                 "larga de 6.o, NCETM 2.24, es entre dos cifras)" % d)
            raise ValueError("son mas de cien saltos de %d: eso es la division larga (6.o), todavia no" % d)
        if saltos == _MAX_SALTOS:
            # PASO M.14 (arreglo): 1000000 : 8 eran 125 000 saltos (15 s).  Un humano no salta mil veces:
            # con un divisor de las tablas se hace la division corta (y para eso hay que saberse la tabla).
            raise ValueError("son mas de %s saltos de %d: asi no se cuenta; se hace la division corta, y para eso "
                             "hay que saberse la tabla del %d (aprender: tablas)" % (_MAX_SALTOS, d, d))
        v = nuevo
        saltos = u.siguiente(saltos)
        camino.append(str(v))
    if _grande(d, u):
        resto = u.usar("restar", a=t, b=v)["valor"] if v else t
    else:
        resto = u.leer(u.contar_hasta(u.decir(v), u.decir(t)))
    q = u.leer(saltos)
    return {"valor": q, "resto": resto, "metodo": "contar de %d en %d (M.3)" % (d, d),
            "cuenta": "de %d en %d: %s -> %d saltos%s"
                      % (d, d, ", ".join(camino) or "(no llega ni a un salto)", q,
                         ("; sobra 1 (no llega a otro salto)" if resto == 1 else "; sobran %d (no llegan a otro salto)" % resto)
                         if resto else ", justo"),
            "vuelta": "", "vuelta_ok": True}
