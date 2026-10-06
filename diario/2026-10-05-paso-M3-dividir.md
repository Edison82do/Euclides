# Paso M.3 — DIVIDIR: REPARTIR Y AGRUPAR — 5 oct 2026

Carlos probó M.2 («ya probé») → se empieza M.3.

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (mirando antes `FUENTES.md`): NCETM 2.6** (*Structures: quotitive and partitive
division*, Year 2), sus puntos:
1. «Los objetos se pueden agrupar en partes iguales, **a veces con resto**».
2. **Agrupar** (cuotitiva): se sabe el total (**dividendo**) y el tamaño del grupo (**divisor**); el
   número de grupos (**cociente**) se halla **contando de divisor en divisor**.
3. **Repartir** (partitiva): se sabe el total y **entre cuántos** se reparte (divisor); lo que le toca
   a cada uno (cociente) se halla también contando de divisor en divisor (una ronda = uno para cada uno).
4. Para ir rápido: **los hechos de multiplicar que ya se saben** y, si el divisor es 2, **la mitad**.
5. «Si el dividendo es **cero**, el cociente es cero; si el dividendo es **igual** al divisor, es uno;
   si el divisor es **uno**, el cociente es el dividendo».
- Common Core **3.OA.A.2** (12 ÷ 3 como reparto o como grupos) y **3.OA.B.6** (la división como un
  **factor desconocido**: 12 ÷ 3 es el número que por 3 da 12) → la comprobación es multiplicar.
- La trampa clásica: **dividir entre cero** no tiene sentido (no se puede repartir entre nadie; los
  grupos de cero nunca se llenan).

**Lo que se construye.**
- Pregunta nueva **«dividir»** con piezas (la más corta que encaja):
  - `dividir_casos_especiales` (1): el punto 5 de NCETM, sin calcular.
  - `dividir_con_la_tabla` (3): si en la memoria hay un producto que da el total con ese divisor
    (6 x 5 = 30 → 30 ÷ 5 = 6) (punto 4).
  - `dividir_a_la_mitad` (5): si el divisor es 2, la mitad haciendo parejas (punto 4).
  - `dividir_saltando` (20): contar de divisor en divisor hasta el total y contar los saltos; lo que
    no llega a otro salto es el **resto** (puntos 1–3).
- Órdenes: `12 en grupos de 3` (agrupar), `12 entre 3` (repartir), `12 : 3` / `12 ÷ 3` / `12 / 3`
  (las dos lecturas). Dibujo para totales pequeños. Nombres: dividendo, divisor, cociente, resto.
- **La comprobación**: cociente × divisor (+ resto) = dividendo, con lo de M.1/M.2.

**Las trampas.**
- `12 en grupos de 3` → 4 grupos.   `12 entre 3` → 4 para cada uno.   `12 : 3` → las dos lecturas.
- `13 en grupos de 3` → 4 grupos y sobra 1.   `14 entre 2` → 7 (la mitad).   `30 : 5` → 6 (la tabla).
- `0 : 4` → 0;  `7 : 7` → 1;  `9 : 1` → 9 (sin calcular).   `8 : 0` → no se puede.
- `3 : 5` → 0 y sobran 3 (no llega para un grupo).

**Prueba de dominio.** Todas las divisiones de 0 a 100 entre 1 a 10 contra el testigo (cociente y
resto), cada pieza donde le toca, la comprobación siempre cierta; las trampas.

**Para Carlos:** `12 en grupos de 3`, `12 entre 3`, `13 : 3`, `30 : 5`, `14 entre 2`, `8 : 0`.

## 2. LO QUE SE HIZO
- Pregunta nueva **«dividir»** con 4 piezas: `dividir_casos_especiales` (1), `dividir_con_la_tabla` (3,
  factor desconocido en la memoria), `dividir_a_la_mitad` (5), `dividir_saltando` (20, con el resto).
  Condiciones: `el_divisor_no_es_cero` (de aplicacion: si falla es IMPOSIBLE), `es_un_caso_especial`,
  `el_divisor_es_dos`, `la_division_esta_en_las_tablas`.
- Parte nueva `sistema/partes/dividir.py`: `12 entre 3` (repartir), `12 en grupos de 3` (agrupar),
  `12 : 3` / `12 ÷ 3` / `12 / 3` (las dos lecturas); dibuja los grupos o el reparto; nombra dividendo,
  divisor, cociente y resto; COMPRUEBA multiplicando (cociente x divisor + resto).
- La guarda de las partes volvio a cazar un nombre repetido (`_GRUPOS` en multiplicar y dividir).
- `pruebas/test_M3_dividir.py` (16 afirmaciones; las 1010 divisiones de 0 a 100 entre 1 a 10 contra el
  testigo, todas comprobadas). Ayuda, `mis_pruebas.txt` (7) y `mis_casos.txt` (9).

## 3. RESULTADO
- `12 en grupos de 3` -> 3, 6, 9, 12: 4 grupos (y el dibujo).  `12 entre 3` -> 4 para cada uno.
- `13 : 3` -> 4 y sobra 1 (4 x 3 + 1 = 13).  `30 : 5` -> 6 con la tabla.  `8 : 0` -> no se puede.
- Proyecto: **1744/1744 afirmaciones + 464/464 casos — VERDE**.

## 4. PENDIENTE: la prueba de Carlos.  Lo que sigue: E.4 (ecuaciones con x y : ; dos pasos).
