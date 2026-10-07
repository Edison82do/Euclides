# -*- coding: utf-8 -*-
"""Pieza de la BALANZA CON x Y : (paso M.12; NCETM 2.18): el hueco SIN CALCULAR LOS LADOS.
   24 x 5 = 12 x ?   -> 12 es 24 a la mitad, asi que el hueco es 5 al doble: 10   (punto 1)
   180 : 20 = 18 : ? -> 18 es 180 diez veces mas pequeno; el divisor tambien: 20 : 10 = 2   (punto 2)
En x, lo que sube un factor lo baja el otro; en :, el dividendo y el divisor cambian IGUAL."""

PIEZA = {
    "id": "balanza_escalando",
    "nombre": "lo que sube un factor, lo baja el otro (en : los dos igual)",
    "unidad": "M.12",
    "responde": "balanza_por",
    "rapidez": 3,
    "que_hace": "compara el numero conocido con su pareja y cambia el otro las mismas veces (NCETM 2.18)",
    "condiciones": [
        ("la_balanza_es_de_por_o_entre", "no son dos multiplicaciones ni dos divisiones"),
    ],
    "usa": ["dividir", "multiplicar"],
}


def _veces(u, grande, pequeno):
    if pequeno in (0, grande) or not u.viene_despues(u.decir(grande), u.decir(pequeno)):
        return None
    r = u.usar("dividir", total=grande, divisor=pequeno)
    return None if r["resultado"].get("resto") else r["valor"]


def _cambiar(u, n, direccion, k):
    """n, k veces mas grande ('sube') o k veces mas pequeno ('baja'; tiene que ser justo)."""
    if direccion == "sube":
        return u.usar("multiplicar", a=n, b=k)["valor"]
    r = u.usar("dividir", total=n, divisor=k)
    if r["resultado"].get("resto"):
        raise ValueError("%d no se puede hacer %d veces mas pequeno justo" % (n, k))
    return r["valor"]


def hacer(s, u):
    c, h = s["completo"], s["con_hueco"]
    hueco_en_b = h["b"] == "?"
    n = h["a"] if hueco_en_b else h["b"]
    if c["op"] == "x":
        parejas = ((c["a"], c["b"]), (c["b"], c["a"]))
    else:   # en la division el dividendo va con el dividendo y el divisor con el divisor
        parejas = ((c["a"], c["b"]),) if hueco_en_b else ((c["b"], c["a"]),)
    for p, otro in parejas:
        if n == p:
            v, frase = otro, "%d es el mismo que %d, asi que el hueco es el mismo que el otro: %d" % (n, p, otro)
            break
        k = _veces(u, n, p)
        sube = True
        if not k:
            k = _veces(u, p, n)
            sube = False
        if not k:
            continue
        if c["op"] == "x":       # lo que sube uno, lo baja el otro
            hacia = "baja" if sube else "sube"
        else:                    # los dos cambian igual
            hacia = "sube" if sube else "baja"
        v = _cambiar(u, otro, hacia, k)
        frase = ("%d es %d veces mas %s que %d; %s el hueco es %d veces mas %s que %d: %d" % (
            n, k, "grande" if sube else "pequeno", p,
            "en x lo que sube uno lo baja el otro, asi que" if c["op"] == "x" else "en : los dos cambian igual, asi que",
            k, "grande" if hacia == "sube" else "pequeno", otro, v))
        break
    else:
        raise ValueError("no veo cuantas veces cambia (no hay pareja que sea justo K veces la otra)")
    return {"valor": v, "metodo": "la equivalencia (M.12)",
            "cuenta": "%s  (sin calcular los lados; NCETM 2.18)" % frase,
            "vuelta": "", "vuelta_ok": True}
