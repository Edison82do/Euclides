# Paso M.1 — MULTIPLICAR = GRUPOS IGUALES — 5 oct 2026

Carlos probó M.0 («ya probé») → se empieza M.1: el signo ×, por fin.

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (mirando antes `FUENTES.md`).**
- Common Core **3.OA.A.1**: «interpretar productos de números enteros; por ejemplo, interpretar
  5 × 7 como el total de objetos en **5 grupos de 7** objetos cada uno». Es la lectura que se usa
  aquí: **a × b = a grupos de b**.
- **NCETM 2.2** (*Structures: multiplication representing equal groups*, Year 2), sus puntos:
  1. «Los objetos se pueden agrupar en grupos **iguales o desiguales**».
  2. «Al describir grupos iguales hay que decir **cuántos grupos** y **cuántos hay en cada uno**».
  3. «Los grupos iguales se pueden escribir como una **suma repetida**».
  4. «Los grupos iguales se pueden escribir como una **multiplicación**».
  5. «Se pueden escribir multiplicaciones con grupos de **cero** y de **uno**».
- Lo que **no** entra aún: que 3 × 4 = 4 × 3 como propiedad (NCETM 2.3 y 2.5: M.2); las tablas de
  memoria (M.2); dividir (NCETM 2.6: M.3); ecuaciones con × (E.4).
- **CPA (Singapur)**: se dibujan los grupos antes de escribir.

**Lo que se construye.**
- Pregunta nueva **«multiplicar»** con la pieza `multiplicar_grupos_iguales`: a × b es la **suma
  de iguales** de M.0 (a veces b) — no hay ninguna cuenta nueva: el × es otra forma de **escribir**
  grupos iguales (punto 4 de NCETM).
- Orden: `3 x 4`, `3 × 4`, `3 * 4` o `3 grupos de 4`. Lee qué dice cada número (punto 2), dibuja
  los grupos (hasta 10 y 10), escribe la suma repetida (punto 3), la hace, y escribe el producto.
- **Grupos desiguales** (punto 1): `grupos de 2, 3 y 4` → «no son iguales: no se escribe con ×; es
  una suma: 2 + 3 + 4 = 9».

**Las trampas.**
- `3 x 4` → 3 grupos de 4: 4 + 4 + 4 = 12.   `5 × 7` (el ejemplo del estándar) → 35.
- `4 x 0` → 4 grupos vacíos: 0.   `0 x 4` → ningún grupo: 0.   `4 x 1` → 4.   `1 x 4` → 4.
- `5 x 2` → saltando de 2 en 2 (N.1).   `25 x 30` → 750 sumando grupo a grupo.
- `40 x 30` → se pasa de mil: no.
- `grupos de 2, 3 y 4` → desiguales: suma, no ×.
- `3 x ? = 12` → eso es E.4 / dividir (M.3): todavía no.

**Prueba de dominio.** Todas las multiplicaciones de 0 a 10 × 0 a 10 contra el testigo y una
muestra hasta mil; los grupos de cero y de uno; los desiguales; todo verde.

**Para Carlos:** `3 x 4`, `5 x 7`, `4 x 0`, `3 grupos de 4`, `grupos de 2, 3 y 4`, `25 x 30`.

## 2. LO QUE SE HIZO
- Pregunta nueva **«multiplicar»** con la pieza `multiplicar_grupos_iguales` (usa «suma_de_iguales»:
  no hay ninguna cuenta nueva). Condicion `los_grupos_tienen_nombre_x`.
- Parte nueva `sistema/partes/multiplicar.py`: lee `3 x 4`, `3 × 4`, `3 * 4`, `3 grupos de 4` y
  `grupos de 2, 3 y 4`; dice que es cada numero, dibuja los grupos, escribe la suma repetida y el producto.
- `3 x 4` ya no lo coge `filas.py` (solo filas y columnas). Y una puerta que habria mentido, cerrada
  antes de abrirse: `3 x 4 = ?` se leia como `4 = ?`; ahora las ecuaciones con x dicen «todavia no».
- La guarda de las partes («un nombre, una parte») cazo `_POR` repetido en filas y multiplicar.
- `pruebas/test_M1_multiplicar.py` (16 afirmaciones; las 121 de 0 a 10 y 150 hasta mil contra el
  testigo). Ayuda, `mis_pruebas.txt` (7) y `mis_casos.txt` (9 + el de M.0 que cambia).

## 3. RESULTADO
- `3 x 4` -> «3 grupos de 4 (el 3 dice CUANTOS GRUPOS; el 4, CUANTOS HAY EN CADA UNO)», el dibujo
  (o o o o)  (o o o o)  (o o o o), 4 + 4 + 4, y 3 x 4 = 12.
- `4 x 0` -> grupos vacios: 0.  `grupos de 2, 3 y 4` -> no son iguales: 9 sumando.  `40 x 30` -> pasa de mil.
- Proyecto: **1699/1699 afirmaciones + 445/445 casos — VERDE**.

## 4. LO QUE SIGUE (del plan)
- **M.2**: las tablas del 2, 5 y 10 y la conmutativa (NCETM 2.3–2.5: 3 x 4 = 4 x 3; dobles y mitades),
  y aprenderlas de memoria como las sumas (ganadas).  Despues **M.3** dividir (NCETM 2.6).

## 5. PENDIENTE: la prueba de Carlos
