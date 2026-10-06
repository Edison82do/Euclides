# Paso F.5 — MULTIPLICAR UN ENTERO POR UNA FRACCIÓN — 7 oct 2026 (madrugada)

Sigue al D.3 (4.º). NCETM Spine 3, Year 4 (el último de fracciones de 4.º).

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (NCETM 3.6, leído el 7 oct; Common Core 4.NF.B.4).**
1. «Sumar varias veces una fracción (propia o impropia) se puede escribir como **multiplicar una fracción
   por un entero**»: 2/5 + 2/5 + 2/5 = 3 × 2/5 = 6/5.
2. «… y lo mismo con un **número mixto**»: 1 2/5 + 1 2/5 + 1 2/5 = 3 × 1 2/5.
3. «Hallar una fracción unitaria de una cantidad se puede escribir como **un entero por una fracción**»:
   1/4 de 12 = 12 × 1/4 = 3.
4. «Una fracción no unitaria de una cantidad se calcula hallando primero la unitaria» (3/4 de 12: 1/4 es 3,
   y 3 de esos son 9) — ya lo hace F.2.
5. «Si se conoce una fracción no unitaria, se halla la unitaria y luego el entero» — ya lo hace F.2
   (`entero: 3/4 es 9`).
- Common Core 4.NF.B.4: a/b como a × (1/b); n × (a/b) = (n × a)/b; problemas.

**Lo que se construye** (en `fracciones.py`).
- `3 x 2/5` → tres veces 2/5: 2/5 + 2/5 + 2/5 = 6/5 = 1 1/5 (el de arriba se multiplica; el de abajo, el
  tamaño de las partes, no cambia).
- `3 x 1 2/5` → partiendo: 3 × 1 = 3 y 3 × 2/5 = 6/5; 3 + 6/5 = 4 1/5; y por impropias: 3 × 7/5 = 21/5.
- `12 x 1/4` y `1/4 x 12` → 3: es 1/4 de 12 (repartir); y también 12/4 (las dos lecturas, de acuerdo).
- `12 x 3/4` → 36/4 = 9 (y 3/4 de 12 = 9).

**Las trampas.**
- `3 x 2/5` → 6/5 = 1 1/5 (no 6/15: el de abajo no se multiplica).
- `3 x 1 2/5` → 4 1/5 (no 3 2/5: también se multiplican las partes).
- `5 x 1/5` → 1.   `0 x 3/4` → 0.   `4 x 3/4` → 3.
- `2/3 x 3/4` → todavía no (fracción por fracción: 6.º, NCETM 3.9).

**Prueba de dominio.** n × a/b y n × (mixto) para n de 0 a 12 y b de 2 a 12 (muestra), contra el
testigo; las dos lecturas de acuerdo cuando la cantidad se reparte justa.

**Para Carlos:** `3 x 2/5`, `3 x 1 2/5`, `12 x 3/4`, `1/4 x 12`.

## 2. LO QUE SE HIZO
- `fracciones.py`: `n x a/b`, `a/b x n` y `n x (mixto)`: sumar la fracción una y otra vez (se cuentan las
  partes: n × a; el de abajo no cambia); con mixtos, partiendo (enteros y partes) y por impropias, de
  acuerdo; con una fracción sola, también la otra lectura (a/b **de** n: repartir y tomar) cuando se
  reparte justo. Fracción por fracción: todavía no (6.º).
- `pruebas/test_F5_entero_por_fraccion.py` (8 afirmaciones; 300 productos contra el testigo, sin
  simplificar — simplificar es de 5.º). Ayuda, `mis_pruebas.txt` (3), `mis_casos.txt` (4).

## 3. RESULTADO
- `3 x 2/5` → «2/5 + 2/5 + 2/5 = 6 quintos» = 1 1/5.  `3 x 1 2/5` → 4 1/5 (3 + 6/5; y 21/5).
- Proyecto: **2131/2131 afirmaciones + 614/614 casos — VERDE** (108 s).
- **Con F.5 queda completo Spine 3 de 4.º** (3.5, 3.6).

## 4. PENDIENTE: la prueba de Carlos.  Sigue G.1: área y perímetro (NCETM 2.16).
