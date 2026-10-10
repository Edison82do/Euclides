# -*- coding: utf-8 -*-
"""Pieza de FRACCION POR FRACCION (paso F.8; NCETM 3.9, punto 1: 'To multiply two fractions, multiply the numerators
and multiply the denominators'; Common Core 5.NF.B.4).
    2/3 x 3/4   ->  arriba por arriba: 2 x 3 = 6;  abajo por abajo: 3 x 4 = 12;  6/12   (luego se simplifica: 1/2)
Es '2/3 DE 3/4': de la tira, 3/4; y de eso, 2/3.  Los trozos se hacen mas pequenos (3 x 4 = 12 trozos en el entero) y
se toman 2 x 3 = 6.
OJO, el error tipico: sumar los de abajo, o multiplicar solo los de arriba (2/3 x 3/4 = 6/3).
LA VUELTA, con la contraria: deshacer cada multiplicacion DIVIDIENDO (6 : 3 = 2 y 12 : 4 = 3: vuelve a 2/3, sin resto);
y el punto 1: si la segunda es menor que un entero, el resultado tiene que ser MAS PEQUENO que la primera (se mira al
mismo de abajo con el mecanismo, viene_despues)."""

PIEZA = {
    "id": "fraccion_por_fraccion_arriba_por_arriba",
    "nombre": "arriba por arriba y abajo por abajo (2/3 x 3/4 = 6/12)",
    "unidad": "F.8",
    "responde": "fraccion_por_fraccion",
    "rapidez": 6,
    "que_hace": "2/3 x 3/4 = (2 x 3)/(3 x 4) = 6/12 (NCETM 3.9, punto 1; 5.NF.B.4)",
    "condiciones": [
        ("son_dos_fracciones", "no son dos fracciones (arriba y abajo enteros, sin ceros)"),
    ],
    "usa": ["multiplicar", "dividir"],
}


def _por(u, a, b):
    v = u.usar("multiplicar", a=a, b=b)["valor"]
    if u.decir(v) is None:
        raise ValueError("%d x %d se pasa de mi lista" % (a, b))
    return v


def _deshacer(u, total, factor, debe):
    """total : factor tiene que dar 'debe', sin resto (la contraria de multiplicar)."""
    r = u.usar("dividir", total=total, divisor=factor)
    return r["valor"] == debe and not r["resultado"].get("resto", 0), r["valor"]


def hacer(s, u):
    (a, b), (c, d) = s["a"], s["b"]
    arriba, abajo = _por(u, a, c), _por(u, b, d)
    pasos = ["arriba por arriba: %d x %d = %d" % (a, c, arriba),
             "abajo por abajo: %d x %d = %d" % (b, d, abajo),
             "%d/%d x %d/%d = %d/%d" % (a, b, c, d, arriba, abajo)]
    # LA VUELTA 1: deshacer cada multiplicacion dividiendo
    ok_a, va = _deshacer(u, arriba, c, a)
    ok_b, vb = _deshacer(u, abajo, d, b)
    ok = ok_a and ok_b
    vuelta = "%d : %d = %d;  %d : %d = %d" % (arriba, c, va, abajo, d, vb)
    explicada = "deshago cada multiplicacion dividiendo: %d : %d = %d y %d : %d = %d, vuelve a %d/%d" \
                % (arriba, c, va, abajo, d, vb, a, b)
    # LA VUELTA 2 (el punto 1): por una fraccion menor que un entero, el resultado es mas pequeno que la primera.
    # Al mismo de abajo (b x d): la primera es (a x d)/(b x d) y el resultado (a x c)/(b x d): basta mirar a x d y a x c.
    if u.viene_despues(u.decir(d), u.decir(c)):
        primera = _por(u, a, d)
        menor = u.viene_despues(u.decir(primera), u.decir(arriba))
        ok = ok and menor
        pasos.append("%d/%d es menos que un entero: el resultado es mas pequeno que %d/%d (%d/%d < %d/%d)"
                     % (c, d, a, b, arriba, abajo, primera, abajo))
        vuelta = "%s;  %d/%d < %d/%d" % (vuelta, arriba, abajo, primera, abajo)
        explicada = "%s; y es mas pequeno que %d/%d, como tiene que ser al multiplicar por menos de un entero (%d/%d " \
                    "< %d/%d)" % (explicada, a, b, arriba, abajo, primera, abajo)
    return {"valor": (arriba, abajo),
            "metodo": "arriba por arriba y abajo por abajo (F.8; NCETM 3.9)",
            "pasos": pasos, "cuenta": "; ".join(pasos),
            "vuelta": "%s ... %s" % (vuelta, "SI" if ok else "NO"), "vuelta_ok": ok,
            "vuelta_explicada": explicada}
