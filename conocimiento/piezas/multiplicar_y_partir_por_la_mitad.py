# -*- coding: utf-8 -*-
"""Pieza de LA MITAD DE UN PRODUCTO en el orden de siempre (paso M.24; NCETM 2.30, punto 2: 'multiplicar la base por
la altura perpendicular y luego dividir entre dos').
    7 x 3 : 2   ->  7 x 3 = 21;  la mitad de 21 es 10, y sobra 1 (10 y medio)
    6 x 4 : 2   ->  6 x 4 = 24;  la mitad de 24 es 12
Sirve siempre (tambien con los dos factores impares), pero cuesta mas que partir antes el factor par: el producto
entero es un numero mas grande.  Es el segundo camino.
OJO, el error tipico: olvidar la mitad (el area del triangulo NO es la del paralelogramo).
LA VUELTA, con la contraria: la mitad mas la mitad (mas lo que sobro) vuelve al producto (el producto ya lo comprueba
la multiplicacion con su propia vuelta)."""

PIEZA = {
    "id": "multiplicar_y_partir_por_la_mitad",
    "nombre": "multiplicar y luego partir por la mitad (7 x 3 : 2 = 21 : 2)",
    "unidad": "M.24",
    "responde": "mitad_de_un_producto",
    "rapidez": 6,
    "que_hace": "7 x 3 : 2 = 21 : 2 = 10 y medio (NCETM 2.30)",
    "condiciones": [
        ("es_un_producto_de_dos_enteros_entre_dos", "no es a x b : 2 con dos enteros (que no sean 0)"),
    ],
    "usa": ["dividir", "multiplicar", "sumar"],
}


def hacer(s, u):
    a, b = s["a"], s["b"]
    producto = u.usar("multiplicar", a=a, b=b)["valor"]
    if u.decir(producto) is None:
        raise ValueError("el producto se pasa de mi lista")
    r = u.usar("dividir", total=producto, divisor=2)
    v, resto = r["valor"], r["resultado"].get("resto", 0)
    pasos = ["%d x %d = %d" % (a, b, producto),
             "la mitad de %d es %d%s" % (producto, v, " y sobra 1 (y medio)" if resto else "")]
    # LA VUELTA: la mitad mas la mitad (mas lo que sobro) vuelve al producto
    doble = u.usar("sumar", a=v, b=v)["valor"] if v else 0
    if resto:
        doble = u.usar("sumar", a=doble, b=1)["valor"] if doble else 1
    ok = doble == producto
    return {"valor": v, "resto": resto,
            "metodo": "multiplicar y partir por la mitad (M.24; NCETM 2.30)",
            "pasos": pasos, "cuenta": "; ".join(pasos),
            "vuelta": "%d + %d%s = %d ... %s" % (v, v, " + 1" if resto else "", doble, "SI" if ok else "NO"),
            "vuelta_ok": ok,
            "vuelta_explicada": "la mitad dos veces%s vuelve a %d (y el producto lo comprobo la multiplicacion con "
                                "su propia vuelta)" % (" (y lo que sobro)" if resto else "", producto)}
