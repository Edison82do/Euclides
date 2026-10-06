# PROGRESO de Euclides — qué está hecho, qué falla, qué toca

> **Regla:** este archivo se **lee al empezar** cada sesión y se **actualiza al terminar**. Si no se
> actualiza, el proyecto deja de ser acumulativo también para ti.

**Última actualización:** 5 de octubre de 2026 — revisión de Claude (Cowork): git, motor partido en
`sistema/partes/`, unidades **6.7** y **7.6** cerradas, fallos de `restar_numeros`/`diferencia_numeros`
arreglados, y **R.1 (el resolvedor)** abierta. Ver `diario/2026-10-05-*.md`.

## Estado por unidades

| Unidad | Estado | Prueba de dominio | Fecha | Notas |
|---|---|---|---|---|
| 0.1 Objetos individuales | **CERRADA** | 8/8 VERDE (2 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-0.1.md` |
| 0.2 Grupos (por atributo) | **CERRADA** | 12/12 VERDE (6 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-0.2.md` |
| 0.3 Pertenencia | **CERRADA** | 13/13 VERDE (5 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-0.3.md` — **Nivel 0 completo** |
| 1.0 Subitizing | **CERRADA** (aislada) | 13/13 VERDE (4 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-1.0.md`. **OJO: pendiente de conectar** — el sistema no ve, la figura se escribe a mano. Ver `diario\2026-10-03-observacion-no-ve.md` |
| 1.1 Cantidad | Aplazada | — | — | Aplazada por acuerdo con Carlos (2026-10-03): sin percepción, quedaría colgada. Ver nota en `PLAN.md` |
| 2.1 Correspondencia uno a uno | **CERRADA** | 15/15 VERDE (7 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-2.1.md`. **Primera unidad que DEDUCE algo** |
| 2.2 Secuencia de conteo (orden estable) | **CERRADA** | 24/24 VERDE (7 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-2.2.md` |
| 2.3 Contar y determinar la cantidad | **CERRADA** | 14/14 VERDE (4 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-2.3.md`. **El sistema ya dice cuántos hay** |
| 2.4 Cardinalidad (Give-N) | **CERRADA** | 36/36 VERDE (11 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-2.4.md` y `diario\2026-10-03-correccion-dame-monton.md`. **El PRINCIPIO: coge del montón la cantidad pedida** |
| 2.5 Orden irrelevante | **CERRADA** | 29/29 VERDE (10 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-2.5.md`. **Reglas lógicas vs convencionales; pseudoerror vs compensación** |
| 2.6 Abstracción | **CERRADA** | 22/22 VERDE (6 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-2.6.md`. **NIVEL 2 COMPLETO** |
| 3.1 Símbolos (cifras 1..9) | **CERRADA** | 31/31 VERDE (9 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-3.1.md`. **Primera vez que el sistema usa CIFRAS** — Nivel 3 abierto |
| 3.2 El cero | **CERRADA** | 15/15 VERDE | 2026-10-03 | `diario\2026-10-03-unidad-3.2.md`. **El vacío deja de ser «no se puede decidir»: ahora es una cantidad** |
| 3.3 Secuencia numérica | **CERRADA** | 31/31 VERDE (11 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-3.3.md`. **DOS listas: la de contar y la de números.** Aquí se arregló el fallo que cazó Carlos |
| 3.4 El puente | **CERRADA** | 32/32 VERDE (8 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-3.4.md`. **NIVEL 3 COMPLETO.** Los 6 caminos; el subitizing (1.0) por fin conectado |

**NIVEL 3 (Números) COMPLETO: 3.1 símbolos · 3.2 el cero · 3.3 secuencia · 3.4 el puente.**

## Nivel 4 — Relaciones (alcance decidido por Carlos, 2026-10-03)

**Decisión de Carlos:** «primero relacionar **cantidades** y después **números**».

Y la investigación lo respalda (NCETM 2023): *los niños deben aprender a comparar cantidades
**antes** de comparar los números abstractos que las representan*. Así que el nivel va en dos pasos:

| Unidad | Objetivo | Cómo se dice |
|---|---|---|
| **4.1 Comparar cantidades** | `comparar: <colección> / <colección>` | en **palabras**: `mas` / `menos` / `tantos_como` |
| **4.2 Comparar números** | `comparar_cifras: <cifra> / <cifra>` | con los **símbolos** `>`, `<`, `=` |
| **4.1 Comparar cantidades** | **CERRADA** | 33/33 VERDE (10 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-4.1.md`. Decide **emparejando** y **verifica contando**. **El tamaño no cuenta** |
| 4.2 Comparar números | **CERRADA** | 29/29 VERDE (7 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-4.2.md`. **Los símbolos `>`,`<`,`=`**; y **las 100 parejas cuadran con las cantidades** |
| 5.1 Componer y descomponer | **CERRADA** | 31/31 VERDE (8 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-5.1.md`. **Las partes y el todo**: el cimiento de la suma. Sin signos todavía |

**Por qué así y no al revés:** de las fuentes, dos cosas que fijan el diseño —
- Los símbolos `=` `<` `>` **solo se usan entre cifras** (National Academy): comparar cantidades se
  dice con palabras; el símbolo llega con los números. Por eso 4.1 no lleva símbolos.
- Se compara **primero perceptualmente, después numéricamente**, y cuesta aprender a **ignorar el
  tamaño de los objetos** (Learning Trajectories, Sarama & Clements). Eso da la trampa de la 4.1.

## Nivel 5 — Operaciones

**Decisión de Carlos:** «**si, componer y descomponer**» (en vez de entrar directo por la suma).

La investigación lo respalda: **componer y descomponer es el cimiento de la suma y la resta** —
*«partir números y volverlos a juntar sostiene la comprensión de la suma y la resta como operaciones
inversas»* (NCETM). Y las trayectorias (Clements & Sarama) lo sitúan **antes** de la suma.

| Unidad | Objetivo | Estado |
|---|---|---|
| **5.1 Componer y descomponer** | `descomponer: <colección>` / `componer: <col> / <col>` | **CERRADA** 31/31 |
| 5.2 La suma | **CERRADA** | 40/40 VERDE (10 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-5.2.md`. **El `+` y el `=`**; el `=` es **equivalencia**. Dos estructuras: **agregación** y **aumentación** |
| **5.3 Las tres entradas** | **CERRADA** | 54/54 VERDE (16 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-5.3.md`. **Los tres grupos separados** (cantidad / cifra / palabra). Arregla el **fallo grave** que cazó Carlos |
| **5.4 La resta (quitar)** | **CERRADA** | 41/41 VERDE (16 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-5.4.md`. **La reducción**: primero/luego/ahora, el signo `-`, los términos y **la vuelta verifica** |
| **5.5 La diferencia** | **CERRADA** | 38/38 VERDE (14 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-5.5.md`. **La tercera y última estructura de la resta**: el HUECO entre dos. **No se quita nada**; el mismo número responde a «cuántos más» y «cuántos menos»; se escribe de **dos maneras** |
| **6.1 Contar hasta 100** | **CERRADA** | 75/75 VERDE (14 trampas) | 2026-10-03 | `diario\2026-10-03-unidad-6.1.md`. **Los 100 nombres se CONSTRUYEN con la regla** (24 memorizadas + 3 formaciones). El **error de decena** explicado. Y **el techo de diez subió a cien en TODO el sistema** |
| **7.1 El método de los dedos** | **CERRADA** | 35/35 VERDE | 2026-10-04 | `diario\2026-10-04-unidad-7.1.md`. **El mecanismo de sumar** (decisión de Carlos: mecánico hasta nuevo aviso): se **anota** el primero (la pizarra = memoria de trabajo), se cogen los dedos del segundo, se **cuenta hacia adelante**, y el último número dicho es el total. Y enseña **por qué** (5 pasos frente a 13) |
| **7.2 Derivar (hacer diez)** | **CERRADA** | 255/255 VERDE | 2026-10-04 | `diario\2026-10-04-unidad-7.2.md`. **La OTRA vía para sumar, y no cuenta nada**: al primero le faltan unos para diez, se **parte** el segundo en esos y el resto, se hace diez y se suma lo que sobra (`7+5` → `7+3+2`). **Derivar es COMBINAR lo que ya se sabe** (partir 5.1 + llegar a diez 6.1). Y el sistema **prueba LAS DOS vías** (decisión de Carlos) y comprueba que dan lo mismo. Limitado a **una cifra**: con dos, `necesito_las_columnas` |
| **6.2 Agrupar de diez en diez** | **CERRADA** | 957/957 VERDE | 2026-10-04 | `diario\2026-10-04-unidad-6.2.md`. **El diez como UNA cosa** (el «unitising» de NCETM): los objetos se cogen de diez en diez y cada montón es **una decena**. Es **lo que hace posible el valor posicional** y el paso al pensamiento multiplicativo. Con el **error típico de Oak** dentro (no seguir contando de diez en diez al llegar a las unidades). Y **comprueba que el orden no cambia el valor** agrupando al revés |
| **6.3 La tabla de 100** | **CERRADA** | 956/956 VERDE | 2026-10-04 | `diario\2026-10-04-unidad-6.3.md`. **El sistema YA LEE cifras de dos dígitos** (`47` → `cuarenta y siete`) y da el **sitio** de cada número (fila = decenas, columna = unidades). Y lo más importante: **una sola verdad** — el mismo número se lee igual por **todas** las puertas. Antes había **cuatro puertas que decían que no sabía** (`cifra_de`, `comparar_cifras`, `comparar_numeros`, `dedos`); arregladas |
| **6.5 Partir en decenas y unidades** | **CERRADA** | 858/858 VERDE | 2026-10-04 | `diario\2026-10-04-unidad-6.5.md`. **Cuánto vale cada cifra**: `47` = 4 decenas + 7 unidades = **40 + 7** (el 4 vale **cuarenta**, no cuatro). Con el **error típico de Oak** dentro (*«transponer los dígitos»*: sumar `4+7=11`). Y los **nombres raros**: `juntar_decenas: 3 / 12` son **cuarenta y dos**, no «treinta y doce» (NZ Maths). **Es el requisito de las columnas** (lo dice Oak) |
| **7.3 Sumar por columnas** | **CERRADA** | 43387/43387 VERDE | 2026-10-04 | `diario\2026-10-04-unidad-7.3.md`. **La nota 7 de Carlos, literal**: unidad con unidad, decena con decena, y **el llevarse**. Y el llevarse **no es un truco: es re-agrupar** (diez unidades hacen una decena, unidad 6.2). Prueba de hierro: **las 5151 parejas del rango entero** (todo a+b ≤ 100). Y **`sumar_numeros:` con dos cifras ya funciona** usando este método |
| **7.4 La resta con los dedos** | **CERRADA** | 25/25 VERDE (+ las 66 parejas) | 2026-10-04 | `diario\2026-10-04-unidad-7.4.md`. **La nota 3 de Carlos**: se toma **EL PRIMERO** con los dedos, se van **BAJANDO** los del segundo, y los que quedan son el resultado. Es **el mecanismo de la 5.4** y el gemelo de la 7.1, pero **al revés** (contar atrás). Se verifica por **la vuelta** (la suma deshace la resta). Y **reutiliza** la condición de la 5.4 en vez de escribir otra |
| **7.5 Restar por columnas** | **CERRADA** | 30/30 VERDE (+ las 5151 parejas) | 2026-10-04 | `diario\2026-10-04-unidad-7.5.md`. **El par de la 7.3**: `columnas: 72 - 45` → 27. Si las unidades de arriba **no llegan**, **NO se da la vuelta a la resta** (el error nº1 de la resta: `5-2=3` sería falso); se **CAMBIA una decena por diez unidades** (72 = 6 dec y 12 u). **Y no es un préstamo**: no se devuelve nada. Es **la misma moneda que el llevarse de la 7.3, al revés**. Y **los tres errores típicos documentados dentro** (34, 36, 24) |
| La resta por columnas | **CERRADA (7.5)** | — | — | — |
| **6.7 La centena** | **CERRADA** | 39/39 VERDE (los 1001 números por 7 puertas) | 2026-10-05 | `diario\2026-10-05-unidad-6.7-y-7.6.md`. **La escalera** (10 d = 1 c), centenas/decenas/unidades, el cero **marcador**, **204 tiene 20 decenas**, nombres de tres cifras (irregulares y cien/ciento). `centena`, `centena:`, y `sitio:`/`partir:` de 101 a 1000. **Una sola verdad** en `nombre:`/`numero:` |
| **R.1 El resolvedor** | **ABIERTA (prototipo, pendiente del OK de Carlos)** | 49/49 VERDE (4356 problemas generados) | 2026-10-05 | `diario\2026-10-05-unidad-R.1.md`. **La nota de Carlos del 3 oct**: `problema: <enunciado>`. Lee con FORMAS (`enunciados.kn`, sin adivinar), prueba los **nueve** conocimientos en cada paso y **descarta con su porqué** (`resolver_r1.kn`), combina pasos, calcula por columnas y verifica por la vuelta. **«Más» puede ser resta** y lo avisa. Dice `no_entiendo` / `no_se_resolver` / `sin_solucion` en vez de inventar |
| **7.6 Columnas con la centena** | **CERRADA** | 46/46 VERDE (8072 sumas + 29275 restas) | 2026-10-05 | Mismo diario. **La nota 7 entera**: «y luego centena con centena». Llevadas en cualquier columna, **restar a través de un cero** (500−247: 4 c, 9 d, 10 u), cada columna con su mecanismo (**cero cajas negras**). 7.3/7.5 solo desvían lo que no sabían |
| 6.4 Comparar de dos cifras | Pendiente | — | — | Casi hecho con la 6.3 (`comparar_cifras: 47 / 3` ya funciona); falta decidir si es unidad propia |
| 6.6 Calcular con decenas y unidades | Pendiente | — | — | |

**Decisiones de diseño de la 5.1 (con la fuente delante):**
- Se parte en **DOS** partes (partir en tres o más es un paso **posterior**, NCETM).
- **No se repite la pareja al revés**: `2+3` y `3+2` son **la misma** (conmutatividad; y la 2.5 ya
  enseñó que el orden no importa) → por eso cinco tiene **3** maneras y no 6.
- El **cero es una parte válida** (`0+5`), pero **el cero no se parte**.
- Y aquí **todavía no se escribe el signo `+`**: se dice con palabras («tres y dos son cinco»).

## Arquitectura en pie

```
E:\Euclides\
  sistema\motor.py              motor: carga .kn, decide, explica con traza (0.1 a 2.1)
  conocimiento\*.kn             15 archivos, todos FIJADOS:
                                  0.1: obj_individual, identidad_referencias, pluralidad, reglas_0_1
                                  0.2: atributo, grupo_por_atributo, reglas_0_2
                                  0.3: pertenencia, reglas_0_3
                                  1.0: subitizing, patrones, reglas_1_0
                                  2.1: secuencia_de_conteo, correspondencia, reglas_2_1
                                  2.2: orden_estable, reglas_2_2
                                  2.3: cuantos_hay, reglas_2_3
                                  2.4: cardinalidad, reglas_2_4
                                  2.5: orden_irrelevante, reglas_2_5
                                  2.6: abstraccion, reglas_2_6
                                  3.1: simbolos, reglas_3_1
                                  3.2: el_cero (modifica reglas_2_3 y reglas_3_1)
                                  3.3: secuencia_de_numeros (los numeros 0..9), reglas_3_3
                                        (modifica el BUCLE de 2.2: siguiente/anterior pasan aqui)
                                  3.4: puente (las 3 representaciones y los 6 caminos), reglas_3_4
                                        (conecta el subitizing 1.0 y añade cifra->cantidad en 'dame')
                                  4.1: comparacion (comparar cantidades), reglas_4_1
                                  4.2: relaciones_entre_numeros (mayor/menor/igual), reglas_4_2
                                  5.1: componer_descomponer (las partes y el todo), reglas_5_1
                                  5.2: la_suma (el signo + y el =, las dos estructuras), reglas_5_2
                                  5.3: las_tres_entradas (los 3 grupos separados; SIN reglas: es
                                        validacion + traduccion + las operaciones de numeros)
                                  5.4: la_resta (el signo -, quitr de un monton, los terminos,
                                        la condicion de aplicacion y la vuelta), reglas_5_4
                                  5.5: la_diferencia (el hueco entre dos; las tres estructuras de la
                                        resta), reglas_5_5
                                  6.1: secuencia_hasta_cien (los 100 nombres: la REGLA y las
                                        excepciones; SIN reglas de decision: es una tabla)
                                  7.1: el_metodo_de_los_dedos (el mecanismo de sumar: los 4 pasos,
                                        la pizarra y por que es mejor que contar todo), reglas_7_1
                                  7.2: derivar (hacer diez: la OTRA via, y las tres piezas que
                                        ya estaban en el sistema), reglas_7_2
                                  6.2: agrupar_en_decenas (el unitising: el diez como UNA cosa),
                                        reglas_6_2
                                  6.3: la_tabla_de_cien (el sitio: fila = decenas, columna =
                                        unidades), reglas_6_3
                                  6.5: partir_en_decenas_y_unidades (cuanto vale cada cifra),
                                        reglas_6_5
  pruebas\test_0_1.py           pruebas de la unidad 0.1
  pruebas\test_0_2.py           pruebas de la unidad 0.2
  pruebas\test_0_3.py           pruebas de la unidad 0.3
  pruebas\test_1_0.py           pruebas de la unidad 1.0
  pruebas\test_2_1.py           pruebas de la unidad 2.1
  pruebas\test_2_2.py           pruebas de la unidad 2.2
  pruebas\test_2_3.py           pruebas de la unidad 2.3
  pruebas\test_2_4.py           pruebas de la unidad 2.4
  pruebas\test_2_5.py           pruebas de la unidad 2.5
  pruebas\test_2_6.py           pruebas de la unidad 2.6
  pruebas\test_3_1.py           pruebas de la unidad 3.1
  pruebas\test_3_2.py           pruebas de la unidad 3.2
  pruebas\test_3_3.py           pruebas de la unidad 3.3
  pruebas\test_3_4.py           pruebas de la unidad 3.4
  pruebas\test_4_1.py           pruebas de la unidad 4.1
  pruebas\test_4_2.py           pruebas de la unidad 4.2
  pruebas\test_5_1.py           pruebas de la unidad 5.1
  pruebas\test_5_2.py           pruebas de la unidad 5.2
  pruebas\test_5_3.py           pruebas de la unidad 5.3
  pruebas\test_5_4.py           pruebas de la unidad 5.4
  pruebas\test_5_5.py           pruebas de la unidad 5.5
  pruebas\test_6_1.py           pruebas de la unidad 6.1
  pruebas\test_7_1.py           pruebas de la unidad 7.1
  pruebas\test_7_2.py           pruebas de la unidad 7.2
  pruebas\test_6_2.py           pruebas de la unidad 6.2
  pruebas\test_6_3.py           pruebas de la unidad 6.3
  pruebas\test_6_5.py           pruebas de la unidad 6.5
  pruebas\test_7_3.py           pruebas de la unidad 7.3
  pruebas\test_ayuda.py         pruebas de la AYUDA (que no se quede atras)
  pruebas\correr_todas.py       lanzador: corre TODAS las pruebas de una vez
  probar.py                     PROBADOR: interactivo, una pregunta suelta, o --casos
  PROBAR.bat                    lanzador de doble clic para Carlos
  herramientas\empaquetar_movil.py   genera el archivo unico para el movil
  movil\euclides_movil.py       EUCLIDES EN UN SOLO ARCHIVO (para el celular)
  movil\Euclides_codigo.zip     el proyecto entero comprimido
  mis_casos.txt                 los casos de prueba DE CARLOS (editable a mano)
  informes\como_probar_v0.2.md / .pdf   guia de uso para Carlos
  diario\, informes\
```

- Formato `.kn`: texto plano `clave: valor`, bloques `|`, listas `-`. Lector propio, sin librerías.
- Las reglas de decisión son **datos** (`reglas_0_1.kn`, `reglas_0_2.kn`), no código.
- El motor evalúa 10 primitivas (3 para 0.1, 7 para 0.2). Nada más.

## Cómo probarlo Carlos (montado el 2026-10-03)

- Doble clic en `PROBAR.bat` → corre `mis_casos.txt` y abre el prompt interactivo.
- `py -3 probar.py "silla,mesa"` → una pregunta suelta con traza.
- `py -3 probar.py --casos` → solo sus casos.
- Carlos escribe sus casos en `mis_casos.txt` (`pregunta | lo esperado | comentario`); se recargan solos.
- **Sintaxis 0.1:** nombres separados por comas (`silla,mesa`).
- **Sintaxis 0.2:** objetos con atributos separados por `;` (`a(color=rojo,forma=cubo); b(color=azul,forma=cubo)`);
  para formar un grupo: criterio, dos puntos y la escena (`color=rojo: a(color=rojo); b(color=azul)`).
- **Sintaxis 0.3:** `pertenece <criterio>: <objetos>` → responde por cada objeto
  (`pertenece color=rojo: taza(color=rojo); plato(color=azul)` → `taza:pertenece, plato:no_pertenece`).
- **Sintaxis 1.0:** `subitizar: <figura>`, figura = 3 filas separadas por `/`, `x` = elemento, `.` = hueco
  (`subitizar: x.x/.../x.x` → `reconocido:cuatro`; `subitizar: x../xx./x.x` → `no_reconocido`).
- **Sintaxis 2.1 contar:** `contar: <colección>` → `emparejado` / `no_alcanza_la_secuencia`.
- **Sintaxis 2.1 revisar:** `revisar: <colección> / <palabras>` → `correcta` / `palabra_repetida` /
  `orden_saltado` / `faltan_objetos_sin_contar` / `palabra_desconocida` / `palabras_de_mas`.
- **Sintaxis 2.2:** `siguiente: <palabra>`, `anterior: <palabra>`, `recitar: <palabra>`,
  `revisar_secuencia: <palabras>` → el valor, `no_lo_se` (se acabó la lista) o `palabra_desconocida`.
- **Sintaxis 2.3:** `cuantos: <colección>` → la cantidad (en palabras) o `no_alcanza_la_secuencia`.
- **Sintaxis 2.4:** `dame: <montón> / <palabra>` (Give-N, word-to-set) → `cogido` + verificación,
  `no_hay_bastantes`, `no_decidible` o `palabra_desconocida`. Y `tiene: <colección> / <palabra>` →
  `si` / `no` / `no_decidible` / `no_alcanza_la_secuencia` / `palabra_desconocida`.
  **En los dos, el montón lo da quien pregunta**: el sistema **no tiene un mundo** y no crea objetos.
- **Sintaxis 2.6:** `misma_cantidad: <colección> / <colección>` → `si` / `no` / `no_decidible` /
  `no_alcanza_la_secuencia`.
- **Sintaxis 3.1:** `cifra: <palabra>` (palabra→cifra) → la cifra / `sin_cifra` /
  `palabra_desconocida`. `palabra: <cifra>` (cifra→palabra) → la palabra / `cifra_desconocida`.
  `cifra_de: <colección>` (cantidad→cifra) → la cifra / `no_alcanza_las_cifras` / `no_decidible`.
  La tabla vive en `conocimiento\simbolos.kn` y **se lee**, no se calcula.
- **Sintaxis 3.2 (el cero):** `cuantos:` y `cifra_de:` con una colección **vacía** → `cero` / `0`.
  Es un **cambio de comportamiento**: antes daban `no_decidible`. Las pruebas de 2.3 y 3.1 se
  actualizaron, y hay una prueba nueva que **documenta el límite**: `tiene:` y `misma_cantidad:` con
  colección vacía **siguen** dando `no_decidible` (el cero solo entra donde la pregunta ES de cantidad).
- **Sintaxis 3.3 (las dos listas):** `listas` (sin `:`) → enseña las dos y su diferencia.
  **`siguiente:` y `anterior:` pasan a ir sobre la SECUENCIA DE NÚMEROS (cero..nueve)**; `recitar:`
  sigue sobre la LISTA DE CONTAR (uno..diez). Por eso `anterior: uno` → `cero`, y `siguiente: diez`
  → `sin_numero` (está en la de contar, no en la de números).
  **Cuidado con esto al tocar el motor: hay dos listas y cada orden usa la suya.**
- **Sintaxis 3.4 (el puente):** `caminos` (sin `:`) → los seis caminos entre las tres representaciones.
  `puente: <colección>` → la colección **de las tres maneras**, enseñando el recuento. **`dame: <montón>
  / 3`** acepta una **cifra** (camino 4, cifra→cantidad). Y `subitizar:` ahora da también **la cifra**.
  Casos límite declarados: `puente:` vacío → `0`; con **diez** objetos → `puente_sin_cifra` (hay cantidad
  y palabra, **no** cifra: el 10 son dos símbolos); `dame: ... / 0` → `cero_no_se_coge`.
- **DOS CAMINOS para saber cuántos hay (3.4):** el **largo** (contar, hasta diez) y el **corto**
  (de un vistazo / subitizing, solo grupos pequeños y reconocibles). **El sistema dice por cuál va**, y
  el corto **no sustituye** al largo.
- **Sintaxis 4.1 (comparar cantidades):** `comparar: <colección> / <colección>` → `mas` (la **primera**
  tiene más) / `menos` / `tantos_como` / `no_alcanza` (alguna pasa de diez). **Sin la barra → NO
  ENTIENDO** (comparar son dos). Decide **emparejando** (uno a uno, sin contar) y **verifica contando**;
  si los dos caminos no cuadraran, lo diría. Y **avisa si hay tamaños distintos** (el tamaño no cuenta).
  **Los símbolos no entran aquí**: `>`, `<`, `=` van entre cifras (4.2).
- **Sintaxis 4.2 (comparar números):** `comparar_cifras: 3 / 2` → `>` / `<` / `=` / `cifra_desconocida`.
  **Va ANTES de `comparar` en el despacho** (`comparar` es prefijo de `comparar_cifras`). La regla de
  fondo: **en la secuencia de números, el que viene DESPUÉS es el mayor** (3.3), y **cuadra con las
  cantidades** (4.1). El sistema dice la lectura («tres es mayor que dos») y hacia dónde mira la boca.
  Hay una prueba que recorre **las 100 parejas (0..9)²** y comprueba que el símbolo de cada una
  coincide con lo que dice la 4.1 sobre colecciones de verdad.
- **EN LAS CONDICIONES, LOS ARGUMENTOS VAN NOMBRADOS:** solo `escena`, `criterio`, `patron`, `cuenta`
  o `palabra` (lo resuelve `evaluar_condicion`). Si una primitiva usa otro nombre, recibe `None`.
  Y **una condición que habla de DOS cosas tiene que mirar las dos**: `cifra_no_conocida` solo miraba
  la primera y `comparar_cifras: 3 / tres` se quedó **sin ninguna regla aplicable**.
- **Sintaxis 5.1 (componer y descomponer):** `descomponer: <colección>` → todas las maneras de partir
  en **DOS** (`termina con "N maneras"`; el probador devuelve las parejas, p. ej. `0+5,1+4,2+3`);
  `descomponer:` vacío → `el_cero_no_se_parte`. `componer: <col> / <col>` → el todo en palabras.
  **No se repite la pareja al revés** (conmutatividad) y **el cero es parte válida**. Si el todo es
  **diez**, la cifra no existe → se da la palabra y se dice. Y **todavía no hay signo `+`**.
- **Sintaxis 5.2 (la suma):** `sumar: <col> / <col>` (AGREGACIÓN) y `anadir: <col> / <col>`
  (AUMENTACIÓN) → la expresión `3 + 2 = 5` (o `3 + 7 = diez` si el total es diez). **Las dos dan el
  mismo número pero cuentan historias distintas**, y el sistema dice cuál. El **`=` es equivalencia**
  (no «pon el resultado»); los términos son **sumandos** y **suma**. **Condición de aplicación: no
  pasa de diez** → `no_alcanza`. Y **la verificación es la vuelta**: la pareja de sumandos tiene que
  estar entre las maneras de partir la suma (5.1).
- **Sintaxis 5.3 (las tres entradas):** los grupos **NO se mezclan** — `cantidad` (a,b,c), `cifra` (3),
  `palabra` (tres). **Un objeto no se puede llamar como un número**: las órdenes de cantidad usan
  `escena_cantidad(...)` y **rechazan** números con `EntradaDelGrupoEquivocado` (el probador lo
  presenta como `grupo_equivocado`). Las órdenes **de números** aceptan **cifra o palabra**:
  `siguiente:`, `anterior:`, `recitar:`, `revisar_secuencia:`, `comparar_numeros:` (antes
  `comparar_cifras:`). Y hay **operaciones de números**: `sumar_numeros: 3 + 2` y
  `descomponer_numero: 5`.
- **Sintaxis 5.4 (la resta como quitar):** `quitar: <montón> / <cuántos>` → `5 - 2 = 3` (el montón
  disminuye; la historia **primero/luego/ahora**; términos **minuendo / sustraendo / resultado**);
  `quitar: a,b / tres` → `no_hay_bastantes` (**la condición de aplicación: no se puede quitar más de
  lo que hay**); `quitar: <doce objetos> / dos` → **`no_alcanza`** (solo se cuenta hasta diez);
  `restar_numeros: 5 - 2` → `5 - 2 = 3` (números). **La vuelta verifica**: `3 + 2 = 5`, comprobado
  **con la suma de verdad** (5.2/5.3). Y **quitar ≠ partir**: aquí los que se van **se van** (5.1).
- **Sintaxis 5.5 (la diferencia):** `diferencia: <colección A> / <colección B>` → la **palabra** del
  hueco (`dos`); `diferencia: a,b,c / a,b,c` → `cero`; `diferencia_numeros: 5 / 3` → `dos`. **Aquí NO
  se quita nada** (los dos montones siguen enteros) y **no hay «todo»**. Las primitivas son **las
  mismas** que en 4.1 (`cuenta_no_alcanza`, `las_dos_iguales`, `la_primera_tiene_mas/menos`): comparar
  y hallar la diferencia son lo mismo, y no puede haber dos verdades. Se escribe de **dos maneras**:
  `5 - 3 = 2` y `3 + 2 = 5` (contar hacia adelante). **Y la prueba de hierro: las tres estructuras
  (quitar 5.4 / partir 5.1 / diferencia 5.5) dan el MISMO número en las 65 parejas.**
- **Sintaxis 7.1 (el método de los dedos):** `dedos: 8 + 5` → el método **paso a paso**, con la
  **pizarra** a la vista (el primero anotado), los dedos del segundo, y el conteo hacia adelante.
  `dedos: ocho + doce` → `no_caben_en_los_dedos`; `dedos: noventa y cinco + nueve` → `no_alcanza`;
  `dedos: 5 + 0` → el total es el primero. **Y enseña el ahorro**: 5 pasos frente a 13.
  **OJO: `dedos: 47 + 3` → `no_es_un_numero`**, porque el sistema **todavía no lee cifras de dos
  dígitos** (eso es la 6.3, pendiente): hay que escribirlo con palabras
  (`dedos: cuarenta y siete + tres`).
- **Sintaxis 6.2 (agrupar de diez en diez):** `agrupar: a,b,…,m` (13 objetos) → **`una decena y tres
  unidades`**, y lo **enseña montón a montón**. Cada montón de diez es **una decena** y se cuenta como
  **una sola cosa** — eso es el «unitising» de NCETM, y es **lo que hace posible el valor posicional**.
  `agrupar:` con menos de diez → `no_hay_decena`; con más de cien → `no_alcanza`; **`agrupar:` vacío →
  `cero`** (el vacío es una cantidad, unidad 3.2 — *no* «no hay decena»). Y **comprueba dos cosas en
  cada respuesta**: que el reparto cuadra (`decenas × 10 + unidades = objetos`) y que **el orden no
  cambia el valor** (Oak): agrupa la colección al revés y compara.
- **EL ERROR TÍPICO DEL VALOR POSICIONAL VA DENTRO.** Oak lo documenta: *«los niños pueden seguir
  contando de diez en diez cuando llegan a las unidades»*. El explicador lo dice explícitamente: las
  **decenas** se cuentan de diez en diez, las **unidades** de uno en uno. Y se cuentan **primero las
  decenas**.
- **Una cifra escrita con dígitos ES UN NÚMERO, aunque no se sepa leer** (arreglo del 4-oct). `47`
  no es el nombre de un objeto: `clasificar_nombre` ahora comprueba `isdigit()`, así que las órdenes
  de cantidad lo rechazan en vez de tomarlo por un objeto y **contestar algo falso** (`cuantos: 47`
  daba `uno`). `silla_1` **no** es todo dígitos: sigue siendo un objeto.
- **Sintaxis 7.2 (derivar / hacer diez):** `derivar: 7 + 5` → **`siete + cinco = doce`**, y lo
  **enseña paso a paso**: al 7 le faltan 3; parto el 5 en 3 + 2; `7 + 3 = 10`; `10 + 2 = 12`.
  **No cuenta nada**: es **transformar** la cuenta en dos cuentas fáciles, y una (llegar a diez) ya
  se sabe. `derivar: 4 + 5` → `no_hace_falta` (no cruza el diez); `derivar: doce + tres` →
  `necesito_las_columnas` (el «hacer diez» es para **una** cifra); `derivar: ocho + manzana` →
  `no_es_un_numero`. **Y el sistema prueba LAS DOS VÍAS** (los dedos y derivar) y comprueba que dan
  **el mismo número** — decisión de Carlos: «admite todo lo que sirva, los dedos y derivar; el que
  pruebe las dos».
- **DERIVAR ES COMBINAR LO QUE YA SE SABE.** Las tres piezas que hacen falta ya estaban en el
  sistema: **partir un número** (5.1), **llegar a diez** (6.1) y **sumar a diez** (5.2). No hizo
  falta ningún conocimiento nuevo; hizo falta **darse cuenta de que se podían encadenar**. Eso es
  el «corazón del proyecto» que pidió Carlos: **aplicar lo que sabe**, no saber qué hacer.
  Respaldo medido: **Tall y Gray** (citado por Number Sense Maths): *«los alumnos de rendimiento
  alto tienden a usar hechos DERIVADOS, y los de rendimiento bajo son mucho más propensos a usar
  métodos de contar»*. Y **Thornton (1978)**: *«enseñar estrategias es más efectivo para asegurar la
  fluidez que la memorización por repetición»*. Y sobre `8 + 9`: *«solo el 5% de los profesores dice
  saberlo; la mayoría lo deriva»*.
- **EL TECHO SE ESCRIBE CON `len(secuencia)`, NUNCA CON EL NÚMERO A MANO.** `sumar_numeros` (5.3)
  tenía `if total > 10` escrito a mano y al subir la secuencia a 100 **se quedó corto**: `7 + 5`
  decía `no_alcanza`. Lo cazó la prueba de hierro de la 7.1 (que prueba las 100 parejas), no las
  pruebas de la 5.3, que solo probaban hasta diez. `_valor_de_numero` usa la secuencia de **números**
  (0..9) y `_valor_de_cantidad` la de **contar** (1..10) **más el cero**. Las órdenes de **cantidad**
  (`dame`, `quitar`) usan la segunda, porque *diez es una cantidad válida y no un número*.
  **La traducción cifra↔palabra vive DENTRO de las funciones `decidir_*`** (`nombre_de_numero`), no en
  el despacho: si estuviera en el despacho, llamar a la función directamente no traduciría (pasó).
- **Alias de respuesta POR UNIDAD:** `uno` es `un_objeto` en 0.1, pero es la cantidad en 2.3. Las
  unidades 2.2 a 2.6 no pasan por la tabla de alias (`SIN_ALIAS` en `probar.py`).
- **OJO al montar casos:** los **nombres repetidos se fusionan** (0.1). Para tres sillas hay que
  escribir `silla_1,silla_2,silla_3`, no `silla,silla,silla`. Me ha fallado **dos veces** por esto.
- **Sintaxis 2.5:** `orden: <colección>` → `coinciden` (con los dos recuentos a la vista) /
  `no_decidible` / `no_alcanza_la_secuencia`. Y `conteo: <recorrido> / <palabras>` → `valido`
  (pseudoerror) / `objeto_repetido` (compensación) / `palabra_repetida` / `orden_saltado` /
  `faltan_objetos_sin_contar` / `palabras_de_mas` / `palabra_desconocida`.
- Regla: **cada unidad que se cierre deja su probador**, no vale entregar código sin forma de probarlo.

## Decisiones aprobadas por Carlos (2026-10-03)

- Esquema del conocimiento: el del método + `errores_tipicos` obligatorio + sección `prueba_de_dominio`.
- Prueba de dominio: mínimo **5 casos no programados** por unidad, **al menos 1 con trampa**.
- **Subitizing** añadido al PLAN.md como unidad **1.0**.

## Qué falta por decidir (con Carlos)

- **¿Se le dan ojos al sistema?** Observación de Carlos (2026-10-03): como el sistema no ve, el
  subitizing no tiene utilidad todavía, y lo mismo pasará con varias unidades del Nivel 1.
  **Matiz posterior del propio Carlos** (2026-10-03): ver serviría para geometría, pero **un cuadrado
  se define por sus características escritas, no por verlo** → el Nivel 4 **no** está bloqueado por la
  falta de visión. Ver `diario\2026-10-03-definir-no-es-ver.md`.
- **Orden del plan cambiado** (decisión de Carlos, 2026-10-03): 1.1–1.4 aplazadas, se sigue por 2.x.
  Motivo: mientras todo se escriba a mano, las unidades del Nivel 1 (que son estructura, no cálculo)
  quedarían colgadas. El Nivel 2 sí **deduce** cosas nuevas.
  Ver `diario\2026-10-03-observacion-no-ve.md`.

## Carné de errores (lo que ya falló, para no repetirlo)

- **Un runner de pruebas que AVISA en vez de FALLAR deja pasar un archivo entero.** `correr_todas.py`
  lee el total de cada archivo con una expresión regular (`TOTAL:` / `UNIDAD x.y:`); si un archivo no
  dice su total, imprimía un **aviso** y **daba VERDE** — con las **255 pruebas de la 7.2 fuera de
  cuenta** (el total seguía diciendo 807). **Regla: un archivo que no dice su total es un FALLO, no
  un aviso; y un archivo que dice `8/10` también.** Un recuento que puede dar VERDE sin contar todo
  no vale para nada.
- **Filtrar la salida de una prueba con `tail`/`grep` esconde el aviso.** El aviso del runner existía
  (y era verde-amarillo desde la 5.3): yo lo tenía delante y **lo tapé con `tail -15`** — la misma
  falta que ya había anotado en la 5.4. **Regla: la salida de una prueba se lee ENTERA.** Si es
  larga, se lee del fichero que el terminal deja; nunca se recorta a ciegas.
- **No reutilizar lo que ya sabe la unidad anterior.** Ha pasado 3 veces: el vocabulario de «grupo»
  con dos sentidos, la separación de entidades, y la 2.1 sin aplicar la identidad de 0.1.
  **Regla: toda unidad nueva que reciba objetos pasa por `escena_0_2` + `entidades_reales`; nunca por
  la vía simple `escena_0_1`, y nunca reimplementando la identidad.**
- **Probar siempre con atributos, no solo con nombres simples.** El caso `a, a, a` pasaba y
  `casa(color=blanco), casa, casa(forma=cuadrado)` fallaba. Las colecciones de prueba deben llevar
  atributos desde el principio.
- **Usar la misma palabra con dos sentidos EN UNIDADES DISTINTAS.** Pasó con «grupo» (0.1 vs 0.2) y
  con «uno»: en 0.1 `uno` significa `un_objeto`; en 2.3 es **la cantidad**. Cazado por los casos de
  Carlos (2 fallos). **Regla: los alias de respuesta son por unidad**, no globales.
- **Fabricar el dato en vez de pedirlo.** En la primera versión de la 2.4, `dame: tres` se **inventaba
  los objetos** (`cosa_uno`, `cosa_dos`…) porque el sistema no tiene un mundo. Violaba la regla de que
  toda respuesta se rastree a un **dato escrito**. Cazado por Carlos preguntando «¿de dónde saca los
  objetos?». **Regla: el sistema no crea datos; si le falta la entrada, la pide o dice que no puede.**
- **No propagar un conocimiento nuevo a lo que ya sabía.** En la 3.2 el cero entró en la **tabla de
  símbolos** pero no en la **secuencia**, y quedaron **dos listas desincronizadas**: `cuantos:` vacío daba
  `cero`, pero `anterior: uno` decía «antes no hay nada» y `recitar: cero` decía «no está en mi lista».
  Cazado por Carlos probando. **Regla: cuando una unidad añade algo (un símbolo, un caso, un dato),
  hay que repasar TODAS las unidades anteriores que hablan de eso.**
- **Dos sitios que deciden lo mismo.** El mismo día, el probador tenía su **propio despacho**
  (`probar.py`) copiado del motor, y las dos copias se desincronizaron: el modo interactivo ya usaba la
  3.3 y el modo `--casos` seguía con la 2.2. **Regla: una sola verdad. Si algo se decide en dos sitios,
  es un fallo esperando.** Y se vigila solo: `correr_todas.py` corre **también** `probar.py --casos`,
  así que si las dos vías se separan, la prueba se pone ROJA.
- **Contestar con seguridad algo falso (el peor de todos).** Las operaciones de **cantidad** aceptan una
  **cifra** o una **palabra de número** como si fuera el **nombre de un objeto**: `sumar: 3 / 2` daba
  **`1 + 1 = 2`**, `comparar: 3 / 2` daba `tantos_como`, `descomponer: 5` daba `1 maneras`. Cazado por
  Carlos. **No revienta y el test no lo caza: pasa por bueno.** Es más grave que los fallos que dan
  error, porque engaña. **Regla: el sistema tiene que AVISAR cuando un nombre es una cifra o una
  palabra de número, sin adivinar la intención** (el nombre «3» puede ser legal como nombre de objeto;
  lo que no puede es pasar en silencio).

| Fecha | Qué pasó | Qué se hizo |
|---|---|---|
| 2026-10-03 | 3 pruebas de 0.2 en rojo en la primera pasada | El fallo era de las pruebas, no del motor: el motor devolvía datos de más y yo esperaba listas vacías. Se ajustó el motor (solo enseña los atributos compartidos cuando la conclusión ES un grupo) y las pruebas |
| 2026-10-03 | Al reescribir `probar.py` se perdió el alias `objeto` → `obj_individual` | Saltó a la vista en el primer `--casos` (2 casos en rojo). Alias restaurado. Lección: el probador también se prueba |
| 2026-10-03 | `write_file` rechazó sobrescribir archivos ya escritos (guardas anti-escritura) | Leer el archivo entero antes de reescribirlo, o usar `patch` para cambios concretos |
| 2026-10-03 | **Carlos escribió `casa(color=azul), carro` y el sistema soltó un traceback (crash)** | Fallo grave: viola la regla 4. Se arregló en tres frentes: (1) el separador de escena ahora admite `;` **y** comas de fuera de los paréntesis, (2) `explicar_pregunta` captura los errores y responde «NO ENTIENDO ESTO» con las formas correctas, (3) prueba de robustez fija en `test_0_2.py` (7 entradas mal escritas: ninguna puede reventar) |
| 2026-10-03 | La validación dejaba pasar `caja(color=rojo))` como si fuera válido (el valor quedaba «rojo)») | Se detectó al escribir la prueba de robustez, no al probarlo Carlos: validación de paréntesis sobrantes. Lección: el traceback de Carlos destapó la familia entera de entradas mal formadas |
| 2026-10-03 | **Observación de Carlos:** «podría haber objetos con el mismo nombre con atributos distintos» | Caso real que faltaba: `casa(color=azul); casa(color=rojo)`. Añadida la regla `hay_entidad_contradictoria` para reconocer y formar: la misma entidad descrita de dos formas que no cuadran → `no_decidible`. Se documentó que **el nombre es el identificador**: dos cosas distintas necesitan nombres distintos (`casa_A`, `casa_B`) |
| 2026-10-03 | **CONTRADICCIÓN DE VOCABULARIO, destapada por Carlos:** `casa,carro` decía `grupo` (0.1) y `casa(color=blanco); carro(color=negro)` decía `no_grupo` (0.2). El mismo par de objetos daba respuestas opuestas | La palabra «grupo» se usaba con dos sentidos: 0.1 = «hay varias cosas» (pluralidad) y 0.2 = «comparten un atributo» (homogeneidad). Son propiedades independientes. **Corregido con el visto bueno de Carlos:** 0.1 pasa a decir `un_objeto` / `varios_objetos` y deja de hablar de grupos; 0.2 dice `grupo_por_atributo` / `sin_atributo_comun` / `una_sola_entidad`. La palabra GRUPO queda reservada a 0.2. Tocado: `pluralidad.kn`, `reglas_0_1.kn`, `reglas_0_2.kn`, `PLAN.md`, pruebas, probador y casos de Carlos |
| 2026-10-03 | El formato `.kn` no admite un ítem de lista partido en dos líneas | Saltó al escribir `pluralidad.kn` (error de sangría). **Limitación conocida del lector**: cada ítem de lista, en una sola línea |
| 2026-10-03 | **Volvió a saltar el mismo fallo del formato** al escribir `identidad_referencias.kn` | En vez de esquivarlo por tercera vez, **se arregló el lector**: un ítem de lista ahora continúa en las líneas siguientes con más sangría. Arreglar la herramienta, no el camino |
| 2026-10-03 | **Sin respuesta de Carlos a la pregunta del objeto sin atributos** (`casa; carro` → sin_atributo_comun vs no_decidible) | Carlos respondió por su cuenta y mejor: **no hay que elegir una respuesta, hay DOS preguntas** — «¿son varias cosas?» (se sabe) y «¿comparten atributo?» (puede no saberse). 0.2 ahora informa de las dos capas y deja de ocultar lo que 0.1 ya sabe |
| 2026-10-03 | **Casa blanca y casa cuadrada:** el sistema las trataba como contradicción cuando NO lo son | Regla de **fusión** (razonada por Carlos): las menciones del mismo identificador cuyos datos no se contradicen **se suman** (una sola casa, mejor descrita). Solo una clave con dos valores distintos contradice → `no_decidible`. Su porqué, que es el correcto: si no, `casa,casa` contaría como dos objetos y sería un grupo |
| 2026-10-03 | Al escribir la robustez de 0.3 se destapó que `pertenece =rojo: taza(color=rojo)` colaba (criterio con el atributo vacío) | `parsear_criterio` no comprobaba el nombre del atributo. Arreglado: sin nombre → «no entiendo». Lección: cada unidad nueva destapa entradas mal formadas nuevas; la robustez se escribe **con** la unidad, no después |
| 2026-10-03 | **Carlos probó `carro(color=negro), carro(color=blanco)` y el sistema dijo «es UN OBJETO» + «se contradicen».** Estaba mal | Su razonamiento, que es el correcto: **una misma cosa no puede ser negra y blanca; un atributo con dos valores distintos PRUEBA que son objetos distintos.** Se sustituyó la regla de «contradicción → no_decidible» por la de **distinción → separar y numerar** (`carro#1`, `carro#2`). Es coherente con lo que él mismo dijo antes: «el mismo objeto **hasta que un atributo lo distinga**». Tocado: `identidad_referencias.kn`, `reglas_0_2.kn`, `reglas_0_3.kn`, motor (nueva `entidades_reales`), pruebas, casos de Carlos y guía |

## Registro de mediciones

| Fecha | Qué se midió | Resultado |
|---|---|---|
| 2026-10-03 | Búsquedas de investigación | 8 búsquedas; fuentes en `diario\2026-10-03-investigacion.md` |
| 2026-10-03 | Pruebas unidad 0.1 | 8/8 correctos — VERDE (3 de ejemplo + 5 de dominio) |
| 2026-10-03 | Primitivas del motor | 3 (`escena_vacia`, `varios_distintos`, `un_solo_distinto`) |
| 2026-10-03 | Probador para Carlos | 4/4 de sus casos VERDE; probado interactivo, con escena suelta y por doble clic (`PROBAR.bat`) |
| 2026-10-03 | Guia de uso | `informes\como_probar_v0.1.pdf` (3 paginas, 8,2 KB, verificado con pypdf) |
| 2026-10-03 | Pruebas unidad 0.2 | 12/12 correctos — VERDE (3 de ejemplo + 9 de dominio) |
| 2026-10-03 | Pruebas de TODO el proyecto | 20/20 — VERDE (0.1: 8/8 ; 0.2: 12/12) |
| 2026-10-03 | Primitivas del motor | 10 (0.1: 3 ; 0.2: 7) |
| 2026-10-03 | Probador ampliado a 0.2 | 11/11 de los casos de Carlos VERDE, y probado por doble clic |
| 2026-10-03 | **Pruebas tras el fallo del crash** | **22/22 — VERDE** (0.1: 8/8 ; 0.2: 14/14, de las cuales 7 son de robustez) |
| 2026-10-03 | **Pruebas tras corregir el vocabulario** | **22/22 — VERDE** otra vez; casos de Carlos 12/12 |
| 2026-10-03 | Contradicción 0.1/0.2 | Resuelta: `casa,carro` → `varios_objetos` y `casa(color=blanco); carro(color=negro)` → `sin_atributo_comun`. Ya no se contradicen |
| 2026-10-03 | **Pruebas tras la fusión y las dos capas** | **29/29 — VERDE** (0.1: 8/8 ; 0.2: 21/21, de las cuales 7 de robustez y 6 de «las dos capas») |
| 2026-10-03 | Lector `.kn` | Arreglado: los ítems de lista admiten continuación en varias líneas |
| 2026-10-03 | **Pruebas tras la unidad 0.3** | **50/50 — VERDE** (0.1: 8/8 ; 0.2: 29/29 ; 0.3: 13/13). Casos de Carlos 18/18 |
| 2026-10-03 | Unidades cerradas | 0.1, 0.2 y 0.3 → **Nivel 0 completo** |
| 2026-10-03 | **Pruebas tras la regla de distinción** | **52/52 — VERDE** (0.1: 8/8 ; 0.2: 29/29 ; 0.3: 15/15). Casos de Carlos **21/21** |
| 2026-10-03 | Contradicciones de vocabulario/diseño detectadas por Carlos | 3 en total: el crash, «grupo» con dos sentidos, y «contradicción» donde había «distinción» |
| 2026-10-03 | **Pruebas tras la unidad 1.0** | **65/65 — VERDE** (0.1: 8/8 ; 0.2: 29/29 ; 0.3: 15/15 ; 1.0: 13/13). Casos de Carlos **27/27** |
| 2026-10-03 | Unidad 1.0 — el sistema **no cuenta** | Comprobado: una figura de 4 elementos no canónica da `no_reconocido` (no «cuatro») |
| 2026-10-03 | **Pruebas tras la unidad 2.1** | **80/80 — VERDE** (0.1: 8/8 ; 0.2: 29/29 ; 0.3: 15/15 ; 1.0: 13/13 ; 2.1: 15/15). Casos de Carlos **35/35** |
| 2026-10-03 | **FALLO encontrado por Carlos probando en el móvil** | En la 2.1, `casa(color=blanco), casa, perro, casa(forma=cuadrado), carro` daba **5 objetos** en vez de 3: no aplicaba la identidad de 0.1 y ni siquiera parseaba los atributos. **Arreglado** → `escena_0_2` + `entidades_reales`. 3 pruebas nuevas (D4/D5/D6) |
| 2026-10-03 | **Pruebas tras el arreglo** | **83/83 — VERDE** (2.1: 18/18). Casos de Carlos **37/37** |
| 2026-10-03 | **Unidad 2.2 (orden estable) cerrada** | **107/107 — VERDE** (0.1: 8/8 ; 0.2: 29/29 ; 0.3: 15/15 ; 1.0: 13/13 ; 2.1: 18/18 ; 2.2: 24/24). Casos de Carlos **49/49** |
| 2026-10-03 | **Unidad 2.3 (cuántos hay) cerrada** | **121/121 — VERDE** (2.3: 14/14). Casos de Carlos **56/56** |
| 2026-10-03 | **FALLO cazado por los casos de Carlos (2 rojos)** | El alias `uno → un_objeto` de 0.1 chocaba con la cantidad `uno` de 2.3: la misma palabra con dos sentidos **en unidades distintas**. **Arreglado**: los alias son **por unidad** (`SIN_ALIAS` en `probar.py`) |
| 2026-10-03 | 2.3 vs 2.4, separadas a propósito | 2.3 = **regla de la última palabra** (procedimiento); 2.4 = **principio de cardinalidad**. La investigación las separa: un 22,3% de 188 niños acertaba «¿cuántos hay?» fallando el 1-a-1 |
| 2026-10-03 | **Unidad 2.4 (cardinalidad) cerrada** | **151/151 — VERDE** (2.4: 30/30). Casos de Carlos **68/68**. Incluye prueba de **coherencia para toda la lista**: `dame: N` → contar lo dado → N |
| 2026-10-03 | **FALLO DE DISEÑO cazado por Carlos** | `dame: tres` (sin montón) **se fabricaba los objetos** el propio sistema: violaba la regla «toda respuesta se rastrea a un dato escrito». **Arreglado por propuesta suya**: `dame: <montón> / <cantidad>` — el sistema **elige** del montón que le dan; sin montón lo dice; si hay menos, `no_hay_bastantes`. 2.4 sube a 36/36 |
| 2026-10-03 | **Pruebas tras el arreglo** | **157/157 — VERDE**. Casos de Carlos **70/70** |
| 2026-10-03 | **Unidad 2.5 (orden irrelevante) cerrada** | **186/186 — VERDE** (2.5: 29/29). Casos de Carlos **78/78** |
| 2026-10-03 | Distinción nueva: reglas **lógicas** vs **convencionales** | De Lago, Escudero & Dopico (2021, Front. Psychol., PMC8202410) + Gelman & Meck (1986): **pseudoerror** (rompe una convencional) → válido; **compensación** (rompe una lógica) → inválido |
| 2026-10-03 | Fallo **del test**, no del motor | El caso del pseudoerror usaba **12 objetos** y el sistema solo cuenta hasta diez: `faltan_objetos_sin_contar` era lo correcto. Caso reajustado a diez |
| 2026-10-03 | Búsqueda web caída (Exa 503) | Se tiró por navegador (PMC) y se localizó la fuente exacta. Anotado |
| 2026-10-03 | **NIVEL 2 COMPLETO** | **208/208 — VERDE** (0.1: 8 ; 0.2: 29 ; 0.3: 15 ; 1.0: 13 ; 2.1: 18 ; 2.2: 24 ; 2.3: 14 ; 2.4: 36 ; 2.5: 29 ; 2.6: 22). Casos de Carlos **84/84** |
| 2026-10-03 | Fallo **mío de nuevo, y dos veces el mismo** | Dos casos de la 2.6 montados con nombres repetidos (`silla,silla,silla`) esperando tres objetos: son **uno**. Es la regla de identidad de 0.1. Anotado en el carné |
| 2026-10-03 | **Nivel 3 abierto — unidad 3.1 (símbolos) cerrada** | **239/239 — VERDE** (3.1: 31/31). Casos de Carlos **98/98**. **Primera vez que el sistema usa CIFRAS** (hasta ahora estaban prohibidas a propósito) |
| 2026-10-03 | 3.1 lee la tabla, no la calcula | La correspondencia palabra↔cifra vive en `simbolos.kn` y el motor la **lee**. Orden de las traducciones tomado de Benoit et al. (2013): palabra→colección, cifra→colección, y **por último** palabra→cifra |
| 2026-10-03 | **Unidad 3.2 (el cero) cerrada** | **254/254 — VERDE** (3.2: 15/15). Casos de Carlos **106/106**. El vacío deja de ser «no se puede decidir»: **es una cantidad (cero)** |
| 2026-10-03 | **FALLO CAZADO POR CARLOS: dos listas desincronizadas** | Al añadir el cero en la 3.2 quedó en la **tabla de cifras** pero no en la **secuencia**: `cuantos:` vacío daba `cero` y `anterior: uno` decía «antes no hay nada». **Arreglado en la 3.3 con DOS listas de verdad** (contar / números) y con una prueba de coherencia |
| 2026-10-03 | **Unidad 3.3 (secuencia de números) cerrada** | **287/287 — VERDE** (3.3: 31/31). Casos de Carlos **114/114**. Dos listas, cada orden con la suya, y el sistema **dice en cuál habla** |
| 2026-10-03 | **Unidad 3.4 (el puente) cerrada — NIVEL 3 COMPLETO** | **319/319 — VERDE** (3.4: 32/32). Casos **124/124**. Los **6 caminos**; el que faltaba era **cifra→cantidad**; y el **subitizing (1.0) por fin conectado**: es el camino CORTO |
| 2026-10-03 | 3.4 declara lo que NO tiene | `puente:` con **diez** objetos → `puente_sin_cifra`: se puede contar hasta diez, pero **la cifra del diez no existe** (son dos símbolos). El sistema da las dos representaciones que tiene y **dice cuál le falta** |
| 2026-10-03 | 3.4 y el cero se tocan | `dame: <montón> / 0` → `cero_no_se_coge`: el cero **es** una cantidad (3.2), pero no una cantidad **que se coja**; dar es coger, y el vacío no se coge |
| 2026-10-03 | **Alcance del Nivel 4 decidido por Carlos** | «primero relacionar **cantidades** y después **números**». La investigación lo respalda (NCETM 2023) y fija además que **los símbolos `=`,`<`,`>` solo se usan entre cifras** → la 4.1 se dice con **palabras**, los símbolos son la 4.2 |
| 2026-10-03 | **Unidad 4.1 (comparar cantidades) cerrada — Nivel 4 abierto** | **352/352 — VERDE** (4.1: 33/33). Casos **132/132**. Decide **emparejando** (sin contar) y **verifica contando**; y **el tamaño de los objetos no cuenta** (la trampa de la unidad) |
| 2026-10-03 | **Unidad 4.2 (comparar números) cerrada** | **381/381 — VERDE** (4.2: 29/29). Casos **140/140**. Los símbolos `>`, `<`, `=`, con la regla «el que viene después en la secuencia es el mayor», **y la prueba de hierro: las 100 parejas (0..9)² cuadran con lo que dice la 4.1 sobre colecciones reales** |
| 2026-10-03 | 4.2: una condición que habla de dos cosas mira las DOS | `cifra_no_conocida` solo miraba la primera cifra, y `comparar_cifras: 3 / tres` se quedaba **sin ninguna regla aplicable** (`ValueError`) en vez de decir `cifra_desconocida`. Regla: **si la condición habla de dos, mira las dos** |
| 2026-10-03 | **Alcance del Nivel 5 decidido por Carlos: componer y descomponer** | «si, componer y descomponer». La investigación lo respalda: componer/descomponer es **el cimiento de la suma y la resta** (NCETM: «partir y volver a juntar sostiene la suma y la resta como inversas») |
| 2026-10-03 | **Unidad 5.1 cerrada** | **412/412 — VERDE** (5.1: 31/31). Casos **152/152**. Cinco se parte de **3 maneras** (0+5, 1+4, 2+3), **sin repetir el orden** y con el **cero como parte**. La prueba de hierro: **las 35 parejas de 1..10, juntadas, devuelven su todo** |
| 2026-10-03 | **Unidad 5.2 (la suma) cerrada** | **452/452 — VERDE** (5.2: 40/40). Casos **161/161**. El **`+`** y el **`=` como equivalencia**; los términos (**sumandos**, **suma**); **dos estructuras** (agregación / aumentación); y **la verificación es la vuelta** de la 5.1. Prueba de hierro: **las 66 sumas (a+b≤10) coinciden con el componer** |
| 2026-10-03 | **Unidad 5.3 (las tres entradas) cerrada — fallo grave arreglado** | **506/506 — VERDE** (5.3: 54/54). Casos **179/179**. **Los tres grupos separados** por decisión de Carlos; un objeto no se puede llamar como un número; las órdenes de números aceptan cifra o palabra; y se opera con números. Prueba de hierro: **las 55 parejas dan lo mismo por los TRES caminos** (sumar números / sumar objetos / componer) |
| 2026-10-03 | **Unidad 5.4 (la resta como quitar) cerrada** | **547/547 — VERDE** (5.4: 41/41). Casos **195/195**. **La reducción**: `quitar:` con la historia **primero/luego/ahora**; el signo **`-`**; los términos **minuendo / sustraendo / resultado**; **la condición de aplicación: no se puede quitar más de lo que hay** (`no_hay_bastantes`); **la vuelta verifica** comprobada con la suma de verdad; y **quitar ≠ partir**. `correr_todas.py` ahora dice **el total del proyecto él solo** |
| 2026-10-03 | **Unidad 5.5 (la diferencia) cerrada — LA RESTA COMPLETA** | **585/585 — VERDE** (5.5: 38/38). Casos **208/208**. **La tercera y última estructura de la resta**: el **HUECO** entre dos cantidades. **No se quita nada** (los dos montones siguen enteros) y **no hay «todo»**; el **mismo número** responde a «cuántos más» y «cuántos menos»; se escribe de **dos maneras** (`5 - 3 = 2` y `3 + 2 = 5`, contar hacia adelante). Reutiliza **las primitivas de 4.1**. **Prueba de hierro: las tres estructuras (quitar 5.4 / partir 5.1 / diferencia 5.5) dan el MISMO número en las 65 parejas** |
| 2026-10-03 | **Unidad 6.1 (contar hasta 100) cerrada** | **770/770 — VERDE**. Casos **228/228**. **Los 100 nombres se CONSTRUYEN con la regla** (24 memorizadas + 3 formaciones): `dieci+u` (16–19), `veinti+u` (21–29), `decena y u` (31–99). **El error de decena explicado** («no es saber poco: es aplicar una regla buena donde ya no vale»). Y **el techo subió de diez a cien en TODO el sistema** sin tocar ninguna regla, porque el techo estaba en `len(secuencia)` y no escrito a mano |
| 2026-10-03 | **La verificación completa que pidió Carlos** | Tras el cambio: **14 archivos en rojo**. Casi todos eran **pruebas obsoletas por mejora** (comprobaban que el sistema NO se inventa lo que no sabe: `once` → `palabra_desconocida`), no roturas: **el sistema no se rompió, creció**. Se actualizaron **caso por caso** (nunca a ciegas) y **cada caso viejo se quedó al lado del nuevo** (`D2b (MEJORA 6.1): ONCE objetos ya SI…`). Un fallo real del **test** de coherencia de 2.4 (montón de diez, `KeyError: 'cogidos'`) → montón de cien. Y se comprobó que el motor **sí** detecta el techo nuevo en 2.1, 3.4, 4.1, 5.1, 5.2 y 5.5 |
| 2026-10-04 | **Unidad 7.1 (el método de los dedos) cerrada** | **807/807 — VERDE**. Casos **230/230**. **El mecanismo de sumar** (decisión de Carlos: mecánico hasta nuevo aviso): se **anota** el primero (la pizarra = memoria de trabajo, EEF), se cogen los dedos del segundo, se **cuenta hacia adelante**, y el último número dicho es el total. Enseña **por qué** es mejor que contar todo (5 pasos frente a 13). Prueba de hierro: **las 100 parejas dan el mismo resultado por los dedos y por la suma** |
| 2026-10-04 | **FALLO REAL cazado por la prueba de hierro de la 7.1** | `sumar_numeros` (5.3) tenía **`if total > 10` escrito a mano**: al subir la secuencia a 100 **se quedó corto**, y `7 + 5` decía `no_alcanza`. **Las pruebas de la 5.3 no lo cazaron porque solo probaban hasta diez.** Arreglado con `len(secuencia)`. Confirmado: era el ÚNICO techo escrito a mano en todo el motor |
| 2026-10-04 | **El probador arrancaba con 228 ejemplos en pantalla** | Al lanzar `probar.py` (o el `.bat`) corría **todos** los casos de `mis_casos.txt` antes de dejar escribir. Quitado: ahora arranca limpio y los casos se piden con `casos`. Y la cabecera estaba **congelada en la 3.3** (le faltaban 3.4 → 6.1) |
| 2026-10-04 | **FALLO GRAVE arreglado: cifras de dos dígitos tomadas por objetos** | `cuantos: 47` daba **`uno`** (y `contar: 47` → `emparejado`, `dame: 47 / uno` → `cogido`). La comprobación de grupos de la **5.3** solo miraba la tabla de símbolos, que es **del 0 al 9**: `47` no estaba, así que pasaba por **nombre de objeto** y el sistema **contestaba con seguridad algo falso** — el fallo nº1 del carné, por la puerta que quedó abierta. Arreglado: `clasificar_nombre` comprueba `isdigit()` (una cifra escrita con dígitos es un NÚMERO aunque no se sepa leer; `silla_1` no lo es). Ahora **lo dice**: «es un número, y yo todavía no sé leer cifras de más de un dígito (eso es la 6.3)». 6 casos nuevos (253 → **259**) |
| 2026-10-04 | **La 7.4 MEJORADA — idea de Carlos: los dedos son la VENTANA de los últimos diez** | **47362/47362 — VERDE**, 31 archivos, 345/345 casos. `dedos: 45 - 7` → **38** y `dedos: 12 - 5` → **7**. La versión anterior exigía que el **primero** no pasara de diez, y **contradecía a la 7.1** (donde el primero se anota y el total no tiene que caber). La idea de Carlos: los diez dedos **no representan el número entero**, representan la **ventana de los últimos diez** terminando en el minuendo — para `12 - 5` van **del 3 al 12** (su ejemplo exacto). Lo que tiene que caber es **lo que se BAJA** (el segundo). FIX: la regla pasa de `primer_numero_pasa_de_diez` a **`segundo_pasa_de_diez`** (la primitiva de la 7.1, **reutilizada**). Y la 7.5 se simplifica: ya no hace falta la «pizarra» aparte. **Fallo cazado**: la primitiva reutilizada necesitaba `_saber` en la cuenta (la 7.1 se lo pasa; yo no) → reventaba con `KeyError` |
| 2026-10-04 | **Unidad 7.5 (restar por columnas) cerrada** | **47357/47357 — VERDE**, 31 archivos, 344/344 casos. `columnas: 72 - 45` → 27. Si las unidades de arriba no llegan, **NO se da la vuelta a la resta** (el error nº1: `5-2=3` sería falso): se **CAMBIA una decena por diez unidades** (72 = 6 dec y 12 u), **y no es un préstamo** (no se devuelve nada) — es **la misma moneda que el llevarse de la 7.3, al revés**. Cada resta de columna con **su método** (7.4; y la pizarra cuando el minuendo no cabe, como en la 7.1). **Los tres errores típicos documentados dentro** (34 = dar la vuelta; 36 = olvidar bajar la decena; 24 = las dos). Prueba de hierro: **las 5151 parejas**, con cambio en >2000. Diario: `diario\2026-10-04-unidad-7.5.md`. Guía: v3.6 |
| 2026-10-04 | **Unidad 7.4 (la resta con los dedos) cerrada — LA NOTA 3 DE CARLOS** | **47327/47327 — VERDE**, 30 archivos, 335/335 casos. `dedos: 9 - 4` → `nueve - cuatro = cinco`. Se toma **el PRIMERO**, se **bajan** los del segundo, y los que quedan son el resultado. Es el **mecanismo de la 5.4** y el gemelo de la 7.1, **al revés** (contar atrás). Se verifica por **la vuelta** (la suma deshace la resta, con el mecanismo de la 7.1). Y la condición de la 5.4 («no se puede quitar más de lo que hay») se **REUTILIZA** en vez de escribir otra. Prueba de hierro: **las 66 parejas**. Diario: `diario\2026-10-04-unidad-7.4.md`. Guía: v3.5 |
| 2026-10-04 | **TRES fallos cazados por Carlos leyendo la salida de `columnas: 47 + 15`** | (1) **`7 + 5 = 12` sin decir de dónde sale**: el sistema escribía la suma como si la supiera **de memoria** — cuando la 7.1 dice que no se usa memoria ni calculadora. FIX: cada suma de columna lleva **su método** (`_suma_con_metodo`, con los dedos 7.1). (2) **`4 + 1 + 1 = 6` de golpe**: sumar **tres** números es un método que el sistema **no tiene** (los suyos son de dos). FIX: en **DOS PASOS** (`4+1=5`, luego `5+1=6`). (3) **`6 x 10`**: usaba **multiplicación que no ha enseñado** (la 5.6 no está). FIX: «**6 decenas son 60**», y **quitado de 8 sitios más** del motor (6.2, 6.3, 6.5). Es la misma decisión que la de los rangos `a..j`. **La investigación lo confirma**: la lista de requisitos previos para las columnas incluye «sumar al menos **tres** números de una cifra» y «**explicar las estrategias y registrarlas**» — o sea, Carlos cazó **tres requisitos pedagógicos escritos** |
| 2026-10-04 | **Investigación del orden (petición de Carlos: «haz tu investigación para saber qué sigue»)** | En `investigacion\2026-10-04-que-sigue.md`. **ESSENTIALmaths** (la tabla de pasos): la secuencia es **suma → resta**, y dentro de cada una **sin reagrupar → con reagrupar**; la resta va **justo después** de la suma. **Achieve the Core**: enseñarlas **seguidas** evita el error típico **`82 − 45 = 43`** (restar siempre el dígito pequeño del grande), y «**en Grade 3 el foco principal es la multiplicación**» — o sea, la multiplicación va **después**. **Decisión de Carlos (4 oct)**: **la centena ANTES que la multiplicación**. Orden acordado: **7.4 → resta por columnas → la centena → multiplicar y dividir**
| 2026-10-04 | **FALLO cazado por Carlos: «cuando escribo ayuda solo llega a la unidad 3.1»** | `probar.py` tenía **DOS textos de ayuda**: el **docstring** del fichero (que yo iba actualizando, llegaba a 7.3) y la constante **`AYUDA`** … **que es la que se imprimía**, y se había quedado **congelada en la 3.1**. Lo peor: yo llevaba **varias sesiones diciendo «cabecera actualizada»** refiriéndome al docstring, mientras el usuario veía el otro. Arreglado **de raíz, no copiando el texto otra vez**: `AYUDA = (__doc__ or "").rstrip() + …` → **una sola verdad**, no pueden volver a separarse. Y `probar.py ayuda` (con comillas) **también** da la ayuda (antes lo tomaba por una ESCENA y contestaba `un_objeto`, porque «ayuda» es un nombre de objeto perfectamente válido). **Y una prueba nueva (`test_ayuda.py`, 82 pruebas)** que vigila que la ayuda mencione **todas** las unidades y **todas** las órdenes: si se añade una unidad y no se toca la ayuda, el proyecto se pone ROJO |
| 2026-10-04 | **Unidad 7.3 (sumar por columnas) cerrada — LA NOTA 7 DE CARLOS** | **47220/47220 — VERDE**. Casos **326/326**. **Unidad con unidad, decena con decena, y el llevarse**: `47 + 15` → 7+5=12 (anoto 2, me llevo 1) y 4+1+1=6 → **62**. Y el llevarse **no es un truco: es RE-AGRUPAR** (diez unidades hacen una decena, 6.2); por eso **nunca puede ser más de 1** (9+9=18). El explicador **avisa de olvidarse** de lo que se lleva («diría 5, y sería FALSO»). Prueba de hierro: **las 5151 parejas del rango entero** (todo a+b ≤ 100), 43387 pruebas. Y **`sumar_numeros:` con dos cifras YA funciona** con este método (`32 + 15 = 47`): el aviso `necesito_las_columnas` desaparece de ahí y se queda solo donde toca (`derivar`, que es de una cifra) |
| 2026-10-04 | **FALLO cazado por Carlos preguntando por `32 + 15`** | `sumar_numeros: 32 + 15` daba **`None + None = cuarenta y siete`**: el resultado era correcto pero **la salida estaba rota** (basura delante del usuario). Fallo **que yo introduje en la 6.3** al extender el lector de cifras: `sumar_numeros` empezó a aceptar dos dígitos pero su formateo no. Arreglado **de raíz, no maquillando el `None`**: el sistema **no tenía método** para sumar de dos cifras (regla 13: cada respuesta sale de un método que se pueda seguir; que Python sume por dentro no es un método enseñado), así que **lo dijo** (`necesito_las_columnas`) hasta que la 7.3 le dio el método. Y en el **orden correcto**: primero el **techo** (`no_alcanza` si pasa de cien), después las columnas. Vale para `sumar:`, `anadir:` y `sumar_numeros:`. Los explicadores también lo dicen en vez de reventar con `KeyError` |
| 2026-10-04 | **NOTA NUEVA de Carlos: la resta con los dedos** | «Todavía no hemos llegado a la resta, pero con los dedos **se toma el primer número con los dedos**, se le van **descontando el segundo número** y **los dedos que quedan son el resultado**.» Anotada en `PLAN.md` como **unidad 7.4** (el mecanismo de la resta, gemelo de la 7.1): hoy `quitar:` sabe *qué* es la resta (5.4) pero **no sabe hacerla con los dedos** |
| 2026-10-04 | **Unidad 6.5 (partir en decenas y unidades) cerrada** | **3833/3833 — VERDE**. Casos **307/307**. **Cuánto vale cada cifra**: `47` = 4 decenas + 7 unidades = **40 + 7**; el 4 vale **cuarenta**, no cuatro. Con el **error típico de Oak** dentro (*«transponer los dígitos»*: `4+7=11`) y los **nombres raros** de NZ Maths (`3 decenas y 12 unidades` son **cuarenta y dos**, **no** «treinta y doce»). **Es el requisito de las columnas** (lo dice Oak: hay que partir antes de sumar de dos cifras). Prueba de hierro: **las 101 cantidades**, y la **coherencia con la 6.3** (partir y sitio dan las mismas decenas y unidades) |
| 2026-10-04 | **Unidad 6.3 (la tabla de 100) cerrada — EL SISTEMA YA LEE CIFRAS DE DOS DÍGITOS** | **2975/2975 — VERDE**. Casos **293/293**. `47` → `cuarenta y siete`, y el **sitio** (fila = decenas, columna = unidades). Lo importante: **una sola verdad**. Antes había **cuatro puertas** que decían que no sabía leerlo (`cifra_de`, `comparar_cifras`, `comparar_numeros`, `dedos`): arregladas todas. Y **la prueba de coherencia**: el mismo número leído por **todas** las puertas da la misma palabra. Prueba de hierro: **las 101 cifras de 0 a 100**, una a una |
| 2026-10-04 | **La verificación que pidió Carlos (con la 6.3 dentro)** | Correr todo con el cambio nuevo: **ROJO** (2016/2019). **Todos los 9 fallos eran la MISMA mejora** (casos que decían «no sé leer cifras de dos dígitos» y ahora sí), ninguno rotura: `cifra: diez` → `10`, `palabra: 10` → `diez`, `cifra_de:` de 10 → `10`, `comparar_cifras: 10/2` → `>`, `sumar_numeros: noventa+noventa` → `no_alcanza`, `dedos: 47+3` → ¡funciona! Actualizados **caso por caso**, con el viejo al lado del nuevo. Y **3 incoherencias reales** que no habían saltado: `comparar_cifras`, `comparar_numeros` y `cifra_de` seguían diciendo que no sabían. Arregladas en el **lector común** (`_a_cifra`, `_sitio_cifra`) |
| 2026-10-04 | **Unidad 6.2 (agrupar de diez en diez) cerrada** | **2019/2019 — VERDE**. Casos **271/271**. **El diez como UNA cosa** (el «unitising» de NCETM): los objetos se cogen de diez en diez y cada montón es **una decena**, que se cuenta como una sola cosa. **Es lo que hace posible el valor posicional** y el paso al pensamiento multiplicativo. Con el **error típico de Oak** dentro (no seguir contando de diez en diez al llegar a las unidades) y **dos comprobaciones en cada respuesta**: el reparto cuadra y **el orden no cambia el valor**. Prueba de hierro: **las 101 cantidades de 0 a 100**, una a una, 957 pruebas |
| 2026-10-04 | **Decisión de Carlos (alcance del valor posicional)** | **Quedarnos en el 100** y seguir el orden **6.3 → 6.5 → 7.3** (leer cifras de dos dígitos → partir en decenas y unidades → sumar por columnas con el *llevarse*, que es su nota 7). No subimos a centenas hasta cerrar eso |
| 2026-10-04 | **Unidad 7.2 (derivar / hacer diez) cerrada** | **1062/1062 — VERDE**. Casos **253/253**. **La OTRA vía para sumar, y no cuenta nada**: al primero le faltan unos para diez, se **parte** el segundo en esos y el resto, se hace diez y se suma lo que sobra (`7+5` → `7+3+2`). **Derivar es COMBINAR lo que ya se sabe** (partir 5.1 + llegar a diez 6.1 + sumar a diez 5.2): ningún conocimiento nuevo, solo encadenar. Y **prueba LAS DOS vías** (dedos y derivar) comprobando que dan lo mismo. Prueba de hierro: las **100 parejas**, tres vías comparadas (derivar, dedos, suma), 255 pruebas |
| 2026-10-04 | **FALLO DEL RUNNER cazado (y el mío de taparlo)** | `correr_todas.py` **avisaba** en vez de **fallar** si un archivo no decía su total → daba **VERDE con las 255 pruebas de la 7.2 fuera de cuenta** (el total seguía diciendo 807). Y yo **lo tapé con `tail -15`** (la falta que ya estaba en el carné desde la 5.4). Arreglado el runner (un archivo sin total = FALLO; un archivo que dice `8/10` = FALLO) y anotado en el carné. Ahora **1062/1062** |
| 2026-10-03 | **Lección de método: cuando una prueba falla hay TRES posibilidades** | (1) el motor está roto, (2) la prueba está obsoleta, (3) **yo he escrito mal el valor esperado** — y la tercera fue la más frecuente hoy. Antes de tocar el motor, **ir a mirar qué hace de verdad**. Errores míos de hoy: `range(11)` donde iba `range(101)`; inventarme la clave `maneras` (era `parejas`); suponer conclusiones (`si`/`valido`) sin comprobarlas; una errata («cincico»). Y dos veces el sistema tenía razón y yo no (`siguiente: once` → `sin_numero`; `revisar_secuencia` solo acepta desde el principio) |
| 2026-10-03 | 5.3: la respuesta visible de `cuantos` era la etiqueta interna | Imprimía `RESULTADO: hay_cantidad` en vez de la cantidad. Es una **caja negra en la presentación**: el cálculo estaba bien y lo que se veía no. Arreglado: ahora pone la cantidad |
| 2026-10-03 | 5.3: nunca un traceback delante de quien prueba | `explicar_pregunta` solo capturaba `ValueError`, así que un `KeyError` interno salía como **traceback**. Ahora captura `Exception` y dice «se ha roto algo por dentro». Regla: **el sistema no revienta nunca delante del usuario** |
| 2026-10-03 | 5.3: la traducción estaba en el despacho, no en la función | `siguiente: 3` funcionaba por la orden pero `decidir_3_3_siguiente("3")` no traducía: **dos verdades otra vez**. Movida a las funciones `decidir_*` |
| 2026-10-03 | 5.3: un caso viejo quedó obsoleto (y era una MEJORA) | `comparar_cifras: 3 / tres` esperaba `cifra_desconocida` desde la 4.2, y ahora es correcto que dé `=`: son **el mismo número**. Corregido |
| 2026-10-03 | **FALLO GRAVE cazado por Carlos: el sistema contesta con seguridad algo falso** | Sus tres notas («¿siguiente solo con palabras?», «¿cómo comparo palabras?», «componer/sumar solo con cantidades») destaparon que las operaciones **de cantidad** aceptan **cifras y palabras de número como nombres de objeto**: `sumar: 3 / 2` → **`1 + 1 = 2`** (¡no suma 3+2!), `comparar: 3 / 2` → `tantos_como`, `descomponer: 5` → `1 maneras`. **No es un error: es una respuesta creíble y falsa, y el sistema no avisa.** Es peor que el fallo de `dame:` porque no revienta: pasa por buena |
| 2026-10-03 | **SEGUNDO fallo del mismo tipo: el probador tenía su propia lógica** | `probar.py` duplicaba el despacho y llamaba a las funciones viejas de 2.2; el cambio de la 3.3 no le llegó. **Arreglado:** se borraron las funciones huérfanas del motor y **`correr_todas.py` ahora corre también los casos**, para que las dos vías se vigilen solas |
| 2026-10-03 | **Caso viejo que quedó obsoleto, cazado por correr TODO** | `palabra: 0` esperaba `cifra_desconocida` desde la 3.1, y ahora el 0 **sí** es una cifra. Corregido. (Regla del método: correr siempre los casos viejos, no solo los de hoy) |
| 2026-10-03 | 2.4 usa la tarea fiable | **Give-N** (word-to-set), no la tarea «¿cuántos hay?». El sistema se **verifica a sí mismo** (recontar) y es un *counter*, no un *grabber* |
| 2026-10-03 | 2.2 no cuela el sucesor | Se aprende el ORDEN DE LA LISTA, no «uno más»: la investigación (Sarnecka & Carey 2008) sitúa el sucesor DESPUÉS de la cardinalidad |
| 2026-10-03 | **Primera deducción del sistema** | 2.1: dada una colección, produce el emparejamiento objeto↔palabra que no se le dio; y sabe decir CUÁL de los tres errores tiene una cuenta mal hecha |
| 2026-10-03 | Cambio de orden del plan | 1.1–1.4 aplazadas por decisión de Carlos; se pasa a 2.x. Anotado en `PLAN.md` |
| 2026-10-03 | Reglas de 0.2 | 10 (5 para reconocer, 5 para formar), tras añadir la de entidad contradictoria |
| 2026-10-03 | Primitivas del motor | 23 en total (contadas del codigo) |
| 2026-10-05 | **Revisión de Claude (Cowork) mientras Euclides estaba sin saldo** | **Git** (`6a446c9` punto de retorno). **Motor partido** en `sistema/partes/` (una pieza por nivel; `motor.py` es la fachada) con la salida de las pruebas **idéntica byte a byte**. El empaquetador del móvil embebe las piezas |
| 2026-10-05 | **OCHO puertas mintiendo con tres cifras, tapadas por el verde** | `columnas: 247+385` sumaba 24+38 «sin método» (caja negra); `restar_numeros: 50-27` daba `None - None` (desde la 6.3); `diferencia_numeros` igual; `sumar_numeros: 900+900` → `KeyError`; `nombre: 247` → `fuera_de_mi_secuencia` mientras el probador decía otra cosa; `sitio:`/`partir:` 247 → fuera_de_la_tabla; `palabra: 247` con traza «DOS cifras» y 247 asteriscos. **Todo arreglado** |
| 2026-10-05 | **Unidades 6.7 y 7.6 cerradas** | **57358/57358 — VERDE**, 33 archivos, **386/386** casos |
| 2026-10-05 | **R.1 abierta: el resolvedor** | **57409/57409 — VERDE**, 34 archivos, **400/400** casos. Prueba de dominio: 3 de 5 problemas no programados resueltos y 2 `no_entiendo` honestos (falta la forma «se le escapan» y el posesivo «su hermano») |
| 2026-10-05 | **El proyecto pasa a Claude** (decisión de Carlos). Método en `METODO.md` | — |
| 2026-10-05 | **Cálculo mecánico de verdad** (`mecanismo.py`): recitar, dedos con nombre, leer/escribir cifras. Antes el total salía de un `a + b` de Python | Verde sin tocar pruebas; rango entero de la 7.6: **1.003.002 cuentas, 0 fallos** |
| 2026-10-05 | **Pruebas optimizadas**: una prueba = una afirmación; rápido + `--hierro` | **1500/1500 afirmaciones + 374/374 casos, 10 s** (antes «57409», 83 s) |
| 2026-10-05 | **R.1: los 11 tipos de CGI** (faltaban los de cambio desconocido) | `test_R_1` G: 11/11 |
| 2026-10-05 | **Paso 1 del plan: ni las condiciones usan calculadora** | `sumar_por_columnas`, `juntar_decenas`, `parejas_que_suman`, `coleccion_de`, `contar_todo` en `mecanismo.py`; 5.1/5.2/5.4/5.5 con objetos ahora juntan, sacan y emparejan objetos de verdad; la tabla de 100 se recita. **`test_sin_calculadora.py`** lee el código y vigila. **1502/1502 + 374/374, verde** |
| 2026-10-06 | **F.3 sumar y restar fracciones dentro de un entero** (NCETM 3.4; noche) | `2/7 + 3/7`, `5/7 - 2/7`, `1 - 3/8`: los de arriba con las piezas, el de abajo se queda (y se dice el error 5/14), la tira y la vuelta. `test_F3` 12/12 (todas las cuentas con b ≤ 12). Proyecto **1970/1970 + 556/556 VERDE**. **3.º completo.** Pendiente: la prueba de Carlos |
| 2026-10-06 | **F.2 fracciones no unitarias; recta; comparar** (NCETM 3.3; 3.NF.A.2, A.3c, A.3d; noche) | No unitarias hasta un entero (`3/4 de 12`, `entero: 3/4 es 9`, `4/4` un entero, `3/1`), `recta: 3/4` dibujada; piezas `fracciones_mismo_denominador` / `_mismo_numerador`; sin nada en común: todavía no (5.º). `test_F2` 16/16; proyecto **1956/1956 + 550/550 VERDE**. Pendiente: la prueba de Carlos |
| 2026-10-06 | **F.1 la parte y el todo; fracciones unitarias** (NCETM 3.1, 3.2; 3.NF.A.1; noche, Carlos duerme) | Parte `fracciones.py`: `fraccion:`, `1/4 de 12` (repartir), `comparar: 1/3 y 1/5` (pregunta `comparar_fracciones`: la regla y la tira), `entero: 1/4 es 3`, `partes: 12 = 4 + 4 + 4`. `test_F1` 23/23; proyecto **1938/1938 + 542/542 VERDE**. Pendiente: la prueba de Carlos |
| 2026-10-06 | **E.6 ¿es razonable? estimar redondeando** (3.OA.D.8; Carlos aprobó N.2) | Parte `estimar.py`: `estimar:` (redondear cada número, cuenta fácil, la BANDA de lo que se pudieron mover) y `razonable:` (fuera de la banda, mal seguro; dentro, razonable — y luego la cuenta de verdad: razonable no es correcta). `test_E6_razonable` 19/19 (813 respuestas malas típicas); proyecto **1913/1913 + 534/534 VERDE**. Pendiente: la prueba de Carlos |
| 2026-10-06 | **N.2 redondear a la decena y a la centena** (3.NBT.A.1; Carlos aprobó E.5) | Pregunta `redondear` con dos caminos que tienen que coincidir: `redondear_en_la_recta` (los dos lados, la mitad del camino, de cuál está más cerca; la mitad por convenio) y `redondear_por_la_cifra` (el atajo). Orden `redondear:`; aviso de la trampa de la cadena (247 → 250 → 300). `test_N2_redondear` 25/25; proyecto **1892/1892 + 526/526 VERDE**. **Probado por Carlos** |
| 2026-10-06 | **E.5 dos pasos, con la letra como hueco** (3.OA.D.8; Carlos aprobó M.6) | Parte `letra.py`: ecuaciones con letra y varias operaciones, el orden de siempre, parentesis, DESHACER hacia atras y comprobar poniendo el numero; `todavia_no`/`no_sale`/`sin_letra`. Problemas de dos pasos en `resolver_r2.py` con su ecuacion (`3 x 4 - 5 = c`). `test_E5_dos_pasos_letra` 31/31; proyecto **1865/1865 + 517/517 VERDE**. Termina el plan ajustado. **Probado por Carlos** |
| 2026-10-06 | **M.6 tabla del 7 y la distributiva** (NCETM 2.9, 2.10; 3.OA.B.5, C.7; Carlos aprobó M.5; **probado**) | Pieza `multiplicar_partiendo` (7 = 5 + 2; también fuera de las tablas: 12 x 6); `tabla del 7`; par/impar del producto y números cuadrados; `divisible` con cualquier divisor; `aprender: tablas` → **todas hasta 10 × 10** (memoria: 317 hechos). `test_M6_tabla7_distributiva` 16/16; proyecto **1832/1832 + 509/509 VERDE**. Pendiente: la prueba de Carlos |
| 2026-10-05 | **M.5 tablas del 3, 6 y 9** (NCETM 2.8; Carlos aprobó M.4) | `tabla del 3/6/9` (de 3 en 3; doble; triple), `multiplicar_doblando` también para el 6, pieza `multiplicar_triplicando`, `divisible: N entre 3/6/9` (suma de cifras), `aprender: tablas` en orden (memoria: 312 hechos). `test_M5_tablas_3_6_9` 14/14; proyecto **1814/1814 + 502/502 VERDE**. Pendiente: la prueba de Carlos |
| 2026-10-05 | **M.4 tablas del 4 y del 8, doblando** (NCETM 2.7; Carlos aprobó R.2) | Pieza `multiplicar_doblando` (hecho derivado: solo si la mitad se sabe); `tabla del 4/8`; `divisible: N entre 2/4/8` con mitades; `aprender: tablas` en orden 2→4→8 (memoria: 285 hechos). `test_M4_tablas_4_8` 13/13; proyecto **1797/1797 + 492/492 VERDE**. Pendiente: la prueba de Carlos |
| 2026-10-05 | **R.2 problemas de × y ÷ con pocas palabras** (3.OA.A.3; Carlos aprobó E.4) | Parte `resolver_r2.py` (formas rústicas, ESQUEMA de grupos iguales llenado por los nombres, barra de Singapur, comprobación con E.0) y 3 piezas de «paso_por» (multiplicar / repartir / agrupar). «cada» con × y con ÷; R.1 intacto. `test_R2_problemas_por` 16/16; proyecto **1781/1781 + 484/484 VERDE**. Pendiente: la prueba de Carlos |
| 2026-10-05 | **Plan ajustado** (Carlos: «ajusta el plan a lo que la pedagogía dicta», sin repaso mezclado) y **E.4 el hueco en × y ÷** (3.OA.A.4) | El sitio del hueco dice qué se busca (NCETM 2.6: repartir / agrupar / deshacer); sin conocimiento nuevo; comprobación con E.0 (que ya entiende `:`). `3 x ? = 13` no entero; `0 x ? = 0` cualquiera. `test_E4_hueco_por` 19/19 (720 ecuaciones); proyecto **1765/1765 + 475/475 VERDE**. Pendiente: la prueba de Carlos |
| 2026-10-05 | **M.3 dividir: repartir y agrupar** (NCETM 2.6; Carlos aprobó M.2) | Pregunta «dividir» (casos especiales / la tabla: factor desconocido / la mitad / saltando con resto); `12 entre 3`, `12 en grupos de 3`, `12 : 3`; comprobación multiplicando; `8 : 0` imposible. `test_M3_dividir` 16/16 (1010 divisiones); proyecto **1744/1744 + 464/464 VERDE**. Pendiente: la prueba de Carlos |
| 2026-10-05 | **M.2 tablas del 2, 5 y 10; conmutativa; dobles y mitades** (NCETM 2.3–2.5) | 4 piezas de multiplicar (cero/uno, memoria, dobles, la otra lectura); `tabla del N`, `mitad: N`, `aprender: tablas` (57 productos, comprobados con la otra lectura); `3 x 4 = 4 x 3` verdadero sin calcular. `test_M2_tablas` 23/23; proyecto **1725/1725 + 455/455 VERDE**. Pendiente: la prueba de Carlos |
| 2026-10-05 | **M.1 multiplicar = grupos iguales** (3.OA.A.1; NCETM 2.2; Carlos aprobó M.0) | Pregunta «multiplicar»: a x b = a grupos de b = la suma de iguales de M.0 (sin cuenta nueva). Grupos de 0 y de 1; grupos desiguales → suma. `3 x 4 = ?` ya no se lee como `4 = ?`. `test_M1_multiplicar` 16/16; proyecto **1699/1699 + 445/445 VERDE**. Pendiente: la prueba de Carlos |
| 2026-10-05 | **M.0 filas y columnas como sumas iguales** (2.OA.C.4; Carlos aprobó N.1) | Parte `filas.py` (dibuja, escribe 4 + 4 + 4, cuenta por filas y por columnas); pregunta «suma de iguales» (saltando si son de 2/5/10; si no, grupo a grupo). `3 x 4` → todavía no. `test_M0_filas` 15/15; proyecto **1681/1681 + 436/436 VERDE**. Pendiente: la prueba de Carlos |
| 2026-10-05 | **N.1 contar de n en n; par o impar** (2.NBT.A.2, 2.OA.C.3, NCETM 2.1; Carlos aprobó E.2) | Mecanismo `saltar`; orden `de 5 en 5 ...`; pregunta «paridad» (emparejar hasta 20 con su doble; la última cifra después); `contar_hasta_de_diez_en_diez` (47 + ? = 77 → 3 saltos). `test_N1_saltos` 19/19; proyecto **1664/1664 + 429/429 VERDE**. Pendiente: la prueba de Carlos |
| 2026-10-05 | **E.2 el `=` como balanza** (Carlos aprobó E.1) | Pregunta «balanza» con 3 piezas (mismo número / compensar sin calcular / calcular un plato). `8 + 4 = ? + 5` → 7, y descarta 12 y 17 con E.0. `57 + 22 = ? + 21` → 58 sin calcular. `test_E2_balanza` 14/14 (1586 balanzas); proyecto **1643/1643 + 420/420 VERDE**. Pendiente: la prueba de Carlos |
| 2026-10-05 | **E.1 ecuaciones con hueco** (1.OA.D.8; Carlos aprobó E.0) | Parte `ecuaciones.py`: lee la ecuación, la cuenta como historia (CGI) y la resuelven las piezas de pasos de R.1 — **sin conocimiento nuevo**; se comprueba con E.0. Escrita directamente; `8 + 3` ya no cae en la 0.1. `test_E1_hueco` 22/22 (1440 ecuaciones); proyecto **1629/1629 + 414/414 VERDE**. Pendiente: la prueba de Carlos |
| 2026-10-05 | **E.0 el `=`: verdadero o falso** (1.OA.D.7; Carlos aprobó P.6) | Pregunta nueva «igualdad» con 3 piezas (escrito igual / dar la vuelta, sin calcular / calcular cada lado). Orden `verdad:`. `4 + 1 = 5 + 2` → FALSO y dice la trampa; cadenas; `10 = 8 + 2`. `test_E0_igual` 17/17; proyecto **1605/1605 + 404/404 VERDE**. Pendiente: la prueba de Carlos |
| 2026-10-05 | **P.6 restar pensando en sumar** (1.OA.B.4; Carlos aprobó P.5) | Pieza `restar_contando_hacia_arriba`: 13 − 8 → «del 8 al 13: 9, 10, 11, 12, 13 → 5, porque 8 + 5 = 13»; solo si están cerca y es más corto que hacia atrás. `test_P6_hacia_arriba` 11/11; proyecto **1587/1587 + 395/395 VERDE**. Pendiente: la prueba de Carlos |
| 2026-10-05 | **Plan pedagógico** (Carlos: «velocidad pedagógica», «cada paso como un plan») y **P.5 dar la vuelta** (1.OA.B.3) | Investigación: antes de las ecuaciones faltaban la conmutativa y restar pensando en sumar. Nuevo orden en `PLAN.md`. Pieza `sumar_dando_la_vuelta` (3 + 47 = 47 + 3). `test_P5_vuelta` 11/11; proyecto **1576/1576 + 389/389 VERDE**. Pendiente: la prueba de Carlos |
| 2026-10-05 | **Paso 4: TÉCNICAS para ir más rápido** | 5 piezas nuevas: `sumar_de_diez_en_diez`, `restar_de_diez_en_diez` (la cifra de las decenas sube/baja: mecanismo nuevo `subir_una_decena`/`bajar_una_decena`), `sumar_compensando`, `restar_compensando`, `sumar_casi_dobles` (solo si el doble se sabe de memoria). Orden nueva `calcular: 47 + 30` (y `calcular sin memoria:`) que enseña TODOS los métodos. `test_tecnicas` 21/21; proyecto **1565/1565 + 384/384 VERDE** |
| 2026-10-05 | **Paso 3: la MEMORIA de hechos** (decisión de Carlos: memorizar es válido según avanza el aprendizaje) | `sistema/partes/memoria.py`, piezas `recordar_suma`/`recordar_resta`, órdenes `memoria`, `aprender: sumas|restas`, `olvidar: todo`. **200 hechos** aprendidos (100 sumas + 100 restas), todos comprobados por la vuelta **y por dos caminos**. `test_memoria` 19/19; proyecto **1543/1543 + 375/375 VERDE** |
| 2026-10-05 | **Paso 2: la base de PIEZAS** (idea de Carlos) | 17 piezas en `conocimiento/piezas/`; motor de piezas sin matemáticas; el método más corto que encaja; prueba de fuego: una pieza nueva entra sin tocar el motor. **1521/1521 + 375/375, verde** |
