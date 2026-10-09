# CLAUDE.md — Euclides (instrucciones para cualquier sesión de Claude, también en la nube)

**Idioma: español con Carlos.** El rumbo lo decide Carlos; la técnica pequeña, Claude.

## Al empezar, leer (en este orden)
1. `METODO.md` — el método y las reglas que no se rompen (sobre todo: SIN CALCULADORA).
2. `PLAN.md`, sección «AÑOS ESCOLARES» — el orden de los pasos (NCETM por Year + Common Core).
3. `PROGRESO.md` (las últimas filas) y el último archivo de `diario/` — dónde se quedó.
4. `FUENTES.md` — las fuentes pedagógicas ya leídas.

## Cómo se trabaja (Carlos)
- **Velocidad pedagógica, un paso cada vez.** Para cada paso:
  1. Investigar la pedagogía (NCETM primero: https://ncetm.org.uk/classroom-resources/primm-... ;
     Common Core) y **escribir el plan en `diario/AAAA-MM-DD-paso-XX-nombre.md`** ANTES de programar:
     lo que dice la fuente, cómo lo haría un humano sin calculadora, lo que se construye, las trampas,
     la prueba de dominio.
  2. Construir. 3. Probar (prueba de dominio contra un testigo + la batería entera en verde).
  4. Cerrar: resultado en el diario, fila en `PLAN.md` y `PROGRESO.md`, fuente en `FUENTES.md`,
     ayuda en `probar.py`, casos en `mis_casos.txt` y `mis_pruebas.txt`,
     `python3 herramientas/empaquetar_movil.py`, commit.
- «Ajusta el plan a lo que la pedagogía dicta.» «Cada cosa, una a una.» Sin repaso mezclado.
- **«Debe trabajar como lo haría un humano sin calculadora.»** Las cuentas las hace el mecanismo y
  las piezas; Python es solo el TESTIGO en las pruebas.
- Carlos prueba en su PC con `MIS_PRUEBAS.bat` / `PROBAR.bat`. Lo que él no ha probado se marca
  «falta la prueba de Carlos».

## Convenciones técnicas (para no romper nada)
- El motor está partido en `sistema/partes/*.py`, unidos por el orden de `sistema/partes/__init__.py`.
  **Un nombre solo puede definirse en UNA parte** (guardia «dos verdades»): las funciones privadas
  nuevas llevan prefijo propio (`_fr_`, `_dec_`, `_neg_`…). Una parte nueva se añade a ese orden.
- Las piezas (métodos) viven en `conocimiento/piezas/*.py` (`PIEZA` + `hacer(s, u)`); sus
  condiciones en `_condiciones.py`, las preguntas en `_objetivos.py`. Una pieza no puede `usar` su
  propia pregunta. Si `vuelta_ok` es False, su respuesta no vale.
- Auditoría sin calculadora (`pruebas/test_sin_calculadora.py`): nada de `a + b`, `a * b`… con
  variables en el motor. Usar `aplicar("sumar", ...)`, `siguiente`, `viene_despues`, formato de texto
  (`"%s%s" %`), `.extend`, `rjust`, `range(k, 0, -1)`.
- Dos techos: contar OBJETOS hasta diez mil (`techo_de_contar`); los NÚMEROS hasta diez millones desde N.6
  (`numero_maximo`: el techo más alto de `conocimiento/el_millon.kn` y `los_millones.kn`).
- Las órdenes se enrutan en `sistema/partes/explicacion.py` (`explicar_pregunta`) y en
  `probar.py` (`preguntar`); el orden de las comprobaciones importa.
- Cada archivo de prueba imprime `TOTAL: x/y`, usa memoria temporal (`EUCLIDES_MEMORIA`).

## Comandos
- Batería entera: `python3 pruebas/correr_todas.py` (≈1 min; debe salir todo en verde).
  Si el entorno corta los comandos largos (≈3 min), se corre en dos mitades seguidas:
  `python3 pruebas/correr_todas.py --parte 1/2` y luego `--parte 2/2` (los casos van en la última).
- Casos de Carlos: `python3 probar.py --archivo mis_pruebas.txt`;  casos: `python3 probar.py --casos`.
- Una pregunta: `python3 probar.py "recta: 3 - 8"`.

## Git
- Trabajar en una rama y empujarla; **no tocar `main`** sin que Carlos lo diga (él la baja a su PC y prueba).
- Al final de cada mensaje de commit:
  `Co-Authored-By: Claude <noreply@anthropic.com>`

## Lecciones de las revisiones (las añade la sesión que revisa; leerlas antes de construir)
- **Una pieza nueva debe COMPROBARSE a sí misma** (`vuelta` real con la operación contraria y
  `vuelta_ok` según salga), no devolver `"vuelta": "", "vuelta_ok": True` sin comprobar nada.
  (Revisión de M.12: las piezas `*_escalando` no lo hacen; queda pendiente.)
- **Probar cerca del techo** (999 999, 1 000 000, productos que se pasan): una condición que llama a
  `decir`/`viene_despues` con un número sin nombre lanzaba KeyError (ya lo atrapa `aplicar`).
- **Nada de contar de uno en uno con números grandes**: un salto grande es una SUMA, no 243 225 pasos.
  Medir el tiempo de casos grandes; si una pregunta tarda más de 2-3 s, algo no es humano.
- **Respetar el año**: dividir entre números de dos cifras con muchos saltos es la división larga
  (6.º, NCETM 2.24); hasta entonces, «todavía no».
- **Comparar tamaños con el mecanismo** (`viene_despues(decir(a), decir(b), saber)`, o `u.viene_despues`
  en las piezas), no con `<`/`>` de Python, en el código NUEVO. (Revisión de M.15: `factores.py` y
  `parejas_de_factores_en_orden.py` ya corregidos.) **DEUDA conocida:** el código viejo tiene ~90
  comparaciones con Python (muchas son legítimas: índices, sangrías, leer archivos; otras miran el tamaño
  de números, p. ej. `primitivas.py`, `nivel_5.py`, `nivel_6.py`). La auditoría aún no las vigila.
  Pasarlas al mecanismo y ampliar `test_sin_calculadora.py` con su lista blanca será un paso aparte.
- **Pendientes de la revisión de M.14:** (RESUELTOS) `99 x 99 x 99` → 970299 desde M.18 (se comprueba dividiendo con
  la división larga); `101 x 100 x 100` → 1010000 desde N.6 (el techo es diez millones).
- **IDEA PARA EL FUTURO (no hacer sin que Carlos lo pida; 7 oct):** elegir la técnica según lo que CUESTA
  en este caso, como un humano de un vistazo. Hoy cada pieza tiene una `rapidez` fija y, para que no haga
  cosas inhumanas con números grandes, se han ido poniendo topes sueltos (grupos iguales ≤ 12, saltos ≤ 100
  o ≤ 1000, contar...). La idea: que cada pieza estime cuántos pasos le costaría ESTE caso y se elija la más
  barata entre las aprendidas; una regla general («nadie repite algo cientos de veces si sabe otra manera»)
  en lugar de los topes. Carlos (7 oct): «en el futuro vemos si es necesario; si no, no».

## ✅ EL PLAN U ESTÁ CUMPLIDO (9 oct): se ha vuelto al orden de NCETM (6.º)
**REGLA desde el plan U (Carlos, 9 oct): lo nuevo entra por el MODELO COMÚN.** Las técnicas nuevas son PIEZAS (operadores)
que el resolvedor universal puede usar en cualquier problema; **no se abre ninguna puerta ni formato nuevo** para un tema.
Cualquier expresión o ecuación que permita el tema tiene que salir por la tabla de puertas (`puertas.py`) y el resolvedor.

## (HECHO) EL PLAN U (8 oct)
El avance por años estuvo en PAUSA. Se trabajó el **plan U** (`diario/2026-10-08-PLAN-U-volverlo-universal.md`),
una fase por sesión, en orden. Regla de oro del plan: **prohibido memorizar problemas o familias de problemas**;
solo relaciones generales (datos), operadores generales (piezas) y búsqueda con control. Nada viejo cambia de
respuesta; lo nuevo, con pocas pruebas representativas. Si la batería tarda demasiado, `--parte 1/3`, `2/3`, `3/3`.
**DECISIÓN DE CARLOS (8 oct): «cuanto más se avanza en matemáticas, menos se habla».** El centro es el problema escrito
con NÚMEROS Y SÍMBOLOS; la parte hablada (U.3, U.3b) NO se sigue ampliando (se queda como está), salvo la REGLA DE
PRUDENCIA: nunca una respuesta falsa (un número que se queda sin usar y no se sabe si sobra, una frase con un cambio que no
se entendió, una respuesta que mezcla cosas → «no entiendo», diciendo qué frase o qué número). La fase U.3c, descartada.

## Dónde se quedó (9 oct 2026, tras el arreglo A.1)
Hecho **A.1 el cero al despejar** (ARREGLO de prudencia, no NCETM; diario `2026-10-09-arreglo-A1-el-cero-al-despejar.md`):
el resolvedor y la puerta vieja E.5 daban respuestas FALSAS con el 0 (`resolver: 0 : r = 0 : 5` → «ninguna»; `0 x r = 0 x 5`
→ «r = 5»; `(r - 2) x (r - 2) = 1` → «ninguna»). Arreglado en la capa general: al deshacer y al aislar se MIRA el 0 delante
de una división; «el mismo número a los dos lados» no vale con el 0; el tope de probar en orden no para mientras lo que se
multiplica es negativo. «Cualquier número menos el 0» se dice como «todavía no» con el porqué (no hay forma de respuesta para
eso: pregunta para Carlos). **Lección:** antes de dar «ninguna» o un número, mirar si algo que divide o multiplica puede ser 0.
**Siguiente: NCETM 2.28** (combinar la división con la suma y la resta; el orden de las operaciones).

## Dónde se quedó antes (9 oct 2026, tras M.21)
Hecho **M.21 el factor de escala y la tabla de razón** (NCETM 2.27, *Scale factors, ratio and proportional reasoning*; diario
`2026-10-09-paso-M21-escala-y-razon.md`): la pregunta de piezas `proporcion` con tres PIEZAS (entre las filas = el factor de
escala 5; dentro de la fila 5.5; pasando por una fila más pequeña 7, con `simplificar_fraccion`), cada una con su vuelta. El
resolvedor las pide (`_u_proporcion` en `_u_despejar`, `universal.py`) al ver `a : b = c : ?` (o `a/b = c/?`) con la letra sola;
si no sale justo, deshace como antes. Se pregunta con `resolver: 2 : 5 = 6 : r` (sin puerta nueva). **Siguiente: NCETM 2.28**
(combinar la división con la suma y la resta; el orden de las operaciones): ahí se decide `(3 + 5 + 7) : 3` sin letras.

## Dónde se quedó antes (9 oct 2026, tras M.20)
Hecho **M.20 la media** (NCETM 2.26; diario `2026-10-09-paso-M20-la-media.md`): la pregunta de piezas `media` con dos PIEZAS,
`media_juntando_y_repartiendo` 9 (sumar y repartir) y `media_nivelando` 5 (la base es el más bajo y lo de encima se reparte
entre todos; solo si están cerca: el costo; vuelta por el EQUILIBRIO). El resolvedor las pide (`_u_media`, `universal.py`)
al ver `(v1 + … + vk) : k` con k = cuántos valores. Se pregunta con `resolver:` (sin puerta nueva); `(3 + 5 + 7) : 3` sin
letras sigue «todavía no» (2.28): pregunta abierta para Carlos. **Siguiente: NCETM 2.27** (mirar en el buscador qué es).

## Dónde se quedó antes (9 oct 2026, tras M.19)
Hecho **M.19 calcular compensando** (NCETM 2.25; diario `2026-10-09-paso-M19-compensar.md`): dos PIEZAS de `multiplicar`,
`multiplicar_redondeando_un_factor` 6.5 (399 x 6 = 400 x 6 − 6; solo a 1 o 2 por debajo de un redondo de una cifra: el
costo) y `multiplicar_por_5_o_25_compensando` 6.6 (x 10 y la mitad; x 100 y la mitad de la mitad), cada una con su vuelta.
Sumar y restar compensando ya era de P.7. Pregunta abierta: derivar de un hecho con x y : (`si 3 x 8 = 24: 30 x 8 = ?`).
**Siguiente: NCETM 2.26** (la media y el reparto igual; mirar en el buscador).

## Dónde se quedó antes (9 oct 2026, tras M.18)
Hecho **M.18 dividir entre dos cifras: la división larga** (NCETM 2.24; diario `2026-10-09-paso-M18-division-larga.md`): dos
PIEZAS de `dividir`, `division_larga` 9.5 (la lista de múltiplos del divisor SUMANDO, restar debajo y bajar la cifra, el 0 del
cociente; vuelta: cociente x divisor + resto) y `dividir_por_un_divisor_compuesto` 9.2 (: 24 = : 4 : 6, solo justas). El
cociente menor que 10 sigue con los saltos (punto 1). Sin puerta nueva: los «todavía no» que pedían la larga salen solos por
el modelo común (`24 x n = 8544`, factores y primos hasta 99 x 99, comprobar tres factores dividiendo, simplificar). Entre
TRES cifras, todavía no. **Siguiente: NCETM 2.25** (mirar en el buscador qué es; la web de NCETM sigue bloqueada).

## Dónde se quedó antes (9 oct 2026, tras M.17)
Hecho **M.17 estrategias para multiplicar números grandes y la multiplicación larga** (NCETM 2.23; diario
`2026-10-09-paso-M17-multiplicacion-larga.md`): cuatro PIEZAS de `multiplicar` (`multiplicar_quitando_los_ceros` 7.5,
`multiplicar_partiendo_un_factor` 9.1 —detrás de M.6, 9—, `multiplicar_por_un_factor_compuesto` 9.2, `multiplicacion_larga` 9.5; la rejilla, 10,
queda para quien no sabe las tablas), cada una con su vuelta por la operación contraria (la división entre una cifra se hace
dentro de la pieza, `_repartir`: usar la pieza `division_corta` haría una vuelta en el mapa, porque ella usa `multiplicar`).
Sin puerta nueva: el resolvedor dice con qué multiplicó (`numero.py`) y comprueba DESHACIENDO lo que todavía no sabe
calcular (`_u_comprobar_deshaciendo`: `n : 24 = 356` → 8544 porque 356 x 24 = 8544). Las piezas que explican su vuelta
llevan `vuelta_explicada` (el explicador de M.1 la enseña). **Siguiente: NCETM 2.24, la división larga.**

## Dónde se quedó antes (8 oct 2026, tras U.4)
Hecho **U.1 el modelo y el lector simbólico** (partes `numero.py`, prefijo `_nu_`, y `universal.py`, prefijo `_u_`; puerta
`resolver:`) y **U.2 buscar con control** (parte `buscar.py`, prefijo `_bu_`: juntar relaciones, reescribir —bloque que ya se
sabe, factor común—, probar en orden con tope y sabiendo cuándo parar, el control por medios y fines con costes en
`conocimiento/universal.kn`; S.3 lee con el lector único y S.2 se traduce al modelo como otra estrategia). La red de
seguridad, en las dos cadenas: si una puerta vieja dice NO ENTIENDO, o TODAVÍA NO a algo con una relación con letras, y el
resolvedor lo resuelve y lo comprueba, contesta él (las cuentas sin letras siguen respetando el año). «de» tras una
fracción o un decimal es POR.
Hecho **U.3 el lector de palabras** (parte `palabras.py`, prefijo `_pa_`; el vocabulario en `conocimiento/frases.kn` y las
estructuras y lo que se sabe —figuras, consecutivos— en `conocimiento/relaciones.kn`): frase a frase → relaciones del mismo
MODELO, que busca U.2. Entra por `resolver:` con palabras y por la red de seguridad de las palabras (si R.1, R.2, la escala...
no llegan). Una palabra nueva se añade en `frases.kn`, nunca en el código; una palabra no puede tener dos sentidos (se avisa).
Hecho **U.3b la cosa de cada cantidad** (en `palabras.py`; tras la revisión de U.3, que halló respuestas falsas): cada cantidad
es (de quién, de qué cosa) —la primera cosa conserva el nombre (`maria`), otra es `maria_lapiz`—; solo se suman o restan las de
la misma cosa (`_pa_comprobar_cosas`, en el modelo); «cada», «N u por X» y los verbos de cada (`frases.kn`) son grupos iguales;
comprar con dinero es gastar; las cosas genéricas (dinero, edad...), las parejas y dimensiones de las figuras, en datos.
Hecho **U.4 una sola tabla de puertas** (parte `puertas.py`, prefijo `_pu_`, la última del orden): la tabla `PUERTAS`, la
misma para `explicar_pregunta` y `responder_pregunta` (`probar.preguntar` es una línea). **Una puerta nueva se añade en esa
tabla, en su sitio del orden** (ya no en dos cadenas). La regla de la red, una sola (`_pu_decidir`): lo simbólico no lo cogen
las puertas de los objetos; si una puerta vieja no da una respuesta y es una relación con letras, decide el resolvedor;
«ningún número para contar» (no_sale, imposible, no_entero, ninguna) es respuesta del año y la explicación enseña también lo
del resolvedor; una cuenta sin letras respeta el año. E.5 es traductor (lee con `_u_leer`); `ecuacion:` y `calcular:` son
«solo para contar». Identidades (desarrollar con la distributiva, `_bu_identidades`) → `cualquiera`. La prudencia con
palabras (`_pa_prudencia`). `herramientas/comparar_puertas.py` compara las puertas viejas con el resolvedor (0 sin explicar).
**Siguiente: U.5 — el examen de transferencia** (secreto, fuera del repositorio). Preguntas abiertas para Carlos (diario de
U.4): si los «no hay número para contar» pasan ya a fracción/negativo; si dos `?` son el mismo número.
Antes: S.3 problemas con dos incógnitas (NCETM 1.31), N.6 hasta diez millones (NCETM 1.30), F.7, F.6, P.7.
Al acabar el plan U se vuelve a NCETM (Spine 2: **2.23**; la división larga 2.24; Spine 3 tras 3.8).
La balanza y `verdad:` con decimales: todavía no (solo enteros) por sus puertas viejas; por `resolver:` sí.
Las fracciones de partida en `comparar:` y en las cuentas (puertas viejas) siguen limitadas a medios…doceavos, décimos,
centésimos y milésimos (el de abajo común puede ser cualquiera hasta el techo). `comparar:` por el mismo de arriba no sale
si pide dividir entre dos cifras (la división larga, 6.º); el del mismo de abajo sí.
Ojo: `test_F7` tiene una prueba de tiempo (`999 1/2 + 999 1/3` < 2 s) que en la nube a veces da 2,1 s (ya pasaba antes de U.1).
