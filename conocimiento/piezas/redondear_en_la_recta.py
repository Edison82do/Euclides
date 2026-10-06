# -*- coding: utf-8 -*-
"""Pieza de REDONDEAR (paso N.2; Common Core 3.NBT.A.1), la que ENTIENDE: en la recta numerica.
Entre que dos decenas (o centenas) esta el numero?  Donde esta la mitad del camino?  De cual esta mas
cerca?  (La Progression de base diez: redondear se entiende en la recta; la regla viene despues.)
Las dos de los lados se ESCRIBEN (ceros en los sitios de la derecha = valor de posicion; la de arriba
saltando de diez o de cien, N.1); la mitad del camino tambien (un cinco a la derecha del sitio)."""

PIEZA = {
    "id": "redondear_en_la_recta",
    "nombre": "en la recta: de cual esta mas cerca",
    "unidad": "N.2",
    "responde": "redondear",
    "rapidez": 9,
    "que_hace": "busca las dos decenas (o centenas) de los lados y la mitad del camino, y mira de cual esta mas cerca",
    "condiciones": [
        ("se_puede_redondear", "el numero no esta en mi lista (hasta mil), o el sitio no es decena ni centena"),
    ],
    "usa": [],
}

# el sitio: (la cifra del sitio, las de su derecha, la de justo a la derecha, el salto, el nombre)
_SITIOS = {"decena": (1, (0,), 0, "diez", "decenas"), "centena": (2, (0, 1), 1, "cien", "centenas"),
           "millar": (3, (0, 1, 2), 2, "mil", "millares")}                     # N.3: tambien al millar


def hacer(s, u):
    n = s["n"]
    i, derecha, junto, salto, plural = _SITIOS[s["a"]]
    cif = u.cifras_de(n)
    while len(cif) <= i:
        cif.append(0)
    abajo_c = list(cif)
    for j in derecha:
        abajo_c[j] = 0
    abajo = u.escribir_cifras(abajo_c)
    if abajo == n:
        return {"valor": n, "metodo": "en la recta (N.2)", "abajo": n, "arriba": n, "mitad": None,
                "cuenta": "%d ya es un numero de %s justas (ceros a la derecha): se queda %d" % (n, plural, n),
                "vuelta": "", "vuelta_ok": True}
    arriba = u.saltar(abajo, salto)
    mitad_c = list(abajo_c)
    mitad_c[junto] = 5
    mitad = u.escribir_cifras(mitad_c)
    pasa = u.escribir_cifras([cif[j] for j in derecha])              # lo que pasa de abajo: se LEE
    falta = u.leer(u.contar_hasta(u.decir(n), u.decir(arriba)))                        # lo que falta: contando hacia arriba
    linea = "%d esta entre %d y %d.  La mitad del camino es %d." % (n, abajo, arriba, mitad)
    lejos = "  De %d a %d hay %d; de %d a %d hay %d." % (abajo, n, pasa, n, arriba, falta)
    if n == mitad:
        valor = arriba
        por = ("%d esta JUSTO en la mitad: no esta mas cerca de ninguna.  Por CONVENIO se sube: %d"
               % (n, arriba))
    elif u.viene_despues(u.decir(n), u.decir(mitad)):
        valor = arriba
        por = "%d pasa de la mitad (%d): esta mas cerca de %d" % (n, mitad, arriba)
    else:
        valor = abajo
        por = "%d no llega a la mitad (%d): esta mas cerca de %d" % (n, mitad, abajo)
    return {"valor": valor, "metodo": "en la recta (N.2)", "abajo": abajo, "arriba": arriba, "mitad": mitad,
            "cuenta": "%s%s\n%s" % (linea, lejos, por), "vuelta": "", "vuelta_ok": True}
