# Diario — 3 de octubre de 2026 — La identidad: un atributo que distingue PRUEBA, no duda

## Lo que probó Carlos

```
carro(color=negro), carro(color=blanco)
```

y el sistema contestó:

```
  AVISO: la misma entidad viene descrita de formas que SE CONTRADICEN:
    carro  [color=negro]
    carro  [color=blanco]
PLURALIDAD (0.1): es UN OBJETO
ATRIBUTOS (0.2): no_decidible
```

Su respuesta: **«eso está mal. aunque tengan el mismo nombre, al tener el atributo del color distinto,
eso es prueba de que son varios objetos».**

Y tiene razón, por una razón lógica que él mismo ya había puesto por escrito antes sin que yo la
aplicara del todo:

> «una casa blanca y una casa cuadrada es el mismo objeto **hasta que un atributo lo distinga**»

Un atributo con **dos valores distintos** en el mismo nombre **es exactamente eso**: lo que las
distingue. Una misma cosa no puede ser negra y blanca a la vez. Así que no hay nada que decidir: **son
dos objetos.**

## El error de fondo

Yo había metido la contradicción como un caso de **duda** (`no_decidible`). Pero la contradicción en la
identidad es una **prueba de distinción**, no una duda. Es el principio de no contradicción aplicado a
la identidad:

- Si dos descripciones **pueden** ser de la misma cosa → son la misma (**fusión**).
- Si **no pueden** ser de la misma cosa → son cosas distintas (**separación**).

## El arreglo

`identidad_referencias.kn`, regla 3, reescrita. Las tres reglas de la identidad quedan así:

| Regla | Qué dice |
|---|---|
| 1 | Mismo identificador → misma entidad; identificadores distintos → entidades distintas |
| 2 (fusión) | Mismo identificador con datos que **no** se contradicen → **una** entidad, datos sumados |
| 3 (distinción) | Mismo identificador con un atributo y **dos valores distintos** → **entidades distintas**, se separan y se numeran (`carro#1`, `carro#2`) |

Resultado, ya funcionando:

```
ESCENA:
    carro  [color=negro]
    carro  [color=blanco]
  AVISO: un mismo nombre con datos que NO pueden ser la misma cosa:
  -> eso PRUEBA que son objetos DISTINTOS. Quedan asi: carro#1, carro#2
PLURALIDAD (0.1): son VARIOS OBJETOS
ATRIBUTOS (0.2): sin_atributo_comun
```

Y los otros dos casos siguen en su sitio, que es lo que importa:
- `casa(color=blanco); casa(forma=cuadrada)` → **un objeto** (los datos se suman: no se contradicen).
- `carro, carro` → **un objeto** (sin atributos, nada los distingue).

## Lo que se tocó

1. `conocimiento\identidad_referencias.kn` — regla 3 reescrita (distinción, no contradicción).
2. `conocimiento\reglas_0_2.kn` y `reglas_0_3.kn` — **eliminadas** las reglas de entidad contradictoria:
   ya no hay nada que decidir, la separación ocurre antes de llegar a las reglas.
3. `sistema\motor.py` — `fusionar()` se sustituye por `entidades_reales()`: une las menciones
   compatibles y **separa** las incompatibles, numerándolas. La primitiva
   `hay_entidad_contradictoria` desaparece.
4. Pruebas de 0.2 y 0.3 actualizadas, y añadidos los casos de Carlos (D8 y D9 de 0.3).

## Medición — salida real

```
Todas las pruebas del proyecto: 52/52   RESULTADO GLOBAL: VERDE
   0.1:  8/8
   0.2: 29/29
   0.3: 15/15
Casos de Carlos: 21 bien, 0 fallan
```

## Lección (al carné de errores)

**Una contradicción en la identidad no es una duda: es una prueba de distinción.** Cuando dos
descripciones de lo mismo no pueden ser ciertas a la vez, no hay que encogerse a `no_decidible` — hay
que concluir que son dos objetos. Y el criterio para separarlas ya lo había dado Carlos él mismo: el
atributo que las distingue.

**Van tres correcciones suyas en una sesión** (el crash, «grupo» con dos sentidos, y esta). Las tres
salieron de leer la respuesta del sistema y razonar sobre ella. El probador no es un extra: es lo que
está encontrando los fallos de diseño.
