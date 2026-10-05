# Paso M.0 — FILAS Y COLUMNAS COMO SUMAS IGUALES — 5 oct 2026

Carlos probó N.1 («ya probé») → se empieza M.0, el puente justo antes de multiplicar.

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (mirando antes `FUENTES.md`).**
- Common Core **2.OA.C.4** (grupo «trabajar con grupos iguales: base para la multiplicación»):
  «usar la **suma** para hallar el total de objetos colocados en **filas y columnas** (hasta 5 filas
  y 5 columnas); escribir una ecuación que exprese el total como una **suma de sumandos iguales**».
  Todavía **no se multiplica**: se suma.
- La Progression de Common Core (OA) y el documento de Nuevo México (2.OA.C): las filas y columnas
  se escriben como **sumas repetidas** — el precursor directo de la multiplicación (3.OA.A.1).
- **Singapur (CPA)**, que usaba Hermes: primero se **ve** (el dibujo de las filas: pictórico) y
  luego se escribe (abstracto).
- **NCETM 2.1** (lo de N.1): contar de 2, 5 y 10 en 10 es contar **grupos**; aquí cada fila es un
  grupo, y si la fila es de 2, de 5 o de 10, se puede **saltar** en vez de sumar.
- Lo que viene después y **no** entra aún: que 3 filas de 4 y 4 filas de 3 dan lo mismo **como
  propiedad** es NCETM 2.3 (conmutativa de la multiplicación, M.2). Aquí solo se **observa**
  contando la misma colección por filas y por columnas.

**Lo que se construye.**
- Orden `3 filas de 4` (y `3 columnas de 4`): **dibuja** las filas con puntos, escribe la **suma de
  iguales** (`4 + 4 + 4`) y la hace.
- Pregunta nueva **«suma de iguales»** con dos piezas:
  - `sumar_iguales_saltando` (rapidez 5): si cada fila es de 2, de 5 o de 10, se cuenta de n en n
    con lo de N.1 (5, 10, 15).
  - `sumar_iguales_uno_a_uno` (rapidez 15): se suma fila a fila con los métodos que ya tiene
    (4 + 4 = 8 de memoria, 8 + 4 = 12...).
- Y se cuenta **también por columnas** (3 + 3 + 3 + 3) para ver que es la misma colección.
- Si se escribe `3 x 4`: «todavía no sé multiplicar (M.1); pero 3 filas de 4 sí».

**Las trampas.**
- `3 filas de 4` → 4 + 4 + 4 = 12; por columnas 3 + 3 + 3 + 3 = 12.
- `5 filas de 5` → 25 saltando de 5 en 5.   `4 filas de 2` → 2, 4, 6, 8.
- `1 fila de 5` → 5 (una sola fila: no hay nada que repetir).   `0 filas de 4` → 0 (no hay nada).
- `3 columnas de 4` → 4 filas de 3 en el dibujo.
- Más de 5 filas: el estándar llega a 5 × 5; se hace igual hasta 10 × 10 y se avisa.
- `3 x 4` → todavía no.

**Prueba de dominio.** Todas las filas y columnas de 0 a 10 contra el testigo, con su pieza; el
dibujo tiene las filas y columnas pedidas; por filas y por columnas da lo mismo.

**Para Carlos:** `3 filas de 4`, `5 filas de 5`, `4 filas de 2`, `3 columnas de 4`, `3 x 4`.

## 2. LO QUE SE HIZO
- Parte nueva `sistema/partes/filas.py`: lee `3 filas de 4` / `3 columnas de 4`, DIBUJA las filas,
  escribe la suma de iguales recitando (4 + 4 + 4), y pregunta a las piezas; cuenta tambien por
  columnas. `3 x 4` -> «todavia no se multiplicar».
- Pregunta nueva **«suma de iguales»** con `sumar_iguales_saltando` (grupos de 2, 5 o 10: lo de N.1)
  y `sumar_iguales_uno_a_uno` (usa «sumar»: memoria, hacer diez, dedos, compensar...).
- `pruebas/test_M0_filas.py` (15 afirmaciones; las 121 filas x columnas de 0 a 10 contra el testigo).
  Ayuda, `mis_pruebas.txt` (6) y `mis_casos.txt` (7).

## 3. RESULTADO
- `3 filas de 4` -> el dibujo, 4 + 4 = 8, 8 + 4 = 12; por columnas 3 + 3 + 3 + 3 = 12: da lo mismo.
- `5 filas de 5` -> 5, 10, 15, 20, 25.   `3 x 4` -> todavia no.
- Proyecto: **1681/1681 afirmaciones + 436/436 casos — VERDE**.

## 4. PENDIENTE: la prueba de Carlos
Con M.0 se termina el «camino a multiplicar» de 2.o. El siguiente es **M.1 multiplicar = grupos
iguales** (NCETM 2.2; 3.OA.A.1): el signo x, por fin, con su plan.
