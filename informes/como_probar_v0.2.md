# Cómo probar Euclides

**Versión 0.2 — 3 de octubre de 2026**
**Unidades que se pueden probar: 0.1 (objetos y grupos) y 0.2 (grupos por atributo)**

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
| **No sabe todavía** | Contar. No dice "hay tres". No compara cantidades. No decide pertenencia |

---

## Las tres formas de preguntar

### 1. Objeto o grupo (unidad 0.1)

Cosas separadas por **comas**. Si repites un nombre, es **la misma** cosa señalada otra vez.

```
silla                 -> objeto individual
silla,mesa            -> grupo
silla,silla           -> objeto individual  (la misma silla, dos veces)
libro,lapiz,vaso      -> grupo
```

### 2. ¿Forman grupo? (unidad 0.2)

Objetos con atributos separados por **punto y coma**. Los atributos van entre paréntesis como
`nombre=valor`, separados por comas.

```
caja_A(color=rojo,forma=cubo); caja_B(color=rojo,forma=esfera)
   -> grupo, comparten color

caja_A(color=rojo,forma=cubo); caja_B(color=azul,forma=cubo)
   -> grupo, comparten forma

caja_A(color=rojo,forma=cubo); caja_B(color=azul,forma=esfera)
   -> no forman grupo: no comparten nada
```

### 3. Dame el grupo de... (unidad 0.2)

El criterio, dos puntos, y la escena.

```
color=rojo: a(color=rojo,forma=cubo); b(color=azul,forma=cubo); c(color=rojo,forma=esfera)
   -> el grupo son a y c
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
| `no_grupo` | no comparten nada |
| `tiene:a,c` | al formar un grupo, el resultado son esos |
| `no_hay_grupo` | ninguno cumple el criterio |
| `no_decidible` | el sistema debe decir que no sabe |
| `?` | no comprobar nada, solo ver qué responde |

Guarda el archivo y vuelve a lanzar el probador: **se recarga solo**. Los `#` son comentarios.

---

## Por qué el sistema explica lo que dice

Cada respuesta sale con su **traza**: qué reglas se han probado, en qué orden, cuál ha decidido y **qué
conocimiento escrito la respalda**. Ejemplo real:

```
PREGUNTA (0.2): forman GRUPO estos objetos?
ESCENA:
    caja_A  [color=rojo, forma=cubo]
    caja_B  [color=rojo, forma=esfera]
  reglas probadas, en orden:
    - reconocer_escena_vacia : escena_vacia(escena) -> falso
    - reconocer_una_sola_entidad : menos_de_dos_entidades(escena) -> falso
    - reconocer_atributo_indeterminado : algun_atributo_indeterminado(escena) -> falso
    - reconocer_grupo_por_atributo : hay_atributo_compartido_por_todos(escena) -> cierto
  atributos que comparten TODOS: color
RESULTADO: grupo_atributo
  lo decide la regla 'reconocer_grupo_por_atributo'
  respaldado por el conocimiento 'grupo_por_atributo' [FIJADO]
```

---

## Qué buscar cuando lo pruebes (lo que me interesa que intentes romper)

1. **Un objeto al que le falta un atributo.** Por ejemplo
   `a(color=rojo); b(color=rojo); c(forma=cubo)`. Aquí el color de `c` **no se sabe** y el sistema
   debería **callarse**, no suponer.
2. **Repetir el mismo nombre** muchas veces en 0.1 (`taza,taza,taza`).
3. **Dos atributos iguales pero con nombre distinto** (`color=rojo` frente a `tono=rojo`): no deberían
   confundirse.
4. **Un solo objeto** con atributos: no debería decir que es un grupo.
5. **Pedir un grupo que no existe** (`color=verde:` cuando nadie es verde).
6. Cosas tuyas: nombres con espacios, mayúsculas y minúsculas, números (`caja1,caja2`).

Si algo te chirría, dímelo con **la línea exacta que escribiste y lo que esperabas**. Se corrige desde la
base: primero el conocimiento escrito, después el código.

---

## Los archivos, por si quieres mirar

| Archivo | Qué es |
|---|---|
| `E:\Euclides\conocimiento\*.kn` | El saber, en texto plano. Se puede leer y editar |
| `E:\Euclides\sistema\motor.py` | El programa que lee, decide y explica |
| `E:\Euclides\pruebas\` | Las pruebas del proyecto |
| `E:\Euclides\mis_casos.txt` | **Tus casos** |
| `E:\Euclides\PROBAR.bat` | El lanzador de doble clic |
| `E:\Euclides\PROGRESO.md` | Qué está hecho, qué falla, qué toca |
| `E:\Euclides\diario\` | Lo que se hizo cada día y lo que se midió |
