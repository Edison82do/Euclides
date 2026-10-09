# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso M.17; NCETM 2.23, puntos 1 y 2): QUITAR LOS CEROS Y AJUSTAR CON EL VALOR DE POSICION.
Si un factor es multiplo de 10, 100 o 1000, se multiplica lo que queda sin los ceros (la multiplicacion corta, o la
larga si los dos siguen siendo de varias cifras) y luego se vuelven a poner TODOS los ceros:
    234 x 30:  234 x 3 = 702 (la corta)  ->  30 es diez veces 3, asi que el producto es diez veces 702 = 7020.
    2300 x 450:  23 x 45 = 1035  ->  tres ceros quitados, tres ceros puestos: 1 035 000.
(Si lo que queda es un hecho de la tabla, 300 x 40, es lo de M.9, que va antes.)
LA VUELTA: el producto, quitandole los ceros que puse (: 10, las cifras bajan), vuelve a dar el producto pequeno."""

PIEZA = {
    "id": "multiplicar_quitando_los_ceros",
    "nombre": "quitar los ceros y volver a ponerlos",
    "unidad": "M.17",
    "responde": "multiplicar",
    "rapidez": 7.5,
    "que_hace": "quita los ceros del final de los factores, multiplica lo que queda (corta o larga) y vuelve a poner todos los ceros",
    "condiciones": [
        ("un_factor_acaba_en_cero", "ningun factor son decenas justas (30, 80, 400...)"),
        ("quitando_los_ceros_queda_una_cuenta_de_varias_cifras",
         "quitando los ceros queda un hecho de la tabla (eso es lo de M.9)"),
    ],
    "usa": ["multiplicacion_corta", "multiplicar_partiendo_un_factor", "multiplicar_por_un_factor_compuesto",
            "multiplicacion_larga", "dividir_por_10_o_100"],
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


_POR_ORDEN = ("multiplicar_partiendo_un_factor", "multiplicar_por_un_factor_compuesto", "multiplicacion_larga")


def _sin_ceros(u, n):
    cif, ceros = u.cifras_de(n), []
    while len(cif) > 1 and cif[0] == 0:
        cif = cif[1:]
        ceros.append(0)
    return u.escribir_cifras(cif), ceros


def _lo_que_queda(u, pa, pb):
    """pa x pb sin ceros: la corta si uno es de una cifra; si no, lo primero que salga en el orden de un humano."""
    if len(u.cifras_de(pa)) == 1 or len(u.cifras_de(pb)) == 1:
        return u.usar("multiplicacion_corta", a=pa, b=pb)
    ultimo = None
    for pid in _POR_ORDEN:
        try:
            return u.usar(pid, a=pa, b=pb)
        except Exception as e:                  # no encaja o no sale: la siguiente
            ultimo = e
    raise ValueError("%d x %d no me sale (%s)" % (pa, pb, ultimo))


def hacer(s, u):
    a, b = s["a"], s["b"]
    pa, ca = _sin_ceros(u, a)
    pb, cb = _sin_ceros(u, b)
    r = _lo_que_queda(u, pa, pb)
    pequeno = r["valor"]
    ceros = []
    ceros.extend(ca)
    ceros.extend(cb)
    cs = list(ceros)
    cs.extend(u.cifras_de(pequeno))
    v = u.escribir_cifras(cs)
    if u.decir(v) is None:
        raise ValueError("se sale de mi lista")
    # LA VUELTA: quitar los ceros que puse (: 10 cada uno) tiene que dar el producto pequeno
    w, ok = v, True
    for _ in ceros:
        d = u.usar("dividir_por_10_o_100", total=w, divisor=10)
        ok = ok and not d["resultado"].get("resto")
        w = d["valor"]
    ok = ok and w == pequeno
    vuelta = "%d%s = %d" % (v, "".join(" : 10" for _ in ceros), w)
    for f, g in ((pa, pb), (pb, pa)):              # y lo pequeno, si se hizo con la corta: repartiendo entre la cifra
        if len(u.cifras_de(f)) == 1:
            q, resto = _repartir(u, pequeno, f)
            ok = ok and not resto and q == g
            vuelta = "%s; %d : %d = %d" % (vuelta, pequeno, f, q)
            break
    quitados = []
    if ca:
        quitados.append("%d = %d con %s" % (a, pa, "un 0" if len(ca) == 1 else "%d ceros" % len(ca)))
    if cb:
        quitados.append("%d = %d con %s" % (b, pb, "un 0" if len(cb) == 1 else "%d ceros" % len(cb)))
    return {"valor": v, "metodo": "quitar los ceros y ajustar (M.17; NCETM 2.23)",
            "cuenta": "quito los ceros: %s; %d x %d = %d   (%s); vuelvo a poner %s: %d x %d = %d"
                      % ("; ".join(quitados), pa, pb, pequeno, r["resultado"]["metodo"],
                         "el 0" if len(ceros) == 1 else "los %d ceros" % len(ceros), a, b, v),
            "vuelta": "%s ... %s" % (vuelta, "SI" if ok else "NO"),
            "vuelta_ok": ok,
            "vuelta_explicada": "con la operacion contraria: quitando los ceros que puse (: 10) vuelve %d%s"
                                % (pequeno, ", y repartiendo entre la cifra vuelve el otro factor" if ";" in vuelta else "")}
