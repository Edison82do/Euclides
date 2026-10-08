# -*- coding: utf-8 -*-
"""Pieza de SUMA Y DIFERENCIA CON LA BARRA, QUITANDO LA DIFERENCIA (paso S.3; NCETM 1.31, puntos 3 y 4).
a + b = 30; a - b = 8.  Las dos barras, alineadas: la de a es como la de b y un trozo de 8 mas.  Si QUITO la
diferencia del todo, quedan DOS barras IGUALES (las dos como b): 30 - 8 = 22; 22 : 2 = 11 = b; y a = 11 + 8 = 19.
Solo hay UNA solucion: la barra no deja otra manera de repartir.  Si la diferencia no cabe en la suma, NINGUNA
(con numeros que se cuentan).  Si queda un impar, con enteros ninguna; con decimales se reparte en decimas (M.13).
Se COMPRUEBA poniendo los numeros en las DOS ecuaciones (19 + 11 = 30; 19 - 11 = 8)."""

PIEZA = {
    "id": "suma_y_diferencia_quitando_la_diferencia",
    "nombre": "la barra: quitar la diferencia y repartir en dos iguales",
    "unidad": "S.3",
    "responde": "dos_incognitas",
    "rapidez": 10,
    "que_hace": "a + b = 30; a - b = 8:  30 - 8 = 22;  22 : 2 = 11 = b;  a = 11 + 8 = 19",
    "condiciones": [
        ("se_dan_la_suma_y_la_diferencia", "no se dan la suma de las dos y su diferencia"),
    ],
    "usa": ["combinar", "dividir", "dividir_decimal", "cumplen_las_ecuaciones"],
}


def hacer(s, u):
    suma, dif = _la_suma_y_la_otra(s, "diferencia")
    mayor, menor, d, total = dif["mayor"], dif["menor"], _normal(dif["n"]), _normal(suma["n"])
    try:
        quedan = _cuenta(u, [["+", [total]], ["-", [d]]])
    except ValueError as e:
        if "debajo del cero" not in str(e):
            raise
        return _ninguna(u, s, total, d)
    pasos = ["QUITO la diferencia: %s - %s = %s  (quedan DOS barras iguales, las dos como %s)" % (total, d, quedan, menor)]
    chica = _repartir(u, quedan)
    pasos.append("las reparto en dos: %s : 2 = %s  ->  %s = %s" % (quedan, chica, menor, chica))
    grande = _cuenta(u, [["+", [chica]], ["+", [d]]])
    pasos.append("%s es %s y %s mas: %s + %s = %s  ->  %s = %s" % (mayor, menor, d, chica, d, grande, mayor, grande))
    valores = {mayor: grande, menor: chica}
    r = {"valor": _escribir(s["letras"], valores), "soluciones": [valores], "cuantas": "una",
         "metodo": "la barra: quitar la diferencia y repartir en dos (NCETM 1.31, punto 4)", "pasos": pasos}
    if "." in chica and not any("." in x for x in (total, d)):
        r["con_enteros"] = "con enteros no habria NINGUNA: %s es impar y no se reparte justo en dos" % quedan
    r["vuelta"], r["vuelta_ok"] = _comprobar(u, s, valores)
    return r


def _ninguna(u, s, total, d):
    """La diferencia no cabe en la suma: la barra grande sola ya se pasa del todo.  Se comprueba mirando la lista."""
    a, b = _alinear(total, d)
    pasa = u.viene_despues(u.decir(_n(u, b)), u.decir(_n(u, a)))
    return {"valor": "ninguna", "soluciones": [], "cuantas": "ninguna",
            "metodo": "la barra: la diferencia no cabe en la suma (NCETM 1.31, punto 1)",
            "pasos": ["QUITO la diferencia: %s - %s ... no se puede: la diferencia es MAYOR que la suma; la barra grande "
                      "sola ya se pasaria del todo" % (total, d)],
            "vuelta": "%s viene despues de %s en la lista: %s" % (d, total, "SI, es mayor" if pasa else "NO"),
            "vuelta_ok": pasa}


def _la_suma_y_la_otra(s, tipo):
    eqs = s["ecuaciones"]
    suma = [e for e in eqs if e["tipo"] == "lineal"][0]
    return suma, [e for e in eqs if e["tipo"] == tipo][0]


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
