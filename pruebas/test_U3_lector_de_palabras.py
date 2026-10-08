# -*- coding: utf-8 -*-
"""
PRUEBAS DE LA FASE U.3 DEL PLAN U: EL LECTOR DE PALABRAS.
El plan y sus trampas: diario/2026-10-08-paso-U3-lector-de-palabras.md
Pocas y representativas (decision de Carlos para lo nuevo), con frases variadas inventadas.  Python solo es TESTIGO.
"""
import os
import re
import shutil
import sys
import tempfile
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)
TMP = tempfile.mkdtemp(prefix="u3_")
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


def R(t, saber=None):
    """Por el lector de palabras directamente (la orden resolver:)."""
    r = motor.decidir_resolver("resolver: " + t, saber or SABER)
    return r.get("respuesta") if r["conclusion"] == "hecho" else r["conclusion"]


def X(t):
    return motor.explicar_pregunta(t, SABER)


def _numero(t):
    """El TESTIGO de la muestra vieja: el numero de una respuesta, sin unidad ni '$' (Python, solo aqui)."""
    m = re.search(r"-?\d+(?:[.,/]\d+)?(?: resto \d+)?", t or "")
    return m.group(0).replace(",", ".") if m else t


def main():
    t0 = time.time()
    print("PRUEBA U.3: EL LECTOR DE PALABRAS")
    print("=" * 60)

    print("\nA - VALORES, JUNTAR Y COMPARAR (sumando y multiplicando)")
    lg = "Un lapiz y una goma cuestan 12 pesos. El lapiz cuesta el doble que la goma. Cuanto cuesta la goma?"
    comprobar("A1 el del plan U: el doble y entre los dos -> 4 pesos (no 6)", R(lg), "4 pesos")
    comprobar("A2 'mas barato que': la vuelta a 'mas'",
              R("El libro cuesta 5 pesos mas barato que el diccionario. El diccionario cuesta 17 pesos. "
                "Cuanto cuesta el libro?"), "12 pesos")
    comprobar("A3 'juntas cuestan' y '3 pesos mas que'",
              R("Una camiseta cuesta 3 pesos mas que una gorra. Juntas cuestan 21 pesos. Cuanto cuesta la gorra?"),
              "9 pesos")
    comprobar("A4 'mayor que' (anos) y 'entre los dos suman'",
              R("Sara es 4 años mayor que Tomas. Entre los dos suman 20 años. ¿Cuántos años tiene Tomas?"), "8 anos")
    comprobar("A5 '3/4 de lo que pesa': comparar multiplicando por una fraccion",
              R("La mochila pesa 3/4 de lo que pesa la maleta. La maleta pesa 8 kilos. ¿Cuánto pesa la mochila?"),
              "6 kilos")
    comprobar("A6 'la mitad que' de algo impar: una fraccion (el numero comun), no 'todavia no'",
              R("La cinta azul mide la mitad que la verde. La verde mide 15 cm. ¿Cuánto mide la azul?"), "15/2 cm")
    comprobar("A7 'Entre Rosa y Pedro tienen' y 'el doble de cromos que'",
              R("Entre Rosa y Pedro tienen 45 cromos. Rosa tiene el doble de cromos que Pedro. "
                "¿Cuántos cromos tiene Rosa?"), "30 cromos")
    comprobar("A8 TRAMPA: dice MAS y es resta (la lectura da ana = luis + 3)",
              R("Ana tiene 8 manzanas. Tiene 3 mas que Luis. Cuantas tiene Luis?"), "5 manzanas")
    comprobar("A9 'la edad de Ana es el doble de la de Luis' (la de Luis = Luis)",
              R("La edad de Ana es el doble de la de Luis. Luis tiene 7 años. ¿Cuántos años tiene Ana?"), "14 anos")

    print("\nB - EL CAMBIO EN EL TIEMPO (la incognita en cualquier sitio)")
    comprobar("B1 al principio: 'tenia algunas', 'gana', 'ahora tiene' -> 7 (no 17)",
              R("Pablo tenia algunas canicas. Gana 5. Ahora tiene 12. Cuantas tenia al principio?"), "7 canicas")
    comprobar("B2 el cambio: 'le dan algunos' -> cuantos le dieron",
              R("Ana tiene 5 cromos. Le dan algunos. Ahora tiene 8. Cuantos le dieron?"), "3 cromos")
    comprobar("B3 la pregunta PRIMERO, con 'si' detras (Leo solo se nombra en la pregunta)",
              R("¿Cuántas canicas tenía Leo al principio si regala 6 y ahora tiene 9?"), "15 canicas")
    comprobar("B4 dos momentos: el orden lo dice frases.kn (la tarde antes que la noche)",
              R("Por la noche el termometro marca -3 grados. Por la tarde marcaba 8 grados. ¿Cuántos grados bajo?"),
              "11 grados")
    comprobar("B5 dinero con decimales y la elipsis ('y 7.25 en leche')",
              R("Tenia 20 pesos. Gasto 4.50 en pan y 7.25 en leche. Cuanto le queda?"), "8.25 pesos")
    t = "Ana tiene 6 caramelos y Luis tiene 4. Ana le da 2 a Luis. ¿Cuántos tiene %s?"
    comprobar("B6 TRAMPA: 'le da 2 a Luis' es un TRASPASO (uno pierde, el otro gana), no 'es igual a'",
              (R(t % "Luis"), R(t % "Ana")), ("6 caramelos", "4 caramelos"))
    comprobar("B7 el cambio es una parte de lo que tenia: 'regala la cuarta parte'",
              R("Carlos tiene 20 cromos y regala la cuarta parte. ¿Cuántos cromos regala?"), "5 cromos")

    print("\nC - GRUPOS IGUALES, PRECIO Y VUELTA")
    comprobar("C1 'cada caja pesa 5 kilos'; '4 cajas' es 4 x caja (no 4 + 5)",
              R("Cada caja pesa 5 kilos. Cuanto pesan 4 cajas?"), "20 kilos")
    comprobar("C2 'hay 20 lapices en 4 cajas iguales' -> en cada caja",
              R("Hay 20 lapices en 4 cajas iguales. Cuantos lapices hay en cada caja?"), "5 lapices")
    comprobar("C3 compra ANTES de decir los precios (las frases en cualquier orden)",
              R("Compra 3 cuadernos y 2 lapices. Cada cuaderno cuesta 4 pesos y cada lapiz 2 pesos. ¿Cuánto paga?"),
              "16 pesos")
    comprobar("C4 la vuelta: 'paga con 50', 'compra 3 cuadernos de 12'",
              R("Paga con 50 pesos. Compra 3 cuadernos de 12 pesos. ¿Cuánto le devuelven?"), "14 pesos")
    comprobar("C5 las partes de un todo: 'hay 25 alumnos', '13 son ninas'",
              R("Hay 25 alumnos en la clase. 13 son ninas. ¿Cuántos son ninos?"), "12 ninos")
    comprobar("C6 'cada semana' y 'en 6 semanas': grupos iguales en el tiempo",
              R("Pedro ahorra 5 pesos cada semana. ¿Cuánto ahorra en 6 semanas?"), "30 pesos")

    print("\nD - LO QUE SE SABE SIN QUE EL TEXTO LO DIGA (relaciones.kn)")
    comprobar("D1 rectangulo: el perimetro NO es largo x ancho",
              R("Un rectangulo mide 8 cm de largo y 5 cm de ancho. Cual es su perimetro?"), "26 cm")
    comprobar("D2 rectangulo al reves: con el perimetro y el ancho, el largo",
              R("Un terreno rectangular tiene 50 m de perimetro. Su ancho es 10 m. ¿Cuánto mide de largo?"), "15 m")
    comprobar("D3 cuadrado: el lado por el area (probar en orden; el perimetro SOBRA)",
              R("Un cuadrado tiene 36 cm cuadrados de area. Cuanto mide su lado?"), "6 cm")
    comprobar("D4 caja: el volumen, con la elipsis por comas",
              R("Una caja mide 5 cm de largo, 3 cm de ancho y 2 cm de alto. ¿Cuál es su volumen?"), "30 cm cubicos")
    comprobar("D5 'consecutivos': el siguiente es el anterior y uno mas",
              R("Dos numeros consecutivos suman 31. Cuales son?"), "15 y 16")
    comprobar("D6 'pares consecutivos': y dos mas", R("Dos numeros pares consecutivos suman 26. ¿Cuáles son?"),
              "12 y 14")
    comprobar("D7 'un numero y su mitad suman 18' (su = el numero)", R("Un numero y su mitad suman 18. Cual es el numero?"),
              "12")
    comprobar("D8 STUDENT: 'el doble de un numero mas 3 es 17'",
              R("El doble de un numero mas 3 es 17. ¿Cuál es el número?"), "7")
    comprobar("D9 STUDENT: 'si a un numero le sumas 5 da 12'", R("Si a un numero le sumas 5 da 12. Cual es el numero?"),
              "7")
    comprobar("D10 'la suma de dos numeros' y 'uno es el triple del otro'",
              R("La suma de dos numeros es 48. Uno es el triple del otro. ¿Cuáles son los números?"), "36 y 12")

    print("\nE - ROBUSTEZ: EL ORDEN, LO QUE SOBRA, LO QUE NO SE ENTIENDE, LO QUE NO ES RAZONABLE")
    ordenes = ("Cuanto cuesta la goma? Un lapiz y una goma cuestan 12 pesos. El lapiz cuesta el doble que la goma.",
               "El lapiz cuesta el doble que la goma. Cuanto cuesta la goma? Un lapiz y una goma cuestan 12 pesos.",
               "Un lapiz y una goma cuestan 12 pesos. Ana tiene 9 años. El lapiz cuesta el doble que la goma. "
               "Cuanto cuesta la goma?")
    comprobar("E1 el mismo problema en otro orden y con una frase que sobra: lo mismo",
              [R(t) for t in ordenes], ["4 pesos", "4 pesos", "4 pesos"])
    x = X("resolver: " + ordenes[2])
    comprobar("E2 lo que sobra se dice y no pasa al buscador", "(sobra: no tiene que ver con la pregunta)" in x, True)
    t = "Ana tiene 8 canicas. Su perro se llama Toby. Tiene 3 mas que Luis. Cuantas tiene Luis?"
    comprobar("E3 una frase que no se entiende: se dice, y con el resto basta", (R(t), "NO LA ENTIENDO" in
              X("resolver: " + t)), ("5 canicas", True))
    comprobar("E4 TRAMPA: 'saca 5' sin saber QUIEN: tiene un cambio, no se adivina (y R.1 sigue igual)",
              (R("En la caja hay 20 lapices. Saca 5. Cuantos quedan?"),
               P("problema: En la caja hay 20 lapices. Saca 5. Cuantos quedan?")), ("no_entiendo", "no_entiendo"))
    comprobar("E5 no es razonable: quitar mas de lo que hay (y R.1 sigue con 'sin_solucion')",
              (R("Hay 4 peces. Se van 9. Cuantos quedan?"), P("problema: Hay 4 peces. Se van 9. Cuantos quedan?")),
              ("no_razonable", "sin_solucion"))
    comprobar("E6 una CUENTA de cosas es entera: 3 bolsas y media no (eso es la division con resto, R.2)",
              (R("Mete 14 caramelos en bolsas de 4. Cuantas bolsas salen?"),
               P("problema: Mete 14 caramelos en bolsas de 4. Cuantas bolsas salen?")), ("no_razonable", "3 resto 2"))
    comprobar("E7 la temperatura SI puede ser negativa", R("Hace 3 grados y baja 8 grados. Cuantos grados hace?"),
              "-5 grados")
    comprobar("E8 falta un dato: no se inventa", R("Ana tiene 5 manzanas. Cuantas tiene Luis?"), "todavia_no")

    print("\nF - LAS PUERTAS: la red de seguridad de las palabras; nada viejo cambia")
    comprobar("F1 por la puerta de siempre (problema:): R.1 no entiende, contesta el lector de palabras",
              P("problema: " + lg), "4 pesos")
    x = X("problema: " + lg)
    comprobar("F1b la explicacion dice que la puerta vieja no llegaba y lo leyo el lector de palabras",
              x.startswith("(la puerta vieja decia: NO ENTIENDO; lo lee el lector de palabras") and
              x.strip().endswith("RESULTADO: 4 pesos"), True)
    viejos = (("problema: Ana tiene 8 manzanas. Tiene 3 mas que Luis. Cuantas tiene Luis?", "5"),
              ("problema: Hay 3 bolsas con 4 caramelos cada una. Cuantos caramelos hay?", "12"),
              ("problema: La cuerda roja mide 6 cm. La azul es 4 veces mas larga. Cuanto mide la azul?", "24 cm"),
              ("La temperatura es -4 grados. Sube 7 grados. Cual es ahora?", "3 grados"),
              ("problema: Hay 17 ninos. En cada coche caben 5. Cuantos coches hacen falta?", "4"))
    comprobar("F2 las puertas viejas siguen contestando lo suyo (R.1, R.2, escala, temperatura)",
              [P(t) for t, _ in viejos], [e for _, e in viejos])

    print("\nG - R.1, R.2, LA ESCALA, LA TEMPERATURA, EL DINERO Y LAS FIGURAS SON VOCABULARIO")
    print("    (una muestra de sus problemas por el lector NUEVO: tiene que dar lo MISMO que la puerta vieja)")
    muestra = (
        # R.1 (CGI)
        ("problema: Ana tiene 5 manzanas. Le dan 3 mas. Cuantas tiene ahora?", None),
        ("problema: Hay 8 pajaros en el arbol. Se van 3. Cuantos quedan?", None),
        ("problema: Ana tiene cinco manzanas y Luis tiene tres. Cuantas tienen entre los dos?", None),
        ("problema: Juan tiene 7 canicas y Pedro tiene 4. Cuantas canicas mas tiene Juan que Pedro?", None),
        ("problema: Luis tiene 3 menos que Ana. Luis tiene 7. Cuantas tiene Ana?", None),
        ("problema: Ana y Luis tienen 9 lapices entre los dos. Ana tiene 4. Cuantos tiene Luis?", None),
        ("problema: Pablo tenia algunas canicas. Gana 5. Ahora tiene 12. Cuantas tenia al principio?", None),
        ("problema: Marta tiene 12 caramelos. Se come 4. Luego compra 10. Cuantos caramelos tiene ahora?", None),
        ("problema: Hay 12 pajaros. Se van algunos. Ahora hay 7. Cuantos se fueron?", None),
        ("problema: Ana y Luis tienen 30 entre los dos. Ana tiene 8 mas que Luis. Cuantas tiene Luis?", None),
        # R.2 (grupos iguales, los que salen justos)
        ("problema: Hay 3 bolsas con 4 caramelos cada una. Cuantos caramelos hay?", None),
        ("problema: Reparte 12 caramelos entre 3 ninos. Cuantos le tocan a cada uno?", None),
        ("problema: Mete 12 caramelos en bolsas de 4. Cuantas bolsas salen?", None),
        ("problema: Hay 12 caramelos. Cada nino tiene 3. Cuantos ninos hay?", None),
        ("problema: Hay 4 cajas. Cada caja tiene 6 lapices. Cuantos lapices hay?", None),
        ("problema: En el cine hay 3 filas de 4 sillas. Cuantas sillas hay?", None),
        ("problema: Cada caja pesa 5 kilos. Cuanto pesan 4 cajas?", None),
        ("problema: Hay 20 lapices en 4 cajas iguales. Cuantos lapices hay en cada caja?", None),
        # S.1 la escala
        ("problema: La cuerda roja mide 6 cm. La azul es 4 veces mas larga. Cuanto mide la azul?", None),
        ("problema: La azul mide 24 cm. Es 4 veces mas larga que la roja. Cuanto mide la roja?", None),
        # N.5 la temperatura
        ("La temperatura es -4 grados. Sube 7 grados. Cual es ahora?", None),
        ("Hace 3 grados y baja 8 grados. Cuantos grados hace?", None),
        ("Por la manana hace -6 grados y a mediodia 5 grados. Cuanto subio?", None),
        ("Hace menos 2 grados y baja 5 grados. Cuantos grados hace?", None),
        # D.3 el dinero, G.1 el area y el perimetro, M.14 el volumen: la orden vieja y su problema con palabras
        ("Compra un cuaderno de 6.35 pesos y paga con 10 pesos. Cuanto le devuelven?", "cambio: pago $10 por $6.35"),
        ("Un rectangulo mide 5 de largo y 3 de ancho. Cual es su area?", "area: rectangulo 5 x 3"),
        ("Un rectangulo mide 5 de largo y 3 de ancho. Cual es su perimetro?", "perimetro: rectangulo 5 x 3"),
        ("Un cuadrado mide 6 de lado. Cual es su perimetro?", "perimetro: cuadrado de 6"),
        ("El perimetro de un cuadrado es 24. Cuanto mide su lado?", "lado: cuadrado de perimetro 24"),
        ("Una caja mide 5 cm de largo, 3 cm de ancho y 2 cm de alto. Cual es su volumen?", "volumen: caja 5 x 3 x 2 cm"),
    )
    distintos = []
    for texto, orden_vieja in muestra:
        viejo = P(orden_vieja or texto)
        nuevo = R(re.sub(r"^problema:\s*", "", texto))
        if _numero(viejo) != _numero(nuevo):
            distintos.append((texto, viejo, nuevo))
    comprobar("G1 %d problemas de las puertas viejas: el lector nuevo da el mismo numero" % len(muestra),
              distintos, [])

    print("\nH - EL VOCABULARIO ESTA EN LOS DATOS")
    t = "Ana tiene 5 cromos. Adquiere 4. Cuantos tiene ahora?"
    comprobar("H1 una palabra que no esta en frases.kn: no la entiende", R(t), "no_entiendo")
    otro = dict(SABER)
    otro.pop("_pa_vocabulario", None)
    otro["frases"] = dict(SABER["frases"])
    otro["frases"]["cambio_mas_de_alguien"] = SABER["frases"]["cambio_mas_de_alguien"] + ", adquiere"
    comprobar("H2 la misma palabra anadida a frases.kn (sin tocar el codigo): la entiende", R(t, otro), "9 cromos")
    otro = dict(SABER)
    otro.pop("_pa_vocabulario", None)
    otro["frases"] = dict(SABER["frases"])
    otro["frases"]["juntos"] = SABER["frases"]["juntos"] + ", tiene"
    comprobar("H3 una palabra con DOS sentidos en frases.kn: se avisa (una palabra, un sentido)", R(t, otro),
              "no_entiendo")
    r = motor.decidir_resolver("resolver: " + t, otro)
    comprobar("H3b ... y dice cual", "dos sentidos" in r.get("porque", ""), True)

    print("\nI - EL TIEMPO (un humano no tarda; cada problema por debajo de 3 s)")
    for q in (lg, "Un cuadrado tiene 36 cm cuadrados de area. Cuanto mide su lado?",
              "Tres numeros consecutivos suman 48. ¿Cuáles son los números?"):
        t1 = time.time()
        R(q)
        d = time.time() - t1
        comprobar("I %s (%.2f s)" % (q[:50], d), d < 3, True)

    print("\n(%.1f s)" % (time.time() - t0))
    print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
    shutil.rmtree(TMP, ignore_errors=True)
    return 1 if MAL else 0


if __name__ == "__main__":
    sys.exit(main())
