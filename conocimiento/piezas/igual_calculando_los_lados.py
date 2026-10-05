# -*- coding: utf-8 -*-
"""Pieza de la IGUALDAD (paso E.0; Common Core 1.OA.D.7): calcular lo que vale CADA lado (con los
metodos que ya tengo) y mirar si es el MISMO numero.  El = no dice 'da': dice 'es el mismo numero
que' (Progression de Common Core).  Por eso 10 = 8 + 2 es verdad, y 4 + 1 = 5 + 2 es FALSO aunque
4 + 1 de 5 (a la derecha no hay un 5: hay 5 + 2, que es 7)."""

PIEZA = {
    "id": "igual_calculando_los_lados",
    "nombre": "calcular cada lado y comparar",
    "unidad": "E.0",
    "responde": "igualdad",
    "rapidez": 20,
    "que_hace": "calcula lo que vale cada lado y mira si todos son el mismo numero",
    "condiciones": [
        ("hay_dos_lados_o_mas", "no hay dos lados que comparar"),
    ],
    "usa": ["sumar", "restar"],
}


def _vale(lado, u):
    if "n" in lado:
        return lado["n"], "es un numero"
    r = u.usar("sumar" if lado["op"] == "+" else "restar", a=lado["a"], b=lado["b"])
    return r["valor"], r["resultado"]["metodo"]


def hacer(s, u):
    valores, lineas = [], []
    for lado in s["lados"]:
        try:
            v, como = _vale(lado, u)
        except Exception as e:            # una resta imposible: ese lado no vale ningun numero
            if isinstance(e, RuntimeError):
                raise
            raise ValueError("%s no se puede hacer (%s): ese lado no es ningun numero" % (lado["texto"], e))
        valores.append(v)
        lineas.append("%s vale %d (%s)" % (lado["texto"], v, como))
    primero = valores[0]
    distintos = [k for k, v in enumerate(valores) if v != primero]
    verdad = not distintos
    nota = ""
    i = s["lados"][0]
    if not verdad and len(s["lados"]) == 2 and "op" in i and s["lados"][1].get("a") == primero:
        nota = ("\nOJO: %s da %d, y a la derecha se ve un %d; pero el = no dice 'da': a la derecha "
                "esta %s entero, que vale %d" % (i["texto"], primero, primero, s["lados"][1]["texto"], valores[1]))
    if not verdad and len(s["lados"]) > 2:
        nota = "\nOJO: en una cadena TODOS los lados tienen que valer lo mismo"
    if verdad:
        cierre = "todos los lados son el mismo numero, %d" % primero
    else:
        k = distintos[0]
        cierre = "%d no es el mismo numero que %d" % (primero, valores[k])
    return {"valor": "verdadero" if verdad else "falso", "metodo": "calcular cada lado (E.0)",
            "cuenta": "%s\n-> %s%s" % ("\n".join(lineas), cierre, nota),
            "vuelta": "", "vuelta_ok": True}
