# Paso M.16 — COMBINAR LA MULTIPLICACIÓN CON LA SUMA Y LA RESTA — 7 oct 2026

Sigue al M.15. Es el segmento **2.22** de NCETM (Spine 2, Year 5): *Combining multiplication with addition
and subtraction*. En Common Core: **5.OA.A.1** («usar paréntesis, corchetes o llaves en expresiones numéricas y
calcular expresiones con esos símbolos») y **5.OA.A.2** («escribir expresiones sencillas que recojan cálculos con
números, e interpretar expresiones sin calcularlas: "suma 8 y 7 y luego multiplica por 2" es 2 × (8 + 7); 3 ×
(18932 + 921) es tres veces 18932 + 921 sin hacer la suma ni el producto»). Viene de 3.OA.D.8 (los dos pasos,
que E.5 ya resolvía con la letra).

## 1. EL PLAN (escrito antes de programar)

**La fuente.** La web de NCETM **sigue sin poder abrirse desde la nube** (`EGRESS_BLOCKED www.ncetm.org.uk`;
también `thecorestandards.org`). Lo que sigue sale del índice de NCETM en el buscador (página
*primm-222-combining-multiplication-with-addition-and-subtraction*) y del texto de Common Core 5.OA.A, que ya
estaba en el proyecto. Falta leer el segmento entero (ejemplos y representaciones) cuando Carlos pueda abrirlo.

- **Los objetivos del segmento:** «aprender a combinar la multiplicación con la suma o la resta; aprender a usar
  los paréntesis para cambiar el orden de las operaciones; apoyarse en lo que se sabe de la propiedad
  distributiva».
- **Punto 1:** «La multiplicación se puede combinar con la suma y la resta. **Sin paréntesis, la multiplicación
  se hace antes** que la suma o la resta; **con paréntesis, primero lo de dentro** del paréntesis».
- **Punto 2:** «Al sumar o restar expresiones de multiplicar que tienen **un factor común**, se puede aplicar
  la **propiedad distributiva**» (4 × 6 + 4 × 2 = 4 × 8).
- Lo que sigue (NCETM 2.28, 6.º): combinar la **división** con la suma y la resta. Aquí todavía no.

Los errores típicos (NCETM, *Year 6 unit 12, Order of operations*; Mr Barton, *Probing questions: order of
operations*; Oak National, *the distributive law* (KS2 y KS3); resúmenes en el buscador):
- **Ir de izquierda a derecha sin mirar**: 3 + 4 × 5 = 35 (es 23).
- **Creer que la suma va antes que la resta** (por el orden de las letras de BIDMAS/PEMDAS): 10 − 3 + 2 = 5
  (es 9: la suma y la resta van **de izquierda a derecha**, en el orden en que vienen).
- **Juntar los factores comunes en vez de los otros**: 4 × 6 + 4 × 2 = (4 + 4) × (6 + 2) = 64 (es 4 × 8 = 32).
- **Creer que la distributiva solo vale con la suma**: también con la resta, 7 × 5 − 7 × 3 = 7 × 2.
- **Olvidar el término suelto**: 5 × 4 + 5 es 5 × 5 (el 5 suelto es 5 × 1), no 5 × 4.

**Cómo lo hace un humano sin calculadora (y así lo hará Euclides).**
- **El orden de siempre (punto 1).** «3 + 4 × 5: miro si hay paréntesis (no); **rodeo las multiplicaciones**:
  4 × 5 = 20; ahora queda 3 + 20 = 23». Con paréntesis: «(3 + 4) × 5: primero lo de dentro, 3 + 4 = 7; luego
  7 × 5 = 35». Varias sumas y restas: «10 − 3 + 2: de izquierda a derecha, 10 − 3 = 7, 7 + 2 = 9». Cada cuenta
  pequeña la hacen las piezas que ya hay (sumar, restar, multiplicar, multiplicar un decimal por un entero de
  M.13, tres factores de M.14).
- **Sacar el factor común (punto 2).** «4 × 6 + 4 × 2: los dos llevan un 4; son 6 cuatros y 2 cuatros, 8
  cuatros: 4 × 8 = 32». Una sola multiplicación en vez de dos (más fácil: 17 × 6 + 3 × 6 = 20 × 6 = 120). Con la
  resta igual: 7 × 5 − 7 × 3 = 7 × 2 = 14. Con un término suelto: 5 × 4 + 5 = 5 × 5 (el 5 es «un cinco»).
- **Respetar el año:** la división combinada (2.28) es de 6.º → «todavía no»; un decimal por otro decimal, de
  6.º → «todavía no»; bajarse de cero por el camino (N.5 solo en la recta) → «todavía no»; pasar
  del millón → «no alcanza».
- **Comprobar con la operación contraria** (lección de M.12): se deshace la cuenta **de la última a la primera**:
  3 + 4 × 5 = 23 → 23 − 3 = 20, 20 : 5 = 4, queda el 4 ✓. En el factor común: 32 : 4 = 8, 8 − 2 = 6, queda el 6 ✓.

**Lo que se construye.**
- Pregunta nueva **`combinar`** («la más rápida»), con la expresión ya leída como situación:
  `{"terminos": [["+", ["3"]], ["+", ["4", "5"]]]}` (cada término: su signo y sus factores; un factor es un número
  en texto o un paréntesis, que es otra expresión).
- Pieza **`combinar_en_el_orden_de_siempre`** (rapidez 20): paréntesis primero (recursivo), luego los productos de
  cada término (dos factores: `multiplicar` o `multiplicar_decimal`; tres o más: `multiplicar_tres`), luego + y −
  de izquierda a derecha (enteros: `sumar`/`restar`; con decimales: alineando el punto como en las columnas de
  D.2 y sumando en las unidades más pequeñas). **Vuelta**: cada cuenta, de la última a la primera, con la
  contraria (− por +, + por −, : por ×); si una división no se puede (el factor es 0, o pide la división larga),
  multiplicando en el otro orden.
- Pieza **`combinar_sacando_el_factor_comun`** (rapidez 5): dos términos de uno o dos números (sin paréntesis)
  que comparten un factor entero → a × (b ± c). **Vuelta**: dividir el resultado entre el factor común y deshacer
  la suma o la resta (32 : 4 = 8, 8 − 2 = 6).
- Parte nueva `sistema/partes/combinar.py` con las órdenes:
  `3 + 4 x 5` (suelta), `combinar: ...`, `calcular: 3 + 4 x 5` (**arreglo**: hoy `calcular: 3 + 4 x 5` dice **7**,
  porque lee solo `3 + 4`: es contestar con seguridad algo falso), `verdad: 3 + 4 x 5 = 35` (o suelta
  `3 + 4 x 5 = 23`). La explicación dice el orden, rodea las multiplicaciones, cuenta paso a paso, enseña el error
  de ir de izquierda a derecha (cuando sale distinto), y en el factor común enseña que el orden de siempre da lo
  mismo y que **no** es (4 + 4) × (6 + 2).
- **Todavía no:** la división combinada (2.28, 6.º), escribir la expresión desde palabras («suma 8 y 7 y luego
  multiplica por 2», 5.OA.A.2) y comparar sin calcular («3 × (18932 + 921) es 3 veces 18932 + 921»), los
  corchetes dentro de paréntesis más allá de lo que lee el árbol, los números con signo delante (−3 + 5 es N.5).

**Las trampas.**
- `3 + 4 x 5` → 23 (no 35). `20 - 3 x 4` → 8 (no 68). `(3 + 4) x 5` → 35.
- `10 - 3 + 2` → 9 (no 5). `4 x 6 + 4 x 2` → 32 (no 64). `7 x 5 - 7 x 3` → 14. `5 x 4 + 5` → 25.
- `calcular: 3 + 4 x 5` → 23 (no 7).
- `verdad: 3 + 4 x 5 = 35` → FALSO (35 es de izquierda a derecha).
- `2 x 3 - 4 x 5` → todavía no (por el camino se baja de cero; N.5 solo en la recta). `12 : 3 + 1` → todavía no (2.28).
- `0.5 x 4 + 1.25` → 3.25 (con decimales); `0.3 x 0.2 + 1` → todavía no (decimal por decimal).
- Cerca del techo: `999 x 1000 + 1000` = 1 000 000 (justo); `999 x 1000 + 1001` → no alcanza;
  `1000 x 1000 - 1` = 999 999.

**Prueba de dominio.** Contra el testigo (Python, solo en la prueba): todas las expresiones `a + b x c`,
`a - b x c`, `a x b + c`, `a x b - c`, `(a + b) x c`, `a x (b - c)`, `a x b + c x d`, `a x b - c x d` con una
muestra de números de 0 a 12 y de hasta tres cifras (las que dan negativo: «no se puede», nunca un número); los
factores comunes en todas las posiciones (a × b + a × c, b × a + c × a, a × b + c × a…); cadenas de + y − de 3 a 5
números; con decimales de una a tres cifras; cerca del millón. Cada pregunta en menos de 2 s.

## RESULTADO (7 oct)

**Hecho, verde: proyecto 2544/2544 + 708/708.** `test_M16_combinar_operaciones` 82/82; mis_casos 708/708; mis_pruebas 195/195;
la auditoría sin calculadora, limpia.

- Una pregunta nueva (`combinar`) y 2 piezas, sin tocar el motor de piezas. **Las dos se comprueban con la operación contraria**
  y la prueba H lo demuestra: con una multiplicación que da uno de más, la vuelta no cuadra y `aplicar` no la da por buena.
  - `combinar_en_el_orden_de_siempre` (rapidez 20): paréntesis (recursivo, también `((2 + 3) x 2 + 1) x 3`), luego los
    productos (dos factores con `multiplicar` o `multiplicar_decimal`; tres o más con `multiplicar_tres` de M.14), luego + y -
    de izquierda a derecha (con decimales: el punto en su sitio, se cuenta en las unidades más pequeñas). **Vuelta**: cada cuenta
    de la última a la primera: `23 - 20 = 3, 20 : 4 = 5`. Si una división no se puede (un factor 0, o la división larga), multiplica
    en el otro orden y lo dice.
  - `combinar_sacando_el_factor_comun` (rapidez 5, gana cuando encaja): dos términos de uno o dos números con un factor
    **entero** en común, en cualquier sitio (`6 x 3 + 2 x 3`, `5 x 4 + 5`, `999 x 1000 + 1000`). **Vuelta**: `32 : 4 = 8, 8 - 2 = 6`.
- Parte nueva `sistema/partes/combinar.py`: lee la cuenta (`x`, `×`, `*`, `−`, `[ ]`, coma decimal), la explica (el orden,
  «rodeo las multiplicaciones: 3 + «4 x 5»», los pasos, la vuelta) y **enseña el error** cuando sale distinto: de izquierda a
  derecha (35), la suma antes que la resta (`10 - (3 + 2) = 5`), `(4 + 4) x (6 + 2) = 64`; en el factor común enseña que el orden
  de siempre da LO MISMO. `verdad:` con cuentas combinadas (y escritas directamente, `3 + 4 x 5 = 23`).
- **Arreglo de un error viejo:** `calcular: 3 + 4 x 5` decía **7** (leía solo `3 + 4`): contestar con seguridad algo falso. Ahora 23.
  Y `x + 5 = 12` sigue siendo de E.5 (la x donde va un número es una letra).
- Dominio contra el testigo (Fraction, solo en la prueba): 8 formas × 45 cuentas (`a + b x c`, `a - b x c`, `a x b + c`, `a x b - c`,
  `(a + b) x c`, `a x (b - c)`, `a x b + c x d`, `a x b - c x d`; las que se bajan de cero, «todavía no»), 344 con factor común en
  todos los sitios (todas por la pieza del factor común), 80 cadenas de 3 a 5 sumas y restas, 240 con decimales de 1 a 3 cifras
  (2 dicen «todavía no» porque contadas en milésimas pasan del millón: el techo de M.13, comprobado por el testigo), 80 igualdades.
  Cerca del techo: `999 x 1000 + 1000` = 1000000, `999 x 1000 + 1001` → no alcanza, `1000 x 1000 - 1` = 999999,
  `999.999 + 0.001 x 1` = 1000. **Tiempo:** cada pregunta con su explicación, 0.2–0.4 s; la prueba entera, 8 s.
- Todavía no (con su porqué): la división combinada (2.28, 6.º); un decimal por otro decimal y un decimal por un entero de dos
  cifras (M.13); bajarse de cero por el camino (`3 - 5 + 4`: un humano podría cambiar el orden, 3 + 4 - 5, pero eso no está en
  2.22); escribir la expresión desde palabras y comparar sin calcular (5.OA.A.2).
- **Falta la prueba de Carlos.** Y leer el segmento entero de NCETM 2.22 cuando se pueda abrir (desde la nube está bloqueada):
  si trae ejemplos o trampas que aquí no están, se añaden.
