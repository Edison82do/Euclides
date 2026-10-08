# -*- coding: utf-8 -*-
"""
LAS PREGUNTAS a las que responden las piezas, y COMO se elige entre las que encajan.

  todas_iguales  -> se hacen TODAS las que encajan y tienen que dar lo mismo (si no, AMBIGUO).
                    Es lo que se pide a un paso de un problema: no se elige a dedo.
  la_mas_rapida  -> se hace la que encaje y sea mas rapida ("rapidez" mas baja); las demas que
                    tambien servian se dicen.  Es lo que se pide a un METODO de calculo: un nino
                    que sabe hacer diez no cuenta con los dedos 8 + 5.
"""
OBJETIVOS = {
    "paso": {"elige": "todas_iguales",
             "que_es": "un paso de un problema: que conocimiento encaja en la situacion"},
    "sumar": {"elige": "la_mas_rapida", "que_es": "hacer una suma, sin calculadora"},
    "restar": {"elige": "la_mas_rapida", "que_es": "hacer una resta, sin calculadora"},
    "paso_por": {"elige": "todas_iguales",
                 "que_es": "un problema de grupos iguales: que casilla del esquema falta (R.2)"},
    "dividir": {"elige": "la_mas_rapida",
                "que_es": "repartir o agrupar: cuantos para cada uno / cuantos grupos (NCETM 2.6)"},
    "multiplicar": {"elige": "la_mas_rapida",
                    "que_es": "a x b: a grupos iguales de b (3.OA.A.1, NCETM 2.2)"},
    "suma_de_iguales": {"elige": "la_mas_rapida",
                        "que_es": "juntar varios grupos IGUALES (filas y columnas, 2.OA.C.4)"},
    "paridad": {"elige": "la_mas_rapida",
                "que_es": "par o impar? (se emparejan de dos en dos y no sobra ninguno?)"},
    "balanza": {"elige": "la_mas_rapida",
                "que_es": "el = como balanza: que va en el hueco si hay cuentas a los dos lados?"},
    "balanza_por": {"elige": "la_mas_rapida",
                    "que_es": "la balanza con x o : (NCETM 2.18): que va en el hueco sin calcular los lados?"},
    "igualdad": {"elige": "la_mas_rapida",
                 "que_es": "el = : los lados son el mismo numero? (verdadero o falso)"},
    "comparar_fracciones": {"elige": "todas_iguales",
                            "que_es": "cual de dos fracciones es mayor (NCETM 3.2, 3.3): la regla y la tira, de acuerdo"},
    "redondear": {"elige": "todas_iguales",
                  "que_es": "a que decena o centena esta mas cerca (3.NBT.A.1): la recta y el atajo, de acuerdo"},
    "multiplicar_decimal": {"elige": "la_mas_rapida",
                            "que_es": "un decimal por un entero (NCETM 2.19; 5.NBT.B.7): 0.3 x 4"},
    "dividir_decimal": {"elige": "la_mas_rapida",
                        "que_es": "un decimal entre un entero (NCETM 2.19; 5.NBT.B.7): 7.2 : 3"},
    "multiplicar_tres": {"elige": "la_mas_rapida",
                         "que_es": "tres factores o mas (NCETM 2.20): en el orden que sea mas facil, 25 x 7 x 4"},
    "parejas_de_factores": {"elige": "la_mas_rapida",
                            "que_es": "todas las parejas de factores de un numero (NCETM 2.21; 4.OA.B.4): 36 = 4 x 9 ..."},
    "primo": {"elige": "la_mas_rapida",
              "que_es": "primo (exactamente dos factores) o compuesto (mas de dos)? (NCETM 2.21)"},
    "combinar": {"elige": "la_mas_rapida",
                 "que_es": "una cuenta con x, + y - (NCETM 2.22; 5.OA.A.1): primero el parentesis, luego las x"},
    "todo_de_las_partes": {"elige": "la_mas_rapida",
                           "que_es": "parte-parte-todo (NCETM 1.28): falta el TODO; se juntan las partes (tres o mas)"},
    "parte_del_todo": {"elige": "la_mas_rapida",
                       "que_es": "parte-parte-todo (NCETM 1.28): se sabe el todo y falta UNA parte (o son iguales)"},
    "redondo_cercano": {"elige": "la_mas_rapida",
                        "que_es": "esta cerca de un redondo (100, 1000...)? cuanto le falta o le sobra (NCETM 1.29)"},
    "derivar": {"elige": "la_mas_rapida",
                "que_es": "sacar una suma o resta nueva de una que ya se sabe (NCETM 1.29, puntos 2, 4 y 5)"},
    "simplificar_fraccion": {"elige": "la_mas_rapida",
                             "que_es": "la forma mas simple de una fraccion (NCETM 3.7, punto 3): 12/18 = 2/3"},
    "hueco_equivalente": {"elige": "la_mas_rapida",
                          "que_es": "el numero que falta en dos fracciones equivalentes (NCETM 3.7, punto 2): 2/3 = ?/12"},
    "mismo_de_abajo": {"elige": "la_mas_rapida",
                       "que_es": "pasar dos fracciones al mismo de abajo (NCETM 3.8): 1/2 y 1/4 -> 2/4 y 1/4"},
    "contar_hasta": {"elige": "la_mas_rapida",
                     "que_es": "cuantos pasos hay de un numero a otro (el hueco, 5.5)"},
}
