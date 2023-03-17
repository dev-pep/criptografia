# Firma digital

Una firma digital tiene dos utilidades: por un lado, garantizar la autenticidad (integridad) del mensaje, y por otro asegurar que el mensaje lo ha generado (lo ha firmado) un remitente determinado.

## Firma con clave privada

Es posible firmar mensajes mediante algoritmos de asimétricos como *RSA*. La idea es: Alice redacta un mensaje M. Luego genera un *digest hash* de dicho mensaje H(M), y encripta ese *hash* con su clave privada: E(H(M)), que es precisamente la firma digital (o firma electrónica). Luego envia el mensaje M (en claro) y también la firma generada. Bob recibe ambas cosas y desencripta la firma utilizando la clave pública de Alice, obteniendo el hash del mensaje H(M). Como también tiene el mensaje, lo pasa a su vez por la función *hash* y compara el *digest* recibido con el que ha calculado. Si coinciden, el mensaje es auténtico y proviene de Alice.

## DSA

El algoritmo *DSA* (*Digital Signature Algorithm*) utiliza el problema del logaritmo discreto para firmar un mensaje.

> *DSA* ha quedado ya obsoleto, y no se utiliza en la actualidad para firmar electrónicamente. Sin embargo, algoritmos basados en este, como el *ECDSA* sí se utilizan.

### Funcionamiento

#### Parámetros del sistema

Primero hay que elegir el algoritmo *hash* a utilizar, y encriptar el mensaje con él, generándose así $H(M)$.

A continuación hay que elegir dos longitudes de bits, $L$ y $N$.

Originalmente se restringía $L$ a ser múltiplo de 64, entre 512 y 1024. Con el tiempo se solían usar tamaños mayores.

En cuanto a $N$, tendremos que $N < L$, y además, $N \leq |H|$, donde $|H|$ es la longitud en bits de la salida de la función *hash*. Existen algunas parejas de valores $(L, N)$ recomendados: (1024, 160), (2048, 224), (2048, 256), o (3072, 256).

A continuación se elegirán dos números primos: $q$, de $N$ bits, y $p$, de $L$ bits. En este caso, se tiene que cumplir que $(p-1)$ sea múltiplo de $q$.

Finalmente se calculará el número $g$ generador, de orden $q$. Este se calcula así: $g = h^{(p-1)/q} \bmod p$, siendo $h$ un número aleatorio en el intervalo $[2,p-2]$. En el improbable caso de que $g=1$, probaremos con un $h$ distinto (típicamente, $h=2$).

Los parámetros del sistema, a compartir entre todos los participantes, son $(H,p,q,g)$.

#### Claves

Cada usuario tendrá una clave privada ($x$) y una pública ($y$):

- $x$ es un número aleatorio del intervalo $[1,q-1]$
- $y=g^x \bmod p$

#### Firma

El remitente envía al receptor o receptores el mensaje $M$, junto con la firma:

- Se elige un entero al azar de $[1,q-1]$. Cada vez que se firma, **se debe elegir un número distinto**.
- $r = (g^k \bmod p) \bmod q$. Si $r=0$, volvemos a empezar con otro $k$.
- $s = (k^{-1} (H(M) + xr)) \bmod q$. Si $s=0$, volvemos a empezar con otro $k$.

La firma es precisamente el par $(r,s)$.

#### Validación

El receptor recibe el mensaje $M$ y la firma $(r,s)$. Ahora debe calcular:

- Comprobar que $0 < r < q$ y $0 < s < q$.
- Calcular $w=s^{-1} \bmod q$.
- Calcular $u_1=H(M) \cdot w \bmod q$.
- Calcular $u_2=r \cdot w \bmod q$.
- Calcular $v=(g^{u_1} \cdot y^{u_2} \bmod p) \bmod q$.

Se puede comprobar matemáticamente que la firma es válida si y solo si $v=r$.

## ECDSA

El *Elliptic Curve Digital Signature Algorithm* está basado en *DSA*, pero usa curva elíptica en lugar del problema del logaritmo discreto.

### Parámetros del sistema

En este caso, los parámetros del sistema son los propios de la curva elegida (por ejemplo, la *SECP256K1*), como el campo elegido (de orden $p$), la ecuación correspondiente (como $y^2=x^3+ax+b$), los factores $a$ y $b$, el punto generador $G$ o el orden $n$ de la curva. También incluiremos la función *hash* $H$ a utilizar.

### Claves

El usuario firmante tendrá una clave privada $d$, dentro del intervalo $[1,n-1]$ y una pública ($Q=dG$):

### Firma

El remitente envía al receptor o receptores el mensaje $M$, junto con la firma:

Si el *digest hash* $H(M)$ es más largo (en bits) que el número de bits del orden de la curva $n$, se descartarán los bits sobrantes de dicho *digest* (por la derecha). El *digest* puede ser más **grande** (en magnitud) que $n$, pero no más **largo** (en bits). Llamaremos $z$ a ese *digest* modificado (o no modificado si no ha hecho falta).

- Se elige un entero $k$ al azar en el intervalo $[1,n-1]$. Cada vez que se firma, **se debe elegir un número distinto**.
- Se calcula el punto de la curva correspondiente: $(x_1, y_1) = kG$.
- $r = x_1 \bmod n$. Si $r=0$, volvemos a empezar con otro $k$.
- $s = (k^{-1} (z + dr)) \bmod n$. Si $s=0$, volvemos a empezar con otro $k$.

La firma es precisamente el par $(r,s)$.

### Validación

El receptor recibe el mensaje $M$ y la firma $(r,s)$. Ahora debe calcular:

- Comprobar que $0 < r < n$ y $0 < s < n$.
- Calcular $H(M)$, y aplicar, si es necesario el (posible) mismo descarte de bits aplicado en la firma. El resultado es $z$.
- Calcular $w=s^{-1} \bmod n$.
- Calcular $u_1=z \cdot w \bmod n$.
- Calcular $u_2=r \cdot w \bmod n$.
- Calcular el punto de la curva $(x_1,y_1) = u_1G + u_2Q$. Si el resultado es el punto $0$, la firma es inválida.

La firma es válida si y solo si $r \equiv x_1 \pmod n$.
