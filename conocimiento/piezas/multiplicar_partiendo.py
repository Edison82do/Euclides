# -*- coding: utf-8 -*-
"""Pieza de MULTIPLICAR (paso M.6): la DISTRIBUTIVA (NCETM 2.10; Common Core 3.OA.B.5).  Se parte un
factor en dos trozos cuyos productos ya se saben: 8 x 7 = 8 x 5 + 8 x 2 = 40 + 16 = 56 (el ejemplo del
estandar).  Y sirve MAS ALLA de las tablas: 12 x 6 = 10 x 6 + 2 x 6 = 60 + 12 = 72."""

PIEZA = {
    "id": "multiplicar_partiendo",
    "nombre": "partir un factor (la distributiva)",
    "unidad": "M.6",
    "responde": "multiplicar",
    "rapidez": 9,
    "que_hace": "parte un factor en dos trozos cuyos productos ya se (7 = 5 + 2) y suma los dos productos",
    "condiciones": [
        ("un_factor_se_puede_partir", "ningun factor se puede partir en trozos cuyos productos ya sepa"),
    ],
    "usa": ["sumar"],
}

_TROZOS = (10, 5, 2, 4, 3)          # se prueba primero lo mas redondo (10 y 5), como hacen los ninos


def _sabido(x, k, u):
    if x == 1:
        return k
    h = u.recuerdo("%d x %d" % (x, k)) or u.recuerdo("%d x %d" % (k, x))
    return h["valor"] if h else None


def partir(s, u):
    """(f, k, p, q, p x k, q x k) o None: f = p + q y los dos productos se saben."""
    for f, k in ((s["a"], s["b"]), (s["b"], s["a"])):
        for p in _TROZOS:
            if not u.viene_despues(u.decir(f), u.decir(p)):
                continue
            q = u.leer(u.contar_hasta(u.decir(p), u.decir(f)))
            pk, qk = _sabido(p, k, u), _sabido(q, k, u)
            if pk is not None and qk is not None:
                return f, k, p, q, pk, qk
    return None


def hacer(s, u):
    f, k, p, q, pk, qk = partir(s, u)
    r = u.usar("sumar", a=pk, b=qk)
    return {"valor": r["valor"], "metodo": "partiendo (M.6)",
            "cuenta": "%d = %d + %d, asi que %d x %d = %d x %d + %d x %d = %d + %d = %d"
                      % (f, p, q, f, k, p, k, q, k, pk, qk, r["valor"]),
            "vuelta": "", "vuelta_ok": True}
