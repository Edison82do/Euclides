# Paso E.4 — EL HUECO EN × Y ÷ — 5 oct 2026

Carlos probó M.3 («todo muy bien») y pidió ajustar el plan a la pedagogía (ver `PLAN.md`, «EL PLAN
AJUSTADO») y hacer cada cosa una a una. Se empieza E.4.

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (mirando antes `FUENTES.md`).**
- Common Core **3.OA.A.4**: «determinar el número desconocido en una ecuación de multiplicación o
  división con tres números». Ejemplos del estándar: `8 × ? = 48`, `5 = _ ÷ 3`, `6 × 6 = ?`.
- Common Core **3.OA.B.6**: «entender la división como un problema de **factor desconocido**»:
  32 ÷ 8 es el número que por 8 da 32. Es la relación que ya usa la comprobación de M.3.
- **NCETM 2.6**: las dos estructuras de la división. El sitio del hueco dice cuál es:
  | ecuación | qué se busca | cómo se halla |
  |---|---|---|
  | `3 x 4 = ?` | el producto | multiplicar (M.1/M.2) |
  | `3 x ? = 12` | cuántos en cada grupo (3 grupos de ?) | **repartir** 12 entre 3 |
  | `? x 4 = 12` | cuántos grupos (? grupos de 4) | **agrupar** 12 en grupos de 4 |
  | `12 : 3 = ?` | el cociente | dividir (M.3) |
  | `12 : ? = 4` | el divisor (¿entre cuántos, para que toquen 4?) | **agrupar** 12 en grupos de 4 |
  | `? : 3 = 4` | el dividendo (¿cuánto había?) | **multiplicar** 4 × 3 (deshacer) |
  con el `=` a cualquier lado (lo de E.0).
- Igual que en E.1, **la ecuación es la situación en símbolos**: no hay conocimiento nuevo, solo
  leer qué falta y usar multiplicar o dividir. Se **comprueba** con E.0 (que ahora entiende `:`).

**Las trampas.**
- `3 x ? = 13` → **no hay número entero**: 13 no se reparte justo entre 3 (sobra 1).
- `0 x ? = 5` → imposible (cero grupos no dan nada).   `0 x ? = 0` → **cualquier número** vale.
- `12 : ? = 0` → imposible;  `? : 0 = 3` → imposible (dividir entre cero).
- `? x ? = 12` → dos huecos.   `3 x 4 = ? x 6` → la balanza con × (todavía no).
- `5 = ? : 3` (el del estándar) → 15.

**Prueba de dominio.** Las seis posiciones × los dos lados del `=` en una muestra contra el
testigo, todas comprobadas con E.0; las trampas.

**Para Carlos:** `3 x ? = 12`, `? x 4 = 12`, `12 : ? = 4`, `? : 3 = 4`, `5 = ? : 3`, `3 x ? = 13`,
`0 x ? = 0`.

## 2. LO QUE SE HIZO
- `sistema/partes/ecuaciones.py`: lee x, *, ×, :, ÷ y / en las ecuaciones; `_resolver_por` mira el SITIO
  del hueco (producto, cuantos en cada grupo, cuantos grupos, cociente, divisor, dividendo), lo dice
  con la estructura de NCETM 2.6 (repartir / agrupar / deshacer) y lo resuelve con las piezas de
  multiplicar y dividir. **Ningun conocimiento nuevo.** Comprobacion con E.0.
- E.0 (`igualdad.py` y `igual_calculando_los_lados`) entiende `:` (si no da justo, lo dice).
- Lo escrito directamente: «Que numero falta: 3 x ? = 12?» se tomaba por una orden («que numero falta:»)
  y caia en la 0.1 — una puerta que mentia, cerrada. Ahora solo se respetan las ordenes de verdad.
- `pruebas/test_E4_hueco_por.py` (19 afirmaciones; 720 ecuaciones: las 6 posiciones x los dos lados).
  `test_M1` D3/D4 cambian (antes «todavia no»; ahora 4 y 12). Ayuda, `mis_pruebas.txt` (7), `mis_casos.txt` (11).

## 3. RESULTADO
- `3 x ? = 12` -> repartir 12 entre 3 -> 4 (3 x 4 = 12 VERDADERO).  `? x 4 = 12` -> agrupar -> 3.
- `5 = ? : 3` -> 15.  `3 x ? = 13` -> no hay numero entero.  `0 x ? = 0` -> cualquiera.
- Proyecto: **1765/1765 afirmaciones + 475/475 casos — VERDE**.

## 4. PENDIENTE: la prueba de Carlos.  Lo que sigue (plan ajustado): R.2 problemas de x y : con pocas palabras.
