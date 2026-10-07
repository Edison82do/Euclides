# Paso S.2 — LAS ESTRUCTURAS COMUNES: PARTE-PARTE-TODO CON TRES PARTES O MÁS — 7 oct 2026

Sigue al M.16. Es el segmento **1.28** de NCETM (Spine 1, Year 5): *Common structures and the part–part–whole
relationship*. Se llama **S.2** porque es de ESTRUCTURAS, como S.1 («veces», NCETM 2.17). En Common Core no tiene
un estándar propio de 5.º: es la estructura «Put Together/Take Apart» de la tabla 1 (K–2, 1.OA.A.1, 2.OA.A.1)
llevada a tres partes o más, a números grandes y a decimales (5.NBT.B.7: sumar y restar decimales hasta las
centésimas), y a contextos de medida (4.MD.A.2, 4.MD.A.3: el perímetro con un lado que falta).

## 1. EL PLAN (escrito antes de programar)

**La fuente.** La web de NCETM **sigue sin poder abrirse desde la nube** (`EGRESS_BLOCKED www.ncetm.org.uk`,
lo he vuelto a probar hoy). Lo que sigue sale del índice de NCETM en el buscador (página
*primm-128-common-structures-and-the-part-part-whole-relationship*). Falta leer el segmento entero (los
ejemplos, las representaciones y los archivos de Year 5) cuando Carlos pueda abrirlo.

- **El objetivo del segmento:** «ampliar la estructura parte-parte-parte-todo (**tres partes o más**) para
  resolver problemas de **parte que falta y de todo que falta** en contextos variados».
- **Punto 1:** «Las relaciones matemáticas de primaria son **aditivas o multiplicativas**; las dos se ven en
  la estructura parte-parte-todo». (Partes distintas: se suman. Partes iguales: el todo son tantas veces la
  parte, y la parte es el todo repartido.)
- **Punto 2:** «En muchos contextos el todo se halla **sumando las partes**. Se pueden usar **estrategias
  distintas** para calcular el todo, pero **la estructura del problema es la misma**».
- **Punto 3:** «Si se sabe el todo y todas las partes menos una, la parte que falta se puede calcular. Se
  pueden usar estrategias distintas, pero la estructura es la misma».
- **Punto 4:** «Problemas de **contextos muy distintos** tienen la misma estructura de **parte que falta**»
  (el perímetro con un lado que falta, el dinero que queda, un camino por tramos, una clase por grupos…).
- Viene de NCETM 1.2 (todo y partes), 1.5 (juntar y partir) y del R.1 de Euclides (los 11 tipos de CGI, con
  dos partes). Lo nuevo: **tres partes o más**, y **ver la estructura igual en contextos distintos**.

Los errores típicos (NCETM *The Bar Model*: «el signo ? marca la parte que no se sabe; sabiendo dos de los
tres valores, se halla el tercero»; Oak National KS1 *Understanding part-part-whole relationships*; las
progresiones de Common Core sobre «Put Together/Take Apart»; resúmenes en el buscador):
- **Sumar el todo con las partes**: «100, 37 y 25; ¿la parte que falta?» → 100 + 37 + 25 = 162. Es tomar
  todos los números y juntarlos sin mirar quién es el todo.
- **Quitar solo una parte**: 100 − 37 = 63 (se olvida el 25).
- **Las partes que se saben ya pasan del todo** (30 de perímetro con lados 20 y 15): no puede ser, y hay que
  decirlo, no dar un número.
- **Dos partes que faltan**: con una sola cuenta no se sabe (pueden ser muchas parejas), salvo que las partes
  sean IGUALES (entonces es repartir: la estructura multiplicativa del punto 1).
- **Con decimales, no alinear el punto**: 2.5 + 0.75 = 0.80 (es 3.25).

**Cómo lo hace un humano sin calculadora (y así lo hará Euclides).**
- **Dibuja la barra** (el modelo de barras de Singapur / NCETM): arriba el todo, abajo las partes, con un ? en lo
  que falta. Mira qué falta: ¿el TODO o una PARTE?
- **Falta el todo → junta las partes.** Estrategias (punto 2):
  - en orden: 37 + 25 = 62; 62 + 63 = 125;
  - **las parejas amigas primero**: «37 y 63 hacen cien (7 + 3 = 10), lo junto antes: 37 + 63 = 100; y 100 + 25
    = 125». (Con decimales igual: 1.25 y 0.75 hacen 2.)
  - **partes iguales**: 6, 6, 6, 6 son 4 seises: 4 x 6 = 24 (punto 1, la estructura multiplicativa).
- **Falta una parte → quita del todo lo que se sabe.** Estrategias (punto 3):
  - **una a una**: 100 − 37 = 63; 63 − 25 = 38;
  - **juntando primero lo que se sabe**: 37 + 25 = 62 (una suma, más fácil), y luego **una sola resta**:
    100 − 62 = 38;
  - **partes iguales que faltan**: «24 en 4 partes iguales» → 24 : 4 = 6 (repartir, M.3).
- **Comprueba con la operación contraria**: el todo que salió, quitándole las partes de la última a la primera,
  tiene que dejar la primera (125 − 63 = 62, 62 − 25 = 37); la parte que salió, sumada con las otras, tiene que
  dar el todo (37 + 38 + 25 = 100); la parte igual, multiplicada por cuántas son, el todo (4 x 6 = 24).
- **Los contextos (punto 4)**: lo mismo con otras palabras: el perímetro es el todo y los lados son las partes;
  lo que tenía es el todo y lo que gasté y lo que me queda son las partes; el camino entero y los tramos… El
  sistema dice en cada caso **quién es el todo y quiénes las partes**, y que es la MISMA estructura.

**Lo que se construye.**
- Dos preguntas nuevas de las piezas (las dos «la más rápida»):
  - **`todo_de_las_partes`** — situación `{"partes": ["37", "25", "63"]}`.
  - **`parte_del_todo`** — situación `{"todo": "100", "partes": ["37", None, "25"]}` (o todas `None` con
    `"iguales": True`).
- Piezas (cada una con su **vuelta real** con la operación contraria):
  - `todo_sumando_en_orden` (rapidez 20): usa `combinar` (M.16, que ya suma con el punto en su sitio).
    Vuelta: el todo menos las partes, de la última a la primera, tiene que dejar la primera.
  - `todo_juntando_las_parejas_amigas` (rapidez 8): tres partes o más y dos cuyas últimas cifras (con el punto
    alineado) hacen diez, **contándolas con los dedos** (`contar_adelante`), no con Python. Las junta primero.
    Vuelta: igual que la anterior.
  - `todo_por_partes_iguales` (rapidez 6): todas las partes iguales → cuántas son (contadas recitando) x la
    parte (`multiplicar` o `multiplicar_decimal`). Vuelta: el todo entre cuántas son (`dividir` o
    `dividir_decimal`); si no se puede dividir, sumando las partes.
  - `parte_quitando_una_a_una` (rapidez 20): usa `combinar` (el todo − p1 − p2 …). Vuelta: todas las partes,
    con la que salió, suman el todo.
  - `parte_juntando_lo_que_se_sabe` (rapidez 12; con dos partes conocidas o más): usa `todo_de_las_partes`
    (así las parejas amigas también sirven aquí) y una sola resta. Vuelta: la misma suma de todas.
  - `parte_repartiendo_en_partes_iguales` (rapidez 10): el todo en N partes iguales → `dividir` /
    `dividir_decimal`; si sobra, «no salen partes iguales justas». Vuelta: N x la parte = el todo.
- Conocimiento nuevo `conocimiento/parte_parte_todo.kn` (FIJADO): la estructura, sus reglas, los errores y
  **los contextos** (cada uno: la palabra del todo, las de las partes, la unidad). Un contexto nuevo es una
  línea del `.kn`, no código.
- Parte nueva `sistema/partes/parte_todo.py` (prefijo `_ppt_`): lee la orden, dibuja la barra, pregunta a las
  piezas, enseña la otra estrategia («LO MISMO: la estructura no cambia»), los errores típicos y la vuelta.
- Las órdenes:
  - `partes: 37, 25, 63; todo: ?` → 125
  - `todo: 100; partes: 37, ?, 25` → 38
  - `todo: 24; partes: ?, ?, ?, ? iguales` → 6 (cada parte)
  - con contexto: `perimetro: 30; lados: 8, 7, 6, ?` → 9 cm; `tenia: 20; gaste: 4.50, 7.25; queda: ?`
    → 8.25 pesos; `camino: ?; tramos: 1.25, 3.5, 0.75` → 5.5 km.
- **Todavía no / no se puede:** dos partes que faltan sin ser iguales («no se puede saber»), las partes que se
  saben pasan del todo («no puede ser»), pasar del millón («no alcanza»), más de tres cifras detrás del punto
  («todavía no», D.2), las fracciones como partes (es Spine 3: 3.7 y 3.8, después).

**Las trampas.**
- `todo: 100; partes: 37, ?, 25` → 38 (no 162, no 63).
- `partes: 37, 25, 63; todo: ?` → 125, y por las parejas amigas (37 + 63 = 100 primero).
- `perimetro: 30; lados: 20, 15, ?` → no se puede (los lados que se saben ya pasan del perímetro).
- `todo: 50; partes: 20, ?, ?` → no se puede saber (faltan dos partes).
- `todo: 26; partes: ?, ?, ?, ? iguales` → no salen justas (sobran 2).
- `partes: 2.5, 0.75, 1.125; todo: ?` → 4.375 (el punto alineado).
- `todo: 10; partes: 4, 6, ?` → 0 (la parte que falta puede ser cero).
- Cerca del techo: `partes: 999999, 1; todo: ?` → 1000000; `partes: 999999, 2; todo: ?` → no alcanza;
  `todo: 1000000; partes: 250000, ?, 250000, 250000` → 250000 (y por partes iguales no: hay una que falta sola).

**Prueba de dominio.** Contra el testigo (Python, solo en la prueba): todos que falta con 2 a 6 partes enteras
(hasta 6 cifras) y decimales de 1 a 3 cifras; partes que faltan en cada sitio; partes iguales (todo y parte);
los errores (pasan del todo, dos que faltan, no salen justas); los contextos del `.kn`, cada uno con su
unidad; cada pieza con una cuenta trucada (la vuelta lo caza); lo de antes sigue igual (`perimetro: 4, 7, 5`,
`37 + ? + 25 = 100`, R.1); y el tiempo: cada pregunta, con su explicación, en menos de 2 s.

## RESULTADO (7 oct)

**Hecho, verde: proyecto 2620/2620 + 723/723.** `test_S2_parte_parte_todo` 72/72; mis_casos 723/723; mis_pruebas 201/201;
la auditoría sin calculadora, limpia.

- Dos preguntas nuevas (`todo_de_las_partes`, `parte_del_todo`) y 6 piezas, sin tocar el motor de piezas. **Todas se comprueban
  con la operación contraria**, y la prueba G lo demuestra: con la cuenta que piden dando uno de más, la vuelta no cuadra.
  - Falta el todo: `todo_por_partes_iguales` (6; 4 x 6 = 24, vuelta 24 : 4 = 6), `todo_juntando_las_parejas_amigas` (8; las
    últimas cifras hacen diez, **contado con los dedos**: 37 + 63 = 100 primero; con decimales 1.25 + 0.75 = 2),
    `todo_sumando_en_orden` (20). Vuelta: el todo menos las partes, de la última a la primera, deja la primera.
  - Falta una parte: `parte_repartiendo_en_partes_iguales` (10; 24 : 4, y si sobra, a décimas como en M.13: 26 : 4 = 6.5;
    vuelta 4 x 6 = 24), `parte_juntando_lo_que_se_sabe` (12; usa `todo_de_las_partes`, así las amigas también valen aquí, y una
    sola resta), `parte_quitando_una_a_una` (20). Vuelta: todas las partes, con la que salió, suman el todo.
  - Las sumas y restas (con el punto en su sitio) las hace `combinar` de M.16: nada de copiar cuentas.
- Conocimiento nuevo `parte_parte_todo.kn` (FIJADO) con **los contextos como datos**: perímetro/lados (cm), tenía/gasté-queda
  (pesos), camino/tramos (km), clase/grupos (niños), bolsa/cosas (kg), día/ratos (horas). Un contexto nuevo es una línea.
- Parte nueva `sistema/partes/parte_todo.py`: lee la orden, dice quién es el TODO y quiénes las PARTES («la MISMA estructura,
  solo cambian las palabras»), dibuja la barra con el ?, enseña la otra estrategia («LO MISMO: la estructura no cambia»), los
  errores típicos (`100 + 37 + 25 = 162`, `100 - 37 = 63`) y la vuelta. Si no falta nada, dice si **cuadra**.
- **Cambio respecto al plan:** `todo: 26; 4 partes iguales` no dice «no salen justas»: da **6.5**, cambiando a décimas como en
  M.13 (lo haría un niño de 5.º). «No salen justas» queda para cuando sobra aun en milésimas (`todo: 10; 3 partes iguales`).
- Las trampas, todas en verde: pasan del todo → `no_se_puede`; faltan dos → `no_se_puede`; faltan el todo y una parte →
  `no_se_puede`; unas se saben y las que faltan son iguales → `todavia_no` (son dos pasos); la parte puede ser 0.
- Dominio contra el testigo (Fraction, solo en la prueba): 150 todos y 150 partes que faltan (2 a 6 partes, hasta 5 cifras,
  en cualquier sitio), 160 con decimales de 1 a 3 cifras, 112 de partes iguales (todo y parte), 9 contextos con su unidad.
- **Cerca del techo:** `partes: 999999, 1` = 1000000; `999999, 2` → no alcanza; `1000000` en 4 partes iguales = 250000;
  `0.001, 0.999, 999999` = 1000000 (las amigas primero). **Límite que se hereda de M.13:** `todo: 999999.999; partes: 0.001, ?`
  dice «no alcanza» porque contado en milésimas pasa del millón (un humano lo haría; es el mismo techo que en M.16).
- **Tiempo:** cada pregunta con su explicación, 0.01–0.1 s; la prueba entera, 6 s.
- La prueba dejó ver una cosa: con la memoria VACÍA, `1000000` en 4 partes → «todavía no», porque la división corta pide la
  tabla del 4 (bien: en 5.º las tablas se saben; la prueba las aprende antes, como la de M.16).
- Una prueba de M.16 quedó **obsoleta por mejora** («ninguna pieza usa `combinar`»): ahora las de S.2 lo usan. Se cambió a
  «ninguna pieza de `combinar` usa `combinar`» (que es lo que vigila la vuelta en el mapa), con el caso viejo escrito al lado.
- Todavía no: escribir el problema en lenguaje rústico con tres personas («Ana, Luis y Eva tienen 100 entre los tres»: R.1 lee
  «entre los dos»); las fracciones como partes (Spine 3, 3.7–3.8); quitar y luego repartir (dos pasos).
- **Falta la prueba de Carlos.** Y leer el segmento entero de NCETM 1.28 (los archivos de Year 5) cuando se pueda abrir: si
  trae contextos o trampas que aquí no están, se añaden (un contexto nuevo es una línea del `.kn`).
