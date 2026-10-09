# Paso M.17 — ESTRATEGIAS PARA MULTIPLICAR NÚMEROS GRANDES Y LA MULTIPLICACIÓN LARGA — 9 oct 2026

Vuelta al orden de NCETM tras el plan U (cumplido). Es el segmento **2.23** de NCETM (Spine 2, Year 6):
*Multiplication strategies for larger numbers and long multiplication*. Se llama **M.17** porque sigue la serie de la
multiplicación (M.10 la multiplicación corta, M.12 la equivalencia, M.14 tres factores, M.15 factores, M.16 combinar).

**REGLA NUEVA desde el plan U (Carlos, 9 oct):** lo nuevo entra por el MODELO COMÚN. Las técnicas nuevas son PIEZAS
(operadores) que el resolvedor universal usa en cualquier problema; **no se abre ninguna puerta ni formato nuevo** para
este tema. Cualquier expresión o ecuación con los números grandes que permita el tema tiene que salir por la tabla de
puertas única (`puertas.py`) y el resolvedor.

## 1. EL PLAN (escrito antes de programar)

**La fuente.** La web de NCETM sigue bloqueada desde la nube (`EGRESS_BLOCKED www.ncetm.org.uk`, probado hoy con
`primm-223-...`). Lo que sigue sale del **buscador** (el resumen de la página del segmento 2.23, el PDF de NCETM
«PSKA multiplication Q7» y las lecciones de Oak National de Year 6 «multiplying and dividing by 2-digit numbers»), y de
**Common Core 5.NBT.B.5** (Achieve the Core: el algoritmo estándar «reduce multiplicar dos números de varias cifras a
una colección de cuentas de una cifra»; el error principal es de VALOR DE POSICIÓN: multiplicar por 4 en vez de por 40).
**Falta leer el segmento entero** (diapositivas, ejemplos) cuando Carlos pueda abrirlo.

Los **cinco puntos de enseñanza** de 2.23 (según el buscador, traducidos):
1. **Múltiplos de 10, 100 o 1000**: se multiplican las decenas, centenas o millares (el hecho pequeño) y luego se
   ajusta el producto con el valor de posición. (300 x 40: 3 x 4 = 12 → 12 000.)
2. **Un factor múltiplo de 10, 100 o 1000**: la multiplicación CORTA y luego se ajusta con el valor de posición.
   (234 x 30: 234 x 3 = 702 → 7020.)
3. **Dos números de dos cifras**: se PARTE UNO de los factores, se hallan los productos parciales y se suman. Se alarga
   a tres cifras por dos. (24 x 15 = 24 x 10 + 24 x 5 = 240 + 120 = 360.)
4. **La multiplicación larga**: un algoritmo de multiplicar y luego SUMAR LOS PRODUCTOS PARCIALES, para números de dos
   cifras o más.
5. **Un factor compuesto**: se multiplica por uno de sus factores y luego por el otro. (24 x 15 = 24 x 3 x 5 = 72 x 5.)

Y lo que se espera ver (PSKA, «look-fors»): que el niño aplique la corta en contextos variados, **explique la estructura
de la larga** (cada fila es un producto parcial; la fila de las decenas es «por 20», no «por 2») y **use lo mental cuando
conviene** (no la larga para 300 x 40). Errores típicos: **no poner el 0 que guarda el sitio** al multiplicar por las
decenas; **olvidar lo que se lleva**; desordenar las columnas al sumar las filas.

**Lo que ya hay (y no se rompe).** La rejilla de N.4 (partir LOS DOS por sitios, el modelo de área) ya multiplica dos
números de varias cifras; la corta (M.10), las decenas justas (M.9, solo si el hecho pequeño se sabe de memoria),
doblar y partir (M.12), las parejas de 100 (M.15). El motor de piezas elige «la más rápida que encaja» (rapidez).
`234 x 56` hoy sale 13104 por la rejilla; `234 x 30`, `2300 x 400` y `24 x 15`, también por la rejilla.

**Cómo lo haría un humano de 6.º sin calculadora.** Mira los números antes de escribir nada:
- ¿acaban en cero? los quita, multiplica lo que queda y los vuelve a poner (puntos 1 y 2);
- ¿dos cifras por dos (o tres por dos)? parte uno de los factores por sitios y suma dos productos parciales (punto 3);
- ¿un factor de dos cifras es una pareja de la tabla (15 = 3 x 5, 24 = 4 x 6)? multiplica por uno y luego por el otro,
  dos multiplicaciones cortas sin sumar nada (punto 5) — sobre todo si el otro factor es grande (1234 x 24);
- si no, la **multiplicación larga** (punto 4): el más largo arriba; una FILA por cada cifra del de abajo, desde las
  unidades, cada fila una multiplicación corta; en la fila de las decenas se pone primero un **0 que guarda el sitio**
  (es «por 20», no «por 2»); en la de las centenas, dos; y se suman las filas por columnas.
  ```
        3456
      x  247
      ------
       24192     3456 x 7
      138240     3456 x 40   (un 0 en las unidades, y 3456 x 4)
      691200     3456 x 200  (dos 0, y 3456 x 2)
      ------
      853632
  ```
- y lo COMPRUEBA con la operación contraria: cada fila, quitando los ceros que puso (÷ 10) y repartiendo entre su cifra
  (la división corta), tiene que volver a dar el número de arriba; y la suma, quitando las filas una a una, tiene que
  dejar 0. Así se cazan el 0 olvidado (la fila de las decenas no se deja dividir entre 10 o no vuelve a dar el de arriba)
  y lo que se lleva olvidado.

**Lo que se construye** (todo PIEZAS de la pregunta `multiplicar`; el motor de piezas, el resolvedor y las puertas no
cambian de forma; cada pieza con su VUELTA real):
1. `multiplicar_quitando_los_ceros` (puntos 1 y 2; rapidez 7.5): quita los ceros del final de los dos factores; lo que
   queda, con la corta (por su nombre) o con la larga si los dos siguen siendo de varias cifras; vuelve a poner todos los
   ceros. Condición nueva: un factor acaba en cero y, quitados los ceros, queda una cuenta de varias cifras (si queda un
   hecho de la tabla, es lo de M.9, que va antes). Vuelta: el producto, quitándole los ceros (÷ 10, por su pieza), vuelve
   a dar el producto pequeño.
2. `multiplicar_partiendo_un_factor` (punto 3; rapidez 9.1, detrás de la distributiva de M.6, 9, que gana cuando los trozos ya se saben: 13 x 12 = 10 x 12 + 3 x 12): dos cifras por dos, o tres por dos; se parte el de dos
   cifras (decenas + unidades): el otro por las decenas (la corta y un 0) y por las unidades (la corta); se suman los dos
   productos parciales. Vuelta: el total quitando un producto parcial da el otro (restar), y cada parcial, quitando su 0
   y repartiendo entre su cifra (la división corta), vuelve a dar el otro factor.
3. `multiplicar_por_un_factor_compuesto` (punto 5; rapidez 9.2): un factor de dos cifras que es una pareja de la tabla
   (dos factores de una cifra, buscados en lo que se sabe de memoria, el de en medio más grande primero: 24 = 4 x 6)
   y el otro de varias cifras: dos multiplicaciones cortas. Vuelta: repartir el resultado entre el segundo factor y
   luego entre el primero (la división corta) vuelve a dar el número de partida.
4. `multiplicacion_larga` (punto 4; rapidez 9.5): los dos de varias cifras; el más largo arriba; una fila por cada cifra
   del de abajo (la corta, por su nombre; una cifra 0 no da fila; una cifra 1 copia el de arriba); los ceros que guardan el
   sitio; las filas se suman con `sumar`; el dibujo en columnas. Vuelta: cada fila ÷ 10 tantas veces como ceros puso y
   ÷ su cifra (la división corta) vuelve a dar el de arriba; el total quitando las filas (restar) deja 0.
   - Las rapideces dejan el orden de un humano: lo mental antes (decenas justas 3, la corta 7, quitar ceros 7.5), luego
     partir uno (8.5) y el compuesto (9), la larga (9.5) y, solo si nada de eso sale, la rejilla (10), que se queda como
     estaba para quien no sabe las tablas (sin las tablas en la memoria, la corta no se usa, M.10, y tampoco la larga).
5. **El resolvedor dice con qué multiplicó** (`numero.py`): cuando los dos factores son de varias cifras, la línea de la
   cuenta lleva el método (`3456 x 247 = 853632   (con la multiplicacion larga)`): se ve que el modelo común usa las
   piezas nuevas sin puerta nueva.
6. **Comprobar una división deshaciéndola** (`universal.py`, en la comprobación final): lo que falta para que salgan las
   ecuaciones del tema. `n : 24 = 356` se despeja con la larga (n = 356 x 24 = 8544), pero la comprobación tenía que
   calcular 8544 : 24, que es la división larga (2.24, todavía no) y decía «no cuadra». Un humano comprueba una división
   con la multiplicación (dividir es lo contrario de multiplicar, NCETM 2.6, 3.OA.B.6: 8544 : 24 = 356 porque
   356 x 24 = 8544). Regla general: si un lado de una relación no se puede calcular, se comprueba DESHACIENDO desde el
   otro lado (lo que se suma se resta, lo que se divide se multiplica...) hasta llegar al trozo que no se podía; si así
   cuadra, cuadra. Vale para `n : 24 - 10 = 346` y para cualquier relación.

**Las trampas.**
- El 0 que guarda el sitio: una larga TRUCADA que lo olvida (3456 x 247 = 24192 + 13824 + 6912) no se da por buena (su
  vuelta no cuadra) y contesta otra pieza con el número bien.
- Lo que se lleva: una corta trucada que lo olvida → la vuelta de la fila no cuadra.
- Ceros en medio del de abajo: 3456 x 205 (la fila de las decenas no existe: 0 x 3456 = 0; la de las centenas lleva dos 0).
- Cifras 1 en el de abajo (3456 x 111): la fila es el de arriba con sus ceros.
- Lo mental cuando conviene: `300 x 40` sigue con las decenas justas; `347 x 6` con la corta; `25 x 48` con doblar y
  partir; `234 x 30` ya no va a la rejilla (quitar los ceros: 234 x 3 = 702 → 7020).
- El techo: `4567 x 3000` sigue «no se puede: me paso de diez millones»; `3162 x 3162` = 9 998 244 sí sale.
- La división entre dos cifras sigue «todavía no» (2.24): `24 x n = 8544` → no_sale (con números para contar).
- Sin las tablas en la memoria: lo de antes (la rejilla con la suma de iguales).
- Nada viejo cambia de respuesta (el número); cambia el método elegido en algunos productos de varias cifras.

**Prueba de dominio** (`pruebas/test_M17_multiplicacion_larga.py`, pocas y representativas): cada pieza contra el testigo
(Python `*`, SOLO en la prueba) en una muestra pequeña al azar fijo; qué pieza elige el control en los casos típicos; las
piezas trucadas (sin el 0, sin lo que se lleva); ceros y unos en el de abajo; el techo; por el modelo común (sin
`resolver:` y con él): cuentas, `n = 3456 x 247`, `n - 1000 = 234 x 56`, `n : 24 = 356`, `n : 24 - 10 = 346`, dos
relaciones, combinar con + y -; lo que sigue siendo «todavía no»; sin las tablas; el tiempo (cada una por debajo de 2 s).

**Para Carlos:** `3456 x 247`, `24 x 15`, `1234 x 24`, `234 x 30`, `n : 24 = 356`.

## RESULTADO (9 oct 2026)

**Hecho. `test_M17` 56/56; proyecto 3385/3385 afirmaciones (3329 de antes + 56) + 873/873 casos, en tercios, VERDE; mis_pruebas 262/262; casos 873/873 (863 + 10 nuevos);
`comparar_puertas` 0 diferencias sin explicar.** Falta la prueba de Carlos.

**Lo que se construyó** (todo PIEZAS de `multiplicar`; ninguna puerta ni formato nuevo):
- `multiplicar_quitando_los_ceros` (puntos 1 y 2, rapidez 7.5): 234 x 30 → 234 x 3 = 702 (la corta) → 7020;
  2300 x 450 → 23 x 45 (partiendo uno) → 1 035 000. Vuelta: el producto : 10 tantas veces como ceros puso vuelve al
  pequeño; y si lo pequeño se hizo con la corta, repartiéndolo entre la cifra vuelve el otro factor.
- `multiplicar_partiendo_un_factor` (punto 3, rapidez 9.1; detrás de M.6): dos por dos o tres por dos; 326 x 47 = 326 x 40 + 326 x 7.
  Vuelta: el total menos un parcial da el otro; cada parcial : 10 y : su cifra vuelve a dar 326.
- `multiplicar_por_un_factor_compuesto` (punto 5, rapidez 9.2): 1234 x 24 = 1234 x 4 x 6 (la pareja, de la memoria; la de
  en medio). Vuelta: 29616 : 6 : 4 = 1234.
- `multiplicacion_larga` (punto 4, rapidez 9.5): el más largo arriba, una fila por cifra (la corta), los 0 que guardan el
  sitio, una cifra 0 no da fila, las filas se suman; el dibujo en columnas. Vuelta: cada fila : 10 (sus ceros) : su cifra
  vuelve a dar el de arriba (así se caza el 0 olvidado y lo que se lleva olvidado), y el total quitando las filas deja la
  última.
- Dos condiciones nuevas en `_condiciones.py` (prefijo `_m17_`); el explicador de M.1 enseña la comprobación de las piezas
  que traen `vuelta_explicada` (las de antes, igual).
- **Por el modelo común:** `numero.py` dice con qué se multiplicó cuando los dos factores son de varias cifras
  (`3456 x 247 = 853632 (con la multiplicacion larga ...)`); `universal.py` comprueba DESHACIENDO
  (`_u_comprobar_deshaciendo`): si un lado de una relación no se puede calcular todavía (8544 : 24 es la división larga),
  se deshace desde el otro lado (lo que se suma se resta, lo que se divide se multiplica) hasta ese trozo.

**Lo que salió al probar (y se arregló).**
- La primera versión comprobaba cada fila con la pieza `division_corta`: el mapa de piezas tenía una VUELTA (la división
  corta se comprueba con `multiplicar`, y `multiplicar` ya incluye la larga) y `test_piezas` se puso en rojo. Ahora la
  división entre una cifra de la comprobación se hace dentro de la pieza (`_repartir`, como la corta de M.11, con las tablas
  de la memoria).
- `quitar los ceros` solo comprobaba los ceros: una corta trucada dentro no se cazaba. Ahora comprueba también lo pequeño.
- La auditoría sin calculadora cazó un `texto % x + (...)` en un mensaje: con formato.
- Partir uno de los factores iba con rapidez 8.5 (la del primer plan) y se adelantaba a la distributiva de M.6 en
  `13 x 12` (10 x 12 + 3 x 12, dos productos que ya se saben: más corto): `test_M6` B6 en rojo por el MÉTODO. Ahora partir
  uno va con 9.1 y el compuesto con 9.2, detrás de M.6 (9): lo viejo sigue igual y en dos por dos sin productos sabidos
  (37 x 46) se parte uno.

**Lo que cambia.** Ningún NÚMERO viejo cambia. Cambia el MÉTODO elegido en productos de varias cifras cuando se saben las
tablas (antes la rejilla; ahora quitar ceros, partir uno, el compuesto o la larga): una prueba vieja lo miraba
(`test_N4` F3, 18 x 38 «con la rejilla») y ahora pide la rejilla por su nombre, con el caso viejo escrito al lado. Sin las
tablas, todo como antes (la rejilla). `n : 24 = 356` (y `n : 24 - 10 = 346`) pasan de `no_cuadra` a `n = 8544`.

**Los límites que quedan (honestos).**
- La división entre dos cifras sigue «todavía no» (`24 x n = 8544` → no_sale): es el paso siguiente, **NCETM 2.24**.
- Comprobar deshaciendo usa la MISMA multiplicación que el despeje (356 x 24): la comprobación independiente es la vuelta
  de la propia larga (cada fila con la operación contraria). Con la división larga (2.24) se podrá comprobar dividiendo.
- La elección sigue por `rapidez` fija (no por lo que cuesta ESTE caso; la idea del futuro de CLAUDE.md, sin tocar).
- La puerta de M.1 sigue escribiendo «LA SUMA REPETIDA: 56 + 56 + ... (el 56, 234 veces)» antes del método: es lo viejo.
- La web de NCETM sigue bloqueada desde la nube: falta leer el segmento 2.23 entero (diapositivas).
