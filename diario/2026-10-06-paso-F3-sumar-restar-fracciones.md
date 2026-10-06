# Paso F.3 — SUMAR Y RESTAR FRACCIONES DENTRO DE UN ENTERO — 6 oct 2026 (noche)

Sigue al F.2. Con este paso se cierra lo de **3.º** en NCETM (Spine 3, Year 3).

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (`FUENTES.md`: NCETM 3.4).**
- «Al **sumar** fracciones con el mismo denominador, **solo se suman los numeradores**.»
- «Al **restar** fracciones con el mismo denominador, solo se restan los numeradores.»
- «Sumar y restar fracciones son **inversas** una de la otra, igual que con los enteros.»
- «Para **restar de un entero**, primero se escribe el entero como una fracción con el numerador y el
  denominador iguales» (1 = 8/8).
- Por qué funciona (NCETM 3.3 y la idea de *unitising* de 2.1/6.2): 1/7 es una **unidad**, como una
  manzana: 2 séptimos + 3 séptimos = 5 séptimos, igual que 2 manzanas + 3 manzanas = 5 manzanas. El
  denominador **no se suma**: dice de qué tamaño son las partes, y no cambia (el error típico:
  2/7 + 3/7 = 5/14).

**Lo que se construye** (en `fracciones.py`).
- `2/7 + 3/7` → los numeradores con la pregunta `sumar`; el denominador se queda; la tira con las dos
  partes; la comprobación por la vuelta (5/7 − 3/7 = 2/7).
- `5/7 - 2/7` → igual con `restar`; la vuelta sumando.
- `1 - 3/8` → el entero se escribe 8/8; 8/8 − 3/8 = 5/8.
- Si llega a un entero, lo dice (3/8 + 5/8 = 8/8 = 1).

**Las trampas.**
- `2/7 + 3/7` → 5/7 (y NO 5/14: el denominador no se suma; se dice por qué).
- `5/7 - 2/7` → 3/7.   `1 - 3/8` → 5/8.   `3/8 + 5/8` → 1.   `3/8 - 3/8` → 0.
- `4/7 + 5/7` → todavía no (pasa de un entero: 4.º).   `2/7 - 5/7` → imposible.
- `1/2 + 1/4` → todavía no (denominadores distintos: NCETM 3.8, 5.º).

**Prueba de dominio.** Todas las sumas y restas a/b ± c/b con b de 2 a 12 dentro del entero, contra el
testigo, con su vuelta; `1 - a/b` para todos; las que se salen, «todavía no» o «imposible».

**Para Carlos:** `2/7 + 3/7`, `5/7 - 2/7`, `1 - 3/8`, `3/8 + 5/8`.

## 2. LO QUE SE HIZO
- `fracciones.py`: la cuenta `a/b ± c/b` y `1 - a/b`. Los de arriba con las preguntas `sumar` / `restar`
  (las piezas de siempre); el de abajo se queda y se dice por qué (y cuál sería el error típico: 5/14);
  la tira con las partes que se añaden (+) o se quitan (x); **la vuelta** con la operación inversa;
  `1` se escribe b/b; si llega a b/b, es un entero.
- Lo que no es de 3.º: pasar de un entero (4.º) o distinto de abajo (5.º) → «todavía no»; quitar más de
  lo que hay → imposible.
- `pruebas/test_F3_sumar_restar_fracciones.py` (12 afirmaciones; **todas** las cuentas a/b ± c/b con b
  de 2 a 12 contra el testigo, con su vuelta; `1 - a/b` para todos). Ayuda, `mis_pruebas.txt` (4),
  `mis_casos.txt` (6).

## 3. RESULTADO
- `2/7 + 3/7` → 5/7 («dos séptimos más tres séptimos = cinco séptimos»; `[###|###|+++|+++|+++|ooo|ooo]`).
- `1 - 3/8` → 5/8.  `3/8 + 5/8` → 1.
- Proyecto: **1970/1970 afirmaciones + 556/556 casos — VERDE**.
- **Con F.3 queda completo lo de 3.º de NCETM** (Spines 1, 2 y 3 de Year 3).

## 4. PENDIENTE: la prueba de Carlos (mañana).  Sigue 4.º: N.3, el 1000 y los números de cuatro cifras (NCETM 1.22).
