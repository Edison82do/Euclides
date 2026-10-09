# Arreglo A.1 — EL CERO AL DESPEJAR (prudencia: nunca una respuesta falsa) — 9 oct 2026

**No es un paso de NCETM: es un ARREGLO** de la regla de prudencia de Carlos (8 oct): *nunca una respuesta falsa*.
Lo encontró M.21 (`resolver: 0 : 5 = 0 : r` → «ninguna»). Se llama **A.1** (el primer arreglo con nombre propio).

**Las reglas de este arreglo** (Carlos, 9 oct): la causa se busca y se arregla en la CAPA GENERAL (cómo se despeja una
letra que divide y qué pasa al multiplicar o dividir por algo que puede ser 0), NUNCA con una receta para un caso; sin
puerta ni formato nuevo; sin calculadora; nada que ya funcionaba cambia su respuesta, salvo las falsas; si la respuesta
exacta («cualquier número menos el 0») no se puede dar todavía, «todavía no» o «no sale», pero nunca algo falso.

## 1. EL PLAN (escrito antes de programar)

### Lo que dice la matemática (y lo que haría un humano sin calculadora)
- **0 : algo = 0** siempre que *algo* no sea 0 (repartir nada entre varios: a cada uno nada). **Entre 0 no se reparte**
  (M.3): `algo : 0` no tiene respuesta, tampoco `0 : 0`.
- **0 x algo = 0** siempre (M.2): si tiene que dar 0, vale CUALQUIER número; si tiene que dar otro, NINGUNO.
- Por eso, al DESHACER una división `0 : r = N` no se puede «pasar r al otro lado» (r = 0 : N): con N = 0 cumple
  cualquier r menos el 0; con N distinto de 0 no cumple ninguno. Y al deshacer `0 x r = N` no se puede dividir entre 0.
- **«El mismo número a los dos lados, así que lo otro es igual»** (la equivalencia de NCETM 2.18, y M.21) solo vale si
  ese número NO es 0: `0 x r = 0 x 5` lo cumple cualquier r, no solo el 5; `0 : r = 0 : 5`, cualquier r menos el 0.
- **«Con la letra más grande nunca sale más pequeño»** (el TOPE de probar en orden, U.2) solo vale si lo que se
  multiplica no es menor que 0: `(r - 2) x (r - 2)` BAJA de r = 0 a r = 2 (4, 1, 0) y luego sube.
- Un humano, ante `0 : r = 0`, no despeja: MIRA que el de delante es 0 y piensa «0 entre lo que sea es 0, menos entre
  0». Es mirar la relación, no hacer la cuenta.

### Qué responde hoy (medido el 9 oct, memoria vacía; `resolver:` y sin orden)
| pregunta | hoy | lo correcto | ¿falsa? |
|---|---|---|---|
| `resolver: 0 : r = 0 : 5` | ninguna | cualquier r menos el 0 | **SÍ** |
| `resolver: 0 : 5 = 0 : r` | ninguna | cualquier r menos el 0 | **SÍ** |
| `resolver: 0 : r = 0` | ninguna | cualquier r menos el 0 | **SÍ** |
| `resolver: 0 : (r - 2) = 0` | ninguna | cualquier r menos el 2 | **SÍ** |
| `resolver: 0 : r + 3 = 3` | ninguna | cualquier r menos el 0 | **SÍ** |
| `resolver: a : b = 0; a = 0` | ninguna | a = 0 y b cualquiera menos el 0 | **SÍ** |
| `0 : r = 0 : 5` (sin orden, puerta E.5) | r = 5 | cualquier r menos el 0 (el 5 es solo uno) | **SÍ** |
| `0 x r = 0 x 5`, `r x 0 = 5 x 0` (E.5) | r = 5 | cualquier número | **SÍ** |
| `0 : r = 3` (E.5) | la explicación dice «RESULTADO: r = 0» (su comprobación dice NO; la respuesta corta es no_cuadra) | ninguna | **SÍ** (lo que se enseña) |
| `r : 0 = 5 : 0`, `0 : r = 0 : 0` (E.5) | la explicación dice «r = 5» / «r = 0» con la comprobación en NO | no se puede (entre 0) | **SÍ** (lo que se enseña) |
| `resolver: (r - 2) x (r - 2) = 1` | ninguna (paró en r = 0: «ya se pasa») | r = 1; r = 3 | **SÍ** |
| `resolver: (r - 2) x (r - 2) = 0` | ninguna | r = 2 | **SÍ** |
| `resolver: 0 : r = 3` | no_cuadra | ninguna (0 : algo es 0, o no se puede) | no (impreciso) |
| `resolver: 0 x r = 0` | cualquiera | cualquiera | no |
| `resolver: r : r = 1` | todavía no | cualquier r menos el 0 | no |
| `resolver: 5 : r = 0` | ninguna | ninguna | no |
| `resolver: r x 0 = 5` | ninguna | ninguna | no |
| `resolver: (r - 2) : (r - 2) = 1` | todavía no | cualquier r menos el 2 | no |

(Las de `(r - 2) x (r - 2)` y la puerta E.5 no estaban en la lista de Carlos: salieron al buscar la familia con un
TESTIGO —Python, solo en la búsqueda— que probó 800 relaciones de una letra con 0, x y : contra r = −12…40 y ½.)

### Las causas (en la capa general)
1. **`_u_deshacer` (universal.py)**, el caso `otro : der = objetivo`: si el objetivo es 0 dice «ninguna» sin mirar si el
   de delante (`otro`) es 0 — su propio mensaje dice «salvo que el de delante sea 0», pero no lo mira. Y con el de
   delante 0 y el objetivo no 0 calcula `der = 0 : N = 0` y luego no cuadra.
2. **`letra._deshacer` (la puerta vieja E.5)**: el mismo despeje sin mirar el 0 (divide entre 0 y dice «0 : 0 no se
   puede», que es verdad pero no es el porqué).
3. **La pieza `balanza_escalando` (M.12, NCETM 2.18)**: «n es el mismo que n, así que el hueco es el mismo que el otro»
   sin mirar que n sea 0.
4. **`explicar_ecuacion_letra`**: si la comprobación dice NO, igual escribe «RESULTADO: r = v».
5. **El TOPE de probar en orden (`_bu_ya_me_paso`, buscar.py)**: da por hecho que lo que se multiplica crece con la
   letra, y `(r - 2)` es negativo (o 0) antes de r = 2.

### Lo que se construye (sin puerta ni formato nuevo; sin pieza nueva)
1. **`_u_deshacer`**: en `otro : der = objetivo`, MIRAR primero si `otro` es 0 (con `_nu_es_cero`, el mecanismo):
   - objetivo 0 → «todavía no»: *0 : algo da 0 con cualquier algo que no sea 0: r puede valer CUALQUIER número menos
     el que hace 0 a lo de detrás (infinitas)*; ese número se busca DESHACIENDO `der = 0` (si sale; si no, se dice en
     general). Es la misma forma que ya tenía `0 x algo = 0` (`_u_por_cero`: «todavía no», cualquier número).
   - objetivo no 0 → «ninguna»: *0 : algo es 0 (o no se puede, entre 0), nunca N*.
2. **`letra._deshacer`**: las mismas dos reglas del 0 (y las de `0 x algo`), con su porqué; la de «cualquiera» dice
   «todavía no» y la de «ninguno», «no sale». (La red de U.4 deja decidir al resolvedor como siempre.)
3. **`balanza_escalando`**: «el mismo número» solo si no es 0 (si es 0, no hay equivalencia: no encaja y se deshace).
4. **`explicar_ecuacion_letra`**: con la comprobación en NO, «NO CUADRA … RESULTADO: no_cuadra» (la misma respuesta
   corta que ya daba).
5. **El tope**: solo se PARA («ya me paso, con más me pasaría más») si, en ese punto, todo lo que se multiplica es 0 o
   más (se calcula con el mecanismo); si algo que se multiplica es negativo, se sigue probando (dentro del tope humano
   de pruebas). Así `r x (r - 2) = 0` sigue saliendo 0 y 2, y `(r - 2) x (r - 2) = 1` sale 1 y 3.

### Las trampas
- Arreglar SOLO `0 : r = 0 : 5` (receta) y dejar `0 : (r - 2) = 0` o `0 : 5 = 0 : r` mal → las pruebas usan formas
  distintas.
- Pasarse al otro lado: decir «cualquiera» en `0 : r = 0` (el 0 NO vale: 0 : 0 no se puede).
- `0 : (r x 0) = 0`: lo de detrás es SIEMPRE 0 → ninguno cumple; no se puede decir «cualquiera menos…».
- Que cambie una respuesta buena: `5 : r = 0` (ninguna), `6 : r = 2` (3), `r x (r - 2) = 0` (0 y 2), `0 x r = 0`
  (cualquiera), `a x b = 0; a + b = 3`, las proporciones de M.21.

### La prueba (`pruebas/test_A1_el_cero.py`, pocas y representativas)
Las falsas de la tabla ya no lo son (por `resolver:` y sin orden); las que estaban bien siguen igual; el TESTIGO
(Python, solo en la prueba) sobre una muestra de relaciones con 0, x y : comprueba que NINGUNA respuesta es falsa
(«ninguna» sin soluciones, «cualquiera» para todas, los valores cumplen y no falta ninguno con números para contar);
la batería entera en verde.

## RESULTADO (9 oct 2026)

**Hecho. `test_A1_el_cero` 40/40 (con el código de antes, 21/40: caza las falsas); proyecto en cuartos 3614/3615
afirmaciones + 909/909 casos; mis_pruebas 287/287; `test_sin_calculadora` 2/2; `comparar_puertas` 0 diferencias sin
explicar.** La única falla es la prueba de TIEMPO de F7 (`999 1/2 + 999 1/3` < 2 s, salió 2,35 s): es la lentitud conocida
de la nube (CLAUDE.md); con el código de antes da lo mismo (2,02 s, también falla), y esa pregunta no pasa por nada de lo
tocado. Falta la prueba de Carlos.

**Lo que se arregló** (todo en la capa general; ninguna puerta, formato ni pieza nueva):
1. `universal.py`, `_u_deshacer` + `_u_cero_entre`: `0 : algo = 0` → «todavía no: CUALQUIER número menos el que hace 0
   a lo de detrás» (el que no vale se busca DESHACIENDO `algo = 0`: «menos el 2» en `0 : (r - 2) = 0`); si lo de
   detrás es 0 siempre (`0 : (r x 0)`), «ninguna»; `0 : algo = N` con N no 0 → «ninguna».
2. `universal.py`, `_u_aislar` + `_u_puede_ser_cero`: al SUSTITUIR no se aísla una letra pasando a dividir entre algo
   que puede ser 0 cuando lo de delante también puede serlo (haría 0 : 0 y perdería soluciones); se busca otro camino.
3. `letra.py` (la puerta vieja E.5), `_le_cero`: las mismas reglas del 0 al deshacer (`0 x algo`, `0 : algo`,
   `algo : 0`), con su porqué; y la explicación con la comprobación en NO ya no escribe «RESULTADO: r = v».
4. `balanza_escalando.py` (M.12): «el mismo número a los dos lados» solo si no es 0.
5. `buscar.py`, el TOPE de probar en orden (`_bu_por_sin_negativos`): solo se para si todo lo que se multiplica es 0
   o más en ese punto; la frase del tope lo dice cuando hay una resta dentro de un producto.

### Qué responde ahora (la tabla del plan)
| pregunta | antes | ahora |
|---|---|---|
| `resolver: 0 : r = 0 : 5`, `0 : 5 = 0 : r`, `0 : r = 0`, `0 : r + 3 = 3` | ninguna (FALSA) | todavía no: cualquier número menos el 0 |
| `resolver: 0 : (r - 2) = 0` | ninguna (FALSA) | todavía no: cualquier número menos el 2 |
| `resolver: a : b = 0; a = 0` | ninguna (FALSA) | todavía no: b cualquier número menos el 0 |
| `0 : r = 0 : 5` (sin orden) | r = 5 (FALSA: no es el único) | todavía no |
| `0 x r = 0 x 5`, `r x 0 = 5 x 0` (sin orden) | r = 5 (FALSA) | cualquiera |
| `0 : r = 3` (sin orden) | la explicación decía «r = 0» | ninguna |
| `r : 0 = 5 : 0`, `0 : r = 0 : 0` (sin orden) | la explicación decía «r = 5» / «r = 0» | no sale (5 : 0, 0 : 0 no se pueden) |
| `resolver: (r - 2) x (r - 2) = 1` | ninguna (FALSA) | r = 1; r = 3 |
| `resolver: (r - 2) x (r - 2) = 0` | ninguna (FALSA) | r = 2 |
| `resolver: 0 : (a - b) = 0; a + b = 3` | ninguna (FALSA) | las 4 parejas (3,0) (2,1) (1,2) (0,3) |
| `resolver: 0 : r = 3` | no_cuadra | ninguna (la exacta) |
| `resolver: 2 : 5 = 0 : r` (estaba en `test_M21`) | no_cuadra | ninguna (la exacta) |
| `resolver: 0 x r = 0` | cualquiera | cualquiera (igual) |
| `resolver: r : r = 1` | todavía no | todavía no (igual; lo exacto: cualquier número menos el 0) |
| `resolver: 5 : r = 0` | ninguna | ninguna (igual) |
| `resolver: r x 0 = 5` | ninguna | ninguna (igual) |
| `resolver: (r - 2) : (r - 2) = 1` | todavía no | todavía no (igual; lo exacto: cualquier número menos el 2) |

**Lo que cambia sin ser falso antes:** `0 : r = 3` y `2 : 5 = 0 : r` pasan de «no cuadra» (un número que no se
comprobó) a «ninguna» (la respuesta exacta: 0 : algo es 0 o no se puede). Se actualizaron las dos afirmaciones de
`test_M21` que guardaban `0 : 5 = 0 : r` → ninguna (la falsa) y `2 : 5 = 0 : r` → no_cuadra.

**La búsqueda de la familia con el TESTIGO** (Python, solo fuera del motor): 800 relaciones de una letra hechas con 0,
`r`, `(r - 2)`, `(r + 1)`, `r x 0`, x y : → antes 28 respuestas que el testigo contradecía, ahora ninguna con números para
contar (por `resolver:` y sin orden); 224 con dos letras → antes 2, ahora 0. La prueba guarda una muestra (156 + 6).

**Lo que queda (honesto, no falso; preguntas para Carlos):**
- «Cualquier número menos el 0» todavía no se puede DAR como respuesta (no hay esa forma de respuesta; abrirla sería un
  formato nuevo): se dice «todavía no» y el porqué lo explica entero. ¿Se abre una respuesta «cualquiera menos …»?
- `r : r = 1` y `(r - 2) : (r - 2) = 1` siguen «todavía no» (la letra que se divide por sí misma no se simplifica: sería
  simplificar sabiendo que no es 0).
- Probar en orden busca solo NÚMEROS PARA CONTAR (desde el 0), y lo dice: `(r + 1) x (r + 1) = 0` → «ninguna (con
  números para contar)», aunque r = −1 cumple; `r x r = 1` → solo r = 1. Es la decisión de U.2, no de esta familia; la
  respuesta corta solo dice «ninguna» / «r = 1». ¿Se deja así hasta los negativos en ecuaciones (NCETM más adelante)?
