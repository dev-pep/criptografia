# BIP-39

Este documento expone una forma estándar de generar una semilla (*seed*) a partir de una frase semilla (*seed phrase*). Dicha semilla se utilizará luego para generar un monedero de criptomonedas.

## Seed phrase

Las palabras se escogen de [una lista](../datos/wordlist.json) de 2048 posibles (*wordlist*). Por lo tanto, cada palabra tendrá un índice de 11 bits. La frase contiene normalmente entre 12 y 24 palabras, de tal modo que define un entero de entre 132 (12x11) y 264 (24x11) bits.

La *seed phrase* contiene, en sí, un mecanismo de *checksum*, con lo que no todas las combinaciones de palabras son válidas: de cada 33 bits, 32 pertenecen a la llamada **entropía**, y uno a dicho ***checksum***.

Supongamos, por ejemplo, una *seed phrase* de 12 palabras. En este caso, tenemos 132 bits, de los cuales los 128 primeros corresponden a la entropía, y los 4 finales al *checksum*. La entropía es siempre 32 veces más larga que el *checksum*. La única razón de dividir entre entropía y *checksum* es para disminuir la probabilidad de introducir frases incorrectas.

Las palabras de la *wordlist* (en inglés) se han elegido de tal forma que es poco probable confundir una palabra con otra. Por otro lado, existen *wordlists* en otros idiomas, aunque se recomienda utilizar la lista en inglés, ya que tiene un alfabeto poco ambiguo, y la codificación de sus caracteres es *ASCII* simple.

Dado que para obtener la semilla del monedero (semilla BIP-39) se utiliza la codificación *UTF-8* de la *seed phrase*, en algunos idiomas es necesario pre-procesar la frase para que se usen caracteres ambiguos (con distintas codificaciones, compuestos, etc.) de una forma estandarizada. Esto no es necesario si se usa la *wordlist* inglesa.

A partir de la *seed phrase*, se usará una función *PBKDF2*, que usa internamente una función *HMAC*, que utiliza a su vez una función *SHA-512*, del modo que se describirá a continuación. El resultado es una **semilla de 512 bits**.

## HMAC

Un algoritmo *HMAC* (*hash-based message authentication code*) sirve para garantizar la autenticidad de un mensaje cuando no se dispone de una infraestructura de clave pública, en el que se envía una firma digital junto con el mensaje. En *HMAC* no existe tal firma.

El primer paso es compartir una contraseña secreta entre las dos partes (con Diffie-Hellman, o similar).

El remitente envía, por un lado, el mensaje en claro, y por otro, el código de autenticación del mensaje (*MAC*) que es el resultado de una función *HMAC*, la cual tiene **dos entradas: la clave secreta y el mensaje** en sí. El *digest* resultante depende pues de esa clave secreta y del mensaje.

El receptor recibe el mensaje y el *digest*. Como posee también la contraseña (y por supuesto el mensaje recibido), puede aplicar la función *HMAC* con las mismas entradas, y si coincide con el *MAC* recibido, el mensaje es auténtico.

Si un tercero intercepta la transmisión, no será capaz de comprobar la autenticidad del mensaje porque no posee la clave.

Dado que una función *HMAC* tiene dos entradas y produce un código a la salida, se han encontrado otros usos para esta función (se verán más abajo).

### Funcionamiento

La función *HMAC* está sustentada sobre una función *hash*, que llamaremos $H()$. Dependiendo pues de cuál sea $H$, hablaremos de las funciones *HMAC-SHA256*, *HMAC-SHA3-512*, etc. La función *hash* elegida nos marcará los otros dos parámetros de la función *HMAC*:

- El tamaño de salida: número de bits del código resultante, que es igual al tamaño de salida del *digest* de la función *hash* utilizada.
- El tamaño de bloque, utilizado internamente por *HMAC*, el cual es siempre mayor que el tamaño de salida.

Para el ejemplo concreto de la *HMAC-SHA512* (muy utilizada en los estándares de *blockchain*), el tamaño de salida es 512 bits (porque la función *hash* es la *SHA-512*), es decir 64 bytes; y el tamaño de bloque de trabajo es de 1024 bits (128 bytes).

Dicho esto, y teniendo $K$ la contraseña secreta, $m$ el mensaje a transmitir y $H$ la función *hash* usada por la *HMAC*, el resultado concreto de la función es:

$HMAC(K,m) = H((K' \oplus opad) \parallel H((K' \oplus ipad) \parallel m))$

Aquí, $\oplus$ indica operación *XOR* bit a bit, $\parallel$ es concatenación de bytes. En cuanto a $K'$, se halla de la siguiente manera:

Si $K$ es **más largo** que el tamaño de bloque interno, $K'=H(K)$; de lo contrario, $K'=K$. Una vez hecha esta corrección, se rellenará $K'$ con bytes 0, hasta que tenga la longitud del bloque (en el caso de *HMAC-SHA512*, 128 bytes).

Para evitar trabajar con valores de $K'$ con muchos ceros a la derecha, se utilizan los valores $ipad$ y $opad$, los cuales tienen un tamaño igual al bloque interno, y son la repetición del byte 0x36 ($ipad$) y del byte 0x5c ($opad$).

### Otros usos: sal + digest

En un sistema determinado, era muy frecuente que las contraseñas se almacenasen mediante su *hash*, por seguridad. Pero esto, a la larga llevó a la recopilación de millones de *hashes* de contraseñas simples, que facilitaban encontrar *hashes* conocidos.

Para ello, en lugar de aplicar una función *hash* a la contraseña (cuya salida depende solamente de esta), se genera una pequeña secuencia de caracteres aleatoria (la **sal**), se aplica la *HMAC* junto con la contraseña; finalmente se almacenan tanto la sal como el *digest*. Así, para verificar la validez de la constraseña introducida por el usuario, se aplica la *HMAC* a esa sal y esa contraseña introducida. Si coincide, es correcta. Con esta técnica, ya no tiene sentido generar y almacenar *hashes* para buscar coincidencias.

### Otros usos: derivación de claves

La derivación de claves (*key derivation*) sirve para derivar (obtener) una o más claves secretas, y con una longitud determinada, a partir de una contraseña memorizable (como una contraseña maestra). Es decir, a partir de una contraseña más o menos fácil de recordar, se puede aplicar una función *HMAC* a dicha contraseña y a una sal (que suele ser un parámetro fijo del sistema) para obtener un código. Este código se puede volver a introducir en la función *HMAC* junto con la contraseña memorizable nuevamente, para obtener otro código. Y así iterar cientos (o miles) de veces para obtener una clave derivada, todo lo compleja (larga) que se desee.

Esto es lo que hacen las funciones derivadoras de claves. Utilizan una *HMAC* (que a su vez utiliza una función *hash*) para iterar varias veces y obtener una clave a partir de una contraseña (la sal inicial, fija o parametrizada, formaría parte de la configuración de esa derivación). La clave obtenida (derivada) está lista para usarse para otros métodos criptográficos. Así, no es necesario recordar la clave derivada, sino únicamente la contraseña (normalmente más fácil de recordar).

## PBKDF2

En el documento BIP-39 se utiliza un algoritmo de derivación de claves llamado *PBKDF* 2 (*password-based key derivation function 2*), el cual genera la semilla (*seed*) BIP-39 aplicando varias iteraciones de una función *HMAC* sobre la frase semilla (*seed phrase*) y un valor de sal inicial. Los parámetros de una función de derivación de claves *PBKDF* 2 son, para hallar la *seed* BIP-39 a partir de la *seed phrase*:

- Función pseudoaleatoria: la función *HMAC* a utilizar con su correspondiente función *hash*. En este caso es la función *HMAC-SHA512*.
- Contraseña: contraseña memorizable de la que derivar una clave segura. En este caso, la *seed phrase*, que debe cumplir con los requisitos BIP-39.
- Sal inicial: secuencia de bits usada en la primera iteración. En este caso, la secuencia de bytes "mnemonic", a la que se concatena una contraseña (*passphrase*) opcional.
- c: número de iteraciones. En este caso, 2048.
- dkLen: longitud de la clave derivada deseada. En este caso, 512 bits.

En las sucesivas llamadas a *HMAC-SHA512*, se pasa la *seed phrase* al parámetro de clave. Al parámetro mensaje, a partir de la segunda llamada se pasa un determinado valor cambiante.

Se pueden utilizar los parámetros aconsejados en el BIP-39 para generar la *seed*, pero también podríamos optar por utilizar nuestros propios parámetros (cambiar la sal inicial por una contraseña propia, distinto número de iteraciones, distinto juego de palabras, etc.). Esto es lo que hacen algunos clientes (programas monedero). Los clientes que se ajusten a este estándar serán todos compatibles entre sí, y una misma *seed phrase* serviría para todos ellos.
