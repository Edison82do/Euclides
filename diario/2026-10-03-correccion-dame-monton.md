# Diario — 3 de octubre de 2026 — Corrección de la 2.4: `dame:` no puede inventarse los objetos

**El fallo de diseño más importante que se ha cazado hasta ahora, y lo cazó Carlos con una pregunta.**

## Lo que dijo Carlos

> «cuando dices "tiene" le das los objetos y le das una cantidad, el verifica, bien. pero cuando
> dices "dame" no le das los objetos solo la cantidad y de donde el saca los objetos?»

Tiene razón, y era un fallo grave.

## El fallo

La primera versión de `dame: tres` producía el conjunto así (línea 836 del motor):

```python
r["conjunto"] = [{"id": "cosa_%s" % secuencia[i], ...} for i in range(n)]
```

**El sistema se fabricaba los objetos.** No hay ningún sitio del que sacarlos, porque **el sistema no
tiene un mundo**: no existe un montón de cosas del que coger.

Y eso incumple la regla del proyecto:

> «Nada de cajas negras: toda respuesta del sistema se rastrea a una regla escrita **y a un dato
> escrito**. Si no se puede rastrear, no vale.»

Había regla, pero el **dato** se lo inventaba. Con `tiene:` no pasaba, porque los objetos los da quien
pregunta.

## La corrección (propuesta por Carlos)

Su idea, que es mejor que la mía: **que `dame` reciba el montón igual que `tiene`**, con la misma
forma:

```
dame:    a,b,c,d,e / tres     -> de estos cinco, dame tres
tiene:   a,b,c / tres         -> estos tres, tienen tres?
```

El montón va **antes** de la barra y la cantidad **después**, en los dos.

Y así el sistema **no crea objetos: elige**. Salida real:

```
PREGUNTA (2.4): de este monton, dame esta cantidad
MONTON (lo que me dan, no me lo invento):
    a
    b
    c
    d
    e
CANTIDAD QUE ME PIDEN: tres
  COJO (3 objetos):
    a          -> uno
    b          -> dos
    c          -> tres
  DEJO (no me los llevo): d, e

  VERIFICACION (cuento lo que he cogido): la ultima palabra es 'tres'
  cuadra con lo pedido: SI
```

## Y salieron dos honestidades nuevas

**1. Sin montón, no hay respuesta.** `dame: tres` a secas ya no se acepta:

```
NO ENTIENDO ESTO: dame necesita un MONTON del que coger.
   se escribe asi:  dame: <monton> / <cantidad>
   ejemplo:         dame: silla_1, silla_2, mesa / tres

El sistema no tiene objetos propios: no se inventa de donde coger.
```

**2. Si en el montón hay menos de los pedidos, no se inventa los que faltan.**

```
dame: a,b / tres
RESULTADO: no_hay_bastantes
  En el monton hay menos objetos que los que me pides, y NO me invento los que faltan.
```

Esa segunda es una trampa excelente, y es del mismo tipo que todas las demás del proyecto: la
respuesta honesta es «no puedo», no un relleno.

## Lo que se tocó

- `conocimiento\cardinalidad.kn` — reglas fijadas **1-bis** y **1-ter**, contando el fallo y el
  arreglo (para que no se repita).
- `conocimiento\reglas_2_4.kn` — Give-N reescrito; 2 primitivas nuevas (`faltan_objetos`,
  `hay_bastantes`); el orden de lectura montón/cantidad, documentado.
- `sistema\motor.py` — `decidir_2_4_dame(escena, palabra)`, explicación nueva, y el mensaje de
  «necesito un montón».
- `pruebas\test_2_4.py` — reescrito: 19 casos de Give-N + 16 de «tiene» + coherencia + robustez.
- `probar.py`, `mis_casos.txt` — sintaxis nueva.

## Medición

```
0.1: 8/8   0.2: 29/29   0.3: 15/15   1.0: 13/13
2.1: 18/18  2.2: 24/24  2.3: 14/14   2.4: 36/36
TOTAL DEL PROYECTO: 157/157   RESULTADO GLOBAL: VERDE
Casos de Carlos: 70 bien, 0 fallan
```

## La lección (al carné de errores y al método)

**El sistema no crea datos: si le falta la entrada, la pide o dice que no puede.**

Es la cuarta vez que aparece el mismo patrón de fondo (una unidad nueva haciendo algo por su cuenta en
vez de apoyarse en lo que ya hay), pero esta es la más grave, porque no era un fallo de coherencia sino
una **invención de datos**: exactamente lo que el proyecto existe para no hacer.

Es también la segunda vez que una pregunta de Carlos —no una prueba, una **pregunta**— destapa un
problema de fondo. La primera fue «¿qué hace el programa?».
