# -*- coding: utf-8 -*-
"""Pieza de DIVIDIR (paso M.12; NCETM 2.18, punto 2): USAR LA EQUIVALENCIA.  'Si el dividendo cambia
multiplicativamente y el divisor cambia DE LA MISMA MANERA, el cociente NO CAMBIA.'
   165 : 5 = 330 : 10 = 33     (doblo los dos: el divisor acaba en 5)
   180 : 20 = 18 : 2 = 9       (quito un cero a los dos: los dos diez veces mas pequenos)
OJO con el resto: el cociente sigue igual, pero el RESTO cambia de tamano (17 : 5 sobran 2; 34 : 10
sobran 4).  Por este camino solo se usan las divisiones JUSTAS; si sobra algo, se usa otro metodo."""

PIEZA = {
    "id": "dividir_escalando",
    "nombre": "cambiar los dos igual (doblar o quitar ceros a los dos)",
    "unidad": "M.12",
    "responde": "dividir",
    "rapidez": 6,
    "que_hace": "doblo los dos si el divisor acaba en 5; quito un cero a los dos si los dos acaban en 0 (NCETM 2.18)",
    "condiciones": [
        ("se_puede_escalar_la_division",
         "el divisor no acaba en 5 y no acaban los dos en cero (o es una division de las tablas)"),
    ],
    "usa": ["sumar", "dividir_por_10_o_100", "dividir_a_la_mitad", "dividir_con_la_tabla",
            "dividir_decenas_justas", "division_corta", "division_larga", "dividir_saltando"],
}

_FINAL = ("dividir_por_10_o_100", "dividir_a_la_mitad", "dividir_con_la_tabla", "dividir_decenas_justas",
          "division_corta", "division_larga", "dividir_saltando")      # M.18: la larga antes que cien saltos


def _sin_ceros(u, n):
    c = u.cifras_de(n)
    while len(c) > 1 and c[0] == 0:
        c = c[1:]
    return c


def _quitar_un_cero(u, n):
    return u.escribir_cifras(u.cifras_de(n)[1:])


def hacer(s, u):
    t, d = s["total"], s["divisor"]
    cadena, pasos = ["%d : %d" % (t, d)], []
    while d not in (10, 100) and not (len(u.cifras_de(d)) == 1 and d != 5):
        if u.cifras_de(t)[0] == 0 and u.cifras_de(d)[0] == 0:
            t, d = _quitar_un_cero(u, t), _quitar_un_cero(u, d)
            pasos.append("quito un cero a los dos")
        elif _sin_ceros(u, d)[0] == 5:
            t2 = u.usar("sumar", a=t, b=t)["valor"]
            d = u.usar("sumar", a=d, b=d)["valor"]
            if u.decir(t2) is None:
                raise ValueError("el doble de %d se sale de mi lista" % t)
            t = t2
            pasos.append("doblo los dos")
        else:
            break
        cadena.append("%d : %d" % (t, d))
    if len(cadena) == 1:
        raise ValueError("no hay nada que cambiar")
    r = None
    for nombre in _FINAL:
        try:
            r = u.usar(nombre, total=t, divisor=d)
        except Exception:
            continue
        break
    if r is None:
        raise ValueError("%d : %d tampoco me sale facil" % (t, d))
    v, resto = r["valor"], r["resultado"].get("resto", 0)
    if resto:
        raise ValueError("%d : %d no es justa: el cociente es el mismo, pero el RESTO cambia de tamano "
                         "(no lo uso)" % (s["total"], s["divisor"]))
    return {"valor": v, "resto": 0, "metodo": "cambiar los dos igual (M.12)",
            "cuenta": "%s = %d  (%s: los dos cambian igual y el cociente no cambia, NCETM 2.18; %d : %d con %s)"
                      % (" = ".join(cadena), v, ", ".join(pasos), t, d, r["resultado"]["metodo"]),
            "cadena": cadena,
            "vuelta": "", "vuelta_ok": True}
