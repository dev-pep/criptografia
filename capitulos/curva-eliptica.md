# Criptografía de Curva Elíptica

Para esta técnica criptográfica, se toma como base la ecuación:

$y^2 = x^3 + ax + b$

Para ello, se toma como base el campo $\mathbb{F}_p$, en este caso, $(\mathbb{Z}_p, +, \cdot)$. Sobre este se define la curva elíptica $E$.:

El **grupo** $(E(\mathbb{F}_p), +)$ tiene estas características:

- Los elementos del grupo, $E(\mathbb{F}_p)$ son todos los puntos $(x, y)$ que pertenecen a la curva.
- La operación del grupo es la suma ($+$).

La suma se define así: dados dos puntos $P$ y $Q$ pertenecientes a la curva elíptica, la suma $R=P+Q$ es un punto $R$ que se halla, gráficamente, de la siguiente forma:

- Se traza una recta que pasa por $P$ y por $Q$ (**intersecta** la curva en ambos puntos).
- Esa recta intersecta también la curva en un tercer punto, llamado $-R$. Reflejando este punto en referencia al eje $x$, obtendremos el punto $R$.

El elemento identidad (o elemento neutro) del grupo es el elemento $0$, y por definición **toda recta vertical intersecta la curva en ese punto**, en el infinito (positivo) de la componente $y$.

También es posible sumar un elemento consigo mismo. En ese caso, $P=Q$, con lo que la suma se puede reescribir $P+Q=P+P=2P$. En este caso, la recta es **tangente** a la curva en el punto $P$. Esta recta cortará la curva en $-R$, procediendo desde aquí de la forma explicada. Al punto obtenido se le puede seguir sumando $P$, con lo que podemos obtener $P, 2P, 3P,...$

En criptografía se suele trabajar sobre un campo finito $\mathbb{F}_p$, donde $p$ es un número primo impar (no 2) o una potencia de dos ($2^m$).

## Definición de la CE

Sea $p$ un número primo impar. Una curva elíptica $E$ sobre el campo $\mathbb{F}_p$ se define por la ecuación $y^2 = x^3 + ax + b$, donde $a,b \in \mathbb{F}_p$, y se cumple que:

$4a^3+27b^2 \not\equiv 0 \pmod p$

El conjunto $E(\mathbb{F}_p)$ pues, está formado por todos los puntos $(x, y)$ tales que $x \in \mathbb{F}_p$, $y \in \mathbb{F}_p$ y $y^2=x^3+ax+b$, junto con un punto especial $0$ en $y=+\infty$.

## Cardinalidad del grupo (ejemplo)

Es importante saber el orden o cardinalidad del grupo, es decir, saber cuántos puntos existen en nuestra curva.

Veamos, por ejemplo, $\mathbb{F}_7$ (en este caso, $p=7$) con $a=3$ y $b=5$.

Comprobaremos primero que se cumpla $4a^3+27b^2 \not\equiv 0 \pmod p$:

$4 \cdot 3^3 + 27 \cdot 5^2 = 108 + 675 = 783 \not\equiv 0 \pmod 7$

Entonces los valores $a$ y $b$ son válidos. La ecuación queda, pues:

$y^2 = x^3 + 3x + 5$

Dado que $x \in \mathbb{Z}_7$, probaremos para $x \in \{0,1,2,3,4,5,6\}$. Empecemos por $x=0$:

$y^2 = 5$

Recordemos que no estamos en el grupo de los números reales, sino en $\mathbb{Z}_7$, con lo que $\pm\sqrt{5}$ no son soluciones válidas; la ecuación debe reescribirse:

$y^2 \equiv 5 \pmod 7$

Es decir, ¿qué número $y \in \mathbb{Z}_7$ al cuadrado es congruente con 5 módulo 7? La solución no es trivial, y no tiene nada que ver con raíces cuadradas. Un modo sería probando con cada uno de los valores (fuerza bruta). En este caso, vemos que ningún número satisface la congruencia. Probemos pues con $x=1$:

$y^2 = 1 + 3 + 5$, lo que pasado a nuestro grupo:

$y^2 \equiv 2 \pmod 7$

Fijémonos que la parte derecha de la congruencia no es $9$ sino $2 \pmod 7$, ya que $1 + 3 + 5 \equiv 2 \pmod 7$.

Provando valores uno a uno, esto nos da dos soluciones: $y=3$ e $y=4$.

> Si nos fijamos en estas soluciones, $3^2=9$, y por otro lado $(-3)^2=9$. Esto concuerda con el hecho de que $4 \equiv -3 \pmod 7$. Las soluciones de $y^2=9$ en el conjunto $\mathbb{R}$ son, de hecho, $3$ y $-3$.

Por lo tanto, ya tenemos dos elementos del conjunto $E(\mathbb{F}_7)$, que son $(1, 3)$ y $(1, 4)$. Y así, deberíamos seguir, probando con los demás valores de $x$.

Como podemos comprobar, el proceso no es trivial, con lo que el método de contar la cardinalidad del grupo valor por valor es altamente ineficiente.

Por suerte, existen métodos mucho más eficientes de calcular la cardinalidad de la curva elíptica $E(\mathbb{F}_p)$.

## Operaciones del grupo

Sea $(E(\mathbb{F}_p),+)$ el grupo cuyo conjunto de elementos está definido por la curva elíptica $E$, entonces, si $P,Q,R \in E(\mathbb{F}_p)$ y $0 \in E(\mathbb{F}_p)$ es el elemento neutro del grupo, entonces dicho grupo dispone de las siguientes operaciones:

- $P+0=0+P=P$
- Si $P=(x,y)$, entonces $-P=(x,-y)$, y $P+(-P)=0$.
- Si $P=(x_1,y_1)$, $Q=(x_2,y_2)$, y $P\neq \pm Q$, entonces $R=P+Q=(x_3,y_3)$ y:
    - $\displaystyle x_3 = \left( \frac{y_2-y_1}{x_2-x_1} \right)^2 - x_1 - x_2$
    - $\displaystyle y_3 = \left( \frac{y_2-y_1}{x_2-x_1} \right) (x_1-x_3) - y_1$
- Si $P=(x_1,y_1)$, y $P\neq-P$, entonces $R=2P=(x_3,y_3)$ y:
    - $\displaystyle x_3 = \left( \frac{3x^2_1+a}{2y_1} \right)^2 - 2x_1$
    - $\displaystyle y_3 = \left( \frac{3x^2_1+a}{2y_1} \right) (x_1-x_3) - y_1$

## Resumen del proceso

En resumen, los pasos para crear una curva elíptica $E$ sobre un campo $\mathbb{F}_p$ son:

- Elegir un número $p$ como módulo base de $\mathbb{F}_p$. Suele ser un número primo muy grande.
- Elegir los parámetros $a$ y $b$, teniendo en cuenta las restricciones indicadas anteriormente.
- Obtener la cardinalidad de nuestra curva $E(\mathbb{F}_p)$.
- Elegir un punto $P$ de la curva que actuará como generador del grupo.

Es decir, los elementos de nuestro grupo serán $P, 2P, 3P,...$ Si nuestro grupo es cíclico y $P$ es un generador del grupo, nuestro grupo será $(E(\mathbb{F}_p),+)$. En caso contrario, los elementos de nuestro grupo serán un subgrupo de $E(\mathbb{F}_p)$.

## Parámetros estandarizados

Existen una serie de juegos o conjuntos de parámetros estandarizados para crear curvas elípticas. Uno de estos juegos de parámetros es el *SECP256K1*, que es el seguido para generar claves públicas en la *blockchain* de ***Bitcoin***, y muchas otras tras esta (como ***Ethereum***). Estos parámetros son:

- Curva $E(\mathbb{F}_p)$, con $p=2^{256} - 2^{32} - 2^9 - 2^8 - 2^7 - 2^6 - 2^4 - 1$ (es un número primo). En haxadecimal es:
    - fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
- $a=0$
- $b=7$
- Número $G$ generador. No genera todos los elementos del grupo original, pero se acerca. En todo caso, el grupo tendrá orden (cardinalidad) $n$, que es el orden del punto $G$. Las coordenadas del punto $G$ son (en hexadecimal):
    - x: 79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    - y: 483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
- Orden del grupo ($n$):
    - fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
- Cofactor $h=1$.

## El cofactor h

De forma similar a lo que se puede hacer en grupos del tipo $(\mathbb{Z}_n, +)$, por ejemplo, podríamos aplicar un cofactor $h$ al punto $G$ generador de nuestro grupo ($hG$). En este caso habría que multiplicar dicho cofactor por el punto generador de nuestro grupo, y generar el grupo a partir de ese resultado. La multiplicación sería, como de costumbre, aplicar la suma de $G$ $h$ veces.

Sin embargo, *SECP256K1* no define cofactor, es decir, $h=1$, con lo que usaremos todos los puntos generados por $G$, siendo el orden del grupo el mismo que el orden de $G$.
