# -*- coding: utf-8 -*-
"""
PROBADOR de Euclides - para que Carlos pruebe el sistema sin tocar codigo.

Formas de usarlo:
  1) Doble clic en PROBAR.bat              (lo mas facil)
  2) python probar.py                      -> modo interactivo
  3) python probar.py "silla,mesa"         -> una pregunta suelta
  4) python probar.py --casos              -> solo tus casos de mis_casos.txt
  5) python probar.py --archivo mis_pruebas.txt  -> los casos de OTRO archivo (MIS_PRUEBAS.bat)

QUE SE PUEDE ESCRIBIR (todo en la misma ventana):

  0.1  UN OBJETO o VARIOS ->  nombres separados por comas
        silla
        silla,mesa
        silla,silla

  0.2  FORMAN GRUPO?    ->  objetos con atributos, separados por punto y coma
        caja_A(color=rojo,forma=cubo); caja_B(color=rojo,forma=esfera)

  0.2  DAME EL GRUPO DE ->  el criterio, dos puntos, y la escena
        color=rojo: caja_A(color=rojo,forma=cubo); caja_B(color=azul,forma=cubo)

  0.3  PERTENECE        ->  empieza por 'pertenece', el criterio, ':' y los objetos
        pertenece color=rojo: taza(color=rojo); plato(color=azul)

  1.0  SUBITIZAR        ->  una figura de 3 filas separadas por '/' (x = elemento, . = hueco)
        subitizar: x.x/.../x.x

  2.1  CONTAR           ->  la coleccion, separada por comas
        contar: silla_1, silla_2, silla_3

  2.1  REVISAR          ->  la coleccion, '/', y las palabras que le pusieron
        revisar: a,b,c / uno,dos,tres

  2.2  SIGUIENTE/ANTERIOR  ->  que va antes y despues en la lista
        siguiente: tres   /   anterior: tres

  2.2  RECITAR          ->  la lista desde esa palabra hasta donde sabe
        recitar: ocho

  2.2  REVISAR_SECUENCIA ->  una recitacion dicha por otro
        revisar_secuencia: uno,dos,cuatro

  2.3  CUANTOS HAY      ->  cuenta la coleccion y da la cantidad
        cuantos: silla_1, silla_2, silla_3

  2.4  DAME             ->  Give-N: le das un monton y te da esa cantidad de ahi
        dame: a,b,c,d,e / tres

  2.4  TIENE            ->  este conjunto tiene esa cantidad?
        tiene: a,b,c / tres

  2.5  ORDEN            ->  cuenta la coleccion de dos maneras: la cantidad no cambia
        orden: a,b,c

  2.5  CONTEO           ->  juzga un recorrido de conteo ajeno
        conteo: c,a,b / uno,dos,tres

  2.6  MISMA_CANTIDAD   ->  dos colecciones, misma cantidad? (aunque sean cosas distintas)
        misma_cantidad: silla_1,silla_2,silla_3 / sonido_1,sonido_2,sonido_3

  3.1  CIFRA            ->  de la palabra a la cifra:   cifra: tres
  3.1  PALABRA          ->  de la cifra a la palabra:   palabra: 3
  3.1  CIFRA_DE         ->  de la cantidad a la cifra:  cifra_de: a,b,c

  3.2  EL CERO          ->  una coleccion vacia tiene cantidad CERO (no es "no se sabe")
        cuantos:              -> cero
        cifra_de:             -> 0

  3.3  SECUENCIA DE NUMEROS  ->  OJO: hay DOS listas
        listas                -> las dos listas y en que se diferencian
        anterior: uno         -> cero   (en los NUMEROS; en la lista de CONTAR el uno es el primero)
        siguiente: cero       -> uno
        siguiente: diez       -> sin_numero  ("diez" no tiene sitio en los numeros)
        NOTA: siguiente: y anterior: van sobre la secuencia de NUMEROS (cero..nueve);
              recitar: sigue sobre la lista de CONTAR (que ahora llega hasta cien).

  3.4  EL PUENTE  ->  cantidad, palabra y cifra son lo mismo dicho de tres maneras
        caminos               -> los SEIS caminos entre las tres representaciones
        puente: a,b,c         -> la coleccion de las tres maneras (ensena el recuento)
        dame: a,b,c,d / 3     -> el sexto camino: de la CIFRA a los objetos
        subitizar: x.x/.../x.x -> el camino CORTO (de un vistazo) tambien da la cifra

  4.1  COMPARAR CANTIDADES  ->  cual tiene mas (se dice con PALABRAS, no con simbolos)
        comparar: a,b,c / d,e  -> mas         (la PRIMERA tiene mas)
        comparar: a,b / c,d,e  -> menos
        comparar: a,b / c,d    -> tantos_como (las dos lo mismo)
        comparar: a,b,c        -> NO ENTIENDO: hacen falta DOS colecciones
        OJO: el TAMANO de los objetos NO cuenta; la cantidad son las cosas.

  4.2  COMPARAR NUMEROS  ->  con los SIMBOLOS >, <, = (van SOLO entre cifras)
        comparar_cifras: 3 / 2   -> >      (tres es MAYOR que dos)
        comparar_cifras: 2 / 3   -> <
        comparar_cifras: 3 / 3   -> =
        DE DONDE SALE: en la secuencia de numeros, el que viene DESPUES es el mayor.
        Y CUADRA CON LAS CANTIDADES: 3 > 2 porque tres cosas son mas que dos (unidad 4.1).

  5.1  COMPONER Y DESCOMPONER  ->  las partes y el todo (el cimiento de la suma y la resta)
        descomponer: a,b,c,d,e   -> 0+5,1+4,2+3   (todas las maneras de partir en DOS)
                                    NO repite 3+2: es la misma que 2+3 (el orden no importa)
                                    Y el cero es una parte valida (0+5)
        descomponer:             -> el_cero_no_se_parte (de cero no hay nada que partir)
        componer: a,b / c,d,e    -> cinco   (dos y tres son cinco)

  5.2  LA SUMA  ->  el signo + y el signo =  (el = es "son lo mismo", NO "pon el resultado")
        sumar: a,b,c / d,e       -> 3 + 2 = 5   (AGREGACION: juntar dos montones que ya estan)
        anadir: a,b,c / d,e      -> 3 + 2 = 5   (AUMENTACION: el monton crece)
                                    las dos dan lo mismo, pero la HISTORIA es distinta
        Los terminos: SUMANDOS (los que se juntan) y SUMA (el resultado).
        Y se verifica por la vuelta: partiendo el 5 tiene que salir "dos y tres" (unidad 5.1).

  5.3  LAS TRES ENTRADAS  ->  OJO: los grupos NO se mezclan
        cantidad -> a, b, c      |      cifra -> 3      |      palabra -> tres
        un OBJETO no se puede llamar como un NUMERO (antes 'sumar: 3 / 2' daba '1 + 1 = 2', falso)
        Y AHORA las ordenes de NUMEROS aceptan cifra O palabra:
        siguiente: 3   /   anterior: 3   /   recitar: 3
        comparar_numeros: dos / 3     -> <      (mezclando palabra y cifra)
        sumar_numeros: 3 + 2          -> 3 + 2 = 5   (o 'dos + tres', da igual)
        descomponer_numero: 5         -> 0+5,1+4,2+3   (partir un NUMERO)
        Y las ordenes de CANTIDAD dicen que no si les das un numero: sumar: 3 / 2 -> grupo_equivocado

  5.4  LA RESTA (quitar)  ->  el signo -, con la historia "primero, luego, ahora"
        quitar: a,b,c,d,e / dos   -> 5 - 2 = 3   (reduccion: el monton DISMINUYE)
        quitar: a,b / tres        -> no_hay_bastantes  (¡no se puede quitar mas de lo que hay!)
        restar_numeros: 5 - 2     -> 5 - 2 = 3   (numeros, sin objetos)
        Los terminos: MINUENDO (de donde), SUSTRAENDO (lo que se quita), RESULTADO (lo que queda).
        Y se verifica por la vuelta: 3 + 2 = 5 (la suma deshace la resta)
        OJO: quitar NO es partir.  En quitar, los que se van SE VAN (unidad 5.1 es partir).

  5.5  LA DIFERENCIA  ->  el HUECO entre dos cantidades (la tercera estructura de la resta)
        diferencia: a,b,c,d,e / a,b,c   -> 2    (cuantos mas tiene una, cuantos menos la otra)
        diferencia: a,b,c / a,b,c       -> cero (¡y el cero es una cantidad!)
        diferencia_numeros: 5 / 3       -> 2    (la diferencia entre numeros)
        ¡AQUI NO SE QUITA NADA!  Los dos montones siguen enteros: nadie se va.
        Se empareja uno con uno, y los que se quedan SIN PAREJA son el hueco.
        Se escribe de DOS maneras: 5 - 3 = 2  y  3 + 2 = 5 (contar hacia adelante).

  7.3  SUMAR POR COLUMNAS  ->  unidad con unidad, decena con decena, y EL LLEVARSE
        columnas: 47 + 15      -> 47 + 15 = 62   (7+5=12: anoto 2 y ME LLEVO 1; y 4+1+1=6)
        columnas: 28 + 15      -> 28 + 15 = 43   (8+5=13: anoto 3 y me llevo 1)
        columnas: 5 + 3        -> 5 + 3 = 8      (SIN llevarse: no pasa de nueve)
        columnas: 60 + 50      -> 60 + 50 = 110  (MEJORA 7.6: antes no_alcanza; ver 7.6)
        CADA SITIO CON SU SITIO.  Y lo que pasa de nueve en las unidades es UNA DECENA que sube
        a la columna de las decenas: ESO es el llevarse.  No es un truco: es RE-AGRUPAR (diez
        unidades hacen una decena, unidad 6.2).  Y lo que se lleva NUNCA puede ser mas de 1
        (9+9=18, o sea una decena).
        Y AHORA 'sumar_numeros:' con dos cifras TAMBIEN funciona, usando este metodo:
        sumar_numeros: 32 + 15  -> 32 + 15 = 47  (por columnas, no cuenta uno a uno)
        ESTA ES LA NOTA 7 DE CARLOS, palabra por palabra.

  7.4  LA RESTA CON LOS DEDOS  ->  se toma el PRIMERO, se van BAJANDO los del segundo
        dedos: 9 - 4           -> 9 - 4 = 5  (se levantan 9, se bajan 4, quedan 5)
        dedos: diez - siete    -> 10 - 7 = 3
        dedos: 9 - 9           -> 9 - 9 = 0  (quitar todo deja cero)
        dedos: 4 - 9           -> no_hay_bastantes  (no hay resta negativa)
        dedos: 45 - 12         -> no_caben_en_los_dedos (lo que tiene que caber es EL SEGUNDO)
        OJO (lo cazo Carlos): el PRIMERO SI puede pasar de diez.  Los diez dedos son la VENTANA DE
        LOS ULTIMOS DIEZ numeros, y el ultimo es el minuendo: para 12 - 5 van DEL 3 AL 12.  Y asi
        cabe 45 - 7 (dedos del 36 al 45: se bajan 7 y quedan 38).  Lo que tiene que caber es LO QUE
        SE BAJA (el segundo), no el primero.  Asi queda IGUAL que la suma (7.1), donde el total
        tampoco tiene que caber.
        (Esta es la nota 3 de Carlos, 4 oct 2026.)

  7.5  RESTAR POR COLUMNAS  ->  columna a columna, y EL INTERCAMBIO de una decena
        columnas: 72 - 45      -> 72 - 45 = 27  (2-5 no llega: 72 = 6 dec y 12 u; 12-5=7 y 6-4=2)
        columnas: 58 - 27      -> 58 - 27 = 31  (SIN cambiar nada: 8-7=1 y 5-2=3)
        columnas: 43 - 17      -> 43 - 17 = 26  (NO da 34 ni 36: los errores tipicos)
        columnas: 45 - 72      -> no_hay_bastantes (no hay resta negativa)
        columnas: 150 - 40     -> 150 - 40 = 110 (MEJORA 7.6: antes no_alcanza)
        SI LAS UNIDADES DE ARRIBA NO LLEGAN, NO SE DA LA VUELTA A LA RESTA: 5 - 2 = 3 seria
        FALSO.  Lo que pasa es que SE CAMBIA una decena por diez unidades (72 = 6 decenas y 12
        unidades, y sigue siendo 72).  Y ESO NO ES PEDIR PRESTADO: no se devuelve nada.  Es la
        MISMA moneda que el llevarse de la suma (7.3), al reves: alli diez unidades subian como
        una decena; aqui una decena baja como diez unidades.
        OJO: al cambiarla, la columna de las decenas BAJA de 7 a 6.  Si se olvida, sale diez de
        mas.  Y cada resta de columna se hace con EL MECANISMO (7.4), no de memoria.

  6.5  PARTIR EN DECENAS Y UNIDADES  ->  cuanto vale CADA CIFRA
        partir: 47              -> 4 decenas + 7 unidades = 47
        juntar_decenas: 4 / 7   -> cuarenta y siete -> 47
        La PRIMERA cifra son DECENAS y la ultima son UNIDADES.  Y cada cifra vale POR SU SITIO:
        en 47 el 4 vale CUARENTA, no cuatro.  OJO con el error tipico (lo documenta Oak): sumar
        las cifras como si valieran lo mismo (4 + 7 = 11) es 'transponer los digitos'.
        Y los numeros raros no se dicen raro: juntar_decenas: 3 / 12 son cuarenta y dos, NO
        'treinta y doce' (lo documenta NZ Maths).
        OJO: partir NO es descomponer.  'descomponer_numero: 5' da las partes que SUMAN
        (0+5, 1+4, 2+3); 'partir: 47' da las DECENAS y las UNIDADES.  Son cosas distintas.
        ESTO ES LO QUE HACE FALTA PARA LAS COLUMNAS (unidad 7.3): hay que saber partir antes.

  6.3  LA TABLA DE 100  ->  el sitio de cada numero (fila = DECENAS, columna = UNIDADES)
        palabra: 47            -> cuarenta y siete   (YA lee cifras de dos digitos)
        cifra: cuarenta y siete -> 47               (la vuelta)
        sitio: 47              -> 4 decenas y 7 unidades (fila 4, columna 7)
        sitio: 100             -> 10 decenas y 0 unidades (fila 9, columna 10)
        sitio: 101             -> 1 centena, 0 decenas y 1 unidad (MEJORA 6.7; antes
                                  fuera_de_la_tabla: sigue fuera de la tabla de 100, pero se parte)
        tabla                  -> la tabla de 100 entera, fila a fila
        Y el MISMO numero se lee igual por TODAS las puertas (una sola verdad): nombre:, palabra:,
        sitio:, comparar_cifras:, cifra_de:, dedos:...  Antes de la 6.3, cuatro de esas puertas
        decian que no sabia leerlo.

  6.2  AGRUPAR DE DIEZ EN DIEZ  ->  el diez pasa a ser UNA cosa (una DECENA)
        agrupar: a,b,c,d,e,f,g,h,i,j,k,l,m  -> una decena y tres  (trece)
        agrupar: a,b,c,d,e,f,g,h,i,j        -> una decena         (diez justo)
        agrupar: a,b,c,d,e,f,g,h,i          -> no_hay_decena  (nueve: no llega a diez)
        agrupar:                             -> cero             (el vacio es CERO, unidad 3.2)
        Los objetos se cogen DE DIEZ EN DIEZ y cada monton se cuenta como UNA SOLA COSA.  Eso es
        el 'unitising' (NCETM) y es lo que hace posible el valor posicional.  Y CUIDADO con el
        error tipico (lo documenta Oak): las DECENAS se cuentan de diez en diez, las UNIDADES
        DE UNO EN UNO (no sigas de diez en diez al llegar a las unidades).
        Y el ORDEN no cambia nada: el sistema lo COMPRUEBA agrupando al reves.

  6.1  CONTAR HASTA 100  ->  los nombres SE CONSTRUYEN, no estan memorizados
        nombre: 47               -> cuarenta y siete (y ENSENA como se construyo)
        numero: cuarenta y siete -> 47              (la vuelta)
        decenas                  -> las decenas, y el ERROR DE DECENA explicado
        Solo hay que saberse 24 palabras (1-10, 11-15, 20, 100 y las decenas); las otras 76
        salen de tres formaciones: dieci+u, veinti+u y 'decena y unidad'.
        Y la secuencia de contar llega al CIEN en TODO el sistema (antes llegaba al diez).

  7.1  EL METODO DE LOS DEDOS  ->  el MECANISMO de sumar (mecanico hasta nuevo aviso)
        dedos: 8 + 5     -> el metodo paso a paso: se ANOTA el primero (la pizarra), se
                            cogen los dedos del segundo, se cuenta HACIA ADELANTE desde el
                            primero, y el ultimo numero dicho es el total.
        dedos: ocho + doce        -> no_caben_en_los_dedos (el segundo no puede pasar de 10)
        dedos: 5 + 0              -> el total es el primero (no se levanta ningun dedo)
        Y ensena POR QUE es mejor que contar todo: 5 pasos frente a 13.
        (Desde la 6.3 tambien lee cifras de dos digitos: dedos: 47 + 3 -> 47 + 3 = 50.)

  7.2  DERIVAR (hacer diez)  ->  la OTRA via para sumar: usar lo que ya sabes, SIN contar
        derivar: 7 + 5      -> siete + cinco = doce, y lo ENSENA paso a paso:
                                al 7 le faltan 3; parto el 5 en 3 + 2; 7 + 3 = 10; 10 + 2 = 12
        derivar: 8 + 9      -> ocho + nueve = diecisiete   (el que casi NADIE tiene memorizado)
        derivar: 4 + 5      -> no_hace_falta   (no cruza el diez: se sabe directamente)
        derivar: doce + tres -> necesito_las_columnas  (mi 'hacer diez' es para UNA cifra)
        Y EL SISTEMA PRUEBA LAS DOS VIAS: ensena lo que dicen los dedos y lo que dice derivar,
        y comprueba que dan LO MISMO.  (Decision de Carlos: 'admite todo lo que sirva, los dedos
        y derivar; el que pruebe las dos'.)
        NO se sabe de memoria ni se usa calculadora: derivar COMBINA lo que ya sabes (partir, 5.1)
        y llegar a diez (6.1).  Y esta medido: los que saben usan hechos DERIVADOS, no contar.

  6.7  LA CENTENA  ->  diez decenas son UNA centena, y la escalera sigue
        centena                -> la escalera: 10 u = 1 d ; 10 d = 1 c ; 10 c = 1 unidad de mil
        centena: 247           -> 2 centenas, 4 decenas y 7 unidades ('doscientos cuarenta y siete')
        centena: 204           -> 2 centenas, 0 decenas y 4 unidades  (el cero es MARCADOR de
                                  posicion; y OJO: 204 tiene VEINTE decenas en total, NZ Maths)
        sitio: 247 / partir: 247  -> lo mismo (pasan de cien: se parten en centenas)
        nombre: 247            -> el ciento de MEMORIA ('doscientos') + el resto de la 6.1
        numero: quinientos     -> 500      (quinientos, setecientos y novecientos son IRREGULARES)
        Y NO se dice '2 x 100': el sistema no sabe multiplicar.  Se dice '2 centenas'.
        La secuencia de contar llega a MIL en todo el sistema.

  7.6  COLUMNAS CON LA CENTENA  ->  LA NOTA 7 ENTERA: unidad, decena y CENTENA
        columnas: 247 + 385    -> 632   (dos llevadas: a las decenas y a las centenas)
        columnas: 999 + 1      -> 1000  (tres llevadas seguidas: sale la unidad de mil)
        columnas: 500 - 247    -> 253   (A TRAVES DE UN CERO: 1 centena por 10 decenas, y 1 de
                                         esas decenas por 10 unidades -> 4 c, 9 d, 10 u.  NO 347)
        columnas: 900 + 200    -> no_alcanza  (pasa de mil)
        Es EL MISMO metodo de la 7.3 y la 7.5, con una columna mas.  Cada columna con su
        mecanismo (los dedos); ninguna cuenta de memoria.  sumar_numeros:, restar_numeros: y
        diferencia_numeros: con varias cifras usan ESTE metodo (antes restar_numeros: 50 - 27
        decia 'None - None', y sumar_numeros: 900 + 900 reventaba).

  R.1  RESOLVER UN PROBLEMA  ->  aplicar TODO lo que sabe, y DESCARTAR con razones
        problema: Ana tiene 5 manzanas. Le dan 3 mas. Cuantas tiene ahora?          -> 8
        problema: Hay 8 pajaros. Se van 3. Cuantos quedan?                          -> 5
        problema: Juan tiene 7 y Pedro tiene 4. Cuantas mas tiene Juan que Pedro?   -> 3
        problema: Ana tiene 8 manzanas. Tiene 3 mas que Luis. Cuantas tiene Luis?   -> 5
                  (dice MAS y es una RESTA: el que falta es el que tiene menos)
        problema: Marta tiene 12. Se come 4. Luego compra 10. Cuantos tiene ahora?  -> 18 (dos pasos)
        problema: Hay 4 peces. Se van 9. Cuantos quedan?                            -> sin_solucion
        problema: El perro come huesos. Cuantos tiene?                              -> no_entiendo
        ES LA NOTA DE CARLOS DEL 3 OCT: no es que sepa que hacer; es que APLIQUE lo que sabe y
        combinaciones, CON DESCARTE.  En cada paso prueba TODOS sus conocimientos (anadir, quitar,
        juntar, la diferencia, la parte que falta, las vueltas...) y ensena por que descarta cada
        uno.  La operacion NUNCA se elige por la palabra.  Cada cuenta se hace por columnas (con
        los dedos en cada columna) y se verifica por la vuelta.  Lee con FORMAS escritas en
        conocimiento/enunciados.kn: si una frase no encaja, dice NO ENTIENDO (no adivina).

  Los atributos van entre parentesis como nombre=valor, separados por comas;
  las cosas entre si van separadas por punto y coma.
  Si repites un nombre en una escena 0.1, es la MISMA entidad senalada otra vez.
"""

import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(RAIZ, "sistema"))

import motor  # noqa: E402
from motor import cargar_conocimiento  # noqa: E402

ARCHIVO_CASOS = os.path.join(RAIZ, "mis_casos.txt")

# Como se puede escribir la respuesta esperada en mis_casos.txt
ALIAS = {
    "objeto": "un_objeto",
    "uno": "un_objeto",
    "grupo": "varios_objetos",       # en 0.1, "grupo" significaba "varios objetos"
    "varios": "varios_objetos",
    "nada": "no_decidible",
    "vacio": "no_decidible",
}

# Unidades cuyas respuestas son palabras de la lista o etiquetas propias: aqui "uno" es UNO,
# no "un_objeto".  (La misma palabra con dos sentidos en unidades distintas ya nos fallo una vez.)
SIN_ALIAS = ("cuantos", "siguiente", "anterior", "recitar", "revisar_secuencia", "dame", "tiene",
             "orden", "conteo", "misma_cantidad", "cifra", "palabra", "cifra_de", "puente", "comparar")


def normalizar_esperado(texto_pregunta, esperado):
    """Traduce la respuesta esperada, PERO por unidad: en 2.2/2.3 'uno' es la cantidad, no 'un_objeto'."""
    e = esperado.strip().lower()
    if texto_pregunta.strip().lower().startswith(SIN_ALIAS):
        return e
    return ALIAS.get(e, e)

# La ayuda es EL MISMO TEXTO que la cabecera del fichero (el docstring de arriba).
# Antes habia DOS textos -- este y el docstring -- y se desfasaron: el que se veia con "ayuda"
# se quedo congelado en la unidad 3.1 mientras el docstring se actualizaba hasta la 7.3.
# Ahora es uno solo: no pueden volver a separarse.
AYUDA = (__doc__ or "").rstrip() + """

  Y tres ordenes sueltas (sin ":"):

    casos     volver a correr tus casos de mis_casos.txt
    ayuda     ver este texto
    salir     terminar
"""



# ------------------------------------------------------------------ preguntar

def preguntar(texto, saber):
    """Devuelve (respuesta normalizada, resultado completo).  Nunca revienta."""
    t = texto.strip()
    try:
        if t.lower().startswith("problema"):
            resto = t[len("problema"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            if not resto:
                return "no_entendido", None
            r = motor.decidir_R1_problema(resto, saber)
            return (str(r["valor"]) if r["conclusion"] == "resuelto" else r["conclusion"]), r
        if t.lower().startswith("cifra_de"):
            resto = t[len("cifra_de"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            r = motor.decidir_3_1_cifra_de(motor.escena_cantidad(resto, saber), saber)
            return r.get("cifra") or r["conclusion"], r
        if t.lower().startswith("cifra"):
            resto = t[len("cifra"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            r = motor.decidir_3_1_cifra(resto.lower(), saber)
            return r.get("cifra") or r["conclusion"], r
        if t.lower().startswith("palabra"):
            resto = t[len("palabra"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            r = motor.decidir_3_1_palabra(resto, saber)
            return r.get("palabra") or r["conclusion"], r
        if t.lower().startswith("misma_cantidad"):
            resto = t[len("misma_cantidad"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, _, der = resto.partition("/")
            r = motor.decidir_2_6_misma_cantidad(motor.escena_cantidad(izq, saber), motor.escena_cantidad(der, saber), saber)
            return r["conclusion"], r
        if t.lower().startswith("orden"):
            resto = t[len("orden"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            r = motor.decidir_2_5_orden(motor.escena_cantidad(resto, saber), saber)
            return r["conclusion"], r
        if t.lower().startswith("conteo"):
            resto = t[len("conteo"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, _, der = resto.partition("/")
            r = motor.decidir_2_5_conteo(
                motor.escena_cantidad(izq, saber), [p.strip().lower() for p in der.split(",") if p.strip()], saber)
            return r["conclusion"], r
        if t.lower().startswith("dame"):
            resto = t[len("dame"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            if "/" not in resto:
                return "no_entendido", None
            izq, _, der = resto.partition("/")
            r = motor.decidir_2_4_dame(motor.escena_cantidad(izq, saber), der.strip().lower(), saber)
            return ("cumplido" if r["conclusion"] == "cogido" else r["conclusion"]), r
        if t.lower().startswith("tiene"):
            resto = t[len("tiene"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, _, der = resto.partition("/")
            r = motor.decidir_2_4_tiene(motor.escena_cantidad(izq, saber), der.strip().lower(), saber)
            return r["conclusion"], r
        if t.lower().startswith("cuantos"):
            resto = t[len("cuantos"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            r = motor.decidir_2_3_cuantos(motor.escena_cantidad(resto, saber), saber)
            return r.get("cantidad") or r["conclusion"], r
        if t.lower().startswith("revisar_secuencia"):
            resto = t[len("revisar_secuencia"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            palabras = [motor.nombre_de_numero(p, saber)[0] for p in resto.split(",") if p.strip()]
            r = motor.decidir_2_2_revisar(palabras, saber)
            return r["conclusion"], r
        if t.lower().startswith("recitar"):
            resto = t[len("recitar"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            r = motor.decidir_2_2_recitar(motor.nombre_de_numero(resto, saber)[0], saber)
            if r["conclusion"] == "recitado":
                return "recitado:" + ",".join(r["tramo"]), r
            return r["conclusion"], r
        if t.lower().startswith("siguiente"):
            resto = t[len("siguiente"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            r = motor.decidir_3_3_siguiente(motor.nombre_de_numero(resto, saber)[0], saber)
            return r.get("siguiente") or r["conclusion"], r
        if t.lower().startswith("anterior"):
            resto = t[len("anterior"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            r = motor.decidir_3_3_anterior(motor.nombre_de_numero(resto, saber)[0], saber)
            return r.get("anterior") or r["conclusion"], r
        if t.lower().startswith("revisar"):
            resto = t[len("revisar"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, _, der = resto.partition("/")
            r = motor.decidir_2_1_revisar(
                motor.escena_cantidad(izq, saber), [p.strip().lower() for p in der.split(",") if p.strip()], saber)
            return r["conclusion"], r
        if t.lower().startswith("contar"):
            resto = t[len("contar"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            r = motor.decidir_2_1_contar(motor.escena_cantidad(resto, saber), saber)
            return r["conclusion"], r
        if t.lower().startswith("subitizar"):
            resto = t[len("subitizar"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            r = motor.decidir_1_0_subitizar(resto, saber)
            if r["conclusion"] == "reconocido":
                return "reconocido:%s" % r["etiqueta"], r
            return "no_reconocido", r
        if t.lower().startswith("nombre"):
            resto = t[len("nombre"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            # UNA SOLA VERDAD: la misma funcion que usa el explicador (antes habia aqui otra logica).
            r = motor.decidir_6_1_nombre(resto, saber)
            return r.get("palabra") or r["conclusion"], r
        if t.lower().startswith("numero"):
            resto = t[len("numero"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            r = motor.decidir_6_1_numero(resto, saber)
            return (str(r["valor"]) if r["conclusion"] == "numero" else r["conclusion"]), r
        if t.lower().startswith("columnas"):
            resto = t[len("columnas"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            if "-" in resto or "menos" in resto.lower():
                sep = "-" if "-" in resto else "menos"
                izq, s, der = resto.partition(sep)
                if not s:
                    return "no_entendido", None
                r = motor.decidir_7_5_columnas(izq.strip(), der.strip(), saber)
                if r["conclusion"] == "se_puede":
                    return r["expresion_cifras"], r
                return r["conclusion"], r
            sep = "+" if "+" in resto else "/"
            izq, s, der = resto.partition(sep)
            if not s:
                return "no_entendido", None
            r = motor.decidir_7_3_columnas(izq.strip(), der.strip(), saber)
            if r["conclusion"] == "se_puede":
                return r["expresion_cifras"], r
            return r["conclusion"], r
        if t.lower().startswith("partir"):
            resto = t[len("partir"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            if not resto:
                return "no_entendido", None
            r = motor.decidir_6_5_partir(resto, saber)
            if r["conclusion"] == "se_puede":
                return r["como_se_parte"], r
            return r["conclusion"], r
        if t.lower().startswith("juntar_decenas"):
            resto = t[len("juntar_decenas"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, _, der = resto.partition("/")
            if izq.strip() == "" or der.strip() == "":
                return "no_entendido", None
            r = motor.decidir_6_5_juntar_decenas(izq.strip(), der.strip(), saber)
            if r["conclusion"] == "se_puede":
                return r["dato"], r
            return r["conclusion"], r
        if t.lower().strip() == "tabla":
            return "la_tabla_de_100", None
        if t.lower().strip() in ("centena", "centenas"):
            return "la_escalera", None
        if t.lower().startswith("centena"):
            resto = t[len("centena"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            if not resto:
                return "no_entendido", None
            r = motor.decidir_6_7_centena(resto, saber)
            if r["conclusion"] == "se_puede":
                return r["dato"], r
            return r["conclusion"], r
        if t.lower().startswith("sitio"):
            resto = t[len("sitio"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            if not resto:
                return "no_entendido", None
            r = motor.decidir_6_3_sitio(resto, saber)
            if r["conclusion"] == "se_puede":
                return r["dato"], r
            return r["conclusion"], r
        if t.lower().startswith("agrupar"):
            resto = t[len("agrupar"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            r = motor.decidir_6_2_agrupar(motor.escena_cantidad(resto, saber), saber)
            if r["conclusion"] == "se_puede":
                return r["como_se_dice"], r
            return r["conclusion"], r
        if t.lower().startswith("derivar"):
            resto = t[len("derivar"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            sep = "+" if "+" in resto else "/"
            izq, s, der = resto.partition(sep)
            if not s:
                return "no_entendido", None
            r = motor.decidir_7_2_derivar(izq.strip(), der.strip(), saber)
            return r.get("expresion") or r["conclusion"], r
        if t.lower().startswith("dedos"):
            resto = t[len("dedos"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            if "-" in resto or "menos" in resto.lower():
                sep = "-" if "-" in resto else "menos"
                izq, s, der = resto.partition(sep)
                if not s:
                    return "no_entendido", None
                r = motor.decidir_7_4_resta_dedos(izq.strip(), der.strip(), saber)
                if r["conclusion"] == "se_puede":
                    return r["expresion"], r
                return r["conclusion"], r
            sep = "+" if "+" in resto else "/"
            izq, s, der = resto.partition(sep)
            if not s:
                return "no_entendido", None
            r = motor.decidir_7_1_dedos(izq.strip(), der.strip(), saber)
            return r.get("expresion") or r["conclusion"], r
        if t.lower().startswith("decenas"):
            r = motor.explicar_6_1_decenas(saber)
            return "las_decenas", {"texto": r}
        if t.lower().startswith("diferencia_numeros"):
            resto = t[len("diferencia_numeros"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, sep, der = resto.partition("/")
            if not sep:
                return "no_entendido", None
            r = motor.decidir_5_5_diferencia_numeros(izq.strip(), der.strip(), saber)
            return r.get("diferencia") or r["conclusion"], r
        if t.lower().startswith("diferencia"):
            resto = t[len("diferencia"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, sep, der = resto.partition("/")
            if not sep:
                return "no_entendido", None
            r = motor.decidir_5_5_diferencia(motor.escena_cantidad(izq, saber),
                                             motor.escena_cantidad(der, saber), saber)
            return r.get("diferencia") or r["conclusion"], r
        if t.lower().startswith("restar_numeros"):
            resto = t[len("restar_numeros"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            sep = "-" if "-" in resto else "/"
            izq, s, der = resto.partition(sep)
            if not s:
                return "no_entendido", None
            r = motor.decidir_5_4_restar_numeros(izq.strip(), der.strip(), saber)
            return r.get("expresion") or r["conclusion"], r
        if t.lower().startswith("quitar"):
            resto = t[len("quitar"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, sep, der = resto.partition("/")
            if not sep:
                return "no_entendido", None
            r = motor.decidir_5_4_quitar(motor.escena_cantidad(izq, saber), der.strip(), saber)
            return r.get("expresion") or r["conclusion"], r
        if t.lower().startswith("sumar_numeros"):
            resto = t[len("sumar_numeros"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            sep = "+" if "+" in resto else "/"
            izq, s, der = resto.partition(sep)
            if not s:
                return "no_entendido", None
            r = motor.decidir_5_3_sumar_numeros(izq.strip(), der.strip(), saber)
            return r.get("expresion") or r["conclusion"], r
        if t.lower().startswith("sumar"):
            resto = t[len("sumar"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, sep, der = resto.partition("/")
            if not sep:
                return "no_entendido", None
            r = motor.decidir_5_2_sumar(motor.escena_cantidad(izq, saber), motor.escena_cantidad(der, saber), saber)
            return r.get("expresion") or r["conclusion"], r
        if t.lower().startswith("anadir"):
            resto = t[len("anadir"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, sep, der = resto.partition("/")
            if not sep:
                return "no_entendido", None
            r = motor.decidir_5_2_anadir(motor.escena_cantidad(izq, saber), motor.escena_cantidad(der, saber), saber)
            return r.get("expresion") or r["conclusion"], r
        if t.lower().startswith("descomponer_numero"):
            resto = t[len("descomponer_numero"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            r = motor.decidir_5_3_descomponer_numero(resto, saber)
            if r["conclusion"] == "parejas":
                trozos = []
                for (ck, cm), (pk, pm) in zip(r["parejas_cifras"], r["parejas_palabras"]):
                    trozos.append("%s+%s" % (ck if ck is not None else pk,
                                             cm if cm is not None else pm))
                return ",".join(trozos), r
            return r["conclusion"], r
        if t.lower().startswith("descomponer"):
            resto = t[len("descomponer"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            r = motor.decidir_5_1_descomponer(motor.escena_cantidad(resto, saber), saber)
            if r["conclusion"] == "parejas":
                # Si una cifra no la tiene (el diez), se usa la palabra.
                trozos = []
                for (ck, cm), (pk, pm) in zip(r["parejas_cifras"], r["parejas_palabras"]):
                    trozos.append("%s+%s" % (ck if ck is not None else pk,
                                             cm if cm is not None else pm))
                return ",".join(trozos), r
            return r["conclusion"], r
        if t.lower().startswith("componer"):
            resto = t[len("componer"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, sep, der = resto.partition("/")
            if not sep:
                return "no_entendido", None
            r = motor.decidir_5_1_componer(motor.escena_cantidad(izq, saber), motor.escena_cantidad(der, saber), saber)
            return r.get("total") or r["conclusion"], r
        if t.lower().startswith("comparar_cifras") or t.lower().startswith("comparar_numeros"):
            if t.lower().startswith("comparar_numeros"):
                resto = t[len("comparar_numeros"):].strip()
            else:
                resto = t[len("comparar_cifras"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, sep, der = resto.partition("/")
            if not sep:
                return "no_entendido", None
            na, _ = motor.nombre_de_numero(izq, saber)
            nb, _ = motor.nombre_de_numero(der, saber)
            r = motor.decidir_4_2_comparar_cifras(na, nb, saber)
            return r.get("simbolo") or r["conclusion"], r
        if t.lower().startswith("comparar"):
            resto = t[len("comparar"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, sep, der = resto.partition("/")
            if not sep:
                return "no_entendido", None
            r = motor.decidir_4_1_comparar(motor.escena_cantidad(izq, saber), motor.escena_cantidad(der, saber), saber)
            return r["conclusion"], r
        if t.lower().startswith("caminos"):
            return "los_caminos", None
        if t.lower().startswith("puente"):
            resto = t[len("puente"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            r = motor.decidir_3_4_puente(motor.escena_cantidad(resto, saber), saber)
            if r["conclusion"] == "vacia":
                return "0", r
            if r["conclusion"] == "puente_sin_cifra":
                return r["cantidad"], r
            return r.get("cifra") or r["conclusion"], r
        if t.lower().startswith("pertenece"):
            resto = t[len("pertenece"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            izq, _, der = resto.partition(":")
            escena = motor.escena_cantidad(der, saber)
            criterio = motor.parsear_criterio(izq)
            rs = motor.decidir_0_3_pertenencia(escena, criterio, saber)
            return ",".join("%s:%s" % (r["objeto"]["id"], r["conclusion"]) for r in rs), rs
        if ":" in t and "=" in t.split(":", 1)[0] and "(" not in t.split(":", 1)[0]:
            izq, _, der = t.partition(":")
            r = motor.decidir_0_2_formar(motor.escena_cantidad(der, saber), motor.parsear_criterio(izq), saber)
            if r["conclusion"] == "grupo_formado":
                return "tiene:" + ",".join(r["miembros"]), r
            return r["conclusion"], r
        if "(" in t or ";" in t:
            r = motor.decidir_0_2_reconocer(motor.escena_cantidad(t, saber), saber)
            if r["conclusion"] == "grupo_atributo":
                return "grupo:" + ",".join(r["atributos_compartidos"]), r
            return r["conclusion"], r
        r = motor.decidir(motor.escena_0_1(t), saber)
        return r["conclusion"], r
    except motor.EntradaDelGrupoEquivocado:
        return "grupo_equivocado", None
    except ValueError:
        return "no_decidible", None
    except Exception:
        return "no_entendido", None


def _en_cifras(texto, saber):
    """'ocho + cinco = trece' -> '8 + 5 = 13' (solo para comparar en MIS PRUEBAS)."""
    mapa = dict(saber.get("_nombre_a_valor") or {})
    mapa["cero"] = 0
    tok = (texto or "").lower().split()
    out, i = [], 0
    while i < len(tok):
        for j in range(min(len(tok), i + 6), i, -1):
            trozo = " ".join(tok[i:j])
            if trozo in mapa:
                out.append(str(mapa[trozo]))
                i = j
                break
        else:
            out.append(tok[i])
            i += 1
    return " ".join(out)


def iguales(esperado, obtenido, saber=None):
    """Compara dos respuestas; en las listas el orden no importa.
    Con 'saber' (MIS PRUEBAS) tambien vale escribir con cifras lo que el sistema dice con palabras:
    '8 + 5 = 13' es lo mismo que 'ocho + cinco = trece'.  En la coleccion grande NO: alli se
    comprueba tambien en que FORMA responde (cifra o palabra), que es parte de lo que se ensena."""
    if esperado == obtenido:
        return True
    if saber is not None and _en_cifras(esperado, saber) == _en_cifras(str(obtenido), saber):
        return True
    for pre in ("grupo:", "tiene:"):
        if esperado.startswith(pre) and obtenido.startswith(pre):
            return sorted(esperado[len(pre):].split(",")) == sorted(obtenido[len(pre):].split(","))
    return False


# ------------------------------------------------------------------ mis casos

def leer_casos(ruta):
    if not os.path.exists(ruta):
        return []
    casos = []
    with open(ruta, "r", encoding="utf-8") as f:
        for n, linea in enumerate(f, 1):
            s = linea.strip()
            if not s or s.startswith("#"):
                continue
            partes = [p.strip() for p in s.split("|")]
            while len(partes) < 3:
                partes.append("")
            casos.append({"linea": n, "texto": partes[0],
                          "esperado": partes[1], "comentario": partes[2]})
    return casos


def correr_mis_casos(saber, mostrar_todo=False, archivo=None, flexible=False):
    archivo = archivo or ARCHIVO_CASOS
    if not os.path.exists(archivo):
        print("No encuentro el archivo %s" % archivo)
        return 0, 1
    casos = leer_casos(archivo)
    print("=" * 78)
    print("MIS CASOS  (%s)" % os.path.basename(archivo))
    print("=" * 78)
    if not casos:
        print("No hay casos todavia.  Abre mis_casos.txt y anade lineas.\n")
        return 0, 0

    bien = fallos = 0
    for c in casos:
        obtenido, _ = preguntar(c["texto"], saber)
        esperado = normalizar_esperado(c["texto"], c["esperado"])
        etiqueta = c["texto"] if c["texto"] else "(vacio)"
        if esperado == "??":
            # '??' = no comprobar, y ENSENAR todo el razonamiento
            print("  [??]    %-44s -> %s   %s" % (etiqueta, obtenido, c["comentario"]))
            print(motor.explicar_pregunta(c["texto"], saber))
            print()
            continue
        if esperado in ("", "?"):
            print("  [?]     %-44s -> %s   %s" % (etiqueta, obtenido, c["comentario"]))
            continue
        if iguales(esperado, obtenido, saber if flexible else None):
            bien += 1
            print("  [BIEN]  %-44s -> %s" % (etiqueta, obtenido))
        else:
            fallos += 1
            print("  [FALLA] %-44s -> %s   (yo esperaba: %s)  %s"
                  % (etiqueta, obtenido, esperado, c["comentario"]))
            if mostrar_todo:
                print(motor.explicar_pregunta(c["texto"], saber))
    print()
    print("  mis casos: %d bien, %d fallan" % (bien, fallos))
    if flexible:
        print("  (escribe pruebas nuevas con [A] en MIS_PRUEBAS.bat; '??' ensena el razonamiento)")
    print()
    return bien, fallos


# ------------------------------------------------------------------ interactivo

def interactivo(saber):
    print()
    print("=" * 78)
    print("PROBADOR DE EUCLIDES")
    print("=" * 78)
    # OJO: aqui NO se corren los casos.  Antes se corrian al arrancar y lo unico que hacian era
    # llenar la pantalla de ejemplos antes de dejar escribir.  Ahora se piden con 'casos'.
    print("  escribe lo que quieras probar y pulsa Enter.")
    print("  'ayuda'  -> todo lo que sabe hacer, por unidades")
    print("  'casos'  -> tus casos de mis_casos.txt (se comprueban todos)")
    print("  'salir'  -> terminar")
    print()
    while True:
        try:
            entrada = input("pregunta> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if entrada.lower() in ("salir", "exit", "quit", "q"):
            break
        if entrada.lower() in ("ayuda", "help", "?"):
            print(AYUDA)
            continue
        if entrada.lower() in ("casos", "mis casos"):
            correr_mis_casos(saber)
            continue
        try:
            print(motor.explicar_pregunta(entrada, saber))
        except Exception as e:  # nunca un traceback delante de quien prueba
            print("NO ENTIENDO ESTO (%s)." % e)
            print("El sistema no adivina: si no entiende, lo dice.")
        print()
    print("Hasta luego.")


# ------------------------------------------------------------------ principal

def main(argv):
    saber = cargar_conocimiento()

    if len(argv) >= 3 and argv[1] == "--archivo":
        ruta = argv[2] if os.path.isabs(argv[2]) else os.path.join(RAIZ, argv[2])
        bien, fallos = correr_mis_casos(saber, mostrar_todo=True, archivo=ruta, flexible=True)
        return 1 if fallos else 0

    if len(argv) >= 2 and argv[1] == "--casos":
        bien, fallos = correr_mis_casos(saber, mostrar_todo=True)
        return 1 if fallos else 0

    # 'ayuda' como argumento tambien tiene que dar la ayuda (antes lo tomaba por una ESCENA y
    # contestaba 'un_objeto', porque 'ayuda' es un nombre de objeto perfectamente valido).
    if len(argv) >= 2 and argv[1].strip().lower() in ("ayuda", "--ayuda", "-h", "--help"):
        print(AYUDA)
        return 0

    if len(argv) >= 2:
        print(motor.explicar_pregunta(" ".join(argv[1:]), saber))
        return 0

    interactivo(saber)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
