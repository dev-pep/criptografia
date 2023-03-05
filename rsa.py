#!/usr/bin/env python3

# Utilidades relacionadas con el algoritmo RSA.

import random
import utils
import primos

# Funciones auxiliares *************************************************************************************************

def rnd_primo(nbits=1024, k=10):
    """Obtiene un número primo aleatorio de la cantidad de bits especificada (útil para p y q)

    :param nbits: número de bits del primo
    :param k: número de iteraciones Miller-Rabin
    :return: el primo aleatorio
    """
    es_primo = False
    while not es_primo:
        # Obtendremos un número primo siguiendo recomendaciones habituales. En primer lugar, se recomiendan 1024 bits.
        entero = random.randint(0, 2 ** nbits - 1)
        # Colocamos el primer bit a 1 (si fuese un 0 ya no sería un entero de nbits):
        entero |= 2 ** (nbits - 1)
        # Ahora colocamos el segundo bit también a 1: es la única forma de asegurar que dos números primos de n bits
        # multiplicados produzcan un número de n*2 bits (y no n*2 - 1), lo cual se recomienda frecuentemente:
        entero |= 2 ** (nbits - 2)
        # También colocamos el último bit a 1, para asegurarnos de que es un entero impar:
        entero |= 1
        es_primo = primos.es_primo_mr(entero, k)  # k=10 iteraciones parecen ser más que suficientes
    return entero

def genera_claves_rsa(nbits, k):
    """Genera claves pública y privada RSA y las retorna

    :param nbits: número de bits de cada primo (p y q)
    :param k: número de iteraciones en el algoritmo de primalidad Miller-Rabin
    :return: orden n (p*q), clave pública, clave privada
    """
    # Primero, obtenemos los números primos p y q (y n):
    p = rnd_primo(nbits, k)
    q = rnd_primo(nbits, k)
    n = p * q
    # Ahora, calculamos λ(n) (Carmichael's totient):
    car_toti = utils.mcm(p - 1, q - 1)
    # Valor típico para e:
    e = 65537
    assert(e < car_toti)
    # Ya solo queda calcular la clave privada (d), mediante el algoritmo de Euclides extendido.
    # Se debe dar e * d = 1 (mod car_toti):
    d = utils.inverso_modn(e, car_toti)
    return n, e, d

# Funciones de las opciones de menú ************************************************************************************

def menu_genera_claves():
    """Genera el par de claves RSA"""
    nbits = utils.input_int("Número de bits de p y q (512-4096, por defecto 1024)", range(512, 4097), 1024)
    k = utils.input_int("Número de iteraciones para el cálculo de p y q (2-128, por defecto 10)", range(2, 129), 10)
    n, e, d = genera_claves_rsa(nbits, k)
    print("Clave pública:")
    print("e:", e)
    print("n:", n)
    print("Clave privada:")
    print("d:", d)

def menu_ejemplo():
    """Una simulación de encriptación / desencriptación"""
    ms_bytes = b"Luke, yo soy tu padre" # mensaje a encriptar
    ms_int = int.from_bytes(ms_bytes, "big")
    n, e, d = genera_claves_rsa(1024, 10)
    print(f"Mensaje a encriptar: {ms_bytes}")
    print(f"Mensaje pasado a entero (hex): {hex(ms_int)[2:]}")
    print(f"Orden p*q (n): {hex(n)[2:]}")
    print(f"Clave pública (e): {hex(e)[2:]}")
    print(f"Clave privada (d): {hex(d)[2:]}")
    ms_d = pow(ms_int, d, n)  # encriptamos con clave privada
    print(f"Mensaje encriptado con la clave privada: {hex(ms_d)[2:]}")
    ms_int = pow(ms_d, e, n)  # desencriptamos con la clave pública
    ms_bytes = utils.int2bytes(ms_int)
    print(f"Mensaje desencriptado con la clave pública: {hex(ms_int)[2:]}")
    print(f"Mensaje desencriptiado pasado a bytes: {ms_bytes}")
    ms_e = pow(ms_int, e, n)  # encriptamos con clave pública
    print(f"Mensaje encriptado con la clave pública: {hex(ms_e)[2:]}")
    ms_int = pow(ms_e, d, n)  # desencriptamos con la clave privada
    print(f"Mensaje desencriptado con la clave privada: {hex(ms_int)[2:]}")
    ms_bytes = utils.int2bytes(ms_int)
    print(f"Mensaje desencriptado pasado a bytes: {ms_bytes}")

# Menu *****************************************************************************************************************

opciones_menu = (
    ("Genera par de claves", menu_genera_claves),
    ("Ejemplo de funcionamiento", menu_ejemplo),
)

# Programa *************************************************************************************************************

if __name__ == '__main__':  # no ejecutaremos menú si el archivo ha sido importado
    # Bucle principal:
    utils.menu(opciones_menu)
