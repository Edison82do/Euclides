# Paso M.24 — CONTEXTOS MULTIPLICATIVOS: ÁREA Y PERÍMETRO 2 (paralelogramo, triángulo, área frente a perímetro, escala) — 10 oct 2026

Siguiente paso del orden de NCETM en 6.º: el segmento **2.30**, el ÚLTIMO de Spine 2. Se llama **M.24** porque sigue la
serie (M.23 era 2.29). Su primera parte es G.1 (NCETM 2.16, *area and perimeter 1*, 4.º).

**REGLA desde el plan U (Carlos, 9 oct):** lo nuevo entra por el MODELO COMÚN (como PIEZA, o en el resolvedor que ya existe,
eligiéndose por su costo); **no se abre ninguna puerta ni formato nuevo**; se respeta el año.

**Las DEUDAS DE PRUDENCIA (CLAUDE.md):** se miró la lista. Este paso NO toca sus temas (ecuaciones con productos,
multiplicar negativos, «cualquiera menos…», el pendiente menor de `2 x 3 - 4 x 5`): no se tacha nada. Sí sale una
respuesta falsa NUEVA, no apuntada, que es de ESTE tema (ver «la trampa que ya estaba»): se arregla aquí.

## 1. EL PLAN (escrito antes de programar)

**La fuente.** La web de NCETM sigue bloqueada desde la nube (`getaddrinfo ENOTFOUND www.ncetm.org.uk`, probado hoy con la
página del segmento). El título y los puntos salen del **buscador**: la página
`primm-230-multiplicative-contexts-area-and-perimeter-2` y el índice de Spine 2 (*Spine 2: Multiplication and Division –
Topic 2.30*, Year 6). **Falta leer el segmento entero** (diapositivas y guía) cuando Carlos pueda abrirlo.

- **Título exacto:** *2.30 Multiplicative contexts: area and perimeter 2* (Year 6).
- **Lo que trabaja** (la introducción): hallar el área de paralelogramos y triángulos identificando la **altura
  perpendicular**; comparar áreas y perímetros; aplicar factores de escala a los lados, al perímetro y al área.
- **Sus cuatro puntos** (teaching points; casi literales del buscador):
  1. **El paralelogramo**: el área se calcula multiplicando la base por la altura perpendicular; todos los paralelogramos
     con la misma base y la misma altura perpendicular tienen la misma área.
  2. **El triángulo**: el área se calcula multiplicando la base por la altura perpendicular y dividiendo entre dos.
  3. **Área y perímetro no van juntos**: figuras con la misma área pueden tener distinto perímetro, y figuras con el
     mismo perímetro, distinta área.
  4. **La escala**: si una figura se transforma con un factor de escala, su perímetro se transforma con el MISMO factor.
- **Common Core**: 6.G.A.1 (el área de triángulos y cuadriláteros especiales componiendo en rectángulos o descomponiendo
  en triángulos), 7.G.A.1 (dibujos a escala), 4.MD.A.3 (fórmulas del área y el perímetro del rectángulo, ya en G.1).
- **Lo que ya había** (no se repite): G.1 (NCETM 2.16) — el rectángulo y el cuadrado, el área contando cuadraditos y
  multiplicando, el perímetro sumando; `comparar: rectangulo 6 x 4 y rectangulo 8 x 3` ya dice «la misma área, distinto
  perímetro» (**el punto 3 ya está**); M.21 (NCETM 2.27) — el factor de escala en la tabla de razón (**el punto 4 sale
  por ahí**: lado y perímetro son una fila, `4 : 14 = 12 : p`); U.3 — las figuras son DATOS en `relaciones.kn` (lo que
  se sabe sin que el texto lo diga) y el lector de palabras las mete en el modelo.

**Cómo lo haría un humano de 6.º sin calculadora.**
- **Paralelogramo** de base 7 cm y altura 3 cm: se corta el triángulo de un lado y se pone al otro: es un **rectángulo**
  de 7 x 3 → **21 cm²**. El lado inclinado (5 cm) NO es la altura: solo sirve para el perímetro (2 x 7 + 2 x 5 = 24 cm).
- **Triángulo** de base 6 cm y altura 4 cm: dos triángulos iguales hacen un paralelogramo de 6 x 4 = 24, así que el
  triángulo es la **mitad**: 24 : 2 = **12 cm²**. Un humano que ve un factor PAR parte primero ese por la mitad
  (6 x 4 : 2 = 3 x 4 = 12): el mismo número con cuentas más pequeñas (la asociativa de M.14, NCETM 2.20). Si los dos
  son impares (7 x 3 : 2), multiplica y parte: 21 : 2 = 10 y medio.
- **Al revés**: un triángulo de 20 cm² y base 5 cm: el paralelogramo doble tiene 40 cm², así que la altura es 40 : 5 =
  **8 cm** (deshacer: x 2, luego : 5).
- **Se comprueba** con la operación contraria: el doble de la mitad tiene que volver al producto.

**Qué responde hoy** (medido el 10 oct, memoria vacía; lista «antes» de 1129 preguntas: `mis_pruebas`, `mis_casos`, los
problemas `R(...)` de todas las pruebas y 30 de este tema):
- `resolver: Un triangulo tiene 6 cm de base y 4 cm de altura. ¿Cuál es su area?` → «todavía no: faltan relaciones» (no
  sabe la fórmula del triángulo). Igual el paralelogramo y el problema inverso (la altura).
- `resolver: 6 x 4 : 2` → 12 (calcula 24 y luego 24 : 2, sin mirar si conviene partir antes).
- **La trampa que ya estaba (respuesta FALSA):** `resolver: Un triangulo rectangulo tiene 6 cm de base y 4 cm de altura.
  ¿Cuál es su area?` → **«24 cm cuadrados»** (lo verdadero es 12). La palabra «rectangulo» hace entrar la figura del
  RECTÁNGULO (con `base=largo`, `altura=ancho`) y calcula largo x ancho.

**Lo que se construye (sin puerta ni formato nuevo; por qué).**
1. **Las fórmulas (puntos 1 y 2): conocimiento del mundo en DATOS**, como las del rectángulo (REGLA FIJADA 2 de
   `relaciones.kn`). Dos figuras nuevas en `conocimiento/relaciones.kn`:
   - `paralelogramo` (palabras: paralelogramo, romboide…; medidas: base, altura, lado, perímetro, área):
     `area = base x altura; perimetro = 2 x base + 2 x lado` (el lado inclinado solo entra en el perímetro).
   - `triangulo` (palabras: triángulo, triangular, triángulo rectángulo, isósceles, escaleno; medidas: base, altura,
     área): `area = base x altura : 2`.
   No es vocabulario de la parte hablada (Carlos decidió no ampliarla): son las palabras de la figura, en DATOS, como en
   G.1; el resolvedor ya sabe calcular y deshacer la fórmula.
2. **La palabra más larga manda** (en `palabras.py`, donde se buscan las figuras): una palabra de figura que solo sale
   DENTRO de otra palabra de figura más larga que también sale («rectangulo» dentro de «triangulo rectangulo»,
   «triangulo» dentro de «triangulo equilatero») no hace entrar su figura. Arregla la trampa: el triángulo rectángulo es
   un triángulo. Es una regla de lectura general (la de los nombres compuestos), no un caso.
3. **La mitad de un producto (punto 2, la técnica humana): una PIEZA nueva, elegida por su costo.** Pregunta de piezas
   nueva `mitad_de_un_producto` (`a x b : 2`), con dos piezas:
   - **`partir_por_la_mitad_un_factor_par`** (rapidez 4): si uno de los factores es par (se mira con `paridad`, la última
     cifra), se parte ESE por la mitad y se multiplica: 6 x 4 : 2 = 3 x 4. **Vuelta**: el doble de lo que sale tiene que
     ser a x b calculado por el otro camino (multiplicando los factores enteros).
   - **`multiplicar_y_partir_por_la_mitad`** (rapidez 6): multiplicar y partir el producto (con lo que sobre: «y medio»).
     **Vuelta**: la mitad más la mitad (más lo que sobró) vuelve al producto.
   El resolvedor la pide en el NÚMERO común (`_u_valor`, como `_u_media` y `_u_divisor_comun`) al ver `a x b : 2` con
   enteros. Si no sale, lo de siempre. **El valor no cambia** (es el mismo número): solo el camino.
4. **El punto 3** (área y perímetro no van juntos) ya está en G.1 (`comparar:`) y con símbolos (`verdad:`): se prueba,
   no se construye. **El punto 4** (la escala del perímetro) sale por la tabla de razón de M.21 (`lado : perímetro =
   lado : ?`): se prueba, no se construye. (El área NO crece con el mismo factor —crece k x k—: el error típico; se prueba
   con `verdad:` que es falso.)

**Las trampas** (los errores típicos):
- **Usar el lado inclinado como altura** (paralelogramo de base 8, lado 5, altura 4: 40 en vez de 32). La fórmula usa la
  altura; el lado solo el perímetro.
- **Olvidar dividir entre dos** en el triángulo (24 en vez de 12): pieza trucada que no parte → la vuelta lo caza.
- **Partir los DOS factores** (6 x 4 : 2 = 3 x 2 = 6): pieza trucada → la vuelta lo caza.
- **El triángulo rectángulo leído como rectángulo**: la trampa que ya estaba (24, FALSO).
- **Pedir el perímetro de un triángulo sin sus lados** (base y altura): no hay fórmula → «faltan relaciones», nunca un número.
- **El área no escala por k**: `verdad: 3 x 4 x 3 = (3 x 3) x (4 x 3)` → falso.
- Cerca del techo: `9999 x 999 : 2` (los dos impares: multiplicar y partir; sale como antes, 9989001/2).

**Lo que cambia a propósito**: los problemas de área del paralelogramo y del triángulo (de «faltan relaciones» a su
respuesta), la altura del triángulo al revés, y la falsa del triángulo rectángulo (24 → 12). En `a x b : 2` cambia el
CAMINO que se enseña, no el número. Todo lo demás, igual (se mide antes y después con la lista).

**Prueba de dominio** (`pruebas/test_M24_area_perimetro_2.py`, pocas y representativas): las dos piezas contra el testigo
(Python, SOLO en la prueba) en una muestra al azar fijo, con su vuelta; qué elige el control; las piezas trucadas
(olvidar la mitad, partir los dos factores); los problemas del paralelogramo y del triángulo (área, al revés, el lado
inclinado que sobra, unidades cuadradas); la trampa del triángulo rectángulo; el perímetro del triángulo sin lados; los
puntos 3 y 4 por lo que ya había; cerca del techo; lo que no cambia; el tiempo (cada una por debajo de 2 s).

**Para Carlos:** `resolver: Un triangulo tiene 6 cm de base y 4 cm de altura. ¿Cuál es su area?`,
`resolver: Un paralelogramo tiene 8 cm de base, 5 cm de lado y 4 cm de altura. ¿Cuál es su area?`,
`resolver: Un triangulo tiene 20 cm2 de area y 5 cm de base. ¿Cuánto mide su altura?`, `resolver: 7 x 3 : 2`,
`resolver: Un triangulo rectangulo tiene 6 cm de base y 4 cm de altura. ¿Cuál es su area?`.

## RESULTADO (10 oct 2026)

**Hecho. `test_M24` 54/54; proyecto en cuartos 3789/3789 afirmaciones + 934/934 casos (99 archivos, VERDE; esta vez
también la prueba de tiempo de F7); mis_pruebas 302/302 con las 5 nuevas (con la memoria de las tablas, como en el PC de
Carlos); `test_sin_calculadora` 2/2; `comparar_puertas` 0 diferencias sin explicar.** Falta la prueba de Carlos.

**Lo que se construyó** (ninguna puerta ni formato nuevo):
- **Las fórmulas (puntos 1 y 2), DATOS** en `relaciones.kn`: `paralelogramo` (paralelogramo, romboide; base, altura, lado,
  perímetro, área: `area = base x altura; perimetro = 2 x base + 2 x lado`) y `triangulo` (triángulo, triangular, triángulo
  rectángulo / isósceles / escaleno; base, altura, área: `area = base x altura : 2`). Un campo nuevo `por_que` que la
  explicación enseña junto a la primera fórmula («se corta un triángulo de un lado y se pone al otro: un rectángulo de base x
  altura; la altura es la perpendicular»; «dos triángulos iguales hacen un paralelogramo: el triángulo es la mitad»). El
  resolvedor ya sabía calcular y deshacer: la altura del triángulo sale deshaciendo (20 x 2 = 40; 40 : 5 = 8).
- **La mitad de un producto, PIEZAS** de la pregunta nueva `mitad_de_un_producto` (`_objetivos.py`; condiciones
  `es_un_producto_de_dos_enteros_entre_dos` y `uno_de_los_factores_es_par`, que mira la última cifra):
  `partir_por_la_mitad_un_factor_par` (4; vuelta: el doble de lo que sale es a x b multiplicado entero, por el otro camino) y
  `multiplicar_y_partir_por_la_mitad` (6; con lo que sobra, «y medio»; vuelta: la mitad dos veces más lo que sobró vuelve al
  producto). Las pide el número común (`_u_mitad_de_un_producto` en `_u_valor`, `universal.py`) al ver `a x b : 2` con
  enteros: **cambia el camino, no el número**.
- **La palabra más larga manda** (`_pa_palabra_de_figura` en `palabras.py`; REGLA FIJADA 6 de `relaciones.kn`).

**Lo que cambió a propósito** (medido antes y después con 1129 preguntas: `mis_pruebas`, `mis_casos`, los `R(...)` de todas
las pruebas y 30 del tema): **cambian 3, todas a propósito**: el área del triángulo y del paralelogramo (de «faltan
relaciones» a 12 y 21 cm²) y la FALSA del triángulo rectángulo (24 → 12). En las pruebas viejas no cambió nada.

**Las deudas de prudencia:** este paso no toca sus temas; no se tacha nada. La falsa nueva (triángulo rectángulo) era de este
tema y queda arreglada.

**Lo que queda (honesto) y preguntas para Carlos:**
- `7 x 3 : 2` y el triángulo de 7 x 3 dan **21/2** (cm²): ¿en 6.º sería 10.5? Es la misma pregunta abierta de `7 : 2` (M.22).
- `resolver: 4000 x 5000 : 2` → todavía no (como antes): la mitad cabe (10 000 000), pero la vuelta multiplica entero y se pasa.
- Dos figuras en un mismo problema («un rectángulo… otro rectángulo…») no se leen (no entiendo): el punto 3 se pregunta con
  `comparar:` (G.1) o con `verdad:`; el 4, con la tabla de razón (`resolver: 4 : 14 = 12 : p`). Ampliarlo sería parte hablada.
- El perímetro del triángulo con sus tres lados por palabras: no (con `perimetro: 3, 4, 5` sí, G.1).
- La web de NCETM sigue bloqueada desde la nube: falta leer el segmento 2.30 entero (diapositivas).
