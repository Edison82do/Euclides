# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO N.6: HASTA DIEZ MILLONES (NCETM 1.30; curriculo ingles de Year 6).
El plan y sus trampas: diario/2026-10-08-paso-N6-diez-millones.md
Python solo aparece aqui como TESTIGO externo.
"""
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
TMP = tempfile.mkdtemp(prefix="n6_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia
import motor  # noqa: E402
import probar  # noqa: E402
from _muestras import modo  # noqa: E402

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


def A(pregunta, **sit):
    r = motor.aplicar(pregunta, sit, SABER)
    return (r.get("valor"), r["pieza"]["id"] if r.get("pieza") else r["conclusion"])


# --- el TESTIGO: los nombres en castellano, escritos aparte (otra implementacion que la del mecanismo)
U = ("cero uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciseis "
     "diecisiete dieciocho diecinueve").split()
VEINTI = {20: "veinte", 21: "veintiuno", 22: "veintidos", 23: "veintitres", 24: "veinticuatro", 25: "veinticinco",
          26: "veintiseis", 27: "veintisiete", 28: "veintiocho", 29: "veintinueve"}
D = {3: "treinta", 4: "cuarenta", 5: "cincuenta", 6: "sesenta", 7: "setenta", 8: "ochenta", 9: "noventa"}
C = {1: "ciento", 2: "doscientos", 3: "trescientos", 4: "cuatrocientos", 5: "quinientos", 6: "seiscientos",
     7: "setecientos", 8: "ochocientos", 9: "novecientos"}


def bajo_mil(n):
    if n < 20:
        return U[n]
    if n < 30:
        return VEINTI[n]
    if n < 100:
        return D[n // 10] + ("" if n % 10 == 0 else " y " + U[n % 10])
    if n == 100:
        return "cien"
    return C[n // 100] + ("" if n % 100 == 0 else " " + bajo_mil(n % 100))


def corto(nombre):
    return nombre[:-1] if nombre.endswith("uno") else nombre


def nombre_testigo(n):
    trozos = []
    mill, mil, resto = n // 1000000, (n // 1000) % 1000, n % 1000
    if mill:
        trozos.append("un millon" if mill == 1 else corto(bajo_mil(mill)) + " millones")
    if mil:
        trozos.append("mil" if mil == 1 else corto(bajo_mil(mil)) + " mil")
    if resto or not trozos:
        trozos.append(bajo_mil(resto))
    return " ".join(trozos)


def signo(a, b):
    return ">" if a > b else "<" if a < b else "="


FRONTERAS = [999999, 1000000, 1000001, 1001000, 1021000, 1100000, 1999999, 2000000, 2000005, 2345678, 5000000,
             9000001, 9999000, 9999999, 10000000]
azar = random.Random(20261008)
MUESTRA = sorted(set(FRONTERAS) | set(azar.sample(range(1000000, 10000001), 400)))

print("=" * 78)
print("PASO N.6 - HASTA DIEZ MILLONES  (%s)" % modo())
print("=" * 78)
try:
    print("\nA - LAS TRAMPAS DEL PLAN (los nombres)")
    comprobar("A1 1000000 -> un millon (no 'uno millon')", S("nombre: 1000000"), "un millon")
    comprobar("A2 2000000 -> dos millones (plural)", S("nombre: 2000000"), "dos millones")
    comprobar("A3 1021000 -> un millon veintiun mil", S("nombre: 1021000"), "un millon veintiun mil")
    comprobar("A4 2000005 -> dos millones cinco (el grupo de ceros no se dice)", S("nombre: 2000005"),
              "dos millones cinco")
    comprobar("A5 10000000 -> diez millones", S("nombre: 10000000"), "diez millones")
    comprobar("A6 10000001: mas alla de diez millones no me lo invento", S("nombre: 10000001"),
              "fuera_de_mi_secuencia")
    comprobar("A7 numero: dos millones cinco -> 2000005 (no 25 ni 2005)", S("numero: dos millones cinco"), "2000005")
    comprobar("A8 numero: un millon mil -> 1001000", S("numero: un millon mil"), "1001000")
    comprobar("A9 numero: un millón (con tilde) -> 1000000", S("numero: un millón"), "1000000")
    comprobar("A10 'dos millon' y 'uno millones' no son nombres (no se adivina)",
              (motor.leer("dos millon", SABER), motor.leer("uno millones", SABER),
               motor.leer("un millones", SABER)), (None, None, None))
    comprobar("A11 nombre: 2345678", S("nombre: 2345678"),
              "dos millones trescientos cuarenta y cinco mil seiscientos setenta y ocho")

    print("\nB - NOMBRES IDA Y VUELTA CONTRA EL TESTIGO (%d numeros: fronteras + azar)" % len(MUESTRA))
    mal_ida = [n for n in MUESTRA if motor.decir(n, SABER) != nombre_testigo(n)]
    comprobar("B1 decir(n) = el nombre del testigo", mal_ida[:3], [])
    mal_vuelta = [n for n in MUESTRA if motor.leer(nombre_testigo(n), SABER) != n]
    comprobar("B2 leer(el nombre del testigo) = n", mal_vuelta[:3], [])

    print("\nC - EL SIGUIENTE Y EL ANTERIOR POR LAS FRONTERAS; LOS SALTOS CRUZAN EL MILLON (punto 4)")
    for a, b in ((999999, 1000000), (1999999, 2000000), (1000999, 1001000), (9999999, 10000000)):
        comprobar("C %d -> %d" % (a, b), motor.leer(motor.siguiente(motor.decir(a, SABER), SABER), SABER), b)
        comprobar("C %d <- %d" % (a, b), motor.leer(motor.anterior(motor.decir(b, SABER), SABER), SABER), a)
    comprobar("C9 despues de diez millones no hay siguiente", motor.siguiente("diez millones", SABER), None)
    comprobar("C10 de 100000 en 100000 desde 700000 cruza el millon",
              S("de 100000 en 100000 desde 700000 hasta 1300000"), "800000, 900000, 1000000, 1100000, 1200000, 1300000")
    comprobar("C11 de 1000000 en 1000000 desde 7000000: se para en diez millones",
              S("de 1000000 en 1000000 desde 7000000"), "8000000, 9000000, 10000000")
    comprobar("C12 de 10 en 10 desde 9999950 (el cuentakilometros)", S("de 10 en 10 desde 9999950"),
              "9999960, 9999970, 9999980, 9999990, 10000000")

    print("\nD - LA ESTRUCTURA (puntos 1, 2 y 3) Y COMPARAR")
    comprobar("D1 millar: 1030405 -> 1000000 + 30000 + 400 + 5", S("millar: 1030405"), "1000000 + 30000 + 400 + 5")
    t = motor.explicar_pregunta("millar: 1030405", SABER)
    comprobar("D2 ... son 1 millon, 30 mil y 405; y hay 10 centenas de millar aunque la cifra sea 0",
              ("1 MILLON, 30 MIL y 405" in t, "10 centenas de millar" in t), (True, True))
    t = motor.explicar_pregunta("millar: 1000000", SABER)
    comprobar("D3 los patrones de las potencias de diez: un millon = 10 centenas de millar = 1000 millares",
              ("un millon = 10 centenas de millar" in t, "un millon = 1000 millares" in t), (True, True))
    comprobar("D4 999999 < 1000000 (mas cifras gana, aunque tenga ceros)", S("comparar: 999999 y 1000000"),
              "999999 < 1000000")
    comprobar("D5 2345678 < 2354678 (la primera distinta)", S("comparar: 2345678 y 2354678"), "2345678 < 2354678")
    comprobar("D6 10000000 > 9999999", S("comparar: 10000000 y 9999999"), "10000000 > 9999999")
    pares = [(azar.randint(100000, 10000000), azar.randint(1000000, 10000000)) for _ in range(60)]
    mal = [(a, b) for a, b in pares if S("comparar: %d y %d" % (a, b)) != "%d %s %d" % (a, signo(a, b), b)]
    comprobar("D7 comparar contra el testigo (60 pares)", mal[:3], [])

    print("\nE - SUMAR Y RESTAR: las columnas y los millones como cosas (puntos 1 y 6)")
    mal = []
    for _ in range(40):
        a, b = azar.randint(1000000, 5000000), azar.randint(10000, 4999999)
        if S("columnas: %d + %d" % (a, b)) != "%d + %d = %d" % (a, b, a + b):
            mal.append((a, b))
        if S("columnas: %d - %d" % (a, b)) != "%d - %d = %d" % (a, b, a - b) and a >= b:
            mal.append((a, "-", b))
    comprobar("E1 columnas contra el testigo (40 sumas y 40 restas de siete cifras)", mal[:3], [])
    comprobar("E2 columnas: 10000000 - 1 (a traves de siete ceros)", S("columnas: 10000000 - 1"),
              "10000000 - 1 = 9999999")
    comprobar("E3 2000000 + 3000000: dos millones + tres millones (contando millones)",
              A("sumar", a=2000000, b=3000000), (5000000, "sumar_miles_justos"))
    r = motor.aplicar("sumar", {"a": 2000000, "b": 3000000}, SABER)
    comprobar("E4 ... y lo dice: 2 millones + 3 millones = 5 millones",
              "2 millones + 3 millones = 5 millones" in r["resultado"]["cuenta"], True)
    comprobar("E5 9000000 - 1000000 = 8000000 (9 millones - 1 millon)",
              A("restar", a=9000000, b=1000000), (8000000, "restar_miles_justos"))
    comprobar("E6 9999999 + 1 = 10000000", S("9999999 + 1"), "10000000")
    comprobar("E7 9999999 + 2: se pasa de diez millones -> ninguna", S("9999999 + 2"), "ninguna")
    comprobar("E8 restar miles justos con muchos miles ya no los cuenta de uno en uno (9000000 - 4000)",
              A("restar", a=9000000, b=4000)[0], 8996000)

    print("\nF - CRUZAR EL MILLON (punto 4): completar el millon y contar hacia arriba pasando por el")
    comprobar("F1 997000 + 5000 = 1002000 (no 1000200 ni 102000), pasando por el millon",
              A("sumar", a=997000, b=5000), (1002000, "sumar_pasando_por_el_millon"))
    r = motor.aplicar("sumar", {"a": 997000, "b": 5000}, SABER)
    comprobar("F2 ... a 997000 le faltan 3000; de los 5000 quedan 2000",
              ("le faltan 3000" in r["resultado"]["cuenta"], "quedan 2000" in r["resultado"]["cuenta"]), (True, True))
    comprobar("F3 1002000 - 997000 = 5000 (3000 hasta el millon y 2000 desde el)",
              A("restar", a=1002000, b=997000), (5000, "restar_pasando_por_el_millon"))
    comprobar("F4 2997000 + 5000 = 3002000 (cualquier millon justo)", A("sumar", a=2997000, b=5000),
              (3002000, "sumar_pasando_por_el_millon"))
    comprobar("F5 9999999 + 1 = 10000000 (al techo justo)", A("sumar", a=9999999, b=1),
              (10000000, "sumar_pasando_por_el_millon"))
    comprobar("F6 997000 + 2000: no llega al millon -> otra pieza", A("sumar", a=997000, b=2000)[1] !=
              "sumar_pasando_por_el_millon", True)
    r = A("sumar", a=500001, b=600000)
    comprobar("F7 500001 + 600000: el primero esta lejos del millon -> otra pieza",
              (r[0], r[1] != "sumar_pasando_por_el_millon"), (1100001, True))
    comprobar("F8 3002000 - 997000: los millones no son vecinos -> otra pieza",
              A("restar", a=3002000, b=997000)[1] != "restar_pasando_por_el_millon", True)
    mal_s, mal_r, por_s, por_r = [], [], 0, 0
    for _ in range(60):
        mill = azar.randint(0, 8)
        a = mill * 1000000 + azar.randint(900000, 999999)
        b = azar.randint(1000000 - a % 1000000, 999999)
        v, pid = A("sumar", a=a, b=b)
        por_s += pid == "sumar_pasando_por_el_millon"
        if v != a + b:
            mal_s.append((a, b, v))
        x = (mill + 1) * 1000000 + azar.randint(0, 999999)
        v, pid = A("restar", a=x, b=a)
        por_r += pid == "restar_pasando_por_el_millon"
        if v != x - a:
            mal_r.append((x, a, v))
    comprobar("F9 60 sumas que cruzan un millon, contra el testigo", mal_s[:3], [])
    comprobar("F10 ... todas pasando por el millon", por_s, 60)
    comprobar("F11 60 restas que cruzan un millon, contra el testigo", mal_r[:3], [])
    comprobar("F12 ... todas contando hacia arriba por el millon", por_r, 60)

    print("\nG - CADA PIEZA NUEVA SE COMPRUEBA DE VERDAD (si una cuenta sale mal, la vuelta lo caza)")
    base = motor.cargar_piezas()

    def modulo(nombre):
        sp = importlib.util.spec_from_file_location(nombre, os.path.join(RAIZ, "conocimiento", "piezas",
                                                                         nombre + ".py"))
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        return m

    class Tramposo:
        """Lo que se le da a la pieza, pero UNA cuenta (la que se nombra) da uno de mas."""

        def __init__(self, real, cual):
            self._real, self._cual = real, cual
            if cual != "usar":
                f = getattr(real, cual)
                setattr(self, cual, lambda *x: f(*x) + 1)

        def __getattr__(self, k):
            return getattr(self._real, k)

        def usar(self, nombre, **sit):
            r = self._real.usar(nombre, **sit)
            if self._cual == "usar":
                r = dict(r)
                r["valor"] = r["valor"] + 1
            return r

    for nombre, sit, cual in (
            ("sumar_pasando_por_el_millon", {"a": 997000, "b": 5000}, "lo_que_falta_para_el_redondo"),
            ("sumar_pasando_por_el_millon", {"a": 997000, "b": 5000}, "usar"),
            ("restar_pasando_por_el_millon", {"a": 1002000, "b": 997000}, "lo_que_falta_para_el_redondo"),
            ("restar_pasando_por_el_millon", {"a": 1002000, "b": 997000}, "sumar_por_columnas")):
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
        comprobar("G %s: con '%s' dando uno de mas, la vuelta NO cuadra" % (nombre, cual), cazado, True)
    falta = [(n, motor.lo_que_falta_para_el_redondo(n, 6, SABER)) for n in azar.sample(range(0, 10000000), 200)]
    comprobar("G lo que falta para el millon, por las cifras, contra el testigo (200)",
              [(n, f) for n, f in falta if f != (1000000 - n % 1000000) % 1000000][:3], [])

    print("\nH - REDONDEAR (punto 5): al millon y a la centena de millar")
    comprobar("H1 2549999 al millon -> 3000000", S("redondear: 2549999 al millon"), "3000000")
    comprobar("H2 2499999 al millon -> 2000000 (no la cadena)", S("redondear: 2499999 al millon"), "2000000")
    t = motor.explicar_pregunta("redondear: 2499999", SABER)
    comprobar("H3 ... y avisa de la trampa de la cadena", "LA TRAMPA DE LA CADENA" in t, True)
    comprobar("H4 9600000 al millon -> 10000000 (el techo)", S("redondear: 9600000 al millón"), "10000000")
    comprobar("H5 2345678 a la centena de millar -> 2300000", S("redondear: 2345678 a la centena de millar"), "2300000")
    mal = []
    for n in azar.sample(range(1000000, 9500000), 60):
        for sitio, k in (("millon", 1000000), ("centena de millar", 100000)):
            esperado = (n + k // 2) // k * k
            if S("redondear: %d a%s %s" % (n, "l" if sitio == "millon" else " la", sitio)) != str(esperado):
                mal.append((n, sitio))
    comprobar("H6 120 redondeos (al millon y a la centena de millar) contra el testigo", mal[:3], [])

    print("\nI - MULTIPLICAR Y DIVIDIR CON SIETE CIFRAS (lo de antes llega solo)")
    motor.aprender("tablas", SABER)
    mal = []
    for _ in range(30):
        a, k = azar.randint(100000, 1111111), azar.randint(2, 9)
        if S("%d x %d" % (a, k)) != str(a * k):
            mal.append((a, k))
        q, d = azar.randint(1000000, 9999999), azar.randint(2, 9)
        esperado = str(q // d) if q % d == 0 else "%d resto %d" % (q // d, q % d)
        if S("%d : %d" % (q, d)) != esperado:
            mal.append((q, ":", d))
    comprobar("I1 30 productos y 30 divisiones cortas contra el testigo", mal[:3], [])
    comprobar("I2 1234567 x 8 = 9876536", S("1234567 x 8"), "9876536")
    comprobar("I3 1234567 x 9: se pasa de diez millones", S("1234567 x 9"), "no_se_puede")
    comprobar("I4 10000000 : 8 = 1250000", S("10000000 : 8"), "1250000")
    comprobar("I5 999999 x 10 = 9999990", S("999999 x 10"), "9999990")

    print("\nJ - LOS DOS TECHOS Y EL TIEMPO (cada pregunta grande, con su explicacion, en menos de 2 s)")
    comprobar("J1 la lista de CONTAR objetos sigue en diez mil", motor.techo_de_contar(SABER), "diez mil")
    comprobar("J2 los NUMEROS llegan a diez millones", motor.numero_maximo(SABER), 10000000)
    lentas = []
    for q in ("9999999 + 1", "10000000 - 3997", "9000000 - 4000", "2345678 + 1234567", "7654321 - 1234567",
              "1002000 - 997000", "calcular: 997000 + 5000", "1234567 x 8", "9999999 : 7", "9999999 : 13",
              "redondear: 9999999", "millar: 9876543", "comparar: 9999999 y 10000000", "multiplos de 999999",
              "simplificar: 5000000/10000000", "equivalente: 10000000 - 3997", "9999990 + ? = 10000000",
              "partes: 2500000, 2500000, 2500000, 2500000; todo: ?", "recta: -5000000 - 5000000"):
        t1 = time.time()
        motor.explicar_pregunta(probar.como_problema(q), SABER)
        d = time.time() - t1
        if d > 2:
            lentas.append((q, round(d, 2)))
    comprobar("J3 19 preguntas grandes, ninguna de mas de 2 s", lentas, [])
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(0 if MAL == 0 else 1)
