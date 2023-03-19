# Direcciones

Las direcciones son los códigos alfanuméricos que se utilizan en las transacciones para indicar un destinatario de la misma. Es equivalente al número de cuenta bancaria en el mundo de las divisas *fiat*.

Una transacción está firmada con la clave privada del autor de la misma, y es necesario que incluya un dirección de destino.

Cada criptomoneda tiene su propia forma de generar la dirección de una cuenta, pero en todo caso, se suele calcular a partir de la clave pública asociada a la cuenta, y se realiza de tal forma que no sea factible deducir dicha clave pública a partir de la dirección.

## Bitcoin

Existen varias criptomonedas que comparten la forma de generar direcciones explicada aquí, simplemente cambiando el prefijo por el asociado a la moneda concreta.

Bitcoin define la siguiente forma de obtener una dirección:

- Formar la secuencia de *bytes*: $0x04 \parallel X \parallel Y$, siendo $(X,Y)$ las coordenadas del punto que define la clave pública. La secuendia tendrá una longitud de 65 *bytes*.
- A esta secuencia se le aplica el *hash SHA-256*, y al resultado obtenido se la aplica el *hash RIPEMD-160*.
- A este resultado de 20 *bytes* se le prefija el código correspondiente a *Bitcoin* en la red principal, que es el 0x00 (en la red de pruebas es 0x6f, *Litecoin* usa el 0x30, etc.).
- La secuencia obtenida se pasa por una codificación Base-58-Check, es decir con el doble *hash SHA-256* previo. El resultado es precisamente la dirección *Bitcoin*.

> Dado que hemos prefijado 0x00 en el caso de Bitcoin, la dirección empezará por el carácter "1".

A esta forma se le llama la dirección sin comprimir (*uncompressed address*), ya que utiliza las dos coordenadas de la clave pública. Sin embargo, actualmente se utiliza más la forma comprimida (*compressed address*), en la que se debe proceder igual que hemos visto pero el primer paso cambia:

- Formar la secuencia de *bytes*: $0x02 \parallel X$, o $0x03 \parallel X$, dependiendo de si la coordenada $Y$ es par (primer caso) o impar (segundo caso). En lugar de 65 *bytes*, esta forma tiene solo 33 *bytes*.

En cuanto a la **clave privada**, *Bitcoin* define una forma de codificarla (llamada *Wallet Input Format*, *WIF*):

- Añadir el prefijo de moneda: en el caso de *Bitcoin* es 0x80 (en la *testnet* sería 0xef, *Litecoin* es 0xb0, etc.). A continuación, los 32 *bytes* de la clave privada.
- Pasar esta secuencia por una codificación Base-58-Check.

Esta codificación es reversible (se puede obtener la clave privada a partir de este código), con lo que más que una dirección se trata de la clave privada en sí, con una codificación Base58 y un *checksum*, para evitar errores al copiar la clave.

Esta es la forma llamada *uncompressed*. Actualmente se utiliza la forma *compressed*, que consiste simplemente en añadir un sufijo 0x01 a la clave privada antes de pasarlo a la codificación Base58 (este *byte* se denomina la *compression flag*).

Una clave privada así codificada empezará por el carácter "L" o "K".

## Ethereum

Mientras que en *Bitcoin* la dirección resultante depende de la red (*mainnet* o *testnet*), debido a prefijos distintos. Sin embargo, una dirección *Ethereum* a partir de una clave pública será la misma en todas las redes.

La obtención de la dirección es muy simple:

- Se pasa la clave pública (concatenación de las coordenadas $X \parallel Y$) por un *hash Keccak-256*.
- Se usan los últimos 20 *bytes*, desechando el resto.
- Se prefija "0x".

### Checksum

Dado que la dirección no tiene ningún tipo de paridad, a posteriori se inventó un sistema para añadirle una forma *checksummed*, y evitar así errores. Tanto la versión *checksummed* como la original deben funcionar igual (solo cambia la configuración de mayúsculas/minúsculas). La versión con paridad se hace así:

- Los 20 *bytes* de la dirección original (sin el prefijo "0x") se pasan por un *hash Keccak-256*.
- Se utilizan los 160 bits más significativos del *digest*, en grupos de 4 bits: si el grupo empieza por el bit 1, es decir, si el grupo define un número mayor a 8, el carácter correspondiente de la dirección se pone en mayúsculas.
