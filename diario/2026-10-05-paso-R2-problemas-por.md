# Paso R.2 — PROBLEMAS DE × Y ÷ CON POCAS PALABRAS — 5 oct 2026

Carlos probó E.4 («ya probé») → se empieza R.2 (paso 10 del plan ajustado).

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (mirando antes `FUENTES.md`).**
- Common Core **3.OA.A.3**: «usar la multiplicación y la división hasta 100 para resolver problemas
  de **grupos iguales**, **filas y columnas** y **cantidades de medida**».
- **CGI** (Carpenter et al.) para × y ÷: las estructuras son **multiplicar** (grupos y tamaño
  conocidos), **dividir agrupando** (cuotitiva: se sabe el tamaño de cada grupo) y **dividir
  repartiendo** (partitiva: se sabe el número de grupos). Es lo mismo que NCETM 2.6.
- **Instrucción por esquemas** (Jitendra; Xin): el esquema de **grupos iguales** tiene tres casillas
  — **cuántos grupos**, **cuántos en cada uno**, **el total** — y el problema dice dos y pregunta por
  una. Lo que decide la operación es **qué casilla falta**, no las palabras clave.
- **Contra las palabras clave** (lo de R.1): «cada» no siempre es multiplicar («hay 12 caramelos;
  cada niño tiene 3; ¿cuántos niños?» es **dividir**), y «entre» no siempre es dividir («Ana y Luis
  tienen 12 entre los dos» es **juntar**, de R.1).
- **Singapur, el modelo de barras**: el total es una barra partida en grupos iguales, con «?» en lo
  que falta:  `[ 4 | 4 | 4 ]` = 12.

**Lo que se construye.**
- Una parte nueva `sistema/partes/resolver_r2.py` que **lee** las frases (lenguaje rústico: «3 bolsas
  con 4 caramelos cada una», «cada caja tiene 4», «reparte 12 entre 3 niños», «mete 12 en bolsas de
  4», «3 filas de 4 sillas», «cada caja pesa 5 kilos») y llena el **esquema** por los **nombres**
  (bolsa → grupo; caramelo → cosa), no por palabras clave.
- Pregunta nueva de las piezas **«paso por»** con tres piezas: `juntar_grupos_iguales` (falta el
  total → multiplicar), `repartir_en_partes_iguales` (falta cuántos en cada → repartir) y
  `agrupar_en_grupos_iguales` (falta cuántos grupos → agrupar). Como en R.1: se prueban todas, se
  descartan con su porqué.
- El **dibujo de barras**, la **comprobación** con E.0 y la respuesta **con su unidad**.
- Un problema con «?» que tiene estas formas va a R.2; si no, sigue yendo a R.1.

**Las trampas.**
- «Hay 3 bolsas con 4 caramelos cada una. ¿Cuántos caramelos hay?» → 12.
- «Reparte 12 caramelos entre 3 niños. ¿Cuántos le tocan a cada uno?» → 4 (repartir).
- «Mete 12 caramelos en bolsas de 4. ¿Cuántas bolsas salen?» → 3 (agrupar).
- «Hay 12 caramelos. Cada niño tiene 3. ¿Cuántos niños hay?» → 4 (**dividir** con «cada»).
- «En el cine hay 3 filas de 4 sillas. ¿Cuántas sillas hay?» → 12 (filas).
- «Cada caja pesa 5 kilos. ¿Cuánto pesan 4 cajas?» → 20 kilos (medida).
- «Mete 14 caramelos en bolsas de 4. ¿Cuántas bolsas salen?» → 3 y sobran 2.
- «Ana y Luis tienen 12 entre los dos…» → sigue siendo de R.1 (juntar).

**Prueba de dominio.** Las tres estructuras y las tres situaciones (grupos, filas, medidas), con
números de una muestra contra el testigo; las trampas de palabras clave; R.1 sigue igual.

**Para Carlos:** los problemas de arriba, escritos directamente.

## 2. LO QUE SE HIZO
- Pregunta nueva **«paso_por»** con 3 piezas: `juntar_grupos_iguales` (usa multiplicar),
  `repartir_en_partes_iguales` y `agrupar_en_grupos_iguales` (usan dividir). Condiciones: se busca el
  total / cuantos en cada / cuantos grupos, y que se sepan las otras dos casillas.
- Parte nueva `sistema/partes/resolver_r2.py`: las FORMAS rusticas (grupos con, en n grupos, filas,
  cada, reparte, en grupos de, hay n; preguntas: cuantos x, a cada, en cada, en total, cuanto pesan);
  el ESQUEMA de grupos iguales se llena por los NOMBRES (la bolsa es el grupo, el caramelo la cosa);
  la BARRA (antes y despues); la comprobacion con E.0; la respuesta con su unidad.
- Un problema con formas propias de grupos iguales va a R.2; los demas siguen en R.1 (sin tocarlo).
- `pruebas/test_R2_problemas_por.py` (16 afirmaciones; 120 problemas al azar de las tres estructuras).
  Ayuda, `mis_pruebas.txt` (8) y `mis_casos.txt` (9).

## 3. RESULTADO
- Las tres estructuras y las tres situaciones; «cada» con multiplicar y con dividir segun el esquema;
  «entre los dos» sigue siendo juntar (R.1); 14 en bolsas de 4 -> 3 bolsas y sobran 2.
- Proyecto: **1781/1781 afirmaciones + 484/484 casos — VERDE**.

## 4. PENDIENTE: la prueba de Carlos.  Lo que sigue: M.4 tablas del 4 y del 8 desde la del 2 (NCETM 2.7).
