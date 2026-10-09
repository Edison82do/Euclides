# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso M.19; NCETM 2.25, 'usar la compensacion para calcular'): REDONDEAR UN FACTOR Y QUITAR
LOS GRUPOS DE MAS.  Si un factor esta justo por debajo de un redondo, se multiplica el redondo (un hecho de la tabla
con ceros: si el factor se hace diez o cien veces mayor, el producto tambien) y se COMPENSA quitando los grupos que
se pusieron de mas:
    399 x 6 = 400 x 6 - 1 x 6 = 2400 - 6 = 2394        (400 grupos de 6 son UNO de mas)
    98 x 37 = 100 x 37 - 2 x 37 = 3700 - 74 = 3626
La trampa: quitar el 1 (2400 - 1) en vez de UN GRUPO (2400 - 6), o sumarlo en vez de quitarlo.
LA VUELTA, con las operaciones contrarias: devolver los grupos quitados vuelve al producto del redondo; ese producto,
sin sus ceros y repartido entre la cifra del redondo, vuelve al otro factor; los grupos repartidos entre cuantos son,
tambien; y si el otro factor es de una cifra, el total repartido entre el (como la corta) vuelve al factor de partida."""

PIEZA = {
    "id": "multiplicar_redondeando_un_factor",
    "nombre": "redondear un factor y quitar los grupos de mas",
    "unidad": "M.19",
    "responde": "multiplicar",
    "rapidez": 6.5,
    "que_hace": "399 x 6 = 400 x 6 - 6: multiplico el redondo y quito los grupos que puse de mas (NCETM 2.25)",
    "condiciones": [
        ("un_factor_esta_justo_debajo_de_un_redondo",
         "ningun factor de mas de doce esta a 1 o 2 por debajo de un redondo (50, 400, 5000...), "
         "o el otro acaba en cero"),
    ],
    "usa": ["buscar_el_redondo_cercano", "multiplicacion_corta", "sumar", "restar", "dividir_por_10_o_100"],
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


def _sin_ceros(u, n):
    cif, ceros = u.cifras_de(n), []
    while len(cif) > 1 and cif[0] == 0:
        cif = cif[1:]
        ceros.append(0)
    return u.escribir_cifras(cif), ceros


def _redondo(u, f):
    """El redondo de una cifra justo por encima de f (lo mismo que mira la condicion), o None."""
    if not u.viene_despues(u.decir(f), "doce"):
        return None
    try:
        r = u.usar("buscar_el_redondo_cercano", n=f, ceros=1)["resultado"]
    except Exception:
        return None
    if not r["sube"] or len(u.cifras_de(_sin_ceros(u, r["valor"])[0])) != 1:
        return None
    return r


def _elegir(u, a, b):
    mejor = None
    for f, g in ((a, b), (b, a)):
        if g in (0, 1) or u.cifras_de(g)[0] == 0:
            continue
        r = _redondo(u, f)
        if r and u.decir(r["pasos"]) == "tres":
            r = None                    # EL COSTO: tres grupos de mas ya no compensan (47 x 6: la corta)
        if r and (mejor is None or u.viene_despues(u.decir(mejor[2]["pasos"]), u.decir(r["pasos"]))):
            mejor = (f, g, r)
    if mejor is None:
        raise ValueError("ningun factor esta justo debajo de un redondo")
    return mejor


def _por_la_cifra(u, g, c):
    """g x c (c de una cifra, la del redondo): el hecho de la tabla si g es de una cifra; si no, la corta."""
    if c == 1:
        return g
    if len(u.cifras_de(g)) == 1:
        h = u.recuerdo("%d x %d" % (c, g)) or u.recuerdo("%d x %d" % (g, c))
        if not h:
            raise ValueError("no se de memoria %d x %d (primero hay que saberse las tablas)" % (c, g))
        return h["valor"]
    return u.usar("multiplicacion_corta", a=g, b=c)["valor"]


def hacer(s, u):
    f, g, r = _elegir(u, s["a"], s["b"])
    R, k = r["valor"], r["pasos"]
    c, ceros = _sin_ceros(u, R)
    pequeno = _por_la_cifra(u, g, c)
    cs = list(ceros)
    cs.extend(u.cifras_de(pequeno))
    RG = u.escribir_cifras(cs)
    if u.decir(RG) is None:
        raise ValueError("%d x %d se sale de mi lista" % (R, g))
    # los grupos de mas: k veces el otro factor (k es 1 o 2), sumando
    grupos, hechas = g, "uno"
    while hechas != u.decir(k):
        grupos = u.usar("sumar", a=grupos, b=g)["valor"]
        hechas = u.siguiente(hechas)
    total = u.usar("restar", a=RG, b=grupos)["valor"]
    # LA VUELTA, con las operaciones contrarias
    ok, vl = True, []
    atras = u.usar("sumar", a=total, b=grupos)["valor"]
    bien = atras == RG
    vl.append("%d + %d = %d ... %s" % (total, grupos, atras, "SI" if bien else "NO"))
    ok = ok and bien
    w = RG
    for _ in ceros:
        d = u.usar("dividir_por_10_o_100", total=w, divisor=10)
        ok = ok and not d["resultado"].get("resto")
        w = d["valor"]
    if c != 1:
        w2, resto = _repartir(u, w, c)
        bien = not resto and w2 == g
        vl.append("%d sin los ceros: %d; %d : %d = %d ... %s" % (RG, w, w, c, w2, "SI" if bien else "NO"))
    else:
        bien = w == g
        vl.append("%d sin los ceros: %d ... %s" % (RG, w, "SI" if bien else "NO"))
    ok = ok and bien
    if k != 1:
        q, resto = _repartir(u, grupos, k)
        bien = not resto and q == g
        vl.append("%d : %d = %d ... %s" % (grupos, k, q, "SI" if bien else "NO"))
        ok = ok and bien
    if len(u.cifras_de(g)) == 1:
        q, resto = _repartir(u, total, g)
        bien = not resto and q == f
        vl.append("%d : %d = %d ... %s" % (total, g, q, "SI" if bien else "NO"))
        ok = ok and bien
    un = "un grupo" if k == 1 else "%d grupos" % k
    return {"valor": total, "metodo": "redondear un factor y compensar (M.19; NCETM 2.25)",
            "cuenta": "%d esta a %d de %d: %d x %d = %d   (%d x %d = %d, con %s); pero son %s de %d de mas: "
                      "%d - %d = %d"
                      % (f, k, R, R, g, RG, c, g, pequeno,
                         "un 0" if len(ceros) == 1 else "%d ceros" % len(ceros), un, g, RG, grupos, total),
            "vuelta": "; ".join(vl), "vuelta_ok": ok,
            "vuelta_explicada": "con las operaciones contrarias: devolviendo %s vuelve %d x %d = %d, y repartiendo "
                                "vuelven los factores" % (un, R, g, RG)}
