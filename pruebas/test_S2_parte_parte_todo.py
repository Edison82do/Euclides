# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO S.2: LAS ESTRUCTURAS COMUNES, PARTE-PARTE-TODO CON TRES PARTES O MAS (NCETM 1.28).
El plan y sus trampas: diario/2026-10-07-paso-S2-parte-parte-todo.md
Python solo aparece aqui como TESTIGO externo (las cuentas con Fraction, +, -, *).
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
TMP = tempfile.mkdtemp(prefix="s2_")
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
    r = motor.decidir_parte_todo(t, SABER)
    return r["valor"] if r["conclusion"] == "hecho" else r["conclusion"]


def P(t):
    return motor.decidir_parte_todo(t, SABER).get("pieza")


def txt(f):
    """El testigo escribe un Fraction como lo escribe el sistema ('4.375', '38')."""
    if f.denominator == 1:
        return str(f.numerator)
    s = "%.6f" % float(f)
    return s.rstrip("0").rstrip(".")


def dec(azar, cifras_max=3):
    k = azar.randint(1, cifras_max)
    return "%d.%s" % (azar.randint(0, 99), "".join(str(azar.randint(0, 9)) for _ in range(k)))


azar = random.Random(128)
try:
    comprobar("0 con la memoria VACIA, 1000000 en 4 partes iguales -> todavia_no (no se sabe la tabla del 4)",
              D("todo: 1000000; 4 partes iguales"), "todavia_no")
    motor.aprender("tablas", SABER)          # en 5.o las tablas ya se saben (repartir con la division corta las pide)
    print("A - FALTA EL TODO: se juntan las partes (2 a 6 partes enteras)")
    malos = []
    for _ in range(150):
        n = azar.randint(2, 6)
        grande = azar.choice([12, 100, 1000, 99999])
        ps = [azar.randint(0, grande) for _ in range(n)]
        texto = "partes: %s; todo: ?" % ", ".join(str(p) for p in ps)
        if D(texto) != txt(Fraction(sum(ps))):
            malos.append((texto, D(texto), sum(ps)))
    comprobar("A 150 todos de 2 a 6 partes contra el testigo", malos, [])
    comprobar("A partes: 37, 25, 63 -> 125", D("partes: 37, 25, 63; todo: ?"), "125")
    comprobar("A ... y lo hace con las parejas amigas (37 + 63 = 100 primero)", P("partes: 37, 25, 63; todo: ?"),
              "todo_juntando_las_parejas_amigas")
    comprobar("A partes: 6, 6, 6, 6 -> 24 por partes iguales (4 x 6)",
              (D("partes: 6, 6, 6, 6; todo: ?"), P("partes: 6, 6, 6, 6; todo: ?")), ("24", "todo_por_partes_iguales"))
    comprobar("A partes: 12, 5, 30 -> 47 en orden (no hay amigas)",
              (D("partes: 12, 5, 30; todo: ?"), P("partes: 12, 5, 30; todo: ?")), ("47", "todo_sumando_en_orden"))
    comprobar("A el todo puede ir primero: todo: ?; partes: 8, 9, 2", D("todo: ?; partes: 8, 9, 2"), "19")

    print("\nB - FALTA UNA PARTE (en cada sitio) contra el testigo")
    malos = []
    for _ in range(150):
        n = azar.randint(2, 6)
        grande = azar.choice([12, 100, 1000, 99999])
        ps = [azar.randint(0, grande) for _ in range(n)]
        k = azar.randrange(n)
        vis = ["?" if i == k else str(p) for i, p in enumerate(ps)]
        texto = "todo: %d; partes: %s" % (sum(ps), ", ".join(vis))
        if D(texto) != str(ps[k]):
            malos.append((texto, D(texto), ps[k]))
    comprobar("B 150 partes que faltan, en cualquier sitio", malos, [])
    comprobar("B todo: 100; partes: 37, ?, 25 -> 38 (no 162, no 63)", D("todo: 100; partes: 37, ?, 25"), "38")
    comprobar("B ... juntando primero lo que se sabe (una sola resta)", P("todo: 100; partes: 37, ?, 25"),
              "parte_juntando_lo_que_se_sabe")
    comprobar("B con una sola parte que se sabe: quitar una a una (una resta)",
              P("todo: 50; partes: ?, 20"), "parte_quitando_una_a_una")
    comprobar("B la parte que falta puede ser cero: todo 10; 4, 6, ?", D("todo: 10; partes: 4, 6, ?"), "0")

    print("\nC - CON DECIMALES (una, dos y tres cifras detras del punto)")
    malos = []
    for _ in range(80):
        n = azar.randint(2, 5)
        ps = [dec(azar) for _ in range(n)]
        total = sum(Fraction(p) for p in ps)
        t1 = "partes: %s; todo: ?" % ", ".join(ps)
        if D(t1) != txt(total):
            malos.append((t1, D(t1), txt(total)))
        k = azar.randrange(n)
        t2 = "todo: %s; partes: %s" % (txt(total), ", ".join("?" if i == k else p for i, p in enumerate(ps)))
        if D(t2) != txt(Fraction(ps[k])):
            malos.append((t2, D(t2), txt(Fraction(ps[k]))))
    comprobar("C 160 cuentas con decimales (todo y parte)", malos, [])
    comprobar("C 2.5, 0.75, 1.125 -> 4.375 (el punto en su sitio, no 0.80)", D("partes: 2.5, 0.75, 1.125; todo: ?"),
              "4.375")
    comprobar("C 1.25, 3.5, 0.75 -> 5.5 con las amigas (1.25 + 0.75 = 2)",
              (D("partes: 1.25, 3.5, 0.75; todo: ?"), P("partes: 1.25, 3.5, 0.75; todo: ?")),
              ("5.5", "todo_juntando_las_parejas_amigas"))
    comprobar("C cuatro cifras detras del punto -> todavia_no", D("partes: 1.2345, 2; todo: ?"), "todavia_no")

    print("\nD - PARTES IGUALES (la estructura multiplicativa, punto 1)")
    malos = []
    for n in range(2, 10):
        for parte in (1, 3, 7, 12, 25, 99, 250):
            t1 = "partes: %s; todo: ?" % ", ".join([str(parte)] * n)
            if (D(t1), P(t1)) != (str(n * parte), "todo_por_partes_iguales"):
                malos.append((t1, D(t1)))
            t2 = "todo: %d; %d partes iguales" % (n * parte, n)
            if D(t2) != str(parte):
                malos.append((t2, D(t2)))
    comprobar("D 112 cuentas de partes iguales (el todo y la parte)", malos, [])
    comprobar("D todo: 24; partes: ?, ?, ?, ? iguales -> 6", D("todo: 24; partes: ?, ?, ?, ? iguales"), "6")
    comprobar("D todo: 26 en 4 partes iguales -> 6.5 (cambiando a decimas, M.13)", D("todo: 26; 4 partes iguales"), "6.5")
    comprobar("D partes: 2.5, 2.5, 2.5 -> 7.5", D("partes: 2.5, 2.5, 2.5; todo: ?"), "7.5")
    comprobar("D todo: 10; 3 partes iguales -> todavia_no (sobra aun en milesimas)",
              D("todo: 10; 3 partes iguales"), "todavia_no")

    print("\nE - LAS TRAMPAS: lo que NO se puede (y se dice, sin dar un numero)")
    for texto, esperado in (("perimetro: 30; lados: 20, 15, ?", "no_se_puede"),
                            ("todo: 50; partes: 20, ?, ?", "no_se_puede"),
                            ("todo: ?; partes: 20, ?", "no_se_puede"),
                            ("todo: 50; partes: 20, ?, ? iguales", "todavia_no"),
                            ("todo: 30; partes: 10, 10, 10", "cuadra"),
                            ("todo: 30; partes: 10, 10, 11", "no_cuadra"),
                            ("todo: 30; partes: ?", "no_entiendo"),
                            ("todo: 30; partes: 1, dos", "no_entiendo")):
        comprobar("E %s -> %s" % (texto, esperado), S(texto), esperado)
    salida = motor.explicar_orden_parte_todo("todo: 100; partes: 37, ?, 25", SABER)
    comprobar("E la explicacion ensena los errores tipicos (162 y 63) y la barra",
              all(x in salida for x in ("NO es 100 + 37 + 25 = 162", "NO es 100 - 37 = 63", "|    ?    |")), True)
    comprobar("E y la otra estrategia da LO MISMO", "LO MISMO" in salida, True)

    print("\nF - LOS CONTEXTOS (punto 4): la misma estructura con otras palabras, cada uno con su unidad")
    for texto, esperado in (("perimetro: 30; lados: 8, 7, 6, ?", "9 cm"),
                            ("tenia: 20; gaste: 4.50, 7.25; queda: ?", "8.25 pesos"),
                            ("tenia: 20; gaste: 4.50, 7.50; queda: ?", "8 pesos"),
                            ("tenia: 20; gaste: 4.25, 7.25; queda: ?", "8.50 pesos"),
                            ("camino: ?; tramos: 1.25, 3.5, 0.75", "5.5 km"),
                            ("clase: 28; grupos: 7, ?, 6, 8", "7 ninos"),
                            ("bolsa: ?; cosas: 0.5, 1.25, 2", "3.75 kg"),
                            ("dia: 24; ratos: 8, 9, ?", "7 horas"),
                            ("perimetro: 36; 4 partes iguales", "cada parte: 9 cm")):
        comprobar("F %s -> %s" % (texto, esperado), S(texto), esperado)
    ctx = motor._pt_contextos(SABER)
    comprobar("F los contextos salen del .kn (6, y el general 'todo')", sorted(ctx),
              ["bolsa", "camino", "clase", "dia", "perimetro", "tenia", "todo"])
    salida = motor.explicar_orden_parte_todo("perimetro: 30; lados: 8, 7, 6, ?", SABER)
    comprobar("F dice quien es el todo y quienes las partes, y que es la MISMA estructura",
              all(x in salida for x in ("perimetro es el TODO", "lados son las PARTES", "MISMA estructura")), True)

    print("\nG - CADA PIEZA SE COMPRUEBA DE VERDAD (si una cuenta sale mal, la vuelta lo caza)")
    base = motor.cargar_piezas()

    def modulo(nombre):
        sp = importlib.util.spec_from_file_location(nombre, os.path.join(RAIZ, "conocimiento", "piezas",
                                                                         nombre + ".py"))
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        return m

    class Tramposo:
        """Lo que se le da a la pieza, pero la cuenta que se le pide da UNO DE MAS (la primera vez)."""

        def __init__(self, real, cual):
            self._real, self._cual, self._hecho = real, cual, False

        def __getattr__(self, k):
            return getattr(self._real, k)

        def usar(self, nombre, **sit):
            r = self._real.usar(nombre, **sit)
            if nombre == self._cual and not self._hecho:
                self._hecho = True
                r = dict(r)
                v = r["valor"]
                r["valor"] = v + 1 if isinstance(v, int) else (str(int(v) + 1) if v.isdigit() else v + "1")
            return r

    for nombre, sit, cual in (
            ("todo_sumando_en_orden", {"partes": ["12", "5", "30"]}, "combinar"),
            ("todo_juntando_las_parejas_amigas", {"partes": ["37", "25", "63"]}, "combinar"),
            ("todo_por_partes_iguales", {"partes": ["6", "6", "6", "6"]}, "multiplicar"),
            ("parte_quitando_una_a_una", {"todo": "100", "partes": ["37", None, "25"]}, "combinar"),
            ("parte_juntando_lo_que_se_sabe", {"todo": "100", "partes": ["37", None, "25"]}, "todo_de_las_partes"),
            ("parte_repartiendo_en_partes_iguales", {"todo": "24", "partes": [None] * 4, "iguales": True}, "dividir")):
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
    mapa = motor.mapa_del_conocimiento()
    comprobar("G ninguna pieza de 'todo_de_las_partes' usa su propia pregunta",
              [p for p, usa in mapa.items() if "todo_de_las_partes" in usa
               and base["piezas"][p]["responde"] == "todo_de_las_partes"], [])
    comprobar("G ninguna pieza usa 'parte_del_todo'", [p for p, usa in mapa.items() if "parte_del_todo" in usa], [])

    print("\nH - LO DE ANTES SIGUE IGUAL (no se lo come la orden nueva)")
    for texto, esperado in (("perimetro: 4, 7, 5", "16"), ("37 + ? + 25 = 100", "38"),
                            ("3 + 4 x 5", "23"), ("calcular: 47 + 30", "77"),
                            ("problema: Ana tiene 8 manzanas. Tiene 3 mas que Luis. Cuantas tiene Luis?", "5"),
                            ("factores: 36", "1, 2, 3, 4, 6, 9, 12, 18, 36")):
        comprobar("H %s -> %s" % (texto, esperado), S(texto), esperado)

    print("\nI - CERCA DEL TECHO, y el TIEMPO (cada pregunta, con su explicacion, en menos de 2 s)")
    for texto, esperado in (("partes: 999999, 1; todo: ?", "1000000"),
                            ("partes: 999999, 2; todo: ?", "no_alcanza"),
                            ("todo: 1000000; partes: 250000, ?, 250000, 250000", "250000"),
                            ("todo: 1000000; 4 partes iguales", "cada parte: 250000"),
                            ("partes: 250000, 250000, 250000, 250000; todo: ?", "1000000"),
                            ("todo: 1000001; partes: 1, ?", "no_alcanza"),
                            ("todo: 999999.999; partes: 0.001, ?", "no_alcanza"),   # contadas en milesimas, el techo de M.13
                            ("partes: 123456, 654321, 98765, 1234; todo: ?", "877776"),
                            ("todo: 877776; partes: 123456, 654321, ?, 1234", "98765"),
                            ("partes: 0.001, 0.999, 999999; todo: ?", "1000000")):
        t1 = time.time()
        r = S(texto)
        dt = time.time() - t1
        comprobar("I %s -> %s (%.2f s)" % (texto, esperado, dt), (r, dt < 2), (esperado, True))
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\nTOTAL: %d/%d" % (BIEN, BIEN + MAL))
