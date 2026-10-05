# Cómo probar Euclides

**Versión 0.3 — 3 de octubre de 2026**
**Unidades: 0.1 (objetos y grupos) y 0.2 (grupos por atributo)**

---

## En una línea

Doble clic en **`E:\Euclides\PROBAR.bat`**. Se abre una ventana, corre tus casos y te deja escribir los
tuyos. Para salir, escribe `salir`.

---

## Qué sabe hacer hoy (y qué no)

| | |
|---|---|
| **0.1** | Decidir si una escena es **un objeto individual** o **un grupo** |
| **0.2** | **Reconocer** si unos objetos forman grupo y decir **qué atributos comparten** |
| **0.2** | **Formar** el grupo de los que cumplen un criterio (`color=rojo`) |
| **Siempre** | Si no entiende lo que le escribes, **lo dice**; nunca revienta |
| **No sabe todavía** | Contar. No dice "hay tres". No compara cantidades. No decide pertenencia |

---

## Las tres formas de preguntar

### 1. Objeto o grupo (unidad 0.1)

Cosas separadas por **comas**. Si repites un nombre, es **la misma** cosa señalada otra vez.

```
silla                 -> objeto individual
silla,mesa            -> grupo
silla,silla           -> objeto individual  (la misma silla, dos veces)
```

### 2. ¿Forman grupo? (unidad 0.2)

Objetos con atributos. Valen **punto y coma** o **comas de fuera** de los paréntesis. Los atributos van
entre paréntesis como `nombre=valor`, separados por comas.

```
caja_A(color=rojo,forma=cubo); caja_B(color=rojo,forma=esfera)   -> grupo, comparten color
caja_A(color=rojo,forma=cubo), caja_B(color=azul,forma=cubo)     -> grupo, comparten forma
casa(color=azul), carro                                          -> no se puede decidir (al carro
                                                                    no le sabemos el color)
```

### 3. Dame el grupo de... (unidad 0.2)

El criterio, dos puntos, y la escena.

```
color=rojo: a(color=rojo,forma=cubo); b(color=azul,forma=cubo); c(color=rojo,forma=esfera)
   -> el grupo son a y c
```

---

## Lo más importante: el nombre es el identificador

El sistema **no ve** los objetos, y **no adivina** por el parecido de los nombres. El nombre que escribes
**es** la identidad de la cosa.

- `silla` y `silla` → **la misma** silla.
- `silla_A` y `silla_B` → **dos** sillas distintas, aunque en el mundo las dos se llamen igual.

Y si escribes la misma cosa con dos descripciones que no cuadran:

```
casa(color=azul); casa(color=rojo)
   -> no se puede decidir: o es la misma casa (y una de las dos es falsa),
      o son dos casas y les falta un nombre distinto
```

---

## Si escribes algo que no entiende

No revienta: te lo dice y te recuerda las formas correctas.

```
pregunta> caja(colorrojo)

NO ENTIENDO ESTO: no entiendo el atributo 'colorrojo'
   se escribe asi:  nombre=valor

FORMAS QUE SI ENTIENDO:
  0.1  objeto o grupo      silla,mesa
  0.2  forman grupo?       a(color=rojo,forma=cubo); b(color=azul,forma=cubo)
  0.2  dame el grupo de... color=rojo: a(color=rojo); b(color=azul)

El sistema no adivina: si no entiende, lo dice.
```

---

## Las tres formas de lanzarlo

1. **Doble clic en `PROBAR.bat`** — lo normal. Corre tus casos y abre la ventana.
2. `py -3 E:\Euclides\probar.py "silla,mesa"` — una pregunta suelta.
3. `py -3 E:\Euclides\probar.py --casos` — todos tus casos de golpe.

Órdenes dentro de la ventana: `casos`, `ayuda`, `salir`.

---

## Dónde escribes TUS casos

Archivo: **`E:\Euclides\mis_casos.txt`** (Bloc de notas). Cada línea:

```
pregunta | lo que espero | comentario
```

Lo que puedes poner en "lo que espero":

| Escribes | Significa |
|---|---|
| `objeto` | una sola entidad |
| `grupo` | dos o más entidades distintas |
| `grupo:color` | forman grupo y comparten el color |
| `grupo:color,forma` | comparten las dos cosas |
| `no_grupo` | no comparten nada (o es una sola cosa) |
| `tiene:a,c` | al formar un grupo, el resultado son esos |
| `no_hay_grupo` | ninguno cumple el criterio |
| `no_decidible` | el sistema debe decir que no sabe |
| `no_entendido` | el sistema debe decir que no entiende la escritura |
| `?` | no comprobar nada, solo ver qué responde |

Guarda el archivo y vuelve a lanzar el probador: **se recarga solo**. Los `#` son comentarios.

---

## Por qué el sistema explica lo que dice

Cada respuesta sale con su **traza**: qué reglas se han probado, en qué orden, cuál ha decidido y **qué
conocimiento escrito la respalda**. Ejemplo real:

```
PREGUNTA (0.2): forman GRUPO estos objetos?
ESCENA:
    casa  [color=azul]
    casa  [color=rojo]
  reglas probadas, en orden:
    - reconocer_escena_vacia : escena_vacia(escena) -> falso
    - reconocer_entidad_contradictoria : hay_entidad_contradictoria(escena) -> cierto
RESULTADO: no_decidible
  lo decide la regla 'reconocer_entidad_contradictoria'
  respaldado por el conocimiento 'identidad_de_referencias' [FIJADO]
```

---

## Qué buscar cuando lo pruebes (lo que me interesa que intentes romper)

1. **Cosas escritas a medias o mal**: `caja(colorrojo)`, `caja()`, `caja(color=)`. Todas deberían
   contestar "no entiendo", ninguna debería romperse.
2. **La misma cosa con dos descripciones distintas** (`casa(color=azul); casa(color=rojo)`).
3. **Mezclas raras de separadores**: `a(color=rojo), b(forma=cubo)`.
4. **Un objeto al que le falta un atributo** que los demás sí tienen: debería callarse.
5. **Repetir el mismo nombre** en 0.1 (`taza,taza,taza`).
6. **Pedir un grupo que no existe** (`color=verde:` cuando nadie es verde).
7. Cosas tuyas: nombres con espacios, mayúsculas y minúsculas, números (`caja1,caja2`).

Si algo te chirría, dímelo con **la línea exacta que escribiste y lo que esperabas**. Se corrige desde la
base: primero el conocimiento escrito, después el código.

---

## Los archivos, por si quieres mirar

| Archivo | Qué es |
|---|---|
| `E:\Euclides\conocimiento\*.kn` | El saber, en texto plano. Se puede leer y editar |
| `E:\Euclides\sistema\motor.py` | El programa que lee, decide y explica |
| `E:\Euclides\pruebas\` | Las pruebas del proyecto (0.1, 0.2 y robustez) |
| `E:\Euclides\mis_casos.txt` | **Tus casos** |
| `E:\Euclides\PROBAR.bat` | El lanzador de doble clic |
| `E:\Euclides\PROGRESO.md` | Qué está hecho, qué falla, qué toca |
| `E:\Euclides\diario\` | Lo que se hizo cada día y lo que se midió |
