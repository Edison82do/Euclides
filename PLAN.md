# PLAN de Euclides — hoja de ruta por unidades pequeñas

**Proyecto:** sistema determinista de conocimiento matemático acumulativo (idea de Carlos, v3 y refinada).
**Regla de oro:** una unidad no se cierra sin su **prueba de dominio en un caso no programado**.
**Estado:** Fase 1 abierta (nada construido todavía).

---

## Fase 1 — objeto → cantidad → conteo → número (niveles 0 a 3, subdivididos)

### Nivel 0 — Realidad concreta
| Unidad | Objetivo | Prueba de dominio |
|---|---|---|
| 0.1 | Representar **objetos individuales** (existen entidades separadas) | Distingue "un objeto" de "varios objetos" (sin contar) |
| 0.2 | Formar y reconocer **grupos** de objetos | Reconoce y describe grupos distintos de un conjunto dado |
| 0.3 | **Pertenencia**: un objeto está o no está en un grupo | Clasifica objetos nuevos en el grupo correcto |

### Nivel 1 — Cantidad (antes del símbolo y del número)
> **Nota de orden (3 de octubre de 2026, decisión de Carlos):** las unidades 1.1–1.4 quedan
> **aplazadas**. Motivo: el sistema todavía no ve, así que toda entrada del Nivel 1 se le da escrita a
> mano y esas unidades quedarían construidas pero sin utilidad (es lo que pasó con la 1.0, que está
> cerrada y **aislada**). Se pasa primero al **Nivel 2 (conteo)**, que es donde el sistema empieza a
> **deducir** algo que no se le ha dado: la cantidad. Se retomarán cuando tengan con qué conectarse.

| Unidad | Objetivo | Prueba de dominio |
|---|---|---|
| 1.0 | **Subitizing**: reconocer de un vistazo la cantidad de un grupo pequeño (2–4), sin contar | Nombra la cantidad de grupos nuevos sin contar ni enumerar |
| 1.1 | Concebir **cantidad** como propiedad de un grupo | Nombra la cantidad de grupos nuevos sin usar cifras |
| 1.2 | Comparar cantidades **sin contar** (más / menos / igual) | Acierta en pares de grupos nuevos |
| 1.3 | **Igualdad y diferencia** de cantidades | Decide igual/diferente en casos nuevos |
| 1.4 | **Mayor y menor** entre cantidades | Ordena tres grupos por cantidad sin contar |

### Nivel 2 — Conteo   ✅ **COMPLETO (3 de octubre de 2026)** — 208/208 pruebas en verde
| Unidad | Objetivo | Prueba de dominio |
|---|---|---|
| 2.1 ✅ | **Correspondencia uno a uno** objeto ↔ elemento de la secuencia | Empareja sin dejar ni repetir |
| 2.2 ✅ | Aprender la **secuencia de conteo** (uno, dos, tres…) | Recita y sigue la secuencia |
| 2.3 ✅ | **Contar** un grupo y determinar su cantidad | Cuenta grupos nuevos y acierta |
| 2.4 ✅ | **Cardinalidad**: el último número dicho es el total | Responde "¿cuántos hay?" tras contar |
| 2.5 ✅ | **Principio de orden irrelevante**: contar en otro orden da lo mismo | Verifica el mismo total contando al revés |
| 2.6 ✅ | **Principio de abstracción**: se puede contar cualquier cosa | Cuenta objetos de otra clase |

**Nota de implementación (2.4):** la tarea Give-N **necesita un montón** que da quien pregunta
(`dame: <montón> / <cantidad>`), porque el sistema **no tiene un mundo** y no debe inventarse los
objetos. Decisión de Carlos.

### Nivel 3 — Números
| Unidad | Objetivo | Prueba de dominio |
|---|---|---|
| 3.1 | **Símbolos** 1..9 como representación de cantidades | Asocia símbolo ↔ cantidad en casos nuevos |
| 3.2 | **El cero** como ausencia de elementos en un contexto | Reconoce y usa el 0 correctamente |
| 3.3 | **Secuencia numérica** y su orden | Ordena y continúa series |
| 3.4 | Puente **cantidad → palabra → símbolo** en los dos sentidos | Traduce en ambas direcciones |

## Fase 2 — relaciones y operaciones (niveles 4 y 5)
- Nivel 4: `=`, `<`, `>` (relaciones entre cantidades y entre números).
- Nivel 5: suma, resta, multiplicación, división — cada una con: qué significa, términos, métodos,
  **condiciones de aplicación** y **verificación** (la inversa verifica; 7−3=4 y 4+3=7).
- Prueba de dominio: **ver la nota de abajo** (notas de Carlos, 3 de octubre de 2026).

### ⭐ NOTA DE CARLOS (3 oct 2026) — QUÉ SIGNIFICA «SABER RESOLVER» (esto es el corazón del proyecto)

> «Algo que quiero con este sistema es que si le doy algún problema **no es que él sepa qué hacer**,
> el asunto sería que el sepa **utilizar o aplicar lo que sabe**, le aplique **todo y combinaciones de
> lo que sabe al problema**, pero **con descarte para solo aplicar las cosas que tienen sentido
> aplicar**.»

Esto es **más exigente** que «elegir la operación», y cambia lo que hay que construir:

1. **NO es un clasificador.** No vale un `si el problema dice "más" → suma`. Eso sería adivinar por la
   palabra, que es justo el error que la investigación señala como el más típico («los niños se fijan
   en "más" y suman»).
2. **APLICAR lo que sabe** = sacar a la luz todos los conocimientos que **podrían** encajar.
3. **COMBINACIONES** = encadenarlos (una respuesta se convierte en dato del siguiente paso).
4. **DESCARTE** = podar los que **no** tienen sentido, **y decir por qué se descartan**. Ese «por qué»
   es la **condición de aplicación** de cada conocimiento (las que ya existen: `no_hay_bastantes`,
   `grupo_equivocado`, `no_alcanza`, `no_es_un_numero`…). Sin el porqué del descarte sería una **caja
   negra**, y la regla 13 del método lo prohíbe.

Consecuencia para el diseño: el **descarte** es una mitad del trabajo, tan importante como la
aplicación. Y hay que poder **enseñar el descarte** («esto lo sé, pero aquí no vale, porque…»).

### ⭐ NOTAS DE CARLOS (4 oct 2026) — EL MECANISMO DE CALCULAR (los dedos, el valor posicional y las columnas)

> **1.** «A los niños se les enseña los números hasta el 10 porque el sistema que usamos es el
> decimal, porque es **más complicado de ahí en adelante** y porque **tenemos 10 dedos**.»
> **2.** «El sistema **debería tener algo que haga el papel de los 10 dedos**.»
> **3.** «Teniendo 10 dedos, para sumar dos números **anotamos el primero** (el sistema debería tener
> **algo que le sirva para anotar**), tomamos el segundo número con los dedos, **continuamos el conteo
> descontando dedos** y cuando se acaben los dedos ahí es el total de la suma. Ya ahí,
> **mecánicamente**, ya sabemos sumar dos números del 0 al 9.»
> **4.** «Para sumar o habría que hacerlo **mecánicamente de esta forma**, o **saberse de memoria**
> algunas sumas, o **usar una calculadora**.»
> **5.** «Este sistema **debe hacerlo mecánicamente hasta nuevo aviso**.»
> **6.** «Ya como sabemos contar hasta 100, hay que enseñarle qué es **unidad, decena, centena, unidad
> de mil, decena de mil, etc.**»
> **7.** «Debemos enseñarle el **método de sumar unidad con unidad, luego decena con decena y luego
> centena con centena**; además de enseñarle que **si pasa de 9 se anota la unidad y la decena que se
> lleva (1) se suma con lo siguiente**.»
> **9.** «Después pruebo lo que hiciste hasta ahora.»
> **10. (4 oct 2026, tarde) LA RESTA CON LOS DEDOS.** «Todavía no hemos llegado a la resta, pero
> con los dedos **se toma el primer número con los dedos**, se le van **descontando el segundo
> número** y **los dedos que quedan son el resultado** de la resta.»
>
> Leído por mí: es **el mismo mecanismo que la 7.1 (los dedos) y la 7.2 (derivar), pero hacia
> atrás**. En la suma se **cuenta hacia adelante** desde el primero; en la resta se **cuenta hacia
> atrás** (o se bajan los dedos que se quitan). Las dos piezas que hacen falta ya están en el
> sistema, pero **a la resta le falta su mecanismo**: hoy `quitar:` sabe *qué* es la resta (5.4:
> la historia primero/luego/ahora, y la vuelta que la verifica) pero **no sabe hacerla con los
> dedos**. Eso es una unidad nueva: **7.4 (el mecanismo de la resta con los dedos)**, gemela de la
> 7.1. Y encaja con la 5.4: los dedos que quedan son **lo que queda después de que se vayan**, que
> es exactamente la definición de quitar.
>
> **DECISIÓN DE CARLOS (4 oct 2026, noche): la CENTENA va ANTES que la multiplicación.** Orden
> acordado: **7.4 (resta con los dedos) → resta por columnas → la centena → y después multiplicar
> y dividir**. Respaldo: el currículo cierra la suma y la resta **hasta tres cifras** antes de que
> la multiplicación sea el foco (Achieve the Core: «At Grade 3, the major focus is multiplication»);
> la centena es **el mismo movimiento que la 6.2 un escalón más arriba** (diez decenas son una
> centena); y los requisitos para multiplicar (tablas, ×10, doblar) no están.
>
> **Y SU REGLA, que refuerza (4 oct): «con cada cambio nuevo hay que probar todo lo anterior».**
> No es solo correr `correr_todas.py`: es **leer la salida entera** y comprobar que lo viejo sigue
> diciendo lo que decía **y que el cambio no ha dejado ninguna puerta mintiendo**.

**Lo que esto significa para el diseño (leído por mí, pendiente de su OK):**

- **LOS DEDOS = el primer modelo del diez.** No es un adorno: es el apoyo **concreto** antes de lo
  abstracto, y es **el mismo diez que la decena**. El sistema necesita un modelo de «diez huecos», de
  los que se van ocupando/liberando.
- **«ALGO QUE LE SIRVA PARA ANOTAR» = memoria de trabajo.** Hoy el sistema es **función pura** (entrada
  → salida) y no apunta nada. El método de los dedos necesita **estado**: el primero anotado y un
  contador que avanza. **Ese estado tiene que VERSE en la traza**, o deja de ser rastreable (regla 13).
- **EL MECANISMO MANDA (nota 5):** nada de hechos memorizados ni de calculadora. Y es reversible, lo
  dice él: «hasta nuevo aviso».
- **Y la nota 7 es la GENERALIZACIÓN de la nota 3**: los dedos dan un dígito + un dígito; las columnas
  dan cualquier suma **usando los dedos por partes**. No son dos métodos distintos: es el mismo, uno
  con la mano y otro con el papel.
- **Lo que trae detrás:** valor posicional más allá de cien (unidad → decena → centena → unidad de mil
  → …), el **acarreo** (que solo puede ser 1, porque 9+9=18 y 18+1=19), y **la resta y la
  multiplicación con el mismo criterio mecánico** (eso no está dicho en las notas y hay que decidirlo).

### NOTA DE ORDEN (3 oct 2026) — lo siguiente NO es la multiplicación

> «antes de entrar a la multiplicación y la división primero vamos a enseñarle a **contar hasta 100**
> por lo menos.»

Así que el orden es: **contar hasta 100** (y lo que traiga detrás) → **después** multiplicación y
división. Motivo: multiplicar es contar grupos de grupos; con el conteo cortado en diez, la
multiplicación no tiene dónde apoyarse. El sistema **hoy cuenta hasta diez** (la lista de contar es
`uno…diez`), y **es un techo que se nota**: aparece como `no_alcanza` en cada unidad.

### NOTA DE CARLOS (3 oct 2026) — la suma y la resta NO están terminadas

> «ahora mismo sabe lo básico de la suma y la resta, supongo que es porque es el nivel, pero le queda
> **mucho por aprender de la suma y la resta y cómo aplicarlo**.»

Cierto: están las **estructuras** (2 de la suma, 3 de la resta) y las **condiciones de aplicación**,
pero falta todo lo demás del nivel 5 — métodos, combinarlas, y sobre todo **aplicarlas a problemas**.
Cerrar una estructura **no es** cerrar la operación.


### ESTADO (5 oct 2026): la centena y la resta por columnas hasta mil, CERRADAS (6.7 y 7.6)

Orden acordado por Carlos: 7.4 → resta por columnas → **la centena** → multiplicar y dividir.
Las tres primeras están hechas. **Antes de multiplicar**, la revisión del 5 oct propone abrir
**R.1 — el resolvedor** (el corazón del proyecto según la nota del 3 oct: «aplicar lo que sabe y
combinaciones, con descarte»), con lo que el sistema YA sabe (suma y resta, sus tres estructuras).
Motivo: es el criterio de éxito del proyecto y hasta ahora no había nada que lo probara; cuanto
más tarde se pruebe la arquitectura con problemas, más caro sale cambiarla. **Pendiente del OK de
Carlos** para seguir por ahí o volver a la multiplicación.

| Unidad | Objetivo | Prueba de dominio |
|---|---|---|
| **R.1** Resolver problemas de una operación | Dado un enunciado de suma o resta, **aplicar** todos los conocimientos que podrían encajar, **descartar** con su porqué los que no, y resolver con el que queda, verificando | Problemas no programados de las 4 estructuras (juntar, añadir, quitar, comparar), con las **trampas de palabra clave** («más» que es resta) |
| R.2 | Dos pasos (combinar: la respuesta de uno es dato del siguiente) | — |
| R.3 | Enseñar un descarte nuevo («esto lo sé, pero aquí no vale porque…») | — |

## ⭐⭐ EL PLAN PEDAGÓGICO (acordado con Carlos el 5 oct 2026, noche)

**Decisión de Carlos:** «vamos a ir a **velocidad pedagógica**» y «sigue cada paso como un plan».
La investigación (Common Core 1.OA / 2.OA, Carpenter-Franke-Levi, Knuth et al., Steinberg) dice que
**antes de las ecuaciones faltan dos propiedades de 1.º**, y que el `=` se enseña en dos tiempos
(verdadero/falso → hueco). Se comprobó: `calcular: 3 + 47` iba por columnas (no da la vuelta) y
`13 - 8` contaba hacia atrás (no piensa en sumar).

**CÓMO SE HACE CADA PASO (regla):**
1. **El plan escrito primero** (en el diario del paso): la pedagogía con sus fuentes, qué se
   construye (piezas), las trampas, y la prueba de dominio.
2. Se construye y se prueba (todo verde, nada de calculadora).
3. **Carlos lo prueba con su `.bat`.** Steinberg: una estrategia necesita de **2 a 4 lecciones**
   para asentarse; no se presentan deprisa. **No se empieza el paso siguiente sin su OK.**

| # | Paso | Estándar / fuente | Prueba de dominio |
|---|---|---|---|
| 1 | ✅ **HECHO y probado por Carlos (5 oct)** — `diario/2026-10-05-paso-P5-dar-la-vuelta.md`. **P.5 Dar la vuelta**: el orden no importa al juntar; empezar por el grande (3 + 47 = 47 + 3) | 1.OA.B.3 (conmutativa) | 3 + 47, 30 + 47 por la vuelta; 47 + 3 no se da la vuelta; los problemas lo aprovechan |
| 2 | ✅ **HECHO y probado por Carlos (5 oct)** — `diario/2026-10-05-paso-P6-restar-sumando.md`. (Progression CC&OA: «contar hacia arriba para restar es más fácil que hacia atrás y refuerza que la resta es un sumando desconocido»; NCETM 1.12) **P.6 Restar pensando en sumar**: contar hacia arriba (13 − 8: de 8 a 13 hay 5) | 1.OA.B.4; «think addition» | 13 − 8, 52 − 48 contando hacia arriba; cuándo conviene y cuándo no |
| 3 | ✅ **HECHO y probado por Carlos (5 oct)** — `diario/2026-10-05-paso-E0-el-igual.md`. **E.0 El `=`: verdadero o falso** (6 = 6, 7 = 8 − 1, 5 + 2 = 2 + 5, 4 + 1 = 5 + 2) | 1.OA.D.7; Carpenter-Franke-Levi | el `=` es «los dos lados valen lo mismo», no «pon el resultado» |
| 4 | ✅ **HECHO y probado por Carlos (5 oct)** — `diario/2026-10-05-paso-E1-hueco.md`. **E.1 Ecuaciones con hueco** (8 + ? = 11, 5 = ? − 3, 6 + 6 = ?) | 1.OA.D.8 | el hueco en las tres posiciones y a los dos lados del `=` |
| 5 | ✅ **HECHO y probado por Carlos (5 oct)** — `diario/2026-10-05-paso-E2-balanza.md`. **E.2 El `=` como balanza** (8 + 4 = ? + 5 → 7, no 12 ni 17) | Knuth et al.; Falkner-Levi-Carpenter | las trampas 12 y 17 descartadas con su porqué |
| 6 | ✅ **HECHO y probado por Carlos (5 oct)** — `diario/2026-10-05-paso-N1-par-impar-saltos.md`. **N.1 Par e impar; contar de n en n** (2, 5, 10) | 2.OA.C.3; 2.NBT.2 | par = suma de dos iguales (los dobles) |
| 7 | ✅ **HECHO y probado por Carlos (5 oct)** — `diario/2026-10-05-paso-M0-filas.md`. **M.0 Filas y columnas como sumas iguales** (3 filas de 4 = 4 + 4 + 4) | 2.OA.C.4 | la suma de iguales, por saltos |
| 8 | ✅ **M.1, M.2 y M.3 HECHOS y probados por Carlos (5 oct)** — multiplicar = grupos iguales; tablas del 2, 5 y 10, conmutativa, dobles y mitades; dividir (repartir y agrupar). Diarios `2026-10-05-paso-M1/M2/M3-*.md` | 3.OA.A.1–2; NCETM 2.2–2.6 | ver los diarios |


### ⭐ EL PLAN AJUSTADO (5 oct, noche) — lo que dicta la pedagogía después de dividir

**Decisión de Carlos (5 oct):** «ajusta el plan a lo que la pedagogía dicta»; «hagamos cada cosa, pero
una a una». El **repaso mezclado** (práctica intercalada) **no** se hace: «eso es para humanos; para
eso están las pruebas».

Por qué este orden (Common Core 3.º, 3.OA; NCETM Spine 2, Year 3–4): primero el desconocido en una
multiplicación o división (3.OA.A.4); luego los problemas con × y ÷ (3.OA.A.3); luego el resto de las
tablas, **derivadas unas de otras** y con la distributiva (NCETM 2.7–2.9, 2.10; 3.OA.B.5, 3.OA.C.7);
y solo al final los problemas de **dos pasos con la letra como hueco** (3.OA.D.8: el mismo estándar
trae la letra, así que E.5 va con ellos).

| # | Paso | Estándar / fuente | Prueba de dominio |
|---|---|---|---|
| 9 | ✅ **HECHO y probado por Carlos (5 oct)** — `diario/2026-10-05-paso-E4-hueco-por.md`. **E.4 El hueco en × y ÷** (`3 x ? = 12`, `? : 4 = 5`, `12 = ? x 3`) | 3.OA.A.4; 3.OA.B.6 (factor desconocido); NCETM 2.6 | el hueco en las tres posiciones, a los dos lados del `=`; sin número entero → se dice |
| 10 | ✅ **HECHO y probado por Carlos (5 oct)** — `diario/2026-10-05-paso-R2-problemas-por.md`. **R.2 Problemas de × y ÷ con pocas palabras** (grupos iguales, filas, repartir, agrupar), con el **modelo de barras** | 3.OA.A.3; CGI (estructuras multiplicativas); Singapur (bar model) | cada estructura con su pieza; las trampas de palabras clave |
| 11 | ✅ **HECHO y probado por Carlos (5 oct)** — `diario/2026-10-05-paso-M4-tablas-4-8.md`. **M.4 Tablas del 4 y del 8 desde la del 2** (doblar) | NCETM 2.7 | cada producto derivado y comprobado; aprender de memoria |
| 12 | ✅ **HECHO y probado por Carlos** — `diario/2026-10-05-paso-M5-tablas-3-6-9.md`. **M.5 Tablas del 3, 6 y 9** (y sus relaciones) | NCETM 2.8 | ídem |
| 13 | ✅ **probado por Carlos** — `diario/2026-10-06-paso-M6-tabla-7-distributiva.md`. **M.6 Tabla del 7 y la distributiva** (7 × 6 = 5 × 6 + 2 × 6) | NCETM 2.9, 2.10; 3.OA.B.5; 3.OA.C.7 | todas las tablas hasta 10 × 10 |
| 14 | ✅ **HECHO y probado por Carlos (6 oct)** — `diario/2026-10-06-paso-E5-dos-pasos-letra.md`. **E.5 Dos pasos, con la letra como hueco** (`3 x n + 2 = 14`) | 3.OA.D.8 | problemas de dos pasos con las cuatro operaciones |

### ⭐ LA CONTINUACIÓN (6 oct) — la estimación, la otra mitad de 3.OA.D.8

Terminado el plan ajustado, lo que queda de 3.OA.D.8 es «valorar si la respuesta es **razonable** con
cálculo mental y **estimación, incluido el redondeo**». Una cosa cada vez: primero redondear
(3.NBT.A.1), luego estimar para comprobar.

| # | Paso | Estándar / fuente | Prueba de dominio |
|---|---|---|---|
| 15 | ✅ **HECHO y probado por Carlos (6 oct)** — **N.2 Redondear a la decena y a la centena** (en la recta: ¿de cuál está más cerca?) — `diario/2026-10-06-paso-N2-redondear.md` | 3.NBT.A.1; Progression NBT | de 0 a 1000 contra el testigo, dos caminos de acuerdo |
| 16 | ✅ **HECHO (6 oct), falta la prueba de Carlos (mañana)** — **E.6 ¿Es razonable? Estimar redondeando** — `diario/2026-10-06-paso-E6-razonable.md` (`38 + 47` ≈ 40 + 50 = 90) | 3.OA.D.8 | respuestas buenas y malas: las malas se cazan |

### ⭐ AÑOS ESCOLARES (6 oct, noche) — Carlos: «avanza algunos años, uno por uno, siguiendo la pedagogía»

Orden de NCETM (Spines 1, 2 y 3, por *Year*) y Common Core (3.NF, 4.NBT, 4.OA, 4.NF). Lo que falta de
**3.º** primero (las fracciones); luego **4.º** (más de mil, tablas del 11 y 12, resto, ×/÷ 10 y 100,
multiplicación y división cortas, décimas); luego **5.º**. Cada paso: plan en su diario → construir →
pruebas → commit. Carlos prueba por la mañana.

| # | Paso | Estándar / fuente | Prueba de dominio |
|---|---|---|---|
| 17 | ✅ **HECHO (6 oct, noche), falta la prueba de Carlos** — **F.1 La parte y el todo; fracciones unitarias** (`1/4 de 12`, `comparar: 1/3 y 1/5`) — `diario/2026-10-06-paso-F1-fracciones-unitarias.md` | NCETM 3.1, 3.2; 3.NF.A.1 | todas las parejas 1/2..1/12; 1/b de n |
| 18 | ✅ **HECHO (6 oct, noche), falta la prueba de Carlos** — `diario/2026-10-06-paso-F2-fracciones-no-unitarias.md`. **F.2 Fracciones no unitarias; en la recta; comparar** | NCETM 3.3; 3.NF.A.2, A.3 | todas las parejas que comparten arriba o abajo |
| 19 | ✅ **HECHO (6 oct, noche), falta la prueba de Carlos** — `diario/2026-10-06-paso-F3-sumar-restar-fracciones.md`. **F.3 Sumar y restar fracciones dentro de un entero** | NCETM 3.4 | todas las cuentas con b ≤ 12 |
| 20 | ✅ **HECHO (6 oct, noche), falta la prueba de Carlos** — `diario/2026-10-06-paso-N3-el-millar.md`. **N.3 El 1000 y los números de cuatro cifras** | NCETM 1.22; 4.NBT.A | los 10 000 nombres; comparar; descomponer; redondear; columnas |
| 21 | ✅ **HECHO (6 oct, noche), falta la prueba de Carlos** — `diario/2026-10-06-paso-M7-tablas-11-12.md`. **M.7 Tablas del 11 y del 12** | NCETM 2.11 | hasta 12 × 12 aprendido; divisibilidad 0–200 |
| 22 | ✅ **HECHO (6 oct, noche), falta la prueba de Carlos** — `diario/2026-10-06-paso-M8-division-con-resto.md`. **M.8 División con resto** | NCETM 2.12; 4.OA.A.3 | 2412 divisiones; interpretar el resto |
| 23 | ✅ **HECHO (6 oct, noche), falta la prueba de Carlos** — `diario/2026-10-06-paso-M9-por-10-y-100.md`. **M.9 Multiplicar y dividir por 10 y por 100** | NCETM 2.13; 3.NBT.A.3 | ×/÷ 10 y 100 hasta diez mil; decenas justas |
| 24 | ✅ **HECHO (6 oct, noche), falta la prueba de Carlos** — `diario/2026-10-06-paso-M10-multiplicacion-corta.md`. **M.10 Partir por sitios y la multiplicación corta** | NCETM 2.14; 4.NBT.B.5 | los 720 de dos cifras × una; muestra de 3–4 cifras |
| 25 | ✅ **HECHO (6 oct, noche), falta la prueba de Carlos** — `diario/2026-10-06-paso-M11-division-corta.md`. **M.11 La división corta** | NCETM 2.15; 4.NBT.B.6 | 1286 divisiones con la vuelta |
| 26 | ✅ **HECHO (7 oct, madrugada), falta la prueba de Carlos** — `diario/2026-10-07-paso-F4-mayores-que-un-entero.md`. **F.4 Más de un entero: números mixtos e impropias** | NCETM 3.5; 4.NF.B.3 | mixtos ↔ impropias; 250 cuentas; 200 comparaciones |
| 27 | ✅ **HECHO (7 oct, madrugada), falta la prueba de Carlos** — `diario/2026-10-07-paso-D1-decimas.md`. **D.1 Las décimas** | NCETM 1.23; 4.NF.C.6 | 300 cuentas, 300 comparaciones, redondeos |
| 28 | ✅ **HECHO (7 oct, madrugada), falta la prueba de Carlos** — `diario/2026-10-07-paso-D2-centesimas-milesimas.md`. **D.2 Centésimas y milésimas** | NCETM 1.24; 4.NF.C.5–7 | 300 cuentas, 300 comparaciones, 572 redondeos |
| 29 | ✅ **HECHO (7 oct, madrugada), falta la prueba de Carlos** — `diario/2026-10-07-paso-D3-dinero.md`. **D.3 El dinero (pesos y centavos)** | NCETM 1.25; 4.MD.A.2 | 200 cuentas de precios, 200 cambios |
| 30 | ✅ **HECHO (7 oct, madrugada), falta la prueba de Carlos** — `diario/2026-10-07-paso-F5-entero-por-fraccion.md`. **F.5 Multiplicar un entero por una fracción** | NCETM 3.6; 4.NF.B.4 | 300 productos |
| 31 | ✅ **HECHO (7 oct, madrugada), falta la prueba de Carlos** — `diario/2026-10-07-paso-G1-area-perimetro.md`. **G.1 Área y perímetro** | NCETM 2.16; 3.MD.C.7, 3.MD.D.8; 4.MD.A.3 | 144 rectángulos; polígonos; compuestas |
| 32 | ✅ **HECHO (7 oct, madrugada), falta la prueba de Carlos** — `diario/2026-10-07-paso-S1-veces.md`. **S.1 «Veces» y fracciones para comparar** | NCETM 2.17; 4.OA.A.1–2 | 160 problemas |
| 33 | ✅ **HECHO (7 oct, madrugada), falta la prueba de Carlos** — `diario/2026-10-07-paso-N4-hasta-un-millon.md`. **N.4 Hasta un millón** | NCETM 1.26; 4.NBT.A, 4.NBT.B.5 | 316 nombres ida y vuelta, fronteras, 60 comparaciones, 80 columnas, 30 rejillas |
| 34 | ✅ **HECHO (7 oct, madrugada), falta la prueba de Carlos** — `diario/2026-10-07-paso-N5-negativos.md`. **N.5 Los números negativos** | NCETM 1.27; 6.NS.C.5–7 | 1722 cuentas en la recta, comparaciones e intervalos de −20 a 20, 200 hasta ±1000 |
| 35 | ✅ **HECHO (7 oct), falta la prueba de Carlos** — `diario/2026-10-07-paso-M12-equivalencia.md`. **M.12 Usar la equivalencia para calcular** (doblar y partir por la mitad; cambiar los dos igual en ÷) | NCETM 2.18 | 200 productos, 578 divisiones, 452 igualdades, 200 huecos |
| 36 | ✅ **HECHO (7 oct), falta la prueba de Carlos** — `diario/2026-10-07-paso-M13-decimales-por-enteros.md`. **M.13 Multiplicar y dividir decimales por enteros** (contar en décimas; × 0.1 = ÷ 10; cambiar a la unidad más pequeña si sobra) | NCETM 2.19; 5.NBT.B.7 | 240 productos, 60 por 0.1/0.01, 250 divisiones, 100 entre 10/100, 18 cerca del techo |
| 37 | ✅ **HECHO (7 oct), falta la prueba de Carlos** — `diario/2026-10-07-paso-M14-tres-factores-volumen.md`. **M.14 Tres factores y volumen** (la pareja amiga primero: 25 x 7 x 4 = 100 x 7; las capas de cubitos; el problema inverso dividiendo) | NCETM 2.20; 5.MD.C.3–5 | 1575 tríos, 6 órdenes, 160 grandes, 120 con decimal, 40 cajas, 12 cubos, 80 inversos, 90 igualdades |
| 38 | ✅ **HECHO (7 oct), falta la prueba de Carlos** — `diario/2026-10-07-paso-M15-factores-multiplos-primos.md`. **M.15 Factores, múltiplos, primos y compuestos** (las parejas probando 1, 2, 3… y parando al cruzarse; la regla corta; la criba; los múltiplos contando; comunes; las parejas de 100) | NCETM 2.21; 4.OA.B.4 | los factores de 1 a 168, primo o compuesto de 0 a 168, la criba, múltiplos de 1 a 12, 450 «múltiplo/factor», 144 múltiplos comunes, 60 números grandes |
| 39 | ✅ **HECHO (7 oct), falta la prueba de Carlos** — `diario/2026-10-07-paso-M16-combinar-operaciones.md`. **M.16 Combinar la multiplicación con la suma y la resta** (sin paréntesis, la x primero; con paréntesis, lo de dentro; + y - de izquierda a derecha; sacar el factor común) | NCETM 2.22; 5.OA.A.1 | 8 formas × 45 contra el testigo, 344 con factor común, 80 cadenas de + y -, 240 con decimales, 80 igualdades, cerca del millón y el tiempo |
| 40 | ✅ **HECHO (7 oct), falta la prueba de Carlos** — `diario/2026-10-07-paso-S2-parte-parte-todo.md`. **S.2 Las estructuras comunes: parte-parte-todo con tres partes o más** (falta el todo: en orden, las parejas amigas, partes iguales; falta una parte: una a una o juntando lo que se sabe; partes iguales que faltan: repartir; los contextos del `.kn`: perímetro, dinero, camino…) | NCETM 1.28; Put Together/Take Apart; 4.MD.A.3 | 150 todos y 150 partes de 2 a 6 partes, 160 con decimales, 112 de partes iguales, trampas, 9 contextos, piezas trucadas, cerca del millón y el tiempo |
| 41 | ✅ **HECHO (7 oct), falta la prueba de Carlos** — `diario/2026-10-07-paso-P7-compensacion.md`. **P.7 Usar la equivalencia y la compensación para calcular** (la misma suma: 4997 + 2456 = 5000 + 2453; la misma diferencia: 1000 − 397 = 1003 − 400; quitar de más y devolver; derivar de un hecho: si 600 − 200 = 400, 600 − 201 = 399; ver la igualdad sin calcular; la balanza con restas; con decimales) | NCETM 1.29; 4.NBT.B.4, 1.OA.D.7 | 150 sumas, 150 restas, 80 derivaciones, 100 igualdades, 80 balanzas, 60 con decimales, piezas trucadas, cerca del millón y el tiempo |
| 42 | ✅ **HECHO (8 oct), falta la prueba de Carlos** — `diario/2026-10-08-paso-F6-fracciones-equivalentes.md`. **F.6 Fracciones equivalentes y simplificar** (la familia multiplicando arriba y abajo por el mismo; simplificar paso a paso, de una vez si el pequeño cabe justo, o con el mayor factor común; la forma más simple con los «trozos grandes»; el hueco por la relación horizontal, la vertical o simplificando primero; ¿son equivalentes?; comparar 3/12 y 1/4) | NCETM 3.7; 4.NF.A.1 | las 576 fracciones de 1/1 a 24/24, 120 hasta 1400, 80 hasta 1000 y 40 hasta el millón (bien o «todavía no», nunca mal), cada método, 120 huecos, 100 parejas con trampas, 10 familias, piezas trucadas, cerca del techo y el tiempo |
| 43 | ✅ **HECHO (8 oct), falta la prueba de Carlos** — `diario/2026-10-08-paso-F7-el-mismo-de-abajo.md`. **F.7 El mismo de abajo: sumar, restar y comparar con distinto de abajo** (relacionadas: cambiar solo una, 1/2 + 1/4 = 2/4 + 1/4; no relacionadas: el producto de los de abajo, 1/3 + 1/4 = 4/12 + 3/12; simplificar al final; mixtos; el error típico 1/2 + 1/3 ≠ 2/5 porque 2/5 < 1/2; comparar por el mismo de abajo y por el mismo de arriba) | NCETM 3.8; 5.NF.A.1–2 | 220 sumas y restas de unitarias, 250 no unitarias, con décimos/centésimos/milésimos, 60 con impropias, 200 comparaciones + los dos caminos siempre de 2 a 12, 100 mixtos, piezas trucadas, cerca del millón y el tiempo |
| 44 | ✅ **HECHO (8 oct), falta la prueba de Carlos** — `diario/2026-10-08-paso-N6-diez-millones.md`. **N.6 Hasta diez millones: el millón como una cosa** (primer paso de 6.º; el techo de los números sube a diez millones; los nombres con millón/millones; la estructura y los patrones de las potencias de diez; cruzar el millón: 997 000 + 5 000 completando el millón, 1 002 000 − 997 000 contando hacia arriba; 2 millones + 3 millones; redondear al millón, con la trampa de la cadena) | NCETM 1.30; Year 6 (números hasta 10 000 000) | 415 nombres ida y vuelta, fronteras, 60 comparaciones, 80 columnas de siete cifras, 120 sumas y restas que cruzan un millón, piezas trucadas, 120 redondeos, 60 ×/÷ cortas, cerca del techo y el tiempo |
| 45 | ✅ **HECHO (8 oct), falta la prueba de Carlos** — `diario/2026-10-08-paso-S3-dos-incognitas.md`. **S.3 Problemas con dos incógnitas** (una, varias o ninguna; la barra alineada; suma y diferencia: quitar la diferencia y repartir en dos, 30 − 8 = 22, 22 : 2 = 11; suma y múltiplo: 3 + 1 = 4 trozos; diferencia y múltiplo: 3 − 1 = 2 trozos; probar en orden cuando no se deja dibujar —una ecuación pone el tope, la otra se comprueba—; una suma sola: una pareja más que la suma; una relación sola: infinitas; los enunciados «entre los dos» y «más que» de R.1) | NCETM 1.31; Year 6 | 30 trampas, 140 sumas y diferencias contra el testigo (112 bien, 28 medios de siete cifras «todavía no», ninguna mal; las dos estrategias de acuerdo), 40 con milésimas, 115 de múltiplo, 186 probando en orden contra el testigo que prueba todo, una sola ecuación, lo que no es de este paso, piezas trucadas, 30 problemas con palabras, cerca del techo y el tiempo |
| 46 | ✅ **HECHO (9 oct), falta la prueba de Carlos** — `diario/2026-10-09-paso-M17-multiplicacion-larga.md`. **M.17 Estrategias para multiplicar números grandes y la multiplicación larga** (primer paso tras el plan U; todo PIEZAS de `multiplicar`, sin puerta nueva: entran por el modelo común. Quitar los ceros y volver a ponerlos: 234 x 30 = 234 x 3 y un 0; partir UNO de los factores: 326 x 47 = 326 x 40 + 326 x 7; un factor compuesto: 1234 x 24 = 1234 x 4 x 6; la LARGA: una fila por cifra con los 0 que guardan el sitio, y se suman; cada pieza se comprueba con la operación contraria —cada fila : 10 y : su cifra, la suma restando—; el resolvedor dice con qué multiplicó y comprueba DESHACIENDO: `n : 24 = 356` → 8544 porque 356 x 24 = 8544) | NCETM 2.23; 5.NBT.B.5 | 4 piezas contra el testigo con su vuelta (90 productos), qué elige el control (10 casos), ceros y unos en medio, el techo, piezas trucadas (el 0 olvidado, lo que se lleva), 11 por la tabla de puertas y el resolvedor, comprobar deshaciendo de verdad, lo que sigue siendo 2.24, el tiempo |
| 47 | ✅ **HECHO (9 oct), falta la prueba de Carlos** — `diario/2026-10-09-paso-M18-division-larga.md`. **M.18 Dividir entre dos cifras: la división larga** (todo PIEZAS de `dividir`, sin puerta nueva. El cociente menor que 10: contar en múltiplos del divisor, como antes; la LARGA: la lista de múltiplos sumando, el que cabe en cada sitio, restar debajo y bajar la cifra, el 0 del cociente; usando los FACTORES del divisor: 8544 : 24 = 8544 : 4 : 6; cada pieza se comprueba multiplicando. Los «todavía no» que pedían la larga ahora salen por el modelo común: ecuaciones, factores y primos hasta 99 x 99, comprobar tres factores dividiendo, simplificar; entre tres cifras, todavía no) | NCETM 2.24; 5.NBT.B.6, 6.NS.B.2 | 2 piezas contra el testigo con su vuelta (85 divisiones), qué elige el control (8 casos), ceros en el cociente y el techo, piezas trucadas (el 0 olvidado, la resta), 13 por el modelo común, sin las tablas, el tiempo |
| 48 | ✅ **HECHO (9 oct), falta la prueba de Carlos** — `diario/2026-10-09-paso-M19-compensar.md`. **M.19 Calcular compensando** (todo PIEZAS de `multiplicar`, sin puerta nueva, elegidas por su costo: REDONDEAR UN FACTOR y quitar los grupos de más, 399 x 6 = 400 x 6 − 6, 98 x 37 = 3700 − 74, solo si el factor está a 1 o 2 por debajo de un redondo de una cifra; POR 5 O 25: x 10 y la mitad, x 100 y la mitad de la mitad, 25 x 37 = 3700 : 4; cada pieza se comprueba con las operaciones contrarias. Lo de sumar y restar compensando (4997 + 2345) ya era de P.7; los puntos 2 y 3 del segmento, de M.9 y M.12) | NCETM 2.25 | 2 piezas contra el testigo con su vuelta (~50 productos), qué elige el control y lo que no roba (15 casos), piezas trucadas (al revés, quitar 1 en vez de un grupo, una mitad sola), el techo, 7 por el modelo común, P.7 igual, sin las tablas, el tiempo |
| 49 | ✅ **HECHO (9 oct), falta la prueba de Carlos** — `diario/2026-10-09-paso-M20-la-media.md`. **M.20 La media** (PIEZAS de la pregunta nueva `media`, que el resolvedor pide al ver `(v1 + … + vk) : k` con k = cuántos valores; sin puerta nueva: se pregunta con `resolver:`. JUNTAR Y REPARTIR: 3 + 4 + 6 = 13, 13 : 3 = 4 y 1/3; NIVELAR sobre el más bajo, solo si están cerca (el costo): 98, 102, 100, 104 → encima 12, 12 : 4 = 3, 101; cada pieza se comprueba —media x cuántos + lo que sobra = el total; el EQUILIBRIO—. El cero cuenta; el valor que falta y el reparto igual ya salían deshaciendo) | NCETM 2.26; 6.SP.A.3 | 2 piezas contra el testigo con su vuelta (~35 medias, enteras y no enteras), qué elige el control (8 casos), piezas trucadas (repartir solo entre los de arriba, olvidar el trozo, olvidar el cero, tirar lo que sobra, juntar mal), 7 por el resolvedor, el techo, lo que no cambia, el tiempo |
| 50 | ✅ **HECHO (9 oct), falta la prueba de Carlos** — `diario/2026-10-09-paso-M21-escala-y-razon.md`. **M.21 El factor de escala y la tabla de razón** (PIEZAS de la pregunta nueva `proporcion`, que el resolvedor pide al ver `a : b = c : ?` con la letra sola en uno de los cuatro sitios; sin puerta nueva: «2 es a 5 como 6 es a ?» se escribe con el signo de dividir. ENTRE LAS FILAS, el factor de escala: de 2 a 6 es x 3, 5 x 3 = 15 (y hacia abajo, : k); DENTRO DE LA FILA: 3 | 12 es x 4, 7 x 4 = 28; PASANDO POR UNA FILA MÁS PEQUEÑA (F.6): 6 | 9 = 2 | 3, x 5 → 15; elegidas por su costo; cada pieza se comprueba deshaciendo con la contraria. Si no sale justo, como antes. Combinaciones y el factor de dos figuras ya salían) | NCETM 2.27; 6.RP.A.3a; 7.G.A.1 | 3 piezas contra el testigo con su vuelta (42 tablas), qué elige el control (10 casos), piezas trucadas (sumar en vez de multiplicar, la columna equivocada, al revés, mezclar las columnas, dividir una sola columna), 9 por el resolvedor, el techo, lo que no cambia, el tiempo |

## EL PLAN ANTERIOR (5 oct, tarde) — sustituido por el de arriba en el orden; se conserva como referencia

**Nota de Carlos (5 oct):** «no nos concentramos en la parte hablada, porque después los
problemas más complejos no tendrán enunciados largos sino la **ecuación directamente y algunas
palabras**». → El centro pasa a ser **la ecuación con hueco**; el lenguaje rústico se queda como
está y se adapta solo cuando haga falta.

Cada paso con su investigación pedagógica, sus trampas, su prueba de dominio y su commit.

| Paso | Qué | Por qué en este orden | Prueba de dominio |
|---|---|---|---|
| **0** | **Deuda**: las condiciones de aplicación que aún miran tamaños con Python, al mecanismo | que NADA del sistema use calculadora antes de crecer | todo verde y la auditoría de aritmética limpia |
| ✅ **P.3** | **HECHO el 5 oct: la memoria de hechos** — ver `diario/2026-10-05-paso-3-memoria.md` | Baroody: contar → razonar → **dominio**; la memoria llega después del razonamiento | 200 hechos aprendidos con dos caminos; un recuerdo falso no se usa |
| ✅ **P.4** | **HECHO el 5 oct** (ver `diario/2026-10-05-paso-4-tecnicas.md`). **Técnicas para ir más rápido** como piezas: dobles y casi dobles (6+7 = 6+6+1), compensación (29+14 = 30+13), de diez en diez (47+30) | los hechos derivados de NRC/Baroody; cada técnica = una pieza con sus condiciones | cada técnica gana donde encaja y se descarta con su porqué donde no |
| **E.1** | **Ecuaciones con hueco de suma y resta**: `8 + ? = 13`, `? - 4 = 9`, `13 = ? + 5` | son los 11 tipos de CGI escritos en símbolos: el hueco en cada sitio pide un conocimiento distinto (operar, contar desde, la vuelta) | huecos en las 3 posiciones, con `=` a la izquierda y a la derecha |
| **E.2** | **El `=` como balanza**: `8 + 4 = ? + 5` | el error más documentado del `=` es leerlo como «pon el resultado» (8+4=12+5) | las trampas `8 + 4 = ? + 5` → 7 (no 12 ni 17) |
| ✅ **E.3** | **HECHO el 5 oct como PIEZAS (idea de Carlos)** — ver `diario/2026-10-05-paso-2-piezas.md`. Lo de abajo era la propuesta original: **Los conocimientos como DATOS**: cada conocimiento del resolvedor declara su situación, sus condiciones y su operación en el `.kn`; el código solo los recorre | para que la multiplicación y la división entren **sin programar el resolvedor** (es R.3: enseñarle algo nuevo = escribirlo) | añadir un conocimiento nuevo solo con datos, y que el resolvedor lo use |
| **M.1** | **Multiplicar = grupos iguales** (contar de n en n, mecánico: saltos en la lista) | lo que la investigación pone primero: grupos iguales antes que la tabla | `3 grupos de 4`, `3 × 4 = ?` |
| **M.2** | **Matrices y conmutatividad** (3×4 = 4×3), dobles, ×10 como decenas (6.2) | los hechos derivados de la multiplicación, como derivar en la suma (7.2) | sin memoria: cada hecho sale de otro |
| **M.3** | **Dividir**: repartir (¿cuántos le tocan a cada uno?) y agrupar (¿cuántos grupos salen?) | las dos estructuras de la división (partitiva y cuotativa) | las dos, y la vuelta con la multiplicación |
| **E.4** | **Ecuaciones con × y ÷**, y **dos pasos**: `3 × ? + 2 = 14` | combinar: la respuesta de un paso es el dato del siguiente | huecos en todas las posiciones |
| **E.5** | **La letra como hueco**: `x + 5 = 12` | el puente al álgebra: la letra es un hueco con nombre | lo mismo que E.1–E.4 con letras |

Lo que queda **fuera** a propósito: entender frases largas en lenguaje natural.

## Fase 3 — lenguaje matemático, métodos y condiciones de aplicación (niveles 6 y 7)
- Nivel 6: terminología y símbolos (sumando, minuendo, divisor…), **cada palabra con su uso**.
- Nivel 7: métodos alternativos (descomposición, cálculo por decenas…) y **cuándo conviene cada uno**.
- Prueba de dominio: dos métodos distintos para el mismo cálculo, y el sistema explica cuál eligió y por qué.

## Fase 4 y siguientes — se planifican cuando la Fase 1 esté cerrada
Álgebra (8), conjuntos (9), geometría (10), representación técnica (11), lógica y demostración (12),
crecimiento autónomo (13). **No se detallan todavía**: se detallan cuando toque, con lo aprendido.

---

## Investigación pedagógica (obligatoria antes de diseñar cada nivel)

Antes de programar la enseñanza de un concepto, buscar en internet **cómo se enseña ese concepto a
niños** y citar la fuente. Pistas de partida: método Montessori (materiales y secuencia), método de
Singapur (concreto → pictórico → abstracto), regletas de Cuisenaire, recta numérica, "subitizing"
(reconocer cantidades pequeñas de un vistazo), y los errores típicos documentados del conteo infantil
(no establecer correspondencia uno a uno, saltarse objetos, no entender que el último número es el total).

**Lo que se busca no es copiar un método, sino sacar la secuencia correcta de conceptos y los errores
típicos, para diseñar las pruebas de dominio con eso.**

---

## Decisiones ya tomadas (por Carlos)

- Nada de voz: solo texto.
- Python primero; C/GPU solo si una razón medida lo justifica.
- Todo por partes pequeñas; las fases se subdividen si hacen falta.
- Al principio no aprende solo: lo que se le enseña, lo entiende y sabe usarlo.
- El documento original es un **punto de partida**, no un texto definitivo: se afina entre Carlos y Euclides.
- **(3 oct 2026) «Saber resolver» = aplicar lo que sabe y combinaciones, con descarte razonado.** No es
  elegir la operación por la palabra. Ver la nota de la Fase 2.
- **(3 oct 2026) Contar hasta 100 va ANTES de multiplicación y división.** Hecho en la **6.1**
  (y sigue: 6.2 agrupar de diez → 6.6 calcular con decenas y unidades).
- **(3 oct 2026) No hay atajos de sintaxis que parezcan notación de otro nivel** (p. ej. rangos `a..j`
  para no escribir los objetos: se escriben uno a uno).

## ✅ PLAN U CUMPLIDO (9 oct, Carlos): se vuelve al orden de NCETM en 6.º (2.23 → M.17, fila 46 de arriba). Desde aquí,
lo nuevo entra por el MODELO COMÚN: técnicas nuevas = piezas que el resolvedor usa; ninguna puerta ni formato nuevo.

## (HECHO) PAUSA DEL AVANCE POR AÑOS (8 oct, decisión de Carlos): PLAN U — volver universal lo que ya sabe
Antes de seguir con NCETM 2.23, se hace universal lo que hay: una representación común (cantidades, relaciones, lo
que se pide), un lector único, un buscador con control y un examen de transferencia con problemas no vistos.
Plan entero: `diario/2026-10-08-PLAN-U-volverlo-universal.md`. Fases: U.1 el modelo y el lector simbólico · U.2
buscar con control · U.3 el lector de palabras · U.4 una sola tabla de puertas · U.5 el examen de transferencia.

| Fase | Estado | Qué | Prueba |
|---|---|---|---|
| U.1 | ✅ **HECHO (8 oct), falta la prueba de Carlos** — `diario/2026-10-08-paso-U1-modelo-y-lector-simbolico.md` | El NÚMERO común (entero, decimal, fracción, negativo; las cuentas con las piezas de siempre), el lector único (varias letras, `;`, paréntesis, fracciones, decimales, negativos, `2n`), calcular despejando (deshacer o contar trozos), sustituir, la comprobación en las relaciones de partida, el presupuesto; puerta `resolver:` y red de seguridad | `test_U1` 63/63 (los seis ejemplos del plan, el lector, 40 cuentas mezcladas contra el testigo, trampas, puertas viejas sin cambiar, despeje trucado, tiempo) |
| U.2 | ✅ **HECHO (8 oct), falta la prueba de Carlos** — `diario/2026-10-08-paso-U2-buscar-con-control.md` | Parte `buscar.py`: los trozos con varias letras; JUNTAR relaciones (restar, sumar o quitar K veces), REESCRIBIR (un bloque que ya se sabe, sacar factor común), PROBAR EN ORDEN con tope humano y sabiendo cuándo parar (`n x n = 49`, `a x b = 24; a + b = 10`, dos relaciones no lineales); el CONTROL por medios y fines (lo que deja y lo que cuesta, en `universal.kn`); la explicación con barras. S.3 lee con el lector único (traductor al modelo); S.2 se dice como el modelo y el resolvedor es otra estrategia que coincide. Los dos fallos de la revisión de U.1: la red de seguridad también con «todavía no» (si hay una relación con letras) y «de» = POR (`3/4 de 20`) | `test_U2` 42/42 (cada operador contra el testigo, el control, el tope, los dos fallos, los traductores, el tiempo) |
| U.3 | ✅ **HECHO (8 oct), falta la prueba de Carlos** — `diario/2026-10-08-paso-U3-lector-de-palabras.md` | El vocabulario en DATOS (`frases.kn`: valor, suma, comparar sumando y multiplicando, cambio, dar, comprar y la vuelta, repartir, cada, momentos en orden, preguntas, unidades) y las estructuras (`relaciones.kn`: parte-todo, cambio, comparar, grupos iguales, figuras, consecutivos); parte `palabras.py`: frases núcleo y elipsis, la pregunta como una frase más, sujeto-verbo-objeto → relaciones, el tiempo, lo que sobra no estorba, la frase que no se entiende, lo razonable; la red de seguridad de las palabras. R.1, R.2, escala, temperatura, dinero, área, perímetro y volumen: una muestra de 30 por el lector nuevo da lo mismo | `test_U3` 51/51 (cada clase del vocabulario, el tiempo, grupos y precio, lo que se sabe, el orden y lo que sobra, lo que no se entiende, lo razonable, las puertas, la muestra vieja, el vocabulario en datos, el tiempo) |
| U.3b | ✅ **HECHO (8 oct), falta la prueba de Carlos** — `diario/2026-10-08-paso-U3b-la-cosa-de-cada-cantidad.md` | LA COSA DE CADA CANTIDAD (tras la revisión de U.3, que halló respuestas falsas): cada cantidad es (de quién, de qué cosa); solo se suman o restan las de la misma cosa (Schwartz 1988) y la comprobación final lo mira; «cada», «por», «N de X cada uno», los verbos de cada («3 cuadernos cuestan 12») = grupos iguales, y lo de cada grupo multiplica los grupos de alguien (el camión); la proporción simple; comprar es gastar; «me sobra», «le queda», «qué temperatura»; «un lado / el otro»; «A por B por C»; «la mitad de lo que tenía», «3/4 de lo que había bajado». Las cosas genéricas, los verbos de cada y las parejas de las figuras, en datos | `test_U3b` 29/29 (dos cosas de alguien, en total de una cosa, cosas mezcladas → no entiendo, la comprobación trucada, grupos iguales de cada forma, la proporción, las preguntas, las figuras, lo que había, nada viejo cambia, el vocabulario en datos, el tiempo) |
| U.4 | ✅ **HECHO (8 oct), falta la prueba de Carlos** — `diario/2026-10-08-paso-U4-una-sola-tabla-de-puertas.md` | UNA SOLA TABLA DE PUERTAS (parte `puertas.py`): `explicar_pregunta` y `responder_pregunta` recorren la misma tabla y deciden con la misma regla; lo escrito con números y símbolos lo decide el modelo común (si una puerta vieja no da una respuesta, el resolvedor; «ningún número para contar» es respuesta del año y se enseña también lo del resolvedor); E.5 traductor (lee con el lector único); `ecuacion:` y `calcular:` no cogen lo que no saben leer (daban respuestas falsas); IDENTIDADES (desarrollar con la distributiva: cualquier número / ninguna); la PRUDENCIA con palabras (un número que sobra y cuenta lo mismo que la pregunta, una frase con un dato que no se entiende → no entiendo). Decisión de Carlos: «cuanto más se avanza, menos se habla»; U.3c descartada | `test_U4` 48/48 (una tabla, el diagnóstico, la red y el año, identidades, E.5 traductor, las falsas, el comparador sin diferencias sin explicar, la prudencia, 20/20 problemas simbólicos nuevos, el tiempo) |
