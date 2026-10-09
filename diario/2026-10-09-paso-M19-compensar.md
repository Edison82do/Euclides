# Paso M.19 — CALCULAR COMPENSANDO — 9 oct 2026

Siguiente paso del orden de NCETM en 6.º: el segmento **2.25** (Spine 2, Year 6), *Using compensation to calculate*.
Se llama **M.19** porque sigue la serie (M.17 la multiplicación larga, M.18 la división larga).

**REGLA desde el plan U (Carlos, 9 oct):** lo nuevo entra por el MODELO COMÚN. Las técnicas nuevas son PIEZAS de la
pregunta `multiplicar`, que el resolvedor universal y todas las piezas que multiplican ya usan; se eligen por su costo
cuando conviene; **no se abre ninguna puerta ni formato nuevo**.

## 1. EL PLAN (escrito antes de programar)

**La fuente.** La web de NCETM sigue bloqueada desde la nube (`EGRESS_BLOCKED www.ncetm.org.uk`, probado hoy con
`primm-225-using-compensation-to-calculate`). Lo que sigue sale del **buscador** (el resumen de la página del segmento
2.25). **Falta leer el segmento entero** (diapositivas) cuando Carlos pueda abrirlo.

La introducción del segmento: *cómo cambian los resultados de multiplicar y dividir cuando UNO de los números se
escala por un factor* (la compensación MULTIPLICATIVA; la aditiva fue 1.29, nuestro P.7). Sus **tres puntos**:
1. **Multiplicar:** si un factor se escala, el producto se escala por el mismo factor.
2. **Dividir, cambia el dividendo** (el divisor igual): el cociente se escala por el mismo factor.
3. **Dividir, cambia el divisor** (el dividendo igual): si el divisor se hace k veces mayor, el cociente se hace k veces
   menor; si el divisor se hace k veces menor, el cociente k veces mayor.

Y para CALCULAR (lo que pide Carlos): se cambia un número para que la cuenta sea fácil y luego se **compensa** el
resultado. Los dos ejemplos de Carlos:
- `4997 + 2345 = 5000 + 2345 - 3` — **ya lo hace Euclides** desde P.7 (NCETM 1.29): `la misma suma` (5000 + 2342) y
  `redondear un sumando y quitar lo que sobra`; y en la resta `quitar el redondo y devolver`. No se toca.
- `399 x 6 = 400 x 6 - 6` — **no lo hace**: hoy sale con la multiplicación corta (tres columnas con llevadas).

**Lo que ya hay de los tres puntos (y no se rompe).**
- Punto 1 con 10, 100: `multiplicar_por_decenas_justas` (M.9: 9 x 80 es diez veces 9 x 8) y `quitar los ceros` (M.17).
- Punto 2: `dividir_decenas_justas` (4800 : 6 es cien veces 48 : 6).
- Punto 3 junto con el 2 (los dos a la vez): `dividir_escalando` (M.12: 1800 : 50 = 3600 : 100 = 36).
- Derivar de una cuenta que se sabe con `si ... :` es de P.7 y solo para + y −. **No se amplía** (sería un formato nuevo
  para esa puerta): pregunta abierta para Carlos.

**Cómo lo haría un humano de 6.º sin calculadora.** Mira los números antes de calcular («¿hay alguno cerca de un
redondo, o es un 5 o un 25?»):
- `399 x 6`: 399 está a 1 de 400. 400 x 6 = 2400 (4 x 6 = 24, con dos ceros: punto 1). Pero puse UN grupo de 6 de más
  (400 grupos en vez de 399): lo quito. 2400 - 6 = 2394.
- `1999 x 7` = 2000 x 7 - 7 = 13993; `98 x 37` = 100 x 37 - 2 x 37 = 3700 - 74 = 3626; `302 x 8` = 300 x 8 + 2 x 8.
- `25 x 37`: 25 x 4 = 100, así que 25 es 100 cuatro veces más pequeño (punto 1 al revés): 100 x 37 = 3700, y el producto
  es cuatro veces más pequeño: la mitad de la mitad, 1850, 925. `5 x 4683`: x 10 y la mitad: 46830 : 2 = 23415.
- No compensa cuando el número no está cerca de un redondo (`347 x 6`: la corta), o cuando ya hay un camino más corto
  (las tablas, un factor con ceros, doblar y partir 25 x 16, las parejas de 100 con 25 x 36).

**Lo que se construye** (PIEZAS de `multiplicar`; el motor, el resolvedor y las puertas no cambian; cada pieza con su
VUELTA real por las operaciones contrarias):
1. `multiplicar_redondeando_un_factor` (rapidez 6.5): un factor de más de doce está a 1, 2 o 3 de un redondo con UNA
   sola cifra que no es cero (50, 400, 5000, 2000000) — lo mira `buscar_el_redondo_cercano` (P.7). Se multiplica el
   redondo (la cifra por el otro factor —el hecho de la tabla o la corta— y los ceros) y se quitan (o se ponen) los
   grupos de más (1, 2 o 3 veces el otro factor, sumando). **Vuelta:** la contraria de cada paso: devolver los grupos
   quitados vuelve al producto del redondo; ese producto sin sus ceros y repartido entre la cifra del redondo vuelve al
   otro factor; y si el otro factor es de una cifra, el total entero repartido entre él (como la corta) vuelve al
   factor de partida.
2. `multiplicar_por_5_o_25_compensando` (rapidez 6.6; punto 1 de 2.25): un factor es 5 o 25 y el otro de dos cifras o
   más. x 5 = x 10 y la mitad; x 25 = x 100 y la mitad de la mitad (5 es 10 dos veces más pequeño; 25 es 100 cuatro
   veces más pequeño: el producto también). Solo si sale justo (el producto por 10 o 100 se parte justo, que siempre
   pasa). **Vuelta:** doblar lo que salió (sumando) una o dos veces vuelve al producto por 10/100; quitando los ceros,
   el otro factor.
- **El costo.** Las dos van antes de la corta (7) y de la larga (9.5) porque, cuando encajan, son UN hecho de la tabla
  con ceros y una resta pequeña (o una o dos mitades), en vez de una columna por cifra con llevadas. Encajan SOLO en ese
  caso (cerca de un redondo, o un 5 o un 25); si no, se queda lo de antes. Detrás de las tablas, la memoria, x 10,
  decenas justas, doblar la tabla, doblar y partir (6): eso sigue siendo más corto.
- **El número no cambia nunca**; lo que cambia es el MÉTODO de las multiplicaciones que encajan (por ejemplo `99 x 37`
  antes era partir un factor; `5 x 4683` la corta).

**Las trampas** (los errores típicos de la compensación):
- **Compensar al revés**: 399 x 6 = 2400 + 6 (sumar en vez de restar el grupo de más). La vuelta lo caza.
- **Quitar 1 en vez de un grupo**: 399 x 6 = 2400 - 1 = 2399 (se quita el número que se redondeó, no el GRUPO). La
  vuelta lo caza (2399 : 6 no da 399).
- **Escalar mal** en el punto 1: 25 x 37 = 3700 : 2 (una mitad sola). La vuelta lo caza.
- Que no robe lo que ya es más corto: `25 x 16` sigue doblar y partir; `25 x 36` las parejas de 100; `8 x 7` las tablas;
  `400 x 6` decenas justas; `347 x 6` la corta; `11 x 12` las tablas.
- Cerca del techo: `1999999 x 5` = 9999995 (el redondo 2000000 x 5 = 10000000 es el techo); `2999999 x 4` se pasa:
  «se pasa», como antes.
- Sin las tablas sabidas: no puede repartir para comprobar, así que no sale y sigue el método de antes.

**Prueba de dominio** (`pruebas/test_M19_compensar.py`, pocas y representativas): cada pieza contra el testigo (Python
`*`, SOLO en la prueba) en una muestra al azar fijo; qué pieza elige el control (y lo que no roba); las piezas trucadas
(las tres trampas); el techo; por el modelo común (la cuenta, `resolver: n = 399 x 6`, `n : 6 = 399`, `6 x n = 2394`);
lo de P.7 sigue igual (`4997 + 2345`); el tiempo (cada una por debajo de 2 s).

**Para Carlos:** `399 x 6`, `98 x 37`, `25 x 37`, `5 x 4683`, `n : 7 = 1999`.

## RESULTADO (9 oct 2026)

**Hecho. `test_M19` 44/44; proyecto en cuartos 3484/3484 afirmaciones + 890/890 casos, VERDE; mis_pruebas 272/272; casos 890/890;
`comparar_puertas` 0 diferencias sin explicar.** Falta la prueba de Carlos.

**Lo que se construyó** (PIEZAS de `multiplicar`; ninguna puerta ni formato nuevo):
- `multiplicar_redondeando_un_factor` (rapidez 6.5): un factor de más de doce justo POR DEBAJO de un redondo de una cifra
  (lo mira `buscar_el_redondo_cercano` de P.7); el redondo por el otro (el hecho de la tabla o la corta, con los ceros) y
  se quitan los grupos de más (sumando el otro factor). La vuelta: devolver los grupos, quitar los ceros y repartir entre
  la cifra del redondo, repartir los grupos entre cuántos son y, si el otro es de una cifra, repartir el total entre él
  (como la corta, dentro de la pieza: usar `division_corta` sería una vuelta en el mapa).
- `multiplicar_por_5_o_25_compensando` (rapidez 6.6; el punto 1 de 2.25): x 10 y la mitad; x 100 y la mitad de la mitad
  (`dividir_a_la_mitad`). La vuelta: doblar sumando y quitar los ceros.
- Dos condiciones en `_condiciones.py` (prefijo `_m19_`). El motor no cambia.

**EL COSTO (cómo se elige).** Las dos van antes de la corta (7) porque, cuando encajan, son un hecho de la tabla con ceros y
una resta pequeña (o una o dos mitades). La condición ES el juicio del costo: compensar solo si los grupos de más son
uno o dos (quitar un grupo o su doble); con TRES (`47 x 6` = 300 − 18) ya no compensa y se queda la corta (lo vio
`test_M10`, B1, la primera vez: el número era el mismo, 282, pero el método cambiaba). Por ENCIMA del redondo (`401 x 6`)
es partir, no compensar: la corta. Si el otro acaba en cero, quitar los ceros es más corto. Lo que ya era más corto
(tablas, x 10, decenas justas, doblar y partir) va antes. (No se ha hecho la idea general de «cuánto cuesta este caso»
de CLAUDE.md: aquí basta con la condición.)

**Lo que cambia sin cambiar el número.** El MÉTODO de las multiplicaciones que encajan: `399 x 6` y `5 x 4683` antes la
corta; `98 x 37`, `99 x 99` y `25 x 37` antes partir un factor. Ninguna afirmación vieja ni ningún caso cambió.

**Lo que salió al probar.** Con tres grupos de más (47 x 6) robaba a la corta: se puso el tope de dos (el costo). Cerca del
techo, `25 x 380627` no puede hacer x 100 (38 062 700 se sale de la lista): la pieza dice que no le sale y lo hace otro
método (la respuesta, la misma).

**Los límites que quedan (honestos).**
- Los puntos 2 y 3 del segmento (el dividendo o el divisor escalados) no tienen pieza nueva: ya los hacen `dividir_decenas_
  justas` (M.9) y `dividir_escalando` (M.12: 1800 : 50 = 3600 : 100). Una pieza «: 50 = : 100 y el doble» haría lo mismo.
- **Derivar de un hecho con x y :** («si 3 x 8 = 24, ¿30 x 8?», «si 36 : 4 = 9, ¿36 : 8?»), que es como NCETM enseña los
  tres puntos, NO entra: la orden `si ... :` de P.7 es solo de + y −, y ampliarla sería un formato nuevo para esa puerta.
  **Pregunta abierta para Carlos.**
- Redondear un factor que NO es de una cifra significativa (1297 x 3 = 1300 x 3 − 9) no se hace: 13 x 3 ya es otra cuenta.
- La web de NCETM sigue bloqueada desde la nube: falta leer el segmento 2.25 entero (diapositivas).
