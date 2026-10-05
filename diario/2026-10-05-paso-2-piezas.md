# Paso 2 del plan — la base de PIEZAS de conocimiento

**Fecha:** 5 de octubre de 2026 · **Hecho: SÍ** · Idea de Carlos.

> «tengamos una base de datos de códigos, así el motor lo hala y aplica al problema uno a uno y no
> están en el motor principal. Aunque haya que programarle a mano y no sea autodidacta, se le
> programará una sola vez y él lo que deberá es saberlo usar.» (Carlos, 5 oct 2026)

## Cómo quedó

```
conocimiento/piezas/
    _objetivos.py      las PREGUNTAS (paso, sumar, restar, contar_hasta) y cómo se elige
    _condiciones.py    las CONDICIONES de aplicación, escritas una vez para todas
    anadir.py, quitar.py, ... (11)     los pasos de un problema (antes en resolver_r1.kn)
    sumar_haciendo_diez.py, sumar_con_dedos.py, sumar_por_columnas.py
    restar_con_dedos.py, restar_por_columnas.py, contar_desde_hasta.py
sistema/partes/piezas.py   EL MOTOR DE PIEZAS (no sabe matemáticas)
```

Cada pieza: **qué es**, **a qué pregunta responde**, **cuándo sirve** (condiciones con el porqué
del descarte), **qué usa** (otras piezas, otras preguntas o lecciones del currículo) y **cómo se
hace**. El motor: carga, prueba TODAS, descarta con razón, aplica.

- **Un paso de un problema**: se hacen todas las que encajan y tienen que dar lo mismo (si no, ambiguo).
- **Un cálculo**: el **método más corto** que encaja — hacer diez antes que los dedos, los dedos
  antes que las columnas — y se dice cuáles otros también servían. Es la progresión de los niños
  (contar → contar desde → hechos derivados), y ahí entrarán la **memoria** y las **técnicas**
  del paso 3 y 4 como piezas más rápidas.

## Las reglas que lo protegen

1. Una pieza solo puede usar el mecanismo y lo que **declaró** en «usa» (si no, error): el mapa
   del conocimiento (`piezas` en el probador) es verdad.
2. El mapa se comprueba: condiciones que existen, «usa» que existen, sin vueltas.
3. `test_sin_calculadora.py` lee también las piezas, **sin lista blanca**.
4. **Prueba de fuego** (`test_piezas.py` D): se copia la carpeta, se añade una pieza nueva
   («sumar cero») como un archivo, y el motor la usa — también dentro de un paso de problema —
   sin tocar una línea del motor.

## Lo medido
1521/1521 afirmaciones + 375/375 casos, verde. 17 piezas.

## Lo que queda para más adelante
Las lecciones 0.1–7.6 (contar, comparar, partir...) siguen siendo funciones del motor; las piezas
de cálculo las usan como «lecciones del currículo» (`u.leccion("7.1")`). Pasarán a piezas cuando
haga falta, sin prisa.
