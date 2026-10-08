# Fase U.4 — UNA SOLA TABLA DE PUERTAS — 8 oct 2026

Cuarta fase del **plan U** (`diario/2026-10-08-PLAN-U-volverlo-universal.md`). Regla de oro: **prohibido memorizar
problemas o familias de problemas**; solo relaciones generales (datos), operadores generales y búsqueda con control.
Nada viejo cambia de respuesta; lo nuevo, con pocas pruebas representativas.

**DECISIÓN DE CARLOS (8 oct): «cuanto más se avanza en matemáticas, menos se habla».** El centro es el problema escrito
con NÚMEROS Y SÍMBOLOS. La parte hablada (U.3, U.3b) NO se sigue ampliando: se queda como está, salvo la REGLA DE
PRUDENCIA (punto 4 de abajo: nunca una respuesta falsa). La fase U.3c queda descartada.

## 0. EL DIAGNÓSTICO (probado el 8 oct antes de tocar nada)

| lo escrito | lo que decía | lo que pasa |
|---|---|---|
| `1/2 x n = 3`, `n + 1/2 = 3/4`, `n : 3 = 1/2` | **no_sale** | E.5 lee `1/2` como `1 : 2` (su lector propio) y se rinde; `resolver:` da 6, 1/4, 3/2 |
| `a + b = 9; a : b = 2` | 0.2 «no decidible» | el `:` lo coge la puerta de los OBJETOS (0.2 formar); `resolver:` da a = 6, b = 3 |
| `6/2 + n = 5` | `2` en una cadena, `n = 2` en la otra | las dos cadenas (`explicar_pregunta` / `preguntar`) NO dicen lo mismo |
| `listas`, `aprender: sumas` | `un_objeto` en `preguntar` | las dos cadenas tienen puertas distintas |
| `2 x (n + 3) = 2 x n + 6` | todavía no | una IDENTIDAD: vale cualquier número |
| `2 x (a + b) = 2 x a + 2 x b`, `(n + 1) x (n + 1) = n x n + 2 x n + 1` | todavía no | identidades (la distributiva) |
| `a + b = a + b + 1` | todavía no | una contradicción: ninguna |
| Tengo 50 pesos. Gasté la mitad. ¿Cuánto me queda? | **50 pesos** | «gasté» no es vocabulario; la frase se ignora: FALSO |
| Un camión lleva 12 cajas. Cada caja pesa 96 kilos. ¿Cuánto pesan las cajas? | **96 kilos** | «las cajas» se lee como «cada caja»; el 12 se queda sin usar: FALSO |
| Un camión lleva 12 cajas. Las cajas pesan 96 kilos. ¿Cuánto pesa cada caja? | **96 kilos** | igual: FALSO |

## 1. EL PLAN (escrito antes de programar)

**Lo que dicen las fuentes** (las del plan U, ya en `FUENTES.md`):
- **Mayer (1992)**: traducir → integrar en UN modelo → planear → ejecutar → comprobar. Si hay dos sitios que traducen
  lo mismo de dos maneras, hay dos verdades: el modelo tiene que ser uno y la entrada, una.
- **Schoenfeld (1979), el control**: saber cuándo una técnica NO sirve y pasar a otra en vez de rendirse. Una puerta
  vieja que dice «no sale» a algo que el resolvedor sabe hacer es falta de control, no falta de técnica.
- **NCETM 2.20–2.22 y Common Core 6.EE.A.3–4** (expresiones equivalentes: la distributiva, agrupar términos
  iguales): dos expresiones son la MISMA si, desarrolladas con la distributiva y agrupadas, quedan iguales; entonces la
  ecuación se cumple para cualquier número. **Common Core 8.EE.C.7a**: una ecuación lineal puede tener UNA solución,
  NINGUNA o INFINITAS; se ve transformándola hasta `x = a`, `a = a` o `a = b` (con a ≠ b).
- **METODO §2.4 y §8** (no se adivina): mejor «no entiendo» que una respuesta falsa. Con palabras: si un número del
  enunciado no se sabe dónde va, o una frase con un cambio no se entendió, el humano prudente pregunta.

**Cómo lo haría un humano sin calculadora.** Ve una ecuación con números y símbolos y la trata como UNA cosa, la escriba
con barra, con coma o con letras: no tiene un cajón distinto para cada forma. Si una manera vieja de mirarla no le da la
respuesta, prueba la general antes de decir «no sé». Si al desarrollar los dos lados quedan iguales (2 x (n + 3) es
2 x n + 6), dice «vale cualquier número»; si quedan iguales menos un número (n + 1 = n + 2), «ninguno». Con un problema
hablado, si le sobra un número y no sabe por qué sobra, o no entendió una frase que cambia algo, no contesta a ciegas.

**Lo que se construye.**
1. **UNA tabla de puertas** (parte nueva `sistema/partes/puertas.py`, prefijo `_pu_`, la última del orden): una lista
   `PUERTAS`, cada puerta con su nombre, cuándo encaja, cómo EXPLICA y cómo RESPONDE (la respuesta corta del probador).
   `explicar_pregunta` y `responder_pregunta` recorren LA MISMA tabla, en el mismo orden, y deciden con LA MISMA regla.
   `probar.preguntar` pasa a ser una llamada a `responder_pregunta`; desaparecen `_explicar_por_las_puertas` y
   `_preguntar_por_las_puertas` (las dos cadenas duplicadas). Las puertas que solo tenía una cadena (`listas`,
   `aprender`, `olvidar`) quedan en las dos.
2. **La regla de la red, una sola** (`_pu_decidir`): si lo escrito lo lee ENTERO el lector simbólico (es una expresión
   o una ecuación con números y símbolos):
   - las puertas de los OBJETOS (0.1, 0.2, 0.3) no lo pueden coger: no son objetos;
   - si la puerta vieja contesta algo que NO es una respuesta (no entiendo, todavía no, no sale, imposible, no se
     puede, ninguna pieza, no decidible, no cuadra...) decide el resolvedor universal: si llega a una respuesta
     comprobada (hecho, cualquiera, o ninguna porque se contradicen) contesta él; si no, se queda lo de la puerta;
   - una excepción, que es una regla vieja del método: el «todavía no» de una CUENTA SIN LETRAS es respetar el año
     (`12 : 3 + 1`, `2/3 x 3/4`): eso es una respuesta («aún no lo he aprendido»), no rendirse.
   - con palabras, la red de U.3 (igual que ahora, pero en un solo sitio).
3. **Las puertas viejas que equivalen al modelo, traductores**: E.5 (la letra) deja su lector propio (el que leía
   `1/2` como `1 : 2`): lee con el lector único (`_u_leer`) y reconoce SU forma en el modelo (una relación, una letra,
   números enteros); lo que no es de su forma (fracciones, decimales, negativos, varias letras) ya no entra por E.5,
   va al resolvedor. Sus respuestas, en lo que sí es suyo, iguales.
4. **Lo que dicen distinto, se ve**: una herramienta (`herramientas/comparar_puertas.py`) pasa todo lo simbólico de
   `mis_casos.txt` y `mis_pruebas.txt` por la puerta vieja Y por el resolvedor y enseña cada caso en que dan respuestas
   DISTINTAS (no solo escritas distinto: `4` y `x = 4` es lo mismo). Cada diferencia se arregla o se explica; la
   prueba de la fase la corre y exige que no haya ninguna sin explicar.
5. **IDENTIDADES y contradicciones** (en el resolvedor, antes de buscar): cada relación se DESARROLLA con la
   distributiva y se agrupan los términos iguales (un polinomio: cuántos trozos de `n`, de `n x n`, de `a x b`... y lo
   suelto), con las cuentas de siempre (`_u_cuenta`). Si los dos lados quedan iguales, la relación es verdad SIEMPRE: no
   dice nada (si todas son así, «cualquier número»: infinitas soluciones); si quedan iguales salvo lo suelto, se
   contradice: «ninguna». Si hay una letra dividiendo, no se desarrolla (una letra en la división puede no valer 0).
6. **LA REGLA DE PRUDENCIA CON PALABRAS** (lo único que se toca de la parte hablada; en `_pa_modelo`):
   - una frase que no se entiende y trae una CANTIDAD (un número, «la mitad», «el doble»...) o un cambio → «no entiendo»
     diciendo la frase (antes solo si traía un número o un verbo de cambio conocido);
   - un NÚMERO del enunciado que se queda fuera (su relación no está conectada con la pregunta) y que es de la MISMA cosa
     que algo de la pregunta (las 12 CAJAS del camión cuando se pregunta por las cajas) → «no entiendo: no sé qué hacer
     con el 12 de 'un camión lleva 12 cajas'». Si es de otra cosa (la edad en un problema de canicas), sobra de verdad;
   - la respuesta que mezcla cosas distintas ya era «no entiendo» (U.3b, `_pa_comprobar_cosas`).
7. **20 problemas simbólicos nuevos** inventados (ecuaciones con letras a los dos lados, sistemas de 2 y 3 incógnitas,
   fracciones, decimales y negativos mezclados, no lineales que salen probando, identidades y contradicciones): se pasan
   tal cual (sin `resolver:`) y se apunta cuántos salen bien.

**Las trampas.**
- Nada viejo cambia: lo que una puerta vieja contestaba con una RESPUESTA sigue igual (la batería vieja en verde). Solo
  cambia lo que era «no sale / no entiendo / todavía no» y el resolvedor resuelve y comprueba; cada cambio se apunta.
- `ecuacion: 3 x ? = 13` → `no_entero` sigue: es una respuesta (con números para contar no hay), del año del hueco.
- `12 : 3 + 1` sigue «todavía no» (el año).
- `8 : 0` sigue «no se puede» (el resolvedor tampoco puede: se queda lo de la puerta).
- `0 x n = 0` → cualquiera; `0 x n = 5` → ninguna; `n : n = 1` NO se desarrolla (letra dividiendo).
- `a + b = 10; 2 x (a + b) = 2 x a + 2 x b`: la segunda es una identidad (no dice nada) y quedan las 11 parejas.
- Con palabras, «Ana tiene 9 años. Luis tiene 6 canicas y Pedro 4. ¿Cuántas canicas tienen Luis y Pedro?» sigue saliendo
  (la edad es de otra cosa: sobra de verdad).

**Prueba de dominio** (`pruebas/test_U4_una_sola_tabla.py`, pocas y representativas): las dos cadenas dicen lo mismo en
una muestra de cada tipo de puerta (y en TODO `mis_casos.txt`); los casos del diagnóstico; la red con «no sale»; el año
respetado; identidades y contradicciones (lineales, con dos letras, no lineales); E.5 traductor; la prudencia con
palabras (los dos casos falsos → no entiendo; lo que sobra de verdad sigue); el comparador sin diferencias sin explicar.

**Para Carlos:** `1/2 x n = 3`, `a + b = 9; a : b = 2`, `2 x (n + 3) = 2 x n + 6`, `n + 1 = n + 2`, el del camión.

## RESULTADO (8 oct 2026)

**Hecho. `test_U4` 48/48; mis_pruebas 257/257; casos 863/863 (853 + 10 nuevos); proyecto 3329/3329 afirmaciones +
863/863 casos (en cuartos), VERDE.** Falta la prueba de Carlos.

**Lo que se construyó.**
- **Parte nueva `sistema/partes/puertas.py`** (prefijo `_pu_`, la última del orden): la tabla `PUERTAS` (las ~95 puertas
  de las dos cadenas, en el orden de siempre; cada una con cuándo encaja, cómo explica y cómo responde). `explicar_pregunta`
  y `responder_pregunta` la recorren las dos y deciden con UNA regla (`_pu_decidir`). `probar.preguntar` es ahora una
  línea (`motor.responder_pregunta`); se borraron `_explicar_por_las_puertas` (explicacion.py) y
  `_preguntar_por_las_puertas` (probar.py). `listas`, `aprender` y `olvidar`, que solo tenía una cadena, están en las dos.
- **La regla de la red, una sola**: lo que el lector simbólico lee entero no lo cogen las puertas de los OBJETOS; si una
  puerta contesta algo que no es una respuesta y es una relación con letras, decide el resolvedor (si llega a una
  respuesta comprobada). La regla mira también lo que va detrás de `ecuacion:`, `verdad:`, `calcular:` (pero la orden
  manda: `verdad: 4 + 1` sigue «no entiendo», porque no hay igualdad que decidir).
  **«Ningún número» con números para contar** (`no_sale`, `imposible`, `no_entero`, `ninguna`) es una respuesta del año
  si el resolvedor solo encuentra una fracción o un negativo: se queda (nada viejo cambia) y **la explicación enseña
  también lo del resolvedor** («3 x n = 13 → no_sale ... el resolvedor universal dice n = 13/3»); si el resolvedor
  encuentra un número para contar, o «cualquier número», o una contradicción, la puerta se equivocaba y decide él.
- **E.5, traductor al modelo** (`letra.py`): ya no tiene lector propio (`_tokens`, `_parse` fuera): lee con `_u_leer` y
  reconoce su forma (una relación, números para contar, sin «por» sin escribir). Lo que no es suyo va al resolvedor.
- **Puertas «solo para contar»**: `ecuacion:` y `calcular:` no cogen fracciones, decimales ni negativos (los leían mal).
- **`herramientas/comparar_puertas.py`**: pasa los 335 casos simbólicos de `mis_casos` y `mis_pruebas` que coge una
  puerta vieja por la puerta Y por el resolvedor: 42 distintas a propósito (cada una con su porqué: el resto, el año, dos
  huecos, «11 parejas»...), **0 sin explicar**. Lo corre `test_U4`.
- **Identidades** (`buscar.py`, `_bu_desarrollar` y `_bu_identidades`): cada relación se desarrolla con la distributiva
  (un polinomio: trozos de n, de n x n, de a x b... y lo suelto, con `_u_cuenta`); iguales → no dice nada (todas así:
  `cualquiera`); iguales salvo lo suelto → `ninguna`. Con una letra dividiendo no se desarrolla.
- **La prudencia con palabras** (`palabras.py`, `_pa_prudencia`): un dato fuera de lo que se usa que CUENTA lo mismo que
  la pregunta (las 12 cajas del camión) → «no entiendo: no sé qué hacer con el 12 de '...'»; una frase que no se entiende
  y trae una cantidad (también «la mitad», «el doble») → «no entiendo esta frase». Lo de otra cosa (la edad) o de otro
  dueño (los caramelos de Ana) sigue sobrando.
- `n = 12/3` → n = 4: la respuesta del resolvedor, en su forma más simple (antes `12/3`).
- `conocimiento/universal.kn`: reglas 11 (desarrollar) y 12 (la tabla y la red), errores típicos y fuentes.

**Lo que salió al probar (y se arregló, de forma general).**
- **Dos puertas viejas daban respuestas FALSAS** con números que no son para contar (lo cazó una muestra de 1742
  expresiones mezcladas por la tabla y por el resolvedor): `calcular: 1/2 + 0.25` → **2** (buscaba «2 + 0» dentro del
  texto); `ecuacion: 0.5 + ? = 12` → **7**, `ecuacion: -2 x ? = 12` → **6** (leía `0.5` como `5`, `-2` como `2`).
  Ahora `calcular` exige la cuenta ENTERA y las dos son «solo para contar»: 3/4, 11.5, -6. Tras el arreglo, 0 falsas.
- `? : 0 = 3`: el resolvedor decía `no_cuadra` (deshacía `x 0`); ahora «entre 0 no se reparte: ninguna».
- La primera versión de la prudencia era demasiado estricta (los caramelos de Ana, la edad de María): no basta con que
  sea la misma COSA; tiene que contar las mismas cosas por las que se pregunta.
- `a + b = 10; 2 x (a + b + c) = ...` decía «ninguna» (comprobaba en la identidad una c que nadie sabía): las identidades
  no entran en la comprobación de probar en orden; ahora «todavía no: c puede valer cualquier cosa».

**Lo que cambia de respuesta** (todo lo que era «no entiendo / no sale / todavía no» y ahora sale y se comprueba, o lo
que era FALSO): `1/2 x n = 3` → n = 6; `n + 1/2 = 3/4` → 1/4; `a + b = 9; a : b = 2` → 6 y 3; `2 x (n + 3) = 2 x n + 6`
→ cualquiera; `a + b = a + b + 1` → ninguna; `0 x n = 5` (E.5: no_sale) → ninguna; `0 x n = 0` → cualquiera (se
actualizó `test_U1`, con su porqué); las tres respuestas falsas de arriba; las dos con palabras («96 kilos», «50 pesos»)
→ no entiendo. Nada de la batería vieja ni de `mis_casos` cambió.

**Los 20 problemas simbólicos nuevos** (inventados, sin `resolver:` delante): **20/20 bien**:
`5 x n - 7 = 2 x n + 8` (5) · `3 x (x - 2) = x + 10` (8) · `y/4 + 3 = y/2 - 1` (16) · `0.5 x m + 1.25 = 3` (3.5) ·
`-3 x k + 4 = 19` (-5) · `2/3 x p = 3/4` (9/8) · `a + b = 17; a - b = 5` (11, 6) · `2 x a + 3 x b = 23; a - b = 4` (7, 3) ·
`x + y + z = 12; x - y = 1; y - z = 1` (5, 4, 3) · `a + b + c = 30; a = 2 x b; c = b + 2` (14, 7, 9) ·
`p + q = 1.5; p - q = 0.25` (0.875, 0.625) · `x + y = -2; x - y = 6` (2, -4) · `n x n = 81` (9) · `n x (n + 1) = 56` (7) ·
`a x b = 18; a + b = 9` (3 y 6; 6 y 3) · `4 x (n + 2) - 8 = 4 x n` (cualquiera) · `5 x (a - 1) = 5 x a - 3` (ninguna) ·
`(x + 2) x (x + 2) = x x x + 4 x x + 4` (cualquiera) · `3 x n + 1/2 = n + 2.5` (1) · `a + b = 8; 3 x a + 3 x b = 20` (ninguna).
Como eran demasiado fáciles, 10 más difíciles: **8/10** (`x/3 - x/4 = 2`, `2 x (x + 1) = 3 x (x - 1)`, un sistema de 3x3
general, `0.2 x (n - 5) = -1.4`, `1 : x = 4`, `a : b = 3; a + b = 20`, `(n - 3) x 4 = -8`,
`3 x (2 x n - 1) - 2 x (n + 4) = 1`); fallan **`n x n - 5 x n + 6 = 0`** y **`x x x = 2 x x`** (todavía no): son no lineales
y ninguna relación pone un TOPE para probar en orden (no son «de + y x = N»).

**Los límites que quedan (honestos).**
- No lineales sin tope (`n x n - 5 x n + 6 = 0`): todavía no.
- `3 x n = 13` sigue «no_sale» (con números para contar); el resolvedor dice 13/3 en la explicación. Igual `1/4 de 13`,
  `ecuacion: 8 + ? = 5`, `a + b = 10; a - b = 12` (ninguna con números para contar; con negativos, 11 y -1). **Pregunta
  para Carlos:** ¿esos «no hay número para contar» deben pasar ya a la fracción o al negativo?
- `ecuacion: ? + ? = 10`: E.1 dice «dos huecos» (pueden ser distintos); el resolvedor los toma como la MISMA letra (5).
- `a - b = 3`: S.3 dice «infinitas»; el resolvedor todavía no lo sabe decir de una relación sola con dos letras.
- Las puertas viejas siguen siendo ~95 entradas en la tabla (juntas, pero no todas traductores): E.5, S.3 y S.2 ya leen
  con el modelo; E.1/E.4 (`ecuacion:`), E.0 (`verdad:`), M.16 (`combinar`), F.x siguen con su lector, protegidos por la
  regla y por la marca «solo para contar».
- La prudencia con palabras mira los datos que se quedan FUERA; un dato mal leído que sí entra en la cuenta no lo ve
  (eso sería ampliar la parte hablada, que Carlos ha parado).
