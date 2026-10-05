# -*- coding: utf-8 -*-
"""Pieza de PAR O IMPAR (paso N.1): para numeros que pasan de veinte no hace falta emparejar todo.
DIEZ se empareja entero (cinco parejas), asi que cada decena y cada centena se emparejan siempre; lo
unico que puede dejar uno suelto son las UNIDADES.  Se mira la ultima cifra y se emparejan solo esas."""

PIEZA = {
    "id": "par_por_la_ultima_cifra",
    "nombre": "mirar la ultima cifra",
    "unidad": "N.1",
    "responde": "paridad",
    "rapidez": 5,
    "que_hace": "las decenas siempre se emparejan (10 = cinco parejas): solo miro las unidades",
    "condiciones": [
        ("pasa_de_veinte", "no pasa de veinte: se empareja entero (es lo que pide el estandar, 2.OA.C.3)"),
    ],
    "usa": [],
}


def hacer(s, u):
    ud = u.cifras_de(s["n"])[0]
    actual, n = "cero", u.decir(ud)
    valor = "par"
    while actual != n:
        uno = u.siguiente(actual)
        if uno == n:
            valor = "impar"
            break
        actual = u.siguiente(uno)
    return {"valor": valor, "metodo": "la ultima cifra (N.1)",
            "cuenta": "diez se empareja entero (cinco parejas), asi que las decenas y centenas de %d "
                      "nunca dejan a nadie suelto.  Solo miro las unidades: %d -> %s"
                      % (s["n"], ud, "no sobra ninguno" if valor == "par" else "sobra uno"),
            "vuelta": "", "vuelta_ok": True}
