# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso M.19; NCETM 2.25, punto 1): 'si un factor se escala, el producto se escala por el mismo
factor'.  5 es 10 dos veces mas pequeno, y 25 es 100 cuatro veces mas pequeno; asi que se multiplica por 10 o por 100
(las cifras suben de sitio) y se COMPENSA haciendo el producto igual de mas pequeno:
    5 x 4683 = 46830 : 2 = 23415               (x 10 y la mitad)
    25 x 37 = 3700 : 4 = 1850 : 2 = 925        (x 100 y la mitad de la mitad)
La trampa: escalar mal (25 x 37 = 3700 : 2: una mitad sola).
LA VUELTA, con las operaciones contrarias: doblar lo que salio (una vez para el 5, dos para el 25) vuelve al producto
por 10 o por 100, y quitandole los ceros vuelve el otro factor."""

PIEZA = {
    "id": "multiplicar_por_5_o_25_compensando",
    "nombre": "por 5 o 25: por 10 o 100 y la mitad (o la mitad de la mitad)",
    "unidad": "M.19",
    "responde": "multiplicar",
    "rapidez": 6.6,
    "que_hace": "5 x 37 = 370 : 2; 25 x 37 = 3700 : 4: escalo el 5 o el 25 y compenso el producto (NCETM 2.25)",
    "condiciones": [
        ("un_factor_es_5_o_25_y_el_otro_grande", "ningun factor es 5 o 25 con el otro de mas de doce (y sin cero al final)"),
    ],
    "usa": ["multiplicar_por_10_o_100", "dividir_a_la_mitad", "sumar", "dividir_por_10_o_100"],
}


def hacer(s, u):
    a, b = s["a"], s["b"]
    f, g = (a, b) if a in (5, 25) and u.cifras_de(b)[0] != 0 and u.viene_despues(u.decir(b), "doce") else (b, a)
    if f not in (5, 25):
        raise ValueError("ningun factor es 5 o 25")
    por, mitades = (10, 1) if f == 5 else (100, 2)
    grande = u.usar("multiplicar_por_10_o_100", a=g, b=por)["valor"]
    if u.decir(grande) is None:
        raise ValueError("%d x %d se sale de mi lista" % (g, por))
    v, pasos = grande, []
    for _ in range(mitades):
        m = u.usar("dividir_a_la_mitad", total=v, divisor=2)
        if m["resultado"].get("resto"):
            raise ValueError("%d no se parte justo por la mitad" % v)
        pasos.append("la mitad de %d = %d" % (v, m["valor"]))
        v = m["valor"]
    # LA VUELTA: doblar (sumando) tantas veces como mitades vuelve a 'grande'; sin los ceros, el otro factor
    w, vl = v, []
    for _ in range(mitades):
        d = u.usar("sumar", a=w, b=w)["valor"]
        vl.append("%d + %d = %d" % (w, w, d))
        w = d
    ok = w == grande
    q = u.usar("dividir_por_10_o_100", total=w, divisor=por)
    ok = ok and not q["resultado"].get("resto") and q["valor"] == g
    vl.append("%d : %d = %d" % (w, por, q["valor"]))
    return {"valor": v, "metodo": "por %d: por %d y %s (M.19; NCETM 2.25)"
                                  % (f, por, "la mitad" if f == 5 else "la mitad de la mitad"),
            "cuenta": "%d es %d %s mas pequeno: %d x %d = %d, y el producto tambien %s mas pequeno: %s"
                      % (f, por, "dos veces" if f == 5 else "cuatro veces", g, por, grande,
                         "dos veces" if f == 5 else "cuatro veces", "; ".join(pasos)),
            "vuelta": "%s ... %s" % ("; ".join(vl), "SI" if ok else "NO"), "vuelta_ok": ok,
            "vuelta_explicada": "con las operaciones contrarias: doblando vuelve %d x %d = %d, y quitando los ceros, %d"
                                % (g, por, grande, g)}
