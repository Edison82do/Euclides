# -*- coding: utf-8 -*-
"""Pieza de DIFERENCIA Y MULTIPLO CON LA BARRA (paso S.3; NCETM 1.31, puntos 2 y 3: la misma barra, con la relacion
aditiva y la multiplicativa a la vez).  a - b = 20; a = 3 x b.  La barra de b es UN trozo; la de a, TRES.  Lo que
a tiene DE MAS son los trozos de a que no estan en b: uno menos que tres = DOS trozos (se recita hacia atras), y
eso es la diferencia: 20 : 2 = 10 = b; a = 3 x 10 = 30.  El error tipico es repartir la diferencia entre 3.
Si a es 1 vez b (son iguales), no tiene trozos de mas: con diferencia 0, infinitas; si no, ninguna.
Se COMPRUEBA poniendo los numeros en las DOS ecuaciones (30 - 10 = 20; 3 x 10 = 30)."""

PIEZA = {
    "id": "diferencia_y_multiplo_con_la_barra",
    "nombre": "la barra: los trozos de mas son la diferencia",
    "unidad": "S.3",
    "responde": "dos_incognitas",
    "rapidez": 10,
    "que_hace": "a - b = 20; a = 3 x b:  3 - 1 = 2 trozos de mas;  20 : 2 = 10 = b;  a = 3 x 10 = 30",
    "condiciones": [
        ("se_dan_la_diferencia_y_un_multiplo_del_mismo_lado", "no se dan la diferencia y cuantas veces la grande es la pequena"),
    ],
    "usa": ["combinar", "dividir", "dividir_decimal", "cumplen_las_ecuaciones"],
}


def hacer(s, u):
    dif = [e for e in s["ecuaciones"] if e["tipo"] == "diferencia"][0]
    mul = [e for e in s["ecuaciones"] if e["tipo"] == "multiplo"][0]
    grande, chica, k, d = mul["grande"], mul["chico"], mul["k"], _normal(dif["n"])
    de_mas = u.anterior(u.decir(_n(u, k)))                 # los k trozos de la grande, menos el que tiene la pequena
    pasos = ["%s es UN trozo; %s son %s trozos: %s tiene %s trozos DE MAS (uno menos que %s), y eso es la diferencia, %s"
             % (chica, grande, k, grande, de_mas.upper(), k, d)]
    if de_mas == "cero":
        return _iguales(u, s, grande, chica, d, pasos)
    n = "%d" % u.leer(de_mas)
    v_chica = _repartir(u, d, n)
    pasos.append("reparto la diferencia en los %s trozos: %s : %s = %s  ->  %s = %s" % (n, d, n, v_chica, chica, v_chica))
    v_grande = _cuenta(u, [["+", [k, v_chica]]])
    pasos.append("%s son %s trozos: %s x %s = %s  ->  %s = %s" % (grande, k, k, v_chica, v_grande, grande, v_grande))
    valores = {grande: v_grande, chica: v_chica}
    r = {"valor": _escribir(s["letras"], valores), "soluciones": [valores], "cuantas": "una", "trozos": n,
         "metodo": "la barra: %s trozos de mas son la diferencia (NCETM 1.31)" % n, "pasos": pasos}
    if "." in v_chica and "." not in d:
        r["con_enteros"] = "con enteros no habria NINGUNA: %s no se reparte justo en %s" % (d, n)
    r["vuelta"], r["vuelta_ok"] = _comprobar(u, s, valores)
    return r


def _iguales(u, s, grande, chica, d, pasos):
    """a = 1 x b: son la misma barra.  Diferencia 0: cualquier pareja igual (infinitas); si no, ninguna.
    Se comprueba con un ejemplo: con los dos iguales, la diferencia sale cero."""
    ejemplo = {grande: "5", chica: "5"}
    r = u.usar("cumplen_las_ecuaciones", ecuaciones=s["ecuaciones"], valores=ejemplo)
    si = r["valor"] == "si"
    if d == "0":
        pasos.append("son la MISMA barra y la diferencia es 0: vale cualquier pareja de iguales")
        return {"valor": "infinitas", "soluciones": [], "cuantas": "infinitas", "pasos": pasos,
                "metodo": "la barra: las dos son iguales (NCETM 1.31, punto 1)",
                "vuelta": "un ejemplo, %s = 5 y %s = 5: %s" % (grande, chica, "; ".join(r["resultado"]["lineas"])),
                "vuelta_ok": si and r["resultado"]["vuelta_ok"]}
    pasos.append("son la MISMA barra: no puede tener %s de mas" % d)
    return {"valor": "ninguna", "soluciones": [], "cuantas": "ninguna", "pasos": pasos,
            "metodo": "la barra: las dos son iguales (NCETM 1.31, punto 1)",
            "vuelta": "un ejemplo, %s = 5 y %s = 5: %s" % (grande, chica, "; ".join(r["resultado"]["lineas"])),
            "vuelta_ok": (not si) and r["resultado"]["vuelta_ok"]}


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
