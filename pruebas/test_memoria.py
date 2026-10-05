# -*- coding: utf-8 -*-
"""
PRUEBAS DE LA MEMORIA DE HECHOS (paso 3 del plan, 5 oct 2026).

Lo que tiene que quedar demostrado (una prueba = una afirmacion):
  A. Sin memoria, el sistema CALCULA (y 'recordar' se descarta con su porque).
  B. Aprender: cada hecho entra calculado sin memoria, comprobado por la vuelta y por un segundo
     camino; y dice COMO lo aprendio.
  C. Despues de aprender, RECUERDA (es lo mas corto) -- pero puede pedirse el camino largo.
  D. Las restas se aprenden como familia de la suma.
  E. Un recuerdo FALSO no se usa: se comprueba, no cuadra, y se calcula por el camino largo.
  F. La memoria no inventa: lo que no aprendio (47 + 5) lo sigue calculando.
Todo en una memoria de prueba (un archivo temporal): la memoria de verdad no se toca.
"""
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
TMP = tempfile.mkdtemp(prefix="memoria_")
RUTA = os.path.join(TMP, "hechos.txt")
os.environ["EUCLIDES_MEMORIA"] = RUTA
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

print("=" * 78)
print("LA MEMORIA DE HECHOS")
print("=" * 78)
try:
    print("\nA - SIN MEMORIA, CALCULA")
    r = motor.aplicar("sumar", {"a": 8, "b": 5}, SABER)
    comprobar("A1 8 + 5 = 13 haciendo diez", (r["pieza"]["id"], r["valor"]), ("sumar_haciendo_diez", 13))
    desc = {c["id"]: c.get("descartado") for c in r["candidatos"]}
    comprobar("A2 'recordar' se descarta: no la tengo", "no la tengo" in (desc["recordar_suma"] or ""), True)

    print("\nB - APRENDER LAS SUMAS")
    a = motor.aprender("sumas", SABER)
    comprobar("B1 aprende las 100 sumas de dos numeros de una cifra", len(a["nuevos"]), 100)
    comprobar("B2 ninguna rechazada", a["rechazados"], [])
    comprobar("B3 casi todas comprobadas tambien por un segundo camino", a["dos_caminos"] >= 90, True)
    h = motor.cargar_memoria()["8 + 5"]
    comprobar("B4 guarda el hecho y COMO lo aprendio", (h["valor"], "diez" in h["como"]), (13, True))
    comprobar("B5 y como lo comprobo", "vuelta" in h["comprobado"] and "otro camino" in h["comprobado"], True)
    a = motor.aprender("sumas", SABER)
    comprobar("B6 practicar otra vez no duplica: ya las sabia", (len(a["nuevos"]), len(a["ya_sabia"])), (0, 100))

    print("\nC - DESPUES, RECUERDA")
    r = motor.aplicar("sumar", {"a": 8, "b": 5}, SABER)
    comprobar("C1 8 + 5 = 13 de memoria", (r["pieza"]["id"], r["valor"]), ("recordar_suma", 13))
    comprobar("C2 y dice como lo aprendio", "de memoria (lo aprendi con" in r["resultado"]["metodo"], True)
    comprobar("C3 y sigue comprobando por la vuelta", r["resultado"]["vuelta_ok"], True)
    r = motor.aplicar("sumar", {"a": 8, "b": 5, "sin_memoria": True}, SABER)
    comprobar("C4 se puede pedir el camino largo (sin memoria)", r["pieza"]["id"], "sumar_haciendo_diez")

    print("\nD - LAS RESTAS, COMO FAMILIA DE LA SUMA")
    a = motor.aprender("restas", SABER)
    comprobar("D1 aprende las 100 restas de la familia", (len(a["nuevos"]), a["rechazados"]), (100, []))
    h = motor.cargar_memoria()["13 - 5"]
    comprobar("D2 13 - 5 = 8, y dice de que suma es familia", (h["valor"], "familia de 8 + 5" in h["comprobado"]), (8, True))
    r = motor.aplicar("restar", {"a": 13, "b": 5}, SABER)
    comprobar("D3 13 - 5 de memoria", (r["pieza"]["id"], r["valor"]), ("recordar_resta", 8))

    print("\nE - UN RECUERDO FALSO NO SE USA")
    with open(RUTA, encoding="utf-8") as f:
        txt = f.read()
    with open(RUTA, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt.replace("8 + 5 = 13 |", "8 + 5 = 14 |"))
    r = motor.aplicar("sumar", {"a": 8, "b": 5}, SABER)
    comprobar("E1 el recuerdo 8 + 5 = 14 no cuadra: calcula y da 13",
              (r["pieza"]["id"], r["valor"]), ("sumar_haciendo_diez", 13))
    fila = [c for c in r["candidatos"] if c["id"] == "recordar_suma"][0]
    comprobar("E2 y dice por que no uso el recuerdo", "NO cuadra" in fila.get("no_salio", ""), True)

    print("\nF - LA MEMORIA NO INVENTA")
    r = motor.aplicar("sumar", {"a": 47, "b": 5}, SABER)
    comprobar("F1 47 + 5 no esta en la memoria: lo calcula", (r["pieza"]["id"] != "recordar_suma", r["valor"]), (True, 52))
    motor.olvidar_todo()
    comprobar("F2 olvidar todo deja la memoria vacia", len(motor.cargar_memoria()), 0)
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 78)
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
sys.exit(1 if MAL else 0)
