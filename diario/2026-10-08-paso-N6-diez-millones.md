# Paso N.6 — HASTA DIEZ MILLONES: LOS MILLONES COMO COSAS — 8 oct 2026

Primer paso de **6.º** (Year 6). Es el segmento **1.30** de NCETM (Spine 1): *Composition and calculation: numbers up
to 10,000,000*. Se llama **N.6** porque sigue la serie de los números (N.3 el millar, N.4 hasta un millón, N.5 los
negativos). Viene de N.4 (NCETM 1.26: los miles como cosas, hasta un millón).

## 1. EL PLAN (escrito antes de programar)

**La fuente.** La web de NCETM **sigue sin poder abrirse desde la nube** (`EGRESS_BLOCKED www.ncetm.org.uk`, probado hoy
con `primm-130-composition-and-calculation-numbers-up-to-10000000`). Lo que sigue sale del **buscador** (el resumen
de la página del segmento y de la unidad de Year 6 «Numbers up to 10,000,000» de NCETM) y del currículo inglés de
Year 6 («leer, escribir, ordenar y comparar números hasta 10 000 000 y saber el valor de cada cifra; redondear
cualquier número entero a la precisión pedida»). **Falta leer el segmento entero** (diapositivas, ejemplos) cuando
Carlos pueda abrirlo.

El segmento (según el buscador): parte de los números de seis cifras que **no** son miles justos y sube a los de
**siete cifras**; suma, resta y redondeo con ellos. Los **seis puntos de enseñanza** (traducidos):
1. **Los patrones de las otras potencias de diez se alargan a la unidad 1 000 000** (diez de cien mil son un millón,
   como diez centenas son mil; y diez millones).
2. **Los números de siete cifras se escriben, se leen y se ordenan viendo cuántos millones, cuántos miles y cuántas
   centenas, decenas y unidades tienen.**
3. **Las cifras dicen la estructura**: se componen y se descomponen.
4. **Lo que se sabe de cruzar los miles sirve para llegar a los millones y cruzarlos.**
5. **A veces se redondea** (para quitar un detalle que sobra, para estimar o dar una media); **otras veces importa el
   número exacto.**
6. **Calcular con soltura** es poder pasar del cálculo mental al escrito según los números de la cuenta.

La unidad de Year 6 añade: leer bien los de siete cifras, **comparar** los de hasta ocho, **redondear al millón y a la
centena de millar**.

**Cómo, sin calculadora (y sin recitar diez millones de palabras).** Igual que en N.4: nadie cuenta hasta diez
millones; **lee la estructura**. El castellano agrupa de tres en tres, como el inglés: 2 345 678 =
«(dos) MILLONES (trescientos cuarenta y cinco) MIL (seiscientos setenta y ocho)». El millón se cuenta como UNA cosa
(como la decena, la centena, el mil): **2 millones + 3 millones = 5 millones**. El siguiente se escribe subiendo la
cifra de las unidades (cuentakilómetros); comparar es mirar las cifras (más cifras, mayor; si no, la primera
distinta). Todo lo que ya calcula por columnas y con las piezas llega solo a diez millones.
- Ojo con los nombres: 1 000 000 es «un millón» (no «uno millón»), 2 000 000 «dos millones» (plural);
  1 021 000 «un millón veintiún mil»; 10 000 000 «diez millones».
- **Cruzar el millón (punto 4)** como se cruza el mil y la decena («hacer diez»): un humano que suma 997 000 + 5 000
  no hace columnas: **completa el millón** (a 997 000 le faltan 3 000; de los 5 000 quedan 2 000) → 1 002 000.
  Lo que le falta a un número para el millón se saca **por las cifras**: cada cifra hasta nueve y la última que no
  es cero hasta diez (997 000 → 0 0 3 0 0 0 = 3 000), como los «complementos a mil» de 1.22. Para restar,
  **cuenta hacia arriba pasando por el millón**: 1 002 000 − 997 000 = 3 000 (hasta el millón) + 2 000 = 5 000.
- **Punto 6 (mental o escrito según los números)**: es lo que ya hace el motor de piezas (la técnica más corta que
  encaja): 997 000 + 5 000 se hace de cabeza (pasando por el millón); 2 345 678 + 1 234 567, por columnas.
  `calcular:` enseña las dos y cuál se elige.

**Lo que se construye.**
- `conocimiento/los_millones.kn` (las reglas: el millón como cosa; los nombres por grupos de tres con «millón /
  millones»; cruzar el millón; el techo de 6.º, **diez millones**). `numero_maximo` lee el techo más alto que haya.
- En el mecanismo (`mecanismo.py`): `decir` y `leer` (y por tanto `siguiente`, `anterior`, `viene_despues`) saben de
  los millones **por la estructura**. «millón» con tilde también se lee.
- Las tablas de los sitios (millar, columnas, multiplicación corta, división corta, redondear, saltar) llegan a
  los **millones** y las **decenas de millón**.
- `millar: 2345678` → cada cifra en su sitio, **2 millones, 345 mil y 678**; `millar: 1000000` → los patrones
  (10 centenas de millar = 100 decenas de millar = 1000 millares = un millón; y 10 millones son diez millones).
- `redondear: 2345678` → también al millar, a la decena de millar, a la **centena de millar** y **al millón**.
- `de 100000 en 100000 desde 700000` cruza el millón; `de 1000000 en 1000000`.
- Piezas nuevas, **con su vuelta real** (la operación contraria por columnas):
  - `sumar_pasando_por_el_millon` (sumar, rapidez 4): el primero está cerca de un millón justo (le faltan menos de
    cien mil), el segundo es menor que un millón y la suma lo cruza: completar el millón y seguir. Vuelta: restar.
  - `restar_pasando_por_el_millon` (restar, rapidez 4): el de abajo está justo debajo de un millón justo y el de
    arriba justo encima (los millones se llevan uno): contar hacia arriba hasta el millón y desde el millón.
    Vuelta: sumar.
  - `sumar_miles_justos` y `restar_miles_justos` llegan solos a diez millones y dicen también los millones
    (2 500 000 + 1 750 000 = 2500 mil + 1750 mil = 4250 mil).
- Los mensajes que decían «un millón» escrito a mano dicen el techo de verdad (`techo(saber)`).
- Las pruebas que fijaban «más de un millón no» en las CUENTAS pasan a «más de diez millones no» (caso por caso,
  dejando escrito el viejo al lado). Contar OBJETOS sigue en diez mil.

**Las trampas.**
- `nombre: 1000000` → un millón; `nombre: 2000000` → dos millones (no «dos millón»); `nombre: 1021000` → un millón
  veintiún mil; `nombre: 10000000` → diez millones; `nombre: 10000001` → no me lo invento (se pasa del techo).
- `numero: dos millones cinco` → 2000005 (no 25 ni 2005); `numero: un millón mil` → 1001000.
- `comparar: 999999 y 1000000` → 1000000 (más cifras aunque tenga ceros); `comparar: 2345678 y 2354678`.
- `997000 + 5000` → 1002000 (no 1 000 200 ni 902 000); `1002000 - 997000` → 5000.
- `9999999 + 1` → 10000000; `9999999 + 2` → se pasa de diez millones.
- `redondear: 2549999 al millon` → 3 000 000 (la cifra de las centenas de millar es 5: sube).
  `redondear: 2499999 al millon` → 2 000 000, **no** 3 000 000: manda la cifra de justo a la derecha (4), no los
  nueves de después (la trampa de la cadena: 2 499 999 → 2 500 000 → 3 000 000 está mal).
- `millar: 1030405` → 1 millón, 30 mil, 405; la cifra de las centenas de millar es 0 pero hay 10 centenas de millar.

**Prueba de dominio** (`pruebas/test_N6_diez_millones.py`). Nombres ida y vuelta en una muestra hasta diez millones
(fronteras + azar fijo) contra un testigo escrito aparte; siguiente/anterior por las fronteras del millón;
comparaciones; sumas y restas de siete cifras por columnas; las dos piezas de pasar por el millón contra el testigo
(con sus vueltas y piezas trucadas que no deben colarse); millones justos; redondeos al millón y a la centena de
millar; multiplicación y división corta con siete cifras; cerca del techo (9 999 999, 10 000 000, lo que se pasa).
**El tiempo**: cada pregunta grande por debajo de 2-3 s; la batería entera, que no se alargue.

**Para Carlos:** `nombre: 2345678`, `millar: 1030405`, `997000 + 5000`, `1002000 - 997000`,
`redondear: 2549999`, `comparar: 999999 y 1000000`.

## RESULTADO (8 oct 2026)

**Hecho, verde: proyecto 2994/2994 + 799/799 (antes 2907 + 770); mis_pruebas 226/226; `test_N6` 75/75.**

**Lo que se construyó.**
- `conocimiento/los_millones.kn`: las 7 reglas (los patrones de las potencias de diez, los nombres con «millón /
  millones», la estructura, cruzar el millón, redondear o no, mental o escrito, el techo). `numero_maximo` toma el
  techo más alto de los `.kn` de la escalera: **diez millones**. Contar OBJETOS sigue en diez mil.
- **El mecanismo** (`mecanismo.py`): `decir`/`leer` por grupos de tres con los millones (un millón / dos millones;
  el grupo de ceros no se dice; «millón» con tilde también se lee); `siguiente`, `anterior` y `viene_despues` llegan
  solos, porque ya iban por las cifras. Nuevo: **`lo_que_falta_para_el_redondo`** (por las cifras: cada una hasta
  nueve, la última hasta diez; 997 000 → 3 000), una cuenta de dedos por cifra; se le da a las piezas en `u`.
- **Dos piezas nuevas, con su vuelta real** (rapidez 2: cuando se está a un paso del millón, se completa):
  - `sumar_pasando_por_el_millon`: 997 000 + 5 000 → le faltan 3 000; de los 5 000 quedan 2 000 (restando);
    1 000 000 y 2 000 = 1 002 000 (se ESCRIBE). Vuelta: 1 002 000 − 5 000 = 997 000 y el hueco 997 000 + 3 000 =
    1 000 000. Sirve en cualquier millón justo (2 997 000 + 5 000 = 3 002 000; 9 999 999 + 1 = 10 000 000).
  - `restar_pasando_por_el_millon`: 1 002 000 − 997 000 → 3 000 hasta el millón + 2 000 desde él = 5 000.
    Vuelta: 997 000 + 5 000 por columnas. (Suma con el mecanismo, no con la pregunta `sumar`: si no, habría una
    vuelta en el mapa —sumar usaría restar y restar usaría sumar—; la caza `test_piezas A3`.)
  - Probadas con piezas trucadas (lo que falta dando uno de más, la resta dando uno de más, las columnas dando uno
    de más): la vuelta lo caza siempre.
- `sumar_miles_justos` y `restar_miles_justos` cuentan **millones** si los dos son millones justos
  (2 millones + 3 millones = 5 millones; 9 millones − 1 millón = 8 millones).
- Las tablas de los sitios llegan a las **unidades y decenas de millón** (millar, columnas, multiplicación por
  sitios, por 10 y 100, división corta, decimales). `millar:` dice los millones, cuántas centenas de millar hay y,
  con 1 000 000 y 10 000 000, los patrones de las potencias de diez. `nombre:` explica el grupo de los millones.
- `redondear:` **al millón** (las dos piezas, la recta y el atajo) y avisa de **la trampa de la cadena** también
  ahí (2 499 999 → 2 500 000 → 3 000 000 está mal). `de 1000000 en 1000000`.
- Los mensajes con «un millón» escrito a mano dicen el techo de verdad (`techo(saber)`), y «se pasa del millón»
  pasó a «se pasa del techo» (parte_todo y combinar lo leen).

**Lo que salió al subir el techo (y se arregló).**
- **Contar de uno en uno, otra vez**: `10000000 - 3997` tardaba 0,7 s (y la orden `equivalente:` 1,4 s) porque
  `restar_centenas_justas` contaba 100 000 − 40 centenas de una en una (99 960 pasos). Lo mismo le pasaba a
  `restar_miles_justos` con 9 000 000 − 4 000. Condición nueva en las dos: se cuentan «cosas» solo si son de **tres
  cifras o menos** (NCETM 1.26: «lo que sirve hasta 1000»), o millones justos. Ahora: 0,03 s.
- **Un fallo viejo** que salía con el techo: en las columnas el total de más de diez mil se decía «None» en
  palabras (`_nombre_o_cero` solo construía hasta diez mil). Arreglado.
- El castellano: «COLUMNA DE LAS MILLONES» → «DE LAS UNIDADES DE MILLÓN»; «en las millares» → «en los millares»;
  «la cifra de las millares» → «de los millares» (estos dos eran viejos).
- 30 pruebas y 13 casos fijaban «más de un millón no»: obsoletos por mejora. Cada uno se cambió **con el caso viejo
  escrito al lado** y su equivalente en diez millones (p. ej. `600000 + 500000` → ahora 1 100 000; se pasa
  `6000000 + 5000000`). Comprobadas las respuestas nuevas contra el testigo (4000 x 300 = 1 200 000, 123 456 x 9 =
  1 111 104, 2943.4 : 8 = 367.925, …).

**Prueba de dominio** `test_N6_diez_millones` 75/75: 415 nombres ida y vuelta contra un testigo escrito aparte;
siguiente/anterior por 4 fronteras del millón; saltos que cruzan el millón; la estructura y los patrones;
60 comparaciones; 40 sumas y 40 restas de siete cifras por columnas; millones justos; 60 sumas y 60 restas que
cruzan un millón (todas por las piezas nuevas, todas bien); las piezas trucadas; 200 «lo que falta» contra el
testigo; 120 redondeos al millón y a la centena de millar; 30 productos y 30 divisiones cortas de siete cifras;
y el tiempo.

**El tiempo.** 19 preguntas grandes (9 999 999 + 1, 10 000 000 − 3 997, 9 999 999 : 13, redondear: 9 999 999,
multiplos de 999 999, `equivalente: 10000000 - 3997`…): todas por debajo de 0,1 s. La más lenta del proyecto que
cambió es `999 x 1000 x 1` (M.14) con 0,48 s. La batería: **139 s** (antes 130 s): los casos nuevos y 17 tríos de
M.14 que antes eran «se pasa del millón» y ahora se calculan y se comprueban dividiendo.

**Lo que queda (no es de este paso).**
- `factores de` y `es primo` con números de siete cifras siguen en «todavía no» (lo de M.15, que llega hasta donde
  probar parejas es humano). `mitad:` de números grandes, igual que antes.
- Los pendientes de M.14 siguen: `100 x 100 x 1001` dice «todavía no» y debería decir que se pasa de diez millones.
- Las piezas de redondear siguen con `"vuelta_ok": True` sin comprobar nada (son viejas: se comprueban la una con
  la otra, porque la pregunta es «todas iguales»).
- **Falta la prueba de Carlos.** Y leer el segmento entero de NCETM 1.30 cuando se pueda abrir.
