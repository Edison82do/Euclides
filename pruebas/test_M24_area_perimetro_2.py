# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.24: CONTEXTOS MULTIPLICATIVOS - AREA Y PERIMETRO 2 (NCETM 2.30, 'Multiplicative contexts: area and
perimeter 2'): el paralelogramo, el triangulo, el area frente al perimetro y la escala.
El plan y sus trampas: diario/2026-10-10-paso-M24-area-perimetro-2.md
Pocas y representativas (decision de Carlos).  Las formulas del paralelogramo y del triangulo son DATOS
(relaciones.kn), una relacion mas en el modelo comun; la mitad de un producto (base x altura : 2) son dos PIEZAS de la
pregunta nueva 'mitad_de_un_producto', que el numero comun del resolvedor pide.  Python solo aparece aqui como TESTIGO.
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
TMP = tempfile.mkdtemp(prefix="m24_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia
import motor  # noqa: E402
import probar  # noqa: E402

BIEN = MAL = 0
PAR = "partir_por_la_mitad_un_factor_par"
MUL = "multiplicar_y_partir_por_la_mitad"


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
    sp = importlib.util.spec_from_file_location("m24_" + nombre, ruta)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def main():
    t0 = time.time()
    azar = random.Random(2030)
    print("=" * 78)
    print("PASO M.24: AREA Y PERIMETRO 2 - PARALELOGRAMO, TRIANGULO, AREA FRENTE A PERIMETRO, ESCALA (NCETM 2.30)")
    print("=" * 78)

    print("\nA - LA MITAD DE UN PRODUCTO (a x b : 2): las dos piezas contra el testigo, con su vuelta")
    malas, n = [], 0
    for _ in range(30):
        a = azar.choice([azar.randint(1, 12), azar.randint(13, 99), azar.randint(100, 999)])
        b = azar.choice([azar.randint(1, 12), azar.randint(13, 99)])
        n += 1
        q, resto = divmod(a * b, 2)                                   # el TESTIGO
        r = motor.aplicar("mitad_de_un_producto", {"a": a, "b": b}, SABER)
        quien = PAR if (a % 2 == 0 or b % 2 == 0) else MUL
        if r["conclusion"] != "hecho" or r["resultado"]["valor"] != q or r["resultado"]["resto"] != resto \
                or r["pieza"]["id"] != quien or not r["resultado"]["vuelta_ok"]:
            malas.append((a, b, r.get("resultado", {}).get("valor")))
    comprobar("A %d productos al azar: el valor del testigo, la pieza que toca por su costo y su vuelta" % n, malas, [])
    malas = []
    base = motor.cargar_piezas()
    for _ in range(15):                                               # la pieza larga tambien sabe con los pares
        a, b = azar.randint(1, 99), azar.randint(1, 99)
        u = motor._Lo_que_puede_usar(base["piezas"][MUL], base, SABER)
        res = base["piezas"][MUL]["hacer"]({"a": a, "b": b}, u)
        if (res["valor"], res["resto"]) != divmod(a * b, 2) or not res["vuelta_ok"]:
            malas.append((a, b))
    comprobar("A 15 con multiplicar y partir (el segundo camino) tambien como el testigo", malas, [])

    print("\nB - EL CONTROL: el costo elige (partir antes el par es mas barato; con los dos impares, multiplicar)")
    for (a, b), quien in (((6, 4), PAR), ((13, 8), PAR), ((7, 3), MUL), ((2, 3), PAR), ((9, 9), MUL)):
        r = motor.aplicar("mitad_de_un_producto", {"a": a, "b": b}, SABER)
        comprobar("B %d x %d : 2 -> %s" % (a, b, quien), r["pieza"]["id"], quien)
    r = motor.aplicar("mitad_de_un_producto", {"a": 6, "b": 4}, SABER)
    comprobar("B 6 x 4 : 2: multiplicar y partir tambien servia (se dice, no se hace)", r.get("tambien_servian"), [MUL])
    r = motor.aplicar("mitad_de_un_producto", {"a": 0, "b": 4}, SABER)
    comprobar("B con un 0 no hay nada que partir: ninguna pieza (lo hace el numero comun, como antes)",
              r["conclusion"], "ninguna")

    print("\nC - LAS TRAMPAS: piezas TRUCADAS (la vuelta las caza)")
    trampas = (
        (MUL, ('v, resto = r["valor"], r["resultado"].get("resto", 0)', 'v, resto = producto, 0'),
         {"a": 6, "b": 4}, "olvidar la mitad (el area del triangulo = la del paralelogramo, 24)"),
        (PAR, ('b=otro)["valor"] if mitad else 0', 'b=u.usar("dividir", total=otro, divisor=2)["valor"])["valor"]'),
         {"a": 6, "b": 4}, "partir LOS DOS factores (6 x 4 : 2 = 3 x 2 = 6)"),
        (PAR, ('mitad = r["valor"]', 'mitad = par'),
         {"a": 6, "b": 4}, "decir que parte y no partir (6 x 4 : 2 = 24)"),
        (MUL, ('pasos = [', 'resto = 0\n    pasos = ['),
         {"a": 7, "b": 3}, "tirar el medio que sobra (7 x 3 : 2 = 10)"),
    )
    for pid, cambio, s, que in trampas:
        u = motor._Lo_que_puede_usar(base["piezas"][pid], base, SABER)
        try:
            cazado = modulo(pid, cambio).hacer(s, u)["vuelta_ok"] is False
        except (ValueError, motor.NoSalio, RuntimeError):
            cazado = True
        comprobar("C %s trucada -> se caza" % que, cazado, True)

    print("\nD - EL PARALELOGRAMO (punto 1): base x altura PERPENDICULAR; el lado inclinado solo va en el perimetro")
    for q, esperado in (
            ("Un paralelogramo tiene 7 cm de base y 3 cm de altura. ¿Cuál es su area?", "21 cm cuadrados"),
            ("Un paralelogramo tiene 8 cm de base, 5 cm de lado y 4 cm de altura. ¿Cuál es su area?", "32 cm cuadrados"),
            ("Un paralelogramo tiene 8 cm de base, 5 cm de lado y 4 cm de altura. ¿Cuál es su perimetro?", "26 cm"),
            ("Un paralelogramo tiene 36 cm2 de area y 9 cm de base. ¿Cuánto mide su altura?", "4 cm"),
            ("Un romboide tiene 12 m de base y 7 m de altura. ¿Cuál es su area?", "84 m cuadrados"),
            ("Un paralelogramo tiene 8 cm de base y 5 cm de lado. ¿Cuál es su area?", "todavia_no")):
        comprobar("D %s -> %s" % (q, esperado), S("resolver: " + q), esperado)
    t = X("resolver: Un paralelogramo tiene 8 cm de base, 5 cm de lado y 4 cm de altura. ¿Cuál es su area?")
    comprobar("D la explicacion dice POR QUE (se corta un triangulo: un rectangulo; el lado inclinado no es la altura)",
              "un rectangulo de base x altura" in t and "la altura es la perpendicular" in t, True)

    print("\nE - EL TRIANGULO (punto 2): base x altura : 2 (la mitad del paralelogramo)")
    for q, esperado in (
            ("Un triangulo tiene 6 cm de base y 4 cm de altura. ¿Cuál es su area?", "12 cm cuadrados"),
            ("Un triangulo tiene 7 cm de base y 3 cm de altura. ¿Cuál es su area?", "21/2 cm cuadrados"),
            ("Un terreno triangular tiene 10 m de base y 6 m de altura. ¿Cuál es su area?", "30 m cuadrados"),
            ("Un triangulo tiene 20 cm2 de area y 5 cm de base. ¿Cuánto mide su altura?", "8 cm"),
            ("Un triangulo tiene 6 cm de base, 5 cm de lado y 4 cm de altura. ¿Cuál es su area?", "12 cm cuadrados"),
            ("Un triangulo equilatero mide 5 cm de lado. Cual es su perimetro?", "15 cm"),
            ("Un triangulo tiene 6 cm de base y 4 cm de altura. ¿Cuál es su perimetro?", "todavia_no")):
        comprobar("E %s -> %s" % (q, esperado), S("resolver: " + q), esperado)
    t = X("resolver: Un triangulo tiene 6 cm de base y 4 cm de altura. ¿Cuál es su area?")
    comprobar("E la explicacion: la mitad del paralelogramo, parte antes el 6 (par) y lo comprueba doblando",
              "el triangulo es la mitad" in t and "6 es par: su mitad es 3" in t and "12 + 12 = 24" in t
              and "... SI" in t, True)

    print("\nF - LA TRAMPA QUE YA ESTABA: el triangulo rectangulo leido como rectangulo (decia 24, FALSO)")
    comprobar("F triangulo rectangulo 6 x 4 -> 12 (la palabra mas larga manda)",
              S("resolver: Un triangulo rectangulo tiene 6 cm de base y 4 cm de altura. ¿Cuál es su area?"),
              "12 cm cuadrados")
    comprobar("F el rectangulo sigue siendo rectangulo (base = largo, altura = ancho)",
              S("resolver: Un rectangulo tiene 6 cm de base y 4 cm de altura. ¿Cuál es su area?"), "24 cm cuadrados")

    print("\nG - LOS PUNTOS 3 Y 4 POR LO QUE YA HABIA (G.1, M.21, verdad:)")
    comprobar("G punto 3: la misma area y distinto perimetro (G.1)",
              S("comparar: rectangulo 6 x 4 y rectangulo 8 x 3"), "area igual, perimetro distinto")
    comprobar("G punto 3: el mismo perimetro y distinta area (2 x 3 + 2 x 4 = 2 x 6 + 2 x 1; 3 x 4 no es 6 x 1)",
              (S("verdad: 2 x 3 + 2 x 4 = 2 x 6 + 2 x 1"), S("verdad: 3 x 4 = 6 x 1")), ("verdadero", "falso"))
    comprobar("G punto 4: la escala del perimetro por la tabla de razon (lado 4 y perimetro 14; lado 12 -> 42)",
              S("resolver: 4 : 14 = 12 : p"), "p = 42")
    comprobar("G punto 4, el error tipico: el AREA no crece con el mismo factor (3 x 4 x 3 no es 9 x 12)",
              S("verdad: 3 x 4 x 3 = (3 x 3) x (4 x 3)"), "falso")

    print("\nH - EN EL RESOLVEDOR CON SIMBOLOS Y CERCA DEL TECHO (el mismo numero que antes; cambia el camino)")
    for q, esperado in (("resolver: 6 x 4 : 2", "12"), ("resolver: 7 x 3 : 2", "21/2"), ("resolver: 1 x 1 : 2", "1/2"),
                        ("resolver: (6 x 4) : 2", "12"), ("resolver: 0 x 9 : 2", "0"), ("resolver: 20 = 5 x h : 2", "h = 8"),
                        ("12 x 5 : 2 + 1", "31"), ("resolver: 3.5 x 4 : 2", "7"), ("resolver: 9999 x 998 : 2", "4989501"),
                        ("resolver: 9999 x 999 : 2", "9989001/2"), ("resolver: 4000 x 5000 : 2", "todavia_no")):
        comprobar("H %s -> %s" % (q, esperado), S(q), esperado)

    print("\nI - LO QUE NO CAMBIA")
    for q, esperado in (("resolver: Un rectangulo mide 8 cm de largo y 5 cm de ancho. Cual es su area?", "40 cm cuadrados"),
                        ("resolver: Un cuadrado tiene 36 cm cuadrados de area. Cuanto mide su lado?", "6 cm"),
                        ("resolver: Un triangulo mide 5 cm de lado. Cual es su perimetro?", "todavia_no"),
                        ("perimetro: triangulo de 5", "15"), ("resolver: 6 x 4 : 3", "8"), ("resolver: 7 : 2 + 1", "9/2")):
        comprobar("I %s -> %s" % (q, esperado), S(q), esperado)

    print("\nJ - EL TIEMPO (cada pregunta muy por debajo de 2 s)")
    for q in ("resolver: 9999 x 999 : 2", "resolver: Un triangulo tiene 9999 m de base y 999 m de altura. ¿Cuál es su area?",
              "resolver: Un triangulo tiene 20 cm2 de area y 5 cm de base. ¿Cuánto mide su altura?"):
        t1 = time.time()
        S(q)
        d = time.time() - t1
        comprobar("J %s (%.2f s)" % (q, d), d < 2, True)

    print("\n(%.1f s)" % (time.time() - t0))
    print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
    shutil.rmtree(TMP, ignore_errors=True)
    return 1 if MAL else 0


if __name__ == "__main__":
    sys.exit(main())
