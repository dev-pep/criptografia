# Números primos

Un número primo es un entero que no se puede descomponer en factores. Solo es divisible por 1 y por sí mismo. Para comprobar si un número es primo o no, es impracticable verificar todas las posibilidades (algoritmo determinista) cuando el número es excesivamente grande (cientos de dígitos). Para ello se utilizan métodos probabilísticos, como el de *Miller-Rabin*.

## Test de Miller-Rabin

Se trata de un test para comprobar si un número es primo, muy útil para el cálculo de número primos grandes. No es determinista, pero puede llegar a aumentar drásticamente la probabilidad de que un número sea primo, añadiendo más iteraciones al proceso. La probabilidad de que un número **compuesto** (no primo) se identifique como primo es, **como mucho** (y suele ser muchísimo menor, sobre todo para números grandes) $\displaystyle \frac{1}{4^k}$, siendo $k$ el número de iteraciones.

### Fundamentos

Sea $n$ un entero impar (si es par ya seguro que no es primo). Entonces, $n-1$ será un número par, con lo que tendrá 2 como factor una o más veces. Sea $s$ el número de factores 2 que componen $n-1$. Entonces, podemos reescribir $n-1$ como $n-1=2^sd$. En este caso, $s$ es un entero positivo, y $d$ es un entero impar.

Consideremos ahora un entero $a$, que es **coprimo** con $n$ y menor que este. Llamaremos **base** a este entero $a$. Entonces se dice que $n$ es un primo probable fuerte para la base $a$ si se cumple una de estas dos condiciones:

- $a^d \equiv 1 \pmod n$.
- $a^{2^rd} \equiv -1 \pmod n$ para algún $0 \leq r < s$.

Si no se cumple ninguna, el número es compuesto.

Efectivamente, el **pequeño teorema de Fermat** dice que si $n$ es primo, para cualquier entero $a$:

$a^{n-1} \equiv 1 \pmod n$

Recordemos que $n-1=2^sd$, con lo que el teorema se reescribiría:

$a^{2^sd} \equiv 1 \pmod n$

Sin embargo, si bien que $n$ sea primo implica que $a^{n-1} \equiv 1 \pmod n$, lo inverso no tiene por qué ser cierto. Si lo fuera, solo habría que calcular $a^{n-1} \pmod n$ y sabríamos si $n$ es primo.

Es por ello que debemos ir calculando la serie de valores, empezando por $a^d$, y elevando al cuadrado cada vez, es decir, los valores $a^{2^rd}$, para $0 \leq r < s$:

$a^d, a^{2d}, a^{2^2d}, a^{2^3d}, ..., a^{2^{s-2}d}, a^{2^{s-1}d}$

Cada valor subsiguiente es el cuadrado del anterior. Por lo tanto cada valor anterior es la raíz cuadrada del siguiente. El algoritmo aprovecha el hecho de que:

- $a^{n-1} \equiv 1 \pmod n$ (pequeño teorema de Fermat).
- Las únicas soluciones válidas para la raíz cuadrada de 1 son 1 y -1.

Por lo tanto, se deberá cumplir que $a^{2^sd} \equiv 1 \pmod n$, y además, en la serie de valores obtenidos, cada valor igual a 1 tendrá a su izquierda un valor 1 o -1 (recordemos que $-1 \equiv n-1 \pmod n$). Si un valor 1 tiene a su izquierda otro valor distinto de 1 y -1, es que ha llegado al 1 de una forma no deseada, con lo que el número es compuesto. Por otro lado, si alguno de los valores es $-1 \pmod n$, no hay ningún requisito especial para su valor a la izquierda, pero el siguiente valor será, lógicamente, $1 \pmod n$, y también los sucesivos valores hasta el final, con lo que $n$ será un probable primo.

En resumen: o bien el primero de los valores $a^d$ es ya 1, o debemos toparnos con algún -1 antes de llegar a $a^{2^sd}$. Si nos topamos con un 1 antes de haber encontrado un -1, el número es compuesto.

En cuanto a la **elección de bases**, la base $a = 1$ no sirve para nada, ya que en ese caso es trivial que $a^d \equiv 1 \pmod n$; y la base $a = n-1$ tampoco sirve, ya que $n-1 \equiv -1 \pmod n$, con lo que $a^d \equiv -1 \pmod n$. Así, se elegirán bases al azar tales que $1 < a < n-1$ (si eligiéramos todas las bases, sería un algoritmo determinista ineficiente).

En cuanto al **número de iteraciones**, suponiendo que un número $n$ sea compuesto, la probabilidad que el algoritmo lo detecte como tal, es mayor al 75%; por otro lado,si el algoritmo clasifica un número como compuesto, es seguro que lo es. Así, la probabilidad de que un número compuesto sea identificado como primo tras $k$ iteraciones es inferior a $\displaystyle \frac{1}{4^k}$. En la práctica, la probabilidad de error es en realidad mucho menor que eso.

### Algoritmo

- Dado el número (entero e impar) a comprobar, $n$, lo escribiremos de esta forma: $n-1 = d \cdot 2^s$. Dado que $n-1$ es par, $s$ será como mínimo 1. El número $d$ es impar (se han factorizado todos los factores 2 fuera).
- Esto es una iteración, que se repetirá $k$ veces:
    - Elegimos al azar un número $a$ perteneciente al intervalo $[2, n-2]$.
    - Calculamos los sucesivos valores de $a^{{2^r}d} \bmod n$ (elevando al cuadrado a cada iteración), para $r$ tomando los valores $0 \leq r < s$:
        - Para $r=0$, si da 1 (módulo $n$) o n-1 (que es $-1 \pmod n$), indica que es un probable primo y pasamos a la siguiente iteración de $k$ (probaremos otra base).
        - Desde $r=1$ hasta $r < s$, si da 1, es un número compuesto seguro y terminamos aquí, retornando ***False***. Si da $n-1$ (o sea $-1 \pmod n$), es un probable primo para esta base, con lo que pasamos a la siguiente iteración de $k$ (probaremos con otra base).
    - Si agotamos todas las $r$ sin haber visto que era un probable primo, es un número compuesto y terminamos aquí, retornando ***False***.
- Si tras probar $k$ iteraciones con distintas bases ($a$) no hemos podido comprobar que es compuesto, es un probable primo, y retornamos ***True***.
