# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.14: MULTIPLICAR TRES FACTORES Y EL VOLUMEN (NCETM 2.20; 5.MD.C.3-5).
El plan y sus trampas: diario/2026-10-07-paso-M14-tres-factores-volumen.md
Python solo aparece aqui como TESTIGO externo (los productos con * y el modulo decimal).
"""
import itertools
import os
import random
import shutil
import sys
import tempfile
import time
from decimal import Decimal

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)
TMP = tempfile.mkdtemp(prefix="m14_")
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


def TF(fs):
    r = motor.aplicar("multiplicar_tres", {"factores": [str(f) for f in fs]}, SABER)
    return r


def T(d):
    """El testigo: el decimal escrito sin ceros de mas ('1.20' -> '1.2', '6.0' -> '6')."""
    return format(Decimal(d).normalize(), "f")


def dec(n, k):
    s = str(n).rjust(k + 1, "0")
    return "%s.%s" % (s[:-k], s[-k:]) if k else s


print("=" * 78)
print("PASO M.14 - TRES FACTORES Y VOLUMEN  (%s)" % modo())
print("=" * 78)

try:
    print("\nA - LAS TRAMPAS DEL PLAN")
    comprobar("A1 2 x 3 x 4 = 24 (antes decia 'un_objeto')", S("2 x 3 x 4"), "24")
    comprobar("A2 25 x 7 x 4 = 700", S("25 x 7 x 4"), "700")
    r = TF([25, 7, 4])
    comprobar("A3 ... por la pareja facil (25 x 4 primero)",
              (r["pieza"]["id"], r["resultado"]["orden"][0]), ("tres_factores_buscando_la_pareja_facil", "25 x 4"))
    r = TF([7, 20, 3])
    comprobar("A4 7 x 20 x 3: las decenas justas al final (7 x 3 primero)", (r["valor"], r["resultado"]["orden"][0]),
              ("420", "7 x 3"))
    comprobar("A5 volumen: caja 5 x 3 x 2 cm = 30 (no 10 ni 31)", S("volumen: caja 5 x 3 x 2 cm"), "30 cm cubicos")
    comprobar("A6 volumen: cubo de 3 = 27 (no 26)", S("volumen: cubo de 3"), "27 unidades cubicas")
    salida = motor.explicar_pregunta("volumen: cubo de 3", SABER)
    comprobar("A7 ... y dice los cubitos de dentro (1) y los que se ven (26)",
              "dentro hay 1 x 1 x 1 = 1; desde fuera se ven 26" in salida, True)
    comprobar("A8 ... y que no es sumar las medidas", "NO es sumar las medidas (3 + 3 + 3 = 9)" in salida, True)
    comprobar("A9 unidades distintas: todavia no", S("volumen: caja 2 m x 30 cm x 4 cm"), "todavia_no")
    comprobar("A10 volumen: 5 x 3 x ? = 62 no sale", S("volumen: 5 x 3 x ? = 62"), "no_sale")
    comprobar("A11 volumen: 5 x 3 x ? = 60 -> 4", S("volumen: 5 x 3 x ? = 60"), "4")
    comprobar("A12 0.25 x 7 x 4 = 7", S("0.25 x 7 x 4"), "7")
    comprobar("A13 0.3 x 0.2 x 5: dos decimales, todavia no", S("0.3 x 0.2 x 5"), "todavia_no")
    r = TF([5, 0, 999])
    comprobar("A14 5 x 0 x 999 = 0 sin cuentas", (r["valor"], r["pieza"]["id"]), ("0", "tres_factores_con_un_cero"))
    comprobar("A15 100 x 100 x 100 = 1000000 (el techo)", S("100 x 100 x 100"), "1000000")
    # antes (techo en un millon): 100 x 100 x 101 -> todavia_no.  N.6: 1010000 ya cabe; se pasa 100 x 100 x 1001
    comprobar("A16 100 x 100 x 1001 se pasa de diez millones: todavia no", S("100 x 100 x 1001"), "todavia_no")
    comprobar("A17 verdad: 2 x 3 x 4 = 4 x 3 x 2 sin calcular", S("verdad: 2 x 3 x 4 = 4 x 3 x 2"), "verdadero")
    salida = motor.explicar_pregunta("verdad: 2 x 3 x 4 = 4 x 3 x 2", SABER)
    comprobar("A18 ... sin calcular de verdad", "No hace falta calcular" in salida, True)
    comprobar("A19 verdad: 2 x 3 x 4 = 2 x 3 x 5 -> FALSO", S("verdad: 2 x 3 x 4 = 2 x 3 x 5"), "falso")
    comprobar("A20 2 x 3 x 4 = 24 escrito directamente -> VERDADERO", S("2 x 3 x 4 = 24"), "verdadero")
    comprobar("A21 3 x ? x 4 = 60 (E.5) sigue igual", S("3 x ? x 4 = 60"), "5")
    salida = motor.explicar_pregunta("25 x 7 x 4", SABER)
    comprobar("A22 25 x 7 x 4 ensena que en el orden de siempre sale LO MISMO",
              "25 x 7 = 175, 175 x 4 = 700 ... SALE LO MISMO" in salida, True)

    print("\nB - CADA PIEZA SE COMPRUEBA CON LA OPERACION CONTRARIA (la vuelta de verdad)")
    base = motor.cargar_piezas()
    for fs, pid in ((["25", "7", "4"], "tres_factores_buscando_la_pareja_facil"),
                    (["2", "3", "7"], "tres_factores_en_orden"),
                    (["5", "0", "9"], "tres_factores_con_un_cero"),
                    (["0", "0", "0"], "tres_factores_con_un_cero")):
        r = motor.aplicar(pid, {"factores": fs}, SABER)
        res = r.get("resultado", {})
        comprobar("B %s: %s con vuelta dividiendo (o sin dividir entre cero)" % (pid, " x ".join(fs)),
                  (r["conclusion"], bool(res.get("vuelta")), res.get("vuelta_ok")), ("hecho", True, True))
    # la vuelta CAZA un producto falso: se le da 701 en vez de 700
    for pid in ("tres_factores_buscando_la_pareja_facil", "tres_factores_en_orden"):
        p = base["piezas"][pid]
        u = motor._Lo_que_puede_usar(p, base, SABER)
        vuelta = p["hacer"].__globals__["_vuelta"]
        try:
            _, ok = vuelta(u, "701", ["25", "7", "4"])
        except ValueError:
            ok = False
        comprobar("B %s: la vuelta NO da por bueno 25 x 7 x 4 = 701" % pid, ok, False)
        texto, ok = vuelta(u, "700", ["25", "7", "4"])
        comprobar("B %s: y si da por bueno 700 (%s)" % (pid, texto), ok, True)

    print("\nC - DOMINIO: tres factores de 0 a 12, contra el testigo")
    azar = random.Random(20261007)
    trios = [t for t in itertools.product(range(13), repeat=3) if 0 in t or 1 in t or 10 in t or 12 in t
             or len(set(t)) == 1]
    trios = sorted(set(trios) | set(azar.sample(list(itertools.product(range(13), repeat=3)), 300)))
    malos, t0, lento = [], time.time(), 0.0
    for t in trios:
        t1 = time.time()
        r = TF(t)
        lento = max(lento, time.time() - t1)
        if r["conclusion"] != "hecho" or r["valor"] != str(t[0] * t[1] * t[2]):
            malos.append((t, r.get("valor"), r.get("porque")))
    print("        %d trios en %.1f s (el mas lento %.2f s)" % (len(trios), time.time() - t0, lento))
    comprobar("C1 todos los trios de la muestra dan el producto del testigo", malos[:3], [])
    comprobar("C2 ninguno tarda mas de 2 s", lento < 2, True)

    print("\nD - DOMINIO: los mismos factores en los 6 ordenes dan lo mismo (conmutativa y asociativa)")
    malos = []
    for t in azar.sample(trios, 40) + [(25, 7, 4), (5, 13, 2), (50, 3, 2), (125, 3, 8)]:
        vals = {TF(list(o)).get("valor") for o in itertools.permutations(t)}
        if vals != {str(t[0] * t[1] * t[2])}:
            malos.append((t, vals))
    comprobar("D1 44 trios x 6 ordenes: siempre el mismo producto", malos, [])

    # hasta aqui, con la memoria VACIA.  Desde aqui, como en el PC de Carlos: con las tablas aprendidas
    # (la division corta de la vuelta las necesita, M.11)
    motor.aprender("tablas", SABER)
    print("\nE - DOMINIO: numeros de dos y tres cifras (cerca del millon), contra el testigo")
    malos, hechos, nos, t0, lento = [], 0, 0, time.time(), 0.0
    casos = [(azar.randint(2, 99), azar.randint(2, 99), azar.randint(2, 9)) for _ in range(80)]
    casos += [(azar.randint(10, 999), azar.choice([2, 4, 5, 8, 10, 20, 25, 50, 100]), azar.randint(2, 99))
              for _ in range(80)]
    for t in casos:
        t1 = time.time()
        r = TF(t)
        lento = max(lento, time.time() - t1)
        if r["conclusion"] == "hecho":
            hechos += 1
            if r["valor"] != str(t[0] * t[1] * t[2]):
                malos.append((t, r["valor"]))
        else:
            nos += 1
            if t[0] * t[1] * t[2] <= 1000000 and "division larga" not in (r.get("porque") or ""):
                malos.append((t, r["conclusion"], r.get("porque")))
    print("        %d trios: %d hechos, %d todavia no (se pasan del techo o la vuelta pide la division larga); "
          "%.1f s, el mas lento %.2f s" % (len(casos), hechos, nos, time.time() - t0, lento))
    comprobar("E1 nunca un producto falso; un 'todavia no' solo por el techo o la division larga", malos[:3], [])
    comprobar("E2 la gran mayoria sale (mas de 140 de 160)", hechos > 140, True)
    comprobar("E3 ninguno tarda mas de 2 s", lento < 2, True)

    print("\nF - DOMINIO: con UN decimal (una, dos y tres cifras decimales), contra el testigo")
    malos, hechos, total = [], 0, 0
    for k in (1, 2, 3):
        for _ in range(40):
            d = dec(azar.randint(1, 10 ** (k + 1)), k)
            a, b = azar.randint(1, 9), azar.choice([2, 4, 5, 6, 8, 10])
            fs = [d, str(a), str(b)]
            azar.shuffle(fs)
            total += 1
            r = TF(fs)
            esperado = T(Decimal(d) * a * b)
            if r["conclusion"] == "hecho":
                hechos += 1
                if r["valor"] != esperado:
                    malos.append((fs, r["valor"], esperado))
    print("        %d productos con un decimal: %d hechos" % (total, hechos))
    comprobar("F1 nunca un producto falso con un decimal", malos[:3], [])
    comprobar("F2 casi todos salen (mas de 100 de 120)", hechos > 100, True)

    print("\nG - EL VOLUMEN: cajas, cubos, figuras de varias cajas y el problema inverso, contra el testigo")
    malos = []
    for _ in range(40):
        l, a, h = azar.randint(1, 12), azar.randint(1, 12), azar.randint(1, 12)
        if S("volumen: caja %d x %d x %d cm" % (l, a, h)) != "%d cm cubicos" % (l * a * h):
            malos.append((l, a, h))
    comprobar("G1 40 cajas", malos, [])
    malos = [n for n in range(1, 13) if S("volumen: cubo de %d m" % n) != "%d m cubicos" % (n * n * n)]
    comprobar("G2 los cubos de 1 a 12", malos, [])
    malos = []
    for _ in range(20):
        c1 = [azar.randint(1, 9) for _ in range(3)]
        c2 = [azar.randint(1, 9) for _ in range(3)]
        esperado = c1[0] * c1[1] * c1[2] + c2[0] * c2[1] * c2[2]
        if S("volumen: %d x %d x %d + %d x %d x %d" % tuple(c1 + c2)) != "%d unidades cubicas" % esperado:
            malos.append((c1, c2))
    comprobar("G3 20 figuras de dos cajas (se suman)", malos, [])
    malos, nos = [], 0
    for _ in range(40):
        l, a, h = azar.randint(1, 12), azar.randint(1, 12), azar.randint(1, 12)
        V = l * a * h
        sitio = azar.randint(0, 2)
        m = [str(l), str(a), str(h)]
        m[sitio] = "?"
        if S("volumen: %s x %s x %s = %d" % (m[0], m[1], m[2], V)) != str([l, a, h][sitio]):
            malos.append((m, V))
        # y uno mas: ya no sale exacto (o sale con decimales, que se comprueban)
        r = S("volumen: %s x %s x %s = %d" % (m[0], m[1], m[2], V + 1))
        if r not in ("no_sale",):
            otros = [x for x in (l, a, h)]
            otros.pop(sitio)
            if Decimal(r) * otros[0] * otros[1] != V + 1:
                malos.append((m, V + 1, r))
        else:
            nos += 1
    print("        40 huecos exactos; 40 con el volumen + 1 (%d no salen ni en milesimas)" % nos)
    comprobar("G4 el problema inverso: dividir uno a uno, y comprobar multiplicando", malos, [])
    comprobar("G5 con decimal: volumen: caja 2.5 x 4 x 3 m = 30", S("volumen: caja 2.5 x 4 x 3 m"), "30 m cubicos")

    print("\nH - LA IGUALDAD CON TRES FACTORES")
    malos = []
    for _ in range(30):
        t = [azar.randint(1, 12) for _ in range(3)]
        o = list(t)
        azar.shuffle(o)
        if S("verdad: %d x %d x %d = %d x %d x %d" % tuple(t + o)) != "verdadero":
            malos.append((t, o))
        cambiado = list(o)
        cambiado[0] = cambiado[0] + 1
        esperado = "verdadero" if t[0] * t[1] * t[2] == cambiado[0] * cambiado[1] * cambiado[2] else "falso"
        if S("verdad: %d x %d x %d = %d x %d x %d" % tuple(t + cambiado)) != esperado:
            malos.append((t, cambiado))
        if S("verdad: %d x %d x %d = %d" % (t[0], t[1], t[2], t[0] * t[1] * t[2])) != "verdadero":
            malos.append(t)
    comprobar("H1 90 igualdades (mismos factores, uno cambiado, el producto)", malos, [])

    print("\nI - CERCA DEL TECHO (un millon) y el TIEMPO")
    for texto, esperado in (("100 x 100 x 100", "1000000"), ("125 x 8 x 1000", "1000000"),
                            ("999 x 1000 x 1", "999000"), ("999 x 999 x 1", "todavia_no"),
                            ("2 x 500000 x 1", "1000000"), ("2 x 500001 x 1", "1000002"), ("2 x 5000001 x 1", "todavia_no"),   # N.6
                            ("1.125 x 8 x 111", "999"), ("6 x 8 x 0.37", "17.76"), ("0.5 x 7 x 20", "todavia_no"), ("0.001 x 7 x 4", "0.028"), ("0.375 x 8 x 9", "27"),
                            ("2 x 3 x 4 x 5", "120"), ("13 x 17 x 19", "todavia_no"),
                            ("volumen: cubo de 100 cm", "1000000 cm cubicos"),
                            ("volumen: cubo de 101 cm", "todavia_no")):
        t1 = time.time()
        r = S(texto)
        dt = time.time() - t1
        comprobar("I %s -> %s (%.2f s)" % (texto, esperado, dt), (r, dt < 2), (esperado, True))

    print("\nJ - LOS DOS ARREGLOS (al medir el tiempo): la mitad por sitios; no saltar mil veces")
    for texto, esperado in (("1000000 : 2", "500000"), ("999999 : 2", "499999 resto 1"), ("846 : 2", "423"),
                            ("1000000 : 8", "125000")):
        t1 = time.time()
        r = S(texto)
        dt = time.time() - t1
        comprobar("J %s -> %s en menos de 2 s (%.2f s; antes 15 s)" % (texto, esperado, dt), (r, dt < 2), (esperado, True))
    r = motor.aplicar("dividir", {"total": 999999, "divisor": 2}, SABER)
    comprobar("J la mitad por sitios se comprueba doblando (499999 + 499999 + 1)",
              (r["pieza"]["id"], r["resultado"]["vuelta_ok"], r["resultado"]["vuelta"]),
              ("dividir_a_la_mitad", True, "499999 + 499999 + 1 = 999999"))
    malos = [n for n in range(101, 3000, 37) if motor.aplicar("dividir", {"total": n, "divisor": 2}, SABER)["valor"] != n // 2
             or motor.aplicar("dividir", {"total": n, "divisor": 2}, SABER)["resultado"]["resto"] != n % 2]
    comprobar("J 80 mitades por sitios contra el testigo", malos, [])
    r = motor.aplicar("dividir_saltando", {"total": 100000, "divisor": 4}, SABER)
    comprobar("J dividir_saltando ya no da 25 000 saltos de 4", (r["conclusion"], "mas de mil saltos" in r.get("porque", "")),
              ("no_salio", True))
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\nTOTAL: %d/%d" % (BIEN, BIEN + MAL))
