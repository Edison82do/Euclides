# -*- coding: utf-8 -*-
"""
Euclides - EL MOTOR DE PIEZAS (paso 2 del plan, idea de Carlos del 5 oct 2026).

Este archivo es UNA PARTE del motor (ver sistema/partes/__init__.py).

LA IDEA (Carlos): "tengamos una base de datos de codigos, asi el motor lo hala y aplica al problema
uno a uno y no estan en el motor principal.  Aunque haya que programarlo a mano, se le programara
una sola vez y el lo que debera es saberlo usar."

ASI QUE: cada CONOCIMIENTO que se usa para resolver es una PIEZA, un archivo propio en
conocimiento/piezas/, con:
    PIEZA = {"id", "nombre", "unidad", "responde", "que_hace", "condiciones", "usa", "rapidez"}
    def hacer(situacion, u): ...
  - "responde": a que PREGUNTA responde ('paso' de un problema, 'sumar', 'restar', ...).
  - "condiciones": [(condicion, por que se descarta si falla), ...]  (las condiciones estan en
    conocimiento/piezas/_condiciones.py: se escriben UNA vez y las usan todas las piezas).
  - "usa": las otras piezas o preguntas que necesita, y las lecciones del curriculo ('7.1'...).
  - hacer(situacion, u): lo hace.  'u' le da SOLO lo que la pieza puede usar: el MECANISMO
    (recitar, dedos, leer cifras) y, si las declaro en "usa", otras piezas (u.usar) y lecciones
    (u.leccion).  Usar algo no declarado es un ERROR: asi el mapa del conocimiento es verdad.

Y ESTE MOTOR NO SABE MATEMATICAS: solo sabe cargar las piezas, probarlas TODAS contra la situacion,
descartar las que no encajan diciendo POR QUE, y aplicar la que queda, como manda la politica de
cada pregunta (conocimiento/piezas/_objetivos.py).  Una pieza nueva NO toca este archivo.
"""

import importlib.util
import os
import sys  # noqa: F401


class NoSalio(Exception):
    """Una pieza que encajaba no pudo terminar (por ejemplo, una cuenta que se pasa de mil)."""


_CACHE_PIEZAS = {}

# Las lecciones del curriculo que una pieza puede pedir (si las declara en "usa").
_LECCIONES = {
    "7.1": "decidir_7_1_dedos",
    "7.2": "decidir_7_2_derivar",
    "7.4": "decidir_7_4_resta_dedos",
    "7.6": "decidir_7_6_columnas",
}

_CAMPOS = ("id", "nombre", "unidad", "responde", "que_hace", "condiciones", "usa")


def dir_piezas():
    return os.path.join(RAIZ, "conocimiento", "piezas")


def _importar(ruta, nombre):
    spec = importlib.util.spec_from_file_location("euclides_pieza_" + nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cargar_piezas(directorio=None):
    """Carga todas las piezas de la carpeta (una vez; si un archivo cambia, se vuelve a cargar).
    Devuelve {"piezas", "condiciones", "de_aplicacion", "objetivos", "problemas"}."""
    directorio = directorio or dir_piezas()
    firma = tuple(sorted((e.name, e.stat().st_mtime_ns, e.stat().st_size)
                         for e in os.scandir(directorio) if e.name.endswith(".py")))
    guardado = _CACHE_PIEZAS.get(directorio)
    if guardado and guardado[0] == firma:
        return guardado[1]
    base = {"piezas": {}, "condiciones": {}, "de_aplicacion": set(), "objetivos": {},
            "problemas": [], "directorio": directorio}
    for nombre in sorted(os.listdir(directorio)):
        if not nombre.endswith(".py"):
            continue
        ruta = os.path.join(directorio, nombre)
        stem = nombre[:-3]
        try:
            mod = _importar(ruta, stem)
        except Exception as e:                      # una pieza rota se dice; no tumba al resto
            base["problemas"].append("%s no se puede cargar: %s" % (nombre, e))
            continue
        if stem == "_condiciones":
            base["condiciones"].update(getattr(mod, "CONDICIONES", {}))
            base["de_aplicacion"] |= set(getattr(mod, "DE_APLICACION", ()))
            continue
        if stem == "_objetivos":
            base["objetivos"].update(getattr(mod, "OBJETIVOS", {}))
            continue
        p = getattr(mod, "PIEZA", None)
        hacer = getattr(mod, "hacer", None)
        if not isinstance(p, dict) or not callable(hacer):
            base["problemas"].append("%s no tiene PIEZA y hacer()" % nombre)
            continue
        falta = [c for c in _CAMPOS if c not in p]
        if falta:
            base["problemas"].append("%s: le faltan los campos %s" % (nombre, falta))
            continue
        if p["id"] != stem:
            base["problemas"].append("%s: su id es '%s' y tiene que ser el nombre del archivo"
                                     % (nombre, p["id"]))
            continue
        pieza = dict(p)
        pieza["hacer"] = hacer
        pieza["archivo"] = nombre
        pieza.setdefault("rapidez", 50)
        base["piezas"][p["id"]] = pieza
    # LAS COMPROBACIONES DEL MAPA: que todo lo que se nombra exista
    preguntas = {p["responde"] for p in base["piezas"].values()}
    for p in base["piezas"].values():
        for c in p["condiciones"]:
            if c[0] not in base["condiciones"]:
                base["problemas"].append("%s: la condicion '%s' no existe en _condiciones.py"
                                         % (p["id"], c[0]))
        for u in p["usa"]:
            if u not in base["piezas"] and u not in preguntas and u not in _LECCIONES:
                base["problemas"].append("%s: usa '%s', y eso no lo sabe nadie" % (p["id"], u))
        if p["responde"] not in base["objetivos"]:
            base["problemas"].append("%s: responde a '%s', que no esta en _objetivos.py"
                                     % (p["id"], p["responde"]))
    _CACHE_PIEZAS[directorio] = (firma, base)
    return base


class _Lo_que_puede_usar:
    """Lo que se le da a una pieza: el mecanismo, y lo que haya declarado en 'usa'."""

    def __init__(self, pieza, base, saber):
        self._pieza, self._base, self.saber = pieza, base, saber
        # el MECANISMO (mecanismo.py): siempre disponible
        s = saber
        self.siguiente = lambda p: siguiente(p, s)
        self.anterior = lambda p: anterior(p, s)
        self.leer = lambda p: leer(p, s)
        self.decir = lambda n: decir(n, s)
        self.viene_despues = lambda p, q: viene_despues(p, q, s)
        self.contar_adelante = lambda a, b, con_dedos=True: contar_adelante(a, b, s, con_dedos)
        self.contar_atras = lambda a, b, con_dedos=True: contar_atras(a, b, s, con_dedos)
        self.contar_hasta = lambda a, b: contar_hasta(a, b, s)
        self.levantar_dedos = lambda p: levantar_dedos(p, s)
        self.cifras_de = cifras_de
        self.escribir_cifras = escribir_cifras
        self.sumar_por_columnas = lambda a, b: sumar_por_columnas(a, b, s)
        # la MEMORIA de hechos (memoria.py): mirar si algo se sabe de memoria
        self.recuerdo = lambda clave: cargar_memoria().get(clave)

    def usar(self, nombre, **situacion):
        if nombre not in self._pieza["usa"]:
            raise RuntimeError("la pieza '%s' usa '%s' sin haberlo declarado en 'usa'"
                               % (self._pieza["id"], nombre))
        r = aplicar(nombre, situacion, self.saber, self._base)
        if r["conclusion"] != "hecho":
            raise NoSalio(r.get("porque") or r["conclusion"])
        return r

    def leccion(self, numero):
        if numero not in self._pieza["usa"]:
            raise RuntimeError("la pieza '%s' usa la leccion %s sin haberla declarado"
                               % (self._pieza["id"], numero))
        return globals()[_LECCIONES[numero]]


def aplicar(pregunta, situacion, saber=None, base=None):
    """
    EL CORAZON: prueba TODAS las piezas que responden a 'pregunta' contra la 'situacion'.
    Devuelve {"conclusion": hecho | imposible | ninguna | ambiguo | no_salio, "candidatos": [...],
              "pieza": la elegida, "resultado": lo que hizo, "porque": ...}
    """
    if saber is None:
        saber = cargar_conocimiento()
    base = base or cargar_piezas()
    politica = base["objetivos"].get(pregunta, {}).get("elige", "todas_iguales")
    candidatas = sorted((p for p in base["piezas"].values() if p["responde"] == pregunta),
                        key=lambda p: (p["rapidez"], p["id"]))
    if not candidatas and pregunta in base["piezas"]:
        candidatas = [base["piezas"][pregunta]]          # se pidio una pieza por su nombre
    tabla, validas = [], []
    for p in candidatas:
        fila = {"id": p["id"], "nombre": p["nombre"], "unidad": p["unidad"]}
        for k, c in enumerate(p["condiciones"]):
            u = _Lo_que_puede_usar(p, base, saber)
            if not base["condiciones"][c[0]](situacion, u):
                fila["descartado"], fila["falla_en"], fila["pasadas"] = c[1], c[0], k
                break
        else:
            fila["aplica"] = True
            validas.append((p, fila))
        tabla.append(fila)
    r = {"pregunta": pregunta, "situacion": situacion, "candidatos": tabla}
    if not validas:
        cerca = [f for f in tabla if f.get("falla_en") in base["de_aplicacion"]]
        r["conclusion"] = "imposible" if cerca else "ninguna"
        r["porque"] = cerca[0]["descartado"] if cerca else \
            "ninguna pieza que tengo responde a '%s' en esta situacion" % pregunta
        return r
    hechos, fallos = [], []
    for k, (p, fila) in enumerate(validas):
        try:
            res = p["hacer"](situacion, _Lo_que_puede_usar(p, base, saber))
            hechos.append((p, res))
        except (NoSalio, ValueError) as e:      # una pieza dice que no le sale con ValueError
            fila["no_salio"] = str(e)
            fallos.append(str(e))
            continue
        if politica == "la_mas_rapida":
            # la mas rapida que SALE; las demas tambien servian: se dice, no se hacen
            r["tambien_servian"] = [q["id"] for q, _ in validas[k + 1:]]
            break
    if not hechos:
        r["conclusion"] = "no_salio"
        r["porque"] = fallos[0]
        return r
    if len({h[1]["valor"] for h in hechos}) > 1:
        r["conclusion"] = "ambiguo"
        r["porque"] = ", ".join("%s da %s" % (p["id"], res["valor"]) for p, res in hechos)
        return r
    r["conclusion"] = "hecho"
    r["pieza"], r["resultado"] = hechos[0]
    r["valor"] = r["resultado"]["valor"]
    r["tambien"] = [p["id"] for p, _ in hechos[1:]]
    return r


def mapa_del_conocimiento(base=None):
    """Que pieza usa que: el mapa, para verlo y para comprobar que no hay vueltas."""
    base = base or cargar_piezas()
    return {p["id"]: list(p["usa"]) for p in base["piezas"].values()}


def explicar_piezas(saber=None):
    base = cargar_piezas()
    L = ["PREGUNTA: que PIEZAS de conocimiento tengo y que usa cada una  (conocimiento/piezas/)", ""]
    por_pregunta = {}
    for p in base["piezas"].values():
        por_pregunta.setdefault(p["responde"], []).append(p)
    for preg in sorted(por_pregunta):
        o = base["objetivos"].get(preg, {})
        L.append("  RESPONDEN A '%s'  (%s)" % (preg, o.get("que_es", "")))
        for p in sorted(por_pregunta[preg], key=lambda p: (p["rapidez"], p["id"])):
            L.append("    %-26s (%s)  usa: %s" % (p["id"], p["unidad"], ", ".join(p["usa"]) or "-"))
        L.append("")
    if base["problemas"]:
        L.append("  PROBLEMAS EN LAS PIEZAS:")
        L.extend("    - " + x for x in base["problemas"])
        L.append("")
    L.append("RESULTADO: %d piezas" % len(base["piezas"]))
    return "\n".join(L)
