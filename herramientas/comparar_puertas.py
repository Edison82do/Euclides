# -*- coding: utf-8 -*-
"""
COMPARAR LAS PUERTAS VIEJAS CON EL RESOLVEDOR UNIVERSAL (fase U.4 del plan U, 8 oct 2026).

Pasa todo lo SIMBOLICO de mis_casos.txt y mis_pruebas.txt (lo que el lector simbolico lee entero) por la puerta vieja
que lo coge Y por el resolvedor universal, y ensena cada caso en que dan respuestas DISTINTAS.  No cuenta como distinto
lo que solo esta escrito distinto ('4' y 'x = 4'; '3/4' y '0.75'; 'VERDADERO' y 'verdadero').

Las que son distintas A PROPOSITO (otra pregunta: 'el resto', 'no hay entero' en el ano del hueco, respetar el ano...)
estan en EXPLICADAS, cada una con su porque.  Una diferencia que no este alli es un fallo: se arregla o se explica.

Python hace aqui de TESTIGO (fractions.Fraction para ver si dos numeros son el mismo): esto es una herramienta de
prueba, no el motor.

Uso:  python3 herramientas/comparar_puertas.py          (lista las diferencias; sale 1 si hay alguna sin explicar)
"""

import os
import re
import sys
import tempfile
from fractions import Fraction

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "sistema"))
if "EUCLIDES_MEMORIA" not in os.environ:                    # memoria propia (vacia): no se toca la de verdad
    os.environ["EUCLIDES_MEMORIA"] = os.path.join(tempfile.mkdtemp(prefix="comparar_"), "hechos.txt")

import motor  # noqa: E402
import probar  # noqa: E402

_ORDENES = re.compile(r"^(ecuacion|hueco|verdad|calcular|resolver)\s*:\s*", re.I)

# Lo que NO es una respuesta (no llega): si la puerta vieja Y el resolvedor no llegan, no hay dos respuestas distintas.
NO_LLEGA = ("no_entiendo", "no_entendido", "todavia_no", "no_sale", "no_se_puede", "ninguna_pieza", "no_decidible",
            "no_alcanza", "no_cuadra")
# 'ningun numero' dicho de varias maneras
NINGUNO = ("ninguna", "imposible")

# Lo que una puerta contesta A PROPOSITO distinto del resolvedor: (como empieza la RESPUESTA vieja) -> porque
EXPLICADAS = {
    "resto": "la division con resto (M.8) contesta otra pregunta: cuantos caben y cuanto sobra",
    "dos_huecos": "E.1: dos huecos pueden ser numeros distintos; el resolvedor toma los dos '?' como la MISMA letra "
                  "(pregunta abierta para Carlos)",
    "sin_hueco": "'ecuacion:' sin hueco: la puerta dice que no hay nada que buscar (para saber si es verdad, 'verdad:')",
    "parejas": "S.3 resume las parejas ('11 parejas con enteros...'); el resolvedor las escribe una a una: son las mismas",
    "infinitas": "S.3 sabe decir 'infinitas' de una relacion sola con dos letras; el resolvedor todavia no",
}
# Lo que es 'ningun numero' con numeros para contar (lo del ano) y el resolvedor encuentra con fracciones o negativos
DEL_ANO = ("no_sale", "imposible", "no_entero", "ninguna", "no_se_puede")


def _numero(t):
    t = t.strip().replace(",", ".")
    m = re.match(r"^(-?\d+) (\d+)/(\d+)$", t)                 # 1 1/2
    if m:
        a, b, c = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return Fraction(a) + Fraction(b, c) * (1 if a >= 0 else -1)
    try:
        return Fraction(t)
    except (ValueError, ZeroDivisionError):
        return None


def _valores(resp):
    """Los numeros de una respuesta: '4' -> [4];  'a = 6, b = 3' -> [6, 3];  '3/4 = 0.75' -> [3/4];  'n = 12' -> [12]."""
    resp = (resp or "").strip()
    if resp.upper() in ("VERDADERO", "FALSO"):
        return [resp.lower()]
    out = []
    for trozo in resp.split(","):
        trozo = trozo.split(" = ")[-1] if " = " in trozo and not re.match(r"^[\d/ .-]+ = [\d/ .-]+$", trozo.strip()) \
            else trozo.split(" = ")[0]
        n = _numero(trozo.replace("el hueco", ""))
        out.append(n if n is not None else trozo.strip().lower())
    return out


def _casos():
    for nombre, flexible in (("mis_casos.txt", False), ("mis_pruebas.txt", True)):
        for c in probar.leer_casos(os.path.join(RAIZ, nombre)):
            t = probar.como_problema(c["texto"]) if flexible else c["texto"]
            yield nombre, c["linea"], t


def comparar(saber, ensenar=True):
    distintas, explicadas, vistas = [], [], 0
    for archivo, linea, t in _casos():
        if not t or t.lower().startswith("resolver"):
            continue
        cuerpo = _ORDENES.sub("", t)
        if not motor.es_expresion_simbolica(cuerpo):
            continue
        if motor.puerta_de(t, saber) == "simbolica":
            continue                                       # ya lo contesta el resolvedor: no hay dos respuestas
        vistas += 1
        vieja, _ = probar.preguntar(t, saber)
        nueva, rn = motor._pu_r_resolver(cuerpo, saber)
        vieja = str(vieja)
        if vieja == nueva or _valores(vieja) == _valores(nueva) or sorted(map(str, _valores(vieja))) == \
                sorted(map(str, _valores(nueva))) or sorted(vieja.split("; ")) == sorted(nueva.split("; ")):
            continue
        if vieja in NINGUNO and nueva in NINGUNO:
            continue
        if (vieja in NO_LLEGA or vieja == "ninguna") and nueva in NO_LLEGA:   # 'ninguna' (pieza) y el techo
            continue                                       # ninguno de los dos llega: no son dos respuestas
        porque = next((p for k, p in EXPLICADAS.items() if vieja.startswith(k) or (" %s" % k) in vieja), None)
        if porque is None and t.lower().startswith("verdad") and "=" not in cuerpo:
            porque = "'verdad:' pide una IGUALDAD; sin '=' no hay nada que decidir (el resolvedor contesta otra pregunta)"
        if porque is None and vieja in DEL_ANO and rn and rn.get("conclusion") == "hecho":
            porque = "con numeros para contar (lo de ese paso) no hay; el resolvedor encuentra una fraccion o un negativo: " \
                     "se queda la puerta y el explicador ensena las dos (U.4: respuesta del ano)"
        if porque is None and vieja == "todavia_no" and not (rn and rn.get("modelo", {}).get("cantidades")):
            porque = "una cuenta sin letras que todavia no toca (respetar el ano, CLAUDE.md)"
        fila = (archivo, linea, t, vieja, nueva, porque)
        (explicadas if porque else distintas).append(fila)
    if ensenar:
        print("COMPARAR LAS PUERTAS VIEJAS CON EL RESOLVEDOR UNIVERSAL (U.4)")
        print("  casos simbolicos que coge una puerta vieja: %d" % vistas)
        print("  distintas a proposito (con su porque): %d" % len(explicadas))
        for a, l, t, v, n, p in explicadas:
            print("     %s:%d  %-34s  vieja: %-14s  resolvedor: %-14s  (%s)" % (a, l, t[:34], v, n, p[:60]))
        print("  DISTINTAS SIN EXPLICAR: %d" % len(distintas))
        for a, l, t, v, n, p in distintas:
            print("     %s:%d  %-34s  vieja: %-14s  resolvedor: %s" % (a, l, t[:34], v, n))
    return vistas, explicadas, distintas


if __name__ == "__main__":
    _, _, d = comparar(motor.cargar_conocimiento())
    sys.exit(1 if d else 0)
