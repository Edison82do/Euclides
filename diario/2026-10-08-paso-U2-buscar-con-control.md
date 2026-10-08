# Fase U.2 — BUSCAR CON CONTROL — 8 oct 2026

Segunda fase del **plan U** (`diario/2026-10-08-PLAN-U-volverlo-universal.md`). Regla de oro: **prohibido memorizar
problemas o familias de problemas**; solo relaciones generales, operadores generales y búsqueda con control. Nada viejo
cambia de respuesta; lo nuevo, con pocas pruebas representativas.

## 1. EL PLAN (escrito antes de programar)

**Lo que dicen las fuentes** (ya en `FUENTES.md`):
- **Newell y Simon (GPS, medios y fines)**: comparar lo que se tiene con lo que se busca y aplicar el operador que MÁS
  reduce la diferencia. Aquí la diferencia se mide en **letras que faltan**: el operador bueno es el que deja una
  relación con menos letras (lo mejor: con una sola, que ya se calcula despejando).
- **Schoenfeld (1979), el CONTROL**: saber las técnicas no basta; hay que elegir CUÁNDO usar cada una, primero lo barato,
  y vigilar si se avanza. → Cada operador tiene un COSTE (en datos, `universal.kn`); en cada paso se miran TODOS los que
  encajan, se descartan los que no bajan las letras, y se elige el más barato de los que más bajan. Con presupuesto.
- **NCETM 1.31** (dos incógnitas): punto 3, la barra enseña la estructura; punto 4, con la suma y la diferencia **se
  quita la diferencia** (juntar dos relaciones: restarlas); punto 5, lo que no se deja dibujar **se prueba en orden**,
  de forma sistemática, y puede tener una, varias o ninguna.
- **Pólya**: trabajar hacia atrás (despejar), **buscar un problema auxiliar** (reescribir: `2 x a + 2 x b = 20` es dos
  veces `a + b = 10`; un bloque que ya se sabe), simplificar.
- **NCETM 2.20–2.22 y M.12/P.7/F.6** (lo que ya sabe): la propiedad distributiva y sacar factor común (`2 x a + 2 x b =
  2 x (a + b)`), simplificar dividiendo todo entre lo mismo (como F.6 con una fracción), agrupar los trozos iguales.
- **F.1** (`3/4 de 20`): «de» entre una fracción y una cantidad es POR (5.NF.B.4: 3/4 de 20 = 3/4 x 20).

**Cómo lo haría un humano sin calculadora.** Mira las relaciones. Si una tiene una sola letra, la calcula. Si no: ¿hay
una letra dicha con las otras? la pone en su sitio (sustituir). ¿Dos relaciones que, juntándolas, se lleva una letra?
(a + b = 30 y a − b = 8: si las sumo, la b se va: 2 trozos de a = 38) — las junta. ¿Una relación que es el doble de
otra, o un trozo que ya sé (a + b)? la reescribe. Y si nada de eso sirve (n x n = 49; a x b = 24 y a + b = 10), prueba en
orden: 0, 1, 2… con un tope (no prueba cien veces), sabiendo cuándo parar (ya me paso y seguir solo me pasaría más).

**Lo que se construye** (todo en `sistema/partes/universal.py`, prefijo `_u_`, y reglas y costes en `universal.kn`):
1. **Los trozos con varias letras**: una relación lineal se lee como «tantos trozos de a, tantos de b… y lo suelto»
   (amplía `_u_lineal` de una letra a varias). Es la representación con la que se juntan y se reescriben relaciones.
2. **Operador 3, JUNTAR RELACIONES**: dos relaciones lineales en las que una letra tiene los MISMOS trozos (se restan)
   o trozos contrarios (se suman); también si los trozos de una son un número entero de veces los de la otra (se toma
   la otra esas veces: «dos veces a + b = 10»). Queda una relación con menos letras.
3. **Operador 4, REESCRIBIR CON EQUIVALENCIAS** (solo si deja menos letras o una relación más simple):
   a) **un bloque que ya se sabe**: si un trozo de una relación (`a + b`, o `a x b`) es entero el lado de otra relación
      que vale un número, se cambia por ese número (`(a + b) x c = 21; a + b = 7` → `7 x c = 21`);
   b) **sacar factor común / simplificar**: si todos los trozos y lo suelto se pueden repartir entre el mismo número,
      se reparte (`2 x a + 2 x b = 20` → `a + b = 10`), con la división de siempre;
   c) **agrupar los trozos iguales**: `a + a + b = 10` → `2 x a + b = 10` (se dice al leer los trozos).
4. **Operador 5, PROBAR EN ORDEN** (con tope humano, como S.3): cuando ninguno de los otros baja las letras. Se elige la
   letra que menos pruebas pide; va desde el 0 (números para contar) y se para cuando **ya se pasa**: en una relación
   `algo = N` hecha solo de + y x (con números que no son negativos), si con esa letra y las demás lo más pequeño que
   pueden ser (0; o 1 si es un producto solo, porque un 0 lo haría 0 y no N) ya se pasa de N, con más se pasaría más.
   En cada prueba se pone el número y se sigue con los otros operadores (sin volver a probar dentro); la prueba vale si
   todas las letras salen números para contar y se cumplen TODAS las relaciones de partida. Una, varias o ninguna. Si
   harían falta más pruebas que el tope (`universal.kn`), todavía no. Vale también cuando la letra sale multiplicada por
   sí misma (`n x n = 49`) y con dos relaciones no lineales (`a x b = 12; a x c = 8; b + c = 5`…).
5. **El control por medios y fines**: en cada vuelta se miran los candidatos de TODOS los operadores (calcular,
   sustituir, juntar, reescribir; probar solo si no hay otro), cada uno con lo que deja (letras de la relación nueva) y su
   coste; se elige el que deja menos letras y, si empatan, el más barato. La explicación dice qué se miró y por qué se
   eligió («juntar: deja 1 letra; sustituir: deja 1 letra pero cuesta más»). Presupuesto de pasos y de pruebas.
6. **La explicación paso a paso con barras**: cada paso lleva su dibujo cuando lo hay: los trozos de cada relación
   (`a: [a]`, `b: [b][b]`…) al juntar; las pruebas en orden, una por línea.
7. **`dos_incognitas` y `parte_todo`, traductores al modelo** (si sus respuestas no cambian): S.3 deja de tener su lector
   propio de ecuaciones: lee con el lector único (`_u_leer`) y reconoce sus formas (suma, diferencia, múltiplo, producto,
   suma con pesos) mirando las RELACIONES del modelo; sus piezas (la barra, probar en orden) siguen haciendo el trabajo y
   la explicación. S.2 traduce su orden (`todo: 24; partes: 7, ?, 5`) al modelo (`todo = 7 + ? + 5`) y el resolvedor
   universal hace de **segunda estrategia** que tiene que coincidir (como las otras estrategias de S.2).
8. **Los dos fallos de la revisión de U.1**, de forma general:
   - **La red de seguridad también con «todavía no»**: cuando una puerta vieja contesta «todavía no» (o «no entiendo») a
     algo que el lector simbólico lee entero y que tiene una RELACIÓN con letras (una ecuación), el resolvedor universal
     tiene su oportunidad; si llega a la respuesta (y la comprueba), contesta él; si no, se queda lo de la puerta. Las
     cuentas sin letras NO entran por aquí: su «todavía no» es «respetar el año» (`12 : 3 + 1`, `2/3 x 3/4`), no un
     problema de forma. En las dos cadenas (`explicar_pregunta` y `preguntar`).
   - **«de» es POR** en el lector simbólico entre una fracción o un decimal y lo que viene detrás (`3/4 de 20`,
     `0.5 de n = 3`), como en F.1. Entre dos enteros no («3 de 4» no es nada).

**Las trampas.**
- `resolver: a + b = 30; a - b = 8` → juntar (sumar: 2 trozos de a = 38 → 19), no sustituir: juntar es más barato.
- `resolver: 2 x a + 3 x b = 12; 2 x a + b = 8` → restar (los dos tienen 2 trozos de a): 2 trozos de b = 4.
- `resolver: a + b = 10; 2 x a + 2 x b + c = 26` → juntar (quitar 2 veces la primera): c = 6; a y b se prueban en orden
  (las 11 parejas con números para contar, con c = 6 en todas).
- `resolver: (x + y) x z = 21; x + y = 7` → el bloque: 7 x z = 21 → z = 3; x, y faltan relaciones.
- `resolver: n x n = 49` → probar en orden: 0, 1, …, 7 (SÍ), 8 (64: ya me paso) → n = 7 (con números para contar).
- `resolver: a x b = 24; a + b = 10` → probar en orden (a de 0 a 10) → a = 4, b = 6; a = 6, b = 4.
- `resolver: n x n = 50` → ninguna (con números para contar). `n x n = 2000000` → todavía no (demasiadas pruebas).
- `resolver: a + b = 10; a + b = 12` sigue «ninguna»; `a + b + c = 10` sigue «todavía no».
- `3/4 de 20` → 15; `resolver: 1/2 de n = 6` → 12; `3 de 4` → no entiendo.
- Lo viejo no cambia: `a + b = 30; a - b = 8` sin la orden sigue por S.3 (la barra); `perimetro: 30; lados: 8, 7, 6, ?`
  sigue igual (con una línea más: la otra estrategia, el modelo).

**Prueba de dominio** (`pruebas/test_U2_buscar_con_control.py`, pocas y representativas): cada operador una o dos veces
(contra un testigo, `fractions.Fraction`, SOLO en la prueba), la elección (juntar antes que sustituir; probar solo al
final), el tope de pruebas, los dos fallos de la revisión, S.3 y S.2 por el modelo con las mismas respuestas, el tiempo.

**Para Carlos:** `resolver: a + b = 30; a - b = 8`, `resolver: n x n = 49`, `resolver: a x b = 24; a + b = 10`,
`3/4 de 20`, `x + y + z = 12; x - y = 2; x x y = 15` (o el que salga en el resumen).

## RESULTADO (8 oct 2026)

**Hecho. `test_U2` 42/42; `test_U1` 63/63; mis_pruebas 243/243; proyecto 3201/3201 afirmaciones + 834/834 casos (824 + 10
nuevos), VERDE.** Falta la prueba de Carlos.

**Lo que se construyó.**
- Parte nueva `sistema/partes/buscar.py` (prefijo `_bu_`), después de `universal.py`:
  - **los trozos con varias letras** (`_bu_trozos`): `2 x a + 3 x b - a` → {a: 1, b: 3}; agrupa los trozos iguales;
  - **juntar** (operador 3): por cada par de relaciones lineales y cada letra que esté en las dos, si sus trozos son los
    mismos (se restan), contrarios (se suman) o K veces (se quita K veces); solo si la letra se va. Con barras;
  - **reescribir** (operador 4): el BLOQUE que ya se sabe (`(x + y) x z = 21; x + y = 7` → `7 x z = 21`) y sacar FACTOR
    COMÚN (prueba con el trozo más pequeño, 2, 3 y 5, con la división de siempre);
  - **probar en orden** (operador 5): solo si nada más baja las letras. El TOPE lo pone una relación «hecha de + y x = N»
    (de ahora o de partida): con la letra = v y las demás en lo más pequeño (0; 1 en un producto solo, que con un 0 daría 0),
    si ya se pasa de N, con más se pasaría más → PARO. Se elige la letra que MENOS pruebas pide. En cada prueba se pone el
    número y se siguen los otros operadores (sin volver a probar dentro); vale si todo sale un número para contar y se
    cumplen las relaciones de PARTIDA. Más de 30 pruebas (`universal.kn`) → todavía no;
  - **el control**: todos los candidatos con lo que dejan y lo que cuestan; se elige el que deja menos letras; si empatan,
    el que no pone una letra dividiendo o por otra (`a = 10 - b` antes que `a = 24 : b`) y luego el más barato. Cuando hubo
    que decidir, la explicación lo dice («MIRO lo que puedo hacer: sustituir -> deja 1 letra (coste 4); juntar -> deja 1
    letra (coste 3). ELIJO juntar»).
- `universal.py`: `_u_buscar` usa el control; las soluciones de probar en orden (una, varias o ninguna, «con números para
  contar, desde el 0»; si hay menos relaciones que letras, «con decimales habría infinitas»); «de» = POR tras una fracción o
  un decimal; la red de seguridad nueva (`_u_la_puerta_no_llega`, `_u_le_toca_al_resolvedor`) en las dos cadenas.
- **S.3 traductor al modelo**: `dos_incognitas.py` ya no tiene lector propio (`_di_tokens` fuera): lee con `_u_leer` y
  reconoce sus formas en las relaciones del modelo. Sus piezas, su barra y sus respuestas, iguales (101/101).
- **S.2 traductor al modelo**: la orden se dice como `todo = parte + parte + ...` (las partes iguales que faltan, la misma
  letra `p`) y el resolvedor universal es una OTRA ESTRATEGIA que tiene que dar LO MISMO (74/74, una línea más).
- `universal.kn`: los costes y el tope de pruebas.

**Lo que salió al probar (y se arregló).**
- `a x b = 24; a + b = 10` decía todavía no: el control aislaba `a = 24 : b` y luego no había tope. Dos arreglos generales:
  el tope puede ponerlo una relación de PARTIDA (también se cumple), y a igualdad se prefiere no poner una letra dividiendo.
- U.1 escribía mal lo aislado: `a = 20 - (2 x b) : 2` (el árbol estaba bien, faltaba el paréntesis al escribirlo):
  ahora `(20 - 2 x b) : 2`.
- `2 x a + 4 x b = 20` probaba la a (11 pruebas): ahora la letra que menos pruebas pide (b: 6).
- La auditoría sin calculadora cazó un `lista + lista`: con `.extend`.
- La prueba trucada de U.1 (sección F) trucaba el despeje solo en `universal.py`: ahora en todas las partes que lo ven.
- Probando en orden, «ninguna» solo es «ninguna con números para contar»: en la red de seguridad no basta (podría haberla con
  decimales): se queda lo de la puerta vieja (`a x b + a = 10; a - b = 1` sigue «todavía no»).

**Lo que cambia de respuesta** (todo por el arreglo 1 de la revisión, que Carlos pidió: antes «todavía no» de una puerta
vieja, ahora el resolvedor lo resuelve y lo comprueba): `n + n = 10` → n = 5 (E.5); `a + a = 10` → a = 5;
`a + b = 500; 2 x a + 5 x b = 1600` → a = 300, b = 200 (S.3: demasiadas pruebas); `a + b = 10; a = 2.5 x b` → 50/7 y 20/7
(S.3: peso con decimales); `a + b = 1.001; a - b = 0` → 1001/2000 (S.3: diezmilésimas); `a + b = 10; a - b = 2;
a = 2 x b` → ninguna (S.3: tres ecuaciones). Y con `resolver:` lo que U.1 dejaba para U.2: `n x n = 49` → 7;
`a + b = 10; 2 x a + 2 x b = 20` → las 11 parejas. Se actualizaron sus pruebas (`test_U1`, `test_S3`, `test_E5`, dos
casos de `mis_casos.txt`), cada una con su porqué.

**Los límites que quedan (honestos).**
- Probar en orden solo con números para contar (desde el 0), sin negativos; necesita una relación «de + y x = N» que ponga
  el tope (`n x n = n + 6`, `a - b = 3` → todavía no).
- Juntar y factor común solo con relaciones LINEALES; el bloque, solo si está escrito igual (`x + y`, no `y + x`).
- Dentro de una prueba no se vuelve a probar (dos letras libres → todavía no: `a + b + c = 10`).
- `a + b = 9; a : b = 2` sigue entrando por la puerta equivocada (0.2, por el `:`): juntar las puertas es U.4.
- Los operadores (los de U.1 y los de U.2) viven en partes del motor, no como PIEZAS en `conocimiento/piezas/` (el plan U
  decía «cada operador es una pieza más»): sus condiciones y costes están en `universal.kn`, pero todavía no salen en el
  mapa de piezas. Pasarlos a piezas (con su `vuelta`) es un paso aparte; la comprobación final en las relaciones de partida
  ya caza un operador que se equivoque.
