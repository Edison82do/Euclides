# Paso M.8 — LA DIVISIÓN CON RESTO — 6 oct 2026 (noche)

Sigue al M.7 (4.º). NCETM Spine 2, Year 4.

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (NCETM 2.12, leído el 6 oct; Common Core 4.NBT.B.6, 4.OA.A.3).**
1. «Los objetos se pueden **agrupar** en grupos iguales, a veces con **resto**; se pueden **repartir**,
   a veces con resto; el resto **se escribe en la ecuación** de la división.»
2. «Si el dividendo es múltiplo del divisor, no hay resto; si no lo es, hay resto. **El resto es
   siempre menor que el divisor**.»
3. «En los problemas, la respuesta de la división hay que **interpretarla** con cuidado para que el
   resto tenga sentido.» (Common Core 4.OA.A.3: «problemas … en los que hay que interpretar el resto».)
   Las tres maneras clásicas: **redondear hacia arriba** (17 niños en coches de 5: hacen falta **4**
   coches, el último no va lleno), **hacia abajo** (con 17 € y libros de 5 €, se pueden comprar **3**),
   o **el resto es la respuesta** (¿cuántos sobran? **2**).

Lo que Euclides ya hacía (M.3, R.2): `17 : 5` → 3 resto 2; los problemas decían «3, y sobran 2».

**Lo que se construye.**
- En `17 : 5`: la ecuación con el resto (**17 = 3 × 5 + 2**) y por qué el resto es menor que el divisor
  («si sobraran 5 o más, cabría otro grupo»).
- `comprobar: 17 : 5 = 2 resto 7` → MAL: 2 × 5 + 7 = 17 cuadra, pero el resto 7 no es menor que 5
  (cabe otro grupo): es 3 resto 2.  `comprobar: 17 : 5 = 3 resto 1` → MAL (3 × 5 + 1 = 16).
- Problemas (R.2): leer «en cada coche caben 5», «¿cuántos coches **hacen falta**?» → **arriba** (4);
  «¿cuántas bolsas **se pueden llenar**?» / «¿cuántos **puede comprar**?» → **abajo** (3); «¿cuántos
  **sobran**?» → el resto (2). Cada vez dice por qué.
- (Se arregla de paso el plural: «coches» y «coche» son lo mismo.)

**Las trampas.**
- `17 : 5` → 3 resto 2, y 17 = 3 × 5 + 2.   `15 : 5` → 3 (sin resto: 15 es múltiplo de 5).
- «Hay 17 niños. En cada coche caben 5. ¿Cuántos coches hacen falta?» → 4 (no 3: los 2 que sobran
  también van).
- «Tiene 17 euros. Cada libro cuesta 5 euros. ¿Cuántos libros puede comprar?» → 3 (no 4: no le llega).
- «Reparte 17 caramelos entre 5 niños. ¿Cuántos sobran?» → 2.
- `comprobar: 17 : 5 = 2 resto 7` → no.

**Prueba de dominio.** Todas las divisiones de 0..200 entre 1..12: cociente y resto contra el testigo,
el resto menor que el divisor, la ecuación; comprobar respuestas buenas y malas; los tres tipos de
problema con números de muestra.

**Para Carlos:** `17 : 5`, `comprobar: 17 : 5 = 2 resto 7`, los tres problemas.

## 2. LO QUE SE HIZO
- `dividir.py`: con resto, la ecuación (17 = 3 × 5 + 2) y el porqué del resto menor que el divisor; sin
  resto, «es múltiplo». Orden nueva `comprobar: 17 : 5 = 2 resto 7` (la vuelta Y el resto menor que el
  divisor; si está mal, da la buena).
- `resolver_r2.py`: **interpretar el resto** según la pregunta: «hacen falta» / «necesita» → arriba;
  «puede», «se pueden», «completas» → abajo; forma nueva «¿cuántos sobran?» → el resto. Cada vez se dice
  por qué (paso 7 de la explicación). La comprobación con resto ahora se **calcula** (antes se daba por
  buena). Y el plural: «coches» y «coche» son el mismo grupo.
- `pruebas/test_M8_division_con_resto.py` (14 afirmaciones: trampas; las 2412 divisiones 0..200 entre
  1..12 contra el testigo; 600 respuestas buenas y malas; 40 problemas de cada tipo). Ayuda,
  `mis_pruebas.txt` (5), `mis_casos.txt` (6).

## 3. RESULTADO
- «¿Cuántos coches hacen falta?» → 4 («los 2 que sobran también necesitan sitio»).  «¿Cuántos libros
  puede comprar?» → 3 («los 2 euros que sobran no llegan para otro libro»).  «¿Cuántos sobran?» → 2.
- Proyecto: **2022/2022 afirmaciones + 577/577 casos — VERDE**.

## 4. PENDIENTE: la prueba de Carlos (mañana).  Sigue M.9: multiplicar y dividir por 10 y por 100 (NCETM 2.13).
