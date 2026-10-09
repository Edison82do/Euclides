# -*- coding: utf-8 -*-
"""Pieza de LA MEDIA NIVELANDO (paso M.20; NCETM 2.26, punto 1): 'la media es lo que tendria cada uno si se
repartiera por igual': las torres se NIVELAN.  El mas bajo es la base; lo que los demas tienen por encima de el se
junta y se reparte entre TODOS; cada uno tiene la base y su trozo:
    98, 102, 100, 104  ->  por encima del 98: 4, 2, 6 = 12;  12 : 4 = 3;  98 + 3 = 101   (sin sumar 404)
Solo encaja cuando CONVIENE (el costo): valores de dos cifras o mas y cerca unos de otros (ninguno a mas de 20 del
mas bajo).  Lejos o pequenos, juntar y repartir es igual de corto.
LA VUELTA, por el EQUILIBRIO (la media es el punto de equilibrio): lo que sobra por encima de la media tiene que ser
lo que falta por debajo, mas lo que sobro al repartir.  No necesita el total, asi que vale cerca del techo.
La trampa: repartir lo de encima solo entre los de arriba, u olvidar poner la base (la vuelta las caza)."""

PIEZA = {
    "id": "media_nivelando",
    "nombre": "nivelar: lo que sobra por encima del mas bajo se reparte entre todos",
    "unidad": "M.20",
    "responde": "media",
    "rapidez": 5,
    "que_hace": "98, 102, 100, 104 -> encima del 98: 4 + 2 + 6 = 12;  12 : 4 = 3;  98 + 3 = 101 (NCETM 2.26)",
    "condiciones": [
        ("son_valores_enteros_y_tantas_partes_como_valores",
         "no son dos valores enteros o mas repartidos entre CUANTOS son: no es una media"),
        ("los_valores_estan_cerca_unos_de_otros",
         "los valores no estan cerca (o son pequenos): nivelar no ahorra nada, mejor juntar y repartir"),
    ],
    "usa": ["restar", "sumar", "dividir"],
}


def hacer(s, u):
    vs, k = list(s["valores"]), s["partes"]
    bajo = vs[0]
    for v in vs[1:]:                                   # el mas bajo, comparando con el mecanismo
        if u.viene_despues(u.decir(bajo), u.decir(v)):
            bajo = v
    encima, trozos = 0, []
    for v in vs:
        if v == bajo:
            continue
        d = u.usar("restar", a=v, b=bajo)["valor"]
        trozos.append("%d - %d = %d" % (v, bajo, d))
        encima = d if encima == 0 else u.usar("sumar", a=encima, b=d)["valor"]
    if encima == 0:
        q, resto = 0, 0
    else:
        r = u.usar("dividir", total=encima, divisor=k)
        q, resto = r["valor"], r["resultado"].get("resto", 0)
    media = bajo if q == 0 else u.usar("sumar", a=bajo, b=q)["valor"]
    pasos = ["el mas bajo es %d: es la base" % bajo]
    if trozos:
        pasos.append("lo que tienen por encima: %s;  junto: %d" % (", ".join(trozos), encima))
        pasos.append("lo reparto entre los %d: %d : %d = %d%s" % (k, encima, k, q, (", y sobra %d (%d/%d para cada uno)"
                                                                               % (resto, resto, k)) if resto else ""))
        if q:
            pasos.append("cada uno: la base y su trozo: %d + %d = %d" % (bajo, q, media))
        else:
            pasos.append("no llega a uno entero para cada uno: cada uno, la base (%d) y lo que sobro repartido" % bajo)
    else:
        pasos.append("todos son iguales: ya estan nivelados")
    # LA VUELTA, por el equilibrio: lo que sobra por encima de la media = lo que falta por debajo + lo que sobro
    sobra, falta = 0, 0
    for v in vs:
        if v == media:
            continue
        if u.viene_despues(u.decir(v), u.decir(media)):
            d = u.usar("restar", a=v, b=media)["valor"]
            sobra = d if sobra == 0 else u.usar("sumar", a=sobra, b=d)["valor"]
        else:
            d = u.usar("restar", a=media, b=v)["valor"]
            falta = d if falta == 0 else u.usar("sumar", a=falta, b=d)["valor"]
    debe = falta if not resto else (resto if falta == 0 else u.usar("sumar", a=falta, b=resto)["valor"])
    ok = sobra == debe
    vl = "por encima de %d sobra %d; por debajo falta %d%s" % (media, sobra, falta,
                                                              (" (y sobraron %d al repartir: %d)" % (resto, debe))
                                                              if resto else "")
    return {"valor": media, "resto": resto, "partes": k,
            "metodo": "nivelar sobre el mas bajo (M.20; NCETM 2.26)",
            "pasos": pasos, "cuenta": "; ".join(pasos),
            "vuelta": "%s ... %s" % (vl, "SI" if ok else "NO"), "vuelta_ok": ok,
            "vuelta_explicada": "por el EQUILIBRIO: lo que sobra por encima de %d (%d) es lo que falta por debajo (%d)%s"
                                % (media, sobra, falta, (" mas lo que sobro al repartir (%d)" % resto) if resto else "")}
