# Paso M.15 — FACTORES, MÚLTIPLOS, PRIMOS Y COMPUESTOS — 7 oct 2026

Sigue al M.14. Es el segmento **2.21** de NCETM (Spine 2, Year 5): *Factors, multiples, prime numbers and
composite numbers*. En Common Core: **4.OA.B.4** («encontrar todas las parejas de factores de un número
del 1 al 100; saber que un número es múltiplo de cada uno de sus factores; decidir si un número del 1 al
100 es múltiplo de un número de una cifra; decidir si un número del 1 al 100 es primo o compuesto»).

## 1. EL PLAN (escrito antes de programar)

**La fuente.** La web de NCETM **sigue sin poder abrirse desde la nube** (`EGRESS_BLOCKED
www.ncetm.org.uk`, y también `ncetm.org.uk` y `cambridgemaths.org`). Los seis puntos de enseñanza salen
del índice de NCETM en el buscador (página *primm-221-factors-multiples-prime-numbers-and-composite-numbers*).
Falta leer el segmento entero (ejemplos y representaciones) cuando Carlos pueda abrirlo en su PC.

1. **Punto 1:** «Los factores son enteros positivos que se multiplican para dar un número».
2. **Punto 2:** «Se pueden usar métodos **sistemáticos** para encontrar todos los factores de un número;
   los factores van **por parejas**; todos los enteros positivos tienen un número **par** de factores salvo
   los números **cuadrados**, que tienen un número **impar**; los números con más de dos factores se llaman
   **compuestos**».
3. **Punto 3:** «Los números **primos** son enteros positivos que tienen **exactamente dos** factores».
4. **Punto 4:** «Un **factor común** es un factor que comparten dos o más números. Un **factor primo** es un
   factor que además es primo».
5. **Punto 5:** «Un **múltiplo** de un número es ese número por un entero; un **múltiplo común** es un
   múltiplo que comparten dos o más números».
6. **Punto 6:** «Las **parejas de factores de 100** sirven para calcular de forma eficiente».

Common Core 4.OA.B.4 y sus tareas (Illustrative Mathematics): los factores como los **lados de
rectángulos** (filas × columnas) que se pueden hacer con n cuadraditos; un primo solo se puede poner en
**una fila**.

Los errores típicos (Cambridge Maths *Espresso 43*; Haylock, cap. 14; Oak National, «checking
understanding of prime numbers»; resúmenes en el buscador):
- **«El 1 es primo»** (sale de la definición mal dicha «se divide entre 1 y entre sí mismo»): el 1 tiene
  UN factor, no dos; no es primo ni compuesto.
- **Confundir factor y múltiplo** («7 es múltiplo de 21»): los factores entran en la multiplicación, los
  múltiplos salen de ella.
- **Olvidar el 1 y el propio número** al dar los factores.
- **«Todos los impares son primos»** (9, 15, 21, 91 no lo son) y **«el 2 no es primo porque es par»**.
- **Dejarse parejas** por buscar sin orden; o seguir buscando **después del medio** (las parejas se
  repiten al revés).
- Creer que los primos son pequeños, o que un número grande siempre tiene un factor pequeño.

- Viene de M.0 (filas y columnas), G.1 (el área de un rectángulo), M.3/M.8 (dividir, con resto), las
  tablas hasta 12 × 12 (M.2–M.7), la divisibilidad de M.4/M.5/M.7 (`divisible: 51 entre 3`), contar de n
  en n (N.1, `saltar`), M.12 (doblar y partir) y M.14 (la pareja amiga 25 × 4). Prepara la 2.22.

**Cómo lo hace un humano sin calculadora (y así lo hará Euclides).**
- **Las parejas de factores, con orden (puntos 1 y 2).** Para 36: «¿1? 1 × 36. ¿2? 36 : 2 = 18, sin
  resto: 2 × 18. ¿3? 3 × 12. ¿4? 4 × 9. ¿5? 36 : 5 = 7 y sobra 1: no. ¿6? 6 × 6: **el mismo con él mismo**.
  ¿7? 36 : 7 = 5: el compañero ya es más pequeño que el 7 → ya me los encuentro al revés: **paro**».
  Cada prueba es una **división con resto** (M.8) que hace la pieza `dividir`; el niño para cuando el
  cociente se hace más pequeño que el que prueba (es «llegar al medio» sin raíces). Factores: 1, 2, 3, 4,
  6, 9, 12, 18, 36 (nueve: impar, porque 6 × 6 es un **cuadrado**). Los rectángulos: 1 fila de 36, 2 filas
  de 18, 3 de 12, 4 de 9, 6 de 6 (un cuadrado).
- **Respetar el año** (lección de M.12): las pruebas solo llegan hasta el **12** (las tablas). Si para
  llegar al medio hay que dividir entre 13 o más (169 en adelante), es la **división larga** (6.º):
  «todavía no».
- **Primo o compuesto (puntos 2 y 3).** Primero lo rápido, como un niño: **las reglas cortas** de M.4/M.5:
  par (y no es el 2) → 2 × la mitad; acaba en 0 o 5 (y no es el 5) → 5 × algo; las cifras suman 3, 6 o 9
  (y no es el 3) → 3 × algo. Eso dice **compuesto** con su pareja, aunque el número sea grande (1000 =
  2 × 500). Si ninguna regla encuentra factor, **se buscan las parejas**: si solo sale 1 × n, es **primo**
  (exactamente dos factores); si sale más, compuesto (91 = 7 × 13, ¡impar y compuesto!). **El 1**: un solo
  factor, ni primo ni compuesto.
- **La criba (Eratóstenes) para los primos hasta 100.** Se escriben del 2 al 100; se tachan los múltiplos
  del 2 **contando de 2 en 2** (N.1), luego del 3, del 5 y del 7; se para cuando el siguiente sin tachar,
  por sí mismo, ya se pasa del final (11 × 11 = 121). Lo que queda son los primos: 25. **Dos caminos**: la
  criba y las parejas tienen que decir lo mismo.
- **Múltiplos (punto 5).** Los de 7: contar de 7 en 7 (7, 14, 21…), cada uno es «7 × 1, 7 × 2…». «¿91 es
  múltiplo de 7?» = ¿91 se reparte en grupos de 7 sin que sobre? (`divisible`). Y al revés, «¿7 es factor
  de 91?» es la misma pregunta: 7 × 13 = 91.
- **Múltiplos comunes de 4 y 6**: se cuentan los del **grande** (6, 12, 18, 24…) y se mira cuáles son
  también de 4 (dividiendo): 12, 24, 36… El más pequeño: 12.
- **Factores comunes de 24 y 36**: las parejas de cada uno, y los que están en las dos listas: 1, 2, 3, 4,
  6, 12; el mayor: 12. **Factores primos de 60**: de sus factores, los primos: 2, 3, 5.
- **Las parejas de 100 (punto 6).** 1 × 100, 2 × 50, 4 × 25, 5 × 20, 10 × 10. Para 25 × 36: «36 = 9 × 4,
  y 25 × 4 = 100: 100 × 9 = 900». Es una técnica de multiplicar más.
- **Comprobar con la operación contraria** (lección de M.12): cada división que se probó se comprueba
  **multiplicando** (cociente × divisor + resto = n); cada pareja, multiplicando (4 × 9 = 36). En las parejas
  de 100, se deshace dividiendo (900 : 100 = 9, 9 × 4 = 36).

**Lo que se construye.**
- Pregunta nueva `parejas_de_factores` y pieza **`parejas_de_factores_en_orden`** (rapidez 10): prueba 1, 2,
  3… con `dividir` (con resto); para al cruzarse; si haría falta dividir entre 13, `ValueError` (todavía no).
  **Vuelta**: cada división, multiplicando de vuelta (cociente × divisor + resto = n).
- Pregunta nueva `primo` («la más rápida») con tres piezas:
  - **`primo_el_uno`** (rapidez 1): el 1 tiene un solo factor (1 × 1 = 1, comprobado multiplicando): ni primo
    ni compuesto.
  - **`compuesto_por_una_regla_corta`** (rapidez 3): par / acaba en 0 o 5 / sus cifras suman 3, 6 o 9 →
    compuesto, con la pareja (dividiendo). **Vuelta**: multiplicar la pareja y que dé n. Si ninguna regla
    encuentra factor, no le sale (`ValueError`) y pasa a la siguiente.
  - **`primo_buscando_parejas`** (rapidez 10): usa `parejas_de_factores`: una pareja → primo; más →
    compuesto. **Vuelta**: la de las parejas (cada división, multiplicando).
- Pieza **`multiplicar_con_las_parejas_de_100`** (pregunta `multiplicar`, rapidez 7: detrás de doblar y
  partir de M.12 para no cambiar lo que ya hacía; se pide con `con 100: 25 x 36`). **Vuelta**: dividir el
  producto entre 100 y multiplicar por el otro trozo (900 : 100 = 9, 9 × 4 = 36).
- Parte nueva `sistema/partes/factores.py` con las órdenes:
  `factores: 36` (las parejas, los rectángulos, cuántos, cuadrado o no, primo/compuesto) ·
  `primo: 37` (`es 37 primo`) · `primos hasta 100` (la criba, comparada con las parejas) ·
  `multiplos de 7` (los doce primeros, contando de 7 en 7) · `multiplos de 7 hasta 100` ·
  `91 es multiplo de 7` · `7 es factor de 91` · `factores comunes: 24 y 36` · `multiplos comunes: 4 y 6` ·
  `factores primos: 60` · `con 100: 25 x 36`.
- **Todavía no:** las parejas de un número que pide dividir entre 13 o más (desde 169), «primo» de un número
  impar grande sin regla corta (997), la descomposición en factores primos (60 = 2 × 2 × 3 × 5: es de 6.º /
  KS3), el mínimo común múltiplo y el máximo común divisor como técnica (aquí solo se dice el más pequeño /
  el mayor de las listas). Los números **cúbicos** no están en los puntos de 2.21 (el M.14 creía que sí): se
  quedan para cuando toquen.

**Las trampas.**
- `primo: 1` → **ni primo ni compuesto** (no «primo»).
- `primo: 2` → primo (aunque sea par); `primo: 91` → compuesto (7 × 13: impar y compuesto); `primo: 9` →
  compuesto; `primo: 51` → compuesto (5 + 1 = 6: 3 × 17).
- `factores: 36` → 1, 2, 3, 4, 6, 9, 12, 18, 36 (nueve: **impar**, el 6 va consigo mismo; no repetir el 6).
- `factores: 12` → incluye el 1 y el 12.
- `21 es multiplo de 7` → sí; `7 es multiplo de 21` → **no** (7 es FACTOR de 21).
- `multiplos de 7` empieza en 7 (7 × 1), no en 0 (en 5.º se cuentan desde el propio número).
- `factores: 169` → todavía no (habría que dividir entre 13: la división larga, 6.º).
- `primo: 1000` → compuesto (2 × 500) en menos de un segundo, aunque sea grande; `primo: 997` → todavía no.
- `factores comunes: 7 y 13` → solo el 1.
- `con 100: 25 x 36` → 900 (36 = 9 × 4; 25 × 4 = 100).

**Prueba de dominio.** Contra el testigo (Python, solo en la prueba): las parejas de factores de **todos**
los números del 1 al 168 (el número de factores, impar ⇔ cuadrado); primo o compuesto de todos los del 1 al
168, y una muestra de números grandes (compuestos por regla corta hasta el millón; impares sin regla →
todavía no); la criba hasta 100 = los 25 primos; múltiplos de 1 a 12 (los doce primeros y «hasta 100»);
«¿es múltiplo / factor?» en una muestra de 1–100 por números de una cifra (y del revés); factores comunes y
múltiplos comunes en una muestra; factores primos de 1–168; parejas de 100 en una muestra. Cerca de los
límites: 168 (sí), 169 (todavía no), 999 999, 1 000 000; cada pregunta en menos de 2 s.

## RESULTADO (7 oct)

**Hecho, verde: proyecto 2462/2462 + 693/693.** `test_M15_factores_multiplos_primos` 82/82; mis_casos 693/693;
mis_pruebas 188/188; la auditoría sin calculadora, limpia.

- Dos preguntas nuevas (`parejas_de_factores`, `primo`) y 5 piezas, sin tocar el motor de piezas. **Todas se comprueban
  con la operación contraria** y `aplicar` las descarta si no cuadra (la prueba B le da «36 : 5 = 7 y sobran 2» y la
  vuelta lo caza):
  - `parejas_de_factores_en_orden` (rapidez 10): prueba 1, 2, 3… con `dividir` (con resto) y **para al cruzarse** (el
    compañero se hace más pequeño que el que prueba, o el mismo consigo mismo). Pasado el 12 ya no divide (eso es la
    división larga): mira si ese número por sí mismo se pasa (13 x 13 = 169 > 168: para; con 169, **todavía no**).
    **Vuelta**: cada división, multiplicando de vuelta (5 x 7 + 1 = 36).
  - `compuesto_por_una_regla_corta` (rapidez 3): par / acaba en 0 o 5 / sus cifras suman 3, 6 o 9 → compuesto con su
    pareja (1000 = 2 x 500; 999 999 = 3 x 333 333). **Vuelta**: multiplicar la pareja. Si ninguna regla encuentra
    factor (97), no le sale y pasa a la siguiente.
  - `primo_buscando_parejas` (rapidez 10): una sola pareja → primo; más → compuesto (91 = 7 x 13).
  - `primo_el_uno` (rapidez 1): 1 x 1 = 1: un solo factor, ni primo ni compuesto.
  - `multiplicar_con_las_parejas_de_100` (rapidez 7, pregunta `multiplicar`; punto 6): 25 x 36 → 36 = 9 x 4 (la mitad
    de la mitad), 25 x 4 = 100 (sumando), 100 x 9 = 900; vuelta 900 : 100 = 9, 9 x 4 = 36. **Va detrás de doblar y
    partir (M.12)**, para no cambiar lo que ya hacía `25 x 36`; se pide con `con 100: 25 x 36`. Primera versión: usaba
    las preguntas `multiplicar` y `dividir` y `test_piezas` lo cazó (una vuelta en el mapa: multiplicar → dividir →
    división corta → multiplicar). Ahora usa solo sumar, la mitad, y ×/÷ 100.
- Parte nueva `sistema/partes/factores.py`: `factores: 36` (cada prueba, dónde para, las parejas, los rectángulos,
  cuántos factores y por qué impar: **36 es un cuadrado**; primo/compuesto; «36 es múltiplo de cada factor»),
  `primo: 91` (y `es 37 primo?`, `37 es primo`), `primos hasta 100` (**la criba**: tacha contando de 2 en 2, de 3 en
  3, de 5 en 5, de 7 en 7 y para en el 11 porque 11 x 11 = 121; **se comprueba por otro camino**, las parejas de cada
  primo), `multiplos de 7` (los doce primeros contando de 7 en 7; un salto de más de diez es una suma),
  `multiplos de 7 hasta 50`, `21 es multiplo de 7` / `7 es factor de 91` (con la divisibilidad de M.4/M.5 y la
  comprobación multiplicando), `factores comunes: 24 y 36`, `multiplos comunes: 4 y 6` (cuenta los del grande y mira
  cuáles son del pequeño), `factores primos: 60`, `con 100: 25 x 36`.
- **Las trampas**, todas en verde: `primo: 1` → ni primo ni compuesto; `primo: 2` → primo; `primo: 91` → compuesto
  («OJO: es impar y no es primo»); `7 es multiplo de 21` → no («es al revés: 7 es FACTOR de 21»); `multiplos de 7`
  empieza en 7; `factores: 36` da el 6 una vez; `factores: 169` y `primo: 997` → todavía no (con los dos porqués).
- Dominio contra el testigo: los factores de **todos** los números del 1 al 168 (cuántos, impar ⇔ cuadrado, vuelta;
  1.4 s en total), primo o compuesto del 0 al 168 (quién lo dice: la regla corta o las parejas), la criba hasta 2, 10,
  30, 50 y 100, los múltiplos de 1 a 12 (doce primeros y hasta 100), 450 preguntas «múltiplo/factor» (y del revés),
  33 factores comunes, los 144 múltiplos comunes de 1 a 12, 56 factores primos, 3 × 56 «con 100», 60 números grandes
  al azar (nunca dice algo falso; los que tienen 2, 3 o 5 de factor, compuestos). Cerca del techo: `primo: 1000000`,
  `999999`, `999995` → compuesto; `1000001` (pasa del millón), `999997`, `1001` → todavía no. Lo más lento:
  `primos hasta 100`, 0.25 s.
- Todavía no (con su porqué): las parejas de los números desde 169 (dividir entre 13 o más: la división larga, 6.º);
  primo o compuesto de un número grande sin regla corta (997, 1001); la descomposición en factores primos y el
  m.c.m./m.c.d. como técnica; la criba de más de 100; los números cúbicos (no están en los puntos de 2.21).
- **Falta la prueba de Carlos.** Y leer el segmento entero de NCETM 2.21 cuando se pueda abrir (desde la nube la web
  está bloqueada): si trae ejemplos o trampas que aquí no están, se añaden.
