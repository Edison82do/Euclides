# -*- coding: utf-8 -*-
"""
Pruebas de la unidad 2.2 - ORDEN ESTABLE (la lista siempre en el mismo orden).

Lo que esta unidad tiene que dejar claro:
  - Saber la lista es saber QUE VA ANTES Y DESPUES de una palabra, sin empezar por "uno".
    (Si solo supiera recitar de corrido desde el principio, no sabria la lista: sabria una cancion.)
  - La lista SE ACABA donde esta escrita.  Despues de "diez" NO se inventa "once".
  - Revisar una recitacion ajena y cazar el salto (reutilizando las primitivas de la 2.1).

  A) CASOS DE EJEMPLO  - los del conocimiento.
  B) CASOS DE DOMINIO  - no programados, con trampas.
  C) ROBUSTEZ          - lo mal escrito se dice, no revienta.

Uso:  python pruebas/test_2_2.py
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

from motor import (cargar_conocimiento, decidir_2_2_recitar, decidir_2_2_revisar,  # noqa: E402
                   decidir_2_3_cuantos, decidir_3_3_anterior, decidir_3_3_siguiente,
                   escena_0_2, explicar_pregunta)


def correr_relacion(casos, funcion, saber, etiqueta):
    print("=" * 76)
    print(etiqueta)
    print("=" * 76)
    bien = 0
    for titulo, palabra, esperado in casos:
        r = funcion(palabra, saber)
        obtenido = r.get("siguiente") or r.get("anterior") or r["conclusion"]
        ok = obtenido == esperado
        bien += ok
        print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
        if not ok:
            print("       esperado=%s  obtenido=%s" % (esperado, obtenido))
    print("-- %d/%d correctos\n" % (bien, len(casos)))
    return bien, len(casos)


# (titulo, palabra, esperado)
EJEMPLOS_SIGUIENTE = [("E1 despues de tres va cuatro", "tres", "cuatro")]
EJEMPLOS_ANTERIOR = [("E2 antes de tres va dos", "tres", "dos")]

DOMINIO_SIGUIENTE = [
    ("D1 despues de siete va ocho (sin empezar por uno)", "siete", "ocho"),
    ("D2 'diez' esta en la lista de contar pero NO en la de numeros -> sin_numero", "diez", "sin_numero"),
    ("D2b TRAMPA: despues de nueve NO hay nada (es el ultimo)", "nueve", "no_lo_se"),
    ("D3 (MEJORA 6.1): 'once' ya SI esta en la de CONTAR, pero no es un NUMERO -> sin_numero",
     "once", "sin_numero"),
    ("D4 despues de uno va dos (el caso facil)", "uno", "dos"),
    ("D5 TRAMPA: una palabra que no es ni numero", "manzana", "palabra_desconocida"),
]

DOMINIO_ANTERIOR = [
    ("D6 antes de nueve va ocho", "nueve", "ocho"),
    ("D7 ARREGLO DEL FALLO: antes de uno esta el CERO (en los numeros)", "uno", "cero"),
    ("D7b TRAMPA: antes del cero NO hay nada (es el primero)", "cero", "no_lo_se"),
    ("D8 'diez' tampoco tiene sitio en los numeros -> sin_numero", "diez", "sin_numero"),
]

# (titulo, palabra, conclusion, tramo, llega_al_final)
DOMINIO_RECITAR = [
    # UNIDAD 6.1: la secuencia ahora llega a CIEN, asi que estos casos cambian de valor (no de
    # sentido).  Y se anaden los SALTOS DE DECENA, que es donde esta la dificultad de verdad.
    # UNIDAD 6.7: la secuencia llega a MIL; el final ya no es cien, es mil.
    ("D9 recitar desde 'novecientos noventa y ocho': los dos ultimos, y avisa de que ahi acaba",
     "novecientos noventa y ocho", "recitado",
     ["novecientos noventa y ocho", "novecientos noventa y nueve", "mil"], True),
    ("D10 recitar desde 'novecientos noventa': la ultima decena entera",
     "novecientos noventa", "recitado",
     ["novecientos noventa", "novecientos noventa y uno", "novecientos noventa y dos",
      "novecientos noventa y tres", "novecientos noventa y cuatro",
      "novecientos noventa y cinco", "novecientos noventa y seis",
      "novecientos noventa y siete", "novecientos noventa y ocho",
      "novecientos noventa y nueve", "mil"], True),
    ("D11 EL SALTO DE DECENA: desde 'dieciocho' recita hasta el final (se comprueba en D18)",
     "dieciocho", "recitado", None, True),
    ("D11b EL OTRO SALTO: desde 'veintiocho' recita hasta el final (se comprueba en D18)",
     "veintiocho", "recitado", None, True),
    ("D12 TRAMPA: recitar desde una palabra que no existe -> no se la inventa",
     "pepito", "palabra_desconocida", None, False),
    ("D12b (MEJORA 6.1): 'veinte' ya SI esta en la lista", "veinte", "recitado", None, True),
]

# (titulo, palabras, conclusion)
DOMINIO_REVISAR = [
    ("D13 una recitacion correcta", "uno,dos,tres", "correcta"),
    ("D14 TRAMPA: se salto el tres", "uno,dos,cuatro", "orden_saltado"),
    ("D15 TRAMPA: las cambio de orden", "uno,tres,dos", "orden_saltado"),
    ("D16 (MEJORA 6.1): 'once' ya SI es de la secuencia; lo que pasa es que SALTA el orden",
     "uno,dos,once", "orden_saltado"),
    ("D16b TRAMPA: una palabra que no existe de verdad sigue sin valer",
     "uno,dos,manzana", "palabra_desconocida"),
    ("D17 la lista entera, bien dicha", "uno,dos,tres,cuatro,cinco", "correcta"),
    # OJO: revisar_secuencia solo acepta recitaciones que EMPIECEN por el principio (es su diseno).
    ("D17c (MEJORA 6.1): los nombres compuestos tambien: hasta veinte, bien dicha",
     "uno,dos,tres,cuatro,cinco,seis,siete,ocho,nueve,diez,once,doce,trece,catorce,quince,"
     "dieciseis,diecisiete,dieciocho,diecinueve,veinte", "correcta"),
]


def correr_recitar(saber):
    print("=" * 76)
    print("C) RECITAR - desde una palabra dada")
    print("=" * 76)
    bien = 0
    for titulo, palabra, concl_esp, tramo_esp, final_esp in DOMINIO_RECITAR:
        r = decidir_2_2_recitar(palabra, saber)
        ok = (r["conclusion"] == concl_esp
              and (tramo_esp is None or r.get("tramo") == tramo_esp)
              and (not final_esp or r.get("llega_al_final")))
        bien += ok
        print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
        if not ok:
            print("       esperado=%s %s final=%s" % (concl_esp, tramo_esp, final_esp))
            print("       obtenido=%s %s final=%s" % (r["conclusion"], r.get("tramo"),
                                                      r.get("llega_al_final")))
    print("-- %d/%d correctos\n" % (bien, len(DOMINIO_RECITAR)))
    # UNIDAD 6.1: la secuencia ENTERA, comprobada A MANO en los puntos que importan (no contra si
    # misma).  Los cuatro saltos de decena son los sitios donde el error tipico aparece.
    r = decidir_2_2_recitar("uno", saber)
    tramo = r.get("tramo") or []
    puntos = {0: "uno", 1: "dos", 17: "dieciocho", 19: "veinte", 28: "veintinueve",
              29: "treinta", 43: "cuarenta y cuatro", 98: "noventa y nueve", 99: "cien"}
    ok = len(tramo) == 1000 and all(len(tramo) > k and tramo[k] == v for k, v in puntos.items())
    print("%-6s D18 LA SECUENCIA ENTERA A MANO: 1000 palabras (6.7), y los saltos de decena bien"
          % ("OK" if ok else "FALLA"))
    if not ok:
        print("       esperado: 1000 palabras con %s" % puntos)
        print("       obtenido: %d palabras: %s" % (len(tramo), {k: (tramo[k] if len(tramo) > k else None) for k in puntos}))
    bien += ok
    total = len(DOMINIO_RECITAR) + 1
    print("-- %d/%d correctos\n" % (bien, total))
    return bien, total


def correr_revisar(saber):
    print("=" * 76)
    print("D) REVISAR una recitacion ajena  (reutiliza las primitivas de la 2.1)")
    print("=" * 76)
    bien = 0
    for titulo, palabras, concl_esp in DOMINIO_REVISAR:
        ws = [p.strip() for p in palabras.split(",") if p.strip()]
        r = decidir_2_2_revisar(ws, saber)
        ok = r["conclusion"] == concl_esp
        bien += ok
        print("%-6s %s" % ("OK" if ok else "FALLA", titulo))
        if not ok:
            print("       esperado=%s  obtenido=%s" % (concl_esp, r["conclusion"]))
    print("-- %d/%d correctos\n" % (bien, len(DOMINIO_REVISAR)))
    return bien, len(DOMINIO_REVISAR)


def correr_robustez(saber):
    print("=" * 76)
    print("E) ROBUSTEZ - lo escrito mal se dice, no revienta")
    print("=" * 76)
    entradas = [
        "siguiente:",
        "anterior: ",
        "recitar:",
        "revisar_secuencia: ",
        "siguiente:  ",
    ]
    bien = 0
    for e in entradas:
        try:
            salida = explicar_pregunta(e, saber)
            ok = isinstance(salida, str) and salida.strip() != ""
            bien += ok
            print("%-6s %r -> %s" % ("OK" if ok else "FALLA", e, salida.splitlines()[0][:56]))
        except Exception as ex:
            print("FALLA  reviento con %r -> %r" % (e, ex))
    print("-- %d/%d correctos\n" % (bien, len(entradas)))
    return bien, len(entradas)


def main():
    saber = cargar_conocimiento()
    a1 = correr_relacion(EJEMPLOS_SIGUIENTE, decidir_3_3_siguiente, saber, "A) SIGUIENTE - ejemplos")
    a2 = correr_relacion(EJEMPLOS_ANTERIOR, decidir_3_3_anterior, saber, "A) ANTERIOR - ejemplos")
    b1 = correr_relacion(DOMINIO_SIGUIENTE, decidir_3_3_siguiente, saber,
                         "B) SIGUIENTE - prueba de dominio (no programados)")
    b2 = correr_relacion(DOMINIO_ANTERIOR, decidir_3_3_anterior, saber,
                         "B) ANTERIOR - prueba de dominio (no programados)")
    c = correr_recitar(saber)
    d = correr_revisar(saber)
    e = correr_robustez(saber)

    print("=" * 76)
    print("TRAZA DE LA TRAMPA PRINCIPAL (D2: despues de diez, NO se inventa once)")
    print("=" * 76)
    print(explicar_pregunta("siguiente: diez", saber))
    print()

    ok = a1[0] + a2[0] + b1[0] + b2[0] + c[0] + d[0] + e[0]
    total = a1[1] + a2[1] + b1[1] + b2[1] + c[1] + d[1] + e[1]
    print("TOTAL: %d/%d" % (ok, total))
    if ok != total:
        print("RESULTADO: ROJO")
        return 1
    print("RESULTADO: VERDE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
