# Diario — 3 de octubre de 2026 — Fallo encontrado por Carlos en la 2.1: la identidad no se aplicaba

## Lo que probó Carlos (ya en el móvil)

```
contar: casa(color=blanco), casa, perro, casa(forma=cuadrado), carro
```

Y el sistema contestó **cinco palabras**, una por cada mención escrita:
`casa(color=blanco) -> uno`, `casa -> dos`, `perro -> tres`, `casa(forma=cuadrado) -> cuatro`,
`carro -> cinco`.

## Por qué está mal

**Mal por dos motivos, y los dos son graves:**

1. **No aplicaba la regla de identidad** que el propio Carlos fijó en la 0.1: `casa(color=blanco)`,
   `casa` y `casa(forma=cuadrado)` **no se contradicen**, así que son **la misma casa** y sus datos
   **se suman** → una casa blanca y cuadrada. La colección tiene **tres** objetos (casa, perro, carro),
   no cinco.
2. **Ni siquiera parseaba los atributos**: mostraba `casa(color=blanco)` como si ese texto entero
   fuera el **nombre** del objeto. En la 2.1 estaba entrando por la vía simple (`escena_0_1`, que es
   solo nombres separados por comas) en vez de por la vía con atributos.

## La causa de fondo (la lección)

La unidad 2.1 se escribió sobre colecciones de **nombres simples** (`a, a, a`), y ahí funcionaba.
Pero en cuanto los objetos traen atributos, hay que pasar por **el mismo camino que 0.1/0.2**:

```
escena_0_2(...)   -> parsea atributos
entidades_reales(...)  -> fusiona lo que es la misma cosa y separa lo que se contradice
```

**Regla para el futuro** (anotada en el skill): *toda unidad nueva que reciba objetos pasa por
`escena_0_2` + `entidades_reales`. No se reimplementa la identidad ni se usa la vía simple.*

Es la **tercera vez** que aparece el mismo patrón: una unidad nueva que no reutiliza lo que ya sabe la
anterior. Las otras dos fueron el vocabulario de «grupo» y la separación de entidades.

## El arreglo

- `decidir_2_1_contar` y `decidir_2_1_revisar` ya aplicaban `entidades_reales`; el fallo estaba en
  **el parseo de la entrada**.
- Cambiado en `motor.py` (`explicar_pregunta`) y en `probar.py`: `escena_0_1` → **`escena_0_2`**.
- **Formato arreglado también**: los nombres largos se pegaban a la flecha
  (`casa(color=blanco) -> uno` salía en la misma línea del encabezado). Ahora el ancho se calcula
  según el nombre más largo (`_cabecera_emparejamiento`).

## Salida correcta, verificada

```
PREGUNTA (2.1): empareja UNA palabra con CADA objeto, en orden
COLECCION:
    casa  [color=blanco, forma=cuadrado]
    perro
    carro
  (los nombres repetidos son el MISMO objeto: no dan dos palabras)
  EMPAREJAMIENTO (una palabra por objeto, ninguna repetida):
    casa       -> uno
    perro      -> dos
    carro      -> tres
RESULTADO: emparejado
```

## Pruebas añadidas (para que no vuelva a pasar)

- **D4** — exactamente el caso de Carlos: tres menciones de la casa → **una** casa, tres palabras.
- **D5** — el contraste: `casa(color=blanco), casa(color=rojo)` → **dos** casas (`casa#1`, `casa#2`).
- **D6** — con atributos y un repetido de verdad: `silla(color=azul), silla(color=azul), mesa` →
  dos palabras.

Y dos casos más en `mis_casos.txt` (37 en total).

## Medición

```
0.1: 8/8   0.2: 29/29   0.3: 15/15   1.0: 13/13   2.1: 18/18
TOTAL: 83/83   RESULTADO GLOBAL: VERDE
Casos de Carlos: 37 bien, 0 fallan
```

## Reenviado

Se regeneró `movil\euclides_movil.py` con el arreglo y se probó con el caso de Carlos **desde el
archivo del móvil**, no desde el proyecto: contesta tres objetos y los casos dan 37/37.
