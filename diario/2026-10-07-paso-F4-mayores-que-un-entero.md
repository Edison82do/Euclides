# Paso F.4 — FRACCIONES MAYORES QUE UN ENTERO: NÚMEROS MIXTOS E IMPROPIAS — 7 oct 2026 (madrugada)

Sigue al M.11. NCETM Spine 3, Year 4 (en F.1–F.3 «más de un entero» decía «todavía no: 4.º»).

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (NCETM 3.5, leído el 7 oct; Common Core 4.NF.B.3).**
1. «Las cantidades hechas de **enteros y partes** se pueden escribir como **números mixtos**» (1 3/4).
2. «Los números mixtos se pueden poner en la **recta numérica**.»
3. «Saber comparar fracciones propias ayuda a comparar números mixtos» (primero los enteros; si son
   iguales, las partes).
4. «Los números mixtos se pueden **partir y juntar** igual que los enteros» (2 3/4 + 1 1/4: enteros con
   enteros, partes con partes).
5. «Los números mixtos se pueden escribir como **fracciones impropias**» (1 3/4 = 7/4) — y al revés.
6. «Las fracciones impropias se **suman y restan** igual que las propias» (5/4 + 3/4 = 8/4 = 2).
- Cómo, sin calculadora: 7/4 → ¿cuántos enteros caben? Es **agrupar 7 cuartos en grupos de 4** (la
  división con resto, M.8): 1 entero y sobran 3 cuartos.  2 3/4 → 2 enteros son 2 × 4 = 8 cuartos, y 3
  más: 11 cuartos.

**Lo que se construye** (en `fracciones.py`; se quita el «todavía no» de más de un entero).
- `fraccion: 7/4` → «siete cuartos = 1 entero y 3/4» (con la división 7 : 4 = 1 resto 3).
- `mixto: 2 3/4` → 11/4 (y la vuelta 11 : 4 = 2 resto 3).
- `recta: 7/4` → la recta de 0 a 2.
- `7/4 de 12` → 21.   `entero: 5/4 es 15` → 12.
- `5/4 + 3/4` → 8/4 = 2;  `7/4 - 2/4` → 5/4 = 1 1/4;  `2 3/4 + 1 1/4` → 4 (partiendo: 3 + 4/4; y por
  impropias: 11/4 + 5/4 = 16/4, de acuerdo);  `3 - 1/4` → 2 3/4.
- `comparar: 2 1/4 y 1 3/4` → por los enteros;  `comparar: 2 1/4 y 2 3/4` → por las partes;
  `comparar: 7/4 y 9/4` → mismo denominador.

**Las trampas.**
- `fraccion: 7/4` → 1 3/4 (no «siete cuartos no se puede»).   `fraccion: 8/4` → 2 enteros justos.
- `mixto: 2 3/4` → 11/4 (no 6/4 sumando 2 + 3 + … ni 23/4).
- `2 3/4 + 1 1/4` → 4 (no 3 4/8: el denominador no se suma).
- `comparar: 2 1/4 y 1 3/4` → 2 1/4 mayor (no «3/4 es más que 1/4»).
- `1/2 + 1/4` → sigue «todavía no» (distinto abajo: 5.º).

**Prueba de dominio.** Impropias ↔ mixtos para b de 2 a 12 y hasta 5 enteros, contra el testigo y ida y
vuelta; sumas y restas con el mismo denominador hasta 5 enteros; comparar mixtos.

**Para Carlos:** `fraccion: 7/4`, `mixto: 2 3/4`, `recta: 7/4`, `2 3/4 + 1 1/4`, `comparar: 2 1/4 y 1 3/4`.

## 2. LO QUE SE HIZO
- `fracciones.py` deja de decir «todavía no» a más de un entero:
  - `fraccion: 7/4` → «siete cuartos = 1 3/4», agrupando los cuartos de cuatro en cuatro (la división con
    resto, M.8); con las tiras de los enteros.
  - `mixto: 2 3/4` → 11/4 (2 × 4 + 3), con la vuelta.
  - `recta: 7/4` → la recta hasta el 2 (los enteros que hagan falta).
  - `a/b de n`, `entero:` y las sumas/restas con el mismo de abajo admiten impropias (5/4 + 3/4 = 2).
  - Cuentas con **números mixtos y enteros** (`2 3/4 + 1 1/4`, `3 - 1/4`): por dos caminos que tienen
    que coincidir — partiendo (enteros con enteros, partes con partes, reagrupando o **cambiando** un
    entero por b/b) y por impropias.
  - `comparar: 2 1/4 y 1 3/4`: primero los enteros, luego las partes.
- Pruebas que decían «más de un entero: todavía no» (F2 A3, F3 A7/B1 y dos casos) pasan a la respuesta.
- `pruebas/test_F4_mayores_que_un_entero.py` (15 afirmaciones: trampas; mixtos ↔ impropias para b de 2 a
  12 y hasta 5 enteros; 250 cuentas por los dos caminos; 200 comparaciones). Ayuda, `mis_pruebas.txt`
  (4), `mis_casos.txt` (5).

## 3. RESULTADO
- `2 3/4 + 1 1/4` → 4 («3 enteros y 4/4 → 4 enteros justos»; «11/4 + 5/4 = 16/4»).  `3 - 1/4` → 2 3/4.
- Proyecto: **2076/2076 afirmaciones + 593/593 casos — VERDE** (98 s).

## 4. PENDIENTE: la prueba de Carlos.  Sigue D.1: las décimas (NCETM 1.23).
