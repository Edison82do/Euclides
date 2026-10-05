# Paso 4 del plan: las TÉCNICAS para ir más rápido — 5 oct 2026

## La decisión de Carlos
«El ser humano memoriza algunos datos y utiliza técnicas para agilizar la solución de problemas;
eso es válido aquí, según va avanzando el proceso de aprendizaje.»

## La pedagogía
- Las estrategias de los niños avanzan: contar todo → contar desde → **hechos derivados** →
  recuerdo (Carpenter, Fuson, NRC 2001; Baroody: contar → razonar → dominio).
- **Casi dobles** (6 + 7 = 6 + 6 + 1): hecho derivado; se apoya en los dobles, que se saben pronto.
- **Saltar de diez en diez** (47 + 30 → 57, 67, 77): la estrategia de «salto» con la tabla del cien;
  la cifra de las decenas cambia y las unidades no se tocan.
- **Compensar** (29 + 14 = 30 + 13; 52 − 29 = 52 − 30 + 1): redondear a la decena y devolver.

## Lo que se hizo
- Mecanismo: `subir_una_decena` / `bajar_una_decena` — se ESCRIBE la cifra de las decenas
  (siguiente/anterior), con el nueve que pasa a cero y la de al lado que sube (y al revés a través
  de un cero). Nada de contar diez pasos, nada de Python.
- 5 piezas: `sumar_de_diez_en_diez` (5), `restar_de_diez_en_diez` (5), `sumar_compensando` (6),
  `restar_compensando` (6), `sumar_casi_dobles` (8). Cada una con sus condiciones y su vuelta.
- Compensar usa **otra pieza por su nombre** (de diez en diez). Si usara «sumar» entero, podría
  llamarse a sí misma: el mapa lo prohíbe.
- Casi dobles **solo encaja si el doble está en la memoria**. Con la memoria llena gana recordar;
  se ve con `calcular sin memoria: 6 + 7`.
- Orden nueva `calcular: 47 + 30`: enseña todos los métodos, cuál encaja, cuál no y por qué, y
  cuál usa. También en `mis_pruebas.txt` y `mis_casos.txt`.
- Arreglos: la caché de la memoria comparaba la hora del archivo (un cambio 13 → 14 en el mismo
  instante no se veía) → ahora compara el texto. La de las piezas miraba ~30 archivos del disco
  compartido en cada cuenta → ahora como mucho una vez por segundo (50 s → 3 s).

## Resultado
`test_tecnicas` 21/21 (muestras: 2465 + 2373 + 4272 + 2092 cuentas comparadas con el testigo).
Proyecto: **1565/1565 afirmaciones + 384/384 casos — VERDE**.
Los problemas las aprovechan solos: «tenía 52 y se van 29» → quitar → compensando → 23.

## Lo que sigue
E.1 / E.2: ecuaciones con hueco (`8 + ? = 13`, `? - 4 = 9`) y el `=` como balanza.
