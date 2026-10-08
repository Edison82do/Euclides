# -*- coding: utf-8 -*-
"""Pieza de SUMA Y DIFERENCIA CON LA BARRA, ANADIENDO LA DIFERENCIA (paso S.3; NCETM 1.31, puntos 3 y 4).  La misma
barra que 'quitando la diferencia', mirada al reves: si a la barra pequena le ANADO el trozo que le falta, quedan
DOS barras como la GRANDE: a + b = 30; a - b = 8 -> 30 + 8 = 38; 38 : 2 = 19 = a; y b = 19 - 8 = 11.
Tiene que dar lo mismo que quitando (la estructura no cambia).  Si la diferencia no cabe en la suma, la pequena
saldria por debajo del cero: NINGUNA.  Se COMPRUEBA poniendo los numeros en las DOS ecuaciones."""

PIEZA = {
    "id": "suma_y_diferencia_anadiendo_la_diferencia",
    "nombre": "la barra: anadir la diferencia y repartir en dos iguales",
    "unidad": "S.3",
    "responde": "dos_incognitas",
    "rapidez": 11,
    "que_hace": "a + b = 30; a - b = 8:  30 + 8 = 38;  38 : 2 = 19 = a;  b = 19 - 8 = 11",
    "condiciones": [
        ("se_dan_la_suma_y_la_diferencia", "no se dan la suma de las dos y su diferencia"),
    ],
    "usa": ["combinar", "dividir", "dividir_decimal", "cumplen_las_ecuaciones"],
}


def hacer(s, u):
    suma, dif = _la_suma_y_la_otra(s, "diferencia")
    mayor, menor, d, total = dif["mayor"], dif["menor"], _normal(dif["n"]), _normal(suma["n"])
    juntas = _cuenta(u, [["+", [total]], ["+", [d]]])
    pasos = ["ANADO la diferencia a la barra pequena: %s + %s = %s  (quedan DOS barras iguales, las dos como %s)"
             % (total, d, juntas, mayor)]
    grande = _repartir(u, juntas)
    pasos.append("las reparto en dos: %s : 2 = %s  ->  %s = %s" % (juntas, grande, mayor, grande))
    try:
        chica = _cuenta(u, [["+", [grande]], ["-", [d]]])
    except ValueError as e:
        if "debajo del cero" not in str(e):
            raise
        return _ninguna(u, s, total, d)
    pasos.append("%s es %s quitandole %s: %s - %s = %s  ->  %s = %s" % (menor, mayor, d, grande, d, chica, menor, chica))
    valores = {mayor: grande, menor: chica}
    r = {"valor": _escribir(s["letras"], valores), "soluciones": [valores], "cuantas": "una",
         "metodo": "la barra: anadir la diferencia y repartir en dos (NCETM 1.31, punto 4)", "pasos": pasos}
    if "." in grande and not any("." in x for x in (total, d)):
        r["con_enteros"] = "con enteros no habria NINGUNA: %s es impar y no se reparte justo en dos" % juntas
    r["vuelta"], r["vuelta_ok"] = _comprobar(u, s, valores)
    return r


def _ninguna(u, s, total, d):
    """La pequena saldria por debajo del cero: la diferencia no cabe en la suma.  Se comprueba mirando la lista."""
    a, b = _alinear(total, d)
    pasa = u.viene_despues(u.decir(_n(u, b)), u.decir(_n(u, a)))
    return {"valor": "ninguna", "soluciones": [], "cuantas": "ninguna",
            "metodo": "la barra: la diferencia no cabe en la suma (NCETM 1.31, punto 1)",
            "pasos": ["la pequena saldria por debajo del cero: la diferencia (%s) es MAYOR que la suma (%s)" % (d, total)],
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
