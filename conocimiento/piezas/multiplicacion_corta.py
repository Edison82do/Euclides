# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso M.10; NCETM 2.14, puntos 2 y 4): LA MULTIPLICACION CORTA.  Columna a columna
desde la DERECHA; en cada columna un hecho de la tabla (de memoria) MAS lo que se lleva; si da diez o mas,
se escribe la cifra de las unidades y se REAGRUPA (se lleva) el resto a la columna de al lado.
      347
    x   6
    -----
     2082     (7 x 6 = 42: escribo 2, llevo 4;  4 x 6 = 24, + 4 = 28: escribo 8, llevo 2;  3 x 6 = 18, + 2 = 20)"""

PIEZA = {
    "id": "multiplicacion_corta",
    "nombre": "la multiplicacion corta (en columnas)",
    "unidad": "M.10",
    "responde": "multiplicar",
    "rapidez": 7,
    "que_hace": "columna a columna desde la derecha: el hecho de la tabla mas lo que se lleva",
    "condiciones": [
        ("un_factor_de_una_cifra_y_otro_de_varias", "no es un numero de varias cifras por uno de una cifra"),
    ],
    "usa": [],
}


def _hecho(u, x, k):
    if x == 0:
        return 0
    if x == 1:
        return k
    h = u.recuerdo("%d x %d" % (x, k)) or u.recuerdo("%d x %d" % (k, x))
    if not h:
        raise ValueError("no se de memoria %d x %d (primero hay que saberse las tablas)" % (x, k))
    return h["valor"]


def hacer(s, u):
    a, b = s["a"], s["b"]
    k, n = (a, b) if len(u.cifras_de(a)) == 1 else (b, a)
    escritas, llevo, pasos = [], 0, []
    for c in u.cifras_de(n):                                 # desde la DERECHA (las unidades primero)
        p = _hecho(u, c, k)
        con = u.sumar_por_columnas(p, llevo) if llevo else p
        cif = u.cifras_de(con)
        escribo = cif[0]
        nuevo_llevo = u.escribir_cifras(cif[1:])
        pasos.append("%d x %d = %d%s: escribo %d%s" % (
            c, k, p, ", + %d que llevaba = %d" % (llevo, con) if llevo else "", escribo,
            ", llevo %d" % nuevo_llevo if nuevo_llevo else ""))
        escritas.append(escribo)
        llevo = nuevo_llevo
    if llevo:
        escritas.extend(u.cifras_de(llevo))
        pasos.append("lo que llevo (%d) se escribe delante" % llevo)
    total = u.escribir_cifras(escritas)
    if u.decir(total) is None:
        raise ValueError("se sale de mi lista")
    ancho = len(str(total))                                   # el ancho de lo escrito (se mira, no se calcula)
    dibujo = ["    %s" % str(n).rjust(ancho), "x   %s" % str(k).rjust(ancho),
              "  --%s" % "".join("-" for _ in range(ancho)), "    %s" % str(total).rjust(ancho)]
    return {"valor": total, "metodo": "la multiplicacion corta (M.10)",
            "cuenta": "%s; %s" % ("; ".join(dibujo), "; ".join(pasos)),
            "vuelta": "", "vuelta_ok": True}
