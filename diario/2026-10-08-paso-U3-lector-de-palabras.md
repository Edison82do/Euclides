# Fase U.3 — EL LECTOR DE PALABRAS — 8 oct 2026

Tercera fase del **plan U** (`diario/2026-10-08-PLAN-U-volverlo-universal.md`). Regla de oro: **prohibido memorizar
problemas o familias de problemas**; solo relaciones generales (datos), operadores generales y búsqueda con control.
Nada viejo cambia de respuesta; lo nuevo, con pocas pruebas representativas.

## 1. EL PLAN (escrito antes de programar)

**Lo que dicen las fuentes** (ya en `FUENTES.md`, sección del plan U):
- **Bobrow (1964), STUDENT**: el enunciado se parte en **frases núcleo**, cada una con UN dato; cada frase núcleo se
  convierte en una ecuación con unas pocas reglas de lenguaje («es» → =, «más» → +, «por» → x, «el doble de» → 2 x,
  «la suma de A y B» → A + B); las mismas palabras dichas en dos sitios son la misma cantidad; lo que se pregunta
  («¿cuánto es X?») es una ecuación más con la incógnita. Sus reglas estaban escritas a mano en el programa: aquí van
  en DATOS (`frases.kn`) para que crezcan sin tocar el código.
- **Bakman (2007), ROBUST**: cada frase da **proposiciones** pequeñas (una cantidad, un cambio, una comparación) que se
  van colocando en el modelo de la situación, vengan en el orden que vengan; la respuesta no debe cambiar si se
  reordenan las frases o se añade información que sobra. Las relaciones que se SABEN sin que el texto las diga (el
  perímetro de un rectángulo, «consecutivos») las pone el conocimiento del mundo, no el texto.
- **Riley, Greeno y Heller (1983); Kintsch y Greeno (1985)**: los esquemas son ESTRUCTURAS — cambio (al principio,
  cambio, al final), combinación (parte + parte = todo), comparación (grande = pequeño + diferencia) — y, en
  multiplicar, grupos iguales (todo = grupos x cada grupo) y comparación multiplicativa (grande = K x pequeño). Se
  rellenan con lo que haya: la incógnita puede estar en cualquier sitio (al principio, el cambio, el final...).
- **Mayer (1992)**: traducir cada frase → integrar en el modelo → planear → ejecutar → comprobar. Esta fase es la
  TRADUCCIÓN y la INTEGRACIÓN con palabras; planear y ejecutar ya lo hace el buscador de U.2.
- **Contra las palabras clave (NC2ML; METODO §5)**: la palabra no elige la operación. «Más que» dice QUIÉN es mayor
  (A = B + N), no «suma»: si lo que falta es B, el buscador acabará restando. Lo mismo «el doble»: A = 2 x B; si
  falta B, se reparte. La lectura da RELACIONES, nunca la cuenta.

**Cómo lo haría un humano sin calculadora.** Lee frase a frase y apunta lo que dice cada una («el lápiz y la goma
juntos: 12»; «el lápiz es dos gomas»); si una frase no la entiende, la deja aparte y mira si le hace falta; junta lo
apuntado (las mismas cosas son las mismas cantidades; «él» es el último que se nombró; «ahora» es después de los
cambios); se acuerda de lo que sabe sin que se lo digan (el perímetro de un rectángulo son dos largos y dos anchos;
dos números consecutivos se llevan uno); mira qué se pregunta; deja de lado lo que no tiene nada que ver con la
pregunta; y lo resuelve como siempre (la barra, despejar, probar...). Al final pone la respuesta con su unidad.

**Lo que se construye.**
1. **`conocimiento/frases.kn`** (el VOCABULARIO, datos): las palabras vacías, los verbos de VALOR («cuesta», «mide»,
   «tiene», «pesa», «hay», «vale», «es», «son», «hace» [grados]…, y sus pasados: «tenía», «costaba» → al principio),
   «suman», los verbos de CAMBIO (sube/gana/le dan… + ; baja/pierde/gasta… −; los que necesitan QUIÉN y los que no),
   «quedan», lo que JUNTA («entre los dos», «en total», «juntos»), las COMPARACIONES aditivas («más que», «menos que»,
   «mayor», «menor», los adjetivos que dan la vuelta: «más barato», «más corto»), los MULTIPLICADORES («el doble», «el
   triple», «la mitad», «un tercio», «la tercera parte», «K veces», «3/4 de», «tres cuartos»), las OPERACIONES de
   STUDENT («más», «menos», «por», «entre», «la suma de», «la diferencia entre», «el producto de», «su doble»,
   «a X le sumas N»), «cada», «grupos de», «reparte… entre», «mete… en bolsas de», los MOMENTOS («al principio»,
   «ahora», «por la mañana», «a mediodía»…), las preguntas («cuánto», «cuántas», «cuál»), las UNIDADES, los números
   sin nombre («un número», «otro número», «el otro», «algunas») y los denominadores con palabra (tercios, cuartos…).
2. **`conocimiento/relaciones.kn`** (las ESTRUCTURAS que se saben, datos, cada una UNA vez, con fórmula escrita con
   nombres): parte-todo (`todo = parte + parte`), cambio (`despues = antes + gana`; `despues = antes - pierde`),
   comparación aditiva (`grande = pequeno + diferencia`), comparación multiplicativa (`grande = veces x pequeno`),
   grupos iguales (`todo = grupos x cada_grupo`), precio y vuelta (`vuelta = pago - gasto`), las FIGURAS
   (rectángulo: `perimetro = 2 x largo + 2 x ancho`, `area = largo x ancho`; cuadrado; caja: `volumen = largo x ancho
   x alto`; cubo), y las relaciones de PALABRAS (`consecutivos`: el siguiente = el anterior + 1; «pares consecutivos»,
   + 2). El código lee las fórmulas con el lector de U.1 (sus nombres son cantidades).
3. **La parte `sistema/partes/palabras.py`** (prefijo `_pa_`), después de `buscar.py`:
   - **preparar**: minúsculas, sin tildes, los números con palabras con la secuencia (6.1/6.7), «un/una» son
     artículos (no números), «menos 2 grados» = −2, las fracciones con palabra (dos tercios = 2/3);
   - **partir** en frases (punto, interrogación, punto y coma) y cada frase en frases NÚCLEO por «y» y por la coma
     cuando el trozo de la derecha trae un dato; un trozo sin verbo toma el verbo (y el sujeto, si le falta) del de
     antes (la elipsis: «mide 8 de largo y 5 de ancho»; «Ana tiene 5 y Luis 3»);
   - **cada frase núcleo → proposiciones** (SUJETO VERBO OBJETO): el sujeto y el objeto se leen como EXPRESIONES de
     STUDENT (cantidades, números, «el doble de X», «X más 3», «la suma de A y B»); valor: `sujeto = objeto`; varios
     sujetos con «y» y verbo en plural, «entre los dos», «suman»: la SUMA; comparación: `A = B + N`, `A = K x B`; cambio:
     una cantidad NUEVA en el tiempo (`ana_1 = ana + 3`); cada / grupos de / repartir: grupos iguales; «N de largo»: el
     atributo de la figura;
   - **la pregunta es una frase más** con «?» en el sitio de lo que se busca («¿cuánto cuesta la goma?» → «la goma
     cuesta ?»; «¿cuántas más tiene Juan que Pedro?» → «Juan tiene ? más que Pedro»): sirve en cualquier sitio del
     texto (la primera, la última, con «si…» detrás);
   - **integrar**: las mismas palabras son la misma cantidad (singular y plural, «la roja» es «la cuerda roja»); sin
     sujeto, el último que se nombró (a quien le pasan cosas, una PERSONA, para «gana», «saca»; cualquiera para «sube»,
     «se van»); el tiempo (al principio, cada cambio, ahora = después del último cambio); «algunas», «un número»:
     incógnitas sin nombre; las fórmulas de `relaciones.kn` cuando sale su palabra (rectángulo, caja, consecutivos);
     las UNIDADES de cada cantidad (y cuadradas / cúbicas para área y volumen);
   - **lo que sobra no estorba**: solo se pasan al buscador las relaciones CONECTADAS con lo que se pregunta; lo demás se
     enseña como «sobra»;
   - **una frase que no se entiende** se dice; si con el resto basta, se resuelve igual — PERO si la frase rara trae un
     CAMBIO o nombra lo que se pregunta (podría cambiar la respuesta), no se adivina: no se contesta;
   - el MODELO (cantidades, relaciones, lo que se pide) va al buscador de U.2 tal cual; la comprobación en las relaciones
     de partida; la respuesta con su unidad.
4. **Las puertas**: `resolver:` con palabras usa este lector; y la **red de seguridad para problemas con palabras**:
   cuando la puerta vieja (R.1, R.2, escala, temperatura...) dice no entiendo / todavía no / no sé resolverlo, y el
   lector de palabras lo lee y el buscador lo resuelve y lo comprueba, contesta él. Si la puerta vieja contesta, se
   queda lo suyo (nada viejo cambia). En las dos cadenas.
5. **R.1, R.2, escala, temperatura, dinero, volumen, área y perímetro pasan a ser vocabulario**: sus frases están en
   `frases.kn` / `relaciones.kn`; una prueba pasa una muestra de sus problemas viejos por el lector NUEVO (con
   `resolver:`) y tiene que dar LO MISMO que la puerta vieja. Las puertas viejas siguen delante (U.4 las junta).

**Las trampas.**
- «Un lápiz y una goma cuestan 12 pesos. El lápiz cuesta el doble que la goma. ¿Cuánto cuesta la goma?» → 4 pesos
  (no 6: el doble no es la mitad de 12). Y con la pregunta PRIMERO, y con una frase que sobra en medio.
- «Ana tiene 8. Tiene 3 más que Luis. ¿Cuántas tiene Luis?» → 5: «más» acaba en resta (la lectura da `ana = luis + 3`).
- «un/una» no es el número 1 en «un lápiz»; sí en «un tercio» es la fracción 1/3.
- «la mitad» de algo que no es par → fracción (el número común de U.1), no «todavía no».
- El tiempo: «Pablo tenía algunas. Gana 5. Ahora tiene 12. ¿Cuántas tenía al principio?» → 7 (no 17).
- «Cada caja pesa 5 kilos. ¿Cuánto pesan 4 cajas?»: «4 cajas» son 4 x caja (grupos iguales), no 4 + 5.
- Figuras: el perímetro NO es largo x ancho; con el perímetro y el largo, sale el ancho (despejando).
- Consecutivos: «dos números consecutivos suman 31» → 15 y 16 (la relación que no dice el texto).
- «Un número y su mitad suman 18» → 12 (su = el número; la mitad = 1/2 x).
- Lo que sobra: «Ana tiene 9 años» en un problema de canicas no estorba.
- «En la caja hay 20 lápices. Saca 5. ¿Cuántos quedan?» sigue «no entiendo» (no se QUIÉN saca: la frase tiene un cambio
  y no se adivina; R.1 lo decía así y así sigue).
- Lo viejo no cambia: R.1, R.2, escala, temperatura siguen contestando por su puerta; `mis_casos` igual.

**Prueba de dominio** (`pruebas/test_U3_lector_de_palabras.py`, pocas y representativas, inventadas con frases
variadas): cada clase del vocabulario una o dos veces (valor, suma, comparación aditiva y multiplicativa, cambio con la
incógnita en cada sitio, grupos iguales, figuras, consecutivos, «un número y su mitad», precio y vuelta), el orden
cualquiera y lo que sobra, la frase que no se entiende (con y sin el resto bastando), las trampas, la muestra de las
puertas viejas por el lector nuevo (misma respuesta), que el vocabulario está en datos (una palabra nueva en
`frases.kn` entra sin tocar código), el tiempo.

**Para Carlos:** el del lápiz y la goma; uno con la pregunta primero; uno de tiempo con «al principio»; un rectángulo
con el perímetro; dos consecutivos.

## RESULTADO (8 oct 2026)

**Hecho. `test_U3` 51/51; mis_pruebas 248/248; casos 843/843 (834 + 9 nuevos); proyecto 3252/3252 afirmaciones +
834/834 casos (en cuartos), VERDE.** Falta la prueba de Carlos.

**Lo que se construyó.**
- `conocimiento/frases.kn` (el VOCABULARIO, ~30 clases de palabras): valor (y su pasado = al principio; «quedan» = al
  final), suman, se diferencian, cambio (+/− ; «de alguien», «le», «de algo»), DAR («le da 2 a Luis»: un traspaso),
  comprar, pagar con, la vuelta, repartir, agrupar, juntos, más/menos y los adjetivos que dan la vuelta («más barato»),
  los multiplicadores, los denominadores con palabra, las operaciones y funciones de STUDENT, cada, «la edad de»
  (= la persona), los momentos EN ORDEN (la tarde antes que la noche), las preguntas, «algunos», «un número», «uno / el
  otro», las unidades y lo que puede ser negativo. Una frase, un sentido: si una palabra sale en dos clases, se avisa.
- `conocimiento/relaciones.kn` (las ESTRUCTURAS, con fórmulas que lee el lector de U.1): parte-todo, cambio (gana /
  pierde), comparar sumando, comparar multiplicando, grupos iguales, la vuelta; las figuras (rectángulo, cuadrado,
  triángulo equilátero, caja, cubo; con sus otros nombres y cuál es cuadrada o cúbica); «consecutivos» y «pares
  consecutivos».
- La parte `sistema/partes/palabras.py` (prefijo `_pa_`): preparar (tildes, números con palabras con la secuencia,
  «menos 2» = −2, «dos tercios» = 2/3), partir en frases y en frases NÚCLEO (la elipsis), la PREGUNTA como una frase más
  con «?» (con «si…» detrás), SUJETO-VERBO-OBJETO → relaciones (valor, suma de varios, comparar, la medida de una
  figura, existir/contar, cambios en el tiempo con sus versiones, traspasos, compras y vuelta, repartir y agrupar,
  ritmos «cada semana», partes de un todo, las expresiones de STUDENT), integrar (las mismas palabras = la misma
  cantidad, el último que se nombró, la persona, las versiones en el tiempo, lo que se SABE de relaciones.kn), el
  MODELO para U.2 (solo lo conectado con la pregunta, sin «callejones»), las UNIDADES (cuadradas y cúbicas), y lo
  RAZONABLE (capa 4 del plan: nada negativo donde no puede haberlo; una cuenta de cosas es entera).
- `universal.py`: `decidir_resolver` usa el lector de palabras cuando hay palabras; la respuesta es lo que se pide, con su
  unidad; la explicación empieza con «LEO frase a frase» (cada frase con sus relaciones, lo que sobra, lo que no se
  entiende, lo que se sabe, EN EL TIEMPO).
- Las puertas: la red de seguridad de las palabras (`_pa_le_toca`) en las dos cadenas: si la puerta vieja no llega (no
  entiendo / todavía no / no sé resolverlo) y el lector de palabras lo resuelve y lo comprueba, contesta él.

**Lo que salió al probar (y se arregló, siempre de forma general).**
- Un FALLO GRAVE: «Ana le da 2 a Luis. ¿Cuántos tiene Luis?» decía 4 (leía «da» como «es igual a», y la frase quedaba
  desconectada de la pregunta). Ahora «dar a alguien» es un TRASPASO (dos cambios) y «da» solo es «=» cuando no da
  nadie (STUDENT). Contestar algo falso con seguridad es el peor fallo (METODO §8).
- Una frase que no se entiende y trae un NÚMERO («Adquiere 4») se ignoraba y la respuesta salía mal: ahora no se adivina.
- «cajas» (cuántas) y «caja» (lo de cada una) se confundían: son dos cantidades distintas.
- El perímetro estorbaba al buscar el lado por el área (y tardaba 4 s): una relación con una cantidad que no sale en
  ninguna otra y no se pide es un CALLEJÓN: sobra.
- «baja» detrás de «más» es un adjetivo («más baja que»), no el verbo; «mayor que» es comparar sumando.
- La unidad: «el doble de dinero» y «6 pesos más»: gana la unidad de verdad (pesos); «y Luis tiene 4» hereda caramelos.
- La auditoría sin calculadora cazó siete sitios (índices y textos con `+`): se reescribieron sin cuentas.

**Lo que cambia de respuesta** (solo lo que antes era «no entiendo» de una puerta vieja y ahora se resuelve y comprueba):
el lápiz y la goma (4 pesos), y en general cualquier problema que R.1/R.2/la escala no leían y el lector nuevo sí.
Nada de la batería vieja ni de `mis_casos` cambió.

**Los límites que quedan (honestos).**
- La división con RESTO de R.2 («cuántos sobran», «cuántos coches hacen falta», «cuántos puede comprar») no es todavía
  vocabulario del modelo (el modelo tiene igualdades, no «lo que sobra» ni redondear): ahí el lector nuevo dice «no es
  razonable» y contesta R.2 como siempre.
- Las frases tienen que ser de las formas de la gramática (sujeto, verbo, dato; la elipsis; la pregunta): un texto
  largo con subordinadas, pronombres lejanos o dos preguntas no se lee.
- «Lucía lee 12 páginas el lunes y el martes lee el doble» (verbos de hacer con momentos) no se lee todavía: «lee» no
  es vocabulario y los momentos solo sirven con el mismo sujeto y un valor.
- Un resultado con fracción se da en fracción (`15/2 cm`), sin pasarlo a decimal.
- Las puertas viejas siguen DELANTE: juntar las puertas es U.4.
