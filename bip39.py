#!/usr/bin/env python3

# Utilidades relacionadas con la seed phrase (BIP-39).
# https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki

import json
import random
import sha2_hashing
import utils

# Funciones auxiliares *************************************************************************************************

def check_phrase(phrase):
    """
    Comprueba que los números de índice recibidos (enteros) forman una frase correcta

    :param phrase: Lista de enteros representando una frase
    :return: True si la frase es correcta, False si no
    """
    # Cada palabra ocupa 11 bits:
    int_phrase = 0  # entero con entropía + checksum
    for word in phrase:
        int_phrase <<= 11
        int_phrase |= word
    nwords = len(phrase)
    # El número de palabras es siempre múltiplo de 3.
    n_bits_entropy = 32 * nwords // 3  # de cada 3 palabras (33 bits), 32 bits son de entropía
    # El número de bits de entropia es siempre múltiplo de 32.
    n_bits_check = n_bits_entropy // 32  # para cada 32 bits de entropía, habrá un bit adicional de checksum
    int_entropy = int_phrase >> n_bits_check  # descartamos los bits de checksum que hay a la derecha
    int_check = int_phrase & (2 ** n_bits_check - 1)
    # Ahora pasamos entropía a bytes para pasar a SHA256:
    bytes_entropy = int_entropy.to_bytes(n_bits_entropy // 8, 'big')
    # Vamos a comprobar si los bits de checksum son correctos:
    check_calc = sha2_hashing.sha256(bytes_entropy, 'int')  # digest de la entropía como número entero
    check_calc >>= (256 - n_bits_check)  # entero con solo los primeros bits del checksum
    # Comparamos:
    return int_check == check_calc

def input_frase(number):
    """
    Solicita y retorna una seed phrase personalizada

    :param number: Número de palabras en la frase (entero)
    :return: Los índices (enteros) de cada palabra
    """
    # Leemos wordlist:
    with open("datos/wordlist.json", "rt") as fjson:
        wordlist = json.load(fjson)
    # Solicita seed phrase
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
    # Leemos wordlist:
    with open("datos/wordlist.json", "rt") as fjson:
        wordlist = json.load(fjson)
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
    # Leemos wordlist:
    with open("datos/wordlist.json", "rt") as fjson:
        wordlist = json.load(fjson)
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
    """Solicita una seed phrase, y muestra los cálculos asociados"""
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
    # Cálculo del entero entropía y el checksum; explicaciones en check_phrase().
    int_phrase = 0
    for word in phrase:
        int_phrase <<= 11
        int_phrase |= word
    nwords = len(phrase)
    n_bits_entropy = 32 * nwords // 3
    n_bits_check = n_bits_entropy // 32
    int_entropy = int_phrase >> n_bits_check
    int_check = int_phrase & (2 ** n_bits_check - 1)
    # Presentación de resultados
    print("Secuencia completa binaria:")
    print(bin(int_phrase)[2:].zfill(n_bits_check + n_bits_entropy))
    print(f"Entropía ({n_bits_entropy} bits / {n_bits_entropy // 8} bytes):")
    print(bin(int_entropy)[2:].zfill(n_bits_entropy))
    print()
    print(f"Entropía (hex): {hex(int_entropy)[2:].zfill(n_bits_entropy // 4)}")
    print(f"Checksum: {bin(int_check)[2:].zfill(n_bits_check)} ({int_check})")

# Menu *****************************************************************************************************************

opciones_menu = (
    ("Generar seed phrase aleatoria", menu_genera),
    ("Cálculo última palabra", menu_ultima),
    ("Comprobar seed phrase", menu_check),
    ("Mostrar números de una seed phrase", menu_numbers),
)

# Programa *************************************************************************************************************

if __name__ == '__main__':  # no ejecutaremos menú si el archivo ha sido importado
    # Bucle principal:
    utils.menu(opciones_menu)
