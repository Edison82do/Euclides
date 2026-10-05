# MÉTODO DE EUCLIDES

**Desde el 5 de octubre de 2026 el proyecto lo lleva Claude con Carlos** (el agente anterior,
Euclides/Hermes, ya no trabaja aquí). Este archivo es el método: se lee al empezar cada sesión,
junto con `PLAN.md` y `PROGRESO.md`, y se actualiza cuando algo del método cambia.

## 1. Qué es el proyecto

Un sistema **determinista** que aprende matemáticas como un niño, unidad a unidad, y que tiene que
**resolver problemas aplicando lo que sabe**:

> «si le doy algún problema no es que él sepa qué hacer, el asunto sería que él sepa utilizar o
> aplicar lo que sabe, le aplique todo y combinaciones de lo que sabe al problema, pero con
> descarte para solo aplicar las cosas que tienen sentido aplicar.» (Carlos, 3 oct 2026)

La pregunta de fondo: **cuánto razonamiento sale de un sistema pequeño si el conocimiento está
estructurado, conectado y se acumula**, sin probabilidad y sin datos masivos.

## 2. Las reglas que no se rompen

1. **Español con Carlos.** El rumbo lo decide Carlos; la técnica pequeña, Claude.
2. **Nada sin respaldo escrito**: cada conocimiento se declara FIJADO, DEMOSTRADO o VERIFICADO.
3. **No se dice «funciona» sin pruebas en verde**, y se enseña la salida.
4. **No se adivina el lenguaje**: si una frase no encaja, el sistema dice NO ENTIENDO.
5. **Se domina lo simple antes de lo siguiente**: una unidad no se cierra sin su prueba de dominio
   en casos no programados.
6. **Las decisiones van en archivos de datos** (`conocimiento/*.kn`), no dispersas por el código.
7. **Nada de cajas negras**: toda respuesta se rastrea a una regla escrita y a un dato escrito.
8. **SIN CALCULADORA** (decisión de Carlos, 4 oct: «mecánicamente hasta nuevo aviso»). Ver §4.
   **Matiz del 5 oct (Carlos):** «en el camino el ser humano memoriza algunos datos y utiliza técnicas
   para agilizar la solución; eso es válido aquí, según va avanzando el aprendizaje». O sea: se
   permite MEMORIA y TÉCNICAS, pero **ganadas**: un hecho solo se memoriza después de haberlo
   calculado con el mecanismo y verificado (y guarda de dónde salió); una técnica es un
   conocimiento más, con sus condiciones de aplicación. Nunca una tabla escrita a mano.
9. **Pedagogía investigada antes de cada avance**, con la fuente citada. Ver §5.
10. **Todo paso a paso**: unidades pequeñas, cada una con su prueba, su diario y su guía.

## 3. Cómo está hecho

```
sistema/motor.py          la fachada (import motor da acceso a todo)
sistema/partes/           el código, una pieza por nivel:
    nucleo, primitivas, MECANISMO, decision, nivel_2 ... nivel_7, explicacion, resolver
conocimiento/*.kn         el saber, en texto (reglas, definiciones, formas de lectura)
conocimiento/piezas/      las PIEZAS: cada conocimiento que se aplica, un archivo (ver §3b)
pruebas/                  test_*.py + _muestras.py + correr_todas.py
mis_casos.txt             los casos de Carlos:  pregunta | lo esperado | comentario
probar.py / PROBAR.bat    el probador (doble clic)
diario/  informes/  investigacion/
```

### 3b. Las piezas (idea de Carlos, 5 oct 2026)
Cada conocimiento que el sistema **aplica** es una pieza en `conocimiento/piezas/`: `PIEZA = {id,
nombre, unidad, responde, que_hace, condiciones, usa, rapidez}` + `def hacer(situacion, u)`.
El motor (`sistema/partes/piezas.py`) no sabe matemáticas: carga, prueba todas, descarta con su
porqué y aplica (un paso: todas iguales; un cálculo: la más rápida que encaja). **Un conocimiento
nuevo = una pieza nueva; el motor no se toca.** Una pieza solo usa el mecanismo y lo que declara
en «usa». Las condiciones se escriben una vez en `_condiciones.py`; las preguntas y su forma de
elegir, en `_objetivos.py`. `piezas` en el probador enseña el mapa.

**Git**: un commit por unidad cerrada (y antes de cualquier cambio grande). `git log --oneline`.

## 4. El mecanismo: cómo calcula sin calculadora (`sistema/partes/mecanismo.py`)

La máquina solo sabe hacer, de verdad, tres cosas de niño pequeño:

1. **Recitar**: dada una palabra de la lista (cero, uno … mil), decir la **siguiente** o la **anterior**.
2. **Levantar dedos**: un dedo con nombre por cada palabra recitada desde «uno»; hay diez.
3. **Leer y escribir cifras**: el valor de una palabra es su **sitio** en la lista; una cifra
   escrita se lee símbolo a símbolo.

Todo lo demás se construye con eso: sumar con los dedos (contar hacia adelante), restar (hacia
atrás), hacer diez, las columnas (cada columna es una cuenta de dedos; «pasa de nueve» = viene
después de «nueve» en la lista; lo que se anota = lo que hay que contar desde «diez»), restar a
través de un cero, juntar decenas, el hueco entre dos números (contar desde el pequeño hasta el
grande). **En el camino de la respuesta no hay ni un `a + b` de Python.** Python solo lee
posiciones, y hace de **testigo externo** en las pruebas.

**Desde el 5 oct (paso 1 del plan) tampoco las condiciones de aplicación usan cuentas de Python**
(«¿el total pasa de mil?» se responde sumando por columnas y mirando si el total tiene palabra en
la lista). Lo vigila `pruebas/test_sin_calculadora.py`: lee el código de todas las piezas y se
pone en rojo si aparece un `a + b` fuera del mecanismo (con una lista blanca, cada sitio con su
porqué: unir textos, leer archivos, dibujar la cuenta). Lo que sí se usa es **comparar** dos
números (`>`, `<`), que es lo de la 4.2: el que viene después en la lista es el mayor.

## 5. El sistema pedagógico (lo que se investigó y cómo se aplica)

| Marco | Qué dice | Dónde está en Euclides |
|---|---|---|
| **Concreto → Pictórico → Abstracto** (Singapur) | primero objetos, luego dibujos, luego símbolos | objetos (niveles 0–2) → marcas/dedos → cifras (3.x, 6.x) |
| **Progresión de estrategias de cálculo** (Carpenter, Fuson; NRC 2001) | contar todo → contar desde el primero → hechos derivados → recuerdo | contar todo (5.2) → los dedos (7.1) → hacer diez (7.2). El recuerdo está **prohibido** por Carlos hasta nuevo aviso |
| **Los 11 tipos de problema de CGI** (Carpenter et al.) | juntar y separar (resultado, cambio o inicio desconocido), parte-parte-todo (todo o parte), comparar (diferencia, mayor o menor) | **R.1 los resuelve los 11** (`test_R_1.py`, sección G) |
| **Instrucción basada en esquemas** (Jitendra, Fuchs) | identificar la estructura: cambio, grupo o comparación; organizar; planificar; resolver | el resolvedor monta la **situación** (quién tiene, qué cambia, qué se compara) antes de elegir nada |
| **Pólya** | comprender, planificar, ejecutar, revisar | leer → situación → probar todo y descartar → calcular → la vuelta |
| **Contra las palabras clave** (NC2ML) | elegir la operación por «más» o «en total» lleva al error | la operación sale de la situación; si «más» resulta ser resta, se avisa |

**Para cada avance**: (1) buscar cómo se enseña ese paso a niños y sus errores típicos, con la
fuente; (2) escribir el conocimiento en `.kn`; (3) programar lo mínimo; (4) prueba con las
trampas de los errores típicos; (5) prueba de dominio con casos no programados; (6) diario, guía,
PROGRESO, commit.

## 6. El lenguaje rústico (decisión de Carlos, 5 oct 2026)

Pasar de lenguaje humano a lenguaje matemático **no es la idea principal del proyecto**. Los
enunciados se escriben en un **lenguaje rústico**: frases cortas de unas pocas formas fijas
(`conocimiento/enunciados.kn`). Lo que importa es la **solución**, no la gramática.

**La regla de oro del lenguaje rústico: describe la SITUACIÓN, nunca la OPERACIÓN.**
«Ana tiene 8. Tiene 3 más que Luis. ¿Cuántas tiene Luis?» es rústico y vale. «Luis = 8 − 3» no
vale: ya trae la operación hecha y no deja al sistema nada que razonar.

Las formas: *X tiene N*, *hay N*, *X gana/compra/le dan N*, *X pierde/regala/se come N*, *llegan N*,
*se van N*, *X tiene N más/menos que Y*, *X e Y tienen N entre los dos*, *X tenía algunos*,
*le dan algunos*, *ahora tiene N*; y las preguntas *¿cuántos tiene X (ahora)?*, *¿cuántos quedan?*,
*¿cuántos tienen entre los dos?*, *¿cuántos más tiene X que Y?*, *¿cuántos tenía al principio?*,
*¿cuántos le dieron / perdió / se fueron?*. Una frase nueva = una forma nueva en el `.kn`.

## 7. Las pruebas

- `python pruebas/correr_todas.py` (o `PRUEBAS_DEL_PROYECTO.bat`) → ~10 s. Las pruebas grandes
  recorren una **muestra**: las **fronteras** (0, 1, 9, 10, 99, 100, 999, 1000, los cambios de
  decena, los ceros intercalados) y unos cuantos **al azar fijo**. Una línea por archivo; la
  salida entera de lo que falle; todo en `pruebas/ultima_salida.txt`.
- **No se prueban todas las combinaciones** (decisión de Carlos, 5 oct 2026): con una buena
  muestra basta. (El rango entero de la 7.6 se comprobó UNA vez, el 5 oct: 1.003.002 cuentas, 0
  fallos; no hace falta repetirlo.)
- **Una prueba = una afirmación.** Una prueba con muestra cuenta como una.
- Cuando una prueba falla hay **tres** posibilidades: el motor está roto, la prueba está obsoleta
  por mejora, o el valor esperado está mal escrito. Antes de tocar el motor, mirar qué hace.
  Una prueba obsoleta se actualiza **caso por caso**, dejando escrito el caso viejo al lado.

## 8. Carné de errores (lo que ya pasó, para no repetirlo)

- **Contestar con seguridad algo falso** es el peor fallo (p. ej. `sumar: 3 / 2` → `1 + 1 = 2`).
  Cuando una entrada admite dos lecturas, se separan los espacios: cantidad / cifra / palabra.
- **Dos verdades**: si algo se decide en dos sitios, se desincroniza. El probador **solo llama**
  a funciones `decidir_*`; nunca calcula por su cuenta (pasó dos veces).
- **Subir un techo no basta con que lo viejo siga en verde**: hay que probar las puertas nuevas.
- **«El método: no hace falta»** fue una caja negra con disfraz. Toda cuenta sale de un método.
- **Un techo se escribe con `len(secuencia)`**, nunca con el número a mano.
- **No se fabrica el dato** que falta: se pide o se dice que falta.
- **Una palabra, un sentido** (pasó con «grupo» y con «uno»).
- **Nunca recortar la salida de una prueba** para darla por buena: el runner enseña entero lo que falla.
- **`silla,silla,silla` es UNA silla**: el nombre es el identificador.
