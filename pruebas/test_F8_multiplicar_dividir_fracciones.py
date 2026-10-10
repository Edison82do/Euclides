# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO F.8: MULTIPLICAR FRACCIONES Y DIVIDIR UNA FRACCION ENTRE UN ENTERO (NCETM 3.9, 'Multiplying fractions
and dividing fractions by a whole number', Year 6).
El plan y sus trampas: diario/2026-10-10-paso-F8-multiplicar-y-dividir-fracciones.md
Pocas y representativas (decision de Carlos).  Fraccion por fraccion es una PIEZA de la pregunta nueva
'fraccion_por_fraccion'; una fraccion entre un entero, dos PIEZAS de 'fraccion_entre_entero' (repartir los de arriba si
caben; si no, convertirlo en una multiplicacion), elegidas por el costo.  Las pide el numero comun del resolvedor.
Python (fractions) solo aparece aqui como TESTIGO.
"""
from fractions import Fraction  # noqa: E402  (el TESTIGO)
import importlib.util
import os
import random
import shutil
import sys
import tempfile
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)
TMP = tempfile.mkdtemp(prefix="f8_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia
import motor  # noqa: E402
import probar  # noqa: E402

BIEN = MAL = 0
FXF = "fraccion_por_fraccion_arriba_por_arriba"
REP = "fraccion_entre_entero_repartiendo_los_de_arriba"
INV = "fraccion_entre_entero_por_la_inversa"


def comprobar(nombre, obtenido, esperado):
    global BIEN, MAL
    if obtenido == esperado:
        BIEN += 1
        print("  bien    %s" % nombre)
    else:
        MAL += 1
        print("  FALLA   %s\n          esperado=%r  obtenido=%r" % (nombre, esperado, obtenido))


SABER = motor.cargar_conocimiento()
PIEZAS = os.path.join(RAIZ, "conocimiento", "piezas")


def S(t):
    return probar.preguntar(probar.como_problema(t), SABER)[0]


def X(t):
    return motor.explicar_pregunta(t, SABER)


def modulo(nombre, cambiar):
    """La pieza leida de su archivo y TRUCADA: 'cambiar' = (lo que hay, lo que se pone), solo la PRIMERA vez."""
    src = open(os.path.join(PIEZAS, nombre + ".py"), encoding="utf-8").read()
    assert cambiar[0] in src, cambiar[0]
    src = src.replace(cambiar[0], cambiar[1], 1)
    ruta = os.path.join(TMP, nombre + ".py")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(src)
    sp = importlib.util.spec_from_file_location("f8_" + nombre, ruta)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def main():
    t0 = time.time()
    azar = random.Random(2031)
    print("=" * 78)
    print("PASO F.8: MULTIPLICAR FRACCIONES Y DIVIDIR UNA FRACCION ENTRE UN ENTERO (NCETM 3.9)")
    print("=" * 78)
    base = motor.cargar_piezas()

    print("\nA - FRACCION POR FRACCION (punto 1): la pieza contra el testigo, con su vuelta")
    malas, n = [], 0
    for _ in range(30):
        a, b = azar.randint(1, 12), azar.choice([azar.randint(1, 12), azar.randint(13, 99)])
        c, d = azar.randint(1, 12), azar.choice([azar.randint(1, 12), azar.randint(13, 99)])
        n += 1
        r = motor.aplicar("fraccion_por_fraccion", {"a": (a, b), "b": (c, d)}, SABER)
        if r["conclusion"] != "hecho" or r["valor"] != (a * c, b * d) or r["pieza"]["id"] != FXF \
                or not r["resultado"]["vuelta_ok"]:
            malas.append((a, b, c, d, r.get("valor")))
        # el MISMO numero (con la memoria vacia, sin las tablas, a veces no sabe simplificar del todo: 30/3969)
        if Fraction(S("resolver: %d/%d x %d/%d" % (a, b, c, d))) != Fraction(a, b) * Fraction(c, d):
            malas.append(("resolver", a, b, c, d))
    comprobar("A %d productos al azar: arriba por arriba y abajo por abajo, el testigo, y su vuelta" % n, malas, [])

    print("\nB - UNA FRACCION ENTRE UN ENTERO (puntos 2 y 3): las dos piezas contra el testigo; el costo elige")
    malas, n = [], 0
    for _ in range(30):
        a, b, k = azar.randint(1, 30), azar.randint(1, 30), azar.randint(1, 12)
        n += 1
        cabe = a % k == 0                                                     # el TESTIGO
        r = motor.aplicar("fraccion_entre_entero", {"a": a, "b": b, "n": k}, SABER)
        if r["conclusion"] != "hecho" or Fraction(*r["valor"]) != Fraction(a, b) / k \
                or r["pieza"]["id"] != (REP if cabe else INV) or not r["resultado"]["vuelta_ok"]:
            malas.append((a, b, k, r.get("valor")))
        u = motor._Lo_que_puede_usar(base["piezas"][INV], base, SABER)        # la larga sirve siempre
        res = base["piezas"][INV]["hacer"]({"a": a, "b": b, "n": k}, u)
        if res["valor"] != (a, b * k) or not res["vuelta_ok"]:
            malas.append(("inversa", a, b, k))
    comprobar("B %d divisiones al azar: el testigo, la pieza que toca por su costo y su vuelta" % n, malas, [])
    for (a, b, k), quien in (((6, 7, 3), REP), ((2, 3, 4), INV), ((3, 4, 3), REP), ((3, 5, 2), INV), ((5, 6, 1), REP)):
        r = motor.aplicar("fraccion_entre_entero", {"a": a, "b": b, "n": k}, SABER)
        comprobar("B %d/%d : %d -> %s" % (a, b, k, quien), r["pieza"]["id"], quien)
    r = motor.aplicar("fraccion_entre_entero", {"a": 6, "b": 7, "n": 3}, SABER)
    comprobar("B 6/7 : 3: convertirlo en una multiplicacion tambien servia (se dice, no se hace)",
              r.get("tambien_servian"), [INV])

    print("\nC - LAS TRAMPAS: piezas TRUCADAS (la vuelta las caza)")
    trampas = (
        (FXF, ("arriba, abajo = _por(u, a, c), _por(u, b, d)", "arriba, abajo = _por(u, a, c), b"),
         {"a": (2, 3), "b": (3, 4)}, "multiplicar solo los de arriba (2/3 x 3/4 = 6/3)"),
        (FXF, ("arriba, abajo = _por(u, a, c), _por(u, b, d)", "arriba, abajo = _por(u, a, d), _por(u, b, c)"),
         {"a": (2, 3), "b": (3, 4)}, "multiplicar cruzado (2/3 x 3/4 = 8/9)"),
        (INV, ("arriba = a ", 'arriba = u.usar("multiplicar", a=a, b=n)["valor"] '),
         {"a": 2, "b": 3, "n": 4}, "multiplicar arriba Y abajo por el entero (2/3 : 4 = 8/12)"),
        (INV, ('abajo = u.usar("multiplicar", a=b, b=n)["valor"]', "abajo = b"),
         {"a": 2, "b": 3, "n": 4}, "no partir los trozos (2/3 : 4 = 2/3)"),
        (REP, ("abajo = b ", 'abajo = u.usar("dividir", total=b, divisor=n)["valor"] '),
         {"a": 6, "b": 9, "n": 3}, "dividir tambien el de abajo (6/9 : 3 = 2/3)"),
    )
    for pid, cambio, s, que in trampas:
        u = motor._Lo_que_puede_usar(base["piezas"][pid], base, SABER)
        try:
            cazado = modulo(pid, cambio).hacer(s, u)["vuelta_ok"] is False
        except (ValueError, motor.NoSalio):
            cazado = True
        comprobar("C %s trucada -> se caza" % que, cazado, True)
    r = motor.aplicar("fraccion_entre_entero", {"a": 2, "b": 3, "n": 4}, SABER)
    fila = [f for f in r["candidatos"] if f["id"] == REP][0]
    comprobar("C repartir los de arriba cuando no caben (2/3 : 4): esa pieza se descarta", fila.get("aplica"), None)

    print("\nD - EN EL RESOLVEDOR Y EN LA PUERTA VIEJA (F.5 ya no dice 'todavia no' a fraccion por fraccion)")
    for q, esperado in (("2/3 x 3/4", "1/2"), ("resolver: 2/3 x 3/4", "1/2"), ("calcular: 2/3 x 3/4", "1/2"),
                        ("3/4 x 2/5", "3/10"), ("1/2 de 1/3", "1/6"), ("2/3 : 4", "1/6"), ("6/7 : 3", "2/7"),
                        ("3/5 : 2", "3/10"), ("resolver: 5/4 x 2/3", "5/6"), ("resolver: 2/3 x 3/2", "1"),
                        ("resolver: 2/3 x 3/4 x 4/5", "2/5"), ("resolver: (2/3 x 3/4) : 3", "1/6"),
                        ("resolver: 3/4 x 1/4 + 1/2", "11/16"), ("resolver: -2/3 x 3/4", "-1/2"),
                        ("resolver: 2/3 : -4", "-1/6"), ("resolver: 0.5 x 1/3", "1/6"),
                        ("resolver: r : 4 = 2/3", "r = 8/3"), ("resolver: r x 3/4 = 3/8", "r = 1/2"),
                        ("verdad: 2/3 x 3/4 = 6/12", "VERDADERO"), ("verdad: 2/3 x 3/4 = 6/7", "FALSO"),
                        ("2 1/2 x 1/3", "todavia_no")):
        comprobar("D %s -> %s" % (q, esperado), S(q), esperado)

    print("\nE - LA EXPLICACION: el punto 1 (mas pequeno), la division como multiplicacion, repartir si cabe")
    t = X("2/3 x 3/4")
    comprobar("E 2/3 x 3/4: arriba por arriba, mas pequeno que 2/3, lo comprueba y simplifica",
              "arriba por arriba: 2 x 3 = 6" in t and "3/4 es menos que un entero" in t and "... SI" in t
              and "6/12 = 1/2" in t, True)
    t = X("resolver: 2/3 x 5/4")
    comprobar("E 2/3 x 5/4: por MAS de un entero no se dice 'mas pequeno'", "es menos que un entero" in t, False)
    t = X("2/3 : 4")
    comprobar("E 2/3 : 4 = 2/3 x 1/4 (una multiplicacion equivalente)", "2/3 : 4 = 2/3 x 1/4" in t and "... SI" in t, True)
    t = X("6/7 : 3")
    comprobar("E 6/7 : 3: reparte los de arriba y el de abajo no se toca", "reparto los de arriba, 6 : 3 = 2" in t, True)

    print("\nF - CERO, UNO Y CERCA DEL TECHO (nunca un numero falso)")
    for q, esperado in (("resolver: 0 x 2/3", "0"), ("resolver: 2/3 x 1", "2/3"), ("resolver: 2/3 : 1", "2/3"),
                        ("resolver: 3/4 : 0", "no_se_puede"), ("resolver: 999/1000 x 999/1000", "998001/1000000"),
                        ("resolver: 1/7 : 1000000", "1/7000000"), ("resolver: 9999/10000 x 9999/10000", "todavia_no"),
                        ("resolver: 1/7 : 10000000", "todavia_no")):
        comprobar("F %s -> %s" % (q, esperado), S(q), esperado)

    print("\nG - LO QUE NO CAMBIA")
    for q, esperado in (("3/4 x 2", "1 2/4"), ("3 x 2/5", "1 1/5"), ("1/4 de 12", "3"), ("resolver: 1/2 : 1/4", "2"),
                        ("resolver: 0.5 x 0.3", "0.15"), ("resolver: 7 : 2", "7/2"), ("resolver: 2/3 x r = 1/2", "r = 3/4"),
                        ("1/2 + 1/3", "5/6")):
        comprobar("G %s -> %s" % (q, esperado), S(q), esperado)

    print("\nH - EL TIEMPO (cada pregunta muy por debajo de 2 s)")
    for q in ("resolver: 999/1000 x 999/1000", "resolver: 1/7 : 1000000", "resolver: 98/99 x 97/98 x 96/97"):
        t1 = time.time()
        S(q)
        d = time.time() - t1
        comprobar("H %s (%.2f s)" % (q, d), d < 2, True)

    print("\n(%.1f s)" % (time.time() - t0))
    print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
    shutil.rmtree(TMP, ignore_errors=True)
    return 1 if MAL else 0


if __name__ == "__main__":
    sys.exit(main())
