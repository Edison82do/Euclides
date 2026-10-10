# Paso F.8 — MULTIPLICAR FRACCIONES Y DIVIDIR UNA FRACCIÓN ENTRE UN ENTERO — 10 oct 2026

Spine 2 terminó con 2.30 (M.24). Se vuelve a **Spine 3 (fracciones)**. Se llama **F.8** porque sigue la serie de las
fracciones (F.7 era NCETM 3.8).

**Qué segmentos de Spine 3 ya están** (PROGRESO.md, PLAN.md y los diarios F.1–F.7):

| NCETM | Título | Año | Paso |
|---|---|---|---|
| 3.1, 3.2 | la parte y el todo; fracciones unitarias | 3.º | F.1 |
| 3.3 | fracciones no unitarias | 3.º | F.2 |
| 3.4 | sumar y restar dentro de un entero | 3.º | F.3 |
| 3.5 | *Working across one whole: improper fractions and mixed numbers* | 4.º | F.4 |
| 3.6 | *Multiplying whole numbers and fractions* | 4.º–5.º | F.5 |
| 3.7 | *Finding equivalent fractions and simplifying fractions* | 5.º | F.6 |
| 3.8 | *Common denomination: more adding and subtracting* | 5.º–6.º | F.7 |
| **3.9** | ***Multiplying fractions and dividing fractions by a whole number*** | **6.º** | **F.8 (este)** |

El primero de 6.º que falta es el **3.9** (F.5 ya lo decía: «2/3 x 3/4 → todavía no, fracción por fracción es de 6.º,
NCETM 3.9»; M.18 también lo apuntaba).

**REGLA desde el plan U (Carlos, 9 oct):** lo nuevo entra por el MODELO COMÚN (como PIEZA, o en el resolvedor que ya
existe, eligiéndose por su costo); **no se abre ninguna puerta ni formato nuevo**; con números y símbolos; se respeta el año.

**Las DEUDAS DE PRUDENCIA (CLAUDE.md):** se miró la lista. Este paso no toca sus temas (ecuaciones con productos,
multiplicar negativos, «cualquiera menos…», el pendiente menor de `2 x 3 - 4 x 5`). Se espera no tachar nada; se mira al
final por si acaso.

## 1. EL PLAN (escrito antes de programar)

**La fuente.** La web de NCETM sigue bloqueada desde la nube (`getaddrinfo ENOTFOUND ncetm.org.uk`, probado hoy con la
página del segmento). El título y los puntos salen del **buscador** (la página
`primm-309-multiplying-fractions-and-dividing-fractions-by-a-whole-number`, Spine 3, Topic 3.9, Year 6).
**Falta leer el segmento entero** (diapositivas y guía) cuando Carlos pueda abrirlo.

- **Título exacto:** *3.9 Multiplying fractions and dividing fractions by a whole number* (Year 6).
- **Sus tres puntos** (teaching points; literales del buscador):
  1. *When a fraction is multiplied by a proper fraction, it makes it smaller. To multiply two fractions, multiply the
     numerators and multiply the denominators.*
  2. *When a fraction is divided by a whole number, it makes it smaller. To divide a fraction by a whole number, convert
     it to an equivalent multiplication.*
  3. *A more efficient method can be used to divide a fraction by a whole number when the whole number is a factor of the
     numerator.*
- **El error típico** (NCETM, *Subject Knowledge Audit*, fracciones): multiplicar (o dividir) el de arriba Y el de abajo
  por el entero, cuando solo toca uno de los dos.
- **Common Core**: 5.NF.B.4 (fracción por fracción: «a/b x c/d = ac/bd», el área de un rectángulo de lados
  fraccionarios), 5.NF.B.5 (multiplicar es ESCALAR: por menos de un entero, más pequeño), 5.NF.B.7a (una fracción
  unitaria entre un entero: 1/3 : 4 = 1/12). La currícula inglesa de Year 6: *multiply simple pairs of proper fractions,
  writing the answer in its simplest form*; *divide proper fractions by whole numbers*.

**Lo que ya había** (medido hoy, memoria vacía):
- El NÚMERO COMÚN del resolvedor (U.1, `numero.py`) ya hace las dos cuentas, **por dentro, sin pieza y sin vuelta**:
  `resolver: 2/3 x 3/4` → 1/2 («arriba por arriba y abajo por abajo»), `resolver: 2/3 : 4` → 1/6 («no se reparte justo:
  cada trozo se parte en 4»), `resolver: 6/7 : 3` → 2/7 («reparto los de arriba»). También `1/2 de 1/3` → 1/6.
- Pero la puerta vieja F.5 coge `2/3 x 3/4` (sin `resolver:`) y dice **«todavía no: fracción por fracción es de 6.º
  (NCETM 3.9)»**: ya estamos en 6.º. Y es incoherente: `2/3 de 3/4` → 1/2, `2/3 x 3/4` → todavía no.
- `2 1/2 x 1/3` (un mixto por una fracción) → todavía no; el resolvedor no lee mixtos.

**Cómo lo haría un humano de 6.º sin calculadora.**
- **2/3 x 3/4** = «2/3 DE 3/4»: arriba por arriba (2 x 3 = 6), abajo por abajo (3 x 4 = 12): 6/12 = 1/2. Con la
  tira (el área): 3/4 de la tira, y de eso tomar 2/3. **Mira si tiene sentido**: 3/4 es menos que un entero, así que el
  resultado tiene que ser MÁS PEQUEÑO que 2/3 (1/2 < 2/3: sí).
- **2/3 : 4** = «la cuarta parte de 2/3» = **2/3 x 1/4** (la división convertida en una multiplicación equivalente):
  2/12 = 1/6. Más pequeño que 2/3: sí.
- **6/7 : 3**: el 3 cabe justo en el 6 de arriba: se reparten los de arriba, 6 séptimos : 3 = **2 séptimos** (como
  6 manzanas : 3 = 2 manzanas). Es el camino corto (punto 3); el largo (6/7 x 1/3 = 6/21 = 2/7) da lo mismo con más cuentas.
- **Se comprueba** con la operación contraria: 1/6 x 4 = 4/6 = 2/3 (vuelve); 6/12 → 6 : 3 = 2 y 12 : 4 = 3 (deshacer
  cada multiplicación vuelve a 2/3).

**Lo que se construye (sin puerta ni formato nuevo).**
1. **Pregunta de piezas nueva `fraccion_por_fraccion`** (`{"a": (arriba, abajo), "b": (arriba, abajo)}`), una PIEZA:
   - **`fraccion_por_fraccion_arriba_por_arriba`** (rapidez 6): arriba x arriba, abajo x abajo (con la pieza
     `multiplicar`). **Vuelta**: deshacer cada multiplicación DIVIDIENDO (producto de arriba : el arriba de la segunda =
     el arriba de la primera; lo mismo abajo, sin resto) **y**, si la segunda es menor que un entero (se mira con
     `viene_despues`), que el resultado sea más pequeño que la primera (se comparan al mismo de abajo: punto 1).
2. **Pregunta de piezas nueva `fraccion_entre_entero`** (`{"a": arriba, "b": abajo, "n": entero}`), dos PIEZAS elegidas
   por el COSTO:
   - **`fraccion_entre_entero_repartiendo_los_de_arriba`** (rapidez 3; punto 3): solo si el entero cabe justo en el de
     arriba (se mira dividiendo). a : n arriba, el de abajo igual. **Vuelta**: (a : n) x n = a (multiplicando).
   - **`fraccion_entre_entero_por_la_inversa`** (rapidez 6; punto 2): a/b : n = a/b x 1/n = a/(b x n). Sirve siempre.
     **Vuelta**: el resultado por n (arriba x n) da (a x n)/(b x n), y dividiendo los dos entre n vuelve a a/b.
   Las dos son la misma fracción (la segunda sin simplificar): **el valor final no cambia** (lo simplifica después
   `simplificar_fraccion`, como siempre).
3. **El número común las pide** (`numero.py`, en `_nu_multiplicar` y `_nu_dividir`): cuando las dos son fracciones (no
   decimales: «0.5 x 0.3» sigue contando partes, M.13), y cuando una fracción se divide entre un entero. El signo, aparte
   (como siempre). Si la pieza no sale, lo de antes. **Cambia el camino que se enseña, no el número.**
4. **La puerta vieja F.5** (`fraccion`): «fracción por fracción» ya es del año → con `no_sabe` (como M.22) se lo pasa al
   resolvedor, sin puerta nueva. El mixto por una fracción (`2 1/2 x 1/3`) sigue «todavía no» (el 3.9 es con fracciones
   propias; el resolvedor no lee mixtos): solo se cambia el porqué.

**Las trampas** (los errores típicos):
- **Multiplicar arriba Y abajo por el entero al dividir** (2/3 : 4 → 8/12, que es 2/3 otra vez): pieza trucada → la
  vuelta lo caza (8/12 x 4 no vuelve a 2/3).
- **Dividir arriba y abajo** (6/9 : 3 → 2/3, el mismo número): pieza trucada → la vuelta lo caza.
- **Sumar los de abajo** al multiplicar o multiplicar solo los de arriba (2/3 x 3/4 = 6/3): pieza trucada → la vuelta.
- **Repartir los de arriba cuando no caben** (2/3 : 4): esa pieza se descarta; sale la de la inversa.
- **«Multiplicar siempre hace más grande»**: con 5/4 (más de un entero) el resultado es MAYOR; la vuelta del punto 1 solo
  exige «más pequeño» si la segunda es menor que un entero.
- **Cero y uno**: `0 x 2/3`, `2/3 x 1`, `2/3 : 1` (como antes).
- Cerca del techo: `999/1000 x 999/1000` (998001/1000000), `5/6 : 1000`, y una que se pasa (`9999/10000 x 9999/10000`:
  el de abajo pasa de diez millones → no sale, nunca un número falso).

**Prueba de dominio** (`pruebas/test_F8_multiplicar_dividir_fracciones.py`, pocas y representativas): las piezas contra
el testigo (Python, SOLO en la prueba) en una muestra al azar fijo, con su vuelta; qué elige el control por el costo; las
piezas trucadas; el resolvedor con y sin `resolver:` (la puerta F.5 ya no dice «todavía no»); el punto 1 en la
explicación; los signos; cerca del techo; lo que no cambia; el tiempo (cada una por debajo de 2 s).

**Lo que cambia a propósito**: `2/3 x 3/4` (y las demás fracción por fracción sin `resolver:`) pasa de «todavía no» a su
respuesta. Todo lo demás, igual (se mide antes y después con la lista: `mis_pruebas`, `mis_casos`, los `R(...)`/`S(...)`
de todas las pruebas y 37 de este tema, 1360 preguntas).

**Para Carlos:** `2/3 x 3/4`, `2/3 : 4`, `6/7 : 3`, `5/4 x 2/3`, `resolver: r : 4 = 2/3`.

## RESULTADO (10 oct 2026)

**Hecho. `test_F8` 58/58; proyecto en cuartos 3847/3847 afirmaciones + 939/939 casos (100 archivos, VERDE); mis_pruebas
307/307 con las 5 nuevas (con la memoria de las tablas, como en el PC de Carlos); `test_sin_calculadora` 2/2;
`comparar_puertas` 0 diferencias sin explicar.** Falta la prueba de Carlos.

**Lo que se construyó** (ninguna puerta ni formato nuevo):
- **Fracción por fracción (punto 1), PIEZA** de la pregunta nueva `fraccion_por_fraccion`:
  `fraccion_por_fraccion_arriba_por_arriba` (6). Vuelta: deshacer cada multiplicación dividiendo (sin resto) y, si la
  segunda es menor que un entero, que el resultado sea más pequeño que la primera (al mismo de abajo, con `viene_despues`).
- **Una fracción entre un entero (puntos 2 y 3), dos PIEZAS** de `fraccion_entre_entero`, por el costo:
  `fraccion_entre_entero_repartiendo_los_de_arriba` (3; solo si el entero cabe justo arriba, se mira dividiendo; vuelta:
  por el entero vuelve) y `fraccion_entre_entero_por_la_inversa` (6; 2/3 : 4 = 2/3 x 1/4; vuelta: por el entero y dividir
  arriba y abajo entre él vuelve a la de partida).
- Las pide el número común (`_nu_con_pieza` en `_nu_multiplicar` y `_nu_dividir`, `numero.py`). **Cambia el camino, no el
  número.** Los decimales siguen con lo suyo (M.13, M.23).
- La puerta vieja F.5 lleva `no_sabe=_fr_es_fraccion_por_fraccion` (como M.22): fracción por fracción, al resolvedor.

**Lo que cambió a propósito** (1360 preguntas antes y después): **cambian 4, todas a propósito**: `2/3 x 3/4`, `1/2 x 1/3`,
`3/4 x 2/5`, `2/5 x 3/4` (de «todavía no» a su respuesta). En las pruebas viejas, solo `test_F5` A6 (el caso viejo, escrito al
lado).

**Las deudas de prudencia:** este paso no toca sus temas; no se tacha nada.

**Lo que queda (honesto) y preguntas para Carlos:**
- ¿Simplificar ANTES de multiplicar (2/3 x 3/4: el 3 de arriba y el de abajo se van)? No está en los puntos de 3.9; sería una
  tercera pieza más barata.
- Un mixto por una fracción (`2 1/2 x 1/3`): todavía no (3.9 es con fracciones propias; el resolvedor no lee mixtos).
- Dividir entre una fracción (`1/2 : 1/4` → 2) ya salía antes (es de KS3): no se tocó.
- `resolver: -2/3 x -3/4` → no entiendo (el lector, ya antes); con paréntesis, `-2/3 x (-3/4)` → 1/2.
- Con la memoria vacía (sin las tablas) a veces no simplifica del todo (`6/81 x 5/49` → 30/3969, el mismo número); con las
  tablas, 10/1323.
- La web de NCETM sigue bloqueada desde la nube: falta leer el segmento 3.9 entero (diapositivas).
