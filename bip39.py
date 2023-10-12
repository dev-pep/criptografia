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
    bytes_entropy = int_entropy.to_bytes(n_bits_entropy // 8, "big")
    # Vamos a comprobar si los bits de checksum son correctos:
    check_calc = sha2_hashing.sha256(bytes_entropy, "int")  # digest de la entropía como número entero
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

def list2string(lista, tobytes=False):
    """Convierte una lista de índices enteros en un string con la frase correspondiente

    :param lista: Lista de índices (enteros)
    :param tobytes: Si es True, el resultado a retornar será bytes en lugar de string
    :return: Frase resultante: string (o bytes si tobytes es True)
    """
    # Leemos wordlist:
    with open("datos/wordlist.json", "rt") as fjson:
        wordlist = json.load(fjson)
    resul = ''
    for l in lista:
        resul += ' ' + wordlist[l]
    resul = resul.strip()
    if tobytes:
        resul = bytes(resul, "utf-8")
    return resul

def string2list(cadena):
    """Convierte un string conteniendo una seed phrase en una lista con los índices correspondientes

    :param cadena: string con la seed phrase (str)
    :return: lista de índices (int) de las palabras de la frase
    """
    # Leemos wordlist:
    with open("datos/wordlist.json", "rt") as fjson:
        wordlist = json.load(fjson)
    resul = []
    palabras = cadena.strip().split()
    for palabra in palabras:
        try:
            i = wordlist.index(palabra)
        except ValueError:
            return []    # palabra no válida
        resul.append(i)
    return resul

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

    :param seedphrase: la seed phrase (bytes)
    :param passphrase: contraseña opcional (bytes)
    :param niter: número de iteraciones
    :return: la clave derivada (bip-39 seed) (bytes)
    """
    # Sal: "mnemonic" + passphrase (la passphrase puede estar vacía)
    sal = b'mnemonic' + passphrase
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

def random_phrase(nwords, formato="num"):
    """Genera y retorna una seed phrase aleatoria correcta

    :param nwords: número de palabras (12, 15, 18, 21 o 24)
    :param formato: formato deseado: "num" (lista de índices enteros), "str" o "bytes"
    :return: seed phrase (string)
    """
    if nwords not in [12, 15, 18, 21, 24]:
        return None
    # Primero elegimos todas las palabras excepto la última:
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
    if formato == "num":
        return phrase
    if formato == "str":
        return list2string(phrase)
    return bytes(list2string(phrase), "utf-8")

def print_frases(palabras, wordlist):
    """Genera una lista de seed phrases coincidentes con las palabras del patrón indicado

    :param palabras: lista de palabras del patrón (puede incluir las palabra '1', '2' y/o '3')
    :param wordlist: la wordlist estándar
    :return: la lista de seed phrases
    """
    comodines = [[], [], []]  # índices de las palabras comodín '1', '2' o '3', respectivamente
    palabrasInt = []  # palabras no comodín (y None para los comodines)
    for i in range(len(palabras)):
        if palabras[i] in ["1", "2", "3"]:
            palabrasInt.append(None)
            comodines[int(palabras[i]) - 1].append(i)
        else:
            palabrasInt.append(wordlist.index(palabras[i]))
    # Vamos a generar todas las frases posibles, dependiendo del número de comodines:
    # 0 comodines:
    if not comodines[0]:
        if check_phrase(palabrasInt):
            print("1.", list2string(palabrasInt))
    # 1 comodín:
    elif not comodines[1]:
        nfrase = 1
        for palabra1 in range(2048):
            for indice in comodines[0]:
                palabrasInt[indice] = palabra1
            if check_phrase(palabrasInt):
                print(nfrase, end='')
                print(".", list2string(palabrasInt))
                nfrase += 1
    # 2 comodines:
    elif not comodines[2]:
        nfrase = 1
        for palabra1 in range(2048):
            for indice in comodines[0]:
                palabrasInt[indice] = palabra1
            for palabra2 in range(2048):
                for indice in comodines[1]:
                    palabrasInt[indice] = palabra2
                if check_phrase(palabrasInt):
                    print(nfrase, end='')
                    print(".", list2string(palabrasInt))
                    nfrase += 1
    # 3 comodines:
    else:
        nfrase = 1
        for palabra1 in range(2048):
            for indice in comodines[0]:
                palabrasInt[indice] = palabra1
            for palabra2 in range(2048):
                for indice in comodines[1]:
                    palabrasInt[indice] = palabra2
                for palabra3 in range(2048):
                    for indice in comodines[2]:
                        palabrasInt[indice] = palabra3
                    if check_phrase(palabrasInt):
                        print(nfrase, end='')
                        print(".", list2string(palabrasInt))
                        nfrase += 1

# Funciones de las opciones de menú ************************************************************************************

def menu_genera():
    """Genera una seed phrase aleatoria correcta y la muestra en pantalla"""
    # Primero debemos saber cuántas palabras queremos (por defecto 12):
    nwords = utils.input_int("Número de palabras (12, 15, 18, 21, 24; por defecto 12)",
                       [12, 15, 18, 21, 24], 12)
    print(random_phrase(nwords, "str"))

def menu_genera_pattern():
    """Genera una lista de seed phrases que cumplen con el patron dado, y las muestra en pantalla"""
    ok = False
    nwords = [12, 15, 18, 21, 24]
    # Leemos wordlist:
    with open("datos/wordlist.json", "rt") as fjson:
        wordlist = json.load(fjson)
    # Primero debemos introducir un patrón correcto:
    while not ok:
        pattern = input("Introduce patrón; usa '1', '2' o '3' como palabras comodín (sin saltos, se pueden repetir).\n"
                        + "'X' cancela la operación:\n")
        if pattern.strip().upper() == "X":
            return
        palabras = pattern.split()
        if len(palabras) not in nwords:
            print("Solo es válido un patrón con 12, 15, 18, 21 o 24 palabras.")
            continue
        nextComodin = 1
        palabrasInvalidas = []
        for palabra in palabras:
            if palabra in ['1', '2', '3']:
                comodin = int(palabra)
                if comodin > nextComodin:  # salto en los comodines
                    nextComodin = 0
                    break
                elif comodin == nextComodin and nextComodin < 3:
                    nextComodin += 1
            elif palabra not in wordlist:
                palabrasInvalidas.append(palabra)
        if not nextComodin:
            print("No es posible indicar saltos en los comodines.")
            continue
        if palabrasInvalidas:
            print("Palabras inválidas:")
            for palabra in palabrasInvalidas:
                print("    ", palabra)
            continue
        ok = True
    # Ya tenemos el patrón introducido como lista (variable palabras), vamos a imprimir las frases:
    print_frases(palabras, wordlist)

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

def phrase2seed(phrase, password, niter=2048):
    """Dada una seed phrase correcta y una contraseña, generará la seed

    La función no comprueba si se trata de una seed phrase correcta o no.
    :param phrase: seed phrase correcta (str)
    :param password: contraseña (puede estar en blanco) (str)
    :param niter: número de iteraciones para pbkdf2() (int)
    :return: seed de 512 bits (int)
    """
    seed = pbkdf2(bytes(phrase, "utf-8"), bytes(password, "utf-8"), niter)
    seed = int.from_bytes(seed, "big")
    return seed

def menu_numbers():
    """Solicita una seed phrase y algunos datos más, y muestra los cálculos asociados"""
    phrase = input_frase()
    if not phrase:
        print('Cancelado.')
        return
    # Ahora comprobamos que la frase sea correcta:
    if check_phrase(phrase):
        print("Frase correcta.")
    else:
        print("Frase incorrecta.")
        return
    niter = utils.input_int("Número de iteraciones PBKDF2 (1-50000). Por defecto 2048 (especificado por BIP-39)",
                            range(1, 50001), 2048)
    passphrase = input("Passphrase (opcional): ")
    print("Calculando...")
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
    seed = phrase2seed(list2string(phrase), passphrase, niter)
    # Presentación de resultados
    print("Secuencia completa binaria:")
    print(bin(int_phrase)[2:].zfill(n_bits_check + n_bits_entropy))
    print(f"Entropía ({n_bits_entropy} bits / {n_bits_entropy // 8} bytes):")
    print(bin(int_entropy)[2:].zfill(n_bits_entropy))
    print(f"Entropía (hex): {hex(int_entropy)[2:].zfill(n_bits_entropy // 4)}")
    print(f"Checksum: {bin(int_check)[2:].zfill(n_bits_check)} ({int_check})")
    print("Seed BIP-39 (512 bits):")
    print(f"{hex(seed)[2:].zfill(128)}")

# Menu *****************************************************************************************************************

opciones_menu = (
    ("Generar seed phrase aleatoria", menu_genera),
    ("Generar seed phrases (con patrón)", menu_genera_pattern),
    ("Cálculo última palabra", menu_ultima),
    ("Comprobar seed phrase", menu_check),
    ("Mostrar números de una seed phrase", menu_numbers),
)

# Programa *************************************************************************************************************

if __name__ == '__main__':  # no ejecutaremos menú si el archivo ha sido importado
    # Bucle principal:
    utils.menu(opciones_menu)
