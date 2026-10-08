# Paso S.3 — PROBLEMAS CON DOS INCÓGNITAS — 8 oct 2026

Segundo paso de **6.º** (Year 6). Es el segmento **1.31** de NCETM (Spine 1): *Problems with two unknowns*. Se llama
**S.3** porque sigue la serie de las estructuras (S.1 «veces», S.2 parte-parte-todo con tres partes o más): es la
misma barra de S.2, pero ahora faltan DOS cosas y hay que ver si con lo que se dice basta para saberlas.

## 1. EL PLAN (escrito antes de programar)

**La fuente.** La web de NCETM **sigue sin abrirse desde la nube** (`EGRESS_BLOCKED www.ncetm.org.uk`, probado hoy con
`primm-131-problems-with-two-unknowns`), y Oak National tampoco (`EGRESS_BLOCKED www.thenational.academy`). Lo que
sigue sale del **buscador** (el resumen del segmento 1.31, el de la unidad 11 de Year 6 «Solving problems with two
unknowns» de la *Curriculum Prioritisation* de NCETM y los resúmenes de las lecciones de Oak de esa unidad). **Falta
leer el segmento entero** (diapositivas, ejemplos) cuando Carlos pueda abrirlo.

Los **cinco puntos de enseñanza** del segmento (traducidos):
1. **Los problemas con dos incógnitas pueden tener una solución, más de una, o ninguna.**
2. **La relación entre las dos incógnitas se puede decir de maneras distintas: aditiva («8 más que») o
   multiplicativa («el triple»).**
3. **Dibujar el modelo (la barra) deja ver la estructura** del problema.
4. **Hay UNA sola solución si se da la suma de las dos y su diferencia** («suma y diferencia»), **o la suma y una
   relación multiplicativa** («suma y múltiplo»).
5. **Algunos problemas no se dejan dibujar fácilmente, pero se resuelven probando y mejorando de forma
   SISTEMÁTICA**; pueden tener una solución, varias o infinitas.

La unidad de Year 6 añade: explicar POR QUÉ un problema de suma y diferencia tiene una sola solución; usar la barra
para enseñar cómo se resuelve; resolver con una, varias o infinitas soluciones. Oak avisa de dos cosas: **no hay una
regla fija para saber cuántas soluciones tiene un problema: hay que razonarlo cada vez**; y el error de dibujar las
barras sin alinearlas (las dos barras tienen que empezar en el mismo sitio, una debajo de la otra, para que se vea
la diferencia). Su ejemplo: A + B = 30, A − B = 8: dos barras, la de A con un trozo de 8 de más.

**Cómo, sin calculadora (como lo haría un humano).**
- **Suma y diferencia** (a + b = 30; a − b = 8). Dibujo las dos barras alineadas: la de a es la de b y un trozo de
  8. Si **quito la diferencia** del todo, quedan **dos barras iguales**: 30 − 8 = 22, 22 : 2 = 11 = b; y a = 11 + 8 =
  19. Otra manera (la misma barra): **añado la diferencia** a la barra pequeña y quedan dos barras como la grande:
  30 + 8 = 38, 38 : 2 = 19 = a; b = 19 − 8 = 11. Dan lo mismo.
  Se ve por qué hay UNA sola: la barra no deja otra forma de repartir.
  Si la diferencia no cabe en la suma (a + b = 10; a − b = 12) no hay ninguna (con números que se cuentan).
  Si al quitar la diferencia queda un número impar (a + b = 9; a − b = 4 → 5 : 2), con enteros no hay ninguna, pero
  con decimales sí (b = 2.5, a = 6.5): repartir en décimas (M.13).
- **Suma y múltiplo** (a + b = 24; a = 3 x b). La barra de b es UN trozo; la de a, TRES trozos como ese. Juntas son
  3 + 1 = **4 trozos iguales** (se cuentan: uno, dos, tres... y uno más): 24 : 4 = 6 = b; a = 3 x 6 = 18.
- **Diferencia y múltiplo** (a − b = 20; a = 3 x b; la misma barra, la relación aditiva y la multiplicativa a la
  vez): la diferencia son los trozos que a tiene de más: 3 − 1 = **2 trozos** = 20 → un trozo es 10 = b; a = 30.
  (El punto 4 solo nombra las dos de la suma; esta también tiene una sola, y se dibuja igual.)
- **Probar en orden** (punto 5): cuando no se deja dibujar (a x b = 24 y a + b = 10; 10 monedas de 2 y de 5 que hacen
  32: a + b = 10 y 2 x a + 5 x b = 32). Una ecuación **pone el tope** (la suma: a va de 0 a 10; el producto: las
  parejas de factores de M.15; 2 x a + 3 x b = 20: el que más pesa va de 0 hasta donde cabe) y la otra **se
  comprueba** en cada prueba. Se prueba EN ORDEN para no dejarse ninguna y saber si hay una, varias o ninguna.
  Un humano no hace cientos de pruebas: hay un tope (escrito en el `.kn`); si harían falta más, «todavía no».
- **Una sola ecuación** (punto 1 y 5): a + b = 10 tiene **11 parejas** de enteros (0 + 10, 1 + 9 … 10 + 0: una más que
  la suma; 9 si no vale el 0) e **infinitas** con decimales. a − b = 3 o a = 3 x b solas: **infinitas** aun con
  enteros (cualquier b vale). a x b = 24: las parejas de factores. 2 x a + 3 x b = 20: probando en orden.

**Lo que se construye.**
- `conocimiento/dos_incognitas.kn`: las reglas (una, varias, ninguna; la relación aditiva o multiplicativa; la barra;
  cuándo hay una sola; probar en orden y su tope), los errores típicos y las fuentes.
- Parte nueva `sistema/partes/dos_incognitas.py` (prefijo `_di_`): LEE las ecuaciones con dos letras (separadas por
  `;`: `a + b = 30; a - b = 8`, también con `x` e `y`, con decimales, y con la orden delante `dos incognitas:` si se
  quiere), dice de qué FORMA es cada una (suma, diferencia, múltiplo, producto, suma con pesos), DIBUJA la barra,
  pregunta a las piezas y explica. Las formas que no conoce: «todavía no» con las que sí.
- Pregunta nueva `dos_incognitas` (la más rápida que sale; las demás que servían se enseñan como OTRA ESTRATEGIA).
- Piezas nuevas, **cada una con su vuelta real** (poner los números en TODAS las ecuaciones y calcularlas con
  `combinar`, M.16):
  - `suma_y_diferencia_quitando_la_diferencia` y `suma_y_diferencia_anadiendo_la_diferencia`;
  - `suma_y_multiplo_con_la_barra`; `diferencia_y_multiplo_con_la_barra`;
  - `probar_en_orden` (sistemático, con el tope del `.kn`);
  - `una_suma_sola_todas_las_parejas`; `sin_tope_infinitas`.
- La orden se enruta en `explicacion.py` y `probar.py` ANTES que la ecuación con letra de E.5 (que con dos letras
  decía «todavía no»).

**Las trampas.**
- `a + b = 30; a - b = 8` → a = 19, b = 11. **No** 30 : 2 = 15 y 15 + 8 = 23 (así suman 38): primero se quita la
  diferencia.
- `a + b = 24; a = 3 x b` → b = 6, a = 18. **No** 24 : 3 = 8: los trozos son 3 + 1 = 4.
- `a - b = 20; a = 3 x b` → b = 10, a = 30. **No** 20 : 3: la diferencia son 3 − 1 = 2 trozos.
- `a + b = 10; a - b = 12` → ninguna (la diferencia no cabe en la suma).
- `a + b = 9; a - b = 4` → a = 6.5, b = 2.5 (con enteros, ninguna).
- `a + b = 10` → 11 parejas con enteros (infinitas con decimales). `a - b = 3` → infinitas.
- `a x b = 24; a + b = 10` → a = 4, b = 6 y a = 6, b = 4 (los mismos números en otro orden: con letras son dos).
- `a + b = 10; 2 x a + 5 x b = 32` → a = 6, b = 4. `2 x a + 3 x b = 20` → cuatro soluciones.
- `b - a = 8` (la grande es b), `x + y = 30; x = y + 8`, `24 = a + b`: el orden y las letras no cambian nada.
- Con dinero y decimales: `a + b = 1.20; a - b = 0.40` → a = 0.8, b = 0.4. Tres decimales:
  `a + b = 1.235; a - b = 0.115` → a = 0.675, b = 0.56. `a + b = 1.001; a - b = 0` → todavía no (diezmilésimas).
- Cerca del techo: `a + b = 9999999; a - b = 1` → a = 5000000, b = 4999999; `a + b = 10000000; a = 4 x b`;
  `a + b = 10000001` → no alcanza.
- `a + b = 100; a x b = 2400` (probar 101 veces no es humano): por las parejas de factores, sí. `a + b = 500;
  2 x a + 5 x b = 1600` → todavía no (demasiadas pruebas).

**Prueba de dominio** (`pruebas/test_S3_dos_incognitas.py`): suma y diferencia en una muestra (enteros, impares,
decimales, grandes) contra un testigo escrito aparte (Python, solo en la prueba); suma y múltiplo y diferencia y
múltiplo con k de 1 a 12; las dos estrategias de suma y diferencia siempre de acuerdo; probar en orden contra el
testigo que prueba todo (productos, monedas, pesos); una sola ecuación (cuántas, infinitas); ninguna; las trampas;
piezas trucadas (una cuenta que da uno de más: la vuelta lo caza); cerca del techo y el tiempo (cada pregunta muy
por debajo de 2-3 s).

**Para Carlos:** `a + b = 30; a - b = 8`, `a + b = 24; a = 3 x b`, `a + b = 10; 2 x a + 5 x b = 32`, `a + b = 10`,
`a + b = 10; a - b = 12`.

## RESULTADO (8 oct 2026)

**Hecho, verde: proyecto 3095/3095 + 813/813 (antes 2994 + 799); mis_pruebas 233/233; `test_S3` 101/101.**

**Lo que se construyó.**
- `conocimiento/dos_incognitas.kn`: las 6 reglas (una, varias o ninguna; aditiva o multiplicativa; la barra alineada;
  cuándo hay una sola; probar en orden y su **tope de 30 pruebas**; una sola ecuación), los errores típicos y las fuentes.
- Parte `sistema/partes/dos_incognitas.py`: lee una o dos ecuaciones con dos letras (`;` entre ellas; `x` e `y` valen;
  el número puede ir a la izquierda, `24 = a + b`; `a = b + 8`, `a = b - 8`, `b x 3 = a`; decimales hasta las milésimas;
  la orden `dos incognitas:` delante es opcional). Dice la FORMA de cada una (suma, diferencia, múltiplo, producto, suma
  con pesos), dibuja la barra, pregunta a las piezas, enseña la otra estrategia, los errores típicos calculados, cuántas
  soluciones hay y por qué, y la comprobación. Se enruta antes que la letra de E.5 (que con dos letras decía «todavía no»;
  con una letra, o la misma dos veces, sigue siendo de E.5).
- Preguntas `dos_incognitas` (la más rápida que sale) y `cumplen_las_ecuaciones` (la comprobación).
- **Ocho piezas**, todas con su vuelta real — poner los números en TODAS las ecuaciones y calcularlas con `combinar`
  (M.16), que a su vez deshace cada cuenta con la contraria:
  - `suma_y_diferencia_quitando_la_diferencia` (30 − 8 = 22; 22 : 2 = 11 = b; a = 19) y
    `suma_y_diferencia_anadiendo_la_diferencia` (30 + 8 = 38; 38 : 2 = 19 = a; b = 11): siempre dan lo mismo.
    Si la diferencia no cabe en la suma, ninguna (y se comprueba mirando la lista). Si queda impar, en décimas.
  - `suma_y_multiplo_con_la_barra` (los trozos se cuentan recitando: tres y uno más, cuatro; 24 : 4 = 6).
  - `diferencia_y_multiplo_con_la_barra` (los trozos de más, recitando hacia atrás: 3 − 1 = 2; 20 : 2 = 10).
  - `probar_en_orden`: el producto (las parejas de factores de M.15, en los dos órdenes), la suma (de 0 a la suma) o
    la suma con pesos (prueba con el que MÁS pesa: `2 x a + 3 x b = 20`, b de 0 a 6, 7 pruebas) ponen el tope; la otra
    ecuación se comprueba en cada prueba. Su vuelta: cada solución en todas las ecuaciones, **cada prueba cumple el tope**
    y **las pruebas se cuentan otra vez** (hice 11 y tenía que hacer 11).
  - `una_suma_sola_todas_las_parejas` (a + b = 10: once parejas, nueve sin el 0; infinitas con decimales).
  - `sin_tope_infinitas` (a − b = 3 o a = 3 x b solas).
  - `poner_los_numeros_en_las_ecuaciones` (la comprobación de todas).
- **Los contextos (punto 4 en palabras):** el resolvedor de R.1 con «Ana y Luis tienen 30 entre los dos. Ana tiene 8 más
  que Luis» decía «me doy vueltas». Ahora, si hay un «entre los dos» y un «más/menos que» de las mismas dos personas y de
  ninguna se sabe nada más, le pasa el problema a S.3 (los nombres hacen de letras): Luis 11. Si saldrían 6.5 canicas,
  **sin solución** (las cosas se cuentan enteras); si la diferencia no cabe, sin solución. Lo de antes (dar vueltas sin
  dato) sigue igual.

**Lo que salió al probar (y se arregló).**
- **Una vuelta que no cazaba un fallo**: `probar_en_orden` con una cuenta trucada (uno de más) calculaba mal el otro
  número de cada prueba, no encontraba ninguna y decía «ninguna» con la vuelta en SÍ (solo contaba las pruebas). Ahora
  también mira que cada prueba cumpla la ecuación del tope: la pieza trucada se caza.
- `a + b = 10; a - b = 12` iba por probar en orden en vez de por la barra: la resta que no se puede llega como `NoSalio`, no
  como `ValueError`. Arreglado: la barra dice «la diferencia es MAYOR que la suma».
- Repartir entre 11 o 12 (suma y múltiplo con k = 10 u 11) no salía: iba directo a las décimas. Ahora primero la división
  de siempre (las tablas del 11 y del 12) y solo si sobra, en décimas.
- Con memoria vacía (las pruebas), repartir pide las tablas: la prueba las aprende primero, como S.2 («en 6.º ya se saben»).
- `a + b = 10000000` reventaba (una pareja más que el techo no tiene nombre). Ahora lo dice.
- En el plan escribí que `a + b = 100; a x b = 2400` saldría por las parejas de factores: **no**. Sacar las parejas de 2400
  pide dividir entre 13 o más (M.15 dice «todavía no»: la división larga) y por la suma serían 101 pruebas. Dice
  «todavía no». (Un humano lo haría probando y MEJORANDO: 50 x 50 = 2500 se pasa, 40 x 60 = 2400. Es la «mejora» del
  punto 5, que aquí todavía no se hace: se prueba en orden.)

**Los límites que quedan (honestos: bien o «todavía no», nunca mal).**
- Medios de siete cifras (`a + b = 6872854; a - b = 15961` → 3 428 446.5): contados en décimas se pasan del techo; no se
  puede comprobar y no se da (28 de los 140 de la muestra; los otros 112, todos bien). Lo mismo con más de tres decimales (`a + b = 1.001; a - b = 0`).
- Repartir un número grande entre 10 o más (`a + b = 567127; a = 10 x b`, 11 trozos): la división larga (NCETM 2.24).
- Más de 30 pruebas (`a + b = 500; 2 x a + 5 x b = 1600`): todavía no. Un producto de cero (`a x b = 0`), tres letras, tres
  ecuaciones, pesos con decimales, la diferencia y el múltiplo de lados contrarios (`a - b = 8; b = 3 x a`): todavía no.
- «Ana tiene el triple que Luis» con palabras: R.1 no tiene esa forma; con la ecuación sí (`a + b = 24; a = 3 x b`).

**El tiempo.** Ninguna pregunta del paso pasa de 0,1 s (la más lenta, explicada entera con sus otras estrategias, ~0,1 s).
La batería: 189-199 s (dos pasadas); la de antes del paso, en la misma máquina y el mismo momento, 183 s (hoy la máquina va más lenta
que los 139 s del diario de N.6).

**Falta la prueba de Carlos.** Y leer el segmento entero de NCETM 1.31 cuando se pueda abrir.
