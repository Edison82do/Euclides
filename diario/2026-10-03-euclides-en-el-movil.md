# Diario — 3 de octubre de 2026 — Euclides en el móvil

## Lo que pidió Carlos

«Puedes enviarme por aquí el archivo con el código a ver si lo puedo ejecutar en mi celular.»

## Qué se hizo

Un **archivo único** que se ejecuta solo, sin carpetas ni instalación de nada más:

`E:\Euclides\movil\euclides_movil.py` — 93 KB, **15 archivos .kn embebidos**.

### Cómo funciona

El código del proyecto no se toca. El generador (`herramientas\empaquetar_movil.py`) lee
`motor.py`, `probar.py`, `mis_casos.txt` y los 15 `.kn`, los **embebe como texto** dentro de un
lanzador, y el lanzador al arrancar:

1. los escribe en una carpeta temporal,
2. y corre el probador tal cual con `runpy`.

Así no hay que adaptar nada, y si mañana cambia el motor, basta volver a generar.

### Por qué hace falta hacer esto

El proyecto **ya era portable** (Python puro, sin librerías de terceros, sin nada de Windows dentro
del motor), pero la forma de lanzarlo no: `PROBAR.bat` es de Windows, y `probar.py` busca el
conocimiento en `..\conocimiento` al lado suyo. El móvil necesita **un solo archivo** porque las
apps de Python para Android (Pydroid 3) abren ficheros sueltos, no carpetas.

### Probado de verdad (no supuesto)

```
1) pregunta suelta:      py -3 euclides_movil.py "contar: a, b, c"
                         -> EMPAREJAMIENTO: a -> uno ; b -> dos ; c -> tres   [emparejado]
2) modo casos:           py -3 euclides_movil.py --casos
                         -> mis casos: 35 bien, 0 fallan
3) interactivo:          revisar / subitizar / salir
                         -> palabra_repetida ; reconocido ; Hasta luego.
```

Los tres modos, con la salida real delante.

## Aviso honesto para Carlos

En el móvil hace falta una **app que ejecute Python** (Pydroid 3 en Android, gratis). El código en sí
no necesita nada: no usa internet, ni librerías, ni permisos.

Lo que **no** lleva el móvil: el probador con doble clic (`PROBAR.bat`) y las pruebas del proyecto
(`pruebas\`). El archivo móvil lleva el sistema y el probador; el ZIP lleva todo, para Termux o para
el PC.

## Archivos

- `E:\Euclides\movil\euclides_movil.py` — el archivo único (93 KB).
- `E:\Euclides\movil\Euclides_codigo.zip` — el proyecto completo (212 KB).
- `E:\Euclides\herramientas\empaquetar_movil.py` — el generador, por si hay que rehacerlo.
