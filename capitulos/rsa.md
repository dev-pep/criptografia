# RSA

Algoritmo de encriptación expuesto inicialmente por **Rivest, Shamir y Adleman**. Debido a la lentitud en encriptar (y desencriptar), su utilidad no es para mensajes excesivamente largos. En este caso, se puede utilizar para intercambiar previamente una clave y utilizar un algoritmo de clave simétrica (mucho más rápidos), como puede ser *AES*.

## Algoritmo

El método actual de obtener las claves se parece mucho al original, pero obtiene valores más eficientes. Por ejemplo, actualmente, en lugar de utilizarse el **totiente de Euler**, se utiliza el llamado **totiente de Carmichael**.

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

## Algoritmo de Euclides

## Algoritmo de Euclides extendido

## Totiente de Carmichael

## Exponenciación módulo n

En ocasiones, como en la encriptación/desencriptación RSA, es necesario calcular potencias con enteros muy grandes en criptografía. Esta operación puede llevar mucho tiempo. Sin embargo, cuando al resultado se le aplica el módulo n, existen métodos muy rápidos para hacer el cálculo. De hecho la función `pow(b, e, n)` utiliza uno de esos métodos de **exponenciación binaria** (*exponentiation by repeated squaring*).
