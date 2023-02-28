# Álgebra para criptografía

Se exponen aquí las bases teóricas que sustentan gran parte de los temas criptográficos.

## Grupos

Un **grupo** $G$ es un conjunto de elementos, junto con una operación binaria ($\star$) cerrada, es decir, dados dos elementos cualquiera $a$ y $b$ pertenecientes a $G$, entonces $a \star b$ da un resultado que pertenece también a $G$. Además, la operación debe cumplir tres requisitos:

- Asociatividad: $a \star (b \star c) = (a \star b) \star c, \forall a,b,c \in G$.
- Existencia de un elemento identidad (o neutro) $i$ tal que $a \star i = i \star a = a, \forall a \in G$.
- Inverso: Para todo elemento existe un inverso: $\forall a \in G \exists b$ tal que $ab = i$.

Ejemplos de grupos: $(\mathbb{Z}, +)$, $(\mathbb{Q}, \cdot)$.

No es un grupo ($\mathbb{Z}^\ast, \cdot$) ya que exceptuando el 1, los elementos no tienen inverso.

En criptografía, los grupos suelen ser finitos, por lo tanto el conjunto de elementos suele ser del tipo $\mathbb{Z}_n=\lbrace 0,1,2,3,...,n-1 \rbrace$. Por ejemplo, $\mathbb{Z}_4=\lbrace 0,1,2,3 \rbrace$. También se suele utilizar la notación $\mathbb{Z}/n\mathbb{Z}$. En el caso del ejemplo, sería el conjunto $\mathbb{Z}/4\mathbb{Z}$.

En este caso, los enteros están acotados, con lo que más allá de cierto valor "dan la vuelta" (*wrap up*). Las operaciones de estos grupos entran dentro de la **aritmética modular**, que es el mecanismo que permite a los enteros dar esa vuelta. En el caso de $\mathbb{Z}_4$, las operaciones serán **módulo 4**.

En la aritmética modular, las expresiones de identidad no utilizan la igualdad sino la llamada **relación de congruencia**. Siguiendo con el ejemplo de $\mathbb{Z}_4$, no podemos afirmar que $3 \cdot 3 = 4 + 1$, pero sí podemos afirmar que $3 \cdot 3 \equiv 4 + 1\pmod 4$. Es decir, 9 es congruente con 5, módulo 4, o 9 y 5 son congruentes módulo 4.

> Véase el apartado sobre aritmética modular más abajo.

Siguiendo con nuestro ejemplo, podemos comprobar que $(\mathbb{Z}, +)$ es un grupo:

- La asociatividad nos la dan las propiedades de la artimética modular.
- El elemento neutro es el $0$.
- Todos los elementos tienen inverso:
    - $0 + 0 \equiv 0 \pmod 4$
    - $1 + 3 \equiv 0 \pmod 4$
    - $2 + 2 \equiv 0 \pmod 4$
    - $3 + 1 \equiv 0 \pmod 4$

Como ejemplo, $(\mathbb{Z}^\ast_4, \cdot)$ no es un grupo ($\mathbb{Z}^\ast_4=\lbrace 1,2,3 \rbrace$), porque no todos los elementos tienen inverso. Sin embargo, $(\mathbb{Z}^\ast_5, \cdot)$ sí lo es.

En general, $(\mathbb{Z}^\ast_p, \cdot)$ **es un grupo si y solo si p es un número primo**. Esto puede verse del siguiente modo: si $n$ es un número compuesto, es porque tiene, como mínimo dos factores. En ese caso, $n=p \cdot q$. Tanto $p$ como $q$ son elementos del conjunto, y la operación $p \cdot q \equiv n \pmod n$, es decir, $p \cdot q \equiv 0 \pmod n$, el resultado es $0$, un elemento que no pertenece al conjunto.

Por otro lado, y como se verá más adelante, en $(\mathbb{Z}^\ast_n, \cdot)$, un elemento $a$ perteneciente al conjunto, tendrá inverso $a^{-1}$ si y solo si $a$ y $n$ son coprimos, con lo que si $n$ no es primo, habrá elementos sin inverso multiplicativo.

## Números coprimos y totiente de Euler

> Dos enteros $a$ y $b$ con **coprimos** si su máximo común divisor es $1$, es decir, si no tienen factores comunes.

> El **totiente de Euler** de un entero $n$ (expresado $\varphi(n)$ ) indica la cantidad de enteros positivos menores a $n$ que son coprimos con $n$.

Si $p$ es un número primo, lógicamente todo número a $0 < a < p$ es coprimo con $p$. Por lo tanto, ya tenemos una primera propiedad de la función totiente de Euler:

- Si $p$ es un número primo, entonces $\varphi(p)=p-1$.

Otras propiedades de la función:

- Función multiplicativa: si $m$ y $n$ son dos números coprimos entre sí, entonces $\varphi(nm) = \varphi(n)\varphi(m)$.
- Totiente de una potencia prima: si $p$ es un número primo y $k$ es un entero positivo, entonces $\varphi(p^k) = p^k - p^{k-1}$, o sea $\varphi(p^k) = p^k(1-\frac{1}{p})$, o también $\varphi(p^k) = p^{k-1}(p-1)$.

Por otro lado, cualquier número natural $n$ se descompone en factores primos, tal que $n=p^{k_1}_1 p^{k_2}_2 ... p^{k_r}_r$. De este modo, tenemos una primera fórmula para calcular totiente de Euler de $n$:

$\varphi(n) = \varphi(p^{k_1}_1) \varphi(p^{k_2}_2) ...  \varphi(p^{k_r}_r)$

Esto es así porque $p^{k_a}_a$ es siempre coprimo con $p^{k_b}_b$, ya que no tienen factores comunes. Por lo tanto:

$\varphi(n) = p^{k_1-1}_1(p_1-1) p^{k_2-1}_2(p_2-1) ... p^{k_r-1}_r(p_r-1)$

Existe otra formulación para la función:

$\displaystyle \varphi(n) = n \prod_{p \mid n} \left(1 - \frac{1}{p} \right)$

La relación $p \mid n$ significa " $p$ divide a $r$ ". En este caso, $p$ toma los valores de todos los números primos que dividen $n$ (sin repetirse, independientemente de su exponente).

Veamos un ejemplo para hallar el totiente de Euler de $144$. Sabemos que $144=3^2 \cdot 2^4$. Entonces, usando la primera fórmula:

$\varphi(144) = 3^{2-1} (3-1) 2^{4-1} (2-1) = 3 \cdot 2 \cdot 8 \cdot 1 = 48$

Usando la segunda fórmula:

$\displaystyle \varphi(144) = 144 \left(1 - \frac{1}{3} \right) \left(1 - \frac{1}{2} \right) = 144 \cdot \frac{2}{3} \cdot \frac{1}{2} = 48$

## Aritmética modular

En **aritmética modular**, la igualdad no se utiliza. En su lugar usaremos la relación de **congruencia**, que cumple (como la igualdad) todas las condiciones de una relación de equivalencia.

Sea $n$ un entero mayor que $1$, dos números enteros $a$ y $b$ son **congruentes módulo n** si $n$ es divisor de su diferencia, es decir, si existe un entero $k$ tal que $a-b=kn$, y se denota:

$a \equiv b \pmod n$

El módulo entre paréntesis indica que la operación módulo se aplica a ambos lados de la equivalencia, no solo a la parte derecha. En este caso, tanto $a$ como $b$ tienen el mismo resto al ser divididos por $n$. Así, podemos decir cosas como:

$26 \equiv 14 \pmod 6$

$35 \equiv -7 \pmod 6$ (también se aplica a números negativos)

Como cualquier relación de equivalencia, la congruencia tiene las siguientes propiedades:

- Reflexiva: $a \equiv a \pmod n$.
- Simétrica: $a \equiv b \pmod n$ si $b \equiv a \pmod n$.
- Transitiva: si $a \equiv b \pmod n$ y $b \equiv c \pmod n$, entonces $a \equiv c \pmod n$.

Si $a \equiv b \pmod n$, $a_1 \equiv b_1 \pmod n$ y $a_2 \equiv b_2 \pmod n$:

- Compatible con la traslación: $a+k \equiv b+k \pmod n$, para $k$ un entero cualquiera.
- Compatible con el escalado: $ka \equiv kb \pmod n$, para $k$ un entero cualquiera.
- $ka \equiv kb \pmod {kn}$, para $k$ un entero cualquiera.
- Compatible con la suma: $a_1 + a_2 \equiv b_1 + b_2 \pmod n$.
- Compatible con la resta: $a_1 - a_2 \equiv b_1 - b_2 \pmod n$.
- Compatible con la multiplicación: $a_1 a_2 \equiv b_1 b_2 \pmod n$.
- Compatible con la exponenciación: $a^k \equiv b^k \pmod n$, para $k$ un entero no negativo.
- Compatible con la evaluación polinomial: $p(a) \equiv p(b) \pmod n$, para $p(x)$ cualquier polinomio con coeficientes enteros.
- Generalmente, es falso que, para cualquier entero $k$ se cumpla $k^a \equiv k^b \pmod n$. Pero sí se cumple:
- $k^c \equiv k^d \pmod n$ si se cumplen estas dos condiciones:
    - $c \equiv d \pmod {\varphi(n)}$, siendo $\varphi(n)$ la función **totiente de Euler** sobre $n$.
    - $k$ y $n$ son **coprimos**.

Reglas para la cancelación de elementos comunes:

- Si $a + k \equiv b + k \pmod n$, donde $k$ es cualquier entero, entonces $a \equiv b \pmod n$. Resta.
- Si $ka \equiv kb \pmod n$, y $k$ es un entero coprimo con $n$, entonces $a \equiv b \pmod n$. División, se amplia más abajo.
- Si $ka \equiv kb \pmod {kn}$, y $k$ es un entero distinto de $0$, entonces $a \equiv b \pmod n$.

**Inverso multiplicativo modular** y división: para un entero $a$ existirá otro entero que llamaremos $a^{-1}$ tal que $a \cdot a^{-1} \equiv 1 \pmod n$ si y solo si $a$ y $n$ son coprimos. El entero $a^{-1}$ se denomina el inverso multiplicativo modular de $a$, módulo $n$.

> Estos conceptos (división e inverso multiplicativo) solo tienen sentido en grupos donde la operación es la multiplicación, o en anillos o campos (ya que estos incluyen la multiplicación, véase más adelante).

Siguiendo con las propiedades de la congruencia:

- Si $a$ tiene inverso multiplicativo módulo $n$ y $a \equiv b \pmod n$, entonces $a^{-1} \equiv b^{-1} \pmod n$ (compatibilidad con el inverso multiplicativo).
- División en aritmética modular: en general, si $a \equiv b \pmod n$, no se puede afirmar que $\displaystyle \frac{a}{k} \equiv \frac{b}{k} \pmod n$. Otra forma de expresarlo es: si $ak \equiv bk \pmod n$, no se puede afirmar que $a \equiv b \pmod n$. Pero sí se puede decir que $\displaystyle a \equiv b \pmod {\frac{n}{mcd(k,n)}}$, donde $mcd(k,n)$ es el **máximo común divisor** de $k$ y $n$.
- División en aritmética modular cuando $k$ es coprimo con $n$: en este caso, $mcd(k,n)=1$, con lo que podemos decir que si $a \cdot k \equiv b \cdot k \pmod n$, entonces $a \equiv b \pmod n$. Esto coincide con el hecho de que $k$ tenga inverso multiplicativo módulo $n$, así que si $a \cdot k \equiv b \cdot k \pmod n$, entonces $a \cdot k \cdot k^{-1} \equiv b \cdot k \cdot k^{-1} \pmod n$, con lo que $a \equiv b \pmod n$. Podemos comprobar, pues, que si $k$ y $n$ son coprimos, se puede dividir cualquier entero entre $k$ multiplicando ese entero por el inverso multiplicativo $k^{-1}$ y aplicando módulo $n$.

Normalmente no se utiliza la notación de la división $\displaystyle \frac{a}{b}$, a no ser que el grupo sea abeliano (multiplicación conmutativa), ya que la notación anterior es ambigua, por no especificar si se trata de $a^{-1} \cdot b$ o $b \cdot a^{-1}$.

Si $p$ es un número primo, a parte del número $0$ (que no tiene inverso multiplicativo nunca), cualquier entero desde $1$ hasta $p-1$ es coprimo con $p$, y por tanto tiene inverso multiplicativo módulo $p$.

> Para calcular el inverso multiplicativo de un entero, se puede utilizar el algoritmo de Euclides extendido.

Algunas propiedades más de la congruencia módulo $n$:

- Teorema de Euler: si $a$ y $n$ son coprimos, entonces $a^{\varphi(n)} \equiv 1 \pmod n$.
- De la anterior, tenemos que $a^{\varphi(n)} a^{-1} \equiv a^{-1} \pmod n$, y por tanto $a^{-1} \equiv a^{\varphi(n)-1} \pmod n$.

### Elementos generadores

Un elemento $g$ perteneciente a un grupo $G$ es un **generador** de dicho grupo si todos sus elementos se pueden obtener aplicando la operación del grupo repetidamente sobre $g$.

Si la operación es la multiplicación ($\cdot$), la aplicación repetida de esta sobre $g$ ($g \cdot g \cdot g ...$) se puede expresar como potencia ($g^k$). Si la operación es la suma ($+$), la aplicación repetida de esta sobre $g$ ($g + g + g ...$) se puede expresar como multiplicación ($k \cdot g$).

Por ejemplo, veamos por qué $2$ no es un generador de $(\mathbb{Z}^\ast_7, \cdot)$:

- $2^1 \equiv 2 \pmod 7$
- $2^2 \equiv 4 \pmod 7$
- $2^3 \equiv 1 \pmod 7$
- $2^4 \equiv 2 \pmod 7$ (se repite $2$ sin haber obtenido todos los elementos)

Así, $2$ solo genera 3 elementos ($2$, $4$ y $1$, que se irían repitiendo: $2$, $4$, $1$, $2$, $4$, $1$,...). Se dice pues que $2$ tiene orden 3 (genera 3 elementos).

En cambio, $3$ sí es generador de $(\mathbb{Z}^\ast_7, \cdot)$:

- $3^1 \equiv 3 \pmod 7$
- $3^2 \equiv 2 \pmod 7$
- $3^3 \equiv 6 \pmod 7$ ($3^2 \cdot 3 \equiv 2 \cdot 3 \pmod 7$)
- $3^4 \equiv 4 \pmod 7$ ($3^3 \cdot 3 \equiv 6 \cdot 3 \pmod 7$)
- $3^5 \equiv 5 \pmod 7$ ($3^4 \cdot 3 \equiv 4 \cdot 3 \pmod 7$)
- $3^6 \equiv 1 \pmod 7$ ($3^5 \cdot 3 \equiv 5 \cdot 3 \pmod 7$)

Así, $3$ genera todos los miembros del grupo (tiene orden 6).

## Teorema de Euler

Dice así: dados dos números naturales $a$ y $n$, coprimos entre sí, entonces:

$a^{\varphi(n)} \equiv 1 \pmod n$

En el caso específico que $n$ sea primo, entonces estamos ante el **pequeño teorema de Fermat**. Es decir, sea $p$ un número primo, entonces para cualquier entero $a$, $a^p-a$ es múltiplo de $p$. Es decir, $a^p-a \equiv 0 \pmod p$, y por lo tanto $a^p \equiv a \pmod p$, y $a^{p-1} \equiv 1 \pmod p$. Dado que $p$ es primo, $\varphi(p)=p-1$, con lo cual se llega al teorema de Euler.

Por poner un ejemplo, supongamos que $n$ es $31$ (número primo). Entonces podemos decir que para cualquier número entero $a$:

$a^{30} \equiv 1 \pmod {31}$

## Otras fórmulas

Si $a \mid b$ (si $a$ divide a $b$), entonces $\varphi(a) \mid \varphi(b)$.

En general, para cualquier par de números naturales $m$ y $n$:

$\displaystyle \varphi(mn) = \varphi(m) \varphi(n) \frac{d}{\varphi(d)}$, donde $d=mcd(m,n)$ (máximo común divisor).

## Isomorfismos

Un isomorfismo entre grupos es una función entre dos grupos que establece una relación exhaustiva uno a uno entre los elementos de ambos, de tal modo que se respetan las operaciones de ambos grupos. Dos grupos que tienen una relación así se denominan **isomorfos**. Dos grupos isomorfos **tienen las mismas propiedades**, con lo que de alguna forma **son el mismo grupo**.

Dados dos grupos $(G, \star)$ y $(H , \odot)$, un isomorfismo de $(G, \star)$ a $(H, \odot)$ es una función **biyectiva** $f:G \to H$ tal que para todo $u$ y $v$ en $G$, se cumple:

$f(u \star v) = f(u) \odot f(v)$

Los dos grupos $(G, \star)$ y $(H, \odot)$ son isomorfos si existe un isomorfismo del uno al otro (y por tanto, del otro al uno), y se indica $(G, \star) \cong (H, \odot)$. Dado que el grupo incluye ya la operación, se puede expresar $G \cong H$ (en algunas ocasiones, incluso $G=H$).

## Grupos abelianos

Un grupo $G$ es **abeliano** simplemente si además de las propiedades vistas hasta ahora, su operación ( $\star$ ) es conmutativa:

- $a \star b = b \star a, \forall a,b \in G$

## Subgrupos

Dado un grupo $G$, un subgrupo $H$ es un subconjunto de elementos de $G$ que forman a su vez un grupo con la misma operación de $G$.

Todo grupo tiene por lo menos dos subgrupos: el grupo trivial (que contiene únicamente el elemento identidad), y él mismo.

Dado un elemento $g$ de un grupo $G$ cualquiera, este elemento genera siempre un subgrupo de $G$ (aunque sea el grupo trivial o el mismo $G$).

Todos los grupos triviales son isomorfos entre sí, con lo cual se habla únicamente **del** grupo trivial (en singular).

## Grupos cíclicos

Un grupo $G$ es cíclico si existe por lo menos un elemento $g$ del mismo que genera todos los elementos del grupo.

Todo grupo cíclico de orden $n$ es isomorfo con el grupo $(\mathbb{Z}_n, +)$. Todo grupo cíclico infinito es isomorfo con $(\mathbb{Z}, +)$.

Otra propiedad de los grupos cíclicos es que **todo grupo cíclico es abeliano**.

Todo elemento de un grupo (ya sea cíclico o no) genera un subgrupo cíclico (lógicamente, porque todos sus elementos se generan con el elemento en cuestión).

Un grupo cíclico de orden $n$ cuyo elemento $g$ es un generador del grupo, tendrá los siguientes elementos (si la operación del grupo es multiplicativa):

$G=\lbrace i, g, g^2, g^3,..., g^{n-1} \rbrace$, donde $i$ es el elemento identidad ($i=g^0$).

Los elementos generados se repiten cíclicamente, es decir, $g^a \equiv g^b \pmod n$ si $a \equiv b \pmod n$. En este caso, podemos ver que $g^n \equiv i \pmod n$, ya que $g^n \equiv g^0 \pmod n$ y $n \equiv 0 \pmod n$. Esto significa que al ir generando los elementos desde $k=0$, cuando obtengamos el valor identidad habremos terminado, ya que volverá a empezar la secuencia.

De forma análoga, si la operación es la suma:

$G=\lbrace i, g, 2g, 3g,..., (n-1)g \rbrace$, donde $i=0g$. En este caso es fácil ver que $i \equiv ng \pmod n$.

Otra característica es que un grupo cíclico **de orden primo** (con un número primo de elementos) no trivial solo puede descomponerse en dos subgrupos: el grupo trivial, y él mismo, lo cual significa que **todos los elementos** del grupo son generadores del mismo, a excepción del elemento identidad, que genera el grupo trivial. En cambio, si el orden del grupo es compuesto, habrá elementos que generarán subgrupos menores no triviales.

Por ejemplo, en el grupo $(\mathbb{Z}_n, +)$, un elemento $g$ distinto del elemento identidad genera exactamente un subgrupo de $\displaystyle \frac{n}{mcd(n,d)}$ elementos. Así, cualquier número del grupo, coprimo con $n$, es un generador del grupo. Esto es útil, por ejemplo, en criptografía de curva elíptica, para el llamado *cofactor h*.

## Anillos y campos

Un anillo (*ring*) R es un conjunto de elementos junto con dos operaciones $+$ (suma) y $\cdot$ (multiplicación) tal que:

- R es un grupo abeliano bajo $+$.
- $\cdot$ es asociativa: $a \cdot (b \cdot c) = (a \cdot b) \cdot c, \forall a,b,c \in R$
- $+$ y $\cdot$ tienen propiedades distributivas:
    - $a \cdot (b + c) = a \cdot b + a \cdot c$
    - $(a + b) \cdot c = a \cdot c + b \cdot c$

Nótese que no se requiere elemento inverso para $\cdot$ (para $+$ sí por ser grupo con esta).

Ejemplos de anillos: $(\mathbb{Z}_n, +, \cdot)$, $(\mathbb{Z}, +, \cdot)$.

Un tipo concreto de anillos son los **campos**. Un campo (*field*) F es un conjunto $\mathbb{F}$ junto a dos operaciones $+$ (suma) y $\cdot$ (multiplicación), tal que:

- $(\mathbb{F}, +)$ es un grupo abeliano.
- $(\mathbb{F}^\ast, \cdot)$ es un grupo abeliano.

El anillo $(\mathbb{Z}_p, +, \cdot)$ es un campo si $p$ es **primo**, y se denota $\mathbb{F}_p$.

También es un campo $(\mathbb{F}_q, +, \cdot)$ si $q$ es una **potencia prima**, es decir, un entero positivo $p^n$, donde $p$ es primo y $n$ es un entero mayor a $0$. Por ejemplo, $5^4$ o $2^{128}$ son potencias primas.

En criptografía es muy frecuente utilizar campos $\mathbb{F}_q$ en los que $q$ es una potencia (muy grande) de 2.

## Algoritmo de Euclides

Se trata de un algoritmo para calcular el **máximo común divisor** de dos enteros. Se basa en el hecho de que el máximo común divisor de dos números sigue siendo el mismo si se reemplaza el mayor de ellos por la diferencia entre ellos. Aplicando este principio repetidamente, al final ambos números son el mismo, concretamente el $mcd$ de los dos números iniciales.

Una versión más eficiente sustituye el más grande por el resto al ser dividido por el más pequeño. En esta versión, el algoritmo termina al llegar a un resto cero, en cuyo caso, el $mcd$ es el menor de los dos enteros que quedan. Si a y b son los enteros de los que deseamos obtener el $mcd$, la idea es que $mcd(a,b) = mcd(b, a \bmod b)$.

Veamos un ejemplo. Para hallar el $mcd$ de 201 y 335:

$mcd(335, 201) = mcd(201, 134) = mcd(134, 67) = mcd(67, 0) = 67$

El orden de los argumentos de entrada no es relevante. Si por ejemplo $b > a$, simplemente se realizará una iteración más:

$mcd(201, 335) = mcd(335, 201) = ...$

## Identidad de Bézout y algoritmo extendido de Euclides

La identidad de Bézout afirma que si $m$ es el $mcd$ de dos enteros $a$ y $b$, este puede expresarse como una suma lineal de dichos enteros. Es decir, es posible encontrar dos enteros $s$ y $t$ tal que $m = sa + tb$.

Estos dos enteros pueden encontrarse a través de los sucesivos valores hallados usando el **algoritmo extendido de Euclides**, que es similar al algoritmo de Euclides visto anteriormente, pero en este caso, a parte de proporcionar los sucesivos restos en las iteraciones, proporciona también los cocientes de la división, y sucesivos valores $s$ y $t$, los cuales son los coeficientes que al multiplicar a los valores $a$ y $b$ iniciales dan como resultado el resto de la iteración actual. Cuando la iteración coincide con que el resto es $mcd(a,b)$, entonces los valores $s$ y $t$ de esa iteración serán los valores buscados.

En la iteración en la que el resto sea $0$, al igual que en el algoritmo de Euclides, sabremos que el resto de la iteración anterior es el $mcd$, y por lo tanto, los valores $s$ y $t$ de esa penúltima iteración serán los valores buscados.

Para la ejecución del algoritmo, necesitamos cuatro series de valores: $q_i, r_i, s_i, t_i$, es decir, sucesivos cocientes, restos, valores $s$ y valores $t$. Si $a$ y $b$ son los enteros iniciales, inicializaremos las series así:

- Cocientes ($q_i$): {} (serie vacía).
- Restos ($r_i$): { $a$, $b$ }.
- Valores $s$ ($s_i$): { $0$, $1$ }.
- Valores $t$ ($t_i$): { $1$, $0$ }.

Si se desea que la serie de cocientes tenga el mismo número de elementos que las demás series, se puede inicializar con dos valores nulos (no se usan): {nulo, nulo}.

A cada iteración se añade un elemento a cada una de las cuatro series:

- $\displaystyle q_i = \frac{r_{i-2}}{r_{i-1}}$ (suma entera, descartando decimales)
- $r_i = r_{i-2} - q_i \cdot r_{i-1}$
- $s_i = s_{i-2} - q_i \cdot s_{i-1}$
- $t_i = t_{i-2} - q_i \cdot t_{i-1}$

En cada iteración, se cumple $r_i = s_i \cdot a + t_i \cdot b$. Cuando $r_k = 0$, entonces $mcd(a,b)=r_{k-1}$, y los valores buscados son $s=s_{k-1}$ y $t=t_{k-1}$.

Veamos uno ejemplo, paso a paso, con los números $928$ y $348$. Tras la inicialización, calculamos primero los valores con $i=2$:

El cociente $q_2 = \frac{928}{348} = 2$, con resto $r_2 = 232$. En esta iteración, $s_2 = 1$ y $t_2 = -2$. Esto nos indica que $r_2 = s_2 \cdot a + t_2 \cdot b$. Efectivamente, $232=1 \cdot 928 + (-2) \cdot 348$. Veamos los valores con $i=3$:

El cociente $q_3 = \frac{348}{232} = 1$, con resto $r_3 = 116$. En esta iteración, $s_3 = -1$ y $t_3 = 3$. Esto nos indica que $r_3 = s_3 \cdot a + t_3 \cdot b$. Efectivamente, $116=(-1) \cdot 928 + 3 \cdot 348$. Veamos los valores con $i=4$:

El cociente $q_4 = \frac{232}{116} = 2$, con resto $r_2 = 0$. Hemos terminado. Sabemos que $mcd(928,348)=116$ (es decir, $r_3$), y que $s=-1$ y $t=3$ (es decir, $s_3, t_3$).

| Índice (i) | Cocientes (q<sub>i</sub>) | Restos (r<sub>i</sub>) | s<sub>i</sub> | t<sub>i</sub> |
| :--------- | :------------------------ | :--------------------- | :------------ | :------------ |
| $0$        | -                         | $928$                  | $1$           | $0$           |
| $1$        | -                         | $348$                  | $0$           | $1$           |
| $2$        | $2$                       | $232$                  | $1$           | $-2$          |
| $3$        | $1$                       | $116$                  | $-1$          | $3$           |
| $4$        | $2$                       | $0$                    | $3$           | $-8$          |

Como en el caso del algoritmo de Euclides, el orden de presentación de los enteros de entrada es irrelevante.

## Cálculo del inverso multiplicativo

Como hemos visto, si $a$ y $n$ son dos enteros, entonces se pueden encontrar dos enteros $s$ y $t$ tales que $mcd(n,a)=sn + ta$. Si $a$ y $n$ son **coprimos**, entonces $sn + ta = 1$. Para ello, consideraremos que $n$ **es un número primo**.

Finalmente, en un anillo $(\mathbb{Z}_n, +, \cdot)$, pasaremos la identidad anterior a aritmética modular:

$ta \equiv 1 \pmod n$

Esto significa que en el mencionado anillo, $t$ es precisamente el inverso multiplicativo de $a$. Por lo tanto, el algoritmo extendido de Euclides nos servirá para hallar el inverso multiplicativo de un entero $a$ en $(\mathbb{Z}_n, +, \cdot)$ utilizando la identidad de Bézout $mcd(a,b) = sa + tb$ con el algoritmo extendido de Euclides.

En este caso, habrá que aplicar el módulo $n$ al valor de $t$ obtenido, ya que este podría ser negativo.

> En el algoritmo de cifrado *RSA*, $n$ no es primo, sino el producto de dos números primos. La clave de encriptación (pública) es el inverso multiplicativo de la clave de desencriptación (privada), con lo que a la hora de elegir la primera deberemos asegurarnos de que es un número coprimo con $n$. Una forma de hacerlo es eligiendo un número primo. De esta forma el inverso será también válido y coprimo con $n$.

## Apéndice: Resumen de tipos numéricos

- Enteros ($\mathbb{Z}$): negativos, positivos y 0. $\mathbb{Z}^\ast$ son los enteros exceptuando el cero.
- Naturales ($\mathbb{N}$): enteros no negativos. $\mathbb{N}^\ast$ son los enteros mayores a cero.
- Racionales ($\mathbb{Q}$): cocientes, fruto de la división de dos enteros cualquiera. $\frac{a}{b}$ es un número racional si $a \in \mathbb{Z}$ y $b \in \mathbb{Z}^\ast$.
- Reales ($\mathbb{R}$): los números que se pueden usar para medir una cantidad real unidimensional.
- Irracionales: todos los números reales no racionales.
- Imaginarios: números producto de un real y la unidad imaginaria ($i = \sqrt{-1}$).
- Complejos ($\mathbb{C}$): números con parte real e imaginaria ($a + bi$), para $a,b \in \mathbb{R}$. Los imaginarios son complejos con a=0.
