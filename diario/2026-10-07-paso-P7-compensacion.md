# Paso P.7 — USAR LA EQUIVALENCIA Y LA COMPENSACIÓN PARA CALCULAR (sumas y restas) — 7 oct 2026

Sigue al S.2. Es el segmento **1.29** de NCETM (Spine 1, Year 5): *Using equivalence and the compensation
property to calculate*. Se llama **P.7** porque amplía las técnicas de la serie P (P.4 compensar con dos cifras
acabadas en 9; P.5 dar la vuelta; P.6 restar pensando en sumar). Es la hermana aditiva de M.12 (NCETM 2.18,
la equivalencia en × y :). En Common Core: 4.NBT.B.4 / 5.NBT (estrategias basadas en el valor posicional y las
propiedades de las operaciones) y 1.OA.D.7 / 2.OA (el = como «es el mismo número que»).

## 1. EL PLAN (escrito antes de programar)

**La fuente.** La web de NCETM **sigue sin poder abrirse desde la nube** (`EGRESS_BLOCKED www.ncetm.org.uk`, probado
hoy otra vez, también los PDF de las *Guidance for teachers*). Lo que sigue sale del índice de NCETM en el buscador
(página *primm-129-using-equivalence-and-the-compensation-property-to-calculate*) y de los resúmenes de las guías
de Upper KS2 (*Number, Addition and Subtraction*, lecciones 16 y 22). Falta leer el segmento entero (los ejemplos
y los archivos de Year 5) cuando Carlos pueda abrirlo.

Los **seis puntos de enseñanza** (traducidos):
1. **La misma suma:** si un sumando aumenta y el otro disminuye **lo mismo**, la suma no cambia.
2. **Cambiar un sumando:** si un sumando aumenta (o disminuye) y el otro se queda igual, la suma aumenta (o
   disminuye) **lo mismo**.
3. **La misma diferencia:** si el minuendo y el sustraendo cambian **lo mismo** (los dos hacia el mismo lado), la
   diferencia no cambia.
4. **Cambiar el minuendo:** si el minuendo aumenta (o disminuye) y el sustraendo se queda igual, la diferencia
   aumenta (o disminuye) lo mismo.
5. **Cambiar el sustraendo:** si el minuendo se queda igual y el sustraendo aumenta (o disminuye), la diferencia
   **disminuye (o aumenta)** lo mismo.
6. **Las ecuaciones:** los dos lados del = valen lo mismo; la suma y la resta son operaciones inversas. Con esto se
   equilibran ecuaciones y se resuelven problemas.

Lo que dicen las guías (los resúmenes): el punto 5 es «probablemente el que más les cuesta», porque los niños
**suponen que si el sustraendo aumenta, la diferencia también aumenta**; con la misma diferencia, el cálculo se
vuelve fácil **cuando el sustraendo es un múltiplo de 10, 100, 1000**; y ante una ecuación «mirar primero si se
puede usar la compensación y solo calcular si no». Ejemplos de otras fuentes del mismo método: 483 − 397 = 486 −
400 (NZ Maths, *Equal additions*); 625 − 398 = 625 − 400 + 2 (redondear y devolver).

Viene de: P.4 (compensar 29 + 14 con dos cifras), E.2 (la balanza con dos sumas: 8 + 4 = ? + 5, que ya citaba la
1.29), M.12 (la equivalencia en × y :), N.3/N.4 (los números hasta un millón) y D.1/D.2 (decimales hasta las
milésimas).

**Cómo lo hace un humano sin calculadora (y así lo hará Euclides).**
- **Mira si un número está CERCA de un redondo** (un múltiplo de 100, 1000…: 397, 4997, 1003). «Cerca» = le faltan
  o le sobran 1, 2 o 3 (los cuenta con los dedos).
- **La misma suma (punto 1):** 4997 + 2456 → «al 4997 le faltan 3 para 5000; se los quito al 2456»: 5000 + 2453.
  Con un redondo la cuenta es fácil (solo cambia una columna): 7453.
- **La misma diferencia (punto 3):** 1000 − 397 → «le sumo 3 a los dos»: 1003 − 400 = 603. Si el sustraendo se pasa
  un poco (1000 − 403) le quito 3 a los dos: 997 − 400 = 597.
- **Quitar de más y devolver (punto 5):** 625 − 398 → 625 − 400 = 225; quité 2 de más, **los devuelvo**: 227. (Sirve
  cuando la misma diferencia no se puede: 999 999 − 997 → sumar 3 a los dos pasaría del millón.)
- **Sumar de más y quitar (punto 2):** 4997 + 2 → no puedo quitarle 3 al 2; 5000 + 2 = 5002 y le quito los 3 que
  puse de más: 4999.
- **Derivar de un hecho que se sabe (puntos 2, 4, 5):** «si 600 − 200 = 400, ¿601 − 200? ¿600 − 201?» Sin volver a
  calcular: el minuendo sube 1 → la diferencia sube 1 (401); el sustraendo sube 1 → la diferencia **baja** 1 (399).
- **Ver la igualdad sin calcular (puntos 1 y 3, pensamiento relacional):** `verdad: 75 - 28 = 77 - 30` → VERDADERO
  (los dos suben 2). `verdad: 75 - 28 = 73 - 30` → FALSO (el minuendo baja 2 y el sustraendo sube 2: la diferencia
  baja 4).
- **La balanza (punto 6):** `74 - 28 = 75 - ?` → el minuendo subió 1, el sustraendo tiene que subir 1: 29 (no 27).
- **Con decimales igual:** 7.2 − 3.9 = 7.3 − 4 = 3.3; 2.98 + 1.45 = 3 + 1.43 = 4.43; 5.003 − 1.998 = 5.005 − 2 = 3.005.
  (Se cuentan en décimas/centésimas/milésimas, como en D.1/M.13, y el redondo es un ENTERO.)
- **Siempre comprueba con la operación contraria** (y por las columnas, para no usar la compensación para
  comprobar la compensación).

**Lo que se construye.**
- Piezas nuevas (cada una con su **vuelta real** con la operación contraria por las columnas — sin ciclos):
  - `sumar_misma_suma` (sumar, rapidez 7): punto 1.
  - `sumar_redondeando_y_quitando` (sumar, rapidez 8): punto 2.
  - `restar_misma_diferencia` (restar, rapidez 7): punto 3.
  - `restar_quitando_de_mas_y_devolviendo` (restar, rapidez 8): punto 5 (la versión grande de P.4).
  - `igual_compensando` (igualdad, rapidez 3): dos sumas o dos restas; VERDADERO o FALSO sin calcular los lados, si
    los cambios son fáciles (caben en los dedos o son decenas/centenas justas). Vuelta: calcula los dos lados.
  - `balanza_misma_diferencia` (balanza, rapidez 5): dos restas, el hueco en el minuendo o en el sustraendo.
    Vuelta: calcula los dos lados.
  - Pregunta nueva `derivar` con `derivar_compensando` (rapidez 5) y `derivar_calculando` (rapidez 20, «también
    servía»). Vuelta: la cuenta nueva hecha de verdad.
- **Deuda que se paga aquí:** `balanza_compensando` (E.2, cita la 1.29) devolvía `vuelta_ok: True` sin comprobar
  nada; pasa a comprobar calculando los dos lados.
- Las condiciones en `_condiciones.py` (prefijo `_p7_`); la pregunta en `_objetivos.py`.
- Parte nueva `sistema/partes/compensacion.py` (prefijo `_cmp_`):
  - la orden `si 600 - 200 = 400: 600 - 201 = ?` (primero comprueba que el hecho que le dan es verdad: un hecho
    falso no se usa);
  - la orden `equivalente:` se amplía a `+` y `-` (y con decimales hasta las milésimas): enseña la cadena
    (1000 − 397 = 1003 − 400 = 603) y la vuelta;
  - la trampa de la balanza con restas («compensar al revés, como en la suma»).
- El cerebro de lo «redondo» (cuántos ceros tiene un número, cuánto le falta) lee cifras y cuenta con los dedos:
  nada de `%`, `//` ni `<` de Python sobre tamaños.

**Las trampas.**
- `600 - 201` sabiendo `600 - 200 = 400` → **399** (no 401: el error del punto 5).
- `74 - 28 = 75 - ?` → **29** (no 27: compensar al revés, como en la suma).
- `verdad: 75 - 28 = 73 - 30` → FALSO; `verdad: 250 + 250 = 260 + 240` → VERDADERO; `verdad: 250 + 250 = 260 + 260`
  → FALSO.
- `1000 - 397` → 603 por la misma diferencia (1003 − 400).
- Cerca del techo: `999999 - 997` → la misma diferencia pasaría del millón → «quitar de más y devolver»: 999 002;
  `999997 + 3` → 1 000 000; `999997 + 5` → no alcanza.
- Un hecho falso: `si 600 - 200 = 500: 600 - 201 = ?` → «el hecho no es verdad: no lo uso».
- Decimales con tres cifras: `equivalente: 5.003 - 1.998` → 5.005 − 2 = 3.005.
- No se puede: restar más de lo que hay (`si 5 - 3 = 2: 5 - 8 = ?` → no hay restas negativas aquí, 5.4).

**Prueba de dominio.** Contra el testigo (Python, solo en la prueba): sumas y restas con un número cerca de un
redondo (100…100 000) hasta el millón; derivaciones de los puntos 2, 4 y 5 al azar fijo; igualdades verdaderas y
falsas (sumas y restas); balanzas de restas con el hueco en cada sitio; decimales de 1 a 3 cifras; cada pieza nueva
con una cuenta trucada (la vuelta lo caza); cerca del techo; y el tiempo (cada pregunta en menos de 2 s).

## RESULTADO (7 oct)

**Hecho, verde: proyecto 2726/2726 + 739/739.** `test_P7_compensacion` 106/106; mis_casos 739/739; mis_pruebas 207/207;
la auditoría sin calculadora, limpia.

- Una pregunta-ayuda nueva (`redondo_cercano`, con la pieza `buscar_el_redondo_cercano`: cuenta 1, 2 o 3 con los dedos hacia
  los dos lados y LEE los ceros del final; la vuelta cuenta al revés) y una pregunta nueva (`derivar`). 9 piezas nuevas, sin
  tocar el motor de piezas, **todas con su vuelta real** (por las columnas, para no comprobar la compensación con la
  compensación ni hacer ciclos):
  - `sumar_misma_suma` (7; punto 1): 4997 + 2456 = 5000 + 2453 = 7453.
  - `sumar_redondeando_y_quitando` (8; punto 2): 4997 + 2 = 5000 + 2 − 3 = 4999 (cuando al otro no se le puede quitar).
  - `restar_misma_diferencia` (7; punto 3): 1000 − 397 = 1003 − 400 = 603; 1000 − 403 = 997 − 400.
  - `restar_quitando_de_mas_y_devolviendo` (8; punto 5): 999 999 − 997 → sumar 3 a los dos pasaría del millón, así que
    999 999 − 1000 = 998 999 y devuelvo 3: 999 002.
  - `igual_compensando` (igualdad, 3): VERDADERO o FALSO **sin calcular** si los cambios son fáciles (dedos o decenas/centenas
    justas); dice cuánto sube o baja el resultado. Vuelta: calcula los dos lados.
  - `balanza_misma_diferencia` (balanza, 5): `74 - 28 = 75 - ?` → 29; `50 - 19 = ? - 20` → 51. Vuelta: los dos platos.
  - `derivar_compensando` (5) y `derivar_calculando` (20): `si 600 - 200 = 400: 600 - 201 = ?` → 399.
- **Deuda pagada:** `balanza_compensando` (E.2) ya no devuelve `vuelta_ok: True` sin mirar: calcula los dos platos.
- Parte nueva `sistema/partes/compensacion.py`: la orden `si … : … = ?` (comprueba primero el hecho: `si 600 - 200 = 500: …`
  → `hecho_falso`; y dice la trampa del punto 5: «401 NO»); `equivalente:` ahora también con + y −, y con decimales hasta las
  milésimas contando en décimas/centésimas/milésimas (7.2 − 3.9 = 7.3 − 4; 5.003 − 1.998 = 5.005 − 2; 2.98 + 1.45 = 3 + 1.43);
  y la trampa nueva de la balanza con restas («27 NO: compensar al revés, como en la suma»).
- El «redondo» exige al menos dos ceros con enteros (100, 1000…): las de dos cifras acabadas en 9 siguen por P.4 (más corto).
  Con decimales, el redondo es un entero.
- Prueba de dominio contra el testigo (al azar fijo): 150 sumas y 150 restas con un número cerca de un redondo (todas por P.7),
  ~80 derivaciones, ~100 igualdades verdaderas y falsas, ~80 balanzas de restas, 60 cuentas con decimales de 1 a 3 cifras; cada
  pieza nueva con una cuenta trucada (la vuelta lo caza, también en `buscar_el_redondo_cercano` contando mal).
- **Cerca del techo:** 999997 + 3 = 1 000 000; 999997 + 5 → no alcanza; 1 000 000 − 999 997 = 3; `999999 - 997 = 1000000 - ?`
  → 998; `equivalente: 999999.999 - 0.998` → no alcanza (en milésimas pasa del millón: el techo de M.13).
- **Tiempo:** cada pregunta, con su explicación, 0.01–0.3 s; la prueba entera, 6 s.
- Tres pruebas viejas quedaron **obsoletas por mejora** (cambiadas caso por caso, con el caso viejo escrito al lado):
  `99 + 14` ahora sale por la misma suma (100 + 13); `15 - 7 = ? - 6` por la misma diferencia; `4 + 1 = 5 + 2` se ve FALSO sin
  calcular (y la pieza que calcula, pedida por su nombre, sigue diciendo la trampa «el = no dice da»).
- Todavía no: la balanza y `verdad:` con decimales (solo enteros, como antes); compensar en problemas de varios pasos.
- **Falta la prueba de Carlos.** Y leer el segmento entero de NCETM 1.29 (los archivos de Year 5) cuando se pueda abrir.
