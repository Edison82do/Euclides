# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso M.17; NCETM 2.23, punto 5): UN FACTOR COMPUESTO.  Si un factor de dos cifras es una
pareja de la tabla (24 = 4 x 6, 15 = 3 x 5), se multiplica por uno de sus factores y luego por el otro: dos
multiplicaciones cortas, sin sumar nada.
    1234 x 24 = 1234 x 4 x 6:  1234 x 4 = 4936;  4936 x 6 = 29616
La pareja se busca en lo que se sabe de memoria (las tablas), la de en medio (24 -> 4 x 6, no 3 x 8).
LA VUELTA: repartir el resultado entre el segundo factor y luego entre el primero (la division corta) vuelve a dar
el numero de partida."""

PIEZA = {
    "id": "multiplicar_por_un_factor_compuesto",
    "nombre": "un factor compuesto (24 = 4 x 6: por 4 y por 6)",
    "unidad": "M.17",
    "responde": "multiplicar",
    "rapidez": 9.2,
    "que_hace": "parte un factor de dos cifras en dos de la tabla (24 = 4 x 6) y hace dos multiplicaciones cortas",
    "condiciones": [
        ("un_factor_de_dos_cifras_es_una_pareja_de_la_tabla",
         "ningun factor de dos cifras es una pareja de la tabla que me sepa (24 = 4 x 6), con el otro de varias cifras"),
    ],
    "usa": ["multiplicacion_corta"],
}


def _repartir(u, n, d):
    """La operacion contraria de x d (d de una cifra): n : d de IZQUIERDA a derecha, como la division corta (M.11),
    cuantas veces cabe con la tabla del d que se sabe; lo que sobra se cambia por diez de la columna de al lado.
    (Se hace aqui y no con la pieza division_corta: esa se comprueba multiplicando, y seria una vuelta en el mapa.)
    Devuelve (cociente, resto)."""
    cociente, sobra = [], 0
    for c in reversed(u.cifras_de(n)):
        cs = [c]
        cs.extend(u.cifras_de(sobra) if sobra else [])
        actual = u.escribir_cifras(cs)
        q, p = 0, 0
        for k in range(1, 10):
            h = u.recuerdo("%d x %d" % (k, d)) or u.recuerdo("%d x %d" % (d, k))
            if k == 1:
                h = {"valor": d}
            if not h:
                raise ValueError("no se de memoria %d x %d (primero hay que saberse las tablas)" % (k, d))
            if h["valor"] != actual and u.viene_despues(u.decir(h["valor"]), u.decir(actual)):
                break
            q, p = k, h["valor"]
        sobra = u.leer(u.contar_hasta(u.decir(p), u.decir(actual))) if p else actual
        if cociente or q:
            cociente.append(q)
    return (u.escribir_cifras(list(reversed(cociente))) if cociente else 0), sobra


def _pareja(u, f):
    if len(u.cifras_de(f)) != 2 or u.cifras_de(f)[0] == 0:
        return None
    mejor = None
    for p in range(2, 10):
        for q in range(p, 10):
            h = u.recuerdo("%d x %d" % (p, q)) or u.recuerdo("%d x %d" % (q, p))
            if h and h["valor"] == f:
                mejor = (p, q)
    return mejor


def hacer(s, u):
    a, b = s["a"], s["b"]
    for f, n in ((b, a), (a, b)):
        par = _pareja(u, f)
        if par and len(u.cifras_de(n)) >= 2:
            break
    else:
        raise ValueError("no hay un factor que sea una pareja de la tabla")
    p, q = par
    m1 = u.usar("multiplicacion_corta", a=n, b=p)
    m2 = u.usar("multiplicacion_corta", a=m1["valor"], b=q)
    total = m2["valor"]
    if u.decir(total) is None:
        raise ValueError("se sale de mi lista")
    # LA VUELTA: deshacer, de la ultima a la primera
    c2, r2 = _repartir(u, total, q)
    c1, r1 = _repartir(u, c2, p)
    ok = not r2 and not r1 and c2 == m1["valor"] and c1 == n
    return {"valor": total, "metodo": "un factor compuesto (M.17; NCETM 2.23)",
            "cuenta": "%d = %d x %d, asi que %d x %d = %d x %d x %d; %d x %d = %d   (la corta); %d x %d = %d   (la corta)"
                      % (f, p, q, n, f, n, p, q, n, p, m1["valor"], m1["valor"], q, total),
            "vuelta": "%d : %d = %d; %d : %d = %d ... %s" % (total, q, c2, c2, p, c1,
                                                            "SI" if ok else "NO"),
            "vuelta_ok": ok,
            "vuelta_explicada": "con la operacion contraria: repartiendo entre %d y luego entre %d vuelve %d" % (q, p, n)}
