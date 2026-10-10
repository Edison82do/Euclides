# Paso M.22 — COMBINAR LA DIVISIÓN CON LA SUMA Y LA RESTA (el orden de las operaciones) — 10 oct 2026

Siguiente paso del orden de NCETM en 6.º: el segmento **2.28** (Spine 2, Year 6). Se llama **M.22** porque sigue la serie
(M.16 combinar la x con la + y la − era 2.22; M.21 la tabla de razón, 2.27).

**REGLA desde el plan U (Carlos, 9 oct):** lo nuevo entra por el MODELO COMÚN (como PIEZA, o en el resolvedor que ya existe,
eligiéndose por su costo); **no se abre ninguna puerta ni formato nuevo**; las preguntas se escriben con números y
símbolos; se respeta el año.

**Las DEUDAS DE PRUDENCIA (CLAUDE.md, 10 oct):** este paso NO toca ninguno de sus temas (ecuaciones con productos,
multiplicar negativos, «cualquiera menos…»): no se tacha nada. Se miró la lista.

## 1. EL PLAN (escrito antes de programar)

**La fuente.** La web de NCETM sigue bloqueada desde la nube (`getaddrinfo ENOTFOUND ncetm.org.uk`, probado hoy con la
página del segmento; también la lección de Oak National Academy). El título y los puntos salen del **buscador** (el
índice de la página `primm-228-combining-division-with-addition-and-subtraction`). **Falta leer el segmento entero**
(diapositivas) cuando Carlos pueda abrirlo.

- **Título exacto:** *2.28 Combining division with addition and subtraction* (Year 6).
- **Lo que trabaja** (la introducción): combinar la división con la suma o la resta; **volver a los paréntesis** para
  cambiar el orden de las operaciones; **apoyarse en la distributiva**. Es el gemelo de 2.22 (M.16), con la división.
- **Sus dos puntos** (teaching points; parafraseados del índice):
  1. **El orden**: la división se puede combinar con la suma y la resta; **sin paréntesis, la división se hace ANTES**
     que la suma o la resta; **con paréntesis, primero lo de dentro**.
  2. **La distributiva**: al sumar o restar expresiones de dividir que tienen un **DIVISOR COMÚN**, se puede aplicar la
     propiedad distributiva (12 : 3 + 6 : 3 = (12 + 6) : 3).
- **Common Core**: 5.OA.A.1 (paréntesis en las expresiones), 6.EE.A.2c (el orden de las operaciones cuando no hay
  paréntesis), 6.EE.A.3 (expresiones equivalentes con la distributiva). Oak National Academy tiene la lección gemela de
  Year 6 «Combine division with addition and subtraction» (explicar en qué orden y escribirlo como igualdad).

**Cómo lo haría un humano de 6.º sin calculadora.**
- `20 - 12 : 4`: rodeo la división, 12 : 4 = 3; luego 20 − 3 = **17** (no 8 : 4 = 2, que sería ir de izquierda a derecha
  sin mirar). `(20 - 12) : 4`: primero el paréntesis, 8; 8 : 4 = **2**.
- `12 : 3 + 6 : 3`: los dos se dividen entre 3: son «12 tercios de algo» y «6 tercios»… mejor: tengo 12 cosas y 6 cosas
  repartidas entre 3 cada vez; es lo mismo que juntar primero las 18 y repartir UNA vez: 18 : 3 = **6**. Con la resta,
  igual: 50 : 5 − 15 : 5 = 35 : 5 = 7. Donde más se nota: `7 : 4 + 9 : 4` — ninguna de las dos sale justa, pero juntas son
  16 : 4 = **4**. Es la distributiva leída al revés, como el factor común de M.16 (una división en vez de dos).
- La media de M.20, `(3 + 5 + 7) : 3`, es dividir con un paréntesis: primero lo de dentro (o nivelar, M.20) → **5**.
- **Se comprueba** deshaciendo con la contraria: 6 x 3 = 18; 18 − 6 = 12 (el primero de arriba).

**Qué responde hoy** (medido el 10 oct, memoria vacía):
- La cuenta sola `12 : 3 + 1`, `(12 + 6) : 3`, `12 : 3 + 6 : 3`, `verdad: 12 : 3 + 1 = 5`, `(3 + 5 + 7) : 3` →
  **«todavía no: dividir dentro de una cuenta combinada es NCETM 2.28»** (el lector de la puerta vieja de M.16 se para en
  el `:`). Era lo que esperaba este paso.
- Por el resolvedor (`resolver: 12 : 3 + 1`) ya sale, en el orden de siempre (el lector simbólico de U.1 ya pone la x y la
  : antes que la + y la −). Pero `resolver: 7 : 4 + 9 : 4` hace las dos divisiones con fracciones (7/4 + 9/4 = 16/4 = 4):
  un humano de 6.º juntaría primero.

**Lo que se construye (sin puerta ni formato nuevo; por qué).**
1. **El orden (punto 1): ya lo sabe el MODELO COMÚN.** No se escribe otra calculadora del orden: cuando la puerta vieja de
   M.16 (que solo sabe la x con la + y la −) se encuentra un `:` dentro de una cuenta combinada, **le pasa la cuenta al
   resolvedor** (en la TABLA de puertas, como ya se hace con `ecuacion:` y `calcular:` cuando traen números que su lector
   no sabe: es encaminar, no una puerta nueva). Así salen la cuenta sola, `verdad:` y `combinar:` con división. En la
   explicación del resolvedor, cuando una división va detrás de una + o una − sin paréntesis, se enseña el **error típico**
   (de izquierda a derecha sin mirar), calculado con el mecanismo, como hacía M.16.
2. **La distributiva (punto 2): una PREGUNTA nueva de piezas, `divisor_comun`** (en `_objetivos.py`, «la más rápida»):
   `{"terminos": [["+", 12], ["+", 6]], "divisor": 3}` — divisiones de enteros con el MISMO divisor, sumadas o restadas.
   - **`juntar_sobre_el_divisor_comun`** (rapidez 5): junta lo de arriba (sumar y restar en el orden en que vienen) y
     divide UNA vez (la pregunta `dividir`: lo que toca y lo que sobra). **Vuelta**: cociente x divisor (+ lo que sobró)
     = lo juntado; y deshaciendo la suma/resta se vuelve al primero de arriba.
   - **`dividir_cada_una_y_juntar`** (rapidez 20; el orden de siempre): cada división por separado y luego juntar; solo si
     TODAS salen justas (con resto no se pueden juntar números para contar). **Vuelta**: cada cociente x divisor vuelve a
     su número de arriba, y deshaciendo la suma se vuelve al primer cociente.
   - **El costo**: una división en vez de varias → el motor coge la de juntar (5) cuando encaja; la otra queda como
     segundo camino (y para cuando juntar no encaja: lo de arriba bajaría de cero, `5 : 5 - 15 : 5`).
   - **El enganche en el resolvedor** (`universal.py`, `_u_valor`, prefijo `_u_`): una cadena de + y − cuyos términos
     son TODOS `entero : d` con el mismo d (no 0, enteros sin signo) pide `divisor_comun`. Lo que sale (cociente y resto)
     se pasa al número común, como la media. Si ninguna pieza encaja, como antes (el número no cambia).

**Las trampas** (los errores típicos):
- **De izquierda a derecha sin mirar**: 20 − 12 : 4 como (20 − 12) : 4 = 2. Se enseña y la prueba lo caza.
- **Juntar también los divisores**: 12 : 3 + 6 : 3 = 18 : 6 = 3 (MAL). La vuelta lo caza (3 x 3 = 9, no 18); pieza trucada.
- **Juntar con divisores distintos**: 12 : 3 + 12 : 4 ≠ 24 : 7 (la condición pide el MISMO divisor); ni con el mismo
  de arriba: 12 : 3 + 12 : 4 ≠ 12 : 7.
- **La división no es conmutativa**: 3 : 12 + 6 : 12 no es 12 : 3 + 12 : 6 (el divisor es el de detrás del `:`).
- Entre 0 no se reparte: `12 : 0 + 1` → no se puede (no «todavía no»). Cerca del techo, «todavía no» como siempre.
- Lo que no es de este año sigue igual: una resta que se baja de cero en la puerta de M.16 (`2 x 3 - 4 x 5`), etc.

**Lo que cambia a propósito** (esperaban este paso): `12 : 3 + 1` → 5 (M.16, U.2, U.4, mis_casos, mis_pruebas) y
`(3 + 5 + 7) : 3` → 5 (M.20). Las pruebas de U.2/U.4 que usaban `12 : 3 + 1` como ejemplo de «respetar el año» pasan a
usar otra cuenta que sigue sin ser del año (`2 x 3 - 4 x 5`, se baja de cero). Todo lo demás, igual (se mide antes y después
con una lista).

**Prueba de dominio** (`pruebas/test_M22_dividir_combinado.py`, pocas y representativas): el orden contra el testigo
(Python `Fraction`, SOLO en la prueba) en una muestra al azar fijo de cuentas con `:` y + / − (con y sin paréntesis); las
dos piezas contra el testigo con su vuelta; qué elige el control (juntar; cada una cuando juntar no encaja); las piezas
trucadas (juntar los divisores, de izquierda a derecha, la vuelta que miente); por las puertas (la cuenta sola, `verdad:`,
`combinar:`, la media); el error típico en la explicación; entre 0; cerca del techo (9 999 999); lo que no cambia; el tiempo
(cada una por debajo de 2 s).

**Para Carlos:** `20 - 12 : 4`, `(20 - 12) : 4`, `7 : 4 + 9 : 4`, `verdad: 12 : 3 + 6 : 3 = 18 : 6`, `(3 + 5 + 7) : 3`.

## RESULTADO (10 oct 2026)

**Hecho. `test_M22` 56/56; proyecto en cuartos 3673/3673 afirmaciones + 909/909 casos, VERDE (97 archivos; también la
prueba de tiempo de F7 esta vez); mis_pruebas 292/292 con las 5 nuevas (con la memoria de las tablas, como en el PC de Carlos); casos 917/917 con los 8 nuevos;
`test_sin_calculadora` 2/2; `comparar_puertas` 0 diferencias sin explicar.** Falta la prueba de Carlos.

**Lo que se construyó** (ninguna puerta ni formato nuevo):
- **El orden (punto 1), por el MODELO COMÚN.** En la tabla de puertas (`puertas.py`), la puerta `combinar` de M.16 lleva
  ahora `no_sabe=_co_lleva_division` (la misma idea que `para_contar`): si la cuenta combinada lleva una `:`, que su
  lector no sabe, la coge el resolvedor (`_pu_al_resolvedor_como`: la respuesta corta escrita como la de la puerta,
  verdadero/falso). El resolvedor ya ponía la x y la : antes que la + y la − (U.1). Valen la cuenta sola, `verdad:` y
  `combinar:`. La puerta de M.16 sigue con todo lo suyo (`3 + 4 x 5`, el factor común…).
- **El error típico** (`universal.py`, `_u_ojo_izquierda`): si una división va detrás de una + o una − sin paréntesis, la
  explicación enseña lo que saldría de izquierda a derecha sin mirar, calculado con el mecanismo: `20 - 12 : 4` →
  «(20 - 12) : 4, saldría 2: está MAL».
- **La distributiva (punto 2), PIEZAS.** Pregunta `divisor_comun` (`_objetivos.py`), condición
  `son_divisiones_con_el_mismo_divisor` (`_m22_mismo_divisor`, `_condiciones.py`) y dos piezas:
  `juntar_sobre_el_divisor_comun` (rapidez 5: juntar lo de arriba y dividir UNA vez; vuelta: cociente x divisor + lo que
  sobró, y deshacer las sumas y restas hasta el primero de arriba) y `dividir_cada_una_y_juntar` (rapidez 20: solo si todas
  salen justas; vuelta: cada cociente x divisor vuelve a su número, y deshacer las sumas de los cocientes). Enganche
  `_u_divisor_comun` en `_u_valor` (una cadena de + y − cuyos términos son todos `entero : d` con el mismo d); lo que sobra
  pasa al número común como en la media (`1 : 4 + 6 : 4` → 7/4).
- **El costo**: juntar (una división) cuando encaja; dividir cada una cuando juntar se pasaría del techo
  (`9999990 : 10 + 20 : 10` → 999999 + 2 = 1000001). Si lo de arriba se baja de cero (`5 : 5 - 15 : 5`), ninguna: como
  antes (−2, con la recta).

**Lo que cambió a propósito** (esperaban este paso): `12 : 3 + 1` → 5 (antes «todavía no», en `test_M16`, `test_U2`,
`test_U4`, `mis_casos` y `mis_pruebas`) y `(3 + 5 + 7) : 3` → 5 (`test_M20`, `mis_casos`). En U.2 y U.4, el ejemplo de
«una cuenta sin letras respeta el año» pasa a ser `2 x 3 - 4 x 5` (se baja de cero: sigue «todavía no»).
**Lo que no cambió:** 383 preguntas medidas antes y después (sumas y restas de divisiones por el resolvedor, con letras y
sin ellas, el 0, el techo, M.16, M.21, A.1): ni una respuesta distinta.

**Un arreglo que salió al probar.** `9999990 : 10 + 20 : 10` decía «no entendido»: el aviso del error típico comparaba
con un número que se salía de la lista. Ahora, si no se puede calcular o comparar, no se enseña el aviso (la respuesta no
depende de él).

**Las deudas de prudencia:** este paso no toca ninguno de sus temas; no se tacha nada.

**Lo que queda (honesto) y preguntas para Carlos:**
- Una división que no sale justa dentro de una cuenta sin letras da una fracción (`7 : 2 + 1` → 9/2), como ya hacía el
  resolvedor. ¿Vale así en 6.º, o debería decir «todavía no» (o el resto) hasta las fracciones como división (NCETM 3.x)?
- La distributiva al revés (partir lo de arriba: 96 : 4 = 80 : 4 + 16 : 4) no se construyó como pieza nueva: es lo que ya
  hace la división corta por dentro.
- La x y la : juntas van de izquierda a derecha (`12 : 3 x 2` → 8), como ya hacía el resolvedor (Common Core); NCETM 2.28
  no lo trabaja.
- La web de NCETM sigue bloqueada desde la nube: falta leer el segmento 2.28 entero (diapositivas).
