# Paso N.3 — EL 1000 Y LOS NÚMEROS DE CUATRO CIFRAS — 6 oct 2026 (noche)

Primer paso de **4.º**. Es la respuesta a la pregunta de Carlos («¿qué pasa con los números de más de
mil?»): en NCETM les toca en Year 4 (segmento 1.22, hasta 10 000); en 5.º hasta un millón (1.26).

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (NCETM 1.22, leído el 6 oct; Common Core 4.NBT.A.1–3).**
1. «**Diez centenas hacen 1000**, que también se descompone en 100 decenas y 1000 unidades.»
2. «Al sumar o restar múltiplos de 100, el resultado es siempre un múltiplo de 100» (300 + 800 = 11
   centenas = 1100: *unitising*, como 3 + 8 = 11).
3. «Los números de más de mil tienen una **estructura** que va con su tamaño: por eso se pueden
   **ordenar, componer y descomponer**.»
4. «Los números se pueden **redondear** para simplificar cuentas o dar un tamaño aproximado.»
5. «Lo aprendido para tres cifras **sirve igual para cuatro**» (las columnas).
6. «1000 también se compone multiplicando: 2 × 500, 4 × 250, 5 × 200.»
- Common Core **4.NBT.A.2**: leer y escribir con cifras, con nombres y en forma desarrollada
  (3456 = 3000 + 400 + 50 + 6); **comparar dos números de varias cifras mirando las cifras de cada
  sitio** (<, =, >). **4.NBT.A.3**: redondear a cualquier sitio.
- Los errores documentados (como la REGLA 4 de la centena): el **cero** como marcador de sitio —
  «dos mil cinco» se escribe 2005, no 20005 ni 205; en 3045 hay 30 centenas aunque la cifra de las
  centenas sea 0.

**Cómo, sin calculadora (como un humano).** Igual que la 6.7 subió el techo de 100 a 1000: los nombres
de cuatro cifras **se construyen con la regla** («dos mil» + el nombre de lo que queda, «trescientos
cuarenta y cinco»; 1000 es «mil», no «un mil»), y la lista de contar llega a **diez mil**. Todo lo que
ya sabe (contar, las columnas, las tablas, redondear, estimar) sigue igual: solo es más larga la lista.
Y lo nuevo de este paso es lo que pide la estructura: **comparar por las cifras**, descomponer, el millar.

**Lo que se construye.**
- `conocimiento/el_millar.kn` (las reglas fijadas: 10 centenas = 1 millar; los cuatro sitios; los
  nombres; el cero; el techo en diez mil).
- La lista de contar hasta 10 000, construida con la regla (en el mismo punto que la 6.7).
- `millar: 3045` → 3 millares, 0 centenas, 4 decenas y 5 unidades; 3000 + 40 + 5; **30 centenas, 304
  decenas**; su nombre. Para 1000: 10 centenas = 100 decenas = 1000 unidades; 2 × 500, 4 × 250, 5 × 200.
- `comparar: 3456 y 3465` → por las cifras, de izquierda a derecha (más cifras gana; si no, la primera
  cifra distinta manda), comprobado con el orden de la lista.
- `redondear: 3456` → también **al millar**; `de 1000 en 1000`.
- Las columnas y estimar con cuatro cifras (lo que ya había, con la lista larga).

**Las trampas.**
- `nombre: 2005` → «dos mil cinco».  `numero: dos mil cinco` → 2005 (no 20005).  `nombre: 1000` → «mil».
- `millar: 3045` → 30 centenas (la cifra de las centenas es 0, pero hay 30).
- `comparar: 999 y 1000` → 1000 (más cifras).  `comparar: 3456 y 3465` → 3465 (decide la de las decenas).
- `comparar: 4999 y 5001` → 5001 (decide la primera: el millar).
- `redondear: 3456 al millar` → 3000;  `3500` → 4000 (mitad);  `9500` → 10 000.
- `columnas: 2345 + 1678` → 4023.   `300 + 800` → 1100.   `nombre: 10001` → todavía no (5.º).

**Prueba de dominio.** Nombres y números de 0 a 10 000 (muestra) ida y vuelta; comparar por cifras
contra el testigo; redondear al millar; columnas con cuatro cifras; y todo lo anterior sigue verde.

**Para Carlos:** `nombre: 2005`, `millar: 3045`, `comparar: 3456 y 3465`, `redondear: 3456`,
`de 1000 en 1000`, `columnas: 2345 + 1678`.

## 2. LO QUE SE HIZO
- `conocimiento/el_millar.kn` (7 reglas fijadas: 10 centenas = 1 millar; los cuatro sitios; los nombres
  con «mil»; el cero que marca el sitio; comparar por las cifras; lo de tres cifras sirve para cuatro; el
  techo en diez mil).
- Parte nueva `sistema/partes/millar.py`: `construir_nombre_hasta_diez_mil` (delega en la 6.7 hasta mil)
  y la lista de contar **hasta diez mil**, construida con la regla en el mismo punto que la 6.7
  (`nucleo.py`). Todo lo que ya sabía (contar, columnas, tablas, redondear, estimar, problemas) llega
  ahora a diez mil sin tocarlo.
- `millar: 3045` (cada cifra y su valor; 3000 + 40 + 5; **cuántas hay de cada**: 30 centenas, 304
  decenas; el OJO del cero; para 1000, las tres descomposiciones y 2 × 500, 4 × 250, 5 × 200).
- `comparar: 3456 y 3465` **por las cifras** (más cifras gana; si no, la primera distinta de izquierda a
  derecha), comprobado con el orden de la lista.
- `nombre:` explica cómo se construye el de cuatro cifras («el millar 'dos mil' + 'cinco'»).
- Redondear **al millar** (4.NBT.A.3) en las dos piezas; `redondear: 3456` da los tres sitios; estimar
  redondea al millar los de cuatro cifras.
- `de 1000 en 1000` (el mecanismo escribe la cifra de los millares).
- Piezas nuevas `sumar_centenas_justas` y `restar_centenas_justas` (NCETM 1.22, punto 2): 300 + 800 = 3
  centenas + 8 centenas = 11 centenas = 1100.
- **El techo, en un solo sitio**: `techo(saber)` = la última palabra de la lista; los mensajes de «no me
  alcanza» la dicen de ahí (antes «mil» estaba escrito a mano en 15 sitios).
- **Las pruebas que fijaban el techo en mil** (25 archivos y 16 líneas de `mis_casos.txt`, una de
  `mis_pruebas.txt`) se movieron a diez mil, como se hizo en la 6.7 al pasar de cien a mil: la trampa
  sigue (mismo sentido), cambia el número. `test_2_4` recorre hasta mil y las fronteras de mil a diez mil
  (si no, tardaba 47 s).
- `pruebas/test_N3_el_millar.py` (21 afirmaciones: trampas; **los 10 000 nombres** contra un testigo
  escrito aparte; comparar 336 parejas; descomponer, redondear al millar, sumar y restar de cuatro cifras
  en muestras). Ayuda, `mis_pruebas.txt` (5), `mis_casos.txt` (9).

## 3. RESULTADO
- `nombre: 2005` → dos mil cinco.  `millar: 3045` → 30 centenas.  `comparar: 4999 y 5001` → «la primera
  distinta es la de los millares».  `300 + 800` → 11 centenas = 1100.  `redondear: 9500 al millar` → 10000.
- Proyecto: **1993/1993 afirmaciones + 565/565 casos — VERDE** (62 s).

## 4. PENDIENTE: la prueba de Carlos (mañana).  Sigue M.7: tablas del 11 y del 12 (NCETM 2.11).
