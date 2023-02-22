# El problema del logaritmo discreto

El problema planteado dice así:

Si $G$ es un grupo bajo la multiplicación, y $g$ es un generador del mismo, entonces:

- Dado un número $a$, es posible hallar $b=g^a$.
- Dado dado un número $b=g^a$ no es posible hallar $a$.

Pongamos, por ejemplo, que el grupo es el habitual $(\mathbb{Z}^\ast_p, \cdot)$. Entonces:

- Dado $a$, podemos calcular $b \equiv g^a \pmod p$.
- Dado $b=g^a$, no es factible calcular $a \equiv \log_g b \pmod p$.

Se podría intentar por fuerza bruta, por ejemplo. En todo caso, para que realmente no sea facible hallar $a$, el grupo debe ser muy grande ($p$ debería tener cientos o incluso miles de bits).

> Para los siguientes ejemplos se utilizarán relaciones de identidad corrientes por simplicidad, pero se entiende que en la práctica se utiliza aritmética modular.

## Método Diffie-Hellman

Este método es un ejemplo de cómo intercambiar un par de claves sobre un medio no seguro utilizando el problema del logaritmo discreto. Sean A y B los dos extremos de la comunicación. El valor $g$ es público:

- A genera un número aleatorio $a$ y envía $g^a$ a B. Mantiene $a$ en secreto.
- B genera un número aleatorio $b$ y envía $g^b$ a A. Mantiene $b$ en secreto.
- A calcula el número $(g^b)^a = g^{ba}$.
- B calcula el número $(g^a)^b = g^{ab} = g^{ba}$.

Ahora ambos tienen ya la clave secreta ($g^{ab}$). Cualquiera que intercepte el mensaje no podrá obtener la clave si no dispone de $a$ o de $b$.

## Generación de un par de claves

Veamos otro ejemplo: una forma simple de generar una clave pública y su correspondiente clave privada. Como siempre, $g$ es público.

- Generamos un número aleatorio $x$ (clave privada).
- Calculamos $y=g^x$. La clave pública es el par $(g, y)$.
- Alguien utiliza nuestra clave pública para encriptar un mensaje. Elige un número al azar $r$, y nos envía:
    - $u = g^r$
    - $v = m \cdot y^r$ ($m$ es el mensaje)
- Como disponemos de la clave privada $x$, desencriptamos: $m=v \cdot u^{-x}$.

Veamos por qué:

$v \cdot u^{-x} = m \cdot y^r \cdot (g^r)^{-x} = m \cdot y^r \cdot g^{-xr}$

Dado que $y = g^x$, entonces esto es igual a:

$m \cdot g^{xr} \cdot g^{-xr} = m$

## Otros

Para encriptar utilizando el esquema simple del problema del logaritmo discreto, la clave privada deberá ser muy larga. En la actualidad, se estima que por encima de los 3000 bits. En otros algoritmos como el de Curva Elíptica es suficiente una clave privada de 256 bits.
