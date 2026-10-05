# -*- coding: utf-8 -*-
"""Pieza de PAR O IMPAR (paso N.1; Common Core 2.OA.C.3): hasta 20, se hacen PAREJAS contando de dos
en dos.  Si al final sobra uno, es impar.  Si no sobra ninguno, es par, y entonces es la suma de dos
numeros iguales (14 = 7 + 7: un doble), que es lo que pide escribir el estandar."""

PIEZA = {
    "id": "par_emparejando",
    "nombre": "hacer parejas (de dos en dos)",
    "unidad": "N.1",
    "responde": "paridad",
    "rapidez": 10,
    "que_hace": "hace parejas contando de dos en dos; si sobra uno es impar",
    "condiciones": [
        ("es_de_veinte_o_menos", "pasa de veinte (el estandar empareja hasta 20; para mas, se mira la ultima cifra)"),
    ],
    "usa": [],
}


def hacer(s, u):
    n = u.decir(s["n"])
    actual, parejas, dichos = "cero", "cero", []
    while actual != n:
        uno = u.siguiente(actual)
        if uno == n:                                  # sobra uno: no tiene pareja
            return {"valor": "impar", "metodo": "hacer parejas (N.1)",
                    "cuenta": "de dos en dos: %s ... y SOBRA UNO: %s parejas y uno suelto"
                              % (", ".join(dichos) or "(ninguna pareja)", parejas),
                    "vuelta": "", "vuelta_ok": True}
        actual = u.siguiente(uno)
        parejas = u.siguiente(parejas)
        dichos.append(str(u.leer(actual)))
    m = u.leer(parejas)
    return {"valor": "par", "metodo": "hacer parejas (N.1)",
            "cuenta": "de dos en dos: %s ... y NO SOBRA NINGUNO: %s parejas.  %d = %d + %d (un doble)"
                      % (", ".join(dichos) or "(no hay nada que emparejar)", parejas, s["n"], m, m),
            "vuelta": "", "vuelta_ok": True}
