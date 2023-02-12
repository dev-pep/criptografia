# Criptografía

El repositorio ***criptografia*** contiene utilidades varias, programadas en *Python*, que pueden resultar útiles para aprender y comprender los distintos aspectos de la criptografía, especialmente la relacionada con los pares de claves RSA.

**IMPORTANTE: Estos scripts no deben usarse para proyectos reales que precisen criptografía. Para ello es recomendable utilizar bibliotecas contrastadas y auditadas por parte de la comunidad y/o espertos en criptografía.** Por otro lado, el uso de estos *scripts* no busca la eficiencia, sino ayudar a comprender el funcionamiento de distintos conceptos de la criptografía, con lo que su ejecución puede ser mucho más lenta que la de bibliotecas y utilidades realizadas con la eficiencia en mente, y programadas en lenguajes compilados, mucho más veloces.

## Scripts

### utils.py

Funciones útiles para los demás *scripts*.

### primos.py

Utilidades relacionadas con el cálculo de números primos grandes. Necesario para el cálculo de la clave pública del algoritmo *RSA*.

#### Test de Miller-Rabin

Se trata de un test para comprobar si un número es primo, muy útil para el cálculo de número primos grandes. No es determinista, pero puede llegar a aumentar drásticamente la probabilidad de que un número sea primo, añadiendo más iteraciones al proceso. La probabilidad de que un número compuesto (no primo) se identifique como primo es, **como mucho** (y suele ser muchísimo menor, sobre todo para números grandes) 1/(4^k), siendo ***k*** el número de iteraciones.

El algoritmo es:

- Dado el número (entero e impar) a comprobar, ***n***, lo escribiremos de esta forma: `n-1 = d 2^s`. Dado que ***n-1*** es par, ***s*** será como mínimo 1. El número ***d*** es impar (se han factorizado todos los 2's fuera).
- Esto es una iteración, que se repetirá ***k*** veces:
    - Elegimos al azar un número ***a*** perteneciente al intervalo [2, n-2].
    - Calculamos los sucesivos valores de `a^((2^r)d) % n`, para ***r*** tomando los valores 0 <= r < s. Los valores que debemos comparar son:
        - Para r=0, si da 1 (1 % n) o n-1 (-1 % n), indica que es un probable primo y pasamos a la siguiente iteración de ***k***.
        - Para r>0, si da 1 es un número compuesto seguro, con lo que terminamos las iteraciones de ***k*** y retornamos ***False***. Si da n-1, es un probable primo, con lo que pasamos a la siguiente iteración de ***k***.
        - Si agotamos todas las ***r*** sin haber encontrado 1 ni -1, es un compuesto. Terminamos iteraciones de ***k*** y retornamos ***False***.

### sha2_hashing.py

*Secure Hash Algorithm*. Utilidades para calcular *digests* (*hashes*) mediante los algoritmos de la familia *SHA-2*. Se implementan 4 de ellos:

- *SHA-224*
- *SHA-256*
- *SHA-384*
- *SHA-512*

El algoritmo genérico utilizado para todos ellos es, dado un mensaje formado por una cantidad arbitraria de *bytes*:

- Aplicar el *padding* necesario al mensaje.
- Dividir el mensaje (en bloques de 512 o 1024 bits).
- Inicializar el vector H (8 elementos) y K (64 o 80 elementos).
- Para cada bloque de mensaje:
    - El bloque se divide en 16 partes (de 32 o 64 bits). Estas partes sirven únicamente para inicializar el vector W, que tiene 64 o 80 elementos.
    - Se inicializan las variables a..h con los valores del vector H tal cual esté.
    - Se aplica la función de compresión, consistente en 64 o 80 iteraciones:
        - Las variables a..h sufren una serie de operaciones y cambios.
    - Al vector H se le suma el valor de las variables a..h (módulo 32 o 64).
- Al final, el resultado es la concatenación del vector H, desde su primer elemento hasta el último, penúltimo o antepenúltimo.

### rsa.py

Algoritmo de encriptación de **Rivest, Shamir y Adleman**. Utilidades para calcular y trabajar con el algoritmo de encriptación de clave pública *RSA*. Debido a la lentitud en encriptar (y desencriptar), su utilidad no es para mensajes excesivamente largos. En este caso, se puede utilizar para intercambiar previamente una clave y utilizar un algoritmo de clave simétrica (mucho más rápidos), como *AES* u otro.

#### Algoritmo

Dos números **enteros** son coprimos entre sí si su mcd (máximo común divisor) es 1, es decir, si no tienen ningún factor común.

Se define la función **totiente de Euler** φ(n) (phi de n) como la cantidad de enteros menores que n que son coprimos de n. Para un número primo n, φ(n)=n-1. Para un número n compuesto por la multiplicación de dos números primos p y q:

φ(n) = φ(p) φ(q) = (p-1) (q-1)

Actualmente dicha función se usa menos, en favor del llamado **totiente de Carmichael**.

#### Método actual

El método actual de obtener las claves se parece mucho al original, pero obtiene valores más eficientes.

Primero, se obtienen dos números primos **grandes**. Originalmente se recomendaba que estos fuesen algo distintos en tamaño. Actualmente es frecuente que ambos tengan el mismo número de bits. Ambos suelen tener sus dos bits más significativos en 1 para asegurar que el número de bits del producto (p*q) tiene tantos bits como la suma del número de bits de cada primo. El número n es el producto de estos dos primos (n=p*q), y será el módulo usado para los cálculos de encriptación y desencriptación; n se comparte como parte de la clave pública (nunca p ni q).

El siguiente paso es calcular el totiente de Carmichael para n: λ(n). Dado que n=p*q, dicho totiente tiene la propiedad λ(n)=mcm(λ(p),λ(q)), siendo mcm el mínimo común múltiplo. Dado que p y q son primos, λ(p)=φ(p)=p−1, y lo mismo con q. Así, λ(n)=mcm(p−1,q−1). Dado que mcm(a,b)=|ab|/mcd(a,b), el mcm se puede calcular usando el **algoritmo de Euclides** (usado para calcular el mcd).

Ahora se calcula el otro número que forma parte de la clave pública: e, tal que 2<e<λ(n). Por otro lado, e y λ(n) son coprimos, es decir, mcd(e,λ(n))=1. Dado que la encriptación utiliza exponenciación binaria, cuanto más corto sea este número y cuantos menos bits 1 contenga, más eficiente será dicha encriptación. Anteriormente se solía utilizar e=3, pero esto le confería menos seguridad al algoritmo. Un número frecuentemente utilizado es 2^16 + 1 (65537), que es un número primo (seguro pues que es coprimo con λ(n)) y con solo dos bits a 1.

Ahora que ya tenemos la clave pública (e y n), calcularemos la clave privada, a la que llamaremos d. Este número es el inverso módulo λ(n) de e. Es decir:

d * e ≡ 1 (mod λ(n))

Para su cálculo, se utiliza el llamado **algoritmo de Euclides extendido**.

Nunca se deben revelar p, q ni λ(n) (se pueden simplemente descartar tras los cálculos). Ni por supuesto d.

Si M es el mensaje en claro (pasado a bits, y representado como entero), **menor que n**, y C es el mensaje cifrado (lógicamente menor que n, ya que se calcula módulo n), para encriptar y desencriptar:

C ≡ M ** e (mod n)

M ≡ C ** d (mod n)

### bip39.py

Explora el [Bitcoin Improvement Proposal 39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki), relativo a la *seed phrase* y la semilla para la generación de monederos. Utiliza la *wordlist* oficial en inglés, almacenada en el archivo ***wordlist.json***.

La *seed phrase* contiene, en sí, un mecanismo de *checksum*, con lo que no todas las combinaciones de palabras son válidas.

#### HMAC

Un algoritmo *HMAC* (*hash-based message authentication code*) genera un código de autenticación de un mensaje, el cual sirve para garantizar la autenticidad de un mensaje (integridad y remitente). En lugar de utilizar una firma digital con criptografía asimétrica, se utiliza una *pre-shared key* y una función *hash* específica (existen así variantes *HMAC-SHA1*, *HMAC-MD5*, etc.). Para poder comprobar la autenticidad del mensaje recibido es necesario poseer la clave compartida. Su ventaja es que no es necesario implementar un sistema de clave pública. 

#### Derivación de claves y PBKDF2

La derivación de claves (*key derivation*) sirve para derivar (obtener) una o más claves secretas, a partir de un valor secreto (como una contraseña maestra).

En BEP-39 se utiliza un algoritmo de derivación de claves llamado *PBKDF* 2 (*password-based key derivation function 2*), el cual genera una clave aplicando de cierta manera (varias iteraciones, etc.) una función hash *HMAC* sobre una contraseña de entrada y una valor de sal. La clave obtenida (derivada) está lista para usarse para otros métodos criptográficos. Así, no es necesario recordar la clave derivada, sino únicamente la contraseña (normalmente más fácil de recordar).

> La sal es utilizada para aumentar la seguridad. Cuando los passwords se almacenan sin sal, puede haber coincidencias que den muchas pistas, cuando dos passwords coincidan. Además, evitan los ataques por fuerza bruta, y hacen inútiles las bases de datos de ejemplos de hashes.

Las entradas de la función *PBKDF* 2 son la *seed phrase* como *string* de *bytes* codificados en *UTF-8*. En este caso, se utiliza la función *hash HMAC-SHA512*, a la que se pasa en las sucesivas llamada, la *seed phrase* al parámetro de clave y un determinado valor cambiante de sal al parámetro de mensaje. El resultado final retornado por esta función será la clave derivada, la *seed* o semilla de 512 bits, que utilizaremos para la creación del monedero.

En el caso específico de BIP-39, la función *PBKDF2* se llamará con otros parámetros específicos:

- La sal de la primera llamada a la función *HMAC* es el *string* "mnemonic" con la misma *seed phrase* concatenada a continuación. Aunque es frecuente ver que se usa únicamente "mnemonic".
- El número de iteraciones se establece en 2048.

Se pueden utilizar los parámetros aconsejados en el BEP-39 para generar la *seed*, pero también podríamos optar por utilizar nuestros propios parámetros; así, solo nosotros sabríamos cómo obtener la *seed* a partir de la *seed phrase*.

## Aspectos matemáticos

### Congruencia módulo n

La congruencia módulo n se indica ***a ≡ b (mod n)***. Es una relación de equivalencia compatible con la suma, la resta, multiplicación y exponenciación de enteros positivos. 

Dos número enteros ***a***, ***b*** son congruentes módulo ***n*** si ***n*** es divisor de su diferencia:

a ≡ b (mod n) implica que (a-b) ≡ kn, para algún entero ***k***. Es lo mismo que decir:

a ≡ kn + b (mod n)

En todo caso:

a-b ≡ 0 (mod n), ya que si a mod n = b mod n, entonces (a-b) mod n es cero.

### Exponenciación módulo n

En ocasiones, como en la encriptación/desencriptación RSA, es necesario calcular potencias con enteros muy grandes en criptografía. Esta operación puede llevar mucho tiempo. Sin embargo, cuando al resultado se le aplica el módulo n, existen métodos muy rápidos para hacer el cálculo. De hecho la función `pow(b, e, n)` utiliza uno de esos métodos de **exponenciación binaria** (*exponentiation by repeated squaring*).
