#!/usr/bin/env python3

# Utilidades relacionadas con la seed phrase (BIP-39).
# https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki

import json
import random
import hashlib
import utils

# Funciones auxiliares *************************************************************************************************

def check_phrase(phrase):
    """
    Comprueba que los números de índice recibidos (enteros) forman una frase correcta

    :param phrase: Lista de enteros representando una frase
    :return: True si la phrase es correcta, False si no
    """
    # String con 0s y 1s de la frase recibida:
    all_bits = ''
    for word in phrase:
        all_bits += f'{bin(word)[2:]:>011}'
    # Strings con 0s y 1s de la entropía y el checksum:
    nwords = len(phrase)
    n_bits_entropy = 32 * nwords // 3
    n_bits_check = n_bits_entropy // 32
    entropy_bits = all_bits[:n_bits_entropy]
    check_bits = all_bits[n_bits_entropy:]
    # Ahora pasamos entropía a bytes:
    entropy_bytes = b''
    for i in range(0, n_bits_entropy, 8):
        entropy_bytes += int(entropy_bits[i:i+8], 2).to_bytes(1, 'big')
    check_calc = hashlib.sha256(entropy_bytes).digest()[0]  # primer byte del checksum (tipo bytes)
    check_calc = f'{bin(check_calc)[2:]:>08}'  # pasamos ese primer byte a string binario
    check_calc = check_calc[:n_bits_check]  # extraemos los n_bits_check primeros
    # Comparamos:
    return check_bits == check_calc

def input_frase(number):
    """
    Solicita y retorna una seed phrase personalizada

    :param number: Número de palabras en la frase (entero)
    :return: Los índices (enteros) de cada palabra
    """
    # Solicita seed phrase
    global wordlist
    phrase = input(f'Introduce seed phrase correcta de {number} palabras:\n').split()
    if len(phrase) != number:
        return False
    resul = []
    for word in phrase:
        if word not in wordlist:
            return False
        resul.append(wordlist.index(word))
    return resul


def list2string(lista):
    """
    Convierte una lista de índices enteros en un string con la frase correspondiente

    :param lista: Lista de índices (enteros)
    :return: Frase resultante (string)
    """
    global wordlist
    resul = ''
    for l in lista:
        resul += ' ' + wordlist[l]
    return resul.strip()

# Funciones de las opciones de menú ************************************************************************************

def menu_genera():
    """
    Genera una seed phrase aleatoria correcta y la muestra en pantalla
    """
    # Primero debemos saber cuántas palabras queremos (por defecto 12):
    nwords = utils.input_int("Número de palabras (12, 15, 18, 21, 24; por defecto 12)",
                       [12, 15, 18, 21, 24], 12)
    # Elegimos todas las palabras excepto la última:
    phrase = []
    while len(phrase) != nwords - 1:
        num = random.randint(0, 2047)  # no hay problema con repetir palabras
        phrase.append(num)
    # Ahora vamos a ver todas las candidatas a última palabra:
    ultimas = []
    for word in range(2048):
        if check_phrase(phrase + [word]):
            ultimas.append(word)
    # Ahora, de entre las candidatas, elegiremos una:
    phrase.append(random.choice(ultimas))
    print(list2string(phrase))

def menu_ultima():
    """
    Calcula la última palabra de una frase incompleta (a la que le falta esta) y muestra todas las posibilidades
    """
    # Primero debemos saber cuántas palabras queremos (por defecto 12):
    nwords = utils.input_int("Número de palabras (12, 15, 18, 21, 24; por defecto 12)",
                       [12, 15, 18, 21, 24], 12)
    lista = input_frase(nwords - 1)
    if not lista:
        print('Cancelado.')
        return
    # Ahora vamos a mostrar todas las posibilidades para la última palabra:
    ultimas = []
    for word in range(2048):
        if check_phrase(lista + [word]):
            ultimas.append(word)
    print("Posibilidades:")
    for word in ultimas:
        print(wordlist[word], end= ' ')
    print()

# Comprobar seed phrase
def menu_check():
    """
    Solicita una seed phrase e indica si es correcta o no
    """
    # Primero debemos saber cuántas palabras queremos (por defecto 12):
    nwords = utils.input_int("Número de palabras (12, 15, 18, 21, 24; por defecto 12)",
                       [12, 15, 18, 21, 24], 12)
    lista = input_frase(nwords)
    if not lista:
        print('Cancelado.')
        return
    if check_phrase(lista):
        print('Frase correcta.')
    else:
        print('Frase incorrecta.')

# Mostrar números de una seed phrase
def menu_numbers():
    """
    Solicita una seed phrase, y muestra los cálculos asociados
    """
    # Primero debemos saber cuántas palabras queremos (por defecto 12):
    nwords = utils.input_int("Número de palabras (12, 15, 18, 21, 24; por defecto 12)",
                       [12, 15, 18, 21, 24], 12)
    phrase = input_frase(nwords)
    if not phrase:
        print('Cancelado.')
        return
    # Ahora comprobamos que la frase sea correcta:
    if check_phrase(phrase):
        print('Frase correcta.')
    else:
        print('Frase incorrecta.')
        return
    # String con 0s y 1s de la frase:
    all_bits = ''
    for word in phrase:
        all_bits += f'{bin(word)[2:]:>011}'
    # Strings con 0s y 1s de la entropía y el checksum:
    n_bits_entropy = 32 * nwords // 3
    entropy_bits = all_bits[:n_bits_entropy]
    check_bits = all_bits[n_bits_entropy:]
    print('Secuencia completa:')
    print(all_bits)
    print(f'Entropía ({n_bits_entropy} bits / {n_bits_entropy // 8} bytes):')
    for i in range(0, n_bits_entropy, 8):
        if (i % 64 == 0) and (i > 0):
            print()
        print(entropy_bits[i:i+8], end=' ')
    print()
    print(f'Entropía (hex): {hex(int(entropy_bits, 2))[2:]}')
    print(f'Checksum: {check_bits} ({int(check_bits, 2)})')

# Menu *****************************************************************************************************************

opciones_menu = (
    ("Generar seed phrase aleatoria", menu_genera),
    ("Cálculo última palabra", menu_ultima),
    ("Comprobar seed phrase", menu_check),
    ("Mostrar números de una seed phrase", menu_numbers),
)

# Programa *************************************************************************************************************

# Leemos wordlist:
f = open('datos/wordlist.json', 'rt')
wordlist = json.load(f)
f.close()

# Bucle principal:
accion = utils.menu(opciones_menu)
while accion:
    accion()
    accion = utils.menu(opciones_menu)
