# Paso M.2 — LAS TABLAS DEL 2, 5 Y 10; LA CONMUTATIVA; DOBLES Y MITADES — 5 oct 2026

Carlos: «Bien, adelante» (tras M.1) → se empieza M.2.

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (mirando antes `FUENTES.md`): NCETM, segmentos 2.3, 2.4 y 2.5 (Year 2).**
- **2.3** (*Times tables: groups of 2 and commutativity, part 1*):
  1. «El número de grupos es un **factor**, el tamaño del grupo es un **factor**, y el total es el
     **producto**». Contar de dos en dos sirve cuando los grupos son de dos.
  2. «Contar de dos en dos es la **tabla del 2**. Dos productos seguidos se diferencian en dos».
  3. «Los factores se pueden escribir **en cualquier orden** y el producto es el mismo» (conmutativa).
- **2.4** (*groups of 10 and of 5, and factors of 0 and 1*): las tablas del 10 y del 5 (seguidos se
  diferencian en 10 / en 5); «cuando **cero** es un factor, el producto es cero; cuando **uno** es un
  factor, el producto es el otro factor».
- **2.5** (*Commutativity part 2, doubling and halving*): la misma multiplicación tiene **dos
  lecturas** de grupos (3 × 5: 3 grupos de 5 o 5 grupos de 3), y un problema de 5 grupos se resuelve
  con la tabla del 5; «si **dos** es un factor, se usan los **dobles**»; «la **mitad** es lo
  contrario del doble».
- La memoria (paso 3, Baroody): las tablas se **aprenden después** de calcularlas y comprobarlas.
- Lo que no entra aún: las demás tablas (3.OA.C.7, más adelante) y dividir (M.3).

**Lo que se construye (piezas de «multiplicar», la más corta que encaja):**
- `multiplicar_por_cero_o_uno` (1): «cero es un factor → 0; uno es un factor → el otro» (2.4).
- `recordar_producto` (1): si la tabla ya se aprendió (y se vuelve a comprobar).
- `multiplicar_con_dobles` (6): si un factor es 2, es el **doble** del otro (7 × 2 = 7 + 7) (2.5).
- `multiplicar_dando_la_vuelta` (8): 5 × 7 = 5 grupos de 7, pero se lee también como **7 grupos de
  5** y se cuenta con la tabla del 5: 5, 10 … 35 (2.3 y 2.5: conmutativa).
- `multiplicar_grupos_iguales` (20): la de M.1.
- Ordenes: `tabla del 2` / `del 5` / `del 10` (cada producto es el anterior más 2, 5 o 10);
  `aprender: tablas` (las tres tablas, comprobadas por las dos lecturas); `mitad: 14` (lo contrario
  del doble: hasta 20, haciendo parejas, y se comprueba con el doble).
- **El `=` con ×** (E.0): `verdad: 3 x 4 = 4 x 3` → VERDADERO sin calcular (los factores al revés).
- Y en la explicación de `a x b`: los nombres **factor** y **producto**.

**Las trampas.**
- `5 x 7` → dando la vuelta: 7 grupos de 5 (5, 10 … 35).   `7 x 5` → 7 grupos de 5, sin vuelta.
- `2 x 9` y `9 x 2` → el doble de 9.   `0 x 8`, `8 x 1` → sin calcular.
- `3 x 4` → ni 2, ni 5, ni 10: grupo a grupo (las otras tablas llegan después).
- `verdad: 3 x 4 = 4 x 3` → verdadero sin calcular.   `verdad: 3 x 4 = 3 + 4` → falso.
- `mitad: 14` → 7 (7 + 7 = 14).   `mitad: 7` → no tiene mitad exacta (es impar).
- `tabla del 3` → todavía no.
- Después de `aprender: tablas`: `6 x 5` de memoria; `3 x 4` sigue sin estar.

**Prueba de dominio.** Las tres tablas contra el testigo; cada pieza donde le toca; las dos lecturas
dan lo mismo; la memoria de tablas comprobada; las trampas.

**Para Carlos:** `tabla del 5`, `5 x 7`, `2 x 9`, `0 x 8`, `verdad: 3 x 4 = 4 x 3`, `mitad: 14`.

## 2. LO QUE SE HIZO
- 4 piezas nuevas de «multiplicar»: `multiplicar_por_cero_o_uno` (1), `recordar_producto` (1, se
  recomprueba con la otra lectura), `multiplicar_con_dobles` (6), `multiplicar_dando_la_vuelta` (8).
  Condiciones: `un_factor_es_cero_o_uno`, `un_factor_es_dos`, `la_otra_lectura_se_salta`,
  `el_producto_esta_en_la_memoria`.
- `multiplicar.py`: `tabla del 2/5/10`, `mitad: N` (hasta 20, con parejas, comprobada con el doble),
  y en cada multiplicacion: lo que prueba y descarta, y los nombres FACTOR y PRODUCTO.
- `memoria.py`: `aprender: tablas` (57 productos: las tres tablas en las dos lecturas; cada uno
  calculado sin memoria y comprobado con la otra lectura). Aprendidas en la memoria de verdad: 257 hechos.
- El = con x (E.0): `3 x 4 = 4 x 3` VERDADERO sin calcular (las piezas de igualdad aceptan x).
- `pruebas/test_M2_tablas.py` (23 afirmaciones). Ayuda, `mis_pruebas.txt` (8), `mis_casos.txt` (10).
  `test_M1` D1 cambia: 5 x 2 ahora sale por el doble (antes saltando): el sistema eligio lo mas corto.

## 3. RESULTADO
- `5 x 7` -> «5 grupos de 7, pero tambien 7 grupos de 5: con la tabla del 5: 5, 10 ... 35».
- `2 x 9` -> el doble de 9.  `0 x 8` -> sin calcular.  `6 x 5` -> de memoria (tras aprender).
- `mitad: 14` -> 7, comprobada con 7 + 7.  `tabla del 3` -> todavia no.
- Proyecto: **1725/1725 afirmaciones + 455/455 casos — VERDE**.

## 4. PENDIENTE: la prueba de Carlos.  Lo que sigue: M.3 dividir (repartir y agrupar; NCETM 2.6).
