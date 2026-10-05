# Investigación — 3 de octubre de 2026

**Encargo de Carlos:** no soy experto, investiga proyectos parecidos y pedagogía; empieza por una idea
básica que luego pulimos.

**Resultado:** 2 frentes investigados con fuentes. Ninguna decisión de diseño tomada todavía.

---

## Frente 1 — Sistemas parecidos (qué se intentó antes y qué se aprendió)

### 1. AM — Automated Mathematician (Douglas Lenat, 1976-77)
- Cada concepto matemático se representa como un **módulo estructurado de conocimiento** con "facetas"
  (slots): definiciones, ejemplos, generalizaciones, algoritmos.
- Arrancó con **115 conceptos** de teoría de conjuntos y en **1 hora de CPU** redescubrió la aritmética
  y parte de la teoría elemental de números (primos, factorización única).
- **Por qué funcionó (lección central):** porque la representación elegida (números como listas unarias
  en Lisp) hacía que las operaciones matemáticas fueran *naturales* sobre la estructura. Lenat lo llama
  "el emparejamiento entre forma y contenido": si la representación no imita la estructura del concepto,
  nada funciona.
- **Por qué falló:** no podía descubrir heurísticas nuevas para los campos nuevos que abría. Y no
  descubrió nunca "resto", "máximo común divisor", "mayor que", "infinito", "demostración".
- **Crítica documentada:** parte de su "conocimiento" estaba en procedimientos no explicados — reglas
  publicadas con términos vagos ("si dos expresiones son estructuralmente similares..."). Es decir,
  **cajas negras**. Lenat mismo lo admitió.

**Lo que nos llevamos:** la representación es lo que da el poder; y la crítica a AM es exactamente
nuestra regla 13 (nada de cajas negras) y regla 4 (no inventar).

### 2. Eurisko (Lenat, sucesor de AM, 1983)
- Añadió una **lengua de heurísticas** con decenas de slots por regla, para que las reglas fueran
  datos y no código.
- Define el **"modelo de acreción" de la formación de teorías**, en 7 pasos:
  1. Ante una definición/objeto/operación nueva: recoger datos empíricos inmediatamente.
  2. Notar regularidades, patrones y excepciones.
  3. Formular hipótesis, modificarlas y **diseñar experimentos** para probarlas.
  4. Economizar: crear definiciones nuevas que acorten las conjeturas útiles.
  5. Destilar heurísticas nuevas a partir de lo aprendido (paso raro).
  6. Cambiar la representación cuando ya no da (paso más raro).
- Eurisko descubrió resultados nuevos de verdad (grafos geodésicos únicos; diseño de flotas; VLSI).

**Lo que nos llevamos:** el modelo de acreción es, casi punto por punto, nuestro ciclo de sesión y el
guion natural de las fases avanzadas (nivel 13, crecimiento autónomo). Se cita como referencia.

### 3. Cyc / OpenCyc (Lenat, 1984 → hoy)
- ~2,2 millones de aserciones escritas a mano por ~40 años de esfuerzo; OpenCyc: 239.000 conceptos.
- La comunidad de IA lo considera un fracaso ("el fracaso más notorio de la historia de la IA",
  Domingos 2015). El cuello de botella fue **la adquisición del conocimiento**: escribir reglas
  complejas a mano no escala, y las interfaces para no expertos resultaron lentas e ineficaces.
- **Lo que sí funcionó bien:** la *validación automática* — restricciones de los predicados que
  rechazan aserciones sin sentido ("Witbrock es un mueble de jardín" se bloquea solo), y el rechazo de
  lo que contradice lo ya sabido.

**Lo que nos llevamos:** **no** ir a escala masiva. Unidad pequeña, verificada, acumulada. Y adoptar
la idea buena de Cyc: el sistema debe poder **rechazar** lo que contradice lo que ya sabe.

### 4. Metamath (Norman Megill)
- Lenguaje deliberadamente mínimo: la sustitución es la única regla; **el verificador son ~300 líneas**
  de código. Verifica ~18.000 demostraciones en 6 segundos.
- 74 de los 100 teoremas clásicos de Wiedijk, verificado además por 5 verificadores independientes
  escritos por 5 personas distintas.
- Clave: cada paso de la demostración **referencia solo un axioma o una demostración anterior**. No hay
  tácticas que "redescubran" la prueba. Todo es transparente y rastreable.
- Frente a Lean/Mizar/Coq, que son gigantes con bibliotecas enormes (mathlib: comunidad entera;
  Mizar: biblioteca central de "artículos" revisados).

**Lo que nos llevamos:** dos ideas de ingeniería. (1) **Verificador pequeño y simple = confianza
total.** (2) Los sistemas formales grandes organizan el saber en **un archivo = un artículo/concepto**
con dependencias explícitas, exactamente el esquema que ya tenemos en el método.

### 5. Aviso de la literatura moderna
- Andrew Avigad (CMU): "el aprendizaje automático tiene intuiciones pero falla en los detalles; la IA
  simbólica es precisa pero se pierde". Los LLM hacen aritmética por atajos simbólicos jerárquicos, no
  por algoritmo (arXiv 2410.15580).
- Conclusión para nosotros: en un dominio **pequeño y bien delimitado**, lo simbólico no se pierde. Ese
  es justo el hueco donde vive nuestro proyecto.

---

## Frente 2 — Pedagogía (cómo se enseña de verdad)

### 1. Los cinco principios del conteo — Gelman & Gallistel (1978)
Son el estándar de la psicología del desarrollo. **Coinciden casi exactamente con nuestras unidades
2.1–2.6**, lo cual valida el plan escrito antes de investigar:
- **uno-a-uno** (un nombre de número por objeto) → unidad 2.1
- **orden estable** (la lista de palabras se repite siempre igual) → unidad 2.2
- **cardinalidad** (el último número dicho es el total) → unidad 2.4
- **abstracción** (se puede contar cualquier cosa) → unidad 2.6
- **irrelevancia del orden** (contar en otro orden da el mismo total) → unidad 2.5

### 2. Trayectorias de aprendizaje — Clements & Sarama (Building Blocks / TRIAD)
Progresión documentada del conteo, con niveles con nombre:
`Recitador → Recitador(10) → Correspondedor → Contador (números pequeños) → Productor → Contador(10)
→ Contador y Productor(10+)`.
Y una **segunda trayectoria paralela, el *subitizing*** (reconocer la cantidad de un vistazo, sin
contar): `Sensación numérica → Reconocedor de números muy pequeños → ... → Subtizador perceptivo hasta
4 → Subtizador conceptual`.
Hallazgo importante: **las dos trayectorias se desarrollan por separado y solo después se conectan.**

**Falta en nuestro PLAN.md:** el *subitizing* no aparece. Candidato a añadirse como unidad del Nivel 1.

### 3. Los "conocedores de subconjuntos" (Wynn 1990/92; Le Corre et al. 2006)
Antes de entender el principio cardinal, los niños aprenden el significado exacto de "uno", luego "dos",
luego "tres", a veces "cuatro", **en ese orden** — y los números siguientes los adquieren **todos de
golpe**, no uno a uno. Es una frontera conceptual muy fina: lo que distingue al que lo entiende es
comprender que "siguiente en la lista" = "un objeto más" (el sucesor).

**Para nosotros:** sugiere diseñar pruebas separadas para 3.1 (símbolos) y 3.4 (el puente), y no dar por
cerrado el nivel 3 hasta probar el salto del sucesor.

### 4. Errores típicos documentados (para diseñar las pruebas de dominio)
- **De secuencia:** omitir números (1,2,3,6,7,10), reordenar, reutilizar.
- **De seguimiento:** contar un objeto dos veces, saltarse uno.
- **De coordinación:** el señalamiento no va en paso con las palabras.
- **Repetición del último número sin entender:** el niño cuenta 5 objetos y, preguntado "¿cuántos hay?",
  vuelve a contar. Y al revés: repite el último número correctamente **sin** entender uno-a-uno
  (el 22% de un estudio de 188 niños de 4-5 años: pasan la pregunta "¿cuántos hay?" pero fallan el
  uno-a-uno). Lección: **la prueba de dominio no puede consistir solo en preguntar "¿cuántos hay?"**.
- **La "regla de la última palabra" superficial** (Fuson 1988; Bermejo et al. 2004): si se hace contar
  5 objetos empezando por la palabra "tres", muchos niños responden "siete" — el último que dijeron.
  Prueba muy fina para separar el que entiende del que repite.
- **Confundir conjuntos con sus elementos** (contar las personas en vez de las familias): fallo del
  principio de abstracción.

**Para nosotros:** cada unidad llevará casos con **trampa deliberada**, sacados de esta lista.

### 5. Concreto → pictórico → abstracto
- Singapur (Ministerio de Educación, desde los 80) y Montessori usan la misma secuencia, que viene del
  modelo de Bruner: *enactivo → icónico → simbólico*.
- Nuestro esquema de conocimiento ya tiene `representaciones: concreta / numerica / formal / general`.
  **La investigación confirma que está bien puesto.**

---

## Fuentes citadas (para el informe a Carlos)

- Lenat, D.B. — *AM* (IJCAI 1977); *Why AM and Eurisko Appear to Work* (AAAI 1983); *Theory Formation by
  Heuristic Search* (Nature of Heuristics II); *Eurisko: Heuristics III* (Artificial Intelligence, 1983).
- Lenat & Guha — *CYC: A Large-Scale Investment in Knowledge Infrastructure* (CACM 1995);
  Matuszek et al. — *An Introduction to the Syntax and Content of Cyc* (AAAI Spring Symposium 2006);
  Davis & Marcus — *Evaluating CYC: Preliminary Notes* (NYU).
- Megill, N. — *The Metamath Proof Language* (2014); Metamath 100 (Wiedijk's list).
- Bancerek et al. — *The Role of the Mizar Mathematical Library* (2018); Avigad — *Formal Mathematics
  and the Lean Theorem Prover* (CMU); *Machine learning and symbolic AI for mathematics* (CMU).
- Gelman, R. & Gallistel, C.R. — *The Child's Understanding of Number* (1978).
- Gelman & Meck — *Preschoolers' counting: Principles before skill* (Cognition, 1983).
- Clements, D.H. & Sarama, J. — *Learning Trajectories in Early Mathematics* (2009);
  learningtrajectories.org (trayectorias de conteo y subitizing).
- Wynn, K. (1990, 1992); Le Corre et al. (2006); Sarnecka & Carey — *How Counting Represents Number*
  (UC eScholarship: "One, Two, Three, Four, Nothing More").
- Fuson (1988); Bermejo et al. (2004) — la regla de la última palabra.
- Nguyen et al. — *More Than Counting: Learning to Count* (Boston College, 2017) — errores típicos.
- Chang, Lee & Koay — *Teaching and Learning with Concrete-Pictorial-Abstract Sequence* (NIE, 2017);
  DREME/Stanford — *What Children Know and Need to Learn about Counting*.

---

## Propuesta que se deriva (pendiente de aprobación de Carlos)

1. **Esquema del conocimiento:** mantener los campos del método, en texto plano legible, un archivo por
   concepto. Añadir un campo obligatorio `errores_tipicos` (los documentados arriba) y una sección
   `prueba_de_dominio` con casos con trampa.
2. **Prueba de dominio estándar:** mínimo 5 casos no programados por unidad, y **al menos uno de ellos
   una trampa** extraída del carné de errores (contar en otro orden, contar empezando por otra palabra,
   preguntar "¿cuántos hay?" después de contar, contar objetos de otra categoría).
3. **Añadir al plan:** *subitizing* (reconocer cantidad sin contar) como unidad del Nivel 1.
4. **Idea básica para arrancar:** Unidad 0.1 (objetos individuales vs grupo) con el motor mínimo
   (cargar concepto, ejecutar prueba, imprimir la traza de qué regla se aplicó).
