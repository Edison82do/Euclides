# Paso M.14 — MULTIPLICAR TRES FACTORES Y EL VOLUMEN — 7 oct 2026

Sigue al M.13. Es el segmento **2.20** de NCETM (Spine 2, Year 5): *Multiplication with three factors
and volume*. En Common Core: **5.MD.C.3–5** (el volumen se mide contando cubos unidad; V = l × a × h =
B × h; volúmenes que se suman) y **5.OA** / 3.OA.B.5 (las propiedades: conmutativa y asociativa).

## 1. EL PLAN (escrito antes de programar)

**La fuente.** La web de NCETM **no se puede abrir desde la nube** (el proxy la bloquea:
`EGRESS_BLOCKED www.ncetm.org.uk`; también thecorestandards.org e illustrativemathematics.org). Los
cinco puntos de enseñanza salen del índice de NCETM en el buscador (página
*primm-220-multiplication-with-three-factors-and-volume*). El resumen de NCETM: «usar la
multiplicación para calcular el volumen de cuboides y de figuras hechas de varios cuboides, usar la
**división** para los problemas inversos, y usar la asociativa y la conmutativa para resolver
multiplicaciones abstractas de **tres factores**». Falta leer el segmento entero (ejemplos y
representaciones) cuando Carlos pueda abrirlo en su PC.

1. **Punto 1:** «El volumen es la cantidad de espacio que ocupa algo».
2. **Punto 2:** «El volumen se mide en unidades cúbicas, como el centímetro cúbico (cm³) y el metro
   cúbico (m³)».
3. **Punto 3:** «El volumen de un cuboide se calcula multiplicando el largo, el ancho y el alto».
4. **Punto 4:** «La conmutativa y la asociativa se pueden usar al multiplicar tres números o más».
5. **Punto 5:** «El orden en que se multiplica se elige según la cuenta más sencilla».

Los errores típicos (investigación sobre contar cubos en un cuboide: Battista y Clements 1996;
Vasilyeva et al. 2013, *Math. Ed. Research Journal* 2021, s13394-021-00405-7):
- contar solo los cubos que **se ven** (las caras de fuera), y olvidar los de **dentro**;
- contar dos veces los de las aristas y las esquinas;
- contar **cuadrados** de las caras en vez de cubos (confundir el volumen con el área);
- **sumar** las medidas (5 + 3 + 2) en vez de multiplicarlas.

- Viene de M.0 (filas y columnas), G.1 (el área: cuadraditos = filas × columnas), M.2 (conmutativa con
  dos factores: `3 x 4 = 4 x 3`), M.10/M.11/M.12 (corta, rejilla, doblar y partir) y M.13 (un decimal
  por un entero). Prepara la 2.21 (factores, múltiplos, primos; los números cúbicos) y la 2.22
  (combinar operaciones).

**Cómo lo hace un humano sin calculadora (y así lo hará Euclides).**
- **Tres factores, el orden fácil (puntos 4 y 5).** 25 × 7 × 4: en el orden de siempre sería
  25 × 7 = 175 y 175 × 4 = 700 (dos cuentas difíciles). Un niño de 5.º **busca la pareja amiga**:
  25 × 4 = 100 (el que acaba en 5 con uno par da decenas justas), y 100 × 7 = 700 (M.9). Cambiar el
  orden es la conmutativa; juntar otra pareja primero es la asociativa. Si un factor ya son decenas
  justas (7 × 20 × 3), **se deja para el final**: 7 × 3 = 21, 21 × 20 = 420.
- **Si hay un cero**, el producto es cero sin hacer cuentas (no hay ningún grupo).
- **Si no hay pareja amiga**, en el orden de siempre, de izquierda a derecha.
- **Con un decimal** (lo de M.13): 0.25 × 7 × 4 → 0.25 × 4 = 1 (25 centésimas × 4 = 100 centésimas),
  1 × 7 = 7. Con dos decimales, todavía no (decimal por decimal es de 6.º).
- **Comprobar con la operación contraria** (lección de M.12): el producto se va **dividiendo** entre los
  factores, uno a uno, y tiene que quedar el último: 700 : 7 = 100, 100 : 4 = 25. Se divide entre los
  que se pueda (de una cifra, 10, 100…); entre el decimal no se divide (6.º).
- **El volumen (puntos 1–3).** Se cuentan **cubitos** de 1 cm de lado que caben dentro. Una **capa** del
  fondo es un rectángulo de largo × ancho cubitos (el área de G.1: filas × columnas); hay tantas capas
  como el alto: V = (l × a) × h (5.MD.C.5a, B × h). Y es multiplicar las tres medidas en el orden más
  fácil (punto 5): sale lo mismo. Se dice en **unidades cúbicas** (cm³, m³).
- **Los cubitos de dentro también cuentan.** En una caja de 3 × 3 × 3 se ven 26 desde fuera; dentro hay
  1 que no se ve: son 27. Euclides los cuenta: dentro hay (l − 2) × (a − 2) × (h − 2).
- **Figuras de varios cuboides**: se parte en cajas y se SUMAN los volúmenes (5.MD.C.5c).
- **El problema inverso** (NCETM: «usar la división»): volumen 60 con base 5 × 3 → la altura. Un humano
  deshace los factores uno a uno: 60 : 5 = 12, 12 : 3 = 4 (o 60 : 15 = 4 con la capa). Se comprueba
  multiplicando: 5 × 3 × 4 = 60.
- **La igualdad sin calcular (punto 4):** `2 x 3 x 4 = 4 x 2 x 3` es VERDADERO porque son los mismos
  factores en otro orden.

**Lo que se construye.**
- Pregunta nueva `multiplicar_tres` («la más rápida»; situación `{"factores": ["25", "7", "4"]}`, en
  texto para que entre un decimal).
- Pieza `tres_factores_con_un_cero` (rapidez 1): hay un cero → 0. **Vuelta:** 0 entre un factor que no
  sea cero da 0, y es el producto de los demás (que llevan el cero).
- Pieza `tres_factores_buscando_la_pareja_facil` (rapidez 5; puntos 4 y 5): busca la pareja que da
  decenas justas (uno acaba en 5, el otro es par) o deja las decenas justas para el final; cada cuenta
  de dos con la pregunta `multiplicar` (o `multiplicar_decimal`). **Vuelta:** dividir el producto entre
  los factores, uno a uno, con `dividir` / `dividir_decimal`; tiene que quedar el último factor.
- Pieza `tres_factores_en_orden` (rapidez 20): de izquierda a derecha. **Vuelta:** igual, dividiendo.
- Parte nueva `sistema/partes/volumen.py`:
  - `25 x 7 x 4` (y `calcular: ...`; tres factores o más): la pieza elegida, las otras cuentas posibles
    (**en el orden de siempre sale lo mismo**: la asociativa), la vuelta.
  - `volumen: caja 5 x 3 x 2` (con o sin cm / m), `volumen: cubo de 4`, `volumen: 5 x 3 x 2 + 4 x 4 x 1`:
    la capa (dibujada si es pequeña), las capas, la cuenta fácil, los cubitos de dentro, la unidad cúbica.
  - `volumen: 5 x 3 x ? = 60`: deshacer dividiendo, comprobar multiplicando; si no sale entero, se dice.
  - `verdad: 2 x 3 x 4 = 4 x 2 x 3` (sin calcular: los mismos factores) y `verdad: 2 x 3 x 4 = 6 x 4`
    (calculando los dos lados).
- **Todavía no:** dos decimales o más; medidas en unidades distintas (`2 m x 30 cm x 4 cm`: cambiar de
  unidad es de más adelante); productos que pasan del millón; la arista de un cubo dado su volumen
  (los números cúbicos son de la 2.21).

**Las trampas.**
- `2 x 3 x 4` hoy dice **«un_objeto»** (lo coge la unidad 0.1): contestar con seguridad algo falso. Debe dar 24.
- `25 x 7 x 4` → 700, por la pareja 25 × 4 = 100 (no 175 × 4).
- `volumen: caja 5 x 3 x 2` → 30 cm³, **no 10** (sumar las medidas), **ni 31** (5·3 + 3·2 + 5·2 = área de
  caras), ni contar solo los de fuera.
- `volumen: cubo de 3` → 27, no 26 (el de dentro también cuenta).
- `volumen: caja 2 m x 30 cm x 4 cm` → todavía no (la misma unidad).
- `volumen: 5 x 3 x ? = 62` → no sale entero.
- `0.25 x 7 x 4` → 7; `0.3 x 0.2 x 5` → todavía no (dos decimales).
- `5 x 0 x 999` → 0 sin cuentas.
- `100 x 100 x 100` → 1000000 (el techo); `100 x 100 x 101` → todavía no.
- `verdad: 2 x 3 x 4 = 4 x 3 x 2` → VERDADERO sin calcular; `verdad: 2 x 3 x 4 = 2 x 3 x 5` → FALSO.

**Prueba de dominio.** Contra el testigo (Python, solo en la prueba): todos los tríos de 0 a 12 (2197
productos, en muestra), una muestra de tríos con números de dos y tres cifras, los mismos factores en
los 6 órdenes dan lo mismo, tríos con un decimal (una, dos y tres cifras decimales), volúmenes de cajas,
cubos y figuras compuestas, problemas inversos (exactos y que no salen), igualdades. Cerca del techo:
100 × 100 × 100, 999 × 1000 × 1, 125 × 8 × 1000; cada pregunta en menos de 2 s.

## RESULTADO (7 oct)

**Hecho, verde: proyecto 2380/2380 + 671/671.** `test_M14_tres_factores_volumen` 66/66; mis_casos 671/671;
mis_pruebas 181/181.

- Pregunta nueva `multiplicar_tres` y 3 piezas, sin tocar el motor de piezas. **Las tres se comprueban con la
  operación contraria** y `aplicar` las descarta si no cuadra (la prueba B le da 701 en vez de 700 y la vuelta lo caza):
  - `tres_factores_buscando_la_pareja_facil` (rapidez 5; puntos 4 y 5): primero la pareja amiga (uno acaba en 5 y el
    otro es par: 25 x 4 = 100), si no las decenas justas al final (7 x 3 = 21, 21 x 20), y con un decimal, el decimal
    con cada entero de una cifra (6 x 8 x 0.37 → 0.37 x 6 = 2.22, 2.22 x 8 = 17.76; no 48 x 0.37). Cada cuenta de
    dos la hacen `multiplicar` o `multiplicar_decimal` (M.13).
  - `tres_factores_en_orden` (rapidez 20): de izquierda a derecha.
  - `tres_factores_con_un_cero` (rapidez 1): 5 x 0 x 999 = 0 sin cuentas; vuelta 0 : 5 = 0 y los demás dan 0.
  - **La vuelta**: el producto se divide entre los factores uno a uno (700 : 7 = 100, 100 : 4 = 25 → queda el 25).
    Si un orden de división se atasca, se prueba otro (1.125 x 8 x 111 = 999: 999 : 111 = 9, 9 : 8 = 1.125). Entre el
    decimal no se divide (6.º). Si ninguna división se puede (13 x 17 x 19: 4199 : 13 es la división larga), **todavía
    no**: sin comprobar no se da por bueno.
- Parte nueva `sistema/partes/volumen.py`: `25 x 7 x 4` (y `calcular:`; tres factores o más) enseña la pareja, que
  **en el orden de siempre sale lo mismo** (25 x 7 = 175, 175 x 4 = 700) y la vuelta. `volumen: caja 5 x 3 x 2 cm`,
  `volumen: cubo de 3`: la capa de abajo (dibujada; el área de G.1), las capas, las tres medidas en el orden fácil,
  **los cubitos de dentro** (cubo de 3: dentro 1, se ven 26, son 27), «no es sumar las medidas», la unidad cúbica.
  `volumen: 5 x 3 x 2 + 4 x 4 x 1` suma cajas. `volumen: 5 x 3 x ? = 60`: deshacer dividiendo (60 : 5 = 12,
  12 : 3 = 4) y comprobar multiplicando; si sale con decimales hasta las milésimas, vale (`5 x ? x 2 = 62` → 6.2);
  si no, `no_sale`. `verdad: 2 x 3 x 4 = 4 x 3 x 2` sin calcular (los mismos factores); con otros factores calcula.
- **La trampa de antes**: `2 x 3 x 4` decía `un_objeto` (lo cogía la unidad 0.1). Ahora 24.
- **Dos arreglos encontrados al medir el tiempo** (lección de M.12):
  - `1000000 : 2` tardaba **15 s** (también en el PC de Carlos): `dividir_a_la_mitad` contaba 500 000 parejas. Ahora,
    con más de cien, parte **por sitios** (la mitad de cada cifra, cambiando lo que sobra por diez de la de al lado)
    y se comprueba doblando (499999 + 499999 + 1 = 999999). 0.00 s.
  - `1000000 : 8` con la memoria vacía tardaba 15 s: `dividir_saltando` daba 125 000 saltos de 8. Ahora no salta más
    de mil veces y dice que eso es la división corta, que pide saberse la tabla. La prueba F1 de N.4
    (`100000 : 4` con memoria vacía) solo pasaba por los 25 000 saltos: ahora aprende las tablas antes (el caso viejo,
    escrito al lado) y comprueba que lo hace la división corta.
- Dominio contra el testigo: 1575 tríos de 0 a 12 (todos los que tienen 0, 1, 10, 12 o repetidos + 300 al azar; con
  la memoria vacía, 2.2 s); 44 tríos en sus 6 órdenes; 160 tríos de dos y tres cifras (143 salen, 17 «todavía no» por
  el millón o la división larga, ninguno falso; lo más lento 0.30 s); 120 con un decimal de 1, 2 y 3 cifras (112
  salen, ninguno falso); 40 cajas, los 12 cubos, 20 figuras de dos cajas, 80 problemas inversos, 90 igualdades.
  Cerca del techo: 100 x 100 x 100 = 1 000 000, 125 x 8 x 1000, cubo de 100 cm; 100 x 100 x 101 y cubo de 101 → todavía no.
- Todavía no (con su porqué): dos decimales; un decimal por decenas justas que no sean 10 o 100 (`0.5 x 7 x 20`: M.13
  multiplica un decimal por un entero de una cifra); unidades distintas; la vuelta que pide la división larga
  (`999 x 999 x 1`, `13 x 17 x 19`); la arista de un cubo dado su volumen (2.21).
- **Falta la prueba de Carlos.** Y leer el segmento entero de NCETM 2.20 cuando se pueda abrir (desde la nube la web
  está bloqueada): si trae ejemplos o trampas que aquí no están, se añaden.
