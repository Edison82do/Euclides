# Paso M.18 — DIVIDIR ENTRE DOS CIFRAS: LA DIVISIÓN LARGA — 9 oct 2026

Siguiente paso del orden de NCETM en 6.º: el segmento **2.24** (Spine 2, Year 6), *Division: dividing by two-digit
divisors*. Se llama **M.18** porque sigue la serie (M.11 la división corta, M.17 la multiplicación larga).

**REGLA desde el plan U (Carlos, 9 oct):** lo nuevo entra por el MODELO COMÚN. Las técnicas nuevas son PIEZAS de la
pregunta `dividir`, que el resolvedor universal y todas las piezas que dividen (factores, primos, tres factores,
combinar, simplificar...) ya usan; **no se abre ninguna puerta ni formato nuevo**.

## 1. EL PLAN (escrito antes de programar)

**La fuente.** La web de NCETM sigue bloqueada desde la nube (`EGRESS_BLOCKED www.ncetm.org.uk`, probado hoy con
`primm-224-division-dividing-by-two-digit-divisors`). Lo que sigue sale del **buscador** (el resumen de la página del
segmento 2.24), de las lecciones de **Oak National** de Year 6 («dividing by a 2-digit divisor including using long
division», «… with a remainder», «using short and long division to divide by a 2-digit divisor»), del mapa de
currículo de un colegio que enlaza sus unidades a 2.24 («división usando factores; introducción a la división larga;
la división larga con resto») y de **Common Core 5.NBT.B.6 / 6.NS.B.2** (5.º: dividendos de hasta cuatro cifras entre
dos cifras con estrategias de valor de posición; 6.º: el algoritmo estándar con fluidez; los cocientes parciales son el
puente). **Falta leer el segmento entero** (diapositivas) cuando Carlos pueda abrirlo.

Los **tres puntos de enseñanza** de 2.24 (según el buscador, traducidos):
1. **Dividendos de dos y tres cifras con el cociente MENOR que 10**: se divide entre dos cifras **contando en múltiplos
   del divisor** (saltos); luego se puede escribir con la corta o la larga.
2. **Dividendos de tres y cuatro cifras con el cociente de 10 O MÁS**: la división **corta o larga** (el algoritmo).
3. **El resto**: el cociente entero con resto entero, con el resto como fracción, o el cociente en decimales.

Lo que dicen Oak y NCETM de cómo se hace y de los errores:
- **Hacer la lista de los múltiplos del divisor** (1 x 24, 2 x 24 ... 9 x 24) antes de empezar: da eficacia y exactitud.
  Se hace con lo que se sabe (doblar, x 10, x 5) o sumando el divisor una y otra vez.
- **Estimar antes** con hechos sabidos y el valor de posición (432 : 12 → 400 : 12 es algo más de 30).
- La larga **escribe la resta debajo** del dividendo y **baja la cifra siguiente** al lado (el cambio de sitio).
- **Error de valor de posición (unitising)**: «7 centenas : 12» no da ni una centena (1 centena x 12 = 1200 ya se pasa):
  se piensa en múltiplos del divisor en ese sitio (6 decenas x 12 = 72 decenas).
- Errores de cuenta (NFER): restar mal, poner una cifra de más o de menos en el cociente (olvidar un 0 en el cociente
  cuando el divisor no cabe en un paso de en medio: 2448 : 24 = 102, no 12).
- **División usando factores** (dividir entre un divisor compuesto: : 24 = : 4 y luego : 6), la contraria del punto 5
  de 2.23.

**Lo que ya hay (y no se rompe).** `dividir_saltando` (M.3) cuenta de divisor en divisor: con un divisor de más de 12
para a los CIEN saltos («eso es la división larga (6.º), todavía no»); con 11 y 12, hasta mil saltos (432 : 12 sale
contando 36 saltos de 12). La corta (M.11) solo con una cifra; cambiar los dos igual (M.12: 600 : 25 = 1200 : 50 = 120 : 5).
El resolvedor (`numero._nu_entre`) divide con la pregunta `dividir`; si no es justo, el cociente es una FRACCIÓN
(5.NF.B.3). M.17 dejó `comprobar deshaciendo` para lo que no se podía dividir.

**Cómo lo haría un humano de 6.º sin calculadora.** Mira el divisor y el tamaño del cociente:
- si el cociente va a ser menor que 10 (el dividendo no llega a diez veces el divisor), **cuenta en múltiplos del
  divisor** (punto 1): eso ya lo hace `dividir_saltando` (pocos saltos) y se queda igual;
- si el divisor de dos cifras es una **pareja de la tabla** (24 = 4 x 6) y se reparte justo, **divide por sus factores**:
  8544 : 4 = 2136, 2136 : 6 = 356 (dos divisiones cortas);
- si no, la **división larga** (punto 2):
  ```
           356
         -----
    24 | 8544        múltiplos de 24: 24, 48, 72, 96, 120, 144, 168, 192, 216
         72          85 decenas de centena... → 8 millares : 24 no da: tomo 85 centenas
         --          85 : 24 → 3 (3 x 24 = 72), 85 - 72 = 13
         134         bajo el 4: 134 decenas : 24 → 5 (120), 134 - 120 = 14
         120
         ---
          144        bajo el 4: 144 : 24 → 6 (144), 144 - 144 = 0
          144
          ---
            0
  ```
  y lo COMPRUEBA con la contraria: cociente x divisor + resto = dividendo (356 x 24 = 8544, con las piezas de multiplicar
  de M.17).

**Lo que se construye** (PIEZAS de la pregunta `dividir`; el motor, el resolvedor y las puertas no cambian de forma;
cada pieza con su VUELTA real):
1. `division_larga` (punto 2; rapidez 9.5): divisor de DOS cifras y cociente de 10 o más. La lista de múltiplos del
   divisor se hace SUMANDO el divisor (lo que hace un niño; no hace falta saber la tabla del 24). De izquierda a derecha:
   se toman cifras hasta que cabe el divisor; en cada paso el múltiplo más grande que cabe (comparando con el
   mecanismo), la RESTA debajo, y se BAJA la cifra siguiente; si el divisor no cabe, se pone un **0 en el cociente**
   (la trampa de 2448 : 24 = 102). El resto, lo que queda al final. El dibujo de la larga. Vuelta: cociente x divisor
   (pregunta `multiplicar`) + resto = dividendo; y el resto menor que el divisor.
2. `dividir_por_un_divisor_compuesto` (la división usando factores; rapidez 9.2): divisor de dos cifras que es una pareja
   de la tabla que se sabe (la de en medio: 24 = 4 x 6), cociente de 10 o más y que se reparta JUSTO en los dos pasos
   (con resto, el resto cambia de tamaño: se deja a la larga). Dos divisiones cortas. Vuelta: el cociente x 6 x 4
   (la corta) vuelve al dividendo.
- **El cociente menor que 10** se queda con los saltos de M.3 (punto 1); las rapideces dejan el orden de un humano:
  casos especiales, la tabla, x 10, decenas justas, la mitad, cambiar los dos igual (6), la corta (7), los factores
  (9.2), la larga (9.5), y contar saltos (20) solo si no hay otra.
- **Respetar el año**: el divisor de TRES cifras o más sigue «todavía no» (2.24 es entre dos cifras): el mensaje de
  `dividir_saltando` lo dice así.

**Los «todavía no» que ahora se pueden hacer** (por el modelo común: todas dividen con la pregunta `dividir`):
- las cuentas `8544 : 24`, `5678 : 23` y en el resolvedor `24 x n = 8544` (→ 356), `n x 47 = 9776`, `8544 : n = 24`;
- **factores y primos** (M.15): las parejas probando 1, 2, 3 ... llegaban hasta 12; ahora siguen dividiendo entre dos
  cifras (`factores: 169` → 1 x 169, 13 x 13; `primo: 997` → primo). Con un número cuyo medio pide dividir entre tres
  cifras (más de 99 x 99 = 9801), sigue «todavía no»;
- **tres factores** (M.14): `99 x 99 x 99` decía «todavía no» porque no lo podía comprobar dividiendo: ahora
  970299 : 99 : 99 = 99 (lo pendiente de la revisión de M.14);
- lo que se comprobaba en el OTRO ORDEN porque dividir pedía la larga (combinar, M.16) ahora se comprueba dividiendo;
- simplificar fracciones (F.6) y lo que use `parejas_de_factores`.
- **No** se tocan (son de otros pasos): dividir ENTRE un decimal o un decimal entre dos cifras (`7.2 : 12`, decimales:
  más adelante), dividir dentro de una cuenta combinada (2.28), fracción por fracción (3.9).
- **El punto 3** (el resto como fracción): el resolvedor ya da el cociente como fracción cuando no es justo
  (`n = 437 : 12`); se comprueba que sale con la larga. El cociente en decimales se deja para cuando toque dividir
  decimales.

**Las trampas.**
- El 0 en el cociente: 2448 : 24 = 102 (no 12); 7224 : 24 = 301; 24024 : 24 = 1001.
- El primer paso: 7 centenas : 12 no da → se toman 75 decenas (no se escribe un 0 delante del cociente).
- Una larga TRUCADA (que olvida el 0 del cociente, o que resta mal) no se da por buena: su vuelta no cuadra.
- El resto: 437 : 12 = 36 resto 5 (el resto menor que el divisor); 9999 : 99 = 101 resto 0.
- Por factores con resto: 437 : 12 no se hace por factores (437 : 3 : 4 no deja el resto bien): la larga.
- Lo de antes con el cociente pequeño: `96 : 24` y `84 : 14` siguen con los saltos; `600 : 25` sigue cambiando los dos.
- Divisor de tres cifras: `98765 : 123` sigue «todavía no».
- Cerca del techo: `9999999 : 99`, `9999999 : 11`.
- Lo que cambia es el MÉTODO en divisiones entre 11 y 12 con el cociente de 10 o más (432 : 12 antes 36 saltos de 12;
  ahora por factores o la larga). El número, el mismo.

**Prueba de dominio** (`pruebas/test_M18_division_larga.py`, pocas y representativas): cada pieza contra el testigo
(Python `//` y `%`, SOLO en la prueba) en una muestra al azar fijo de dividendos de 3 a 7 cifras y divisores de 10 a 99;
qué pieza elige el control; los ceros del cociente; las piezas trucadas; el techo; los tres cifras «todavía no»; por el
modelo común (cuenta, `24 x n = 8544`, `8544 : n = 24`, `n = 437 : 12`); factores y primos de antes y de ahora; tres
factores; lo que no cambia; el tiempo (cada una por debajo de 2 s).

**Para Carlos:** `8544 : 24`, `2448 : 24`, `5678 : 23`, `24 x n = 8544`, `primo: 997`.

## RESULTADO (9 oct 2026)

**Hecho. `test_M18` 55/55; proyecto 3440/3440 afirmaciones + 883/883 casos, en tercios, VERDE; mis_pruebas 267/267;
`comparar_puertas` 0 diferencias sin explicar.** Falta la prueba de Carlos.

**Lo que se construyó** (PIEZAS de `dividir`; ninguna puerta ni formato nuevo):
- `division_larga` (punto 2, rapidez 9.5): la lista de múltiplos del divisor se va escribiendo SUMANDO el divisor al último
  (por columnas, con el mecanismo; no hace falta saberse la tabla del 23); en cada sitio el múltiplo más grande que cabe
  (comparando con el mecanismo), la resta debajo, se baja la cifra; si no cabe, un 0 en el cociente. El dibujo de la larga.
  Vuelta: cociente x divisor (la pregunta `multiplicar`, con las piezas de M.17) + resto = dividendo, y el resto menor que
  el divisor. Funciona también SIN las tablas.
- `dividir_por_un_divisor_compuesto` (la división usando factores, rapidez 9.2): 8544 : 24 = 8544 : 4 : 6 (dos cortas),
  solo si se reparte justo las dos veces. Vuelta: x 6 y x 4 (la corta) vuelve al dividendo.
- Dos condiciones nuevas en `_condiciones.py` (prefijo `_m18_`): divisor de dos cifras y cociente de 10 o más (el
  dividendo llega a diez veces el divisor: el divisor con un 0 detrás, comparado con el mecanismo); y que además sea una
  pareja de la tabla.
- `dividir_saltando`: con TRES cifras dice «dividir entre tres cifras todavía no». `dividir_escalando` prueba la larga
  antes que los cien saltos (era lento: 0,1 s por cada fallo).
- `parejas_de_factores_en_orden` (M.15): sigue probando entre dos cifras hasta cruzarse; si 100 x 100 no se pasa del
  número, dice «todavía no» al empezar (como antes, sin probar 99 divisiones para nada).

**Los «todavía no» que ahora salen** (cada uno es la división larga; todos por el modelo común, sin tocar su parte):
- `24 x n = 8544` → 356 (antes no_sale); `n x 47 = 9776` → 208; `resolver: 8544 : n = 24` → n = 356.
- `n : 24 = 356` → 8544: antes contestaba el resolvedor (n = 8544, comprobando deshaciendo); ahora la puerta vieja de E.5
  ya sabe comprobar 8544 : 24 y contesta ella, con su forma (`8544`, como `24 x n = 8544` → `356`). El número, el mismo.
- `factores: 169` → 1, 13, 169; `primo: 997` → primo; `primo: 1001` → compuesto; factores de 170, 200, 500, 1000...
- `99 x 99 x 99` → 970299 y `13 x 17 x 19` → 4199 (M.14 no los podía comprobar dividiendo: lo pendiente de la revisión de
  M.14). `1814 : 15` → 120 resto 14 (M.12). `a + b = 567127; a = 10 x b` → a = 515570, b = 51557 (S.3).
- Simplificar 836/722 → 22/19, 221/247 → 17/19, el mayor factor común de 200/300 (F.6).
- 15 afirmaciones viejas (test_M12, M14, M15, M17, F6, S3) y 5 casos de Carlos miraban esos «todavía no»: actualizados
  con el caso viejo escrito al lado. Ningún otro número cambia.

**Lo que cambia sin cambiar el número.** El MÉTODO en divisiones entre 11 y 12 (y entre dos cifras) con el cociente de
10 o más: 432 : 12 antes eran 36 saltos de 12; ahora 432 : 3 : 4. Los saltos se quedan para el cociente menor que 10.

**Lo que salió al probar (y se arregló).**
- La primera lista de múltiplos usaba la pregunta `sumar` (todas sus piezas, con sus condiciones) ocho veces por
  división: `factores: 9991` tardaba 2 s. Ahora se escribe cuando hace falta, con la suma por columnas del mecanismo.
- `dividir_escalando` doblaba 55 → 110 y probaba cien saltos de 110 antes de rendirse; ahora prueba antes la larga.
- La auditoría sin calculadora cazó `margen + T` (unir textos con `+`): con formato.

**Los límites que quedan (honestos).**
- Dividir entre TRES cifras sigue «todavía no» (2.24 es entre dos); por eso factores/primos llegan hasta 9999.
- `factores: 9991` hace 99 divisiones largas: ~1,5 s (lo más largo del año; un humano tardaría una tarde).
- El punto 3 (el resto como fracción) lo da el resolvedor (`n = 437 : 12` → 437/12); como mixto (36 5/12) o en decimales
  (dividir decimales), todavía no.
- `7.2 : 12` (un decimal entre dos cifras) sigue «todavía no»: es de dividir decimales, otro paso.
- La corta con divisor de dos cifras (que NCETM también enseña) no se hace aparte: la larga escribe lo mismo con las restas.
- La web de NCETM sigue bloqueada desde la nube: falta leer el segmento 2.24 entero (diapositivas).
