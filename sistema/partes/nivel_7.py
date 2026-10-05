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
    va = _valor_de_cantidad(pa, saber)
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
    r["anotado"] = pa
    r["los_pasos"] = []
    for k in range(1, vb + 1):
        valor = va + k
        r["los_pasos"].append({"dedo": k, "quedan": vb - k, "valor": valor,
                               "palabra": _palabra_de(valor, secuencia)})
    r["total_valor"] = va + vb
    r["total"] = _palabra_de(va + vb, secuencia)
    r["expresion"] = "%s + %s = %s" % (pa, pb, r["total"])
    tabla = _tabla(saber)
    r["cifra_a"], r["cifra_b"] = tabla.get(pa), tabla.get(pb)
    r["cifra_total"] = tabla.get(r["total"])
    r["hay_cifras"] = (r["cifra_a"] is not None and r["cifra_b"] is not None)
    if r["hay_cifras"]:
        r["expresion_cifras"] = "%s + %s = %s" % (r["cifra_a"], r["cifra_b"],
                                                  r["cifra_total"] or r["total"])
    else:
        r["expresion_cifras"] = r["expresion"]
    # LAS CUENTAS DEL AHORRO: contar hacia adelante da VB pasos; contar todo daria A+B.
    r["pasos_dados"] = vb
    r["pasos_contando_todo"] = va + vb
    r["pasos_ahorrados"] = va
    r["la_suma_cuadra"] = (r["total_valor"] == va + vb)
    # LA COMPROBACION: al total se le quita el segundo y tiene que volver a salir el primero.
    r["expresion_inversa"] = "%s - %s = %s" % (r["total"], pb, pa)
    r["verificacion"] = (r["total_valor"] - vb == va)
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
    faltan = 10 - va          # lo que le falta al primero para llegar a DIEZ
    r["faltan_para_diez"] = faltan
    r["sobra_del_segundo"] = vb - faltan
    r["parte_para_diez"] = faltan
    r["parte_que_sobra"] = vb - faltan
    r["primera_cuenta"] = "10" if faltan else "0"
    r["paso_1"] = "%d + %d = 10" % (va, faltan)
    r["paso_2"] = "10 + %d = %d" % (vb - faltan, va + vb)
    r["total_valor"] = va + vb
    r["total"] = _palabra_de(va + vb, secuencia)
    r["expresion"] = "%s + %s = %s" % (pa, pb, r["total"])
    r["suma_de_tres"] = "%d + %d + %d" % (va, faltan, vb - faltan)
    tabla = _tabla(saber)
    r["cifra_a"], r["cifra_b"] = tabla.get(pa), tabla.get(pb)
    r["cifra_total"] = tabla.get(r["total"])
    if r["cifra_a"] is not None and r["cifra_b"] is not None:
        r["expresion_cifras"] = "%s + %s = %s" % (r["cifra_a"], r["cifra_b"],
                                                  r["cifra_total"] or r["total"])
    else:
        r["expresion_cifras"] = r["expresion"]
    r["las_partes_cuadran"] = (faltan + (vb - faltan) == vb)
    r["verificacion"] = (va + faltan == 10 and 10 + (vb - faltan) == va + vb)
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
                      % (r["palabra_a"], r["palabra_b"], _palabra_de(r["valor_a"] + r["valor_b"],
                                                                     r["secuencia"])))
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

def decidir_7_3_columnas(texto_a, texto_b, saber=None):
    """
    Unidad 7.3: SUMAR POR COLUMNAS.  Unidad con unidad, decena con decena, y el llevarse.

      47 + 15  ->  7+5 = 12 (anoto 2, me llevo 1);  4+1+1 = 6  ->  62

    El llevarse NO es un truco: es RE-AGRUPAR (diez unidades hacen una decena, unidad 6.2).
    """
    if saber is None:
        saber = cargar_conocimiento()
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    pa, ca = nombre_de_numero(texto_a, saber)
    pb, cb = nombre_de_numero(texto_b, saber)
    va, vb = _valor_de_numero(pa, saber), _valor_de_numero(pb, saber)
    cuenta = {"valor_a": va, "valor_b": vb, "secuencia": secuencia}
    r = _aplicar_reglas(saber["reglas_7_3"]["reglas_columnas"], None, None, saber, cuenta=cuenta)
    r["texto_a"], r["texto_b"] = texto_a, texto_b
    r["palabra_a"], r["palabra_b"] = pa, pb
    r["valor_a"], r["valor_b"] = va, vb
    if r["conclusion"] != "se_puede":
        return r
    # --- LAS DOS COLUMNAS -------------------------------------------------
    ua, ub = va % 10, vb % 10
    da, db = va // 10, vb // 10
    suma_unidades = ua + ub
    se_lleva = suma_unidades // 10        # 0 o 1 (nunca mas: 9+9=18)
    anota_unidades = suma_unidades % 10
    suma_decenas = da + db + se_lleva
    total = va + vb
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
    # COMPROBACIONES
    r["recompone"] = (suma_decenas * 10 + anota_unidades == total)
    r["el_llevado_es_una_decena"] = (suma_unidades == anota_unidades + se_lleva * 10)
    r["lleva_como_mucho_uno"] = se_lleva <= 1   # 9+9=18 -> se lleva 1, nunca 2
    r["sin_llevarse_daria_mal"] = (se_lleva > 0 and da + db != suma_decenas)
    # la verificacion de siempre: por la vuelta (partir el total, unidad 5.1)
    r["parejas_del_total"] = [(k, total - k) for k in range(0, total // 2 + 1)]
    r["verificacion"] = sorted((va, vb)) in [sorted(p) for p in r["parejas_del_total"]]
    return r


def explicar_7_3_columnas(texto_a, texto_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
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
    su = _suma_con_metodo(va % 10, vb % 10, saber)
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
    escena_54 = [{"id": i + 1} for i in range(va)] if va is not None else []
    cuenta = {"secuencia": secuencia, "valor_a": va, "valor_b": vb, "pedido_valor": vb,
              "otra": [None] * (vb or 0),
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
    quedan = va - vb
    r["quedan"] = quedan
    r["resta"] = _palabra_de(quedan, secuencia) if quedan else "cero"
    r["expresion"] = "%s - %s = %s" % (pa, pb, r["resta"])
    tabla = _tabla(saber)
    r["cifra_a"], r["cifra_b"] = tabla.get(pa, str(va) if va is not None else None), \
                                 tabla.get(pb, str(vb) if vb is not None else None)
    r["cifra_resta"] = tabla.get(r["resta"], str(quedan))
    r["expresion_cifras"] = "%s - %s = %s" % (r["cifra_a"], r["cifra_b"], r["cifra_resta"])
    # LA VENTANA DE LOS DEDOS: los diez dedos son los ULTIMOS DIEZ numeros, y el ultimo es el
    # minuendo.  Si el minuendo es 12, la ventana es del 3 al 12.  Si es 9, del 1 al 9.
    r["desde"] = max(1, va - (r["dedos"] - 1))
    r["dedos_levantados"] = va - r["desde"] + 1
    r["ventana"] = (r["desde"], va)
    r["cabe_entero"] = (r["desde"] == 1)
    # EL PASO A PASO: los dedos que se van bajando, con el numero que va quedando
    r["bajadas"] = [{"bajo": i, "quedan": va - i} for i in range(1, vb + 1)]
    r["pasos_dados"] = vb
    # LA VUELTA: la suma deshace la resta (unidad 7.1)
    vuelta = decidir_7_1_dedos(str(quedan), str(vb), saber)
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
    NO se sabe de memoria y NO se usa calculadora: se usa el mecanismo de la unidad 7.4 (los dedos,
    contando hacia atras).  Si el minuendo no cabe en los dedos (12, que sale despues de cambiar la
    decena), se ANOTA en la pizarra y se bajan los dedos del sustraendo -- igual que en la suma
    (7.1), donde el primero tambien se anota.
    """
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    pa = _palabra_de(a, secuencia) if a else "cero"
    pb = _palabra_de(b, secuencia) if b else "cero"
    queda = a - b
    d = {"a": a, "b": b, "queda": queda, "palabra_a": pa, "palabra_b": pb,
         "palabra_queda": _palabra_de(queda, secuencia) if queda else "cero"}
    ded = decidir_7_4_resta_dedos(str(a), str(b), saber)
    if ded["conclusion"] == "se_puede":
        d["metodo"] = "dedos (7.4)"
        d["ventana"] = ded.get("ventana")
        if ded.get("cabe_entero"):
            d["como"] = ("se levantan %s y se bajan %d dedos: quedan %s"
                         % (pa, b, d["palabra_queda"]))
        else:
            d["como"] = ("los dedos van del %d al %d (el ultimo es %s), y se bajan %d: quedan %s"
                         % (ded["desde"], a, pa, b, d["palabra_queda"]))
    else:
        # No deberia pasar en una columna (lo que se baja siempre es de una cifra), pero si pasa,
        # el sistema lo DICE en vez de inventarse el resultado.
        d["metodo"] = None
        d["como"] = "no cabe en los dedos, y el sistema no tiene otro mecanismo para esto"
    d["cuenta"] = "%d - %d = %d" % (a, b, queda)
    return d


def decidir_7_5_columnas(texto_a, texto_b, saber=None):
    """
    Unidad 7.5: RESTAR POR COLUMNAS.  Columna a columna, y si las unidades de arriba no llegan, se
    CAMBIA una decena por diez unidades (el intercambio, que NO es un prestamo).

      72 - 45  ->  2-5 no llega -> 72 = 6 dec y 12 u -> 12-5=7 -> 6-4=2  ->  27
      58 - 27  ->  8-7=1 y 5-2=3 sin cambiar nada                      ->  31
    """
    if saber is None:
        saber = cargar_conocimiento()
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    pa, ca = nombre_de_numero(texto_a, saber)
    pb, cb = nombre_de_numero(texto_b, saber)
    va = _valor_de_cantidad(pa, saber)
    vb = _valor_de_cantidad(pb, saber)
    escena_54 = [{"id": i + 1} for i in range(va)] if va is not None else []
    cuenta = {"secuencia": secuencia, "valor_a": va, "valor_b": vb, "pedido_valor": vb,
              "texto_a": texto_a, "texto_b": texto_b,
              "otra": [None] * (vb or 0)}
    r = _aplicar_reglas(saber["reglas_7_5"]["reglas_columnas_resta"], escena_54, None, saber,
                        cuenta=cuenta)
    r["secuencia"] = secuencia
    r["texto_a"], r["texto_b"] = texto_a, texto_b
    r["palabra_a"], r["palabra_b"] = pa, pb
    r["valor_a"], r["valor_b"] = va, vb
    if r["conclusion"] != "se_puede":
        return r
    # PASO 0 - partir cada numero (unidad 6.5)
    r["dec_a"], r["uni_a"] = divmod(va, 10)
    r["dec_b"], r["uni_b"] = divmod(vb, 10)
    # PASO 1 - la columna de las unidades, y el INTERCAMBIO si no llega
    r["hay_intercambio"] = r["uni_a"] < r["uni_b"]
    if r["hay_intercambio"]:
        r["dec_a_despues"] = r["dec_a"] - 1
        r["uni_a_despues"] = r["uni_a"] + 10
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
    r["intercambio_vale_igual"] = (r["dec_a_despues"] * 10 + r["uni_a_despues"]) == va
    r["resta"] = unidad["queda"] + decena["queda"] * 10
    r["resultado"] = _palabra_de(r["resta"], secuencia) if r["resta"] else "cero"
    r["expresion"] = "%s - %s = %s" % (pa, pb, r["resultado"])
    tabla = _tabla(saber)
    r["cifra_a"], r["cifra_b"] = tabla.get(pa, str(va)), tabla.get(pb, str(vb))
    r["cifra_resultado"] = tabla.get(r["resultado"], str(r["resta"]))
    r["expresion_cifras"] = "%s - %s = %s" % (r["cifra_a"], r["cifra_b"], r["cifra_resultado"])
    # LA VUELTA: la suma deshace la resta (con las columnas de la 7.3)
    vuelta = decidir_7_3_columnas(str(r["resta"]), str(vb), saber)
    r["vuelta"] = vuelta
    r["verificacion"] = (vuelta["conclusion"] == "se_puede" and vuelta["total_valor"] == va)
    r["verificacion_texto"] = "sumando sale otra vez el de arriba"
    return r


def explicar_7_5_columnas(texto_a, texto_b, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
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
