# Euclides

**Un sistema determinista que aprende matemáticas de primaria como un niño, curso a curso, sin calculadora.**

Euclides no usa redes neuronales ni la aritmética de Python para resolver: cada cuenta la hace con
procedimientos mecánicos que un alumno haría a mano (contar, las tablas, la suma en columnas, la
división larga…), y cada respuesta se **comprueba deshaciendo el camino** antes de darla. Si no puede
comprobarla, no la da.

> *English summary:* Euclides is a deterministic, rule-based system that learns primary-school
> mathematics step by step, following the UK NCETM curriculum (Year 1 to Year 6). It computes without
> using the host language's arithmetic, verifies every answer by working backwards, and prefers saying
> "not yet" over giving a wrong answer. It is an experiment, now paused; see "Estado" below.

## Qué hace

- **Sigue el temario de NCETM** (Inglaterra), segmento a segmento, de 1.º a 6.º de primaria: números,
  las cuatro operaciones, fracciones, decimales, medidas, área y perímetro, razón y proporción, la media,
  ecuaciones sencillas con letras.
- **Sin calculadora:** los números se manejan como cifras y palabras; una prueba
  (`pruebas/test_sin_calculadora.py`) vigila que el motor no use la aritmética de Python con los
  números del problema.
- **Varias técnicas para lo mismo, elegidas por su costo** (por ejemplo `399 x 6 = 400 x 6 - 6`
  antes que la multiplicación en columnas), como piezas en `conocimiento/piezas/`.
- **Un resolvedor general** (`sistema/partes/universal.py`): lee una expresión o un sistema de
  ecuaciones con símbolos, lo pasa a un modelo común (cantidades, relaciones, lo que se pide) y lo
  resuelve despejando, sustituyendo y, si hace falta, probando valores en orden con un tope.
- **Prudencia:** responde «todavía no», «no entiendo» o «no se puede» antes que algo falso. Las fallas
  conocidas están apuntadas en `CLAUDE.md` («Deudas de prudencia»).
- **Explica lo que hace:** qué métodos probó, cuál eligió y por qué, y cómo lo comprobó.

## Cómo probarlo

Necesita Python 3 (solo la biblioteca estándar).

```
python probar.py                      # modo interactivo: escribe una pregunta
python probar.py "resolver: 2 : 5 = 6 : r"
python probar.py --casos              # los casos de mis_casos.txt
python pruebas/correr_todas.py        # toda la batería de pruebas
```

En Windows: doble clic en `PROBAR.bat` o en `PRUEBAS_DEL_PROYECTO.bat`.

Algunos ejemplos:

```
399 x 6                                  -> 2394   (redondea un factor y quita los grupos de más)
20 - 12 : 4                              -> 17     (y explica el error de hacerlo de izquierda a derecha)
2/3 x 3/4                                -> 1/2
4.5 x 1000                               -> 4500   (las cifras suben tres sitios)
resolver: (x - 1) : 2 + (x + 1) : 4 = 5  -> x = 7
resolver: a + b = 7; 2 x a - b = 5       -> a = 4, b = 3
resolver: m = (98 + 102 + 100 + 104) : 4 -> m = 101 (nivelando, como la media de 6.º)
```

## Cómo está organizado

| Carpeta / archivo | Qué hay |
|---|---|
| `sistema/` | el motor (`motor.py` y sus partes en `sistema/partes/`) |
| `conocimiento/` | lo que sabe, como datos: hechos, relaciones (`*.kn`) y las piezas (técnicas) |
| `pruebas/` | cien archivos de pruebas, uno por paso del temario |
| `diario/` | el diario de cada paso: el plan (escrito antes de programar), las fuentes y el resultado |
| `METODO.md`, `PLAN.md`, `PROGRESO.md`, `FUENTES.md` | el método de trabajo, el orden del temario, lo hecho y las fuentes pedagógicas |
| `CLAUDE.md` | las instrucciones y lecciones para las sesiones de trabajo con IA |
| `probar.py` | el probador para usarlo sin tocar código |

## Cómo se construyó

Lo dirigió Carlos Guzmán; el código lo escribieron agentes de IA (Claude) paso a paso, con una regla
fija: primero el plan en el diario a partir de las fuentes (NCETM, Common Core, Pólya…), después el
código, después las pruebas, y una revisión independiente de cada paso antes de unirlo.

## Estado: proyecto en pausa (octubre de 2026)

Llegó hasta 6.º de primaria (NCETM Spine 2 completo y fracciones de 6.º, 3.9). Lo que aprendimos:

- Un sistema de reglas puede resolver bien y de forma verificable lo que está dentro de su temario,
  y explicar cada paso.
- Pero no aporta algo nuevo frente a lo que ya existe (los sistemas de álgebra por computadora, los
  demostradores automáticos): para ir más allá, probar todas las reglas y sus combinaciones se dispara,
  y hay que volver a los procedimientos conocidos.
- La idea de que aprenda solo necesitaría entender el **lenguaje**, no solo los símbolos; ese es el
  reto que habría que resolver primero.

Se publica como experiencia, por si a alguien le sirve.

## Licencia

MIT — ver `LICENSE`.
