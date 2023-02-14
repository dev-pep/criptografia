# Álgebra para criptografía

Se exponen aquí las bases teóricas que sustentan gran parte de los temas criptográficos.

## Grupos

Un **grupo** G es un conjunto de elementos, junto con una operación binaria ($\star$) cerrada, es decir, dados dos elementos cualquiera a y b pertenecientes a G, entonces $a \star b$ da un resultado que pertenece también a G. Además, la operación debe cumplir tres requisitos:

- Asociatividad: $a \star (b \star c) = (a \star b) \star c, \forall a,b,c \in G$
- Existencia de un elemento identidad i tal que $a \star i = i \star a = a, \forall a \in G$
- Inverso: Para todo elemento existe un inverso: $\forall a \in G \exists b$ tal que $ab = i$






## Apéndice. Resumen de tipos numéricos

- Enteros ($\mathbb{Z}$): negativos, positivos y 0. $\mathbb{Z}^*$ son los enteros exceptuando el cero.
- Naturales ($\mathbb{N}$): enteros no negativos. $\mathbb{N}^*$ son los enteros mayores a cero.
- Racionales ($\mathbb{Q}$): cocientes, fruto de la división de dos enteros cualquiera. $frac{a}{b}$ es un número racional si $a \in \mathbb(Z)$ y $b \in \mathbb(Z)^*$.
- Reales ($\mathbb{R}$): los números que se pueden usar para medir una cantidad real unidimensional.
- Irracionales: todos los números reales no racionales.
- Imaginarios: números producto de un real y la unidad imaginaria ($i = \sqrt{-1}$).
- Complejos ($\mathbb{C}$): números con parte real e imaginaria ($a + bi$).
