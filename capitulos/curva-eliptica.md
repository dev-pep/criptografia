# Criptografía de Curva Elíptica

Se trata de una técnica criptográfica de clave pública, basada en una curva elíptica definida sobre un campo finito. Es mucho más eficiente que *RSA*, ya que la seguridad de una clave privada de 256 bits de *CE* equivale la de una de más de 3000 bits en *RSA*.

La base es que dado un punto base de la curva multiplicado por un entero grande, y dado también el punto base, no es factible encontrar el factor que lo multiplica. Es equivalente al problema del logaritmo discreto, pero con la división (no podemos dividir el punto multiplicado entre el punto original).

La base de esta técnica es la ecuación:

$y^2 = x^3 + ax + b$

Pero en lugar de definirla sobre un plano XY real, se define sobre un campo finito, junto con un punto en el infinito llamado punto $0$. Este conjunto, junto con una operación suma que definiremos más tarde, forma un **grupo abeliano** cuyo punto identidad es el punto en el infinito (punto $0$ ).

Para su uso, las partes deben estar de acuerdo en los parámetros del dominio que se utilizarán.

## Parámetros

Por un lado, está el tamaño u **orden del campo finito** sobre el que se construirá la curva. Este viene indicado como $p$, y suele ser un número grande primo, o una potencia grande de 2 ($2^m$), aunque en este último caso existe algún parámetro extra que no trataremos, por lo que nos centraremos en el primer caso (el más común, sobre todo en aplicaciones como *blockchains*).

Por otro lado, se definen las **constantes** $a$ y $b$ de la ecuación. Lo único que hay que tener en cuenta es que se debe cumplir $4a^3+27b^2 \neq 0$, de lo contrario, no todas las rectas que intersectan la recta en 2 puntos la intersectan también en un tercero.

También existe el **punto base** $G$, que es el elemento generador de todos los puntos del grupo con el que trabajaremos. El **orden de este punto** $G$ es otro de los parámetros, $n$. Como todos los puntos de la curva son generados por este elemento $G$, nuestro grupo es un grupo cíclico.

Basándonos en una de las definiciones de número generador de un grupo cíclico, el orden de $G$ es el menor número entero $n>0$ tal que al aplicar dicho generador $n$ veces obtenemos el elemento identidad. En nuestro caso, $nG = 0$.

Lo ideal es que $n$ sea primo, ya que la eficiencia esta técnica es la del mayor factor primo de $n$. Si $|E(\mathbb{F}_p)|$ es el orden de la curva entera, y $n$ es el orden del generador $G$, definiremos el **cofactor** $h$ como:

$\displaystyle h=\frac{|E(\mathbb{F}_p)|}{n}$

Nos interesaría que $h$ fuese lo menor posible, ya que así dispondríamos de más puntos de la curva. Sin embargo, dado que nos interesa un $n$ primo, si $h$ es pequeño (hasta $4$, incluso a veces se acepta $8$) y $n$ es primo, resulta aceptable. Aunque lo ideal es $h=1$, es decir, un $|E(\mathbb{F}_p)|$ primo.

Supongamos que $|E(\mathbb{F}_p)| = 4n$, con $n$ primo. Es decir, que el orden de la curva entera no es primo, sino un número primo multiplicado por $4$. Si utilizamos como generador un punto $Q$ que tiene orden $4n$, no obtenemos beneficio adicional en cuanto a seguridad respecto a si usamos un grupo generado por $G$, con orden $n$. Y sin embargo estaríamos utilizando 4 veces más de puntos inútilmente. Es preferible utilizar el mínimo imprescindible de puntos ($n$), y usar el punto $G$.

> Si deseamos utilizar encriptación para una aplicación práctica, no es aconsejable calcular nuestros propios parámetros de dominio, sino utilizar un juego de parámetros contrastado y diseñado por expertos.

El principal problema es el cálculo del orden de la curva y del punto generador, ya que es complejo de implementar, y consume grandes cantidades de tiempo. Por suerte, existen entidades de estandarización que han diseñado juegos de parámetros. El método utilizado podría ser algo así:

- Elección del orden $p$ del campo $\mathbb{F}_p$ sobre el que construir la curva $E(\mathbb{F}_p)$. En este caso, tendríamos el campo $(\mathbb{Z}_p, +, \cdot)$. A tener en cuenta, el orden del campo debería tener una longitud aproximada del doble de las claves a utilizar. Es decir, si deseamos una seguridad de 256 bits, $p$ debería tener unos 512 bits.
- Elección de los parámetros de la ecuación $a$ y $b$.
- Cálculo del orden de la curva. Este complejo cálculo se realiza mediante el algoritmo de Schoof, o similar. Los elementos del grupo, $E(\mathbb{F}_p)$ son todos los puntos $(x, y)$ que pertenecen a la curva.

En este punto, si el orden de la curva $|E(\mathbb{F}_p)|$ es primo, sabemos que cualquier punto (excepto el $0$) generará todos los puntos, y que $h=1$. Elegimos un puntos $G$ al azar, y ya hemos terminado.

En cambio, si $|E(\mathbb{F}_p)|$ no es primo, buscamos el factor primo más grande, teniendo en cuenta que $h \leq 4$. Si $h$ va a ser grande, volvemos a empezar (con otra curva).

Si lo que hallamos es un orden tal que $1 < h \leq 4$, entonces simplemente habrá que buscar un punto $G$ que genere un grupo de orden $\displaystyle \frac{|E(\mathbb{F}_p)|}{h}$. Para ello, elegiremos un punto cualquiera $P$ de la curva, y lo multiplicaremos por el cofactor; eso nos dará $G$, es decir $G=hP$. ¿Por qué? Lo entenderemos haciendo un símil con el grupo $(\mathbb{Z}_n, +)$, con $n$ primo o compuesto:

En dicho grupo, exceptuando la identidad (número $0$), cada elemento $a$ genera un subgrupo de orden $\displaystyle \frac{n}{mcd(n,a)}$. Si $a$ es coprimo con $n$, entonces $a$ generará el grupo entero. Pero supongamos que $p$ es un número primo y que $n=4p$. En este caso tendríamos un cofactor $h=4$. Si elegimos un elemento $a$ al azar para generar un subgrupo, y que $a$ es primo. Como $a$ y $n$ son coprimos ($mcd(n,a)=1$), $a$ generará todo el grupo. Pero si en lugar de $a$ elegimos $b=ha=4a$. Entonces, $mcd(n,b)=4$, con lo que $b$ generará un subgrupo de orden $p$, que es lo que buscábamos.

Pero, ¿y si el punto al azar $a$ ya cumple $mcd(n,a)=4$? No importa, si $b=4a$, igualmente se sigue cumpliendo que $mcd(n,b)=4$. Por lo tanto, la opción de elegir un número al azar y multiplicarlo por el cofactor nos dará un subgrupo de orden $p$.

Pero, ¿y si el punto al azar $a$ ya cumple $mcd(n,a)=p$? Pues ya sería mala suerte. Supongamos que, como hemos dicho, $n=4p$, y que $p$ es un número de 256 bits. Disponemos de $4p$ números para elegir al azar. Y de los $4p$ números disponibles, solo hay 4 divisibles por $p$, que son $p$, $2p$, $3p$ y $4p$. Es decir, cada $p$ números, 1 es divisible por $p$. Realmente es muchísimo más probable sentarse en un pajar y clavarse la aguja.

## Operación suma

La operación del grupo es la llamada suma ($+$), aunque no tiene mucho que ver con la suma aritmética.

La suma del grupo se define así: dados dos puntos $P$ y $Q$ pertenecientes a la curva elíptica, la suma $R=P+Q$ es un punto $R$ que se halla, gráficamente, de la siguiente forma:

- Se traza una recta que pasa por $P$ y por $Q$ (**intersecta** la curva en ambos puntos).
- Esa recta intersecta también la curva en un tercer punto, llamado $-R$. Reflejando este punto sobre el eje $X$, obtendremos el punto $R$.

También es posible sumar un elemento consigo mismo. En ese caso, $P=Q$, con lo que la suma se puede reescribir $P+Q=P+P=2P$. Aquí, la recta es **tangente** a la curva en el punto $P$. Esta recta cortará la curva en $-R$, procediendo desde aquí de la forma anterior. Al punto obtenido se le puede seguir sumando $P$, con lo que podemos obtener $P, 2P, 3P,...$ Es la forma de "multiplicar" un punto por un entero.

El elemento identidad (o elemento neutro) del grupo es el elemento $0$, llamado también punto en el infinito; por definición toda recta vertical intersecta la recta en ese punto en el infinito positivo de la componente $Y$.

### Operaciones derivadas de la suma

Si $P,Q,R \in E(\mathbb{F}_p)$ y $0 \in E(\mathbb{F}_p)$ es el elemento neutro del grupo (punto en el infinito), entonces dicho grupo dispone de las siguientes operaciones:

- $P+0=0+P=P$
- Si $P=(x,y)$, entonces $-P=(x,-y)$, y $P+(-P)=0$.
- Suma de puntos. Si $P=(x_1,y_1)$, $Q=(x_2,y_2)$, y $P\neq \pm Q$, entonces $R=P+Q=(x_3,y_3)$ y:
    - $\displaystyle x_3 = \left( \frac{y_2-y_1}{x_2-x_1} \right)^2 - x_1 - x_2$
    - $\displaystyle y_3 = \left( \frac{y_2-y_1}{x_2-x_1} \right) (x_1-x_3) - y_1$
- Duplicar punto (*point doubling*). Si $P=(x_1,y_1)$, y $P\neq-P$, entonces $R=2P=(x_3,y_3)$ y:
    - $\displaystyle x_3 = \left( \frac{3x^2_1+a}{2y_1} \right)^2 - 2x_1$
    - $\displaystyle y_3 = \left( \frac{3x^2_1+a}{2y_1} \right) (x_1-x_3) - y_1$

A la hora de hacer los cálculos, hay que tener en cuenta que cuando estamos en el dominio del campo $\mathbb{F}_p$ las operaciones son módulo $p$. Además, las divisiones son en aritmética modular, y se deber realizar multiplicando por el inverso. En cuanto a las raíces cuadradas, se usará también la raíz cuadrada modular.

Cuando multipliquemos enteros por un punto (el punto generador, normalmente), hay que tener en cuenta que la operación no se puede hacer sumando el punto $G$ una y otra vez, ya que el entero suele ser inmenso (cientos de bits), con lo que se con técnicas del tipo doblar y añadir.

## Parámetros estandarizados

Existen una serie de juegos o conjuntos de parámetros estandarizados para crear curvas elípticas. Uno de estos juegos de parámetros es el *SECP256K1*, que es el seguido para generar claves públicas en la *blockchain* de ***Bitcoin***, y muchas otras tras esta (como ***Ethereum***). Estos parámetros son:

- Curva $E(\mathbb{F}_p)$, con $p=2^{256} - 2^{32} - 2^9 - 2^8 - 2^7 - 2^6 - 2^4 - 1$ (es un número primo). Es el tamaño del campo finito, y por tanto el número que define el módulo a aplicar a la aritmética modular. En hexadecimal, el número es:
    - fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
- $a=0$.
- $b=7$.
- Punto $G$ generador. El grupo tendrá orden (cardinalidad) $n$, que es el orden del punto $G$. Las coordenadas del punto $G$ son (en hexadecimal):
    - x: 79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    - y: 483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
- Orden del grupo final ($n$, orden de $G$):
    - fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
- Cofactor $h=1$ (el orden de la curva completa es primo).
