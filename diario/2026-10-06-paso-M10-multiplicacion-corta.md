# Paso M.10 — PARTIR POR SITIOS Y LA MULTIPLICACIÓN CORTA — 6 oct 2026 (noche)

Sigue al M.9 (4.º). NCETM Spine 2, Year 4.

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (NCETM 2.14, leído el 6 oct; Common Core 4.NBT.B.5).**
1. «La distributiva sirve para multiplicar cualquier número de **dos cifras** por uno de una cifra:
   se **parte por sitios** (decenas y unidades), se multiplica cada parte y se **suman los productos
   parciales**.»  47 × 6 = 40 × 6 + 7 × 6 = 240 + 42 = 282.
2. «… y con el algoritmo de la **multiplicación corta**: las cifras bien alineadas; se empieza por la
   **derecha** (las unidades); si el producto de una columna es **diez o más**, se **reagrupa** (se
   lleva).»
3–4. Lo mismo con **tres cifras** (347 × 6 = 300 × 6 + 40 × 6 + 7 × 6).
- Primero la comprensión (partir), después el algoritmo (corta). Y Common Core 4.NBT.B.5 pide
  «ilustrar y explicar el cálculo» (ecuaciones, rectángulos, modelos de área).
- Como un humano: cada columna es **un hecho de la tabla que se sabe de memoria** (6 × 7 = 42), más lo
  que se lleva; nada de sumar 47 seis veces.

**Lo que se construye** (dos piezas nuevas de `multiplicar`, las dos solo si los hechos de una cifra
están en la memoria: son métodos de quien ya se sabe las tablas).
- `multiplicar_partiendo_por_sitios`: 347 × 6 → 300 × 6 = 1800 (3 × 6 = 18, cien veces), 40 × 6 = 240,
  7 × 6 = 42; 1800 + 240 + 42 = 2082.
- `multiplicacion_corta`: columna a columna desde la derecha: 7 × 6 = 42, escribo 2 y llevo 4; 4 × 6 =
  24, + 4 = 28, escribo 8 y llevo 2; 3 × 6 = 18, + 2 = 20: 2082. Dibujada en columnas.
- Las dos se hacen y tienen que dar lo mismo (la explicación enseña las dos).
- Orden `corta: 347 x 6` para ver el algoritmo aunque haya otro camino más corto.

**Las trampas.**
- `47 x 6` → 282 (no 2442: el error de no llevar o de escribir 42 entero en la columna).
- `347 x 6` → 2082 (llevar a través de un cero: 3 × 6 + 2 = 20).   `6 x 47` → lo mismo.
- `1234 x 9` → 11106 → se pasa de diez mil.   `25 x 4` → 100.
- Sin las tablas en la memoria, estas piezas no se usan (lo dicen) y se calcula de otra manera.

**Prueba de dominio.** Todas las de dos cifras × una cifra (10..99 × 2..9) y una muestra de tres
cifras × una cifra, por las dos piezas, contra el testigo y de acuerdo entre ellas.

**Para Carlos:** `aprender: tablas` (si no lo ha hecho), `47 x 6`, `corta: 347 x 6`.

## 2. LO QUE SE HIZO
- Piezas nuevas `multiplicar_partiendo_por_sitios` (productos parciales con las cifras subidas de sitio)
  y `multiplicacion_corta` (columna a columna desde la derecha, el hecho de la tabla más lo que se lleva;
  dibujada en columnas). Las dos solo con los hechos de una cifra **en la memoria** (si no, lo dicen y se
  calcula de otra manera).
- En la explicación de `47 x 6`, la corta se comprueba siempre partiendo por sitios. Orden nueva
  `corta: 347 x 6` (el algoritmo aunque haya otro camino).
- Dos pruebas de antes cambian de ejemplo (no de sentido): M6 B6 usa 13 × 12 para la distributiva (15 × 6
  ya va por la corta); M7 B4 acepta que 11 × 7 se aprenda por la corta.
- `pruebas/test_M10_multiplicacion_corta.py` (10 afirmaciones; **los 720 productos** de dos cifras × una
  cifra por las dos piezas; 200 de tres y cuatro cifras). Ayuda, `mis_pruebas.txt` (3), `mis_casos.txt` (3).

## 3. RESULTADO
- `corta: 347 x 6` → «7 x 6 = 42: escribo 2, llevo 4; 4 x 6 = 24, + 4 = 28 …; 3 x 6 = 18, + 2 = 20» → 2082;
  y «300 x 6 + 40 x 6 + 7 x 6 = 1800 + 240 + 42 = 2082 … lo mismo».
- Proyecto: **2049/2049 afirmaciones + 585/585 casos — VERDE** (89 s).

## 4. PENDIENTE: la prueba de Carlos (mañana).  Sigue M.11: la división corta (NCETM 2.15; 4.NBT.B.6).
