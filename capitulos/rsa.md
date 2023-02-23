# RSA

Algoritmo de encriptación expuesto inicialmente por **Rivest, Shamir y Adleman**. Debido a la lentitud en encriptar (y desencriptar), los algoritmos de encriptación asimétrica no son útiles para mensajes excesivamente largos. En este caso, se puede utilizar para intercambiar previamente una clave y utilizar posteriormente un algoritmo de clave simétrica (mucho más rápidos), como puede ser *AES*, para enviar el mensaje largo.

## Algoritmo

El método actual de obtener las claves se parece mucho al original, pero obtiene valores más eficientes.

### n, p, q

Primero, se obtienen dos números primos **grandes** $p$ y $q$. Originalmente se recomendaba que estos fuesen algo distintos en tamaño. Actualmente es frecuente que ambos tengan el mismo número de bits. Ambos suelen tener sus dos bits más significativos puestos a 1 para asegurar que el número de bits del producto ($p \cdot q$) tiene tantos bits como la suma del número de bits de cada número primo. El número $n$ es el producto de estos dos primos ($n=p \cdot q$), y los cálculos de encriptación y desencriptación se harán en $\mathbb{Z}^\ast_n$. El número $n$ se comparte como parte de la clave pública (nunca $p$ ni $q$).

> La base de este algoritmo es que no es factible hallar los factores $p$ y $q$ a partir de $n$, debido a la magnitud de estos números.

### Totiente de Carmichael

En el algoritmo original, Rivest, Shamir y Adleman utilizaban el **totiente de Euler** de $n$ ( $\varphi(n)$ ) para seguir con los cálculos. Actualmente se utiliza el llamado **totiente de Carmichael** ( $\lambda(n)$ ), por producir valores más eficientes, y por tanto claves más pequeñas para el mismo nivel de seguridad que usando el totiente de Euler.

Dado que este totiente tiene la propiedad $\lambda(ab) = mcm(\lambda(a), \lambda(b))$ (siendo *mcm* el mínimo común múltiplo), entonces $\lambda(p) = \varphi(p) = p-1$ y $\lambda(q) = \varphi(q) = q-1$, ya que $p$ y $q$ son primos. Por lo tanto, tenemos que, dado que $n=p \cdot q$, entonces $\lambda(n)=mcm(\lambda(p), \lambda(q))=mcm(p-1,q-1)$.

Dado que $\displaystyle mcm(a,b) = \frac{|ab|}{mcd(a,b)}$ (*mcd* es el máximo común divisor), podemos utilizar el **algoritmo de Euclides** para hallar el máximo común divisor, y posteriormente el mínimo común múltiplo, para finalmente obtener el totiente de Carmichael:

$\displaystyle \lambda(n) = \frac{|(p-1)(q-1)|}{mcd(p-1,q-1)}$

### Clave pública

Luego se calcula el otro número que forma parte de la clave pública a parte de $n$: de trata de un número $e$, tal que $2 < e < \lambda(n)$ (si $e=1$, el mensaje encriptado será idéntico al mensaje sin encriptar). Por otro lado, $e$ y $\lambda(n)$ deben ser coprimos, es decir, $mcd(e,\lambda(n))=1$. Dado que la encriptación utiliza exponenciación binaria para el cálculo, cuanto más corto sea este número y cuantos menos bits 1 contenga, más eficiente será dicha encriptación. Anteriormente se solía utilizar siempre $e=3$ (no importa, es la clave pública), pero esto le confería menos seguridad al algoritmo. Un número frecuentemente utilizado es $2^{16} + 1$ (65537), que es un número primo (seguro pues que es coprimo con $\lambda(n)$ ) y con solo dos bits a 1 (el primero y el último).

### Clave privada

Ahora que ya tenemos la clave pública ($e, n$), calcularemos la clave privada, a la que llamaremos $d$. Este número es el inverso multiplicativo de $e$ módulo $\lambda(n)$. Es decir:

$d \cdot e \equiv 1 \pmod {\lambda(n)}$

Para su cálculo, utilizaremos el **algoritmo de Euclides extendido**.

## Conclusión

Nunca se deben revelar $p$, $q$ ni $\lambda(n)$ (se pueden simplemente descartar tras los cálculos). Ni por supuesto $d$.

Se puede demostrar que esto funciona aunque el mensaje $m$ no sea coprimo con $n$.

Si $M$ es el mensaje en claro (pasado a bits, y representado como entero), **siempre menor que n**, por pertenecer a $\mathbb{Z}^\ast_n$, y $C$ es el mensaje encriptado (lógicamente también menor que $n$), para encriptar y desencriptar:

- Encriptar: $C \equiv M ^ e \pmod n$
- Desencriptar: $M \equiv C ^ d \pmod n$
