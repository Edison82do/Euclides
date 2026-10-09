# Paso M.20 — LA MEDIA (repartir por igual) — 9 oct 2026

Siguiente paso del orden de NCETM en 6.º: el segmento **2.26** (Spine 2, Year 6), *Mean average and equal shares*.
Se llama **M.20** porque sigue la serie (M.17 la multiplicación larga, M.18 la división larga, M.19 compensar).

**REGLA desde el plan U (Carlos, 9 oct):** lo nuevo entra por el MODELO COMÚN, como PIEZAS que el resolvedor usa y que
se eligen por su costo cuando conviene; **no se abre ninguna puerta ni formato nuevo**; las preguntas se escriben con
números y símbolos.

## 1. EL PLAN (escrito antes de programar)

**La fuente.** La web de NCETM sigue bloqueada desde la nube (`EGRESS_BLOCKED www.ncetm.org.uk`, probado hoy con
`primm-226-mean-average`). Lo que sigue sale del **buscador** (el resumen de la página del segmento 2.26 y de la unidad
13 de Year 6 de *Curriculum Prioritisation*, «Mean average»). **Falta leer el segmento entero** (diapositivas) cuando
Carlos pueda abrirlo. Sus **cuatro puntos** (teaching points):
1. **La media es el tamaño de cada parte si se reparte por igual** (las torres que se NIVELAN: se quita de las altas y
   se da a las bajas hasta que todas son iguales).
2. **La media es la suma de los valores dividida entre cuántos valores hay.** Si se sabe la media y cuántos son, se sabe
   el total (media x cuántos); la media cambia si cambia el total o cuántos valores hay (y un CERO cuenta como valor).
3. La media sirve para **comparar** dos conjuntos de datos.
4. La media **no siempre** es una buena manera de resumir los datos.

La unidad 13 de Year 6 dice lo mismo en seis resultados: la media y el reparto igual; calcularla; cómo cambia si cambia el
total o el número de valores; el cero o el valor que falta; comparar; cuándo no sirve. **Common Core**: 6.SP.A.3 (una
medida del centro resume todos los valores con UN número) y la *Progression* de estadística de 6.º-8.º: la media como
**reparto justo** (*fair share*) y como **punto de equilibrio** (lo que sobra por encima de la media es igual a lo que
falta por debajo).

**Cómo lo haría un humano de 6.º sin calculadora.**
- `3, 5, 7`: junto 3 + 5 + 7 = 15 y lo reparto entre 3: 5 para cada uno (punto 2). O NIVELO: al 7 le sobran 2 y al 3 le
  faltan 2; paso 2 del 7 al 3: todos 5 (punto 1).
- `98, 102, 100, 104`: no sumo 404; NIVELO sobre el más bajo: el 98 es la base; por encima sobran 4, 2 y 6, juntos 12;
  12 entre los 4 son 3 para cada uno: 98 + 3 = 101. Es mucho más corto cuando los valores están CERCA (el costo).
- `3, 4, 6`: 13 entre 3 no sale justo: 4 y sobra 1, que también se reparte: 4 1/3 (13/3). **La media no tiene por qué
  ser entera ni ser uno de los valores.**
- `0, 4, 8`: el 0 CUENTA: 12 entre 3 = 4 (no entre 2).
- El valor que falta: «la media de 4, 7 y otro es 6» → el total es 6 x 3 = 18; falta 18 − 11 = 7 (punto 2 al revés).
- **Se comprueba**: media x cuántos (+ lo que sobró) = el total; o por el EQUILIBRIO: lo que sobra por encima de la media
  es lo mismo que lo que falta por debajo.

**Cómo se pregunta (sin puerta ni formato nuevo; por qué).** Con el resolvedor universal, que ya lee paréntesis, `:`,
fracciones y relaciones:
- `resolver: m = (98 + 102 + 100 + 104) : 4` — la media es la suma entre cuántos son (punto 2, escrito con símbolos).
- `resolver: 3 x m = 3 + 5 + 7` — el reparto igual: 3 partes iguales hacen el total (punto 1 escrito como relación).
- `resolver: (4 + 7 + n) : 3 = 6` — el valor que falta (ya sale hoy deshaciendo: 6 x 3 = 18).
- Comparar: `resolver: a = (...) : 3; b = (...) : 4` da las dos medias.

La cuenta sola `(3 + 5 + 7) : 3` (sin letras) responde hoy «todavía no: dividir dentro de una cuenta combinada es NCETM
2.28 (el orden de las operaciones)». **No se toca**: abrirla sería adelantar un año (la regla de U.4: una cuenta sin letras
respeta el año) y cambiar respuestas de M.16. Por `resolver:` ya se podía calcular (13/3), así que la media entra por ahí.
**Pregunta para Carlos**: si `(3 + 5 + 7) : 3` debe salir ya en 2.26 o esperar a 2.28.
No se crea `media: 3, 5, 7` ni nada parecido: sería una puerta nueva.

**Lo que hay hoy.** `resolver: m = (3 + 4 + 6) : 3` → 13/3 sumando y dividiendo (las piezas de sumar y dividir, sin
saber que es una media). `(4 + 7 + n) : 3 = 6` → 7. Lo que NO hay: nivelar (punto 1), la comprobación por el equilibrio,
y valores grandes cuyo total se pasa del techo (`(9999998 + 9999999 + 10000000) : 3`: sumar se sale de la lista).

**Lo que se construye** (todo PIEZAS; el motor de piezas no cambia):
- Una PREGUNTA nueva de piezas, `media` (en `_objetivos.py`, «la más rápida»): situación `{valores, partes}`, valores
  enteros (el cero también) y tantas partes como valores. Devuelve el cociente y lo que sobra (como `dividir`).
1. `media_juntando_y_repartiendo` (rapidez 9; punto 2): junta los valores sumando (las piezas de `sumar`) y reparte el
   total entre cuántos son (las de `dividir`). **Vuelta** con las contrarias: cociente x cuántos + lo que sobra vuelve al
   total, y al total se le quitan los valores uno a uno hasta 0.
2. `media_nivelando` (rapidez 5; punto 1): el más bajo es la base (se halla comparando con el mecanismo); lo que cada uno
   tiene por encima (restas pequeñas), junto, se reparte entre todos y se pone encima de la base. **Encaja SOLO si
   conviene (el costo)**: el más bajo tiene dos cifras o más y ninguno pasa de él en más de 20 (si no, juntar es igual de
   corto y nivelar no ahorra nada). **Vuelta** por el EQUILIBRIO (la *Progression*): lo que sobra por encima de la media
   tiene que ser lo que falta por debajo más lo que sobró al repartir; no necesita el total, así que vale cerca del techo.
- **El enganche en el resolvedor** (parte `universal.py`, `_u_valor`): cuando un árbol es `(v1 + v2 + … + vk) : k`, con
  enteros y el divisor igual a CUÁNTOS valores hay (contados), el resolvedor pide la pregunta `media` (así se elige por el
  costo); si ninguna pieza sale, calcula como antes. Lo que sale se pasa al número común (cociente + sobra/k, simplificado):
  **el número es el mismo de antes** (13/3); cambia el MÉTODO cuando encaja nivelar, y la explicación dice «la media».
  Si el divisor no es cuántos son (`(3 + 5 + 7) : 5`), no es una media: como antes.

**Las trampas** (los errores típicos):
- **Olvidar el cero** al contar los valores (`0, 4, 8` entre 2 = 6). El enganche cuenta los valores escritos.
- **Dividir entre el número equivocado** (entre el mayor, o entre 2 siempre). La vuelta lo caza.
- **Redondear o tirar lo que sobra** (`3, 4, 6` → 4). La media es 4 1/3: lo que sobra también se reparte.
- **Nivelar mal**: repartir lo de encima entre los que están por encima en vez de entre TODOS, u olvidar sumar la base.
  La vuelta del equilibrio lo caza.
- Cerca del techo: los valores cerca de diez millones; el total se pasa, pero nivelar no lo necesita.

**Prueba de dominio** (`pruebas/test_M20_media.py`, pocas y representativas): cada pieza contra el testigo (Python
`sum`/`divmod`, SOLO en la prueba) en una muestra al azar fijo, enteras y no enteras; qué pieza elige el control (cerca →
nivelar; lejos o pequeños → juntar); las piezas trucadas (las trampas); por el resolvedor (la media, el reparto igual,
el valor que falta, el cero, comparar, no entera); el techo; lo que no cambia (`(3 + 5 + 7) : 3` sigue «todavía no»;
`(3 + 5 + 7) : 5` no es media); el tiempo (cada una por debajo de 2 s).

**Para Carlos:** `resolver: m = (98 + 102 + 100 + 104) : 4`, `resolver: m = (3 + 4 + 6) : 3`, `resolver: 3 x m = 3 + 5 + 7`,
`resolver: (4 + 7 + n) : 3 = 6`, `resolver: m = (0 + 4 + 8) : 3`.

## RESULTADO (9 oct 2026)

**Hecho. `test_M20` 38/38; proyecto en cuartos 3522/3522 afirmaciones + 890/890 casos, VERDE; mis_pruebas 277/277; casos
896/896; `comparar_puertas` 0 diferencias sin explicar.** Falta la prueba de Carlos.

**Lo que se construyó** (ninguna puerta ni formato nuevo):
- La pregunta de piezas `media` (`_objetivos.py`, la más rápida) y dos condiciones en `_condiciones.py` (prefijo `_m20_`).
- `media_juntando_y_repartiendo` (rapidez 9; punto 2): junta sumando y reparte entre cuántos son. La vuelta: media x
  cuántos + lo que sobró = el total, y quitándole los valores no queda nada.
- `media_nivelando` (rapidez 5; punto 1): la base es el más bajo (comparando con el mecanismo), lo de encima se junta y se
  reparte entre TODOS. Solo si conviene (el costo): el más bajo con dos cifras o más y ninguno a más de 20 de él. La
  vuelta por el EQUILIBRIO: lo que sobra por encima de la media = lo que falta por debajo + lo que sobró al repartir.
- El enganche en el resolvedor (`universal.py`: `_u_sumandos`, `_u_media`, llamado desde `_u_valor`): `(v1 + … + vk) : k`
  con enteros y el divisor igual a cuántos valores hay (contados, mirando que se LLAMEN igual) pide `media`; lo que sale
  pasa al número común (4 y 1/3 = 13/3). Si no es media o no sale, como antes.

**Lo que cambia sin cambiar el número.** El MÉTODO y la explicación de las medias que pasan por el resolvedor: ahora dicen
«LA MEDIA de … repartir por igual entre los k» y cómo se comprueba. Ninguna afirmación vieja ni ningún caso cambió. **Lo
que sale nuevo**: medias cuyo total se pasa del techo pero los valores están cerca (`(9999998 + 9999999 + 10000000) : 3` →
9999999; antes «todavía no»): nivelar no necesita el total, igual que un humano.

**Por qué se pregunta con `resolver:`.** La cuenta sola `(3 + 5 + 7) : 3` sigue «todavía no» (dividir dentro de una cuenta
combinada es 2.28 en la puerta de M.16; una cuenta sin letras respeta el año). Por el resolvedor ya se podía escribir la
media (`m = (…) : k`), el reparto igual (`3 x m = 3 + 5 + 7`) y el valor que falta (`(4 + 7 + n) : 3 = 6`): no hacía falta
nada nuevo para preguntarla. **Pregunta abierta para Carlos:** si `(3 + 5 + 7) : 3` sin letras debe salir ya en 2.26.

**Lo que salió al probar.** `(9999999 + 10000000) : 2`: nivelar da 9999999 y sobra 1 (9999999 y 1/2), pero el número común
lo escribe 19999999/2 y el de arriba se pasa del techo: «todavía no» (honesto; un número mixto en el modelo sería otro paso).

**Los límites que quedan (honestos).**
- Solo medias de ENTEROS por las piezas; con decimales o fracciones (`(2.5 + 3.5) : 2`) se calcula como antes (sumar y
  dividir con el número común), sin decir «la media».
- `3 x m = 3 + 5 + 7` y el valor que falta salen por deshacer (como antes), no por las piezas de `media`.
- Los puntos 3 (comparar) y 4 (cuándo no sirve la media) no tienen pieza: comparar se hace pidiendo las dos medias en un
  `resolver:` con `;`; el punto 4 es de hablar («cuanto más se avanza, menos se habla»).
- La web de NCETM sigue bloqueada desde la nube: falta leer el segmento 2.26 entero (diapositivas).
