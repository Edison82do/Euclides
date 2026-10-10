# -*- coding: utf-8 -*-
"""
PRUEBAS DEL PASO M.23: EL VALOR DE POSICION DE LOS DECIMALES - x Y : POR 10, 100 Y 1000, Y CAMBIAR DE UNIDAD
(NCETM 2.29, 'Decimal place-value knowledge, multiplication and division').
El plan y sus trampas: diario/2026-10-10-paso-M23-decimales-por-10-100-1000.md
Pocas y representativas (decision de Carlos).  Las cifras se mueven (punto 1): dos PIEZAS de las preguntas que ya
existian (multiplicar_decimal, dividir_decimal), que el resolvedor pide.  Cambiar de unidad (punto 2): las
equivalencias de las medidas en DATOS (relaciones.kn), una relacion mas en el modelo comun.  Python solo aparece aqui
como TESTIGO externo.
"""
import importlib.util
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
TMP = tempfile.mkdtemp(prefix="m23_")
os.environ["EUCLIDES_MEMORIA"] = os.path.join(TMP, "hechos.txt")      # memoria vacia
import motor  # noqa: E402
import probar  # noqa: E402

BIEN = MAL = 0
POR = "decimal_por_10_100_1000_moviendo_las_cifras"
ENTRE = "entre_10_100_1000_moviendo_las_cifras"


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


def escrito(w):
    """El testigo escrito como lo escribe Euclides: sin ceros de mas ('4500', '0.035')."""
    t = format(w.normalize(), "f")
    return t.rstrip("0").rstrip(".") if "." in t else t


def decimal_al_azar(azar):
    k = azar.randint(1, 3)
    e = azar.choice(["0", "%d" % azar.randint(1, 9), "%d" % azar.randint(10, 999)])
    d = "".join(azar.choice("0123456789") for _ in range(k - 1)) + azar.choice("123456789")
    return "%s.%s" % (e, d)


def modulo(nombre, cambiar):
    """La pieza leida de su archivo y TRUCADA: 'cambiar' = (lo que hay, lo que se pone), solo la PRIMERA vez."""
    src = open(os.path.join(PIEZAS, nombre + ".py"), encoding="utf-8").read()
    assert cambiar[0] in src, cambiar[0]
    src = src.replace(cambiar[0], cambiar[1], 1)
    ruta = os.path.join(TMP, nombre + ".py")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(src)
    sp = importlib.util.spec_from_file_location("m23_" + nombre, ruta)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def main():
    t0 = time.time()
    azar = random.Random(2029)
    print("=" * 78)
    print("PASO M.23: x Y : POR 10, 100 Y 1000 MOVIENDO LAS CIFRAS; CAMBIAR DE UNIDAD (NCETM 2.29)")
    print("=" * 78)

    print("\nA - POR 10, 100 O 1000 (punto 1): las cifras suben; contra el testigo, con su vuelta")
    malas, n = [], 0
    for _ in range(30):
        x, p = decimal_al_azar(azar), azar.choice(["10", "100", "1000"])
        n += 1
        r = motor.aplicar("multiplicar_decimal", {"x": x, "y": p} if azar.random() < 0.5 else {"x": p, "y": x}, SABER)
        if r["conclusion"] != "hecho" or r["valor"] != escrito(Decimal(x) * Decimal(p)) or r["pieza"]["id"] != POR \
                or not r["resultado"]["vuelta_ok"]:
            malas.append((x, p, r.get("valor")))
    comprobar("A %d productos al azar: el valor del testigo, la pieza que mueve las cifras y su vuelta" % n, malas, [])

    print("\nB - ENTRE 10, 100 O 1000 (punto 1): las cifras bajan (tambien un ENTERO); mas de tres decimales, todavia no")
    malas, n, todavia = [], 0, 0
    for _ in range(30):
        x = decimal_al_azar(azar) if azar.random() < 0.5 else "%d" % azar.randint(1, 99999)
        p = azar.choice(["10", "100", "1000"])
        w = Decimal(x) / Decimal(p)
        r = motor.aplicar("dividir_decimal", {"x": x, "d": p}, SABER)
        n += 1
        if -w.normalize().as_tuple().exponent > 3:          # el testigo pasa de las milesimas
            todavia += 1
            if r["conclusion"] == "hecho":
                malas.append((x, p, r.get("valor")))
        elif r["conclusion"] != "hecho" or r["valor"] != escrito(w) or r["pieza"]["id"] != ENTRE \
                or not r["resultado"]["vuelta_ok"]:
            malas.append((x, p, r.get("valor")))
    comprobar("B %d divisiones al azar (%d pasan de las milesimas): como el testigo, con su vuelta" % (n, todavia),
              malas, [])

    print("\nC - POR LA PUERTA VIEJA (sin tocarla): el control coge la pieza mas barata; las viejas quedan detras")
    for q, esperado in (("4.5 x 1000", "4500"), ("1000 x 0.037", "37"), ("0.3 x 10", "3"), ("3.5 : 100", "0.035"),
                        ("2.75 x 100", "275"), ("60.4 x 1000", "60400"), ("3.5 : 1000", "todavia_no"),
                        ("12.6 : 1000", "todavia_no")):
        comprobar("C %s -> %s" % (q, esperado), S(q), esperado)
    r = motor.aplicar("dividir_decimal", {"x": "3.5", "d": "10"}, SABER)
    otras = [c["id"] for c in r.get("candidatos", []) if c.get("id") and not c.get("descartado")]
    comprobar("C 3.5 : 10: elige mover las cifras (1.5); la pieza de M.13 tambien encajaba",
              (r["pieza"]["id"], "dividir_decimal_por_10_o_100" in otras), (ENTRE, True))
    t = X("4.5 x 1000")
    comprobar("C la explicacion: cada cifra sube TRES sitios (4 unidades -> 4 millares) y lo comprueba bajandolas",
              "TRES sitios" in t and "4 unidades -> 4 millares" in t and "5 decimas -> 5 centenas" in t
              and "4500 : 1000 = 4.5" in t and "... SI" in t, True)

    print("\nD - LAS TRAMPAS: piezas TRUCADAS (la vuelta las caza)")
    base = motor.cargar_piezas()
    trampas = (
        (POR, ("        _subir(delante, detras)\n    valor", "        detras.append(('0', None))\n    valor"),
         {"x": "4.5", "y": "100"}, "anadir ceros (4.5 x 100 = 4.500)"),
        (POR, ("for _ in por[1:]:", "for _ in por[2:]:"),
         {"x": "0.037", "y": "1000"}, "contar mal los sitios (0.037 x 1000 = 3.7)"),
        (ENTRE, ("        _bajar(delante, detras)\n    valor", "        _subir(delante, detras)\n    valor"),
         {"x": "3.5", "d": "100"}, "mover hacia el lado que no es (3.5 : 100 = 350)"),
        (ENTRE, ('e = "".join(c for c, _ in delante).lstrip("0") or "0"', 'e = "".join(c for c, _ in delante) or "0"'),
         {"x": "375", "d": "1000"}, "dejar los ceros escritos donde no van"),
    )
    for pid, cambio, s, que in trampas:
        u = motor._Lo_que_puede_usar(base["piezas"][pid], base, SABER)
        try:
            res = modulo(pid, cambio).hacer(s, u)
            cazado = res["vuelta_ok"] is False or res["valor"] != {"4.5": "450", "0.037": "37", "3.5": "0.035",
                                                                   "375": "0.375"}[s["x"]]
        except (ValueError, motor.NoSalio, RuntimeError):
            cazado = True
        comprobar("D %s trucada -> se caza" % que, cazado, True)

    print("\nE - EN EL RESOLVEDOR (el numero comun pide las piezas; sin puerta nueva)")
    for q, esperado in (("resolver: 4.5 x 1000", "4500"), ("resolver: 375 : 1000", "0.375"),
                        ("resolver: -375 : 100", "-3.75"), ("resolver: n x 100 = 37", "n = 0.37"),
                        ("resolver: 4.5 x 1000 + 1", "4501"), ("resolver: n : 1000 = 0.25", "n = 250"),
                        ("resolver: 30 : 100 + 45 : 100", "0.75"),
                        ("resolver: 3.5 : 1000", "7/2000")):        # mas de tres decimales: lo de siempre
        comprobar("E %s -> %s" % (q, esperado), S(q), esperado)
    t = X("resolver: 375 : 1000")
    comprobar("E la explicacion del resolvedor dice que las cifras bajan tres sitios", "cada cifra baja tres sitios" in t,
              True)

    print("\nF - CAMBIAR DE UNIDAD (punto 2): lo que se sabe de las medidas, en datos; en los dos sentidos")
    for q, esperado in (("Una cuerda mide 3.2 km. ¿Cuántos m mide?", "3200 m"),
                        ("Un camino mide 2500 m. ¿Cuántos km mide?", "2.5 km"),
                        ("Una mesa mide 1.2 m. ¿Cuántos cm mide?", "120 cm"),
                        ("Una cinta mide 45 cm. ¿Cuántos m mide?", "0.45 m"),
                        ("Un lápiz mide 15 cm. ¿Cuántos mm mide?", "150 mm"),
                        ("Una bolsa pesa 1.5 kg. ¿Cuántos gramos pesa?", "1500 gramos"),
                        ("Un paquete pesa 750 g. ¿Cuántos kg pesa?", "0.75 kg"),
                        ("Una botella tiene 2 litros. ¿Cuántos ml tiene?", "2000 ml"),
                        ("Ana tiene 3 m de cuerda. ¿Cuántos cm de cuerda tiene?", "300 cm")):
        comprobar("F %s -> %s" % (q, esperado), S("resolver: " + q), esperado)
    t = X("resolver: Una cuerda mide 3.2 km. ¿Cuántos m mide?")
    comprobar("F la explicacion dice lo que se sabe (1 km = 1000 m) y lo comprueba",
              "1 km = 1000 m" in t and "cuerda_m = 1000 x cuerda" in t and "... SI" in t, True)
    comprobar("F la unidad pequena da el numero GRANDE (no 3.2 km = 0.0032 m)",
              motor.viene_despues(motor.decir(3200, SABER), motor.decir(3, SABER), SABER), True)

    print("\nG - LA PRUDENCIA: nunca una respuesta falsa")
    comprobar("G '3 m y 25 cm' (una medida compuesta): antes decia '25 cm' (FALSO); ahora no entiendo",
              S("resolver: Una cuerda mide 3 m y 25 cm. ¿Cuántos cm mide?"), "no_entiendo")
    comprobar("G km -> cm (sin la equivalencia directa): todavia no, no una respuesta inventada",
              S("resolver: Una cuerda mide 3 km. ¿Cuántos cm mide?"), "todavia_no")
    comprobar("G dos personas en km y en m: sigue no entiendo (no se juntan cosas distintas)",
              S("resolver: Ana corre 3 km y Luis corre 500 m. ¿Cuántos m corren entre los dos?"), "no_entiendo")

    print("\nH - CERCA DEL TECHO (9 999 999) Y LAS MILESIMAS")
    for q, esperado in (("99999.9 x 100", "9999990"), ("999999.9 x 100", "todavia_no"), ("9999.999 x 1000", "9999999"),
                        ("resolver: 9999999 : 1000", "9999.999"), ("resolver: 9999999 : 10", "999999.9"),
                        ("0.001 x 1000", "1"), ("0.001 : 10", "todavia_no"), ("resolver: 0.001 : 10", "1/10000")):
        comprobar("H %s -> %s" % (q, esperado), S(q), esperado)

    print("\nI - LO QUE NO CAMBIA")
    for q, esperado in (("375 : 10", "37 resto 5"), ("4700 : 1000", "4 resto 700"), ("23 x 1000", "23000"),
                        ("0.3 x 0.4", "todavia_no"), ("0.3 x 4", "1.2"), ("7.2 : 3", "2.4"),
                        ("resolver: 7 : 2 + 1", "9/2"), ("resolver: 1/4 : 10", "1/40"), ("resolver: 1/4 x 100", "25"),
                        ("resolver: Ana tiene 3 m de cuerda y Luis tiene 2 m de cuerda. ¿Cuántos m tienen entre los dos?",
                         "5 m"),
                        ("resolver: Juan tiene 3 kg de manzanas. Compra 2 kg más. ¿Cuántos kg tiene?", "5 kg")):
        comprobar("I %s -> %s" % (q, esperado), S(q), esperado)

    print("\nJ - EL TIEMPO (cada pregunta muy por debajo de 2 s)")
    for q in ("9999.999 x 1000", "resolver: 9999999 : 1000", "resolver: n x 1000 = 4700",
              "resolver: Un camino mide 2500 m. ¿Cuántos km mide?"):
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
