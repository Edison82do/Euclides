# Diario — 3 de octubre de 2026 — Corrección de vocabulario (la contradicción del «grupo»)

## Lo que encontró Carlos

Probando el sistema escribió:

```
casa(color=blanco); carro(color=negro)
```

y razonó: «no son grupo con relación al color, pero sí son grupo al ser dos objetos distintos
según la regla anterior».

Tenía razón, y lo que había descubierto era una **contradicción dentro del sistema**:

```
casa,carro                                -> grupo        (unidad 0.1)
casa(color=blanco); carro(color=negro)    -> no_grupo     (unidad 0.2)
```

El mismo par de objetos recibía respuestas opuestas. Eso, en un sistema cuyo valor entero es que
nada se contradiga y todo se pueda rastrear, es un fallo de los gordos.

## La causa

La palabra **grupo** se estaba usando con dos sentidos distintos:

- **0.1** llamaba grupo a «hay varias entidades distintas» → *pluralidad*.
- **0.2** llamaba grupo a «comparten un atributo» → *homogeneidad*.

Y son **dos propiedades independientes**: hay conjuntos de varias cosas sin criterio común
(`casa, carro`) y conjuntos de varias cosas con criterio común (`casa_A, casa_B`, las dos casas).
Decir `no_grupo` en el segundo caso **negaba** lo que la unidad anterior había afirmado.

**De dónde venía:** del `PLAN.md` original, que en la prueba de dominio de 0.1 ya escribía
«distingue un objeto de un grupo». La ambigüedad estaba heredada del plan y yo la arrastré al código
sin verla. Ejemplo claro de por qué la regla 11 (preguntar antes de cambiar el diseño) existe.

## El arreglo (aprobado por Carlos antes de tocarlo)

| Unidad | Antes | Ahora |
|---|---|---|
| 0.1 | `obj_individual` / `grupo` | **`un_objeto` / `varios_objetos`** (0.1 no habla de grupos) |
| 0.2 reconocer | `grupo_atributo` / `no_grupo` | **`grupo_por_atributo` / `sin_atributo_comun`** |
| 0.2 con una sola cosa | `no_grupo` | **`una_sola_entidad`** (la pregunta de grupo no aplica) |

Con eso, la misma pareja ya no se contradice:

```
casa,carro                                -> varios_objetos
casa(color=blanco); carro(color=negro)    -> sin_atributo_comun   (son varios, pero sin criterio)
casa_A(color=blanco); casa_B(color=blanco)-> grupo_atributo       (varios, y comparten el color)
```

La palabra **GRUPO queda reservada a 0.2**, y siempre significa «varios objetos que además comparten
un atributo con el mismo valor». Es justo donde el plan la pone.

## Lo que se tocó

1. `conocimiento\pluralidad.kn` — reescrito: ya no habla de grupos, y deja anotado el error corregido.
2. `conocimiento\reglas_0_1.kn` — conclusiones `un_objeto` / `varios_objetos`.
3. `conocimiento\reglas_0_2.kn` — conclusiones `grupo_por_atributo` / `sin_atributo_comun` /
   `una_sola_entidad`, con la aclaración de que `sin_atributo_comun` **no** niega la pluralidad.
4. `PLAN.md` — corregida la prueba de dominio de 0.1.
5. `sistema\motor.py` — el encabezado y la pregunta de 0.1; la lógica no cambió (las conclusiones son datos).
6. `pruebas\test_0_1.py` y `pruebas\test_0_2.py` — expectativas actualizadas.
7. `probar.py` y `mis_casos.txt` — alias y textos, para que Carlos pueda seguir escribiendo
   `objeto` / `varios` y no tenga que recordar los nombres internos.

## Medición — salida real

```
Todas las pruebas del proyecto: 22/22   RESULTADO GLOBAL: VERDE
Casos de Carlos: 12 bien, 0 fallan
casa,carro                             -> varios_objetos
casa(color=blanco); carro(color=negro) -> sin_atributo_comun
casa_A(color=blanco); casa_B(color=blanco) -> grupo_atributo (comparten color)
```

## Fallo secundario, en el camino

Al reescribir `pluralidad.kn` el motor se negó a cargarlo: **el formato `.kn` no admite un ítem de
lista partido en dos líneas**. Queda anotado como limitación conocida del lector; el ítem va en una
sola línea.

## Lección

**El vocabulario es parte de la base de conocimiento, no una etiqueta cosmética.** Una palabra usada
con dos sentidos en el mismo sistema produce contradicciones que el código no puede arreglar. Y fue
Carlos, razonando sobre lo que el sistema le contestaba, quien la encontró. Pruébalo tú: eso es lo
que la ha destapado.
