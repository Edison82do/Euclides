# -*- coding: utf-8 -*-
"""
Euclides - Nivel 7 - metodos de calculo (7.1 a 7.5).

Este archivo es UNA PARTE del motor.  No se importa suelto: lo carga sistema/motor.py,
que junta todas las partes en un solo espacio de nombres (por eso aqui se usan funciones
definidas en otras partes sin importarlas).  Ver sistema/partes/__init__.py.
"""

import os  # noqa: F401
import sys  # noqa: F401

# ------------------------------------------------- el metodo de los dedos (7.1)

def decidir_7_1_dedos(texto_a, texto_b, saber=None):
    """
    Unidad 7.1: EL METODO DE LOS DEDOS (sumar contando hacia adelante, mecanico).

      1. se ANOTA el primero (la pizarra),
      2. se cogen con los dedos tantos como el SEGUNDO,
      3. se cuenta HACIA ADELANTE desde el primero, un paso por dedo,
      4. el ultimo numero dicho es el total.

    OJO: el total es DONDE SE PARA.  No tiene que caber en los dedos: los dedos cuentan los PASOS.
    """
    if saber is None:
        saber = cargar_conocimiento()
    pa, ca = nombre_de_numero(texto_a, saber)
    pb, cb = nombre_de_numero(texto_b, saber)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    # PASO N.4: el primero puede ser un numero GRANDE (mas alla de la lista de contar); se LEE
    # por su estructura y se cuenta hacia adelante con 'siguiente' (que sabe pasar de sitio).
    va = _valor_de_cantidad(pa, saber)
    if va is None and pa is not None:
        va = _valor_de_numero(pa, saber)
    vb = _valor_de_cantidad(pb, saber)
    cuenta = {"secuencia": secuencia, "valor_a": va, "valor_b": vb, "_saber": saber}
    r = _aplicar_reglas(saber["reglas_7_1"]["reglas_dedos"], None, None, saber, cuenta=cuenta)
    r["secuencia"] = secuencia
    r["entidades"] = []
    r["texto_a"], r["texto_b"] = texto_a, texto_b
    r["palabra_a"], r["palabra_b"] = pa, pb
    r["venia_en_cifra"] = (ca, cb)
    r["valor_a"], r["valor_b"] = va, vb
    r["dedos"] = _cuantos_dedos(saber)
    if r["conclusion"] != "se_puede":
        return r
    # LA PIZARRA: lo que se ha anotado, y los pasos uno a uno.
    # EL MECANISMO (mecanismo.py): se levantan los dedos del segundo recitando uno, dos...; y por
    # cada dedo que se baja se dice la palabra SIGUIENTE de la lista.  Ninguna suma de Python.
    r["anotado"] = pa
    c = contar_adelante(pa, pb, saber)
    if c["conclusion"] != "se_puede":
        r["conclusion"] = c["conclusion"]
        return r
    r["los_pasos"] = []
    for k, p in enumerate(c["pasos"]):
        r["los_pasos"].append({"dedo": leer(p["dedo_numero"], saber),
                               "dedo_nombre": p["dedo"],
                               "quedan": len(c["pasos"][k + 1:]),     # los dedos que siguen arriba
                               "valor": leer(p["dice"], saber), "palabra": p["dice"]})
    r["total"] = c["resultado"]
    r["total_valor"] = leer(r["total"], saber)
    r["expresion"] = "%s + %s = %s" % (pa, pb, r["total"])
    tabla = _tabla(saber)
    r["cifra_a"], r["cifra_b"] = tabla.get(pa), tabla.get(pb)
    r["cifra_total"] = tabla.get(r["total"]) or str(r["total_valor"])
    r["hay_cifras"] = (r["cifra_a"] is not None and r["cifra_b"] is not None)
    if r["hay_cifras"]:
        r["expresion_cifras"] = "%s + %s = %s" % (r["cifra_a"], r["cifra_b"],
                                                  r["cifra_total"] or r["total"])
    else:
        r["expresion_cifras"] = r["expresion"]
    # LAS CUENTAS DEL AHORRO: contar hacia adelante son tantos pasos como dedos bajados; contar
    # todo desde el uno llega al total (tantos pasos como su sitio); y los que me ahorro son los
    # de antes del primero (su sitio).
    r["pasos_dados"] = len(c["pasos"])
    r["pasos_contando_todo"] = r["total_valor"]
    r["pasos_ahorrados"] = va
    # LA COMPROBACION, TAMBIEN MECANICA: desde el total se cuentan los dedos del segundo HACIA
    # ATRAS (7.4) y tiene que salir el primero.
    vuelta = contar_atras(r["total"], pb, saber)
    r["la_suma_cuadra"] = vuelta.get("resultado") == pa
    r["expresion_inversa"] = "%s - %s = %s" % (r["total"], pb, pa)
    r["verificacion"] = r["la_suma_cuadra"]
    return r


def explicar_7_1_dedos(texto_a, texto_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_7_1_dedos(texto_a, texto_b, saber)
    lineas = ["PREGUNTA (7.1): como se suman estos DOS NUMEROS, MECANICAMENTE?"
              "  (el metodo de los dedos)"]
    lineas.append("NUMEROS:  %s  y  %s" % (texto_a, texto_b))
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  Alguno de los dos no es un numero que conozca (los mios van del CERO al CIEN).")
        return "\n".join(lineas)
    if r["conclusion"] == "no_caben_en_los_dedos":
        lineas.append("RESULTADO: no_caben_en_los_dedos")
        lineas.append("  El SEGUNDO numero es %s, y solo tengo %d dedos." % (r["palabra_b"], r["dedos"]))
        lineas.append("  CONDICION DE APLICACION: al segundo numero no le pueden pasar de %d."
                      % r["dedos"])
        lineas.append("  (El PRIMERO puede ser mas grande, porque no se coge con los dedos: se ANOTA.)")
        return "\n".join(lineas)
    if r["conclusion"] == "no_alcanza":
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  La suma se pasaria de %s, que es hasta donde se contar."
                      % _hasta_donde_cuento(saber).upper())
        return "\n".join(lineas)
    if r["hay_cifras"]:
        lineas.append("EN CIFRAS: %s" % r["expresion_cifras"])
    lineas.append("")
    lineas.append("  PASO 1 - SE ANOTA EL PRIMERO.  El primero no se cuenta: se GUARDA.")
    lineas.append("    PIZARRA:  %s        <- aqui esta anotado, y de aqui no se mueve"
                  % r["anotado"])
    lineas.append("    (esto es la MEMORIA DE TRABAJO: hay que aguantarlo mientras se cuenta.")
    lineas.append("     Es la parte que cuesta, y por eso el sistema tiene la pizarra a la vista)")
    lineas.append("")
    lineas.append("  PASO 2 - SE COGEN CON LOS DEDOS tantos como el SEGUNDO numero (%s)."
                  % r["palabra_b"])
    lineas.append("    dedos levantados: %d  de  %d" % (r["valor_b"], r["dedos"]))
    if r["valor_b"] == 0:
        lineas.append("    (ninguno: el segundo es CERO, asi que no se levanta ni un dedo)")
    lineas.append("")
    lineas.append("  PASO 3 - SE CUENTA HACIA ADELANTE DESDE EL PRIMERO, un paso por dedo.")
    lineas.append("    OJO: se empieza a contar DESDE EL %s, NO desde el uno."
                  % r["anotado"].upper())
    if r["los_pasos"]:
        for p in r["los_pasos"]:
            lineas.append("      dedo %d:  se dice '%s'   (quedan %d dedos)"
                          % (p["dedo"], p["palabra"], p["quedan"]))
    else:
        lineas.append("      (no hay pasos: no se levanto ningun dedo)")
    lineas.append("")
    lineas.append("  PASO 4 - SE ACABARON LOS DEDOS: el ULTIMO numero dicho es el total.")
    lineas.append("    el ultimo numero dicho: %s" % r["total"].upper())
    lineas.append("")
    lineas.append("  ¡OJO CON LA TRAMPA!  El total NO tiene que caber en los dedos:")
    lineas.append("  los dedos cuentan los PASOS, no el resultado.  Aqui %s no cabe en %d dedos,"
                  % (r["total"], r["dedos"]))
    lineas.append("  y no pasa nada.")
    lineas.append("")
    lineas.append("  POR QUE ESTO ES MEJOR QUE CONTAR TODO:")
    lineas.append("    contando hacia adelante (desde el %s):  %d pasos"
                  % (r["anotado"], r["pasos_dados"]))
    lineas.append("    contando todo (desde el uno):           %d pasos"
                  % r["pasos_contando_todo"])
    lineas.append("    -> el mismo resultado, pero %d pasos MENOS."
                  % r["pasos_ahorrados"])
    lineas.append("    Contar todo es lo que hace quien aun no sabe sumar.  Y cuanto mas grandes son")
    lineas.append("    los numeros, mas se nota la diferencia.")
    lineas.append("")
    lineas.append("  COMPROBACION (al total se le quita el segundo y vuelve el primero):")
    lineas.append("    %s ... %s" % (r["expresion_inversa"],
                                     "SI" if r["verificacion"] else "NO"))
    if not r["verificacion"]:
        lineas.append("    NO CUADRA. El sistema no elige uno: lo dice.")
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["expresion"])
    lineas.append("  %s   (%s mas %s igual a %s)" % (r["expresion"], r["palabra_a"],
                                                     r["palabra_b"], r["total"]))
    lineas.append("")
    lineas.append("  Y ES MECANICO: todo lo que hay arriba sale de los cuatro pasos.  Nada se sabe")
    lineas.append("  de memoria ni sale de una calculadora (decision de Carlos, 4 oct 2026).")
    lineas.append("")
    lineas.append("  LA OTRA VIA (derivar, unidad 7.2): si este segundo numero pasa del DIEZ, los dedos")
    lineas.append("  ya no llegan... pero DERIVAR (hacer diez) SI.  El sistema prueba las dos cuando puede.")
    otra = decidir_7_2_derivar(texto_a, texto_b, saber)
    if otra["conclusion"] == "se_puede":
        lineas.append("    DERIVANDO: %s   (y no cuenta nada: hace diez y sumo lo que sobra)"
                      % otra["expresion"])
        lineas.append("    -> las dos vias dan lo mismo: %s"
                      % ("SI" if otra["total_valor"] == r["total_valor"] else "NO"))
    else:
        lineas.append("    DERIVAR aqui dice: %s" % otra["conclusion"])
    return "\n".join(lineas)


# ------------------------------------------------- derivar / hacer diez (7.2)

def decidir_7_2_derivar(texto_a, texto_b, saber=None):
    """
    Unidad 7.2: DERIVAR (hacer diez).  Usar lo que ya se sabe para NO contar.

      7 + 5  ->  al 7 le faltan 3 para diez
              ->  parto el 5 en 3 y 2
              ->  7 + 3 = 10, y 10 + 2 = 12

    No hace falta nada nuevo: se COMBINAN la particion (5.1) y la suma (5.2).
    """
    if saber is None:
        saber = cargar_conocimiento()
    pa, ca = nombre_de_numero(texto_a, saber)
    pb, cb = nombre_de_numero(texto_b, saber)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    va = _valor_de_cantidad(pa, saber)
    vb = _valor_de_cantidad(pb, saber)
    cuenta = {"secuencia": secuencia, "valor_a": va, "valor_b": vb, "_saber": saber}
    r = _aplicar_reglas(saber["reglas_7_2"]["reglas_derivar"], None, None, saber, cuenta=cuenta)
    r["secuencia"] = secuencia
    r["entidades"] = []
    r["texto_a"], r["texto_b"] = texto_a, texto_b
    r["palabra_a"], r["palabra_b"] = pa, pb
    r["valor_a"], r["valor_b"] = va, vb
    if r["conclusion"] != "se_puede":
        return r
    # EL MECANISMO: cuantos le faltan al primero para DIEZ (contar de el hasta diez); se PARTE el
    # segundo quitandole esos (contar hacia atras); y desde diez se sigue con lo que sobra.
    faltan_p = contar_hasta(pa, "diez", saber)
    sobra_p = contar_atras(pb, faltan_p, saber)["resultado"]
    total_p = contar_adelante("diez", sobra_p, saber)["resultado"]
    faltan, sobra = leer(faltan_p, saber), leer(sobra_p, saber)
    r["faltan_para_diez"] = faltan
    r["sobra_del_segundo"] = sobra
    r["parte_para_diez"] = faltan
    r["parte_que_sobra"] = sobra
    r["primera_cuenta"] = "10" if faltan else "0"
    r["total_valor"] = leer(total_p, saber)
    r["total"] = total_p
    r["paso_1"] = "%d + %d = 10" % (va, faltan)
    r["paso_2"] = "10 + %d = %d" % (sobra, r["total_valor"])
    r["expresion"] = "%s + %s = %s" % (pa, pb, r["total"])
    r["suma_de_tres"] = "%d + %d + %d" % (va, faltan, sobra)
    tabla = _tabla(saber)
    r["cifra_a"], r["cifra_b"] = tabla.get(pa), tabla.get(pb)
    r["cifra_total"] = tabla.get(r["total"]) or str(r["total_valor"])
    if r["cifra_a"] is not None and r["cifra_b"] is not None:
        r["expresion_cifras"] = "%s + %s = %s" % (r["cifra_a"], r["cifra_b"],
                                                  r["cifra_total"] or r["total"])
    else:
        r["expresion_cifras"] = r["expresion"]
    # comprobaciones con el mismo mecanismo: las dos partes juntas dan el segundo, y el primero
    # con su parte llega justo a diez
    r["las_partes_cuadran"] = contar_adelante(faltan_p, sobra_p, saber).get("resultado") == pb
    r["verificacion"] = contar_adelante(pa, faltan_p, saber).get("resultado") == "diez"
    # LA OTRA VIA: los dedos tienen que decir lo mismo (decision de Carlos: que pruebe las dos).
    otra = decidir_7_1_dedos(texto_a, texto_b, saber)
    r["la_otra_via"] = otra
    if otra["conclusion"] == "se_puede":
        r["las_dos_vias_coinciden"] = (otra["total_valor"] == r["total_valor"])
        r["la_otra_via_dice"] = otra["total"]
        r["la_otra_via_pasos"] = otra["pasos_dados"]
    else:
        r["las_dos_vias_coinciden"] = None
        r["la_otra_via_dice"] = None
    return r


def explicar_7_2_derivar(texto_a, texto_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_7_2_derivar(texto_a, texto_b, saber)
    lineas = ["PREGUNTA (7.2): como se suman estos DOS NUMEROS DERIVANDO?"
              "  (hacer diez: usar lo que ya sabes, sin contar)"]
    lineas.append("NUMEROS:  %s  y  %s" % (texto_a, texto_b))
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  Alguno de los dos no es un numero que conozca (los mios van del CERO al CIEN).")
        return "\n".join(lineas)
    if r["conclusion"] == "necesito_las_columnas":
        lineas.append("RESULTADO: necesito_las_columnas")
        lineas.append("  El primero (%s) es de DOS cifras, y mi 'hacer diez' es para numeros de UNA."
                      % r["palabra_a"])
        lineas.append("  CONDICION DE APLICACION: partir y completar diez necesita una cifra.")
        lineas.append("  Con dos cifras hay que ir por COLUMNAS: unidad con unidad, decena con decena")
        lineas.append("  (unidad 7.3, que todavia no esta).  No lo hago mal: lo digo.")
        return "\n".join(lineas)
    if r["conclusion"] == "no_hace_falta":
        lineas.append("RESULTADO: no_hace_falta")
        lineas.append("  %s y %s ya suman %s, y NO cruzan el diez: no hay nada que hacer."
                      % (r["palabra_a"], r["palabra_b"], contar_adelante(r["palabra_a"], r["palabra_b"],
                                                                         saber)["resultado"]))
        lineas.append("  Derivar sirve para cuando la suma PASA de diez (7 + 5, 8 + 4, 9 + 9).")
        return "\n".join(lineas)
    if r["hay_cifras"] if "hay_cifras" in r else False:
        pass
    lineas.append("")
    lineas.append("  ESTO NO ES CONTAR: es TRANSFORMAR la cuenta en dos cuentas mas faciles, y una")
    lineas.append("  de ellas (%s) ya la se." % ("llegar a diez"))
    lineas.append("")
    lineas.append("  PASO 1 - ¿CUANTO LE FALTA AL PRIMERO PARA LLEGAR A DIEZ?")
    lineas.append("    al %s le faltan %d  (porque %d + %d = 10)"
                  % (r["palabra_a"], r["faltan_para_diez"], r["valor_a"], r["faltan_para_diez"]))
    lineas.append("")
    lineas.append("  PASO 2 - PARTO EL SEGUNDO EN DOS, PARA SEPARAR ESA PARTE  (es partir, unidad 5.1)")
    lineas.append("    %s  =  %d  +  %d" % (r["palabra_b"], r["parte_para_diez"], r["parte_que_sobra"]))
    lineas.append("    (la primera parte es la que hace diez; la segunda es la que sobra)")
    lineas.append("")
    lineas.append("  PASO 3 - HAGO DIEZ, y luego sumo lo que sobra:")
    lineas.append("    %s        <- aqui ya hay DIEZ" % r["paso_1"])
    lineas.append("    %s        <- y esto es sumarle lo que sobraba" % r["paso_2"])
    lineas.append("")
    lineas.append("  LA CUENTA ENTERA ES UNA SUMA DE TRES:  %s = %d"
                  % (r["suma_de_tres"], r["total_valor"]))
    lineas.append("")
    lineas.append("  COMPROBACION DE LA DERIVACION (las dos partes tienen que ser el segundo):")
    lineas.append("    %d + %d = %d ... %s"
                  % (r["parte_para_diez"], r["parte_que_sobra"], r["valor_b"],
                     "SI" if r["las_partes_cuadran"] else "NO"))
    lineas.append("    y los dos pasos: %s y %s ... %s"
                  % (r["paso_1"], r["paso_2"], "SI" if r["verificacion"] else "NO"))
    lineas.append("")
    lineas.append("  LAS DOS VIAS (prueba de Carlos: que pruebe las dos):")
    if r["las_dos_vias_coinciden"] is None:
        lineas.append("    los DEDOS no pueden hacer esta cuenta (el segundo pasa de diez),")
        lineas.append("    asi que aqui solo hay una via.")
    else:
        lineas.append("    DERIVANDO (esto):  %s" % r["total"])
        lineas.append("    CON LOS DEDOS (7.1): %s, y costaria %d pasos"
                      % (r["la_otra_via_dice"], r["la_otra_via_pasos"]))
        lineas.append("    -> las dos dan lo mismo: %s"
                      % ("SI" if r["las_dos_vias_coinciden"] else "NO. ¡NO CUADRAN!"))
        lineas.append("    La diferencia: derivando NO se cuenta nada.")
    lineas.append("")
    lineas.append("  POR QUE DERIVAR ES MEJOR QUE CONTAR (esta medido, no es una opinion):")
    lineas.append("    'los metodos de contar hacia adelante no solo son menos eficientes, estan")
    lineas.append("     asociados con un RENDIMIENTO MAS BAJO... los alumnos de rendimiento alto")
    lineas.append("     tienden a usar HECHOS DERIVADOS'  (Tall y Gray, citado por Number Sense Maths)")
    lineas.append("    Y '8 + 9' casi nadie lo tiene memorizado: solo el 5% de los profesores dice")
    lineas.append("    'saberlo'; la mayoria lo deriva.  (Number Sense Maths)")
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["expresion"])
    lineas.append("  %s   (%s mas %s igual a %s)" % (r["expresion"], r["palabra_a"],
                                                     r["palabra_b"], r["total"]))
    lineas.append("")
    lineas.append("  Y NO SE SABE DE MEMORIA NI SE USA CALCULADORA: sale de partir y de hacer diez,")
    lineas.append("  que ya estaban en el sistema.  Derivar es COMBINAR lo que ya se sabe.")
    return "\n".join(lineas)



# ------------------------------------------------- sumar por columnas (7.3)

def decidir_7_3_columnas(texto_a, texto_b, saber=None, verificar=True):
    """
    Unidad 7.3: SUMAR POR COLUMNAS.  Unidad con unidad, decena con decena, y el llevarse.

      47 + 15  ->  7+5 = 12 (anoto 2, me llevo 1);  4+1+1 = 6  ->  62

    El llevarse NO es un truco: es RE-AGRUPAR (diez unidades hacen una decena, unidad 6.2).
    """
    if saber is None:
        saber = cargar_conocimiento()
    # UNIDAD 7.6: si el total pasa de cien, hace falta la columna de las CENTENAS.
    if _va_a_la_7_6("+", texto_a, texto_b, saber):
        return decidir_7_6_columnas(texto_a, "+", texto_b, saber, verificar=verificar)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    pa, ca = nombre_de_numero(texto_a, saber)
    pb, cb = nombre_de_numero(texto_b, saber)
    va, vb = _valor_de_numero(pa, saber), _valor_de_numero(pb, saber)
    cuenta = {"valor_a": va, "valor_b": vb, "secuencia": secuencia, "_saber": saber}
    r = _aplicar_reglas(saber["reglas_7_3"]["reglas_columnas"], None, None, saber, cuenta=cuenta)
    r["texto_a"], r["texto_b"] = texto_a, texto_b
    r["palabra_a"], r["palabra_b"] = pa, pb
    r["valor_a"], r["valor_b"] = va, vb
    if r["conclusion"] != "se_puede":
        return r
    # --- LAS DOS COLUMNAS (todo con el MECANISMO: dedos, y leer y escribir cifras) ------------
    ca_, cb_ = cifras_de(va), cifras_de(vb)          # LEER: 47 -> [7, 4]
    ua, ub = ca_[0], cb_[0]
    da, db = escribir_cifras(ca_[1:]), escribir_cifras(cb_[1:])    # lo que queda son DECENAS
    col_u = _suma_con_metodo(ua, ub, saber)          # la columna de las unidades, con los dedos
    suma_unidades = col_u["total"]
    pasa = viene_despues(col_u["palabra_total"], "nueve", saber)    # PASA DE NUEVE?
    se_lleva = 1 if pasa else 0
    # lo que se anota es lo que hay que contar DESDE DIEZ hasta la suma (12 -> dos)
    anota_unidades = leer(contar_hasta("diez", col_u["palabra_total"], saber), saber) if pasa \
        else suma_unidades
    col_d = _dos_pasos(da, db, 1, saber) if se_lleva else _suma_con_metodo(da, db, saber)
    suma_decenas = col_d["total"]
    total = escribir_cifras([anota_unidades] + cifras_de(suma_decenas))   # ESCRIBIR: 6 y 2 -> 62
    r["unidades_a"], r["unidades_b"] = ua, ub
    r["decenas_a"], r["decenas_b"] = da, db
    r["suma_unidades"] = suma_unidades
    r["se_lleva"] = se_lleva
    r["anota_unidades"] = anota_unidades
    r["suma_decenas"] = suma_decenas
    r["total_valor"] = total
    r["cuenta_unidades"] = "%d + %d = %d" % (ua, ub, suma_unidades)
    r["cuenta_decenas"] = ("%d + %d + %d = %d" % (da, db, se_lleva, suma_decenas) if se_lleva
                           else "%d + %d = %d" % (da, db, suma_decenas))
    r["hay_que_llevarse"] = se_lleva > 0
    r["total"] = _palabra_de(total, secuencia) if total else "cero"
    r["tabla"] = _tabla(saber)
    r["expresion"] = "%s + %s = %s" % (pa, pb, r["total"])
    r["expresion_cifras"] = "%d + %d = %d" % (va, vb, total)
    # COMPROBACIONES (con el mecanismo, no con Python)
    # - juntar otra vez decenas y unidades (6.5) da el total
    jd = decidir_6_5_juntar_decenas(str(suma_decenas), str(anota_unidades), saber)
    r["recompone"] = jd.get("total") == total
    # - lo que se lleva es una decena: desde diez, contando lo anotado, sale la suma de la columna
    r["el_llevado_es_una_decena"] = (not se_lleva) or \
        contar_adelante("diez", decir(anota_unidades, saber), saber).get("resultado") == col_u["palabra_total"]
    r["lleva_como_mucho_uno"] = se_lleva <= 1   # 9+9=18 -> se lleva 1, nunca 2
    r["sin_llevarse_daria_mal"] = bool(se_lleva) and \
        _suma_con_metodo(da, db, saber)["total"] != suma_decenas
    # - LA VUELTA: restando por columnas (7.5) el segundo, tiene que salir el primero
    if verificar:
        v = decidir_7_5_columnas(str(total), str(vb), saber, verificar=False)
        r["verificacion"] = v["conclusion"] == "se_puede" and v["resta"] == va
        r["verificacion_texto"] = "%d - %d = %s" % (total, vb, v.get("resta"))
    return r


def explicar_7_3_columnas(texto_a, texto_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    if _va_a_la_7_6("+", texto_a, texto_b, saber):
        return explicar_7_6_columnas(texto_a, "+", texto_b, saber)
    r = decidir_7_3_columnas(texto_a, texto_b, saber)
    lineas = ["PREGUNTA (7.3): sumar estos DOS NUMEROS por COLUMNAS"
              "  (unidad con unidad, decena con decena, y el llevarse)"]
    lineas.append("NUMEROS:  %s  y  %s" % (texto_a, texto_b))
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  Alguno no es un numero que conozca (los mios van del CERO al CIEN).")
        return "\n".join(lineas)
    if r["conclusion"] == "no_alcanza":
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  La suma se pasa de CIEN (%s + %s), y mi tabla llega al cien."
                      % (r["valor_a"], r["valor_b"]))
        lineas.append("  No me lo invento: mas alla del cien no tengo sitio.")
        return "\n".join(lineas)
    va, vb = r["valor_a"], r["valor_b"]
    lineas.append("")
    lineas.append("  SE PONE UNO DEBAJO DEL OTRO y se suman las COLUMNAS:")
    lineas.append("")
    lineas.append("       %s" % va)
    lineas.append("     + %s" % vb)
    lineas.append("     " + "-" * (max(len(str(va)), len(str(vb))) + 2))
    lineas.append("")
    lineas.append("  PASO 0 - SE PARTE CADA NUMERO EN DECENAS Y UNIDADES (unidad 6.5):")
    lineas.append("    %d = %d decenas y %d unidades   |   %d = %d decenas y %d unidades"
                  % (va, r["decenas_a"], r["unidades_a"], vb, r["decenas_b"], r["unidades_b"]))
    lineas.append("")
    lineas.append("  PASO 1 - COLUMNA DE LAS UNIDADES (se empieza por la derecha):")
    su = _suma_con_metodo(cifras_de(va)[0], cifras_de(vb)[0], saber)
    lineas.append("    la suma es %s, y NO se sabe de memoria: %s" % (r["cuenta_unidades"],
                                                                      su["como"] or "con el metodo"))
    lineas.append("    (el metodo: %s -- unidad 7.1/7.2.  Se hace con el mecanismo, no con una"
                  " calculadora.)" % su["metodo"])
    if r["hay_que_llevarse"]:
        lineas.append("    -> %d PASA DE NUEVE.  Y %d son UNA DECENA Y %d UNIDADES"
                      % (r["suma_unidades"], r["suma_unidades"], r["anota_unidades"]))
        lineas.append("       (diez unidades hacen una decena: unidad 6.2).")
        lineas.append("    -> se ANOTA el %d en las unidades" % r["anota_unidades"])
        lineas.append("    -> y me LLEVO %d DECENA para la columna siguiente" % r["se_lleva"])
    else:
        lineas.append("    -> NO pasa de nueve: se anota el %d y no hay nada que llevarse."
                      % r["anota_unidades"])
    lineas.append("")
    lineas.append("  PASO 2 - COLUMNA DE LAS DECENAS (en DOS PASOS, porque sumar TRES numeros de")
    lineas.append("  golpe no es un metodo que el sistema tenga):")
    dp = _dos_pasos(r["decenas_a"], r["decenas_b"], r["se_lleva"], saber)
    p1, p2 = dp["paso_1"], dp["paso_2"]
    if r["hay_que_llevarse"]:
        lineas.append("    PRIMERO los dos de arriba:  %d + %d = %d" % (p1["a"], p1["b"], p1["total"]))
        lineas.append("      (el metodo: %s)" % (p1["metodo"] or "no hace falta: no cruza el diez"))
        lineas.append("    Y LUEGO le sumo la que me llevo:  %d + %d = %d"
                      % (p2["a"], p2["b"], p2["total"]))
        lineas.append("      (el metodo: %s)" % (p2["metodo"] or "no hace falta: no cruza el diez"))
        lineas.append("    -> %d + %d + %d = %d, en dos pasos" % (r["decenas_a"], r["decenas_b"],
                                                                 r["se_lleva"], r["suma_decenas"]))
        lineas.append("    OJO: si me olvidara de la que me llevo, me quedaria en %d, y seria FALSO."
                      % p1["total"])
    else:
        lineas.append("    %d + %d = %d   (no hay nada que llevarse)"
                      % (p1["a"], p1["b"], p1["total"]))
    lineas.append("")
    lineas.append("  LA CUENTA ENTERA:")
    lineas.append("    %d decenas y %d unidades  ->  %s" % (r["suma_decenas"], r["anota_unidades"],
                                                            r["total"]))
    lineas.append("    (y NO se escribe '%d x 10': el sistema todavia no sabe multiplicar.  Se dice"
                  % r["suma_decenas"])
    lineas.append("     'son %d decenas', que es lo que si sabe: juntar decenas, unidad 6.5.)"
                  % r["suma_decenas"])
    lineas.append("")
    lineas.append("  COMPROBACIONES:")
    lineas.append("    - juntando las columnas: %d decenas y %d unidades son %d ... %s"
                  % (r["suma_decenas"], r["anota_unidades"], r["total_valor"],
                     "SI" if r["recompone"] else "NO"))
    if r["hay_que_llevarse"]:
        lineas.append("    - el llevado es una decena entera: %d son %d unidad y 1 decena ... %s"
                      % (r["suma_unidades"], r["anota_unidades"],
                         "SI" if r["el_llevado_es_una_decena"] else "NO"))
        lineas.append("    - y lo que se lleva NUNCA puede ser mas de 1: 9+9=18, o sea una decena"
                      " ... %s" % ("SI" if r["lleva_como_mucho_uno"] else "NO"))
    lineas.append("    - la vuelta (partir el total, unidad 5.1): %s y %s tienen que salir de %d ... %s"
                  % (r["valor_a"], r["valor_b"], r["total_valor"],
                     "SI" if r["verificacion"] else "NO"))
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["expresion_cifras"])
    lineas.append("")
    lineas.append("  Y ESTO ES LA NOTA 7, PALABRA POR PALABRA: sumar \"unidad con unidad, luego")
    lineas.append("  decena con decena, y si pasa de 9 se anota la unidad y la decena que se lleva")
    lineas.append("  se suma con lo siguiente\".")
    lineas.append("  Y EL LLEVARSE NO ES UN TRUCO: es RE-AGRUPAR.  Las DIEZ unidades que sobran se")
    lineas.append("  convierten en una DECENA que sube a su columna -- lo mismo que ya sabia hacer")
    lineas.append("  al juntar (unidad 6.5).")
    return "\n".join(lineas)


# ------------------------------------------------- la resta con los dedos (7.4)

def decidir_7_4_resta_dedos(texto_a, texto_b, saber=None):
    """
    Unidad 7.4: LA RESTA CON LOS DEDOS.  Se toma el primero, se van BAJANDO los del segundo, y los
    dedos que quedan son el resultado.

      9 - 4  ->  se levantan 9 (del 1 al 9), se bajan 4, quedan 5.

    **LO QUE CAZO CARLOS (4 oct 2026, por la tarde):** la version anterior exigia que EL PRIMERO
    cupiera en los dedos (no pasar de diez), y eso era MAL, por dos razones:

      1. CONTradecia a la suma: la 7.1 ya funciona asi -- los dedos cuentan los PASOS, y el primero
         se anota; el total NO tiene que caber ("no tiene que caber en los dedos").
      2. Y es que los diez dedos NO tienen que representar el numero entero: representan la VENTANA
         DE LOS ULTIMOS DIEZ, terminando en el minuendo.  Para 12 - 5 los dedos van DEL 3 AL 12; se
         bajan 5 y quedan 7.  Y asi CABE 45 - 7 (dedos del 36 al 45, se bajan 7, quedan 38).

    ES DECIR: lo unico que tiene que caber en los dedos es EL SEGUNDO (el que se baja).  El primero
    puede ser tan grande como quiera: solo marca DONDE ACABA la ventana.
    """
    if saber is None:
        saber = cargar_conocimiento()
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    pa, ca = nombre_de_numero(texto_a, saber)
    pb, cb = nombre_de_numero(texto_b, saber)
    va = _valor_de_cantidad(pa, saber)
    vb = _valor_de_cantidad(pb, saber)
    # Se le pasa la cuenta en el MISMO formato que la unidad 5.4, para REUTILIZAR su primitiva
    # ('no se puede quitar mas de lo que hay') y no escribir una segunda verdad.
    escena_54 = coleccion_de(pa, saber) if va is not None else []
    cuenta = {"secuencia": secuencia, "valor_a": va, "valor_b": vb, "pedido_valor": vb,
              "otra": coleccion_de(pb, saber) if vb is not None else [],
              # La primitiva 'segundo_pasa_de_diez' es la de la 7.1 y necesita saber cuantos dedos
              # hay: hay que pasarle '_saber', igual que hace la 7.1.  Si no, revienta.
              "_saber": saber}
    r = _aplicar_reglas(saber["reglas_7_4"]["reglas_resta_dedos"], escena_54, None, saber,
                        cuenta=cuenta)
    r["secuencia"] = secuencia
    r["texto_a"], r["texto_b"] = texto_a, texto_b
    r["palabra_a"], r["palabra_b"] = pa, pb
    r["valor_a"], r["valor_b"] = va, vb
    r["dedos"] = _cuantos_dedos(saber)
    if r["conclusion"] != "se_puede":
        return r
    # EL MECANISMO: se baja un dedo por cada uno del segundo, diciendo la palabra ANTERIOR.
    c = contar_atras(pa, pb, saber)
    if c["conclusion"] != "se_puede":
        r["conclusion"] = c["conclusion"]
        return r
    r["resta"] = c["resultado"]
    quedan = leer(r["resta"], saber)
    r["quedan"] = quedan
    r["expresion"] = "%s - %s = %s" % (pa, pb, r["resta"])
    tabla = _tabla(saber)
    r["cifra_a"], r["cifra_b"] = tabla.get(pa, str(va) if va is not None else None), \
                                 tabla.get(pb, str(vb) if vb is not None else None)
    r["cifra_resta"] = tabla.get(r["resta"], str(quedan))
    r["expresion_cifras"] = "%s - %s = %s" % (r["cifra_a"], r["cifra_b"], r["cifra_resta"])
    # LA VENTANA DE LOS DEDOS: los diez dedos son los ULTIMOS DIEZ numeros, y el ultimo es el
    # minuendo.  Si el minuendo es 12, la ventana es del 3 al 12.  Si es 9, del 1 al 9.
    # (Mecanico: se ponen los dedos en las ultimas palabras que acaban en el primero, hacia atras,
    #  hasta que se acaban los dedos o se llega al uno.)
    ventana = []
    w = pa
    for _dedo in DEDOS_CON_NOMBRE:
        if w is None or w == "cero":
            break
        ventana.append(w)
        w = anterior(w, saber)
    r["desde"] = leer(ventana[-1], saber) if ventana else 1
    r["dedos_levantados"] = len(ventana)
    r["ventana"] = (r["desde"], va)
    r["cabe_entero"] = (not ventana) or ventana[-1] == "uno"
    # EL PASO A PASO: los dedos que se van bajando, con el numero que va quedando
    r["bajadas"] = [{"bajo": leer(p["dedo_numero"], saber), "quedan": leer(p["dice"], saber)}
                    for p in c["pasos"]]
    r["pasos_dados"] = len(c["pasos"])
    # LA VUELTA: la suma deshace la resta (unidad 7.1)
    vuelta = decidir_7_1_dedos(r["resta"], pb, saber)
    r["vuelta"] = vuelta
    r["verificacion"] = (vuelta["conclusion"] == "se_puede" and vuelta["total_valor"] == va)
    r["verificacion_texto"] = ("%s + %s = %s" % (r["resta"], pb, pa))
    return r


def explicar_7_4_resta_dedos(texto_a, texto_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_7_4_resta_dedos(texto_a, texto_b, saber)
    lineas = ["PREGUNTA (7.4): como se resta MECANICAMENTE?  (el metodo de los dedos, AL REVES que"
              " la suma)"]
    lineas.append("NUMEROS:  %s  y  %s" % (texto_a, texto_b))
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  Alguno de los dos no es un numero que conozca.")
        return "\n".join(lineas)
    if r["conclusion"] == "no_caben_en_los_dedos":
        lineas.append("RESULTADO: no_caben_en_los_dedos")
        lineas.append("  El que se BAJA (%s) es mas grande que mis %d dedos: no puedo bajar %d dedos"
                      % (r["palabra_b"], r["dedos"], r["valor_b"]))
        lineas.append("  si solo tengo %d.  Y lo que tiene que caber es EL QUE SE BAJA (el segundo),"
                      " no el primero: el primero solo marca DONDE ACABA la ventana."
                      % r["dedos"])
        return "\n".join(lineas)
    if r["conclusion"] == "no_hay_bastantes":
        lineas.append("RESULTADO: no_hay_bastantes")
        lineas.append("  No se pueden bajar mas dedos de los que hay: hay %s y se quieren bajar %s."
                      % (r["palabra_a"], r["palabra_b"]))
        lineas.append("  Eso seria una resta NEGATIVA, y aqui no existe (unidad 5.4).")
        return "\n".join(lineas)
    lineas.append("")
    lineas.append("  OJO: ES AL REVES QUE LA SUMA.  En la suma se toman los dedos del SEGUNDO y se")
    lineas.append("  cuenta hacia adelante desde el primero.  Aqui se toma EL PRIMERO y se van")
    lineas.append("  BAJANDO los del segundo.  Es CONTAR HACIA ATRAS.")
    lineas.append("")
    lineas.append("  PASO 1 - LOS DEDOS REPRESENTAN LA VENTANA DE LOS ULTIMOS DIEZ NUMEROS, y el")
    lineas.append("  ultimo de ellos es el MINUENDO (%s)." % r["palabra_a"])
    if r["cabe_entero"]:
        lineas.append("    dedos levantados: del 1 al %d  (%d dedos)" % (r["valor_a"],
                                                                      r["dedos_levantados"]))
    else:
        lineas.append("    %s no cabe entero en los dedos, pero NO HACE FALTA: los dedos van del"
                      " %d al %d" % (r["palabra_a"], r["desde"], r["valor_a"]))
        lineas.append("    (%d dedos, y el ultimo marca donde ACABA la cuenta)" % r["dedos_levantados"])
        lineas.append("    Y asi cabe cualquier minuendo: lo que tiene que caber es lo que se BAJA.")
    lineas.append("")
    lineas.append("  PASO 2 - SE VAN BAJANDO tantos como el SEGUNDO (%s), uno a uno." % r["palabra_b"])
    for b in r["bajadas"]:
        lineas.append("    bajo %d:  van quedando %d" % (b["bajo"], b["quedan"]))
    lineas.append("")
    lineas.append("  PASO 3 - LOS DEDOS QUE QUEDAN SON EL RESULTADO.")
    lineas.append("    quedan levantados: %d" % r["quedan"])
    lineas.append("")
    lineas.append("  POR QUE ESTO ES 'QUITAR' (unidad 5.4): primero habia %s, se van %s, ahora quedan"
                  " %s." % (r["palabra_a"], r["palabra_b"], r["resta"]))
    lineas.append("  Y los dedos que quedan son, literalmente, LO QUE QUEDA DESPUES DE QUE SE VAYAN.")
    lineas.append("")
    lineas.append("  LA CUENTA DE LOS PASOS:")
    lineas.append("    empezando en %d y contando hacia atras %d veces se llega a %d"
                  % (r["valor_a"], r["pasos_dados"], r["quedan"]))
    lineas.append("")
    lineas.append("  VERIFICACION (la vuelta: la suma deshace la resta):")
    lineas.append("    %s ... %s" % (r["verificacion_texto"], "SI" if r["verificacion"] else "NO"))
    lineas.append("    (y esa suma la hace con SU mecanismo, el de los dedos hacia adelante, 7.1)")
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["expresion"])
    lineas.append("")
    lineas.append("  Y ES MECANICO: se dan %d pasos, uno por dedo.  No se sabe de memoria ni se usa"
                  " calculadora." % r["pasos_dados"])
    return "\n".join(lineas)


# ------------------------------------------------- restar por columnas (7.5)

def _dec_u(d, u):
    """Escribe '3 decenas y 1 unidad' (en singular cuando toca)."""
    return "%d %s y %d %s" % (d, "decena" if d == 1 else "decenas", u,
                              "unidad" if u == 1 else "unidades")


def _resta_con_metodo(a, b, saber):
    """
    Hace una resta (de una columna) y devuelve COMO se hizo, para poder ENSENARLO.
    El resultado SALE del mecanismo de la 7.4 (dedos hacia atras): no se sabe de memoria y no se
    calcula con Python.  Si no hay mecanismo que valga, NO se inventa: se dice.
    """
    pa, pb = decir(a, saber), decir(b, saber)
    ded = decidir_7_4_resta_dedos(pa, pb, saber)
    if ded["conclusion"] != "se_puede":
        raise ValueError("no tengo mecanismo para %s - %s (%s)" % (a, b, ded["conclusion"]))
    queda = ded["quedan"]
    d = {"a": a, "b": b, "queda": queda, "palabra_a": pa, "palabra_b": pb,
         "palabra_queda": ded["resta"], "metodo": "dedos (7.4)", "ventana": ded.get("ventana")}
    if ded.get("cabe_entero"):
        d["como"] = ("se levantan %s y se bajan %d dedos: quedan %s" % (pa, b, d["palabra_queda"]))
    else:
        d["como"] = ("los dedos van del %d al %d (el ultimo es %s), y se bajan %d: quedan %s"
                     % (ded["desde"], a, pa, b, d["palabra_queda"]))
    d["cuenta"] = "%d - %d = %d" % (a, b, queda)
    return d


def decidir_7_5_columnas(texto_a, texto_b, saber=None, verificar=True):
    """
    Unidad 7.5: RESTAR POR COLUMNAS.  Columna a columna, y si las unidades de arriba no llegan, se
    CAMBIA una decena por diez unidades (el intercambio, que NO es un prestamo).

      72 - 45  ->  2-5 no llega -> 72 = 6 dec y 12 u -> 12-5=7 -> 6-4=2  ->  27
      58 - 27  ->  8-7=1 y 5-2=3 sin cambiar nada                      ->  31
    """
    if saber is None:
        saber = cargar_conocimiento()
    # UNIDAD 7.6: si el de arriba pasa de cien, hace falta la columna de las CENTENAS.
    if _va_a_la_7_6("-", texto_a, texto_b, saber):
        return decidir_7_6_columnas(texto_a, "-", texto_b, saber, verificar=verificar)
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    pa, ca = nombre_de_numero(texto_a, saber)
    pb, cb = nombre_de_numero(texto_b, saber)
    va = _valor_de_cantidad(pa, saber)
    vb = _valor_de_cantidad(pb, saber)
    escena_54 = coleccion_de(pa, saber) if va is not None else []
    cuenta = {"secuencia": secuencia, "valor_a": va, "valor_b": vb, "pedido_valor": vb,
              "texto_a": texto_a, "texto_b": texto_b,
              "otra": coleccion_de(pb, saber) if vb is not None else []}
    r = _aplicar_reglas(saber["reglas_7_5"]["reglas_columnas_resta"], escena_54, None, saber,
                        cuenta=cuenta)
    r["secuencia"] = secuencia
    r["texto_a"], r["texto_b"] = texto_a, texto_b
    r["palabra_a"], r["palabra_b"] = pa, pb
    r["valor_a"], r["valor_b"] = va, vb
    if r["conclusion"] != "se_puede":
        return r
    # PASO 0 - partir cada numero (unidad 6.5)
    # (LEER las cifras: la ultima son las unidades y lo de delante son las decenas)
    ca_, cb_ = cifras_de(va), cifras_de(vb)
    r["dec_a"], r["uni_a"] = escribir_cifras(ca_[1:]), ca_[0]
    r["dec_b"], r["uni_b"] = escribir_cifras(cb_[1:]), cb_[0]
    # PASO 1 - la columna de las unidades, y el INTERCAMBIO si no llega
    r["hay_intercambio"] = r["uni_a"] < r["uni_b"]
    if r["hay_intercambio"]:
        # EL INTERCAMBIO, mecanico: la decena de arriba baja una (la palabra ANTERIOR) y las
        # unidades pasan a ser "diez y lo que habia" (contar desde diez)
        r["dec_a_despues"] = leer(anterior(decir(r["dec_a"], saber), saber), saber)
        r["uni_a_despues"] = leer(contar_adelante("diez", decir(r["uni_a"], saber), saber)["resultado"], saber)
        unidad = _resta_con_metodo(r["uni_a_despues"], r["uni_b"], saber)
        decena = _resta_con_metodo(r["dec_a_despues"], r["dec_b"], saber)
    else:
        r["dec_a_despues"] = r["dec_a"]
        r["uni_a_despues"] = r["uni_a"]
        unidad = _resta_con_metodo(r["uni_a"], r["uni_b"], saber)
        decena = _resta_con_metodo(r["dec_a"], r["dec_b"], saber)
    r["unidad"], r["decena"] = unidad, decena
    r["resta_unidades"] = unidad["cuenta"]
    r["resta_decenas"] = decena["cuenta"]
    # Y LA COMPROBACION DEL INTERCAMBIO: sigue valiendo lo mismo
    # (y se comprueba JUNTANDO otra vez, con la 6.5, que no con una multiplicacion)
    r["intercambio_vale_igual"] = decidir_6_5_juntar_decenas(
        str(r["dec_a_despues"]), str(r["uni_a_despues"]), saber).get("total") == va
    r["resta"] = escribir_cifras([unidad["queda"]] + cifras_de(decena["queda"]))
    r["resultado"] = _palabra_de(r["resta"], secuencia) if r["resta"] else "cero"
    r["expresion"] = "%s - %s = %s" % (pa, pb, r["resultado"])
    tabla = _tabla(saber)
    r["cifra_a"], r["cifra_b"] = tabla.get(pa, str(va)), tabla.get(pb, str(vb))
    r["cifra_resultado"] = tabla.get(r["resultado"], str(r["resta"]))
    r["expresion_cifras"] = "%s - %s = %s" % (r["cifra_a"], r["cifra_b"], r["cifra_resultado"])
    # LA VUELTA: la suma deshace la resta (con las columnas de la 7.3)
    vuelta = decidir_7_3_columnas(str(r["resta"]), str(vb), saber, verificar=False)
    r["vuelta"] = vuelta
    r["verificacion"] = (vuelta["conclusion"] == "se_puede" and vuelta["total_valor"] == va)
    r["verificacion_texto"] = "sumando sale otra vez el de arriba"
    return r


def explicar_7_5_columnas(texto_a, texto_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    if _va_a_la_7_6("-", texto_a, texto_b, saber):
        return explicar_7_6_columnas(texto_a, "-", texto_b, saber)
    r = decidir_7_5_columnas(texto_a, texto_b, saber)
    lineas = ["PREGUNTA (7.5): restar estos DOS NUMEROS por COLUMNAS  (y el intercambio de una"
              " decena)"]
    lineas.append("NUMEROS:  %s  y  %s" % (texto_a, texto_b))
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  Alguno de los dos no es un numero que conozca.")
        return "\n".join(lineas)
    if r["conclusion"] == "no_hay_bastantes":
        lineas.append("RESULTADO: no_hay_bastantes")
        lineas.append("  Al de abajo (%s) no se le puede quitar al de arriba (%s): seria una resta"
                      " NEGATIVA." % (r["palabra_b"], r["palabra_a"]))
        lineas.append("  Y aqui no existe (unidad 5.4).  Se dice, no se inventa.")
        return "\n".join(lineas)
    if r["conclusion"] == "no_alcanza":
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  Alguno pasa de cien, y la resta por columnas no llega tan alto todavia.")
        return "\n".join(lineas)
    lineas.append("")
    lineas.append("  SE PONE UNO DEBAJO DEL OTRO y se restan las COLUMNAS (se empieza por la"
                  " derecha):")
    lineas.append("")
    lineas.append("       %s" % r["cifra_a"])
    lineas.append("    -  %s" % r["cifra_b"])
    lineas.append("    ----")
    lineas.append("")
    lineas.append("  PASO 0 - SE PARTE CADA NUMERO EN DECENAS Y UNIDADES (unidad 6.5):")
    lineas.append("    %s = %d decenas y %d unidades   |   %s = %d decenas y %d unidades"
                  % (r["palabra_a"], r["dec_a"], r["uni_a"], r["palabra_b"], r["dec_b"], r["uni_b"]))
    lineas.append("")
    lineas.append("  PASO 1 - COLUMNA DE LAS UNIDADES (se empieza por la derecha):")
    if r["hay_intercambio"]:
        lineas.append("    %d - %d ... NO SE PUEDE.  Arriba hay %d y abajo %d: no llega."
                      % (r["uni_a"], r["uni_b"], r["uni_a"], r["uni_b"]))
        lineas.append("    Y OJO: ESO NO SE ARREGLA DANDO LA VUELTA A LA RESTA.  El de arriba es LO")
        lineas.append("    QUE HAY; si no llega, no se cambia el orden.  %d - %d seria FALSO."
                      % (r["uni_b"], r["uni_a"]))
        lineas.append("    -> SE CAMBIA una decena por diez unidades (y esto NO es un prestamo: no")
        lineas.append("       hay que devolver nada).  Se coge UNA de las %d decenas y se abre en"
                      % r["dec_a"])
        lineas.append("       diez unidades:")
        lineas.append("         %s = %d decenas y %d unidades  ->  %d decenas y %d unidades"
                      % (r["palabra_a"], r["dec_a"], r["uni_a"], r["dec_a_despues"],
                         r["uni_a_despues"]))
        lineas.append("       Y SIGUE SIENDO %s ... %s"
                      % (r["palabra_a"], "SI" if r["intercambio_vale_igual"] else "NO"))
        lineas.append("       (no se escribe '%d + %d = %d': son %d DECENAS y %d unidades, y el"
                      % (r["dec_a_despues"], r["uni_a_despues"], r["valor_a"],
                         r["dec_a_despues"], r["uni_a_despues"]))
        lineas.append("        sistema todavia no sabe multiplicar.  Se dice 'son %d decenas', que"
                      " es lo que si sabe: unidad 6.5.)" % r["dec_a_despues"])
        lineas.append("    -> AHORA SI:  %s" % r["resta_unidades"])
        lineas.append("       (el metodo: %s)" % r["unidad"]["como"])
        lineas.append("    -> Y AL CAMBIAR LA DECENA, LA COLUMNA DE LAS DECENAS PASA DE %d A %d."
                      % (r["dec_a"], r["dec_a_despues"]))
        lineas.append("       Si se olvidara, la respuesta saldria DIEZ DE MAS.")
    else:
        lineas.append("    %d - %d = %d  (SI llega: no hay que cambiar nada)"
                      % (r["uni_a"], r["uni_b"], r["unidad"]["queda"]))
        lineas.append("       (el metodo: %s)" % r["unidad"]["como"])
    lineas.append("")
    lineas.append("  PASO 2 - COLUMNA DE LAS DECENAS:")
    lineas.append("    %s" % r["resta_decenas"])
    lineas.append("       (el metodo: %s)" % r["decena"]["como"])
    lineas.append("")
    lineas.append("  LA CUENTA ENTERA:")
    lineas.append("    %s  ->  %s" % (_dec_u(r["decena"]["queda"], r["unidad"]["queda"]),
                                       r["resultado"]))
    lineas.append("")
    lineas.append("  COMPROBACIONES:")
    lineas.append("    - el cambio de la decena no cambia el numero: %d dec y %d u siguen siendo %d"
                  " ... %s" % (r["dec_a_despues"], r["uni_a_despues"], r["valor_a"],
                               "SI" if r["intercambio_vale_igual"] else "NO"))
    lineas.append("    - la vuelta (la suma deshace la resta, unidad 7.3): %s + %s = %s ... %s"
                  % (r["resultado"], r["palabra_b"], r["palabra_a"],
                     "SI" if r["verificacion"] else "NO"))
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["expresion"])
    lineas.append("")
    if r["hay_intercambio"]:
        lineas.append("  Y EL INTERCAMBIO NO ES UN TRUCO: es la MISMA MONEDA que el llevarse de la")
        lineas.append("  suma (unidad 7.3), cambiada al REVES.  Alli, diez unidades se juntaban en")
        lineas.append("  una decena que SUBIA; aqui, una decena se abre en diez unidades que BAJAN.")
        lineas.append("  Es cambiar una decena por diez unidades.  Ni se presta ni se devuelve.")
    else:
        lineas.append("  AQUI NO HA HECHO FALTA CAMBIAR NADA: las unidades de arriba llegaban.")
        lineas.append("  Y por eso se aprenden LAS DOS juntas: es lo mismo, con un paso de mas.")
    return "\n".join(lineas)


def _detalle_error(escena, r):
    """Dice, en palabras, QUE ha estado mal.  Sin usar cifras (unidad 3.1)."""
    palabras, secuencia = r["palabras"], r["secuencia"]
    c = r["conclusion"]
    if c == "faltan_objetos_sin_contar":
        sin = [o["id"] for o in r["entidades"][len(palabras):]]
        return "  -> quedaron objetos SIN contar: %s" % ", ".join(sin)
    if c == "palabras_de_mas":
        return "  -> hay mas palabras que objetos: sobra %s" % ", ".join(palabras[len(r["entidades"]):])
    if c == "palabra_repetida":
        vistas, repes = set(), []
        for p in palabras:
            if p in vistas and p not in repes:
                repes.append(p)
            vistas.add(p)
        return "  -> se uso la misma palabra mas de una vez: %s" % ", ".join(repes)
    if c == "palabra_desconocida":
        raras = [p for p in palabras if p not in secuencia]
        return "  -> no conozco estas palabras: %s" % ", ".join(raras)
    if c == "orden_saltado":
        esperadas = secuencia[:len(palabras)]
        faltan = [p for p in esperadas if p not in palabras]
        if faltan:
            return "  -> falta por decir: %s" % ", ".join(faltan)
        return "  -> las palabras no van en el orden de la secuencia"
    return None


# ------------------------------------------------- columnas con la centena (7.6)
#
# LA NOTA 7 DE CARLOS ENTERA: unidad con unidad, decena con decena, CENTENA CON CENTENA.
# No es un metodo nuevo: es el de la 7.3 y la 7.5 con las columnas que hagan falta (hasta mil).
# Cada columna se hace con SU MECANISMO (dedos 7.1 / 7.4): ninguna cuenta sale de "Python suma".

_NOMBRE_COLUMNA = ("unidades", "decenas", "centenas", "unidades de mil", "decenas de mil", "centenas de mil", "unidades de millon",
                   "decenas de millon")
_UNA_DE_LA_COLUMNA = ("unidad", "decena", "centena", "unidad de mil", "decena de mil", "centena de mil", "unidad de millon",
                      "decena de millon")


def _dos_valores(texto_a, texto_b, saber):
    pa, _ = nombre_de_numero(texto_a, saber)
    pb, _ = nombre_de_numero(texto_b, saber)
    return pa, pb, _valor_de_numero(pa, saber), _valor_de_numero(pb, saber)


def _va_a_la_7_6(op, texto_a, texto_b, saber):
    """Decide si una suma/resta por columnas pasa de la 7.3/7.5 (hasta cien) a la 7.6.
    Suma: si el TOTAL pasa de cien.  Resta: si el de ARRIBA pasa de cien.  (Asi todo lo que la
    7.3 y la 7.5 ya hacian sigue saliendo EXACTAMENTE igual.)"""
    _, _, va, vb = _dos_valores(texto_a, texto_b, saber)
    for t in (texto_a, texto_b):          # una cifra que no se sabe leer pero ES un numero
        t = (t or "").strip()
        if t.isdigit() and int(t) > 100 and (va is None or vb is None):
            return True
    if va is None or vb is None:
        return False
    cien = "cien"
    if op == "-":
        return viene_despues(decir(va, saber), cien, saber)
    if viene_despues(decir(va, saber), cien, saber) or viene_despues(decir(vb, saber), cien, saber):
        return True
    t = sumar_por_columnas(va, vb, saber)          # mecanico: el total pasa de cien?
    return t is None or viene_despues(decir(t, saber), cien, saber)


def decidir_7_6_columnas(texto_a, op, texto_b, saber=None, verificar=True):
    """
    Unidad 7.6: SUMAR (op '+') o RESTAR (op '-') POR COLUMNAS, con las que hagan falta.

      247 + 385:  7+5=12 (anoto 2, llevo 1) ; 4+8=12, +1=13 (anoto 3, llevo 1) ; 2+3=5, +1=6 -> 632
      500 - 247:  0 no llega, y las decenas son 0 -> cambio 1 centena por 10 decenas, y 1 decena
                  por 10 unidades -> 10-7=3 ; 9-4=5 ; 4-2=2 -> 253
    """
    if saber is None:
        saber = cargar_conocimiento()
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    pa, pb, va, vb = _dos_valores(texto_a, texto_b, saber)
    cuenta = {"valor_a": va, "valor_b": vb, "secuencia": secuencia,
              "texto_a": texto_a, "texto_b": texto_b, "_saber": saber}
    reglas = saber["reglas_7_6"]["reglas_suma" if op == "+" else "reglas_resta"]
    r = _aplicar_reglas(reglas, None, None, saber, cuenta=cuenta)
    r["unidad"] = "7.6"
    r["op"] = op
    r["texto_a"], r["texto_b"] = texto_a, texto_b
    r["palabra_a"], r["palabra_b"] = pa, pb
    r["valor_a"], r["valor_b"] = va, vb
    if r["conclusion"] != "se_puede":
        return r
    arriba = _partir_por_ordenes(va)          # 6.7: las cifras por sitio, de derecha a izquierda
    abajo = _partir_por_ordenes(vb)
    n = max(len(arriba), len(abajo))
    arriba = _rellenar(arriba, n)          # 47 debajo de 247 -> [7, 4, 0]
    abajo = _rellenar(abajo, n)
    r["arriba"], r["abajo"] = list(arriba), list(abajo)
    pasos = []
    if op == "+":
        lleva = 0
        anotadas = []
        for i in range(n):
            p1 = _suma_con_metodo(arriba[i], abajo[i], saber)
            p2 = _suma_con_metodo(p1["total"], lleva, saber) if lleva else None
            hecho = p2 if p2 else p1
            s = hecho["total"]
            # PASA DE NUEVE? (viene despues de 'nueve' en la lista).  Si pasa, se anota lo que hay
            # que contar desde 'diez' hasta la suma, y se lleva UNO.  Mecanico, sin dividir.
            if viene_despues(hecho["palabra_total"], "nueve", saber):
                anota = leer(contar_hasta("diez", hecho["palabra_total"], saber), saber)
                nueva = 1
            else:
                anota, nueva = s, 0
            pasos.append({"columna": _NOMBRE_COLUMNA[i], "a": arriba[i], "b": abajo[i],
                          "paso_1": p1, "paso_2": p2, "lleva_de_antes": lleva,
                          "suma": s, "anota": anota, "se_lleva": nueva})
            anotadas.append(anota)
            lleva = nueva
        if lleva:
            anotadas.append(lleva)
            pasos.append({"columna": _NOMBRE_COLUMNA[n], "solo_lo_que_se_lleva": lleva,
                          "anota": lleva})
        cifras_resultado = anotadas
    else:
        arr = list(arriba)
        cifras_resultado = []
        for i in range(n):
            cambios = []
            if arr[i] < abajo[i]:
                # EL INTERCAMBIO: se busca la PRIMERA columna de la izquierda que tenga algo
                j = i + 1
                while j < n and arr[j] == 0:
                    j += 1
                for k in range(j, i, -1):     # y se baja escalon a escalon (a traves de los ceros)
                    arr[k] = leer(anterior(decir(arr[k], saber), saber), saber)          # una menos
                    arr[k - 1] = leer(contar_adelante("diez", decir(arr[k - 1], saber),
                                                      saber)["resultado"], saber)   # diez mas
                    cambios.append({"de": _UNA_DE_LA_COLUMNA[k], "por": "diez %s" % _NOMBRE_COLUMNA[k - 1],
                                    "queda": list(arr),
                                    "sigue_valiendo": _deshacer_cambios(arr, saber) == list(arriba)})
            rr = _resta_con_metodo(arr[i], abajo[i], saber)
            pasos.append({"columna": _NOMBRE_COLUMNA[i], "a": arr[i], "b": abajo[i],
                          "cambios": cambios, "resta": rr, "queda": rr["queda"],
                          "a_traves_de_un_cero": len(cambios) > 1})
            cifras_resultado.append(rr["queda"])
        r["arriba_despues"] = arr
        # EL ERROR TIPICO nº1: dar la vuelta en cada columna (restar el pequeno del grande)
        r["si_diera_la_vuelta"] = escribir_cifras(
            [leer(contar_hasta(decir(min(a, b), saber), decir(max(a, b), saber), saber), saber)
             for a, b in zip(arriba, abajo)])
    r["pasos"] = pasos
    total = escribir_cifras(cifras_resultado)
    r["total_valor"] = total
    r["resta"] = total
    r["total"] = _nombre_o_cero(total, saber)
    r["resultado"] = r["total"]
    r["expresion"] = "%s %s %s = %s" % (pa, op, pb, r["total"])
    r["expresion_cifras"] = "%d %s %d = %d" % (va, op, vb, total)
    r["hay_que_llevarse"] = any(p.get("se_lleva") for p in pasos) if op == "+" else None
    r["hay_intercambio"] = any(p.get("cambios") for p in pasos) if op == "-" else None
    r["a_traves_de_un_cero"] = any(p.get("a_traves_de_un_cero") for p in pasos)
    r["metodos_usados"] = sorted({(p.get("paso_1") or p.get("resta") or {}).get("metodo") or "?"
                                  for p in pasos if "solo_lo_que_se_lleva" not in p})
    # LA VUELTA: la resta se comprueba sumando, y la suma restando (sin bucles: un solo nivel)
    if verificar:
        if op == "+":
            v = decidir_7_6_columnas(str(total), "-", str(vb), saber, verificar=False)
            r["verificacion"] = v["conclusion"] == "se_puede" and v["total_valor"] == va
            r["verificacion_texto"] = "%d - %d = %s" % (total, vb, v.get("total_valor"))
        else:
            v = decidir_7_6_columnas(str(total), "+", str(vb), saber, verificar=False)
            r["verificacion"] = v["conclusion"] == "se_puede" and v["total_valor"] == va
            r["verificacion_texto"] = "%d + %d = %s" % (total, vb, v.get("total_valor"))
    return r


def _deshacer_cambios(arr, saber):
    """Para COMPROBAR que un cambio no cambia el numero: se deshace (diez de una columna vuelven
    a ser UNA de la siguiente) y tienen que salir las cifras de antes.  Todo contando."""
    copia = list(arr)
    for i in range(len(copia)):
        if viene_despues(decir(copia[i], saber), "nueve", saber):
            copia[i] = leer(contar_hasta("diez", decir(copia[i], saber), saber), saber)
            if i + 1 < len(copia):
                copia[i + 1] = leer(siguiente(decir(copia[i + 1], saber), saber), saber)
    return copia


def _como_columna(p):
    m = (p.get("paso_1") or p.get("resta") or {})
    return "%s" % (m.get("metodo") or "sin metodo")


def explicar_7_6_columnas(texto_a, op, texto_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_7_6_columnas(texto_a, op, texto_b, saber)
    verbo = "sumar" if op == "+" else "restar"
    lineas = ["PREGUNTA (7.6): %s estos DOS NUMEROS por COLUMNAS  (unidad, decena y CENTENA)" % verbo]
    lineas.append("NUMEROS:  %s  y  %s" % (texto_a, texto_b))
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  Alguno no es un numero que sepa leer (los mios van del CERO al %s)." % techo(saber).upper())
        return "\n".join(lineas)
    if r["conclusion"] == "no_alcanza":
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  Se pasa de %s, y mi secuencia de contar llega ahi.  No me lo invento." % techo(saber).upper())
        return "\n".join(lineas)
    if r["conclusion"] == "no_hay_bastantes":
        lineas.append("RESULTADO: no_hay_bastantes")
        lineas.append("  Al de arriba (%s) no se le puede quitar el de abajo (%s): seria NEGATIVA."
                      % (r["valor_a"], r["valor_b"]))
        lineas.append("  CONDICION DE LA RESTA (5.4): no se puede quitar mas de lo que hay.")
        return "\n".join(lineas)
    va, vb = r["valor_a"], r["valor_b"]
    ancho = max(len(str(va)), len(str(vb))) + 2
    lineas.append("")
    lineas.append("  SE PONE UNO DEBAJO DEL OTRO, cada cifra en SU columna (6.7):")
    lineas.append("")
    lineas.append("     %s" % str(va).rjust(ancho))
    lineas.append("   %s %s" % (op, str(vb).rjust(ancho)))
    lineas.append("     " + "-" * ancho)
    lineas.append("")
    lineas.append("  SE EMPIEZA POR LA DERECHA (las unidades) y se va columna a columna:")
    for i, p in enumerate(r["pasos"]):
        lineas.append("")
        if "solo_lo_que_se_lleva" in p:
            lineas.append("  COLUMNA DE LAS %s: no hay cifras, pero baja la que me llevo: %d"
                          % (p["columna"].upper(), p["anota"]))
            continue
        lineas.append("  COLUMNA DE LAS %s:" % p["columna"].upper())
        if op == "+":
            p1 = p["paso_1"]
            lineas.append("    %d + %d = %d   (metodo: %s%s)"
                          % (p["a"], p["b"], p1["total"], p1.get("metodo") or "ninguno",
                             (": " + p1["como"]) if p1.get("como") else ""))
            if p["paso_2"]:
                p2 = p["paso_2"]
                lineas.append("    y le sumo la que me llevo, EN OTRO PASO: %d + %d = %d   (metodo: %s)"
                              % (p1["total"], p["lleva_de_antes"], p2["total"],
                                 p2.get("metodo") or "ninguno"))
            if p["se_lleva"]:
                lineas.append("    -> %d PASA DE NUEVE: son 1 %s y %d.  Anoto %d y ME LLEVO 1 a las %s."
                              % (p["suma"], _UNA_DE_LA_COLUMNA[i + 1], p["anota"], p["anota"],
                                 _NOMBRE_COLUMNA[i + 1]))
                lineas.append("       (diez %s hacen una %s: es RE-AGRUPAR, no un truco)"
                              % (p["columna"], _UNA_DE_LA_COLUMNA[i + 1]))
            else:
                lineas.append("    -> anoto %d" % p["anota"])
        else:
            for c in p["cambios"]:
                lineas.append("    no llega: CAMBIO 1 %s por %s   -> arriba queda %s ... sigue valiendo %d: %s"
                              % (c["de"], c["por"], _dibujar_ordenes(c["queda"]), va,
                                 "SI" if c["sigue_valiendo"] else "NO"))
            if p["a_traves_de_un_cero"]:
                lineas.append("    (A TRAVES DE UN CERO: la columna de al lado no tenia nada que cambiar, asi")
                lineas.append("     que se fue a la siguiente, y se bajo ESCALON A ESCALON.  Por eso el cero")
                lineas.append("     se queda en 9, no en 10: uno de esos diez bajo a la columna de la derecha.)")
            rr = p["resta"]
            lineas.append("    %d - %d = %d   (metodo: %s%s)"
                          % (p["a"], p["b"], rr["queda"], rr.get("metodo") or "ninguno",
                             (": " + rr["como"]) if rr.get("como") else ""))
    lineas.append("")
    lineas.append("  LA CUENTA ENTERA:  %s   ('%s')" % (r["expresion_cifras"], r["total"]))
    lineas.append("")
    lineas.append("  COMPROBACIONES:")
    lineas.append("    - cada columna salio de un METODO (%s), no de memoria ... %s"
                  % (", ".join(r["metodos_usados"]),
                     "SI" if "?" not in r["metodos_usados"] else "NO"))
    lineas.append("    - la vuelta (%s): %s sale otra vez el de arriba ... %s"
                  % ("la suma deshace la resta" if op == "-" else "la resta deshace la suma",
                     r.get("verificacion_texto"), "SI" if r.get("verificacion") else "NO"))
    if op == "-" and r["si_diera_la_vuelta"] != r["total_valor"]:
        lineas.append("")
        lineas.append("  OJO CON EL ERROR TIPICO: dar la vuelta en las columnas (restar el pequeno del")
        lineas.append("  grande) daria %d, y seria FALSO." % r["si_diera_la_vuelta"])
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["expresion"])
    lineas.append("  (en cifras: %s)" % r["expresion_cifras"])
    lineas.append("")
    lineas.append("  ES LA NOTA 7 ENTERA: unidad con unidad, decena con decena y CENTENA CON CENTENA.")
    return "\n".join(lineas)


def _dibujar_ordenes(cifras):
    partes = []
    for i in range(len(cifras) - 1, -1, -1):
        partes.append("%d %s" % (cifras[i], {0: "u", 1: "d", 2: "c", 3: "um"}[i]))
    return ", ".join(partes)
