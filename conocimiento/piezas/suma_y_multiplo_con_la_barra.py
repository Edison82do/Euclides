# -*- coding: utf-8 -*-
"""Pieza de SUMA Y MULTIPLO CON LA BARRA (paso S.3; NCETM 1.31, puntos 2, 3 y 4).  a + b = 24; a = 3 x b.  La barra
de b es UN trozo; la de a, TRES trozos como ese (la relacion MULTIPLICATIVA).  Juntas son 3 y uno mas = CUATRO
trozos iguales (se cuentan recitando: despues del tres, el cuatro): 24 : 4 = 6 = b; a = 3 x 6 = 18.
El error tipico es repartir entre 3 (24 : 3 = 8) y olvidar el trozo de b.  Solo hay UNA solucion.
Si el reparto no sale justo, se reparte en decimas (M.13): a + b = 10; a = 3 x b -> 10 : 4 = 2.5.
Se COMPRUEBA poniendo los numeros en las DOS ecuaciones (18 + 6 = 24; 3 x 6 = 18)."""

PIEZA = {
    "id": "suma_y_multiplo_con_la_barra",
    "nombre": "la barra: contar los trozos iguales y repartir la suma",
    "unidad": "S.3",
    "responde": "dos_incognitas",
    "rapidez": 10,
    "que_hace": "a + b = 24; a = 3 x b:  3 + 1 = 4 trozos;  24 : 4 = 6 = b;  a = 3 x 6 = 18",
    "condiciones": [
        ("se_dan_la_suma_y_un_multiplo", "no se dan la suma de las dos y cuantas veces es una la otra"),
    ],
    "usa": ["combinar", "dividir", "dividir_decimal", "cumplen_las_ecuaciones"],
}


def hacer(s, u):
    suma = [e for e in s["ecuaciones"] if e["tipo"] == "lineal"][0]
    mul = [e for e in s["ecuaciones"] if e["tipo"] == "multiplo"][0]
    grande, chica, k, total = mul["grande"], mul["chico"], mul["k"], _normal(suma["n"])
    trozos = u.siguiente(u.decir(_n(u, k)))                 # los k trozos de la grande y UNO mas, el de la pequena
    n = "%d" % u.leer(trozos)
    pasos = ["%s es UN trozo; %s son %s trozos como ese: juntas, %s y uno mas = %s trozos IGUALES" % (
        chica, grande, k, k, trozos.upper())]
    v_chica = _repartir(u, total, n)
    pasos.append("reparto la suma en los %s trozos: %s : %s = %s  ->  %s = %s" % (n, total, n, v_chica, chica, v_chica))
    v_grande = _cuenta(u, [["+", [k, v_chica]]])
    pasos.append("%s son %s trozos: %s x %s = %s  ->  %s = %s" % (grande, k, k, v_chica, v_grande, grande, v_grande))
    valores = {grande: v_grande, chica: v_chica}
    r = {"valor": _escribir(s["letras"], valores), "soluciones": [valores], "cuantas": "una", "trozos": n,
         "metodo": "la barra: %s trozos iguales (NCETM 1.31, punto 4: suma y multiplo)" % n, "pasos": pasos}
    if "." in v_chica and "." not in total:
        r["con_enteros"] = "con enteros no habria NINGUNA: %s no se reparte justo en %s" % (total, n)
    r["vuelta"], r["vuelta_ok"] = _comprobar(u, s, valores)
    return r


def _comprobar(u, s, valores):
    r = u.usar("cumplen_las_ecuaciones", ecuaciones=s["ecuaciones"], valores=valores)
    return "; ".join(r["resultado"]["lineas"]), r["valor"] == "si" and r["resultado"]["vuelta_ok"]


def _cuenta(u, terminos):
    try:
        return _normal(u.usar("combinar", terminos=terminos)["valor"])
    except Exception as e:                          # 'combinar' no sale (por debajo del cero, o se pasa del techo)
        raise ValueError(str(e))


def _repartir(u, x, entre="2"):
    """x : entre.  Con enteros, primero la division de siempre (las tablas, tambien la del 11 y la del 12); si
    sobra algo, en decimas, centesimas o milesimas (M.13)."""
    if "." not in x:
        try:
            r = u.usar("dividir", total=_n(u, x), divisor=_n(u, entre))
            if not r["resultado"].get("resto"):
                return "%d" % r["valor"]
        except Exception:
            pass
    try:
        return _normal(u.usar("dividir_decimal", x=x, d=entre)["valor"])
    except Exception as e:
        raise ValueError("%s : %s no me sale: %s" % (x, entre, e))


def _escribir(letras, valores):
    return ", ".join("%s = %s" % (l, valores[l]) for l in letras)


def _alinear(f, g):
    e1, _, d1 = f.partition(".")
    e2, _, d2 = g.partition(".")
    k = max(len(d1), len(d2))
    return ("%s%s" % (e1, d1.ljust(k, "0"))).lstrip("0") or "0", ("%s%s" % (e2, d2.ljust(k, "0"))).lstrip("0") or "0"


def _n(u, f):
    """'175' -> 175: LEER las cifras de un entero escrito."""
    return u.escribir_cifras([int(c) for c in reversed(f)])


def _normal(f):
    if "." in f:
        f = f.rstrip("0").rstrip(".")
    e, punto, d = f.partition(".")
    e = e.lstrip("0") or "0"
    return "%s.%s" % (e, d) if punto else e
