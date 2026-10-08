# -*- coding: utf-8 -*-
"""
Euclides - EL RESOLVEDOR UNIVERSAL, SEGUNDA FASE: BUSCAR CON CONTROL (fase U.2 del plan U, 8 oct 2026).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).  Prefijo _bu_.

U.1 (universal.py) lee el MODELO y tiene dos operadores: calcular despejando y sustituir.  Aqui se anaden tres, y el
CONTROL que elige cual usar (diario/2026-10-08-paso-U2-buscar-con-control.md):

  3. JUNTAR RELACIONES: dos relaciones en las que una letra tiene los mismos trozos se RESTAN (o se SUMAN si son
     contrarios; o se quita la otra K veces si son K veces): la letra se va (NCETM 1.31, punto 4: quitar la diferencia).
  4. REESCRIBIR CON EQUIVALENCIAS: un BLOQUE que ya se sabe ((a + b) x c = 21 con a + b = 7 -> 7 x c = 21); sacar
     FACTOR COMUN y simplificar (2 x a + 2 x b = 20 -> a + b = 10); agrupar los trozos iguales (a + a = 2 x a).
  5. PROBAR EN ORDEN (NCETM 1.31, punto 5), con un tope humano: cuando nada de lo anterior baja las letras (n x n = 49;
     a x b = 24 y a + b = 10).  Desde el 0, y se para cuando YA SE PASA (seguir solo pasaria mas).

EL CONTROL (Newell y Simon: medios y fines; Schoenfeld: cuando usar cada cosa).  En cada vuelta se miran TODOS los
operadores que encajan, cada uno con lo que DEJA (las letras de la relacion que sale: cuantas menos, mas cerca de
calcular) y lo que CUESTA (conocimiento/universal.kn).  Se elige el que deja menos letras; si empatan, el mas barato.
Probar en orden solo si no hay otro.  Con presupuesto de pasos y de pruebas.  Sin recetas de ninguna familia.
"""

_BU_UNO = ("+", 1, 1, "entero")
_BU_NOMBRES = {"calcular": "calcular despejando", "sustituir": "sustituir", "juntar": "juntar relaciones",
               "reescribir": "reescribir", "probar": "probar en orden"}


# ------------------------------------------------------------- los numeros pequenos del control (con el mecanismo)

def _bu_kn(saber, clave, defecto):
    t = str((saber.get("universal") or {}).get(clave, defecto))
    return escribir_cifras(cifras_de(t if t.isdigit() else defecto))      # LEER las cifras: '30' -> 30


def _bu_menor(a, b, saber):
    """a es MAS PEQUENO que b (4.2: b viene despues en la lista)."""
    return viene_despues(decir(b, saber), decir(a, saber), saber)


def _bu_pasa(x, y, saber):
    """El numero comun x se PASA de y (x - y es positivo y no es cero)."""
    d = _u_cuenta("-", x, y, saber, [])
    return d[0] == "+" and not _nu_es_cero(d)


def _bu_para_contar(x):
    """Un numero para contar: entero (abajo 1) y no negativo."""
    return x[2] == 1 and (x[0] == "+" or _nu_es_cero(x))


# ------------------------------------------------------------- los TROZOS con varias letras

def _bu_trozos(e, saber):
    """Una expresion lineal -> ({letra: trozos}, suelto).  Agrupa los trozos iguales (a + a = 2 trozos de a).
    _UNoLineal si una letra se multiplica por otra (o por si misma) o divide."""
    if e[0] == "letra":
        return {e[1]: _BU_UNO}, _NU_CERO
    if e[0] == "num":
        return {}, e[1]
    if e[0] == "par":
        return _bu_trozos(e[1], saber)
    if e[0] == "neg":
        c, k = _bu_trozos(e[1], saber)
        return dict((l, _nu_opuesto(v)) for l, v in c.items()), _nu_opuesto(k)
    op, izq, der = e[1], e[2], e[3]
    if op in "+-":
        c1, k1 = _bu_trozos(izq, saber)
        c2, k2 = _bu_trozos(der, saber)
        return _bu_mezclar(c1, c2, op, saber), _u_cuenta(op, k1, k2, saber, [])
    if op == "x" and not _u_letras(izq):
        return _bu_escalar(_bu_trozos(der, saber), "x", _u_valor(izq, saber, []), saber)
    if not _u_letras(der):
        return _bu_escalar(_bu_trozos(izq, saber), op, _u_valor(der, saber, []), saber)
    raise _UNoLineal("una letra se multiplica o se divide por una letra")


def _bu_mezclar(c1, c2, op, saber):
    c = dict(c1)
    for l, v in c2.items():
        if l in c:
            c[l] = _u_cuenta(op, c[l], v, saber, [])
        else:
            c[l] = v if op == "+" else _nu_opuesto(v)
    return dict((l, v) for l, v in c.items() if not _nu_es_cero(v))


def _bu_escalar(ck, op, v, saber):
    c, k = ck
    return (dict((l, _u_cuenta(op, x, v, saber, [])) for l, x in c.items()),
            _u_cuenta(op, k, v, saber, []))


def _bu_rel_trozos(rel, saber):
    """izq = der  ->  (trozos de las letras a la izquierda, lo suelto a la derecha); el primer trozo, positivo."""
    c1, k1 = _bu_trozos(rel[0], saber)
    c2, k2 = _bu_trozos(rel[1], saber)
    c = _bu_mezclar(c1, c2, "-", saber)
    k = _u_cuenta("-", k2, k1, saber, [])
    return _bu_derecha(c, k)


def _bu_derecha(c, k):
    """Si el primer trozo queda quitando, se le da la vuelta a todo (los dos lados al reves: sigue siendo igual)."""
    primero = next(iter(c.values()), None)
    if primero is not None and primero[0] == "-":
        return dict((l, _nu_opuesto(v)) for l, v in c.items()), _nu_opuesto(k)
    return c, k


def _bu_rel_de_trozos(c, k):
    """({a: 2, b: -1}, 8) -> el arbol de 2 x a - b = 8."""
    e = None
    for l, v in c.items():
        positivo = v[0] == "+"
        cuanto = v if positivo else _nu_opuesto(v)
        t = ("letra", l) if cuanto == _BU_UNO else ("op", "x", ("num", cuanto), ("letra", l))
        if e is None:
            e = t if positivo else ("neg", t)
        else:
            e = ("op", "+" if positivo else "-", e, t)
    return (e if e is not None else ("num", _NU_CERO), ("num", k))


def _bu_barra(c, k, saber):
    """La barra: [a][a][b] = 30;  [a] quitando [b] = 8;  [a] x 12 = 36."""
    pon, quita = [], []
    for l, v in c.items():
        cuanto = v if v[0] == "+" else _nu_opuesto(v)
        caja = "[%s]" % _u_nombre(l)
        if cuanto[2] == 1 and not viene_despues(decir(cuanto[1], saber), "cinco", saber):
            dibujo = "".join(caja for _ in range(cuanto[1], 0, -1))
        else:
            dibujo = "%s x %s" % (caja, _nu_texto(cuanto))
        (pon if v[0] == "+" else quita).append(dibujo)
    t = "".join(pon) or "0"
    if quita:
        t = "%s quitando %s" % (t, "".join(quita))
    return "%s = %s" % (t, _nu_texto(k))


# ------------------------------------------------------------- los candidatos de cada operador

def _bu_candidatos(rels, saber):
    """Todo lo que se puede hacer ahora, cada cosa con lo que deja (letras) y lo que cuesta."""
    cands = []
    formas = []
    for rel in rels:
        try:
            formas.append(_bu_rel_trozos(rel, saber))
        except (_UNoLineal, _UNoSale, _NuNoSale, KeyError):
            formas.append(None)                          # no es lineal (o no se deja contar en trozos)
    cands.extend(_bu_calcular(rels, saber))
    cands.extend(_bu_sustituir(rels, saber))
    cands.extend(_bu_juntar(rels, formas, saber))
    cands.extend(_bu_bloques(rels, saber))
    cands.extend(_bu_simplificar(rels, formas, saber))
    return cands


def _bu_cuantas_letras(rel):
    return len(_u_distintas(_u_letras_rel(rel)))


def _bu_calcular(rels, saber):
    out = []
    for i, rel in enumerate(rels):
        letras = _u_distintas(_u_letras_rel(rel))
        if len(letras) != 1:
            continue
        if len(_u_letras_rel(rel)) != 1:
            try:
                _u_lineal(rel[0], letras[0], saber, [])
                _u_lineal(rel[1], letras[0], saber, [])
            except (_UNoLineal, _UNoSale, _NuNoSale, KeyError):
                continue                                 # la letra por si misma (n x n): eso se prueba en orden
        out.append({"op": "calcular", "i": i, "letra": letras[0], "deja": 0, "coste": "coste_calcular",
                    "dice": "%s solo tiene %s" % (_u_rel_texto(rel), _u_nombre(letras[0]))})
    return out


def _bu_sustituir(rels, saber):
    out = []
    for i, rel in enumerate(rels):
        todas = _u_letras_rel(rel)
        for letra in _u_distintas(todas):
            otras = [j for j, r in enumerate(rels) if j != i and letra in _u_letras_rel(r)]
            if not otras:
                continue                                 # no esta en otra relacion: ponerla no baja nada
            arbol, como = None, None
            for lado, otro in ((rel[0], rel[1]), (rel[1], rel[0])):
                if lado == ("letra", letra) and letra not in _u_letras(otro):
                    arbol, como = otro, "sola"
            if arbol is None and todas.count(letra) == 1:
                con, sin = (rel[0], rel[1]) if letra in _u_letras(rel[0]) else (rel[1], rel[0])
                arbol, como = _u_aislar(con, sin, letra), "aislada"
            if arbol is None:
                continue
            nuevas = [(_u_poner(rels[j][0], letra, arbol), _u_poner(rels[j][1], letra, arbol)) for j in otras]
            deja = None
            for x in nuevas:
                n = _bu_cuantas_letras(x)
                if deja is None or _bu_menor(n, deja, saber):
                    deja = n
            out.append({"op": "sustituir", "i": i, "letra": letra, "arbol": arbol, "como": como, "deja": deja,
                        "torcido": _bu_torcido(arbol),
                        "coste": "coste_sustituir_sola" if como == "sola" else "coste_sustituir_aislando",
                        "dice": "%s = %s" % (_u_nombre(letra), _u_texto(arbol))})
    return out


def _bu_torcido(e):
    """Una letra multiplicada por otra o dividiendo (24 : b): lo que se pone ya no es una cosa de trozos."""
    if e[0] in ("num", "letra"):
        return False
    if e[0] in ("par", "neg"):
        return _bu_torcido(e[1])
    if (e[1] == "x" and _u_letras(e[2]) and _u_letras(e[3])) or (e[1] == ":" and _u_letras(e[3])):
        return True
    return _bu_torcido(e[2]) or _bu_torcido(e[3])


def _bu_juntar(rels, formas, saber):
    """Dos relaciones lineales; una letra con trozos iguales (restar), contrarios (sumar) o K veces (quitar K veces)."""
    out = []
    for i, fi in enumerate(formas):
        for j, fj in enumerate(formas):
            if i == j or fi is None or fj is None:
                continue
            for letra in fi[0]:
                if letra not in fj[0]:
                    continue
                try:
                    k = _u_cuenta(":", fi[0][letra], fj[0][letra], saber, [])
                except (_UNoSale, _NuNoSale, KeyError):
                    continue
                if k[2] != 1:
                    continue                             # no son un numero entero de veces
                try:
                    c = _bu_mezclar(fi[0], dict((l, _u_cuenta("x", k, v, saber, [])) for l, v in fj[0].items()),
                                    "-", saber)
                    suelto = _u_cuenta("-", fi[1], _u_cuenta("x", k, fj[1], saber, []), saber, [])
                except (_UNoSale, _NuNoSale, KeyError):
                    continue
                c, suelto = _bu_derecha(c, suelto)
                if not _bu_menor(len(c), len(fi[0]), saber):
                    continue
                if k == _BU_UNO:
                    como = "las RESTO (%s tiene los mismos trozos en las dos)" % _u_nombre(letra)
                elif _nu_iguales(k, _nu_opuesto(_BU_UNO), saber):
                    como = "las SUMO (los trozos de %s se quitan en una y se ponen en la otra)" % _u_nombre(letra)
                elif k[0] == "+":
                    como = "a la primera le QUITO %s veces la segunda (%s tiene %s veces sus trozos)" % (
                        _nu_texto(k), _u_nombre(letra), _nu_texto(k))
                else:
                    como = "a la primera le SUMO %s veces la segunda" % _nu_texto(_nu_opuesto(k))
                out.append({"op": "juntar", "i": i, "j": j, "letra": letra, "nueva": _bu_rel_de_trozos(c, suelto),
                            "trozos": (c, suelto), "como": como, "deja": len(c),
                            "coste": "coste_juntar" if k == _BU_UNO or _nu_iguales(k, _nu_opuesto(_BU_UNO), saber)
                            else "coste_juntar_veces",
                            "dice": "%s  y  %s" % (_u_rel_texto(rels[i]), _u_rel_texto(rels[j]))})
    return out


def _bu_sin_par(e):
    while e[0] == "par":
        e = e[1]
    return e


def _bu_cambiar_bloque(e, bloque, valor):
    """Cambia el bloque (un trozo del arbol, escrito igual) por el numero.  Devuelve (arbol, si lo cambio)."""
    if _bu_sin_par(e) == bloque:
        return ("num", valor), True
    if e[0] in ("num", "letra"):
        return e, False
    if e[0] in ("par", "neg"):
        dentro, si = _bu_cambiar_bloque(e[1], bloque, valor)
        return (e[0], dentro), si
    a, si1 = _bu_cambiar_bloque(e[2], bloque, valor)
    b, si2 = _bu_cambiar_bloque(e[3], bloque, valor)
    return ("op", e[1], a, b), si1 or si2


def _bu_bloques(rels, saber):
    """Un bloque que ya se sabe: un lado de una relacion (con dos letras o mas) vale un numero, y ese mismo bloque
    esta dentro de otra relacion (Polya: un problema auxiliar ya resuelto)."""
    out = []
    for j, rel in enumerate(rels):
        for lado, otro in ((rel[0], rel[1]), (rel[1], rel[0])):
            bloque = _bu_sin_par(lado)
            if _u_letras(otro) or len(_u_distintas(_u_letras(bloque))) == 1 or not _u_letras(bloque):
                continue
            try:
                valor = _u_valor(otro, saber, [])
            except (_UNoSale, KeyError):
                continue
            for i, r2 in enumerate(rels):
                if i == j:
                    continue
                a, si1 = _bu_cambiar_bloque(r2[0], bloque, valor)
                b, si2 = _bu_cambiar_bloque(r2[1], bloque, valor)
                if not (si1 or si2):
                    continue
                nueva = (a, b)
                if not _bu_menor(_bu_cuantas_letras(nueva), _bu_cuantas_letras(r2), saber):
                    continue
                out.append({"op": "reescribir", "i": i, "nueva": nueva, "deja": _bu_cuantas_letras(nueva),
                            "coste": "coste_reescribir",
                            "como": "el BLOQUE %s ya se sabe (%s): lo cambio por %s" % (
                                _u_texto(bloque), _u_rel_texto(rel), _nu_texto(valor)),
                            "dice": "el bloque %s = %s" % (_u_texto(bloque), _nu_texto(valor))})
    return out


def _bu_simplificar(rels, formas, saber):
    """Sacar factor comun: si todos los trozos y lo suelto se reparten justo entre el mismo numero, se reparte
    (como simplificar una fraccion, F.6).  Se prueba con el trozo mas pequeno y con 2, 3 y 5."""
    out = []
    for i, f in enumerate(formas):
        if f is None or len(f[0]) in (0, 1):
            continue
        cuantos = [v if v[0] == "+" else _nu_opuesto(v) for v in f[0].values()]
        suelto = f[1] if f[1][0] == "+" else _nu_opuesto(f[1])
        if any(x[2] != 1 for x in cuantos) or suelto[2] != 1:
            continue
        chico = cuantos[0][1]
        for x in cuantos:
            if _bu_menor(x[1], chico, saber):
                chico = x[1]
        for d in (chico, 2, 3, 5):
            if d == 1 or not _bu_menor(1, d, saber):
                continue
            if all(_bu_reparte(x[1], d, saber) for x in cuantos) and _bu_reparte(suelto[1], d, saber):
                dn = ("+", d, 1, "entero")
                try:
                    c, k = _bu_escalar(f, ":", dn, saber)
                except (_UNoSale, _NuNoSale, KeyError):
                    break
                nueva = _bu_rel_de_trozos(c, k)
                out.append({"op": "reescribir", "i": i, "nueva": nueva, "deja": len(c), "coste": "coste_reescribir",
                            "como": "saco FACTOR COMUN: todo se reparte entre %d, asi que %s es %d veces %s" % (
                                d, _u_rel_texto(rels[i]), d, _u_rel_texto(nueva)),
                            "dice": "factor comun %d" % d})
                break
    return out


def _bu_reparte(n, d, saber):
    if n == 0:
        return True
    try:
        _, resto = _nu_entre(n, d, saber)
    except (_NuNoSale, KeyError):
        return False
    return resto == 0


# ------------------------------------------------------------- el CONTROL: elegir por medios y fines

def _bu_elegir(cands, saber):
    """El que deja menos letras; si empatan, el que no pone una letra dividiendo o por otra; luego, el mas barato;
    si todo empata, el primero."""
    mejor = None
    for c in cands:
        c["cuesta"] = _bu_kn(saber, c["coste"], "5")
        c.setdefault("torcido", False)
        if mejor is None or _bu_menor(c["deja"], mejor["deja"], saber):
            mejor = c
        elif c["deja"] == mejor["deja"]:
            if mejor["torcido"] and not c["torcido"]:
                mejor = c
            elif c["torcido"] == mejor["torcido"] and _bu_menor(c["cuesta"], mejor["cuesta"], saber):
                mejor = c
    return mejor


def _bu_miro(cands, mejor, saber):
    """Una linea con lo que se miro: el mejor de cada operador, lo que deja y lo que cuesta."""
    vistos = []
    por_op = {}
    for c in cands:
        if c["op"] not in por_op:
            vistos.append(c["op"])
            por_op[c["op"]] = c
        elif _bu_menor(c["deja"], por_op[c["op"]]["deja"], saber):
            por_op[c["op"]] = c
    if not [o for o in vistos if o != mejor["op"] and por_op[o]["deja"] == mejor["deja"]]:
        return None                                      # no habia que decidir: lo mejor dejaba menos letras
    trozos = ["%s -> deja %d %s (coste %d)" % (_BU_NOMBRES[o], por_op[o]["deja"],
                                               "letra" if por_op[o]["deja"] == 1 else "letras",
                                               por_op[o]["cuesta"]) for o in vistos]
    return "MIRO lo que puedo hacer: %s.  ELIJO %s (deja menos letras; si empatan, lo mas barato)" % (
        ";  ".join(trozos), _BU_NOMBRES[mejor["op"]])


# ------------------------------------------------------------- el bucle

def _bu_resolver(rels, saber, etapas, originales, puede_probar=True):
    """Los operadores, elegidos por el control, hasta saberlo todo.  Devuelve la lista de soluciones ({letra: numero});
    una sola si no hizo falta probar en orden."""
    rels = list(rels)
    conocidas, aisladas = {}, []
    presupuesto, usados = _u_presupuesto(saber), 0
    while True:
        rels = _bu_sin_letras(rels, saber, etapas)
        if not rels:
            break
        usados = _u_siguiente(usados, saber)
        if viene_despues(decir(usados, saber), decir(presupuesto, saber), saber):
            raise _UNoSale("todavia_no", "llevo %d pasos y no llego (un humano no da tantas vueltas)" % presupuesto)
        cands = _bu_candidatos(rels, saber)
        if not cands:
            if not puede_probar:
                raise _UNoSale("todavia_no", "con lo que se, ninguna relacion baja las letras")
            return _bu_probar(rels, conocidas, aisladas, saber, etapas, originales)
        mejor = _bu_elegir(cands, saber)
        miro = _bu_miro(cands, mejor, saber)
        rels = _bu_hacer(mejor, rels, conocidas, aisladas, saber, etapas, miro)
    return [_bu_volver(conocidas, aisladas, saber, etapas)]


def _bu_sin_letras(rels, saber, etapas):
    """Las relaciones que ya no tienen letras se miran: si no son verdad, se contradicen (ninguna)."""
    quedan = []
    for rel in rels:
        if _u_letras_rel(rel):
            quedan.append(rel)
            continue
        pasos = []
        vi, vd = _u_valor(rel[0], saber, pasos), _u_valor(rel[1], saber, pasos)
        if not _nu_iguales(vi, vd, saber):
            etapas.append(("MIRO %s: ya no tiene letras" % _u_rel_texto(rel),
                           pasos + ["%s no es %s: las relaciones se contradicen" % (_nu_texto(vi), _nu_texto(vd))]))
            ex = _UNoSale("ninguna", "las relaciones se contradicen (%s = %s es falso): ningun numero las cumple"
                          % (_nu_texto(vi), _nu_texto(vd)))
            ex.corto = "%s da %s, no %s" % (_u_rel_texto(rel).split(" = ")[0], _nu_texto(vi), _nu_texto(vd))
            raise ex
        etapas.append(("MIRO %s: ya no tiene letras y es verdad; no dice nada nuevo" % _u_rel_texto(rel), []))
    return quedan


def _bu_hacer(c, rels, conocidas, aisladas, saber, etapas, miro):
    pre = [miro] if miro else []
    rel = rels[c["i"]]
    if c["op"] == "calcular":
        letra = c["letra"]
        pasos = []
        v = _u_despejar(rel, letra, saber, pasos)
        conocidas[letra] = v
        pre.extend(pasos)
        etapas.append(("CALCULO %s en %s (solo falta %s)" % (_u_nombre(letra), _u_rel_texto(rel), _u_nombre(letra)),
                       pre + ["%s = %s" % (_u_nombre(letra), _nu_texto(v))]))
        resto = [x for k, x in enumerate(rels) if k != c["i"]]
        return [(_u_poner(a, letra, ("num", v)), _u_poner(b, letra, ("num", v))) for a, b in resto]
    if c["op"] == "sustituir":
        letra, arbol = c["letra"], c["arbol"]
        resto = [x for k, x in enumerate(rels) if k != c["i"]]
        resto = [(_u_poner(a, letra, arbol), _u_poner(b, letra, arbol)) for a, b in resto]
        lineas = pre + ["%s = %s" % (_u_nombre(letra), _u_texto(arbol))]
        if resto:
            lineas.append("la pongo en las demas: %s" % ";  ".join(_u_rel_texto(x) for x in resto))
        etapas.append(("SUSTITUYO: en %s, %s %s" % (_u_rel_texto(rel), _u_nombre(letra),
                                                   "esta sola en un lado" if c["como"] == "sola"
                                                   else "sale una vez: la aislo deshaciendo"), lineas))
        aisladas.append((letra, arbol))
        return resto
    nuevas = list(rels)
    nuevas[c["i"]] = c["nueva"]
    if c["op"] == "juntar":
        otra = rels[c["j"]]
        fi, fj = _bu_rel_trozos(rel, saber), _bu_rel_trozos(otra, saber)
        lineas = pre + ["LAS BARRAS:",
                        "   %s   es   %s" % (_u_rel_texto(rel).ljust(22), _bu_barra(fi[0], fi[1], saber)),
                        "   %s   es   %s" % (_u_rel_texto(otra).ljust(22), _bu_barra(fj[0], fj[1], saber)),
                        "%s: queda %s" % (c["como"], _bu_barra(c["trozos"][0], c["trozos"][1], saber)),
                        "es decir: %s" % _u_rel_texto(c["nueva"])]
        etapas.append(("JUNTO dos relaciones: %s  y  %s (se va %s)" % (_u_rel_texto(rel), _u_rel_texto(otra),
                                                                       _u_nombre(c["letra"])), lineas))
    else:
        etapas.append(("REESCRIBO %s" % _u_rel_texto(rel),
                       pre + [c["como"], "queda: %s" % _u_rel_texto(c["nueva"])]))
    return nuevas


def _bu_volver(conocidas, aisladas, saber, etapas):
    """Se vuelve a lo aislado, con lo que ya se sabe."""
    conocidas = dict(conocidas)
    for letra, arbol in reversed(aisladas):
        faltan = [l for l in _u_distintas(_u_letras(arbol)) if l not in conocidas]
        if faltan:
            raise _UNoSale("todavia_no", "faltan relaciones: %s puede valer cualquier cosa (infinitas)"
                           % ", ".join(_u_nombre(l) for l in faltan))
        pasos = []
        v = _u_valor(_u_poner_todas(arbol, conocidas), saber, pasos)
        conocidas[letra] = v
        etapas.append(("VUELVO a %s = %s" % (_u_nombre(letra), _u_texto(arbol)),
                       pasos + ["%s = %s" % (_u_nombre(letra), _nu_texto(v))]))
    return conocidas


# ------------------------------------------------------------- operador 5: PROBAR EN ORDEN

def _bu_monotona(e):
    """Hecha solo de + y x (y de quitar o repartir un numero): con letras mas grandes, nunca sale mas pequena."""
    if e[0] == "num":
        return e[1][0] == "+" or _nu_es_cero(e[1])
    if e[0] == "letra":
        return True
    if e[0] == "par":
        return _bu_monotona(e[1])
    if e[0] == "neg":
        return False
    if e[1] in "+x":
        return _bu_monotona(e[2]) and _bu_monotona(e[3])
    if e[1] == "-":
        return _bu_monotona(e[2]) and not _u_letras(e[3])
    return _bu_monotona(e[2]) and e[3][0] == "num" and e[3][1][0] == "+" and not _nu_es_cero(e[3][1])


def _bu_solo_por(e):
    if e[0] in ("num", "letra"):
        return True
    if e[0] == "par":
        return _bu_solo_por(e[1])
    if e[0] == "neg":
        return False
    return e[1] in "x:" and _bu_solo_por(e[2]) and _bu_solo_por(e[3])


def _bu_topes(rels, saber):
    """Las relaciones que ponen tope: algo hecho de + y x = un numero.  [(con letras, el numero, solo por)]"""
    out = []
    for rel in rels:
        for lado, otro in ((rel[0], rel[1]), (rel[1], rel[0])):
            if _u_letras(lado) and not _u_letras(otro) and _bu_monotona(lado):
                try:
                    n = _u_valor(otro, saber, [])
                except (_UNoSale, KeyError):
                    continue
                out.append((lado, n, _bu_solo_por(lado) and not _nu_es_cero(n), rel))
    return out


def _bu_ya_me_paso(tope, letra, v, saber):
    """Con la letra = v y las DEMAS lo mas pequeno que pueden ser (0; o 1 si es un producto solo, que con un 0 daria 0
    y no N), ya se pasa de N?  Entonces con mas, se pasaria mas."""
    lado, n, solo_por, _ = tope
    minimo = ("+", 1, 1, "entero") if solo_por else _NU_CERO
    e = _u_poner(lado, letra, ("num", v))
    for l in _u_distintas(_u_letras(e)):
        e = _u_poner(e, l, ("num", minimo))
    otras = [l for l in _u_distintas(_u_letras(lado)) if l != letra]
    try:
        valor = _u_valor(e, saber, [])
    except (_UNoSale, KeyError):
        return True, "%s se pasa de mi techo" % _u_texto(lado)          # se pasa del techo: ya se pasa
    dice = "%s%s ya da %s, y se pasa de %s" % (
        "aunque %s fuera %s, " % (" y ".join(otras), _nu_texto(minimo)) if otras else "",
        _u_texto(lado), _nu_texto(valor), _nu_texto(n))
    return _bu_pasa(valor, n, saber), dice


def _bu_probar(rels, conocidas, aisladas, saber, etapas, originales):
    """Probar en orden, desde el 0, la letra que tiene un tope; en cada prueba se sigue con los otros operadores."""
    quedan = _u_distintas([l for rel in rels for l in _u_letras_rel(rel)])
    topes = _bu_topes(rels, saber)                       # el tope lo pone una de ahora o una de PARTIDA (tambien se cumplen)
    topes.extend(t for t in _bu_topes(originales, saber) if t[3] not in rels)
    letras = []
    for t in topes:
        for l in _u_distintas(_u_letras(t[0])):
            if l in quedan and l not in letras:
                letras.append(l)
    if not letras:
        raise _UNoSale("todavia_no", "nada baja las letras y ninguna relacion pone un TOPE para probar en orden "
                                     "(pueden ser infinitas, o falta otra relacion)")
    tope_de_pruebas = _bu_kn(saber, "tope_de_pruebas", "30")
    letra, de_quien, menos = None, None, None            # la que MENOS pruebas pide (S.3: la que mas pesa)
    for l in letras:
        n, t = _bu_cuantas_pruebas([t for t in topes if l in _u_letras(t[0])], l, tope_de_pruebas, saber)
        if menos is None or _bu_menor(n, menos, saber):
            letra, de_quien, menos = l, t, n
    mios = [t for t in topes if letra in _u_letras(t[0])]
    lineas = ["ninguna otra cosa baja las letras: PRUEBO EN ORDEN %s = 0, 1, 2 ... (numeros para contar)"
              % _u_nombre(letra),
              "EL TOPE lo pone %s: con %s mas grande nunca sale mas pequeno; cuando ya me pase, PARO"
              % (_u_rel_texto(de_quien[3]), _u_nombre(letra))]
    soluciones, hechas, v = [], 0, _NU_CERO
    while True:
        pasado = None
        for t in mios:
            si, e = _bu_ya_me_paso(t, letra, v, saber)
            if si:
                pasado = (t, e)
                break
        if pasado:
            lineas.append("%s = %s: %s (con mas, se pasaria mas): PARO" % (_u_nombre(letra), _nu_texto(v), pasado[1]))
            break
        hechas = _u_siguiente(hechas, saber)
        if viene_despues(decir(hechas, saber), decir(tope_de_pruebas, saber), saber):
            raise _UNoSale("todavia_no", "harian falta mas de %d pruebas y un humano no prueba tantas una a una"
                           % tope_de_pruebas)
        lineas.append(_bu_una_prueba(rels, letra, v, conocidas, aisladas, saber, originales, soluciones))
        v = _u_cuenta("+", v, _BU_UNO, saber, [])
    etapas.append(("PRUEBO EN ORDEN (NCETM 1.31, punto 5): %d pruebas" % hechas, lineas))
    return soluciones


def _bu_cuantas_pruebas(mios, letra, tope, saber):
    """Cuantas pruebas pide la letra: desde el 0 hasta que un tope dice que ya se pasa (o mas que el tope humano)."""
    n, v = 0, _NU_CERO
    while not viene_despues(decir(n, saber), decir(tope, saber), saber):
        for t in mios:
            if _bu_ya_me_paso(t, letra, v, saber)[0]:
                return n, t
        n = _u_siguiente(n, saber)
        v = _u_cuenta("+", v, _BU_UNO, saber, [])
    return n, mios[0]


def _bu_una_prueba(rels, letra, v, conocidas, aisladas, saber, originales, soluciones):
    prueba = "%s = %s" % (_u_nombre(letra), _nu_texto(v))
    sub = [(_u_poner(a, letra, ("num", v)), _u_poner(b, letra, ("num", v))) for a, b in rels]
    try:
        dentro = _bu_resolver(sub, saber, [], originales, puede_probar=False)[0]
    except _UNoSale as ex:
        if ex.conclusion in ("ninguna", "no_se_puede"):
            return "%s: %s ... NO" % (prueba, getattr(ex, "corto", ex.porque))
        raise _UNoSale("todavia_no", "con %s todavia no se sabe lo demas (%s): probar una letra no basta"
                       % (prueba, ex.porque))
    valores = dict(conocidas)
    valores[letra] = v
    valores.update(dentro)
    valores = _bu_volver(valores, aisladas, saber, [])
    otras = ", ".join("%s = %s" % (_u_nombre(l), _nu_texto(x)) for l, x in valores.items() if l != letra)
    lleva = "%s%s" % (prueba, " -> %s" % otras if otras else "")
    raros = [l for l, x in valores.items() if not _bu_para_contar(x)]
    if raros:
        return "%s ... NO VALE (%s no es un numero para contar)" % (lleva, ", ".join(_u_nombre(l) for l in raros))
    r = {}
    _u_comprobar({"relaciones": originales}, valores, saber, r)
    if not r["comprobacion_ok"]:
        return "%s ... NO" % lleva
    soluciones.append(valores)
    return "%s ... SI (cumple todas)" % lleva
