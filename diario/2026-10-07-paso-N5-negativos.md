# Paso N.5 — LOS NÚMEROS NEGATIVOS: CONTAR, COMPARAR, CALCULAR CRUZANDO EL CERO — 7 oct 2026 (madrugada)

Sigue al N.4. Es el segmento 1.27 de NCETM (Year 5). Common Core los trae en 6.º (6.NS.C.5–7);
NCETM los adelanta a 5.º con escalas y contextos (la temperatura).

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (NCETM 1.27, *Negative numbers: counting, comparing and calculating*, leído el 7 oct).**
1. «Los números positivos y negativos sirven para representar un **cambio**.»
2. «Nuestro sistema de numeración incluye números **menores que cero**: los negativos. Los mayores que
   cero son los positivos.»
3. «El signo **menos (−)** delante de la cifra indica que el valor es negativo.»
4. «Los negativos se ven en **escalas horizontales**: a la izquierda del cero, negativos (menores que
   cero); a la derecha, positivos. **Cuanto mayor es la cifra después del signo, más lejos está del
   cero**» (y por eso más pequeño).
5. «Saber dónde están los positivos y los negativos sirve para calcular **intervalos a través del cero**.»
6. «Los negativos se usan en coordenadas y gráficas» → eso va con la geometría, más adelante.
- Common Core 6.NS.C.7: «−3 °C es más caliente que −7 °C»; el valor absoluto es la **distancia al cero**.

**Cómo lo hace un humano sin calculadora (y así lo hará Euclides).**
- La recta sigue a la izquierda del cero como un **espejo**: antes del cero va «menos uno», antes de
  «menos uno» va «menos dos»… Ir a la izquierda en los negativos es ir hacia arriba en la cifra.
- **Comparar**: el negativo siempre es menor que el cero y que cualquier positivo; entre dos negativos,
  el de cifra **mayor** está más lejos del cero, a la izquierda: es **menor** (−7 < −3).
- **Cruzar el cero** es como «hacer diez» (P.2): se parte el salto en el tramo **hasta el cero** y lo
  que queda **después**. 3 − 8: bajo 3 hasta el cero, me quedan 5 → −5. −4 + 7: subo 4 hasta el cero,
  me quedan 3 → 3.
- Sin cruzar: −6 + 2 → me acerco al cero 2: −4. −4 − 3 → me alejo 3: −7.
- **El intervalo** entre −4 y 7: 4 hasta el cero y 7 desde el cero → 11. Entre −9 y −2: 9 − 2 = 7.
- Las cuentas de los tramos son sumas y restas de naturales: se hacen con las piezas de siempre.

**Lo que se construye** (parte nueva `sistema/partes/negativos.py`).
- `negativo: -5` → «menos cinco»: 5 a la izquierda del cero; menor que cero; su distancia al cero es 5.
- `comparar: -3 y -7` → −3 > −7 (con el porqué: −7 está más lejos del cero, a la izquierda).
- `recta: desde 3 bajando 6` → 2, 1, 0, −1, −2, −3 (contar hacia atrás cruzando el cero) y
  `recta: desde -5 subiendo 7`.
- `recta: 3 - 8` → −5 y `recta: -4 + 7` → 3, `recta: -4 - 3`, `recta: -6 + 2` (con la recta dibujada
  en texto si es corta).
- `intervalo: -4 y 7` → 11.
- Problemas de temperatura (el cambio): «La temperatura es -4 grados. Sube 7 grados. ¿Cuál es ahora?» → 3;
  «Es 3 grados y baja 8» → −5; «Por la mañana -6 y a mediodía 5. ¿Cuánto subió?» → 11.
- OJO: `3 - 8` **sin** la recta sigue diciendo «no hay bastantes» (con cosas no se puede quitar 8 de 3);
  con la recta, sí. Se dice en el mensaje.

**Las trampas.**
- `comparar: -3 y -7` → −3 > −7 (no −7 > −3 por «7 es más que 3»).
- `comparar: -1 y 0` → −1 < 0.   `comparar: -100 y 2` → −100 < 2.
- `recta: 3 - 8` → −5 (no 5).   `recta: -4 + 7` → 3 (no −11 ni 11).   `recta: -4 - 3` → −7 (no −1).
- `intervalo: -4 y 7` → 11 (no 3).   `intervalo: -9 y -2` → 7 (no 11).
- `recta: 5 - 5` → 0 (el cero no es ni positivo ni negativo).

**Prueba de dominio.** Contra un testigo: todas las sumas y restas en la recta con números entre −20 y 20
(41 × 41 × 2), una muestra hasta ±1000; todas las comparaciones de −20 a 20; intervalos.

## RESULTADO (7 oct, madrugada)

**Hecho, verde: proyecto 2226/2226 + 637/637; mis_pruebas 164/164.**

- Parte nueva `sistema/partes/negativos.py`. Un número con signo es (signo, cuánto); todas las cuentas
  con «cuánto» las hacen las piezas de siempre (sumar, restar). Comparar mira las cifras con
  `viene_despues` (más lejos del cero). Contar en la recta usa `siguiente`/`anterior` en espejo.
- Cruzar el cero se explica como «hacer diez»: hasta el cero, y lo que queda.
- `3 - 8` sin la recta sigue diciendo «imposible» (con cosas no se puede); con `recta:` da −5, y lo dice.
- Problemas de temperatura con pocas palabras (sube, baja, cuánto subió), también «menos 2 grados».
- Prueba de dominio `test_N5_negativos` 26/26: 1722 cuentas en la recta (−20..20 ± 0..20), todas las
  comparaciones con algún negativo y todos los intervalos de −20 a 20, 200 cuentas hasta ±1000.
- Las coordenadas (punto 6 de NCETM) quedan para la geometría.
