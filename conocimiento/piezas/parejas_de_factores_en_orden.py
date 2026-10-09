# -*- coding: utf-8 -*-
"""Pieza de LAS PAREJAS DE FACTORES (paso M.15; NCETM 2.21, puntos 1 y 2; 4.OA.B.4).  'Se pueden usar
metodos SISTEMATICOS para encontrar todos los factores; los factores van POR PAREJAS.'  Para 36: se
prueba 1, 2, 3 ... DIVIDIENDO (con resto, M.8): 36 : 1 = 36, 36 : 2 = 18, 36 : 3 = 12, 36 : 4 = 9,
36 : 5 = 7 y sobra 1 (no), 36 : 6 = 6 (el mismo consigo mismo: un CUADRADO) ... y se PARA cuando el
companero se hace mas pequeno que el que pruebo (ya me los encontraria al reves).
Respetar el ano: se divide con las tablas, hasta el 12.  Si para llegar al medio hubiera que dividir entre
13 o mas, se mira antes si ese numero por si mismo ya se pasa (13 x 13 = 169: la multiplicacion de dos
cifras por dos cifras SI es de 4.o/5.o); si no se pasa, haria falta la division larga (6.o): todavia no.
PASO M.18 (NCETM 2.24): con la division larga se divide entre DOS cifras: se sigue probando hasta el 99.  Solo si
el medio pide dividir entre TRES cifras (100 x 100 = 10000 no se pasa del numero), todavia no.
Se COMPRUEBA cada division con la contraria: el cociente por el divisor, mas lo que sobro, da el numero."""

PIEZA = {
    "id": "parejas_de_factores_en_orden",
    "nombre": "probar 1, 2, 3 ... dividiendo, hasta cruzarse",
    "unidad": "M.15",
    "responde": "parejas_de_factores",
    "rapidez": 10,
    "que_hace": "36: 1 x 36, 2 x 18, 3 x 12, 4 x 9, 6 x 6 (pruebo en orden y paro al cruzarme)",
    "condiciones": [
        ("es_un_entero_positivo", "no es un entero positivo (los factores son de 1 en adelante)"),
    ],
    "usa": ["dividir", "multiplicar", "sumar"],
}


def hacer(s, u):
    n = s["n"]
    d, parejas, probados, por_si_mismo, cruce = 1, [], [], None, None
    while True:
        if u.viene_despues(u.decir(d), "doce"):          # ya no es de las tablas
            dd = u.usar("multiplicar", a=d, b=d)["valor"]
            if u.viene_despues(u.decir(dd), u.decir(n)):      # se pasa (mirado con el mecanismo)
                por_si_mismo = "%d x %d = %d ya se pasa de %d: no hace falta seguir" % (d, d, dd, n)
                break
            if d == 13:                    # M.18: la division larga es entre DOS cifras; se mira antes de empezar
                cc = u.usar("multiplicar", a=100, b=100)["valor"]
                if not u.viene_despues(u.decir(cc), u.decir(n)):
                    raise ValueError("para llegar al medio de %d habria que dividir entre numeros de tres cifras "
                                     "(100 x 100 = %d no se pasa de %d): eso todavia no (la division larga de 6.o es "
                                     "entre dos cifras; llego hasta el 99)" % (n, cc, n))
        r = u.usar("dividir", total=n, divisor=d)
        q, resto = r["valor"], r["resultado"].get("resto", 0)
        if u.viene_despues(u.decir(d), u.decir(q)):       # el companero ya es mas pequeno: me cruzo
            cruce = (d, q, resto)
            break
        probados.append((d, q, resto))
        if not resto:
            parejas.append((d, q))
        if q == d:
            break
        d = u.leer(u.siguiente(u.decir(d)))
    vuelta, ok = _vuelta(u, n, probados)
    pequenos = [p for p, _ in parejas]
    grandes = [q for p, q in reversed(parejas) if q != p]
    pequenos.extend(grandes)
    return {"valor": ", ".join("%d x %d" % p for p in parejas), "parejas": parejas, "factores": pequenos,
            "probados": probados, "cuadrado": bool(parejas) and parejas[-1][0] == parejas[-1][1],
            "por_si_mismo": por_si_mismo, "cruce": cruce,
            "metodo": "probar en orden dividiendo, hasta cruzarse (M.15; NCETM 2.21)",
            "cuenta": "%d = %s" % (n, " = ".join("%d x %d" % p for p in parejas)),
            "vuelta": vuelta, "vuelta_ok": ok}


def _vuelta(u, n, probados):
    """LA OPERACION CONTRARIA: cada division que se probo, multiplicando de vuelta (y sumando lo que sobro)."""
    textos, ok = [], True
    for d, q, resto in probados:
        m = u.usar("multiplicar", a=d, b=q)["valor"]
        if resto:
            m = u.usar("sumar", a=m, b=resto)["valor"]
            textos.append("%d x %d + %d = %d" % (d, q, resto, m))
        else:
            textos.append("%d x %d = %d" % (d, q, m))
        if m != n:
            ok = False
    return ", ".join(textos), ok
