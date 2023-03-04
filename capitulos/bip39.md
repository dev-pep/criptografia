# BIP-39

La *seed phrase* contiene, en sí, un mecanismo de *checksum*, con lo que no todas las combinaciones de palabras son válidas. Para más detalles al respecto, véase el código fuente en ***bip39.py***.

## HMAC

Un algoritmo *HMAC* (*hash-based message authentication code*) sirve para garantizar la autenticidad de un mensaje cuando no se dispone de una infraestructura de clave pública, en el que se envía un *digest hash* firmado. Con *HMAC* no existe tal firma.

El primer paso es compartir una contraseña secreta entre las dos partes (con Diffie-Hellmann, o similar).

El remitente envía, por un lado, el mensaje en claro, y por otro, el código de autenticación del mensaje (*MAC*) que es el resultado de una función *HMAC*, la cual tiene **dos entradas: la clave secreta y el mensaje** en sí. El *digest* resultante depende pues de la clave y el mensaje.

El receptor recibe el mensaje y el *digest*. Como posee la contraseña y el mensaje, puede aplicar la función *HMAC* sobre mensaje y clave, y si coincide con el *digest* recibido, el mensaje es auténtico.

Si un tercero intercepta la transmisión, no será capaz de comprobar la autenticidad del mensaje porque no posee la clave.

Dado que una función *HMAC* tiene dos entradas y produce un código a la salida, se han encontrado otros usos para esta función.

### Otros usos: sal + digest

En un sistema determinado, era muy frecuente que las bases de datos de contraseñas almacenasen su *hash* en lugar de la contraseña, por seguridad. Pero esto, a la larga es inseguro también, ya que muchas contraseñas son simples y se pueden repetir. Se podrían recopilar millones de *hashes* de contraseñas simples, y en cuestión de tiempo encontraríamos un *hash* conocido en una base de datos del sistema.

Para ello, en lugar de aplicar una función *hash* y almacenar, se genera una pequeña secuencia de caracteres aleatoria (la **sal**), se aplica la *HMAC* con la contraseña a guardar y la sal, y se almacena la sal + el *digest*. Así, para verificar la validez de la constraseña introducida por el usuario, se aplica la *HMAC* con esa sal y esa contraseña. Si coincide, es correcta. Con esta técnica, ya no tiene sentido generar y almacenar *hashes* para buscar coincidencias.

### Otros usos: derivación de claves

La derivación de claves (*key derivation*) sirve para derivar (obtener) una o más claves secretas, a partir de una contraseña memorizable (como una contraseña maestra). Es decir, a partir de una contraseña más o menos fácil de recordar, se puede aplicar una función *HMAC* a dicha contraseña y a una sal (que suele ser un parámetro fijo del sistema) para obtener un código. Este código se puede volver a introducir en la función *HMAC* junto con la contraseña memorizable nuevamente, para obtener otro código. Y así iterar cientos (o miles) de veces para obtener una clave derivada, todo lo compleja que se desee.

Esto es lo que hacen las funciones derivadoras de claves. Utilizan una *HMAC* (que a su vez utiliza una función *hash*) para iterar varias veces y obtener una clave a partir de una contraseña.

En BIP-39 se utiliza un algoritmo de derivación de claves llamado *PBKDF* 2 (*password-based key derivation function 2*), el cual genera una clave aplicando varias iteraciones de una función *HMAC* sobre una contraseña de entrada y una valor de sal inicial. La clave obtenida (derivada) está lista para usarse para otros métodos criptográficos. Así, no es necesario recordar la clave derivada, sino únicamente la contraseña (normalmente más fácil de recordar).

Los parámetros de una función de derivación de claves *PBKDF* 2 son:

- Función pseudoaleatoria: la función *HMAC* a utilizar con su correspondiente función *hash*.
- Contraseña: contraseña memorizable de la que derivar una clave segura.
- Sal: secuencia de bits determinada.
- c: número de iteraciones.
- dkLen: longitud de la clave derivada deseada.

Para obtener una *seed* BIP-39, las entradas de la función *PBKDF* 2 son:

- Función pseudoaleatoria: *HMAC-SHA512*.
- Contraseña: la *seed phrase* como *string* de *bytes* codificados en *UTF-8*.
- Sal: esta sal se pasa al parámetro de mensaje en la primera llamada a la función *HMAC*, y es el *string* "mnemonic" con la misma *seed phrase* concatenada a continuación. Aunque es frecuente ver que se usa únicamente "mnemonic".
- c: 2048.
- dkLen: 512 bits.

En las sucesivas llamadas a *HMAC-SHA512*, se pasa la *seed phrase* al parámetro de clave. Al parámetro mensaje, a partir de la segunda llamada se pasa un determinado valor cambiante.

Se pueden utilizar los parámetros aconsejados en el BIP-39 para generar la *seed*, pero también podríamos optar por utilizar nuestros propios parámetros; así, solo nosotros sabríamos cómo obtener la *seed* a partir de la *seed phrase*.
