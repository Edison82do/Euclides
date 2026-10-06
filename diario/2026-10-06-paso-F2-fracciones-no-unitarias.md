# Paso F.2 — FRACCIONES NO UNITARIAS; EN LA RECTA; COMPARAR — 6 oct 2026 (noche)

Sigue al F.1 (hecho; Carlos lo prueba mañana). Trabajo sin parar, en orden, como pidió Carlos.

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (`FUENTES.md`: NCETM 3.3; Common Core 3.NF.A.2, A.3c, A.3d).**
- NCETM **3.3**: «todas las fracciones no unitarias están hechas de **varias fracciones unitarias
  iguales**»; «se escriben igual; el numerador es mayor que uno»; «cuando numerador y denominador son
  iguales, la fracción es **un entero**»; «las fracciones son **números** que se pueden poner en la
  **recta numérica**»; «sumar una y otra vez una fracción unitaria da una no unitaria»; comparar:
  **mismo denominador → manda el numerador**; **mismo numerador → manda el denominador, al revés**.
- Common Core **3.NF.A.2** (la fracción en la recta: de 0 a 1 partido en b trozos; a/b está a «a
  trozos» del 0); **3.NF.A.3c** (los enteros como fracciones: 3 = 3/1; 4/4 = 1); **3.NF.A.3d**
  (comparar con el mismo numerador o el mismo denominador, y decir por qué).
- Lo que NO es de 3.º en NCETM: fracciones mayores que un entero (5/4, NCETM 3.5, 4.º) y comparar con
  numeradores y denominadores distintos (fracciones equivalentes y denominador común, NCETM 3.7–3.8,
  5.º). Se dice «todavía no».

**Lo que se construye** (en `fracciones.py`, que F.1 dejó preparado).
1. `fraccion: 3/4` → «tres cuartos» = 1/4 + 1/4 + 1/4; la tira con 3 partes tomadas; `4/4` → un entero;
   `3/1` → 3 enteros; `0/4` → cero.
2. `recta: 3/4` → la recta de 0 a 1 partida en 4 trozos y la marca a 3 trozos del 0.
3. `3/4 de 12` → repartir 12 en 4 (3 cada parte) y tomar 3 partes: 3 x 3 = 9. `entero: 3/4 es 9` → una
   parte es 9 : 3 = 3, el entero 3 + 3 + 3 + 3 = 12.
4. Comparar: dos piezas nuevas en `comparar_fracciones`: `fracciones_mismo_denominador` y
   `fracciones_mismo_numerador`; la tira (F.1) se amplía a no unitarias. Las que encajan, todas, y
   tienen que coincidir.

**Las trampas.**
- `comparar: 2/5 y 3/5` → 3/5 mayor.   `comparar: 2/3 y 2/5` → 2/3 mayor (el error: «5 es más»).
- `comparar: 2/3 y 3/5` → todavía no (numerador y denominador distintos: 5.º).
- `fraccion: 4/4` → un entero.   `fraccion: 5/4` → todavía no (4.º).   `fraccion: 0/4` → cero.
- `3/4 de 12` → 9.   `2/3 de 10` → no sale justo.   `entero: 3/4 es 9` → 12;  `entero: 3/4 es 10` → no sale.
- `recta: 3/4` → la marca a tres trozos; `recta: 4/4` → en el 1.

**Prueba de dominio.** Todas las parejas a/b con b de 2 a 12 y a ≤ b que compartan numerador o
denominador, contra el testigo (las piezas que encajan, de acuerdo); a/b de n en una muestra; el
entero desde una parte no unitaria; la recta.

**Para Carlos:** `fraccion: 3/4`, `recta: 3/4`, `3/4 de 12`, `comparar: 2/3 y 2/5`, `comparar: 2/5 y 3/5`.

## 2. LO QUE SE HIZO
- `fracciones.py` se abre a las no unitarias **hasta un entero** (a ≤ b; más de un entero, 4.º → «todavía
  no»): `fraccion: 3/4` (= 1/4 + 1/4 + 1/4; `4/4` un entero; `3/1` tres enteros; `0/4` cero);
  `3/4 de 12` (repartir y tomar 3 partes); `entero: 3/4 es 9` (una parte = 9 : 3, y luego sumar).
- Orden nueva `recta: 3/4`: la recta de 0 a 1 dibujada en trozos iguales y la marca.
- Comparar: piezas nuevas `fracciones_mismo_denominador` y `fracciones_mismo_numerador`; la tira se
  amplía a no unitarias. Sin nada en común (2/3 y 3/5): «todavía no» (equivalentes, NCETM 3.7, 5.º).
- `pruebas/test_F2_fracciones_no_unitarias.py` (16 afirmaciones; todas las parejas con b ≤ 12 que
  comparten arriba o abajo contra el testigo, y las que no comparten nada: no se atreve). Ayuda,
  `mis_pruebas.txt` (5), `mis_casos.txt` (8).

## 3. RESULTADO
- `comparar: 2/3 y 2/5` → 2/3 > 2/5 (la tira de 15: 10 contra 6; y «mismo de arriba, al revés»).
- `3/4 de 12` → 9.  `recta: 3/4` → dibujada.  `fraccion: 4/4` → un entero.
- Proyecto: **1956/1956 afirmaciones + 550/550 casos — VERDE**.

## 4. PENDIENTE: la prueba de Carlos (mañana).  Sigue F.3: sumar y restar dentro de un entero (NCETM 3.4).
