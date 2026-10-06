# Paso D.3 — EL DINERO: PESOS Y CENTAVOS — 7 oct 2026 (madrugada)

Sigue al D.2 (4.º). NCETM Spine 1, Year 4 (el último segmento de Spine 1 de 4.º).

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (NCETM 1.25, leído el 7 oct; Common Core 4.MD.A.2).**
1. «Un penique es **una centésima** de libra; la manera de escribir el dinero se basa en los números con
   décimas y centésimas.»  Aquí: **un centavo es la centésima parte de un peso** ($3.45 = 3 pesos y 45
   centavos = 345 centavos). (NCETM usa libras; uso pesos y centavos, la moneda de Carlos.)
2. «Las estrategias de **cálculo equivalente** sirven para sumar precios corrientes» — $2.99 es un
   centavo menos que $3: $2.99 + $1.50 = $3 + $1.50 − 1 centavo = $4.49 (la compensación, P.4, con dinero).
3. «Para el **cambio** cuando se paga con billetes, lo eficiente es **contar hacia adelante** (la
   diferencia)»: de $6.35 a $10 → 5 centavos hasta $6.40, 60 centavos hasta $7, y 3 pesos hasta $10:
   $3.65 (la resta como diferencia, P.6 y NCETM 1.12).
4. «Las **columnas** sirven para sumar y restar dinero» (D.1/D.2).
5. «El cambio cuando se compran **varias cosas** usa la estructura parte-parte-(parte)-todo»: lo pagado
   es el todo; las cosas y el cambio son las partes.
- Common Core 4.MD.A.2: problemas de dinero con decimales.

**Lo que se construye** (parte nueva `sistema/partes/dinero.py`, sobre `decimales.py`).
- `dinero: $3.45` → 3 pesos y 45 centavos = 345 centavos.
- `$2.99 + $1.50` → en columnas, y si un precio acaba en .99 o .95, también compensando.
- `cambio: pago $10 por $6.35` → contando hacia adelante; comprobado sumando (6.35 + 3.65 = 10).
- `cambio: pago $20 por $3.45 + $6.80 + $2.15` → el total (parte + parte + parte) y el cambio; la barra
  del todo y las partes; comprobado.

**Las trampas.**
- `$2.99 + $1.50` → $4.49.   `$3.45 + $6.80` → $10.25 (los centavos pasan de 100: un peso más).
- `cambio: pago $10 por $6.35` → $3.65 (no $4.65 ni $3.75).   `pago $5 por $5` → $0.
- `cambio: pago $5 por $6.35` → no alcanza.   `$3.456` → los centavos son dos cifras.

**Prueba de dominio.** Sumas y restas de precios y cambios de billetes de 1, 5, 10, 20, 50, 100 y 200
(muestra), contra un testigo en centavos enteros.

**Para Carlos:** `dinero: $3.45`, `$2.99 + $1.50`, `cambio: pago $10 por $6.35`,
`cambio: pago $20 por $3.45 + $6.80 + $2.15`.

## 2. LO QUE SE HIZO
- Parte nueva `sistema/partes/dinero.py` (sobre `decimales.py`): `dinero: $3.45` (345 centavos);
  `$2.99 + $1.50` (en centavos como cosas, en columnas con los nombres del dinero, y **compensando**
  cuando un precio acaba en .99 o .95); `cambio: pago $10 por $6.35` (**contando hacia adelante**: hasta
  la decena de centavos, hasta el peso, hasta lo pagado; comprobado sumando); con varias cosas, el todo y
  las partes con su barra.
- Pesos y centavos en vez de libras y peniques (la moneda de Carlos); el signo $ al principio.
- `pruebas/test_D3_dinero.py` (10 afirmaciones; 200 cuentas de precios y 200 cambios con billetes de 1 a
  50, testigo en centavos enteros). Ayuda, `mis_pruebas.txt` (3), `mis_casos.txt` (5).

## 3. RESULTADO
- `cambio: pago $10 por $6.35` → «de $6.35 a $6.40: $0.05; de $6.40 a $7.00: $0.60; de $7.00 a $10.00:
  $3.00» → $3.65.  `$2.99 + $1.50` → $4.49 (también «$3.00 + $1.50, y le quito ese centavo»).
- Proyecto: **2121/2121 afirmaciones + 610/610 casos — VERDE** (104 s).
- **Con D.3 queda completo Spine 1 de 4.º** (1.22–1.25).

## 4. PENDIENTE: la prueba de Carlos.  Sigue F.5: multiplicar un entero por una fracción (NCETM 3.6).
