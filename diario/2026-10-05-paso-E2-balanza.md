# Paso E.2 — EL `=` COMO BALANZA — 5 oct 2026

Carlos probó E.1 con su `.bat` («ya probé») → se empieza E.2.

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (mirando antes `FUENTES.md`).**
- **Falkner, Levi & Carpenter** (1999) y **Carpenter, Franke & Levi** (2003): `8 + 4 = __ + 5`.
  En el estudio que cita SEDL, de los alumnos de 6.º el **84 % puso 12** («el = es poner el
  resultado») y el **14 % puso 17** («sumo todo lo que veo»). La respuesta es **7**.
- **Knuth et al.** (2006, 2008): quien ve el `=` como **equivalencia** (los dos lados valen lo mismo)
  resuelve mejor las ecuaciones con operaciones a los dos lados. La **balanza** es el modelo: los
  dos platos pesan lo mismo.
- **Pensamiento relacional** (Carpenter et al.; Stephens; Kızıltoprak y Yavuzsoy Köse 2017):
  `57 + 22 = ? + 21` se resuelve **sin calcular**: 21 es uno menos que 22, así que el hueco es uno
  más que 57 → 58. Niveles: calcular los dos lados → calcular y ver la relación → ver la relación.
- **NCETM 1.29** (Year 5): *Using equivalence and the compensation property to calculate* — la
  compensación como propiedad (aquí, en su forma más sencilla).
- **Progression CC & OA**: el `=` es siempre «es el mismo número que».

**Lo que se construye.** Una pregunta nueva de las piezas, **«balanza»** (la más corta que encaja):
- `balanza_mismo_numero` (rapidez 1): `8 + 4 = 8 + ?` → 4, sin calcular (los dos platos tienen un 8;
  lo demás tiene que pesar igual). También en la resta (`12 − 5 = 12 − ?` → 5; `? − 3 = 9 − 3` → 9).
- `balanza_compensando` (rapidez 5): `8 + 4 = ? + 5` → «5 es uno más que 4, así que el hueco es uno
  menos que 8: 7», **sin calcular los lados** (solo la diferencia pequeña, con los dedos).
- `balanza_calculando_un_lado` (rapidez 20): calcula el plato completo (8 + 4 = 12) y entonces es
  una ecuación de E.1 (`12 = ? + 5`), que resuelven las piezas de los problemas.
- La explicación enseña además **las dos respuestas equivocadas famosas** (12 y 17) y por qué no:
  se ponen en el hueco y se pregunta a E.0 → FALSO.
- La comprobación final, con E.0.

**Las trampas.**
- `8 + 4 = ? + 5` → 7 (no 12 ni 17, y se dice por qué).
- `57 + 22 = ? + 21` → 58 sin calcular 57 + 22.
- `8 + 4 = 8 + ?` → 4 sin calcular.   `? + 4 = 8 + 5` → 9.   `8 + ? = 7 + 5` → 4.
- `15 − 7 = ? − 6` → 14 (calculando: la compensación en la resta va al revés y no se toca aún).
- `8 + 4 = 15 − ?` → 3 (operaciones distintas: calculando).
- `8 + 4 = ? + 13` → imposible (el plato de la derecha ya pesa más).

**Prueba de dominio.** Muestra de balanzas (el hueco en las 4 posiciones, + y −) contra el testigo,
comprobadas por E.0; cada pieza donde le toca; las trampas.

**Para Carlos:** `8 + 4 = ? + 5`, `57 + 22 = ? + 21`, `8 + 4 = 8 + ?`, `15 - 7 = ? - 6`,
`8 + 4 = ? + 13`.

## 2. LO QUE SE HIZO
- Pregunta nueva **«balanza»** (`_objetivos.py`) y tres piezas: `balanza_mismo_numero` (1),
  `balanza_compensando` (5) y `balanza_calculando_un_lado` (20; usa sumar/restar y los pasos de R.1).
  Condiciones nuevas: `hay_un_plato_completo`, `comparten_un_numero`, `los_dos_lados_son_sumas`,
  `hay_una_pareja_cerca`.
- `sistema/partes/ecuaciones.py`: lo que antes decia «eso es la balanza, todavia no» ahora pregunta a las
  piezas de balanza; comprueba con E.0; y prueba en el hueco **las dos respuestas equivocadas de siempre**
  (lo que da el plato completo, y sumar todo) para decir por que NO.
- `pruebas/test_E2_balanza.py` (14 afirmaciones; la muestra resuelve 1586 balanzas con + y -, el hueco
  en todas las posiciones). Ayuda, `mis_pruebas.txt` (6) y `mis_casos.txt` (6 + el de E.1 que cambia).

## 3. RESULTADO
- `8 + 4 = ? + 5` -> «5 es uno mas que 4; para que la balanza siga igual, el hueco es uno MENOS que 8: 7
  (sin calcular los lados)».  Y: «12 NO (leer el = como da): 8 + 4 = 12 + 5 es FALSO;  17 NO (sumar todo
  lo que se ve): 8 + 4 = 17 + 5 es FALSO».
- `57 + 22 = ? + 21` -> 58 sin calcular.  `8 + 4 = 8 + ?` -> 4.  `15 - 7 = ? - 6` -> 14 (calculando).
- Proyecto: **1643/1643 afirmaciones + 420/420 casos — VERDE**.

## 4. PENDIENTE: la prueba de Carlos
Con E.2 termina la parte del `=`. No se empieza N.1 (par e impar; contar de n en n) hasta su OK.
