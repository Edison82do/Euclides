# -*- coding: utf-8 -*-
"""Pieza de SUMA DE IGUALES (paso M.0; Common Core 2.OA.C.4): se suma grupo a grupo con los metodos
que ya se tienen.  3 filas de 4: 4 + 4 = 8 (de memoria), 8 + 4 = 12.  Todavia NO se multiplica:
2.OA.C.4 pide usar la SUMA y escribir el total como una suma de sumandos iguales."""

PIEZA = {
    "id": "sumar_iguales_uno_a_uno",
    "nombre": "sumar grupo a grupo",
    "unidad": "M.0",
    "responde": "suma_de_iguales",
    "rapidez": 15,
    "que_hace": "suma el primer grupo con el segundo, lo que da con el tercero... con los metodos que tengo",
    "condiciones": [
        ("los_grupos_tienen_nombre", "no se cuantos grupos son"),
    ],
    "usa": ["sumar"],
}


def hacer(s, u):
    if s["veces"] == 0:
        return {"valor": 0, "metodo": "sumar grupo a grupo (M.0)", "cuenta": "no hay ningun grupo: 0",
                "pasos": [], "vuelta": "", "vuelta_ok": True}
    # PASO M.13 (arreglo): sumar grupo a grupo esta bien con pocos grupos; con mas de cien, un humano no
    # hace 999 999 sumas (5 x 999999 tardaba 75 s): se hace de otra manera.
    if u.viene_despues(u.decir(s["veces"]), "cien"):
        raise ValueError("son mas de cien grupos: no se suman uno a uno, se hace de otra manera")
    total, marca, pasos = s["n"], "uno", []
    while marca != u.decir(s["veces"]):
        r = u.usar("sumar", a=total, b=s["n"])
        pasos.append("%d + %d = %d (%s)" % (total, s["n"], r["valor"], r["resultado"]["metodo"]))
        total = r["valor"]
        marca = u.siguiente(marca)
    return {"valor": total, "metodo": "sumar grupo a grupo (M.0)",
            "cuenta": "; ".join(pasos) or "un solo grupo: no hay nada que sumar, son %d" % total,
            "pasos": pasos, "vuelta": "", "vuelta_ok": True}
