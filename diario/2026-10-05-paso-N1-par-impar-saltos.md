# Paso N.1 — CONTAR DE n EN n; PAR E IMPAR — 5 oct 2026

Carlos probó E.2 («ya probé») → se empieza N.1, el primer paso del camino a multiplicar.

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (mirando antes `FUENTES.md`).**
- Common Core **2.NBT.A.2**: «contar hasta 1000; **contar de 5 en 5, de 10 en 10 y de 100 en 100**».
  Y **2.NBT.B.8**: «sumar o restar 10 o 100 mentalmente a un número de 100 a 900».
- Common Core **2.OA.C.3** (grupo *«trabajar con grupos iguales: base para la multiplicación»*):
  «decidir si un grupo de objetos (hasta 20) tiene un número **par o impar** de elementos, por
  ejemplo **emparejándolos** o **contándolos de 2 en 2**; escribir un número par como la suma de dos
  sumandos iguales» (los dobles).
- **NCETM 2.1** (*Counting, unitising and coins*, Year 1): «podemos contar de forma eficiente
  contando en grupos de **dos** / de **diez** / de **cinco**». Es el primer segmento del camino a
  multiplicar (Spine 2): contar **grupos** como si fueran **unidades** (*unitising*, que Hermes ya
  usó en la 6.2).
- **NCETM 1.7**: sumar o quitar dos a un número par o impar (el par sigue par).
- El paso pendiente de E.1: `47 + ? = 77` contaba 30 pasos de uno en uno; un niño **salta de 10 en
  10** (57, 67, 77: 3 saltos = 30). Es la misma idea aplicada a «contar hasta».

**Lo que se construye.**
1. **Mecanismo**: `saltar(desde, de, saber)` — de 2 y de 5: recitar en voz baja y decir en voz alta
   el último (dos dedos, cinco dedos); de 10 y de 100: **escribir** la cifra de las decenas o de las
   centenas (como en la 2.NBT.B.8, sin contar diez ni cien pasos).
2. **Orden** `de 5 en 5 hasta 50` (también `desde`): dice la serie, y si el final no está en el
   camino lo dice («50 no se toca: ... 48, 53»).
3. Pregunta nueva **«paridad»** con dos piezas:
   - `par_emparejando` (hasta 20, 2.OA.C.3): se hacen parejas con las marcas; si sobra una, es
     impar. Si es par, dice la suma de dos iguales (14 = 7 + 7: los dobles).
   - `par_por_la_ultima_cifra` (de 10 a 1000): **10 se empareja entero** (cinco parejas), así que
     las decenas y centenas siempre se emparejan; solo hay que mirar la cifra de las unidades.
   Orden `par: 14`.
4. Pieza `contar_hasta_de_diez_en_diez` (responde a «contar hasta»): si las unidades son iguales
   (47 y 77), se salta de 10 en 10 y se cuentan los saltos (3 saltos = 30).

**Las trampas.**
- `de 2 en 2 hasta 20` → 2, 4, … 20.   `de 5 en 5 desde 3 hasta 50` → 50 no se toca.
- `de 10 en 10 desde 47 hasta 97`; `de 100 en 100 desde 250` (hasta 950); pasar de mil → se para.
- `par: 0` → par (cero parejas).   `par: 7` → impar (sobra uno).   `par: 14` → par, 7 + 7.
- `par: 846` → par mirando el 6;  `par: 1000` → par.
- `47 + ? = 77` → de diez en diez (antes: 30 pasos).   `47 + ? = 78` → ya no son decenas justas.

**Prueba de dominio.** Las series contra el testigo; par/impar de 0 a 1000 (muestra) contra el
testigo y con su pieza; `contar_hasta` de diez en diez en una muestra.

**Para Carlos:** `de 5 en 5 hasta 50`, `de 10 en 10 desde 47 hasta 97`, `de 100 en 100 desde 250`,
`par: 14`, `par: 7`, `par: 846`, `47 + ? = 77`.

## 2. LO QUE SE HIZO
- Mecanismo: `saltar(desde, de)` (de 2 y de 5 recitando con los dedos; de 10 y de 100 escribiendo la
  cifra del sitio) y `subir_una_centena`.
- Parte nueva `sistema/partes/saltos.py`: la orden `de 5 en 5 [desde A] [hasta B]` y `par: N`.
- Pregunta nueva **«paridad»** con `par_emparejando` (hasta 20, dice el doble: 14 = 7 + 7) y
  `par_por_la_ultima_cifra` (pasa de 20; dice por que basta: diez se empareja entero).
- Pieza `contar_hasta_de_diez_en_diez`: `47 + ? = 77` -> 57, 67, 77 -> 3 saltos = 30 (lo pendiente de E.1).
- `pruebas/test_N1_saltos.py` (19 afirmaciones; saltos, series, par/impar de 0 a 1000 y contar hasta en
  muestras contra el testigo). Ayuda, `mis_pruebas.txt` (8) y `mis_casos.txt` (9).

## 3. RESULTADO
- Las series, con el aviso cuando un numero no se toca (de 5 en 5 desde 3, el 50 no: 48 -> 53).
- `par: 14` -> PAR, siete parejas, 14 = 7 + 7.  `par: 7` -> IMPAR, tres parejas y uno suelto.
- `par: 846` -> PAR mirando el 6, y explica por que.
- Proyecto: **1664/1664 afirmaciones + 429/429 casos — VERDE**.

## 4. PENDIENTE: la prueba de Carlos
No se empieza M.0 (filas y columnas como sumas iguales) hasta su OK.
