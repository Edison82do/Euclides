# -*- coding: utf-8 -*-
"""
PRUEBAS DE LA FASE U.1 DEL PLAN U: EL MODELO Y EL LECTOR SIMBOLICO.
El plan y sus trampas: diario/2026-10-08-paso-U1-modelo-y-lector-simbolico.md
Pocas y representativas (decision de Carlos para lo nuevo).  Python solo aparece aqui como TESTIGO externo.
"""
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
TMP = tempfile.mkdtemp(prefix="u1_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria propia (vacia)
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


def P(t):
    """Lo que contesta el probador (las dos cadenas de puertas acaban igual)."""
    return probar.preguntar(t, SABER)[0]


def E(t):
    """Lo que dice el explicador: su ultima linea."""
    return motor.explicar_pregunta(t, SABER).strip().splitlines()[-1].replace("RESULTADO:", "").strip()


def testigo(f):
    """El testigo escribe una fraccion como la escribe Euclides (forma mas simple)."""
    return str(f.numerator) if f.denominator == 1 else "%d/%d" % (f.numerator, f.denominator)


def main():
    t0 = time.time()
    print("PRUEBA: FASE U.1 - EL MODELO Y EL LECTOR SIMBOLICO")
    print("=" * 60)

    print("\nA - LOS EJEMPLOS DEL PLAN U (los seis tienen que salir)")
    for q, esperado in (("a + b = 1/2; a - b = 1/4", "a = 3/8, b = 1/8"),
                        ("3 x n = 4.5", "n = 1.5"),
                        ("resolver: (a + 5) x 2 = 26", "a = 8"),
                        ("x + y + z = 40; x = y; z = 2 x y", "x = 10, y = 10, z = 20"),
                        ("1/2 + 0.25", "3/4"),
                        ("-3 + 2 x 4", "5")):
        comprobar("A %s -> %s (probador)" % (q, esperado), P(q), esperado)
        comprobar("A %s -> %s (explicador)" % (q, esperado), E(q), esperado)
    comprobar("A (a + 5) x 2 = 26 sin la orden: sigue por E.5 (como antes)", P("(a + 5) x 2 = 26"), "8")
    comprobar("A resolver: 3 x n = 12 (la puerta nueva)", P("resolver: 3 x n = 12"), "n = 4")
    comprobar("A 1/2 + 0.25: tambien en decimal", "3/4 = 0.75" in motor.explicar_pregunta("1/2 + 0.25", SABER), True)

    print("\nB - EL LECTOR: lo que lee y lo que no")
    m = motor._u_leer("2n + 3 = 11; x = -2; y = 3 x x")
    comprobar("B las cantidades en el orden en que salen", m["cantidades"], ["n", "x", "y"])
    comprobar("B tres relaciones", len(m["relaciones"]), 3)
    comprobar("B 'x' entre dos cosas es POR, si no, LETRA", motor._u_texto(m["relaciones"][2][1]), "3 x x")
    for q, ok in (("1/2 + 0.25", True), ("3 x (-2) = n", True), ("4,5 + 1", True), ("a + b = 1/2; a - b = 1/4", True),
                  ("3 + + 4", False), ("3 4 + 1", False), ("a + b; a = 2", False), ("3 x n", False),
                  ("silla,mesa", False), ("hola + 1", False), ("7", False), ("a = b = 3", False)):
        comprobar("B %s: %s" % (q, "se lee" if ok else "no se lee"), motor.es_expresion_simbolica(q), ok)

    print("\nC - EL NUMERO COMUN contra el testigo (cuentas mezcladas, muestra pequena)")
    azar = random.Random(81)
    bien = 0
    total = 0
    formas = []
    for _ in range(40):
        def uno():
            k = azar.choice(("e", "d", "f", "n"))
            if k == "e":
                v = azar.randint(0, 40)
                return str(v), Fraction(v)
            if k == "d":
                v = azar.randint(1, 99)
                return "%d.%d" % divmod(v, 10) if v % 10 else str(v // 10), Fraction(v, 10)
            if k == "f":
                a, b = azar.randint(1, 11), azar.randint(2, 12)
                return "%d/%d" % (a, b), Fraction(a, b)
            v = azar.randint(1, 30)
            return "-%d" % v, Fraction(-v)
        (ta, fa), (tb, fb) = uno(), uno()
        op = azar.choice("+-x:")
        if op == ":" and fb == 0:
            continue
        esperado = {"+": fa + fb, "-": fa - fb, "x": fa * fb, ":": fa / fb if fb else None}[op]
        q = "%s %s %s" % (ta, op, tb if not tb.startswith("-") else "(%s)" % tb)
        r = motor.decidir_resolver(q, SABER)
        total += 1
        if r["conclusion"] == "hecho":
            v = r["valor"]
            obtenido = Fraction(v[1], v[2]) * (-1 if v[0] == "-" else 1)
            if obtenido == esperado:
                bien += 1
            else:
                formas.append("%s -> %s (testigo %s)" % (q, r["respuesta"], esperado))
        else:
            formas.append("%s -> %s: %s" % (q, r["conclusion"], r.get("porque")))
    comprobar("C %d cuentas mezcladas: todas como el testigo%s" % (total, (" (" + "; ".join(formas[:3]) + ")") if formas
                                                                    else ""), bien, total)
    comprobar("C 0.5 x 0.3 + 1/4 = 2/5", P("0.5 x 0.3 + 1/4"), "2/5")
    comprobar("C 3/4 : 1/8 = 6 (con el mismo de abajo, cuantas veces cabe)", P("3/4 : 1/8"), "6")
    comprobar("C 7 : 2 = 7/2 (lo que no se reparte justo es una fraccion)", P("resolver: 7 : 2"), "7/2")
    comprobar("C 2 - 5 = -3 (pasa del cero)", P("resolver: 2 - 5"), "-3")

    print("\nD - LAS TRAMPAS")
    for q, esperado in (("a + b = 10; a + b = 12", "ninguna"),               # se contradicen
                        ("resolver: a + b = 10; 2 x a + 2 x b = 20",                   # dicen lo mismo: U.2 las junta (0 = 0)
                         "a = 0, b = 10; a = 1, b = 9; a = 2, b = 8; a = 3, b = 7; a = 4, b = 6; a = 5, b = 5; "
                         "a = 6, b = 4; a = 7, b = 3; a = 8, b = 2; a = 9, b = 1; a = 10, b = 0"),  # y prueba en orden
                        ("resolver: 0 x n = 5", "ninguna"),
                        ("resolver: 0 x n = 0", "todavia_no"),
                        ("resolver: 5 : 0", "no_se_puede"),
                        ("resolver: n x n = 49", "n = 7"),                    # no lineal: probar en orden (U.2)
                        ("resolver: n + 1 = 10000000", "n = 9999999"),        # cerca del techo
                        ("resolver: n - 1 = 10000000", "todavia_no"),         # se pasa del techo: sin reventar
                        ("resolver: 3 x n + 2 = n + 10", "n = 4"),                      # la letra a los dos lados: trozos
                        ("resolver: 12 : n = 3", "n = 4"),
                        ("x = -2; y = 3 x x", "x = -2, y = -6"),
                        ("resolver: a + b + c = 10", "todavia_no")):
        comprobar("D %s -> %s" % (q, esperado), P(q), esperado)

    print("\nE - NADA VIEJO CAMBIA (unas cuantas puertas de cada tipo)")
    for q, esperado in (("a + b = 30; a - b = 8", "a = 19, b = 11"),          # S.3 (la barra)
                        ("a + b = 1.001; a - b = 0", "a = 1001/2000, b = 1001/2000"),  # S.3 dice todavia no
                        # (diezmilesimas); desde U.2 la red de seguridad le da su oportunidad al resolvedor
                        ("a + b + c = 10", "todavia_no"),                     # E.5 (la letra tres veces)
                        ("3 x n = 13", "no_sale"),                            # E.5: no es entero
                        ("3 + 4 x 5", "23"),                                  # M.16
                        ("2.7 + 1.5", "4.2"),                                 # D.1
                        ("1/2 + 1/4", "3/4"),                                 # F.7
                        ("3 + + 4", "no_entiendo"),
                        ("silla,mesa", "varios_objetos")):
        comprobar("E %s -> %s (como antes)" % (q, esperado), P(q), esperado)

    print("\nF - LA COMPROBACION ES DE VERDAD (una pieza trucada no da respuesta)")
    mod = sys.modules[motor._DONDE_ESTA["_u_despejar"]]
    original = mod._u_despejar
    # (U.2: el despeje lo llama tambien el control de buscar.py: se truca en todas las partes que lo ven)
    partes = [m for n, m in list(sys.modules.items()) if n.startswith(mod.__name__.rsplit(".", 1)[0])
              and getattr(m, "_u_despejar", None) is original]

    def trucado(rel, letra, saber, pasos):
        v = original(rel, letra, saber, pasos)
        return motor._nu_sumar(v, ("+", 1, 1, "entero"), saber, [])            # da UNO DE MAS
    for m in partes:
        m._u_despejar = trucado
    try:
        for q in ("a + b = 1/2; a - b = 1/4", "3 x n = 4.5", "x + y + z = 40; x = y; z = 2 x y"):
            comprobar("F %s con el despeje trucado: no_cuadra" % q, motor.decidir_resolver(q, SABER)["conclusion"],
                      "no_cuadra")
    finally:
        for m in partes:
            m._u_despejar = original
    comprobar("F y sin trucar vuelve a salir", P("3 x n = 4.5"), "n = 1.5")

    print("\nG - EL TIEMPO (un humano no tarda; cada pregunta muy por debajo de 2 s)")
    for q in ("a + b = 1/2; a - b = 1/4", "x + y + z = 40; x = y; z = 2 x y", "resolver: 9999999 - 1 x 2 + 3/7"):
        t = time.time()
        P(q)
        d = time.time() - t
        comprobar("G %s (%.2f s)" % (q, d), d < 2, True)

    print("\n(%.1f s)" % (time.time() - t0))
    print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
    shutil.rmtree(TMP, ignore_errors=True)
    return 1 if MAL else 0


if __name__ == "__main__":
    sys.exit(main())
