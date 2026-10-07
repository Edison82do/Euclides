# Paso M.13 — MULTIPLICAR Y DIVIDIR DECIMALES POR NÚMEROS ENTEROS — 7 oct 2026

Sigue al M.12. Es el segmento **2.19** de NCETM (Spine 2, Year 5): *Calculation: ×/÷ decimal fractions
by whole numbers*. En Common Core: **5.NBT.B.7** («multiplicar y dividir decimales hasta las centésimas
con estrategias basadas en el valor posicional y las propiedades de las operaciones; relacionar la
estrategia con un método escrito y explicar el razonamiento»).

## 1. EL PLAN (escrito antes de programar)

**La fuente.** La web de NCETM **no se puede abrir desde la nube** (el proxy la bloquea:
`EGRESS_BLOCKED www.ncetm.org.uk`). Los cinco puntos de enseñanza salen del índice de NCETM en el
buscador (página *primm-219-calculation-decimal-fractions-by-whole-numbers*). Falta leer el segmento
entero (ejemplos, representaciones) cuando Carlos pueda abrirlo en su PC.

1. **Punto 1:** «Los decimales (con un número entero de décimas o de centésimas) se pueden multiplicar
   por un número entero usando los hechos que ya se saben y **contando en décimas (unitising)**».
   4 × 7 décimas = 28 décimas, igual que 4 × 7 unidades = 28 unidades → 4 × 0.7 = 2.8.
2. **Punto 2:** «Multiplicar por 0.1 es lo mismo que dividir entre 10; por 0.01, lo mismo que dividir
   entre 100». Al dividir entre 10 las cifras **bajan un sitio** (a la derecha); entre 100, dos.
3. **Punto 3:** «Para multiplicar un número de una cifra por un decimal de hasta dos cifras decimales:
   se pasa el decimal a entero multiplicando por 10 o 100, se hace la cuenta con una estrategia
   adecuada, y se **ajusta** el producto dividiendo entre 10 o 100». 3.27 × 4 → 327 × 4 = 1308 → 13.08.
4. **Punto 4:** «Si el multiplicador es menor que uno, el producto es **menor** que el multiplicando; si
   es mayor que uno, es mayor». (Contra la idea de que multiplicar siempre agranda.)
5. **Punto 5:** «Para dividir un decimal de hasta dos cifras decimales entre un número de **una cifra**:
   se pasa a entero (× 10 o × 100), se divide con una estrategia adecuada y se ajusta el cociente
   (÷ 10 o ÷ 100)». 7.2 : 3 → 72 décimas : 3 = 24 décimas = 2.4.

- Viene de D.1/D.2 (la décima y la centésima como COSAS: 2.7 = 27 décimas), de M.9 (× y ÷ 10 y 100: las
  cifras suben o bajan de sitio), de M.10/M.11 (multiplicación y división cortas) y de F.5 (3 × 2/5:
  se cuentan los quintos). Prepara la 2.26/2.27 de 6.º (decimal por decimal) y los porcentajes.

**Cómo lo hace un humano sin calculadora (y así lo hará Euclides).**
- **Contar en la unidad pequeña (puntos 1, 3 y 5).** 0.3 es «3 décimas»; 3.27 son «327 centésimas».
  Se leen las cifras sin el punto (eso es × 10 o × 100: las cifras suben de sitio). Se hace la cuenta
  de ENTEROS con las piezas que ya hay (la tabla, la corta, partir…). El resultado está en décimas o
  centésimas: se vuelve a poner el punto (÷ 10 o ÷ 100: las cifras bajan de sitio). 12 décimas = 1.2.
- **En la división, si sobra algo, se cambia a la unidad más pequeña** (como en la resta y en la
  división corta: 1 décima = 10 centésimas). 1.3 : 4 → 13 décimas : 4 = 3 y sobra 1 → «escribo un cero
  detrás: 1.30 son 130 centésimas» → 130 : 4 = 32 y sobran 2 → 1300 milésimas : 4 = 325 → 0.325.
  Se llega hasta las milésimas (lo que ya conoce, D.2); si aún sobra, **todavía no** (redondear el
  cociente es de 6.º).
- **Por 0.1 y por 0.01 (punto 2):** 35 × 0.1 → las cifras bajan un sitio → 3.5. Entre 10 y entre 100
  con un decimal: 3.5 : 10 → 0.35. Es mover cifras, no calcular.
- **Comprobar con la operación contraria** (lección de la revisión de M.12): el producto se comprueba
  DIVIDIENDO (1.2 : 4 = 0.3); el cociente se comprueba MULTIPLICANDO (24 décimas × 3 = 72 décimas);
  por 0.1 se comprueba multiplicando por 10 (las cifras vuelven a subir).
- **El sentido del tamaño (punto 4):** al final se compara el producto con el decimal: por un número
  mayor que uno sale MÁS; por 0.1, MENOS.

**Lo que se construye.**
- Preguntas nuevas `multiplicar_decimal` (situación `{"x": "0.3", "n": 4}`) y `dividir_decimal`
  (`{"x": "7.2", "d": 3}`), las dos «la más rápida».
- Pieza `multiplicar_decimal_contando_partes` (rapidez 5; puntos 1 y 3): cuenta el decimal en su unidad
  pequeña, multiplica enteros con la pregunta `multiplicar`, vuelve a poner el punto; **vuelta**: el
  producto entre el entero con `dividir_decimal` tiene que dar el decimal de antes.
- Pieza `multiplicar_por_una_decima` (rapidez 2; punto 2): un entero o decimal por 0.1 o 0.01 → las
  cifras bajan uno o dos sitios; **vuelta**: × 10 o × 100 (las cifras suben) da lo de antes.
- Pieza `dividir_decimal_contando_partes` (rapidez 5; punto 5): divisor de una cifra (2 a 9); cuenta en
  la unidad pequeña, divide enteros con la pregunta `dividir`, si sobra cambia a la unidad siguiente
  (hasta las milésimas); **vuelta**: cociente × divisor (en la unidad pequeña, con `multiplicar`) =
  dividendo, sin resto.
- Pieza `dividir_decimal_por_10_o_100` (rapidez 2; punto 2): las cifras bajan uno o dos sitios;
  **vuelta**: × 10 o × 100.
- Parte nueva `sistema/partes/decimales_por.py`: lee `0.3 x 4`, `4 x 0.3`, `7.2 : 3`, `35 x 0.1`,
  `3.5 : 10` y lo explica (las dos lecturas: cosas y columnas, el sentido del tamaño, la vuelta).
- Lo que **todavía no**: decimal por decimal (`0.3 x 0.4`, 6.º), dividir entre un decimal, dividir entre
  números de dos cifras (11 a 99: división larga, 6.º), más de tres cifras detrás del punto, y los
  cocientes que no salen exactos hasta las milésimas.

**Las trampas.**
- `0.3 x 4` → 1.2 (no **0.12**: son 12 DÉCIMAS, no centésimas).
- `1.5 x 4` → 6 (no **4.20**: el error de multiplicar el entero y el decimal por separado y pegarlos;
  15 décimas × 4 = 60 décimas = 6; y no «6.0»).
- `0.25 x 4` → 1 (no 1.00, ni 0.100).
- `0.12 : 4` → 0.03 (no **0.3**: son 12 CENTÉSIMAS : 4 = 3 centésimas).
- `0.6 : 2` → 0.3 (no 3: el punto no se pierde).
- `1.3 : 4` → 0.325 (sobra: se cambia a centésimas y a milésimas).
- `0.4 x 0.1` y `0.3 x 0.4` → todavía no (decimal por decimal es de 6.º).
- `7.2 : 12` → todavía no (NCETM 2.19: entre un número de una cifra).
- `35 x 0.1` → 3.5: por menos de uno sale MENOS (punto 4); `0.3 x 4 = 1.2` es más que 0.3.

**Prueba de dominio.** Contra el testigo (Python en la prueba, con enteros: x en milésimas): una
muestra de productos decimal × entero (de una, dos y tres cifras decimales, enteros de 2 a 12 y
algunos mayores), los 2 órdenes (0.3 x 4 y 4 x 0.3); productos por 0.1 y 0.01; una muestra de
divisiones exactas y con cambio de unidad, y las que no salen; ÷ 10 y ÷ 100 con decimales. Cerca del
techo: 999.999, 99999.9 × 9, y que tarden menos de 2 s.

## RESULTADO (7 oct)

**Hecho, verde: proyecto 2309/2309 + 654/654.** `test_M13_decimales_por_enteros` 54/54; mis_casos 654/654;
mis_pruebas 174/174.

- Dos preguntas nuevas (`multiplicar_decimal`, `dividir_decimal`) y 4 piezas, sin tocar el motor de piezas.
  **Las cuatro se comprueban con la operación contraria** y `aplicar` las descarta si no cuadra:
  - `multiplicar_decimal_contando_partes` (rapidez 5): 3.27 x 4 = 327 centésimas x 4 = 1308 centésimas =
    13.08 (la cuenta de enteros la hace la pregunta `multiplicar`: la tabla, la corta, doblar y partir…).
    Vuelta: 13.08 : 4 con `dividir_decimal` tiene que dar 3.27.
  - `multiplicar_por_una_decima` (rapidez 2): 35 x 0.1 = 35 : 10 = 3.5. Vuelta: las cifras vuelven a subir.
  - `dividir_decimal_contando_partes` (rapidez 5): 7.2 : 3 = 72 décimas : 3 = 24 décimas. Si sobra, **sigue
    con lo que sobra** cambiándolo por la unidad más pequeña (como la división corta, sin rehacer la
    cuenta): 1.3 : 4 → 3 décimas y sobra 1 → 10 centésimas : 4 = 2 y sobran 2 → 20 milésimas : 4 = 5 →
    0.325. Vuelta: 325 milésimas x 4 = 1300 milésimas = 1.3.
  - `dividir_decimal_por_10_o_100` (rapidez 2): 3.5 : 10 = 0.35. Vuelta: x 10.
- Parte nueva `sistema/partes/decimales_por.py`: lee `0.3 x 4`, `4 x 0.3`, `35 x 0.1`, `7.2 : 3`,
  `3.5 : 10` (también con coma) y explica: contar en la unidad pequeña, la cuenta de enteros, el punto en
  su sitio, el OJO de la trampa (12 décimas, no 0.12), **otro camino por partes** (3.27 x 4 = 12 + 1.08,
  que explica por qué 1.5 x 4 no es 4.20), **el tamaño** del punto 4 (por 0.1 sale MENOS) y la vuelta.
- Todavía no (con su porqué): decimal por decimal (salvo 0.1 y 0.01), dividir entre un decimal, por o
  entre números de dos cifras (salvo 10 y 100; NCETM 2.19 dice «de una cifra»), más de tres cifras
  detrás del punto, y las divisiones que no salen exactas ni en milésimas (1 : 3).
- **Cerca del techo**: 111.111 x 9 = 999.999 y 999.999 : 7 = 142.857 salen; 999.999 x 9 y 2943.4 : 8
  (2 943 400 milésimas) pasan del millón contado en la unidad pequeña: todavía no (no se puede comprobar
  multiplicando). Todo en menos de 0.1 s.
- **Arreglo encontrado al medir el tiempo** (lección de la revisión de M.12): `5 x 999999` tardaba **76 s**
  porque `multiplicar_dando_la_vuelta` lo leía como 999 999 grupos de 5 y `sumar_iguales_saltando` /
  `sumar_iguales_uno_a_uno` daban 999 999 saltos/sumas. Ahora, con más de cien grupos, esas dos piezas
  dicen que así no se cuenta y se hace de otra manera (como `dividir_saltando`). Ahora tarda 0.01 s.
- Dominio contra el testigo (el módulo `decimal` de Python, solo en la prueba): 240 productos (una, dos y
  tres cifras decimales; por 1–9, 10 y 100; en los dos órdenes), 60 por 0.1/0.01, 250 divisiones (justas,
  cambiando de unidad y las que no salen), 100 entre 10/100 y 18 casos cerca del techo, cada uno < 2 s.
- **Falta la prueba de Carlos.** Y leer el segmento entero de NCETM 2.19 cuando se pueda abrir (desde la
  nube la web está bloqueada): si trae ejemplos o trampas que aquí no están, se añaden.
