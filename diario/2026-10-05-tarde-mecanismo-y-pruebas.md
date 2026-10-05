# 5 oct 2026 (tarde) — el cálculo mecánico de verdad, las pruebas optimizadas y los 11 tipos de CGI

**Quién:** Claude. Desde hoy el proyecto lo lleva Claude con Carlos (el agente anterior ya no).

## 1. El cálculo era mecánico solo de palabra
Revisando cómo calcula para explicárselo a Carlos: los dedos (7.1) **contaban la historia** paso a
paso, pero el total salía de `va + vb` en Python, y la comprobación era `total - vb == va`: una
calculadora comprobándose a sí misma. Lo mismo en 7.2, 7.4, las columnas, 6.5, 6.7…

**Arreglado** con `sistema/partes/mecanismo.py`: la máquina solo sabe **recitar** (siguiente /
anterior en la lista cero…mil), **levantar dedos con nombre** (diez) y **leer/escribir cifras**.
Todo lo demás se construye con eso. Las 57.409 pruebas de entonces siguieron en verde **sin tocar
ninguna**. Comprobado además el rango entero de la 7.6: **1.003.002 sumas y restas, 0 fallos**
(21.240 a través de un cero).

## 2. Pruebas optimizadas (petición de Carlos)
- **Una prueba = una afirmación**: 57.409 «pruebas» eran en realidad ~1.500 afirmaciones
  (la 7.3 sola contaba 43.387 porque contaba cada caso).
- **Modo rápido** (por defecto): fronteras + muestra fija. **`--hierro`**: el rango entero.
- El runner corre todo en un proceso, enseña una línea por archivo y **entero** lo que falle.
- `cargar_conocimiento` con caché (se releían 68 archivos del disco en cada llamada) y
  `entidades_reales` sin recorrido cuadrático.
- 29 casos repetidos quitados de `mis_casos.txt`.
- **83 s → 10 s.** 1.500/1.500 afirmaciones + 374/374 casos.

## 3. Los 11 tipos de problema de CGI
R.1 resolvía 9 de los 11 tipos de Carpenter et al. Faltaban los de **cambio desconocido**
(«Ana tiene 5. Le dan algunas. Ahora tiene 8. ¿Cuántas le dieron?»). Añadidos, resueltos
**contando desde el antes hasta el después** (la estrategia que usan los niños para este tipo).

## 4. Fuentes
- Problem types (CGI): Saddle Up for 2nd Grade, *Understanding Word Problem Types*.
- Schema-based instruction (change / group / compare; FOPS): Hughes & Cuevas 2020, *Georgia
  Educational Researcher* (ERIC EJ1262620), que cita Jitendra et al. 1998 y Fuchs et al. 2006.
- Progresión de estrategias (count all → count on → derived facts → recall): McGraw-Hill, *Summary
  of Research* (cita Carpenter et al. 1993, NRC 2001, Steinberg 1985, Baroody 2006).
- Pólya: *How to Solve It* (comprender, planificar, ejecutar, revisar).
