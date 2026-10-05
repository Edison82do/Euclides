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
