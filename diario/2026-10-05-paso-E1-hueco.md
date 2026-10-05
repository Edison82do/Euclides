# Paso E.1 — ECUACIONES CON HUECO — 5 oct 2026

Carlos probó E.0 con su `.bat` («ya probé») → se empieza E.1.

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (mirando antes `FUENTES.md`).**
- Common Core **1.OA.D.8**: «determinar el número desconocido que hace verdadera una ecuación de
  suma o resta con tres números»: `8 + ? = 11`, `5 = _ − 3`, `6 + 6 = _`.
- **Progression CC & OA**: en 1.º el desconocido aparece **en todas las posiciones** (resultado,
  cambio y comienzo desconocidos), y `5 = 2 + 3` enseña que el `=` es «es el mismo número que».
- **CGI (Carpenter, Fennema, Franke)**: cada posición del hueco ES un tipo de problema. `8 + ? = 11`
  es «juntar con el cambio desconocido»; `? + 3 = 11` es «juntar con el comienzo desconocido». La
  ecuación es **la misma situación escrita en símbolos** — Euclides ya sabe resolver las 11 (R.1).
- **Clements & Sarama**: el comienzo desconocido (`? + 6 = 11`) es lo más difícil; primero sale
  por tanteo, luego contando (*Numbers-in-Numbers*). Aquí sale **deshaciendo** (la vuelta).
- **NCETM 1.31** (Year 6): *Problems with two unknowns* → `? + ? = 10` no es de este paso: se dice.
- **Pólya**: comprobar la solución. Aquí se comprueba **con lo de E.0**: se pone el número en el
  hueco y se pregunta si la igualdad es verdadera.

**Lo que se construye.**
- Una parte nueva, `sistema/partes/ecuaciones.py`, que solo **LEE** la ecuación y la traduce a la
  situación de un problema (la misma que usa el resolvedor), y la historia en lenguaje rústico:
  | ecuación | situación (CGI) | pieza que la resuelve |
  |---|---|---|
  | `8 + 3 = ?` | juntar, resultado desconocido | añadir |
  | `8 + ? = 11` | juntar, cambio desconocido | lo que llegó (contar de 8 a 11) |
  | `? + 3 = 11` | juntar, comienzo desconocido | deshacer lo que llegó (11 − 3) |
  | `11 − 3 = ?` | separar, resultado desconocido | quitar |
  | `11 − ? = 8` | separar, cambio desconocido | lo que se fue (contar de 8 a 11) |
  | `? − 3 = 8` | separar, comienzo desconocido | deshacer lo que se fue (8 + 3) |
  con el `=` a la derecha o a la izquierda (`11 = 8 + ?`).
- Las **piezas de pasos** que ya existen la resuelven (no se programa ningún conocimiento nuevo:
  es la prueba de que la ecuación es la situación en símbolos).
- **La comprobación**: se pone el número en el hueco y se pregunta a la igualdad (E.0).
- Orden `ecuacion: 8 + ? = 11` (y `hueco:`). **Y escrita directamente** (`8 + ? = 11`), como pidió
  Carlos para los problemas que vendrán: «la ecuación directamente y algunas palabras».

**Las trampas.**
- `8 + ? = 5` → **imposible** (si llega algo, no puede haber menos).   `? − 9 = 3` → 12.
- `5 = ? − 3` (el del estándar, hueco a la derecha del `=`) → 8.
- `? + ? = 10` → dos huecos: hay muchas respuestas (eso es de más adelante, NCETM 1.31).
- `8 + 4 = ? + 5` → hueco con cuentas a los dos lados: **la balanza, E.2** (todavía no).
- `8 + 3 = 11` sin hueco → se dice que no hay hueco (para eso está `verdad:`).
- Huecos escritos `?`, `_`, `__` o `□`.

**Prueba de dominio.** Las seis posiciones × los dos lados del `=`, en una muestra contra el
testigo; cada una por la pieza que le toca; la comprobación por E.0 siempre verdadera; las trampas.

**Para Carlos (su `.bat`):** `8 + ? = 11`, `? + 3 = 11`, `5 = ? - 3`, `11 - ? = 8`, `8 + ? = 5`,
`? + ? = 10`, escritas directamente (sin orden delante).

## 2. LO QUE SE HIZO
- Parte nueva `sistema/partes/ecuaciones.py`: LEE la ecuacion (con palabras alrededor, huecos ? _ __ y
  el cuadradito, el = a cualquier lado), la cuenta como una HISTORIA y la traduce a la situacion de un
  problema. **No se programo ningun conocimiento nuevo**: la resuelven las piezas de pasos de R.1
  (anadir, lo que llego, deshacer lo que llego, quitar, lo que se fue, deshacer lo que se fue).
- La comprobacion: el numero en el hueco y se pregunta a la igualdad (E.0).
- Orden `ecuacion:` / `hueco:`, y **escrita directamente**. De paso, lo escrito sin orden se reparte:
  ecuacion con hueco -> ecuacion; `8 + 3 = 11` -> verdad; `8 + 3` -> calcular (antes `8 + 3` caia en
  la 0.1 y contestaba «un_objeto»: una puerta que mentia, cerrada).
- `pruebas/test_E1_hueco.py` (22 afirmaciones; la muestra resuelve 1440 ecuaciones: las 6 posiciones
  x los dos lados del =). Ayuda, `mis_pruebas.txt` (8) y `mis_casos.txt` (10).

## 3. RESULTADO
- `8 + ? = 11` -> «juntar con el CAMBIO desconocido: tenia 8, le dan algunos, ahora tiene 11» ->
  cuantos llegaron (de 8 a 11) -> 3 -> compruebo: 8 + 3 = 11 VERDADERO.
- `? + 3 = 11` -> comienzo desconocido -> deshacer (11 - 3) -> 8.  `5 = ? - 3` -> 8.
- Trampas: `8 + ? = 5` imposible; `? + ? = 10` dos huecos; `8 + 4 = ? + 5` -> la balanza (E.2).
- Proyecto: **1629/1629 afirmaciones + 414/414 casos — VERDE**.

## 4. OBSERVACION PARA MAS ADELANTE
- `47 + ? = 77` sale bien (30) pero CONTANDO 30 pasos de uno en uno. Un nino saltaria de diez en diez
  (57, 67, 77). Es una pieza de «contar hasta» de diez en diez: se propone cuando toque (NCETM 1.14).

## 5. PENDIENTE: la prueba de Carlos
No se empieza E.2 (la balanza) hasta que Carlos lo pruebe con su `.bat`.
