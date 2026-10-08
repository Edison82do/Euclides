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

  PIEZAS  ->  el MAPA DEL CONOCIMIENTO: que piezas tiene y que usa cada una
        piezas                 -> las piezas de conocimiento/piezas/, por la pregunta que responden
        Cada conocimiento que usa el resolvedor es una PIEZA: un archivo con lo que es, CUANDO
        sirve (sus condiciones, con el porque del descarte), lo que USA y como se hace.  El motor
        solo las carga, las prueba todas, descarta y aplica.  Una pieza nueva = un archivo nuevo.
        Para calcular elige el METODO MAS CORTO que encaja: hacer diez, los dedos, las columnas.

  CALCULAR  ->  una cuenta suelta: TODOS los metodos que tengo, cual encaja y cual uso (paso 4)
        calcular: 47 + 30      -> 77   de diez en diez: 57, 67, 77 (la cifra de las decenas sube)
        calcular: 29 + 14      -> 43   compensar: al 29 le doy uno del 14 -> 30 + 13
        calcular: 52 - 29      -> 23   compensar: quito 30 (uno de mas) y devuelvo uno
        calcular sin memoria: 6 + 7  -> 13   casi dobles: 6 + 6 = 12 (de memoria) y uno mas
        calcular: 8 + 5        -> 13   de memoria (si ya lo aprendi; si no, haciendo diez)
        calcular: 3 + 47       -> 50   DAR LA VUELTA (P.5): 47 + 3, empiezo por el grande
        calcular: 30 + 47      -> 77   la vuelta y de diez en diez: 47 + 30
        calcular: 52 - 48      -> 4    RESTAR PENSANDO EN SUMAR (P.6): del 48 al 52 -> 49, 50, 51, 52
        calcular: 100 - 95     -> 5    96 ... 100 (sin cambiar centenas por decenas)
        calcular: 13 - 2       -> 11   se quita poco: mas corto hacia atras (y lo dice)
        Cada tecnica es una PIEZA con sus condiciones: donde no encaja se descarta con su porque.

  ECUACION  ->  que numero va en el HUECO? (paso E.1; 1.OA.D.8)  -- se puede escribir DIRECTAMENTE
        8 + ? = 11             -> 3    juntar con el CAMBIO desconocido: cuento de 8 a 11
        ? + 3 = 11             -> 8    el COMIENZO desconocido: deshago (11 - 3)
        5 = ? - 3              -> 8    el hueco al otro lado del = da igual
        11 - ? = 8             -> 3    separar con el cambio desconocido
        8 + ? = 5              -> imposible     ? + ? = 10 -> dos huecos
        Huecos: ?  _  __  o el cuadradito.  Las palabras de alrededor no molestan.
        Cada ecuacion se cuenta como una HISTORIA y la resuelven las piezas de los problemas (R.1);
        luego se COMPRUEBA poniendo el numero en el hueco (verdad:, E.0).
        ecuacion: ... / hueco: ...  -> lo mismo con la orden delante.
        Y escrito directamente: '8 + 3 = 11' -> verdad,  '8 + 3' -> calcular.

  DIVIDIR  ->  repartir y agrupar (paso M.3; NCETM 2.6)
        12 en grupos de 3      -> 4    AGRUPAR: cuantos grupos? contando 3, 6, 9, 12
        12 entre 3             -> 4    REPARTIR: cuantos para cada uno? (rondas de uno para cada uno)
        12 : 3                 -> 4    (tambien 12 ÷ 3 y 12 / 3): las dos lecturas
        13 : 3                 -> 4 resto 1   a veces sobra
        30 : 5                 -> 6    con la tabla que se: 6 x 5 = 30 (factor desconocido)
        15 : 2                 -> 7 resto 1   la mitad
        0 : 4 / 7 : 7 / 9 : 1  -> 0 / 1 / 9   sin calcular
        8 : 0                  -> no se puede (no se reparte entre nadie)
        Siempre se COMPRUEBA multiplicando: cociente x divisor (+ resto) = dividendo.

  TABLA DEL 7 Y LA DISTRIBUTIVA  ->  (paso M.6; NCETM 2.9, 2.10; 3.OA.B.5, C.7)
        tabla del 7            -> cada producto PARTIDO: 7 = 5 + 2 -> 8 x 7 = 40 + 16 = 56
        aprender: tablas       -> ya TODAS hasta 10 x 10, cada una sacada de otras y comprobada
        12 x 6                 -> 72   mas alla de las tablas: 10 x 6 + 2 x 6
        7 x 9                  -> 63   y dice: impar x impar -> el producto es IMPAR
        6 x 6                  -> 36   y dice: es un NUMERO CUADRADO
        divisible: 49 entre 7  -> si   (para el 7 no hay regla corta: dividiendo)

  TABLAS DEL 3, 6 Y 9  ->  sus relaciones (paso M.5; NCETM 2.8)
        tabla del 3            -> contar de 3 en 3
        tabla del 6            -> el DOBLE de la del 3
        tabla del 9            -> el TRIPLE de la del 3
        7 x 9                  -> 63   (si 7 x 3 ya se sabe: 21 + 21 + 21)
        divisible: 51 entre 3  -> si   (5 + 1 = 6: la suma de las cifras)
        divisible: 72 entre 6  -> si   (par, y 7 + 2 = 9)
        divisible: 999 entre 9 -> si   (9+9+9 = 27 -> 2+7 = 9)

  TABLAS DEL 4 Y DEL 8  ->  doblando (paso M.4; NCETM 2.7)
        tabla del 4            -> cada producto, el DOBLE del de la tabla del 2
        tabla del 8            -> cada producto, el DOBLE del de la tabla del 4
        7 x 8                  -> 56   (si 7 x 4 ya se sabe: 28 + 28)
        aprender: tablas       -> ahora tambien la del 4 y la del 8, en orden (2 -> 4 -> 8)
        divisible: 36 entre 8  -> no   (36 -> 18 -> 9: entre 8 hay que partir por la mitad TRES veces)
        divisible: 40 entre 8  -> si   (40 -> 20 -> 10 -> 5)

  TABLAS  ->  las tablas del 2, 5 y 10; la conmutativa; dobles y mitades (paso M.2; NCETM 2.3-2.5)
        tabla del 5            -> 0 x 5 = 0 ... 10 x 5 = 50 (contar de 5 en 5)
        5 x 7                  -> 35   la OTRA LECTURA: 7 grupos de 5, con la tabla del 5
        2 x 9                  -> 18   un factor es 2: el DOBLE de 9
        0 x 8 / 8 x 1          -> 0 / 8   sin calcular (un factor es cero o uno)
        3 x 4 = 4 x 3          -> VERDADERO sin calcular (los factores en cualquier orden)
        mitad: 14              -> 7    lo contrario del doble (hasta 20); mitad: 7 -> impar
        aprender: tablas       -> las tablas del 2, 5 y 10 a la memoria (comprobadas con la otra lectura)

  MULTIPLICAR  ->  a x b son a GRUPOS IGUALES de b (paso M.1; 3.OA.A.1, NCETM 2.2)
        3 x 4                  -> 12   3 grupos de 4: los dibuja, 4 + 4 + 4, y 3 x 4 = 12
        5 x 7                  -> 35   (el ejemplo del estandar: 5 grupos de 7)
        4 x 0 / 0 x 4          -> 0    grupos vacios / ningun grupo
        5 x 2                  -> 10   grupos de 2: saltando 2, 4, 6, 8, 10
        3 grupos de 4          -> 12   lo mismo, dicho con palabras   (tambien 3 * 4, 3 × 4)
        grupos de 2, 3 y 4     -> 9    NO son iguales: no es una multiplicacion, es una suma
        40 x 30                -> no se puede (pasa de mil)
        (3 x ? = 12: ver ECUACION CON x Y :)

  FILAS  ->  filas y columnas como SUMAS IGUALES (paso M.0; 2.OA.C.4): el puente a multiplicar
        3 filas de 4           -> 12   lo DIBUJA, escribe 4 + 4 + 4 y lo suma grupo a grupo;
                                       y lo cuenta tambien por columnas (3 + 3 + 3 + 3): da lo mismo
        5 filas de 5           -> 25   cada fila es de 5: salta 5, 10, 15, 20, 25 (lo de N.1)
        3 columnas de 4        -> 12   (4 filas de 3 en el dibujo)
        (3 x 4 es MULTIPLICAR: ver MULTIPLICAR)
        El estandar llega a 5 x 5; dibuja hasta 10 filas y 10 columnas.

  SALTOS Y PAR  ->  contar de n en n; par o impar (paso N.1; 2.NBT.A.2, 2.OA.C.3, NCETM 2.1)
        de 2 en 2 hasta 20     -> 2, 4, 6 ... 20
        de 5 en 5 desde 3 hasta 50  -> 8, 13 ... 48  (y dice que el 50 no se toca)
        de 10 en 10 desde 47 hasta 97  -> 57, 67, 77, 87, 97  (se ESCRIBE la cifra de las decenas)
        de 100 en 100 desde 250  -> 350 ... 950  (se para antes de pasar de mil)
        par: 14                -> PAR (hago parejas: 7 parejas, 14 = 7 + 7, un doble)
        par: 7                 -> IMPAR (tres parejas y uno suelto)
        par: 846               -> PAR (diez se empareja entero: solo miro las unidades)
        Y 47 + ? = 77 ya no cuenta 30 pasos: salta 57, 67, 77 -> 30.

  PROBLEMAS DE x Y :  ->  grupos iguales, filas, medidas (paso R.2; 3.OA.A.3)  -- se escriben directamente
        Hay 3 bolsas con 4 caramelos cada una. Cuantos caramelos hay?    -> 12 caramelos
        Reparte 12 caramelos entre 3 ninos. Cuantos le tocan a cada uno?  -> 4 caramelos
        Mete 12 caramelos en bolsas de 4. Cuantas bolsas salen?           -> 3 bolsas
        Hay 12 caramelos. Cada nino tiene 3. Cuantos ninos hay?           -> 4 ninos  ('cada' y DIVIDIR)
        En el cine hay 3 filas de 4 sillas. Cuantas sillas hay?           -> 12 sillas
        Cada caja pesa 5 kilos. Cuanto pesan 4 cajas?                     -> 20 kilos
        Llena el ESQUEMA de grupos iguales (grupos, en cada uno, total) por los NOMBRES, no por
        palabras clave; dibuja la BARRA (Singapur) y comprueba.  Los de sumar y restar siguen en R.1.

  FRACCIONES  ->  la parte y el todo; fracciones unitarias (paso F.1; NCETM 3.1, 3.2; 3.NF.A.1)
        fraccion: 1/4          -> un cuarto: el entero en 4 partes IGUALES, se toma una  [####|oooo|oooo|oooo]
        1/4 de 12              -> 3    REPARTIR 12 en 4 partes iguales (M.3)    1/4 de 13 -> no_sale
        comparar: 1/3 y 1/5    -> 1/3 > 1/5   mas partes, partes MAS PEQUENAS (y en una tira de 15 cuadritos)
        entero: 1/4 es 3       -> 12   el entero son 4 partes de 3: 3 + 3 + 3 + 3
        partes: 12 = 4 + 4 + 4 -> 1/3   (5 + 4 + 3 -> desiguales: no son tercios)
        De medios a doceavos (1/2 a 1/12).

  FRACCIONES NO UNITARIAS  ->  varias partes; en la recta; comparar (paso F.2; NCETM 3.3; 3.NF.A.2, A.3)
        fraccion: 3/4          -> tres cuartos = 1/4 + 1/4 + 1/4    (4/4 -> un entero; 3/1 -> 3 enteros)
        recta: 3/4             -> la recta de 0 a 1 en 4 trozos, la marca a tres trozos del 0
        3/4 de 12              -> 9    (12 en 4 partes de 3, y se toman 3)     entero: 3/4 es 9 -> 12
        comparar: 2/5 y 3/5    -> 2/5 < 3/5   mismo de abajo: manda el de arriba
        comparar: 2/3 y 2/5    -> 2/3 > 2/5   mismo de arriba: manda el de abajo, AL REVES
        comparar: 2/3 y 3/5    -> todavia_no (sin nada en comun: equivalentes, 5.o)   5/4 -> todavia_no (4.o)

  SUMAR Y RESTAR FRACCIONES  ->  dentro de un entero, mismo de abajo (paso F.3; NCETM 3.4)
        2/7 + 3/7              -> 5/7   las partes son del mismo tamano: se cuentan como manzanas
                                        (el de abajo NO se suma: 5/14 seria el error)
        5/7 - 2/7              -> 3/7       1 - 3/8 -> 5/8 (1 = 8/8)       3/8 + 5/8 -> 1
        Con la vuelta (sumar y restar son inversas).  Pasar de un entero: 4.o.  Distinto abajo: 5.o.

  EL MILLAR  ->  el 1000 y los numeros de cuatro cifras, hasta DIEZ MIL (paso N.3, 4.o; NCETM 1.22; 4.NBT.A)
        nombre: 2005           -> dos mil cinco   (el millar 'dos mil' + 'cinco'; el cero marca las centenas)
        numero: dos mil cinco  -> 2005            (no 20005 ni 205)
        millar: 3045           -> 3000 + 40 + 5   y CUANTAS hay: 3 millares, 30 centenas, 304 decenas
        millar: 1000           -> 10 centenas = 100 decenas = 1000 unidades; 2 x 500 = 4 x 250 = 5 x 200
        comparar: 3456 y 3465  -> 3456 < 3465  mirando las CIFRAS: mas cifras gana; si no, la primera distinta
        redondear: 3456        -> decena 3460, centena 3500, millar 3000      de 1000 en 1000
        300 + 800              -> 1100   3 centenas + 8 centenas = 11 centenas (las centenas como cosas)
        columnas: 2345 + 1678  -> 4023   (lo de tres cifras sirve para cuatro)
        La lista de contar llega a DIEZ MIL (para contar objetos).  Los numeros: hasta UN MILLON (N.4), DIEZ MILLONES (N.6).

  HASTA UN MILLON  ->  numeros de cinco y seis cifras (paso N.4, 4.o-5.o; NCETM 1.26; 4.NBT.A, 4.NBT.B.5)
        nombre: 21000          -> veintiun mil      nombre: 101000 -> ciento un mil
        nombre: 200005         -> doscientos mil cinco   (se lee por grupos de tres: '200 mil' y '5')
        millar: 345678         -> 300000 + 40000 + 5000 + 600 + 70 + 8   (345 MIL y 678)
        comparar: 99999 y 100000  -> 99999 < 100000   (mas cifras gana)
        345000 + 278000        -> 623000   345 mil + 278 mil = 623 mil (el mil como una cosa)
        columnas: 500000 - 1   -> 499999   (cambiar a traves de cinco ceros)
        18 x 38                -> 684      LA REJILLA: 10 x 30 + 10 x 8 + 8 x 30 + 8 x 8 (los dos por sitios)
        redondear: 345678      -> ... decena de millar 350000, centena de millar 300000
        de 10000 en 10000 desde 970000  -> 980000, 990000, 1000000
        Contar OBJETOS sigue hasta diez mil; los NUMEROS llegan a un millon.  Mas alla: N.6 (6.o).

  HASTA DIEZ MILLONES  ->  numeros de siete cifras; el millon como una cosa (paso N.6, 6.o; NCETM 1.30)
        nombre: 2345678        -> dos millones trescientos cuarenta y cinco mil seiscientos setenta y ocho
        nombre: 1021000        -> un millon veintiun mil   (un millon; dos millones: singular y plural)
        numero: dos millones cinco  -> 2000005   (el grupo de los miles es 000: no se dice)
        millar: 1030405        -> 1 millon, 30 mil y 405; hay 10 centenas de millar aunque la cifra sea 0
        millar: 1000000        -> los patrones: 10 centenas de millar = 1000 millares = un millon
        comparar: 999999 y 1000000  -> 999999 < 1000000   (mas cifras gana)
        997000 + 5000          -> 1002000   PASANDO POR EL MILLON: le faltan 3000, de los 5000 quedan 2000
        1002000 - 997000       -> 5000      contando hacia arriba: 3000 hasta el millon y 2000 desde el
        2000000 + 3000000      -> 5000000   2 millones + 3 millones = 5 millones (el millon como cosa)
        redondear: 2499999     -> ... al millon 2000000 (no 3000000: la trampa de la cadena)
        de 100000 en 100000 desde 700000 hasta 1300000  -> cruza el millon
        calcular: 997000 + 5000  -> mental (pasar por el millon) o escrito (columnas): se elige el mas corto
        Los NUMEROS llegan a DIEZ MILLONES; contar OBJETOS sigue hasta diez mil.

  DOS INCOGNITAS  ->  una solucion, varias o ninguna; la barra o probar en orden (paso S.3, 6.o; NCETM 1.31)
        a + b = 30; a - b = 8          -> a = 19, b = 11   la BARRA: quito la diferencia, 30 - 8 = 22; 22 : 2 = 11 = b
                                          (no 30 : 2 = 15 y 15 + 8 = 23: asi juntan 38)
        a + b = 24; a = 3 x b          -> a = 18, b = 6    3 trozos y UNO mas = 4 trozos: 24 : 4 = 6 (no 24 : 3)
        a - b = 20; a = 3 x b          -> a = 30, b = 10   los trozos DE MAS (3 - 1 = 2) son la diferencia
        a + b = 10; a - b = 12         -> ninguna          la diferencia no cabe en la suma
        a + b = 9; a - b = 4           -> a = 6.5, b = 2.5 (con enteros, ninguna)
        a + b = 10                     -> 11 parejas con enteros (9 sin el 0); infinitas con decimales
        a - b = 3   o   a = 3 x b      -> infinitas        (una relacion sola no pone tope)
        a x b = 24; a + b = 10         -> a = 4, b = 6; a = 6, b = 4   PROBAR EN ORDEN por las parejas de factores
        a + b = 10; 2 x a + 5 x b = 32 -> a = 6, b = 4     (10 monedas de 2 y de 5 que hacen 32)
        2 x a + 3 x b = 20             -> cuatro soluciones (pruebo con el que mas pesa: menos pruebas)
        Tambien: x + y = 30; x = y + 8   24 = a + b   b - a = 8   y con la orden delante, dos incognitas: ...
        Con palabras: Ana y Luis tienen 30 entre los dos. Ana tiene 8 mas que Luis. Cuantas tiene Luis?  -> 11
        Mas de 30 pruebas -> todavia no (un humano no prueba tantas).  Se comprueba poniendo los numeros en las ecuaciones.

  EL RESOLVEDOR UNIVERSAL  ->  el modelo y el lector simbolico (plan U, fase U.1; todo lo que se escribe con simbolos)
        resolver: a + b = 1/2; a - b = 1/4  -> a = 3/8, b = 1/8   SUSTITUYE a = 1/2 - b; cuenta los trozos de b
        3 x n = 4.5            -> n = 1.5    DESHACE el x 3: 45 decimas : 3 = 15 decimas
        resolver: (a + 5) x 2 = 26  -> a = 8  (sin la orden sigue saliendo por E.5)
        x + y + z = 40; x = y; z = 2 x y  -> x = 10, y = 10, z = 20   1 + 1 + 2 = 4 trozos de y = 40
        1/2 + 0.25             -> 3/4 (= 0.75)  el NUMERO COMUN: 0.25 = 25/100 = 1/4; el mismo de abajo
        -3 + 2 x 4             -> 5      primero el x; luego signos distintos: 8 - 3, con el signo del 8
        resolver: 3/4 : 1/8    -> 6      con el mismo de abajo, cuantas veces cabe
        resolver: 7 : 2        -> 7/2    lo que no se reparte justo es una fraccion
        resolver: a + b = 10; a + b = 12  -> ninguna (se contradicen)     resolver: 0 x n = 5  -> ninguna
        Enteros, decimales (4.5 o 4,5), fracciones (1/2), negativos (-3), parentesis, varias letras, ';' entre
        relaciones, 2n = 2 x n.  Al final COMPRUEBA en las relaciones de PARTIDA.  Lo que una puerta vieja no
        entiende y esto si, va aqui solo.  Faltan relaciones, o la letra por si misma (n x n) -> todavia no (U.2).

  MAS DE UN ENTERO  ->  numeros mixtos y fracciones impropias (paso F.4; NCETM 3.5; 4.NF.B.3)
        fraccion: 7/4          -> siete cuartos = 1 3/4   (agrupo 7 cuartos de 4 en 4: 1 entero y sobran 3)
        mixto: 2 3/4           -> 11/4   (2 enteros son 8 cuartos, y 3 mas)
        recta: 7/4             -> la recta de 0 a 2, la marca a siete trozos
        2 3/4 + 1 1/4          -> 4      enteros con enteros, partes con partes (y por impropias: 11/4 + 5/4)
        3 - 1/4                -> 2 3/4  (cambio un entero por 4/4)
        comparar: 2 1/4 y 1 3/4 -> 2 1/4 > 1 3/4   primero los enteros, luego las partes

  DECIMAS  ->  0.1 es una decima: el uno partido en diez (paso D.1; NCETM 1.23; 4.NF.C.6)
        decimal: 2.3           -> 23 decimas  (2 enteros y 3 decimas = 2 + 0.3 = 2 + 3/10; entre 2 y 3)
        2.7 + 1.5              -> 4.2   en columnas con el punto alineado (7 + 5 = 12: escribo 2, llevo 1)
                                        y contando en decimas: 27 decimas + 15 decimas = 42 decimas
        4.2 - 1.5              -> 2.7   (cambio 1 unidad por diez decimas)
        comparar: 0.9 y 1.1    -> 0.9 < 1.1    redondear: 2.7 -> 3    de 0.1 en 0.1 desde 0.7
        Se escribe con punto (tambien vale la coma).  Centesimas (2.35): todavia no.

  CENTESIMAS Y MILESIMAS  ->  0.01 y 0.001 (paso D.2; NCETM 1.24; 4.NF.C.5-7)
        decimal: 2.35          -> 235 centesimas  (2 + 0.3 + 0.05)
        comparar: 0.5 y 0.45   -> 0.5 > 0.45  (0.50 contra 0.45: no '45 es mas que 5')
        2.35 + 1.7             -> 4.05  (los puntos alineados: 1.70)     5 - 0.25 -> 4.75
        redondear: 2.35 a la decima -> 2.4      redondear: 2.35 -> 2 (al entero)
        de 0.01 en 0.01 desde 0.98    fraccion: 35/100 -> 0.35;  3/10 = 30/100

  DINERO  ->  pesos y centavos: un centavo es la centesima parte de un peso (paso D.3; NCETM 1.25)
        dinero: $3.45          -> 345 centavos
        $2.99 + $1.50          -> $4.49   en columnas, y COMPENSANDO: $3.00 + $1.50, menos 1 centavo
        cambio: pago $10 por $6.35   -> $3.65   contando hacia adelante: 5 centavos, 60 centavos, 3 pesos
        cambio: pago $20 por $3.45 + $6.80 + $2.15   -> $7.60   (el todo y las partes)

  ENTERO POR FRACCION  ->  sumar una fraccion una y otra vez (paso F.5; NCETM 3.6; 4.NF.B.4)
        3 x 2/5                -> 1 1/5   2/5 + 2/5 + 2/5 = 6 quintos (el de abajo no se multiplica)
        3 x 1 2/5              -> 4 1/5   partiendo: 3 enteros y 6/5;  por impropias: 3 x 7/5 = 21/5
        12 x 3/4               -> 9       y la otra lectura: 3/4 de 12 (repartir en 4, tomar 3)
        2/3 x 3/4              -> todavia_no (fraccion por fraccion: 6.o)

  FRACCIONES EQUIVALENTES  ->  valen lo mismo; SIMPLIFICAR (paso F.6; NCETM 3.7; 4.NF.A.1)
        simplificar: 12/18     -> 2/3     paso a paso: 6/9 (entre 2), 2/3 (entre 3); no se queda en 6/9
        simplificar: 5/20      -> 1/4     el 5 cabe justo en el 20: de una vez;   simplificar: 3/4 -> 3/4 (ya lo es)
        simplificar: 26/39     -> 2/3     el factor comun 13 no es de las tablas: los "trozos grandes" (13 y 13)
        equivalentes: 2/3      -> 2/3 = 4/6 = 6/9 = 8/12 = 10/15 = 12/18   (arriba y abajo POR EL MISMO; con tiras)
        2/3 = ?/12             -> 8       la relacion horizontal: de 3 a 12 es x 4
        4/12 = 5/?             -> 15      la relacion vertical: en 4/12 el de abajo es 3 veces el de arriba
        4/6 = ?/9              -> 6       simplificar primero: 2/3, y de 3 a 9 es x 3;   2/3 = ?/10 -> no_sale
        equivalentes: 2/3 y 3/4  -> no    sumar lo mismo arriba y abajo NO da una equivalente (hay que multiplicar)
        equivalentes: 3/12 y 1/4 -> si    (y comparar: 3/12 y 1/4 -> 3/12 = 1/4: sus numeros mas grandes no la hacen mayor)
        2/3 = 8/12             -> VERDADERO
        Cada respuesta se comprueba: multiplicando de vuelta, o simplificando las dos a la misma.

  EL MISMO DE ABAJO  ->  sumar, restar y comparar con distinto de abajo (paso F.7; NCETM 3.8; 5.NF.A.1-2)
        1/2 + 1/4              -> 3/4     relacionadas (4 : 2 = 2, justo): cambio solo una, 1/2 = 2/4
        1/3 + 1/4              -> 7/12    no relacionadas: 3 x 4 = 12;  4/12 + 3/12
        1/2 + 1/3              -> 5/6     y dice el error tipico: NO es 2/5 (2/5 es menor que 1/2)
        5/6 - 1/3              -> 1/2     5/6 - 2/6 = 3/6, y se simplifica al final
        2/3 + 3/4              -> 1 5/12  17/12, mas de un entero;   1/4 - 1/2 -> imposible
        2 1/2 + 1 1/4          -> 3 3/4   los mixtos, a impropias y al mismo de abajo
        comparar: 2/3 y 3/4    -> 2/3 < 3/4   por el mismo de abajo (8/12, 9/12) y el de arriba (6/9, 6/8)
        Cada paso se comprueba: dividiendo de vuelta lo que se multiplico, y la cuenta contraria.

  AREA Y PERIMETRO  ->  la superficie y el borde (paso G.1; NCETM 2.16; 3.MD.C.7, 3.MD.D.8)
        area: rectangulo 5 x 3       -> 15 unidades cuadradas  (3 filas de 5 cuadraditos = 5 x 3)
        perimetro: rectangulo 5 x 3  -> 16   (5 + 3 + 5 + 3: el borde, en unidades de longitud)
        perimetro: cuadrado de 6     -> 24   (4 x 6)      perimetro: 4, 7, 5 -> 16 (suma de lados)
        lado: cuadrado de perimetro 24 -> 6  (24 : 4)     area: 6 x 4 + 3 x 2 -> 30 (figura compuesta)
        comparar: rectangulo 6 x 2 y rectangulo 4 x 3 -> la misma area y distinto perimetro
        Con unidades: rectangulo 5 cm x 3 cm  ->  15 cm cuadrados

  NEGATIVOS  ->  numeros menores que cero: contar, comparar y calcular cruzando el cero (paso N.5; NCETM 1.27; 6.NS.C)
        negativo: -5           -> menos cinco: 5 pasos a la IZQUIERDA del cero
        comparar: -3 y -7      -> -3 > -7   (el de cifra mayor esta mas lejos del cero: es MENOR)
        recta: 3 - 8           -> -5    hasta el cero 3, me quedan 5 (como hacer diez)
        recta: -4 + 7          -> 3     recta: desde 3 bajando 6 -> 2, 1, 0, -1, -2, -3
        intervalo: -4 y 7      -> 11    (4 hasta el cero y 7 desde el cero)
        La temperatura es -4 grados. Sube 7 grados. Cual es ahora?            -> 3 grados
        Por la manana hace -6 grados y a mediodia 5 grados. Cuanto subio?     -> 11 grados
        3 - 8 sin la recta sigue siendo 'imposible': con cosas no se quitan 8 de 3.

  EQUIVALENCIA  ->  cambiar los numeros sin cambiar el resultado (paso M.12; NCETM 2.18)
        equivalente: 25 x 16   -> 400   25 x 16 = 50 x 8 = 100 x 4 (doblo uno, parto el otro por la mitad)
        equivalente: 165 : 5   -> 33    165 : 5 = 330 : 10 (doblo LOS DOS: el cociente no cambia)
        equivalente: 180 : 20  -> 9     180 : 20 = 18 : 2 (quito un cero a los dos)
        verdad: 3 x 12 = 6 x 6 -> VERDADERO sin calcular (6 es 3 al doble, 6 es 12 a la mitad)
        verdad: 3 x 12 = 4 x 11 -> FALSO  (uno mas aqui, uno menos alli es cosa de la SUMA)
        verdad: 96 : 4 = 192 : 2 -> FALSO (en : los dos cambian IGUAL, no al reves)
        24 x 5 = 12 x ?        -> 10    (12 es 24 a la mitad: el hueco es 5 al doble)
        180 : 20 = 18 : ?      -> 2     (el dividendo diez veces mas pequeno: el divisor tambien)
        Y 25 x 16, 165 : 5 ... sin decir 'equivalente' tambien lo usan si es lo mas corto.

  DECIMALES POR ENTEROS  ->  multiplicar y dividir un decimal por un entero (paso M.13; NCETM 2.19; 5.NBT.B.7)
        0.3 x 4                -> 1.2    3 decimas x 4 = 12 decimas (no 0.12: son decimas, no centesimas)
        3.27 x 4               -> 13.08  327 centesimas x 4 = 1308 centesimas; y por partes 12 + 1.08
        1.5 x 4                -> 6      (no 4.20: el entero y las decimas no se pegan, se SUMAN)
        35 x 0.1               -> 3.5    por 0.1 es entre 10: las cifras bajan un sitio (sale MENOS)
        7.2 : 3                -> 2.4    72 decimas : 3 = 24 decimas
        1.3 : 4                -> 0.325  sobra: se CAMBIA a centesimas y a milesimas
        0.12 : 4               -> 0.03   (no 0.3: son 12 centesimas)
        3.5 : 10               -> 0.35   las cifras bajan un sitio
        0.3 x 0.4, 7.2 : 12, 7.2 : 0.3 -> todavia_no (decimal por decimal y division larga: 6.o)
        Cada cuenta se comprueba con la contraria: 1.2 : 4 = 0.3;  24 decimas x 3 = 72 decimas.

  TRES FACTORES Y VOLUMEN  ->  multiplicar tres numeros en el orden mas facil; el volumen (paso M.14; NCETM 2.20; 5.MD.C.3-5)
        25 x 7 x 4             -> 700    la pareja amiga primero: 25 x 4 = 100, 100 x 7 = 700 (no 175 x 4)
        7 x 20 x 3             -> 420    las decenas justas al final: 7 x 3 = 21, 21 x 20
        0.25 x 7 x 4           -> 7      0.25 x 4 = 1 (con un decimal, como en M.13)
        5 x 0 x 999            -> 0      con un cero no hay nada, sin cuentas
        2 x 3 x 4 = 24  /  verdad: 2 x 3 x 4 = 4 x 3 x 2  -> VERDADERO (los mismos factores: sin calcular)
        volumen: caja 5 x 3 x 2 cm   -> 30 cm cubicos  la capa (5 x 3 = 15 cubitos) por 2 capas; no 10 (sumar)
        volumen: cubo de 3     -> 27     (no 26: el cubito de DENTRO tambien cuenta)
        volumen: 5 x 3 x 2 + 4 x 4 x 1   -> 46   una figura de dos cajas: se SUMAN
        volumen: 5 x 3 x ? = 60          -> 4    el problema inverso: 60 : 5 = 12, 12 : 3 = 4
        volumen: caja 2 m x 30 cm x 4 cm -> todavia_no (la misma unidad);  0.3 x 0.2 x 5 -> todavia_no
        Cada producto se comprueba DIVIDIENDO entre los factores, uno a uno: 700 : 7 = 100, 100 : 4 = 25.

  FACTORES, MULTIPLOS Y PRIMOS  ->  (paso M.15; NCETM 2.21; 4.OA.B.4)
        factores: 36           -> 1, 2, 3, 4, 6, 9, 12, 18, 36   pruebo 1, 2, 3 ... dividiendo y paro al cruzarme;
                                  9 factores (impar): 6 x 6, 36 es un CUADRADO
        primo: 91              -> compuesto   (7 x 13: impar y NO primo)
        primo: 1               -> ni_primo_ni_compuesto   (un solo factor; el error tipico)
        primo: 1000            -> compuesto   (es par: 2 x 500, la regla corta)
        primos hasta 100       -> los 25 primos   (la criba: tacho de 2 en 2, de 3 en 3, de 5 en 5, de 7 en 7)
        multiplos de 7         -> 7, 14 ... 84   (contando de 7 en 7);   multiplos de 7 hasta 50
        21 es multiplo de 7 -> si;   7 es multiplo de 21 -> no (es al reves: 7 es FACTOR de 21)
        factores comunes: 24 y 36  -> 1, 2, 3, 4, 6, 12      multiplos comunes: 4 y 6 -> 12, 24 ...
        factores primos: 60    -> 2, 3, 5
        con 100: 25 x 36       -> 900   (las parejas de 100: 36 = 9 x 4 y 25 x 4 = 100)
        factores: 169, primo: 997 -> todavia_no (habria que dividir entre 13: la division larga, 6.o)
        Cada division se comprueba multiplicando: 5 x 7 + 1 = 36.

  COMBINAR LA x CON LA + Y LA -  ->  el orden de siempre y el factor comun (paso M.16; NCETM 2.22; 5.OA.A.1)
        3 + 4 x 5              -> 23     rodeo la x: 4 x 5 = 20; luego 3 + 20 (no 35: de izquierda a derecha esta MAL)
        (3 + 4) x 5            -> 35     el parentesis primero: 3 + 4 = 7; luego 7 x 5
        10 - 3 + 2             -> 9      la + y la - en el orden en que vienen (no 10 - 5: la suma NO va antes)
        4 x 6 + 4 x 2          -> 32     FACTOR COMUN: 6 cuatros y 2 cuatros = 4 x 8 (no (4 + 4) x (6 + 2) = 64)
        7 x 5 - 7 x 3          -> 14     tambien con la resta: 7 x 2;     5 x 4 + 5 -> 25 (el 5 suelto es 5 x 1)
        0.5 x 4 + 1.25         -> 3.25   con decimales (M.13 y las columnas con el punto)
        verdad: 3 + 4 x 5 = 35 -> FALSO  (y se puede escribir directamente: 3 + 4 x 5 = 23 -> verdadero)
        calcular: 3 + 4 x 5    -> 23     (antes leia solo 3 + 4 y decia 7)
        2 x 3 - 4 x 5 -> todavia_no (se baja de cero);  12 : 3 + 1 -> todavia_no (dividir: 2.28, 6.o)
        Cada cuenta se comprueba con la contraria, de la ultima a la primera: 23 - 20 = 3, 20 : 4 = 5.

  PARTE-PARTE-TODO  ->  tres partes o mas; la misma estructura en contextos distintos (paso S.2; NCETM 1.28)
        partes: 37, 25, 63; todo: ?       -> 125   falta el TODO: junto las partes (37 y 63 son amigas: 100 primero)
        todo: 100; partes: 37, ?, 25      -> 38    falta UNA PARTE: junto lo que se sabe (62) y lo quito de una vez
                                                   (no 162: el todo NO se suma con las partes; no 63: hay que quitar TODAS)
        partes: 6, 6, 6, 6; todo: ?       -> 24    partes iguales: 4 x 6 (tambien es multiplicativa)
        todo: 24; 4 partes iguales        -> cada parte: 6   (o: todo: 24; partes: ?, ?, ?, ? iguales)
        perimetro: 30; lados: 8, 7, 6, ?  -> 9 cm  el perimetro es el TODO; los lados, las PARTES
        tenia: 20; gaste: 4.50, 7.25; queda: ?   -> 8.25 pesos     camino: ?; tramos: 1.25, 3.5, 0.75 -> 5.5 km
        (los contextos estan en conocimiento/parte_parte_todo.kn: clase/grupos, bolsa/cosas, dia/ratos...)
        perimetro: 30; lados: 20, 15, ? -> no_se_puede (ya pasan del todo);  todo: 50; partes: 20, ?, ? -> no_se_puede
        todo: 30; partes: 10, 10, 10    -> cuadra    (no falta nada: miro si las partes juntan el todo)
        Las partes se separan con coma y los decimales llevan punto.  Se comprueba con la contraria: 37 + 38 + 25 = 100.

  COMPENSAR CON + Y -  ->  cambiar los numeros sin cambiar el resultado, o mover lo que ya se sabe (paso P.7; NCETM 1.29)
        4997 + 2456            -> 7453   la MISMA SUMA: a 4997 le faltan 3 para 5000; se los quito al otro: 5000 + 2453
        1000 - 397             -> 603    la MISMA DIFERENCIA: le sumo 3 a LOS DOS: 1003 - 400
        999999 - 997           -> 999002 (sumar 3 pasaria del millon): quito 1000 y devuelvo los 3 de mas
        equivalente: 1000 - 397 -> 603   ensena la cadena 1000 - 397 = 1003 - 400 = 603
        equivalente: 7.2 - 3.9 -> 3.3    con decimales: 7.3 - 4;   equivalente: 5.003 - 1.998 -> 3.005 (5.005 - 2)
        si 600 - 200 = 400: 600 - 201 = ?  -> 399  el sustraendo SUBE 1: la diferencia BAJA 1 (no 401: la trampa)
        si 250 + 250 = 500: 251 + 250 = ?  -> 501  un sumando sube 1: la suma sube 1
        verdad: 75 - 28 = 77 - 30  -> VERDADERO sin calcular (los dos suben 2)
        verdad: 75 - 28 = 73 - 30  -> FALSO (el minuendo baja 2 y el sustraendo sube 2: la diferencia baja 4)
        74 - 28 = 75 - ?       -> 29     en la resta los dos se mueven HACIA EL MISMO LADO (no 27, como en la suma)
        Cada cuenta se comprueba con la contraria por las columnas: 603 + 397 = 1000.

  VECES  ->  comparar multiplicando: "K veces" y fracciones (paso S.1; NCETM 2.17; 4.OA.A.1-2)
        veces: 4 veces 6       -> 24   (4 veces mas NO es 4 mas: eso seria 10)
        cuantas veces: 24 y 6  -> 4    (24 es 4 veces 6; 6 es 1/4 de 24)
        La cuerda roja mide 6 cm. La azul es 4 veces mas larga. Cuanto mide la azul?        -> 24 cm
        La azul mide 24 cm. Es 4 veces mas larga que la roja. Cuanto mide la roja?          -> 6 cm
        La azul mide 24 cm. La roja mide 1/4 de la azul. Cuanto mide la roja?               -> 6 cm
        La azul mide 24 cm y la roja 6 cm. Cuantas veces es mas larga la azul?             -> 4 veces

  REDONDEAR  ->  a la decena o a la centena MAS CERCANA (paso N.2; 3.NBT.A.1)
        redondear: 37          -> decena 40, centena 0   (las dos)
        redondear: 37 a la decena   -> 40   EN LA RECTA: entre 30 y 40, la mitad es 35, pasa de la mitad
                                            EL ATAJO: la cifra de las unidades es 7 (de 5 para arriba): sube
        redondear: 35 a la decena   -> 40   justo en la mitad: se sube por CONVENIO
        redondear: 247 a la centena -> 200  (no 300: se redondea el numero, no lo ya redondeado)
        redondear: 995 a la decena  -> 1000     redondear: 49 a la centena -> 0
        Los dos caminos se hacen siempre y tienen que coincidir.  Al millar: todavia no.

  ESTIMAR / RAZONABLE  ->  es razonable la respuesta?  estimar redondeando (paso E.6; 3.OA.D.8)
        estimar: 38 + 47            -> cerca de 90   (40 + 50; la cuenta de verdad, entre 80 y 100)
        razonable: 38 + 47 = 75     -> no    (fuera de la banda: la llevada olvidada)
        razonable: 38 + 47 = 95     -> si, pero mal: es 85   (razonable NO es lo mismo que correcta)
        razonable: 3 x 47 = 141     -> si    (3 x 50 = 150; 47 se movio como mucho 5, 3 veces: 15)
        LA BANDA: cada numero se mueve como mucho 5 al redondear a la decena (50 a la centena);
        fuera de la banda la respuesta esta mal SEGURO.  Sumas, restas y un factor de una cifra;
        dividir, o dos factores grandes: todavia no.

  DOS PASOS, CON LA LETRA  ->  ecuaciones con una LETRA en el hueco (paso E.5; 3.OA.D.8)
        3 x 4 - 5 = c          -> c = 7   el orden de siempre: PRIMERO x y :, LUEGO + y -
        2 + 3 x 4 = n          -> 14 (no 20: sin parentesis no se va de izquierda a derecha)
        (2 + 3) x 4 = n        -> 20 (el parentesis manda)
        3 x n + 2 = 14         -> 4    DESHACER de fuera hacia dentro: 14 - 2 = 12, 12 : 3 = 4
        x + 5 = 12             -> 7    la x es LETRA si va donde un numero; entre dos numeros es 'por'
        20 - 2 x n = 8         -> 6        12 : n = 3 -> 4        3 x 4 = ? x 6 -> el hueco = 2
        n + n = 10 -> todavia_no (la letra dos veces)     3 x n + 2 = 13 -> no_sale (no hay entero)
        Siempre comprueba poniendo el numero en la letra (como verdad:).
        Problemas de dos pasos (R.2 y luego un cambio), con la ecuacion escrita con letra:
        Ana tiene 3 bolsas con 4 caramelos cada una. Se come 5. Cuantos le quedan?   -> 7
        Ana tiene 3 bolsas con 4 caramelos cada una. Le dan 5. Cuantos tiene ahora?  -> 17

  TABLAS DEL 11 Y DEL 12  ->  partiendo 10 + 1 y 10 + 2 (paso M.7; NCETM 2.11)
        tabla del 11           -> 0, 11 ... 110    7 x 11 = 7 x 10 + 7 x 1 = 70 + 7
        tabla del 12           -> 0, 12 ... 120    y es el DOBLE de la del 6
        divisible: 84 entre 12 -> si   (entre 3 por las cifras Y entre 4 por dos mitades)
        divisible: 77 entre 11 -> si   (dos cifras iguales)
        aprender: tablas       -> ahora hasta 12 x 12 (al acabar 4.o)

  DIVISION CON RESTO  ->  el resto, en la ecuacion y en los problemas (paso M.8; NCETM 2.12; 4.OA.A.3)
        17 : 5                 -> 3 resto 2;  17 = 3 x 5 + 2;  el resto es MENOR que el divisor
        comprobar: 17 : 5 = 2 resto 7   -> no (la vuelta cuadra, pero con 7 cabe otro grupo de 5)
        Hay 17 ninos. En cada coche caben 5. Cuantos coches hacen falta?        -> 4 (los 2 tambien van)
        Tiene 17 euros. Cada libro cuesta 5 euros. Cuantos libros puede comprar? -> 3 (no llega para otro)
        Reparte 17 caramelos entre 5 ninos. Cuantos sobran?                     -> 2 (el resto)

  POR 10 Y POR 100  ->  las cifras suben o bajan de sitio (paso M.9; NCETM 2.13; 3.NBT.A.3)
        23 x 10                -> 230   cada cifra sube un sitio (las unidades quedan vacias: un cero)
        23 x 100               -> 2300  por 10 dos veces
        47 : 10                -> 4 resto 7   las decenas son el cociente; las unidades sobran
        9 x 80                 -> 720   9 x 8 = 72 (de memoria) y 80 es diez veces 8
        120 : 4                -> 30    12 : 4 = 3 y 120 es diez veces 12

  MULTIPLICACION CORTA  ->  partir por sitios y el algoritmo en columnas (paso M.10; NCETM 2.14; 4.NBT.B.5)
        47 x 6                 -> 282   7 x 6 = 42: escribo 2, llevo 4;  4 x 6 = 24, + 4 = 28 ...
        corta: 347 x 6         -> 2082  el algoritmo dibujado, y comprobado PARTIENDO POR SITIOS:
                                        300 x 6 + 40 x 6 + 7 x 6 = 1800 + 240 + 42
        (Cada columna es un hecho de la tabla: hace falta haberlas aprendido, 'aprender: tablas'.)

  DIVISION CORTA  ->  de izquierda a derecha, cambiando lo que sobra (paso M.11; NCETM 2.15; 4.NBT.B.6)
        72 : 3                 -> 24   7 decenas : 3 = 2 decenas, sobra 1 -> se CAMBIA por 10 unidades -> 12 : 3 = 4
        corta: 305 : 5         -> 61   las 3 centenas no dan para cada uno: pasan a decenas (30)
        corta: 4321 : 7        -> 617 resto 2   (con la vuelta: 617 x 7 + 2 = 4321)

  ECUACION CON x Y :  ->  el hueco en una multiplicacion o division (paso E.4; 3.OA.A.4)
        3 x ? = 12             -> 4    cuantos en cada grupo: REPARTIR 12 entre 3
        ? x 4 = 12             -> 3    cuantos grupos: AGRUPAR 12 en grupos de 4
        12 : ? = 4             -> 3    el divisor: agrupar 12 en grupos de 4
        ? : 3 = 4              -> 12   el dividendo: deshacer, 4 x 3
        5 = ? : 3              -> 15   (el ejemplo del estandar)
        3 x ? = 13             -> no_entero (13 no se reparte justo entre 3)
        0 x ? = 0 -> cualquiera     0 x ? = 5 -> imposible     ? x ? = 12 -> dos huecos
        Se escriben directamente; se comprueban con verdad: (que ya entiende x y :).

  BALANZA  ->  cuentas a los DOS lados del = (paso E.2): los dos platos pesan lo mismo
        8 + 4 = ? + 5          -> 7    compensar: 5 es uno mas que 4, el hueco uno menos que 8
                                       (y dice por que NO 12 ni 17, las respuestas de siempre)
        57 + 22 = ? + 21       -> 58   sin calcular los lados
        8 + 4 = 8 + ?          -> 4    el mismo numero en los dos platos
        15 - 7 = ? - 6         -> 14   calculando un plato (8) y luego E.1
        8 + 4 = ? + 13         -> imposible (el otro plato ya pesa mas)

  VERDAD  ->  el = : VERDADERO o FALSO? (paso E.0; 1.OA.D.7)
        verdad: 4 + 1 = 5 + 2  -> FALSO (5 y 7.  OJO: 4 + 1 da 5, pero el = no dice 'da')
        verdad: 10 = 8 + 2     -> VERDADERO (el resultado tambien puede ir a la izquierda)
        verdad: 7 = 7          -> VERDADERO sin calcular (escrito igual)
        verdad: 5 + 2 = 2 + 5  -> VERDADERO sin calcular (los mismos numeros al reves, P.5)
        verdad: 3 + 5 = 8 + 2 = 10  -> FALSO (en una cadena todos los lados valen lo mismo)
        verdadero o falso: ... -> lo mismo
        El = SIEMPRE significa 'es el mismo numero que' (Progression de Common Core).

  MEMORIA  ->  hechos que se saben de memoria, GANADOS (paso 3)
        aprender: sumas        -> practica las 100 sumas de dos numeros de una cifra y las guarda
        aprender: restas       -> sus restas (la familia de cada suma: 8+5=13 -> 13-5=8)
        memoria                -> que se de memoria y COMO lo aprendi
        olvidar: todo          -> borra la memoria (vuelve a calcularlo todo)
        Un hecho solo entra si lo CALCULE sin memoria, lo COMPROBE por la vuelta y, si hay otro
        metodo, por un SEGUNDO camino.  Al recordarlo lo vuelvo a comprobar: si no cuadra, no lo uso.
        (Common Core 2.OA.B.2: al final de 2.o, 'know from memory all sums of two one-digit numbers'.)

  Los atributos van entre parentesis como nombre=valor, separados por comas;
  las cosas entre si van separadas por punto y coma.
  Si repites un nombre en una escena 0.1, es la MISMA entidad senalada otra vez.
"""

import os
import re
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
    """Devuelve (respuesta normalizada, resultado completo).  Nunca revienta.
    La puerta 'resolver:' (U.1) y la RED DE SEGURIDAD: lo que una puerta vieja no entiende pero el lector
    simbolico lee entero, y el resolvedor resuelve, va al resolvedor (si no, se queda lo de la puerta)."""
    t = texto.strip()
    try:
        if motor.es_orden_resolver(t):
            return _respuesta_resolver(t, saber)
    except Exception:
        return "no_entendido", None
    resp = _preguntar_por_las_puertas(t, saber)
    if resp[0] in ("no_entiendo", "no_entendido"):
        try:
            if motor.es_expresion_simbolica(t) and motor.decidir_resolver(t, saber)["conclusion"] == "hecho":
                return _respuesta_resolver(t, saber)
        except Exception:
            pass
    return resp


def _respuesta_resolver(t, saber):
    r = motor.decidir_resolver(t, saber)
    if r["conclusion"] == "no_entiendo":
        return "no_entiendo", r
    if r["conclusion"] == "hecho":
        return r["respuesta"], r
    return r["conclusion"], r


def _preguntar_por_las_puertas(texto, saber):
    t = texto.strip()
    try:
        if t.lower().strip() in ("piezas", "mapa"):
            return "las_piezas", None
        if motor.es_orden_dos_incognitas(t):              # dos incognitas (S.3; NCETM 1.31): antes que la letra (E.5)
            salida = motor.explicar_orden_dos_incognitas(t, saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if motor.es_orden_factores(t):
            salida = motor.explicar_orden_factores(t, saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if motor.es_orden_equivalentes(t):                 # fracciones equivalentes y simplificar (F.6; NCETM 3.7)
            salida = motor.explicar_orden_equivalentes(t, saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            r = salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip()
            return ({"VERDADERO": "verdadero", "FALSO": "falso"}.get(r, r)), None
        if motor.es_orden_combinar(t):                     # x con + y - (M.16): antes que calcular: y verdad:
            salida = motor.explicar_orden_combinar(t, saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            r = salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip()
            return ({"VERDADERO": "verdadero", "FALSO": "falso"}.get(r, r)), None
        if motor.es_orden_parte_todo(t, saber):              # parte-parte-todo con tres partes o mas (S.2)
            salida = motor.explicar_orden_parte_todo(t, saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if t.lower().startswith("divisible"):
            salida = motor.explicar_divisible(t[len("divisible"):].lstrip(":").strip(), saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if t.lower().startswith("tabla del") or t.lower().startswith("mitad"):
            salida = (motor.explicar_tabla(t, saber) if t.lower().startswith("tabla")
                      else motor.explicar_mitad(t[len("mitad"):].lstrip(":").strip(), saber))
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if motor.es_orden_derivar(t):                        # derivar de un hecho que se sabe (P.7; NCETM 1.29)
            salida = motor.explicar_orden_derivar(t, saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if motor.es_orden_equivalente(t):
            salida = motor.explicar_orden_equivalente(t, saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if motor.es_orden_negativos(t):
            salida = motor.explicar_orden_negativos(t, saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if motor.es_orden_escala(t):
            salida = motor.explicar_orden_escala(t, saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if motor.es_orden_geometria(t):
            salida = motor.explicar_orden_geometria(t, saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if motor.es_orden_dinero(t):
            salida = motor.explicar_orden_dinero(t, saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if motor.es_orden_volumen(t):
            salida = motor.explicar_orden_volumen(t, saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            r = salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip()
            return ({"VERDADERO": "verdadero", "FALSO": "falso"}.get(r, r)), None      # como en verdad: (E.0)
        if motor.es_orden_decimal_por(t):
            salida = motor.explicar_orden_decimal_por(t, saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if motor.es_orden_decimal(t):
            salida = motor.explicar_orden_decimal(t, saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if t.lower().startswith("corta"):
            salida = motor.explicar_corta(t[len("corta"):].lstrip(":").strip(), saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if motor.es_comprobar_division(t):
            salida = motor.explicar_comprobar_division(t, saber)
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if t.lower().startswith("millar") or motor.es_comparar_numeros(t):
            salida = (motor.explicar_millar(t, saber) if t.lower().startswith("millar")
                      else motor.explicar_comparar_numeros(t, saber))
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if motor.es_orden_fraccion(t):
            salida = motor.explicar_orden_fraccion(t, saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if motor.es_division(t):
            r = motor.decidir_dividir(t, saber)
            if r["conclusion"] != "hecho":
                return ("no_se_puede" if r["conclusion"] == "imposible" else r["conclusion"]), None
            return "%d%s" % (r["valor"], " resto %d" % r["resto"] if r["resto"] else ""), None
        if motor.es_multiplicacion(t):
            r = motor.decidir_multiplicar(t, saber)
            return (str(r["valor"]) if r["conclusion"] in ("hecho", "desiguales") else r["conclusion"]), None
        if re.match(r"^(filas:\s*)?\d+\s+(filas?|columnas?)\s+de\s+\d+", t.lower()):
            r = motor.decidir_filas(re.sub(r"^filas:\s*", "", t.lower()), saber)
            return (str(r["valor"]) if r["conclusion"] == "hecho" else r["conclusion"]), None
        if re.match(r"^de\s+\d+\s+en\s+\d+", t.lower()):
            salida = motor.explicar_saltos(t, saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if t.lower().startswith(("estimar", "razonable")):
            salida = (motor.explicar_estimar(t[len("estimar"):].lstrip(":").strip(), saber)
                      if t.lower().startswith("estimar")
                      else motor.explicar_razonable(t[len("razonable"):].lstrip(":").strip(), saber))
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if t.lower().startswith("redondear"):
            salida = motor.explicar_redondear(t[len("redondear"):].lstrip(":").strip(), saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if t.lower().startswith("par:") or t.lower().startswith("par "):
            salida = motor.explicar_paridad(t[3:].lstrip(":").strip(), saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip().lower(), None
        if motor.es_ecuacion_con_letra(t.split(":", 1)[1] if t.lower().startswith(("ecuacion", "hueco")) and ":" in t else t):
            r = motor.decidir_ecuacion_letra(t.split(":", 1)[1] if t.lower().startswith(("ecuacion", "hueco")) and ":" in t else t, saber)
            return (str(r["valor"]) if r["conclusion"] == "hecho" else r["conclusion"]), None
        if t.lower().startswith("ecuacion") or t.lower().startswith("hueco"):
            r = motor.decidir_ecuacion(t.split(":", 1)[1] if ":" in t else t, saber)
            return (str(r["valor"]) if r["conclusion"] == "hecho" else r["conclusion"]), None
        if t.lower().startswith("verdad"):
            resto = t.split(":", 1)[1] if ":" in t else t[len("verdad"):]
            r = motor.decidir_igualdad(resto, saber)
            if r["conclusion"] == "no_entiendo":
                return "no_entiendo", None
            return (r["valor"] if r["conclusion"] == "hecho" else "no_se_puede"), None
        if t.lower().startswith("calcular"):
            salida = motor.explicar_calculo(t[len("calcular"):].strip(), saber)
            if salida.startswith("NO ENTIENDO"):
                return "no_entiendo", None
            return salida.strip().splitlines()[-1].replace("RESULTADO:", "").strip(), None
        if t.lower().strip() == "memoria":
            return "%d hechos" % len(motor.cargar_memoria()), None
        if t.lower().startswith("problema"):
            resto = t[len("problema"):].strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            if not resto:
                return "no_entendido", None
            if motor.es_problema_por(resto, saber):
                r = motor.decidir_R2_problema(resto, saber)
                if r["conclusion"] != "hecho":
                    return r["conclusion"], r
                return "%d%s" % (r["valor"], " resto %d" % r["resto"] if r["resto"] else ""), r
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
        if motor.es_expresion_simbolica(t):                  # la red de seguridad (U.1): numeros y letras, no objetos
            return _respuesta_resolver(t, saber)
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


def correr_mis_casos(saber, mostrar_todo=False, archivo=None, flexible=False, trozo=None):
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

    if trozo:                                      # (k, n): solo los casos k, k+n, k+2n... (la bateria en paralelo)
        casos = casos[trozo[0]::trozo[1]]
    bien = fallos = 0
    for c in casos:
        if flexible:
            c["texto"] = como_problema(c["texto"])
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

def como_problema(texto):
    """Lo que se escribe DIRECTAMENTE, sin orden delante (Carlos: 'la ecuacion directamente y algunas
    palabras'):  una ecuacion con hueco (8 + ? = 11) -> ecuacion;  un problema con su pregunta (?) ->
    problema;  una igualdad sin hueco (8 + 3 = 11) -> verdad;  una cuenta suelta (8 + 3) -> calcular."""
    t = texto.strip()
    if re.match(r"^(verdad|ecuacion|hueco|problema|calcular)\w*\s*:", t.lower()):   # ya lleva su orden
        return t
    if motor.es_orden_dos_incognitas(t):                  # dos incognitas (S.3): a + b = 30; a - b = 8
        return t
    if motor.es_ecuacion_con_letra(t):                    # una ecuacion con LETRA o de dos pasos (E.5)
        return t
    if t.lower().startswith("volumen"):                   # el volumen con hueco (M.14) lleva su orden
        return t
    if motor.es_orden_factores(t):                        # factores, primos, multiplos (M.15): '?' no es un problema
        return t
    if motor.es_orden_parte_todo(t):                      # parte-parte-todo (S.2): el '?' es la parte que falta
        return t
    if motor.es_orden_derivar(t):                         # si 600 - 200 = 400: 600 - 201 = ? (P.7): no es una ecuacion
        return t
    if motor.es_orden_equivalentes(t):                    # 2/3 = ?/12 y 2/3 = 8/12 (F.6): fracciones, no una ecuacion
        return t
    if "=" in t and any(h in t for h in ("?", "_", "\u25a1")):   # una ECUACION con hueco (E.1, E.4)
        return "ecuacion: " + t
    if re.match(r"^[a-z_ ]+:", t.lower()):                 # otra orden con su nombre delante
        return t
    if "?" in t:
        return "problema: " + t
    if re.match(r"^[\d\s+\-=\u2212x*\u00d7]+$", t.lower()) and "=" in t:            # una igualdad sin hueco (E.0)
        return "verdad: " + t
    if re.match(r"^\d+\s*[+\-\u2212]\s*\d+$", t):                   # una cuenta suelta
        return "calcular: " + t
    return t


def interactivo(saber):
    print()
    print("=" * 78)
    print("PROBADOR DE EUCLIDES")
    print("=" * 78)
    # OJO: aqui NO se corren los casos.  Antes se corrian al arrancar y lo unico que hacian era
    # llenar la pantalla de ejemplos antes de dejar escribir.  Ahora se piden con 'casos'.
    print("  escribe lo que quieras probar y pulsa Enter.")
    print("  UN PROBLEMA se puede escribir directamente, con su pregunta:")
    print("      Ana tiene 8 manzanas. Tiene 3 mas que Luis. Cuantas tiene Luis?")
    print("  y se ve TODO el proceso: como lo lee, que prueba, que descarta y por que, la cuenta")
    print("  y la comprobacion.")
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
            print(motor.explicar_pregunta(como_problema(entrada), saber))
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
        trozo = None
        if len(argv) >= 4 and argv[2] == "--trozo":          # --casos --trozo 0/4  (lo usa correr_todas.py)
            k, _, n = argv[3].partition("/")
            trozo = (int(k), int(n))
        bien, fallos = correr_mis_casos(saber, mostrar_todo=True, trozo=trozo)
        return 1 if fallos else 0

    # 'ayuda' como argumento tambien tiene que dar la ayuda (antes lo tomaba por una ESCENA y
    # contestaba 'un_objeto', porque 'ayuda' es un nombre de objeto perfectamente valido).
    if len(argv) >= 2 and argv[1].strip().lower() in ("ayuda", "--ayuda", "-h", "--help"):
        print(AYUDA)
        return 0

    if len(argv) >= 2:
        print(motor.explicar_pregunta(como_problema(" ".join(argv[1:])), saber))
        return 0

    interactivo(saber)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
