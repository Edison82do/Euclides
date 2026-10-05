# Paso P.6 — RESTAR PENSANDO EN SUMAR (contar hacia arriba) — 5 oct 2026

Carlos probó P.5 con su `.bat` («todo muy bien») → se empieza P.6 (regla de velocidad pedagógica).

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (mirando antes `FUENTES.md`).**
- Common Core **1.OA.B.4**: «entender la resta como un problema de **sumando desconocido**: resta
  10 − 8 buscando el número que, sumado a 8, da 10».
- **Progression CC & OA (K–5)**: «contar hacia arriba para restar es **más fácil** que contar hacia
  atrás» y «contar hacia arriba **refuerza** que la resta es un problema de sumando desconocido».
- **McGraw-Hill** (resumen de investigación): contar hacia atrás obliga a llevar dos procesos
  opuestos a la vez y los errores crecen con los números; contar hacia arriba («think addition»)
  es accesible en 1.º y deja la resta tan precisa como la suma.
- **NCETM 1.12** (*Subtraction as difference*) y la unidad 5.5 de Euclides: «¿cuántos más?» se ve
  como `12 + ? = 15` o como `15 − 12 = ?` — **es lo mismo**.
- **Clements & Sarama**: *Numbers-in-Numbers +/-* — mantener la parte y el todo a la vez.
- **El matiz que enseñan los maestros**: no siempre conviene. **Si se quita poco** (13 − 2), contar
  hacia atrás es más corto; **si los números están cerca** (13 − 8, 52 − 48), contar hacia arriba.
  Un buen restador **elige**.

**Lo que se construye.**
- Pieza `restar_contando_hacia_arriba` (responde a «restar», rapidez 12): desde lo que se quita
  se cuenta hacia arriba hasta lo que había, con los dedos; los dedos levantados son la resta.
  La vuelta sale sola: es la suma (8 + 5 = 13).
- Condiciones: no se quita más de lo que hay; **la distancia cabe en los dedos** (los números están
  cerca); y **contar hacia arriba es más corto que hacia atrás** (la distancia es menor que lo que
  se quita).
- La explicación: «13 − 8: ¿cuánto le falta al 8 para llegar al 13? 9, 10, 11, 12, 13: 5.
  Porque 8 + 5 = 13».

**Las trampas.**
- 13 − 2: se quita poco → hacia atrás (2 pasos), no hacia arriba (11) — y se dice por qué.
- 13 − 5: hacia arriba serían 8 pasos, hacia atrás 5 → hacia atrás.
- 52 − 48 → 49, 50, 51, 52: 4 (antes: columnas).
- 100 − 95 → 96 … 100: 5 — sin cambiar centenas por decenas (por columnas es «a través de ceros»).
- 13 − 13 → 0;  8 − 13 → imposible.
- Un problema («Había 52 pájaros. Se van 48. ¿Cuántos quedan?») lo usa solo.

**Prueba de dominio.** Muestra de restas con los números cerca contra el testigo; la vuelta (la
suma) cuadra; el motor la elige solo cuando es lo más corto; las trampas; todo verde.

**Para Carlos (su `.bat`):** `calcular sin memoria: 13 - 8`, `calcular: 52 - 48`,
`calcular: 100 - 95`, `calcular: 13 - 2`, y el problema de los pájaros.

## 2. LO QUE SE HIZO
- Pieza `conocimiento/piezas/restar_contando_hacia_arriba.py` (rapidez 12). Condiciones nuevas:
  `estan_cerca` (de uno a otro cabe en los dedos) y `hacia_arriba_es_mas_corto`.
- `pruebas/test_P6_hacia_arriba.py` (11 afirmaciones; la muestra recorre 3080 restas contra el testigo).
  La muestra cazo un fallo: cerca del techo (mil) `contar_adelante` no da resultado -> arreglado.
- Lenguaje rustico: la forma `habia {n} {cosa}` (el problema de los pajaros en pasado).
- Ayuda, `mis_pruebas.txt` (6 pruebas para Carlos) y `mis_casos.txt` (6 casos).

## 3. RESULTADO
- 13 - 8 (sin memoria) -> «cuanto le falta al 8 para llegar al 13? 9, 10, 11, 12, 13: 5 dedos.
  Porque 8 + 5 = 13».  52 - 48 -> 4.  100 - 95 -> 5 sin cambiar centenas.
- Trampas: 13 - 2 y 13 - 5 van hacia atras (y dice por que); 8 - 13 imposible.
- Proyecto: **1587/1587 afirmaciones + 395/395 casos — VERDE**.

## 4. PENDIENTE: la prueba de Carlos
No se empieza E.0 (el `=`: verdadero o falso) hasta que Carlos lo pruebe con su `.bat`.
