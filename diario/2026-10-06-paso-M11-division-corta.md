# Paso M.11 — PARTIR Y LA DIVISIÓN CORTA — 6 oct 2026 (noche)

Sigue al M.10 (4.º). NCETM Spine 2, Year 4.

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (NCETM 2.15, leído el 6 oct; Common Core 4.NBT.B.6).**
1. «Un número de dos cifras se divide entre uno de una cifra **partiéndolo** en decenas y unidades,
   dividiendo cada parte y **sumando los cocientes parciales**; si al dividir las decenas sobra alguna,
   hay que **cambiar** las decenas que sobran **por unidades** antes de dividir las unidades.»
2. «… con el algoritmo de la **división corta**, que va de la cifra **más grande** (izquierda) a la más
   pequeña (derecha); si sobra en la columna de las decenas, se **cambia**.»
3–4. Lo mismo con **tres cifras** (centenas que sobran → decenas).
- Common Core 4.NBT.B.6: cocientes y restos con dividendos de hasta cuatro cifras y divisores de una
  cifra, «usando estrategias basadas en el valor de posición … e ilustrando y explicando el cálculo».
- Es el **cambio** (*exchange*) de la resta por columnas (7.5/7.6: «cambio 1 centena por 10 decenas»),
  ahora para repartir. Y cada paso es un hecho de la tabla que se sabe de memoria (como en M.10).

**Lo que se construye.**
- Pieza `division_corta` (responde a `dividir`): de izquierda a derecha, en cada sitio «¿cuántas veces
  cabe el divisor?» con la tabla que se sabe; lo que sobra **se cambia** por diez de la columna siguiente;
  lo que sobra al final es el resto. Dibujada («la parada del autobús») y comprobada por la vuelta
  (cociente × divisor + resto, con la multiplicación).
- Orden `corta: 72 : 3` para verla aunque haya otro camino.

**Las trampas.**
- `72 : 3` → 24 (7 decenas: 2 por cabeza y sobra 1 decena → 10 unidades + 2 = 12 unidades → 4).
- `84 : 4` → 21 (sin cambiar nada).   `96 : 8` → 12.   `75 : 4` → 18 resto 3.
- `305 : 5` → 61 (3 centenas no dan 1 para cada uno: se juntan con las decenas, 30 decenas → 6).
- `4321 : 7` → 617 resto 2.   `100 : 7` → 14 resto 2.
- Sin las tablas en la memoria no se usa (y se divide de otra manera).

**Prueba de dominio.** Todas las de 10..999 entre 2..9 (muestra amplia) y una muestra hasta diez mil,
contra el testigo, con la vuelta.

**Para Carlos:** `aprender: tablas`, `72 : 3`, `corta: 305 : 5`, `4321 : 7`.

## 2. LO QUE SE HIZO
- Pieza `division_corta` (responde a `dividir`): de izquierda a derecha; en cada sitio la mayor q con
  q × divisor ≤ lo que hay (mirando la tabla en la memoria); lo que sobra **se cambia** por diez de la
  columna siguiente; si al principio no da ni una, pasa a la columna siguiente; lo que sobra al final es
  el resto. Dibujada («la parada del autobús») y con la vuelta hecha con la multiplicación.
- La explicación de `72 : 3` enseña cada línea del algoritmo; orden `corta: 72 : 3`.
- M3 C6 (31 : 5) ya no va «saltando»: va por la corta, como haría un niño de 4.º que se sabe las tablas.
- `pruebas/test_M11_division_corta.py` (9 afirmaciones; 1136 divisiones de 10..999 entre 2..9 y 150 de
  cuatro cifras, con la vuelta). Ayuda, `mis_pruebas.txt` (3), `mis_casos.txt` (3).

## 3. RESULTADO
- `corta: 4321 : 7` → «4 millares no dan para cada uno … 43 centenas : 7 = 6, sobra 1 → se cambia por 10
  decenas …» → 617 resto 2 (617 × 7 + 2 = 4321).
- Proyecto: **2059/2059 afirmaciones + 588/588 casos — VERDE** (95 s).

## 4. PENDIENTE: la prueba de Carlos (mañana).  Con M.11 queda la parte de número de 4.º en NCETM
(Spine 2 hasta 2.15).  Siguen las décimas (1.23) y las fracciones de 4.º (3.5, 3.6).
