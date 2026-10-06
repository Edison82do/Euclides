# Paso S.1 — «VECES» Y FRACCIONES PARA COMPARAR: LA ESCALA — 7 oct 2026 (madrugada)

Sigue al G.1. Es el último segmento de 4.º en NCETM Spine 2.

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (NCETM 2.17, leído el 7 oct; Common Core 4.OA.A.1–2).**
1. «Una longitud más larga se puede describir a partir de una más corta con el lenguaje de **"veces"**;
   si se sabe la corta, la larga se calcula **multiplicando**.»
2. «Una más corta se describe a partir de la larga con el lenguaje de las **fracciones**; si se sabe la
   larga, la corta se calcula **dividiendo**.»
3. «Otras medidas se comparan igual, con "veces" y fracciones.»
- Common Core 4.OA.A.1: «35 = 5 × 7 es: 35 es **5 veces** 7, y 7 veces 5»; 4.OA.A.2: problemas de
  **comparación multiplicativa**, distinguiéndolos de la comparación **aditiva** (el error documentado:
  «4 veces más largo» leído como «4 cm más»).
- Es el esquema de COMPARACIÓN (R.1/CGI) pero multiplicativo: cantidad pequeña, cantidad grande, «veces».

**Lo que se construye** (parte nueva `sistema/partes/escala.py`).
- `veces: 4 veces 6` → 24.   `cuantas veces: 24 y 6` → 24 es 4 veces 6, y 6 es 1/4 de 24.
- Problemas con pocas palabras:
  - «La cuerda roja mide 6 cm. La azul es 4 veces mas larga. ¿Cuánto mide la azul?» → 24 (multiplicar).
  - «La azul mide 24 cm. Es 4 veces mas larga que la roja. ¿Cuánto mide la roja?» → 6 (dividir).
  - «La azul mide 24 cm. La roja mide 1/4 de la azul. ¿Cuánto mide la roja?» → 6 (la fracción, F.1).
  - «La azul mide 24 cm y la roja 6 cm. ¿Cuántas veces es más larga la azul?» → 4.
- En cada uno, el aviso: «4 veces más NO es 4 más (eso sería 10)».

**Las trampas.**
- 4 veces 6 → 24 (no 10).   «24 es 4 veces la roja» → 6 (no 96 ni 20).   1/4 de 24 → 6.
- `cuantas veces: 25 y 6` → no es un número entero de veces (4 y sobra 1).

**Prueba de dominio.** Los cuatro tipos de problema con números de muestra contra el testigo.

**Para Carlos:** `veces: 4 veces 6`, `cuantas veces: 24 y 6`, y los problemas de las cuerdas.

## 2. LO QUE SE HIZO
- Parte nueva `sistema/partes/escala.py`: `veces: 4 veces 6`, `cuantas veces: 24 y 6`, y problemas de
  comparación multiplicativa con pocas palabras (la larga multiplicando; la corta dividiendo; la corta
  como fracción de la larga; cuántas veces, dividiendo). Siempre el aviso de la comparación aditiva.
- `pruebas/test_S1_veces.py` (9 afirmaciones; 160 problemas de los cuatro tipos). Ayuda,
  `mis_pruebas.txt` (3), `mis_casos.txt` (4).

## 3. RESULTADO
- «La azul mide 24 cm. Es 4 veces más larga que la roja. ¿Cuánto mide la roja?» → «la corta es 1/4 de
  ella: dividir, 24 : 4 = 6» → 6 cm.
- Proyecto: **2156/2156 afirmaciones + 623/623 casos — VERDE** (109 s).
- **Con S.1 queda recorrido 4.º de NCETM** (Spines 1, 2 y 3 de Year 4).

## 4. PENDIENTE: la prueba de Carlos.  Sigue 5.º: hasta un millón (NCETM 1.26).
