# Álgebra para criptografía

Se exponen aquí las bases teóricas que sustentan gran parte de los temas criptográficos.

## Resumen de tipos numéricos

- Enteros ($\mathbb{Z}$): negativos, positivos y 0. $\mathbb{Z}^\ast$ son los enteros exceptuando el cero.
- Naturales ($\mathbb{N}$): enteros no negativos. $\mathbb{N}^\ast$ son los enteros mayores a cero.
- Racionales ($\mathbb{Q}$): cocientes, fruto de la división de dos enteros cualquiera. $\frac{a}{b}$ es un número racional si $a \in \mathbb{Z}$ y $b \in \mathbb{Z}^\ast$.
- Reales ($\mathbb{R}$): los números que se pueden usar para medir una cantidad real unidimensional.
- Irracionales: todos los números reales no racionales.
- Imaginarios: números producto de un real y la unidad imaginaria ($i = \sqrt{-1}$).
- Complejos ($\mathbb{C}$): números con parte real e imaginaria ($a + bi$), para $a,b \in \mathbb{R}$. Los imaginarios son complejos con a=0.

## Grupos

Un **grupo** G es un conjunto de elementos, junto con una operación binaria ($\star$) cerrada, es decir, dados dos elementos cualquiera a y b pertenecientes a G, entonces $a \star b$ da un resultado que pertenece también a G. Además, la operación debe cumplir tres requisitos:

- Asociatividad: $a \star (b \star c) = (a \star b) \star c, \forall a,b,c \in G$
- Existencia de un elemento identidad (o neutro) $i$ tal que $a \star i = i \star a = a, \forall a \in G$
- Inverso: Para todo elemento existe un inverso: $\forall a \in G \exists b$ tal que $ab = i$

Ejemplos de grupos: $(\mathbb{Z}, +)$, $(\mathbb{Q}, \cdot)$.

No es un grupo ($\mathbb{Z}^\ast, \cdot$) ya que exceptuando el 1, los elementos no tienen inverso.

En criptografía, los grupos suelen ser finitos, por lo tanto el conjunto de elementos suele ser del tipo $\mathbb{Z}_n=\{0,1,2,3,...,n-1\}$. Por ejemplo, $\mathbb{Z}_4=\{0,1,2,3\}$.

En este caso, los enteros están acotados, con lo que más allá de cierto valor "dan la vuelta" (*wrap up*). Se trata de la **aritmética modular**, que es el mecanismo que permite a los enteros dar esa vuelta. En el caso de $\mathbb{Z}_4$, las operaciones serán **módulo 4**.

En la aritmética modular, las expresiones de identidad no utilizan la igualdad sino la llamada **relación de congruencia**. Siguiendo con el ejemplo de $\mathbb{Z}_4$, no podemos afirmar que $3 \cdot 3 = 4 + 1$, pero sí podemos afirmar que $3 \cdot 3 \equiv 4 + 1\pmod 4$. Es decir, 9 es congruente con 5, módulo 4, o 9 y 5 son congruentes módulo 4.

> Véase el apartado sobre la relación de congruencia más abajo.

Siguiendo con nuestro ejemplo, podemos comprobar que $(\mathbb{Z}, +)$ es un grupo:

- La asociatividad nos la dan las propiedades de la artimética modular.
- El elemento neutro es el 0.
- Todos los elementos tienen inverso:
    - $0 + 0 \equiv 0 \pmod 4$
    - $1 + 3 \equiv 0 \pmod 4$
    - $2 + 2 \equiv 0 \pmod 4$
    - $3 + 1 \equiv 0 \pmod 4$

Como ejemplo, $$(\mathbb{Z}^\ast_4, \cdot)$$ no es un grupo ($$\mathbb{Z}^\ast_4=\{1,2,3\}$$), porque no todos los elementos tienen inverso. Sin embargo, $(\mathbb{Z}^\ast_5, \cdot)$ sí lo es.

En general, $(\mathbb{Z}^\ast_p, \cdot)$ **es un grupo si p es un número primo**.

### Elementos generadores

Un elemento g perteneciente a un grupo G es un **generador** de dicho grupo si todos sus elementos se pueden obtener aplicando la operación del grupo repetidamente sobre g.

Si la operación es la multiplicación ($\cdot$), la aplicación repetida de esta sobre g ($g \cdot g \cdot g ...$) se puede expresar como potencia ($g^k$). Si la operación es la suma ($+$), la aplicación repetida de esta sobre g ($g + g + g ...$) se puede expresar como multiplicación ($k \cdot g$).

Por ejemplo, veamos por qué 2 no es un generador de $(\mathbb{Z}^\ast_7, \cdot)$:

- $2^1 \equiv 2 \pmod 7$
- $2^2 \equiv 4 \pmod 7$
- $2^3 \equiv 1 \pmod 7$
- $2^4 \equiv 2 \pmod 7$ (se repite 2 sin haber obtenido todos los elementos)

Así, 2 solo genera 3 elementos (2, 4 y 1, que se irían repitiendo: 2, 4, 1, 2, 4, 1,...). Se dice pues que 2 tiene orden 3.

En cambio, 3 sí es generador de $(\mathbb{Z}^\ast_7, \cdot)$:

- $3^1 \equiv 3 \pmod 7$
- $3^2 \equiv 2 \pmod 7$
- $3^3 \equiv 6 \pmod 7$ ($3^2 \cdot 3 \equiv 2 \cdot 3 \pmod 7$)
- $3^4 \equiv 4 \pmod 7$ ($3^3 \cdot 3 \equiv 6 \cdot 3 \pmod 7$)
- $3^5 \equiv 5 \pmod 7$ ($3^4 \cdot 3 \equiv 4 \cdot 3 \pmod 7$)
- $3^6 \equiv 1 \pmod 7$ ($3^5 \cdot 3 \equiv 5 \cdot 3 \pmod 7$)

Así, 3 genera todos los miembros del grupo (tiene orden 6).

## Grupos abelianos

Un grupo es **abeliano** si además de las propiedades vistas hasta ahora, su operación es conmutativa:

- $a \star b = b \star a, \forall a,b \in G$

## Anillos

Un anillo (*ring*) R es un conjunto de elementos junto con dos operaciones $+$ (suma) y $\star$ (multiplicación) tal que:

- R es un grupo abeliano bajo $+$.
- $\star$ es asociativa: $a \star (b \star c) = (a \star b) \star c, \forall a,b,c \in R$
- $+$ y $\star$ tienen propiedades distributivas:
    - $a \star (b + c) = a \star b + a \star c$
    - $(a + b) \star c = a \star c + b \star c$

Nótese que no se requiere elemento inverso para $\star$ (para $+$ sí por ser grupo abeliano con esta).

Ejemplos de anillos: $(\mathbb{Z}_n, +, \cdot)$, $(\mathbb{Z}, +, \cdot)$.

## Campos

Existe varias formas de definir un campo. Un campo (field) F es un conjunto $\mathbb{F}$ junto a dos operaciones $+$ (suma) y $\star$ (multiplicación), tal que:

- $(\mathbb{F}, +)$ es un grupo abeliano.
- $(\mathbb{F}^\ast, \cdot)$ es un grupo abeliano.

$(\mathbb{Z}_p, +, \cdot)$ es un campo si p es **primo**, y se denota $(\mathbb{F}_p$.

También es un campo $(\mathbb{F}_q$ si q es una **potencia prima**, es decir, un entero positivo $p^n$, donde p es primo y n es un entero mayor a 0. Por ejemplo, $5^4$ o $2^{128}$ son potencias primas.

En criptografía es muy frecuente utilizar campos $(\mathbb{F}_q$ en los que q es una potencia (muy grande) de 2.

## Relación de congruencia
