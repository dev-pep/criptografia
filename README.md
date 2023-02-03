# Criptografía

El repositorio ***criptografia*** contiene utilidades varias, programadas en *Python*, que pueden resultar útiles para aprender y comprender los distintos aspectos de la criptografía, especialmente la relacionada con los pares de claves RSA.

## Scripts

### utils.py

Funciones útiles para los demás *scripts*.

### primos.py

Utilidades relacionadas con el cálculo de números primos.

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

Utilidades para calcular *digests* (*hashes*) mediante los algoritmos de la familia *SHA-2* (*SHA-256*, *SHA-512*, etc.).

### rsa.py

Utilidades para calcular y trabajar con el algoritmo de encriptación asimétrica RSA.

### bip39.py

Explora el [Bitcoin Improvement Proposal 39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki), relativo a la *seed phrase*. Utiliza la *wordlist* oficial en inglés, almacenada en el archivo ***wordlist.json***.
