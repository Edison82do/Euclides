# PLAN U — VOLVER UNIVERSAL LO QUE YA SABE EUCLIDES — 8 oct 2026

**Decisión de Carlos (8 oct):** se PAUSA el avance por años escolares (la siguiente era NCETM 2.23). Antes de
seguir añadiendo cosas, se hace universal lo que ya hay: que ante un problema que NINGÚN paso preparó, el sistema
lo aborde como nuevo y aplique TODO lo que sabe, combinándolo con restricciones, hasta llegar solo a la solución.
«No quiero memorización de soluciones de problemas conocidos, porque cuando encuentre uno desconocido se
paralizará.» Se acepta que un método universal tarde más. Pruebas: pocas y representativas (no una batería grande
para lo nuevo); la batería vieja tiene que seguir en verde.

## 1. EL DIAGNÓSTICO (revisión del código, 8 oct)

**Lo que ya es universal:** las TÉCNICAS. 124 piezas para 30 preguntas (sumar 13, multiplicar 15, restar 11,
dividir 8...), cada una con sus condiciones; el motor prueba las que encajan; casi todas se comprueban solas
(la vuelta). Y hay un resolvedor de ecuaciones de verdad: `letra._deshacer` (deshace las operaciones de fuera
hacia dentro para una incógnita, y comprueba sustituyendo).

**Lo que NO es universal: la ENTRADA y la REPRESENTACIÓN.**
- Unas **33 puertas** de entrada, cada una con su formato (`volumen:`, `partes: …; todo: ?`, `recta:`,
  `equivalente:`, `a + b = 30; a - b = 8`, frases de temperatura...), revisadas en cadena en DOS sitios casi
  iguales (`explicacion.explicar_pregunta` y `probar.preguntar`): si una frase no encaja en ninguna, «no entiendo»
  aunque tenga todas las técnicas para resolverlo; y a veces entra por la puerta equivocada
  (`a + b = 1/2; a - b = 1/4` acaba en la unidad 0.2, «objetos sin atributo común»).
- **No hay una representación común:** cada parte guarda el problema a su manera (`{"a","b"}`, `{"total","divisor"}`,
  el árbol de `letra`, los términos de `combinar`, las ecuaciones de `dos_incognitas` como textos, el `todo/partes`
  de `parte_todo`, las situaciones de `resolver`...). Cuatro o cinco lectores de expresiones que se solapan.
- **Los números no se mezclan:** enteros, decimales, fracciones y negativos viven en partes distintas; una cuenta
  que mezcla dos tipos (`1/2 + 0.25`) no tiene camino.
- **Los problemas con palabras** se leen con plantillas de frase entera (R.1, R.2) y con expresiones regulares
  sueltas en cada parte (escala, negativos, dinero): una frase dicha de otra manera no entra.

Prueba hecha el 8 oct: «Un lápiz y una goma cuestan 12 pesos. El lápiz cuesta el doble que la goma. ¿Cuánto
cuesta la goma?» → `no_entiendo`, aunque es exactamente el problema de suma y múltiplo que sabe resolver (S.3).

## 2. LO QUE DICE LA INVESTIGACIÓN (fuentes en FUENTES.md)

- **Cómo lo hace una persona** (Mayer 1992; Passolunghi y otros 1996; Kintsch y Greeno): 1) **traducir** cada
  frase, 2) **integrar** todo en un modelo de la situación, 3) **planear**, 4) **ejecutar** y 5) **comprobar** si
  es razonable. El modelo de la situación es el corazón: lo que se sabe, lo que falta y cómo se relacionan.
- **Los esquemas son estructuras, no recetas** (Riley, Greeno y Heller 1983: cambio, combinación, comparación;
  NCETM 1.28: «la misma estructura en contextos distintos»; NCETM 1.31: el dibujo de barras). Un esquema no es la
  solución memorizada de una familia: es una RELACIÓN entre cantidades (parte + parte = todo; grande = K × pequeño;
  grande − pequeño = diferencia). Saber relaciones generales es lo contrario de memorizar problemas.
- **Leer con robustez** (Bakman 2007, sobre los esquemas de Riley-Greeno-Heller): la respuesta no debe cambiar si
  se reordenan las frases o se añade información que sobra; cada frase se convierte en PROPOSICIONES pequeñas
  (cantidades y relaciones), y los esquemas se rellenan con lo que haya, venga de donde venga.
- **STUDENT** (Bobrow 1964): partir el enunciado en frases núcleo, cada una con un solo dato, y convertir cada una
  en una ecuación; luego resolver el sistema. Su debilidad: las reglas de lenguaje escritas a mano (aquí será igual:
  el vocabulario irá en datos, `.kn`, para que crezca sin tocar código).
- **Sin plantillas fijas** (Roy y Roth 2015): la estructura de la solución se ARMA componiendo relaciones (árboles de
  expresiones), no se elige de un catálogo de plantillas.
- **Análisis de medios y fines** (Newell y Simon, GPS): comparar lo que se tiene con lo que se busca y aplicar el
  operador que reduce la diferencia; cada paso abre submetas. **Pólya**: trabajar hacia atrás, buscar un problema
  auxiliar, simplificar.
- **Schoenfeld (1979):** saber las técnicas no basta; hace falta el CONTROL: saber CUÁNDO usar cada una y vigilar si
  se avanza. → El buscador necesita reglas de elección y un presupuesto, no probarlo todo con todo.

## 3. LA IDEA: CUATRO CAPAS

```
  texto ──► [1 TRADUCIR] ──► MODELO DEL PROBLEMA ──► [3 RESOLVER: buscar] ──► respuesta ──► [4 COMPROBAR]
             (lectores)      (cantidades, relaciones,   (operadores = lo que ya sabe,
                              lo que se busca)            elegidos por medios y fines)
```

**Capa 2 — EL MODELO DEL PROBLEMA (la representación común).** Todo problema, venga como venga, se traduce a:
- **cantidades**: cada una con nombre (`a`, `goma`, `lapiz`, `?`), valor conocido o desconocido, y su cosa/unidad
  (pesos, cm, grados...) si la hay;
- **relaciones**: igualdades entre expresiones con + − × : y paréntesis (`lapiz + goma = 12`, `lapiz = 2 x goma`,
  `todo = parte1 + parte2 + parte3`, `volumen = largo x ancho x alto`);
- **lo que se pide**: una o varias cantidades, o «¿es verdad?», o «¿cuál es mayor?».
- **los números** de un solo tipo para el sistema: un NÚMERO que puede ser entero, decimal, fracción o negativo; al
  operar, se manda a la pieza de su tipo (las que ya existen) y, si los tipos se mezclan, se pasa a uno común como
  haría un niño (0.25 = 1/4; 1/2 = 0.5) con lo que ya sabe (D.1/D.2, F.6, F.7, N.5).
- Las relaciones de los esquemas (parte-todo, cambio, comparación aditiva, comparación multiplicativa, grupos
  iguales, área, volumen, perímetro, precio) se escriben UNA vez, como datos, en `conocimiento/relaciones.kn`:
  son el «vocabulario de estructuras», no soluciones.

**Capa 1 — TRADUCIR (una sola puerta, varios lectores).**
- **El lector simbólico, uno solo**: amplía el de `letra` (que ya tiene paréntesis y el orden de las operaciones)
  para varias letras, varias ecuaciones separadas por `;`, fracciones, decimales y negativos. Sustituye, poco a poco,
  a los cuatro o cinco lectores que se solapan.
- **El lector de palabras**: frase → proposiciones pequeñas (como STUDENT y Bakman), con un VOCABULARIO de
  relaciones en datos (`conocimiento/frases.kn`): «entre los dos», «en total», «juntos» → suma; «más que»,
  «menos que» → diferencia; «el doble», «el triple», «K veces» → múltiplo; «la mitad», «un tercio de» → fracción;
  «cada», «grupos de» → producto; «sube», «baja», «gana», «pierde», «gasta» → cambio; «cuestan», «mide», «tiene»
  → valor. Lo que una frase no deja leer se dice, pero NO bloquea si con el resto basta.
- **Las puertas viejas siguen** (no se rompe nada), pero se van convirtiendo en traductores al modelo cuando su
  respuesta sea la misma. Y se juntan las dos cadenas duplicadas en UNA tabla de puertas.
- Lo que no entra por ninguna puerta vieja va al lector general antes de decir «no entiendo».

**Capa 3 — RESOLVER (buscar con lo que sabe; medios y fines, con control).** Estado = el modelo. Operadores:
1. **Calcular**: una relación en la que solo falta UNA cantidad → se despeja deshaciendo (`letra._deshacer`) y se
   calcula con las piezas de siempre. (Es «trabajar hacia atrás» de Pólya y la propagación de restricciones.)
2. **Sustituir**: una cantidad que ya se sabe, o que se expresa con otra (`lapiz = 2 x goma`), se mete en las demás
   relaciones → baja el número de incógnitas (el dibujo de barras: `2 x goma + goma = 12` → 3 trozos = 12).
3. **Juntar relaciones**: sumar o restar dos igualdades (la suma y la diferencia de S.3: quitar la diferencia).
4. **Reescribir con equivalencias** (lo de M.12, P.7, F.6...: agrupar, sacar factor común, simplificar) cuando
   deja una relación con una sola incógnita.
5. **Probar en orden** (S.3), con tope humano, cuando nada de lo anterior baja las incógnitas.
- **El control** (Schoenfeld): en cada paso se elige el operador que MÁS acerca a lo que se pide (menos incógnitas
  en el camino hacia la meta; primero lo barato); hay un presupuesto de pasos («un humano no da cien vueltas»);
  si se agota, «todavía no», diciendo hasta dónde llegó. Cada operador es una PIEZA más (con condiciones y
  «usa»), así que entra en el mismo motor y en el mapa.
- Se explica como un alumno: «la goma es 1 trozo, el lápiz 2 trozos; 3 trozos son 12; 1 trozo = 4».

**Capa 4 — COMPROBAR.** Al final, los valores se ponen en TODAS las relaciones del enunciado original (no en las
transformadas) y se mira si es razonable (E.6: el tamaño; nada negativo donde no puede haberlo). Si no cuadra, no
se da la respuesta.

## 4. LAS FASES (una sesión de la nube por fase; Claude revisa cada una antes de unirla)

- **U.1 — El modelo y el lector simbólico.** El NÚMERO común (los cuatro tipos y el paso de uno a otro), el lector
  único de expresiones y ecuaciones (varias letras, `;`, fracciones, decimales, negativos), los operadores 1 y 2
  (calcular despejando y sustituir) y la comprobación. Puerta nueva `resolver:` + red de seguridad al final de la
  cadena. Ejemplos que deben salir: `a + b = 1/2; a - b = 1/4`, `3 x n = 4.5`, `(a + 5) x 2 = 26`,
  `x + y + z = 40; x = y; z = 2 x y`, `1/2 + 0.25`, `-3 + 2 x 4`.
- **U.2 — Buscar con control.** Operadores 3, 4 y 5, el presupuesto, la elección por medios y fines, y la
  explicación paso a paso (barras). `dos_incognitas` y `parte_todo` pasan a ser traductores al modelo (si sus
  respuestas no cambian).
- **U.3 — El lector de palabras.** Frases → proposiciones con `frases.kn` y `relaciones.kn`; información que sobra;
  frases en cualquier orden. R.1, R.2, escala, temperatura, dinero, volumen, perímetro: sus frases pasan a ser
  vocabulario en datos.
- **U.4 — Una sola tabla de puertas.** Se juntan `explicar_pregunta` y `preguntar`; las puertas viejas que ya
  equivalen al modelo se convierten en traductores; nada de lo viejo cambia de respuesta.
- **U.5 — El examen de transferencia.** Problemas que NINGÚN paso preparó, mezclando temas. Claude guarda un examen
  SECRETO (fuera del repositorio, para no «enseñar para el examen») y lo pasa en cada revisión; el resultado se
  apunta en el diario. Lo que falle dice qué falta (vocabulario, un operador, el control), nunca se arregla con una
  receta para ese problema.

## 5. LAS REGLAS DE ESTE PLAN

- **Prohibido memorizar problemas**: nada de reconocer una familia de enunciados y tener su solución escrita. Solo
  relaciones generales (datos), operadores generales (piezas) y búsqueda. Si un problema del examen falla, se
  arregla la capa que falló, de forma general.
- **Nada viejo cambia de respuesta** (la batería vieja en verde); lo nuevo, con pocas pruebas representativas
  (decisión de Carlos), más el examen de transferencia.
- **Sin calculadora**, como siempre: las cuentas las siguen haciendo las piezas; el buscador solo decide QUÉ cuenta
  hacer. Comparar tamaños con el mecanismo.
- Puede tardar más (aceptado por Carlos), pero con presupuesto: si se agota, «todavía no» y hasta dónde llegó.
- Al acabar el plan U se vuelve al orden de NCETM (2.23), y cada paso nuevo entrará ya por el modelo.
