# Hashing

Los algoritmos de *hashing* producen, a partir de unos datos de entrada, un *digest* o *hash*. Es una encriptación en un solo sentido, es decir, a partir del *digest* no es posible obtener la entrada original.

## Algoritmos SHA-2

Se implementan las versiones *SHA-224*, *SHA-256*, *SHA-384* y *SHA-512*. Cada uno de ellos tiene unos parámetros de funcionamiento distintos, pero en general realizan una serie de acciones parecidas sobre los datos de entrada. La entrada consiste en una serie arbitraria de *bytes*, y en general, las acciones son estas:

- Se aplica el *padding* oportuno al mensaje (un bit 1 obligatorio, seguido de los 0's necesarios y el entero con la longitud inicial).
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

## Algoritmos RIPEMD

Se implementa la versión *RIPEMD-160*.

### RIPEMD-160

En este algoritmo es importante tener en cuenta la *endianness*: el mensaje está dividido en bloques de 512 bits (64 bytes). Estos bloques está a su vez divididos en enteros (palabras) de 32 bits (4 bytes). Estas palabras están codificadas como *Little Endian*, con lo que el orden de los 4 bytes que la componen va de menos significativo a más significativo. Sin embargo, la ordenación interna de cada byte (orden de los bits) es *big endian*.

A tener en cuenta, el *padding* inicial del mensaje lleva al final un entero de 64 bits (8 bytes): este entero también es little endian, con lo que debe invertirse la secuencia de 8 bytes al añadirse.

Esta *endianness* debe tenerse en cuenta al convertir enteros en *bytes* o viceversa. Fuera de las conversiones, no afecta en absoluto.

El resultado del *digest* es de 160 bits.
