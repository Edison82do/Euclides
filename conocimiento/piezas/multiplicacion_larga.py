# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso M.17; NCETM 2.23, punto 4; Common Core 5.NBT.B.5): LA MULTIPLICACION LARGA.
Multiplicar y luego SUMAR LOS PRODUCTOS PARCIALES.  El mas largo arriba; una FILA por cada cifra del de abajo,
desde las unidades; cada fila es una multiplicacion corta (M.10); en la fila de las decenas se pone primero un 0 que
GUARDA EL SITIO (es "por 40", no "por 4"), en la de las centenas dos; y las filas se suman por columnas.
        3456
      x  247
      ------
       24192     3456 x 7
      138240     3456 x 40   (un 0, y 3456 x 4)
      691200     3456 x 200  (dos 0, y 3456 x 2)
      ------
      853632
LA VUELTA (con la operacion contraria): cada fila, quitandole los ceros que puse (: 10) y repartiendola entre su
cifra (la division corta), vuelve a dar el de arriba; y el total, quitandole las filas, deja la ultima.  Asi se caza
el 0 olvidado y lo que se lleva olvidado (los errores tipicos)."""

PIEZA = {
    "id": "multiplicacion_larga",
    "nombre": "la multiplicacion larga (filas y sumarlas)",
    "unidad": "M.17",
    "responde": "multiplicar",
    "rapidez": 9.5,
    "que_hace": "una fila (multiplicacion corta) por cada cifra del de abajo, con los ceros que guardan el sitio, y se suman las filas",
    "condiciones": [
        ("los_dos_factores_de_varias_cifras", "no son dos numeros de varias cifras"),
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

_SITIO = ("unidades", "decenas", "centenas", "millares", "decenas de millar", "centenas de millar", "millones")
_CEROS = ("", "un 0", "dos 0", "tres 0", "cuatro 0", "cinco 0", "seis 0")


def _por_una_cifra(u, arriba, d):
    """arriba x d con d de una cifra: la corta (por su nombre); x 1 es el mismo; x 0 no da fila."""
    if d == 0:
        return 0
    if d == 1:
        return arriba
    return u.usar("multiplicacion_corta", a=arriba, b=d)["valor"]


def _deshacer_fila(u, fila, veces, d, arriba):
    """La operacion contraria de una fila: : 10 tantas veces como ceros puse, y : d (la division corta)."""
    v = fila
    for _ in range(veces):
        r = u.usar("dividir_por_10_o_100", total=v, divisor=10)
        if r["resultado"].get("resto"):
            return False, "%d no se deja dividir entre 10: falta el 0 que guarda el sitio" % v
        v = r["valor"]
    if d != 1:
        q, resto = _repartir(u, v, d)
        if resto:
            return False, "%d : %d no es justo" % (v, d)
        v = q
    return v == arriba, "%d%s%s = %d" % (fila, "".join(" : 10" for _ in range(veces)),
                                         " : %d" % d if d != 1 else "", v)


def hacer(s, u):
    a, b = s["a"], s["b"]
    arriba, abajo = (b, a) if len(u.cifras_de(b)) > len(u.cifras_de(a)) else (a, b)
    filas, notas = [], []                       # filas: (fila, ceros, cifra)
    for i, d in enumerate(u.cifras_de(abajo)):  # desde las UNIDADES
        if d == 0:
            notas.append("la cifra de las %s es 0: %d x 0 = 0, no hay fila" % (_SITIO[i], arriba))
            continue
        p = _por_una_cifra(u, arriba, d)
        cs = [0 for _ in range(i)]
        cs.extend(u.cifras_de(p))
        fila = u.escribir_cifras(cs)
        ct = [0 for _ in range(i)]
        ct.append(d)
        trozo = u.escribir_cifras(ct)
        if i:
            notas.append("%d x %d = %d   (las %s: %s que guarda%s el sitio, y %d x %d = %d)"
                         % (arriba, trozo, fila, _SITIO[i], _CEROS[i], "n" if i != 1 else "", arriba, d, p))
        else:
            notas.append("%d x %d = %d   (las unidades%s)" % (arriba, d, fila,
                                                             ": la multiplicacion corta" if d != 1 else ""))
        filas.append((fila, i, d))
    total = 0
    for f, _, _ in filas:
        try:
            total = u.usar("sumar", a=total, b=f)["valor"] if total else f
        except KeyError:
            raise ValueError("la suma de las filas se sale de mi lista")
    if u.decir(total) is None:
        raise ValueError("se sale de mi lista")
    # el dibujo, en columnas (se mira lo escrito, no se calcula)
    ancho = max(len(str(total)), len(str(arriba)), len(str(abajo)) + 2)
    raya = "".join("-" for _ in range(ancho))
    dibujo = ["  %s" % str(arriba).rjust(ancho), "x %s" % str(abajo).rjust(ancho), "  %s" % raya]
    dibujo.extend("  %s" % str(f).rjust(ancho) for f, _, _ in filas)
    dibujo.extend(["  %s" % raya, "  %s" % str(total).rjust(ancho)])
    # LA VUELTA: cada fila con la operacion contraria; y el total quitando las filas
    ok, vlineas = True, []
    for f, veces, d in filas:
        bien, linea = _deshacer_fila(u, f, veces, d, arriba)
        vlineas.append("%s %s" % (linea, "SI" if bien else "NO"))
        ok = ok and bien
    resto = total
    for f, _, _ in filas[:-1]:
        resto = u.usar("restar", a=resto, b=f)["valor"]
    queda_bien = bool(filas) and resto == filas[-1][0]
    vlineas.append("%d quitando las filas %s deja %d, la ultima fila ... %s"
                   % (total, " y ".join(str(f) for f, _, _ in filas[:-1]) or "(no hay mas)", resto,
                      "SI" if queda_bien else "NO"))
    ok = ok and queda_bien
    return {"valor": total, "metodo": "la multiplicacion larga (M.17; NCETM 2.23)",
            "cuenta": "%s; %s; sumo las filas por columnas: %s = %d"
                      % ("; ".join(dibujo), "; ".join(notas), " + ".join(str(f) for f, _, _ in filas), total),
            "vuelta": "; ".join(vlineas), "vuelta_ok": ok,
            "vuelta_explicada": "con la operacion contraria: cada fila quitando sus ceros (: 10) y entre su cifra "
                                "(la division corta) vuelve a dar %d; y la suma, restando" % arriba}
