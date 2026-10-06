# Paso G.1 — ÁREA Y PERÍMETRO (rectángulos y polígonos) — 7 oct 2026 (madrugada)

Sigue al F.5 (4.º). NCETM Spine 2, Year 4.

## 1. EL PLAN (escrito antes de programar)

**La pedagogía (NCETM 2.16, leído el 7 oct; Common Core 3.MD.C.5–7, 3.MD.D.8, 4.MD.A.3).**
1. «El **perímetro** es la distancia alrededor del borde de una figura plana.»
2. «Se mide en **unidades de longitud** y se calcula **sumando** los lados.»
3. «La **multiplicación** sirve para el perímetro de los **polígonos regulares** (todos los lados iguales),
   y la **división** para lo inverso (si se sabe el perímetro, el lado).»
4. «El **área** es la medida de la **superficie** de una cosa plana.»
5. «Se mide en **unidades cuadradas** (cm², m²).»
6. «El área de un **rectángulo** se calcula multiplicando; las figuras rectilíneas **compuestas** se
   parten en rectángulos.»
- Common Core 3.MD.C.7: el área de un rectángulo **embaldosándolo** con cuadraditos (filas y columnas,
  M.0), y viendo que es lo mismo que multiplicar los lados. 3.MD.D.8: rectángulos con el **mismo
  perímetro y distinta área**, y al revés (el error documentado: confundir área y perímetro).
- Euclides no ve figuras: se describen con palabras y números (como pidió Carlos: «la ecuación
  directamente y algunas palabras»); el rectángulo se dibuja con cuadraditos.

**Lo que se construye** (parte nueva `sistema/partes/geometria.py`).
- `perimetro: rectangulo 5 x 3` → 5 + 3 + 5 + 3 = 16 (y 2 × 5 + 2 × 3); `perimetro: 4, 7, 5` → la suma
  de los lados; `perimetro: cuadrado de 6` → 4 × 6 = 24; `perimetro: hexagono de 5` → 6 × 5.
- `lado: cuadrado de perimetro 24` → 24 : 4 = 6 (lo inverso).
- `area: rectangulo 5 x 3` → 3 filas de 5 cuadraditos (dibujados) = 15 unidades cuadradas = 5 × 3.
- `area: 6 x 4 + 3 x 2` → una figura compuesta partida en dos rectángulos: 24 + 6 = 30.
- `comparar: rectangulo 6 x 2 y rectangulo 4 x 3` → misma área (12), distinto perímetro (16 y 14).
- Con unidades: `rectangulo 5 cm x 3 cm` → 16 cm de perímetro, 15 cm² de área.

**Las trampas.**
- `area: rectangulo 5 x 3` → 15 (no 16);  `perimetro: rectangulo 5 x 3` → 16 (no 15).
- `perimetro: cuadrado de 6` → 24 (no 36).   `area: cuadrado de 6` → 36.
- `lado: cuadrado de perimetro 25` → no sale entero (25 : 4 = 6 resto 1).
- `perimetro: triangulo de 5` → 15 (equilátero: tres lados iguales).

**Prueba de dominio.** Rectángulos de 1×1 a 12×12: área y perímetro contra el testigo; polígonos
regulares de 3 a 10 lados; figuras compuestas de dos rectángulos (muestra).

**Para Carlos:** `area: rectangulo 5 x 3`, `perimetro: rectangulo 5 x 3`, `comparar: rectangulo 6 x 2 y
rectangulo 4 x 3`, `lado: cuadrado de perimetro 24`.

## 2. LO QUE SE HIZO
- Parte nueva `sistema/partes/geometria.py`: `perimetro:` de un rectángulo (sumando los cuatro lados,
  comprobado con 2 × a + 2 × b), de una figura por sus lados, de un polígono regular (3 a 10 lados:
  multiplicando); `lado:` de un polígono regular por su perímetro (dividiendo; si no sale justo, lo dice);
  `area:` de un rectángulo o un cuadrado (dibujado con cuadraditos, por filas — M.0 — y multiplicando, de
  acuerdo), de una figura compuesta de rectángulos (sumando sus áreas); `comparar: rectangulo … y
  rectangulo …` (área y perímetro por separado; avisa si una es igual y la otra no). Unidades opcionales
  (cm, m, mm, km) y «unidades cuadradas».
- `pruebas/test_G1_area_perimetro.py` (12 afirmaciones; 144 rectángulos, 8 polígonos × 20 lados y lo
  inverso, 50 compuestas). Ayuda, `mis_pruebas.txt` (3), `mis_casos.txt` (5).

## 3. RESULTADO
- `area: rectangulo 5 x 3` → 15 unidades cuadradas;  `perimetro:` → 16.  `comparar: rectangulo 6 x 2 y
  rectangulo 4 x 3` → «la misma área con distinto perímetro: el área y el perímetro NO van juntos».
- Proyecto: **2145/2145 afirmaciones + 619/619 casos — VERDE** (110 s).

## 4. PENDIENTE: la prueba de Carlos.  Queda de 4.º: NCETM 2.17 (escala); y 5.º (hasta un millón, 1.26).
