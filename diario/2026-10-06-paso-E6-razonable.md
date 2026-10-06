# Paso E.6 — ¿ES RAZONABLE? ESTIMAR REDONDEANDO — 6 oct 2026

Carlos probó N.2 («ya probé, continúa») → paso 16, el último de «la continuación».

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (mirando antes `FUENTES.md`).**
- Common Core **3.OA.D.8** (segunda mitad): «**valorar si la respuesta es razonable** usando cálculo
  mental y **estrategias de estimación, incluido el redondeo**». Requisito: 3.NBT.A.1 (N.2, hecho).
- La *Progression* de Operaciones (3.º) y las guías de los estados: estimar es redondear cada número y
  hacer la cuenta fácil (38 + 47 ≈ 40 + 50 = 90); sirve para **cazar errores grandes**: olvidarse de
  la llevada (38 + 47 = 75), poner mal las cifras de sitio (= 815).
- Lo que hay que decir con honradez: **razonable no quiere decir correcta**. Una estimación caza los
  errores grandes, no los pequeños (38 + 47 = 95 está cerca de 90 y está mal). Por eso, después de la
  estimación, Euclides hace también la cuenta de verdad y lo dice.
- ¿Cuánto es «cerca»? No a ojo: cada número, al redondear a la decena, se mueve **como mucho 5** (a la
  centena, como mucho 50). En una suma o una resta, la cuenta de verdad no puede alejarse de la
  estimación más que lo que se movieron los dos juntos (5 + 5 = 10). Fuera de esa banda, **seguro que
  está mal**. En a × b con un factor de una cifra (3 × 47 ≈ 3 × 50), solo se redondea el grande y la
  banda es a veces 5 (3 × 5 = 15).

**Lo que se construye.**
- Una parte nueva `sistema/partes/estimar.py`:
  - `estimar: 38 + 47` → redondea cada número (hasta 99 a la decena; de 100 en adelante a la centena),
    con la pregunta `redondear` (N.2), hace la cuenta fácil con las piezas, y dice la banda.
  - `razonable: 38 + 47 = 75` → estima, mira si 75 cae dentro de la banda (con la lista: viene antes o
    después), dice SI o NO; y luego la cuenta de verdad («razonable no es lo mismo que correcta»).
- Sumas, restas y a × b con un factor de una cifra. Dividir, o dos factores de dos cifras: todavía no.

**Las trampas.**
- `estimar: 38 + 47` → cerca de 90 (40 + 50).   `razonable: 38 + 47 = 75` → NO (la llevada olvidada).
- `razonable: 38 + 47 = 85` → SÍ, y es correcta.   `razonable: 38 + 47 = 95` → SÍ razonable, pero NO
  correcta (la estimación no caza errores pequeños; lo dice).
- `razonable: 38 + 47 = 815` → NO (cifras en su sitio equivocado).
- `razonable: 92 - 38 = 64` → estimación 90 − 40 = 50, banda 40 a 60: NO (la cuenta es 54).
- `razonable: 3 x 47 = 141` → 3 × 50 = 150, banda 135 a 165: SÍ.   `3 x 47 = 1210` o `= 121` → NO.
- `estimar: 247 + 385` → 200 + 400 = 600 (centenas, banda 100).
- `estimar: 12 : 3` → todavía no.   `estimar: 23 x 47` → todavía no (dos factores de dos cifras).

**Prueba de dominio.** Muestra de sumas, restas y productos: la respuesta buena siempre «razonable»;
respuestas malas típicas (sin llevada, ±10 y ±100, cifras cambiadas) cazadas cuando caen fuera de la
banda y nunca una buena rechazada; la banda contra el testigo.

**Para Carlos:** `estimar: 38 + 47`, `razonable: 38 + 47 = 75`, `razonable: 38 + 47 = 95`,
`razonable: 3 x 47 = 141`.

## 2. LO QUE SE HIZO
- Parte nueva `sistema/partes/estimar.py`:
  - `estimar: 38 + 47`: redondea cada número con la pregunta `redondear` (N.2; hasta 99 a la decena,
    de 100 en adelante a la centena), hace la cuenta fácil con las piezas y calcula la **banda**
    (5 + 5 en decenas, 50 + 50 en centenas; en a × b con un factor de una cifra, a × 5 o a × 50).
  - `razonable: 38 + 47 = 75`: mira en la lista si la respuesta cae dentro de la banda; fuera, «seguro
    que está mal»; dentro, «razonable». Después hace la cuenta de verdad: si era razonable pero no la
    buena, lo dice («la estimación caza los errores grandes, no los pequeños»).
  - Respuestas honestas: dividir o dos factores grandes → todavía no; dos factores de una cifra → no
    hace falta (es de la tabla); restar más de lo que hay → imposible; si la banda pasa de mil, se
    corta en mil y lo dice.
- `pruebas/test_E6_razonable.py` (19 afirmaciones: trampas; 190 cuentas con la banda contra el
  testigo y la buena nunca rechazada; 813 respuestas malas típicas — sin llevada, ±10, ±100, ×10 —
  cazadas fuera de la banda y «razonable pero mal» dentro). Ayuda, `mis_pruebas.txt` (5),
  `mis_casos.txt` (8).

## 3. RESULTADO
- `estimar: 38 + 47` → cerca de 90 (entre 80 y 100).  `razonable: 38 + 47 = 75` → no.
- `razonable: 38 + 47 = 95` → «si, pero mal: es 85».  `razonable: 3 x 47 = 141` → si (banda 135 a 165).
- Proyecto: **1913/1913 afirmaciones + 534/534 casos — VERDE**.

## 4. PENDIENTE: la prueba de Carlos.  Con E.6 queda completo 3.OA.D.8 (dos pasos, letra y estimación).
Lo que dice la pedagogía que sigue (a proponer): NCETM Year 4 — 2.11 tablas del 11 y del 12; 2.12
multiplicar y dividir por 10 y 100 / división con resto; y la multiplicación de varias cifras.
