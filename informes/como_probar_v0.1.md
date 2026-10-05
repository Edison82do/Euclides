# Cómo probar Euclides

**Versión 0.1 — 3 de octubre de 2026**
**Unidad que se puede probar: 0.1 — objetos individuales y grupos**

---

## En una línea

Doble clic en **`E:\Euclides\PROBAR.bat`**. Se abre una ventana negra, corre tus casos y te deja escribir
los tuyos. Para salir, escribe `salir`.

No hace falta saber programar. Lo único que se teclea son listas de cosas separadas por comas.

---

## Qué hace el sistema hoy (y qué no)

| | |
|---|---|
| **Sabe** | Decidir si una escena es **un objeto individual** o **un grupo** (dos o más entidades distintas) |
| **No sabe todavía** | Contar. No dice "hay tres". No agrupa por criterio. No compara cantidades |

Esto es a propósito: la unidad 0.1 es solo distinguir "uno" de "varios".

---

## Cómo se escribe una escena

Se ponen los objetos separados por comas. **Si repites un nombre, el sistema entiende que es la misma
entidad señalada otra vez.** Si pones nombres distintos, son entidades distintas.

| Escribes | El sistema entiende | Responde |
|---|---|---|
| `silla` | una entidad | objeto individual |
| `silla,mesa` | dos entidades distintas | grupo |
| `silla,silla` | la misma silla, señalada dos veces | objeto individual |
| `libro,lapiz,vaso` | tres entidades distintas | grupo |
| *(Enter sin escribir nada)* | escena vacía | "no decidible" |

---

## Las tres formas de probar

**1. La ventana interactiva (lo normal).**
Doble clic en `PROBAR.bat`. Primero corre tus casos guardados y luego te pregunta `escena>`. Escribes,
pulsas Enter y te contesta con la explicación completa de por qué ha dicho eso.

Órdenes dentro de la ventana:

- `casos` — volver a correr tus casos guardados
- `ayuda` — recordar cómo se escribe
- `salir` — terminar

**2. Una escena suelta, sin entrar en la ventana.**

```
py -3 E:\Euclides\probar.py "silla,mesa"
```

**3. Tus casos guardados, todos de golpe.**

```
py -3 E:\Euclides\probar.py --casos
```

---

## Dónde escribes TUS casos

Archivo: **`E:\Euclides\mis_casos.txt`** (se abre con el Bloc de notas).

Cada línea es un caso, con este formato:

```
escena | lo que espero | comentario
```

- **escena** — las cosas separadas por comas
- **lo que espero** — `objeto`, `grupo`, `no_decidible`, o `?` si solo quieres ver qué responde
- **comentario** — texto libre, opcional

Ejemplo:

```
taza,taza,taza   | objeto | la misma taza señalada tres veces
coche,arbol,perro| grupo  | tres cosas distintas
```

Guarda el archivo y vuelve a lanzar el probador: **se recarga solo**. No hay que tocar nada más.

Los `#` al principio de una línea son comentarios y se ignoran.

---

## Por qué el sistema explica lo que dice

Cada respuesta sale con su **traza**: qué regla se ha probado, en qué orden, cuál ha decidido y **qué
conocimiento escrito la respalda**. El sistema nunca dice "porque sí". Un ejemplo real:

```
ESCENA: silla, mesa
  identificadores distintos: mesa, silla
  reglas probadas, en orden:
    - escena_sin_entidades : escena_vacia(escena) -> falso
    - escena_con_varias_entidades : varios_distintos(escena) -> cierto
RESULTADO: grupo
  lo decide la regla 'escena_con_varias_entidades'
  respaldado por el conocimiento 'pluralidad' (Pluralidad de una escena) [FIJADO]
```

---

## Qué buscar cuando lo pruebes (esto es lo que me interesa que intentes romper)

1. **Repetir el mismo nombre** muchas veces — ¿sigue diciendo "objeto individual" o se confunde?
2. **Dos cosas distintas que se llaman igual** (`silla_A,silla_B` se escribe distinto, pero prueba
   también a escribir dos veces exactamente `silla` en una lista más larga como `silla,mesa,silla`).
3. **Escena vacía** — ¿se calla o inventa algo?
4. **Cosas raras que se te ocurran**: nombres con espacios, mayúsculas y minúsculas, números
   (`caja1,caja2`).

Si algo te parece mal, **dímelo con la línea exacta que escribiste y lo que esperabas**. Con eso lo
corrijo desde la base: primero el conocimiento escrito, después el código.

---

## Los archivos, por si quieres mirar

| Archivo | Qué es |
|---|---|
| `E:\Euclides\conocimiento\*.kn` | El saber, escrito en texto plano. Se puede leer y editar |
| `E:\Euclides\sistema\motor.py` | El programa que lee, decide y explica |
| `E:\Euclides\pruebas\` | Las pruebas del proyecto |
| `E:\Euclides\mis_casos.txt` | **Tus casos** |
| `E:\Euclides\PROBAR.bat` | El lanzador de doble clic |
| `E:\Euclides\PROGRESO.md` | Qué está hecho, qué falla, qué toca |
| `E:\Euclides\diario\` | Lo que se hizo cada día y lo que se midió |
