# Paso N.4 — HASTA UN MILLÓN: LA ESTRUCTURA DE LOS MILES — 7 oct 2026 (madrugada)

Primer paso de **5.º**. NCETM Spine 1, Year 5 (segmento 1.26).

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (NCETM 1.26, leído el 7 oct; Common Core 4.NBT.A, 5.NBT.A).**
1. «Los números hechos de **centenas de mil, decenas de mil y unidades de mil** se entienden enlazándolos
   con los hechos de **centenas, decenas y unidades**» — 345 000 son **345 mil**: el MIL se cuenta como
   una cosa (unitising), igual que la decena (6.2), la centena (6.7) y el millar (N.3).
2. «Los múltiplos de 1000 hasta 1 000 000 se ponen en la recta numérica usando lo que se sabe de la recta
   hasta 1000.»
3. «Se ordenan y comparan por su composición y su lugar en la recta.»
4. «**Lo que sirve para calcular hasta 1000 sirve para los múltiplos de 1000 hasta un millón**»:
   345 mil + 278 mil = (345 + 278) mil = 623 mil.
5. «Se redondean para simplificar cuentas o dar un tamaño aproximado.»
6. «Patrones conocidos sirven para dividir 10 000 y 100 000 en 2, 4 y 5 partes» (100 mil : 4 = 25 mil).

**Cómo, sin calculadora (y sin recitar un millón de palabras).** Una persona no cuenta hasta un millón:
**lee la estructura**. La lista de contar se queda en diez mil (contar cosas una a una llega hasta ahí);
los números más grandes se **construyen por grupos de tres cifras** («trescientos cuarenta y cinco mil
seiscientos setenta y ocho» = el nombre de 345 + «mil» + el nombre de 678), se **leen** al revés, el
**siguiente** se escribe subiendo la cifra de las unidades (como en el cuentakilómetros), y se
**comparan** por las cifras (N.3). Así, todo lo que ya calcula por columnas y con las piezas llega al
millón sin contar paso a paso. El techo nuevo está en `conocimiento/el_millon.kn`.
- Ojo con los nombres (el castellano): 1000 es «mil», pero 21 000 es «veintiún mil» y 101 000 «ciento un
  mil» (el «uno» delante de «mil» se apocopa); 1 000 000 es «un millón».

**Lo que se construye.**
- `conocimiento/el_millon.kn` (las reglas: los miles como cosas; los nombres por periodos; el techo).
- En el mecanismo (`mecanismo.py`): `decir`, `leer`, `siguiente`, `anterior` y `viene_despues` saben de
  números más allá de la lista, **por la estructura** (sin calculadora: cifras que se leen y escriben).
- `nombre: 345678`, `numero: …`, `millar: 345678` (cada cifra en su sitio, hasta las centenas de mil;
  y **345 mil**), `comparar: 345678 y 354678`, `redondear: 345678` (a la decena de mil, a la centena de mil).
- `345000 + 278000` → «345 mil + 278 mil = 623 mil» (pieza de miles justos, como las centenas justas).
- `100000 : 4` → 25 mil (100 mil : 4).
- Las pruebas que fijaban el techo de las **cuentas** en diez mil pasan a un millón; las de **contar
  cosas** (escenas) se quedan en diez mil.

**Las trampas.**
- `nombre: 21000` → veintiún mil (no «veintiuno mil»);  `nombre: 101000` → ciento un mil;
  `nombre: 1000000` → un millón;  `nombre: 345678` → trescientos cuarenta y cinco mil seiscientos setenta y ocho.
- `numero: doscientos mil cinco` → 200005 (no 2005 ni 2000005).
- `comparar: 99999 y 100000` → 100000 (más cifras).
- `345000 + 278000` → 623000;  `600000 + 500000` → se pasa de un millón.
- `redondear: 345678 a la centena de mil` → 300000.

**Prueba de dominio.** Nombres ida y vuelta en una muestra hasta un millón contra un testigo escrito
aparte; siguiente/anterior por las fronteras (9999 → 10000, 99999 → 100000); comparar; sumas y restas
grandes por columnas; miles justos; redondeos.

**Para Carlos:** `nombre: 345678`, `nombre: 21000`, `345000 + 278000`, `comparar: 99999 y 100000`,
`redondear: 345678`.

## RESULTADO (7 oct, madrugada)

**Hecho, verde: proyecto 2197/2197 + 631/631; mis_pruebas 161/161.**

**Los dos techos (la decisión importante).**
- **Contar objetos** (escenas, montones, la lista de contar) se queda en **diez mil**: nadie cuenta un
  millón de piedras una a una. `techo_de_contar(saber)` = la última palabra de la lista.
- **Los números** (leer, escribir, comparar, calcular) llegan a **un millón**: `numero_maximo(saber)`
  (de `el_millon.kn`). Más allá del millón, «no me lo invento» (`nombre: 1000001` → fuera_de_mi_secuencia).

**Cómo lo hace sin calculadora.** `decir`/`leer` van por **grupos de tres** (el castellano: «345 mil 678»),
con el apócope («veintiún mil», «ciento un mil»). `siguiente`/`anterior` suben o bajan **la cifra de un
sitio** y pasan los nueves a cero (como en el cuentakilómetros): 99 999 → 100 000. `viene_despues`
compara cifras (más cifras gana; si no, la primera distinta).

**Lo que salió al subir el techo (y se arregló).**
- La **división corta** se comía la sexta cifra (100000 : 4 daba 2500): las tablas de nombres de sitio
  llegaban a los millares. Se alargaron a las centenas de millar en todas las partes que las tenían.
  Y una regla nueva en el motor de piezas: **si la comprobación de una pieza no cuadra, su respuesta no
  vale** (`vuelta_ok` falso → no salió). Así un fallo así ya no puede colarse.
- **Lentitud**: 99999 x 100 tardaba 80 s porque «grupos iguales» sumaba 99 999 veces. Un humano no
  hace eso: ahora grupos iguales solo se usa con **doce grupos o menos** (en una de las dos lecturas),
  y partir (la distributiva) solo parte números de dos cifras.
- Eso dejó sin camino a **18 x 38** (dos cifras por dos cifras). Common Core 4.NBT.B.5 lo pide en 4.º
  «con estrategias de valor posicional… modelos de área». Pieza nueva **la rejilla**
  (`multiplicar_en_rejilla`): se parten los dos por sitios y cada casilla es un hecho de la tabla con
  las cifras subidas de sitio: 300 + 80 + 240 + 64 = 684.
- **Los dedos** (7.1) con un primer número grande: ahora lo leen por su estructura y cuentan hacia
  adelante cruzando la frontera (99 998 + 4 = cien mil dos).
- Las pruebas que fijaban «más de diez mil no» en CUENTAS se movieron a «más de un millón no».
- La batería completa ahora corre **en paralelo** (2 procesos): 52 s.

**Prueba de dominio** `test_N4_hasta_un_millon` 41/41: nombres ida y vuelta en 316 números (fronteras +
azar) contra un testigo escrito aparte; siguiente/anterior por 4 fronteras; 60 comparaciones; 40 sumas y
40 restas por columnas; miles justos; 30 productos de dos cifras por la rejilla; redondeos.
