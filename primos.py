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
    if n <= 2:
        return False
    if n == 2 or n == 3:
        return True
    sq = int(math.sqrt(n)) + 1
    for i in range(2, sq):
        if n % i == 0:
            return False
    return True

# Funciones de las opciones de menú ************************************************************************************

def menu_genera():
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

# Menu *****************************************************************************************************************

opciones_menu = (
    ("Generar primeros", menu_genera),
    ("Segunda opción de menú", None)
)

# Programa *************************************************************************************************************

# Bucle principal:
accion = utils.menu(opciones_menu)
while accion:
    accion()
    accion = utils.menu(opciones_menu)
