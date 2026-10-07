# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.16: COMBINAR LA MULTIPLICACION CON LA SUMA Y LA RESTA (NCETM 2.22; 5.OA.A.1).
El plan y sus trampas: diario/2026-10-07-paso-M16-combinar-operaciones.md
Python solo aparece aqui como TESTIGO externo (las cuentas con Fraction, +, -, *).
"""
import importlib.util
import os
import random
import re
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
TMP = tempfile.mkdtemp(prefix="m16_")
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


def S(t):
    return probar.preguntar(probar.como_problema(t), SABER)[0]


def D(t):
    r = motor.decidir_combinar(t, SABER)
    return r["valor"] if r["conclusion"] == "hecho" else r["conclusion"]


# ---------------------------------------------------------------- EL TESTIGO

class _Bajo(Exception):
    pass


def testigo(texto):
    """El valor con Fraction, en el orden de siempre; 'todavia_no' si por el camino se baja de cero (de
    izquierda a derecha, como lo hace el sistema)."""
    toks = texto.replace("(", " ( ").replace(")", " ) ").split()
    pos = [0]

    def ver():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def tomar():
        pos[0] += 1
        return toks[pos[0] - 1]

    def factor():
        t = tomar()
        if t == "(":
            v = expr()
            tomar()
            return v
        return Fraction(t)

    def term():
        v = factor()
        while ver() == "x":
            tomar()
            v = v * factor()
        return v

    def expr():
        v = term()
        while ver() in ("+", "-"):
            op = tomar()
            w = term()
            v = v + w if op == "+" else v - w
            if v < 0:
                raise _Bajo()
        return v

    try:
        v = expr()
    except _Bajo:
        return "todavia_no"
    if v.denominator == 1:
        return str(v.numerator)
    d = format(float(v), ".3f").rstrip("0").rstrip(".")
    return d


def T(texto):
    v = testigo(texto)
    if v != "todavia_no" and "." not in v and int(v) > 1000000:
        return "no_alcanza"
    return v


print("=" * 78)
print("PRUEBAS DEL PASO M.16: COMBINAR LA x CON LA + Y LA - (NCETM 2.22; 5.OA.A.1)")
print("=" * 78)
try:
    motor.aprender("tablas", SABER)          # en 5.o las tablas ya se saben (M.13 las pide para los decimales)
    print("\nA - LAS TRAMPAS DEL PLAN")
    for texto, esperado in (("3 + 4 x 5", "23"), ("20 - 3 x 4", "8"), ("(3 + 4) x 5", "35"),
                            ("10 - 3 + 2", "9"), ("4 x 6 + 4 x 2", "32"), ("7 x 5 - 7 x 3", "14"),
                            ("5 x 4 + 5", "25"), ("calcular: 3 + 4 x 5", "23"),
                            ("verdad: 3 + 4 x 5 = 35", "falso"), ("verdad: 3 + 4 x 5 = 23", "verdadero"),
                            ("3 + 4 x 5 = 23", "verdadero"), ("(3 + 4) x 5 = 35", "verdadero"),
                            ("verdad: 4 x 6 + 4 x 2 = 4 x 8", "verdadero"),
                            ("verdad: 4 x 6 + 4 x 2 = 8 x 8", "falso"),
                            ("2 x 3 - 4 x 5", "todavia_no"), ("12 : 3 + 1", "todavia_no"),
                            ("0.5 x 4 + 1.25", "3.25"), ("0.3 x 0.2 + 1", "todavia_no"),
                            ("999 x 1000 + 1000", "1000000"), ("999 x 1000 + 1001", "no_alcanza"),
                            ("1000 x 1000 - 1", "999999"), ("combinar: 17 x 6 + 3 x 6", "120"),
                            ("[2 + 3] x 4", "20"), ("2,5 x 4 + 1", "11"), ("3 × 4 − 2", "10"),
                            ("2 + 3 -", "no_entiendo"), ("1.2345 + 1 x 2", "todavia_no"),
                            ("2000000 + 1 x 2", "no_alcanza"), ("((2 + 3) x 2 + 1) x 3", "33")):
        comprobar("A %s -> %s" % (texto, esperado), S(texto), esperado)

    print("\nB - LO QUE SE ENSENA (la explicacion)")
    e = motor.explicar_pregunta("3 + 4 x 5", SABER)
    comprobar("B 3 + 4 x 5 rodea la multiplicacion", "3 + «4 x 5»" in e, True)
    comprobar("B ... y dice que de izquierda a derecha saldria 35 (MAL)", "saldria 35" in e, True)
    comprobar("B ... y se comprueba con la contraria", "COMPRUEBO" in e and "20 : 4 = 5" in e, True)
    e = motor.explicar_pregunta("10 - 3 + 2", SABER)
    comprobar("B 10 - 3 + 2: la suma NO va antes que la resta (10 - (3 + 2) = 5)", "10 - (3 + 2) = 5" in e, True)
    e = motor.explicar_pregunta("4 x 6 + 4 x 2", SABER)
    comprobar("B 4 x 6 + 4 x 2: saca el factor comun, 4 x (6 + 2)", "4 x (6 + 2)" in e, True)
    comprobar("B ... no es (4 + 4) x (6 + 2) = 64", "(4 + 4) x (6 + 2) = 64" in e, True)
    comprobar("B ... y en el orden de siempre sale LO MISMO", "LO MISMO" in e, True)
    comprobar("B ... y se comprueba: 32 : 4 = 8, 8 - 2 = 6", "32 : 4 = 8, 8 - 2 = 6" in e, True)
    e = motor.explicar_pregunta("(3 + 4) x 5", SABER)
    comprobar("B (3 + 4) x 5: primero el parentesis", "3 + 4 = 7   <- dentro del parentesis" in e, True)

    print("\nC - EL ORDEN DE SIEMPRE: ocho formas, contra el testigo")
    azar = random.Random(22)
    chicos = list(range(0, 13))
    grandes = [15, 25, 37, 99, 100, 125, 250, 999]
    formas = ["%d + %d x %d", "%d - %d x %d", "%d x %d + %d", "%d x %d - %d", "( %d + %d ) x %d",
              "%d x ( %d - %d )", "%d x %d + %d x %d", "%d x %d - %d x %d"]
    for forma in formas:
        k = forma.count("%d")
        malos, n, nunca_falso = [], 0, True
        for _ in range(45):
            ns = tuple(azar.choice(chicos if azar.random() < 0.75 else grandes) for _ in range(k))
            texto = (forma % ns).replace("( ", "(").replace(" )", ")")
            obtenido, esperado = D(texto), T(forma % ns)
            n += 1
            if obtenido != esperado:
                malos.append((texto, obtenido, esperado))
        comprobar("C %-20s %d cuentas" % (forma.replace("%d", "a"), n), malos, [])

    print("\nD - EL FACTOR COMUN en todos los sitios (a x b + a x c, b x a + c x a, ... y con un numero suelto)")
    malos, no_usada = [], []
    for a in (2, 3, 4, 6, 7, 9, 12, 25):
        for b, c in ((6, 2), (5, 3), (17, 3), (8, 8), (11, 1)):
            for forma in ("%d x %d + %d x %d", "%d x %d - %d x %d"):
                for orden in ((a, b, a, c), (b, a, c, a), (a, b, c, a), (b, a, a, c)):
                    texto = forma % orden
                    r = motor.decidir_combinar(texto, SABER)
                    esp = T(texto)
                    v = r["valor"] if r["conclusion"] == "hecho" else r["conclusion"]
                    if v != esp:
                        malos.append((texto, v, esp))
                    elif r["conclusion"] == "hecho" and r["pieza"] != "combinar_sacando_el_factor_comun":
                        no_usada.append(texto)
        for texto in ("%d x 5 + %d" % (a, a), "%d + 5 x %d" % (a, a), "%d x 5 - %d" % (a, a)):
            r = motor.decidir_combinar(texto, SABER)
            if r.get("valor") != T(texto):
                malos.append((texto, r.get("valor"), T(texto)))
            elif r["pieza"] != "combinar_sacando_el_factor_comun":
                no_usada.append(texto)
    comprobar("D 344 cuentas con factor comun dan lo del testigo", malos, [])
    comprobar("D ... y todas se hacen sacando el factor comun", no_usada, [])
    sin = [t for t in ("4 x 6 + 3 x 2", "0 x 5 + 0 x 3", "1.5 x 3 + 1.5 x 5", "4 x 6 + 4 x 2 + 1", "(4 x 6) + 4 x 2")
           if motor.decidir_combinar(t, SABER).get("pieza") == "combinar_sacando_el_factor_comun"]
    comprobar("D sin factor comun entero (o tres terminos, o un parentesis), el orden de siempre", sin, [])
    comprobar("D 3 x 1.5 + 3 x 2.5 = 3 x 4 = 12 (el factor comun es entero)", D("3 x 1.5 + 3 x 2.5"), "12")

    print("\nE - SUMAS Y RESTAS SEGUIDAS: de izquierda a derecha")
    malos = []
    for _ in range(80):
        k = azar.randint(3, 5)
        ns = [azar.randint(0, 200) for _ in range(k)]
        texto = " ".join("%d" % ns[0] if i == 0 else "%s %d" % (azar.choice("+-"), x) for i, x in enumerate(ns))
        if D(texto) != T(texto):
            malos.append((texto, D(texto), T(texto)))
    comprobar("E 80 cadenas de 3 a 5 numeros", malos, [])

    print("\nF - CON DECIMALES (una, dos y tres cifras detras del punto)")
    malos, techo = [], 0

    def en_pequenas_pasa(texto):
        """El techo de M.13: la cuenta de enteros que dice que no le sale (el decimal contado en sus unidades
        mas pequenas, por el entero) de verdad pasa del millon (el testigo la multiplica)."""
        r = motor.decidir_combinar(texto, SABER)
        m = re.search(r"la cuenta de enteros (\d+) x (\d+) no me sale", r.get("porque", ""))
        return r["conclusion"] == "todavia_no" and m is not None and int(m.group(1)) * int(m.group(2)) > 1000000

    for _ in range(60):
        x = "%d.%s" % (azar.randint(0, 99), "".join(str(azar.randint(0, 9)) for _ in range(azar.randint(1, 3))))
        y = "%d.%s" % (azar.randint(0, 99), "".join(str(azar.randint(0, 9)) for _ in range(azar.randint(1, 3))))
        m = azar.randint(1, 9)
        for texto in ("%s x %d + %s" % (x, m, y), "%s + %d x %s" % (y, m, x), "(%s + %s) x %d" % (x, y, m),
                      "%d x %s - %s" % (m, x, y)):
            if D(texto) != T(texto):
                if en_pequenas_pasa(texto):
                    techo += 1
                else:
                    malos.append((texto, D(texto), T(texto)))
    comprobar("F 240 cuentas con decimales (%d dicen todavia_no: contadas en milesimas pasan del millon, "
              "el techo de M.13)" % techo, malos, [])
    comprobar("F 0.125 x 8 + 0.875 = 1.875", D("0.125 x 8 + 0.875"), "1.875")
    comprobar("F 9.999 + 0.001 x 1 = 10", D("9.999 + 0.001 x 1"), "10")
    comprobar("F 2.5 x 12 + 1 -> todavia_no (un decimal por un entero de dos cifras, M.13)", D("2.5 x 12 + 1"),
              "todavia_no")

    print("\nG - VERDAD: con cuentas combinadas")
    malos = []
    for _ in range(40):
        a, b, c = azar.randint(0, 12), azar.randint(0, 12), azar.randint(0, 12)
        texto = "%d + %d x %d" % (a, b, c)
        bueno = T(texto)
        for otro, esp in ((bueno, "verdadero"), (str((a + b) * c), "verdadero" if str((a + b) * c) == bueno else "falso")):
            if S("verdad: %s = %s" % (texto, otro)) != esp:
                malos.append((texto, otro))
    comprobar("G 80 igualdades (la buena y la de izquierda a derecha)", malos, [])

    print("\nH - CADA PIEZA SE COMPRUEBA DE VERDAD (si una cuenta sale mal, la vuelta lo caza)")
    base = motor.cargar_piezas()

    def modulo(nombre):
        sp = importlib.util.spec_from_file_location(nombre, os.path.join(RAIZ, "conocimiento", "piezas",
                                                                         nombre + ".py"))
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        return m

    class Tramposo:
        """Lo que se le da a la pieza, pero la multiplicacion da UNO DE MAS."""

        def __init__(self, real):
            self._real = real

        def __getattr__(self, k):
            return getattr(self._real, k)

        def usar(self, nombre, **sit):
            r = self._real.usar(nombre, **sit)
            if nombre == "multiplicar":
                r = dict(r)
                r["valor"] = r["valor"] + 1
            return r

    for nombre, texto in (("combinar_en_el_orden_de_siempre", "3 + 4 x 5"),
                          ("combinar_sacando_el_factor_comun", "4 x 6 + 4 x 2")):
        pieza = base["piezas"][nombre]
        m = modulo(nombre)
        arbol = motor.decidir_combinar(texto, SABER)["arbol"]
        u = motor._Lo_que_puede_usar(pieza, base, SABER)
        bien = m.hacer({"terminos": arbol}, u)
        comprobar("H %s: %s = %s y su vuelta cuadra" % (nombre, texto, bien["valor"]),
                  (bien["vuelta_ok"], bool(bien["vuelta"])), (True, True))
        try:
            mal = m.hacer({"terminos": arbol}, Tramposo(u))
            cazado = mal["vuelta_ok"] is False
        except ValueError:
            cazado = True
        comprobar("H %s: con una multiplicacion mal, la vuelta NO cuadra" % nombre, cazado, True)
    mapa = motor.mapa_del_conocimiento()
    comprobar("H ninguna pieza usa 'combinar' (no hay vuelta en el mapa)",
              [p for p, usa in mapa.items() if "combinar" in usa], [])

    print("\nI - LO DE ANTES SIGUE IGUAL (no se lo come la orden nueva)")
    for texto, esperado in (("calcular: 47 + 30", "77"), ("2 x 3 x 4", "24"), ("3 x 4 - 5 = c", "7"),
                            ("2 + 3 x 4 = n", "14"), ("(2 + 3) x 4 = n", "20"),
                            ("verdad: 3 x 12 = 4 x 11", "falso"), ("volumen: 5 x 3 x 2 + 4 x 4 x 1", "46 unidades cubicas"),
                            ("8 + 3 = 11", "verdadero"), ("3 x 4", "12")):
        comprobar("I %s -> %s" % (texto, esperado), S(texto), esperado)
    comprobar("I 'combinar' es una pregunta de las piezas", "combinar" in base["objetivos"], True)

    print("\nJ - CERCA DEL TECHO, y el TIEMPO (cada pregunta, con su explicacion, en menos de 2 s)")
    for texto in ("999 x 1000 + 1000", "1000 x 1000 - 1", "999 x 999 + 1998", "999 x 999 + 1999",
                  "(999 + 1) x (999 + 1)", "123 x 456 + 789 x 12", "500000 + 500000 - 1 x 0",
                  "999.999 + 0.001 x 1", "12 x 13 + 12 x 7", "3 x (18932 + 921)", "7 + 8 x 9 - 6 x 5 + 4 x 3 x 2"):
        t1 = time.time()
        r = S(texto)
        dt = time.time() - t1
        comprobar("J %s -> %s (%.2f s)" % (texto, T(texto), dt), (r, dt < 2), (T(texto), True))
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\nTOTAL: %d/%d" % (BIEN, BIEN + MAL))
