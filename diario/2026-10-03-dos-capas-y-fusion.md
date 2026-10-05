# Diario — 3 de octubre de 2026 — Las dos capas, y la fusión del mismo objeto

## Lo que planteó Carlos

Dos cosas, en una sola frase, y las dos eran correctas.

### 1. «No comparten atributos, pero al saber que son dos cosas diferentes, tenemos un grupo; en
cuanto a atributos es no decidible»

Se refería a `casa(color=azul); carro`. Yo le había preguntado si un objeto sin atributos escritos
debía entenderse como «no sabemos» o como «no tiene». Él respondió mejor que mis tres opciones: **no hay
que elegir una respuesta, hay dos preguntas distintas.**

- «¿Son varias cosas?» → **sí, se sabe** (dos entidades distintas).
- «¿Comparten algún atributo?» → **no se sabe** (al carro no le hemos declarado atributos).

El fallo era mío: 0.2 devolvía un `no_decidible` pelado que **ocultaba** la información que la unidad
0.1 ya tenía. Ahora la respuesta lleva **las dos capas**:

```
ESCENA:
    casa  [color=azul]
    carro
PLURALIDAD (0.1): son VARIOS OBJETOS
  atributos que NO se saben: color
ATRIBUTOS (0.2): no_decidible
```

### 2. «Casa blanca y casa cuadrada es el mismo objeto hasta que un atributo lo distinga»

Y aquí destapó un segundo error: el sistema trataba **cualquier** mención repetida con atributos
distintos como contradicción. Pero `casa(color=blanco)` y `casa(forma=cuadrada)` **no se contradicen**:
son la misma casa descrita dos veces, y sus datos **se suman**.

Su razonamiento para que fuera así, que es el bueno: **si no, `casa, casa` sería un grupo**, y eso rompe
la unidad 0.1.

Regla nueva, fijada por escrito en `identidad_referencias.kn`:

| Caso | Qué pasa |
|---|---|
| Misma entidad, datos que **no** se contradicen | **Fusión**: sus atributos se suman, sigue siendo **un solo objeto** |
| Misma entidad, mismo atributo con **dos valores distintos** | **Contradicción** → `no_decidible`, el sistema no elige |

```
casa(color=blanco); casa(forma=cuadrada)  -> un_objeto  [color=blanco, forma=cuadrada]
casa(color=blanco); casa(color=rojo)      -> Aviso: se contradicen -> no_decidible
casa, casa                                -> un_objeto  (sigue bien: el nombre manda)
```

## Lo que se tocó

1. `conocimiento\identidad_referencias.kn` — reglas de **fusión** y **contradicción** escritas, con su porqué.
2. `sistema\motor.py` — función `fusionar()`: une las menciones del mismo identificador; marca como
   contradictoria solo la entidad con un atributo de dos valores distintos.
3. `sistema\motor.py` — las respuestas de 0.2 llevan ahora **PLURALIDAD (0.1)** y **ATRIBUTOS (0.2)**.
4. `sistema\motor.py` — la nota de fusión avisa correctamente: «se unen y sus datos se suman» cuando es
   fusión, y «SE CONTRADICEN» cuando es contradicción. (En la primera pasada el mensaje decía que se
   sumaban también en el caso contradictorio: mentira, corregido.)
5. `pruebas\test_0_2.py` — nueva sección **D) Las dos capas** (6 casos) y el caso D9 de fusión.

## Fallo de herramienta, arreglado en la herramienta

Por **tercera vez** el formato `.kn` falló con un ítem de lista partido en dos líneas. Las dos primeras
veces esquivé el problema escribiendo el ítem en una línea. Esta vez se arregló el **lector**: un ítem de
lista continúa en las líneas siguientes si llevan más sangría. *Arreglar la herramienta, no el camino.*

## Medición — salida real

```
Todas las pruebas del proyecto: 29/29   RESULTADO GLOBAL: VERDE
   0.1:  8/8
   0.2: 21/21  (9 de dominio + 4 de dominio al formar + 7 de robustez + 1 de fusión)
             (más 6 casos de «las dos capas», incluidos en 0.2)
Casos de Carlos: 12 bien, 0 fallan
```

Comprobado con la traza delante:

```
casa(color=azul); carro                       -> 0.1: varios_objetos | 0.2: no_decidible
casa; carro                                   -> 0.1: varios_objetos | 0.2: sin_atributo_comun
casa(color=azul)                              -> 0.1: un_objeto      | 0.2: una_sola_entidad
casa(color=blanco); casa(forma=cuadrada)      -> 0.1: un_objeto      | 0.2: una_sola_entidad  (fusionados)
casa(color=blanco); carro(color=negro)        -> 0.1: varios_objetos | 0.2: sin_atributo_comun
casa(color=blanco); casa(color=rojo)          -> 0.1: un_objeto      | 0.2: no_decidible  (se contradicen)
```

## Lección

**Una respuesta que se calla no es lo mismo que una respuesta honesta.** El sistema tenía razón al no
inventar el color del carro, pero se equivocaba al devolver un «no sé» que borraba lo que sí sabía. La
honestidad es decir **todo** lo que se sabe y **señalar** lo que no — no encogerse.

Y otra: **el mismo objeto descrito dos veces no son dos objetos.** Confundirlo rompía la unidad 0.1 entera.
