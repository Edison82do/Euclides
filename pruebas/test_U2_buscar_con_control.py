# -*- coding: utf-8 -*-
"""
PRUEBAS DE LA FASE U.2 DEL PLAN U: BUSCAR CON CONTROL.
El plan y sus trampas: diario/2026-10-08-paso-U2-buscar-con-control.md
Pocas y representativas (decision de Carlos para lo nuevo).  Python solo aparece aqui como TESTIGO externo.
"""
import itertools
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
TMP = tempfile.mkdtemp(prefix="u2_")
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
    """Lo que contesta el probador."""
    return probar.preguntar(t, SABER)[0]


def X(t):
    """La explicacion entera."""
    return motor.explicar_pregunta(t, SABER)


# ------------------------------------------------------------------ el TESTIGO (Python, solo aqui)

def _relaciones(texto):
    t = re.sub(r"^resolver\s*:?\s*", "", texto)
    return [r.split("=") for r in t.split(";")]


def _vale(expr, valores):
    e = re.sub(r"(?<=[\w)])\s+x\s+(?=[\w(])", " * ", expr).replace(":", "/")       # la x entre dos cosas es POR
    trozos = []
    for t in re.findall(r"\d+(?:\.\d+)?|[a-z]|.", e):
        if t[0].isdigit():
            trozos.append("Fraction('%s')" % t)
        elif t.isalpha():
            trozos.append("Fraction('%s')" % valores[t])
        else:
            trozos.append(t)
    return eval("".join(trozos), {"Fraction": Fraction})


def cumple(texto, valores):
    return all(_vale(a, valores) == _vale(b, valores) for a, b in _relaciones(texto))


def leer_respuesta(resp):
    """'a = 4, b = 6; a = 6, b = 4' -> [{'a': '4', 'b': '6'}, ...]"""
    out = []
    for sol in resp.split(";"):
        out.append(dict((p.split("=")[0].strip(), p.split("=")[1].strip()) for p in sol.split(",")))
    return out


def a_mano(texto, letras, hasta):
    """El testigo prueba TODAS las combinaciones de enteros de 0 a 'hasta' (fuerza bruta)."""
    sols = []
    for vs in itertools.product(range(hasta + 1), repeat=len(letras)):
        v = dict(zip(letras, [str(x) for x in vs]))
        try:
            if cumple(texto, v):
                sols.append(v)
        except ZeroDivisionError:
            pass
    return sorted(tuple(sorted(s.items())) for s in sols)


def como_conjunto(resp):
    return sorted(tuple(sorted(s.items())) for s in leer_respuesta(resp))


def main():
    t0 = time.time()
    print("PRUEBA: FASE U.2 - BUSCAR CON CONTROL")
    print("=" * 60)

    print("\nA - LOS OPERADORES NUEVOS (contra el testigo)")
    q = "resolver: a + b = 30; a - b = 8"
    comprobar("A1 juntar: %s" % q, P(q), "a = 19, b = 11")
    comprobar("A1b ... las RESTA (la a tiene los mismos trozos): quedan 2 trozos de b", "las RESTO" in X(q)
              and "[b][b] = 22" in X(q), True)
    q = "resolver: 2 x a + 2 x b = 20; a - b = 2"
    comprobar("A2 juntar K veces: %s" % q, P(q), "a = 6, b = 4")
    comprobar("A2b ... le quita 2 veces la otra", "QUITO 2 veces" in X(q), True)
    q = "resolver: 2 x a + 3 x b = 13; 2 x a + b = 8"
    r = P(q)
    comprobar("A3 juntar con fracciones (el testigo lo comprueba): %s -> %s" % (q, r), cumple(q, leer_respuesta(r)[0]),
              True)
    q = "resolver: (x + y) x z = 21; x + y = 7"
    r = P(q)
    comprobar("A4 reescribir: el BLOQUE x + y ya se sabe -> z = 3 en todas", "BLOQUE x + y" in X(q)
              and all(s["z"] == "3" for s in leer_respuesta(r)), True)
    comprobar("A4b ... y x, y probando en orden = el testigo", como_conjunto(r), a_mano(q, ["x", "y", "z"], 7))
    q = "resolver: 2 x a + 4 x b = 20"
    comprobar("A5 reescribir: saca FACTOR COMUN (2)", "FACTOR COMUN" in X(q), True)
    comprobar("A5b ... y prueba en orden: las de enteros = el testigo", como_conjunto(P(q)), a_mano(q, ["a", "b"], 10))
    comprobar("A6 probar en orden: n x n = 49", P("resolver: n x n = 49"), "n = 7")
    comprobar("A6b n x n = 50 -> ninguna (con numeros para contar)", P("resolver: n x n = 50"), "ninguna")
    comprobar("A6c n x n + n = 30 (la letra por si misma y suelta)", P("resolver: n x n + n = 30"), "n = 5")
    q = "resolver: a x b = 24; a + b = 10"
    comprobar("A7 probar en orden: %s = el testigo" % q, como_conjunto(P(q)), a_mano(q, ["a", "b"], 10))
    q = "resolver: a x b = 12; a x c = 8; b + c = 5"
    comprobar("A8 dos relaciones no lineales: %s = el testigo" % q, como_conjunto(P(q)), a_mano(q, ["a", "b", "c"], 12))
    q = "resolver: x + y + z = 12; x - y = 2; x x y = 15"
    comprobar("A9 tres letras, una no lineal: %s = el testigo" % q, como_conjunto(P(q)), a_mano(q, ["x", "y", "z"], 12))

    print("\nB - EL CONTROL (medios y fines, con presupuesto)")
    x = X("resolver: a + b = 30; a - b = 8")
    comprobar("B1 juntar y sustituir dejan 1 letra: ELIGE juntar (mas barato) y lo dice",
              "ELIJO juntar relaciones" in x and "sustituir -> deja 1 letra" in x, True)
    x = X("resolver: x + y + z = 40; x = y; z = 2 x y")
    comprobar("B2 una letra sola en un lado (x = y): sustituir es lo mas barato",
              x.split("  1. ")[1].startswith("SUSTITUYO"), True)
    comprobar("B3 probar en orden solo cuando nada mas baja las letras", "PRUEBO EN ORDEN" in x, False)
    x = X("resolver: n x n = 2000000")
    comprobar("B4 el tope de pruebas: n x n = 2000000 -> todavia no", P("resolver: n x n = 2000000"), "todavia_no")
    comprobar("B4b ... y dice por que", "un humano no prueba tantas" in x, True)
    comprobar("B5 se para cuando YA SE PASA (n = 8: 64)", "n = 8: n x n ya da 64" in X("resolver: n x n = 49"), True)
    comprobar("B6 sin tope para probar: a - b = 3 -> todavia no", P("resolver: a - b = 3"), "todavia_no")
    comprobar("B7 se contradicen: ninguna", P("resolver: a + b = 10; a + b = 12"), "ninguna")
    comprobar("B8 probar con una letra no basta (a + b + c = 10): todavia no", P("resolver: a + b + c = 10"), "todavia_no")

    print("\nC - LOS DOS FALLOS DE LA REVISION DE U.1 (de forma general)")
    comprobar("C1 S.3 dice todavia no (demasiadas pruebas); el resolvedor junta",
              P("a + b = 500; 2 x a + 5 x b = 1600"), "a = 300, b = 200")
    comprobar("C1b ... y lo dice", "la puerta vieja decia: TODAVIA NO" in X("a + b = 500; 2 x a + 5 x b = 1600"), True)
    comprobar("C2 tres letras y una no lineal, sin la orden", P("x + y + z = 12; x - y = 2; x x y = 15"),
              "x = 5, y = 3, z = 4")
    comprobar("C3 una cuenta sin letras sigue respetando el ano: 2 x 3 - 4 x 5 (se baja de cero)", P("2 x 3 - 4 x 5"), "todavia_no")
    comprobar("C3b 12 : 3 + 1 ya es del ano desde M.22 (NCETM 2.28)", P("12 : 3 + 1"), "5")
    comprobar("C4 probando solo sale 'ninguna con enteros': se queda lo de la puerta vieja",
              P("a x b + a = 10; a - b = 1"), "todavia_no")
    comprobar("C5 'de' es POR: 3/4 de 20", P("3/4 de 20"), "15")
    comprobar("C5b resolver: 3/4 de 20", P("resolver: 3/4 de 20"), "15")
    comprobar("C5c resolver: 1/2 de n = 6", P("resolver: 1/2 de n = 6"), "n = 12")
    comprobar("C5d resolver: 0.5 de n = 3 (un decimal)", P("resolver: 0.5 de n = 3"), "n = 6")
    comprobar("C5e entre dos enteros 'de' no es nada: 3 de 4", P("resolver: 3 de 4"), "no_entiendo")

    print("\nD - LOS TRADUCTORES AL MODELO (las respuestas no cambian)")
    comprobar("D1 S.3 lee con el lector unico (ya no tiene lector propio)",
              hasattr(motor, "_di_tokens") or not hasattr(motor, "_di_relacion"), False)
    x = X("a + b = 30; a - b = 8")
    comprobar("D1b S.3 sigue siendo S.3 (la barra) con la misma respuesta",
              "PREGUNTA (S.3)" in x and x.strip().endswith("RESULTADO: a = 19, b = 11"), True)
    comprobar("D1c S.3: a x b = 24; a + b = 10 sigue igual", P("a x b = 24; a + b = 10"), "a = 4, b = 6; a = 6, b = 4")
    x = X("perimetro: 30; lados: 8, 7, 6, ?")
    comprobar("D2 S.2: el modelo (30 = 8 + 7 + 6 + ?) da LO MISMO", "el MODELO, U.2: 30 = 8 + 7 + 6 + ?" in x
              and "sale 9 ... LO MISMO" in x and x.strip().endswith("RESULTADO: 9 cm"), True)
    x = X("todo: 24; 4 partes iguales")
    comprobar("D2b S.2 partes iguales: la MISMA letra (24 = p + p + p + p)", "24 = p + p + p + p" in x
              and "sale 6 ... LO MISMO" in x, True)

    print("\nE - EL TIEMPO (un humano no tarda; cada pregunta por debajo de 3 s)")
    for q in ("resolver: a x b = 12; a x c = 8; b + c = 5", "resolver: a x b = 24", "a + b = 500; 2 x a + 5 x b = 1600"):
        t = time.time()
        P(q)
        d = time.time() - t
        comprobar("E %s (%.2f s)" % (q, d), d < 3, True)

    print("\n(%.1f s)" % (time.time() - t0))
    print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
    shutil.rmtree(TMP, ignore_errors=True)
    return 1 if MAL else 0


if __name__ == "__main__":
    sys.exit(main())
