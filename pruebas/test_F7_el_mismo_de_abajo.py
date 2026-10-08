# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO F.7: EL MISMO DE ABAJO — SUMAR, RESTAR Y COMPARAR CON DISTINTO DE ABAJO (NCETM 3.8; 5.NF.A.1-2).
El plan y sus trampas: diario/2026-10-08-paso-F7-el-mismo-de-abajo.md
Python solo aparece aqui como TESTIGO externo (Fraction).
"""
import importlib.util
import os
import random
import shutil
import sys
import tempfile
import time
from fractions import Fraction

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)
TMP = tempfile.mkdtemp(prefix="f7_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria propia: solo las tablas
import motor  # noqa: E402
import probar  # noqa: E402

BIEN = MAL = 0


def comprobar(nombre, obtenido, esperado):
    global BIEN, MAL
    if obtenido == esperado:
        BIEN += 1
        print("  bien    %s" % nombre)
    else:
        MAL += 1
        print("  FALLA   %s\n          esperado=%r  obtenido=%r" % (nombre, esperado, obtenido))


SABER = motor.cargar_conocimiento()
AZAR = random.Random(38)
NOMBRES = list(range(2, 13)) + [100, 1000]


def S(t):
    return probar.preguntar(probar.como_problema(t), SABER)[0]


def texto(f):
    """como escribe Euclides un resultado: 3/4, 1, 0, 1 5/12."""
    if f.denominator == 1:
        return str(f.numerator)
    e, r = divmod(f.numerator, f.denominator)
    return "%d/%d" % (r, f.denominator) if e == 0 else "%d %d/%d" % (e, r, f.denominator)


def relacionadas(b, d):
    return max(b, d) % min(b, d) == 0


def signo(x, y):
    return ">" if x > y else "<" if x < y else "="


def revisar_cuenta(fa, op, fb, malos):
    """La cuenta contra el testigo: el valor (en su forma mas simple), la vuelta, y el metodo elegido."""
    r = motor.decidir_cuenta_fracciones(fa, op, fb, SABER)
    v = Fraction(*fa) + Fraction(*fb) if op == "+" else Fraction(*fa) - Fraction(*fb)
    if v < 0:
        if r["conclusion"] != "imposible":
            malos.append((fa, op, fb, "debia ser imposible", r["conclusion"]))
        return
    if r["conclusion"] != "hecho" or Fraction(*r["valor"]) != v or not r["vuelta_ok"]:
        malos.append((fa, op, fb, r.get("valor"), v))
        return
    if v and (r["valor"][0], r["valor"][1]) != (v.numerator, v.denominator):
        malos.append((fa, op, fb, "no simplificada", r["valor"]))
    elegida = r["comun"]["pieza"]["id"]
    if (elegida == "mismo_de_abajo_cambiando_una") != relacionadas(fa[1], fb[1]):
        malos.append((fa, op, fb, "metodo", elegida))


try:
    print("=" * 78)
    print("PASO F.7 - EL MISMO DE ABAJO: SUMAR, RESTAR Y COMPARAR CON DISTINTO DE ABAJO")
    print("=" * 78)
    motor.aprender("tablas", SABER)          # en 5.o las tablas ya se saben

    print("\nA - LAS TRAMPAS DEL PLAN")
    for t, esperado, porque in (
            ("1/2 + 1/3", "5/6", "no 2/5 (arriba con arriba, abajo con abajo)"),
            ("1/2 + 1/4", "3/4", "no 2/6; relacionadas: cambiar solo una"),
            ("3/4 - 1/2", "1/4", "no 2/2 (restar los de abajo)"),
            ("3/4 + 5/8", "1 3/8", "no unitarias relacionadas"),
            ("1/3 + 1/4", "7/12", "no relacionadas: 3 x 4"),
            ("1/2 + 2/4", "1", "un entero justo"),
            ("5/6 - 1/3", "1/2", "3/6, simplificada al final"),
            ("2/3 + 3/4", "1 5/12", "mas de un entero"),
            ("1/4 - 1/2", "imposible", "se quita mas de lo que hay"),
            ("1/2 - 2/4", "0", "lo mismo: cero"),
            ("comparar: 2/3 y 3/4", "2/3 < 3/4", "antes todavia no"),
            ("comparar: 3/12 y 1/4", "3/12 = 1/4", "equivalentes, ahora por tres caminos"),
            ("comparar: 5/8 y 7/12", "5/8 > 7/12", "no relacionadas"),
            ("2 1/2 + 1 1/4", "3 3/4", "mixtos"),
            ("3 1/3 - 1 1/2", "1 5/6", "mixtos, hay que cambiar un entero"),
            ("1 1/2 - 2 1/4", "imposible", "mixtos: se quita mas de lo que hay"),
            ("1/2 + 1/13", "todavia_no", "los de abajo de partida: los que tienen nombre"),
            ("1/2 + 1/0", "imposible", "el cero abajo")):
        comprobar("A %s -> %s  (%s)" % (t, esperado, porque), S(t), esperado)
    t = motor.explicar_pregunta("1/2 + 1/3", SABER)
    comprobar("A 1/2 + 1/3 dice el error tipico: NO es 2/5, porque 2/5 es menor que 1/2",
              "NO es 2/5" in t and "2/5 es MENOR que 1/2" in t, True)
    t = motor.explicar_pregunta("3/4 - 1/2", SABER)
    comprobar("A 3/4 - 1/2 dice el error de restar los de abajo (2/2 es mayor que 3/4)", "2/2 es MAYOR que 3/4" in t, True)
    t = motor.explicar_pregunta("1/2 + 1/4", SABER)
    comprobar("A 1/2 + 1/4: cambia solo una y dice que multiplicar tambien servia",
              ("Cambio solo 1/2" in t, "[si]  multiplicar los de abajo" in t), (True, True))
    t = motor.explicar_pregunta("5/6 - 1/3", SABER)
    comprobar("A 5/6 - 1/3: 3/6 y simplifica a 1/2", "3/6 = 1/2" in t, True)

    print("\nB - SUMAR Y RESTAR, CONTRA EL TESTIGO (valor, la vuelta, simplificada, y el metodo: cambiar una SOLO si son relacionadas)")
    malos = []
    unitarias = [(1, b) for b in range(2, 13)]
    for x in unitarias:
        for y in unitarias:
            if x[1] != y[1]:
                for op in "+-":
                    revisar_cuenta(x, op, y, malos)
    comprobar("B1 las 220 cuentas de unitarias de 1/2 a 1/12", malos[:3], [])
    malos = []
    for _ in range(250):
        b, d = AZAR.sample(range(2, 13), 2)
        revisar_cuenta((AZAR.randint(1, b - 1), b), AZAR.choice("+-"), (AZAR.randint(1, d - 1), d), malos)
    comprobar("B2 250 cuentas no unitarias (de abajo de 2 a 12) al azar fijo", malos[:3], [])
    malos = []
    for _ in range(120):
        b, d = AZAR.sample(NOMBRES, 2)
        if 1000 in (b, d) or 100 in (b, d):
            revisar_cuenta((AZAR.randint(1, b - 1), b), AZAR.choice("+-"), (AZAR.randint(1, d - 1), d), malos)
    comprobar("B3 cuentas con decimos, centesimos y milesimos", malos[:3], [])
    malos = []
    for _ in range(60):                       # impropias tambien (5/4 + 2/3)
        b, d = AZAR.sample(range(2, 13), 2)
        revisar_cuenta((AZAR.randint(b, 3 * b), b), AZAR.choice("+-"), (AZAR.randint(1, 2 * d), d), malos)
    comprobar("B4 60 cuentas con impropias", malos[:3], [])

    print("\nC - COMPARAR SIN NADA EN COMUN (los dos caminos de F.7, de acuerdo con el testigo)")
    malos, dos = [], 0
    for _ in range(200):
        b, d = AZAR.sample(NOMBRES, 2)
        x, y = (AZAR.randint(1, b), b), (AZAR.randint(1, d), d)
        if x[0] == y[0]:
            continue
        r = motor.decidir_comparar_fracciones(x, y, SABER)
        ids = [p for p, _ in r.get("todos", [])]
        # el mismo de arriba no sale cuando pide dividir entre dos cifras o mas (715 x 93: la division larga es de 6.o)
        if r["conclusion"] != "hecho" or r["valor"] != signo(Fraction(*x), Fraction(*y)) \
                or "fracciones_con_el_mismo_de_abajo" not in ids:
            malos.append((x, y, r.get("valor"), ids))
        dos += "fracciones_con_el_mismo_de_arriba" in ids
    comprobar("C1 200 parejas al azar fijo (medios ... milesimos); %d tambien por el mismo de arriba" % dos, malos[:3], [])
    malos = []
    for b in range(2, 13):
        for d in range(2, 13):
            for a in sorted({1, b - 1}):
                x, y = (a, b), (d - 1, d)
                if b == d or a == d - 1:
                    continue
                r = motor.decidir_comparar_fracciones(x, y, SABER)
                if r["conclusion"] != "hecho" or r["valor"] != signo(Fraction(*x), Fraction(*y)) or len(r["todos"]) < 2:
                    malos.append((x, y, r.get("valor")))
    comprobar("C1b con de abajo de 2 a 12 salen SIEMPRE los dos caminos (1/b y (b-1)/b contra (d-1)/d)", malos[:3], [])
    r = motor.decidir_comparar_fracciones((1, 2), (2, 4), SABER)
    comprobar("C2 1/2 y 2/4 (equivalentes): '=' por tres caminos",
              (r["valor"], sorted(p for p, _ in r["todos"])),
              ("=", ["fracciones_con_el_mismo_de_abajo", "fracciones_con_el_mismo_de_arriba",
                     "fracciones_equivalentes_simplificando"]))

    print("\nD - NUMEROS MIXTOS CON DISTINTO DE ABAJO (contra el testigo)")
    malos = []
    for _ in range(100):
        b, d = AZAR.sample(range(2, 13), 2)
        x = (AZAR.randint(0, 5), AZAR.randint(1, b - 1), b)
        y = (AZAR.randint(0, 5), AZAR.randint(1, d - 1), d)
        op = AZAR.choice("+-")
        fx, fy = x[0] + Fraction(x[1], b), y[0] + Fraction(y[1], d)
        v = fx + fy if op == "+" else fx - fy
        t = "%s %s %s" % ("%d %d/%d" % x if x[0] else "%d/%d" % x[1:], op, "%d %d/%d" % y if y[0] else "%d/%d" % y[1:])
        esperado = "imposible" if v < 0 else texto(v)
        if S(t) != esperado:
            malos.append((t, S(t), esperado))
    comprobar("D1 100 cuentas con mixtos al azar fijo", malos[:3], [])

    print("\nE - CADA PIEZA SE COMPRUEBA DE VERDAD (si una cuenta sale mal, la vuelta lo caza)")
    base = motor.cargar_piezas()

    def modulo(nombre):
        sp = importlib.util.spec_from_file_location(nombre, os.path.join(RAIZ, "conocimiento", "piezas", nombre + ".py"))
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        return m

    class Tramposo:
        """Lo que se le da a la pieza, pero la cuenta que se le pide (la vez 'vez') da UNO DE MAS."""

        def __init__(self, real, cual, vez=1):
            self._real, self._cual, self._vez, self._hecho = real, cual, vez, False

        def __getattr__(self, k):
            return getattr(self._real, k)

        def usar(self, nombre, **sit):
            r = self._real.usar(nombre, **sit)
            if nombre == self._cual and not self._hecho:
                self._vez -= 1
                if self._vez == 0:
                    self._hecho = True
                    r = dict(r)
                    if isinstance(r["valor"], int):
                        r["valor"] = r["valor"] + 1
                    else:                                 # dos fracciones: la primera, una de mas arriba
                        (xa, d), otra = r["valor"]
                        r["valor"] = ((xa + 1, d), otra)
            return r

    for nombre, sit, cual, vez in (
            ("mismo_de_abajo_cambiando_una", {"a": (1, 2), "b": (1, 4)}, "multiplicar", 1),
            ("mismo_de_abajo_cambiando_una", {"a": (1, 2), "b": (1, 4)}, "dividir", 1),
            ("mismo_de_abajo_cambiando_una", {"a": (5, 8), "b": (3, 4)}, "dividir", 2),
            ("mismo_de_abajo_multiplicando_los_de_abajo", {"a": (1, 3), "b": (1, 4)}, "multiplicar", 1),
            ("mismo_de_abajo_multiplicando_los_de_abajo", {"a": (2, 3), "b": (3, 4)}, "multiplicar", 3),
            ("mismo_de_abajo_multiplicando_los_de_abajo", {"a": (2, 3), "b": (3, 4)}, "dividir", 2),
            ("fracciones_con_el_mismo_de_abajo", {"a": (2, 3), "b": (3, 4)}, "mismo_de_abajo", 1),
            ("fracciones_con_el_mismo_de_abajo", {"a": (2, 3), "b": (3, 4)}, "dividir", 1),
            ("fracciones_con_el_mismo_de_arriba", {"a": (2, 3), "b": (3, 4)}, "multiplicar", 1),
            ("fracciones_con_el_mismo_de_arriba", {"a": (2, 3), "b": (3, 4)}, "multiplicar", 2),
            ("fracciones_con_el_mismo_de_arriba", {"a": (2, 3), "b": (4, 9)}, "dividir", 1)):
        m = modulo(nombre)
        real = motor.Lo_que_puede_usar(base["piezas"][nombre], base, SABER) if hasattr(motor, "Lo_que_puede_usar") \
            else motor._Lo_que_puede_usar(base["piezas"][nombre], base, SABER)
        bien = m.hacer(sit, real)
        try:
            truco = m.hacer(sit, Tramposo(real, cual, vez))
            cazado = bien["vuelta_ok"] is True and truco["vuelta_ok"] is False
        except Exception:
            cazado = bien["vuelta_ok"] is True     # la cuenta mala tambien puede hacer que no salga: tampoco vale
        comprobar("E %s: con '%s' (vez %d) dando uno de mas, la vuelta NO cuadra" % (nombre, cual, vez), cazado, True)
    mapa = motor.mapa_del_conocimiento()
    comprobar("E ninguna pieza usa su propia pregunta",
              [p for p, usa in mapa.items() if base["piezas"][p]["responde"] in usa], [])
    comprobar("E las piezas cargan sin problemas", base["problemas"], [])

    print("\nF - LO DE ANTES SIGUE IGUAL")
    for t, esperado in (("2/7 + 3/7", "5/7"), ("1 - 3/8", "5/8"), ("4/7 + 5/7", "1 2/7"), ("2 1/4 + 1 3/4", "4"),
                        ("comparar: 1/3 y 1/5", "1/3 > 1/5"), ("comparar: 2/3 y 2/5", "2/3 > 2/5"),
                        ("simplificar: 12/18", "2/3"), ("2/3 = ?/12", "8"), ("3 x 2/5", "1 1/5"),
                        ("equivalentes: 2/3 y 3/4", "no"), ("0.3 + 0.45", "0.75"), ("recta: 3 - 8", "-5")):
        comprobar("F %s -> %s" % (t, esperado), S(t), esperado)

    print("\nG - CERCA DEL TECHO, y el TIEMPO (cada pregunta, con su explicacion, en menos de 2 s)")
    for t, esperado in (("1/7 + 1/1000", "1007/7000"), ("999/1000 + 1/1000", "1"), ("999/1000 + 1/100", "1 9/1000"),
                        ("1/11 + 1/1000", "1011/11000"), ("1/100 - 1/1000", "9/1000"), ("7/12 - 5/11", "17/132"),
                        ("comparar: 999/1000 y 11/12", "999/1000 > 11/12"), ("comparar: 1/1000 y 1/999", "todavia_no"),
                        ("comparar: 7/11 y 5/8", "7/11 > 5/8"), ("999 1/2 + 999 1/3", "1998 5/6"),
                        ("1/1000 + 1/999", "todavia_no")):
        t1 = time.time()
        r = S(t)
        motor.explicar_pregunta(probar.como_problema(t), SABER)
        dt = time.time() - t1
        comprobar("G %s -> %s (%.2f s)" % (t, esperado, dt), (r, dt < 2), (esperado, True))
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\nTOTAL: %d/%d" % (BIEN, BIEN + MAL))
