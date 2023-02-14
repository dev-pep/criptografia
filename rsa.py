#!/usr/bin/env python3

# Utilidades relacionadas con el algoritmo RSA.

import random
import utils
import primos

# Funciones auxiliares *************************************************************************************************

def mcd(x, y):
    """Calcula el máximo común divisor de dos enteros mediante el algoritmo de Euclides

    :param x: primer entero
    :param y: segundo entero
    :return: máximo común divisor de los dos enteros
    """
    x1 = max(x, y)
    x2 = min(x, y)
    # Hallaremos q y r tal que: x1 = q * x2 + r
    q = x1 // x2
    r = x1 - q * x2
    while r:  # mientras el resto no sea 0
        lastr = r
        x1 = x2
        x2 = r
        q = x1 // x2
        r = x1 - q * x2
    return lastr

def mcm(x, y):
    """Calcula el mínimo común múltiplo de dos enteros usando el algoritmo de Euclides para encontrar antes el mcd

    :param x: primer entero
    :param y: segundo entero
    :return: mínimo común múltiplo de los dos enteros
    """
    return abs(x * y) // mcd(x, y)

def euclid_ext(x, y):
    """Calcula el mcd y los factores de Bezout de dos enteros mediante el algoritmo extendido de Euclides

    :param x: primer entero
    :param y: segundo entero
    :return: máximo común divisor de los dos enteros, así como los coeficientes de Bezout (mcd, s, t)
    """
    # Buscaremos el mcd, así como los coeficientes s y t de la identidad de Bezout: mcd = s*x + t*y para algún x, y.
    # Para ello usaremos 4 series de datos:
    q = [None, max(x, y)]  # cocientes
    r = [max(x, y), min(x, y)]  # restos
    s = [1, 0]  # coeficientes s
    t = [0, 1]  # coeficientes t
    while r[-1]:  # mientras el último elemento de r no sea 0
        q.append(r[-2] // r[-1])
        r.append(r[-2] - q[-1] * r[-1])
        s.append(s[-2] - q[-1] * s[-1])
        t.append(t[-2] - q[-1] * t[-1])
    # Ya tenemos el resultado. Si lo usamos para encontrar el inverso módulo n, es decir, si buscamos
    # un número N tal que y * N mod x = 1, la respuesta es t[-2] mod x
    return r[-2], s[-2], t[-2]

def inverso_modn(x, n):
    """Calcula el inverso módulo n del entero x

    Utiliza el algoritmo de Euclides extendido, euclid_ext().
    :param x: entero del que calcular el inverso módulo n
    :param n: módulo para el cálculo
    :return: el inverso módulo n calculado
    """
    # El resultado será un número y tal que (x * y) % n = 1
    assert(n > x)
    inv = euclid_ext(n, x)[2] % n
    try:
        assert(x * inv % n == 1)
    except AssertionError:
        # x solo tiene inverso módulo n si x y n son coprimos
        return None
    return inv

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
    # Primero, obtenemos los números primos p y q (y n):
    p = rnd_primo(nbits, k)
    q = rnd_primo(nbits, k)
    n = p * q
    # Ahora, calculamos λ(n) (Carmichael's totient):
    car_toti = mcm(p - 1, q - 1)
    # Valor típico para e:
    e = 65537
    assert (e < car_toti)
    # Ya solo queda calcular la clave privada (d), mediante el algoritmo de Euclides extendido.
    # Se debe dar e * d = 1 (mod car_toti):
    d = inverso_modn(e, car_toti)
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

# Menu *****************************************************************************************************************

opciones_menu = (
    ("Genera par de claves", menu_genera_claves),
)

# Programa *************************************************************************************************************

if __name__ == '__main__':  # no ejecutaremos menú si el archivo ha sido importado
    # Bucle principal:
    utils.menu(opciones_menu)
