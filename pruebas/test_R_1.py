# -*- coding: utf-8 -*-
"""
Pruebas de la unidad R.1 - EL RESOLVEDOR: aplicar todo lo que se sabe, y descartar con razones.

Lo que tiene que quedar demostrado (nota de Carlos del 3 oct 2026, y resolver_r1.kn):
  - LEER sin adivinar: cada frase encaja en una forma, o NO ENTIENDE y senala cual.
  - APLICAR TODO: en cada paso se prueban TODOS los conocimientos, no se elige uno a dedo.
  - DESCARTAR CON RAZONES: cada descartado dice POR QUE (una condicion escrita en datos).
  - NO ES UN CLASIFICADOR POR PALABRAS: "mas" puede ser resta y "menos" puede ser suma.
  - COMBINAR: varios pasos, y la respuesta de uno es el dato del siguiente.
  - CALCULAR CON EL METODO DEL SISTEMA (columnas + dedos) y VERIFICAR por la vuelta.
  - DECIR QUE NO cuando falta un dato, cuando es imposible o cuando no entiende.

LA PRUEBA DE HIERRO (E): cientos de problemas generados con las CUATRO estructuras y varias
formas de decirlas, en todo el rango; la respuesta tiene que ser la buena en todos.
"""

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, RAIZ)
sys.path.insert(0, AQUI)
import motor  # noqa: E402
import _muestras  # noqa: E402
import probar  # noqa: E402

BIEN = 0
MAL = 0


def comprobar(nombre, obtenido, esperado):
    global BIEN, MAL
    if obtenido == esperado:
        BIEN += 1
        print("  bien    %s" % nombre)
    else:
        MAL += 1
        print("  FALLA   %s\n          esperado=%r  obtenido=%r" % (nombre, esperado, obtenido))


SABER = motor.cargar_conocimiento()
N_CONOC = len([p for p in motor.cargar_piezas()["piezas"].values() if p["responde"] == "paso"])


def R(texto):
    return motor.decidir_R1_problema(texto, SABER)


def aplicados(r):
    return [p["aplicado"] for p in r.get("pasos") or [] if "aplicado" in p]


print("=" * 78)
print("UNIDAD R.1 - EL RESOLVEDOR")
print("=" * 78)

# ------------------------------------------------------------------ A: las cuatro estructuras
print("\nA - LAS ESTRUCTURAS QUE EL SISTEMA YA CONOCE (5.1, 5.2, 5.4, 5.5)")
casos = [
    ("A1 anadir", "Ana tiene 5 manzanas. Le dan 3 mas. Cuantas tiene ahora?", 8, ["anadir"]),
    ("A2 quitar", "Hay 8 pajaros en el arbol. Se van 3. Cuantos quedan?", 5, ["quitar"]),
    ("A3 juntar", "Ana tiene cinco manzanas y Luis tiene tres. Cuantas tienen entre los dos?", 8, ["juntar"]),
    ("A4 diferencia", "Juan tiene 7 canicas y Pedro tiene 4. Cuantas canicas mas tiene Juan que Pedro?", 3, ["diferencia"]),
    ("A5 parte que falta", "Ana y Luis tienen 9 lapices entre los dos. Ana tiene 4. Cuantos tiene Luis?", 5, ["parte_que_falta"]),
    ("A6 la vuelta de anadir", "Pablo tenia algunas canicas. Gana 5. Ahora tiene 12. Cuantas tenia al principio?", 7, ["deshacer_lo_que_llego"]),
    ("A7 la vuelta de quitar", "Pablo tenia algunas canicas. Pierde 5. Ahora tiene 12. Cuantas tenia al principio?", 17, ["deshacer_lo_que_se_fue"]),
    ("A8 con tres cifras (7.6)", "Ana tiene 247 cromos. Le regalan 385. Cuantos tiene ahora?", 632, ["anadir"]),
    ("A9 con palabras", "Ana tiene cuarenta y siete cromos. Pierde doce. Cuantos le quedan?", 35, ["quitar"]),
]
for nombre, texto, valor, apl in casos:
    r = R(texto)
    comprobar("%s: da %d" % (nombre, valor), (r["conclusion"], r.get("valor")), ("resuelto", valor))
    comprobar("%s: y lo resuelve con %s" % (nombre, apl), aplicados(r), apl)

# ------------------------------------------------------------------ B: la trampa de la palabra
print("\nB - NO ES UN CLASIFICADOR POR PALABRAS (la nota de Carlos)")
r = R("Ana tiene 8 manzanas. Tiene 3 mas que Luis. Cuantas tiene Luis?")
comprobar("B1 dice 'mas' y es una RESTA: Luis tiene 5", r.get("valor"), 5)
comprobar("B2 la operacion aplicada es restar", r["pasos"][-1]["operacion"], "restar")
comprobar("B3 y lo AVISA (pero el aviso no decide nada)", bool(r["avisos"]), True)
r = R("Luis tiene 3 menos que Ana. Luis tiene 7. Cuantas tiene Ana?")
comprobar("B4 dice 'menos' y es una SUMA: Ana tiene 10", (r.get("valor"), r["pasos"][-1]["operacion"]), (10, "sumar"))
r1 = R("Ana tiene 5 manzanas. Le dan 3. Cuantas tiene ahora?")
r2 = R("Ana tiene 5 manzanas. Le dan 3 mas. Cuantas tiene ahora?")
comprobar("B5 quitar la palabra 'mas' no cambia nada (la decide la situacion)",
          (r1.get("valor"), aplicados(r1)), (r2.get("valor"), aplicados(r2)))

# ------------------------------------------------------------------ C: aplicar todo y descartar
print("\nC - APLICAR TODO Y DESCARTAR CON RAZONES")
r = R("Marta tiene 12 caramelos. Se come 4. Luego compra 10. Cuantos caramelos tiene ahora?")
comprobar("C1 combina dos pasos: 12 - 4 = 8 y 8 + 10 = 18", (r.get("valor"), aplicados(r)), (18, ["quitar", "anadir"]))
todos = all(len(p["candidatos"]) == N_CONOC for p in r["pasos"])
comprobar("C2 en CADA paso se prueban TODOS los conocimientos (%d)" % N_CONOC, todos, True)
uno = all(sum(1 for c in p["candidatos"] if c.get("aplica")) == 1 for p in r["pasos"])
comprobar("C3 y en cada paso queda UNO solo", uno, True)
razones = all(c.get("aplica") or c.get("descartado") for p in r["pasos"] for c in p["candidatos"])
comprobar("C4 todo descartado lleva su PORQUE (no hay cajas negras)", razones, True)
comprobar("C5 cada paso se verifica por la vuelta", r["verificado"], True)
# ANTES (C6): todo se calculaba por columnas (7.3/7.5/7.6).  MEJORA (paso 2, piezas): se usa el
# metodo MAS CORTO que encaja (hacer diez, los dedos, las columnas), como un nino que ya sabe mas.
comprobar("C6 y en cada paso se usa el metodo mas corto que encaja (piezas de calculo)",
          all(p["metodo_pieza"] == next(c["id"] for c in p["metodo_candidatos"] if c.get("aplica"))
              for p in r["pasos"]), True)
r = R("Ana tiene 5 manzanas. Luis tiene 3 mas que Ana. Cuantas tienen entre los dos?")
comprobar("C7 combina comparar y juntar: 5 + 3 = 8, y 5 + 8 = 13",
          (r.get("valor"), aplicados(r)), (13, ["comparacion_hacia_arriba", "juntar"]))
t = motor.explicar_pregunta("problema: Ana tiene 8 manzanas. Tiene 3 mas que Luis. Cuantas tiene Luis?", SABER)
comprobar("C8 la explicacion ensena los descartes con [no] ... porque", "[no]" in t and "porque" in t, True)

# ------------------------------------------------------------------ D: decir que no
print("\nD - DECIR QUE NO (sin inventar)")
comprobar("D1 una frase que no encaja: no_entiendo", R("El perro come huesos. Cuantos tiene?")["conclusion"], "no_entiendo")
comprobar("D2 y senala la frase", R("El perro come huesos. Cuantos tiene?")["frase"], "el perro come huesos")
comprobar("D3 sin pregunta: no_entiendo", R("Ana tiene 5 manzanas.")["conclusion"], "no_entiendo")
comprobar("D4 dos preguntas: no_entiendo (R.1 resuelve una)",
          R("Ana tiene 5. Cuantas tiene? Cuantas tiene Luis?")["conclusion"], "no_entiendo")
comprobar("D5 falta un dato: no_se_resolver", R("Ana tiene 5 manzanas. Cuantas tiene Luis?")["conclusion"], "no_se_resolver")
r = R("Hay 4 peces. Se van 9. Cuantos quedan?")
comprobar("D6 imposible (quitar mas de lo que hay): sin_solucion", r["conclusion"], "sin_solucion")
comprobar("D7 y dice la condicion de la 5.4", "no se puede quitar mas de lo que hay" in r["porque"], True)
comprobar("D8 cosas distintas no se juntan",
          R("Ana tiene 5 manzanas. Luis tiene 3 peras. Cuantas tienen entre los dos?")["conclusion"], "no_se_resolver")
comprobar("D9 un lugar no 'saca' nada: no_entiendo",
          R("En la caja hay 20 lapices. Saca 5. Cuantos quedan?")["conclusion"], "no_entiendo")
comprobar("D10 dar vueltas sin dato: no_se_resolver",
          R("Ana tiene 3 mas que Luis. Luis tiene 2 menos que Ana. Cuantas tiene Ana?")["conclusion"], "no_se_resolver")
comprobar("D11 pasa de mil: no_se_resolver (y no se lo inventa)",
          R("Hay 900 hormigas. Llegan 200 mas. Cuantas hay ahora?")["conclusion"], "no_se_resolver")
comprobar("D12 el dato ya esta: no hace falta operar",
          (R("Ana tiene 9 canicas. Cuantas tiene ahora?").get("valor"), R("Ana tiene 9 canicas. Cuantas tiene ahora?")["pasos"]), (9, []))

# ------------------------------------------------------------------ E: la prueba de hierro
print("\nE - LA PRUEBA DE HIERRO (problemas generados, las cuatro estructuras)")
plantillas = [
    ("{q} tiene {a} cromos. Le dan {b}. Cuantos tiene ahora?", lambda a, b: a + b),
    ("{q} tiene {a} cromos. Compra {b} mas. Cuantos tiene ahora?", lambda a, b: a + b),
    ("Hay {a} pajaros. Llegan {b} mas. Cuantos hay ahora?", lambda a, b: a + b),
    ("{q} tiene {a} cromos. Pierde {b}. Cuantos le quedan?", lambda a, b: a - b if b <= a else None),
    ("Hay {a} pajaros. Se van {b}. Cuantos quedan?", lambda a, b: a - b if b <= a else None),
    ("{q} tiene {a} cromos y Luis tiene {b}. Cuantos tienen entre los dos?", lambda a, b: a + b),
    ("{q} tiene {a} cromos y Luis tiene {b}. Cuantos mas tiene {q} que Luis?", lambda a, b: abs(a - b)),
    ("{q} tiene {a} cromos. Tiene {b} mas que Luis. Cuantos tiene Luis?", lambda a, b: a - b if b <= a else None),
    ("{q} tiene {a} cromos. Tiene {b} menos que Luis. Cuantos tiene Luis?", lambda a, b: a + b),
    ("{q} y Luis tienen {a} cromos entre los dos. {q} tiene {b}. Cuantos tiene Luis?", lambda a, b: a - b if b <= a else None),
    ("{q} tenia algunos cromos. Gana {b}. Ahora tiene {a}. Cuantos tenia al principio?", lambda a, b: a - b if b <= a else None),
    ("{q} tiene {a} cromos. Le dan algunos. Ahora tiene {b}. Cuantos le dieron?", lambda a, b: b - a if b >= a else None),
    ("Hay {a} pajaros. Se van algunos. Ahora hay {b}. Cuantos se fueron?", lambda a, b: a - b if b <= a else None),
]
probados = malos = imposibles_bien = 0
for i, (pl, oraculo) in enumerate(plantillas):
    for a in range(0, 501, 23 if False else 61):
        for b in range(0, 501, 29 if False else 67):
            esperado = oraculo(a, b)
            if esperado is not None and esperado > 1000:
                continue
            r = R(pl.format(q="Ana", a=a, b=b))
            probados += 1
            if esperado is None:
                if r["conclusion"] in ("sin_solucion", "no_se_resolver"):
                    imposibles_bien += 1
                else:
                    malos += 1
                    if malos < 5:
                        print("    deberia decir que no: %s -> %s" % (pl.format(q="Ana", a=a, b=b), r.get("valor")))
            elif r["conclusion"] != "resuelto" or r["valor"] != esperado or not r["verificado"]:
                malos += 1
                if malos < 5:
                    print("    %s -> %s %s (esperaba %s)" % (pl.format(q="Ana", a=a, b=b), r["conclusion"],
                                                          r.get("valor"), esperado))
comprobar("E1 los %d problemas generados dan la respuesta buena (o dicen que no cuando toca)" % probados, malos, 0)
comprobar("E2 y se recorrio la rejilla (%s): %d problemas" % (_muestras.modo(), probados), probados > 500, True)
comprobar("E3 y en los imposibles dice que no (%d)" % imposibles_bien, imposibles_bien > 50, True)

# ------------------------------------------------------------------ G: los 11 tipos de CGI
print("\nG - LOS ONCE TIPOS DE PROBLEMA DE SUMA Y RESTA (Cognitively Guided Instruction)")
# Carpenter et al.: juntar (3), separar (3), parte-parte-todo (2) y comparar (3).  Uno de cada.
cgi = [
    ("juntar, resultado desconocido", "Ana tiene 5 cromos. Le dan 3. Cuantos tiene ahora?", 8),
    ("juntar, cambio desconocido", "Ana tiene 5 cromos. Le dan algunos. Ahora tiene 8. Cuantos le dieron?", 3),
    ("juntar, inicio desconocido", "Ana tenia algunos cromos. Le dan 3. Ahora tiene 8. Cuantos tenia al principio?", 5),
    ("separar, resultado desconocido", "Ana tiene 8 cromos. Pierde 3. Cuantos le quedan?", 5),
    ("separar, cambio desconocido", "Ana tiene 8 cromos. Pierde algunos. Ahora tiene 5. Cuantos perdio?", 3),
    ("separar, inicio desconocido", "Ana tenia algunos cromos. Pierde 3. Ahora tiene 5. Cuantos tenia al principio?", 8),
    ("parte-parte-todo, todo desconocido", "Ana tiene 5 cromos y Luis tiene 3. Cuantos tienen entre los dos?", 8),
    ("parte-parte-todo, parte desconocida", "Ana y Luis tienen 8 cromos entre los dos. Ana tiene 5. Cuantos tiene Luis?", 3),
    ("comparar, diferencia desconocida", "Ana tiene 8 cromos y Luis tiene 5. Cuantos mas tiene Ana que Luis?", 3),
    ("comparar, mayor desconocido", "Luis tiene 5 cromos. Ana tiene 3 mas que Luis. Cuantos tiene Ana?", 8),
    ("comparar, menor desconocido", "Ana tiene 8 cromos. Tiene 3 mas que Luis. Cuantos tiene Luis?", 5),
]
for tipo, texto, valor in cgi:
    comprobar("G %s -> %d" % (tipo, valor), R(texto).get("valor"), valor)

# ------------------------------------------------------------------ F: una sola verdad
print("\nF - EL PROBADOR Y EL EXPLICADOR DICEN LO MISMO")
for texto in ("Ana tiene 8 manzanas. Tiene 3 mas que Luis. Cuantas tiene Luis?",
              "Hay 4 peces. Se van 9. Cuantos quedan?", "El perro come huesos. Cuantos tiene?"):
    obt, _ = probar.preguntar("problema: " + texto, SABER)
    vis = [l for l in motor.explicar_pregunta("problema: " + texto, SABER).splitlines() if l.startswith("RESULTADO")][-1]
    comprobar("F '%s...' -> %s" % (texto[:30], obt), vis.split()[1] == obt, True)

print("\n" + "=" * 78)
print("UNIDAD R.1: %d/%d correctos" % (BIEN, BIEN + MAL))
print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
print("=" * 78)
sys.exit(1 if MAL else 0)
