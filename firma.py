#!/usr/bin/env python3

# Utilidades relacionadas con firma digital.

import random

import sha2_hashing
import utils
import primos

# Funciones de las opciones de menú ************************************************************************************

def menu_dsa():
    """Muestra un ejemplo de funcionamiento de firma con DSA"""
    # Usaremos como función hash SHA-224 (puede ser cualquiera de las SHA-2, incluso SHA-1)
    l = 1024  # longitud clave; múltiplo de 64, 512<=l<=1024; actualmente recomendado 2048, o incluso 3072
    n = 160  # módulo; n<l, y n debe ser menor o igual que la longitud del hash (en este caso 512)
    # Ahora buscaremos un número primo q de n bits:
    q = 0
    while not primos.es_primo_mr(q, 25):
        q = random.randint(2 ** (n - 1), 2 ** n - 1) | 1
    # Ahora un número primo p de l bits tal que (p-1) es múltiplo de q:
    # Si p tiene l bits, estará entre 2^(l-1) y 2^l-1, y si tiene que ser múltiplo de q, es decir k*q, entonces
    # k tiene que ser entre 1+2^(l-1)/q y (2^l-1)/q:
    p = 0
    minimo = 1 + 2 ** (l-1) // q
    maximo = (2 ** l - 1) // q
    while not primos.es_primo_mr(p, 25):
        p_menos1 = random.randint(minimo, maximo) * q
        p = p_menos1 + 1
    g = 1
    while g == 1:
        h = random.randint(2, p - 2)  # h aleatorio [2, p-2]
        g = pow(h, (p - 1) // q, p)
    # El número g es el generador, de orden q.
    # Los parámetros (p, q, g) se pueden compartir entre todos los usuarios que van a validar firmas.
    print("Parámetros del dominio (a compartir entre todos):")
    print(f"p: {p}")
    print(f"q: {q}")
    print(f"g (generador, de orden q): {p}")

    # Cálculo de las claves:
    x = random.randint(1, q - 1)  # x es la clave privada
    y = pow(g, x, p)  # y es la clave pública
    print("Claves del firmante:")
    print(f"Clave privada: {x}")
    print(f"Clave pública: {y}")

    # Firma del mensaje:
    m = b"Luke, yo soy tu padre"  # mensaje
    digest = sha2_hashing.sha224(m, "int")
    # Como n=160, solo usaremos los 160 primeros bits, con lo que eliminamos los 64 menos significativos:
    digest >>= 64
    r = s = 0
    while r == 0 or s == 0:
        k = random.randint(1, q - 1)  # se debe crear un k aleatorio distinto cada nueva firma
        r = pow(g, k, p) % q
        if r == 0:
            continue
        k_inverso = utils.inverso_modn(k, q)
        s = (k_inverso * (digest + x * r)) % q
    # La firma es (r, s).
    print("Envío del firmante:")
    print(f"Mensaje: {m}")
    print("Firma:")
    print(f"r: {r}")
    print(f"s: {s}")

    # Lado receptor. El receptor recibe (m, y, r, s), es decir, el mensaje en claro, la clave pública del remitente
    # que firma, y la firma en sí. Por otro lado, todos conocen los parámetros (p, q, g). Pero solo el remitente
    # dispone de x.
    # Comprobaciones:
    assert 0 < r < q and 0 < s < q
    w = utils.inverso_modn(s, q)
    digest = sha2_hashing.sha224(m, "int")  # calcula el digest por su cuenta
    digest >>= 64  # nuevamente usa solo los primeros 160 bits
    u1 = (digest * w) % q
    u2 = (r * w) % q
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p ) % q
    # La firma es válida solo si v == r:
    assert v == r
    print("Comprobación de la firma; el valor calculado v debe ser igual a r para que la firma sea válida:")
    print(f"r: {r}")
    print(f"v: {v}")

# Menu *****************************************************************************************************************

opciones_menu = (
    ("Ejemplo de firma con DSA", menu_dsa),
)

# Programa *************************************************************************************************************

if __name__ == '__main__':  # no ejecutaremos menú si el archivo ha sido importado
    # Bucle principal:
    utils.menu(opciones_menu)
