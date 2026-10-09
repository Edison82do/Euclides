# -*- coding: utf-8 -*-
"""
PRUEBAS DEL ARREGLO A.1: EL CERO AL DESPEJAR (prudencia de Carlos: nunca una respuesta falsa).
El plan, la tabla de lo que respondia antes y las causas: diario/2026-10-09-arreglo-A1-el-cero-al-despejar.md
Pocas y representativas.  Python (Fraction) solo aparece aqui como TESTIGO externo.
"""
import os
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
TMP = tempfile.mkdtemp(prefix="a1_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia
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


def E(t):
    return motor.explicar_pregunta(t, SABER)


# ------------------------------------------------------------- el TESTIGO (solo aqui)

def _testigo_valor(t, valores):
    py = re.sub(r"(\d+)", r"Fraction(\1)", t.replace(" x ", " * ").replace(" : ", " / "))
    try:
        return eval(py, {"Fraction": Fraction}, dict(valores))
    except ZeroDivisionError:
        return None


def _testigo_cumple(q, valores):
    for rel in q.split(";"):
        izq, der = rel.split("=")
        a, b = _testigo_valor(izq, valores), _testigo_valor(der, valores)
        if a is None or b is None or a != b:
            return False
    return True


def falsa(q, res, letras=("r",), hasta=25):
    """Por que la respuesta es FALSA (con numeros para contar, de 0 a 'hasta'), o None si no lo es."""
    import itertools
    dominio = [Fraction(n) for n in range(hasta)]
    sols = [dict(zip(letras, v)) for v in itertools.product(dominio, repeat=len(letras))
            if _testigo_cumple(q, dict(zip(letras, v)))]
    todas = len(dominio) ** len(letras)
    if res == "ninguna":
        return "dice ninguna y hay %s" % sols[0] if sols else None
    if res == "cualquiera":
        return None if len(sols) == todas else "dice cualquiera y no vale para todos"
    if res.startswith(letras[0] + " ="):
        dados = [dict((x.split("=")[0].strip(), Fraction(x.split("=")[1].strip())) for x in s.split(","))
                 for s in res.split(";")]
        if any(not _testigo_cumple(q, d) for d in dados):
            return "da un valor que no cumple"
        if len(sols) == todas:
            return "da valores sueltos y vale cualquiera"
        if len(sols) > len(dados):
            return "faltan soluciones: %s" % sols[:4]
    return None                                          # todavia_no, no_sale, no_cuadra...: no afirma nada falso


def main():
    t0 = time.time()
    print("=" * 78)
    print("A - LAS QUE ERAN FALSAS (por resolver:)")
    for q, esperado in (("0 : r = 0 : 5", "todavia_no"),            # era 'ninguna': vale cualquier r menos el 0
                        ("0 : 5 = 0 : r", "todavia_no"),
                        ("0 : r = 0", "todavia_no"),
                        ("0 : (r - 2) = 0", "todavia_no"),          # cualquiera menos el 2
                        ("0 : r + 3 = 3", "todavia_no"),
                        ("a : b = 0; a = 0", "todavia_no"),
                        ("(r - 2) x (r - 2) = 1", "r = 1; r = 3"),  # era 'ninguna' (el tope paraba en r = 0)
                        ("(r - 2) x (r - 2) = 0", "r = 2"),
                        ("0 : (a - b) = 0; a + b = 3", "a = 3, b = 0; a = 2, b = 1; a = 1, b = 2; a = 0, b = 3")):
        comprobar("A resolver: %s -> %s" % (q, esperado), S("resolver: " + q), esperado)
    t = E("resolver: 0 : (r - 2) = 0")
    comprobar("A el porque dice cual es el que no vale: 'CUALQUIER numero menos el 2'",
              "CUALQUIER numero menos el 2" in t, True)
    comprobar("A 0 : (r x 0) = 0: lo de detras es 0 siempre -> ninguna (no 'cualquiera menos...')",
              S("resolver: 0 : (r x 0) = 0"), "ninguna")

    print("\nB - LAS QUE ERAN FALSAS POR LAS PUERTAS VIEJAS (sin orden: E.5 y la equivalencia de M.12)")
    for q, esperado in (("0 : r = 0 : 5", "todavia_no"),            # era 'r = 5' (la equivalencia con el 0)
                        ("0 x r = 0 x 5", "cualquiera"),            # era 'r = 5'
                        ("r x 0 = 5 x 0", "cualquiera"),
                        ("0 : r = 3", "ninguna")):                  # la explicacion decia 'r = 0' (y no cuadraba)
        comprobar("B %s -> %s" % (q, esperado), S(q), esperado)
    for q in ("0 : r = 3", "r : 0 = 5 : 0", "0 : r = 0 : 0"):
        t = E(q)
        comprobar("B la explicacion de %s no da un numero que no cuadra" % q,
                  re.search(r"RESULTADO: r = \d", t) is None, True)
    t = E("ecuacion: 0 : n = 0")
    comprobar("B ecuacion: 0 : n = 0 (E.5) -> todavia no, con su porque",
              ("RESULTADO: todavia_no" in t, "CUALQUIER numero" in t), (True, True))

    print("\nC - LO QUE NO CAMBIA (las que ya estaban bien)")
    for q, esperado in (("resolver: 0 x r = 0", "cualquiera"), ("resolver: r x 0 = 5", "ninguna"),
                        ("resolver: 5 : r = 0", "ninguna"), ("resolver: r : r = 1", "todavia_no"),
                        ("resolver: (r - 2) : (r - 2) = 1", "todavia_no"), ("resolver: 6 : r = 2", "r = 3"),
                        ("resolver: 6 : (r - 2) = 3", "r = 4"), ("resolver: r x (r - 2) = 0", "r = 0; r = 2"),
                        ("resolver: r x r = 1", "r = 1"), ("resolver: a x b = 6; a - b = 1", "a = 3, b = 2"),
                        ("resolver: a x b = 0; a + b = 3", "a = 3, b = 0; a = 0, b = 3"),
                        ("resolver: r : 0 = 5", "ninguna"), ("resolver: 2 : 5 = 6 : r", "r = 15"),
                        ("24 x 5 = 12 x r", "10"), ("180 : 20 = 18 : r", "2"), ("12 x r = 12 x 7", "7")):
        comprobar("C %s -> %s" % (q, esperado), S(q), esperado)

    print("\nD - EL TESTIGO: ninguna respuesta FALSA en una muestra de la familia (0, x y :)")
    lados = ["0 : r", "0 : (r - 2)", "0 x r", "r x 0", "r : r", "5 : r", "r : 5", "(r - 2) x (r - 2)", "r x (r - 3)",
             "(r - 1) : (r - 1)", "0 : (r x 0)", "(0 x r) : 5", "0 : r + 3"]
    otros = ["0", "1", "3", "0 : 5", "0 x 5", "0 : r"]
    malas = []
    for pre in ("resolver: ", ""):
        for a in lados:
            for b in otros:
                q = "%s = %s" % (a, b)
                por = falsa(q, S(pre + q))
                if por:
                    malas.append((pre + q, por))
    for q in ("a : b = 0; a = 0", "a x b = 0; b = 0", "0 : (a - b) = 0; a + b = 3", "0 : a = 0 : b; a = 2",
              "a x 0 = b x 0; a + b = 2", "a x b = 0; a = b"):
        por = falsa(q, S("resolver: " + q), ("a", "b"), 8)
        if por:
            malas.append((q, por))
    comprobar("D %d relaciones con una letra (por resolver: y sin orden) y 6 con dos: ninguna falsa"
              % (2 * len(lados) * len(otros)), malas, [])

    print("\nE - EL TIEMPO (cada pregunta muy por debajo de 2 s)")
    for q in ("resolver: 0 : (r - 2) = 0", "resolver: (r - 2) x (r - 2) = 1", "0 : r = 0 : 5",
              "resolver: 0 : (a - b) = 0; a + b = 3"):
        t1 = time.time()
        S(q)
        d = time.time() - t1
        comprobar("E %s (%.2f s)" % (q, d), d < 2, True)

    print("\n(%.1f s)" % (time.time() - t0))
    print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
    shutil.rmtree(TMP, ignore_errors=True)
    return 1 if MAL else 0


if __name__ == "__main__":
    sys.exit(main())
