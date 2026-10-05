# Diario — 3 de octubre de 2026 (sesión 1, cierre definitivo)

## Corrección tras las pruebas de Carlos

Carlos probó el sistema por su cuenta (que era justamente lo que queríamos) y encontró dos cosas.

### 1. Un fallo grave mío: el sistema reventó en vez de decir «no entiendo»

Escribió:

```
casa(color=azul), carro
```

y el sistema soltó un **traceback** de Python. Eso viola de frente la regla 4 del proyecto: el sistema
tiene que saber decir «no entiendo esto» en vez de romperse. Un traceback no enseña nada a quien está
probando y, peor, esconde que el sistema no había entendido la entrada.

**Qué se arregló, en tres frentes:**

1. **El separador de escena.** Antes solo valía `;` entre objetos con atributos. Ahora el motor parte la
   escena por `;` **o** por comas de fuera de los paréntesis (un contador de profundidad decide cuáles
   son separadores de atributo y cuáles de objeto). Así `casa(color=azul), carro` se entiende, que es
   justo lo que un humano escribe.
2. **Nunca un traceback.** `explicar_pregunta` captura los errores de lectura y responde:

```
NO ENTIENDO ESTO: no entiendo el atributo 'colorrojo'
   se escribe asi:  nombre=valor

FORMAS QUE SI ENTIENDO:
  0.1  objeto o grupo      silla,mesa
  0.2  forman grupo?       a(color=rojo,forma=cubo); b(color=azul,forma=cubo)
  0.2  dame el grupo de... color=rojo: a(color=rojo); b(color=azul)

El sistema no adivina: si no entiende, lo dice.
```

3. **Prueba de robustez nueva** (`correr_robustez` en `test_0_2.py`): 7 entradas mal escritas
   (`caja(colorrojo)`, `caja(color=)`, `caja(=rojo)`, `(color=rojo)`, `caja(color=rojo`,
   `caja(color=rojo))`, `color=: a(color=rojo)`) y **ninguna puede reventar**: todas tienen que
   producir «NO ENTIENDO».

**Fallo secundario, encontrado al escribir esa prueba (no lo encontró Carlos):** `caja(color=rojo))`
colaba como válido y el valor quedaba siendo `rojo)`. Faltaba validar los paréntesis sobrantes. Lección
anotada: el traceback de Carlos destapó una **familia entera** de entradas mal formadas que estaban sin
cubrir.

### 2. Su hallazgo conceptual: objetos con el mismo nombre y atributos distintos

Carlos lo dijo así: «podría haber objetos con el mismo nombre con atributos distintos».

Es exactamente el problema de la identidad, ahora en el terreno de los atributos. Y destapó un caso que
no estaba cubierto:

```
casa(color=azul); casa(color=rojo)
```

Aquí el mismo identificador aparece **dos veces con descripciones que no cuadran**: o es la misma casa
(y entonces una de las dos descripciones es falsa), o son dos casas distintas **y les falta un nombre
distinto**. El sistema no puede elegir por su cuenta, así que **se calla**: nuevo conocimiento regla
`hay_entidad_contradictoria`, aplicada tanto a reconocer como a formar, con conclusión `no_decidible`.

**Lo que hay que decirle claro a Carlos:** en la representación actual, **el nombre de la entidad es su
identificador**. Dos cosas distintas necesitan nombres distintos (`casa_A`, `casa_B`), aunque en el
mundo las dos se llamen «casa». El sistema no deduce del parecido de los nombres: eso se decidió en la
unidad 0.1 y se mantiene.

### Medición — salida real

```
Todas las pruebas del proyecto: 22/22   RESULTADO GLOBAL: VERDE
   0.1:  8/8
   0.2: 14/14  (2 de ejemplo + 5 de dominio + 1 de formar + 4 de dominio de formar... y 7 de robustez)
Robustez: 7/7 entradas mal escritas -> todas dicen «NO ENTIENDO», ninguna revienta
Casos de Carlos: 11 bien, 0 fallan
```

### Lo que este incidente enseña (y queda anotado)

- **Probar no es un extra: es lo que ha destapado los dos fallos.** Si Carlos no hubiera escrito su
  propia línea, el crash habría seguido ahí.
- **Una entrada mal formada no es un error del usuario: es una pregunta legítima que el sistema debe
  saber rechazar.** De ahí la prueba de robustez, que a partir de ahora acompaña a cada unidad.
- **Los casos raros que él imagina son mejores que los que yo invento.** `casa(color=azul), carro`
  y `casa` con dos descripciones distintas son ahora pruebas fijas del proyecto.
