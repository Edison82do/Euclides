# -*- coding: utf-8 -*-
"""Pieza de PROBAR EN ORDEN (paso S.3; NCETM 1.31, punto 5: 'algunos problemas no se dejan dibujar facilmente,
pero se resuelven probando y mejorando de forma SISTEMATICA; pueden tener una solucion, varias o ninguna').
Una ecuacion PONE EL TOPE y la otra se COMPRUEBA en cada prueba:
  - el producto, a x b = 24: las parejas de factores (M.15), en los dos ordenes;
  - la suma, a + b = 10: a va de 0 a 10 y b es lo que falta (10 - a);
  - la suma con pesos, 2 x a + 3 x b = 20: el que MAS pesa va de 0 hasta donde cabe (menos pruebas), y el otro
    es lo que queda repartido entre su peso (si no sale justo, esa prueba no vale).
En orden, para no dejarse ninguna y saber si hay una, varias o ninguna (con enteros desde el 0).  Un humano no
prueba cientos de veces: si harian falta mas pruebas que el tope (conocimiento/dos_incognitas.kn), todavia no.
Se COMPRUEBA poniendo cada solucion en TODAS las ecuaciones, y contando otra vez las pruebas hechas."""

PIEZA = {
    "id": "probar_en_orden",
    "nombre": "probar en orden (sistematico): una ecuacion pone el tope, la otra se comprueba",
    "unidad": "S.3",
    "responde": "dos_incognitas",
    "rapidez": 40,
    "que_hace": "a x b = 24; a + b = 10:  1 x 24 (25, no), 2 x 12 (14, no), 3 x 8 (11, no), 4 x 6 (10, SI) ...",
    "condiciones": [
        ("no_es_una_suma_sola", "es una suma sola: sus parejas se cuentan sin probarlas"),
        ("una_ecuacion_pone_el_tope", "ninguna ecuacion pone un tope (un producto o una suma de enteros)"),
    ],
    "usa": ["combinar", "dividir", "parejas_de_factores", "cumplen_las_ecuaciones"],
}


def hacer(s, u):
    tope = (u.saber.get("dos_incognitas") or {}).get("tope_de_pruebas", "30")
    tope_p = u.decir(_n(u, tope))
    tope_eq = _el_tope(s["ecuaciones"])
    otras = [e for e in s["ecuaciones"] if e is not tope_eq]
    if tope_eq["tipo"] == "producto":
        candidatos, cuantas_p, como = _por_los_factores(u, tope_eq, tope_p)
    else:
        candidatos, cuantas_p, como = _de_cero_hasta_donde_cabe(u, tope_eq, tope_p)
    pasos = ["EL TOPE lo pone %s: %s" % (tope_eq["texto"], como)]
    if otras:
        pasos.append("en cada prueba COMPRUEBO %s" % " y ".join(e["texto"] for e in otras))
    soluciones, hechas, torcidas = [], "cero", []
    for valores, nota in candidatos:
        hechas = u.siguiente(hechas)                       # cuento las pruebas recitando
        prueba = ", ".join("%s = %s" % (l, valores[l]) for l in s["letras"] if l in valores)
        if nota:
            pasos.append("  %s: %s ... NO VALE" % (prueba, nota))
            continue
        t = u.usar("cumplen_las_ecuaciones", ecuaciones=[tope_eq], valores=valores)
        if t["valor"] != "si" or not t["resultado"]["vuelta_ok"]:
            torcidas.append(prueba)                        # la prueba ni siquiera cumple el tope: algo se calculo mal
        if not otras:
            soluciones.append(valores)
            pasos.append("  %s ... SI" % prueba)
            continue
        r = u.usar("cumplen_las_ecuaciones", ecuaciones=otras, valores=valores)
        si = r["valor"] == "si"
        pasos.append("  %s: %s" % (prueba, "; ".join(x.split("  ->  ", 1)[1] for x in r["resultado"]["lineas"])))
        if si:
            soluciones.append(valores)
    if not otras:
        pasos.append("son las de ENTEROS; con DECIMALES habria infinitas (no hay otra ecuacion que las pare)")
    cuantas = "ninguna" if not soluciones else ("una" if not soluciones[1:] else "varias")
    valor = "ninguna" if not soluciones else "; ".join(_escribir(s["letras"], v) for v in soluciones)
    r = {"valor": valor, "soluciones": soluciones, "cuantas": cuantas, "pruebas": "%d" % u.leer(hechas),
         "metodo": "probar en orden, de forma sistematica (NCETM 1.31, punto 5), con enteros desde el %s"
                   % ("1" if tope_eq["tipo"] == "producto" else "0"),
         "pasos": pasos}
    # LA VUELTA: cada solucion en TODAS las ecuaciones; y las pruebas hechas son todas las que habia
    trozos, ok = [], hechas == cuantas_p and not torcidas
    if torcidas:
        trozos.append("estas pruebas NO cumplen el tope, algo se calculo mal: %s" % "; ".join(torcidas))
    else:
        trozos.append("cada prueba cumple %s" % tope_eq["texto"])
    trozos.append("conte otra vez las pruebas: hice %d y tenia que hacer %d: %s" % (
        u.leer(hechas), u.leer(cuantas_p), "estan TODAS" if ok else "FALTAN"))
    for v in soluciones:
        t, bien = _comprobar(u, s, v)
        trozos.append(t)
        ok = ok and bien
    r["vuelta"], r["vuelta_ok"] = "; ".join(trozos), ok
    return r


def _el_tope(eqs):
    """El producto si lo hay (pocas parejas); si no, una suma sin pesos; si no, una con pesos."""
    for quiere in ("producto", "suma", "lineal"):
        for e in eqs:
            if e["tipo"] == "producto" and quiere == "producto" and e["n"].isdigit() and e["n"].strip("0"):
                return e
            if e["tipo"] == "lineal" and e["n"].isdigit() and all(c.isdigit() for c in e["coef"].values()):
                if quiere == "lineal" or set(e["coef"].values()) == {"1"}:
                    return e
    raise ValueError("ninguna ecuacion pone un tope")


def _demasiadas(u, cuantas_p, tope_p, que):
    if cuantas_p is None:
        raise ValueError("harian falta mas pruebas que mi techo (%s): todavia no" % que)
    if u.viene_despues(cuantas_p, tope_p):
        raise ValueError("harian falta %d pruebas (%s), y un humano no prueba tantas una a una: todavia no "
                         "(el tope es %d)" % (u.leer(cuantas_p), que, u.leer(tope_p)))


def _por_los_factores(u, eq, tope_p):
    a, b = eq["letras"]
    r = u.usar("parejas_de_factores", n=_n(u, eq["n"]))
    parejas = r["resultado"]["parejas"]
    todas = [(f, g) for f, g in parejas]                  # a la ida, y luego al reves (si no son iguales)
    todas.extend((g, f) for f, g in reversed(parejas) if f != g)
    cuantas_p = "cero"
    for _ in todas:
        cuantas_p = u.siguiente(cuantas_p)
    _demasiadas(u, cuantas_p, tope_p, "las parejas de factores de %s" % eq["n"])
    candidatos = [({a: "%d" % f, b: "%d" % g}, "") for f, g in todas]
    como = "las parejas de factores de %s (M.15: %s), en los dos ordenes: %d pruebas" % (
        eq["n"], r["valor"], u.leer(cuantas_p))
    return candidatos, cuantas_p, como


def _de_cero_hasta_donde_cabe(u, eq, tope_p):
    a, b = eq["letras"]
    ca, cb = eq["coef"][a], eq["coef"][b]
    x, y, cx, cy = a, b, ca, cb
    if u.viene_despues(u.decir(_n(u, cb)), u.decir(_n(u, ca))):
        x, y, cx, cy = b, a, cb, ca                         # pruebo con el que MAS pesa: menos pruebas
    n = eq["n"]
    if cx == "1":
        hasta = n
    else:
        hasta = "%d" % u.usar("dividir", total=_n(u, n), divisor=_n(u, cx))["valor"]
    hasta_p = u.decir(_n(u, hasta))
    cuantas_p = u.siguiente(hasta_p)
    _demasiadas(u, cuantas_p, tope_p, "%s de 0 a %s" % (x, hasta))
    como = "%s va de 0 a %s (%d pruebas)%s" % (
        x, hasta, u.leer(cuantas_p), "" if cx == "1" else ": %s x %s ya se pasaria de %s" % (cx, u.leer(u.siguiente(hasta_p)), n))
    candidatos, w = [], "cero"
    while True:
        vx = "%d" % u.leer(w)
        usado = vx if cx == "1" else _cuenta(u, [["+", [cx, vx]]])
        queda = _cuenta(u, [["+", [n]], ["-", [usado]]])
        if cy == "1":
            candidatos.append(({x: vx, y: queda}, ""))
        else:
            d = u.usar("dividir", total=_n(u, queda), divisor=_n(u, cy))
            if d["resultado"].get("resto"):
                candidatos.append(({x: vx}, "quedan %s, y %s : %s no sale justo" % (queda, queda, cy)))
            else:
                candidatos.append(({x: vx, y: "%d" % d["valor"]}, ""))
        if w == hasta_p:
            break
        w = u.siguiente(w)
    return candidatos, cuantas_p, como


def _comprobar(u, s, valores):
    r = u.usar("cumplen_las_ecuaciones", ecuaciones=s["ecuaciones"], valores=valores)
    return "; ".join(r["resultado"]["lineas"]), r["valor"] == "si" and r["resultado"]["vuelta_ok"]


def _cuenta(u, terminos):
    try:
        return _normal(u.usar("combinar", terminos=terminos)["valor"])
    except Exception as e:                          # 'combinar' no sale (por debajo del cero, o se pasa del techo)
        raise ValueError(str(e))


def _escribir(letras, valores):
    return ", ".join("%s = %s" % (l, valores[l]) for l in letras)


def _n(u, f):
    """'175' -> 175: LEER las cifras de un entero escrito."""
    return u.escribir_cifras([int(c) for c in reversed(f)])


def _normal(f):
    if "." in f:
        f = f.rstrip("0").rstrip(".")
    e, punto, d = f.partition(".")
    e = e.lstrip("0") or "0"
    return "%s.%s" % (e, d) if punto else e
