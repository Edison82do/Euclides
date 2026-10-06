# Paso N.2 — REDONDEAR A LA DECENA Y A LA CENTENA — 6 oct 2026

Carlos probó E.5 («ya probé, continúa») → se termina el plan ajustado y se empieza la continuación que
dicta la pedagogía: **la estimación** (la otra mitad de 3.OA.D.8: «¿es razonable la respuesta?»).
Una cosa cada vez: primero **redondear** (N.2), luego **estimar para comprobar** (E.6).

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (mirando antes `FUENTES.md`).**
- Common Core **3.NBT.A.1**: «usar el valor de posición para **redondear números enteros a la decena
  o a la centena más cercana**». Es requisito de **3.OA.D.8** («valorar si la respuesta es razonable
  con cálculo mental y estimación, **incluido el redondeo**»).
- La *Progression* de Números en base diez (3.º) y las guías de los estados (Utah *Core Guide* 3.º):
  redondear se **entiende en la recta numérica**: ¿entre qué dos decenas está 37? (30 y 40); ¿dónde está
  **la mitad del camino**? (35); ¿de cuál está **más cerca**? La regla «5 o más sube» llega **después**,
  como atajo de lo que se entendió, no en lugar de ello.
- Lo que está **justo en la mitad** (35, 250) no está más cerca de ninguna: se sube **por convenio**
  (y hay que decir que es un convenio, no algo que se deduce).
- El error documentado: **redondear en cadena** (247 → 250 → 300). A la centena, 247 está entre 200 y
  300, y 247 no llega a la mitad (250): **200**.

**Lo que se construye.**
- Pregunta nueva **«redondear»** (situación: el número y el sitio, decena o centena), con política
  **todas_iguales**: los dos caminos se hacen y tienen que dar lo mismo.
  - Pieza `redondear_en_la_recta` (la comprensión): escribe las dos decenas/centenas de los lados
    (poniendo ceros = valor de posición; la de arriba saltando de diez o de cien, N.1), escribe la
    mitad del camino (un 5 en el sitio de la derecha: 35, 250), y mira en la lista si el número viene
    antes o después de la mitad. Dice cuánto le falta a cada lado (lo que pasa de abajo se lee en las
    cifras; lo que falta hasta arriba se cuenta hacia arriba, como P.6).
  - Pieza `redondear_por_la_cifra` (el atajo): mira solo la cifra de la derecha del sitio: 5, 6, 7,
    8 o 9 → sube; 0 a 4 → se queda.
- Orden `redondear: 37` (las dos), `redondear: 37 a la decena`, `redondear: 247 a la centena`.
- Hasta mil (la lista que sabe). Más allá, o al millar: **todavía no**.

**Las trampas.**
- `37` → 40;  `32` → 30;  `35` → 40 (la mitad: convenio);  `40` → 40 (ya es redondo).
- `247` a la centena → **200** (no 300 por cadena);  `250` → 300 (mitad);  `249` → 200.
- `995` a la decena → 1000 (cambia la centena: se salta de diez);  `950` a la centena → 1000.
- `49` a la centena → 0;  `4` a la decena → 0;  `5` → 10;  `0` → 0;  `1000` → 1000.
- `1001`, o `redondear: 4567 al millar` → todavía no.

**Prueba de dominio.** Una muestra de 0 a 1000 (fronteras + azar fijo), a la decena y a la centena,
contra el testigo; los dos caminos siempre de acuerdo; la cadena y la mitad.

**Para Carlos:** `redondear: 37`, `redondear: 35`, `redondear: 247`, `redondear: 995 a la decena`,
`redondear: 49 a la centena`.

## 2. LO QUE SE HIZO
- Pregunta nueva **«redondear»** (política *todas_iguales*: los dos caminos se hacen y tienen que dar
  lo mismo) con dos piezas:
  - `redondear_en_la_recta` (la comprensión): escribe las dos decenas/centenas de los lados (ceros a la
    derecha; la de arriba saltando de diez o de cien), la mitad del camino (un 5 a la derecha del sitio),
    cuánto hay a cada lado (lo que pasa se lee en las cifras; lo que falta se cuenta hacia arriba) y mira
    en la lista si el número pasa de la mitad. En la mitad justa: **convenio**, se sube (y lo dice).
  - `redondear_por_la_cifra` (el atajo): la cifra de justo a la derecha del sitio, de 5 para arriba sube.
- Parte nueva `sistema/partes/redondear.py`: la orden `redondear: 37` (las dos), `... a la decena`,
  `... a la centena`, `... mas cercana`; al millar o pasado mil: todavía no. Si se piden las dos y la
  **cadena** engañaría (247 → 250 → 300), avisa: se redondea el número, no lo ya redondeado.
- `aplicar` guarda lo que dijo cada camino (`todos`) para poder enseñarlos.
- `pruebas/test_N2_redondear.py` (25 afirmaciones: trampas; 404 números a la decena y 295 a la centena
  contra el testigo con los dos caminos; 40 de la cadena; explicación y probador). Ayuda,
  `mis_pruebas.txt` (5), `mis_casos.txt` (9).

## 3. RESULTADO
- `redondear: 37 a la decena` → «37 esta entre 30 y 40. La mitad del camino es 35. De 30 a 37 hay 7; de
  37 a 40 hay 3. 37 pasa de la mitad: esta mas cerca de 40» y el atajo dice lo mismo.
- `redondear: 247` → decena 250, centena 200, con el OJO de la cadena.  `35` → 40 por convenio.
- Proyecto: **1892/1892 afirmaciones + 526/526 casos — VERDE**.

## 4. PENDIENTE: la prueba de Carlos.  Lo que sigue: E.6 ¿es razonable? estimar redondeando (3.OA.D.8).
