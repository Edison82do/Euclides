# Paso E.5 — DOS PASOS, CON LA LETRA COMO HUECO — 6 oct 2026

Carlos probó M.6 («ya probé») → se empieza E.5 (paso 14, el último del plan ajustado).

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (mirando antes `FUENTES.md`).**
- Common Core **3.OA.D.8**: «resolver problemas de **dos pasos** con las cuatro operaciones;
  **representarlos con ecuaciones con una letra** en lugar de la cantidad desconocida; valorar si la
  respuesta es razonable con cálculo mental y **estimación** (redondeando)».
- Su nota: los alumnos deben hacer las operaciones **en el orden de siempre** cuando no hay paréntesis
  (primero × y ÷, luego + y −, de izquierda a derecha).
- **La letra es un hueco con nombre** (el puente al álgebra; es lo que en el plan antiguo era E.5).
- **Pólya** / «trabajar hacia atrás»: si la letra está dentro (`3 x n + 2 = 14`), se **deshace** de
  fuera hacia dentro: 3 × n = 14 − 2 = 12; n = 12 : 3 = 4.
- **Singapur / esquemas**: un problema de dos pasos es **un esquema y luego otro** (primero los grupos
  iguales, luego lo que cambia).
- La **estimación redondeando** (3.NBT.A.1) Euclides todavía no la tiene: aquí la comprobación será
  **poner el número en la letra** (E.0). Redondear queda apuntado como el paso siguiente.

**Lo que se construye.**
- Una parte nueva `sistema/partes/letra.py`: lee ecuaciones con **letra** (cualquier letra; la `x`
  es letra si está donde va un número y signo de multiplicar si está entre dos números) y con **dos o
  más operaciones** y paréntesis; las calcula **en el orden de siempre**, paso a paso, con las piezas;
  y si la letra está dentro, **deshace** hacia atrás. Comprueba sustituyendo.
- Problemas de dos pasos con pocas palabras (R.2 + un cambio): «Ana tiene 3 bolsas con 4 caramelos
  cada una. Se come 5. ¿Cuántos le quedan?» → el esquema de grupos iguales (12) y luego quitar (7); y
  escribe la ecuación con letra: `3 x 4 - 5 = c`.

**Las trampas.**
- `3 x 4 - 5 = c` → c = 7 (primero la multiplicación).   `2 + 3 x 4 = n` → 14, **no 20**.
- `(2 + 3) x 4 = n` → 20 (el paréntesis manda).
- `3 x n + 2 = 14` → n = 4 (deshacer).   `x + 5 = 12` → x = 7 (la x es letra).   `20 - 2 x n = 8` → 6.
- `n + n = 10` → la letra dos veces: todavía no.   `3 x n + 2 = 13` → no hay número entero.
- «Ana tiene 3 bolsas con 4 caramelos cada una. Le dan 5. ¿Cuántos tiene ahora?» → 17.

**Prueba de dominio.** Muestra de expresiones de dos operaciones contra el testigo (orden de siempre);
la letra en cada sitio, deshaciendo, comprobada; los problemas de dos pasos.

**Para Carlos:** `3 x 4 - 5 = c`, `2 + 3 x 4 = n`, `(2 + 3) x 4 = n`, `3 x n + 2 = 14`, `x + 5 = 12`,
y el problema de las bolsas.

## 2. LO QUE SE HIZO
- Parte nueva `sistema/partes/letra.py`: lee ecuaciones con **una letra** (cualquiera; la `x` es letra
  si va donde un numero y «por» si va entre dos numeros; `?` tambien vale) y con dos o mas operaciones y
  parentesis. Calcula **en el orden de siempre** (primero x y :, luego + y -, de izquierda a derecha),
  cuenta a cuenta y con las piezas; si la letra esta dentro, **deshace** de fuera hacia dentro. Siempre
  **comprueba poniendo el numero en la letra**. Avisa del orden cuando se mezclan sin parentesis.
- Respuestas honestas: `todavia_no` (la letra dos veces, o dos letras), `no_sale` (no hay entero),
  `sin_letra` (eso es una igualdad: `verdad:`).
- `resolver_r2.py`: problemas de **dos pasos** (grupos iguales y luego un cambio: «se come 5», «le dan
  5»), con la ecuacion escrita con letra (`3 x 4 - 5 = c`) y resuelta tambien por su lado.
- Las puertas que podian mentir, cerradas: `8 + 4 = ? + 5` sigue en la balanza (E.2), `8 + ? = 11` en
  E.1, `verdad: ...` y `3 x 4 = 4 x 3` (sin letra ni hueco) siguen siendo una igualdad (E.0) — esta
  ultima la cazo `mis_pruebas.txt` y ya esta tapada.
- `pruebas/test_E5_dos_pasos_letra.py` (31 afirmaciones: trampas; 120 expresiones contra el testigo;
  60 ecuaciones con la letra en cada uno de los 3 sitios; la x; los problemas; el probador). Ayuda,
  `mis_pruebas.txt` (6), `mis_casos.txt` (8). La auditoria «sin calculadora» paso tras quitar tres
  sumas de Python del lector (ahora toma las piezas de una en una, sin contar posiciones).

## 3. RESULTADO
- `3 x 4 - 5 = c` -> c = 7.  `2 + 3 x 4 = n` -> 14 (y el OJO del orden).  `(2 + 3) x 4 = n` -> 20.
- `3 x n + 2 = 14` -> deshace: 14 - 2 = 12, 12 : 3 = 4.  `x + 5 = 12` -> 7.  `n + n = 10` -> todavia_no.
- Bolsas: «se come 5» -> 7 caramelos; «le dan 5» -> 17.
- Proyecto: **1865/1865 afirmaciones + 517/517 casos — VERDE**.

## 4. PENDIENTE: la prueba de Carlos.  Con E.5 se termina el plan ajustado (pasos 9 a 14).
Lo que dice la pedagogia que sigue (a proponer, no empezado): la **estimacion redondeando** (3.NBT.A.1,
la otra mitad de 3.OA.D.8: «¿es razonable?»), y despues NCETM Year 4 (2.11 tablas del 11 y 12, 2.12
division con resto, 2.13 x y : por 10 y 100).
