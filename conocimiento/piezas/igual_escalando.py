# -*- coding: utf-8 -*-
"""Pieza de la IGUALDAD (paso M.12; NCETM 2.18): VER LA EQUIVALENCIA SIN CALCULAR.
   3 x 12 = 6 x 6 es VERDAD: 6 es 2 veces 3, y 6 es 12 : 2.  Un factor sube 2 veces y el otro baja 2
   veces: el producto no cambia (punto 1).
   96 : 4 = 48 : 2 es VERDAD: los dos a la mitad, el cociente no cambia (punto 2).
Si no hay esa relacion, no se puede decir nada sin calcular: lo decide la pieza que calcula los lados.
(La trampa: 3 x 12 = 4 x 11 no es verdad; 'uno mas aqui, uno menos alli' es la compensacion de la SUMA.)"""

PIEZA = {
    "id": "igual_escalando",
    "nombre": "la equivalencia (x: sube uno, baja el otro; :, los dos igual)",
    "unidad": "M.12",
    "responde": "igualdad",
    "rapidez": 3,
    "que_hace": "ve si los lados son equivalentes (NCETM 2.18) sin hacer las cuentas",
    "condiciones": [
        ("dos_lados_por_o_entre", "no son dos multiplicaciones ni dos divisiones"),
    ],
    "usa": ["dividir"],
}


def _veces(u, grande, pequeno):
    """K si grande es K veces pequeno (justo, K > 1); si no, None."""
    if pequeno in (0, grande) or not u.viene_despues(u.decir(grande), u.decir(pequeno)):
        return None
    r = u.usar("dividir", total=grande, divisor=pequeno)
    return None if r["resultado"].get("resto") else r["valor"]


def _relacion(u, p, q):
    """('sube', K) si q es K veces p; ('baja', K) si p es K veces q; None si no."""
    k = _veces(u, q, p)
    if k:
        return "sube", k
    k = _veces(u, p, q)
    if k:
        return "baja", k
    return None


def hacer(s, u):
    i, d = s["lados"]
    if i["op"] == "x":
        for (p, q), (r, t) in (((i["a"], d["a"]), (i["b"], d["b"])), ((i["a"], d["b"]), (i["b"], d["a"]))):
            x, y = _relacion(u, p, q), _relacion(u, r, t)
            if x and y and x[1] == y[1] and x[0] != y[0]:
                return {"valor": "verdadero", "metodo": "la equivalencia (M.12)",
                        "cuenta": "%d -> %d %s %d veces y %d -> %d %s %d veces: un factor sube y el otro baja "
                                  "lo mismo, el producto NO cambia (NCETM 2.18, punto 1).  No hace falta calcular"
                                  % (p, q, x[0], x[1], r, t, y[0], y[1]),
                        "vuelta": "", "vuelta_ok": True}
        raise ValueError("no veo un factor que suba lo que baja el otro")
    x, y = _relacion(u, i["a"], d["a"]), _relacion(u, i["b"], d["b"])
    if x and y and x == y:
        return {"valor": "verdadero", "metodo": "la equivalencia (M.12)",
                "cuenta": "el dividendo %d -> %d %s %d veces y el divisor %d -> %d tambien %s %d veces: los dos "
                          "cambian IGUAL, el cociente NO cambia (NCETM 2.18, punto 2).  No hace falta calcular"
                          % (i["a"], d["a"], x[0], x[1], i["b"], d["b"], y[0], y[1]),
                "vuelta": "", "vuelta_ok": True}
    raise ValueError("el dividendo y el divisor no cambian igual")
