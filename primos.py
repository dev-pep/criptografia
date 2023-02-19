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

def es_primo_mr(n, k):
    """
    Comprueba si un número es primo o no (Miller-Rabin, no determinista)

    :param n: El número entero a comprobar
    :param k: El número máximo de iteraciones
    :return: True si es primo (probablemente), False si no (seguro)
    """

    # Un pequeño filtro para empezar. Primero descartaremos que sea < 2, o uno de los primeros primos,
    # o divisible por uno de estos (leemos archivo json generado):
    if n < 2:
        return False
    with open("datos/primos.json", "rt") as f:
        primos = json.load(f)
    if n in primos:
        return True
    for primo in primos:
        if n % primo == 0:
            return False
    # Descartado esto, empecemos.
    # Calculamos s y d, tal que n-1 = d*2^s (n es impar, d será impar)
    d = (n - 1) // 2
    s = 1
    while d % 2 == 0:
        d //= 2
        s +=1
    # Empezamos las k interacciones:
    for _ in range(k):
        # Primero elegimos una base al azar, entre 2 y n-2:
        a = random.randint(2, n - 2)
        # Obtenemos el primero de los valores: a^d (mod n):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:  # 1 (mod n), o -1 (mod n)
            continue  # probable primo, procesamos otra base
        probable_primo = False
        for _ in range(s):  # s veces
            x = pow(x, 2, n)  # elevamos x al cuadrado
            if x == 1:  # llegamos a 1 sin haber pasado por -1: número compuesto
                return False
            if x == n - 1:  # -1 (mod n)
                probable_primo = True
                break
        if not probable_primo:  # si no hay -1 para ninguna r con esta base, es compuesto:
            return False
    # Si tras todas las iteraciones no lo hemos podido descartar, es que probablemente sea primo:
    return True

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

if __name__ == '__main__':  # no ejecutaremos menú si el archivo ha sido importado
    # Bucle principal:
    utils.menu(opciones_menu)
