# Fase U.3b — LA COSA DE CADA CANTIDAD — 8 oct 2026

Fase intermedia del **plan U** (`diario/2026-10-08-PLAN-U-volverlo-universal.md`), pedida por Carlos tras la revisión de
U.3, que encontró una respuesta FALSA. Regla de oro: **prohibido memorizar problemas o familias de problemas**; solo
relaciones generales (datos), operadores generales y búsqueda con control. Nada viejo cambia de respuesta.

## 0. EL DIAGNÓSTICO (probado el 8 oct antes de tocar nada)

| enunciado | U.3 decía | lo que pasa |
|---|---|---|
| Ana tiene 8 años. Luis tiene 6 canicas. ¿Cuántas tienen entre los dos? | **14 anos** | suma años con canicas: FALSO |
| 3 cuadernos cuestan 12 pesos. ¿Cuánto cuestan 5 cuadernos? | **5 cuadernos** | «3 cuadernos» se leía como el número 3: FALSO |
| Juan tiene 20 pesos. Compra 3 lápices de 4 pesos cada uno. ¿Cuánto le queda? | **4 pesos** | «le queda» se iba al lápiz: FALSO |
| María tiene 8 años y 15 lápices. ¿Cuántos lápices tiene María? | ninguna (8 = 15) | María = 8 y María = 15 |
| Un camión lleva 12 cajas. Cada caja pesa 8 kilos. ¿Cuántos kilos lleva? | todavía no | el «por caja» no multiplica |
| Un rectángulo de 30 cm de perímetro; un lado mide 8. ¿Cuánto mide el otro? | no entiendo | «un lado / el otro» |
| Tengo 50 pesos. Gasto 32. ¿Cuánto me sobra? | no entiendo | «me sobra» |
| Una caja mide 5 cm por 4 cm por 3 cm. ¿Cuál es su volumen? | todavía no | «A por B por C» |
| Ana tenía 40 canicas. Pierde la mitad de lo que tenía. ¿Cuántas le quedan? | no entiendo | «de lo que tenía» |

**La causa es general:** el modelo no sabe de QUÉ es cada cantidad. Una cantidad era solo un nombre (`maria`); su
unidad era un adorno para la respuesta, no parte del modelo.

## 1. EL PLAN (escrito antes de programar)

**Lo que dicen las fuentes.**
- **Schwartz (1988), «Intensive quantity and referent transforming arithmetic operations»** (NCTM, Hiebert y Behr,
  eds.): una cantidad es un número CON SU REFERENTE (4 canicas). Sumar y restar CONSERVAN el referente: solo se suman
  cantidades de la misma cosa. Multiplicar y dividir lo TRANSFORMAN: una cantidad «intensiva» (la que lleva «por»:
  pesos por cuaderno, kilos por caja) por una «extensiva» (5 cuadernos) da otra extensiva (pesos).
- **Kintsch y Greeno (1985)** (WORDPRO): el texto se vuelve una lista de proposiciones sobre CONJUNTOS; cada conjunto
  tiene su objeto (de qué cosa), su cantidad y su especificación (de quién, cuándo). Dos frases solo hablan del mismo
  conjunto si coinciden en todo eso. Es lo que Mayer llama INTEGRAR el modelo de la situación.
- **Vergnaud (1983), las estructuras multiplicativas**: el «isomorfismo de medidas» (una caja ↔ 8 kilos; 12 cajas ↔ ?)
  es la proporción simple: con el valor de UNA (la unidad) se pasa a cualquier número de ellas; y el «producto de
  medidas» (largo por ancho, largo por ancho por alto).
- **NCETM 2.2 y Common Core 3.OA.A.3** (grupos iguales: número de grupos × lo de cada grupo, y sus inversas) y
  **Common Core 6.RP.A.3b** (el valor unitario: si 3 cuadernos cuestan 12, uno cuesta 4).

**Cómo lo haría un humano sin calculadora.** Al leer «María tiene 8 años y 15 lápices» apunta DOS cosas de María: sus
años y sus lápices. Cuando le preguntan «cuántos lápices en total» junta solo los LÁPICES de cada uno; si le preguntan
«cuántos tienen entre los dos» y uno tiene años y el otro canicas, dice que eso no se junta. Si 3 cuadernos cuestan 12,
sabe que todos cuestan lo mismo: uno cuesta 4 y 5 cuestan 20. Si un camión lleva 12 cajas y cada una pesa 8 kilos, el
camión lleva 12 veces 8 kilos. Al final mira la respuesta: ¿junta cosas distintas? entonces algo leyó mal.

**Lo que se construye.**
1. **Cada cantidad es (de quién, de qué cosa).** En el lector (`palabras.py`) cada frase tiene su COSA (las palabras que
   van detrás del número: «15 lápices», «8 años», «12 pesos»; en la pregunta, detrás de «cuántos»: «cuántos lápices»).
   Una cosa con nombre (una persona, el camión) que sale con DOS cosas distintas da DOS cantidades: la primera conserva
   su nombre (`maria`: así nada viejo cambia de nombre) y las otras se llaman `maria_lapices`. Las versiones en el
   tiempo (los cambios) van con cada (de quién, de qué cosa) por separado. Si se pregunta por alguien que tiene varias
   cosas sin decir cuál, no se adivina: «no entiendo».
2. **Las cosas, en datos** (`frases.kn`): las palabras que son la misma cosa (singular y plural; kg = kilos) y las
   palabras GENÉRICAS que valen por una cosa de su clase («dinero» → pesos, euros...; «edad» → años): «¿cuánto dinero
   le queda?» pregunta por sus pesos.
3. **Solo se suman o restan cantidades de la misma cosa**: «en total», «entre los dos» juntan la cosa que pregunta la
   pregunta (o la de la frase); los miembros que no la tienen no se juntan (si falta, no se adivina).
4. **«Cada» es GRUPOS IGUALES** (Schwartz: lo intensivo × lo extensivo): «cada X pesa P», «P por X», «N X de P cada
   uno», «el precio de cada X», «K X de P pesos»; y con los VERBOS DE CADA (`frases.kn`: cuesta, vale, pesa, mide...)
   «3 cuadernos cuestan 12» es 3 × (lo de un cuaderno) = 12 (todos los cuadernos cuestan lo mismo). Lo que se
   SABE (relaciones.kn, grupos iguales): si alguien tiene N de X (12 cajas) y X tiene lo de cada uno en otra cosa (8
   kilos por caja), lo suyo de esa otra cosa = N × lo de cada X (los kilos del camión = cajas × kilos por caja).
5. **La comprobación final mira las cosas** (capa 4): cada relación del modelo se mira con las cosas de sus cantidades;
   en un `+`, un `-` o un `=` las dos partes tienen que ser de la misma cosa (un número suelto vale con cualquiera);
   en `x` y `:` la cosa se transforma (no se mira). Si una relación junta cosas distintas, no se da la respuesta:
   mejor «no entiendo» que una respuesta falsa.
6. **Los otros fallos generales del lector**, cada uno en datos o en la gramática general:
   - las preguntas «¿cuánto me sobra?», «¿cuánto queda?», «¿cuánto le queda?» (son lo de AL FINAL de quien se habla;
     «me», «te» son como «le»); «¿qué temperatura hace?» (qué + cosa = cuánto de esa cosa);
   - las figuras con «un lado / el otro»: el rectángulo tiene dos lados distintos (largo y ancho), dichos en
     `relaciones.kn` («pares: lado = largo, ancho»); «el otro» es el otro de la pareja del último que se nombró;
   - las medidas con «por»: «mide A por B (por C)» da las DIMENSIONES de la figura en su orden (`relaciones.kn`:
     `dimensiones: largo, ancho, alto`); «por» delante de una cosa sin número («5 kilos por caja») es «de cada»;
   - los cambios que dependen de lo que había: «pierde la mitad de lo que tenía» (de lo que tenía ANTES de ese cambio),
     «subió 3/4 de lo que había bajado» (del cambio anterior de esa cosa con ese verbo); los participios («bajado»,
     «ganado»...) en `frases.kn`;
   - comprar con dinero es un CAMBIO del dinero del que compra (gasta lo que cuestan las compras);
   - la proporción simple (el valor de una, y las veces) sale de los puntos 4 y 1, sin regla propia.

**Las trampas.**
- «Ana tiene 8 años. Luis tiene 6 canicas. ¿Cuántas tienen entre los dos?» → NO entiendo (no 14).
- «María tiene 8 años y 15 lápices. Luis tiene 6 lápices. ¿Cuántos lápices tienen en total?» → 21 lápices (sobra la edad).
- «3 cuadernos cuestan 12 pesos. ¿Cuánto cuestan 5 cuadernos?» → 20 pesos (y «¿cuánto cuesta un cuaderno?» → 4).
- «Juan tiene 20 pesos. Compra 3 lápices de 4 pesos cada uno. ¿Cuánto le queda?» → 8 pesos (no 4).
- «Un camión lleva 12 cajas. Cada caja pesa 8 kilos. ¿Cuántos kilos lleva el camión?» → 96 kilos.
- «Pedro tiene 12 años y 30 canicas. Juan tiene 5 canicas más que Pedro. ¿Cuántas canicas tienen entre los dos?» → 65.
- Ninguna respuesta vieja cambia: los nombres de las cantidades de una sola cosa siguen iguales.

**Prueba de dominio** (`pruebas/test_U3b_la_cosa.py`, pocas y representativas, inventadas): cosas distintas de una misma
persona, «en total» que junta solo una cosa, cosas mezcladas → no entiendo, información que sobra, grupos iguales con
cada forma de decir «cada», la proporción simple, las preguntas nuevas, «un lado / el otro», «A por B por C», cambios de
lo que había, y que la comprobación de las cosas caza una relación que mezcla (trucada a mano).

**Para Carlos:** el de María, el de los cuadernos, el del camión, el del rectángulo con «el otro», el de la temperatura.

## RESULTADO (8 oct 2026)

**Hecho. `test_U3b` 29/29; `test_U3` 51/51; mis_pruebas 252/252; casos 853/853 (843 + 10 nuevos); proyecto
3281/3281 afirmaciones + 853/853 casos (en tercios), VERDE.** Falta la prueba de Carlos.

**Lo que se construyó** (todo en `palabras.py`, prefijo `_pa_`, y el vocabulario en `frases.kn` / `relaciones.kn`):
- **La cosa de cada frase** (`_pa_cosa_de_toks`): las palabras detrás del primer número del dato o del «?» de la pregunta;
  si no hay, la que dice el VERBO (`frases.kn`, `cosa_del_verbo`: «cuesta» → dinero, «pesa» → masa, «mide» → longitud),
  o la de la frase núcleo anterior («Ana tiene 5 canicas y Luis 3»).
- **(de quién, de qué cosa)** (`_pa_de_cosa`): la primera cosa de alguien se queda con su nombre (`maria`; así nada viejo
  cambia de nombre); otra cosa distinta es otra cantidad (`maria_lapiz`), con sus propias versiones en el tiempo. Sin
  cosa y con varias: no se adivina («no se de cual se habla»). Las cosas se comparan en singular, con las que son la misma
  (`mismas_cosas`: kg = kilo) y las GENÉRICAS (`cosas_genericas`: dinero ↔ pesos, euros...; edad ↔ años; masa, longitud,
  temperatura).
- **La comprobación de las cosas** (`_pa_comprobar_cosas`, capa 4): en cada relación del modelo, `+`, `-` e `=` tienen
  que unir la misma cosa (un número suelto vale con cualquiera; `x` por un número la conserva; `x` y `:` entre cantidades
  la transforman). Si algo junta cosas distintas: «no entiendo» con el porqué. La explicación dice de qué cosa es cada
  cantidad.
- **Grupos iguales**: los VERBOS DE CADA (`verbos_de_cada`: cuesta, vale, pesa...) hacen de «3 cuadernos cuestan 12»
  `3 x cuaderno = 12`; «N u por X» (`_pa_por_cada`) es lo de cada X; y lo que se SABE: si alguien tiene N de X y se sabe
  lo de cada X en otra cosa, lo suyo de esa cosa = N x lo de cada X (los kilos del camión). La proporción simple sale de
  ahí sin regla propia (el valor de una con el buscador; «8 kilos» es «8 kilos de peras» si es lo único por kilo).
- **Comprar con precio es gastar** (`_pa_paga_comprando`): si el que compra tiene dinero, baja lo que cuestan las compras.
- **Las preguntas**: «me sobra», «le queda», «sobran» (`verbos_quedan`, `verbos_quedan_le`); «qué temperatura hace»
  (qué + cosa = cuánto de esa cosa); «Si …, ¿cuánto…?» (lo de antes del «¿» es un hecho).
- **Las figuras**: `pares` («un lado / el otro» del rectángulo = largo / ancho) y `dimensiones` («mide A por B por C»).
- **Lo que había**: «la mitad de lo que tenía» (antes de ese cambio), «3/4 de lo que había bajado» (el cambio de antes con
  ese verbo; los participios en `frases.kn`); «y luego» también parte la frase.

**Lo que cambia de respuesta** (solo el lector de palabras, por `resolver:` o por la red de seguridad; nada de la batería
vieja ni de `mis_casos` cambió): las tres respuestas FALSAS de U.3 ahora son «no entiendo» (años + canicas) o la buena
(20 pesos, 8 pesos); y los «no entiendo / todavía no» del diagnóstico ahora se resuelven (ver la tabla del §0).

**Los límites que quedan (honestos).**
- «Pedro tiene 15 canicas y 9 años. Gana 4.» → no entiendo (no se sabe de qué gana: un humano diría canicas porque los años
  no se ganan; eso sería saber qué cosas pueden cambiar, no está en los datos).
- «Ana tiene 12 pesos. Luis tiene 5 canicas. ¿Cuántos pesos en total?» → todavía no (no supone que Luis tiene 0 pesos).
- Las unidades distintas de una misma magnitud (kilos y gramos) son cosas distintas: no se pasan de una a otra.
- «el otro» solo sabe de las parejas de las figuras y de los grupos de números; «un lado» es siempre el primero.
- Las cantidades «por» solo con la forma «N cosa por X» al final del dato.
