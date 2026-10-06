# Paso M.6 — LA TABLA DEL 7 Y LA DISTRIBUTIVA — 6 oct 2026

Carlos probó M.5 («ya probé») → se empieza M.6 (paso 13 del plan ajustado).

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (mirando antes `FUENTES.md`).**
- **NCETM 2.9** (*Times tables: 7 and patterns within/across times tables*, Year 3):
  1. La tabla del 7 es contar de 7 en 7; seguidos se diferencian en 7.
  2. «Si los dos factores son **impares**, el producto es impar; si uno es impar y el otro par, el
     producto es **par**; si los dos son pares, es par».
  3. «Cuando los dos factores son iguales, el producto es un **número cuadrado**; se dibuja como un
     **cuadrado** de filas y columnas».
  4. Reglas de divisibilidad para otros divisores.
- **NCETM 2.10** (*Connecting multiplication and division, and the distributive law*, Year 4):
  1. «La multiplicación es conmutativa; **la división no**».
  2. «La multiplicación es **distributiva**: los hechos se sacan de otros conocidos **partiendo uno de
     los factores** (partir el número de grupos)».
  3. «La distributiva sirve para sacar hechos **más allá de las tablas** que se saben».
- Common Core **3.OA.B.5** (propiedades como estrategias; ejemplo del estándar: 8 × 7 = 8 × 5 + 8 × 2)
  y **3.OA.C.7** (soltura con todas las tablas hasta 10 × 10).

**Lo que se construye.**
- Pieza `multiplicar_partiendo` (la distributiva, rapidez 9): parte un factor en dos trozos cuyos
  productos ya se saben (7 = 5 + 2: 7 × 6 = 5 × 6 + 2 × 6 = 30 + 12 = 42; 12 = 10 + 2: 12 × 6 = 60 + 12).
- `tabla del 7` (cada fila partida: 5 × k + 2 × k; y seguidos se diferencian en 7).
- `aprender: tablas` termina con la del 7 → **todas las tablas hasta 10 × 10**, cada una sacada de
  otras y comprobada (3.OA.C.7).
- En cada multiplicación: **par o impar** del producto por la regla de los factores, y si los dos
  factores son iguales, **número cuadrado** con su dibujo en cuadrado.
- `divisible:` entre cualquier divisor (para los que no tienen regla, dividiendo con lo que sabe).
- La división no es conmutativa: `verdad: 12 : 3 = 3 : 12` → no es verdad.

**Las trampas.**
- `7 x 6` sin tablas en memoria → no se puede partir (no hay hechos conocidos): grupo a grupo.
- Con tablas: `8 x 7` = 8 × 5 + 8 × 2 = 40 + 16 = 56 (el ejemplo del estándar).
- `12 x 6` (fuera de las tablas) = 10 × 6 + 2 × 6 = 72.
- `7 x 9`: impar × impar → impar.   `6 x 6` → cuadrado.
- `tabla del 11` → todavía no (NCETM 2.11, Year 4).

**Prueba de dominio.** Todas las tablas hasta 10 × 10 aprendidas y comprobadas; la distributiva donde
le toca y más allá de las tablas (hasta 12 × 10) contra el testigo; las reglas de par/impar y cuadrados.

**Para Carlos:** `tabla del 7`, `aprender: tablas`, `8 x 7`, `12 x 6`, `6 x 6`, `divisible: 49 entre 7`.

## 2. LO QUE SE HIZO
- Pieza `multiplicar_partiendo` (la distributiva, rapidez 9; condicion `un_factor_se_puede_partir`):
  parte un factor en trozos de 10, 5, 2, 4 o 3 cuyos productos ya se saben. Sirve dentro y FUERA de las
  tablas (12 x 6, 15 x 7).
- `multiplicar.py`: `tabla del 7` (5 x k + 2 x k); en cada multiplicacion, la regla de PAR o IMPAR y el
  NUMERO CUADRADO; `divisible:` con cualquier divisor (si no hay regla corta, dividiendo).
- `aprender: tablas` termina con la del 7: **todas las tablas hasta 10 x 10** en la memoria
  (memoria de verdad: 317 hechos), cada una sacada de otras y comprobada con la otra lectura.
- `pruebas/test_M6_tabla7_distributiva.py` (16 afirmaciones). `test_M2/M4/M5` se ajustan (ahora la que
  falta es la del 11). Ayuda, `mis_pruebas.txt` (6), `mis_casos.txt` (7 + 2 que cambian).

## 3. RESULTADO
- `tabla del 7` -> «8 x 7 = 8 x 5 + 8 x 2 = 40 + 16 = 56».  `12 x 6` -> 10 x 6 + 2 x 6 = 72.
- `7 x 9` -> «impar x impar -> IMPAR».  `6 x 6` -> «NUMERO CUADRADO».  `divisible: 49 entre 7` -> si.
- Proyecto: **1832/1832 afirmaciones + 509/509 casos — VERDE**.

## 4. PENDIENTE: la prueba de Carlos.  Lo que sigue: E.5 problemas de dos pasos con la letra como hueco (3.OA.D.8).
