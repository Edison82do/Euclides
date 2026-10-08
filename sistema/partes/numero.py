# -*- coding: utf-8 -*-
"""
Euclides - EL NUMERO COMUN (fase U.1 del plan U, 8 oct 2026).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

Hasta ahora los enteros, los decimales, las fracciones y los negativos vivian en partes distintas y una cuenta que
los mezclaba (1/2 + 0.25) no tenia camino.  Aqui un NUMERO es UNA cosa:

    (signo, arriba, abajo, tipo)        signo '+' o '-';  arriba y abajo enteros;  tipo entero | decimal | fraccion

    7     -> ('+', 7, 1, 'entero')       4.5  -> ('+', 45, 10, 'decimal')     (D.1: 45 decimas)
    1/2   -> ('+', 1, 2, 'fraccion')     -3   -> ('-', 3, 1, 'entero')         (N.5: del otro lado del cero)

Y se opera como lo haria un nino (Common Core 7.NS.A.1-2; NCETM 1.23-1.24, 1.27, 3.7, 3.8):
  - un decimal ES una fraccion de diez, cien o mil: si se mezcla con una fraccion, se pasa al MISMO DE ABAJO (F.7);
  - sumar y restar: el mismo de abajo y se suman o se restan los de arriba;  con signos distintos se quita el mas
    pequeno del mas grande y queda el signo del mas grande (la recta, N.5);
  - multiplicar: arriba por arriba y abajo por abajo (5.NF.B.4; con decimas, M.13: contar las partes);
  - dividir entre un entero: si el de arriba se reparte justo, se reparte (45 decimas : 3 = 15 decimas); si no, se
    parte cada trozo (3/4 : 2 = 3/8; 7 : 2 = 7/2, 5.NF.B.3);  entre una fraccion: por ella dada la vuelta (6.NS.A.1);
  - al final, la forma mas simple (F.6) y se escribe en el tipo que toca.
TODAS las cuentas las hacen las PIEZAS de siempre (sumar, restar, multiplicar, dividir, mismo_de_abajo,
simplificar_fraccion, hueco_equivalente) y los tamanos se comparan con el mecanismo (viene_despues).  Cada cuenta deja
su linea en 'pasos', para explicarla.
"""


class _NuNoSale(Exception):
    """Una cuenta que no sale (se pasa del techo, una pieza que no puede, dividir entre cero...)."""


_NU_CERO = ("+", 0, 1, "entero")
_NU_DIEZ = {1: 10, 10: 100, 100: 1000}                 # D.2: cada sitio, diez veces mas pequeno (leer cifras)
_NU_POTENCIAS = (1, 10, 100, 1000)


def _nu_leer(texto):
    """'7' -> entero;  '4.5' o '4,5' -> decimal (45/10);  '1/2' -> fraccion.  Es LEER las cifras."""
    t = texto.replace(" ", "").replace(",", ".")
    if "/" in t:
        a, b = t.split("/", 1)
        arriba, abajo = escribir_cifras(cifras_de(a)), escribir_cifras(cifras_de(b))
        if abajo == 0:
            raise _NuNoSale("%s: abajo no puede haber un cero (no se parte en cero trozos)" % texto)
        return ("+", arriba, abajo, "fraccion")
    if "." in t:
        e, d = t.split(".", 1)
        if len(d) > 3:
            raise _NuNoSale("%s: con mas de tres cifras detras del punto todavia no (llego a las milesimas)" % texto)
        arriba = _dec_en_pequenas(t, len(d))
        abajo = escribir_cifras([0 for _ in d] + [1])          # 1 y tantos ceros como cifras detras del punto
        return ("+", arriba, abajo, "decimal")
    return ("+", escribir_cifras(cifras_de(t)), 1, "entero")


def _nu_es_cero(x):
    return x[1] == 0


def _nu_opuesto(x):
    if _nu_es_cero(x):
        return x
    return ("-" if x[0] == "+" else "+", x[1], x[2], x[3])


def _nu_tipo(*xs):
    tipos = {x[3] for x in xs}
    for t in ("fraccion", "decimal"):
        if t in tipos:
            return t
    return "entero"


def _nu_texto(x):
    """Escribir el numero: -3, 1.5, 3/8.  Un decimal con su punto si abajo es 10, 100 o 1000."""
    s, a, b, t = x
    signo = "-" if s == "-" and a != 0 else ""
    if b == 1:
        return "%s%d" % (signo, a)
    if t == "decimal" and b in _NU_POTENCIAS:
        return "%s%s" % (signo, _dec_escribir(a, len(str(b)) - 1))
    return "%s%d/%d" % (signo, a, b)


# ------------------------------------------------------------- las cuentas de enteros: las PIEZAS

def _nu_pieza(pregunta, situacion, saber):
    r = aplicar(pregunta, situacion, saber)
    if r["conclusion"] != "hecho":
        raise _NuNoSale(r.get("porque") or "%s no me sale" % pregunta)
    return r


def _nu_suma(a, b, saber):
    if a == 0:
        return b
    if b == 0:
        return a
    return _nu_pieza("sumar", {"a": a, "b": b}, saber)["valor"]


def _nu_resta(a, b, saber):
    """a - b con a mayor o igual que b."""
    if b == 0:
        return a
    if a == b:
        return 0
    return _nu_pieza("restar", {"a": a, "b": b}, saber)["valor"]


def _nu_por(a, b, saber):
    if a == 1:
        return b
    if b == 1:
        return a
    if a == 0 or b == 0:
        return 0
    return _nu_pieza("multiplicar", {"a": a, "b": b}, saber)["valor"]


def _nu_entre(a, b, saber):
    """(cociente, resto) de a : b, con las piezas de dividir."""
    if b == 1:
        return a, 0
    if a == 0:
        return 0, 0
    r = _nu_pieza("dividir", {"total": a, "divisor": b}, saber)
    return r["valor"], r["resultado"].get("resto", 0)


def _nu_mayor(a, b, saber):
    """a es MAYOR que b (4.2: viene despues en la lista)."""
    pa, pb = decir(a, saber), decir(b, saber)
    if pa is None or pb is None:
        raise _NuNoSale("%d o %d se pasa de mi techo (%s)" % (a, b, techo(saber)))
    return viene_despues(pa, pb, saber)


# ------------------------------------------------------------- el mismo de abajo y la forma mas simple

def _nu_mismo_de_abajo(x, y, saber, pasos):
    """Devuelve (arriba de x, arriba de y, abajo comun).  F.7: con las piezas de mismo_de_abajo."""
    if x[2] == y[2]:
        return x[1], y[1], x[2]
    if _nu_es_cero(x):
        return 0, y[1], y[2]
    if _nu_es_cero(y):
        return x[1], 0, x[2]
    r = _nu_pieza("mismo_de_abajo", {"a": (x[1], x[2]), "b": (y[1], y[2])}, saber)
    (xa, d), (ya, _) = r["valor"]
    pasos.append("el mismo de abajo: %d/%d = %d/%d y %d/%d = %d/%d   (%s)"
                 % (x[1], x[2], xa, d, y[1], y[2], ya, d, r["resultado"]["metodo"]))
    return xa, ya, d


def _nu_simple(x, saber, pasos):
    """La forma mas simple (F.6).  Un decimal se deja en decimas, centesimas o milesimas mientras pueda."""
    s, a, b, t = x
    if a == 0:
        return _NU_CERO
    if b == 1:
        return (s, a, 1, "entero" if t == "entero" else t)
    if t == "decimal" and b in _NU_POTENCIAS:
        return x
    r = aplicar("simplificar_fraccion", {"a": a, "b": b}, saber)
    if r["conclusion"] != "hecho":
        pasos.append("%d/%d: no se simplificarla mas (%s)" % (a, b, r.get("porque", "")))
        return x
    na, nb = r["resultado"]["arriba"], r["resultado"]["abajo"]
    if (na, nb) != (a, b):
        pasos.append("simplifico: %d/%d = %d/%d   (%s)" % (a, b, na, nb, r["resultado"]["metodo"]))
    nuevo = (s, na, nb, t)
    if t == "decimal":                       # un decimal que se dividio: vuelve a decimas, centesimas o milesimas
        nuevo = _nu_en_decimas(nuevo, saber, pasos) or (s, na, nb, "fraccion")
    return nuevo


def _nu_en_decimas(x, saber, pasos):
    """3/4 -> 75/100 (= 0.75), si sale justo con 10, 100 o 1000 abajo (hueco_equivalente, F.6).  Si no, None."""
    s, a, b, _ = x
    if b in _NU_POTENCIAS:
        return (s, a, b, "decimal")
    for diez in (10, 100, 1000):
        _, resto = _nu_entre(diez, b, saber) if not _nu_mayor(b, diez, saber) else (0, 1)
        if resto:
            continue
        r = aplicar("hueco_equivalente", {"completa": (a, b), "con_hueco": (None, diez)}, saber)
        if r["conclusion"] == "hecho":
            pasos.append("%d/%d = %s/%d = %s" % (a, b, r["valor"], diez, _dec_escribir(r["valor"], len(str(diez)) - 1)))
            return (s, r["valor"], diez, "decimal")
    return None


def _nu_decimal_a_fraccion(x, saber, pasos):
    """0.25 = 25/100 = 1/4: el decimal se dice como fraccion (para mezclarlo con una fraccion)."""
    if x[3] != "decimal" or x[2] == 1:
        return x
    y = _nu_simple((x[0], x[1], x[2], "fraccion"), saber, [])
    pasos.append("el decimal es una fraccion: %s = %d/%d%s" % (_nu_texto(x).lstrip("-"), x[1], x[2],
                                                              "" if y[2] == x[2] else " = %d/%d" % (y[1], y[2])))
    return y


# ------------------------------------------------------------- las cuatro cuentas

def _nu_preparar(x, y, saber, pasos):
    """Si se mezclan un decimal y una fraccion, el decimal se pasa a fraccion (como haria un nino)."""
    if {x[3], y[3]} == {"decimal", "fraccion"}:
        x, y = _nu_decimal_a_fraccion(x, saber, pasos), _nu_decimal_a_fraccion(y, saber, pasos)
    return x, y


def _nu_sumar(x, y, saber, pasos):
    x, y = _nu_preparar(x, y, saber, pasos)
    tipo = _nu_tipo(x, y)
    if _nu_es_cero(x):
        return y
    if _nu_es_cero(y):
        return x
    xa, ya, d = _nu_mismo_de_abajo(x, y, saber, pasos)
    if x[0] == y[0]:
        r = (x[0], _nu_suma(xa, ya, saber), d, tipo)
    elif xa == ya:
        r = _NU_CERO
    elif _nu_mayor(xa, ya, saber):
        r = (x[0], _nu_resta(xa, ya, saber), d, tipo)
        pasos.append("signos distintos (la recta, N.5): %d - %d = %d, con el signo del mas grande"
                     % (xa, ya, r[1]))
    else:
        r = (y[0], _nu_resta(ya, xa, saber), d, tipo)
        pasos.append("signos distintos (la recta, N.5): %d - %d = %d, con el signo del mas grande"
                     % (ya, xa, r[1]))
    return _nu_simple(r, saber, pasos)


def _nu_restar(x, y, saber, pasos):
    x, y = _nu_preparar(x, y, saber, pasos)
    if x[0] == "+" and y[0] == "+" and not _nu_es_cero(y):      # quitar de lo que hay (lo de siempre)
        xa, ya, d = _nu_mismo_de_abajo(x, y, saber, pasos)
        if xa == ya:
            return _NU_CERO
        if _nu_mayor(xa, ya, saber):
            return _nu_simple(("+", _nu_resta(xa, ya, saber), d, _nu_tipo(x, y)), saber, pasos)
        r = ("-", _nu_resta(ya, xa, saber), d, _nu_tipo(x, y))
        pasos.append("se quita mas de lo que hay: pasa del cero (la recta, N.5): %d - %d = %d, en negativo"
                     % (ya, xa, r[1]))
        return _nu_simple(r, saber, pasos)
    return _nu_sumar(x, _nu_opuesto(y), saber, pasos)


def _nu_multiplicar(x, y, saber, pasos):
    x, y = _nu_preparar(x, y, saber, pasos)
    tipo = _nu_tipo(x, y)
    if _nu_es_cero(x) or _nu_es_cero(y):
        return _NU_CERO
    signo = "+" if x[0] == y[0] else "-"
    arriba = _nu_por(x[1], y[1], saber)
    abajo = _nu_por(x[2], y[2], saber)
    if x[2] != 1 or y[2] != 1:
        pasos.append("arriba por arriba y abajo por abajo: %d x %d = %d;  %d x %d = %d"
                     % (x[1], y[1], arriba, x[2], y[2], abajo))
    return _nu_simple((signo, arriba, abajo, tipo), saber, pasos)


def _nu_dividir(x, y, saber, pasos):
    x, y = _nu_preparar(x, y, saber, pasos)
    if _nu_es_cero(y):
        raise _NuNoSale("dividir entre cero no se puede (no hay grupos de cero que hagan %s)" % _nu_texto(x))
    tipo = _nu_tipo(x, y)
    if _nu_es_cero(x):
        return _NU_CERO
    signo = "+" if x[0] == y[0] else "-"
    if y[2] != 1:                    # entre una fraccion o un decimal: con el MISMO DE ABAJO, cuantas veces cabe
        xa, ya, d = _nu_mismo_de_abajo(x, y, saber, pasos)
        pasos.append("con el mismo de abajo, dividir es ver cuantas veces cabe: %d/%d : %d/%d = %d : %d"
                     % (xa, d, ya, d, xa, ya))
        x, y = (signo, xa, 1, "entero"), ("+", ya, 1, "entero")
    c, resto = _nu_entre(x[1], y[1], saber)
    if not resto:                                     # se reparte justo: 45 decimas : 3 = 15 decimas
        if x[2] != 1:
            pasos.append("%d/%d : %d -> reparto los de arriba: %d : %d = %d" % (x[1], x[2], y[1], x[1], y[1], c))
        return _nu_simple((signo, c, x[2], tipo), saber, pasos)
    abajo = _nu_por(x[2], y[1], saber)                # no se reparte justo: cada trozo se parte (5.NF.B.3, 5.NF.B.7)
    pasos.append("%s : %d no se reparte justo: cada trozo se parte en %d -> %d/%d"
                 % (_nu_texto(("+", x[1], x[2], x[3])), y[1], y[1], x[1], abajo))
    return _nu_simple((signo, x[1], abajo, "fraccion" if tipo == "entero" else tipo), saber, pasos)


_NU_CUENTAS = {"+": _nu_sumar, "-": _nu_restar, "x": _nu_multiplicar, ":": _nu_dividir}


def _nu_cuenta(op, x, y, saber, pasos):
    """Una cuenta con el numero comun: deja su linea y devuelve el resultado."""
    sub = []
    try:
        r = _NU_CUENTAS[op](x, y, saber, sub)
    except KeyError as e:                       # un numero sin nombre (pasa del techo)
        raise _NuNoSale("un numero se pasa de mi techo (%s): %s" % (techo(saber), e))
    pasos.append("%s %s %s = %s" % (_nu_parentesis(x), op, _nu_parentesis(y), _nu_texto(r)))
    pasos.extend("     (%s)" % p for p in sub)
    return r


def _nu_parentesis(x):
    t = _nu_texto(x)
    return "(%s)" % t if t.startswith("-") else t


def _nu_iguales(x, y, saber):
    """Son el MISMO numero?  Al mismo de abajo y se miran los de arriba (y el signo)."""
    if _nu_es_cero(x) or _nu_es_cero(y):
        return _nu_es_cero(x) and _nu_es_cero(y)
    if x[0] != y[0]:
        return False
    xa, ya, _ = _nu_mismo_de_abajo(x, y, saber, [])
    return xa == ya
