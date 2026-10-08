# Fase U.1 — EL MODELO Y EL LECTOR SIMBÓLICO — 8 oct 2026

Primera fase del **plan U** (`diario/2026-10-08-PLAN-U-volverlo-universal.md`). El avance por años sigue en pausa.
Regla de oro: **prohibido memorizar problemas o familias de problemas**; solo relaciones generales, operadores generales
y búsqueda con control. Nada viejo cambia de respuesta; lo nuevo, con pocas pruebas representativas.

## 1. EL PLAN (escrito antes de programar)

**Lo que dicen las fuentes** (las del plan U, ya en `FUENTES.md`, más las del currículo de cada operación):
- **Mayer (1992) y Kintsch y Greeno**: traducir → integrar en un MODELO (lo que se sabe, lo que falta, cómo se relacionan)
  → planear → ejecutar → comprobar. Esta fase hace el modelo y la traducción de lo que viene escrito con símbolos.
- **Pólya, «trabajar hacia atrás»**, y **Newell y Simon (medios y fines)**: si en una relación falta UNA cantidad, se
  deshacen las operaciones de fuera hacia dentro (es `letra._deshacer`, de E.5: Common Core 3.OA.D.8, 6.EE.B.7,
  7.EE.B.4: `px + q = r`, `p(x + q) = r`). Si faltan varias, se busca una que se pueda decir con las otras y se pone en
  su sitio (sustituir): el número de incógnitas baja.
- **El dibujo de barras (NCETM 1.31)**: cuando la misma letra sale varias veces, se cuentan los TROZOS
  (`x = y; z = 2 x y` → x es 1 trozo de y, z son 2; con y, 1 + 1 + 2 = 4 trozos = 40). Contar trozos no es una receta de
  una familia: vale para cualquier relación lineal, con cualquier número de letras.
- **Los números se mezclan como lo hace un niño** (Common Core 7.NS.A.1–2 y 7.NS.A.2d; NCETM 3.7, 3.8, 1.23–1.24, 1.27):
  un decimal ES una fracción de diez, cien o mil (D.1/D.2: 0.25 son 25 centésimas = 25/100 = 1/4, F.6); dos fracciones
  se suman con el MISMO DE ABAJO (F.7); un negativo es un número del otro lado del cero (N.5): sumar dos de signo
  distinto es quitar el más pequeño del más grande, y queda el signo del más grande (en la recta). Multiplicar
  fracciones: arriba por arriba y abajo por abajo (5.NF.B.4; con décimas, M.13 «contar las partes»); dividir entre un
  entero: si el de arriba se reparte justo, se reparte (45 décimas : 3 = 15 décimas); si no, se parte cada trozo
  (3/4 : 2 = 3/8, 5.NF.B.7); dividir entre una fracción es multiplicar por ella dada la vuelta (6.NS.A.1). Un entero que
  no se reparte justo es una fracción (5.NF.B.3: 7 : 2 = 7/2).

**Cómo lo haría un humano sin calculadora.** Lee lo que está escrito, ve qué letras hay y qué relaciones; si una relación
tiene una sola letra, la despeja deshaciendo (o contando trozos si sale varias veces); si no, busca una letra que esté
dicha con las otras (`x = y`) y la mete en las demás; al final pone los números en el enunciado de partida y mira si
cuadra. Las cuentas las hace con lo que sabe: sumar, restar, multiplicar y dividir enteros (las piezas), el mismo de
abajo y simplificar (F.6/F.7), la recta (N.5).

**Lo que se construye.**
1. **El NÚMERO común** (parte nueva `sistema/partes/numero.py`, prefijo `_nu_`): un número es `(signo, arriba, abajo,
   tipo)` con tipo entero, decimal o fracción. Leer `4.5` → 45/10 (decimal); `1/2` → fracción; `-3` → negativo. Las
   cuatro cuentas, cada una con las PIEZAS de siempre (`sumar`, `restar`, `multiplicar`, `dividir`, `mismo_de_abajo`,
   `simplificar_fraccion`, `hueco_equivalente`) y comparando tamaños con el mecanismo (`viene_despues`). Cada cuenta deja
   su línea de explicación («0.25 = 25/100 = 1/4», «1/2 = 2/4», «2/4 + 1/4 = 3/4»). Escribir el resultado en el tipo que
   toca: si hubo una fracción, fracción en su forma más simple (y su decimal si sale justo en décimas, centésimas o
   milésimas); si solo decimales, decimal; si solo enteros, entero (o fracción si no da justo).
2. **El lector único** (parte nueva `sistema/partes/universal.py`, prefijo `_u_`): amplía el de `letra` — números enteros,
   decimales (punto o coma), fracciones (`1/2`), negativos (`-3`, `x = -2`, `3 x (-2)`), paréntesis, varias letras,
   varias ecuaciones con `;`, el `x` que es POR entre dos cosas y LETRA en los demás sitios, `2n` = 2 x n. Devuelve el
   MODELO: `{cantidades (las letras, en el orden en que salen), relaciones (árboles izq = der), pide}`. Sin `=`: una
   expresión para calcular.
3. **Los operadores** (sin receta de ninguna familia):
   - **calcular despejando**: una relación con UNA sola letra que falta: si sale una vez, se deshace de fuera hacia
     dentro (como E.5, con el NÚMERO común); si sale varias veces y es lineal, se cuentan los trozos (k trozos y un número
     suelto) y se deshace; si no es lineal (`y x y`), «todavía no» (U.2: probar en orden).
   - **sustituir**: si ninguna relación tiene una sola letra, se elige una con letras donde una letra esté SOLA en un lado
     (`x = y`, `z = 2 x y`) o, si no, una que salga una sola vez (se aísla deshaciendo, con letras: `a = 1/2 - b`), y se
     pone en todas las demás. Al final se calcula lo aislado con los números que salgan.
   - **un presupuesto** (de los datos, `conocimiento/universal.kn`): un humano no da cien vueltas; si se agota, «todavía no».
4. **La comprobación final** en TODAS las relaciones ORIGINALES (no en las transformadas), calculando cada lado con el
   NÚMERO común. Si no cuadra, no se da la respuesta. Si faltan relaciones (más letras que datos), «todavía no» (U.2).
5. **La puerta** `resolver:` (y `resolver ...` sin dos puntos) y **la red de seguridad**: lo que ninguna puerta vieja
   recoge y el lector simbólico lee entero (antes de caer en 0.1/0.2), y lo que una puerta vieja contesta con
   «NO ENTIENDO» pero el lector simbólico sí lee, va al resolvedor. Las ecuaciones con TRES letras o más ya no entran por
   S.3 (que solo sabe dos y decía «todavía no»): van a la red. Las dos cadenas (`explicar_pregunta` y `preguntar`) igual.
6. `conocimiento/universal.kn`: las reglas (el número común, los operadores, el presupuesto, la comprobación) y las fuentes.

**Las trampas.**
- `1/2 + 0.25` → 3/4 (= 0.75). No 1.25/2 ni 1/2.25: el decimal se pasa a fracción primero (0.25 = 1/4).
- `-3 + 2 x 4` → 5: primero el x (8); luego −3 + 8: signos distintos, 8 − 3 = 5 y el signo del 8. No −3 + 2 = −1, −1 x 4 = −4.
- `3 x n = 4.5` → 1.5 (45 décimas : 3 = 15 décimas). E.5 decía «no es entero»; aquí es un decimal.
- `(a + 5) x 2 = 26` → 8 (deshacer el x 2 primero: 13; luego el + 5).
- `a + b = 1/2; a - b = 1/4` → a = 3/8, b = 1/8 (sustituir a = 1/2 − b; quedan 2 trozos de b quitados de 1/2).
- `x + y + z = 40; x = y; z = 2 x y` → x = 10, y = 10, z = 20 (4 trozos = 40).
- Nada viejo cambia: `a + b = 30; a - b = 8` sigue por S.3 (la barra); `(a + 5) x 2 = 26` sigue por E.5;
  `a + b + c = 10` sigue «todavía no» (faltan relaciones); `3 + + 4` sigue «no entiendo».
- Una letra que falta y no se puede saber (`a + b = 10; 2 x a + 2 x b = 20`): las relaciones dicen lo mismo → todavía no.
- Contradicción (`a + b = 10; a + b = 12`) → ninguna (al sustituir queda 10 = 12, falso).
- Dividir entre cero (`0 x n = 5`, `5 : 0`) → no se puede.
- Cerca del techo (`n + 1 = 10000000`), números sin nombre → «todavía no», sin reventar.

**Prueba de dominio** (`pruebas/test_U1_modelo_y_lector.py`, pocas y representativas, como pidió Carlos): el lector (lo que
lee y lo que no), el NÚMERO común contra un testigo (`fractions.Fraction`, SOLO en la prueba) en una muestra pequeña de
cuentas mezcladas, los seis ejemplos del plan, las trampas de arriba, que las puertas viejas no cambian (unas cuantas
de cada una), la comprobación (una pieza trucada no da respuesta) y el tiempo (cada pregunta por debajo de 2–3 s).

**Para Carlos:** `resolver: a + b = 1/2; a - b = 1/4`, `3 x n = 4.5`, `x + y + z = 40; x = y; z = 2 x y`, `1/2 + 0.25`,
`-3 + 2 x 4`.

## RESULTADO (8 oct 2026)

**Hecho. `test_U1` 63/63; mis_pruebas 238/238; casos 824/824 (813 + 11 nuevos); batería vieja en verde (ver abajo).**

**Lo que se construyó.**
- `sistema/partes/numero.py` (prefijo `_nu_`): el NÚMERO común `(signo, arriba, abajo, tipo)`. Leer `7`, `4.5`/`4,5`,
  `1/2`, `-3`. Las cuatro cuentas, todas con las piezas de siempre (`sumar`, `restar`, `multiplicar`, `dividir`,
  `mismo_de_abajo`, `simplificar_fraccion`, `hueco_equivalente`) y comparando con `viene_despues`:
  - decimal con fracción → el decimal se dice como fracción (0.25 = 25/100 = 1/4) y el mismo de abajo (F.7);
  - signos distintos → el pequeño del grande, con el signo del grande (N.5); quitar de más → pasa del cero;
  - multiplicar → arriba por arriba, abajo por abajo; dividir entre un entero → repartir los de arriba si es justo
    (45 décimas : 3 = 15 décimas), si no, partir cada trozo (7 : 2 = 7/2); entre una fracción o un decimal → al mismo
    de abajo y cuántas veces cabe (3/4 : 1/8 = 6/8 : 1/8 = 6 : 1 = 6);
  - escribir en el tipo que toca (fracción en su forma más simple; decimal; entero) y, si había decimales y sale una
    fracción, también su decimal si es justo (3/4 = 0.75).
- `sistema/partes/universal.py` (prefijo `_u_`): el lector único (amplía el de `letra`: varias letras, `;`, fracciones,
  decimales, negativos con el `-` de delante, paréntesis, `2n` = 2 x n, la `x` POR entre dos cosas y LETRA en los demás
  sitios; con palabras no lee: eso es U.3) → el MODELO (cantidades, relaciones, lo que se pide; sin `=`, una cuenta).
  Operadores: **calcular despejando** (una letra que sale una vez: deshacer de fuera hacia dentro; varias veces: contar
  los TROZOS de cada lado y repartir; `0 x n` → ninguna o cualquiera; `n x n` → todavía no, U.2) y **sustituir** (una
  letra sola en un lado, o aislada deshaciendo con letras). El bucle con **presupuesto** (20 pasos, en `universal.kn`).
  **La comprobación** en TODAS las relaciones de partida. Relaciones que se contradicen → ninguna; que dicen lo mismo o
  faltan → todavía no (infinitas, U.2).
- Puerta `resolver:` y **red de seguridad** en las dos cadenas (`explicar_pregunta` y `preguntar`): antes de caer en
  0.1/0.2 (objetos), y cuando una puerta vieja dice NO ENTIENDO pero el resolvedor lo resuelve (si no lo resuelve, se
  queda lo de la puerta: nada viejo cambia). `dos_incognitas` solo coge ecuaciones con DOS letras (con tres decía
  «todavía no: no sé de qué forma es»; `a + b + c = 10` sigue «todavía no», ahora por E.5 como antes por S.3).
- `conocimiento/universal.kn`: las seis reglas, los errores típicos, las fuentes y el presupuesto.

**Los seis ejemplos del plan:** `a + b = 1/2; a - b = 1/4` → a = 3/8, b = 1/8 (antes: 0.2, «sin atributo común»);
`3 x n = 4.5` → 1.5 (antes: «un objeto»); `(a + 5) x 2 = 26` → 8 (ya salía por E.5; por `resolver:` también);
`x + y + z = 40; x = y; z = 2 x y` → 10, 10, 20 (antes: S.3 «todavía no»); `1/2 + 0.25` → 3/4 (antes: «un objeto»);
`-3 + 2 x 4` → 5 (antes: M.16 «no entiendo '-'»).

**Lo que salió al probar (y se arregló).**
- `13 - 5` decía «signos distintos (la recta)»: restar era sumar el opuesto. Ahora quitar de lo que hay es lo de
  siempre, y solo se habla de la recta cuando pasa del cero o hay negativos.
- Contar trozos enseñaba cuentas con ceros (`0 + 0 = 0`): ahora se dice cada lado como «1/2 quitando 2 trozos de b» y
  solo se enseñan las cuentas de verdad; si los trozos se QUITAN, «son lo que va de 1/4 a 1/2».
- `0 x n = 5` decía «no se puede dividir entre cero»: ahora «0 por algo es 0 siempre: ningún número cumple».
- La auditoría sin calculadora cazó dos `lista + lista` (las letras de un árbol): ahora con `.extend`.
- En la prueba, tres casos que creía nuevos los coge una puerta vieja (E.5 da `8` y no `a = 8`; S.3 da las 11 parejas
  de `a + b = 10; 2 x a + 2 x b = 20`; E.5 dice «todavía no» a `3 x n + 2 = n + 10`): se dejan como estaban y lo nuevo se
  prueba con `resolver:`. Juntar las puertas es U.4.

**Los límites que quedan (honestos).**
- Sin probar en orden ni juntar relaciones (U.2): `n x n = 49`, `a x b = 24; a + b = 10` por `resolver:` → todavía no.
- Más de tres decimales en lo que se escribe → todavía no (las milésimas, D.2).
- La explicación es de cuentas y trozos, todavía sin dibujar la barra (U.2).
- `test_F7` tiene una prueba de tiempo (`999 1/2 + 999 1/3` < 2 s) que en la nube da a veces 2,1 s; ya fallaba ANTES de
  U.1 en la batería de partida de esta sesión (3094/3095) y en otra pasada salió en verde. No es de U.1.
