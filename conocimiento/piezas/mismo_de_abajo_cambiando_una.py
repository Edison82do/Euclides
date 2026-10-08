# -*- coding: utf-8 -*-
"""Pieza del MISMO DE ABAJO (paso F.7; NCETM 3.8, puntos 1, 2 y 3): fracciones RELACIONADAS.  En 1/2 y 1/4 los cuartos
caben justos en los medios (4 : 2 = 2): basta con CAMBIAR UNA, la de las partes grandes: 1/2 = 2/4 (arriba y abajo por
2, como en F.6).  La otra se queda como esta.  El de abajo comun es el mas grande de los dos.
LA VUELTA: la que se cambio se divide de vuelta (arriba y abajo entre lo mismo) y tiene que salir la de partida."""

PIEZA = {
    "id": "mismo_de_abajo_cambiando_una",
    "nombre": "relacionadas: cambiar solo una",
    "unidad": "F.7",
    "responde": "mismo_de_abajo",
    "rapidez": 3,
    "que_hace": "1/2 y 1/4: 4 : 2 = 2, justo -> 1/2 = 2/4 (x 2) y 1/4 se queda",
    "condiciones": [
        ("los_de_abajo_son_distintos", "tienen el mismo de abajo (o hay un cero abajo): no hay nada que cambiar"),
        ("un_de_abajo_cabe_justo_en_el_otro", "ningun de abajo cabe justo en el otro (no son relacionadas)"),
    ],
    "usa": ["dividir", "multiplicar"],
}


def hacer(s, u):
    fa, fb = s["a"], s["b"]
    a_grande = u.viene_despues(u.decir(fa[1]), u.decir(fb[1]))
    chica, grande = (fb, fa) if a_grande else (fa, fb)          # chica: la de MENOS partes (partes grandes)
    k = u.usar("dividir", total=grande[1], divisor=chica[1])["valor"]
    arriba = u.usar("multiplicar", a=chica[0], b=k)["valor"]
    nueva = (arriba, grande[1])
    # LA VUELTA: dividir de vuelta la cambiada
    va = u.usar("dividir", total=nueva[0], divisor=k)
    vb = u.usar("dividir", total=nueva[1], divisor=k)
    ok = (va["valor"], vb["valor"]) == chica and not va["resultado"].get("resto", 0) \
        and not vb["resultado"].get("resto", 0)
    na, nb = (grande, nueva) if a_grande else (nueva, grande)
    return {"valor": (na, nb), "abajo": grande[1], "por": (1, k) if a_grande else (k, 1),
            "metodo": "relacionadas: cambiar solo una (F.7)",
            "cuenta": "%d : %d = %d, justo: en cada parte de 1/%d caben %d de 1/%d.  Cambio solo %d/%d: arriba y "
                      "abajo por %d -> %d/%d;  %d/%d se queda" % (grande[1], chica[1], k, chica[1], k, grande[1],
                                                                 chica[0], chica[1], k, nueva[0], nueva[1], grande[0],
                                                                 grande[1]),
            "vuelta": "%d/%d entre %d: %d : %d = %d, %d : %d = %d -> %d/%d" % (
                nueva[0], nueva[1], k, nueva[0], k, va["valor"], nueva[1], k, vb["valor"], va["valor"], vb["valor"]),
            "vuelta_ok": ok}
