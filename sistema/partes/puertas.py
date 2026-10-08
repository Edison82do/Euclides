# -*- coding: utf-8 -*-
"""
Euclides - UNA SOLA TABLA DE PUERTAS (fase U.4 del plan U, 8 oct 2026).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).  Prefijo _pu_.

Hasta U.3 habia DOS cadenas de puertas casi iguales: explicacion.explicar_pregunta (lo que se ensena) y
probar.preguntar (la respuesta corta de las pruebas), y no siempre decian lo mismo (`6/2 + n = 5` daba `2` en una y
`n = 2` en la otra; `listas` y `aprender` solo estaban en una).  Ahora hay UNA tabla, PUERTAS, en el orden de siempre;
cada puerta dice cuando encaja, como EXPLICA y como RESPONDE.  explicar_pregunta y responder_pregunta recorren la misma
tabla y deciden con la misma regla (_pu_decidir):

  - lo que el lector simbolico lee ENTERO (una expresion o una ecuacion con numeros y simbolos) no lo pueden coger las
    puertas de los OBJETOS (0.1, 0.2, 0.3);
  - si una puerta vieja contesta algo que NO es una respuesta (no entiendo, todavia no, no sale, imposible, no se
    puede, ninguna pieza...) y es una relacion con letras, decide el RESOLVEDOR UNIVERSAL (si llega a una respuesta
    comprobada; si no, se queda lo de la puerta).  Una cuenta sin letras solo pasa al resolvedor si la puerta no la
    supo LEER: su «todavia no» es respetar el ano (12 : 3 + 1, 2/3 x 3/4), una respuesta, no rendirse;
  - con palabras, la red de U.3 (_pa_le_toca).
"""

import re  # noqa: F401


# ------------------------------------------------------------- ayudas para escribir las puertas

def _pu_resto(t, palabra):
    """Lo que va detras de la orden (y de sus dos puntos)."""
    resto = t[len(palabra):].strip()
    if resto.startswith(":"):
        resto = resto[1:].strip()
    return resto


def _pu_tras(t, palabra):
    """'mitad: 12' -> '12' (la forma de las ordenes cortas: se quitan los dos puntos de delante)."""
    return t[len(palabra):].lstrip(":").strip()


def _pu_ultima(salida, mapa=None, minus=False, mira_no_entiendo=True):
    """La respuesta corta de una explicacion: su ultima linea 'RESULTADO: ...' (o 'no_entiendo')."""
    if mira_no_entiendo and salida.startswith("NO ENTIENDO"):
        return "no_entiendo"
    r = salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip()
    if mapa:
        r = mapa.get(r, r)
    return r.lower() if minus else r


_PU_VF = {"VERDADERO": "verdadero", "FALSO": "falso"}


def _pu_puerta(nombre, si, explicar, responder=None, objetos=False, mapa=None, minus=False, mira_no_entiendo=True,
               para_contar=False):
    """Una puerta: cuando encaja (si), como se explica y como se responde.  Sin 'responder', la respuesta es la ultima
    linea de la explicacion (UNA SOLA VERDAD: lo que se ensena y lo que se responde salen de lo mismo).
    'para_contar': su lector solo sabe numeros para contar (enteros sin signo); si lo escrito trae fracciones, decimales o
    negativos no es de su forma (U.4: leia '0.5' como '0' y daba respuestas falsas) y lo coge el resolvedor."""
    return {"nombre": nombre, "si": si, "explicar": explicar, "responder": responder, "objetos": objetos,
            "mapa": mapa, "minus": minus, "mira_no_entiendo": mira_no_entiendo, "para_contar": para_contar}


def _pu_empieza(*palabras):
    return lambda t, tl, saber: tl.startswith(palabras)


def _pu_valor_o(r, bien=("hecho",)):
    return (str(r["valor"]) if r["conclusion"] in bien else r["conclusion"]), None


# ------------------------------------------------------------- las respuestas que salen de decidir_*

def _pu_r_dividir(t, saber):
    r = decidir_dividir(t, saber)
    if r["conclusion"] != "hecho":
        return ("no_se_puede" if r["conclusion"] == "imposible" else r["conclusion"]), None
    return "%d%s" % (r["valor"], " resto %d" % r["resto"] if r["resto"] else ""), None


def _pu_filas_texto(t):
    return re.sub(r"^filas:\s*", "", t.lower())


def _pu_ecuacion_resto(t):
    tl = t.lower()
    return t.split(":", 1)[1] if tl.startswith(("ecuacion", "hueco")) and ":" in t else t


def _pu_e_ecuacion(t, saber):
    resto = t.split(":", 1)[1] if ":" in t else t
    if es_ecuacion_con_letra(resto):
        return explicar_ecuacion_letra(resto, saber)
    return explicar_ecuacion(resto, saber)


def _pu_r_ecuacion(t, saber):
    resto = _pu_ecuacion_resto(t)
    if es_ecuacion_con_letra(resto):
        return _pu_valor_o(decidir_ecuacion_letra(resto, saber))
    return _pu_valor_o(decidir_ecuacion(t.split(":", 1)[1] if ":" in t else t, saber))


def _pu_verdad_resto(t):
    return t.split(":", 1)[1] if ":" in t else t[len("verdad"):]


def _pu_r_verdad(t, saber):
    r = decidir_igualdad(_pu_verdad_resto(t), saber)
    if r["conclusion"] == "no_entiendo":
        return "no_entiendo", None
    return (r["valor"] if r["conclusion"] == "hecho" else "no_se_puede"), None


def _pu_e_olvidar(t, saber):
    if _pu_resto(t, "olvidar").lower() != "todo":
        return "NO ENTIENDO ESTO: se escribe  olvidar: todo   (borra la memoria de hechos)"
    olvidar_todo()
    return "PREGUNTA: olvidar todo lo que se de memoria\n\nRESULTADO: olvidado (vuelvo a calcularlo todo)"


def _pu_e_problema(t, saber):
    resto = _pu_resto(t, "problema")
    if not resto:
        return ("NO ENTIENDO ESTO: dame el enunciado.\n"
                "   se escribe asi:  problema: Ana tiene 5 manzanas. Le dan 3. Cuantas tiene ahora?")
    if es_problema_por(resto, saber):
        return explicar_R2_problema(resto, saber)
    return explicar_R1_problema(resto, saber)


def _pu_r_problema(t, saber):
    resto = _pu_resto(t, "problema")
    if not resto:
        return "no_entendido", None
    if es_problema_por(resto, saber):
        r = decidir_R2_problema(resto, saber)
        if r["conclusion"] != "hecho":
            return r["conclusion"], r
        return "%d%s" % (r["valor"], " resto %d" % r["resto"] if r["resto"] else ""), r
    r = decidir_R1_problema(resto, saber)
    return (str(r["valor"]) if r["conclusion"] == "resuelto" else r["conclusion"]), r


def _pu_escena(t, palabra, saber):
    return escena_cantidad(_pu_resto(t, palabra), saber)


def _pu_dos_escenas(t, palabra, saber, sep="/"):
    izq, _, der = _pu_resto(t, palabra).partition(sep)
    return escena_cantidad(izq, saber), escena_cantidad(der, saber)


def _pu_lista(der):
    return [p.strip().lower() for p in der.split(",") if p.strip()]


def _pu_e_dame(t, saber):
    resto = _pu_resto(t, "dame")
    if "/" not in resto:
        return ("NO ENTIENDO ESTO: dame necesita un MONTON del que coger.\n"
                "   se escribe asi:  dame: <monton> / <cantidad>\n"
                "   ejemplo:         dame: silla_1, silla_2, mesa / tres\n\n"
                "El sistema no tiene objetos propios: no se inventa de donde coger.")
    izq, _, der = resto.partition("/")
    return explicar_2_4_dame(escena_cantidad(izq, saber), der.strip().lower(), saber)


def _pu_r_dame(t, saber):
    resto = _pu_resto(t, "dame")
    if "/" not in resto:
        return "no_entendido", None
    izq, _, der = resto.partition("/")
    r = decidir_2_4_dame(escena_cantidad(izq, saber), der.strip().lower(), saber)
    return ("cumplido" if r["conclusion"] == "cogido" else r["conclusion"]), r


def _pu_con_resto(palabra, explica_vacio, hacer):
    """Una orden que necesita algo detras ('nombre: 47'): sin nada, dice como se escribe."""
    def e(t, saber):
        resto = _pu_resto(t, palabra)
        if not resto:
            return explica_vacio
        return hacer(resto, saber)
    return e


def _pu_r_con_resto(palabra, decidir_, clave, bien="se_puede"):
    def r_(t, saber):
        resto = _pu_resto(t, palabra)
        if not resto:
            return "no_entendido", None
        r = decidir_(resto, saber)
        if r["conclusion"] == bien:
            return r[clave], r
        return r["conclusion"], r
    return r_


def _pu_partir_resta(resto):
    """'72 - 45' (o 'menos') -> (izq, der) o None."""
    sep = "-" if "-" in resto else "menos"
    izq, s, der = resto.partition(sep)
    return (izq.strip(), der.strip()) if s else None


def _pu_partir_suma(resto):
    sep = "+" if "+" in resto else "/"
    izq, s, der = resto.partition(sep)
    return (izq.strip(), der.strip()) if s else None


def _pu_es_resta(resto):
    return "-" in resto or "menos" in resto.lower()


def _pu_e_columnas(t, saber):
    resto = _pu_resto(t, "columnas")
    if _pu_es_resta(resto):            # Unidad 7.5: 'columnas: 72 - 45' es la RESTA por columnas (y el intercambio)
        par = _pu_partir_resta(resto)
        if not par:
            return ("NO ENTIENDO ESTO: restar por columnas quita DOS numeros.\n"
                    "   se escribe asi:  columnas: 72 - 45")
        return explicar_7_5_columnas(par[0], par[1], saber)
    par = _pu_partir_suma(resto)
    if not par:
        return ("NO ENTIENDO ESTO: columnas suma o resta DOS numeros.\n"
                "   se escribe asi:  columnas: 47 + 15   o   columnas: 72 - 45")
    return explicar_7_3_columnas(par[0], par[1], saber)


def _pu_r_columnas(t, saber):
    resto = _pu_resto(t, "columnas")
    resta = _pu_es_resta(resto)
    par = _pu_partir_resta(resto) if resta else _pu_partir_suma(resto)
    if not par:
        return "no_entendido", None
    r = (decidir_7_5_columnas if resta else decidir_7_3_columnas)(par[0], par[1], saber)
    if r["conclusion"] == "se_puede":
        return r["expresion_cifras"], r
    return r["conclusion"], r


def _pu_e_juntar_decenas(t, saber):
    izq, _, der = _pu_resto(t, "juntar_decenas").partition("/")
    if izq.strip() == "" or der.strip() == "":
        return ("NO ENTIENDO ESTO: dime las decenas, una barra, y las unidades.\n"
                "   se escribe asi:  juntar_decenas: 4 / 7")
    return explicar_6_5_juntar_decenas(izq.strip(), der.strip(), saber)


def _pu_r_juntar_decenas(t, saber):
    izq, _, der = _pu_resto(t, "juntar_decenas").partition("/")
    if izq.strip() == "" or der.strip() == "":
        return "no_entendido", None
    r = decidir_6_5_juntar_decenas(izq.strip(), der.strip(), saber)
    if r["conclusion"] == "se_puede":
        return r["dato"], r
    return r["conclusion"], r


def _pu_e_derivar(t, saber):
    par = _pu_partir_suma(_pu_resto(t, "derivar"))
    if not par:
        return ("NO ENTIENDO ESTO: derivar suma DOS numeros.\n"
                "   se escribe asi:  derivar: 7 + 5")
    return explicar_7_2_derivar(par[0], par[1], saber)


def _pu_r_derivar(t, saber):
    par = _pu_partir_suma(_pu_resto(t, "derivar"))
    if not par:
        return "no_entendido", None
    r = decidir_7_2_derivar(par[0], par[1], saber)
    return r.get("expresion") or r["conclusion"], r


def _pu_e_dedos(t, saber):
    resto = _pu_resto(t, "dedos")
    # Unidad 7.4: 'dedos: 9 - 4' es la RESTA con los dedos (se baja el segundo).
    # 'dedos: 8 + 5' es la SUMA (se cuentan los dedos del segundo hacia adelante).
    if _pu_es_resta(resto):
        par = _pu_partir_resta(resto)
        if not par:
            return ("NO ENTIENDO ESTO: la resta con los dedos quita DOS numeros.\n"
                    "   se escribe asi:  dedos: 9 - 4")
        return explicar_7_4_resta_dedos(par[0], par[1], saber)
    par = _pu_partir_suma(resto)
    if not par:
        return ("NO ENTIENDO ESTO: el metodo de los dedos suma o resta DOS numeros.\n"
                "   se escribe asi:  dedos: 8 + 5   o   dedos: 9 - 4")
    return explicar_7_1_dedos(par[0], par[1], saber)


def _pu_r_dedos(t, saber):
    resto = _pu_resto(t, "dedos")
    if _pu_es_resta(resto):
        par = _pu_partir_resta(resto)
        if not par:
            return "no_entendido", None
        r = decidir_7_4_resta_dedos(par[0], par[1], saber)
        if r["conclusion"] == "se_puede":
            return r["expresion"], r
        return r["conclusion"], r
    par = _pu_partir_suma(resto)
    if not par:
        return "no_entendido", None
    r = decidir_7_1_dedos(par[0], par[1], saber)
    return r.get("expresion") or r["conclusion"], r


def _pu_dos(palabra, sep, aviso, explicar_, decidir_, clave, numeros=False, separar=None):
    """Una orden de DOS cosas separadas ('sumar: a,b / c'): sin separador, dice como se escribe."""
    def partir(t):
        resto = _pu_resto(t, palabra)
        if separar:
            s = separar(resto)
            izq, hay, der = resto.partition(s)
        else:
            izq, hay, der = resto.partition(sep)
        return izq, hay, der

    def e(t, saber):
        izq, hay, der = partir(t)
        if not hay:
            return aviso
        if numeros:
            return explicar_(izq.strip(), der.strip(), saber)
        return explicar_(escena_cantidad(izq, saber), escena_cantidad(der, saber), saber)

    def r_(t, saber):
        izq, hay, der = partir(t)
        if not hay:
            return "no_entendido", None
        if numeros:
            r = decidir_(izq.strip(), der.strip(), saber)
        else:
            r = decidir_(escena_cantidad(izq, saber), escena_cantidad(der, saber), saber)
        return (r.get(clave) or r["conclusion"]) if clave else r["conclusion"], r
    return e, r_


def _pu_parejas(r):
    """Las parejas de descomponer, con cifras (y la palabra si una cifra no la tiene: el diez)."""
    trozos = []
    for (ck, cm), (pk, pm) in zip(r["parejas_cifras"], r["parejas_palabras"]):
        trozos.append("%s+%s" % (ck if ck is not None else pk, cm if cm is not None else pm))
    return ",".join(trozos)


def _pu_r_descomponer(palabra, decidir_, escena=False):
    def r_(t, saber):
        resto = _pu_resto(t, palabra)
        r = decidir_(escena_cantidad(resto, saber) if escena else resto, saber)
        if r["conclusion"] == "parejas":
            return _pu_parejas(r), r
        return r["conclusion"], r
    return r_


def _pu_comparar_cifras_resto(t):
    tl = t.lower()
    return _pu_resto(t, "comparar_numeros" if tl.startswith("comparar_numeros") else "comparar_cifras")


def _pu_e_comparar_cifras(t, saber):
    izq, sep, der = _pu_comparar_cifras_resto(t).partition("/")
    if not sep:
        return ("NO ENTIENDO ESTO: comparar_cifras necesita DOS numeros.\n"
                "   se escribe asi:  comparar_cifras: 3 / 2\n\n"
                "Comparar es comparar DOS cosas: con una sola no hay nada que decidir.")
    return explicar_4_2_comparar_cifras(izq.strip(), der.strip(), saber)


def _pu_r_comparar_cifras(t, saber):
    izq, sep, der = _pu_comparar_cifras_resto(t).partition("/")
    if not sep:
        return "no_entendido", None
    na, _ = nombre_de_numero(izq, saber)
    nb, _ = nombre_de_numero(der, saber)
    r = decidir_4_2_comparar_cifras(na, nb, saber)
    return r.get("simbolo") or r["conclusion"], r


def _pu_r_puente(t, saber):
    r = decidir_3_4_puente(_pu_escena(t, "puente", saber), saber)
    if r["conclusion"] == "vacia":
        return "0", r
    if r["conclusion"] == "puente_sin_cifra":
        return r["cantidad"], r
    return r.get("cifra") or r["conclusion"], r


def _pu_secuencia(t, saber):
    return [nombre_de_numero(p, saber)[0] for p in _pu_resto(t, "revisar_secuencia").split(",") if p.strip()]


def _pu_r_recitar(t, saber):
    r = decidir_2_2_recitar(nombre_de_numero(_pu_resto(t, "recitar"), saber)[0], saber)
    if r["conclusion"] == "recitado":
        return "recitado:" + ",".join(r["tramo"]), r
    return r["conclusion"], r


def _pu_r_subitizar(t, saber):
    r = decidir_1_0_subitizar(_pu_resto(t, "subitizar"), saber)
    if r["conclusion"] == "reconocido":
        return "reconocido:%s" % r["etiqueta"], r
    return "no_reconocido", r


def _pu_pertenece(t, saber):
    izq, _, der = _pu_resto(t, "pertenece").partition(":")
    return escena_cantidad(der, saber), parsear_criterio(izq)


def _pu_r_pertenece(t, saber):
    escena, criterio = _pu_pertenece(t, saber)
    rs = decidir_0_3_pertenencia(escena, criterio, saber)
    return ",".join("%s:%s" % (r["objeto"]["id"], r["conclusion"]) for r in rs), rs


def _pu_es_formar(t, tl, saber):
    return ":" in t and "=" in t.split(":", 1)[0] and "(" not in t.split(":", 1)[0]


def _pu_r_formar(t, saber):
    izq, _, der = t.partition(":")
    r = decidir_0_2_formar(escena_cantidad(der, saber), parsear_criterio(izq), saber)
    if r["conclusion"] == "grupo_formado":
        return "tiene:" + ",".join(r["miembros"]), r
    return r["conclusion"], r


def _pu_r_reconocer(t, saber):
    r = decidir_0_2_reconocer(escena_cantidad(t, saber), saber)
    if r["conclusion"] == "grupo_atributo":
        return "grupo:" + ",".join(r["atributos_compartidos"]), r
    return r["conclusion"], r


def _pu_r_resolver(t, saber):
    r = decidir_resolver(t, saber)
    if r["conclusion"] == "no_entiendo":
        return "no_entiendo", r
    if r["conclusion"] == "hecho":
        return r["respuesta"], r
    return r["conclusion"], r


# ------------------------------------------------------------- LA TABLA (el orden importa: es el de siempre)

def _pu_tabla():
    P = _pu_puerta
    E = _pu_empieza
    sumar_e, sumar_r = _pu_dos("sumar", "/", (
        "NO ENTIENDO ESTO: para sumar hacen falta DOS cantidades.\n"
        "   se escribe asi:  sumar: <coleccion> / <coleccion>\n"
        "   ejemplo:         sumar: a,b,c / d,e\n\n"
        "Con una sola cantidad no hay nada que juntar."), explicar_5_2_sumar, decidir_5_2_sumar, "expresion")
    anadir_e, anadir_r = _pu_dos("anadir", "/", (
        "NO ENTIENDO ESTO: para anadir hacen falta DOS cantidades.\n"
        "   se escribe asi:  anadir: <coleccion> / <lo que se anade>\n"
        "   ejemplo:         anadir: a,b,c / d,e\n\n"
        "Si no hay nada que anadir, el monton no crece."), explicar_5_2_anadir, decidir_5_2_anadir, "expresion")
    componer_e, componer_r = _pu_dos("componer", "/", (
        "NO ENTIENDO ESTO: componer necesita DOS partes.\n"
        "   se escribe asi:  componer: <coleccion> / <coleccion>\n"
        "   ejemplo:         componer: a,b / c,d,e\n\n"
        "Para juntar hacen falta DOS partes (las partes son lo que se junta)."),
        explicar_5_1_componer, decidir_5_1_componer, "total")
    comparar_e, comparar_r = _pu_dos("comparar", "/", (
        "NO ENTIENDO ESTO: comparar necesita DOS colecciones.\n"
        "   se escribe asi:  comparar: <coleccion> / <coleccion>\n"
        "   ejemplo:         comparar: a,b,c / d,e\n\n"
        "Comparar es comparar DOS cosas: con una sola no hay nada que decidir."),
        explicar_4_1_comparar, decidir_4_1_comparar, None)
    diferencia_e, diferencia_r = _pu_dos("diferencia", "/", (
        "NO ENTIENDO ESTO: la diferencia necesita DOS colecciones.\n"
        "   se escribe asi:  diferencia: <una coleccion> / <otra coleccion>\n"
        "   ejemplo:         diferencia: a,b,c,d,e / a,b,c\n\n"
        "Con una sola no hay hueco que mirar."), explicar_5_5_diferencia, decidir_5_5_diferencia, "diferencia")
    difnum_e, difnum_r = _pu_dos("diferencia_numeros", "/", (
        "NO ENTIENDO ESTO: para la diferencia hacen falta DOS numeros.\n"
        "   se escribe asi:  diferencia_numeros: 5 / 3"),
        explicar_5_5_diferencia_numeros, decidir_5_5_diferencia_numeros, "diferencia", numeros=True)
    restnum_e, restnum_r = _pu_dos("restar_numeros", None, (
        "NO ENTIENDO ESTO: para restar numeros hacen falta DOS numeros.\n"
        "   se escribe asi:  restar_numeros: 5 - 2\n\n"
        "Con uno solo no hay nada que quitar."),
        explicar_5_4_restar_numeros, decidir_5_4_restar_numeros, "expresion", numeros=True,
        separar=lambda resto: "-" if "-" in resto else "/")
    sumnum_e, sumnum_r = _pu_dos("sumar_numeros", None, (
        "NO ENTIENDO ESTO: para sumar numeros hacen falta DOS numeros.\n"
        "   se escribe asi:  sumar_numeros: 3 + 2\n\n"
        "Con uno solo no hay nada que juntar."),
        explicar_5_3_sumar_numeros, decidir_5_3_sumar_numeros, "expresion", numeros=True,
        separar=lambda resto: "+" if "+" in resto else "/")

    def e_quitar(t, saber):
        izq, sep, der = _pu_resto(t, "quitar").partition("/")
        if not sep:
            return ("NO ENTIENDO ESTO: quitar necesita un MONTON y UNA CANTIDAD.\n"
                    "   se escribe asi:  quitar: <monton> / <cuantos>\n"
                    "   ejemplo:         quitar: a,b,c,d,e / dos\n\n"
                    "El sistema no tiene objetos propios: no se inventa de donde quitar.")
        return explicar_5_4_quitar(escena_cantidad(izq, saber), der.strip(), saber)

    def r_quitar(t, saber):
        izq, sep, der = _pu_resto(t, "quitar").partition("/")
        if not sep:
            return "no_entendido", None
        r = decidir_5_4_quitar(escena_cantidad(izq, saber), der.strip(), saber)
        return r.get("expresion") or r["conclusion"], r

    def conteo(t, saber, f):
        izq, _, der = _pu_resto(t, "conteo").partition("/")
        return f(escena_cantidad(izq, saber), _pu_lista(der), saber)

    def revisar(t, saber, f):
        izq, _, der = _pu_resto(t, "revisar").partition("/")
        return f(escena_cantidad(izq, saber), _pu_lista(der), saber)

    def tiene(t, saber, f):
        izq, _, der = _pu_resto(t, "tiene").partition("/")
        return f(escena_cantidad(izq, saber), der.strip().lower(), saber)

    def misma(t, saber, f):
        izq, _, der = _pu_resto(t, "misma_cantidad").partition("/")
        return f(escena_cantidad(izq, saber), escena_cantidad(der, saber), saber)

    return [
        P("piezas", lambda t, tl, s: tl.strip() in ("piezas", "mapa"), lambda t, s: explicar_piezas(s),
          lambda t, s: ("las_piezas", None)),
        # dos incognitas (S.3; NCETM 1.31): antes que la letra de E.5
        P("dos_incognitas", lambda t, tl, s: es_orden_dos_incognitas(t), explicar_orden_dos_incognitas),
        P("factores", lambda t, tl, s: es_orden_factores(t), explicar_orden_factores),
        # fracciones equivalentes y simplificar (F.6; NCETM 3.7)
        P("equivalentes", lambda t, tl, s: es_orden_equivalentes(t), explicar_orden_equivalentes, mapa=_PU_VF),
        # x con + y - (M.16): antes que calcular: y verdad:
        P("combinar", lambda t, tl, s: es_orden_combinar(t), explicar_orden_combinar, mapa=_PU_VF),
        # parte-parte-todo con tres partes o mas (S.2)
        P("parte_todo", lambda t, tl, s: es_orden_parte_todo(t, s), explicar_orden_parte_todo),
        P("divisible", E("divisible"), lambda t, s: explicar_divisible(_pu_tras(t, "divisible"), s)),
        P("tabla_del", E("tabla del"), explicar_tabla),
        P("mitad", E("mitad"), lambda t, s: explicar_mitad(_pu_tras(t, "mitad"), s)),
        # derivar de un hecho que se sabe (P.7; NCETM 1.29)
        P("derivar_hecho", lambda t, tl, s: es_orden_derivar(t), explicar_orden_derivar),
        P("equivalente", lambda t, tl, s: es_orden_equivalente(t), explicar_orden_equivalente),
        P("negativos", lambda t, tl, s: es_orden_negativos(t), explicar_orden_negativos),
        P("escala", lambda t, tl, s: es_orden_escala(t), explicar_orden_escala),
        P("geometria", lambda t, tl, s: es_orden_geometria(t), explicar_orden_geometria),
        P("dinero", lambda t, tl, s: es_orden_dinero(t), explicar_orden_dinero),
        # como en verdad: (E.0)
        P("volumen", lambda t, tl, s: es_orden_volumen(t), explicar_orden_volumen, mapa=_PU_VF),
        P("decimal_por", lambda t, tl, s: es_orden_decimal_por(t), explicar_orden_decimal_por),
        P("decimal", lambda t, tl, s: es_orden_decimal(t), explicar_orden_decimal),
        P("corta", E("corta"), lambda t, s: explicar_corta(_pu_tras(t, "corta"), s)),
        P("comprobar_division", lambda t, tl, s: es_comprobar_division(t), explicar_comprobar_division,
          mira_no_entiendo=False),
        P("millar", E("millar"), explicar_millar),
        P("comparar_numeros", lambda t, tl, s: es_comparar_numeros(t), explicar_comparar_numeros),
        P("fraccion", lambda t, tl, s: es_orden_fraccion(t), explicar_orden_fraccion),
        P("dividir", lambda t, tl, s: es_division(t), explicar_dividir, _pu_r_dividir),
        P("multiplicar", lambda t, tl, s: es_multiplicacion(t), explicar_multiplicar,
          lambda t, s: _pu_valor_o(decidir_multiplicar(t, s), ("hecho", "desiguales"))),
        P("filas", lambda t, tl, s: re.match(r"^(filas:\s*)?\d+\s+(filas?|columnas?)\s+de\s+\d+", tl),
          lambda t, s: explicar_filas(_pu_filas_texto(t), s),
          lambda t, s: _pu_valor_o(decidir_filas(_pu_filas_texto(t), s))),
        P("saltos", lambda t, tl, s: re.match(r"^de\s+\d+\s+en\s+\d+", tl), explicar_saltos),
        P("estimar", E("estimar"), lambda t, s: explicar_estimar(_pu_tras(t, "estimar"), s)),
        P("razonable", E("razonable"), lambda t, s: explicar_razonable(_pu_tras(t, "razonable"), s)),
        P("redondear", E("redondear"), lambda t, s: explicar_redondear(_pu_tras(t, "redondear"), s)),
        P("par", E("par:", "par "), lambda t, s: explicar_paridad(t[3:].lstrip(":").strip(), s), minus=True),
        P("ecuacion", E("ecuacion", "hueco"), _pu_e_ecuacion, _pu_r_ecuacion, para_contar=True),
        P("letra", lambda t, tl, s: es_ecuacion_con_letra(t), explicar_ecuacion_letra,
          lambda t, s: _pu_valor_o(decidir_ecuacion_letra(t, s))),
        P("verdad", E("verdad"), lambda t, s: explicar_igualdad(_pu_verdad_resto(t), s), _pu_r_verdad),
        P("calcular", E("calcular"), lambda t, s: explicar_calculo(t[len("calcular"):].strip(), s), para_contar=True),
        P("memoria", lambda t, tl, s: tl.strip() == "memoria", lambda t, s: explicar_memoria(s),
          lambda t, s: ("%d hechos" % len(cargar_memoria()), None)),
        P("aprender", E("aprender"), lambda t, s: explicar_aprender(_pu_resto(t, "aprender"), s)),
        P("olvidar", E("olvidar"), _pu_e_olvidar),
        P("problema", E("problema"), _pu_e_problema, _pu_r_problema),
        P("cifra_de", E("cifra_de"), lambda t, s: explicar_3_1_cifra_de(_pu_escena(t, "cifra_de", s), s),
          lambda t, s: (lambda r: (r.get("cifra") or r["conclusion"], r))(
              decidir_3_1_cifra_de(_pu_escena(t, "cifra_de", s), s))),
        P("cifra", E("cifra"), lambda t, s: explicar_3_1_cifra(_pu_resto(t, "cifra").lower(), s),
          lambda t, s: (lambda r: (r.get("cifra") or r["conclusion"], r))(
              decidir_3_1_cifra(_pu_resto(t, "cifra").lower(), s))),
        P("palabra", E("palabra"), lambda t, s: explicar_3_1_palabra(_pu_resto(t, "palabra"), s),
          lambda t, s: (lambda r: (r.get("palabra") or r["conclusion"], r))(
              decidir_3_1_palabra(_pu_resto(t, "palabra"), s))),
        P("misma_cantidad", E("misma_cantidad"), lambda t, s: misma(t, s, explicar_2_6_misma_cantidad),
          lambda t, s: (lambda r: (r["conclusion"], r))(misma(t, s, decidir_2_6_misma_cantidad))),
        P("orden", E("orden"), lambda t, s: explicar_2_5_orden(_pu_escena(t, "orden", s), s),
          lambda t, s: (lambda r: (r["conclusion"], r))(decidir_2_5_orden(_pu_escena(t, "orden", s), s))),
        P("conteo", E("conteo"), lambda t, s: conteo(t, s, explicar_2_5_conteo),
          lambda t, s: (lambda r: (r["conclusion"], r))(conteo(t, s, decidir_2_5_conteo))),
        P("dame", E("dame"), _pu_e_dame, _pu_r_dame),
        P("tiene", E("tiene"), lambda t, s: tiene(t, s, explicar_2_4_tiene),
          lambda t, s: (lambda r: (r["conclusion"], r))(tiene(t, s, decidir_2_4_tiene))),
        P("listas", E("listas"), lambda t, s: explicar_3_3_listas(s), lambda t, s: ("las_listas", None)),
        P("nombre", E("nombre"), _pu_con_resto("nombre", "NO ENTIENDO ESTO: dime un numero del 1 al 100.\n"
                                                         "   se escribe asi:  nombre: 47", explicar_6_1_nombre),
          # UNA SOLA VERDAD: la misma funcion que usa el explicador
          lambda t, s: (lambda r: (r.get("palabra") or r["conclusion"], r))(
              decidir_6_1_nombre(_pu_resto(t, "nombre"), s))),
        P("numero", E("numero"), _pu_con_resto("numero", "NO ENTIENDO ESTO: dime un nombre de numero.\n"
                                                         "   se escribe asi:  numero: cuarenta y siete",
                                               explicar_6_1_numero),
          lambda t, s: (lambda r: ((str(r["valor"]) if r["conclusion"] == "numero" else r["conclusion"]), r))(
              decidir_6_1_numero(_pu_resto(t, "numero"), s))),
        P("columnas", E("columnas"), _pu_e_columnas, _pu_r_columnas),
        P("partir", E("partir"), _pu_con_resto("partir", "NO ENTIENDO ESTO: dime un numero.\n"
                                                         "   se escribe asi:  partir: 47", explicar_6_5_partir),
          _pu_r_con_resto("partir", decidir_6_5_partir, "como_se_parte")),
        P("juntar_decenas", E("juntar_decenas"), _pu_e_juntar_decenas, _pu_r_juntar_decenas),
        P("tabla", lambda t, tl, s: tl.strip() == "tabla", lambda t, s: explicar_6_3_tabla(s),
          lambda t, s: ("la_tabla_de_100", None)),
        P("escalera", lambda t, tl, s: tl.strip() in ("centena", "centenas"), lambda t, s: explicar_6_7_escalera(s),
          lambda t, s: ("la_escalera", None)),
        P("centena", E("centena"), _pu_con_resto("centena", "NO ENTIENDO ESTO: dime un numero.\n"
                                                             "   se escribe asi:  centena: 247", explicar_6_7_centena),
          _pu_r_con_resto("centena", decidir_6_7_centena, "dato")),
        P("sitio", E("sitio"), _pu_con_resto("sitio", "NO ENTIENDO ESTO: dime un numero.\n"
                                                       "   se escribe asi:  sitio: 47", explicar_6_3_sitio),
          _pu_r_con_resto("sitio", decidir_6_3_sitio, "dato")),
        P("agrupar", E("agrupar"), lambda t, s: explicar_6_2_agrupar(_pu_escena(t, "agrupar", s), s),
          lambda t, s: (lambda r: ((r["como_se_dice"] if r["conclusion"] == "se_puede" else r["conclusion"]), r))(
              decidir_6_2_agrupar(_pu_escena(t, "agrupar", s), s))),
        P("derivar", E("derivar"), _pu_e_derivar, _pu_r_derivar),
        P("dedos", E("dedos"), _pu_e_dedos, _pu_r_dedos),
        P("decenas", E("decenas"), lambda t, s: explicar_6_1_decenas(s),
          lambda t, s: ("las_decenas", {"texto": explicar_6_1_decenas(s)})),
        P("diferencia_numeros", E("diferencia_numeros"), difnum_e, difnum_r),
        P("diferencia", E("diferencia"), diferencia_e, diferencia_r),
        P("restar_numeros", E("restar_numeros"), restnum_e, restnum_r),
        P("quitar", E("quitar"), e_quitar, r_quitar),
        P("sumar_numeros", E("sumar_numeros"), sumnum_e, sumnum_r),
        P("sumar", E("sumar"), sumar_e, sumar_r),
        P("anadir", E("anadir"), anadir_e, anadir_r),
        P("descomponer_numero", E("descomponer_numero"),
          lambda t, s: explicar_5_3_descomponer_numero(_pu_resto(t, "descomponer_numero"), s),
          _pu_r_descomponer("descomponer_numero", decidir_5_3_descomponer_numero)),
        P("descomponer", E("descomponer"),
          lambda t, s: explicar_5_1_descomponer(_pu_escena(t, "descomponer", s), s),
          _pu_r_descomponer("descomponer", decidir_5_1_descomponer, escena=True)),
        P("componer", E("componer"), componer_e, componer_r),
        P("comparar_cifras", E("comparar_cifras", "comparar_numeros"), _pu_e_comparar_cifras, _pu_r_comparar_cifras),
        P("comparar", E("comparar"), comparar_e, comparar_r),
        P("caminos", E("caminos"), lambda t, s: explicar_3_4_caminos(s), lambda t, s: ("los_caminos", None)),
        P("puente", E("puente"), lambda t, s: explicar_3_4_puente(_pu_escena(t, "puente", s), s), _pu_r_puente),
        P("cuantos", E("cuantos"), lambda t, s: explicar_2_3_cuantos(_pu_escena(t, "cuantos", s), s),
          lambda t, s: (lambda r: (r.get("cantidad") or r["conclusion"], r))(
              decidir_2_3_cuantos(_pu_escena(t, "cuantos", s), s))),
        P("revisar_secuencia", E("revisar_secuencia"), lambda t, s: explicar_2_2_revisar(_pu_secuencia(t, s), s),
          lambda t, s: (lambda r: (r["conclusion"], r))(decidir_2_2_revisar(_pu_secuencia(t, s), s))),
        P("recitar", E("recitar"), lambda t, s: explicar_2_2_recitar(_pu_resto(t, "recitar"), s), _pu_r_recitar),
        P("siguiente", E("siguiente"), lambda t, s: explicar_3_3_siguiente(_pu_resto(t, "siguiente"), s),
          lambda t, s: (lambda r: (r.get("siguiente") or r["conclusion"], r))(
              decidir_3_3_siguiente(nombre_de_numero(_pu_resto(t, "siguiente"), s)[0], s))),
        P("anterior", E("anterior"), lambda t, s: explicar_3_3_anterior(_pu_resto(t, "anterior"), s),
          lambda t, s: (lambda r: (r.get("anterior") or r["conclusion"], r))(
              decidir_3_3_anterior(nombre_de_numero(_pu_resto(t, "anterior"), s)[0], s))),
        P("revisar", E("revisar"), lambda t, s: revisar(t, s, explicar_2_1_revisar),
          lambda t, s: (lambda r: (r["conclusion"], r))(revisar(t, s, decidir_2_1_revisar))),
        P("contar", E("contar"), lambda t, s: explicar_2_1_contar(_pu_escena(t, "contar", s), s),
          lambda t, s: (lambda r: (r["conclusion"], r))(decidir_2_1_contar(_pu_escena(t, "contar", s), s))),
        P("subitizar", E("subitizar"), lambda t, s: explicar_1_0_subitizar(_pu_resto(t, "subitizar"), s),
          _pu_r_subitizar),
        P("pertenece", E("pertenece"), lambda t, s: explicar_0_3_pertenencia(*(_pu_pertenece(t, s) + (s,))),
          _pu_r_pertenece, objetos=True),
        P("formar", _pu_es_formar,
          lambda t, s: explicar_0_2_formar(escena_cantidad(t.partition(":")[2], s),
                                           parsear_criterio(t.partition(":")[0]), s),
          _pu_r_formar, objetos=True),
        # la red de seguridad (U.1): numeros y letras, no objetos
        P("simbolica", lambda t, tl, s: es_expresion_simbolica(t), explicar_orden_resolver, _pu_r_resolver),
        P("reconocer", lambda t, tl, s: "(" in t or ";" in t,
          lambda t, s: explicar_0_2_reconocer(escena_cantidad(t, s), s), _pu_r_reconocer, objetos=True),
        P("objetos", lambda t, tl, s: True, lambda t, s: explicar(escena_0_1(t), s),
          lambda t, s: (lambda r: (r["conclusion"], r))(decidir(escena_0_1(t), s)), objetos=True),
    ]


_PU_TABLA = []

# lo que trae una orden ('ecuacion:', 'calcular:') cuyo lector solo sabe numeros para contar, con otros numeros
_PU_AL_RESOLVEDOR = _pu_puerta("simbolica", None, lambda t, s: explicar_orden_resolver(_pu_cuerpo(t), s),
                               lambda t, s: _pu_r_resolver(_pu_cuerpo(t), s))


def puertas():
    """LA TABLA (se arma una vez: las funciones de las puertas son de otras partes)."""
    if not _PU_TABLA:
        _PU_TABLA.extend(_pu_tabla())
    return _PU_TABLA


def _pu_elegir_puerta(t, saber, simbolica):
    tl = t.lower()
    for p in puertas():
        if p["objetos"] and simbolica:
            continue                                 # numeros y simbolos no son objetos (U.4)
        try:
            if p["si"](t, tl, saber):
                if p["para_contar"] and not _pu_solo_para_contar(_pu_cuerpo(t)):
                    return _PU_AL_RESOLVEDOR
                return p
        except Exception as ex:                      # mirar si encaja tampoco puede reventar: se dice al explicar
            return _pu_rota(p["nombre"], ex)
    return None


def _pu_numeros_raros(e):
    """Hay en el arbol algun numero que no es para contar (fraccion, decimal, negativo)?"""
    if e[0] == "num":
        return e[1][3] != "entero" or e[1][2] != 1 or (e[1][0] == "-" and not _nu_es_cero(e[1]))
    if e[0] == "neg":
        return True
    if e[0] == "par":
        return _pu_numeros_raros(e[1])
    if e[0] == "op":
        return _pu_numeros_raros(e[2]) or _pu_numeros_raros(e[3])
    return False


def _pu_solo_para_contar(cuerpo):
    """Lo escrito, si lo lee el lector simbolico, solo tiene numeros para contar (si no lo lee, no se sabe: True)."""
    try:
        m = _u_leer(cuerpo)
    except (ValueError, _NuNoSale):
        return True
    arboles = [m["expresion"]] if m["expresion"] is not None else []
    for izq, der in m["relaciones"]:
        arboles.extend((izq, der))
    return not any(_pu_numeros_raros(a) for a in arboles)


def _pu_rota(nombre, ex):
    def falla(t, saber):
        raise ex
    return _pu_puerta(nombre, None, falla, falla)


# ------------------------------------------------------------- explicar y responder, con la puerta elegida

_PU_FORMAS = (
    "FORMAS QUE SI ENTIENDO:\n"
    "  0.1  un objeto o varios  silla,mesa\n"
    "  0.2  forman grupo?       a(color=rojo,forma=cubo); b(color=azul,forma=cubo)\n"
    "  0.2  dame el grupo de... color=rojo: a(color=rojo); b(color=azul)\n"
    "  0.3  pertenece           pertenece color=rojo: taza(color=rojo)\n"
    "  1.0  subitizar          subitizar: x.x/.../x.x\n"
    "  2.1  contar             contar: a, b, c\n"
    "  2.1  revisar            revisar: a,b,c / uno,dos,tres\n"
    "  2.2  siguiente          siguiente: tres\n"
    "  2.2  anterior           anterior: tres\n"
    "  2.2  recitar            recitar: ocho\n"
    "  2.2  revisar_secuencia  revisar_secuencia: uno,dos,cuatro\n"
    "  3.3  listas            listas                 (las dos listas y su diferencia)\n"
    "  3.4  caminos           caminos                (los seis caminos del puente)\n"
    "  3.4  puente            puente: a,b,c          (la coleccion de las tres maneras)\n"
    "  4.1  comparar          comparar: a,b,c / d,e   (mas / menos / tantos_como)\n"
    "  4.2  comparar_cifras   comparar_cifras: 3 / 2  (> < =, la boca mira al mayor)\n"
    "  5.1  descomponer       descomponer: a,b,c,d,e  (todas las maneras de partir en dos)\n"
    "  5.1  componer          componer: a,b / c,d,e   (juntar las partes)\n"
    "  5.2  sumar             sumar: a,b,c / d,e      (agregacion: el signo + y el =)\n"
    "  5.2  anadir            anadir: a,b,c / d,e     (aumentacion: el monton crece)\n"
    "  5.3  sumar_numeros     sumar_numeros: 3 + 2   (numeros, sin objetos)\n"
    "  5.3  descomponer_numero descomponer_numero: 5 (partir un numero)\n"
    "  5.3  comparar_numeros  comparar_numeros: dos / 3 (cifra o palabra)\n"
    "  5.4  quitar            quitar: a,b,c,d,e / dos (resta: quitar de un monton)\n"
    "  5.4  restar_numeros    restar_numeros: 5 - 2  (numeros, sin objetos)\n"
    "  5.5  diferencia        diferencia: a,b,c,d,e / a,b,c (el HUECO entre las dos)\n"
    "  5.5  diferencia_numeros diferencia_numeros: 5 / 3\n"
    "  6.1  nombre             nombre: 47  (y ENSENA como se construyo el nombre)\n"
    "  6.1  numero             numero: cuarenta y siete  (la vuelta)\n"
    "  6.1  decenas            las decenas y el error de decena\n"
    "  7.1  dedos              dedos: 8 + 5  (el METODO de sumar: se anota el primero,\n"
    "                          se cuentan los dedos del segundo y se sigue desde el primero)\n"
    "  2.3  cuantos           cuantos: silla_1, silla_2, silla_3\n"
    "  2.4  dame              dame: a,b,c,d,e / tres\n"
    "  2.4  tiene             tiene: a,b,c / tres\n"
    "  2.5  orden             orden: a,b,c\n"
    "  2.5  conteo            conteo: c,a,b / uno,dos,tres\n"
    "  2.6  misma_cantidad    misma_cantidad: silla_1,silla_2 / sonido_1,sonido_2\n"
    "  3.1  cifra             cifra: tres           (palabra -> cifra)\n"
    "  3.1  palabra           palabra: 3            (cifra   -> palabra)\n"
    "  3.1  cifra_de          cifra_de: a,b,c       (cantidad -> cifra)\n\n"
    "El sistema no adivina: si no entiende, lo dice.")


def _pu_explicar_puerta(p, t, saber):
    """La explicacion de la puerta.  Nunca revienta: un fallo con traceback no ensena nada a quien esta probando, y el
    sistema tiene que saber decir 'no entiendo'."""
    try:
        return p["explicar"](t, saber)
    except Exception as e:  # NUNCA un traceback delante de quien prueba
        if not isinstance(e, ValueError):
            return ("NO ENTIENDO ESTO: se ha roto algo por dentro (%s: %s).\n\n"
                    "El sistema no deberia reventar nunca: lo siento, apuntalo.\n"
                    % (type(e).__name__, e))
        return "NO ENTIENDO ESTO: %s\n\n%s" % (e, _PU_FORMAS)


def _pu_responder_puerta(p, t, saber, salida=None):
    """(respuesta corta, resultado) de la puerta.  Nunca revienta."""
    try:
        if p["responder"] is not None:
            return p["responder"](t, saber)
        if salida is None:
            salida = p["explicar"](t, saber)
        return _pu_ultima(salida, p["mapa"], p["minus"], p["mira_no_entiendo"]), None
    except EntradaDelGrupoEquivocado:
        return "grupo_equivocado", None
    except ValueError:
        return "no_decidible", None
    except Exception:
        return "no_entendido", None


# ------------------------------------------------------------- LA REGLA DE LA RED (una sola, para las dos salidas)

# Lo que una puerta contesta cuando NO llega a una respuesta (U.4: cualquiera de estas deja decidir al resolvedor).
_PU_NO_ES_RESPUESTA = ("no_entiendo", "no_entendido", "todavia_no", "no_sale", "imposible", "no_se_puede",
                       "ninguna_pieza", "no_decidible", "grupo_equivocado", "no_cuadra", "no_razonable",
                       "no_se_resolver", "sin_letra", "no_alcanza")
# En una cuenta SIN letras, solo lo que es no haberla sabido LEER (lo demas es el ano: una respuesta).
_PU_NO_LA_LEYO = ("no_entiendo", "no_entendido", "no_decidible", "grupo_equivocado")
# 'No hay ningun numero' (con lo que se sabe en ese paso: numeros para contar).  Es una respuesta del ano si el
# resolvedor solo encuentra uno que NO es para contar (una fraccion, un negativo); si encuentra uno para contar, o dice
# cualquier numero, la puerta se equivocaba y decide el.
_PU_DEL_ANO = ("no_sale", "imposible", "no_entero", "ninguna")

_PU_ORDEN = re.compile(r"^(ecuacion|hueco|verdad|calcular)\s*:\s*", re.I)


def _pu_cuerpo(t):
    """Lo escrito sin la orden de delante ('ecuacion: 8 + ? = 5' -> '8 + ? = 5'): lo que lee el resolvedor."""
    return _PU_ORDEN.sub("", t).strip()


def _pu_corta(resp):
    """La respuesta corta como conclusion: 'no_entendido' es 'no_entiendo'."""
    return {"no_entendido": "no_entiendo"}.get(resp, resp)


def _pu_resolvedor(cuerpo, saber):
    try:
        return decidir_resolver(cuerpo, saber)
    except Exception:
        return {"conclusion": "no_entiendo"}


def _pu_comprobada(r):
    """Una respuesta COMPROBADA del resolvedor: hecho, cualquier numero, o ninguna porque las relaciones se contradicen
    (probando en orden, 'ninguna' es solo con numeros para contar: no basta)."""
    if r["conclusion"] == "ninguna":
        return not r.get("probado")
    return r["conclusion"] in ("hecho", "cualquiera")


def _pu_para_contar(r):
    """La respuesta del resolvedor son numeros para contar (enteros, no negativos)."""
    if r.get("valores"):
        return all(_bu_para_contar(v) for v in r["valores"].values())
    if r.get("soluciones") is not None:
        return True
    if r.get("valor") is not None:
        return _bu_para_contar(r["valor"])
    return r.get("verdad") is not None


def _pu_decidir(t, saber, resp, p):
    """Quien contesta: 'puerta', 'resolvedor' o 'puerta_del_ano' (se queda la puerta, que contesto lo de su ano, y se
    ensena tambien lo del resolvedor).  LA REGLA DE U.4, una sola (y la de U.3 con palabras)."""
    con = _pu_corta(resp)
    cuerpo = _pu_cuerpo(t)
    if _pu_simbolica(cuerpo):
        if con not in _PU_NO_ES_RESPUESTA and con not in _PU_DEL_ANO:
            return "puerta"                          # la puerta vieja contesta: nada viejo cambia
        try:
            m = _u_leer(cuerpo)
        except (ValueError, _NuNoSale):
            return "puerta"
        orden = _PU_ORDEN.match(t)
        if orden and (bool(m["relaciones"]) != (orden.group(1).lower() != "calcular")):
            return "puerta"                          # la orden pide otra cosa ('verdad: 4 + 1' no tiene igualdad)
        r = None
        if con in _PU_DEL_ANO:
            r = _pu_resolvedor(cuerpo, saber)
            if r["conclusion"] == "hecho" and not _pu_para_contar(r):
                return "puerta_del_ano"              # sin numeros para contar no sale: la respuesta de su ano
            if (r["conclusion"] == "ninguna" and con != "no_sale") or (con == "ninguna" and r["conclusion"] != "cualquiera"):
                return "puerta"                      # los dos dicen que ningun numero: con las palabras de la puerta
        con_letras = bool(m["relaciones"] and m["cantidades"])
        if not con_letras and con not in _PU_NO_LA_LEYO and con not in _PU_DEL_ANO:
            return "puerta"                          # una cuenta sin letras: su 'todavia no' es respetar el ano
        if r is None:
            r = _pu_resolvedor(cuerpo, saber)
        return "resolvedor" if _pu_comprobada(r) else "puerta"
    if _pa_le_toca(t, con, saber):                   # con palabras (U.3)
        return "resolvedor"
    return "puerta"


def _pu_simbolica(t):
    try:
        return es_expresion_simbolica(t)
    except Exception:
        return False


def _pu_hay_que_decidir(t, simbolica):
    """Solo hace falta mirar la red si son numeros y simbolos (tambien detras de 'ecuacion:'...), o si hay palabras."""
    return simbolica or _pu_cuerpo(t) != t or bool(re.search(r"[a-z]{3,}", t.lower()))


def explicar_pregunta(texto, saber=None):
    """LA PUERTA DE ENTRADA de lo que se ensena (UNA tabla: la misma que responder_pregunta)."""
    if saber is None:
        saber = cargar_conocimiento()
    t = texto.strip()
    if es_orden_resolver(t):                         # el resolvedor universal (plan U, fase U.1)
        return explicar_orden_resolver(t, saber)
    simbolica = _pu_simbolica(t)
    p = _pu_elegir_puerta(t, saber, simbolica)
    salida = _pu_explicar_puerta(p, t, saber)
    if p["nombre"] == "simbolica" or not _pu_hay_que_decidir(t, simbolica):
        return salida
    resp, _ = _pu_responder_puerta(p, t, saber, salida if p["responder"] is None else None)
    quien = _pu_decidir(t, saber, resp, p)
    if quien == "resolvedor":
        como = ("lo lee el lector simbolico y lo resuelve el resolvedor universal, U.1-U.4" if _pu_simbolica(_pu_cuerpo(t))
                else "lo lee el lector de palabras y lo resuelve el buscador, U.3")
        lee = _pu_cuerpo(t) if _pu_simbolica(_pu_cuerpo(t)) else t
        return "(la puerta vieja decia: %s; %s; la puerta era '%s')\n\n%s" % (
            _pu_corta(resp).upper().replace("_", " "), como, p["nombre"], explicar_orden_resolver(lee, saber))
    if quien == "puerta_del_ano":
        otra = _pu_r_resolver(_pu_cuerpo(t), saber)
        salida = "%s\n\n  (con numeros para contar, lo de este paso, no hay; el resolvedor universal, con fracciones y\n" \
                 "   negativos, dice: %s.  Pruebalo con  resolver: %s)" % (salida, otra[0], _pu_cuerpo(t))
    return salida


def responder_pregunta(texto, saber=None):
    """La respuesta corta (la de las pruebas y de mis_casos): (respuesta normalizada, resultado).  Nunca revienta."""
    if saber is None:
        saber = cargar_conocimiento()
    t = texto.strip()
    try:
        if es_orden_resolver(t):
            return _pu_r_resolver(t, saber)
    except Exception:
        return "no_entendido", None
    simbolica = _pu_simbolica(t)
    p = _pu_elegir_puerta(t, saber, simbolica)
    resp = _pu_responder_puerta(p, t, saber)
    if p["nombre"] == "simbolica" or not _pu_hay_que_decidir(t, simbolica):
        return resp
    if _pu_decidir(t, saber, resp[0], p) == "resolvedor":
        try:
            return _pu_r_resolver(_pu_cuerpo(t) if _pu_simbolica(_pu_cuerpo(t)) else t, saber)
        except Exception:
            return "no_entendido", None
    return resp


def puerta_de(texto, saber=None):
    """El nombre de la puerta que coge lo escrito (para las pruebas y el comparador)."""
    if saber is None:
        saber = cargar_conocimiento()
    t = texto.strip()
    if es_orden_resolver(t):
        return "resolver"
    return _pu_elegir_puerta(t, saber, _pu_simbolica(t))["nombre"]
