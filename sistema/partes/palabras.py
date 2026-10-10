# -*- coding: utf-8 -*-
"""
Euclides - EL LECTOR DE PALABRAS (fase U.3 del plan U, 8 oct 2026).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).  Prefijo _pa_.

U.1 lee lo que se escribe con SIMBOLOS y lo pone en el MODELO (cantidades, relaciones, lo que se pide); U.2 lo resuelve
buscando con control.  Aqui se lee lo que se escribe con PALABRAS y se pone en el MISMO modelo, como STUDENT (Bobrow
1964) y ROBUST (Bakman 2007): el enunciado se parte en frases NUCLEO y cada una da proposiciones pequenas.

    'Un lapiz y una goma cuestan 12 pesos'      ->  lapiz + goma = 12          (juntar: parte + parte = todo)
    'El lapiz cuesta el doble que la goma'      ->  lapiz = 2 x goma           (comparar multiplicando)
    'Cuanto cuesta la goma?'                    ->  se pide: goma               (la pregunta es una frase mas)

El VOCABULARIO esta en conocimiento/frases.kn y las ESTRUCTURAS (parte-todo, cambio, comparar, grupos iguales, las
figuras, 'consecutivos'...) en conocimiento/relaciones.kn: aqui solo esta la GRAMATICA que los recorre (sujeto, verbo,
dato; la elipsis; la pregunta).  Leer no es elegir la operacion: las palabras dan RELACIONES y la cuenta la elige el
buscador.  Lo que sobra no estorba (solo pasa lo conectado con la pregunta); una frase que no se entiende se dice.
"""

import re


class _PaNo(Exception):
    """Una frase nucleo que no se deja leer (con el porque)."""


_PA_TILDES = str.maketrans("áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN")
_PA_SINTAXIS = ("de", "del", "que", "y", "en", "con", "a", "al", "o")     # las palabras de la gramatica (no son datos)
_PA_LUGAR = ("en", "sobre", "dentro", "bajo")
_PA_LETRAS = ("n", "m", "p", "q", "r", "s", "t")                        # los nombres de los numeros sin nombre
_PA_ESTRUCTURA_DE = {"+": "cambio_gana", "-": "cambio_pierde"}
_PA_EXISTIR = ("hay", "salen", "hacen falta", "caben", "cabe", "habia")

# las clases de palabras: (clave de frases.kn, clase, lo que lleva)
_PA_LISTAS = (
    ("articulos", "art", None), ("posesivos", "su", None), ("relleno", "relleno", None), ("iguales", "relleno", None),
    ("verbos_valor", "verbo", {"tipo": "valor"}), ("verbos_valor_pasado", "verbo", {"tipo": "valor", "tiempo": "inicio"}),
    ("verbos_quedan", "verbo", {"tipo": "valor", "tiempo": "final"}), ("verbos_toca", "verbo", {"tipo": "toca"}),
    ("verbos_quedan_le", "verbo", {"tipo": "valor", "tiempo": "final", "quien": "le"}),
    ("verbos_suman", "verbo", {"tipo": "suman"}), ("verbos_diferencia", "verbo", {"tipo": "diferencia"}),
    ("cambio_mas_de_alguien", "verbo", {"tipo": "cambio", "signo": "+", "quien": "alguien"}),
    ("cambio_mas_le", "verbo", {"tipo": "cambio", "signo": "+", "quien": "le"}),
    ("cambio_mas_de_algo", "verbo", {"tipo": "cambio", "signo": "+", "quien": "algo"}),
    ("cambio_menos_de_alguien", "verbo", {"tipo": "cambio", "signo": "-", "quien": "alguien"}),
    ("cambio_menos_de_algo", "verbo", {"tipo": "cambio", "signo": "-", "quien": "algo"}),
    ("verbos_compra", "verbo", {"tipo": "compra", "signo": "+", "quien": "alguien"}),
    ("verbos_dar", "verbo", {"tipo": "dar", "signo": "-", "quien": "alguien"}),
    ("verbos_pago_con", "verbo", {"tipo": "pago_con", "quien": "alguien"}),
    ("verbos_vuelta", "verbo", {"tipo": "vuelta", "quien": "le"}),
    ("verbos_paga", "verbo", {"tipo": "paga", "signo": "-", "quien": "alguien"}),
    ("verbos_reparte", "verbo", {"tipo": "reparte", "quien": "alguien"}),
    ("verbos_agrupa", "verbo", {"tipo": "agrupa", "quien": "alguien"}),
    ("juntos", "juntos", None), ("mas", "masmenos", "+"), ("menos", "masmenos", "-"), ("veces", "veces", None),
    ("cada", "cada", None), ("cada_uno", "cada_uno", None), ("momento_inicio", "momento", "inicio"),
    ("momento_final", "momento", "final"), ("momentos", "momento", None), ("preguntas", "preg", None),
    ("desconocidos", "algo", None), ("genericos", "generico", None), ("lo_de", "lo_de", None),
)
_PA_MAPAS = (("multiplicadores", "mult"), ("denominadores", "den"), ("operaciones", "op"), ("funciones", "func"),
             ("cual_de_un_grupo", "cual"))


# ------------------------------------------------------------- 0. el vocabulario (de los datos)

def _pa_lista(v):
    if isinstance(v, list):
        return [x.strip() for x in v if x.strip()]
    return [p.strip() for p in (v or "").replace("\n", " ").split(",") if p.strip()]


def _pa_vocabulario(saber):
    """frases.kn -> {frase (tupla de palabras): (clase, valor)}.  Una frase, UN sentido (si sale dos veces, error)."""
    cache = saber.get("_pa_vocabulario")
    if cache:
        return cache
    f = saber.get("frases") or {}
    frases = {}

    def poner(frase, clase, valor):
        clave = tuple(frase.split())
        if clave in frases and frases[clave] != (clase, valor):
            raise ValueError("frases.kn: '%s' tiene dos sentidos (una palabra, un sentido)" % frase)
        frases[clave] = (clase, valor)

    for clave, clase, valor in _PA_LISTAS:
        for fr in _pa_lista(f.get(clave)):
            v = dict(valor) if isinstance(valor, dict) else (fr if clase == "momento" and valor is None else valor)
            if isinstance(v, dict):
                v["palabra"] = fr
            poner(fr, clase, v)
    for clave, clase in _PA_MAPAS:
        for fr, v in (f.get(clave) or {}).items():
            poner(fr, clase, v)
    voc = {"frases": frases, "largo": max(len(k) for k in frases) if frases else 1,
           "al_reves": set(_pa_lista(f.get("al_reves"))), "unidades": set(_pa_lista(f.get("unidades"))),
           "sujeto_de_verbo": dict(f.get("sujeto_de_verbo") or {}), "palabras": set(),
           "orden_momentos": _pa_lista(f.get("momentos")), "negativos": set(_pa_lista(f.get("pueden_ser_negativos"))),
           "genericas": {k: set(_pa_lista(v)) for k, v in (f.get("cosas_genericas") or {}).items()},
           "mismas": dict(f.get("mismas_cosas") or {}), "de_cada": set(_pa_lista(f.get("verbos_de_cada"))),
           "cosa_del_verbo": {v: k for k, lista in (f.get("cosa_del_verbo") or {}).items() for v in _pa_lista(lista)}}
    for k in frases:
        voc["palabras"].update(k)
    saber["_pa_vocabulario"] = voc
    return voc


def _pa_relaciones(saber):
    """relaciones.kn: las estructuras, las figuras y las relaciones de palabras."""
    cache = saber.get("_pa_relaciones")
    if cache:
        return cache
    r = saber.get("relaciones") or {}
    figuras = []
    for fg in r.get("figuras") or []:
        otros = {}
        for par in _pa_lista(fg.get("otros_nombres")):
            a, _, b = par.partition("=")
            otros[a.strip()] = b.strip()
        pares = {}
        for par in _pa_lista(fg.get("pares")):              # 'lado=largo ancho': un lado / el otro (U.3b)
            a, _, b = par.partition("=")
            pares[a.strip()] = b.split()
        figuras.append({"nombre": fg["nombre"], "palabras": _pa_lista(fg.get("palabras")), "pares": pares,
                        "dimensiones": _pa_lista(fg.get("dimensiones")),
                        "medidas": _pa_lista(fg.get("medidas")), "otros": otros,
                        "formulas": [x.strip() for x in fg.get("formulas", "").split(";") if x.strip()],
                        "cuadradas": _pa_lista(fg.get("cuadradas")), "cubicas": _pa_lista(fg.get("cubicas"))})
    palabras = [{"nombre": p["nombre"], "palabras": _pa_lista(p.get("palabras")), "formula": p.get("formula", "")}
                for p in r.get("palabras") or []]
    medidas = [{"grande": set(_pa_lista(m.get("grande"))), "pequena": set(_pa_lista(m.get("pequena"))),
                "veces": escribir_cifras(cifras_de(str(m.get("veces"))))} for m in r.get("medidas") or []]
    out = {"estructuras": dict(r.get("estructuras") or {}), "figuras": figuras, "palabras": palabras,
           "medidas": medidas}
    saber["_pa_relaciones"] = out
    return out


def _pa_formula(texto):
    """'perimetro = 2 x largo + 2 x ancho' -> (izq, der), con el lector de U.1 (los nombres son cantidades)."""
    toks = []
    for w in texto.replace("(", " ( ").replace(")", " ) ").split():
        if w in ("+", "-", ":", "x"):
            toks.append(("op", w))
        elif w in ("(", ")", "="):
            toks.append((w, w))
        elif w[0].isdigit():
            toks.append(("num", w))
        else:
            toks.append(("letra", w))
    k = toks.index(("=", "="))
    return _u_arbol(toks[:k]), _u_arbol(toks[k + 1:])


def _pa_rellenar(e, roles):
    """Pone en cada nombre de la formula la cantidad que toca (un arbol); una lista se pone como una SUMA."""
    if e[0] == "letra" and e[1] in roles:
        v = roles[e[1]]
        return _pa_suma(v) if isinstance(v, list) else v
    if e[0] == "op" and e[1] == "+" and _pa_solo(e, "parte") and isinstance(roles.get("parte"), list):
        return _pa_suma(roles["parte"])
    if e[0] in ("par", "neg"):
        return (e[0], _pa_rellenar(e[1], roles))
    if e[0] == "op":
        return ("op", e[1], _pa_par(_pa_rellenar(e[2], roles)), _pa_par(_pa_rellenar(e[3], roles)))
    return e


def _pa_solo(e, nombre):
    if e[0] == "letra":
        return e[1] == nombre
    return e[0] == "op" and e[1] == "+" and _pa_solo(e[2], nombre) and _pa_solo(e[3], nombre)


def _pa_par(e):
    return e if e[0] in ("num", "letra", "par") else ("par", e)


def _pa_suma(lista):
    e = lista[0]
    for x in lista[1:]:
        e = ("op", "+", e, _pa_par(x))
    return e


def _pa_estructura(ctx, nombre, roles, frase):
    """Una ESTRUCTURA de relaciones.kn, rellena con las cantidades de esta frase."""
    izq, der = _pa_formula(ctx["rel"]["estructuras"][nombre])
    _pa_apuntar(ctx, _pa_rellenar(izq, roles), _pa_rellenar(der, roles), frase, nombre)


def _pa_apuntar(ctx, izq, der, frase, porque):
    ctx["rels"].append({"rel": (izq, der), "frase": frase, "porque": porque,
                        "unidad": ctx.get("unidad_frase") or ctx.get("unidad_heredada")})


# ------------------------------------------------------------- 1. preparar y partir

def _pa_normal(texto):
    t = texto.translate(_PA_TILDES).lower()
    t = re.sub(r"^\s*(problema|resolver)\s*:?\s*", "", t)
    return t.replace("−", "-").replace("¡", " ").replace("$", " $ ")


def _pa_personas(texto, voc, saber):
    """Las PERSONAS: los nombres con mayuscula que no son palabras del vocabulario (Ana, Luis)."""
    out = set()
    nombres = saber.get("_nombre_a_valor") or {}
    for w in re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+", texto):
        if not w[0].isupper():
            continue
        p = w.translate(_PA_TILDES).lower()
        if p in voc["palabras"] or p in _PA_SINTAXIS or p in nombres or p in ("hay", "cuanto", "si"):
            continue
        out.add(p)
    return out


def _pa_frases(texto):
    """Las frases (por . ? ! ;), cada una con si es PREGUNTA.  El punto de un decimal (4.50) no parte."""
    t = _pa_normal(texto)
    out, actual, pregunta = [], [], False
    for trozo in re.split(r"(\?|!|;|\.(?!\d)|¿)", t):
        if trozo == "¿":
            frase = " ".join("".join(actual).split()).strip(" ,")
            if frase:                                      # 'si 2 kilos cuestan 9, ¿cuanto...?': lo de antes es un hecho
                out.append((frase, False))
            actual, pregunta = [], True
            continue
        if trozo in ("?", "!", ";", "."):
            frase = " ".join("".join(actual).split())
            if frase:
                out.append((frase, pregunta or trozo == "?"))
            actual, pregunta = [], False
            continue
        actual.append(trozo)
    frase = " ".join("".join(actual).split())
    if frase:
        out.append((frase, pregunta))
    return out


def _pa_tokens(frase, voc, saber):
    """Las palabras de una frase, cada una con su CLASE (lo mas largo que este en el vocabulario primero)."""
    nombres = saber.get("_nombre_a_valor") or {}
    w = re.findall(r"-?\d+(?:[.,]\d+)?(?:/\d+)?|[a-z][a-z0-9]*|,|\?", frase.replace("$", " "))
    out = []
    while w:
        hecho = False
        for j in range(len(w[:voc["largo"]]), 0, -1):
            clave = tuple(w[:j])
            if clave in voc["frases"]:
                clase, valor = voc["frases"][clave]
                out.append((clase, valor, " ".join(clave)))
                w, hecho = w[j:], True
                break
        if hecho:
            continue
        for j in range(len(w[:6]), 0, -1):                     # los numeros dichos con palabras (6.1 / 6.7)
            trozo = " ".join(w[:j])
            v = 0 if trozo == "cero" else nombres.get(trozo)
            if v is not None:
                out.append(("num", ("+", v, 1, "entero"), trozo))
                w, hecho = w[j:], True
                break
        if hecho:
            continue
        p = w[0]
        if p[0].isdigit() or (p[0] == "-" and p[1:2].isdigit()):
            n = _nu_leer(p.lstrip("-"))
            out.append(("num", _nu_opuesto(n) if p.startswith("-") else n, p))
        elif p == ",":
            out.append((",", ",", ","))
        elif p in _PA_SINTAXIS:
            out.append((p if p != "del" else "de", p, p))
        else:
            out.append(("palabra", p, p))
        w = w[1:]
    out = _pa_juntar_tokens(out)
    for k, t in enumerate(out):                       # 'mas BAJA que': detras de mas/menos es un adjetivo, no un verbo
        if t[0] == "verbo" and k and out[k - 1][0] == "masmenos" and t[2] in voc["al_reves"]:
            out[k] = ("palabra", t[2], t[2])
    return out


def _pa_juntar_tokens(toks):
    """Lo que va pegado: 'menos 2' (grados) es -2; '2 tercios' es 2/3; 'un tercio' es 1/3; 'lo que cuesta' se salta."""
    out, i = [], 0
    while i < len(toks):
        t = toks[i]
        sig = toks[i + 1] if i + 1 < len(toks) else None
        if t[0] == "masmenos" and t[1] == "-" and sig and sig[0] == "num" and (not out or out[-1][0] == "verbo"):
            out.append(("num", _nu_opuesto(sig[1]), "menos " + sig[2]))
            i += 2
            continue
        if t[0] in ("num", "art") and sig and sig[0] == "den" and (t[0] == "num" or t[2] in ("un", "una")):
            arriba = t[1][1] if t[0] == "num" else 1
            out.append(("num", ("+", arriba, escribir_cifras(cifras_de(sig[1])), "fraccion"), "%s %s" % (t[2], sig[2])))
            i += 2
            continue
        if t[0] == "relleno" and t[2] in ("lo que", "de lo que"):
            if t[2] == "de lo que" and out and out[-1][0] in ("mult", "num"):
                out.append(("de", "de", "de"))
                k = i + 1
                if sig and sig[0] == "verbo" and k + 1 < len(toks) and toks[k + 1][0] == "verbo":
                    k = k + 1                              # 'de lo que habia BAJADO': el verbo es el segundo
                if k < len(toks) and toks[k][0] == "verbo":    # U.3b: 'la mitad de lo que TENIA' (lo de antes)
                    out.append(("lo_que", toks[k][1], "lo que " + toks[k][2]))
                    i = k + 1
                    continue
            if sig and sig[0] == "verbo":
                i += 1                                     # 'el doble de lo que CUESTA la goma': ese verbo no es el de la frase
            i += 1
            continue
        out.append(t)
        i += 1
    return out


# ------------------------------------------------------------- 2. las frases nucleo

def _pa_verbo(toks):
    """El verbo de la frase: el primero."""
    for k, t in enumerate(toks):
        if t[0] == "verbo":
            return k
    return None


def _pa_hay_dato(toks):
    return any(t[0] in ("num", "pide", "algo", "mult", "verbo") for t in toks)


def _pa_nucleos(toks):
    """Parte por 'y' y por la coma DESPUES del verbo, cuando el trozo de la derecha trae un dato.  Lo de 'la suma de A
    y B' no se parte (la funcion se lleva su 'y')."""
    v = _pa_verbo(toks)
    if v is None:
        return [toks]
    cortes, pendientes = [], 0
    for k in range(v + 1, len(toks)):
        t = toks[k]
        if t[0] == "func":
            pendientes = pendientes + 1
        elif t[0] in ("y", ",") or (t[0] == "relleno" and t[2].startswith("y ")):     # 'y luego'
            if pendientes:
                pendientes = pendientes - 1
                continue
            if _pa_hay_dato(toks[k + 1:]) and _pa_hay_dato(toks[v + 1:k]):
                cortes.append(k)
    out, desde = [], 0
    for k in cortes:
        out.append(toks[desde:k])
        desde = k + 1
    out.append(toks[desde:])
    return [x for x in out if x]


def _pa_pregunta(toks):
    """La pregunta es una frase mas, con '?' donde va lo que se busca:  'cuanto cuesta la goma' -> 'la goma cuesta ?'."""
    k = next((i for i, t in enumerate(toks) if t[0] == "preg"), None)
    if k is None:
        raise _PaNo("no se que se pregunta")
    preg = toks[k][2]
    v = _pa_verbo(toks)
    if v is None or v < k:
        raise _PaNo("en la pregunta no encuentro el verbo")
    medio, resto = toks[k + 1:v], toks[v + 1:]
    if preg in ("cual", "cuales", "que numero", "que numeros"):
        if not resto and preg in ("cuales", "que numeros"):
            resto = [("generico", None, "numeros")]            # 'cuales son?': los del grupo
        return resto, toks[v], [("pide", None, "?")] + medio
    q = next((i for i, t in enumerate(resto) if t[0] == "que"), None)
    sujeto, cola = (resto, []) if q is None else (resto[:q], resto[q:])
    objeto = [("pide", None, "?")]
    objeto.extend(medio)
    objeto.extend(cola)
    return sujeto, toks[v], objeto


# ------------------------------------------------------------- 3. las cantidades (el registro de lo que se nombra)

def _pa_singular(w):
    if len(w) > 4 and w.endswith("ces"):
        return w[:-3] + "z"
    if len(w) > 4 and w.endswith("es") and w[-3] not in "aeiou":
        return w[:-2]
    if len(w) > 3 and w.endswith("s"):
        return w[:-1]
    return w


def _pa_nuevo_ente(ctx, clave, tipo, nombre, persona=False):
    e = {"clave": clave, "tipo": tipo, "nombre": nombre, "persona": persona, "versiones": [nombre], "momentos": {},
         "unidad": None}
    ctx["entes"].append(e)
    ctx["nombres"].add(nombre)
    return e


def _pa_libre(ctx, base):
    nombre, k = base, 1
    while nombre in ctx["nombres"]:
        k = k + 1
        nombre = "%s_%d" % (base, k)
    return nombre


def _pa_buscar_ente(ctx, palabras, tipo=None):
    """La cantidad que ya se nombro con esas palabras (singular o plural; 'la roja' es 'la cuerda roja')."""
    clave = set(_pa_singular(w) for w in palabras)
    for e in reversed(ctx["entes"]):
        if (tipo and e["tipo"] != tipo) or e.get("dueno"):
            continue
        if clave and (clave <= set(e["clave"]) or set(palabras) <= set(e["clave"])):
            return e
    return None


def _pa_ente(ctx, palabras, tipo="uno", crear=True):
    """Las palabras de una cosa -> su cantidad (la busca; si no esta, la crea)."""
    palabras = [w for w in palabras if w not in ("iguales", "igual")]
    if not palabras:
        raise _PaNo("falta de que cosa se habla")
    fig = _pa_medida(ctx, palabras)
    if fig:
        return fig
    e = _pa_buscar_ente(ctx, palabras, tipo)
    if e is None and tipo == "uno":                   # 'la azul' (uno), 'el numero': no una cuenta ('cajas')
        e = next((x for x in [_pa_buscar_ente(ctx, palabras, t) for t in ("numero", "medida")] if x), None)
    if e:
        return e
    if not crear:
        return None
    clave = tuple(_pa_singular(w) for w in palabras)
    persona = len(palabras) == 1 and palabras[0] in ctx["personas"]
    if persona:
        clave = tuple(palabras)                       # 'Luis' no es el plural de nada
    base = "_".join(palabras) if tipo == "cuenta" else "_".join(clave)
    return _pa_nuevo_ente(ctx, clave, tipo, _pa_libre(ctx, base), persona)


def _pa_medida(ctx, palabras):
    """'largo', 'el perimetro', 'su area' de una figura que ha salido -> la cantidad de esa medida.  'Un lado' del
    rectangulo es el primero de su pareja (relaciones.kn, 'pares'); 'el otro' sera el otro (U.3b)."""
    for fg in ctx["figuras"]:
        for w in palabras:
            m = fg["otros"].get(w, w)
            if m in fg["pares"]:
                cual = fg["pares"][m][0]
                ctx["par_ultimo"] = (fg, m, cual)
                return _pa_medida_de(ctx, fg, cual)
            if m in fg["medidas"]:
                return _pa_medida_de(ctx, fg, m)
    return None


def _pa_medida_de(ctx, fg, m):
    e = _pa_buscar_ente(ctx, [m], "medida")
    if e:
        return e
    e = _pa_nuevo_ente(ctx, (m,), "medida", _pa_libre(ctx, m))
    e["figura"] = fg
    ctx["figuras_usadas"].append(fg) if fg not in ctx["figuras_usadas"] else None
    return e


def _pa_version(ctx, e, tiempo):
    """El nombre de la cantidad en ese momento: al principio (la 0), al final (se decide al acabar), uno con nombre
    ('por la manana': una version para cada momento) o la de ahora mismo en la historia."""
    if tiempo == "inicio":
        return e["versiones"][0]
    if tiempo == "final":
        return "\x00final\x00" + e["nombre"]
    if tiempo:
        if tiempo not in e["momentos"]:
            if e["momentos"]:
                _pa_otra_version(ctx, e)
            e["momentos"][tiempo] = len(e["versiones"]) - 1
            ctx["que_es"][e["versiones"][-1]] = "%s %s" % (e["nombre"].replace("_", " "), tiempo)
        return e["versiones"][e["momentos"][tiempo]]
    return e["versiones"][-1]


def _pa_otra_version(ctx, e):
    nombre = _pa_libre(ctx, "%s_%d" % (e["nombre"], len(e["versiones"])))
    e["versiones"].append(nombre)
    ctx["nombres"].add(nombre)
    return nombre


def _pa_letra(ctx, e, tiempo=None, exacto=False):
    """La letra de una cantidad.  Si no es 'exacto', primero se mira DE QUE COSA es en esta frase (U.3b): Maria con
    lapices y Maria con anos son dos cantidades."""
    if not exacto:
        e = _pa_de_cosa(ctx, e, ctx.get("cosa_frase"))
    raiz = e.get("dueno") or e
    ctx["ultimo"] = raiz
    if raiz["persona"]:
        ctx["ultima_persona"] = raiz
    ctx["mencionados"].append(raiz)
    return ("letra", _pa_version(ctx, e, tiempo))


# ------------------------------------------------------------- 3b. la COSA de cada cantidad (U.3b)

def _pa_cosa(ctx, palabras):
    """Las palabras de una cosa -> su forma comun: en singular, y las que son la misma ('kg' = 'kilo'; frases.kn)."""
    mismas = ctx["voc"]["mismas"]
    out = []
    for w in palabras:
        s = _pa_singular(mismas.get(w, w))
        out.append(mismas.get(s, s))
    return tuple(out)


def _pa_misma_cosa(ctx, a, b):
    """Dos cosas son la misma si las palabras de una estan en la otra ('kilos' y 'kilos de manzanas'), o si una es una
    palabra GENERICA de la clase de la otra ('dinero' y 'pesos'; frases.kn)."""
    if set(a) <= set(b) or set(b) <= set(a):
        return True
    gen = ctx["voc"]["genericas"]
    for x, y in ((a, b), (b, a)):
        if len(x) == 1 and x[0] in gen and set(y) & gen[x[0]]:
            return True
    return False


def _pa_es_generica(ctx, c):
    return len(c) == 1 and c[0] in ctx["voc"]["genericas"]


def _pa_cosa_de_toks(toks, ctx):
    """La cosa de un dato: las palabras que van detras del primer numero ('15 lapices', '2 kilos de manzanas'), o del
    '?' ('cuantos lapices').  Lo que va detras de 'de' si es una medida de una figura ('8 cm de largo') no es la cosa."""
    for k, t in enumerate(toks):
        if t[0] not in ("num", "pide", "algo"):
            continue
        palabras, j = [], k + 1
        while j < len(toks) and (toks[j][0] == "palabra" or (
                toks[j][0] == "de" and palabras and j + 1 < len(toks) and toks[j + 1][0] == "palabra"
                and not _pa_es_medida(ctx, [toks[j + 1][2]]))):
            if toks[j][0] == "palabra":
                palabras.append(toks[j][2])
            j = j + 1
        return _pa_cosa(ctx, palabras) if palabras else None
    return None


def _pa_de_cosa(ctx, e, cosa):
    """La cantidad (de quien, de que cosa).  La primera cosa de alguien se queda con su nombre ('maria'); otra cosa
    distinta es OTRA cantidad ('maria_lapiz').  Sin cosa: si tiene varias, no se adivina."""
    if e["tipo"] != "uno":
        return e
    raiz = e.get("dueno") or e
    familia = [raiz]
    familia.extend(raiz.get("hijos", []))
    if cosa is None:
        if e is not raiz or len(familia) == 1:
            return e
        raise _PaNo("%s tiene varias cosas (%s): no se de cual se habla" % (
            raiz["nombre"], ", ".join(" ".join(x["cosa"]) for x in familia if x.get("cosa"))))
    iguales = [x for x in familia if x.get("cosa") and _pa_misma_cosa(ctx, x["cosa"], cosa)]
    if len(iguales) > 1:
        raise _PaNo("'%s' de %s: hay varias cosas asi" % (" ".join(cosa), raiz["nombre"]))
    if iguales:
        x = iguales[0]
        if _pa_es_generica(ctx, x["cosa"]) and not _pa_es_generica(ctx, cosa):
            x["cosa"] = cosa                          # 'dinero' -> 'pesos'
        return x
    if raiz.get("cosa") is None:
        raiz["cosa"] = cosa
        return raiz
    hijo = _pa_nuevo_ente(ctx, raiz["clave"], "uno", _pa_libre(ctx, "%s_%s" % (raiz["nombre"], "_".join(cosa))))
    hijo["dueno"], hijo["cosa"] = raiz, cosa
    raiz.setdefault("hijos", []).append(hijo)
    return hijo


def _pa_cosa_de_arbol(e, cosas, ctx):
    """La cosa de un lado de una relacion (Schwartz 1988): sumar y restar CONSERVAN la cosa (las dos tienen que ser la
    misma); multiplicar por un numero la conserva; multiplicar o dividir dos cantidades la TRANSFORMA (no se mira).
    Devuelve (cosa o None, el choque o None)."""
    if e[0] == "letra":
        return cosas.get(e[1]), None
    if e[0] == "num":
        return None, None
    if e[0] in ("par", "neg"):
        return _pa_cosa_de_arbol(e[1], cosas, ctx)
    a, ch = _pa_cosa_de_arbol(e[2], cosas, ctx)
    if ch:
        return None, ch
    b, ch = _pa_cosa_de_arbol(e[3], cosas, ctx)
    if ch:
        return None, ch
    if e[1] in ("+", "-"):
        if a and b and not _pa_misma_cosa(ctx, a, b):
            return None, (a, b)
        return a or b, None
    if e[1] == "x" and (e[2][0] == "num" or e[3][0] == "num"):
        return a or b, None
    return None, None


def _pa_cosas_de_letras(ctx):
    cosas = dict(ctx["cosa_pedido"])
    for e in ctx["entes"]:
        if e.get("cosa"):
            for v in e["versiones"]:
                cosas[v] = e["cosa"]
    return cosas


def _pa_comprobar_cosas(ctx, rels):
    """CAPA 4 con las cosas: una relacion que suma, resta o iguala cosas distintas ('8 anos + 6 canicas') junta lo que
    no se junta; algo se leyo mal: mejor no entender que dar una respuesta falsa."""
    cosas = _pa_cosas_de_letras(ctx)
    for r in rels:
        if r.get("sabido") and r["porque"] == "medida":    # M.23: 1 km = 1000 m cambia de unidad a proposito
            continue
        izq, der = r["rel"]
        a, ch = _pa_cosa_de_arbol(izq, cosas, ctx)
        if ch is None:
            b, ch = _pa_cosa_de_arbol(der, cosas, ctx)
            if ch is None and a and b and not _pa_misma_cosa(ctx, a, b):
                ch = (a, b)
        if ch:
            raise ValueError("'%s' junta cosas distintas (%s con %s): eso no se suma ni se iguala"
                             % (_u_rel_texto(r["rel"]), " ".join(ch[0]), " ".join(ch[1])))


def _pa_medida_compuesta(ctx, rels):
    """M.23 (prudencia): si la misma cosa se da con NUMERO en dos unidades ('la cuerda mide 3 m y 25 cm'), no son dos
    medidas que tengan que cuadrar (1 m = 100 cm): es UNA medida compuesta (3 m + 25 cm) o algo mal leido.  Todavia no
    se juntan: mejor no entender que dar una respuesta falsa ('25 cm' o 'ninguna')."""
    dadas = set()
    for r in ctx["rels"]:
        if r.get("sabido"):
            continue
        izq, der = r["rel"]
        for a, b in ((izq, der), (der, izq)):
            if a[0] == "letra" and not _pa_hay_letra(b):
                dadas.add(a[1])
    for r in rels:
        if r.get("sabido") and r["porque"] == "medida" and set(_u_letras_rel(r["rel"])) <= dadas:
            raise ValueError("'%s': la misma cosa se da en dos unidades, con un numero en cada una (una medida "
                             "compuesta, como 3 m y 25 cm?): todavia no las junto" % r["frase"])


def _pa_hay_letra(e):
    if e[0] == "letra":
        return True
    if e[0] in ("par", "neg"):
        return _pa_hay_letra(e[1])
    return e[0] == "op" and (_pa_hay_letra(e[2]) or _pa_hay_letra(e[3]))


def _pa_incognita(ctx, base):
    nombre = _pa_libre(ctx, base)
    ctx["nombres"].add(nombre)
    ctx["incognitas"].append(nombre)
    return ("letra", nombre)


def _pa_pedido(ctx):
    """El '?' de la pregunta: una cantidad nueva que es lo que se pide."""
    nombre = _pa_libre(ctx, "lo_pedido")
    ctx["nombres"].add(nombre)
    ctx["pide"].append(nombre)
    if ctx.get("cosa_frase"):
        ctx["cosa_pedido"][nombre] = ctx["cosa_frase"]
    return ("letra", nombre)


# ------------------------------------------------------------- 4. leer un trozo: las expresiones de STUDENT

def _pa_trozos_por_y(toks):
    """'Ana y Luis', 'A, B y C': los de un sujeto.  La 'y' de 'la suma de A y B' se la lleva la funcion."""
    out, actual, pendientes = [], [], 0
    for t in toks:
        if t[0] == "func":
            pendientes = pendientes + 1
        if t[0] in ("y", ",") and not pendientes:
            out.append(actual)
            actual = []
            continue
        if t[0] == "y" and pendientes:
            pendientes = pendientes - 1
        actual.append(t)
    out.append(actual)
    return [x for x in out if x]


def _pa_expresion(toks, ctx, lado="sujeto"):
    """Un trozo -> un arbol.  Lo de STUDENT: 'el doble de un numero mas 3', 'la suma de A y B', 'su mitad', '4 cajas'."""
    quedan = [t for t in toks if not (t[0] == "relleno" or (t[0] == "a" and t is toks[0]))]

    def ver(k=0):
        return quedan[k] if k < len(quedan) else (None, None, None)

    def tomar():
        return quedan.pop(0)

    def suma():
        e = producto()
        while ver()[0] == "masmenos" and ver(1)[0] not in (None, "que"):
            op = tomar()[1]
            e = ("op", op, e, _pa_par(producto()))
        return e

    def producto():
        e = factor()
        while ver()[0] == "op":
            op = tomar()[1]
            e = ("op", op, _pa_par(e), _pa_par(factor()))
        return e

    def factor():
        t = ver()
        if t[0] is None:
            raise _PaNo("falta algo al final")
        if t[0] == "mult" or (t[0] == "art" and ver(1)[0] == "mult"):
            if t[0] == "art":
                tomar()
            m = _nu_leer(tomar()[1])
            if ver()[0] == "de":
                tomar()
                return ("op", "x", ("num", m), _pa_par(factor()))
            raise _PaNo("'%s' de que?" % t[2])
        if t[0] == "su":
            tomar()
            return lo_suyo()
        if t[0] == "func" or (t[0] == "art" and ver(1)[0] == "func"):
            if t[0] == "art":
                tomar()
            return funcion(tomar()[1])
        if t[0] == "lo_que":                               # 'de lo que pesa la maleta' / 'de lo que tenia'
            tomar()
            return factor() if quedan else _pa_lo_que(ctx, t[1])
        if t[0] == "num":
            tomar()
            n = ("num", t[1])
            if ver()[0] == "veces":
                tomar()
                if ver()[0] in (None, "masmenos", "que"):
                    raise _PaNo("%s veces que?" % t[2])
                return ("op", "x", n, _pa_par(factor()))
            if ver()[0] == "de" and t[1][3] in ("fraccion", "decimal"):
                tomar()
                return ("op", "x", n, _pa_par(factor()))
            if ver()[0] == "palabra":
                palabras = nombre()                        # '4 kilos de manzanas'
                e = _pa_por_unidad(ctx, palabras)
                if e is None and lado == "sujeto" and ctx["de_cada"] and not _pa_es_medida(ctx, palabras):
                    e = _pa_ente(ctx, [_pa_singular(w) for w in palabras])   # '3 cuadernos cuestan 12' (U.3b):
                    e["por_unidad"] = True                                   # 3 x lo de un cuaderno
                if e is not None and lado == "sujeto":
                    return ("op", "x", n, _pa_letra(ctx, e))       # '4 cajas' (cada caja pesa 5): 4 x caja
                _pa_unidad(ctx, palabras)
            return n
        if t[0] == "pide":
            tomar()
            return _pa_pedido(ctx)
        if t[0] == "algo":
            tomar()
            return _pa_incognita(ctx, "algunos")
        return cosa()

    def funcion(op):
        """'la suma de A y B', 'su producto' (de los de un grupo)."""
        miembros = []
        if ver()[0] == "de":
            tomar()
        resto = list(quedan)
        del quedan[:]
        partes = _pa_trozos_por_y(resto)
        if len(partes) > 1:
            for p in partes:
                miembros.append(_pa_expresion(p, ctx, lado))
        else:
            grupo = _pa_grupo_de(ctx, resto)
            miembros = [_pa_letra(ctx, e) for e in grupo]
        return _pa_operar(op, miembros)

    def lo_suyo():
        """'su doble', 'su mitad' (del ultimo que se nombro); 'su perimetro'; 'su suma' (la de un grupo)."""
        t = ver()
        if t[0] == "mult":
            tomar()
            if ctx["ultimo"] is None:
                raise _PaNo("'su' de quien?")
            return ("op", "x", ("num", _nu_leer(t[1])), _pa_letra(ctx, ctx["ultimo"]))
        if t[0] == "func":
            tomar()
            grupo = ctx["grupo"] or []
            if len(grupo) < 2:
                raise _PaNo("'su %s' de quienes?" % t[2])
            return _pa_operar(t[1], [_pa_letra(ctx, e) for e in grupo])
        return cosa()

    def nombre():
        """Las palabras de un nombre: 'la cuerda roja', 'un kilo de manzanas', 'el largo del rectangulo'."""
        palabras = []
        while ver()[0] == "palabra" or (ver()[0] == "de" and palabras and (
                ver(1)[0] == "palabra" or (ver(1)[0] == "art" and _pa_es_medida(ctx, palabras)))):
            if ver()[0] == "de":
                tomar()
                if ver()[0] == "art":
                    tomar()
                if _pa_es_medida(ctx, palabras):
                    continue                              # 'el largo DEL rectangulo': la medida es 'largo'
                if ver()[0] == "palabra" and _pa_es_medida(ctx, [ver()[2]]):
                    break
                continue
            palabras.append(tomar()[2])
        if palabras and _pa_es_medida(ctx, palabras[:1]):
            return palabras[:1]
        return palabras

    def de_n(e):
        """'X de N unidades [de MEDIDA]': lo que vale X (o una medida suya), dicho pegado al nombre."""
        tomar()
        n = ("num", tomar()[1])
        uni = []
        while ver()[0] == "palabra":
            uni.append(tomar()[2])
        destino = e
        if ver()[0] == "de" and ver(1)[0] == "palabra" and _pa_es_medida(ctx, [ver(1)[2]]):
            tomar()
            destino = _pa_medida(ctx, [tomar()[2]])
        if uni:
            ctx["unidad_de"][destino["versiones"][0]] = " ".join(uni)
        ctx["rels"].append({"rel": (("letra", destino["versiones"][0]), n), "frase": ctx["frase"],
                            "porque": "medida" if destino is not e else "valor", "unidad": " ".join(uni) or None})
        if destino is e:
            e["por_unidad"] = True

    def cosa():
        """Una cosa con nombre ('el lapiz', 'la cuerda roja', 'Ana', 'un numero', 'el otro', 'cada caja')."""
        while ver()[0] == "lo_de":                    # 'la edad de Juan' es Juan
            tomar()
        t = ver()
        nuevo = False
        cada = False
        if t[0] == "cada":
            tomar()
            cada = True
        if ver()[0] == "art":
            nuevo = ver()[2] in ("un", "una", "unos", "unas")
            tomar()
        t = ver()
        if t[0] == "cual" and t[2] in ("otro", "otra", "el otro", "la otra") and ctx["par_ultimo"] and (
                ver(1)[0] is None or (ver(1)[0] == "palabra" and ver(1)[2] in ctx["par_ultimo"][0]["pares"])):
            tomar()                                       # 'el otro (lado)' del rectangulo: el otro de la pareja
            if ver()[0] == "palabra":
                tomar()
            fg, m, cual = ctx["par_ultimo"]
            otro = [x for x in fg["pares"][m] if x != cual][0]
            return _pa_letra(ctx, _pa_medida_de(ctx, fg, otro))
        if t[0] == "cual":
            tomar()
            if ver()[0] == "generico":
                tomar()
                return _pa_letra(ctx, _pa_numero_nuevo(ctx))
            numeros = ctx["grupo"] or [x for x in ctx["entes"] if x["tipo"] == "numero"]
            if t[2] in ("otro", "otra") and len(numeros) == 1:      # 'un numero es 5 veces OTRO': uno nuevo
                return _pa_letra(ctx, _pa_numero_nuevo(ctx))
            return _pa_letra(ctx, _pa_del_grupo(ctx, int(t[1])))
        if t[0] == "generico":
            tomar()
            if ver()[0] == "cual" and ver()[2] in ("otro", "otra"):
                tomar()
                nuevo = True
            if nuevo:
                return _pa_letra(ctx, _pa_numero_nuevo(ctx))
            e = _pa_buscar_ente(ctx, ["numero"], "numero") if not ctx["grupo"] else ctx["grupo"][0]
            if e is None:
                e = _pa_numero_nuevo(ctx)
            return _pa_letra(ctx, e)
        palabras = nombre()
        if not palabras:
            raise _PaNo("no entiendo '%s'" % (t[2] or ""))
        e = _pa_ente(ctx, palabras)
        if ver()[0] == "de" and ver(1)[0] == "num":       # 'una caja de 60 cm cubicos de volumen', 'un libro de 9 pesos'
            de_n(e)
        if cada:
            ctx["tasa_frase"] = e
        if nuevo and not e["persona"] and e["tipo"] == "uno":
            e["por_unidad"] = True                       # 'un cuaderno cuesta 3': lo de CADA cuaderno
        return _pa_letra(ctx, e)

    e = suma()
    if quedan:
        raise _PaNo("sobra '%s'" % " ".join(t[2] for t in quedan))
    return e


def _pa_es_medida(ctx, palabras):
    return any(fg["otros"].get(w, w) in fg["medidas"] or w in fg["pares"] for fg in ctx["figuras"] for w in palabras)


def _pa_operar(op, miembros):
    if len(miembros) < 2:
        raise _PaNo("hacen falta dos para operar")
    e = miembros[0]
    for m in miembros[1:]:
        e = ("op", op, _pa_par(e), _pa_par(m))
    return e


def _pa_por_unidad(ctx, palabras):
    """'cajas' cuando ya se sabe lo que vale CADA caja: 4 cajas es 4 x caja."""
    clave = set(_pa_singular(w) for w in palabras)
    for e in reversed(ctx["entes"]):
        if e["tipo"] == "uno" and e.get("por_unidad") and clave == set(e["clave"]):
            return e
    mas = [e for e in ctx["entes"] if e["tipo"] == "uno" and e.get("por_unidad") and not e.get("dueno")
           and clave and clave < set(e["clave"])]
    return mas[0] if len(mas) == 1 else None             # '8 kilos' (de manzanas, que es lo unico por kilo)


def _pa_unidad(ctx, palabras):
    u = " ".join(palabras)
    if ctx.get("unidad_frase") is None:
        ctx["unidad_frase"] = u


def _pa_numero_nuevo(ctx):
    usados = [e for e in ctx["entes"] if e["tipo"] == "numero"]
    base = _PA_LETRAS[len(usados)] if len(usados) < len(_PA_LETRAS) else "numero"
    return _pa_nuevo_ente(ctx, ("numero",), "numero", _pa_libre(ctx, base))


def _pa_del_grupo(ctx, k):
    grupo = ctx["grupo"] or [e for e in ctx["entes"] if e["tipo"] == "numero"]
    if len(grupo) < k:
        raise _PaNo("'el %s' de que grupo?" % ("otro" if k == 2 else "primero"))
    return grupo[k - 1]


def _pa_grupo_de(ctx, toks):
    """'los numeros', 'los dos', 'ellos': los de un grupo (o los dos ultimos que se nombraron)."""
    if ctx["grupo"]:
        return ctx["grupo"]
    vistos = []
    for e in reversed(ctx["mencionados"]):
        if e not in vistos and e["tipo"] != "medida":
            vistos.append(e)
    if len(vistos) < 2:
        raise _PaNo("'los dos' quienes?")
    return [vistos[1], vistos[0]]


# ------------------------------------------------------------- 5. una frase nucleo -> proposiciones

def _pa_nucleo(toks, ctx, pregunta, antes):
    """SUJETO VERBO OBJETO -> relaciones.  'antes' es el nucleo anterior de la misma frase (para la elipsis)."""
    toks = list(toks)
    tiempo = None
    for t in toks:
        if t[0] == "momento":
            tiempo = t[1]
    toks = [t for t in toks if t[0] != "momento"]
    while toks and toks[0][0] in ("relleno", "y", ","):
        toks = toks[1:]
    if pregunta:
        sujeto, verbo, objeto = _pa_pregunta(toks)
    else:
        v = _pa_verbo(toks)
        if v is None:                                      # la elipsis: 'y 5 de ancho', 'y Luis 3'
            if not antes:
                raise _PaNo("no tiene verbo")
            verbo = antes["verbo"]
            k = next((i for i, t in enumerate(toks) if t[0] in ("num", "pide", "algo", "mult")), None)
            if k:
                sujeto, objeto = toks[:k], toks[k:]
            else:
                sujeto, objeto = antes["sujeto"], toks
            if not sujeto:
                sujeto = antes["sujeto"]
        else:
            sujeto, verbo, objeto = toks[:v], toks[v], toks[v + 1:]
    tiempo = tiempo or verbo[1].get("tiempo") or ("final" if pregunta and verbo[1]["tipo"] != "cambio" else None)
    cosa = _pa_cosa_de_toks(objeto, ctx)                  # U.3b: de que cosa habla esta frase
    del_verbo = ctx["voc"]["cosa_del_verbo"].get(verbo[1].get("palabra"))
    ctx["cosa_frase"] = cosa or ctx.get("cosa_heredada") or ((del_verbo,) if del_verbo else None)
    ctx["de_cada"] = verbo[1].get("palabra") in ctx["voc"]["de_cada"]
    ctx["unidad_frase"] = None
    ctx["tasa_frase"] = None
    objeto = _pa_por_cada(objeto, ctx)                    # '3 pesos por kilo': lo de CADA kilo
    if objeto is None:
        return {"verbo": verbo, "sujeto": sujeto}
    tipo = verbo[1]["tipo"]
    if _pa_ritmo(sujeto, objeto, ctx, pregunta):
        return {"verbo": verbo, "sujeto": sujeto}
    if pregunta and ctx["reparto"] is not None and (any(t[0] == "cada_uno" for t in sujeto)
                                                    or any(t[0] == "cada_uno" for t in objeto)):
        verbo = ("verbo", {"tipo": "toca", "palabra": verbo[2]}, verbo[2])      # 'cuantos recibe cada uno?'
        tipo = "toca"
    nucleo = {"verbo": verbo, "sujeto": sujeto}
    if tipo in ("cambio", "paga") and not (tipo == "paga" and pregunta and ctx["compras"]):
        _pa_cambio(sujeto, verbo, objeto, ctx, pregunta)
    elif tipo == "dar":
        _pa_dar(sujeto, verbo, objeto, ctx, pregunta, tiempo)
    elif tipo == "compra":
        _pa_compra(sujeto, verbo, objeto, ctx)
    elif tipo == "paga":
        _pa_estructura_simple(ctx, "lo_que_paga", objeto)
    elif tipo == "pago_con":
        _pa_estructura_simple(ctx, "pago", objeto)
    elif tipo == "vuelta":
        _pa_estructura_simple(ctx, "vuelta", objeto)
    elif tipo == "reparte":
        _pa_reparte(objeto, ctx, sujeto)
    elif tipo == "agrupa":
        _pa_agrupa(objeto, ctx)
    elif tipo == "diferencia":
        miembros = _pa_sujetos(sujeto, ctx, tiempo)
        if len(miembros) != 2:
            raise _PaNo("se diferencian: hacen falta dos")
        _pa_apuntar(ctx, ("op", "-", miembros[0], miembros[1]), _pa_dato(objeto, ctx), ctx["frase"], "diferencia")
    else:
        _pa_valor(sujeto, verbo, objeto, ctx, tiempo)
    return nucleo


def _pa_dato(toks, ctx):
    """Lo que hay detras del verbo cuando es un dato: '12 pesos', '?', 'algunas', o una expresion ('el doble de 3')."""
    toks = [t for t in toks if t[0] != "relleno"]
    if not toks:
        raise _PaNo("falta el dato")
    if toks[0][0] in ("num", "pide", "algo") and all(t[0] == "palabra" or t[0] in ("masmenos",) for t in toks[1:]):
        uni = [t[2] for t in toks[1:] if t[0] == "palabra"]
        if uni:
            _pa_unidad(ctx, uni)
        t = toks[0]
        if t[0] == "num":
            return ("num", t[1])
        if t[0] == "pide":
            return _pa_pedido(ctx)
        return _pa_incognita(ctx, "algunos")
    corte = next((i for i, t in enumerate(toks) if i and t[0] in ("de", "en", "para", "con", "a")
                  and not (t[0] == "de" and i == 1 and toks[0][0] == "num"
                           and toks[0][1][3] in ("fraccion", "decimal"))), None)
    if corte and toks[0][0] in ("num", "pide", "algo") and not _pa_hay_dato(toks[corte:]):
        return _pa_dato(toks[:corte], ctx)                # '4.50 en pan': lo de despues no es un dato
    return _pa_expresion(toks, ctx, "objeto")


def _pa_sujetos(sujeto, ctx, tiempo):
    """Los del sujeto (uno o varios), como arboles."""
    sujeto = [t for t in sujeto if t[0] not in ("juntos", "relleno")]
    if sujeto and sujeto[0][0] == "a" and len(sujeto) > 1 and sujeto[1][0] != "art":
        sujeto = sujeto[1:]
    partes = _pa_trozos_por_y(sujeto)
    out = []
    for p in partes:
        e = _pa_expresion(p, ctx, "sujeto")
        out.append(_pa_en_tiempo(e, ctx, tiempo))
    return out


def _pa_en_tiempo(e, ctx, tiempo):
    """Si el arbol es una cosa sola, la version del momento que toca."""
    if e[0] == "letra" and tiempo:
        ent = next((x for x in ctx["entes"] if e[1] in x["versiones"]), None)
        if ent:
            return ("letra", _pa_version(ctx, ent, tiempo))
    return e


def _pa_quien(ctx, verbo):
    """El sujeto que no se dice: el ultimo que se nombro (una PERSONA si el verbo es 'de alguien' o 'le')."""
    pal = verbo[1].get("palabra")
    defecto = ctx["voc"]["sujeto_de_verbo"].get(pal)
    if defecto:
        return _pa_ente(ctx, defecto.split())
    if ctx["ultimo"] is None and ctx["ultima_persona"] is None and verbo[1]["tipo"] == "valor" \
            and verbo[1].get("palabra") not in _PA_EXISTIR:
        e = _pa_ente(ctx, ["el_que_tiene"])               # 'Tenia 20 pesos': alguien que no se nombra
        e["persona"] = True
        return e
    if verbo[1].get("quien") in ("alguien", "le"):
        if ctx["ultima_persona"] is None and len(ctx["personas"]) == 1:      # la unica persona del texto
            ctx["ultima_persona"] = _pa_ente(ctx, list(ctx["personas"]))
        if ctx["ultima_persona"] is None:
            raise _PaNo("no se QUIEN %s (no se ha nombrado a nadie)" % pal)
        if ctx["ultimo"] is not None and not ctx["ultimo"]["persona"] and ctx["ultimo"]["tipo"] == "cuenta":
            raise _PaNo("no se QUIEN %s (lo ultimo que se nombro es una cosa)" % pal)
        return ctx["ultima_persona"]
    if ctx["ultimo"] is None:
        raise _PaNo("no se de que se habla")
    return ctx["ultimo"]


def _pa_valor(sujeto, verbo, objeto, ctx, tiempo):
    frase = ctx["frase"]
    numeros = ctx["grupo"] or [e for e in ctx["entes"] if e["tipo"] == "numero"]
    if [t[0] for t in objeto] == ["pide"] and len(numeros) > 1 and any(t[0] == "generico" and t[2].endswith("s")
                                                                        for t in sujeto):
        ctx["pide"].extend(e["versiones"][0] for e in numeros)              # 'cuales son los numeros?'
        return
    pal = verbo[1].get("palabra")
    entre = bool(sujeto) and sujeto[0][0] == "op" and sujeto[0][2] == "entre"     # 'entre Rosa y Pedro tienen 45'
    if entre:
        sujeto = [("juntos", None, "entre")] + list(sujeto[1:])
    sin_lugar = [t for t in sujeto if t[0] not in ("relleno", "juntos")]
    lugar = sin_lugar and sin_lugar[0][0] == "en"
    if _pa_es_parte(sin_lugar, objeto, pal, ctx):
        return
    if (pal in _PA_EXISTIR and (not sin_lugar or lugar)) or (lugar and verbo[1]["tipo"] == "valor"):
        todo = list(objeto)
        todo.extend(sin_lugar)
        return _pa_existe(todo, ctx, tiempo)      # 'en la caja hay 20' = 'hay 20 en la caja'
    if verbo[1]["tipo"] == "toca" or (sin_lugar and sin_lugar[0][0] == "cada_uno"):
        e = ctx["reparto"]
        if e is None:
            raise _PaNo("a cada uno de quienes?")
        _pa_apuntar(ctx, _pa_letra(ctx, e), _pa_dato([t for t in objeto if t[0] != "cada_uno"], ctx), frase,
                    "lo de cada uno")
        return
    if _pa_es_grupos(objeto):                          # 'tengo 3 cajas con 8 huevos cada una'
        return _pa_existe(objeto, ctx, tiempo)
    cuenta = None if _pa_tiene_grupos(ctx, sin_lugar) else _pa_es_cuenta_pedida(objeto, ctx)
    if cuenta is not None:                             # 'cuantos huevos tengo?': los huevos que hay
        _pa_apuntar(ctx, _pa_letra(ctx, cuenta, tiempo), _pa_dato(objeto, ctx), frase, "valor")
        return
    juntos = any(t[0] == "juntos" for t in sujeto) or any(t[0] == "juntos" for t in objeto) \
        or verbo[1]["tipo"] == "suman"
    objeto = [t for t in objeto if t[0] != "juntos"]
    cada_uno = any(t[0] == "cada_uno" for t in objeto)
    objeto = [t for t in objeto if t[0] != "cada_uno"]
    if not sin_lugar:
        if juntos:
            miembros = [_pa_letra(ctx, e) for e in _pa_grupo_de(ctx, [])]
        else:
            miembros = [_pa_letra(ctx, _pa_quien(ctx, verbo), tiempo)]
    elif sin_lugar[0][0] == "cada":
        miembros = _pa_sujetos(sin_lugar, ctx, tiempo)
        ent = ctx["tasa_frase"]
        if ent is not None:
            ent["por_unidad"] = True
            ctx["tasas"].append(ent)
    else:
        miembros = _pa_sujetos(sin_lugar, ctx, tiempo)
    if len(miembros) == 1 and juntos and miembros[0][0] == "letra":
        grupo = [e for e in (ctx["grupo"] or []) if miembros[0][1] in e["versiones"]]
        if grupo:
            miembros = [_pa_letra(ctx, e) for e in ctx["grupo"]]
    if cada_uno:
        for m in miembros:
            _pa_apuntar(ctx, m, _pa_dato(objeto, ctx), frase, "cada uno")
        return
    if len(miembros) > 1:
        _pa_estructura(ctx, "parte_todo", {"todo": _pa_dato(objeto, ctx), "parte": miembros}, frase)
        return
    a = miembros[0]
    if ctx["tasa_frase"] is not None and ctx["tasa_frase"] in ctx["tasas"]:
        ctx["tasa_frase"]["unidad_tasa"] = None
    if _pa_dimensiones(objeto, ctx, frase):
        return
    if _pa_comparar(a, objeto, ctx, frase):
        return
    if _pa_atributo(a, sin_lugar, objeto, ctx, frase):
        return
    d = _pa_dato(objeto, ctx)
    if d[0] == "letra" and d[1] in ctx["incognitas"] and a[0] == "letra":     # 'tenia algunas canicas': no se sabe
        ctx["incognitas"].remove(d[1])
        if ctx.get("unidad_frase"):
            ctx["unidad_de"][a[1]] = ctx["unidad_frase"]
        return
    _pa_apuntar(ctx, a, d, frase, "valor")
    if ctx["tasa_frase"] is not None:
        ctx["tasa_frase"]["unidad_tasa"] = ctx.get("unidad_frase")


def _pa_es_parte(sujeto, objeto, pal, ctx):
    """'13 son ninas' (despues de 'hay 25 alumnos'): una PARTE del todo; '?cuantos son ninos?': otra parte."""
    if pal not in ("son", "es", "eran") or ctx["todo"] is None:
        return False
    obj = [t for t in objeto if t[0] != "relleno"]
    if len(sujeto) == 1 and sujeto[0][0] == "num" and obj and all(t[0] == "palabra" for t in obj):
        palabras, dato = [t[2] for t in obj], ("num", sujeto[0][1])
    elif sujeto and all(t[0] in ("palabra", "art") for t in sujeto) and [t[0] for t in obj] == ["pide"]:
        palabras, dato = [t[2] for t in sujeto if t[0] == "palabra"], None
    else:
        return False
    todo = ctx["todo"]
    parte = _pa_ente(ctx, palabras, "cuenta")
    if parte is todo or not palabras:
        return False
    partes = ctx["partes"].setdefault(todo["nombre"], [])
    if parte not in partes:
        partes.append(parte)
    ctx["unidad_frase"] = todo["nombre"].replace("_", " ")
    _pa_apuntar(ctx, _pa_letra(ctx, parte), dato or _pa_pedido(ctx), ctx["frase"], "una parte")
    return True


def _pa_ritmo(sujeto, objeto, ctx, pregunta):
    """'ahorra 5 pesos CADA semana': lo de cada semana (grupos iguales en el tiempo).  Y en la pregunta, 'en 6 semanas'
    (con 'semana' de las de cada): 6 x semana."""
    obj = [t for t in objeto if t[0] != "relleno"]
    if not pregunta:
        k = next((i for i, t in enumerate(obj) if t[0] == "cada" and i), None)
        if k is None or obj[0][0] != "num" or not obj[k + 1:] or any(t[0] != "palabra" for t in obj[k + 1:]) \
                or any(t[0] != "palabra" for t in obj[1:k]):
            return False
        e = _pa_ente(ctx, [t[2] for t in obj[k + 1:]])
        e["por_unidad"] = True
        uni = " ".join(t[2] for t in obj[1:k])
        e["unidad_tasa"] = uni or None
        if uni:
            ctx["unidad_frase"] = uni
        _pa_apuntar(ctx, _pa_letra(ctx, e), ("num", obj[0][1]), ctx["frase"], "lo de cada uno")
        return True
    todo = [t for t in sujeto if t[0] != "relleno"]
    todo.extend(obj)
    for k, t in enumerate(todo):
        if t[0] in ("en", "para") and todo[k + 1:k + 2] and todo[k + 1][0] == "num":
            palabras = [x[2] for x in todo[k + 2:] if x[0] == "palabra"]
            e = _pa_por_unidad(ctx, palabras) if palabras else None
            if e is not None:
                if e.get("unidad_tasa"):
                    ctx["unidad_frase"] = e["unidad_tasa"]
                _pa_apuntar(ctx, _pa_pedido(ctx), ("op", "x", ("num", todo[k + 1][1]), _pa_letra(ctx, e)),
                            ctx["frase"], "grupos iguales")
                return True
    return False


def _pa_es_grupos(objeto):
    """'3 cajas con 8 huevos cada una', '3 filas de 4 sillas': grupos iguales en el objeto."""
    c = [t[0] for t in objeto if t[0] not in ("relleno", "cada_uno")]
    if len(c) < 5 or c[0] != "num" or c[1] != "palabra":
        return False
    k = 1
    while k < len(c) and c[k] == "palabra":
        k = k + 1
    return c[k:k + 3] in (["con", "num", "palabra"], ["de", "num", "palabra"])


def _pa_tiene_grupos(ctx, sujeto):
    """'cuantos kilos lleva EL CAMION' cuando el camion tiene cajas y se sabe lo de cada caja: se pide una cosa del
    camion (U.3b), no la cuenta suelta de los kilos."""
    palabras = [t[2] for t in sujeto if t[0] == "palabra"]
    e = _pa_buscar_ente(ctx, palabras, "uno") if palabras else None
    if e is None:
        return False
    familia = [e]
    familia.extend(e.get("hijos", []))
    return any(x.get("por_unidad") and _pa_misma_cosa(ctx, x["clave"], q["cosa"])
               for q in familia if q.get("cosa") for x in ctx["entes"] if not x.get("dueno"))


def _pa_es_cuenta_pedida(objeto, ctx):
    """'? huevos' cuando 'huevos' ya es una CUENTA (cuantos hay): se pide esa cuenta."""
    c = [t for t in objeto if t[0] != "relleno"]
    if len(c) < 2 or c[0][0] != "pide" or any(t[0] != "palabra" for t in c[1:]):
        return None
    palabras = [t[2] for t in c[1:]]
    e = _pa_buscar_ente(ctx, palabras, "cuenta")
    if e is None and any(x.get("unidad_tasa") == " ".join(palabras) for x in ctx["tasas"]):
        e = _pa_ente(ctx, palabras, "cuenta")             # los huevos de las cajas (grupos iguales)
    return e


def _pa_comparar(a, objeto, ctx, frase):
    """'N mas que B' / 'el doble que B' / 'K veces mas larga que B' / '3/4 de lo que B'.  Sin 'que': B es el ultimo
    otro que se nombro ('la azul es 4 veces mas larga').  Llena las estructuras de comparar (relaciones.kn)."""
    q = next((i for i, t in enumerate(objeto) if t[0] == "que"), None)
    izq = objeto if q is None else objeto[:q]
    izq = [t for t in izq if t[0] not in ("relleno",)]
    clases = [t[0] for t in izq]
    multi = (clases[:1] == ["mult"] or clases[:2] == ["art", "mult"] or clases[1:2] == ["veces"]
             or (clases[:2] == ["num", "de"] and izq[0][1][3] in ("fraccion", "decimal")))
    aditiva = not multi and "masmenos" in clases and any(c in ("num", "pide", "algo") for c in clases[:1])
    if not (aditiva or multi):
        return False
    if q is None:
        resto = list(izq[2:] if clases[:2] == ["art", "mult"] else izq[1:])
        while resto and resto[0][0] in ("veces", "de"):
            resto = resto[1:]
        if multi and resto and resto[0][0] != "masmenos" and (
                any(t[0] in ("lo_de", "art", "su", "cual", "generico", "num", "lo_que") for t in resto)
                or _pa_buscar_ente(ctx, [t[2] for t in resto if t[0] == "palabra"])):
            return False                                  # 'el doble de 3', '3 veces la edad de Juan': una expresion
        b = _pa_otro(ctx, a)
    else:
        b = _pa_expresion([t for t in objeto[q + 1:] if t[0] != "relleno"], ctx, "sujeto")
    if aditiva:
        k = clases.index("masmenos")
        signo = izq[k][1]
        detras = [t[2] for t in izq[k + 1:]]
        if any(w in ctx["voc"]["al_reves"] for w in detras):
            signo = "-" if signo == "+" else "+"
        n = _pa_dato(izq[:k], ctx)
        grande, pequeno = (a, b) if signo == "+" else (b, a)
        _pa_estructura(ctx, "comparacion_aditiva", {"grande": grande, "pequeno": pequeno, "diferencia": n}, frase)
        return True
    if izq[0][0] == "art":
        izq = izq[1:]
    if izq[0][0] == "mult":
        veces = ("num", _nu_leer(izq[0][1]))
    elif izq[0][0] == "pide":
        veces = _pa_pedido(ctx)
    else:
        veces = ("num", izq[0][1])
    resto = izq[1:]
    if resto and resto[0][0] in ("veces", "de"):
        resto = resto[1:]
    uni = [t[2] for t in resto if t[0] == "palabra" and t[2] not in ctx["voc"]["al_reves"]]
    if uni and not any(t[0] == "masmenos" for t in resto):
        _pa_unidad(ctx, uni)
    _pa_estructura(ctx, "comparacion_multiplicativa", {"grande": a, "veces": veces, "pequeno": b}, frase)
    return True


def _pa_dimensiones(objeto, ctx, frase):
    """'mide 5 cm por 4 cm por 3 cm': las DIMENSIONES de la figura en su orden (relaciones.kn; U.3b)."""
    trozos, actual = [], []
    for t in objeto:
        if t[0] == "op" and t[2] == "por":
            trozos.append(actual)
            actual = []
        elif t[0] != "relleno":
            actual.append(t)
    trozos.append(actual)
    if len(trozos) < 2 or any(not x or x[0][0] not in ("num", "pide", "algo") or any(y[0] != "palabra" for y in x[1:])
                              for x in trozos):
        return False
    fg = next((f for f in ctx["figuras"] if len(f["dimensiones"]) == len(trozos)), None)
    if fg is None:
        return False
    for m, x in zip(fg["dimensiones"], trozos):
        _pa_apuntar(ctx, _pa_letra(ctx, _pa_medida_de(ctx, fg, m)), _pa_dato(x, ctx), frase, "medida")
    return True


def _pa_por_cada(objeto, ctx):
    """'3 pesos por kilo', '40 personas por vagon': lo de CADA uno (grupos iguales; Schwartz: una cantidad 'por').
    Se apunta y se quita del objeto (None si no queda nada mas)."""
    obj = [t for t in objeto if t[0] != "relleno"]
    k = next((i for i, t in enumerate(obj) if t[0] == "op" and t[2] == "por" and i >= 2), None)
    if k is None or obj[0][0] != "num" or any(t[0] != "palabra" for t in obj[1:k]):
        return objeto
    detras = [t for t in obj[k + 1:] if t[0] not in ("art", "cada")]
    if not detras or any(t[0] != "palabra" for t in detras) or _pa_es_medida(ctx, [t[2] for t in detras]):
        return objeto
    uni = [t[2] for t in obj[1:k]]
    e = _pa_ente(ctx, [_pa_singular(t[2]) for t in detras])
    e["por_unidad"], e["unidad_tasa"] = True, " ".join(uni)
    if e not in ctx["tasas"]:
        ctx["tasas"].append(e)
    ctx["cosa_frase"] = _pa_cosa(ctx, uni)
    _pa_unidad(ctx, uni)
    ctx["unidad_de"][e["versiones"][0]] = " ".join(uni)
    _pa_apuntar(ctx, _pa_letra(ctx, e), ("num", obj[0][1]), ctx["frase"], "lo de cada uno")
    return None


def _pa_lo_que(ctx, verbo):
    """'la mitad de LO QUE TENIA' (lo que tenia antes de este cambio); '3/4 de LO QUE HABIA BAJADO' (el cambio de
    antes de esa cosa con ese verbo).  U.3b."""
    e = ctx["quien_cambia"]
    if e is None:
        raise _PaNo("'lo que %s' de quien?" % verbo.get("palabra", ""))
    if verbo["tipo"] == "cambio":
        for ent, s, cambio in reversed(ctx["cambios"]):
            if ent is e and s == verbo["signo"]:
                return _pa_par(cambio)
        raise _PaNo("antes no hubo ningun '%s'" % verbo.get("palabra", ""))
    return ("letra", e["versiones"][-1])


def _pa_otro(ctx, a):
    for e in reversed(ctx["mencionados"]):
        if a[0] == "letra" and a[1] in e["versiones"]:
            continue
        if e["tipo"] in ("uno", "cuenta", "numero"):
            return _pa_letra(ctx, e)
    raise _PaNo("comparado con que?")


def _pa_atributo(a, sujeto, objeto, ctx, frase):
    """'mide 8 cm de largo', 'tiene 30 cm de perimetro', 'un cuadrado de 6 de lado': la MEDIDA de la figura."""
    k = next((i for i, t in enumerate(objeto) if t[0] == "de" and i), None)
    if k is None or not objeto or objeto[0][0] not in ("num", "pide", "algo"):
        return False
    palabras = [t[2] for t in objeto[k + 1:] if t[0] in ("palabra",)]
    if not palabras or not _pa_es_medida(ctx, palabras):
        return False
    m = _pa_medida(ctx, palabras)
    d = _pa_dato(objeto[:k], ctx)
    _pa_apuntar(ctx, _pa_letra(ctx, m), d, frase, "medida")
    return True


def _pa_existe(objeto, ctx, tiempo):
    """'hay 8 pajaros', 'hay 20 lapices en 4 cajas', 'hay 3 bolsas con 4 caramelos cada una', 'hay 3 filas de 4 sillas',
    'hay ? lapices en cada caja'.  Lo que hay es una CUENTA (cuantos hay)."""
    frase = ctx["frase"]
    objeto = [t for t in objeto if t[0] not in ("relleno",)]
    if not objeto or objeto[0][0] not in ("num", "pide", "algo"):
        raise _PaNo("hay... cuantos?")
    k = 1
    palabras = []
    while k < len(objeto) and objeto[k][0] == "palabra":
        palabras.append(objeto[k][2])
        k = k + 1
    if not palabras:                                  # 'ahora hay 7': de lo ultimo que se conto
        ultimo = next((e for e in reversed(ctx["mencionados"]) if e["tipo"] == "cuenta"), None)
        if ultimo is None:
            raise _PaNo("hay cuantos de que?")
        palabras = ultimo["nombre"].split("_")
    resto = objeto[k:]
    dato = _pa_dato(objeto[:1], ctx)
    if resto and resto[0][0] == "en" and len(resto) > 1 and resto[1][0] == "cada":   # 'hay ? lapices en cada caja'
        grupo = _pa_ente(ctx, [t[2] for t in resto[2:] if t[0] == "palabra"])
        grupo["por_unidad"] = True
        grupo["unidad_tasa"] = " ".join(palabras)
        if grupo not in ctx["tasas"]:
            ctx["tasas"].append(grupo)
        _pa_unidad(ctx, palabras)
        _pa_apuntar(ctx, _pa_letra(ctx, grupo), dato, frase, "lo de cada uno")
        return
    total = _pa_ente(ctx, palabras, "cuenta")
    _pa_unidad(ctx, palabras)
    if resto and resto[0][0] in ("en", "de", "con") and len(resto) > 1 and resto[1][0] == "num":
        n2 = ("num", resto[1][1])
        mas = [t[2] for t in resto[2:] if t[0] == "palabra"]
        if not mas:
            raise _PaNo("en %s de que?" % resto[1][2])
        if resto[0][0] == "en":                            # 20 lapices en 4 cajas: lo de cada caja no se sabe
            grupos = _pa_ente(ctx, mas, "cuenta")
            cada = _pa_ente(ctx, mas)
            cada["por_unidad"] = True
            cada["unidad_tasa"] = " ".join(palabras)
            if cada not in ctx["tasas"]:
                ctx["tasas"].append(cada)
            ctx["reparto"] = cada
            _pa_apuntar(ctx, _pa_letra(ctx, total, tiempo), dato, frase, "valor")
            _pa_apuntar(ctx, _pa_letra(ctx, grupos), n2, frase, "valor")
            return
        # 3 filas de 4 sillas;  3 bolsas con 4 caramelos cada una
        cada = _pa_ente(ctx, [_pa_singular(w) for w in palabras])
        cada["por_unidad"] = True
        cada["unidad_tasa"] = " ".join(mas)
        if cada not in ctx["tasas"]:
            ctx["tasas"].append(cada)
        _pa_apuntar(ctx, _pa_letra(ctx, total, tiempo), dato, frase, "valor")
        _pa_apuntar(ctx, _pa_letra(ctx, cada), n2, frase, "lo de cada uno")
        return
    if resto and not (resto[0][0] in ("en", "de", "para") and not _pa_hay_dato(resto)):
        raise _PaNo("no entiendo '%s'" % " ".join(t[2] for t in resto))
    _pa_apuntar(ctx, _pa_letra(ctx, total, tiempo), dato, frase, "valor")
    if ctx["partes"].get(total["nombre"]) is None:
        ctx["todo"] = total                                # 'hay 25 alumnos': un TODO que puede tener partes


def _pa_cambio(sujeto, verbo, objeto, ctx, pregunta):
    """Gana, pierde, sube, baja, le dan, se van: una cantidad NUEVA en el tiempo (despues = antes +/- cambio).
    El cambio puede ser un numero, 'algunos' (no se sabe) o una parte de lo que tenia ('la cuarta parte')."""
    sujeto = [t for t in sujeto if t[0] not in ("relleno",)]
    if sujeto and sujeto[0][0] in ("en", "a", "al"):     # 'en la primera parada bajan 8': el sitio no es quien cambia
        sujeto = []
    if sujeto:
        partes = _pa_trozos_por_y(sujeto)
        if len(partes) != 1:
            raise _PaNo("cambian varios a la vez")
        e = _pa_cosa_sola(partes[0], ctx)
    else:
        e = _pa_quien(ctx, verbo)
    e = _pa_de_cosa(ctx, e, ctx.get("cosa_frase"))         # U.3b: lo que cambia es UNA cosa de alguien
    signo = verbo[1]["signo"]
    obj = [t for t in objeto if t[0] not in ("relleno", "masmenos")]
    if pregunta:
        return _pa_cambio_pedido(e, signo, ctx)
    ctx["quien_cambia"] = e
    try:
        cuanto = _pa_cuanto_cambia(obj, e, verbo, ctx)
    finally:
        ctx["quien_cambia"] = None
    _pa_un_cambio(ctx, e, signo, cuanto, "%s %s" % (verbo[2], " ".join(t[2] for t in objeto if t[0] != "relleno")))
    return e


def _pa_cuanto_cambia(obj, e, verbo, ctx):
    if obj and (obj[0][0] == "mult" or (obj[0][0] == "art" and obj[1:2] and obj[1][0] == "mult")) \
            and not [t for t in obj if t[0] == "de"]:
        m = obj[0] if obj[0][0] == "mult" else obj[1]     # 'regala la cuarta parte': de lo que tiene ahora
        return ("op", "x", ("num", _nu_leer(m[1])), ("letra", e["versiones"][-1]))
    if obj and any(t[0] == "lo_que" for t in obj) and (obj[0][0] in ("mult", "num") or (
            obj[0][0] == "art" and obj[1:2] and obj[1][0] == "mult")):
        return _pa_dato(obj, ctx)                         # 'la mitad de lo que tenia' (U.3b)
    if not obj or obj[0][0] not in ("num", "algo", "pide"):
        raise _PaNo("%s... cuanto?" % verbo[2])
    return _pa_dato(obj, ctx)


def _pa_un_cambio(ctx, e, signo, cambio, texto):
    """La cantidad e cambia: despues = antes +/- cambio (relaciones.kn: cambio_gana / cambio_pierde)."""
    if cambio[0] == "letra" and cambio[1] in ctx["incognitas"]:
        ctx["cambios_desconocidos"].append((e, signo, cambio[1]))
    antes = _pa_letra(ctx, e, exacto=True)
    despues = ("letra", _pa_otra_version(ctx, e))
    ctx["cambios"].append((e, signo, cambio))
    ctx["que_es"][antes[1]] = ctx["que_es"].get(antes[1]) or "%s al principio" % e["nombre"].replace("_", " ")
    ctx["que_es"][despues[1]] = "%s despues de '%s'" % (e["nombre"].replace("_", " "), texto)
    ctx["ultimo"] = e
    _pa_estructura(ctx, _PA_ESTRUCTURA_DE[signo], {"despues": despues, "antes": antes, "cambio": cambio}, ctx["frase"])


def _pa_dar(sujeto, verbo, objeto, ctx, pregunta, tiempo):
    """'Ana le da 2 a Luis': un TRASPASO (Ana pierde 2 y Luis gana 2).  Sin 'a quien': el que da pierde.  Y 'da' sin
    nadie que de es 'es igual a' (STUDENT: 'si a un numero le sumas 5 da 12')."""
    obj = [t for t in objeto if t[0] not in ("relleno",)]
    k = next((i for i, t in enumerate(obj) if t[0] == "a" and i), None)
    quien_da = [t for t in sujeto if t[0] not in ("relleno",)]
    persona = not quien_da or (len(quien_da) <= 2 and quien_da[-1][0] == "palabra"
                               and quien_da[-1][2] in ctx["personas"])
    if not persona and k is None:
        return _pa_valor(sujeto, ("verbo", {"tipo": "valor", "palabra": verbo[2]}, verbo[2]), objeto, ctx, tiempo)
    menos = ("verbo", dict(verbo[1], tipo="cambio", signo="-", quien="alguien"), verbo[2])
    if k is None:
        return _pa_cambio(sujeto, menos, objeto, ctx, pregunta)
    receptor = _pa_cosa_sola(obj[k + 1:], ctx)
    if pregunta:
        return _pa_cambio(sujeto, menos, obj[:k], ctx, True)
    e = _pa_cambio(sujeto, menos, obj[:k], ctx, False)
    cambio = ctx["cambios"][-1][2]
    _pa_un_cambio(ctx, receptor, "+", cambio, "le dan %s" % " ".join(t[2] for t in obj[:k]))
    ctx["ultimo"], ctx["ultima_persona"] = e, e if e["persona"] else ctx["ultima_persona"]


def _pa_cosa_sola(toks, ctx):
    e = _pa_expresion(toks, ctx, "objeto")
    if e[0] != "letra":
        raise _PaNo("lo que cambia tiene que ser una cosa")
    return next(x for x in ctx["entes"] if e[1] in x["versiones"])


def _pa_cambio_pedido(e, signo, ctx):
    """'cuantos le dieron?', 'cuanto subio?': el cambio que no se sabia; o, si no hubo cambios, lo que va de la primera
    vez a la ultima."""
    for ent, s, letra in ctx["cambios_desconocidos"]:
        if ent is e and s == signo:
            ctx["pide"].append(letra)
            return
    for ent, s, cambio in ctx["cambios"]:                 # 'cuantos regala?' (regalo la cuarta parte)
        if ent is e and s == signo:
            _pa_apuntar(ctx, _pa_pedido(ctx), cambio, ctx["frase"], "el cambio")
            return
    if len(e["versiones"]) < 2:
        raise _PaNo("no hubo ningun cambio")
    primera, ultima = e["versiones"][0], e["versiones"][-1]
    orden = ctx["voc"]["orden_momentos"]                  # 'por la tarde' va antes que 'por la noche' (frases.kn)
    con_orden = sorted((orden.index(m), k) for m, k in e["momentos"].items() if m in orden)
    if len(con_orden) == len(e["momentos"]) and len(con_orden) > 1:
        primera, ultima = e["versiones"][con_orden[0][1]], e["versiones"][con_orden[-1][1]]
    q = _pa_pedido(ctx)
    _pa_estructura(ctx, _PA_ESTRUCTURA_DE[signo], {"despues": ("letra", ultima), "antes": ("letra", primera),
                                                   "cambio": q}, ctx["frase"])


def _pa_compra(sujeto, verbo, objeto, ctx):
    """Comprar cosas con PRECIO: lo que paga = cantidad x precio de cada una.  Sin precio, es un cambio (R.1)."""
    obj = [t for t in objeto if t[0] not in ("relleno",)]
    partes = _pa_trozos_por_y(obj)
    compras = []
    cosa_frase, ctx["cosa_frase"] = ctx["cosa_frase"], None     # lo de cada cosa es de su PRECIO (U.3b)
    for p in partes:
        if len(p) >= 2 and p[0][0] in ("num", "art") and p[1][0] == "palabra":
            k = 1
            palabras = []
            while k < len(p) and p[k][0] == "palabra":
                palabras.append(p[k][2])
                k = k + 1
            n = ("num", p[0][1]) if p[0][0] == "num" else ("num", ("+", 1, 1, "entero"))
            resto = p[k:]
            if resto and resto[0][0] == "de" and len(resto) > 1 and resto[1][0] == "num":   # un libro de 13.50 pesos
                e = _pa_ente(ctx, palabras)
                e["por_unidad"] = True
                precio = [t[2] for t in resto[2:] if t[0] == "palabra"]
                _pa_unidad(ctx, precio)
                ctx["cosa_frase"] = _pa_cosa(ctx, precio) if precio else None
                _pa_apuntar(ctx, _pa_letra(ctx, e), ("num", resto[1][1]), ctx["frase"], "precio")
                ctx["cosa_frase"] = None
                compras.append(("op", "x", n, _pa_letra(ctx, e)) if p[0][0] == "num" else _pa_letra(ctx, e))
                continue
            e = _pa_por_unidad(ctx, palabras)
            if e is None and set(_pa_singular(w) for w in palabras) <= ctx["con_precio"] and palabras:
                e = _pa_ente(ctx, palabras)                   # su precio se dice despues ('cada cuaderno cuesta 4')
                e["por_unidad"] = True
            if e is not None and not resto:
                compras.append(("op", "x", n, _pa_letra(ctx, e)))
                continue
        compras = None
        break
    ctx["cosa_frase"] = cosa_frase
    if compras:
        ctx["compras"].extend(compras)
        _pa_paga_comprando(sujeto, verbo, compras, ctx)
        return
    _pa_cambio(sujeto, verbo, objeto, ctx, False)


def _pa_paga_comprando(sujeto, verbo, compras, ctx):
    """Comprar con precio es GASTAR: si el que compra tiene dinero, su dinero baja lo que cuestan las compras (U.3b)."""
    suj = [t for t in sujeto if t[0] not in ("relleno",)]
    try:
        quien = _pa_cosa_sola(suj, ctx) if suj else _pa_quien(ctx, verbo)
    except _PaNo:
        return
    raiz = quien.get("dueno") or quien
    familia = [raiz]
    familia.extend(raiz.get("hijos", []))
    dinero = [x for x in familia if x.get("cosa") and _pa_misma_cosa(ctx, ("dinero",), x["cosa"])]
    if len(dinero) == 1:
        _pa_un_cambio(ctx, dinero[0], "-", _pa_suma(compras), "paga lo que compra")


def _pa_estructura_simple(ctx, nombre, objeto):
    """'paga con 20' (pago), 'le devuelven ?' (vuelta), 'cuanto paga?' (lo que paga): las cantidades del dinero."""
    e = _pa_ente(ctx, [nombre])
    ctx["dinero"].add(nombre)
    _pa_apuntar(ctx, _pa_letra(ctx, e), _pa_dato([t for t in objeto if t[0] not in ("relleno",)], ctx),
                ctx["frase"], nombre)


def _pa_reparte(objeto, ctx, sujeto=()):
    """'reparte 12 caramelos entre 3 ninos': todo = grupos x lo de cada uno (lo de cada uno no se sabe).
    'Tres amigos se reparten 24 cromos': los grupos son los del sujeto."""
    obj = [t for t in objeto if t[0] not in ("relleno",)]
    suj = [t for t in sujeto if t[0] not in ("relleno",)]
    if suj and suj[0][0] == "num" and not any(t[0] == "op" and t[2] == "entre" for t in obj):
        k = next((i for i, t in enumerate(obj) if t[0] in ("en", "a")), len(obj))
        obj = obj[:k]
        obj.append(("op", ":", "entre"))
        obj.extend(suj)
    k = next((i for i, t in enumerate(obj) if t[0] == "op" and t[2] == "entre"), None)
    if k is None or k < 1 or k + 1 >= len(obj) or obj[k + 1][0] != "num":
        raise _PaNo("repartir: se dice 'reparte N cosas entre N'")
    total = _pa_ente(ctx, [t[2] for t in obj[1:k] if t[0] == "palabra"] or ["cosas"], "cuenta")
    quienes = [t[2] for t in obj[k + 2:] if t[0] == "palabra"] or ["grupos"]
    grupos = _pa_ente(ctx, quienes, "cuenta")
    cada = _pa_ente(ctx, [_pa_singular(w) for w in quienes])
    cada["por_unidad"], cada["unidad_tasa"] = True, total["nombre"]
    ctx["tasas"].append(cada)
    ctx["reparto"] = cada
    _pa_apuntar(ctx, _pa_letra(ctx, total), _pa_dato(obj[:1], ctx), ctx["frase"], "valor")
    _pa_apuntar(ctx, _pa_letra(ctx, grupos), ("num", obj[k + 1][1]), ctx["frase"], "valor")


def _pa_agrupa(objeto, ctx):
    """'mete 12 caramelos en bolsas de 4': todo = grupos x lo de cada uno (los grupos no se saben)."""
    obj = [t for t in objeto if t[0] not in ("relleno",)]
    k = next((i for i, t in enumerate(obj) if t[0] == "en"), None)
    if k is None or k < 1 or len(obj[k:]) < 4 or obj[k + 2][0] != "de" or obj[k + 3][0] != "num":
        raise _PaNo("agrupar: se dice 'mete N cosas en bolsas de N'")
    total = _pa_ente(ctx, [t[2] for t in obj[1:k] if t[0] == "palabra"] or ["cosas"], "cuenta")
    grupos = _pa_ente(ctx, [obj[k + 1][2]], "cuenta")
    cada = _pa_ente(ctx, [_pa_singular(obj[k + 1][2])])
    cada["por_unidad"], cada["unidad_tasa"] = True, total["nombre"]
    ctx["tasas"].append(cada)
    _pa_apuntar(ctx, _pa_letra(ctx, total), _pa_dato(obj[:1], ctx), ctx["frase"], "valor")
    _pa_apuntar(ctx, _pa_letra(ctx, cada), ("num", obj[k + 3][1]), ctx["frase"], "lo de cada uno")
    _pa_letra(ctx, grupos)


# ------------------------------------------------------------- 6. el modelo

def _pa_contexto(texto, saber):
    voc = _pa_vocabulario(saber)
    return {"saber": saber, "voc": voc, "rel": _pa_relaciones(saber), "personas": _pa_personas(texto, voc, saber),
            "entes": [], "nombres": set(), "rels": [], "pide": [], "incognitas": [], "mencionados": [],
            "ultimo": None, "ultima_persona": None, "grupo": None, "figuras": [], "figuras_usadas": [],
            "tasas": [], "reparto": None, "compras": [], "dinero": set(), "cambios_desconocidos": [],
            "frase": "", "unidad_frase": None, "tasa_frase": None, "unidad_de": {}, "que_es": {}, "cambios": [],
            "todo": None, "partes": {}, "cosa_frase": None, "cosa_heredada": None, "cosa_pedido": {},
            "de_cada": False, "quien_cambia": None, "par_ultimo": None}


def _pa_preparar_figuras_y_grupos(toks, ctx):
    """Las palabras que traen relaciones que se SABEN: una figura con sus medidas; 'dos numeros consecutivos'."""
    palabras = [t[2] for t in toks]
    texto = " %s " % " ".join(palabras)
    for fg in ctx["rel"]["figuras"]:
        if fg in ctx["figuras"]:
            continue
        medidas = list(fg["medidas"])
        medidas.extend(fg["otros"])
        medidas.extend(fg["pares"])
        if any(" %s " % w in texto for w in fg["palabras"]) and \
                any(" %s " % m in ctx["todo_el_texto"] for m in medidas):
            ctx["figuras"].append(fg)
    for k, t in enumerate(toks):                          # 'dos numeros (pares) consecutivos': un GRUPO
        if t[0] == "generico" and k and toks[k - 1][0] == "num" and t[2].endswith("s"):
            cuantos = toks[k - 1][1][1]
            despues = " ".join(x[2] for x in toks[k + 1:k + 3])
            relacion = None
            for p in ctx["rel"]["palabras"]:
                for w in p["palabras"]:
                    if despues == w or despues.startswith(w + " ") or (" " not in w and despues.split(" ")[:1] == [w]):
                        if relacion is None or len(w) > len(relacion[1]):
                            relacion = (p, w)
            if ctx["grupo"] is None:
                ctx["grupo"] = [_pa_numero_nuevo(ctx) for _ in range(cuantos)]
            nuevos = toks[:k - 1]
            nuevos.append(("art", "los", "los"))
            nuevos.append(("generico", None, "numeros"))
            quitar = len(relacion[1].split()) if relacion else 0
            nuevos.extend(toks[k + 1 + quitar:])
            if relacion:
                for a, b in zip(ctx["grupo"], ctx["grupo"][1:]):
                    izq, der = _pa_formula(relacion[0]["formula"])
                    roles = {"siguiente": ("letra", b["nombre"]), "anterior": ("letra", a["nombre"])}
                    _pa_apuntar(ctx, _pa_rellenar(izq, roles), _pa_rellenar(der, roles),
                                "%s %s" % (t[2], relacion[1]), relacion[0]["nombre"])
            return nuevos
    return toks


def _pa_leer(texto, saber):
    """El MODELO de un problema con palabras: {'cantidades', 'relaciones', 'pide', 'lecturas', 'unidades'...}."""
    ctx = _pa_contexto(texto, saber)
    frases = _pa_frases(texto)
    if not frases:
        raise ValueError("no hay nada que leer")
    ctx["todo_el_texto"] = " %s " % " ".join(re.findall(r"[a-z]+", _pa_normal(texto)))
    hechos, preguntas = [], []
    ctx["con_precio"] = set()
    for frase, es_pregunta in frases:
        toks = _pa_tokens(frase, ctx["voc"], saber)
        for k, t in enumerate(toks):                       # 'cada cuaderno', 'un libro cuesta': lo que tiene PRECIO
            if t[0] == "cada" or (t[0] == "art" and t[2] in ("un", "una")):
                j = k + 1
                while j < len(toks) and toks[j][0] in ("art", "palabra"):
                    if toks[j][0] == "palabra":
                        ctx["con_precio"].add(_pa_singular(toks[j][2]))
                    j = j + 1
        if es_pregunta and len(toks) > 1 and toks[0][0] == "que" and toks[1][0] == "palabra":
            toks[0] = ("preg", None, "cuanto")             # 'que temperatura hace?' (U.3b)
        if es_pregunta or (toks and toks[0][0] == "preg"):
            k = next((i for i, t in enumerate(toks) if t[0] == "relleno" and t[2] == "si" and i), None)
            if k:                                          # 'cuanto cuesta la goma si ...': lo de detras es un hecho
                hechos.append((" ".join(t[2] for t in toks[k + 1:]), toks[k + 1:]))
                toks = toks[:k]
            preguntas.append((frase if k is None else " ".join(t[2] for t in toks), toks))
        else:
            hechos.append((frase, toks))
    lecturas = []
    for frase, toks in hechos:
        lecturas.append(_pa_leer_frase(frase, toks, ctx, False))
    for frase, toks in preguntas:
        lecturas.append(_pa_leer_frase(frase, toks, ctx, True))
    _pa_lo_que_se_sabe(ctx)
    return _pa_modelo(texto, ctx, lecturas)


def _pa_leer_frase(frase, toks, ctx, pregunta):
    antes = len(ctx["rels"])
    pide_antes = len(ctx["pide"])
    toks = _pa_preparar_figuras_y_grupos(toks, ctx)
    leido = {"frase": frase, "pregunta": pregunta, "error": None, "desde": antes}
    try:
        anterior = None
        ctx["unidad_heredada"] = None
        ctx["cosa_heredada"] = None
        for nucleo in (_pa_nucleos(toks) if not pregunta else [toks]):
            ctx["frase"] = frase
            anterior = _pa_nucleo(nucleo, ctx, pregunta, anterior)
            ctx["cosa_heredada"] = ctx.get("cosa_frase")       # 'Ana tiene 5 canicas y Luis 3' (canicas)
            ctx["unidad_heredada"] = ctx.get("unidad_frase") or ctx["unidad_heredada"]    # 'y Luis tiene 4' (caramelos)
        ctx["unidad_heredada"] = None
    except (_PaNo, _NuNoSale, KeyError, IndexError, ValueError) as ex:
        del ctx["rels"][antes:]
        del ctx["pide"][pide_antes:]
        leido["error"] = str(ex) or "no la entiendo"
        leido["cambio"] = any(t[0] == "verbo" and t[1]["tipo"] in ("cambio", "compra", "paga", "reparte", "agrupa", "dar")
                              for t in toks)
        leido["palabras"] = set(t[2] for t in toks if t[0] == "palabra")
        leido["dato"] = any(t[0] in ("num", "algo", "mult") for t in toks)     # U.4: 'la mitad' tambien es un dato
    leido["hasta"] = len(ctx["rels"])
    ctx["cosa_heredada"] = ctx["cosa_frase"] = None
    return leido


def _pa_lo_que_se_sabe(ctx):
    """Las relaciones que no dice el texto: las formulas de las figuras, los grupos iguales, lo que se paga y la vuelta."""
    for fg in ctx["figuras_usadas"]:
        for f in fg["formulas"]:
            izq, der = _pa_formula(f)
            roles = {}
            for m in fg["medidas"]:
                e = _pa_buscar_ente(ctx, [m], "medida") or _pa_nuevo_ente(ctx, (m,), "medida", _pa_libre(ctx, m))
                e["figura"] = fg
                roles[m] = ("letra", e["nombre"])
            _pa_apuntar_sabido(ctx, _pa_rellenar(izq, roles), _pa_rellenar(der, roles),
                               "lo que se sabe del %s: %s" % (fg["nombre"], f), fg["nombre"])
    for cada in ctx["tasas"]:                              # grupos iguales: todo = grupos x cada grupo
        u = cada.get("unidad_tasa")
        grupos = _pa_buscar_ente(ctx, list(cada["clave"]), "cuenta")
        todo = _pa_buscar_ente(ctx, u.split(), "cuenta") if u else None
        if todo is None and grupos is not None:
            otros = [e for e in ctx["entes"] if e["tipo"] == "cuenta" and e is not grupos]
            todo = otros[0] if len(otros) == 1 else None
        if grupos is not None and todo is not None:
            izq, der = _pa_formula(ctx["rel"]["estructuras"]["grupos_iguales"])
            roles = {"todo": ("letra", todo["versiones"][0]), "grupos": ("letra", grupos["versiones"][0]),
                     "cada_grupo": ("letra", cada["versiones"][0])}
            _pa_apuntar_sabido(ctx, _pa_rellenar(izq, roles), _pa_rellenar(der, roles),
                               "grupos iguales: %s" % ctx["rel"]["estructuras"]["grupos_iguales"], "grupos_iguales")
    for raiz in [e for e in ctx["entes"] if e.get("hijos")]:     # U.3b: el camion lleva 12 CAJAS y cada caja 8 KILOS:
        familia = [raiz]                                            # los kilos del camion = cajas x lo de cada caja
        familia.extend(raiz["hijos"])
        for q1 in familia:
            for q2 in familia:
                if q1 is q2 or not q1.get("cosa") or not q2.get("cosa"):
                    continue
                cada = next((x for x in ctx["entes"] if x.get("por_unidad") and x.get("cosa") and not x.get("dueno")
                             and _pa_misma_cosa(ctx, x["clave"], q1["cosa"])
                             and _pa_misma_cosa(ctx, x["cosa"], q2["cosa"])), None)
                if cada is not None:
                    _pa_apuntar_sabido(ctx, ("letra", "\x00final\x00" + q2["nombre"]),
                                       ("op", "x", ("letra", "\x00final\x00" + q1["nombre"]),
                                        ("letra", cada["versiones"][0])),
                                       "grupos iguales: %s de %s = %s x lo de cada %s" % (
                                           " ".join(q2["cosa"]), raiz["nombre"], " ".join(q1["cosa"]),
                                           " ".join(cada["clave"])), "grupos_iguales")
    for raiz in [e for e in ctx["entes"] if e.get("hijos")]:     # M.23: la misma cosa en dos unidades (km y m)
        familia = [raiz]
        familia.extend(raiz["hijos"])
        for grande in familia:
            for pequena in familia:
                eq = _pa_equivalencia(ctx, grande.get("cosa"), pequena.get("cosa"))
                if grande is pequena or eq is None or grande["versiones"][1:] or pequena["versiones"][1:]:
                    continue                       # si una cambia, no se sabe en que momento valen lo mismo: no se usa
                _pa_apuntar_sabido(ctx, ("letra", pequena["versiones"][0]),
                                   ("op", "x", ("num", ("+", eq["veces"], 1, "entero")), ("letra", grande["versiones"][0])),
                                   "lo que se sabe de las medidas: 1 %s = %d %s" % (
                                       grande["cosa"][0], eq["veces"], pequena["cosa"][0]), "medida")
    for todo in ctx["entes"]:                              # las partes de un todo ('13 son ninas'): parte + parte = todo
        partes = ctx["partes"].get(todo["nombre"]) or []
        if len(partes) > 1:
            izq, der = _pa_formula(ctx["rel"]["estructuras"]["parte_todo"])
            roles = {"todo": ("letra", todo["versiones"][0]), "parte": [("letra", x["versiones"][0]) for x in partes]}
            _pa_apuntar_sabido(ctx, _pa_rellenar(izq, roles), _pa_rellenar(der, roles),
                               "las partes de %s: %s" % (todo["nombre"], ctx["rel"]["estructuras"]["parte_todo"]),
                               "parte_todo")
    if ctx["compras"] and ("lo_que_paga" in ctx["dinero"] or "vuelta" in ctx["dinero"]):
        paga = _pa_ente(ctx, ["lo_que_paga"])
        _pa_apuntar_sabido(ctx, ("letra", paga["nombre"]), _pa_suma(ctx["compras"]),
                           "lo que paga: cantidad x precio de cada uno", "precio")
    if "vuelta" in ctx["dinero"]:
        izq, der = _pa_formula(ctx["rel"]["estructuras"]["vuelta"])
        roles = {n: ("letra", _pa_ente(ctx, [n])["nombre"]) for n in ("vuelta", "pago", "lo_que_paga")}
        _pa_apuntar_sabido(ctx, _pa_rellenar(izq, roles), _pa_rellenar(der, roles),
                           "la vuelta: %s" % ctx["rel"]["estructuras"]["vuelta"], "vuelta")


def _pa_equivalencia(ctx, grande, pequena):
    """M.23 (NCETM 2.29): 'km' y 'm' (o 'm de cuerda' y 'cm de cuerda'): la fila de medidas de relaciones.kn que pasa de
    la unidad grande a la pequena; None si no son la misma cosa en dos unidades de la misma magnitud."""
    if not grande or not pequena or grande[1:] != pequena[1:]:
        return None
    return next((m for m in ctx["rel"].get("medidas") or [] if grande[0] in m["grande"] and pequena[0] in m["pequena"]),
                None)


def _pa_apuntar_sabido(ctx, izq, der, frase, porque):
    ctx["rels"].append({"rel": (izq, der), "frase": frase, "porque": porque, "unidad": None, "sabido": True})


def _pa_final(ctx, e):
    """'ahora' / 'al final': la ultima version de esa cantidad (despues de todos los cambios)."""
    if e[0] == "letra" and e[1].startswith("\x00final\x00"):
        base = e[1][len("\x00final\x00"):]
        ent = next(x for x in ctx["entes"] if x["nombre"] == base)
        return ("letra", ent["versiones"][-1])
    if e[0] in ("par", "neg"):
        return (e[0], _pa_final(ctx, e[1]))
    if e[0] == "op":
        return ("op", e[1], _pa_final(ctx, e[2]), _pa_final(ctx, e[3]))
    return e


def _pa_modelo(texto, ctx, lecturas):
    for r in ctx["rels"]:
        r["rel"] = (_pa_final(ctx, r["rel"][0]), _pa_final(ctx, r["rel"][1]))
    pide = []
    for p in ctx["pide"]:
        if p not in pide:
            pide.append(p)
    for r in list(ctx["rels"]):                           # 'la goma cuesta ?': se pide la goma (sin otra cantidad)
        izq, der = r["rel"]
        if der[0] == "letra" and der[1] in pide and izq[0] == "letra" and izq[1] not in pide and \
                len([x for x in ctx["rels"] if der[1] in _u_letras_rel(x["rel"])]) == 1:
            pide[pide.index(der[1])] = izq[1]
            r["pedido"] = izq[1]
    if not pide:
        mal = [l for l in lecturas if l["pregunta"] and l["error"]]
        if mal:
            raise ValueError("no entiendo la pregunta '%s' (%s)" % (mal[0]["frase"], mal[0]["error"]))
        raise ValueError("no encuentro la pregunta (lo que se pide)")
    # lo que sobra no estorba: solo lo CONECTADO con lo que se pide
    conectadas, letras = [], set(pide)
    cambia = True
    while cambia:
        cambia = False
        for r in ctx["rels"]:
            if r in conectadas or r.get("pedido"):
                continue
            ls = set(_u_letras_rel(r["rel"]))
            if ls & letras:
                conectadas.append(r)
                letras |= ls
                cambia = True
    _pa_prudencia(ctx, conectadas, pide)                  # U.4: un numero que sobra sin saber por que
    _pa_sin_callejones(conectadas, pide)
    _pa_comprobar_cosas(ctx, conectadas)                  # U.3b: nada junta cosas distintas
    _pa_medida_compuesta(ctx, conectadas)                 # M.23: '3 m y 25 cm' no son dos medidas de lo mismo
    for r in list(conectadas):
        for l in _u_letras_rel(r["rel"]):
            letras.add(l)
    no_leidas = [l for l in lecturas if l["error"]]
    for l in no_leidas:                                   # una frase rara que podria cambiar la respuesta: no se adivina
        nombres = set()
        for e in ctx["entes"]:
            if set(e["versiones"]) & letras:
                nombres.update(e["clave"])
        suyas = set(_pa_singular(w) for w in l["palabras"]) | l["palabras"]
        de_otro = any(set(e["clave"]) & suyas for e in ctx["entes"] if not set(e["versiones"]) & letras)
        if l["cambio"] or (suyas & nombres) or (l["dato"] and not de_otro):
            raise ValueError("no entiendo esta frase: '%s' (%s), y podria cambiar la respuesta"
                             % (l["frase"], l["error"]))
    cantidades = []
    for p in pide:
        cantidades.append(p)
    for r in ctx["rels"]:
        if r in conectadas:
            for l in _u_letras_rel(r["rel"]):
                if l not in cantidades:
                    cantidades.append(l)
    con_pedido = list(conectadas)
    con_pedido.extend(r for r in ctx["rels"] if r.get("pedido"))
    unidades = _pa_unidades(ctx, con_pedido)
    tipos = {}
    for e in ctx["entes"]:
        for v in e["versiones"]:
            tipos[v] = e["tipo"] if not set(e["clave"]) & ctx["voc"]["negativos"] else "puede_negativo"
    return {"cantidades": cantidades, "relaciones": [r["rel"] for r in ctx["rels"] if r in conectadas],
            "tipos": tipos, "negativos": ctx["voc"]["negativos"], "que_es": ctx["que_es"],
            "expresion": None, "texto": " ".join(_pa_normal(texto).split()), "pide": pide, "palabras": True,
            "lecturas": lecturas, "apuntes": ctx["rels"], "conectadas": conectadas, "unidades": unidades,
            "cosas": {l: c for l, c in _pa_cosas_de_letras(ctx).items() if l in cantidades}}


def _pa_hay_numero(e):
    if e[0] == "num":
        return True
    if e[0] in ("par", "neg"):
        return _pa_hay_numero(e[1])
    if e[0] == "op":
        return _pa_hay_numero(e[2]) or _pa_hay_numero(e[3])
    return False


def _pa_numeros_de(e):
    if e[0] == "num":
        return [_nu_texto(e[1])]
    if e[0] in ("par", "neg"):
        return _pa_numeros_de(e[1])
    if e[0] == "op":
        out = _pa_numeros_de(e[2])
        out.extend(_pa_numeros_de(e[3]))
        return out
    return []


def _pa_prudencia(ctx, conectadas, pide):
    """LA REGLA DE PRUDENCIA (U.4, decision de Carlos): nunca una respuesta falsa.  Un dato que se queda FUERA (su
    relacion no esta conectada con lo que se pide) sobra de verdad si es de otra cosa (la edad en un problema de
    canicas) o de otro dueno (los caramelos de Ana cuando se pregunta por los de Luis).  Pero si CUENTA las mismas cosas
    por las que se pregunta ('un camion lleva 12 CAJAS' cuando se pregunta lo que pesan las cajas), no se sabe por que
    sobra: algo se leyo mal, y se dice que numero y que frase."""
    cosas = _pa_cosas_de_letras(ctx)

    def claves(letras):                                    # los nombres de las COSAS (no personas, no 'lo de alguien')
        out = []
        for e in ctx["entes"]:
            if set(e["versiones"]) & set(letras) and not e.get("dueno") and not e.get("persona"):
                out.append(tuple(e["clave"]))
        return out

    dentro = set(pide)
    for r in conectadas:
        dentro.update(_u_letras_rel(r["rel"]))
    cosas_dentro = [cosas[l] for l in dentro if cosas.get(l)]
    claves_dentro = claves(dentro)
    for r in ctx["rels"]:
        if r in conectadas or r.get("pedido") or r.get("sabido") or not (
                _pa_hay_numero(r["rel"][0]) or _pa_hay_numero(r["rel"][1])):
            continue
        letras = _u_letras_rel(r["rel"])
        mias = [(cosas[l], claves_dentro) for l in letras if cosas.get(l)]
        mias.extend((c, claves_dentro) for c in claves(letras))
        mias.extend((c, cosas_dentro) for c in claves(letras))
        for c, contra in mias:
            if c and any(d and _pa_misma_cosa(ctx, c, d) for d in contra):
                numeros = _pa_numeros_de(r["rel"][0])
                numeros.extend(_pa_numeros_de(r["rel"][1]))
                raise ValueError("no se que hacer con el %s de '%s': cuenta %s, lo mismo que la pregunta, y no lo uso "
                                 "(algo he leido mal)" % (" y el ".join(numeros), r["frase"], " ".join(c)))


def _pa_sin_callejones(conectadas, pide):
    """Una relacion con una cantidad que no sale en NINGUNA otra y que no se pide solo dice cuanto vale esa cantidad
    (el perimetro, cuando se pregunta el lado por el area): no ayuda a lo que se pide, sobra."""
    cambia = True
    while cambia:
        cambia = False
        for r in list(conectadas):
            for l in _u_distintas(_u_letras_rel(r["rel"])):
                if l in pide:
                    continue
                if not [x for x in conectadas if x is not r and l in _u_letras_rel(x["rel"])]:
                    conectadas.remove(r)
                    cambia = True
                    break


def _pa_unidades(ctx, rels):
    """La unidad de cada cantidad: la de su frase; y la comparten las de una misma relacion (que no sea de figura)."""
    u = dict(ctx["unidad_de"])
    for e in ctx["entes"]:
        if e["tipo"] == "cuenta":
            for v in e["versiones"]:
                u[v] = e["nombre"].replace("_", " ")
    medidas = ctx["voc"]["unidades"]
    rels = sorted(rels, key=lambda r: 0 if (r.get("unidad") or "").split(" ")[0] in medidas else 1)
    cambia = True
    while cambia:                                         # primero las unidades de verdad (pesos), luego las cosas
        cambia = False
        for r in rels:
            ls = _u_distintas(_u_letras_rel(r["rel"]))
            uni = r.get("unidad")
            if r["porque"] in ("grupos_iguales", "lo de cada uno") or r.get("sabido") and r["porque"] != "precio" \
                    and r["porque"] != "vuelta":
                continue
            if uni is None or uni.split(" ")[0] not in medidas:
                conocidas = [u[l] for l in ls if l in u and (uni is None or u[l].split(" ")[0] in medidas)]
                uni = conocidas[0] if conocidas else uni
            if uni is None:
                continue
            for l in ls:
                if l not in u:
                    u[l] = uni
                    cambia = True
    for e in ctx["entes"]:                                 # lo de CADA uno: en lo que se reparte
        if e.get("unidad_tasa") and e["versiones"][0] not in u:
            u[e["versiones"][0]] = e["unidad_tasa"].replace("_", " ")
    for e in ctx["entes"]:                                 # el area en unidades cuadradas, el volumen en cubicas
        fg = e.get("figura")
        if e["tipo"] != "medida" or fg is None or e["nombre"] in u:
            continue
        lineal = next((u[x["nombre"]] for x in ctx["entes"] if x.get("figura") is fg and x["nombre"] in u
                       and x["clave"][0] not in fg["cuadradas"] and x["clave"][0] not in fg["cubicas"]), None)
        if lineal is None:                             # '36 cm cuadrados de area': el lado, en cm
            lineal = next((re.sub(r"\s*(cuadrad|cubic)\w*$|[23]$", "", u[x["nombre"]]) for x in ctx["entes"]
                           if x.get("figura") is fg and x["nombre"] in u), None)
        if lineal is None:
            continue
        if e["clave"][0] in fg["cuadradas"]:
            u[e["nombre"]] = "%s cuadrados" % lineal
        elif e["clave"][0] in fg["cubicas"]:
            u[e["nombre"]] = "%s cubicos" % lineal
        else:
            u[e["nombre"]] = lineal
    return u


def es_problema_con_palabras(texto, saber=None):
    """Lo lee el lector de palabras (y tiene una pregunta)."""
    if saber is None:
        saber = cargar_conocimiento()
    if not re.search(r"[a-zA-Z]{3,}", _pa_normal(texto)):
        return False
    try:
        _pa_leer(texto, saber)
    except Exception:
        return False
    return True


def _pa_le_toca(texto, conclusion_vieja, saber):
    """LA RED DE SEGURIDAD DE LAS PALABRAS (U.3): la puerta vieja de un problema con palabras (R.1, R.2, la escala...) no
    llega (no entiende, todavia no, no sabe resolverlo), y el lector de palabras lo lee y el buscador lo resuelve y lo
    comprueba: contesta el.  Si no, se queda lo de la puerta (nada viejo cambia)."""
    if conclusion_vieja not in ("no_entiendo", "todavia_no", "no_se_resolver"):
        return False
    if es_expresion_simbolica(texto) or not re.search(r"[a-z]{3,}", _pa_normal(texto)):
        return False
    try:
        r = decidir_resolver(texto, saber)
    except Exception:
        return False
    return r["conclusion"] == "hecho" and r.get("modelo", {}).get("palabras", False)


def _pa_conclusion_de_salida(salida):
    """La conclusion de lo que contesto una puerta vieja (la ultima linea 'RESULTADO: ...', o 'NO ENTIENDO')."""
    if salida.startswith("NO ENTIENDO"):
        return "no_entiendo"
    lineas = salida.strip().splitlines()
    if lineas and lineas[-1].startswith("RESULTADO:"):
        return lineas[-1][len("RESULTADO:"):].strip()
    return None


def _pa_explicar_lectura(m, saber):
    """Lo que leyo de cada frase: sus relaciones, lo que no entendio, lo que sobra."""
    L = ["  LEO frase a frase (STUDENT / Bakman: cada frase da relaciones pequenas; frases.kn y relaciones.kn):"]
    conectadas = m["conectadas"]
    for l in m["lecturas"]:
        cabeza = "     %s'%s'" % ("(pregunta) " if l["pregunta"] else "", l["frase"])
        if l["error"]:
            L.append("%s  ->  NO LA ENTIENDO (%s); con el resto basta" % (cabeza, l["error"]))
            continue
        rels = m["apuntes"][l["desde"]:l["hasta"]]
        if not rels:
            L.append("%s  ->  (lo que se pide)" % cabeza if l["pregunta"] else "%s  ->  (nada que apuntar)" % cabeza)
            continue
        L.append(cabeza)
        for r in rels:
            if r.get("pedido"):
                L.append("         ->  se pide: %s" % r["pedido"])
                continue
            sobra = "" if r in conectadas else "   (sobra: no tiene que ver con la pregunta)"
            L.append("         ->  %s   [%s]%s" % (_u_rel_texto(r["rel"]), r["porque"].replace("_", " "), sobra))
    sabidas = [r for r in m["apuntes"] if r.get("sabido")]
    if sabidas:
        L.append("     LO QUE SE SABE (relaciones.kn), aunque el texto no lo diga:")
        for r in sabidas:
            sobra = "" if r in conectadas else "   (sobra)"
            L.append("         ->  %s   [%s]%s" % (_u_rel_texto(r["rel"]), r["frase"], sobra))
    tiempos = [(n, q) for n, q in m["que_es"].items() if n in m["cantidades"]]
    if tiempos:
        L.append("     EN EL TIEMPO:")
        for n, q in tiempos:
            L.append("         %s = %s" % (n, q))
    cosas = m.get("cosas") or {}
    if cosas:                                             # U.3b: de que cosa es cada cantidad
        L.append("     DE QUE COSA ES CADA CANTIDAD (solo se suman o restan las de la misma cosa):")
        L.append("         %s" % "; ".join("%s: %s" % (l, " ".join(c)) for l, c in cosas.items()))
        L.append("         COMPRUEBO LAS COSAS: ninguna relacion junta cosas distintas")
    L.append("     SE PIDE: %s" % ", ".join(m["pide"]))
    L.append("")
    return L


def _pa_razonable(valores, modelo, saber):
    """CAPA 4 (comprobar si es razonable, E.6): una cantidad de cosas, un precio o una medida no puede ser negativa (la
    temperatura y los numeros si); una CUENTA de cosas (cuantos pajaros, cuantas bolsas) es entera.  Devuelve el porque
    si algo no es razonable, o None."""
    for letra, v in valores.items():
        tipo = modelo["tipos"].get(letra, "pedido")
        u = modelo["unidades"].get(letra) or ""
        if tipo in ("numero", "puede_negativo") or set(u.split()) & modelo["negativos"]:
            continue
        if v[0] == "-" and not _nu_es_cero(v):
            return "%s saldria %s: no puede ser menos de cero (no se puede quitar mas de lo que hay)" % (
                letra, _nu_texto(v))
        if tipo == "cuenta" and v[2] != 1:
            return ("%s saldria %s: no es un numero entero de %s (repartir con lo que SOBRA es la division con resto, "
                    "R.2)" % (letra, _nu_texto(v), letra))
    return None


def _pa_respuesta(valores, modelo):
    """La respuesta: lo que se pide, con su unidad."""
    out = []
    for p in modelo["pide"]:
        v = _nu_texto(valores[p])
        u = modelo["unidades"].get(p)
        out.append("%s %s" % (v, u) if u else v)
    if len(out) == 1:
        return out[0]
    return "%s y %s" % (", ".join(out[:-1]), out[-1])
