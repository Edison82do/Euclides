# -*- coding: utf-8 -*-
"""
PRUEBAS DE LA FASE U.3b DEL PLAN U: LA COSA DE CADA CANTIDAD.
El plan y sus trampas: diario/2026-10-08-paso-U3b-la-cosa-de-cada-cantidad.md
Pocas y representativas (decision de Carlos para lo nuevo), inventadas, con informacion que sobra y cosas mezcladas.
Python solo es TESTIGO.
"""
import os
import shutil
import sys
import tempfile
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)
TMP = tempfile.mkdtemp(prefix="u3b_")
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
    """Lo que contesta el probador (por la puerta de siempre)."""
    return probar.preguntar("problema: " + t, SABER)[0]


def R(t, saber=None):
    """Por el lector de palabras directamente (la orden resolver:)."""
    r = motor.decidir_resolver("resolver: " + t, saber or SABER)
    return r.get("respuesta") if r["conclusion"] == "hecho" else r["conclusion"]


def main():
    t0 = time.time()
    print("PRUEBA U.3b: LA COSA DE CADA CANTIDAD")
    print("=" * 60)

    print("\nA - CADA CANTIDAD ES (DE QUIEN, DE QUE COSA)")
    comprobar("A1 'Maria tiene 8 anos y 15 lapices': dos cantidades de Maria (antes: 8 = 15, ninguna)",
              R("Maria tiene 8 años y 15 lapices. ¿Cuántos lapices tiene Maria?"), "15 lapices")
    comprobar("A2 'en total' junta solo los lapices (la edad sobra)",
              R("Maria tiene 8 años y 15 lapices. Luis tiene 6 lapices. ¿Cuántos lapices tienen en total?"),
              "21 lapices")
    comprobar("A3 las cosas en otro orden y dos edades que sobran",
              R("Luis tiene 10 años y 7 cromos. Su hermana tiene 4 cromos y 12 años. "
                "¿Cuántos cromos tienen entre los dos?"), "11 cromos")
    comprobar("A4 comparar en la cosa que toca: 'Juan tiene 5 canicas mas que Pedro' (Pedro tiene anos y canicas)",
              R("Pedro tiene 12 años y 30 canicas. Juan tiene 5 canicas mas que Pedro. "
                "¿Cuántas canicas tienen entre los dos?"), "65 canicas")
    comprobar("A5 un cambio es de UNA cosa: gana canicas, sus anos no cambian",
              [R("Pedro tiene 15 canicas y 9 años. Gana 4 canicas. ¿Cuántas canicas tiene Pedro?"),
               R("Pedro tiene 15 canicas y 9 años. Gana 4 canicas. ¿Cuántos años tiene Pedro?")],
              ["19 canicas", "9 anos"])
    comprobar("A6 la palabra GENERICA: 'cuanto dinero le queda' pregunta por sus pesos (los hermanos sobran)",
              R("Ana tiene 30 pesos y 4 hermanos. Gasta 12 pesos. ¿Cuánto dinero le queda?"), "18 pesos")

    print("\nB - COSAS DISTINTAS NO SE JUNTAN (mejor no entender que contestar algo falso)")
    comprobar("B1 TRAMPA: '8 anos' + '6 canicas' (U.3 decia '14 anos')",
              R("Ana tiene 8 años. Luis tiene 6 canicas. ¿Cuántas tienen entre los dos?"), "no_entiendo")
    comprobar("B2 ... y por la puerta de siempre tampoco da un numero",
              P("Ana tiene 8 años. Luis tiene 6 canicas. ¿Cuántas tienen entre los dos?") in
              ("no_entiendo", "no_se_resolver", "todavia_no"), True)
    comprobar("B3 se pregunta por alguien con dos cosas sin decir cual: no se adivina",
              R("Ana tiene 12 pesos y 5 canicas. ¿Cuánto tiene Ana?"), "no_entiendo")
    comprobar("B4 'cuantos pesos en total' y Luis solo tiene canicas: falta un dato, no se inventa",
              R("Ana tiene 12 pesos. Luis tiene 5 canicas. ¿Cuántos pesos tienen en total?"), "todavia_no")
    r = motor.decidir_resolver("resolver: Un perro pesa 12 kilos. Un gato tiene 3 años. ¿Cuánto tienen juntos?",
                               SABER)
    comprobar("B5 la comprobacion de las cosas dice que junta y con que",
              (r["conclusion"], "junta cosas distintas" in r.get("porque", "")), ("no_entiendo", True))
    ctx = {"voc": motor._pa_vocabulario(SABER), "cosa_pedido": {},
           "entes": [{"versiones": ["a"], "cosa": ("ano",)}, {"versiones": ["b"], "cosa": ("canica",)}]}
    try:                                                   # una relacion trucada a mano: a + b = 14
        motor._pa_comprobar_cosas(ctx, [{"rel": (("op", "+", ("letra", "a"), ("letra", "b")), ("num", motor._nu_leer("14")))}])
        cazada = False
    except ValueError:
        cazada = True
    comprobar("B6 una relacion trucada que suma anos con canicas: la comprobacion la caza", cazada, True)

    print("\nC - 'CADA' ES GRUPOS IGUALES (total = grupos x lo de cada uno, y sus inversas)")
    comprobar("C1 TRAMPA: '3 cuadernos cuestan 12' (U.3 decia '5 cuadernos'): la proporcion simple",
              [R("3 cuadernos cuestan 12 pesos. ¿Cuánto cuestan 5 cuadernos?"),
               R("4 entradas cuestan 36 pesos. ¿Cuánto cuesta una entrada?")], ["20 pesos", "9 pesos"])
    comprobar("C2 'si 2 kilos de peras cuestan 9 pesos, cuanto cuestan 6 kilos' (y el precio en fraccion)",
              R("Si 2 kilos de peras cuestan 9 pesos, ¿cuánto cuestan 6 kilos de peras?"), "27 pesos")
    comprobar("C3 'por' delante de una cosa es 'de cada': '3 pesos por kilo'",
              R("Las manzanas cuestan 3 pesos por kilo. ¿Cuánto cuestan 5 kilos?"), "15 pesos")
    comprobar("C4 un 'por grupo' multiplica un numero de grupos: los kilos del camion = cajas x kilos de cada caja",
              R("Un camion lleva 12 cajas. Cada caja pesa 8 kilos. ¿Cuántos kilos lleva el camion?"), "96 kilos")
    comprobar("C5 ... con 'por vagon' y con la edad del capitan que sobra",
              [R("Un tren tiene 8 vagones y 25 personas por vagon. ¿Cuántas personas lleva el tren?"),
               R("Un barco lleva 15 contenedores. Cada contenedor pesa 2 toneladas. El capitan tiene 50 años. "
                 "¿Cuántas toneladas lleva el barco?")], ["200 personas", "30 toneladas"])
    comprobar("C6 TRAMPA: 'compra 3 lapices de 4 pesos cada uno': comprar es gastar (U.3 decia '4 pesos')",
              R("Juan tiene 20 pesos. Compra 3 lapices de 4 pesos cada uno. ¿Cuánto le queda?"), "8 pesos")
    comprobar("C7 ... con una frase que sobra en medio",
              R("Marta tiene 30 pesos. Compra 2 libros de 9 pesos cada uno. Su hermano tiene 8 años. "
                "¿Cuánto dinero le queda?"), "12 pesos")
    comprobar("C8 'el precio de cada' y 'una caja de galletas pesa 3 kilos'",
              [R("El precio de cada cuaderno es 6 pesos. ¿Cuánto cuestan 3 cuadernos?"),
               R("Una caja de galletas pesa 3 kilos. Un camion lleva 20 cajas de galletas. "
                 "¿Cuántos kilos lleva el camion?")], ["18 pesos", "60 kilos"])

    print("\nD - LAS PREGUNTAS Y LAS FIGURAS")
    comprobar("D1 'cuanto me sobra' (lo de al final de quien habla)",
              R("Tengo 50 pesos. Gasto 32 pesos. ¿Cuánto me sobra?"), "18 pesos")
    comprobar("D2 'un lado / el otro' del rectangulo, con el perimetro y con el area",
              [R("Un rectangulo tiene 30 cm de perimetro. Un lado mide 8 cm. ¿Cuánto mide el otro?"),
               R("Un rectangulo tiene 40 cm2 de area. Un lado mide 8 cm. ¿Cuánto mide el otro lado?")],
              ["7 cm", "5 cm"])
    comprobar("D3 'mide A por B (por C)': las dimensiones de la figura",
              [R("Una caja mide 5 cm por 4 cm por 3 cm. ¿Cuál es su volumen?"),
               R("Un rectangulo mide 8 cm por 5 cm. ¿Cuál es su area?")], ["60 cm cubicos", "40 cm cuadrados"])

    print("\nE - CAMBIOS QUE DEPENDEN DE LO QUE HABIA")
    comprobar("E1 'pierde la mitad de lo que tenia' / 'regala la tercera parte de lo que tenia'",
              [R("Ana tenia 40 canicas. Pierde la mitad de lo que tenia. ¿Cuántas le quedan?"),
               R("Pablo tenia 60 cromos. Regala la tercera parte de lo que tenia. ¿Cuántos cromos le quedan?")],
              ["20 canicas", "40 cromos"])
    comprobar("E2 'subio 3/4 de lo que habia bajado' y 'que temperatura hace ahora'",
              R("La temperatura bajo 8 grados y luego subio 3/4 de lo que habia bajado. Al principio hacia 20 grados. "
                "¿Qué temperatura hace ahora?"), "18 grados")

    print("\nF - NADA VIEJO CAMBIA; EL VOCABULARIO EN DATOS")
    comprobar("F1 el lapiz y la goma (U.3) y una cuenta vieja de R.2 siguen igual",
              [R("Un lapiz y una goma cuestan 12 pesos. El lapiz cuesta el doble que la goma. Cuanto cuesta la goma?"),
               P("Hay 3 bolsas con 4 caramelos cada una. Cuantos caramelos hay?")], ["4 pesos", "12"])
    t = "Ana tiene 30 pesos y 4 hermanos. Gasta 12 pesos. ¿Cuánta plata le queda?"
    otro = dict(SABER)
    otro.pop("_pa_vocabulario", None)
    otro["frases"] = dict(SABER["frases"])
    otro["frases"]["cosas_genericas"] = dict(SABER["frases"]["cosas_genericas"])
    otro["frases"]["cosas_genericas"]["plata"] = "peso, euro, dolar"
    comprobar("F2 'plata' no esta en frases.kn: es otra cosa de Ana, sin dato (todavia no); anadida (sin tocar el "
              "codigo) como palabra del dinero: 18 pesos", [R(t), R(t, otro)], ["todavia_no", "18 pesos"])

    print("\nG - EL TIEMPO (un humano no tarda; cada problema por debajo de 3 s)")
    for q in ("Un camion lleva 12 cajas. Cada caja pesa 8 kilos. ¿Cuántos kilos lleva el camion?",
              "Pedro tiene 12 años y 30 canicas. Juan tiene 5 canicas mas que Pedro. ¿Cuántas canicas tienen "
              "entre los dos?"):
        t1 = time.time()
        R(q)
        d = time.time() - t1
        comprobar("G %s (%.2f s)" % (q[:50], d), d < 3, True)

    print("\n(%.1f s)" % (time.time() - t0))
    print("TOTAL: %d/%d" % (BIEN, BIEN + MAL))
    shutil.rmtree(TMP, ignore_errors=True)
    return 1 if MAL else 0


if __name__ == "__main__":
    sys.exit(main())
