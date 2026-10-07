# Paso M.12 — USAR LA EQUIVALENCIA PARA CALCULAR (doblar y dividir a la mitad; escalar la división) — 7 oct 2026

Sigue al N.5. Es el segmento **2.18** de NCETM (Spine 2, Year 5): *Using equivalence to calculate*.
Common Core no tiene un estándar propio para esto; es la estrategia de 5.NBT.B.5–6 / 6.NS.B.2
(«estrategias basadas en las propiedades de las operaciones»).

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (NCETM 2.18, leído el 7 oct; la web de NCETM no se puede abrir desde la nube: los dos
puntos de enseñanza salen del índice de NCETM en el buscador).** El objetivo del segmento: *ser más
eficiente al calcular usando la equivalencia, ajustando los factores (en la multiplicación) y el
dividendo y el divisor (en la división)*.
1. **Punto 1 (multiplicar):** «si un factor aumenta multiplicativamente y el otro disminuye de la misma
   manera, **el producto no cambia**». 25 × 16 = 50 × 8 = 100 × 4 = 400.
2. **Punto 2 (dividir):** «si el dividendo cambia multiplicativamente y el divisor cambia **de la misma
   manera**, **el cociente no cambia**». 180 : 20 = 18 : 2 = 9;  165 : 5 = 330 : 10 = 33.
- Viene de la 2.5 (doblar y dividir a la mitad en las tablas), de la 2.13 (×/÷ 10 y 100) y de la 2.17
  («veces»). Prepara la 2.19 (decimales) y la proporcionalidad.

**Cómo lo hace un humano sin calculadora (y así lo hará Euclides).**
- **Doblar y dividir a la mitad.** Si un factor acaba en 5 (25, 35, 125) y el otro es par, se dobla el
  primero (25 → 50: el 5 se vuelve un 0) y se parte el otro por la mitad (16 → 8). Se repite mientras
  el factor, sin sus ceros, siga acabando en 5 y el otro siga siendo par: 25 × 16 → 50 × 8 → 100 × 4.
  Al final un factor son **decenas o centenas justas** y la cuenta es fácil (M.9).
  El doble es una suma (x + x); la mitad, parejas (M.3). Nada nuevo.
- **Escalar la división.** Si el divisor acaba en 5 (5, 15, 25…), se doblan **los dos** (165 : 5 =
  330 : 10). Si los dos acaban en cero, se les quita un cero **a los dos** (los dos se hacen diez veces
  más pequeños: 180 : 20 = 18 : 2). Al final el divisor es 10/100/1000 o de una cifra.
  OJO con el resto: si la división **no es justa**, el cociente sigue igual pero el **resto cambia de
  tamaño** (17 : 5 = 3 y sobran 2; 34 : 10 = 3 y sobran 4). Por este camino solo se usan las justas;
  si sobra algo, la pieza lo dice y se usa otro método.
- **Ver la equivalencia sin calcular** (pensamiento relacional, como en E.0 y E.2):
  `verdad: 3 x 12 = 6 x 6` → VERDADERO **sin hacer las cuentas**: 6 es el doble de 3 y 6 es la mitad de 12.
  `24 x 5 = 12 x ?` → 10: 12 es la mitad de 24, así que el hueco es el doble de 5.
  `180 : 20 = 18 : ?` → 2: 18 es diez veces más pequeño que 180, el divisor también.

**Lo que se construye.**
- Pieza `multiplicar_escalando` (responde «multiplicar», rapidez 6): doblar y dividir a la mitad.
  Usa `sumar` (el doble) y `dividir_a_la_mitad` (la mitad), y para la cuenta final
  `multiplicar_por_10_o_100`, `multiplicar_por_decenas_justas` o `multiplicacion_corta` (por su nombre:
  no puede usar su propia pregunta).
- Pieza `dividir_escalando` (responde «dividir», rapidez 6): doblar los dos / quitar un cero a los dos.
  Para la cuenta final, las piezas de dividir por su nombre (por 10 o 100, la mitad, la tabla, la corta).
- Pieza `igual_escalando` (responde «igualdad», rapidez 3): VERDADERO sin calcular si un factor sube
  K veces y el otro baja K veces (en ×), o si dividendo y divisor cambian los dos K veces (en :).
  Si no hay esa relación, no le sale y decide la pieza que calcula los lados.
- Pregunta nueva `balanza_por` con la pieza `balanza_escalando`: el hueco en `a x b = c x ?` y en
  `a : b = c : ?` (o `? : d`) sin calcular los lados. La parte `letra.py` la prueba primero; si no
  encaja, se sigue como siempre (calcular un lado y deshacer).
- Orden `equivalente: 25 x 16` / `equivalente: 375 : 25`: enseña la cadena de cuentas equivalentes.

**Las trampas.**
- `verdad: 3 x 12 = 4 x 11` → FALSO (la compensación de la SUMA —uno más aquí, uno menos allí— no
  vale en la multiplicación: 36 ≠ 44).
- `verdad: 96 : 4 = 192 : 2` → FALSO (en la división los dos cambian **igual**, no al revés: 24 ≠ 96).
- `verdad: 96 : 4 = 48 : 2` → VERDADERO sin calcular (los dos a la mitad).
- `24 x 5 = 12 x ?` → 10 (no 3, ni 17).   `180 : 20 = 18 : ?` → 2 (no 200).
- `17 : 5` → 3 y sobran 2 (no «3 y sobran 4», que es lo que daría 34 : 10 si se copiara el resto).
- `25 x 16` → 400 por doblar y dividir a la mitad; `25 x 15` → no encaja (15 es impar) y se hace de
  otra manera.

**Prueba de dominio.** Contra el testigo: todos los productos f × g con f acabado en 5 (5..195) y g par
(2..40) que encajan; una muestra de divisiones justas con divisor que acaba en 5 o con ceros a los dos
lados; las igualdades equivalentes (verdaderas sin calcular) y sus trampas (falsas); huecos en
`a x b = c x ?` y `a : b = c : ?`.

## RESULTADO (7 oct)

**Hecho, verde: proyecto 2252/2252 + 643/643.** `test_M12_equivalencia` 26/26; mis_casos 643/643; mis_pruebas 168/168.

- 4 piezas nuevas, sin tocar el motor de piezas:
  - `multiplicar_escalando` (rapidez 6): dobla el factor que acaba en 5 y parte el otro por la mitad
    mientras se pueda; la cuenta final la hace una pieza por su nombre (por 10/100, decenas justas, la
    corta). `125 x 24 = 250 x 12 = 500 x 6 = 1000 x 3 = 3000`. No entra en las tablas (hasta el 12).
  - `dividir_escalando` (rapidez 6): dobla los dos si el divisor acaba en 5; quita un cero a los dos si
    los dos acaban en 0. `375 : 25 = 750 : 50 = 75 : 5 = 150 : 10 = 15`. Si no es justa, no la usa (el
    resto cambiaría de tamaño) y la hace otro método: `17 : 5` → 3 resto 2.
  - `igual_escalando` (igualdad, rapidez 3): VERDADERO sin calcular si un factor sube K veces y el otro
    baja K veces, o si dividendo y divisor cambian los dos K veces. Si no, decide la pieza que calcula.
  - `balanza_escalando` (pregunta nueva `balanza_por`): el hueco en `a x b = c x ?` y `a : b = c : ?`
    sin calcular los lados; `letra.py` la prueba primero y, si no encaja, calcula como siempre.
- Parte nueva `sistema/partes/equivalencia.py`: la orden `equivalente: 25 x 16` (la cadena de cuentas
  equivalentes y la comprobación con la operación contraria) y el enganche de la balanza.
- Prueba de dominio: 200 productos (107 por la equivalencia), 578 divisiones (282 por la equivalencia,
  todas justas), 452 igualdades (verdaderas sin calcular, y las trampas falsas), 200 huecos (todos sin
  calcular los lados). Todo contra el testigo.
- **Falta la prueba de Carlos.** Y leer el segmento entero de NCETM 2.18 cuando se pueda abrir (desde la
  nube la web está bloqueada): si trae ejemplos o trampas que aquí no están, se añaden.
