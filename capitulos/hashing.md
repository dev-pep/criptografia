# Hashing

Los algoritmos de *hashing* producen, a partir de unos datos de entrada, un *digest* o *hash*. Es una encriptación en un solo sentido, es decir, a partir del *digest* no es posible obtener la entrada original.

## Algoritmos SHA-2

Se implementan las versiones *SHA-224*, *SHA-256*, *SHA-384* y *SHA-512*. Cada uno de ellos tiene unos parámetros de funcionamiento distintos, pero en general realizan una serie de acciones parecidas sobre los datos de entrada. La entrada consiste en una serie arbitraria de *bytes*, y en general, las acciones son estas:

- Se aplica el *padding* oportuno al mensaje.
- Se divide el mensaje en bloques (de 512 o 1024 bits, según la versión).
- Se inicializa un vector H (de 8 elementos) y un vector K (de 64 o 80 elementos).
- Para cada bloque del mensaje:
    - El bloque se divide en 16 partes (de 32 o 64 bits). Estas partes sirven únicamente para inicializar el vector W, que tiene 64 o 80 elementos.
    - Se inicializan las variables a..h con los valores del vector H tal cual esté.
    - Se aplica la función de compresión, consistente en 64 o 80 iteraciones:
        - Las variables a..h sufren una serie de operaciones y cambios, con operaciones bit a bit específicas de cada algoritmo.
    - Al vector H se le suma el valor de las variables a..h (módulo 32 o 64).
- Al final, el resultado es la concatenación del vector H, desde su primer elemento hasta el último, penúltimo o antepenúltimo.

Para más detalles, en la implementación en *Python*, la función correspondiente al algoritmo *SHA-256* está profusamente comentada. El resto de funciones documenta las diferencias con la anterior.
