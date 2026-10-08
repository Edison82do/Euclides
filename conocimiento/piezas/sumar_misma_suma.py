# -*- coding: utf-8 -*-
"""Pieza de SUMAR (paso P.7; NCETM 1.29, punto 1): LA MISMA SUMA.  'Si un sumando aumenta y el otro
disminuye LO MISMO, la suma no cambia.'  4997 + 2456: al 4997 le faltan 3 para 5000; se los quito al
2456 y queda 5000 + 2453, que es facil (con un redondo solo cambian sus columnas): 7453.
Es la compensacion de P.4 (29 + 14 = 30 + 13) llevada a centenas, miles y decimales."""

PIEZA = {
    "id": "sumar_misma_suma",
    "nombre": "la misma suma (lo que gana uno lo pierde el otro)",
    "unidad": "P.7",
    "responde": "sumar",
    "rapidez": 7,
    "que_hace": "si un sumando esta a 1, 2 o 3 de un redondo (4997), se lo paso del otro: 5000 + 2453",
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


def _el_de_mas_ceros(u, s):
    """El sumando que se redondea: el que tiene un redondo; si los dos, el que gana mas ceros."""
    ra, rb = _redondo(u, s["a"], s.get("ceros", 2)), _redondo(u, s["b"], s.get("ceros", 2))
    if ra and (not rb or not u.viene_despues(u.decir(rb["ceros"]), u.decir(ra["ceros"]))):
        return s["a"], s["b"], ra
    return s["b"], s["a"], rb


def hacer(s, u):
    x, otro, r = _el_de_mas_ceros(u, s)
    d, R = u.decir(r["pasos"]), r["valor"]
    if r["sube"]:          # al x le faltan d: se los quito al otro
        w = u.contar_atras(u.decir(otro), d).get("resultado")
        frase = "a %d le faltan %s para %d: se los quito a %d" % (x, d, R, otro)
    else:                  # x se pasa d: se los doy al otro
        w = u.contar_adelante(u.decir(otro), d).get("resultado")
        frase = "%d se pasa %s de %d: se los doy a %d" % (x, d, R, otro)
    if w is None:
        raise ValueError("a %d no le puedo quitar %s" % (otro, d) if r["sube"] else "%d + %s se sale de mi lista" % (otro, d))
    o2 = u.leer(w)
    v = como = None
    for nombre in _FINAL:
        try:
            f = u.usar(nombre, a=R, b=o2)
        except Exception:
            continue
        v, como = f["valor"], f["resultado"]["metodo"]
        break
    if v is None:
        raise ValueError("%d + %d tampoco me sale" % (R, o2))
    # LA VUELTA, con la operacion contraria y por las columnas (no con la compensacion): sale el primero
    k = u.usar("restar_por_columnas", a=v, b=s["b"])["valor"]
    return {"valor": v, "metodo": "la misma suma (P.7)",
            "cadena": [[s["a"], "+", s["b"]], [R, "+", o2]],
            "cuenta": "%d + %d = %d + %d = %d  (%s: la suma no cambia, NCETM 1.29; %d + %d con %s)"
                      % (s["a"], s["b"], R, o2, v, frase, R, o2, como),
            "vuelta": "%d - %d = %d" % (v, s["b"], k),
            "vuelta_ok": k == s["a"]}
