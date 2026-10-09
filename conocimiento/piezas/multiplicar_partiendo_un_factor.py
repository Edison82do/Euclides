# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso M.17; NCETM 2.23, punto 3): PARTIR UNO DE LOS FACTORES.  Dos numeros de dos cifras
(o tres por dos): se parte el de dos cifras en decenas y unidades, se hallan los dos productos parciales y se suman.
    24 x 15 = 24 x 10 + 24 x 5 = 240 + 120 = 360
    326 x 47 = 326 x 40 + 326 x 7 = 13040 + 2282 = 15322
(La rejilla de N.4 parte LOS DOS; aqui solo uno: dos productos parciales en vez de cuatro o seis casillas.)
LA VUELTA: el total quitando un producto parcial da el otro (restar); y cada parcial, quitando su 0 (: 10) y
repartiendolo entre su cifra (la division corta), vuelve a dar el otro factor."""

PIEZA = {
    "id": "multiplicar_partiendo_un_factor",
    "nombre": "partir uno de los factores (24 x 10 + 24 x 5)",
    "unidad": "M.17",
    "responde": "multiplicar",
    "rapidez": 9.1,
    "que_hace": "parte el factor de dos cifras en decenas y unidades, multiplica el otro por cada trozo y suma",
    "condiciones": [
        ("los_dos_factores_de_varias_cifras", "no son dos numeros de varias cifras"),
        ("dos_cifras_por_dos_o_tres_por_dos", "no es de dos cifras por dos (o tres por dos)"),
    ],
    "usa": ["multiplicacion_corta", "sumar", "restar", "dividir_por_10_o_100"],
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


def _por_una_cifra(u, n, d):
    if d == 0:
        return 0
    if d == 1:
        return n
    return u.usar("multiplicacion_corta", a=n, b=d)["valor"]


def hacer(s, u):
    a, b = s["a"], s["b"]
    # se parte el de DOS cifras (si los dos lo son, el segundo: 24 x 15 -> 15 = 10 + 5)
    f, n = (b, a) if len(u.cifras_de(b)) == 2 else (a, b)
    unidades, decenas = u.cifras_de(f)
    trozo_d = u.escribir_cifras([0, decenas])
    pd = _por_una_cifra(u, n, decenas)
    cs = [0]
    cs.extend(u.cifras_de(pd))
    parcial_d = u.escribir_cifras(cs)
    parcial_u = _por_una_cifra(u, n, unidades)
    if unidades:
        total = u.usar("sumar", a=parcial_d, b=parcial_u)["valor"]
    else:
        total = parcial_d
    if u.decir(total) is None:
        raise ValueError("se sale de mi lista")
    lineas = ["%d = %d + %d" % (f, trozo_d, unidades),
              "%d x %d = %d   (%d x %d = %d, y un 0: son decenas)" % (n, trozo_d, parcial_d, n, decenas, pd)]
    if unidades:
        lineas.append("%d x %d = %d" % (n, unidades, parcial_u))
    lineas.append("los productos parciales se suman: %d + %d = %d" % (parcial_d, parcial_u, total))
    # LA VUELTA, con las operaciones contrarias
    ok, vl = True, []
    queda = u.usar("restar", a=total, b=parcial_d)["valor"] if unidades else 0
    ok = ok and queda == parcial_u
    vl.append("%d - %d = %d, el otro parcial ... %s" % (total, parcial_d, queda, "SI" if queda == parcial_u else "NO"))
    d10 = u.usar("dividir_por_10_o_100", total=parcial_d, divisor=10)
    w = d10["valor"]
    bien = not d10["resultado"].get("resto")
    if decenas != 1:
        w, resto = _repartir(u, w, decenas)
        bien = bien and not resto
    bien = bien and w == n
    vl.append("%d : 10%s = %d ... %s" % (parcial_d, " : %d" % decenas if decenas != 1 else "", w, "SI" if bien else "NO"))
    ok = ok and bien
    if unidades not in (0, 1):
        q, resto = _repartir(u, parcial_u, unidades)
        bien = not resto and q == n
        vl.append("%d : %d = %d ... %s" % (parcial_u, unidades, q, "SI" if bien else "NO"))
        ok = ok and bien
    return {"valor": total, "metodo": "partir uno de los factores (M.17; NCETM 2.23)",
            "cuenta": "; ".join(lineas), "vuelta": "; ".join(vl), "vuelta_ok": ok,
            "vuelta_explicada": "con las operaciones contrarias: restando un parcial queda el otro, y cada parcial "
                                "entre su trozo vuelve a dar %d" % n}
