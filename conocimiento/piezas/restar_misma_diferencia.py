# -*- coding: utf-8 -*-
"""Pieza de RESTAR (paso P.7; NCETM 1.29, punto 3): LA MISMA DIFERENCIA.  'Si el minuendo y el sustraendo
cambian LO MISMO, la diferencia no cambia.'  1000 - 397: le sumo 3 a los dos: 1003 - 400 = 603.  Es
como en la recta: si los dos numeros se corren igual, lo que hay de uno a otro no cambia.  (NZ Maths lo
llama 'equal additions': 483 - 397 = 486 - 400.)  OJO: en la resta los dos se mueven HACIA EL MISMO
LADO; en la suma, uno sube y el otro baja."""

PIEZA = {
    "id": "restar_misma_diferencia",
    "nombre": "la misma diferencia (muevo los dos igual)",
    "unidad": "P.7",
    "responde": "restar",
    "rapidez": 7,
    "que_hace": "si lo que se quita esta a 1, 2 o 3 de un redondo (397), muevo los dos igual: 1003 - 400",
    "condiciones": [
        ("el_de_abajo_no_es_mayor", "se quitaria mas de lo que hay (no hay restas negativas, 5.4)"),
        ("el_de_abajo_esta_cerca_de_un_redondo", "lo que se quita no esta a 1, 2 o 3 de un redondo (100, 1000...)"),
    ],
    "usa": ["buscar_el_redondo_cercano", "restar_miles_justos", "restar_centenas_justas", "restar_por_columnas",
            "sumar_por_columnas"],
}

_FINAL = ("restar_miles_justos", "restar_centenas_justas", "restar_por_columnas")


def hacer(s, u):
    r = u.usar("buscar_el_redondo_cercano", n=s["b"], ceros=s.get("ceros", 2))["resultado"]
    d, R = u.decir(r["pasos"]), r["valor"]
    if r["sube"]:          # al sustraendo le faltan d: se los sumo a LOS DOS
        w = u.contar_adelante(u.decir(s["a"]), d).get("resultado")
        frase = "le sumo %s a los dos" % d
        if w is None:
            raise ValueError("%d + %s se sale de mi lista (pasaria del millon)" % (s["a"], d))
    else:                  # el sustraendo se pasa d: se los quito a LOS DOS
        w = u.contar_atras(u.decir(s["a"]), d).get("resultado")
        frase = "le quito %s a los dos" % d
    a2 = u.leer(w)
    v = como = None
    for nombre in _FINAL:
        try:
            f = u.usar(nombre, a=a2, b=R)
        except Exception:
            continue
        v, como = f["valor"], f["resultado"]["metodo"]
        break
    if v is None:
        raise ValueError("%d - %d tampoco me sale" % (a2, R))
    # LA VUELTA, con la operacion contraria y por las columnas: la diferencia mas lo que se quito
    k = u.usar("sumar_por_columnas", a=v, b=s["b"])["valor"]
    return {"valor": v, "metodo": "la misma diferencia (P.7)",
            "cadena": [[s["a"], "-", s["b"]], [a2, "-", R]],
            "cuenta": "%d - %d = %d - %d = %d  (%s: la diferencia no cambia, NCETM 1.29; %d - %d con %s)"
                      % (s["a"], s["b"], a2, R, v, frase, a2, R, como),
            "vuelta": "%d + %d = %d" % (v, s["b"], k),
            "vuelta_ok": k == s["a"]}
