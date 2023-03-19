# BIP-32

Este documento especifica cómo crear un **monedero determinista jerárquico** (*Hierarchical Deterministic Wallet*, *HDW*) a partir de una semilla (*seed*), obtenida preferentemente mediante la especificación *BIP-39*.

## Introducción: monederos

Un monedero no es más que una combinación de una clave privada y una clave pública, de tal manera que se puedan firmar transacciones monetarias en el ámbito de las criptomonedas, y recibir fondos en el mismo monedero.

Para obtener un monedero, pues, solo hay que generar ese par de claves. Una forma sería mediante la **creación aleatoria** y almacenamiento de esas claves. Esto sería un monedero **no determinista**, y no lleva ningún proceso especial de creación, a parte de la aleatoriedad. Para trasladar el monedero habría que copiar las claves de un lugar a otro.

Sin embargo, es más cómodo recordar una información mnemónica como la *seed phrase* expuesta en *BIP-39*, a partir de la cual poder generar el monedero en cualquier cliente de criptomonedas. Esto es un **monedero determinista**. Evidentemente, los softwares de creación de los monederos de origen y destino deben usar el mismo procedimiento y los mismos parámetros, por ejemplo los parámetros exactos indicados en *BIP-39* y *BIP-32*, pues de lo contrario, una misma *seed phrase* generaría monederos distintos. en ambos softwares (clientes).

### Clientes de criptomonedas

Muchos clientes son incompatibles entre sí, usando su propia *wordlist*, o cambiando cualquier parámetro del sistema (incluso usando un sistema completamente distinto), de tal modo que la *seed phrase* solo sirve para trasladar el monedero al mismo cliente (en otro equipo o en el mismo).

Un software cliente, llamado normalmente un "monedero", es cualquier programa que permita esa generación de claves (de monederos), así como la obtención de la *seed phrase* para traslado o recuperación del monedero, firmar transacciones (enviar fondos), etc.

### Monederos deterministas

Un monedero es determinista cuando utiliza un mecanismo para su generación tal que la semilla obtenida genera siempre el mismo par de claves. En clientes que cumplan la presente especificación, el monedero se puede trasladar de uno a otro cliente. Pueden ser de varios tipos: únicos (si generan una sola dirección), secuenciales o jerárquicos.

Tener varias direcciones en un monedero podría verse como tener varias cuentas en un banco.

### Monederos secuenciales

Un monedero secuencial determinista genera varias direcciones, es decir, varias cuentas de criptomoneda, y lo hace de forma secuencial. A partir de una semilla, se generarán 2, 3, o más direcciones.

Una forma sería obteniendo claves privadas aleatoriamente mediante una función del tipo $H(seed+n)$, donde $H$ sería una función *hash*, *seed* nuestra semilla, y $n$ tomaría varios valores 0, 1, 2...

### Monederos jerárquicos

El monedero jerárquico determinista es similar al monedero secuencial, en cuanto a que genera múltiples direcciones. Sin embargo, en lugar de ser una serie de direcciones generados secuencialmente, se crea un árbol de direcciones, con un nodo raíz (o maestro), con varios nodos hijo (cada uno representando una dirección), que a su vez pueden tener varios nodos hijo. Así, habría direcciones a distintos niveles.

Veremos aquí la técnica que expone *BIP-32* para la creación de estos monederos jerárquicos.

## Bases

Los pares de claves generados pertenecerán al sistema de encriptación con curva elíptica, específicamente usando la curva *SECP256K1*. Así, la clave privada será un número entero módulo $n$ (orden de la curva), y la pública, el punto en la curva correspondiente al indicado por la clave privada.

Las conversiones entre enteros y series de *bytes* son *big endian* (el *byte* más significativo primero).

> Cuando hablemos de valores compuestos por bits, no distinguiremos entre secuencias de *bytes* y tipos enteros, pues ambas formas guardan la misma información. Se usará el tipo que corresponda mejor en cada caso.

## Claves extendidas

Cada nodo del árbol contendrá tres elementos importantes:

- Una clave privada: un número entero $k$ (será módulo $n$).
- Una clave pública: un punto de la curva $K$, siendo este $K=kG$ ($G$ es el punto generador de la curva).
- Un código de cadena (*chain code*) particular $c$, que extiende la entropía del nodo.

Se llama **clave privada extendida** al par $(k,c)$, y **clave pública extendida** al par $(K,c)$. Ambas comparten el mismo *chain code* dentro del nodo.

## Representación de los datos

Tanto el *chain code* como la clave privada son secuencias de 256 bits (32 *bytes*), representables tanto como entero como secuencia de *bytes* (siempre *big endian*).

Sin embargo, los puntos de la curva elíptica están formados por un par de coordenadas $(x,y)$. Para representar, pues, un punto de la curva, hay que serializarlo (convertirlo en una secuencia de *bytes*, o un entero incluso).

La serialización de un punto tiene esta forma:

- 1 *byte* prefijo con el siguiente valor:
    - 0x02 si la coordenada $y$ es par.
    - 0x03 si la coordenada $y$ es impar.
- Los 32 *bytes* de la coordenada $x$.

Así, la serialización de un punto de la curva tiene 33 *bytes*.

> Dada una coordenada $x$, existen 2 coordenadas $y$ posibles, que son $y=a$, y $y=-a$; como las operaciones son módulo $p$, estas dos posibilidades son congruentes con $a$ y $p-a$. Como $p$ es un número impar (y primo), entonces si $a$ es par, $p-a$ es impar, y viceversa. Por lo tanto, es suficiente saber si la coordenada $y$ es par o impar para saber cuál de las dos posibilidades es.

## Obtención de las claves maestras

A partir de una semilla como la obtenida a partir de la *seed phrase* (*BIP-39*), obtenemos el primer nodo del árbol, o **nodo maestro** (*master node*); la clave privada del nodo maesto, se simboliza como $m$ (la pública es $M$).

Se utiliza como entrada pues, una semilla de entre 128 y 512 bits de tamaño. En el caso de utilizar *BIP-39* para generar la semilla, disponemos de un valor $S$ de 512 bits ().

Calculamos $I = HMAC-SHA512(key="Bitcoin seed", data=S)$, que es a su vez un valor de 512 bits.

Partimos $I$ en dos partes de 256 bits: $I_L$ y $I_R$ (parte izquierda y parte derecha respectivamente).

Ya tenemos la clave privada del nodo maestro (*master private key*): $k=I_L$. También tenemos el *master chain code*: $c=I_R$. En el caso de que $I_L=0$ o $I_L \geq n$, la clave es inválida y hay que probar con otra semilla.

Una vez obtenida la clave privada, obtener la pública es muy sencillo: solo hay que calcular el punto $M=mG$.

## Huella (identificador)

Un nodo puede identificarse usando una función *Hash160*, que no es más que la aplicación del *hash RIPEMD-160* tras un *SHA-256* de la serialización **de la clave pública** (serialización de un punto) correspondiente a ese nodo.

Los primeros 32 bits (4 *bytes*) de este identificador forman la llamada **huella de la clave** (*key fingerprint*), que es en realidad la huella de ese nodo.

## Serialización de claves extendidas

Las claves **extendidas** se serializan utilizando una serie de campos concatenados:

- Versión: 4 *bytes* con uno de estos valores:
    - 0x0488b21e: clave pública, red principal (*mainnet*).
    - 0x0488ade4: clave privada, red principal (*mainnet*).
    - 0x043587cf: clave pública, red de pruebas (*testnet*).
    - 0x04358394: clave privada, red de pruebas (*testnet*).
- Profundidad: un *byte* con el nivel del nodo (0 para el maestro, 1 para sus nodos derivados, 2,...).
- Huella: 4 *bytes* con el *fingerprint* de la clave del padre (0x00000000 si es el nodo maestro).
- Número de hijo: 4 *bytes* indicando el índice usado para derivar el hijo.
- El *chain code* (32 *bytes*).
- La clave en sí (33 *bytes*):
    - Si es una clave pública, serializada como punto de la curva.
    - Si es una clave privada, un *byte* 0x00 seguido por la clave en sí.

Una vez obtenidos estos 78 *bytes* se pueden codificar del siguiente modo:

- Realizar un doble *hash SHA-256* sobre ellos, es decir, aplicarles dicho *hash*, y al *digest* resultante, volvérselo a aplicar. Utilizar los primeros 4 *bytes* del resultado y añadirlos a los 78 *bytes* iniciales (ahora tenemos 82 *bytes*).
- Codificar los 82 *bytes* con Base58.

Así, obtenemos un *string* de hasta 112 caracteres, que empezará por ***xpub***, ***xprv***, ***tpub*** o ***tprv***.

## Derivación de claves

A partir de un nodo cualquiera del árbol, se pueden derivar los tres valores mencionados para obtener el contenido de un nodo hijo, el cual obtendrá sus propios valores (claves privada y pública, y *chain code*).

La función para derivar (obtener las claves del nodo hijo a partir de las del padre) toma como argumentos **la clave extendida** (privada o pública) del padre y un **número de índice** $i$ (número de hijo), retornando la clave extendida (privada o pública) del hijo.

## Claves normales y endurecidas

El índice o número de hijo $i$ puede tomar un valor cualquiera entre $0$ y $2^{32}-1$. De estos índices, la mitad (de $0$ a $2^{31}-1$) generarán claves extendidas **normales**, mientras que la otra mitad (de $2^{31}$ a $2^{32}-1$) generarán las llamadas claves extendidas **endurecidas** (*hardened extended keys*).

Para denotar derivación normal o endurecida se utiliza la notación $i_H$. Así, por ejemplo, el índice $3_H$ es en realidad $2^{31} + 3$.

## Funciones de derivación (CKD)

### Derivación de clave privada extendida

La función $CKD_{priv}$ recibe como entrada, por un lado, el par $(k,c)$, es decir, clave privada extendida, y por otro, el número $i$, es decir, el índice del hijo a derivar. El resultado es la clave privada extendida del hijo número $i$, es decir, el par $(k_i,c_i)$:

$CKD_{priv}((k,c),i)=(k_i,c_i)$

El algoritmo es el siguiente:

- Si $i \geq 2^{31}$, generaremos una clave extendida privada del hijo, que será una ***hardened key*** ($k$ son 32 *bytes*, $i$ son 4 *bytes*):
    - $I=HMAC-SHA512(key=c, data=k33 \parallel i)$, donde $k33=0x00 \parallel k$ (33 *bytes*).
- Si no, generaremos una clave extendida privada **normal** del hijo:
    - $I=HMAC-SHA512(key=c, data=K33 \parallel i)$, donde $K33$ es la serialización del punto $kG$, como se ha explicado anteriormente (también 33 *bytes*).
- Una vez hecho esto, el resultado $I$, de 512 bits (64 *bytes*), se divide en dos partes de 256 bits (32 *bytes*): $I_L$ (izquierda) y $I_R$ (derecha).
- La clave privada del hijo es $k_i=I_L+k \bmod n$. Si $I_L \geq n$, o $k_i=0$, esta clave no es válida y debería procederse con un hijo distinto.
- El *chain code* del hijo $c_i$ es $I_R$.

A partir de la clave privada extendida del hijo obtenida, se puede fácilmente calcular la clave pública extendida de ese hijo.

### Derivación de clave pública extendida

La función $CKD_{pub}$ recibe como entrada, por un lado, el par $(K,c)$, es decir, clave pública extendida, y por otro, el número $i$, es decir, el índice del hijo a derivar. El resultado es la clave pública extendida del hijo número $i$, es decir, el par $(K_i,c_i)$:

$CKD_{pub}((K,c),i)=(K_i,c_i)$

En este caso, la función solo está definida para claves normales, **no se pueden derivar** ***hardened keys***, por lo tanto, $i<2^{31}$ siempre.

El algoritmo es el siguiente:

- $I=HMAC-SHA512(key=c, data=K33 \parallel i)$, donde $K33$ es la serialización de la clave pública $K$, es decir la serializadión del punto $K$ (33 *bytes*). En este caso, $i$ ocupa nuevamente 4 *bytes*.
- Se divide $I$, de 512 bits (64 *bytes*), en dos partes de 256 bits (32 *bytes*): $I_L$ (izquierda) y $I_R$ (derecha).
- La clave pública del hijo es una suma de dos puntos de la curva: $K_i=I_L \cdot G+K$. Si $I_L \geq n$, o si $K_i$ es el punto en el infinito, esta clave no es válida y debería procederse con un hijo distinto.
- El *chain code* del hijo $c_i$ es $I_R$.

## Clave privada extendida del padre a pública del hijo

El algoritmo de derivación de la clave privada no *hardened* está diseñado de tal forma que a partir de la clave privada del padre, se puede llegar a la clave pública del hijo por dos caminos:

- Calculando la clave pública del padre a partir de su clave privada y luego derivando esa clave pública.
- Derivando la clave privada del padre (derivación no *hardened*), y luego calculando la clave pública del hijo a partir de esa clave derivada.

En ambos casos obtenemos la misma clave. Es decir, suponiendo que las claves extendidas del padre son $k_{padre}$ (privada) y $K_{padre}$ (pública), y la función $N(k)=K$ calcula la clave pública que corresponde a la clave privada que le indicamos como entrada, entonces:

$CKD_{pub}(N(k_{padre})) = N(CKD_{priv}(k_{padre}))$

> Recordemos que los índices *hardened* no están disponibles en la derivación de clave pública extendida.

## Árbol y rutas de derivación

De esta forma, vamos formando un árbol, desde el nodo maestro, derivando las claves privadas extendidas para obtener nuevos nodos con su par de claves y su *chain code*.

En caso de derivar una clave pública extendida, lo que obtenemos es un nodo hijo con clave pública extendida, pero sin clave privada. Es decir, un nodo calculado a partir de la clave pública extendida del padre, no tendrá clave privada, ni él ni sus descendientes (que deberemos calcular a mediante $CKD_{pub}$).

Las rutas de derivación son un identificador de un nodo dentro del árbol. Indica la ruta desde el nodo raíz (indicado como ***m***), hasta el nodo en cuestión. Cada parte de la ruta indica el número de hijo, con un formato del tipo ***m/a/b/c***, con tantos elementos como niveles. Por ejemplo, el nodo ***m/0/1*** indica: partiendo de la clave privada extendida del nodo maestro (***m***) derivamos la clave privada extendida del hijo ***0***, y a partir de esta, derivamos la clave privada extendida de su hijo ***1***. En este caso, han sido dos derivaciones **normales**.

Para referirnos a derivaciones *hardened*, utilizaremos el carácter apóstrofe (***'***). Por ejemplo: ***m/2'/0/3'*** indica una primera derivación *hardened* (hijo *hardened* 2), luego una derivación normal (0) y por último una derivación *hardened* (*hardened* 3).

Por otro lado, también podemos referirnos a derivaciones de clave pública extendida. Los siguientes ejemplos producen el mismo resultado:

- ***M/3/0*** parte de la clave pública extendida del nodo maestro.
- ***N(m)/3/0*** es lo mismo.
- ***N(m/3)/0*** realiza una primera derivación de clave privada extendida, luego calcula la clave pública y finalmente realiza una derivación de clave pública extendida.
- ***N(m/3/0)*** realiza dos derivaciones de clave privada extendida y finalmente hace el cálculo de la clave pública.

En el caso de que hubiera un paso con derivación *hardened*:

- ***N(m/3'/0)*** es correcto.
- ***N(m/3')/0*** es correcto (mismo resultado).
- ***N(m)/3'/0*** no es posible.

## Uso

La idea general es que un par de claves (pública + privada) definen una cuenta de criptomoneda. En general, a partir de la clave pública se obtiene una dirección pública, que es la que se usará para recibir pagos, con lo que deberemos compartir esa clave pública o dirección pública si queremos que alguien realice una transacción hacia nuestra dirección.

Por otro lado, una clave privada se utiliza para obtener la correspondiente dirección privada, que no hay que compartir más que con quien deba tener acceso a los fondos de esa dirección. Con la clave privada se firma una transacción (mediante *ECDSA*), y se envía esa transacción firmada al *blockchain*.

Entonces, el uso del árbol de nodos visto hasta ahora es precisamente otorgar a terceros la posibilidad de acceder a la información que nosotros deseemos.

El documento *BIP-32* hace unas sugerencias generales acerca del uso del árbol de claves. Una posibilidad es, a partir del nodo maestro, generar una serie de cuentas correspondientes a los hijos de dicho nodo. Tomemos una de esas cuentas; podríamos dotarla de dos cadenas de claves (*key chains*) llamadas **cadena interna** y **cadena externa**.

La cadena externa, correspondiente al hijo 0 de esa cuenta, se podría compartir con terceros entregándoles la clave pública y el *chain code*, es decir, la **clave pública extendida**. Así, tal tercero podría generar todo un subárbol de claves públicas, en cada una de las cuales se podrían recibir fondos. Esto sería útil, por ejemplo, si el monedero es propiedad de una empresa que tiene una página *web* desarrollada por un una compañía externa. Los desarrolladores indicarán las direcciones públicas necesarias para recibir los pagos *online*, pudiendo generar todos los que deseen (la idea sería no dejar huecos en los índices), subdividiendo el árbol como desearan, utilizando cada dirección pública para un producto, cliente o familia de productos, etc.

El departamento de contabilidad de la propia empresa sí dispondría de las claves privadas extendidas, con lo que podría generar las claves privadas correspondientes a esas cuentas, para posteriormente redistribuir los fondos que hubiesen entrado.

En cuanto a la cadena interna de una cuenta, estaría formada por subcuentas que no tuviesen nada que ver con el exterior, y para el propio funcionamiento interno de la empresa.

Por ejemplo, en el caso de la cuenta ***m/3'***, podríamos compartir ***N(m/3'/0)*** de tal modo que se realizarían pagos por parte de los clientes en ***m/3'/0/0***, ***m/3'/0/1***, ***m/3'/0/2***, etc. Mientras que para uso interno tendríamos las cuentas ***m/3'/1/0***, ***m/3'/1/1***, ***m/3'/1/2***.

Otro uso de compartir una clave pública extendida, es, por ejemplo, para dar a un auditor la posibilidad de comprobar todas las cuentas de una cadena (o subárbol). En este caso, el auditor podría ir generando claves, y comprobando las transacciones en el *ledger*, es decir, en el *blockchain* (un *blockchain* proporciona la información de **todas** las transacciones públicamente).

> La única forma de saber si dos direcciones públicas (o dos clave públicas) pertenecen al mismo árbol, y por tanto a la misma persona o entidad, es disponiendo de claves públicas extendidas. Por eso se dice que proporcionando una clave pública extendida se pierde privacidad en cuanto a ese subárbol, mientras que proporcionando una clave privada extendida se pierde el dinero de ese subárbol.

### Seguridad

Dando una clave pública, un atacante no puede hallar la correspondiente clave privada.

Dando una clave privada extendida $(k_i,c_i)$ y su correspondiente índice $i$ (por ejemplo a una de las sucursales de nuestra empresa), un atacante no podría encontrar la clave privada del nodo padre.

> No es algo inmediato de fácil deducción, pero es bueno saber que el conocimiento de la clave pública extendida de un nodo más una clave privada no *hardened* de alguno de sus descendientes, es equivalente a saber la clave privada extendida de ese nodo (y así todos los pares extendidos del subárbol entero). Por eso es útil la derivación *hardened*. En todo caso, hay que ir con cuidado a la hora de compartir claves públicas **extendidas**.

## BIP-44

El documento *BIP-44* aconseja un uso concreto del árbol de nodos.

El nivel 0 es, en todos los casos, el nodo maestro, y ahí no puede haber cambio.

El siguiente nivel (nivel 1) sirve para definir el propósito, es decir, para especificar el formato que tendrá el subárbol. En este caso, será el hijo 44, indicando que este subárbol tiene este formato. Esta derivación es *hardened*. El hecho de que el nivel 1 marque el estándar utilizado por el subárbol es precisamente lo que recomienda *BIP-43*.

En el nivel 2 tenemos la moneda para la que se usará el el subárbol. Dado que utilizar un mismo par de claves (un mismo nodo, la misma dirección) para monedas distintas puede llevar distintos problemas, aunque puede hacerse (es típico usar una misma dirección para monedas que usan el mismo método de generación de direcciones a partir de las claves). En este caso, tendríamos en este nivel un subárbol para cada moneda. Esta derivación es *hardened*.

El nivel 3 es para las distintas cuentas que queramos tener de cada moneda, empezado por la 0. Disponemos de un par de miles de millones de cuentas a nuestra disposición. La derivación es *hardened*.

El nivel 4 está pensado para el cambio. A *grosso modo*, en el caso específico de Bitcoin, las transacciones no pueden ser de una cantidad arbitraria de moneda. Por el modo en que está diseñado, sino que es frecuente tras recibir un pago, tener que devolver el "cambio", como hace el dependiente en una tienda de chuches.

De esta forma, el nivel 4 tendrá dos nodos, el 0 y el 1. Cada nodo tendrá a su vez una cadena de hijos, que formarán el nivel más bajo del árbol (nivel 5). Tanto el nivel 4 como el 5 son derivaciones normales.

El nodo 0 del nivel 4 se usará para recibir pagos, es decir, se compartirán las claves públicas de sus hijos. El hijo correspondiente del nivel 1 se utilizará para enviar ese cambio.

Supongamos que tenemos la cuenta ***m/44'/0'/7'*** para recibir pagos. Es decir: nodo maestro; estándar *BIP-44*; moneda Bitcoin (tiene el número 0), y cuenta número 7. Entonces, nuestra cadena externa será la ***m/44'/0'/7'/0***, es decir, compartiremos las claves públicas de ***m/44'/0'/7'/0/0***, ***m/44'/0'/7'/0/1***, ***m/44'/0'/7'/0/2***, etc. (o la clave pública extendida de ***m/44'/0'/7'/0*** para que alguien comparta las claves mencionadas). En este caso, cuando recibamos un pago en, por ejemplo, la cuenta ***m/44'/0'/7'/0/147***, utilizaremos la cuenta interna (o cuenta de cambio) ***m/44'/0'/7'/1/147*** para retornar el cambio al pagador. De todo esto se debe encargar el cliente (software monedero), sin que el usuario tenga que conocer todos estos mecanismos.

Veamos otro ejemplo: podríamos tener, además (o solamente), un nodo para cuentas Ethereum (moneda con número 60). En este caso, no es necesario tener una cadena de cambio, puesto que en Ethereum las transacciones sí pueden tener el tamaño que deseemos. Por tanto, en lugar de tener cadena 0 y cadena 1, solo suele haber una cadena 0 en árboles Ethereum. Una dirección así podría ser la ***m/44'/60'/7'/0/35***. No es necesario tener la cuenta asociada ***m/44'/60'/7'/1/35***.

En cuanto al software monedero, al generar el árbol, debe realizar un descubrimiento de cuentas, es decir, en la cadena externa, empezará por el 0, y si esta tiene transacciones en la *blockchain*, seguirá con la 1, la 2, etc., hasta encontrar un hueco (*gap*) prudencial de direcciones sin transacciones (actualmente se recomienda 20). En la cadena interna (si existe) no hace falta buscar, solo replicar lo encontrado en la externa, porque las cuentas internas están asociadas a las respectivas cuentas de la cadena externa.
