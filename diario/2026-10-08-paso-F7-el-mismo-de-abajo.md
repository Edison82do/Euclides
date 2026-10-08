# Paso F.7 — EL MISMO DE ABAJO: SUMAR, RESTAR Y COMPARAR FRACCIONES CON DISTINTO DE ABAJO — 8 oct 2026

Sigue al F.6. Es el segmento **3.8** de NCETM (Spine 3, Year 5): *Common denomination: more adding and subtracting*.
Se llama **F.7** porque sigue la serie de las fracciones (F.1 … F.6). En Common Core: **5.NF.A.1** (sumar y restar
fracciones con distinto denominador, también números mixtos, cambiándolas por equivalentes con el mismo denominador) y
**5.NF.A.2** (comprobar si una respuesta es razonable con fracciones de referencia: «2/5 + 1/2 = 3/7 está mal porque
3/7 < 1/2»).

## 1. EL PLAN (escrito antes de programar)

**La fuente.** La web de NCETM **sigue sin poder abrirse desde la nube** (`EGRESS_BLOCKED www.ncetm.org.uk`, probado hoy
con la página del segmento `primm-308-common-denomination-more-adding-and-subtracting`; Oak National Academy también está
bloqueada). Lo que sigue sale del **buscador** (el resumen de la página del segmento) y del texto de Common Core 5.NF.A.1–2.
**Falta leer el segmento entero** (las diapositivas, los ejemplos, las preguntas de práctica) cuando Carlos pueda abrirlo.

La introducción del segmento (según el buscador): los alumnos aprenden a **sumar y restar fracciones con distinto
denominador encontrando primero un denominador común**, y a **comparar fracciones con varios métodos**, entre ellos
pasarlas a un denominador común. Los **cinco puntos de enseñanza** (resumidos por el buscador, traducidos):
1. **Sumar fracciones relacionadas** (un denominador es múltiplo del otro: 1/2 y 1/4): el primer paso es **cambiar una**
   de las dos para que tengan el mismo de abajo, el «denominador común».
2. **Restar fracciones relacionadas**: el mismo primer paso.
3. **Lo mismo con fracciones no unitarias** relacionadas (3/4 + 5/8).
4. **Fracciones no relacionadas** (1/3 y 1/4): **el producto de los dos de abajo** sirve de denominador común (12).
5. **Comparar**: pasarlas a un denominador común es **uno de varios** métodos.

Common Core 5.NF.A.1: `2/3 + 5/4 = 8/12 + 15/12 = 23/12`; en general `a/b + c/d = (ad + bc)/bd`; **no hace falta
simplificar** el resultado en este curso (se puede). Incluye **números mixtos**. 5.NF.A.2: estimar con fracciones de
referencia para ver que una respuesta es razonable; el error típico, **sumar arriba con arriba y abajo con abajo**
(1/2 + 1/3 = 2/5), se caza porque 2/5 es MENOR que 1/2 y sumarle algo no puede dar menos. Otro error que avisan
(Oak, por el buscador): **sumar o restar los de abajo** entre sí.

Viene de: F.3 (sumar y restar con el mismo de abajo: los de arriba se cuentan, el de abajo no cambia), F.4 (mixtos e
impropias), F.2 (comparar con el mismo arriba o abajo), F.6 (equivalentes: multiplicar arriba y abajo por el mismo;
simplificar), M.2–M.7 (las tablas), M.3/M.8 (dividir y ver si sobra), M.15 (múltiplos).

**Cómo lo hace un humano sin calculadora (y así lo hará Euclides).**
- **Relacionadas** `1/2 + 1/4`: mira los de abajo; 4 : 2 = 2, justo: los cuartos caben en los medios. Cambia SOLO la de
  los medios: 1/2 = 2/4 (arriba y abajo por 2). Ahora las partes son del mismo tamaño: 2/4 + 1/4 = 3/4 (cuenta los
  cuartos, como en F.3). `3/4 - 5/8` → 6/8 - 5/8 = 1/8.
- **No relacionadas** `1/3 + 1/4`: 4 : 3 no es justo (ni 3 : 4): multiplica los de abajo: 3 x 4 = 12. Cada una por el
  de abajo de la otra: 1/3 = 4/12 (por 4), 1/4 = 3/12 (por 3). 4/12 + 3/12 = 7/12.
- **Simplifica al final** si se puede (5/6 - 1/3 → 5/6 - 2/6 = 3/6 = 1/2), y si se pasa de un entero lo dice como mixto
  (2/3 + 3/4 = 17/12 = 1 5/12).
- **La vuelta** (como en F.3): lo contrario. Para la suma, al resultado (en el de abajo común) le quita la segunda; sale
  la primera ya cambiada, y **dividiéndola de vuelta** (entre lo que se multiplicó) sale la de partida. Para la resta,
  suma de vuelta.
- **Restar más de lo que hay**: `1/4 - 1/2` → primero ve cuál es mayor (con el mismo de abajo): se quita más de lo que
  hay → no se puede (los negativos con fracciones no son de 5.º).
- **Mixtos** `2 1/2 + 1 1/4`: los pasa a impropias (5/2 + 5/4), busca el mismo de abajo (10/4 + 5/4 = 15/4) y lo dice
  como mixto: 3 3/4.
- **Comparar** `2/3 y 3/4` (no comparten nada): el mismo de abajo, 12: 8/12 y 9/12 → 9 partes son más que 8 → 2/3 < 3/4.
  Y como NCETM dice «varios métodos», también **el mismo de arriba** (el producto de los de arriba): 2/3 = 6/9 y
  3/4 = 6/8; los octavos son más grandes que los novenos → 3/4 es mayor. Los dos caminos tienen que decir lo mismo (la
  pregunta `comparar_fracciones` es de «todas iguales»).
- **El error típico** se dice en cada suma: «1/2 + 1/3 NO es 2/5 (arriba con arriba, abajo con abajo): 2/5 es menor
  que 1/2, y sumar algo no puede dar menos» — comparando 2/5 con 1/2 con el mecanismo (5.NF.A.2).

**Lo que se construye.**
- Pregunta nueva en `_objetivos.py`: `mismo_de_abajo` (la más rápida): pasar dos fracciones con distinto de abajo a
  equivalentes con el mismo de abajo.
- Piezas nuevas, **todas con su vuelta real** (dividir de vuelta arriba y abajo entre lo que se multiplicó y ver que sale
  la de partida):
  - `mismo_de_abajo_cambiando_una` (mismo_de_abajo, rapidez 3): relacionadas, un de abajo cabe justo en el otro; se
    cambia solo una (NCETM 3.8, puntos 1–3).
  - `mismo_de_abajo_multiplicando_los_de_abajo` (mismo_de_abajo, rapidez 6): el producto de los de abajo; se cambian las
    dos (punto 4). También sirve con las relacionadas (es más largo).
  - `fracciones_con_el_mismo_de_abajo` (comparar_fracciones, rapidez 6): usa `mismo_de_abajo` y compara los de arriba
    (punto 5).
  - `fracciones_con_el_mismo_de_arriba` (comparar_fracciones, rapidez 7): el producto de los de arriba (o el que cabe
    justo); compara los de abajo al revés (F.2).
- Las condiciones en `_condiciones.py` (prefijo `_f7_`): los de abajo son distintos; un de abajo cabe justo en el otro.
- Parte nueva `sistema/partes/comun_denominador.py` (prefijo `_cd_`): la cuenta `1/2 + 1/4`, `3/4 - 5/8` (pasar al mismo
  de abajo con las piezas, contar los de arriba como en F.3, la vuelta, simplificar, el mixto, el error típico) y los
  mixtos con distinto de abajo. `fracciones.py` le pasa estas cuentas en vez de decir «todavía no».
- Los de abajo de partida siguen siendo los que tienen nombre (medios … doceavos, décimos, centésimos, milésimos); el de
  abajo común puede ser cualquier número de la lista (hasta el millón): 1/7 + 1/1000 = 1000/7000 + 7/7000.

**Las trampas.**
- `1/2 + 1/3` → 5/6, **no 2/5** (arriba con arriba y abajo con abajo); `1/2 + 1/4` → 3/4, no 2/6.
- `3/4 - 1/2` → 1/4, **no 2/2** (restar los de abajo).
- `1/2 + 1/2` y `2/4 + 1/2`: el mismo de abajo o relacionadas; `1/2 + 2/4` = 1 (un entero justo).
- `5/6 - 1/3` → 3/6 → **1/2** (simplificar al final).
- `2/3 + 3/4` → 17/12 = **1 5/12** (más de un entero).
- `1/4 - 1/2` → **no se puede** (se quita más de lo que hay); `1/2 - 2/4` → 0.
- `comparar: 2/3 y 3/4` → 2/3 < 3/4 (antes «todavía no»); `comparar: 3/12 y 1/4` sigue siendo =, ahora por tres caminos.
- `comparar: 5/8 y 7/12` (no relacionadas, ni producto pequeño: 96 o el 24).
- Cerca del techo: `1/1000 + 1/999`? (999 no tiene nombre de fracción → todavía no); `1/7 + 1/1000` → 1007/7000;
  `999/1000 + 1/1000` → 1; `1/11 + 1/1000` = 11000 abajo. Y el tiempo de cada una.
- `2 1/2 + 1 1/4` → 3 3/4; `3 1/3 - 1 1/2` → 1 5/6 (hay que cambiar un entero); `1 1/2 - 2 1/4` → no se puede.

**Prueba de dominio.** Contra el testigo (`fractions` de Python, solo en la prueba): todas las sumas y restas de
fracciones propias con de abajo de 2 a 12 y distintos (relacionadas y no), comprobando el valor, la vuelta, que se elige
`cambiando una` exactamente cuando son relacionadas y que la forma simplificada es la del testigo; una muestra con
décimos, centésimos y milésimos; todas las comparaciones de parejas sin nada en común de 2 a 12 (los dos caminos de
acuerdo con el testigo); mixtos al azar fijo; las trampas; cada pieza nueva con una cuenta trucada (la vuelta la caza);
cerca del techo; y el tiempo (cada pregunta en menos de 2 s).

## RESULTADO (8 oct)

**Hecho, verde: proyecto 2907/2907 + 770/770.** `test_F7_el_mismo_de_abajo` 66/66 (≈ 50 s, por la cantidad de casos);
mis_casos 770/770; mis_pruebas 219/219; la auditoría sin calculadora, limpia.

- Una pregunta nueva (`mismo_de_abajo`) y 4 piezas nuevas, sin tocar el motor de piezas, **todas con su vuelta real** (dividen de
  vuelta, arriba y abajo, entre lo que multiplicaron, y tiene que salir la de partida; ninguna se fía de la comprobación de otra):
  - `mismo_de_abajo_cambiando_una` (3): relacionadas, 1/2 y 1/4 → 4 : 2 = 2, justo → 1/2 = 2/4 y 1/4 se queda.
  - `mismo_de_abajo_multiplicando_los_de_abajo` (6): 1/3 y 1/4 → 3 x 4 = 12 → 4/12 y 3/12. Con las relacionadas «también servía».
  - `fracciones_con_el_mismo_de_abajo` (comparar_fracciones, 6): `comparar: 2/3 y 3/4` → 8/12 y 9/12 → 2/3 < 3/4.
  - `fracciones_con_el_mismo_de_arriba` (comparar_fracciones, 7): 2/3 = 6/9 y 3/4 = 6/8 → los octavos son más grandes → lo mismo.
    Como `comparar_fracciones` es de «todas iguales», los dos caminos (y el de F.6 si son equivalentes) tienen que coincidir.
- Parte nueva `sistema/partes/comun_denominador.py` (`_cd_`): las cuentas con distinto de abajo que `fracciones.py` antes
  contestaba con «todavía no». Pasos: el mismo de abajo (la tabla de métodos), contar los de arriba como en F.3, la vuelta (la
  cuenta contraria y dividir de vuelta), simplificar al final (F.6) y decirlo como mixto si pasa de un entero (F.4). Los mixtos con
  distinto de abajo se pasan a impropias. El **error típico** se dice comparando con el mecanismo: «1/2 + 1/3 NO es 2/5: 2/5 es
  MENOR que 1/2, y sumarle algo no puede dar menos»; «3/4 - 1/2 NO es 2/2: 2/2 es MAYOR que 3/4».
- Restar más de lo que hay: se ve al pasarlas al mismo de abajo (1/4 - 1/2 → 1/4 contra 2/4) → no se puede.
- 6 pruebas viejas quedaron **obsoletas por mejora** (cambiadas con el caso viejo escrito al lado): `test_F2` A7 y B1 (las 4730
  parejas sin nada en común ahora salen todas, por dos caminos), `test_F3` A9, `test_F4` A11 y D1, `test_F6` A e I. Y 2 casos de
  `mis_casos.txt` (comparar 2/3 y 3/5; 1/2 + 1/4).
- **Respetar el año:** el camino del mismo de arriba con números grandes (715/1000 y 93/100: 715 x 93) pide dividir entre dos
  cifras o más para la vuelta, que es la división larga (6.º): **no sale**, y la comparación la hace solo el del mismo de abajo
  (en la muestra al azar, 177 de 200 salieron por los dos caminos; con los de abajo de 2 a 12, siempre los dos).
- **Todavía no** (y lo dice): fracciones de partida con un de abajo sin nombre (1/13, 1/999). El de abajo común sí puede ser
  cualquiera de la lista: 1/11 + 1/1000 = 1011/11000. No se busca el **menor** múltiplo común (1/4 + 1/6 va por 24 y se simplifica
  al final: 10/24 = 5/12); NCETM 3.8 pide el producto, y el menor común es una mejora para cuando Carlos lo pida.
- **Tiempo:** cada pregunta, con su explicación, 0.01–0.2 s (cerca del millón, `999 1/2 + 999 1/3` → 1998 5/6 en 0.16 s).
- **Falta la prueba de Carlos.** Y leer el segmento entero de NCETM 3.8 cuando se pueda abrir.
