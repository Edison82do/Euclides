# Diario — 3 de octubre de 2026 — Dos observaciones de una prueba de Carlos

Carlos probó (en el móvil):

```
dame: casa(color=rojo), casa(forma=cuadrado), pero, carro / dos
```

Y salió bien. Pero de esa prueba salen **dos cosas** que conviene dejar escritas.

## 1. Tres unidades encadenadas funcionando (esto es bueno)

Fíjate en el montón que entiende el sistema:

```
MONTON (lo que me dan, no me lo invento):
    casa  [color=rojo, forma=cuadrado]
    pero
    carro
```

Carlos escribió **cuatro** cosas y el sistema ve **tres**, porque:

- **unidad 0.1** (identidad): `casa(color=rojo)` y `casa(forma=cuadrado)` **no se contradicen** → son
  **la misma casa**, y sus datos **se suman** → una casa roja y cuadrada. Esa es la regla que fijó
  Carlos en su día, y funciona **dentro** de una unidad posterior.
- **unidad 2.1** (correspondencia): una palabra por objeto.
- **unidad 2.4** (cardinalidad): coge dos del montón, verifica, y deja lo que sobra.

Es la primera vez que se ve una cadena de **tres unidades** cooperando en una sola respuesta. El
sistema no reimplementa: cada capa usa lo que sabe la anterior.

## 2. Mejora de transparencia (hecha)

Antes decía *qué* cogía, pero no *por qué esos y no otros*. Ahora lo dice:

```
  COJO (2 objetos):
    casa       -> uno
    pero       -> dos
  (cojo los PRIMEROS del monton, en el orden en que me los das)
  DEJO (no me los llevo): carro
```

Es la regla del proyecto: **nada de cajas negras**. Una elección que el sistema hace por su cuenta
tiene que estar dicha, aunque sea trivial.

## 3. Un hallazgo para la pieza del LENGUAJE (anotado, no arreglado)

Carlos escribió **«pero»** (parece que quería decir «perro»), y el sistema lo aceptó como un objeto
llamado *pero*, tan tranquilo.

**Y eso es correcto por ahora**: para el sistema, los nombres son **identificadores**, y no sabe qué
palabras existen en español. «pero» es para él tan válido como «casa».

Pero apunta a algo real, y es de la **tercera pieza** del proyecto (el lenguaje, que va aparte):
en una frase, «pero», «y», «con», «que» son **palabras del idioma**, no nombres de cosas. Hoy el
sistema no puede distinguirlas, porque **todavía no lee frases**: lee listas.

Queda anotado para cuando se aborde el lenguaje. Hoy no es un fallo: es un límite declarado.
