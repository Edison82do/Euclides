# Paso D.1 — LAS DÉCIMAS — 7 oct 2026 (madrugada)

Sigue al F.4 (4.º). NCETM Spine 1, Year 4.

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (NCETM 1.23, leído el 7 oct; Common Core 4.NF.C.6).**
1. «Cuando el uno se parte en **diez partes iguales**, cada parte es **una décima** del entero» (F.1:
   1/10).
2. «Las décimas se pueden escribir como **fracciones decimales**: 0.1 es una décima; **el uno es diez
   veces 0.1**.»
3. «Se puede **contar de décima en décima** hasta el uno **y pasarlo**» (0.8, 0.9, 1, 1.1 …).
4. «Los números con décimas se **componen** sumando y multiplicando» (2.3 = 2 + 0.3 = 23 × 0.1).
5. «Los hechos y estrategias que ya se saben, **también las columnas**, sirven con décimas.»
6. «Se redondea al entero más cercano **mirando la cifra de las décimas**.»
- Common Core 4.NF.C.6: escribir 62/100 como 0.62; localizar 0.62 en la recta (aquí, las décimas).
- Cómo, sin calculadora (el *unitising* de siempre, 6.2 / N.3): **la décima es una cosa**: 2.7 + 1.5 son
  27 décimas + 15 décimas = 42 décimas = 4.2. Diez décimas hacen un entero, como diez unidades una
  decena. En columnas: se alinean las comas (el punto) y se lleva de las décimas a las unidades.
- Se escribe con **punto** (como NCETM y como en la República Dominicana); se acepta también la coma.

**Lo que se construye** (parte nueva `sistema/partes/decimales.py`).
- `decimal: 2.3` → 2 enteros y 3 décimas = 23 décimas = 2 + 0.3 = 2 + 3/10; en la recta entre 2 y 3.
- `de 0.1 en 0.1 desde 0.7` → 0.8, 0.9, 1, 1.1 … (pasando el uno).
- `2.7 + 1.5`, `4.2 - 1.5` → en columnas (con el punto alineado), y comprobado contando en décimas.
- `comparar: 2.3 y 1.9` → por las cifras (los enteros primero).
- `redondear: 2.7` → 3 (la cifra de las décimas, 7, de cinco para arriba).
- `fraccion: 3/10` dice también «= 0.3».
- Centésimas (2.35): todavía no (D.2).

**Las trampas.**
- `decimal: 0.3` → 3 décimas, entre 0 y 1.   `decimal: 1.0` → 10 décimas = 1.
- `2.7 + 1.5` → 4.2 (no 3.12: diez décimas hacen un entero).   `4.2 - 1.5` → 2.7 (cambiar un entero por
  diez décimas).   `0.9 + 0.1` → 1.
- `comparar: 0.9 y 1.1` → 1.1 (no «9 es más que 1»).   `redondear: 2.5` → 3 (mitad: convenio).
- `de 0.1 en 0.1 desde 0.8` → 0.9, 1, 1.1 … (no «0.10»).
- `2.35 + 1` → todavía no (centésimas, D.2).

**Prueba de dominio.** Sumas y restas de números con décimas (muestra) contra el testigo, por las dos
maneras; comparar y redondear en muestras; contar de décima en décima.

**Para Carlos:** `decimal: 2.3`, `2.7 + 1.5`, `4.2 - 1.5`, `de 0.1 en 0.1 desde 0.7`, `comparar: 0.9 y 1.1`.

## 2. LO QUE SE HIZO
- Parte nueva `sistema/partes/decimales.py` (preparada para D.2: el número de cifras detrás del punto
  es un parámetro):
  - `decimal: 2.3` (las cifras en su sitio; 23 décimas; 2 + 0.3 = 2 + 3/10; en la recta).
  - `2.7 + 1.5`, `4.2 - 1.5`, `2 + 0.5`: **en columnas con el punto alineado** (llevando «diez décimas
    hacen una unidad», o **cambiando** una unidad por diez décimas), y **contando en décimas** con las
    piezas de siempre (27 + 15 = 42 décimas).
  - `comparar: 0.9 y 1.1` (los enteros; luego la primera cifra distinta detrás del punto).
  - `redondear: 2.7` (la cifra de las décimas; la mitad, por convenio).
  - `de 0.1 en 0.1 desde 0.7 [hasta …]` (pasa el uno: 0.9, 1, 1.1).
  - `fraccion: 3/10` dice además «= 0.3».
- `pruebas/test_D1_decimas.py` (16 afirmaciones; 300 sumas/restas, 300 comparaciones y los redondeos de
  una muestra, contra un testigo que cuenta en décimas enteras, sin coma flotante). Ayuda,
  `mis_pruebas.txt` (5), `mis_casos.txt` (7).

## 3. RESULTADO
- `2.7 + 1.5` → 4.2 («décimas: 7 + 5 = 12 → escribo 2, llevo 1 (diez décimas hacen una unidad)»).
- `4.2 - 1.5` → 2.7 («cambio 1 de las unidades por diez décimas (allí quedan 3)»).
- Proyecto: **2094/2094 afirmaciones + 600/600 casos — VERDE** (99 s).

## 4. PENDIENTE: la prueba de Carlos.  Sigue D.2: centésimas y milésimas (NCETM 1.24).
