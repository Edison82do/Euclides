# Paso F.1 — LA PARTE Y EL TODO; LAS FRACCIONES UNITARIAS — 6 oct 2026 (noche)

Carlos (6 oct, noche): «puedes ir trabajando en orden pedagógico uno por uno … no te detengas, avanza
algunos años escolares … como lo haría un humano sin calculadora … con un plan y paso por paso».
Las pruebas de Carlos quedan para mañana. Antes de los números de más de mil (4.º) falta lo que queda
de **3.º**: las fracciones (NCETM 3.1–3.4; Common Core 3.NF). Se empieza por aquí.

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (NCETM Spine 3, leído el 6 oct; Common Core 3.NF.A.1).**
- NCETM **3.1** (*Preparing for fractions: the part–whole relationship*): «cualquier elemento de un
  todo es una parte»; «un todo se puede dividir en partes **iguales o desiguales**»; «el tamaño de las
  partes se puede comparar»; «si se conocen una de las partes iguales y cuántas partes iguales hay, se
  puede **construir el todo**».
- NCETM **3.2** (*Unit fractions*): «un todo se puede dividir en cualquier número de partes iguales»;
  «una parte igual de un todo es una **fracción unitaria**; cada una tiene un nombre»; «se aplica en
  contextos distintos» (una parte de una cantidad); «las fracciones unitarias se comparan mirando el
  denominador: **cuanto mayor el denominador, menor la fracción**»; «si se conoce el tamaño de una
  fracción unitaria, el todo se saca **sumando repetidamente** esa fracción».
- Common Core **3.NF.A.1**: 1/b es la cantidad que forma una parte cuando un todo se parte en b partes
  iguales. (El currículo inglés de 3.º: hallar una fracción unitaria de un conjunto = **repartir**.)
- Lo que Euclides no puede (no ve): «las partes iguales no tienen por qué parecerse» (NCETM 3.2, punto 4)
  es sobre dibujos. Se queda apuntado.

**Lo que se construye** (parte nueva `sistema/partes/fracciones.py`).
1. `fraccion: 1/4` → «UN CUARTO»: el entero en 4 partes iguales, una de ellas; el de abajo dice en
   cuántas partes, el de arriba cuántas se toman; la tira; y «cuatro cuartos hacen un entero».
   Los nombres: medio, tercio, cuarto … décimo, onceavo, doceavo. (Las no unitarias, 3/4: F.2.)
2. `1/4 de 12` → **repartir** 12 en 4 partes iguales (la pregunta `dividir`, M.3): 3. Con su tira.
   Si no sale justo (1/4 de 13), lo dice: no se reparte en partes iguales sin partir las cosas.
3. `comparar: 1/3 y 1/5` → pregunta nueva **«comparar_fracciones»** (todas_iguales, dos caminos):
   - `fracciones_por_el_denominador` (la regla de NCETM 3.2): más partes → partes más pequeñas.
   - `fracciones_en_una_tira` (lo concreto): una tira de 3 x 5 = 15 cuadritos; 1/3 son 5, 1/5 son 3.
4. `entero: 1/4 es 3` → el todo desde una parte (NCETM 3.1 y 3.2): 3 + 3 + 3 + 3 = 4 x 3 = 12.
5. `partes: 12 = 4 + 4 + 4` → ¿hacen el entero? ¿son iguales? → «tres partes iguales: cada una es
   1/3 de 12». `partes: 12 = 5 + 4 + 3` → desiguales: no son tercios.

**Las trampas.**
- `comparar: 1/3 y 1/5` → 1/3 es MAYOR (el error típico: «5 es más que 3, así que 1/5 es más»).
- `comparar: 1/4 y 1/4` → iguales.   `1/2 de 10` → 5.   `1/4 de 13` → no sale justo.
- `fraccion: 1/0` → no se puede partir en cero partes.   `fraccion: 1/1` → un entero.
- `partes: 12 = 4 + 4 + 3` → no hacen el entero (11).   `partes: 12 = 6 + 6` → medios.
- `entero: 1/5 es 7` → 35.   `fraccion: 3/4` → todavía no (F.2).

**Prueba de dominio.** Comparar todas las parejas de fracciones unitarias de 1/2 a 1/12 contra el
testigo (y los dos caminos de acuerdo); 1/b de n en una muestra (justas y no justas); el entero desde
una parte; partes iguales y desiguales.

**Para Carlos:** `fraccion: 1/4`, `1/4 de 12`, `comparar: 1/3 y 1/5`, `entero: 1/4 es 3`,
`partes: 12 = 4 + 4 + 4`.

## 2. LO QUE SE HIZO
- Parte nueva `sistema/partes/fracciones.py` con cinco órdenes: `fraccion: 1/4` (nombre, qué dice el
  de arriba y el de abajo, la tira, «cuatro cuartos hacen un entero»); `1/4 de 12` (REPARTIR con la
  pregunta `dividir`, con su tira; si no sale justo, lo dice); `comparar: 1/3 y 1/5`; `entero: 1/4 es 3`
  (sumando la parte una y otra vez, comprobado multiplicando); `partes: 12 = 4 + 4 + 4` (¿hacen el
  entero?, ¿son iguales?, ¿qué fracción es cada una?).
- Pregunta nueva **«comparar_fracciones»** (todas_iguales) con dos piezas: `fracciones_por_el_denominador`
  (la regla de NCETM 3.2) y `fracciones_en_una_tira` (lo concreto: una tira de a x b cuadritos repartida
  de las dos maneras).
- Las partes iguales «que no se parecen» (NCETM 3.2, punto 4) son de dibujos: Euclides no ve. Apuntado.
- `pruebas/test_F1_fracciones_unitarias.py` (23 afirmaciones: trampas; las 121 parejas 1/2..1/12 contra
  el testigo con los dos caminos; 201 casos de 1/b de n; el entero desde una parte; partes iguales).
  Ayuda, `mis_pruebas.txt` (5), `mis_casos.txt` (8).

## 3. RESULTADO
- `comparar: 1/3 y 1/5` → 1/3 > 1/5 («en 5 partes las partes son más pequeñas»; «una tira de 15
  cuadritos: 1/3 son 5 y 1/5 son 3»).  `1/4 de 12` → 3 con `[###|ooo|ooo|ooo]`.  `entero: 1/4 es 3` → 12.
- Proyecto: **1938/1938 afirmaciones + 542/542 casos — VERDE**.

## 4. PENDIENTE: la prueba de Carlos (mañana).  Sigue F.2: fracciones no unitarias (NCETM 3.3).
