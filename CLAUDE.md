# CLAUDE.md — Euclides (instrucciones para cualquier sesión de Claude, también en la nube)

**Idioma: español con Carlos.** El rumbo lo decide Carlos; la técnica pequeña, Claude.

## Al empezar, leer (en este orden)
1. `METODO.md` — el método y las reglas que no se rompen (sobre todo: SIN CALCULADORA).
2. `PLAN.md`, sección «AÑOS ESCOLARES» — el orden de los pasos (NCETM por Year + Common Core).
3. `PROGRESO.md` (las últimas filas) y el último archivo de `diario/` — dónde se quedó.
4. `FUENTES.md` — las fuentes pedagógicas ya leídas.

## Cómo se trabaja (Carlos)
- **Velocidad pedagógica, un paso cada vez.** Para cada paso:
  1. Investigar la pedagogía (NCETM primero: https://ncetm.org.uk/classroom-resources/primm-... ;
     Common Core) y **escribir el plan en `diario/AAAA-MM-DD-paso-XX-nombre.md`** ANTES de programar:
     lo que dice la fuente, cómo lo haría un humano sin calculadora, lo que se construye, las trampas,
     la prueba de dominio.
  2. Construir. 3. Probar (prueba de dominio contra un testigo + la batería entera en verde).
  4. Cerrar: resultado en el diario, fila en `PLAN.md` y `PROGRESO.md`, fuente en `FUENTES.md`,
     ayuda en `probar.py`, casos en `mis_casos.txt` y `mis_pruebas.txt`,
     `python3 herramientas/empaquetar_movil.py`, commit.
- «Ajusta el plan a lo que la pedagogía dicta.» «Cada cosa, una a una.» Sin repaso mezclado.
- **«Debe trabajar como lo haría un humano sin calculadora.»** Las cuentas las hace el mecanismo y
  las piezas; Python es solo el TESTIGO en las pruebas.
- Carlos prueba en su PC con `MIS_PRUEBAS.bat` / `PROBAR.bat`. Lo que él no ha probado se marca
  «falta la prueba de Carlos».

## Convenciones técnicas (para no romper nada)
- El motor está partido en `sistema/partes/*.py`, unidos por el orden de `sistema/partes/__init__.py`.
  **Un nombre solo puede definirse en UNA parte** (guardia «dos verdades»): las funciones privadas
  nuevas llevan prefijo propio (`_fr_`, `_dec_`, `_neg_`…). Una parte nueva se añade a ese orden.
- Las piezas (métodos) viven en `conocimiento/piezas/*.py` (`PIEZA` + `hacer(s, u)`); sus
  condiciones en `_condiciones.py`, las preguntas en `_objetivos.py`. Una pieza no puede `usar` su
  propia pregunta. Si `vuelta_ok` es False, su respuesta no vale.
- Auditoría sin calculadora (`pruebas/test_sin_calculadora.py`): nada de `a + b`, `a * b`… con
  variables en el motor. Usar `aplicar("sumar", ...)`, `siguiente`, `viene_despues`, formato de texto
  (`"%s%s" %`), `.extend`, `rjust`, `range(k, 0, -1)`.
- Dos techos: contar OBJETOS hasta diez mil (`techo_de_contar`); los NÚMEROS hasta diez millones desde N.6
  (`numero_maximo`: el techo más alto de `conocimiento/el_millon.kn` y `los_millones.kn`).
- Las órdenes se enrutan en `sistema/partes/explicacion.py` (`explicar_pregunta`) y en
  `probar.py` (`preguntar`); el orden de las comprobaciones importa.
- Cada archivo de prueba imprime `TOTAL: x/y`, usa memoria temporal (`EUCLIDES_MEMORIA`).

## Comandos
- Batería entera: `python3 pruebas/correr_todas.py` (≈1 min; debe salir todo en verde).
  Si el entorno corta los comandos largos (≈3 min), se corre en dos mitades seguidas:
  `python3 pruebas/correr_todas.py --parte 1/2` y luego `--parte 2/2` (los casos van en la última).
- Casos de Carlos: `python3 probar.py --archivo mis_pruebas.txt`;  casos: `python3 probar.py --casos`.
- Una pregunta: `python3 probar.py "recta: 3 - 8"`.

## Git
- Trabajar en una rama y empujarla; **no tocar `main`** sin que Carlos lo diga (él la baja a su PC y prueba).
- Al final de cada mensaje de commit:
  `Co-Authored-By: Claude <noreply@anthropic.com>`

## Lecciones de las revisiones (las añade la sesión que revisa; leerlas antes de construir)
- **Una pieza nueva debe COMPROBARSE a sí misma** (`vuelta` real con la operación contraria y
  `vuelta_ok` según salga), no devolver `"vuelta": "", "vuelta_ok": True` sin comprobar nada.
  (Revisión de M.12: las piezas `*_escalando` no lo hacen; queda pendiente.)
- **Probar cerca del techo** (999 999, 1 000 000, productos que se pasan): una condición que llama a
  `decir`/`viene_despues` con un número sin nombre lanzaba KeyError (ya lo atrapa `aplicar`).
- **Nada de contar de uno en uno con números grandes**: un salto grande es una SUMA, no 243 225 pasos.
  Medir el tiempo de casos grandes; si una pregunta tarda más de 2-3 s, algo no es humano.
- **Respetar el año**: dividir entre números de dos cifras con muchos saltos es la división larga
  (6.º, NCETM 2.24); hasta entonces, «todavía no».
- **Comparar tamaños con el mecanismo** (`viene_despues(decir(a), decir(b), saber)`, o `u.viene_despues`
  en las piezas), no con `<`/`>` de Python, en el código NUEVO. (Revisión de M.15: `factores.py` y
  `parejas_de_factores_en_orden.py` ya corregidos.) **DEUDA conocida:** el código viejo tiene ~90
  comparaciones con Python (muchas son legítimas: índices, sangrías, leer archivos; otras miran el tamaño
  de números, p. ej. `primitivas.py`, `nivel_5.py`, `nivel_6.py`). La auditoría aún no las vigila.
  Pasarlas al mecanismo y ampliar `test_sin_calculadora.py` con su lista blanca será un paso aparte.
- **Pendientes de la revisión de M.14:** `99 x 99 x 99` dice «todavía no» aunque calcula 970299 (porque
  no puede comprobarlo dividiendo): podría comprobarlo multiplicando en otro orden. `101 x 100 x 100`
  dice «todavía no» cuando debería decir que se pasa del millón.
- **IDEA PARA EL FUTURO (no hacer sin que Carlos lo pida; 7 oct):** elegir la técnica según lo que CUESTA
  en este caso, como un humano de un vistazo. Hoy cada pieza tiene una `rapidez` fija y, para que no haga
  cosas inhumanas con números grandes, se han ido poniendo topes sueltos (grupos iguales ≤ 12, saltos ≤ 100
  o ≤ 1000, contar...). La idea: que cada pieza estime cuántos pasos le costaría ESTE caso y se elija la más
  barata entre las aprendidas; una regla general («nadie repite algo cientos de veces si sabe otra manera»)
  en lugar de los topes. Carlos (7 oct): «en el futuro vemos si es necesario; si no, no».

## Dónde se quedó (8 oct 2026)
Hecho hasta **S.3 problemas con dos incógnitas** (NCETM 1.31, Year 6): `a + b = 30; a - b = 8` con la barra (quitar la
diferencia y repartir en dos), suma y múltiplo (3 + 1 = 4 trozos), diferencia y múltiplo, probar en orden (tope de 30 pruebas
en `conocimiento/dos_incognitas.kn`), una suma sola (una pareja más que la suma), una relación sola (infinitas); y R.1 con
«entre los dos» + «más que». Parte `dos_incognitas.py`; preguntas `dos_incognitas` y `cumplen_las_ecuaciones`.
Antes: N.6 hasta diez millones (NCETM 1.30): el techo de los NÚMEROS es **diez millones** (`numero_maximo`, de
`conocimiento/los_millones.kn`); contar objetos sigue en diez mil. F.7, F.6, P.7.
Siguiente: mirar en el índice de NCETM lo que sigue en Year 6 de Spine 1 (tras 1.31), lo que queda de Year 5 (Spine 2:
**2.23**, cuyo título no se pudo ver desde la nube; Spine 3 tras 3.8). (La división combinada con + y - es 2.28, de 6.º;
la división larga, 2.24.)
La balanza y `verdad:` con decimales: todavía no (solo enteros). Las fracciones de partida en `comparar:` y en las cuentas
siguen limitadas a medios…doceavos, décimos, centésimos y milésimos (el de abajo común puede ser cualquiera hasta el techo).
`comparar:` por el mismo de arriba no sale si pide dividir entre dos cifras (la división larga, 6.º); el del mismo de abajo sí.
