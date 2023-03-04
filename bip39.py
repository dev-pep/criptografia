#!/usr/bin/env python3

# Utilidades relacionadas con la seed phrase (BIP-39).
# https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki

import json
import random
import sha2_hashing
import utils

# Funciones auxiliares *************************************************************************************************

def check_phrase(phrase):
    """Comprueba que los números de índice recibidos (enteros) forman una frase correcta

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

def input_frase(full=True):
    """Solicita y retorna una seed phrase personalizada

    :param full: Si es True, solicitará una frase completa, de lo contrario, una palabra menos
    :return: Los índices (enteros) de cada palabra
    """
    # Número de palabras aceptadas:
    if full:
        mensaje = "Introduce una frase válida (12, 15, 18, 21 o 24 palabras), o X para cancelar: "
        nwords = [12, 15, 18, 21, 24]
    else:
        mensaje = "Frase válida sin la última palabra (11, 14, 17, 20 o 23 palabras), o X para cancelar: "
        nwords = [11, 14, 17, 20, 23]
    # Leemos wordlist:
    with open("datos/wordlist.json", "rt") as fjson:
        wordlist = json.load(fjson)
    # Solicita seed phrase
    ok = False
    while not ok:
        phrase_str = input(f"{mensaje}\n")
        if phrase_str.upper() == "X":
            return False
        phrase = phrase_str.split()
        if len(phrase) not in nwords:
            print("Número de palabras erróneo.")
            continue
        resul = []
        ok = True
        for word in phrase:
            if word not in wordlist:
                print(f"Palabra {word} no es válida.")
                ok = False
                break
            resul.append(wordlist.index(word))
    return resul

def list2string(lista):
    """Convierte una lista de índices enteros en un string con la frase correspondiente

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

def hmac_sha512(k, ms):
    """Es la función pseudo aleatoria utilizada por pbkdf2()

    :param k: contraseña secreta; recibe la seedphrase del PBKDF2 (bytes)
    :param ms: mensaje a validar; recibe la sal (bytes)
    :return: clave derivada; el digest resultante que combina clave y mensaje (bytes)
    """
    # Cuando HMAC usa SHA-512, block size es 128 bytes; la salida es de 64 bytes.
    # Si la clave excede el tamaño del bloque, aplicamos su hash:
    if len(k) > 128:
        k = sha2_hashing.sha512(k, "bytes")
    # Sea como sea, la clave tiene que ocupar 128 bytes (rellenar con bytes 0 por la derecha):
    k += (128 - len(k)) * b'\x00'
    # Paddings:
    opad = b'\x5c' * 128
    ipad = b'\x36' * 128
    # Resto de cálculos:
    return sha2_hashing.sha512(utils.xor(k, opad) + sha2_hashing.sha512(utils.xor(k, ipad) + ms, "bytes"), "bytes")

def pbkdf2(seedphrase, passphrase, niter=2048):
    """Calcula la seed mediante la Password-Based Key Derivation Function 2

    Parámetros específicos para BIP-39: función pseudo aleatoria HMAC-SHA512, sal "mnemonic"+passphrase,
    2048 iteraciones, y 512 bits en la salida (derived key).

    :param seedphrase: la seed phrase
    :param passphrase: contraseña opcional
    :param niter: número de iteraciones
    :return: la clave derivada (bip-39 seed)
    """
    seedphrase = bytes(seedphrase, "utf-8")  # pasamos de string a bytes
    # Sal: "mnemonic" + passphrase (la passphrase puede estar vacía)
    sal = b'mnemonic' + bytes(passphrase, "utf-8")
    # dklen = hlen, por lo que la DK es igual a T1, es decir, DK = F(Password, Salt, 2048, 1).
    # Vamos a calcular U1, U2,... U2048, y los iremos añadiendo mediante xor al resultado
    resul = hmac_sha512(seedphrase, sal + b'\x00\x00\x00\x01')
    # resul contiene U1; falta añadir (con xor) U2,...U2048:
    u_anterior = resul
    # Quedan niter-1 iteraciones, porque la primera (U1) ya está hecha:
    for _ in range(niter - 1):
        u_next = hmac_sha512(seedphrase, u_anterior)  # u_anterior hace de sal
        resul = utils.xor(resul, u_next)
        u_anterior = u_next
    return resul

# Funciones de las opciones de menú ************************************************************************************

def menu_genera():
    """Genera una seed phrase aleatoria correcta y la muestra en pantalla"""
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
    """Calcula la última palabra de una frase incompleta (a la que le falta esta) y muestra todas las posibilidades"""
    # Leemos wordlist:
    with open("datos/wordlist.json", "rt") as fjson:
        wordlist = json.load(fjson)
    lista = input_frase(False)
    if not lista:
        print("Cancelado.")
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
    """Solicita una seed phrase e indica si es correcta o no"""
    lista = input_frase()
    if not lista:
        print('Cancelado.')
        return
    if check_phrase(lista):
        print('Frase correcta.')
    else:
        print('Frase incorrecta.')

# Mostrar números de una seed phrase
def menu_numbers():
    """Solicita una seed phrase y algunos datos más, y muestra los cálculos asociados"""
    phrase = input_frase()
    if not phrase:
        print('Cancelado.')
        return
    # Ahora comprobamos que la frase sea correcta:
    if check_phrase(phrase):
        print("Frase correcta. Calculando...")
    else:
        print("Frase incorrecta.")
        return
    niter = utils.input_int("Número de iteraciones PBKDF2 (1-50000). Por defecto 2048 (especificado por BIP-39)",
                            range(1, 50001), 2048)
    passphrase = input("Passphrase (opcional): ")
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
    # Vamos a generar la semilla (seed):
    seed = pbkdf2(list2string(phrase), passphrase, niter)
    seed = int.from_bytes(seed, "big")
    # Presentación de resultados
    print("Secuencia completa binaria:")
    print(bin(int_phrase)[2:].zfill(n_bits_check + n_bits_entropy))
    print(f"Entropía ({n_bits_entropy} bits / {n_bits_entropy // 8} bytes):")
    print(bin(int_entropy)[2:].zfill(n_bits_entropy))
    print(f"Entropía (hex): {hex(int_entropy)[2:].zfill(n_bits_entropy // 4)}")
    print(f"Checksum: {bin(int_check)[2:].zfill(n_bits_check)} ({int_check})")
    print("Seed (512 bits):")
    print(f"{hex(seed)[2:].zfill(128)}")

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
