# Paso D.2 — CENTÉSIMAS Y MILÉSIMAS — 7 oct 2026 (madrugada)

Sigue al D.1 (4.º). NCETM Spine 1, Year 4.

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (NCETM 1.24, leído el 7 oct; Common Core 4.NF.C.5–7).**
1. «Cuando el uno se parte en **100** partes iguales, cada una es **una centésima**; y cuando **una
   décima** se parte en diez partes iguales, cada parte es **una centésima**.»
2. «0.01 es una centésima; el uno es cien veces 0.01; **0.1 es diez veces 0.01**.»
3. «Se cuenta de centésima en centésima hasta el uno y pasándolo.»
4. «Se componen sumando y multiplicando» (2.35 = 2 + 0.3 + 0.05 = 235 × 0.01).
5. Se usan en medidas, escalas y gráficas.
6. «Las columnas y lo que ya se sabe sirven igual que con décimas.»
7. «Se redondea **a la décima** mirando la cifra de las centésimas, o **al entero** mirando la de las
   décimas.»
8. «Partiendo el uno en **1000** partes, cada una es **una milésima**; lo de décimas y centésimas sirve
   para milésimas.»
- Common Core 4.NF.C.5 (3/10 = 30/100), 4.NF.C.6 (0.62 = 62/100), **4.NF.C.7 (comparar dos decimales
  hasta las centésimas razonando sobre su tamaño)** — el error documentado: «0.45 es más que 0.5 porque
  45 es más que 5». Se compara cifra a cifra **desde el punto**, rellenando con ceros (0.50 y 0.45).

**Lo que se construye** (en `decimales.py`, que ya estaba preparado: el número de cifras detrás del punto
pasa de 1 a 3; en `fracciones.py`, los de abajo 100 y 1000).
- `decimal: 2.35` → 2 enteros, 3 décimas y 5 centésimas = 235 centésimas = 2 + 0.3 + 0.05.
- `2.35 + 1.7` (se alinean los puntos: 1.70), `5 - 0.25`, `0.125 + 0.875`.
- `comparar: 0.5 y 0.45` → 0.5 mayor (0.50 contra 0.45).
- `redondear: 2.35 a la decima` → 2.4;  `redondear: 2.35` → 2 (al entero).
- `de 0.01 en 0.01 desde 0.97` → 0.98, 0.99, 1, 1.01 …
- `fraccion: 35/100` → 0.35;  `fraccion: 3/10` → 0.3 = 30/100.

**Las trampas.**
- `comparar: 0.5 y 0.45` → 0.5 > 0.45 (no «45 > 5»).   `comparar: 0.3 y 0.30` → iguales.
- `2.35 + 1.7` → 4.05 (no 2.52 sumando 35 + 17).   `5 - 0.25` → 4.75.   `0.125 + 0.875` → 1.
- `de 0.01 en 0.01 desde 0.98` → 0.99, 1, 1.01 (no 0.100).
- `redondear: 2.95 a la decima` → 3 (sube y arrastra).   `0.1234` → todavía no (diezmilésimas).

**Prueba de dominio.** Sumas y restas con hasta tres cifras decimales mezcladas, comparaciones (con las
de «más cifras») y redondeos a la décima y al entero, contra un testigo que cuenta en milésimas enteras.

**Para Carlos:** `decimal: 2.35`, `comparar: 0.5 y 0.45`, `2.35 + 1.7`, `redondear: 2.35 a la decima`.

## 2. LO QUE SE HIZO
- `decimales.py`: hasta **tres cifras** detrás del punto (décimas, centésimas, milésimas):
  - `decimal: 2.35` (las cifras en su sitio; 235 centésimas; 2 + 0.3 + 0.05; qué es una centésima).
  - Cuentas con distinto número de cifras: se **alinean los puntos** (1.7 = 1.70); las columnas de
    derecha a izquierda (la más pequeña primero), llevando y cambiando — también a través de ceros (5 −
    0.25: «las columnas de en medio, que estaban a 0, se quedan en 9»).
  - `comparar: 0.5 y 0.45` → «se escriben con las mismas cifras: 0.50 y 0.45» (el error «45 > 5»).
  - `redondear: 2.35 a la decima` (mirando las centésimas) y al entero (mirando las décimas).
  - `de 0.01 en 0.01 …` y `de 0.001 en 0.001 …`.
- `fracciones.py`: los de abajo 100 y 1000 (centésimos, milésimos), con su escritura con punto, y
  `3/10 = 30/100` (4.NF.C.5).
- Límite honesto: se cuenta en la unidad más pequeña, y la lista llega a diez mil: con milésimas, hasta
  10; con centésimas, hasta 100; más allá dice «todavía no» (lo levantará 5.º, con el millón).
- `pruebas/test_D2_centesimas_milesimas.py` (13 afirmaciones; 300 cuentas, 300 comparaciones con
  distinto número de cifras, 572 redondeos; testigo en milésimas enteras). D1 A9 pasa a la respuesta.
  Ayuda, `mis_pruebas.txt` (4), `mis_casos.txt` (5).

## 3. RESULTADO
- `comparar: 0.5 y 0.45` → 0.5 > 0.45.  `2.35 + 1.7` → 4.05.  `5 - 0.25` → 4.75.
- Proyecto: **2109/2109 afirmaciones + 605/605 casos — VERDE** (99 s).

## 4. PENDIENTE: la prueba de Carlos.  Sigue D.3: el dinero (NCETM 1.25).
