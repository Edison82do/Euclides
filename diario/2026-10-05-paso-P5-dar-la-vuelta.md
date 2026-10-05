# Paso P.5 — DAR LA VUELTA (el orden no importa al juntar) — 5 oct 2026

## 1. EL PLAN (escrito antes de programar)

**La pedagogía.**
- Common Core 1.OA.B.3: «si se sabe 8 + 3 = 11, se sabe 3 + 8 = 11» (propiedad conmutativa),
  como **estrategia**, no como nombre.
- La estrategia de los niños **«contar desde el mayor»** (la estrategia *min*, Groen y Parkman;
  Siegler): para 3 + 47 se empieza en 47 y se cuentan 3 — no se cuentan 47 desde el 3.
- McGraw-Hill (resumen de investigación): una vez que el niño sabe que el orden no importa,
  «cuenta desde el sumando mayor», y eso mejora mucho la eficacia.
- Se aprende **en contexto**: juntar dos montones da lo mismo empiece por donde empiece.
  **OJO (trampa):** vale para **juntar** (sumar); **NO** para quitar: 8 − 3 no es 3 − 8.

- **(Añadido al revisar las fuentes de Hermes)** NCETM, segmento 1.7 (Year 1): *«Addition is
  commutative: when the order of the addends is changed, the sum remains the same.»*  Y la
  Progression de Common Core (CC & OA): *«students might also use the commutative property to
  shorten tasks, by counting on from the larger addend even if it is second»*: es justo la pieza.
  Clements & Sarama: es el nivel *Counting Strategies +/-* de su trayectoria.

**Lo que se construye.**
- Una pieza `sumar_dando_la_vuelta` (responde a «sumar»): si el primero es el **menor** y el primero
  es **corto** (cabe en los dedos, o son decenas justas), le da la vuelta y usa un método corto:
  los dedos (47 + 3) o de diez en diez (47 + 30). Usa esas piezas **por su nombre** (si usara
  «sumar» entero podría darse la vuelta a sí misma sin fin: el mapa lo prohíbe).
- Rapidez 15: después de hacer diez (10), antes de los dedos (20) y las columnas (40).
- La explicación dice **por qué** se puede: «juntar 3 y 47 es lo mismo que juntar 47 y 3».

**Las trampas (pruebas que tienen que salir bien).**
- 47 + 3: ya empieza por el grande → no se da la vuelta (se descarta con su porqué).
- 3 + 47 → 47 + 3 con los dedos: 48, 49, 50.   30 + 47 → 47 + 30 de diez en diez: 57, 67, 77.
- 15 + 47: el primero no es corto → darle la vuelta no ayuda → columnas.
- 8 − 3 / 3 − 8: no hay «vuelta» en la resta (ninguna pieza de restar da la vuelta).
- Un problema («Ana tiene 3, le dan 47») la usa sin saber que existe.

**Prueba de dominio.** Muestra de parejas (primero corto, segundo mayor) comparada con el testigo,
la vuelta cuadra y el motor la elige; las trampas de arriba; todo el proyecto verde.

**Para Carlos (su `.bat`):** `calcular: 3 + 47`, `calcular: 30 + 47`, `calcular: 47 + 3`,
`calcular: 15 + 47`, y el problema «Ana tiene 3 canicas. Le dan 47. Cuantas tiene ahora?».

## 2. LO QUE SE HIZO
- Pieza `conocimiento/piezas/sumar_dando_la_vuelta.py` (rapidez 15; usa por su nombre
  `sumar_de_diez_en_diez` y `sumar_con_dedos`). Condiciones nuevas: `el_primero_es_menor`,
  `el_primero_es_corto`.
- `pruebas/test_P5_vuelta.py` (11 afirmaciones; la muestra recorre 5019 sumas contra el testigo).
- Ayuda, `mis_pruebas.txt` (5 pruebas nuevas para Carlos) y `mis_casos.txt` (5 casos).

## 3. RESULTADO
- 3 + 47 → «3 + 47 = 47 + 3 (juntar 3 y 47 es lo mismo que juntar 47 y 3: empiezo por el grande);
  desde el 47, 3 dedos» → 50.  30 + 47 → 47 + 30 → 57, 67, 77.
- Trampas: 47 + 3 no da la vuelta; 15 + 47 → columnas (no ayuda); la resta no tiene vuelta.
- Proyecto: **1576/1576 afirmaciones + 389/389 casos — VERDE**.

## 4. PENDIENTE: la prueba de Carlos (regla del plan pedagógico)
No se empieza P.6 (restar pensando en sumar) hasta que Carlos lo pruebe con su `.bat`.
