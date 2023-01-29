#!/usr/bin/env python3

# Utilidades relacionadas con el cálculo de números primos.

import random
import math
import json
import utils

# Funciones auxiliares *************************************************************************************************

def es_primo(n):
    """
    Comprueba si un número es primo o no (determinista)

    :param n: El número entero a comprobar
    :return: True si es primo, False si no
    """
    if n < 2:
        return False
    sq = int(math.sqrt(n)) + 1
    for i in range(2, sq):
        if n % i == 0:
            return False
    return True

def es_primo_mr(n, k_total):
    """
    Comprueba si un número es primo o no (Miller-Rabin, no determinista)

    :param n: El número entero a comprobar
    :param k_total: El número máximo de iteraciones
    :return: True si es primo (probablemente), False si no (seguro)
    """
    # Primero descartaremos que sea divisible por uno de los primeros primos (archivo json generado)
    with open("datos/primos.json", "rt") as f:
        primos = json.load(f)
    for primo in primos:
        if n % primo == 0:
            return False
    # Descartado esto, empecemos.
    # Calculamos s y d, tal que n-1 = d 2^s
    naux = (n - 1) // 2
    s = 1
    while naux % 2 == 0:
        naux //= 2
        s +=1
    d = (n - 1) // (2 ** s)
    # Vamos a realizar las iteraciones (k):
    for k in range(k_total):
        # Obtenemos número a al azar:
        a = random.randint(2, n - 2)
        # Obtenemos a^d % n, es decir, a^((2^r)d) % n, con r=0:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue  # esta iteración de k ha mostrado que es un probable primo, pasamos a la siguiente
        # Si seguimos con la interacción actual, haremos el resto de r's (0 < r < s), que tienen diferente criterio:
        # Acelera mucho en lugar de hacer a^((2^r)d) % n incrementando la r, hacer x = x^2 mod n:
        for _ in range(1, s):  # quedan s veces
            x = pow(x, 2, n)
            # Si x es n-1 (-1 mod n), ya indica posible primo, es decir, pasaremos a la siguiente iteración de k;
            # si es 1, ya indica que seguro que es compuesto; si terminamos todas las r sin encontrar 1 ni n-1,
            # también será un compuesto:
            if x == 1 or x == n - 1:
                break  # hemos encontrado un valor indicativo en esta iteración de k
        if x != n - 1:  # solo -1 mod n nos habría indicado posible primo (y por tanto proseguiremos iteraciones)
            return False
    return True  # si tras todas las iteraciones no lo hemos podido descartar, es que probablemente sea primo

# Funciones de las opciones de menú ************************************************************************************

def menu_genera_json():
    """
    Genera los N primeros números primos, y los guarda en datos/primos.json
    """
    n = utils.input_int("¿Cuántos números primos quieres generar? (10-5000, por defecto 500)", range(10, 5001), 500)
    primos = []
    contador = 2
    while len(primos) < n:
        if es_primo(contador):
            primos.append(contador)
        contador += 1
    # Ahora generaremos el JSON:
    with open("datos/primos.json", "wt") as f:
        json.dump(primos, f, indent=4)

def menu_comprobar_num():
    """
    Comprueba si un número determinado es primo o no, y muestra el resultado en pantalla
    """
    # Preguntar número entero
    numero = utils.input_int("Número entero", None, -1)
    ninter = utils.input_int("Número de iteraciones (1-100, por defecto 10)", range(1, 101), 10)
    if es_primo_mr(numero, ninter):
        print("El número ES primo.")
    else:
        print("El número NO ES primo.")

def menu_generar_num():
    """
    Genera e imprime en pantalla un número primo de la cantidad de bits indicada
    """
    # Preguntar número de bits; 1º y último bit serán '1'
    nbits = utils.input_int("Número de bits (8-2048, por defecto 1024)", range(8, 2049), 1024)
    ninter = utils.input_int("Número de iteraciones (1-100, por defecto 64)", range(1, 101), 64)
    primo = False
    while not primo:
        print(".", end="", flush=True)
        nrand = random.randint(2 ** (nbits-1), 2 ** nbits - 1) | 1
        primo = es_primo_mr(nrand, ninter)
    print("\nNúmero primo:")
    print(nrand)
    print(f"{nbits} bits, {len(str(nrand))} cifras decimales.")

# Menu *****************************************************************************************************************

opciones_menu = (
    ("Generar primeros (JSON)", menu_genera_json),
    ("Comprobar un número", menu_comprobar_num),
    ("Generar número primo", menu_generar_num)
)

# Programa *************************************************************************************************************

# Bucle principal:
accion = utils.menu(opciones_menu)
while accion:
    accion()
    accion = utils.menu(opciones_menu)
