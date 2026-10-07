# -*- coding: utf-8 -*-
"""Pieza de RESTAR (paso P.7; NCETM 1.29, punto 5): CAMBIAR EL SUSTRAENDO.  'Si el minuendo se queda igual
y el sustraendo aumenta, la diferencia DISMINUYE lo mismo.'  625 - 398: quito 400, que es 2 mas que 398:
625 - 400 = 225 tiene 2 de menos; los devuelvo: 227.  (Es P.4, 52 - 29 = 52 - 30 + 1, con centenas y
miles.)  La trampa de siempre: creer que si el sustraendo sube, la diferencia tambien sube."""

PIEZA = {
    "id": "restar_quitando_de_mas_y_devolviendo",
    "nombre": "quitar el redondo y devolver (o quitar) lo que sobra",
    "unidad": "P.7",
    "responde": "restar",
    "rapidez": 8,
    "que_hace": "quito el redondo (400 en vez de 398) y devuelvo lo que quite de mas",
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
    if u.viene_despues(u.decir(R), u.decir(s["a"])):
        raise ValueError("%d no llega a %d: no puedo quitar de mas" % (s["a"], R))
    v1 = como = None
    for nombre in _FINAL:
        try:
            f = u.usar(nombre, a=s["a"], b=R)
        except Exception:
            continue
        v1, como = f["valor"], f["resultado"]["metodo"]
        break
    if v1 is None:
        raise ValueError("%d - %d tampoco me sale" % (s["a"], R))
    if r["sube"]:          # quite d de mas: la diferencia tiene d de menos; los devuelvo
        w = u.contar_adelante(u.decir(v1), d).get("resultado")
        frase = "quite %s de mas (%d en vez de %d): la diferencia tiene %s de MENOS; los devuelvo" % (d, R, s["b"], d)
    else:                  # quite d de menos: la diferencia tiene d de mas; los quito
        w = u.contar_atras(u.decir(v1), d).get("resultado")
        frase = "quite %s de menos (%d en vez de %d): la diferencia tiene %s de MAS; los quito" % (d, R, s["b"], d)
    if w is None:
        raise ValueError("no hay numero")
    v = u.leer(w)
    k = u.usar("sumar_por_columnas", a=v, b=s["b"])["valor"]
    return {"valor": v, "metodo": "quitar el redondo y devolver (P.7)",
            "cadena": [[s["a"], "-", s["b"]], [s["a"], "-", R]],
            "cuenta": "%d - %d = %d (%s);  %s: %d  (NCETM 1.29, punto 5)" % (s["a"], R, v1, como, frase, v),
            "vuelta": "%d + %d = %d" % (v, s["b"], k),
            "vuelta_ok": k == s["a"]}
