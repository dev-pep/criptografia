#!/usr/bin/env python3

# Utilidades relacionadas con la seed phrase (BIP-39).
# https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki

import json
import random
import sha2_hashing
import utils
import time

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
    resul = []
    while not ok:
        phrase_str = input(f"{mensaje}\n")
        if phrase_str.upper() == "X":
            return False
        phrase = phrase_str.split()
        if len(phrase) not in nwords:
            print("Número de palabras erróneo.")
            continue
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
    for litem in lista:
        resul += ' ' + wordlist[litem]
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
    """Es la función pseudoaleatoria utilizada por pbkdf2()

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

def print_frases(palabras, wordlist, maxretries=1000):
    """Imprime en pantalla una relación de seed phrases coincidentes con el patrón indicado

    :param palabras: lista de palabras del patrón
    :param wordlist: la wordlist estándar
    :param maxretries: número máximo de reintentos a la hora de buscar una frase correcta
    :return: True (éxito) o False (error)
    """
    # Vamos a generar un diccionario con las sublistas de palabras adecuadas para los comodines
    # de empieza con y acaba en:
    sublistas = {}
    for palabra in palabras:
        if palabra != "*" and palabra.startswith("*"):
            if palabra not in sublistas.keys():
                sublistas[palabra] = []
            sufijo = palabra[1:]
            for word in wordlist:
                if word.endswith(sufijo):
                    sublistas[palabra].append(wordlist.index(word))
        elif palabra != "*" and palabra.endswith("*"):
            if palabra not in sublistas.keys():
                sublistas[palabra] = []
            prefijo = palabra[:-1]
            for word in wordlist:
                if word.startswith(prefijo):
                    sublistas[palabra].append(wordlist.index(word))
    # Ahora comprobaremos si alguna de las sublistas está vacía:
    for clave in sublistas.keys():
        if not sublistas[clave]:
            print(f"No hay coincidencias con '{clave}'.")
            return False  # retornamos con error
    # Vamos a preguntar cuántas frases queremos:
    nfrases = utils.input_int("Introduce el número de frases a generar (1-50),"
                              + " por defecto 10", range(1, 51), 10)
    # Vamos a crear un set para llenarlo de frases:
    frases = set()
    # Llenamos el set de frases (si se puede):
    while len(frases) < nfrases:
        # Vamos a generar una frase correcta (varios intentos):
        retry = 0
        ok = False
        while not ok:
            retry += 1
            if retry > maxretries:
                frases.add(f"{maxretries} intentos alcanzados ({int(time.time() * 1000000)})")
                break
            frase = []
            # Diccionario para las palabras repetibles:
            repetibles = {}
            for palabra in palabras:
                if palabra == "*":  # aleatoria
                    frase.append(random.randint(0, 2047))
                elif palabra.find("*") >= 0:  # comodín prefijo/sufijo
                    frase.append(random.choice(sublistas[palabra]))
                elif palabra.isnumeric():  # comodín repetible
                    if palabra in repetibles.keys():
                        frase.append(repetibles[palabra])
                    else:
                        repetibles[palabra] = random.randint(0, 2047)
                        frase.append(repetibles[palabra])
                else:  # solo puede ser una palabra de la wordlist
                    frase.append(wordlist.index(palabra))
            # Ya tenemos la frase; vamos a ver si es correcta y no la hemos repetido:
            if check_phrase(frase):
                n = len(frases)
                frases.add(list2string(frase))
                if len(frases) > n:  # no hemos repetido frase
                    ok = True
    # Ahora imprimimos las frases:
    contador = 1
    for frase in frases:
        print(str(contador) + ".", frase)
        contador += 1
    return True  # retornamos con éxito

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
        ok = True
        pattern = input("Introduce patrón: palabra, '*' (aleatoria), 'texto*' (empieza con), '*texto' (acaba en),\n"
                        + "'1', '2', '3', etc. (sin saltos, aleatoria repetible), 'X' (cancela la operación):\n")
        # X - Cancelar:
        if pattern.strip().upper() == "X":
            return
        # Comprobar número de elementos:
        palabras = pattern.split()
        if len(palabras) not in nwords:
            print("Solo es válido un patrón con 12, 15, 18, 21 o 24 palabras.")
            ok = False
            continue
        next_comodin = 1
        # Comprobación de los elementos (palabras) indicados:
        for palabra in palabras:
            # Aleatorio, empieza con, o acaba en:
            if palabra.startswith("*") or palabra.endswith("*"):
                continue
            # Palabra exacta:
            if palabra in wordlist:
                continue
            # Tiene que ser un entero (aleatoria repetible):
            try:
                numero = int(palabra)
            except ValueError:
                print(f"Valor inválido ({palabra}).")
                ok = False
                break
            # El entero es correcto:
            if numero < next_comodin:
                continue
            if numero == next_comodin:
                next_comodin += 1
                continue
            # Error de salto en comodín repetible:
            print(f"Salto en comodín repetible ({palabra}).")
            ok = False
            break
        # Ya tenemos el patrón introducido como lista (variable: palabras), vamos a imprimir las frases:
        if not print_frases(palabras, wordlist):
            ok = False

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
        print(wordlist[word], end=' ')
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
