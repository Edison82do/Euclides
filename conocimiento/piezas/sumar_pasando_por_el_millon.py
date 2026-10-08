# -*- coding: utf-8 -*-
"""Pieza de calculo: SUMAR PASANDO POR EL MILLON (paso N.6; NCETM 1.30, punto 4: 'lo que se sabe de cruzar los
miles sirve para llegar a los millones y cruzarlos').  Es "hacer diez" (7.2) con millones:
997 000 + 5 000:  a 997 000 le faltan 3 000 para el millon; de los 5 000 quedan 2 000; un millon y 2 000 = 1 002 000.
Lo que falta para el millon se saca POR LAS CIFRAS (cada una hasta nueve, la ultima hasta diez), sin columnas.
Un humano no pone 997 000 + 5 000 en columnas: completa el millon (punto 6: mental o escrito segun los numeros)."""

PIEZA = {
    "id": "sumar_pasando_por_el_millon",
    "nombre": "completar el millon y seguir",
    "unidad": "N.6",
    "responde": "sumar",
    "rapidez": 2,
    "que_hace": "si el primero esta justo debajo de un millon justo y la suma lo pasa: completa el millon y suma lo que queda",
    "condiciones": [
        ("la_suma_pasa_por_un_millon_justo",
         "el primero no esta justo debajo de un millon justo (le faltan mas de cien mil), o el segundo no llega a completarlo"),
        ("el_total_tiene_nombre", "el total se pasa de lo que se"),
    ],
    "usa": ["restar"],
}


def hacer(s, u):
    a, b = s["a"], s["b"]
    cif = u.cifras_de(a)
    millones = u.escribir_cifras(cif[6:])
    falta = u.lo_que_falta_para_el_redondo(a, 6)                     # por las cifras: 997000 -> 3000
    redondo = u.escribir_cifras([0, 0, 0, 0, 0, 0] + u.cifras_de(u.leer(u.siguiente(u.decir(millones)))))
    llega = u.sumar_por_columnas(u.escribir_cifras(cif[:6]), falta)  # comprobar el hueco: 997000 + 3000 = 1000000
    queda = u.usar("restar", a=b, b=falta)["valor"]                   # de los 5000, quito los 3000 que gaste
    escrito = u.cifras_de(queda)                                      # el millon justo y lo que queda, ESCRITO:
    while len(escrito) < 6:                                           # lo que queda en las seis cifras de la derecha
        escrito.append(0)
    escrito.extend(u.cifras_de(redondo)[6:])                          # y los millones del redondo a la izquierda
    total = u.escribir_cifras(escrito)
    if u.decir(total) is None:
        raise ValueError("%d + %d se pasa de lo que se" % (a, b))
    # LA VUELTA: al total le quito el segundo y tiene que salir el primero
    atras = u.usar("restar", a=total, b=b)["valor"]
    cuenta = ("%d + %d: a %d le faltan %d para %d (cada cifra hasta nueve, la ultima hasta diez); "
              "de los %d quedan %d (%d - %d = %d); %d y %d son %d"
              % (a, b, a, falta, redondo, b, queda, b, falta, queda, redondo, queda, total))
    return {"valor": total, "metodo": "pasar por el millon (N.6)", "cuenta": cuenta,
            "vuelta": "%d - %d = %d (y el hueco: %d + %d = %d)" % (total, b, atras, u.escribir_cifras(cif[:6]), falta, llega),
            "vuelta_ok": atras == a and llega == u.escribir_cifras([0, 0, 0, 0, 0, 0, 1])}
