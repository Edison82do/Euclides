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
    "igualdad": {"elige": "la_mas_rapida",
                 "que_es": "el = : los lados son el mismo numero? (verdadero o falso)"},
    "contar_hasta": {"elige": "la_mas_rapida",
                     "que_es": "cuantos pasos hay de un numero a otro (el hueco, 5.5)"},
}
