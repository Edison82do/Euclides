# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO F.6: FRACCIONES EQUIVALENTES Y SIMPLIFICAR (NCETM 3.7; 4.NF.A.1).
El plan y sus trampas: diario/2026-10-08-paso-F6-fracciones-equivalentes.md
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
TMP = tempfile.mkdtemp(prefix="f6_")
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
AZAR = random.Random(37)


def S(t):
    return probar.preguntar(probar.como_problema(t), SABER)[0]


def testigo(a, b):
    """la forma mas simple, escrita como la escribe Euclides (3/1 -> '3')."""
    f = Fraction(a, b)
    return str(f.numerator) if f.denominator == 1 else "%d/%d" % (f.numerator, f.denominator)


def simplificar(a, b, pieza="simplificar_fraccion"):
    r = motor.aplicar(pieza, {"a": a, "b": b}, SABER)
    return r.get("valor") if r["conclusion"] == "hecho" else r["conclusion"]


try:
    print("=" * 78)
    print("PASO F.6 - FRACCIONES EQUIVALENTES Y SIMPLIFICAR")
    print("=" * 78)
    motor.aprender("tablas", SABER)          # en 5.o las tablas ya se saben (la division corta las pide)

    print("\nA - LAS TRAMPAS DEL PLAN")
    for texto, esperado, porque in (
            ("equivalentes: 2/3 y 3/4", "no", "sumar 1 arriba y abajo no es multiplicar"),
            ("comparar: 3/12 y 1/4", "3/12 = 1/4", "no 'mayor porque sus numeros son mayores'"),
            ("equivalentes: 2/3 y 4/9", "no", "arriba x 2 y abajo x 3"),
            ("simplificar: 3/4", "3/4", "ya es la mas simple (no solo las unitarias)"),
            ("simplificar: 12/18", "2/3", "no se queda en 6/9"),
            ("simplificar: 26/39", "2/3", "el 13 no es de las tablas"),
            ("4/6 = ?/9", "6", "ni horizontal ni vertical: simplificar primero"),
            ("2/3 = ?/10", "no_sale", "no hay entero"),
            ("4/12 = 5/?", "15", "la relacion vertical"),
            ("2/3 = ?/12", "8", "la relacion horizontal"),
            ("12/18 = 2/?", "3", "horizontal dividiendo"),
            ("?/15 = 4/5", "12", "el hueco a la izquierda"),
            ("simplificar: 12/4", "3", "una impropia que es un entero"),
            ("simplificar: 0/5", "0", "cero"), ("simplificar: 5/0", "imposible", "cero partes"),
            ("2/0 = ?/4", "imposible", "cero partes"), ("0/5 = ?/7", "0", "cero"),
            ("2/3 = 8/12", "verdadero", "sin hueco: verdadero o falso"), ("verdad: 2/3 = 3/4", "falso", "la aditiva"),
            ("equivalentes: 3/12 y 1/4", "si", "la del audit")):
        comprobar("A %s -> %s (%s)" % (texto, esperado, porque), S(texto), esperado)
    t = motor.explicar_pregunta("equivalentes: 2/3 y 3/4", SABER)
    comprobar("A la trampa aditiva se dice", "sumar lo mismo NO da una equivalente" in t, True)
    t = motor.explicar_pregunta("equivalentes: 2/3 y 4/9", SABER)
    comprobar("A la trampa de 'distinto numero' se dice", "no es el MISMO numero" in t, True)
    t = motor.explicar_pregunta("comparar: 3/12 y 1/4", SABER)
    comprobar("A comparar 3/12 y 1/4 dice que sus numeros mas grandes no la hacen mayor", "no la hace mayor" in t, True)
    t = motor.explicar_pregunta("simplificar: 3/4", SABER)
    comprobar("A simplificar 3/4 avisa: no solo las unitarias", "no solo las unitarias" in t, True)
    t = motor.explicar_pregunta("comparar: 2/3 y 3/4", SABER)
    # OBSOLETA POR MEJORA (F.7, 8 oct; NCETM 3.8). Antes: "A comparar 2/3 y 3/4 -> todavia no, y dice que es de 3.8"
    # (S(...) == "todavia_no" y "NCETM 3.8" en la explicacion).  Ahora sale con el mismo de abajo (F.7).
    comprobar("A comparar 2/3 y 3/4 -> desde F.7: 2/3 < 3/4, con el mismo de abajo",
              (S("comparar: 2/3 y 3/4"), "el mismo de abajo (F.7)" in t), ("2/3 < 3/4", True))

    print("\nB - SIMPLIFICAR, CONTRA EL TESTIGO")
    malos = [(a, b, simplificar(a, b)) for a in range(1, 25) for b in range(1, 25)
             if simplificar(a, b) != testigo(a, b)]
    comprobar("B todas las a/b con arriba y abajo de 1 a 24 (576)", malos, [])
    malos = []
    for _ in range(120):
        g, x, y = AZAR.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 20, 21, 25, 30, 35]), AZAR.randint(1, 40), \
            AZAR.randint(1, 40)
        a, b = g * x, g * y
        if simplificar(a, b) != testigo(a, b):
            malos.append((a, b, simplificar(a, b)))
    comprobar("B 120 al azar hasta 1400 (un factor comun hecho de doses, treses, cincos y sietes)", malos, [])
    malos, todavia = [], 0
    for _ in range(80):
        a, b = AZAR.randint(1, 1000), AZAR.randint(1, 1000)
        v = simplificar(a, b)
        todavia += v == "no_salio"
        if v not in (testigo(a, b), "no_salio"):
            malos.append((a, b, v))
    comprobar("B 80 al azar hasta 1000: bien o 'todavia no' (%d), NUNCA mal" % todavia, (malos, todavia < 8), ([], True))
    comprobar("B 836/722 (comparten 38 = 2 x 19): todavia no (el 19 pide la division larga)", simplificar(836, 722),
              "no_salio")
    malos = []
    for _ in range(40):
        b = AZAR.choice([1000, 10000, 100000, 1000000, 360000, 720720, 500000])
        a = AZAR.randint(1, b)
        if simplificar(a, b) not in (testigo(a, b), "no_salio"):
            malos.append((a, b, simplificar(a, b)))
    comprobar("B 40 al azar hasta el millon: bien o 'todavia no', NUNCA mal", malos, [])
    for a, b in ((500000, 1000000), (999999, 1000000), (250000, 1000000), (125, 1000), (375, 1000), (1000000, 1000000),
                 (1000000, 250000), (13, 26), (17, 51), (91, 143)):
        comprobar("B simplificar: %d/%d -> %s" % (a, b, testigo(a, b)), simplificar(a, b), testigo(a, b))
    comprobar("B 221/247 (13 x 17 y 13 x 19): todavia no (los trozos grandes pasan de 168)", simplificar(221, 247),
              "no_salio")

    print("\nC - CADA METODO DE SIMPLIFICAR, CONTRA EL TESTIGO (donde encaja)")
    for pid in ("simplificar_por_el_de_arriba", "simplificar_paso_a_paso", "simplificar_con_el_mayor_factor_comun"):
        malos, hechos = [], 0
        for _ in range(80):
            a, b = AZAR.randint(1, 168), AZAR.randint(1, 168)
            if pid == "simplificar_por_el_de_arriba" and AZAR.random() < 0.6:
                b = a * AZAR.randint(1, 9) if a * 9 <= 999 else b
            v = simplificar(a, b, pid)
            if v in ("ninguna", "no_salio"):
                continue
            hechos += 1
            if v != testigo(a, b):
                malos.append((a, b, v))
        comprobar("C %s: %d hechas, todas bien" % (pid, hechos), (malos, hechos > 10), ([], True))
    r = motor.aplicar("simplificar_fraccion", {"a": 12, "b": 18}, SABER)
    comprobar("C 12/18: elige paso a paso y dice que el mayor factor comun tambien servia",
              (r["pieza"]["id"], r.get("tambien_servian")), ("simplificar_paso_a_paso",
                                                            ["simplificar_con_el_mayor_factor_comun"]))
    r = motor.aplicar("simplificar_fraccion", {"a": 5, "b": 20}, SABER)
    comprobar("C 5/20: el pequeno cabe justo -> 1/4 de una vez", (r["pieza"]["id"], r["valor"]),
              ("simplificar_por_el_de_arriba", "1/4"))
    r = motor.aplicar("simplificar_con_el_mayor_factor_comun", {"a": 200, "b": 300}, SABER)
    comprobar("C el mayor factor comun con 200 no sale (las tablas llegan a 168): todavia no",
              r["conclusion"], "no_salio")

    print("\nD - EL HUECO, CONTRA EL TESTIGO (en las cuatro posiciones; con y sin entero)")
    malos, con, sin = [], 0, 0
    for _ in range(120):
        p, q = AZAR.randint(1, 15), AZAR.randint(1, 15)
        sitio = AZAR.randint(0, 3)
        if AZAR.random() < 0.7:                    # una que SI tiene entero (escalando la forma mas simple)
            f = Fraction(p, q)
            k = AZAR.randint(1, 12)
            conocido = (f.numerator * k) if sitio in (2, 3) else (f.denominator * k)
        else:
            conocido = AZAR.randint(1, 60)
        if sitio in (0, 1):                        # el hueco arriba:  p/q = ?/conocido  o  ?/conocido = p/q
            esperado = p * conocido / q
            texto = ("%d/%d = ?/%d" % (p, q, conocido)) if sitio == 0 else ("?/%d = %d/%d" % (conocido, p, q))
        else:                                      # el hueco abajo:   p/q = conocido/?  o  conocido/? = p/q
            esperado = q * conocido / p
            texto = ("%d/%d = %d/?" % (p, q, conocido)) if sitio == 2 else ("%d/? = %d/%d" % (conocido, p, q))
        esperado = "%d" % esperado if esperado == int(esperado) else "no_sale"
        con, sin = (con + 1, sin) if esperado != "no_sale" else (con, sin + 1)
        if S(texto) != esperado:
            malos.append((texto, esperado, S(texto)))
    comprobar("D 120 huecos (%d con entero, %d sin): todos bien" % (con, sin), (malos, con > 40, sin > 15), ([], True, True))
    for texto, esperado in (("1/2 = ?/1000000", "500000"), ("500000/1000000 = 1/?", "2"), ("3/4 = 750000/?", "1000000"),
                            ("1/3 = ?/1000000", "no_sale"), ("7/8 = ?/1000", "875"), ("6/4 = ?/2", "3")):
        comprobar("D %s -> %s" % (texto, esperado), S(texto), esperado)

    print("\nE - SON EQUIVALENTES? CONTRA EL TESTIGO (parejas que si, y trampas que no)")
    malos = []
    for _ in range(100):
        a, b = AZAR.randint(1, 20), AZAR.randint(1, 20)
        tipo = AZAR.randint(0, 3)
        if tipo == 0:                              # equivalente: los dos por el mismo
            k = AZAR.randint(2, 9)
            c, d = a * k, b * k
        elif tipo == 1:                            # la aditiva: sumar lo mismo
            k = AZAR.randint(1, 9)
            c, d = a + k, b + k
        elif tipo == 2:                            # distinto numero arriba y abajo
            k, j = AZAR.randint(2, 6), AZAR.randint(2, 6)
            c, d = a * k, b * j
        else:
            c, d = AZAR.randint(1, 60), AZAR.randint(1, 60)
        esperado = "si" if Fraction(a, b) == Fraction(c, d) else "no"
        if S("equivalentes: %d/%d y %d/%d" % (a, b, c, d)) != esperado:
            malos.append((a, b, c, d, esperado))
    comprobar("E 100 parejas (equivalentes, aditivas, distinto numero, al azar)", malos, [])
    t = motor.explicar_pregunta("equivalentes: 3/5 y 7/9", SABER)
    comprobar("E 3/5 y 7/9 (sumar 4): dice la trampa aditiva", ("sumar lo mismo NO" in t, S("equivalentes: 3/5 y 7/9")),
              (True, "no"))
    comprobar("E 0/5 y 0/7 -> si (las dos son cero)", S("equivalentes: 0/5 y 0/7"), "si")

    print("\nF - LAS FAMILIAS (cada una de la lista vale lo mismo; contra el testigo)")
    malos = []
    for a, b in ((2, 3), (1, 5), (12, 18), (3, 4), (5, 2), (7, 12), (1, 1), (9, 6), (11, 13), (500000, 1000000)):
        r = S("equivalentes: %d/%d" % (a, b))
        partes = [x.strip() for x in r.split("=")]
        if not all(Fraction(*map(int, x.split("/"))) == Fraction(a, b) for x in partes) or "%d/%d" % (a, b) not in partes:
            malos.append((a, b, r))
    comprobar("F 10 familias: todas equivalentes a la de partida", malos, [])
    comprobar("F la familia de 2/3", S("equivalentes: 2/3"), "2/3 = 4/6 = 6/9 = 8/12 = 10/15 = 12/18")
    comprobar("F la de 12/18, tambien hacia abajo", S("equivalentes: 12/18").split(" = ")[:4], ["2/3", "4/6", "6/9", "12/18"])
    t = motor.explicar_pregunta("equivalentes: 1/3", SABER)
    comprobar("F en 1/3 se dice la relacion vertical (la tabla del 3)", "la tabla del 3" in t, True)
    comprobar("F y se dibujan las tiras", "[########|oooooooo|oooooooo]" in t, True)
    comprobar("F 500000/1000000: no pasa del millon", S("equivalentes: 500000/1000000"), "1/2 = 500000/1000000")

    print("\nG - COMPARAR DOS EQUIVALENTES (no comparten arriba ni abajo)")
    malos = []
    for a, b in ((1, 2), (1, 3), (2, 3), (3, 4), (1, 4), (2, 5), (5, 6)):
        for k in (2, 3):
            if b * k <= 12:
                if S("comparar: %d/%d y %d/%d" % (a * k, b * k, a, b)) != "%d/%d = %d/%d" % (a * k, b * k, a, b):
                    malos.append((a, b, k))
    comprobar("G comparar a/b con sus equivalentes (b x k hasta 12): iguales", malos, [])
    comprobar("G lo de antes sigue: comparar 1/3 y 1/5", S("comparar: 1/3 y 1/5"), "1/3 > 1/5")
    comprobar("G lo de antes sigue: comparar 2/5 y 3/5", S("comparar: 2/5 y 3/5"), "2/5 < 3/5")

    print("\nH - CADA PIEZA SE COMPRUEBA DE VERDAD (si una cuenta sale mal, la vuelta lo caza)")
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
                    else:                                 # una fraccion: la de arriba, una de mas
                        res = dict(r["resultado"])
                        res["arriba"] = res["arriba"] + 1
                        r["valor"] = "%d/%d" % (res["arriba"], res["abajo"])
                        r["resultado"] = res
            return r

    for nombre, sit, cual, vez in (
            ("simplificar_por_el_de_arriba", {"a": 5, "b": 20}, "multiplicar", 1),
            ("simplificar_por_el_de_arriba", {"a": 5, "b": 20}, "dividir", 1),
            ("simplificar_paso_a_paso", {"a": 12, "b": 18}, "multiplicar", 2),
            ("simplificar_paso_a_paso", {"a": 375, "b": 1000}, "multiplicar", 1),
            ("simplificar_con_el_mayor_factor_comun", {"a": 12, "b": 18}, "multiplicar", 1),
            ("simplificar_con_el_mayor_factor_comun", {"a": 12, "b": 18}, "dividir", 1),
            ("hueco_por_la_relacion_horizontal", {"completa": (2, 3), "con_hueco": (None, 12)}, "multiplicar", 1),
            ("hueco_por_la_relacion_vertical", {"completa": (4, 12), "con_hueco": (5, None)}, "multiplicar", 1),
            ("hueco_simplificando_primero", {"completa": (4, 6), "con_hueco": (None, 9)}, "multiplicar", 1),
            ("hueco_simplificando_primero", {"completa": (4, 6), "con_hueco": (None, 9)}, "simplificar_fraccion", 2),
            ("fracciones_equivalentes_simplificando", {"a": (3, 12), "b": (1, 4)}, "multiplicar", 1)):
        pieza = base["piezas"][nombre]
        m = modulo(nombre)
        u = motor._Lo_que_puede_usar(pieza, base, SABER)
        bien = m.hacer(sit, u)
        comprobar("H %s = %s y su vuelta cuadra (%s)" % (nombre, bien["valor"], bien["vuelta"]),
                  (bien["vuelta_ok"], bool(bien["vuelta"])), (True, True))
        try:
            mal = m.hacer(sit, Tramposo(u, cual, vez))
            cazado = mal["vuelta_ok"] is False
        except (ValueError, motor.NoSalio):
            cazado = True
        comprobar("H %s: con '%s' (vez %d) dando uno de mas, la vuelta NO cuadra" % (nombre, cual, vez), cazado, True)
    mapa = motor.mapa_del_conocimiento()
    comprobar("H ninguna pieza usa su propia pregunta",
              [p for p, usa in mapa.items() if base["piezas"][p]["responde"] in usa], [])
    comprobar("H las piezas cargan sin problemas", base["problemas"], [])

    print("\nI - LO DE ANTES SIGUE IGUAL")
    for texto, esperado in (("3 x 2/5", "1 1/5"), ("2/7 + 3/7", "5/7"), ("3/4 de 12", "9"), ("fraccion: 3/4", "tres cuartos"),
                            ("equivalente: 25 x 16", "400"), ("equivalente: 1000 - 397", "603"), ("12 : 3", "4"),
                            ("8 + 4 = ? + 5", "7"), ("comparar: 1/3 y 2/3", "1/3 < 2/3"), ("1/4 + 1/2", "3/4")):    # antes ("1/4 + 1/2", "todavia_no"): F.7
        comprobar("I %s -> %s" % (texto, esperado), S(texto), esperado)

    print("\nJ - CERCA DEL TECHO, y el TIEMPO (cada pregunta, con su explicacion, en menos de 2 s)")
    for texto, esperado in (("simplificar: 500000/1000000", "1/2"), ("simplificar: 999999/1000000", "999999/1000000"),
                            ("simplificar: 999998/1000000", "499999/500000"), ("simplificar: 1000000/1000000", "1"),
                            ("simplificar: 1000001/2", "todavia_no"), ("equivalentes: 1/2 y 500000/1000000", "si"),
                            ("1/2 = ?/1000000", "500000"), ("equivalentes: 999999/1000000", "?"),
                            ("2/3 = ?/999999", "666666"), ("equivalentes: 1/7 y 142857/999999", "si")):
        t1 = time.time()
        r = S(texto)
        motor.explicar_pregunta(probar.como_problema(texto), SABER)
        dt = time.time() - t1
        if esperado == "?":
            esperado = r if r.startswith("999999/1000000") else "999999/1000000 ..."
        comprobar("J %s -> %s (%.2f s)" % (texto, esperado, dt), (r, dt < 2), (esperado, True))
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\nTOTAL: %d/%d" % (BIEN, BIEN + MAL))
