# -*- coding: utf-8 -*-
"""Pieza de SUMAR (paso P.7; NCETM 1.29, punto 2): CAMBIAR UN SUMANDO.  'Si un sumando aumenta y el otro
se queda igual, la suma aumenta LO MISMO.'  4997 + 2: sumo 5000 + 2 = 5002, pero puse 3 de mas, asi
que la suma tiene 3 de mas: los quito, 4999.  (Sirve cuando no se le puede pasar nada al otro.)"""

PIEZA = {
    "id": "sumar_redondeando_y_quitando",
    "nombre": "redondear un sumando y quitar lo que sobra",
    "unidad": "P.7",
    "responde": "sumar",
    "rapidez": 8,
    "que_hace": "sumo con el redondo (5000 + 2) y quito lo que puse de mas (o pongo lo que quite)",
    "condiciones": [
        ("un_sumando_esta_cerca_de_un_redondo", "ningun sumando esta a 1, 2 o 3 de un redondo (100, 1000...)"),
        ("el_total_tiene_nombre", "el total se pasa de lo que se escribir (mi techo)"),
    ],
    "usa": ["buscar_el_redondo_cercano", "sumar_miles_justos", "sumar_centenas_justas", "sumar_por_columnas",
            "restar_por_columnas"],
}

_FINAL = ("sumar_miles_justos", "sumar_centenas_justas", "sumar_por_columnas")


def _redondo(u, n, ceros):
    try:
        return u.usar("buscar_el_redondo_cercano", n=n, ceros=ceros)["resultado"]
    except Exception:
        return None


def hacer(s, u):
    r = _redondo(u, s["a"], s.get("ceros", 2))
    x, otro = s["a"], s["b"]
    if r is None:
        r = _redondo(u, s["b"], s.get("ceros", 2))
        x, otro = s["b"], s["a"]
    d, R = u.decir(r["pasos"]), r["valor"]
    v1 = como = None
    for nombre in _FINAL:
        try:
            f = u.usar(nombre, a=R, b=otro)
        except Exception:
            continue
        v1, como = f["valor"], f["resultado"]["metodo"]
        break
    if v1 is None:
        raise ValueError("%d + %d se sale de mi lista" % (R, otro))
    if r["sube"]:          # puse d de mas: la suma tiene d de mas
        w = u.contar_atras(u.decir(v1), d).get("resultado")
        frase = "%d es %s mas que %d: la suma sale %s de mas; los quito" % (R, d, x, d)
    else:
        w = u.contar_adelante(u.decir(v1), d).get("resultado")
        frase = "%d es %s menos que %d: a la suma le faltan %s; los pongo" % (R, d, x, d)
    if w is None:
        raise ValueError("no hay numero")
    v = u.leer(w)
    k = u.usar("restar_por_columnas", a=v, b=s["b"])["valor"]
    return {"valor": v, "metodo": "redondear un sumando (P.7)",
            "cadena": [[s["a"], "+", s["b"]], [R, "+", otro]],
            "cuenta": "%d + %d = %d (%s);  %s: %d  (NCETM 1.29, punto 2)"
                      % (R, otro, v1, como, frase, v),
            "vuelta": "%d - %d = %d" % (v, s["b"], k),
            "vuelta_ok": k == s["a"]}
