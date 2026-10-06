# -*- coding: utf-8 -*-
"""
Euclides - Nivel 6 - valor posicional (6.1, 6.2, 6.3, 6.5, 6.7).

Este archivo es UNA PARTE del motor.  No se importa suelto: lo carga sistema/motor.py,
que junta todas las partes en un solo espacio de nombres (por eso aqui se usan funciones
definidas en otras partes sin importarlas).  Ver sistema/partes/__init__.py.
"""

import os  # noqa: F401
import sys  # noqa: F401

# ------------------------------------------------- la secuencia hasta 100 (6.1)

def _tabla_nombres(saber):
    """
    La tabla de la unidad 6.1, ya NORMALIZADA: los numeros como enteros, no como texto.
    El .kn es texto; convertirlo aqui, en un solo sitio, evita repetir la conversion por todas
    partes (y evita el error de comparar un texto con un numero).
    """
    d = saber.get("secuencia_hasta_cien") or {}

    def a_entero(x):
        try:
            return int(x)
        except (TypeError, ValueError):
            return None

    memorizadas, decenas, formaciones = {}, {}, []
    for k, v in (d.get("memorizadas") or {}).items():
        n = a_entero(k)
        if n is not None:
            memorizadas[n] = v
    for k, v in (d.get("decenas") or {}).items():
        n = a_entero(k)
        if n is not None:
            decenas[n] = v
    for f in (d.get("formaciones") or []):
        desde, hasta = a_entero(f.get("desde")), a_entero(f.get("hasta"))
        if desde is not None and hasta is not None:
            formaciones.append({"nombre": f.get("nombre"), "desde": desde, "hasta": hasta,
                                "prefijo": f.get("prefijo"), "junta": f.get("junta")})
    return {"memorizadas": memorizadas, "decenas": decenas, "formaciones": formaciones}


def construir_nombre_hasta_cien(n, saber):
    """
    Unidad 6.1: el nombre de un numero del 1 al 100, CONSTRUIDO con la regla.

    No esta memorizado: se construye.  Se sabe de memoria solo lo que la regla no puede dar
    (1-10, 11-15, 20, 100 y las decenas); lo demas sale de las tres formaciones.
    Devuelve None si esta fuera del 1..100 (o si falta un dato).
    """
    tabla = _tabla_nombres(saber)
    if n in tabla["memorizadas"]:
        return tabla["memorizadas"][n]
    if n in tabla["decenas"]:
        return tabla["decenas"][n]
    for f in tabla["formaciones"]:
        if f["desde"] <= n <= f["hasta"]:
            unidad = tabla["memorizadas"].get(cifras_de(n)[0])      # la ultima cifra
            if not unidad:
                return None
            if f.get("junta") == "pegado":
                return "%s%s" % (f["prefijo"], unidad)
            if f.get("junta") == "con_y":
                decena = tabla["decenas"].get(escribir_cifras([0] + cifras_de(n)[1:]))  # 47 -> 40
                if not decena:
                    return None
                return "%s y %s" % (decena, unidad)
    return None


def construir_nombre_hasta_mil(n, saber):
    """
    Unidad 6.7: el nombre de un numero del 1 al 1000, CONSTRUIDO con la regla.

    Por debajo de 100 delega en la 6.1 (misma verdad, no una copia).  De 100 a 999 compone con la
    palabra del CIENTO (que se sabe de memoria: son nueve) mas el nombre del resto.
    Y 1000 es "mil".

    OJO con las dos irregularidades:
      - 100 solo es "cien"; de 101 a 199 es "ciento ..."; y de 200 en adelante ya es la palabra del
        cientos a secas (200 -> "doscientos").
      - quinientos, setecientos y novecientos NO se construyen pegando "-cientos".
    Devuelve None si esta fuera del 1..1000.
    """
    if n is None or n < 1 or n > 1000:
        return None
    if n <= 100:
        return construir_nombre_hasta_cien(n, saber)
    if n == 1000:
        return _centenas(saber).get("mil") or "mil"
    cent, resto = escribir_cifras(cifras_de(n)[2:]), escribir_cifras(cifras_de(n)[:2])  # 247 -> 2 y 47
    cientos = _centenas(saber)
    if resto == 0:
        return cientos["cientos_solos"].get(cent)
    palabra_cientos = cientos["cientos"].get(cent)
    if not palabra_cientos:
        return None
    nombre_resto = construir_nombre_hasta_cien(resto, saber)
    if not nombre_resto:
        return None
    return "%s %s" % (palabra_cientos, nombre_resto)


def _centenas(saber):
    """
    Los datos de los cientos, tal como estan escritos en la_centena.kn.
    OJO: el lector de .kn devuelve las claves como TEXTO ('2'), asi que aqui se pasan a numero.
    Si no, buscar el 5 daria None y "quinientos" no saldria nunca.
    """
    d = saber.get("la_centena") or {}
    if not d:
        return d
    out = dict(d)
    for clave in ("cientos", "cientos_solos"):
        t_ = d.get(clave)
        if isinstance(t_, dict):
            out[clave] = {}
            for k, v in t_.items():
                try:
                    out[clave][int(k)] = v
                except (TypeError, ValueError):
                    out[clave][k] = v
    return out


def _secuencia_hasta_mil(saber):
    """Los 1000 nombres, en orden, construidos con la regla (unidad 6.7, que sube el techo)."""
    return [construir_nombre_hasta_mil(n, saber) for n in range(1, 1001)]


def _secuencia_hasta_cien(saber):
    """Los 100 nombres, en orden, construidos con la regla de la unidad 6.1."""
    return [construir_nombre_hasta_cien(n, saber) for n in range(1, 101)]


def de_donde_sale_el_nombre(n, saber):
    """Como se construyo ese nombre: que formacion, y con que piezas.  Para poder EXPLICARLO."""
    tabla = _tabla_nombres(saber)
    if n in tabla["memorizadas"]:
        return {"tipo": "memorizada", "palabra": tabla["memorizadas"][n]}
    if n in tabla["decenas"]:
        return {"tipo": "decena", "palabra": tabla["decenas"][n]}
    for f in tabla["formaciones"]:
        if f["desde"] <= n <= f["hasta"]:
            unidad_valor = cifras_de(n)[0]
            piezas = {"unidad": tabla["memorizadas"].get(unidad_valor), "unidad_valor": unidad_valor}
            if f.get("junta") == "pegado":
                piezas["prefijo"] = f["prefijo"]
            elif f.get("junta") == "con_y":
                dec_ = escribir_cifras([0] + cifras_de(n)[1:])
                piezas["decena"] = tabla["decenas"].get(dec_)
                piezas["decena_valor"] = dec_
            return {"tipo": f["nombre"], "junta": f.get("junta"), "piezas": piezas,
                    "desde": f["desde"], "hasta": f["hasta"]}
    return None


def _la_decena_que_le_toca(n):
    """La decena a la que pertenece un numero (para hablar del error de decena)."""
    return escribir_cifras([0] + cifras_de(n)[1:])


def explicar_6_1_nombre(texto, saber=None):
    """'nombre: 47' -> la palabra, y ENSEÑA COMO SE CONSTRUYO (que es lo de esta unidad)."""
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (6.1): como se LLAMA este numero?"]
    t = texto.strip()
    d = decidir_6_1_nombre(t, saber)
    if d["conclusion"] in ("no_lo_se", "no_entendido"):
        lineas.append("RESULTADO: no_lo_se")
        lineas.append("  '%s' no es un numero del 1 al %d escrito con cifras."
                      % (t, len(saber["secuencia_de_conteo"]["palabras"])))
        return "\n".join(lineas)
    n = d["valor"]
    lineas.append("NUMERO: %d" % n)
    if d["conclusion"] == "fuera_de_mi_secuencia":
        lineas.append("RESULTADO: fuera_de_mi_secuencia")
        lineas.append("  Mi secuencia de contar llega del UNO al %s.  Mas alla no me invento" % techo(saber).upper())
        lineas.append("  nombres, porque no los tengo escritos en ningun sitio.")
        return "\n".join(lineas)
    palabra = d["palabra"]
    if n > 1000:
        # PASO N.3 (4.o): el MILLAR se dice delante ('dos mil') y el resto se construye como antes.
        mil, resto = escribir_cifras(cifras_de(n)[3:]), escribir_cifras(cifras_de(n)[:3])
        lineas.append("")
        if n == 10000:
            lineas.append("  DIEZ MILLARES son UNA DECENA DE MIL, y se llama '%s' (el techo de 4.o)." % palabra)
        elif resto == 0:
            lineas.append("  ES UN MILLAR EXACTO: %d millares se dicen '%s' (la cifra + 'mil'; y 1000 es 'mil'"
                          % (mil, palabra))
            lineas.append("  a secas, nunca 'un mil').")
        else:
            nombre_mil = construir_nombre_hasta_diez_mil(escribir_cifras([0, 0, 0] + cifras_de(n)[3:]), saber)
            lineas.append("  SE CONSTRUYE con DOS piezas (paso N.3):")
            lineas.append("     el millar '%s' (de %d millares) + el resto, %d, que es '%s' (6.7)"
                          % (nombre_mil, mil, resto, construir_nombre_hasta_mil(resto, saber)))
            lineas.append("     ->  %s" % palabra)
            if escribir_cifras(cifras_de(n)[:3]) and cifras_de(n)[2] == 0:
                lineas.append("  OJO: no hay centenas sueltas: se escribe con un CERO en su sitio (%d), y al leer"
                              " no se dice nada de ellas." % n)
        lineas.append("")
        lineas.append("RESULTADO: %s" % palabra)
        return "\n".join(lineas)
    if n > 100:
        # UNIDAD 6.7: el CIENTO se sabe de memoria (son nueve) y el resto se construye como antes.
        cent, resto = escribir_cifras(cifras_de(n)[2:]), escribir_cifras(cifras_de(n)[:2])
        cientos = _centenas(saber)
        lineas.append("")
        if n == 1000:
            lineas.append("  DIEZ CENTENAS son UNA UNIDAD DE MIL, y se llama '%s' (hay que saberselo)."
                          % palabra)
        elif resto == 0:
            lineas.append("  ES UNA CENTENA EXACTA: %d centenas se dicen '%s' (de memoria: los cientos"
                          % (cent, palabra))
            lineas.append("  son nueve palabras, y quinientos, setecientos y novecientos son irregulares).")
        else:
            lineas.append("  SE CONSTRUYE con DOS piezas (unidad 6.7):")
            lineas.append("     el ciento '%s' (de %d centenas, de memoria) + el resto, %d, que es '%s' (6.1)"
                          % (cientos["cientos"].get(cent), cent, resto,
                             construir_nombre_hasta_cien(resto, saber)))
            lineas.append("     ->  %s" % palabra)
            if cent == 1:
                lineas.append("  OJO: 100 solo es 'cien', pero delante de algo es 'ciento' (no 'cien %s')."
                              % construir_nombre_hasta_cien(resto, saber))
        lineas.append("")
        lineas.append("RESULTADO: %s" % palabra)
        return "\n".join(lineas)
    info = de_donde_sale_el_nombre(n, saber) or {}
    lineas.append("")
    if info.get("tipo") == "memorizada":
        lineas.append("  ESTE NOMBRE HAY QUE SABERSE DE MEMORIA.  Aqui la regla no llega:")
        lineas.append("  del 1 al 10 y del 11 al 15 son irregulares (once, doce, trece... no salen de")
        lineas.append("  ninguna regla), y el 20 tampoco (no es 'veinti-diez').")
    elif info.get("tipo") == "decena":
        lineas.append("  ESTE NOMBRE HAY QUE SABERSE DE MEMORIA: es una DECENA, y es justo el punto")
        lineas.append("  donde la regla se ROMPE.  Por eso 'veintinueve' no sigue con 'veintidiez':")
        lineas.append("  sigue con 'treinta'.  Las decenas hay que saberselas.")
    elif info.get("junta") == "pegado":
        p = info["piezas"]
        lineas.append("  SE CONSTRUYE con la formacion '%s' (del %d al %d), TODO PEGADO:"
                      % (info["tipo"], info["desde"], info["hasta"]))
        lineas.append("     prefijo '%s' + la unidad '%s'  ->  %s" % (p["prefijo"], p["unidad"], palabra))
        lineas.append("  (La unidad que se pega es la PALABRA del 1 al 9, nunca una cifra.)")
    elif info.get("junta") == "con_y":
        p = info["piezas"]
        lineas.append("  SE CONSTRUYE con la formacion '%s' (del %d al %d), y va SEPARADO:"
                      % (info["tipo"], info["desde"], info["hasta"]))
        lineas.append("     la decena '%s' + ' y ' + la unidad '%s'  ->  %s"
                      % (p["decena"], p["unidad"], palabra))
    lineas.append("")
    lineas.append("  OJO: ese es el numero %d, y su nombre es '%s'.  El nombre NO dice las cifras" % (n, palabra))
    lineas.append("  (eso sera la unidad 6.2); dice como se lee.")
    lineas.append("")
    lineas.append("RESULTADO: %s" % palabra)
    return "\n".join(lineas)


def explicar_6_1_numero(texto, saber=None):
    """'numero: cuarenta y siete' -> el numero.  La vuelta: de la PALABRA al numero."""
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (6.1): que numero es este nombre?  (la vuelta)"]
    t = texto.strip().lower()
    lineas.append("PALABRA: %s" % t)
    d = decidir_6_1_numero(t, saber)
    if d["conclusion"] == "numero" and d["valor"] > 100:
        lineas.append("")
        lineas.append("  Lo busco en mi secuencia de nombres hasta %s (los construyo con la regla, 6.7 y N.3):" % techo(saber).upper())
        lineas.append("  es el que esta en el sitio %d." % d["valor"])
        lineas.append("")
        lineas.append("RESULTADO: %d" % d["valor"])
        return "\n".join(lineas)
    for n in range(1, 101):
        if construir_nombre_hasta_cien(n, saber) == t:
            lineas.append("")
            lineas.append("  Lo construyo hasta encontrar el que coincide:")
            info = de_donde_sale_el_nombre(n, saber) or {}
            if info.get("tipo") in ("memorizada", "decena"):
                lineas.append("  y es de las que hay que SABERSE (no sale de ninguna regla).")
            elif info.get("junta") == "pegado":
                lineas.append("  formacion '%s': '%s' es el prefijo y '%s' es la unidad."
                              % (info["tipo"], info["piezas"]["prefijo"], info["piezas"]["unidad"]))
            elif info.get("junta") == "con_y":
                lineas.append("  formacion '%s': '%s' es la decena y '%s' la unidad."
                              % (info["tipo"], info["piezas"]["decena"], info["piezas"]["unidad"]))
            lineas.append("")
            lineas.append("RESULTADO: %d" % n)
            return "\n".join(lineas)
    lineas.append("RESULTADO: no_lo_se")
    lineas.append("  '%s' no es un nombre de mi secuencia.  No me lo invento." % t)
    lineas.append("  (Mi secuencia son los 1000 nombres; los construyo con la regla y los recorro.)")
    return "\n".join(lineas)


def explicar_6_1_decenas(saber=None):
    """Las decenas: los nombres donde la regla se ROMPE.  Por eso hay que saberselas."""
    if saber is None:
        saber = cargar_conocimiento()
    tabla = _tabla_nombres(saber)
    lineas = ["LAS DECENAS (unidad 6.1): los nombres donde la REGLA SE ROMPE"]
    lineas.append("  Del 31 al 99 los nombres se construyen: la decena + ' y ' + la unidad.")
    lineas.append("  Pero cada DECENA hay que sabersela, porque no sale de ninguna regla:")
    lineas.append("")
    for n in sorted(tabla["decenas"]):
        lineas.append("    %d   %s" % (n, tabla["decenas"][n]))
    lineas.append("")
    lineas.append("  Y el 20 tambien es irregular: veinte (no 'veinti-diez').  Y el 100: cien.")
    lineas.append("")
    lineas.append("  LO IMPORTANTE, EL ERROR DE DECENA:")
    lineas.append("    veintiocho, veintinueve, ... ¿y ahora?")
    lineas.append("    Si siguiera la regla saldria 'veintidiez', que NO EXISTE.")
    lineas.append("    El nombre CAMBIA: treinta.")
    lineas.append("    Ese error lo hace quien ha entendido la regla DEMASIADO BIEN.  No es no saber:")
    lineas.append("    es aplicar una regla buena donde ya no vale.")
    lineas.append("")
    lineas.append("  Y CONTAR DE DIEZ EN DIEZ (esto prepara la unidad 6.2):")
    lineas.append("    %s" % ", ".join(tabla["decenas"][n] for n in sorted(tabla["decenas"])))
    lineas.append("    (cada uno es UN GRUPO DE DIEZ; contar asi es contar dieces)")
    return "\n".join(lineas)



# ------------------------------------------------- agrupar de diez en diez (6.2)

def decidir_6_2_agrupar(escena, saber=None):
    """
    Unidad 6.2: AGRUPAR DE DIEZ EN DIEZ.  Coger los objetos de diez en diez y contar los montones
    como UNA cosa (una decena), mas lo que sobra suelto (las unidades).

      13 objetos  ->  UNA DECENA y 3 UNIDADES

    Esto es el "unitising" (NCETM): diez unidades son UNA decena, y la decena es una cosa nueva.
    """
    if saber is None:
        saber = cargar_conocimiento()
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    cuenta = {"secuencia": secuencia, "_saber": saber}
    r = _aplicar_reglas(saber["reglas_6_2"]["reglas_agrupar"], escena, None, saber, cuenta=cuenta)
    r["escena"] = escena
    r["secuencia"] = secuencia
    if r["conclusion"] != "se_puede":
        r["cuantos_objetos"] = len(escena)
        return r
    total = len(escena)

    def _agrupar(objetos):
        """MECANICO: se van cogiendo los objetos uno a uno, uno por dedo; cuando se acaban los
        diez dedos, ese monton es UNA decena y se empieza otro.  Lo que queda en la mano, sueltos."""
        montones, mano = [], []
        for o in objetos:
            mano.append(o)
            if len(mano) == len(DEDOS_CON_NOMBRE):   # la mano llena: diez
                montones.append(mano)
                mano = []
        return montones, mano

    montones, sueltos = _agrupar(escena)
    decenas = len(montones)
    unidades = len(sueltos)
    r["cuantos_objetos"] = total
    r["decenas"] = decenas
    r["unidades"] = unidades
    r["montones"] = montones
    r["sueltos"] = sueltos
    r["palabra_total"] = _palabra_de(total, secuencia)
    r["cifra_total"] = _tabla(saber).get(r["palabra_total"])
    r["decenas_en_palabra"] = _palabra_de(decenas, secuencia) if decenas else "cero"
    r["unidades_en_palabra"] = _palabra_de(unidades, secuencia) if unidades else "cero"
    # COMO SE DICE ENTERO: "una decena y tres" / "cuatro decenas" / "tres unidades" (si no hay decena)
    # OJO: la decena es FEMENINA ("una decena", no "uno decena").
    r["decena_o_decenas"] = "una decena" if decenas == 1 else "%s decenas" % r["decenas_en_palabra"]
    if total == 0:
        # El conjunto VACIO no es "no hay decena": es CERO (unidad 3.2).  El vacio es una cantidad.
        r["como_se_dice"] = "cero"
    elif decenas and unidades:
        r["como_se_dice"] = "%s y %s" % (r["decena_o_decenas"], r["unidades_en_palabra"])
    elif decenas:
        r["como_se_dice"] = r["decena_o_decenas"]
    else:
        r["como_se_dice"] = "%s unidad%s" % (r["unidades_en_palabra"], "" if unidades == 1 else "es")
    # COMPROBACION 1: los montones y los sueltos tienen que ser TODOS los objetos, ni uno mas ni uno menos.
    r["reparto_cuadra"] = (contar_todo(*(montones + [sueltos])) == total
                           and all(len(m) == len(DEDOS_CON_NOMBRE) for m in montones))
    # COMPROBACION 2 (la de Oak): el ORDEN de los objetos NO cambia el valor.  Se agrupa al reves.
    al_reves = list(reversed(escena))
    m2, s2 = _agrupar(al_reves)
    r["decenas_al_reves"] = len(m2)
    r["unidades_al_reves"] = len(s2)
    r["el_orden_da_igual"] = (r["decenas_al_reves"] == decenas and r["unidades_al_reves"] == unidades)
    r["ordeno_bien"] = len(sueltos) < len(DEDOS_CON_NOMBRE)
    return r


def explicar_6_2_agrupar(escena, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_6_2_agrupar(escena, saber)
    lineas = ["PREGUNTA (6.2): como se agrupan estos objetos DE DIEZ EN DIEZ?"
              "  (el diez pasa a ser UNA cosa: una DECENA)"]
    lineas.append("OBJETOS: %d" % len(escena))
    if r["conclusion"] == "no_alcanza":
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  Son %d objetos, y mi secuencia llega hasta %s.  No me lo invento."
                      % (r["cuantos_objetos"], _hasta_donde_cuento(saber)))
        return "\n".join(lineas)
    if r["conclusion"] == "no_hay_decena":
        lineas.append("RESULTADO: no_hay_decena")
        lineas.append("  Son %d objetos y para hacer UNA decena hacen falta DIEZ." % r["cuantos_objetos"])
        lineas.append("  Con menos de diez NO hay monton que hacer: quedan todos sueltos, y eso son")
        lineas.append("  %d unidad%s." % (r["cuantos_objetos"], "" if r["cuantos_objetos"] == 1 else "es"))
        lineas.append("  (Una decena es diez unidades EXACTAS.  No hay media decena.)")
        return "\n".join(lineas)
    lineas.append("")
    lineas.append("  SE VAN COGIENDO MONTONES DE DIEZ.  Cada monton de diez es UNA DECENA,")
    lineas.append("  y se cuenta como si fuera UNA SOLA COSA (eso es el 'unitising', NCETM).")
    lineas.append("")
    for i, m in enumerate(r["montones"], 1):
        lineas.append("    MONTON %d:  %s" % (i, " ".join(x["id"] for x in m)))
        if i == 1:
            lineas.append("               ^ estos diez objetos son UNA DECENA: ya no se cuentan uno a uno,")
            lineas.append("                 se cuentan como 'uno'.")
    if r["sueltos"]:
        lineas.append("    SUELTOS:   %s" % " ".join(x["id"] for x in r["sueltos"]))
        lineas.append("               ^ y estos NO llegan a diez: son las UNIDADES, y se cuentan DE UNO EN UNO.")
    lineas.append("")
    lineas.append("  SE CUENTAN PRIMERO LAS DECENAS, y despues las unidades (lo dice Oak):")
    lineas.append("    DECENAS:   %d    (se cuentan de DIEZ EN DIEZ: uno, dos, tres... montones)"
                  % r["decenas"])
    lineas.append("    UNIDADES:  %d    (y estas DE UNO EN UNO)" % r["unidades"])
    lineas.append("")
    lineas.append("  OJO CON EL ERROR TIPICO (lo documenta Oak): NO se siguen contando de diez en diez")
    lineas.append("  cuando ya se llega a las unidades.  Las decenas van de diez en diez; las unidades,")
    lineas.append("  de uno en uno.  Si contaras '2 decenas y 3 unidades' de diez en diez, dirias")
    lineas.append("  cualquier cosa.")
    lineas.append("")
    lineas.append("  COMPROBACIONES:")
    lineas.append("    - el reparto cuadra: %d decenas y %d unidades son %d ... %s"
                  % (r["decenas"], r["unidades"], r["cuantos_objetos"],
                     "SI" if r["reparto_cuadra"] else "NO"))
    lineas.append("    - y el ORDEN no cambia nada (Oak): agrupando al reves sale %d decena(s) y %d"
                  % (r["decenas_al_reves"], r["unidades_al_reves"]))
    lineas.append("      unidad(es) ... %s" % ("SI" if r["el_orden_da_igual"] else "NO"))
    lineas.append("")
    lineas.append("RESULTADO: %s   (que son %s objetos)" % (r["como_se_dice"], r["palabra_total"]))
    if r["cifra_total"]:
        lineas.append("  En cifras: %s" % r["cifra_total"])
    elif r["cuantos_objetos"] >= 10:
        lineas.append("  (Su cifra son DOS simbolos, y eso es la unidad 6.3: aqui todavia no la leo.)")
    lineas.append("")
    lineas.append("  Y ESTO ES LO QUE HACE POSIBLE EL VALOR POSICIONAL: diez unidades son UNA decena.")
    lineas.append("  La misma cantidad vista de dos maneras: %d unidades sueltas, o %d monton(es) de diez"
                  % (r["cuantos_objetos"], r["decenas"]))
    lineas.append("  y %d suelta(s)." % r["unidades"])
    lineas.append("  Y sera el paso a multiplicar: %d veces una decena son %d (eso es la unidad 5.6,"
                  " que aun no esta)." % (r["decenas"], escribir_cifras([0] + cifras_de(r["decenas"]))))
    return "\n".join(lineas)


# ------------------------------------------------- la tabla de 100 (6.3)

def decidir_6_3_sitio(texto, saber=None):
    """
    Unidad 6.3: EL SITIO de un numero en la tabla de 100.  Decenas = fila, unidades = columna.

      sitio: 47  ->  fila 4 (cuarenta) y columna 7 (siete)  ->  4 decenas y 7 unidades
    """
    if saber is None:
        saber = cargar_conocimiento()
    palabra, venia_en_cifra = nombre_de_numero(texto, saber)
    valor = _valor_de_numero(palabra, saber)
    # Si es una CIFRA aunque pase de cien, el valor se sabe: que lo diga la regla (fuera_de_la_tabla).
    t = texto.strip()
    if valor is None and t.isdigit():
        valor = int(t)
    cuenta = {"valor": valor, "_saber": saber,
              "secuencia": saber["secuencia_de_conteo"]["palabras"]}
    r = _aplicar_reglas(saber["reglas_6_3"]["reglas_sitio"], None, None, saber, cuenta=cuenta)
    r["texto_dado"] = texto
    r["palabra"] = palabra
    r["venia_en_cifra"] = venia_en_cifra
    r["valor"] = valor
    if r["conclusion"] == "de_la_centena":
        # UNIDAD 6.7: pasa de cien pero no de mil.  Su sitio son centenas, decenas y unidades.
        ce = decidir_6_7_centena(texto, saber)
        ce["regla_6_3"] = r["regla"]
        ce["de_la_centena"] = True
        return ce
    if r["conclusion"] != "se_puede":
        return r
    cif = cifras_de(valor)                      # LEER: la ultima cifra son las unidades
    d, u = escribir_cifras(cif[1:]), cif[0]
    r["decenas"] = d
    r["unidades"] = u
    # EL SITIO EN LA TABLA (la tabla de 100 es 1..100: fila 0 = 1..10, fila 9 = 91..100).
    if valor >= 1:
        # la tabla va del 1 al 100 en filas de diez: una decena exacta cierra la fila de ANTES
        # (el 10 es el ultimo de la fila 0) y va en la columna 10
        if u == 0:
            r["fila"] = leer(anterior(decir(d, saber), saber), saber)
            r["columna"] = 10
        else:
            r["fila"], r["columna"] = d, u
        r["esta_en_la_tabla"] = True
    else:
        r["fila"] = None
        r["columna"] = None
        r["esta_en_la_tabla"] = False   # el cero no esta en la tabla (la tabla empieza en el uno)
    r["decena_en_palabra"] = _palabra_de(d, saber["secuencia_de_conteo"]["palabras"]) if d else "cero"
    r["unidad_en_palabra"] = _palabra_de(u, saber["secuencia_de_conteo"]["palabras"]) if u else "cero"
    r["es_una_decena"] = (u == 0)
    r["es_de_una_cifra"] = (valor < 10)
    r["dato"] = ("cero decenas y cero unidades" if valor == 0
                 else "%d decenas y %d unidades" % (d, u))
    return r


def explicar_6_3_sitio(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_6_3_sitio(texto, saber)
    if r.get("de_la_centena"):
        return explicar_6_7_centena(texto, saber, desde="sitio")
    lineas = ["PREGUNTA (6.3): en que SITIO esta este numero en la tabla de 100?"
              "  (fila = DECENAS, columna = UNIDADES)"]
    lineas.append("NUMERO:  %s" % texto)
    if r["conclusion"] == "no_alcanza":
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  Es un numero, pero pasa de %s: se sale de mi secuencia.  No me lo invento." % techo(saber).upper())
        return "\n".join(lineas)
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  No es un numero que conozca (los mios van del CERO al CIEN).")
        return "\n".join(lineas)
    if r["conclusion"] == "fuera_de_la_tabla":
        lineas.append("RESULTADO: fuera_de_la_tabla")
        lineas.append("  Mi tabla llega hasta el CIEN (diez decenas justas).  Este numero no tiene")
        lineas.append("  sitio, y no me lo invento.")
        return "\n".join(lineas)
    v = r["valor"]
    lineas.append("")
    if v == 0:
        lineas.append("  El CERO no esta en la tabla de 100: la tabla empieza en el UNO.  Y el cero")
        lineas.append("  tiene cero decenas y cero unidades (es una cantidad, unidad 3.2).")
        lineas.append("")
        lineas.append("RESULTADO: cero decenas y cero unidades  (el cero no tiene sitio en la tabla)")
        return "\n".join(lineas)
    if r["es_de_una_cifra"]:
        lineas.append("  Una cifra sola (%d) va SIEMPRE en la fila de las decenas = CERO," % v)
        lineas.append("  o sea: %s decenas y %s unidades.  Por eso se dice '%s' y NO"
                      % (r["decena_en_palabra"], r["unidad_en_palabra"], r["palabra"]))
        lineas.append("  'cero decenas y %s': el cero de las decenas NO se dice." % r["unidad_en_palabra"])
    else:
        lineas.append("  LA PRIMERA CIFRA son las DECENAS:  %s  ->  %d decenas (fila %d)"
                      % (r["decena_en_palabra"], r["decenas"], r["fila"]))
        lineas.append("  LA SEGUNDA CIFRA son las UNIDADES: %s  ->  %d unidades (columna %d)"
                      % (r["unidad_en_palabra"], r["unidades"], r["columna"]))
    lineas.append("")
    lineas.append("  LA TABLA DE 100 (la fila del numero marcada):")
    filas = _filas_de_la_tabla(saber)
    f = r["fila"]
    for k, fila in enumerate(filas):
        if k != f and anterior(decir(k, saber), saber) != decir(f, saber) \
                and siguiente(decir(k, saber), saber) != decir(f, saber):
            continue                                   # solo la fila del numero y sus vecinas
        celdas = ["[%3d]" % n if n == v else " %3d " % n for n in fila]
        marca = "  <-- AQUI" if v in fila else ""
        lineas.append("    fila %d: %s%s" % (k, "".join(celdas), marca))
    lineas.append("")
    lineas.append("  COMO SE LEE (esto es leer una cifra de dos digitos):")
    lineas.append("    %s  ->  %s  ->  '%s'" % (texto if r["venia_en_cifra"] else r["palabra"],
                                                r["dato"], r["palabra"]))
    lineas.append("  Y EL SITIO ES EL VALOR, no es lo mismo que la cantidad:")
    lineas.append("    en %d, el %d son %s; pero en %d el mismo %d serian %s decenas."
                  % (v, cifras_de(v)[0], r["unidad_en_palabra"],
                     escribir_cifras(list(reversed(cifras_de(v)))), cifras_de(v)[0],
                     r["unidad_en_palabra"]))
    if r["es_una_decena"]:
        lineas.append("")
        lineas.append("  OJO: es una DECENA EXACTA (0 unidades), asi que su columna es la 10 y se")
        lineas.append("  dice '%s', sin 'y cero'." % r["palabra"])
    lineas.append("")
    lineas.append("  COMPROBACION: %d son %d decenas y %d unidades  ... %s"
                  % (v, r["decenas"], r["unidades"], "SI" if decidir_6_5_juntar_decenas(str(r["decenas"]), str(r["unidades"]), saber).get("total") == v else "NO"))
    lineas.append("")
    lineas.append("RESULTADO: %s %s (fila %d, columna %d)"
                  % (r["dato"], "-> '%s'" % r["palabra"], r["fila"], r["columna"]))
    return "\n".join(lineas)


def _filas_de_la_tabla(saber):
    """La tabla de 100: se RECITA del uno al cien y se corta en filas de diez (una mano llena)."""
    filas, fila = [], []
    p = "uno"
    while p is not None:
        fila.append(leer(p, saber))
        if len(fila) == len(DEDOS_CON_NOMBRE):
            filas.append(fila)
            fila = []
        if p == "cien":
            break
        p = siguiente(p, saber)
    return filas


def explicar_6_3_tabla(saber=None):
    """La tabla de 100 entera, para verla."""
    if saber is None:
        saber = cargar_conocimiento()
    lineas = ["PREGUNTA (6.3): ensename la TABLA DE 100",
              "  (la fila son las DECENAS; la columna son las UNIDADES)",
              ""]
    for k, fila in enumerate(_filas_de_la_tabla(saber)):
        lineas.append("  fila %d: %s" % (k, "".join(" %3d " % n for n in fila)))
    lineas.append("")
    lineas.append("  COMO SE RECORRE:")
    lineas.append("    - dentro de una fila, DE UNO EN UNO (47 -> 48: todavia en la fila 4)")
    lineas.append("    - bajando de fila, DE DIEZ EN DIEZ (47 -> 57: otra decena entera)")
    lineas.append("    (y cada fila es UNA DECENA ENTERA: eso es la unidad 6.2)")
    lineas.append("")
    lineas.append("  La tabla llega hasta el %s, que son DIEZ decenas justas (la ultima fila)."
                  % _hasta_donde_cuento(saber))
    lineas.append("  Se cuenta de dos maneras y las dos son ciertas: uno a uno (100 palabras) o de")
    lineas.append("  diez en diez (10 filas).  Es la misma cantidad.")
    lineas.append("")
    lineas.append("RESULTADO: la tabla de 100, fila a fila")
    lineas.append("   (prueba 'sitio: 47' para ver el sitio de un numero en concreto)")
    return "\n".join(lineas)


# ------------------------------------------------- partir en decenas y unidades (6.5)

def decidir_6_5_partir(texto, saber=None):
    """
    Unidad 6.5: PARTIR EN DECENAS Y UNIDADES.  Cuanto vale cada cifra.

      47  =  4 decenas  +  7 unidades  =  40 + 7
    """
    if saber is None:
        saber = cargar_conocimiento()
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    palabra, venia = nombre_de_numero(texto, saber)
    valor = _valor_de_numero(palabra, saber)
    t = texto.strip()
    if valor is None and t.isdigit():
        valor = int(t)
    cuenta = {"valor": valor, "secuencia": secuencia}
    r = _aplicar_reglas(saber["reglas_6_5"]["reglas_partir"], None, None, saber, cuenta=cuenta)
    r["texto_dado"], r["palabra"], r["venia_en_cifra"], r["valor"] = texto, palabra, venia, valor
    if r["conclusion"] == "de_la_centena":
        # UNIDAD 6.7: de tres cifras se parte en CENTENAS, decenas y unidades.
        ce = decidir_6_7_centena(texto, saber)
        ce["de_la_centena"] = True
        return ce
    if r["conclusion"] != "se_puede":
        return r
    cif = cifras_de(valor)                    # LEER la cifra: la ultima son las unidades
    d, u = escribir_cifras(cif[1:]), cif[0]   # y lo de delante son las decenas
    r["decenas"], r["unidades"] = d, u
    r["valor_de_las_decenas"] = escribir_cifras([0] + cif[1:])   # el 4 de 47 vale 40
    r["tabla"] = _tabla(saber)
    r["palabra_del_total"] = _palabra_de(valor, secuencia) if valor else "cero"
    # COMO SE DICE: "cuatro decenas y siete unidades" / "cuarenta y siete"
    r["partes_dichas"] = "%s decenas y %s unidades" % (
        _palabra_de(d, secuencia) if d else "cero",
        _palabra_de(u, secuencia) if u else "cero")
    r["cuenta_de_la_particion"] = ("%d decenas y %d unidades son %d" % (d, u, valor) if d
                                   else "solo unidades: son %d" % valor)
    r["como_se_parte"] = "%d decenas + %d unidades = %d" % (d, u, valor)
    r["valor_posicional"] = ("%d vale %d (no %d)" % (d, r["valor_de_las_decenas"], d)
                             if d else "el 0 de las decenas no vale nada")
    # EL ERROR TIPICO DE OAK: sumar las cifras como si valieran lo mismo
    r["si_sumara_las_cifras"] = _suma_con_metodo(d, u, saber)["total"]
    r["seria_el_error"] = (r["si_sumara_las_cifras"] != valor)
    return r


def explicar_6_5_partir(texto, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_6_5_partir(texto, saber)
    if r.get("de_la_centena"):
        return explicar_6_7_centena(texto, saber, desde="partir")
    lineas = ["PREGUNTA (6.5): cuanto vale CADA CIFRA de este numero?  (partirlo en decenas y unidades)"]
    lineas.append("NUMERO:  %s" % texto)
    if r["conclusion"] == "no_alcanza":
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  Es un numero, pero pasa de %s: se sale de mi secuencia.  No me lo invento." % techo(saber).upper())
        return "\n".join(lineas)
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  No es un numero que conozca (los mios van del CERO al CIEN).")
        return "\n".join(lineas)
    if r["conclusion"] == "fuera_de_la_tabla":
        lineas.append("RESULTADO: fuera_de_la_tabla")
        lineas.append("  Mi tabla llega hasta el CIEN.  Este numero no lo parto: no me lo invento.")
        return "\n".join(lineas)
    v, d, u = r["valor"], r["decenas"], r["unidades"]
    lineas.append("")
    lineas.append("  LA PRIMERA CIFRA SON LAS DECENAS y la ultima son las UNIDADES (BBC Bitesize).")
    lineas.append("")
    if v < 10:
        lineas.append("  %d tiene UNA cifra sola, asi que va en las unidades:" % v)
        lineas.append("    0 decenas y %d unidades.  Y el cero de las decenas NO se dice: se dice '%s'."
                      % (v, r["palabra_del_total"]))
    else:
        lineas.append("    DECENAS:   %d   ->  y NO vale %d: vale %d  (porque son %d decenas)"
                      % (d, d, r["valor_de_las_decenas"], d))
        lineas.append("    UNIDADES:  %d   ->  y esto SI vale %d" % (u, u))
    lineas.append("")
    lineas.append("  LA CUENTA ES:  %s" % r["cuenta_de_la_particion"])
    lineas.append("  Es decir: %s" % r["partes_dichas"])
    lineas.append("  Y eso es el mismo numero de antes: '%s' = %s" % (r["palabra_del_total"], v))
    lineas.append("")
    lineas.append("  POR QUE ESTO IMPORTA (el error tipico, lo documenta Oak):")
    if r["seria_el_error"]:
        lineas.append("    OJO: si sumaras las cifras como si valieran lo mismo, %d + %d = %d,"
                      % (d, u, r["si_sumara_las_cifras"]))
        lineas.append("    y %d NO es %d.  Eso es 'transponer los digitos': las decenas NO son unidades."
                      % (r["si_sumara_las_cifras"], v))
    else:
        lineas.append("    aqui las cifras suman %d y el numero es %d: justo por eso hay que mirar"
                      % (r["si_sumara_las_cifras"], v))
        lineas.append("    EL SITIO, no la cifra.  La misma cifra vale cosas distintas segun donde este.")
    lineas.append("    En 73 el 7 vale SETENTA; en el 7 solo, vale SIETE.  El sitio es el valor.")
    lineas.append("")
    lineas.append("  COMPROBACION (juntarlo otra vez tiene que dar el numero):")
    lineas.append("    %d decenas y %d unidades son %d ... %s"
                  % (d, u, v, "SI" if decidir_6_5_juntar_decenas(str(d), str(u), saber).get("total") == v else "NO"))
    lineas.append("")
    lineas.append("RESULTADO: %s decenas + %s unidades = %d"
                  % (d, u, v))
    lineas.append("")
    lineas.append("  Y ESTO ES LO QUE HACE FALTA PARA SUMAR POR COLUMNAS (unidad 7.3): suma")
    lineas.append("  decenas con decenas y unidades con unidades.  Para eso hay que saber partir")
    lineas.append("  primero, y por eso van en este orden.  (Lo dice Oak.)")
    return "\n".join(lineas)


def decidir_6_5_juntar_decenas(decenas, unidades, saber=None):
    """
    Unidad 6.5, al reves: JUNTAR las decenas y las unidades.

      4 decenas y 7 unidades  ->  47
    """
    if saber is None:
        saber = cargar_conocimiento()
    secuencia = saber["secuencia_de_conteo"]["palabras"]

    def _a_valor(txt):
        p, _ = nombre_de_numero(str(txt), saber)
        v = _valor_de_numero(p, saber)
        return v

    d, u = _a_valor(decenas), _a_valor(unidades)
    cuenta = {"decenas": d, "unidades": u, "secuencia": secuencia}
    r = _aplicar_reglas(saber["reglas_6_5"]["reglas_juntar_decenas"], None, None, saber, cuenta=cuenta)
    r["decenas_dadas"], r["unidades_dadas"] = decenas, unidades
    r["decenas"], r["unidades"] = d, u
    if r["conclusion"] != "se_puede":
        return r
    # JUNTAR, mecanico: las decenas se escriben con un cero detras de su cifra (4 decenas -> 40,
    # la palabra 'cuarenta') y desde ahi se cuentan las unidades una a una.  (Asi 3 decenas y 12
    # unidades dan cuarenta y dos: contando, se pasa solo de una decena a la siguiente.)
    total = juntar_decenas(d, u, saber)          # mecanismo.py
    r["total"] = total
    r["palabra"] = _palabra_de(total, secuencia) if total else "cero"
    r["cuenta"] = "%d decenas y %d unidades son %d" % (d, u, total)
    r["dato"] = "%s -> %d" % (r["palabra"], total) if total else "cero -> 0"
    r["demasiadas_unidades"] = u >= 10
    r["se_dice"] = r["palabra"]
    return r


def explicar_6_5_juntar_decenas(decenas, unidades, saber=None):
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_6_5_juntar_decenas(decenas, unidades, saber)
    lineas = ["PREGUNTA (6.5): juntando estas decenas y estas unidades, que numero sale?"]
    lineas.append("DECENAS:  %s     UNIDADES:  %s" % (decenas, unidades))
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  Las decenas y las unidades tienen que ser numeros que conozca.")
        return "\n".join(lineas)
    if r["conclusion"] in ("fuera_de_la_tabla", "no_alcanza"):
        lineas.append("RESULTADO: %s" % r["conclusion"])
        lineas.append("  Eso se pasa de %s (%d decenas y %d unidades), y mi secuencia llega ahi."
                      % (techo(saber).upper(), r["decenas"], r["unidades"]))
        return "\n".join(lineas)
    d, u = r["decenas"], r["unidades"]
    lineas.append("")
    lineas.append("  CADA DECENA SON DIEZ (unidad 6.2), asi que %d decenas son %d"
                  % (d, escribir_cifras([0] + cifras_de(d))))
    lineas.append("  Y las unidades valen lo que dicen: %d" % u)
    lineas.append("")
    lineas.append("  SE JUNTAN:  %s" % r["cuenta"])
    lineas.append("")
    if r["demasiadas_unidades"]:
        lineas.append("  OJO: hay %d unidades, y con DIEZ unidades se hace OTRA DECENA." % u)
        lineas.append("  Por eso no se dice 'cuarenta y quince': se dice '%s'." % r["palabra"])
        lineas.append("  (Los nombres raros tipo 'sesenta y quince' son el error de decena otra vez.)")
        lineas.append("")
    lineas.append("  COMPROBACION (partirlo otra vez tiene que dar lo mismo):")
    lineas.append("    %d -> %d decenas y %d unidades" % (r["total"], d, u))
    lineas.append("")
    lineas.append("RESULTADO: %s" % r["dato"])
    return "\n".join(lineas)


def _suma_con_metodo(a, b, saber):
    """
    Hace una suma pequena (la de una columna) y devuelve COMO se hizo, para poder ENSENARLO.
    El total SALE del metodo ensenado: los dedos (7.1) o, si no caben, derivar (7.2).  Ninguna
    suma de Python.  Si no hay metodo que valga, NO se inventa: se dice.
    Lo cazo Carlos: la suma por columnas decia "7 + 5 = 12" a secas, y no decia de donde salia.
    """
    pa, pb = decir(a, saber), decir(b, saber)
    ded = decidir_7_1_dedos(pa, pb, saber)
    d = {"a": a, "b": b, "palabra_a": pa, "palabra_b": pb}
    if ded["conclusion"] == "se_puede":
        d["metodo"] = "dedos (7.1)"
        d["detalle"] = ded
        d["palabra_total"] = ded["total"]
        d["como"] = ("se anota el %s y se cuentan %d dedos hacia adelante desde el %s"
                     % (pa, b, pa))
    else:
        der = decidir_7_2_derivar(pa, pb, saber)
        if der["conclusion"] != "se_puede":
            raise ValueError("no tengo metodo para %s + %s" % (a, b))
        d["metodo"] = "derivar (7.2)"
        d["detalle"] = der
        d["palabra_total"] = der["total"]
        d["como"] = ("al %s le faltan %d para diez, y se parte el %s en %d y %d"
                     % (pa, der["faltan_para_diez"], pb, der["parte_para_diez"],
                        der["parte_que_sobra"]))
    d["total"] = leer(d["palabra_total"], saber)
    return d


def _dos_pasos(a, b, c, saber):
    """
    Suma TRES numeros de una cifra EN DOS PASOS, porque el sistema solo tiene el metodo de sumar
    DOS.  Antes decia "4 + 1 + 1 = 6" de golpe, que es un metodo que NO tiene.

    Lo cazo Carlos: "4 + 1 + 1 = 6 no deberia ser 4+1 = 5 y 5 + 1 = 6?"
    """
    p1 = _suma_con_metodo(a, b, saber)
    p2 = _suma_con_metodo(p1["total"], c, saber)
    return {"paso_1": p1, "paso_2": p2, "total": p2["total"]}


# ------------------------------------------------- la centena (6.7)
#
# LA ESCALERA: 10 unidades hacen 1 decena, 10 decenas hacen 1 centena, 10 centenas hacen 1 unidad
# de mil.  Es el MISMO movimiento de la 6.2 (el diez como UNA cosa), un escalon mas arriba.
# Todo lo que se dice aqui sale de la_centena.kn y de reglas_6_7.kn.

_ORDENES = (("unidad", "unidades"), ("decena", "decenas"), ("centena", "centenas"),
            ("unidad de mil", "unidades de mil"))


def _orden(i, cuantas):
    """'1 centena' / '2 centenas' (en singular cuando toca)."""
    sing, plur = _ORDENES[i]
    return "%d %s" % (cuantas, sing if cuantas == 1 else plur)


def _partir_por_ordenes(valor):
    """Las cifras de un numero, de la derecha a la izquierda (se LEEN de la cifra escrita)."""
    return cifras_de(valor)


def _nombre_o_cero(n, saber):
    return construir_nombre_hasta_diez_mil(n, saber) if n else "cero"


def decidir_6_7_centena(texto, saber=None):
    """
    Unidad 6.7: LA CENTENA.  Un numero hasta mil, partido en centenas, decenas y unidades.

      247  ->  2 centenas, 4 decenas y 7 unidades  =  doscientos + cuarenta + siete
      204  ->  2 centenas, 0 decenas y 4 unidades  (y OJO: tiene VEINTE decenas, no cero)
    """
    if saber is None:
        saber = cargar_conocimiento()
    secuencia = saber["secuencia_de_conteo"]["palabras"]
    palabra, venia = nombre_de_numero(texto, saber)
    valor = _valor_de_numero(palabra, saber)
    t = texto.strip()
    if valor is None and t.isdigit():
        valor = int(t)          # es un numero aunque se salga: que lo diga la regla (no_alcanza)
    cuenta = {"valor": valor, "secuencia": secuencia}
    r = _aplicar_reglas(saber["reglas_6_7"]["reglas_centena"], None, None, saber, cuenta=cuenta)
    r["texto_dado"], r["palabra"], r["venia_en_cifra"], r["valor"] = texto, palabra, venia, valor
    if r["conclusion"] != "se_puede":
        return r
    cifras = cifras_de(valor)        # LEER la cifra simbolo a simbolo (unidades primero)
    while len(cifras) < 3:
        cifras.append(0)        # 47 -> 0 centenas, 4 decenas, 7 unidades
    r["cifras"] = cifras
    r["unidades"], r["decenas"], r["centenas"] = cifras[0], cifras[1], cifras[2]
    r["unidades_de_mil"] = cifras[3] if len(cifras) > 3 else 0
    # LO QUE VALE CADA CIFRA (por su SITIO).  Se dice con nombres, no con 'x 100' (regla 6).
    valores = []
    for i, c in enumerate(cifras):
        vale = escribir_cifras(_rellenar([], i) + [c])   # la cifra con sus ceros detras: 2 -> 200
        valores.append({"orden": _ORDENES[i][1], "cifra": c, "vale": vale,
                        "dicho": _orden(i, c),
                        "vale_en_palabra": _nombre_o_cero(vale, saber)})
    r["valores"] = valores
    partes = [_orden(i, c) for i, c in reversed(list(enumerate(cifras)))]
    r["dato"] = ", ".join(partes[:-1]) + " y " + partes[-1]
    r["como_se_parte"] = " + ".join(partes) + " = %d" % valor
    r["palabra"] = _nombre_o_cero(valor, saber)
    # EL ERROR TIPICO (NZ Maths): "204 no tiene decenas".  Si las tiene: las de las centenas tambien.
    r["decenas_en_total"] = escribir_cifras(cifras[1:])     # todo lo de delante de las unidades
    r["centenas_en_total"] = escribir_cifras(cifras[2:])
    r["ceros_de_relleno"] = [v["orden"] for v in valores[:-1] if v["cifra"] == 0 and valor >= 10]
    # COMPROBACIONES (sin cajas negras: juntar otra vez tiene que dar el numero)
    r["recompone"] = escribir_cifras(cifras) == valor     # se vuelven a escribir juntas
    r["nombre_coincide"] = (_valor_de_numero(r["palabra"], saber) == valor) if valor else True
    return r


def explicar_6_7_escalera(saber=None):
    """'centena' (sin numero) -> la escalera entera, comprobada con lo que el sistema ya sabe."""
    if saber is None:
        saber = cargar_conocimiento()
    cent = _centenas(saber)
    lineas = ["PREGUNTA (6.7): que es una CENTENA?  (la escalera del valor posicional)", ""]
    lineas.append("  LA ESCALERA VA DE DIEZ EN DIEZ, Y SIEMPRE IGUAL (la_centena.kn, regla 1):")
    pasos = [("10 unidades", "1 decena", 10), ("10 decenas", "1 centena", 100),
             ("10 centenas", "1 unidad de mil", 1000)]
    for a, b, v in pasos:
        lineas.append("    %-12s hacen  %-16s  (%s)" % (a, b, _nombre_o_cero(v, saber)))
    lineas.append("  Es el MISMO movimiento repetido: juntas DIEZ de una cosa y tienes UNA de la"
                  " siguiente.")
    lineas.append("  (Lo mismo que la 6.2 hizo con el diez, un escalon mas arriba.)")
    lineas.append("")
    lineas.append("  COMPROBADO CON LO QUE YA SABIA:")
    jd = decidir_6_5_juntar_decenas("10", "0", saber)
    lineas.append("    juntar 10 decenas y 0 unidades (6.5) -> %s ... %s"
                  % (jd.get("palabra", jd["conclusion"]), "SI" if jd.get("total") == 100 else "NO"))
    c10 = decidir_6_7_centena("1000", saber)
    lineas.append("    1000 partido por ordenes -> %s ... %s"
                  % (c10.get("dato", c10["conclusion"]),
                     "SI" if c10.get("unidades_de_mil") == 1 else "NO"))
    lineas.append("")
    lineas.append("  LOS NOMBRES DE LOS CIENTOS hay que SABERSELOS (son nueve); el resto se construye:")
    for k in range(1, 10):
        solo = cent["cientos_solos"].get(k)
        con = cent["cientos"].get(k)
        extra = "" if solo == con else "   (pero %d solo es '%s')" % (escribir_cifras([0, 0, k]), solo)
        irr = "   <- IRREGULAR" if con in (cent.get("irregulares") or []) else ""
        lineas.append("    %d centenas -> %s ...%s%s" % (k, con, extra, irr))
    lineas.append("    y 10 centenas -> %s" % (cent.get("mil") or "mil"))
    lineas.append("")
    lineas.append("  EL CERO TIENE DOS USOS (NZ Maths): como CANTIDAD ('ninguno') y como")
    lineas.append("  MARCADOR DE POSICION (en 704 dice que no hay decenas SUELTAS).")
    lineas.append("")
    lineas.append("RESULTADO: la_escalera")
    return "\n".join(lineas)


def explicar_6_7_centena(texto, saber=None, desde=None):
    """'centena: 247' (y sitio:/partir: de tres cifras) -> centenas, decenas y unidades."""
    if saber is None:
        saber = cargar_conocimiento()
    r = decidir_6_7_centena(texto, saber)
    cab = "PREGUNTA (6.7): como se PARTE este numero en centenas, decenas y unidades?"
    if desde:
        cab += "  (llegado por '%s:', que pasa de cien)" % desde
    lineas = [cab, "NUMERO:  %s" % texto]
    if r["conclusion"] == "no_es_un_numero":
        lineas.append("RESULTADO: no_es_un_numero")
        lineas.append("  '%s' no es un numero que sepa leer (los mios van del CERO al %s)." % (texto, techo(saber).upper()))
        return "\n".join(lineas)
    if r["conclusion"] == "no_alcanza":
        lineas.append("RESULTADO: no_alcanza")
        lineas.append("  %s es un numero, pero se sale de mi secuencia (llega a %s).  No me lo"
                      " invento." % (r["valor"], techo(saber).upper()))
        return "\n".join(lineas)
    v = r["valor"]
    lineas.append("")
    lineas.append("  SE PARTE POR SITIOS, de la derecha a la izquierda (la posicion dice el valor, Oak):")
    for i, c in enumerate(r["valores"]):
        if i >= 3 and c["cifra"] == 0:
            continue
        lineas.append("    %-16s %d  ->  vale %s (%d)" % (c["orden"].upper() + ":", c["cifra"],
                                                          c["vale_en_palabra"], c["vale"]))
    lineas.append("")
    lineas.append("  O SEA:  %s" % r["como_se_parte"])
    if r["centenas"] or r["unidades_de_mil"]:
        lineas.append("  (y NO se dice '%d x 100': el sistema no sabe multiplicar.  Se dice '%s', que"
                      % (r["centenas"], _orden(2, r["centenas"])))
        lineas.append("   es juntar decenas de diez en diez, un escalon mas arriba.)")
    if r["ceros_de_relleno"]:
        lineas.append("")
        lineas.append("  OJO CON EL CERO: aqui es un MARCADOR DE POSICION (no hay %s sueltas)."
                      % " ni ".join(r["ceros_de_relleno"]))
    if v >= 100:
        lineas.append("")
        lineas.append("  Y EL ERROR TIPICO (NZ Maths): '%d no tiene decenas' o 'tiene %d decenas'."
                      % (v, r["decenas"]))
        lineas.append("  NO: en %d hay %d DECENAS en total (las de las centenas tambien cuentan)."
                      % (v, r["decenas_en_total"]))
        lineas.append("  La cifra de las decenas dice solo las SUELTAS: %d." % r["decenas"])
    lineas.append("")
    lineas.append("  EL NOMBRE SE CONSTRUYE (6.1 + los cientos de la 6.7):  '%s'" % r["palabra"])
    lineas.append("")
    lineas.append("  COMPROBACIONES:")
    lineas.append("    - juntando lo que vale cada cifra sale %d ... %s"
                  % (v, "SI" if r["recompone"] else "NO"))
    lineas.append("    - y el nombre, leido otra vez, es %d ... %s"
                  % (v, "SI" if r["nombre_coincide"] else "NO"))
    lineas.append("")
    lineas.append("RESULTADO: %s -> '%s'" % (r["dato"], r["palabra"]))
    return "\n".join(lineas)


def decidir_6_1_nombre(texto, saber=None):
    """
    'nombre: 247' -> la palabra.  UNA SOLA VERDAD para el probador y para el explicador.
    (Antes el probador tenia su propia logica y decia 'ciento uno' mientras el explicador -- lo
    que ve quien prueba -- decia 'fuera_de_mi_secuencia'.  Lo cazo la revision del 5 oct 2026.)
    """
    if saber is None:
        saber = cargar_conocimiento()
    t = texto.strip()
    if not t:
        return {"conclusion": "no_entendido"}
    if not t.isdigit():
        return {"conclusion": "no_lo_se", "texto": t}
    n = int(t)
    if n < 1 or n > len(saber["secuencia_de_conteo"]["palabras"]):
        return {"conclusion": "fuera_de_mi_secuencia", "valor": n}
    return {"conclusion": "nombre", "valor": n, "palabra": construir_nombre_hasta_diez_mil(n, saber)}


def decidir_6_1_numero(texto, saber=None):
    """'numero: doscientos cuarenta y siete' -> 247.  Lee el MISMO mapa que todas las puertas."""
    if saber is None:
        saber = cargar_conocimiento()
    t = texto.strip().lower()
    if not t:
        return {"conclusion": "no_entendido"}
    v = (saber.get("_nombre_a_valor") or {}).get(t)
    if v is None:
        return {"conclusion": "no_lo_se", "texto": t}
    return {"conclusion": "numero", "valor": v, "palabra": t}
