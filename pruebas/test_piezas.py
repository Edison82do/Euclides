# -*- coding: utf-8 -*-
"""
PRUEBAS DEL MOTOR DE PIEZAS (paso 2 del plan; la idea de Carlos del 5 oct 2026).

Lo que tiene que quedar demostrado:
  A. Todas las piezas de conocimiento/piezas/ cargan, y el MAPA es verdad: cada condicion existe,
     todo lo que una pieza dice que usa existe, y no hay vueltas (A usa B que usa A).
  B. El motor prueba TODAS las piezas, descarta con razon, y elige segun la pregunta (un paso:
     todas tienen que dar lo mismo; un calculo: el metodo mas corto que encaja).
  C. Una pieza NO puede usar lo que no declaro (si no, el mapa mentiria).
  D. LA PRUEBA DE FUEGO: una pieza NUEVA entra copiando un archivo a la carpeta, sin tocar el
     motor, y el motor la usa.
"""
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
# Estas pruebas miran los METODOS de calculo: con una memoria vacia, para que lo aprendido
# no cambie que pieza gana (la memoria tiene su propia prueba: test_memoria.py).
os.environ["EUCLIDES_MEMORIA"] = os.path.join(tempfile.mkdtemp(), "hechos.txt")
import motor  # noqa: E402

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
BASE = motor.cargar_piezas()

print("=" * 78)
print("EL MOTOR DE PIEZAS")
print("=" * 78)

print("\nA - LAS PIEZAS Y SU MAPA")
comprobar("A1 cargan sin problemas", BASE["problemas"], [])
comprobar("A2 hay piezas de pasos y de calculo (y las que vengan)",
          {"contar_hasta", "paso", "restar", "sumar"} <= {p["responde"] for p in BASE["piezas"].values()},
          True)
mapa = motor.mapa_del_conocimiento(BASE)


def _llega(desde, hasta, visto=()):
    for u in mapa.get(desde, []):
        destinos = [p["id"] for p in BASE["piezas"].values() if p["responde"] == u] or [u]
        for d in destinos:
            if d == hasta or (d not in visto and _llega(d, hasta, visto + (d,))):
                return True
    return False


vueltas = [p for p in mapa if _llega(p, p)]
comprobar("A3 no hay vueltas en el mapa (ninguna pieza se usa a si misma)", vueltas, [])
comprobar("A4 cada pieza vive en su archivo (id = nombre del archivo)",
          all(p["archivo"] == p["id"] + ".py" for p in BASE["piezas"].values()), True)

print("\nB - PROBAR TODAS, DESCARTAR CON RAZON, ELEGIR")
r = motor.aplicar("sumar", {"a": 8, "b": 5}, SABER)
comprobar("B1 8 + 5 = 13", r["valor"], 13)
comprobar("B2 con el metodo mas corto que encaja: hacer diez", r["pieza"]["id"], "sumar_haciendo_diez")
comprobar("B3 y dice que los dedos y las columnas tambien servian", r["tambien_servian"],
          ["sumar_con_dedos", "sumar_por_columnas"])
r = motor.aplicar("sumar", {"a": 247, "b": 385}, SABER)
comprobar("B4 247 + 385: los dedos se descartan (el segundo no cabe) -> columnas",
          (r["pieza"]["id"], r["valor"]), ("sumar_por_columnas", 632))
desc = {c["id"]: c.get("descartado") for c in r["candidatos"]}
comprobar("B5 y el descarte lleva su porque", "no cabe en los dedos" in (desc["sumar_con_dedos"] or ""), True)
r = motor.aplicar("restar", {"a": 3, "b": 5}, SABER)
comprobar("B6 3 - 5: imposible (no hay restas negativas)", r["conclusion"], "imposible")
r = motor.aplicar("sumar", {"a": 900000, "b": 200000}, SABER)
comprobar("B7 900000 + 200000: ninguna pieza (se pasa de un millon, N.4)", r["conclusion"] in ("ninguna", "imposible"), True)
r = motor.aplicar("paso", {"tipo": "cambio", "antes": 5, "signo": "+", "n": 3}, SABER)
comprobar("B8 un paso: se prueban TODAS las piezas de pasos",
          len(r["candidatos"]), len([p for p in BASE["piezas"].values() if p["responde"] == "paso"]))
comprobar("B9 y encaja una sola: anadir -> 8", (r["pieza"]["id"], r["valor"]), ("anadir", 8))

print("\nC - UNA PIEZA NO USA LO QUE NO DECLARO")
p = dict(BASE["piezas"]["anadir"])
p["usa"] = []
u = motor._Lo_que_puede_usar(p, BASE, SABER)
try:
    u.usar("sumar", a=1, b=2)
    comprobar("C1 usar sin declarar da error", "no dio error", "error")
except RuntimeError:
    comprobar("C1 usar sin declarar da error", "error", "error")

print("\nD - LA PRUEBA DE FUEGO: UNA PIEZA NUEVA, SIN TOCAR EL MOTOR")
tmp = tempfile.mkdtemp(prefix="piezas_")
try:
    for f in os.listdir(BASE["directorio"]):
        if f.endswith(".py"):
            shutil.copy(os.path.join(BASE["directorio"], f), tmp)
    # la pieza nueva: sumar CERO (el numero no cambia).  Un archivo, y nada mas.
    with open(os.path.join(tmp, "sumar_cero.py"), "w", encoding="utf-8") as fh:
        fh.write(
            "PIEZA = {'id': 'sumar_cero', 'nombre': 'sumar cero', 'unidad': 'prueba',\n"
            "         'responde': 'sumar', 'rapidez': 1,\n"
            "         'que_hace': 'sumar cero deja el numero igual',\n"
            "         'condiciones': [('el_segundo_es_cero', 'el segundo no es cero')],\n"
            "         'usa': []}\n\n"
            "def hacer(s, u):\n"
            "    return {'valor': s['a'], 'metodo': 'sumar cero', 'cuenta': '%d + 0' % s['a'],\n"
            "            'vuelta': '', 'vuelta_ok': True}\n")
    with open(os.path.join(tmp, "_condiciones.py"), "a", encoding="utf-8") as fh:
        fh.write("\nCONDICIONES['el_segundo_es_cero'] = lambda s, u: s['b'] == 0\n")
    base2 = motor.cargar_piezas(tmp)
    comprobar("D1 la carpeta con la pieza nueva carga sin problemas", base2["problemas"], [])
    r = motor.aplicar("sumar", {"a": 47, "b": 0}, SABER, base2)
    comprobar("D2 el motor la USA (es la mas corta que encaja)", (r["pieza"]["id"], r["valor"]), ("sumar_cero", 47))
    r = motor.aplicar("sumar", {"a": 47, "b": 3}, SABER, base2)
    comprobar("D3 y la DESCARTA cuando no encaja, con su porque",
              [c.get("descartado") for c in r["candidatos"] if c["id"] == "sumar_cero"], ["el segundo no es cero"])
    r = motor.aplicar("paso", {"tipo": "cambio", "antes": 47, "signo": "+", "n": 0}, SABER, base2)
    comprobar("D4 y un PASO de problema la aprovecha sin saber que existe",
              r["resultado"]["pieza"]["id"], "sumar_cero")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
