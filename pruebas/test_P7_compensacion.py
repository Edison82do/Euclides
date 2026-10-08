# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO P.7: USAR LA EQUIVALENCIA Y LA COMPENSACION PARA CALCULAR, con + y - (NCETM 1.29).
El plan y sus trampas: diario/2026-10-07-paso-P7-compensacion.md
Python solo aparece aqui como TESTIGO externo (las cuentas con +, -, Fraction).
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
TMP = tempfile.mkdtemp(prefix="p7_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria propia y vacia
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
AZAR = random.Random(129)
REDONDOS = [100, 200, 500, 1000, 3000, 5000, 10000, 40000, 100000, 300000]
CERCA = [-3, -2, -1, 1, 2, 3]


def S(t):
    return probar.preguntar(probar.como_problema(t), SABER)[0]


def A(pregunta, **sit):
    r = motor.aplicar(pregunta, sit, SABER)
    return (r["valor"] if r["conclusion"] == "hecho" else r["conclusion"]), r.get("pieza", {}).get("id")


def cerca_de_un_redondo():
    return AZAR.choice(REDONDOS) + AZAR.choice(CERCA)


def txt(f):
    if f.denominator == 1:
        return str(f.numerator)
    return ("%.6f" % float(f)).rstrip("0").rstrip(".")


try:
    print("A - LA MISMA SUMA (punto 1) y REDONDEAR UN SUMANDO (punto 2): contra el testigo")
    malos, por_p7 = [], 0
    for _ in range(150):
        x = cerca_de_un_redondo()
        o = AZAR.randint(4, 300000)
        a, b = (x, o) if AZAR.random() < 0.5 else (o, x)
        v, p = A("sumar", a=a, b=b)
        if v != a + b:
            malos.append((a, b, v))
        if p in ("sumar_misma_suma", "sumar_redondeando_y_quitando"):
            por_p7 += 1
    comprobar("A1 150 sumas con un sumando a 1, 2 o 3 de un redondo: todas bien", malos, [])
    comprobar("A2 y todas por la compensacion de P.7 (%d)" % por_p7, por_p7, 150)
    comprobar("A3 4997 + 2456 = 7453 por la misma suma", A("sumar", a=4997, b=2456), (7453, "sumar_misma_suma"))
    comprobar("A4 4997 + 2: al 2 no se le pueden quitar 3 -> redondear y quitar (punto 2): 4999",
              A("sumar", a=4997, b=2), (4999, "sumar_redondeando_y_quitando"))
    comprobar("A5 1003 + 245: el 1003 se pasa 3 -> 1000 + 248", A("sumar", a=1003, b=245), (1248, "sumar_misma_suma"))
    comprobar("A6 29 + 14 sigue por P.4 (es mas corto)", A("sumar", a=29, b=14), (43, "sumar_compensando"))
    comprobar("A7 345 + 123: ninguno cerca de un redondo -> las columnas", A("sumar", a=345, b=123),
              (468, "sumar_por_columnas"))
    comprobar("A8 la cadena: 4997 + 2456 = 5000 + 2453",
              motor.aplicar("sumar", {"a": 4997, "b": 2456}, SABER)["resultado"]["cadena"],
              [[4997, "+", 2456], [5000, "+", 2453]])

    print("\nB - LA MISMA DIFERENCIA (punto 3) y QUITAR DE MAS Y DEVOLVER (punto 5): contra el testigo")
    malos, por_p7 = [], 0
    for _ in range(150):
        b = cerca_de_un_redondo()
        a = AZAR.randint(b, 999999)
        v, p = A("restar", a=a, b=b)
        if v != a - b:
            malos.append((a, b, v))
        if p in ("restar_misma_diferencia", "restar_quitando_de_mas_y_devolviendo"):
            por_p7 += 1
    comprobar("B1 150 restas con el sustraendo a 1, 2 o 3 de un redondo: todas bien", malos, [])
    comprobar("B2 y todas por la compensacion de P.7 (%d)" % por_p7, por_p7, 150)
    comprobar("B3 1000 - 397 = 1003 - 400 = 603", A("restar", a=1000, b=397), (603, "restar_misma_diferencia"))
    comprobar("B4 1000 - 403 = 997 - 400 = 597", A("restar", a=1000, b=403), (597, "restar_misma_diferencia"))
    comprobar("B5 625 - 398 = 227", A("restar", a=625, b=398), (227, "restar_misma_diferencia"))
    # antes (techo en un millon): 999999 - 997, la misma diferencia pasaria del millon.  N.6: lo mismo en diez millones
    r = motor.aplicar("restar", {"a": 9999999, "b": 997}, SABER)
    comprobar("B6 9999999 - 997: la misma diferencia pasaria de diez millones -> quitar 1000 y devolver 3: 9999002",
              (r["valor"], r["pieza"]["id"], [c.get("no_salio", "")[-26:] for c in r["candidatos"]
                                              if c["id"] == "restar_misma_diferencia"]),
              (9999002, "restar_quitando_de_mas_y_devolviendo", ["se sale de mi lista (pasaria del techo)"[-26:]]))
    comprobar("B7 398 - 397: no llega a 400 para quitar de mas, pero la misma diferencia si: 1",
              A("restar", a=398, b=397)[0], 1)
    comprobar("B8 52 - 29 sigue por P.4", A("restar", a=52, b=29), (23, "restar_compensando"))
    comprobar("B9 397 - 1000: se quitaria mas de lo que hay", A("restar", a=397, b=1000)[0], "imposible")

    print("\nC - DERIVAR DE UN HECHO QUE SE SABE (puntos 2, 4 y 5): contra el testigo")
    for texto, esperado in (("si 600 - 200 = 400: 600 - 201 = ?", "399"),      # LA trampa: no 401
                            ("si 600 - 200 = 400: 601 - 200 = ?", "401"),
                            ("si 600 - 200 = 400: 599 - 200 = ?", "399"),
                            ("si 600 - 200 = 400: 600 - 199 = ?", "401"),
                            ("si 250 + 250 = 500: 251 + 250 = ?", "501"),
                            ("si 250 + 250 = 500: 250 + 249 = ?", "499"),
                            ("si 250 + 250 = 500: 260 + 240 = ?", "500"),
                            ("si 3400 + 2600 = 6000: 3420 + 2580 = ?", "6000"),
                            ("si 600 - 200 = 500: 600 - 201 = ?", "hecho_falso"),
                            ("si 5 - 3 = 2: 5 - 8 = ?", "no_se_puede"),
                            ("si 5 - 8 = 2: 5 - 3 = ?", "hecho_falso")):
        comprobar("C %s -> %s" % (texto, esperado), S(texto), esperado)
    salida = motor.explicar_orden_derivar("si 600 - 200 = 400: 600 - 201 = ?", SABER)
    comprobar("C dice la trampa del punto 5 (401 NO) y usa el hecho, no la cuenta entera",
              ("401 NO" in salida, "[SI]  mover el resultado que se sabe" in salida), (True, True))
    malos, por_p7 = [], 0
    for _ in range(80):
        op = AZAR.choice("+-")
        a = AZAR.randint(100, 400000)
        b = AZAR.randint(10, a) if op == "-" else AZAR.randint(10, 400000)
        r0 = a + b if op == "+" else a - b
        cambios = [0, 1, 2, 3, -1, -2, -3, 10, -10, 20, 100, -100]
        c, d = a + AZAR.choice(cambios), b + AZAR.choice(cambios)
        nuevo = c + d if op == "+" else c - d
        if c < 0 or d < 0 or nuevo < 0:
            continue
        r = motor.aplicar("derivar", {"hecho": {"a": a, "op": op, "b": b, "r": r0},
                                      "nuevo": {"a": c, "op": op, "b": d}}, SABER)
        if r.get("valor") != nuevo:
            malos.append((a, op, b, c, d, r.get("valor")))
        if r.get("pieza", {}).get("id") == "derivar_compensando":
            por_p7 += 1
    comprobar("C %d derivaciones al azar fijo: todas bien" % por_p7, malos, [])
    comprobar("C y todas moviendo el resultado que se sabe", por_p7 > 70, True)

    print("\nD - VER LA IGUALDAD SIN CALCULAR (puntos 1 y 3, y sus trampas): contra el testigo")
    for texto, esperado in (("verdad: 75 - 28 = 77 - 30", "verdadero"), ("verdad: 75 - 28 = 73 - 30", "falso"),
                            ("verdad: 250 + 250 = 260 + 240", "verdadero"), ("verdad: 250 + 250 = 260 + 260", "falso"),
                            ("verdad: 250 + 250 = 240 + 260", "verdadero"), ("verdad: 1000 - 397 = 1003 - 400", "verdadero"),
                            ("verdad: 1000 - 397 = 997 - 400", "falso"), ("verdad: 4997 + 2456 = 5000 + 2453", "verdadero")):
        comprobar("D %s -> %s" % (texto, esperado), S(texto), esperado)
    malos = []
    por_p7 = 0
    for _ in range(100):
        op = AZAR.choice("+-")
        a = AZAR.randint(50, 500000)
        b = AZAR.randint(20, a) if op == "-" else AZAR.randint(20, 400000)
        da = AZAR.choice([1, 2, 3, 5, 10, 20, 100, 0])
        db = da if AZAR.random() < 0.5 else AZAR.choice([1, 2, 3, 10, 30, 0])
        sa, sb = AZAR.choice([1, -1]), AZAR.choice([1, -1])
        c, d = a + sa * da, b + sb * db
        if c < 0 or d < 0 or (op == "-" and d > c):
            continue
        izq = {"texto": "%d %s %d" % (a, op, b), "a": a, "op": op, "b": b}
        der = {"texto": "%d %s %d" % (c, op, d), "a": c, "op": op, "b": d}
        r = motor.aplicar("igualdad", {"lados": [izq, der]}, SABER)
        testigo = "verdadero" if (a + b if op == "+" else a - b) == (c + d if op == "+" else c - d) else "falso"
        if r.get("valor") != testigo:
            malos.append((izq["texto"], der["texto"], r.get("valor")))
        if r.get("pieza", {}).get("id") == "igual_compensando":
            por_p7 += 1
    comprobar("D %d igualdades al azar fijo (verdaderas y falsas): todas bien" % por_p7, malos, [])
    comprobar("D y casi todas sin calcular los lados", por_p7 > 70, True)

    print("\nE - LA BALANZA CON DOS RESTAS (punto 6): contra el testigo")
    for texto, esperado in (("74 - 28 = 75 - ?", "29"), ("50 - 19 = ? - 20", "51"), ("1000 - 397 = 1003 - ?", "400"),
                            ("1000 - 397 = ? - 400", "1003"), ("74 - 28 = 72 - ?", "26"), ("5 - 3 = 2 - ?", "0"),
                            ("5 - 3 = 1 - ?", "imposible")):
        comprobar("E %s -> %s" % (texto, esperado), S(texto), esperado)
    salida = motor.explicar_pregunta("ecuacion: 74 - 28 = 75 - ?", SABER)
    comprobar("E dice la trampa: 27 NO (compensar al reves, como en la suma)",
              "27 NO (compensar al reves" in salida, True)
    malos = []
    for _ in range(80):
        a = AZAR.randint(30, 900000)
        b = AZAR.randint(10, a)
        k = AZAR.choice([1, 2, 3, -1, -2, 10, 100, -100])
        if AZAR.random() < 0.5:
            c = a + k
            if c < 0 or b + k < 0:
                continue
            texto, testigo = "%d - %d = %d - ?" % (a, b, c), b + k
        else:
            e = b + k
            if e < 0 or a + k < 0:
                continue
            texto, testigo = "%d - %d = ? - %d" % (a, b, e), a + k
        if S(texto) != str(testigo):
            malos.append((texto, testigo, S(texto)))
    comprobar("E 80 balanzas de restas al azar fijo: todas bien", malos, [])

    print("\nF - CON DECIMALES (D.1, D.2): contra el testigo")
    for texto, esperado in (("equivalente: 7.2 - 3.9", "3.3"), ("equivalente: 2.98 + 1.45", "4.43"),
                            ("equivalente: 5.003 - 1.998", "3.005"), ("equivalente: 4.997 + 0.25", "5.247"),
                            ("equivalente: 10 - 0.997", "9.003"), ("equivalente: 1000 - 397", "603"),
                            ("equivalente: 4997 + 2456", "7453"), ("equivalente: 345 + 123", "no_encaja"),
                            ("equivalente: 1.2345 - 0.999", "todavia_no"), ("equivalente: 3.9 - 7.2", "no_se_puede")):
        comprobar("F %s -> %s" % (texto, esperado), S(texto), esperado)
    salida = motor.explicar_orden_equivalente("equivalente: 7.2 - 3.9", SABER)
    comprobar("F 7.2 - 3.9 = 7.3 - 4 (la cadena) y lo comprueba sumando",
              ("= 7.3 - 4" in salida, "COMPRUEBO sumando: 3.3 + 3.9 = 7.2 ... SI" in salida), (True, True))
    malos = []
    for _ in range(60):
        k = AZAR.choice([1, 2, 3])
        uno = Fraction(1, 10 ** k)
        R = AZAR.choice([1, 2, 5, 10, 40])
        x = Fraction(R) + AZAR.choice(CERCA) * uno
        o = Fraction(AZAR.randint(1, 50000), 10 ** k)
        op = AZAR.choice("+-")
        if op == "-":
            a, b = (o + x, x) if AZAR.random() < 0.5 else (x + o, x)
            texto, testigo = "equivalente: %s - %s" % (txt(a), txt(b)), a - b
        else:
            texto, testigo = "equivalente: %s + %s" % (txt(x), txt(o)), x + o
        if S(texto) != txt(testigo):
            malos.append((texto, txt(testigo), S(texto)))
    comprobar("F 60 cuentas con decimales de 1 a 3 cifras: todas bien", malos, [])

    print("\nG - CADA PIEZA SE COMPRUEBA DE VERDAD (si una cuenta sale mal, la vuelta lo caza)")
    base = motor.cargar_piezas()

    def modulo(nombre):
        sp = importlib.util.spec_from_file_location(nombre, os.path.join(RAIZ, "conocimiento", "piezas",
                                                                         nombre + ".py"))
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        return m

    class Tramposo:
        """Lo que se le da a la pieza, pero la cuenta que se le pide da UNO DE MAS (la vez 'cual_vez')."""

        def __init__(self, real, cual):
            cual, self._vez = (cual, 1) if isinstance(cual, str) else cual
            self._real, self._cual, self._hecho = real, cual, False
            if cual == "contar_adelante":                      # contar se 'salta' un numero, siempre
                def contar(a, b, con_dedos=True):
                    r = dict(real.contar_adelante(a, b, con_dedos))
                    if r.get("resultado"):
                        r["resultado"] = real.siguiente(r["resultado"])
                    return r
                self.contar_adelante = contar

        def __getattr__(self, k):
            return getattr(self._real, k)

        def usar(self, nombre, **sit):
            r = self._real.usar(nombre, **sit)
            if nombre == self._cual and not self._hecho:
                self._vez -= 1
            if nombre == self._cual and not self._hecho and self._vez == 0:
                self._hecho = True
                r = dict(r)
                r["valor"] = r["valor"] + 1
            return r

    lados = lambda a, op, b: {"texto": "%d %s %d" % (a, op, b), "a": a, "op": op, "b": b}  # noqa: E731
    for nombre, sit, cual in (
            ("buscar_el_redondo_cercano", {"n": 997}, "contar_adelante"),
            ("sumar_misma_suma", {"a": 4997, "b": 2456}, "sumar_por_columnas"),
            ("sumar_redondeando_y_quitando", {"a": 4997, "b": 2}, "sumar_por_columnas"),
            ("restar_misma_diferencia", {"a": 1000, "b": 397}, "restar_por_columnas"),
            ("restar_quitando_de_mas_y_devolviendo", {"a": 625, "b": 398}, "restar_por_columnas"),
            ("igual_compensando", {"lados": [lados(75, "-", 28), lados(77, "-", 30)]},
             ("restar_por_columnas", 3)),            # las dos primeras solo miran si el cambio es facil
            ("balanza_misma_diferencia", {"completo": {"a": 74, "op": "-", "b": 28},
                                          "con_hueco": {"a": 75, "op": "-", "b": "?"}}, "sumar"),
            ("balanza_compensando", {"completo": {"a": 34, "op": "+", "b": 26},
                                     "con_hueco": {"a": 33, "op": "+", "b": "?"}}, "sumar"),
            ("derivar_compensando", {"hecho": {"a": 600, "op": "-", "b": 200, "r": 400},
                                     "nuevo": {"a": 600, "op": "-", "b": 201}}, "restar"),
            ("derivar_calculando", {"nuevo": {"a": 600, "op": "-", "b": 201}}, "restar")):
        pieza = base["piezas"][nombre]
        m = modulo(nombre)
        u = motor._Lo_que_puede_usar(pieza, base, SABER)
        bien = m.hacer(sit, u)
        comprobar("G %s = %s y su vuelta cuadra (%s)" % (nombre, bien["valor"], bien["vuelta"]),
                  (bien["vuelta_ok"], bool(bien["vuelta"])), (True, True))
        try:
            mal = m.hacer(sit, Tramposo(u, cual))
            cazado = mal["vuelta_ok"] is False
        except (ValueError, motor.NoSalio):
            cazado = True
        comprobar("G %s: con '%s' dando uno de mas, la vuelta NO cuadra" % (nombre, str(cual)), cazado, True)
    mapa = motor.mapa_del_conocimiento()
    comprobar("G ninguna pieza usa su propia pregunta",
              [p for p, usa in mapa.items() if base["piezas"][p]["responde"] in usa], [])
    comprobar("G las piezas cargan sin problemas", base["problemas"], [])

    print("\nH - LO DE ANTES SIGUE IGUAL")
    for texto, esperado in (("34 + 26 = 33 + ?", "27"), ("8 + 4 = ? + 5", "7"), ("verdad: 3 x 12 = 6 x 6", "verdadero"),
                            ("verdad: 3 x 12 = 4 x 11", "falso"), ("equivalente: 25 x 16", "400"),
                            ("equivalente: 375 : 25", "15"), ("7.2 - 3.9", "3.3"), ("calcular: 47 + 30", "77"),
                            ("verdad: 4 + 1 = 5 + 2", "falso"), ("37 + ? + 25 = 100", "38")):
        comprobar("H %s -> %s" % (texto, esperado), S(texto), esperado)

    print("\nI - CERCA DEL TECHO, y el TIEMPO (cada pregunta, con su explicacion, en menos de 2 s)")
    for texto, esperado in (("999997 + 3", "1000000"), ("999997 + 5", "1000002"), ("9999997 + 5", "ninguna"),   # N.6: antes 999997 + 5 -> ninguna
                            ("999999 - 997", "999002"), ("1000000 - 999997", "3"),
                            ("1000000 - 3", "999997"), ("equivalente: 999999 - 997", "999002"),
                            ("si 999999 - 1 = 999998: 1000000 - 1 = ?", "999999"),
                            ("si 500000 + 499999 = 999999: 500000 + 500000 = ?", "1000000"),
                            ("verdad: 999999 - 997 = 1000000 - 998", "verdadero"),
                            ("999999 - 997 = 1000000 - ?", "998"),
                            ("equivalente: 999.997 + 0.003", "1000"),
                            ("equivalente: 999999.999 - 0.998", "no_alcanza")):
        t1 = time.time()
        r = S(texto)
        dt = time.time() - t1
        comprobar("I %s -> %s (%.2f s)" % (texto, esperado, dt), (r, dt < 2), (esperado, True))
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\nTOTAL: %d/%d" % (BIEN, BIEN + MAL))
