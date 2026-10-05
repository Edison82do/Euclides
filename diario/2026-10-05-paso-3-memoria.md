# Paso 3 del plan: la MEMORIA de hechos — 5 oct 2026

## La decisión de Carlos
«En el camino el ser humano memoriza algunos datos y utiliza técnicas para agilizar la solución de
problemas; eso es válido aquí, según va avanzando el proceso de aprendizaje.»

## La pedagogía
- Baroody: tres fases — **contar → razonar (hechos derivados) → dominio**. «Fact fluency leads to
  memorization down the road, but it doesn't start there.» → la memoria llega **después**, nunca en
  lugar del razonamiento.
- Common Core 2.OA.B.2: al final de 2.º, «know from memory all sums of two one-digit numbers».
- Las restas se aprenden como **familia** de la suma (8 + 5 = 13 → 13 − 5 = 8, 13 − 8 = 5).

## Lo que se hizo
- `sistema/partes/memoria.py`: `cargar_memoria`, `aprender`, `olvidar_todo`, y sus explicaciones.
- `conocimiento/memoria/hechos.txt`: una línea por hecho → `8 + 5 = 13 | cómo | comprobado | fecha`.
- Piezas `recordar_suma` y `recordar_resta` (rapidez 1, la más corta). Condiciones nuevas:
  `se_permite_recordar`, `la_suma_esta_en_la_memoria`, `la_resta_esta_en_la_memoria`.
- El motor de piezas: si la más rápida **no sale** (p. ej. un recuerdo que no cuadra), pasa a la
  siguiente y lo dice.
- Órdenes: `memoria`, `aprender: sumas`, `aprender: restas`, `olvidar: todo`.
- `test_memoria.py` (19 afirmaciones, en una memoria temporal); `test_piezas` usa memoria vacía.
- El paquete del móvil lleva también la memoria.

## Reglas de la memoria (no se rompen)
1. Un hecho solo entra **calculado sin memoria**, **comprobado por la vuelta** y, si hay otro
   método que también sirve, **por un segundo camino** que tiene que dar lo mismo.
2. Cada hecho dice **cómo** y **cuándo** se aprendió. Nadie lo escribe a mano.
3. Al recordar **se vuelve a comprobar**. Prueba: se falsificó `8 + 5 = 14` en la memoria → el
   sistema no lo usa, calcula haciendo diez y da 13, y dice por qué.
4. La memoria no inventa: `47 + 5` no está y se sigue calculando.

## Resultado
`aprender: sumas` → 100 nuevas, 100 por dos caminos, 0 rechazadas. `aprender: restas` → 100.
Un problema de Ana (8 + 5) ahora dice: «CALCULO con de memoria (lo aprendí con hacer diez (7.2))».
Proyecto: **1543/1543 afirmaciones + 375/375 casos — VERDE**.

## Lo que sigue (P.4)
Técnicas como piezas: dobles y casi dobles, compensación, de diez en diez.
