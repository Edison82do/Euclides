# Paso E.0 — EL `=`: ¿VERDADERO O FALSO? — 5 oct 2026

Carlos probó P.6 con su `.bat` («todo bien») → se empieza E.0.

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (mirando antes `FUENTES.md`).**
- Common Core **1.OA.D.7**: «entender el significado del signo igual y decidir si las ecuaciones de
  suma y resta son **verdaderas o falsas**»: `6 = 6`, `7 = 8 − 1`, `5 + 2 = 2 + 5`, `4 + 1 = 5 + 2`.
- **Progression CC & OA**: el `=` «no siempre significa "da" o "resulta", pero **siempre** significa
  **"es el mismo número que"**». Por eso `5 = 2 + 3` se escribe también así.
- **NCETM 1.5**: el `=` nace como **equivalencia** entre el todo y la suma de las partes.
- **Carpenter, Franke & Levi** (*Thinking Mathematically*, 2003): se empieza por frases
  **verdadero/falso** antes que por frases con hueco, para que el `=` sea una relación.
- **Knuth et al.** (2006, 2008): la mayoría de los alumnos lee el `=` como «pon el resultado»; los
  que lo leen como equivalencia resuelven mucho mejor las ecuaciones. Proponen discutir las
  **cadenas** que escriben los niños: `3 + 5 = 8 + 2 = 10` es **falsa** (3 + 5 no es 10).
- **Pensamiento relacional** (Carpenter et al.; Stephens; Kızıltoprak y Yavuzsoy Köse 2017): tres
  niveles — (1) calcular los dos lados, (2) calcular y luego ver la relación, (3) **ver la relación
  sin calcular**. Aquí: el nivel 1 siempre, y el 3 cuando hay una razón que ya se sabe (los dos
  lados escritos igual; **dar la vuelta**, P.5). La compensación sin calcular (57 + 22 = 58 + 21)
  se deja para E.2 (la balanza).

**Lo que se construye.**
- Una pregunta nueva de las piezas: **«igualdad»** (¿los lados valen lo mismo?), con el más corto
  que encaja.
- Piezas: `igual_escrito_igual` (los lados están escritos igual: verdadero sin calcular),
  `igual_dando_la_vuelta` (5 + 2 = 2 + 5: los mismos números al revés, P.5: verdadero sin calcular),
  `igual_calculando_los_lados` (calcula cada lado con los métodos que ya tiene y mira si es el mismo
  número de la lista).
- Orden nueva: `verdad: 4 + 1 = 5 + 2`  (también `verdadero o falso: ...`). Sirve con varios `=`.

**Las trampas.**
- `4 + 1 = 5 + 2` → **FALSO** (a la izquierda 5, a la derecha 7). La trampa es pensar «4 + 1 da 5,
  y ahí está el 5». Hay que decirlo.
- `10 = 8 + 2` → **VERDADERO** (el resultado puede ir a la izquierda).
- `7 = 7` → **VERDADERO** (sin ninguna operación).   `7 = 8 − 1` → **VERDADERO**.
- `5 + 2 = 2 + 5` → **VERDADERO sin calcular** (dar la vuelta).
- `3 + 5 = 8 + 2 = 10` → **FALSO** (la cadena: 8 no es 10).
- `8 + 4 = 12 + 5` → **FALSO** (el error de escribir «lo que da» y seguir).
- `3 − 5 = 2` → no se puede decir: 3 − 5 no se puede hacer (no hay restas negativas).

**Prueba de dominio.** Muestra de igualdades verdaderas y falsas contra el testigo; las trampas;
todo verde.

**Para Carlos (su `.bat`):** `verdad: 4 + 1 = 5 + 2`, `verdad: 10 = 8 + 2`, `verdad: 7 = 7`,
`verdad: 5 + 2 = 2 + 5`, `verdad: 3 + 5 = 8 + 2 = 10`.

## 2. LO QUE SE HIZO
- Una pregunta nueva de las piezas, **«igualdad»** (`_objetivos.py`), y tres piezas:
  `igual_escrito_igual` (rapidez 1), `igual_dando_la_vuelta` (2, usa lo de P.5 sin calcular) y
  `igual_calculando_los_lados` (20, usa «sumar» y «restar»). Condiciones nuevas: `hay_dos_lados_o_mas`,
  `todos_los_lados_estan_escritos_igual`, `son_los_mismos_numeros_al_reves`.
- Una parte nueva del motor, `sistema/partes/igualdad.py`: solo LEE la frase (lados con un numero o
  con una suma/resta, uno o varios `=`) y pregunta a las piezas.
- Orden `verdad: 4 + 1 = 5 + 2` (y `verdadero o falso: ...`).
- `pruebas/test_E0_igual.py` (17 afirmaciones; la muestra juzga 400 igualdades al azar, 165 verdaderas).
- Ayuda, `mis_pruebas.txt` (6 pruebas para Carlos) y `mis_casos.txt` (9 casos).

## 3. RESULTADO
- `4 + 1 = 5 + 2` -> FALSO, y dice la trampa: «4 + 1 da 5, y a la derecha se ve un 5; pero el =
  no dice da: a la derecha esta 5 + 2 entero, que vale 7».
- `5 + 2 = 2 + 5` y `7 = 7` -> VERDADERO **sin calcular** (pensamiento relacional).
- `3 + 5 = 8 + 2 = 10` -> FALSO (la cadena).  `3 - 5 = 2` -> no se puede decir.
- Proyecto: **1605/1605 afirmaciones + 404/404 casos — VERDE**.

## 4. PENDIENTE: la prueba de Carlos
No se empieza E.1 (ecuaciones con hueco) hasta que Carlos lo pruebe con su `.bat`.
