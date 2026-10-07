# -*- coding: utf-8 -*-
"""Pieza de HALLAR EL TODO JUNTANDO PRIMERO LAS PAREJAS AMIGAS (paso S.2; NCETM 1.28, punto 2: 'estrategias
distintas, la misma estructura').  Con tres partes o mas, se mira si dos hacen un numero redondo: sus ultimas
cifras (con el punto en su sitio) hacen DIEZ.  Partes 37, 25, 63: el 7 y el 3 hacen diez (contado con los
dedos), asi que 37 + 63 = 100 primero; y luego 100 + 25 = 125.  Con decimales igual: 1.25 y 0.75 (5 y 5) hacen 2.
Las sumas las hace 'combinar' (M.16).  Se COMPRUEBA quitando al todo las partes, de la ultima a la primera."""

PIEZA = {
    "id": "todo_juntando_las_parejas_amigas",
    "nombre": "juntar primero las dos partes que hacen un numero redondo",
    "unidad": "S.2",
    "responde": "todo_de_las_partes",
    "rapidez": 8,
    "que_hace": "37, 25, 63 -> 37 + 63 = 100 (7 y 3 hacen diez); 100 + 25 = 125",
    "condiciones": [
        ("se_saben_todas_las_partes", "no se saben todas las partes: no es buscar el todo"),
        ("hay_tres_partes_o_mas", "son solo dos partes: no hay orden que elegir"),
        ("hay_dos_partes_amigas", "no hay dos partes cuyas ultimas cifras hagan diez"),
    ],
    "usa": ["combinar"],
}


def hacer(s, u):
    partes = [_normal(p) for p in s["partes"]]
    i, j = _la_pareja(partes, u)
    orden = [partes[i], partes[j]]
    orden.extend(p for k, p in enumerate(partes) if k not in (i, j))
    r = u.usar("combinar", terminos=[["+", [p]] for p in orden])
    todo = r["valor"]
    k = _decimales(partes[i], partes[j])
    aviso = "%s y %s son AMIGAS: %s y %s hacen diez (contado con los dedos); las junto primero" % (
        partes[i], partes[j], _ultima(partes[i], k), _ultima(partes[j], k))
    vuelta, ok = _quitar_de_la_ultima_a_la_primera(u, todo, orden)
    return {"valor": todo, "metodo": "las parejas amigas primero (NCETM 1.28, S.2)", "orden": orden,
            "pasos": [aviso] + r["resultado"]["pasos"], "vuelta": vuelta, "vuelta_ok": ok}


def _decimales(f, g):
    return max(len(f.partition(".")[2]), len(g.partition(".")[2]))


def _ultima(f, k):
    """La ultima cifra con el punto alineado a k cifras (escribir ceros a la derecha, no calcular)."""
    e, _, d = f.partition(".")
    return d.ljust(k, "0")[-1] if k else e[-1]


def _amigas(f, g, u):
    k = _decimales(f, g)
    a, b = _ultima(f, k), _ultima(g, k)
    if a == "0" or b == "0":
        return False
    return u.contar_adelante(u.decir(int(a)), u.decir(int(b))).get("resultado") == "diez"


def _la_pareja(partes, u):
    for i, f in enumerate(partes):
        for j in range(i, len(partes)):
            if j != i and _amigas(f, partes[j], u):
                return i, j
    raise ValueError("no hay dos partes amigas")


def _quitar_de_la_ultima_a_la_primera(u, todo, partes):
    terminos = [["+", [todo]]]
    terminos.extend(["-", [p]] for p in reversed(partes[1:]))
    texto = " - ".join([todo] + list(reversed(partes[1:])))
    try:
        queda = u.usar("combinar", terminos=terminos)["valor"]
    except Exception as e:
        return "%s: no se puede (%s)" % (texto, e), False
    bien = _normal(queda) == partes[0]
    return "%s = %s%s" % (texto, queda, "" if bien else " (y tenia que quedar %s)" % partes[0]), bien


def _normal(f):
    if "." in f:
        f = f.rstrip("0").rstrip(".")
    e, punto, d = f.partition(".")
    e = e.lstrip("0") or "0"
    return "%s.%s" % (e, d) if punto else e
