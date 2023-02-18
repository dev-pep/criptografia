# BIP-39

La *seed phrase* contiene, en sí, un mecanismo de *checksum*, con lo que no todas las combinaciones de palabras son válidas.

#### HMAC

Un algoritmo *HMAC* (*hash-based message authentication code*) genera un código de autenticación de un mensaje, el cual sirve para garantizar la autenticidad de un mensaje (integridad y remitente). En lugar de utilizar una firma digital con criptografía asimétrica, se utiliza una *pre-shared key* y una función *hash* específica (existen así variantes *HMAC-SHA1*, *HMAC-MD5*, etc.). Para poder comprobar la autenticidad del mensaje recibido es necesario poseer la clave compartida. Su ventaja es que no es necesario implementar un sistema de clave pública.

#### Derivación de claves y PBKDF2

La derivación de claves (*key derivation*) sirve para derivar (obtener) una o más claves secretas, a partir de un valor secreto (como una contraseña maestra).

En BIP-39 se utiliza un algoritmo de derivación de claves llamado *PBKDF* 2 (*password-based key derivation function 2*), el cual genera una clave aplicando de cierta manera (varias iteraciones, etc.) una función hash *HMAC* sobre una contraseña de entrada y una valor de sal. La clave obtenida (derivada) está lista para usarse para otros métodos criptográficos. Así, no es necesario recordar la clave derivada, sino únicamente la contraseña (normalmente más fácil de recordar).

> La sal es utilizada para aumentar la seguridad. Cuando los passwords se almacenan sin sal, puede haber coincidencias que den muchas pistas, cuando dos passwords coincidan. Además, evitan los ataques por fuerza bruta, y hacen inútiles las bases de datos de ejemplos de hashes.

Las entradas de la función *PBKDF* 2 son la *seed phrase* como *string* de *bytes* codificados en *UTF-8*. En este caso, se utiliza la función *hash HMAC-SHA512*, a la que se pasa en las sucesivas llamada, la *seed phrase* al parámetro de clave y un determinado valor cambiante de sal al parámetro de mensaje. El resultado final retornado por esta función será la clave derivada, la *seed* o semilla de 512 bits, que utilizaremos para la creación del monedero.

En el caso específico de BIP-39, la función *PBKDF2* se llamará con otros parámetros específicos:

- La sal de la primera llamada a la función *HMAC* es el *string* "mnemonic" con la misma *seed phrase* concatenada a continuación. Aunque es frecuente ver que se usa únicamente "mnemonic".
- El número de iteraciones se establece en 2048.

Se pueden utilizar los parámetros aconsejados en el BIP-39 para generar la *seed*, pero también podríamos optar por utilizar nuestros propios parámetros; así, solo nosotros sabríamos cómo obtener la *seed* a partir de la *seed phrase*.
