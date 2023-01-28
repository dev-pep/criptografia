#!/usr/bin/env python3

# Utilidades relacionadas con la seed phrase (BIP-39).
# https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki

import json
import random
import hashlib

# Funciones auxiliares *************************************************************************************************

def check_phrase(phrase):  # phrase es una lista de enteros
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
    # Lista de enteros a string con la frase
    global wordlist
    resul = ''
    for l in lista:
        resul += ' ' + wordlist[l]
    return resul.strip()


def input_int(ms, vals, default=None):
    # vals puede ser una lista o un range
    resul = None
    while resul not in vals:
        n = input(f'{ms}: ')
        if n == '':
            resul = default
            continue
        try:
            resul = int(n)
        except ValueError:
            continue
    return resul


def pinta_menu():
    global menu
    maxlen = 0
    for opcion in menu:
        if len(opcion[0]) > maxlen:
            maxlen = len(opcion[0])
    print('╔' + (6 + maxlen) * '═' + '╗')
    for i in range(len(menu)):
        relleno = maxlen - len(menu[i][0]) + 1
        print(f'║ {i + 1:2}. {menu[i][0]}' + relleno * ' ' + '║')
    print('║  X. Salir' + (maxlen - 4) * ' ' + '║' )
    print('╚' + (6 + maxlen) * '═' + '╝')

# Funciones de las opciones de menú ************************************************************************************

# Generar seed phrase aleatoria:
def menu_genera():
    # Primero debemos saber cuántas palabras queremos (por defecto 12):
    nwords = input_int("Número de palabras (12, 15, 18, 21, 24; por defecto 12)",
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


# Cálculo última palabra:
def menu_ultima():
    # Primero debemos saber cuántas palabras queremos (por defecto 12):
    nwords = input_int("Número de palabras (12, 15, 18, 21, 24; por defecto 12)",
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
    # Primero debemos saber cuántas palabras queremos (por defecto 12):
    nwords = input_int("Número de palabras (12, 15, 18, 21, 24; por defecto 12)",
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
    # Primero debemos saber cuántas palabras queremos (por defecto 12):
    nwords = input_int("Número de palabras (12, 15, 18, 21, 24; por defecto 12)",
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

menu = (
    ("Generar seed phrase aleatoria", menu_genera),
    ("Cálculo última palabra", menu_ultima),
    ("Comprobar seed phrase", menu_check),
    ("Mostrar números de una seed phrase", menu_numbers),
)

# Programa *************************************************************************************************************

# Leemos wordlist:
f = open('wordlist.json', 'rt')
wordlist = json.load(f)
f.close()
# Bucle principal:
accion = ''
while accion != 'X':
    pinta_menu()
    accion = input('Introduce opción: ').upper()
    if accion == 'X':
        continue
    try:
        numAccion = int(accion)
        if numAccion < 1 or numAccion > len(menu):
            raise ValueError
    except ValueError:
        print('Opción no válida.')
        continue
    menu[numAccion - 1][1]()
