#!/usr/bin/env python3

# Algoritmos de hashing SHA-2, específicamente SHA-224, SHA-256, SHA-384 y SHA-512.

import os
import utils
import json
import decimal

# Funciones auxiliares *************************************************************************************************

def rr(entero, n, ancho):
    """
    Right rotation, rotación cíclica de bits a la derecha

    :param entero:   El entero a rotar
    :param n:        Cuántos bits hay que rotar
    :param ancho:    Cuántos bits componen el entero
    :return: El entero rotado
    """
    assert(entero < 2 ** ancho)
    return (entero >> n | entero << (ancho - n)) & (2 ** ancho - 1)

def int2hex(entero, ancho, prefijo="0x"):
    """
    A partir de un entero, retorna un string con el mismo, en formato de literal hexadecimal

    :param entero:  El entero en sí
    :param ancho:   El número de cifras hexadecimales; no corta, pero puede añadir ceros a la izquierda
    :param prefijo: Prefijo a añadir
    :return: El string con el entero, en formato de literal entero hexadecimal
    """
    return prefijo + format(hex(entero)[2:], f">0{ancho}")

def int2bin(entero, ancho, prefijo="0b"):
    """
    A partir de un entero, retorna un string con el mismo, en formato de literal binario

    :param entero:  El entero en sí
    :param ancho:   El número de cifras binarias; no corta, pero puede añadir ceros a la izquierda
    :param prefijo: Prefijo a añadir
    :return: El string con el entero, en formato de literal entero binario
    """
    return prefijo + format(bin(entero)[2:], f">0{ancho}")

def sha224(ms, formato="hex"):
    """
    Retorna el digest del mensaje de entrada, aplicando SHA-224

    :param ms: Mensaje de entrada (bytes)
    :param formato: Formato de la salida: 'hex' (string), 'bin' (string) o 'int' (entero)
    :return: El digest resultante
    """
    # Leemos el archivo de constantes:
    with open("datos/hash.json", "rt") as fjson:
        constantes = json.load(fjson)
    # Al ser la función prácticamente igual a sha256(), solo se comentan las diferencias. El resto, sin comentar.
    longitud = len(ms) * 8
    if len(ms) % 64 != 56:
        ms += b'\x80'
    if len(ms) % 64 == 56:
        bytes0_padding = 0
    elif len(ms) % 64 < 56:
        bytes0_padding = 56 - (len(ms) % 64)
    else:
        bytes0_padding = 120 - (len(ms) % 64)
    ms += bytes0_padding * b'\x00'
    long64 = int.to_bytes(longitud, 8, 'big')
    ms += long64
    bloques = [ms[i:i+64] for i in range(0, len(ms), 64)]
    H = []
    for i in range(8):
        hexstr = constantes['SHA-224']['h'][i]  # Estos valores son distintos que en el caso de SHA-256
        H.append(int(hexstr[2:], 16))
    K = []
    for i in range(64):
        hexstr = constantes['SHA-224']['k'][i]
        K.append(int(hexstr[2:], 16))
    for bloque in bloques:
        M = [bloque[i:i + 4] for i in range(0, len(bloque), 4)]
        W = []
        for m in M:
            W.append(int.from_bytes(m, 'big'))
        for t in range(16, 64):
            s0 = rr(W[t - 15], 7, 32) ^ rr(W[t - 15], 18, 32) ^ (W[t - 15] >> 3)
            s1 = rr(W[t - 2], 17, 32) ^ rr(W[t - 2], 19, 32) ^ (W[t - 2] >>  10)
            nextW = (s0 + W[t - 16] + s1 + W[t - 7]) % (2 ** 32)
            W.append(nextW)
        a = H[0]
        b = H[1]
        c = H[2]
        d = H[3]
        e = H[4]
        f = H[5]
        g = H[6]
        h = H[7]
        for i in range(64):
            S1 = rr(e, 6, 32) ^ rr(e, 11, 32) ^ rr(e, 25, 32)
            ch = (e & f) ^ ((~e) & g)
            T1 = (h + S1 + ch + K[i] + W[i]) % (2 ** 32)
            S0 = rr(a, 2, 32) ^ rr(a, 13, 32) ^ rr(a, 22, 32)
            maj = (a & b) ^ (a & c) ^ (b & c)
            T2 = (S0 + maj) % (2 ** 32)
            h = g
            g = f
            f = e
            e = (d + T1) % (2 ** 32)
            d = c
            c = b
            b = a
            a = (T1 + T2) % (2 ** 32)
        H[0] = (H[0] + a) % (2 ** 32)
        H[1] = (H[1] + b) % (2 ** 32)
        H[2] = (H[2] + c) % (2 ** 32)
        H[3] = (H[3] + d) % (2 ** 32)
        H[4] = (H[4] + e) % (2 ** 32)
        H[5] = (H[5] + f) % (2 ** 32)
        H[6] = (H[6] + g) % (2 ** 32)
        H[7] = (H[7] + h) % (2 ** 32)
    resultado = 0
    for i in range(7):  # A diferencia de SHA-256, H[7] se descarta, quedando solo H[0..6]
        resultado += H[i] << (32 * (6 - i))
    if formato == "hex":
        return int2hex(resultado, 56, "")
    if formato == "bin":
        return int2bin(resultado, 224, "")
    if formato == "int":
        return resultado
    return None

def sha256(ms, formato="hex"):
    """
    Retorna el digest del mensaje de entrada, aplicando SHA-256

    :param ms: Mensaje de entrada (bytes)
    :param formato: Formato de la salida: 'hex' (string), 'bin' (string) o 'int' (entero)
    :return: El digest resultante
    """
    # Leemos el archivo de constantes:
    with open("datos/hash.json", "rt") as fjson:
        constantes = json.load(fjson)
    # Esta función está plenamente comentada.
    # Todos los enteros, si no se dice lo contrario, son de 32 bits, Big Endian, y toda suma es módulo 2^32.
    # Se asume que la longitud en bits del mensaje de entrada es siempre múltiplo de 8 (solo bytes completos).
    longitud = len(ms) * 8  # longitud del mensaje en bits
    # Relleno del mensaje: longitud tiene que ser 448 bits tras aplicar módulo 512, es decir, 56 bytes tras
    # aplicar módulo 64. El relleno consiste en un bit '1' seguido de todos los bits '0' necesarios, es
    # decir un byte b'\x80' (0b10000000) seguido de todos los bytes b'\x00' (0b00000000) necesarios.
    # Si es necesario, añadimos el byte b'\x80'.
    if len(ms) % 64 != 56:
        ms += b'\x80'
    # Ahora calcularemos el número de bytes b'\x00' necesarios:
    if len(ms) % 64 == 56:
        bytes0_padding = 0
    elif len(ms) % 64 < 56:
        bytes0_padding = 56 - (len(ms) % 64)  # los que faltan para 56
    else:  # len(ms) % 64 > 56
        bytes0_padding = 120 - (len(ms) % 64)  # 64 - (len(ms) % 64) + 56: los que faltan para 64, más otros 56
    # Ahora los añadimos:
    ms += bytes0_padding * b'\x00'
    # Ahora hay que añadirle un entero de 64 bits (8 bytes) Big Endian con la longitud (en bits) del mensaje inicial.
    # Tranquilos, 64 bits son suficientes para expresar una longitud de más de 2 millones de terabytes.
    long64 = int.to_bytes(longitud, 8, 'big')
    ms += long64
    # Ya está preparado el mensaje en 'ms'. Ahora dividimos el mensaje en bloques de 512 bits (64 bytes), y realizamos
    # la misma operación sobre cada uno de estos bloques.
    bloques = [ms[i:i+64] for i in range(0, len(ms), 64)]
    # En cada iteración (una por bloque de 512 bits), los valores de H[0..7] irán cambiando. Al final el digest será
    # la concatenación de estos H[0..7]. Los llamaremos "el valor hash".
    # Los inicializamos primero, antes de empezar las iteraciones:
    H = []
    for i in range(8):
        hexstr = constantes['SHA-256']['h'][i]
        H.append(int(hexstr[2:], 16))
    # También inicializaremos las constantes K[0..63]:
    K = []
    for i in range(64):
        hexstr = constantes['SHA-256']['k'][i]
        K.append(int(hexstr[2:], 16))
    # Empezamos ya las iteraciones (1 por cada 512 bits del mensaje):
    for bloque in bloques:
        # El bloque de 512 bits se divide en 16 partes de 32 bits (4 bytes)
        M = [bloque[i:i + 4] for i in range(0, len(bloque), 4)]  # M[0..15] -> el bloque en 16 partes de 4 bytes
        # Vamos a crear ahora 64 valores W[0..63], de manera que:
        #     W[0..15] = M[0..15]
        #     Para t>15:
        #     W[t] = sigma0(W[t-15]) + W[t-16] + sigma1(W[t-2]) + W[t-7]
        # Recordemos que las sumas son módulo 2^32, definamos sigma0() y sigma1():
        #     sigma0(x) = rr(x,7) xor rr(x,18) xor shr(x,3)
        #     sigma1(x) = rr(x,17) xor rr(x,19) xor shr(x,10)
        W = []
        for m in M:  # primeros 16, convertidos de bytes a int
            W.append(int.from_bytes(m, 'big'))
        for t in range(16, 64):  # resto
            s0 = rr(W[t - 15], 7, 32) ^ rr(W[t - 15], 18, 32) ^ (W[t - 15] >> 3)
            s1 = rr(W[t - 2], 17, 32) ^ rr(W[t - 2], 19, 32) ^ (W[t - 2] >>  10)
            nextW = (s0 + W[t - 16] + s1 + W[t - 7]) % (2 ** 32)
            W.append(nextW)
        # Ya tenemos los W[0..63]
        # Ahora inicializamos las variables a..h al valor hash actual, para aplicar la "función de compresión":
        a = H[0]
        b = H[1]
        c = H[2]
        d = H[3]
        e = H[4]
        f = H[5]
        g = H[6]
        h = H[7]
        # Ahora aplicaremos la función de compresión, que consiste en 64 iteraciones. Cada iteración, lo que
        # hace es calcular dos enteros T1 y T2, y luego realizar algunos cambios a las variables a..h:
        for i in range(64):
            # Como siempre, las sumas son módulo 2^32:
            #     T1 = h + SUM1(e) + ch(e,f,g) + K[i] + W[i]
            #     T2 = SUM0(a) + maj(a,b,c)
            # Y tenemos que:
            #     SUM0(x) = rr(x,2) xor rr(x,13) xor rr(x,22)
            #     SUM1(x) = rr(x,6) xor rr(x,11) xor rr(x,25)
            #     ch(x,y,z) bitwise choice, si x=0, da z; si x=1, da y
            #     maj(x,y,z) bitwise majority, si hay más 1's que 0's, es 1; si hay más 0's que 1's es 0
            S1 = rr(e, 6, 32) ^ rr(e, 11, 32) ^ rr(e, 25, 32)
            ch = (e & f) ^ ((~e) & g)
            T1 = (h + S1 + ch + K[i] + W[i]) % (2 ** 32)
            S0 = rr(a, 2, 32) ^ rr(a, 13, 32) ^ rr(a, 22, 32)
            maj = (a & b) ^ (a & c) ^ (b & c)
            T2 = (S0 + maj) % (2 ** 32)
            # Cambiamos las variables a..h:
            h = g
            g = f
            f = e
            e = (d + T1) % (2 ** 32)
            d = c
            c = b
            b = a
            a = (T1 + T2) % (2 ** 32)
        # Ya tenemos el resultado de la función de compresión, que es a..h. Sumaremos esto al valor hash actual:
        H[0] = (H[0] + a) % (2 ** 32)
        H[1] = (H[1] + b) % (2 ** 32)
        H[2] = (H[2] + c) % (2 ** 32)
        H[3] = (H[3] + d) % (2 ** 32)
        H[4] = (H[4] + e) % (2 ** 32)
        H[5] = (H[5] + f) % (2 ** 32)
        H[6] = (H[6] + g) % (2 ** 32)
        H[7] = (H[7] + h) % (2 ** 32)
    # Hemos terminado. El hash es la concatenación de los enteros H[0..7]:
    resultado = 0
    for i in range(8):
        resultado += H[i] << (32 * (7 - i))
    # Formateamos el resultado y lo retornamos:
    if formato == "hex":
        return int2hex(resultado, 64, "")
    if formato == "bin":
        return int2bin(resultado, 256, "")
    if formato == "int":
        return resultado
    return None

def sha384(ms, formato="hex"):
    """
    Retorna el digest del mensaje de entrada, aplicando SHA-384

    :param ms: Mensaje de entrada (bytes)
    :param formato: Formato de la salida: 'hex' (string), 'bin' (string) o 'int' (entero)
    :return: El digest resultante
    """
    # Leemos el archivo de constantes:
    with open("datos/hash.json", "rt") as fjson:
        constantes = json.load(fjson)
    # Al ser la función prácticamente igual a sha512(), solo se comentan las diferencias con esta.
    # El resto, sin comentar.
    longitud = len(ms) * 8
    if len(ms) % 128 != 112:
        ms += b'\x80'
    if len(ms) % 128 == 112:
        bytes0_padding = 0
    elif len(ms) % 128 < 112:
        bytes0_padding = 112 - (len(ms) % 128)
    else:
        bytes0_padding = 240 - (len(ms) % 128)
    ms += bytes0_padding * b'\x00'
    long128 = int.to_bytes(longitud, 16, 'big')
    ms += long128
    bloques = [ms[i:i+128] for i in range(0, len(ms), 128)]
    H = []
    for i in range(8):
        hexstr = constantes['SHA-384']['h'][i]  # La tabla h propia de SHA-384
        H.append(int(hexstr[2:], 16))
    K = []
    for i in range(80):
        hexstr = constantes['SHA-384']['k'][i]
        K.append(int(hexstr[2:], 16))
    for bloque in bloques:
        M = [bloque[i:i + 8] for i in range(0, len(bloque), 8)]
        W = []
        for m in M:
            W.append(int.from_bytes(m, 'big'))
        for t in range(16, 80):
            s0 = rr(W[t - 15], 1, 64) ^ rr(W[t - 15], 8, 64) ^ (W[t - 15] >> 7)
            s1 = rr(W[t - 2], 19, 64) ^ rr(W[t - 2], 61, 64) ^ (W[t - 2] >>  6)
            nextW = (s0 + W[t - 16] + s1 + W[t - 7]) % (2 ** 64)
            W.append(nextW)
        a = H[0]
        b = H[1]
        c = H[2]
        d = H[3]
        e = H[4]
        f = H[5]
        g = H[6]
        h = H[7]
        for i in range(80):
            S1 = rr(e, 14, 64) ^ rr(e, 18, 64) ^ rr(e, 41, 64)
            ch = (e & f) ^ ((~e) & g)
            T1 = (h + S1 + ch + K[i] + W[i]) % (2 ** 64)
            S0 = rr(a, 28, 64) ^ rr(a, 34, 64) ^ rr(a, 39, 64)
            maj = (a & b) ^ (a & c) ^ (b & c)
            T2 = (S0 + maj) % (2 ** 64)
            h = g
            g = f
            f = e
            e = (d + T1) % (2 ** 64)
            d = c
            c = b
            b = a
            a = (T1 + T2) % (2 ** 64)
        H[0] = (H[0] + a) % (2 ** 64)
        H[1] = (H[1] + b) % (2 ** 64)
        H[2] = (H[2] + c) % (2 ** 64)
        H[3] = (H[3] + d) % (2 ** 64)
        H[4] = (H[4] + e) % (2 ** 64)
        H[5] = (H[5] + f) % (2 ** 64)
        H[6] = (H[6] + g) % (2 ** 64)
        H[7] = (H[7] + h) % (2 ** 64)
    resultado = 0
    for i in range(6):  # En este caso se descartan H[6] y H[7], resultando H[0..5]
        resultado += H[i] << (64 * (5 - i))
    if formato == "hex":
        return int2hex(resultado, 96, "")
    if formato == "bin":
        return int2bin(resultado, 384, "")
    if formato == "int":
        return resultado
    return None

def sha512(ms, formato="hex"):
    """
    Retorna el digest del mensaje de entrada, aplicando SHA-512

    :param ms: Mensaje de entrada (bytes)
    :param formato: Formato de la salida: 'hex' (string), 'bin' (string) o 'int' (entero)
    :return: El digest resultante
    """
    # Leemos el archivo de constantes:
    with open("datos/hash.json", "rt") as fjson:
        constantes = json.load(fjson)
    # Al ser la función prácticamente igual a sha256(), solo se comentan las diferencias con esta.
    # El resto, sin comentar.
    # De entrada, los enteros aquí son Big Endian de 64 bits, y las sumas módulo 2^64.
    longitud = len(ms) * 8
    # La longitud de padding debe ser 896 bits módulo 1024 (112 bytes módulo 128)
    if len(ms) % 128 != 112:
        ms += b'\x80'
    if len(ms) % 128 == 112:
        bytes0_padding = 0
    elif len(ms) % 128 < 112:
        bytes0_padding = 112 - (len(ms) % 128)
    else:
        bytes0_padding = 240 - (len(ms) % 128)  # 128 - (len(ms) % 128) + 112: los que faltan para 128, más otros 112
    ms += bytes0_padding * b'\x00'
    # El entero con la longitud del mensaje inicial es un big endian de 128 bits (16 bytes):
    long128 = int.to_bytes(longitud, 16, 'big')
    ms += long128
    # El mensaje se divide en bloques de 1024 bits (128 bytes)
    bloques = [ms[i:i+128] for i in range(0, len(ms), 128)]
    H = []
    for i in range(8):
        hexstr = constantes['SHA-512']['h'][i]  # La tabla h propia de SHA-512
        H.append(int(hexstr[2:], 16))
    K = []
    for i in range(80):  # En este caso, son 80 constantes
        hexstr = constantes['SHA-512']['k'][i]  # La tabla k propia de SHA-512
        K.append(int(hexstr[2:], 16))
    for bloque in bloques:
        M = [bloque[i:i + 8] for i in range(0, len(bloque), 8)]  # se divide el bloque en 16 trozos de 64 bits
        W = []
        for m in M:
            W.append(int.from_bytes(m, 'big'))
        for t in range(16, 80):  # En este caso, son 80 W's
            # sigma0(x) = rr(x,1) xor rr(x,8) xor shr(x,7)
            # sigma1(x) = rr(x,19) xor rr(x,61) xor shr(x,6)
            s0 = rr(W[t - 15], 1, 64) ^ rr(W[t - 15], 8, 64) ^ (W[t - 15] >> 7)
            s1 = rr(W[t - 2], 19, 64) ^ rr(W[t - 2], 61, 64) ^ (W[t - 2] >>  6)
            nextW = (s0 + W[t - 16] + s1 + W[t - 7]) % (2 ** 64)
            W.append(nextW)
        a = H[0]
        b = H[1]
        c = H[2]
        d = H[3]
        e = H[4]
        f = H[5]
        g = H[6]
        h = H[7]
        for i in range(80):  # En este caso son 80 rounds
            # SUM0(x) = rr(x,28) xor rr(x,34) xor rr(x,39)
            # SUM1(x) = rr(x,14) xor rr(x,18) xor rr(x,41)
            S1 = rr(e, 14, 64) ^ rr(e, 18, 64) ^ rr(e, 41, 64)
            ch = (e & f) ^ ((~e) & g)
            T1 = (h + S1 + ch + K[i] + W[i]) % (2 ** 64)
            S0 = rr(a, 28, 64) ^ rr(a, 34, 64) ^ rr(a, 39, 64)
            maj = (a & b) ^ (a & c) ^ (b & c)
            T2 = (S0 + maj) % (2 ** 64)
            h = g
            g = f
            f = e
            e = (d + T1) % (2 ** 64)
            d = c
            c = b
            b = a
            a = (T1 + T2) % (2 ** 64)
        H[0] = (H[0] + a) % (2 ** 64)
        H[1] = (H[1] + b) % (2 ** 64)
        H[2] = (H[2] + c) % (2 ** 64)
        H[3] = (H[3] + d) % (2 ** 64)
        H[4] = (H[4] + e) % (2 ** 64)
        H[5] = (H[5] + f) % (2 ** 64)
        H[6] = (H[6] + g) % (2 ** 64)
        H[7] = (H[7] + h) % (2 ** 64)
    resultado = 0
    for i in range(8):
        resultado += H[i] << (64 * (7 - i))
    if formato == "hex":
        return int2hex(resultado, 128, "")
    if formato == "bin":
        return int2bin(resultado, 512, "")
    if formato == "int":
        return resultado
    return None

# Funciones de las opciones de menú ************************************************************************************

def menu_generatabs():
    """Genera las tablas utilizadas por los algoritmos de hashing

    Utiliza como entrada el archivo de números primos 'datos/primos.json'. Genera los archivo 'datos/hash.json'.
    """
    # Leemos tabla de números primos:
    try:
        with open("datos/primos.json", "rt") as f:
            primos = json.load(f)
    except FileNotFoundError:
        print("Problemas abriendo archivo de números primos.")
        return
    hash_json = {'SHA-224': {}, 'SHA-256': {}, 'SHA-384': {}, 'SHA-512': {}}

    # SHA-224 y SHA-256 ************************************************************************************************
    # Enteros de 32 bits.
    hash_json['SHA-224']['h'] = []
    hash_json['SHA-224']['k'] = []
    hash_json['SHA-256']['h'] = []
    hash_json['SHA-256']['k'] = []
    # SHA-224 - h[0..7] - segundos 32 bits de la parte fraccional de las raíces cuadradas de los primos 9º a 16º:
    for i in range(8, 16):
        n = decimal.Decimal(primos[i]).sqrt()  # raíz cuadrada del primo, usamos Decimal por precisión
        n -= int(n)  # eliminamos la parte entera
        n *= 2 ** 64  # corremos la coma 64 posiciones a la derecha (en binario, no en decimal)
        n = int(n)  # descartamos ahora la parte fraccional restante, obteniendo un entero de 64 bits
        n &= 2 ** 32 - 1  # eliminamos los primeros 32 bits y nos quedamos con los segundos
        n = int2hex(n, 8)  # pasamos el entero a un string: número hexadecimal de 8 cifras (4 bytes)
        hash_json['SHA-224']['h'].append(n)
    # SHA-256 - h[0..7] - primeros 32 bits de la parte fraccional de las raíces cuadradas de los primeros 8 primos:
    for i in range(8):
        n = primos[i] ** (1/2)  # raíz cuadrada del primo
        n -= int(n)  # eliminamos la parte entera
        n *= 2 ** 32  # corremos la coma 32 posiciones a la derecha (en binario, no en decimal)
        n = int(n)  # descartamos ahora la parte fraccional restante, obteniendo el entero de 32 bits que buscamos
        n = int2hex(n, 8)  # pasamos el entero a un string: número hexadecimal de 8 cifras (4 bytes)
        hash_json['SHA-256']['h'].append(n)
    # SHA-224 y SHA-256 - k[0..63] - primeros 32 bits de parte fraccional de raíces cúbicas de los primeros 64 primos:
    for i in range(64):
        n = primos[i] ** (1/3)  # raíz cúbica del primo
        n -= int(n)  # eliminamos la parte entera
        n *= 2 ** 32  # corremos la coma 32 posiciones a la derecha (en binario, no en decimal)
        n = int (n)  # descartamos ahora la parte fraccional restante, obteniendo el entero de 32 bits que buscamos
        n = int2hex(n, 8)  # pasamos el entero a un string: número hexadecimal de 8 cifras (4 bytes)
        hash_json['SHA-224']['k'].append(n)
        hash_json['SHA-256']['k'].append(n)

    # SHA-224 y SHA-256 ************************************************************************************************
    # Enteros de 64 bits.
    hash_json['SHA-384']['h'] = []
    hash_json['SHA-384']['k'] = []
    hash_json['SHA-512']['h'] = []
    hash_json['SHA-512']['k'] = []
    # SHA-384 - h[0..7] - primeros 64 bits de la parte fraccional de las raíces cuadradas de los primos 9º a 16º:
    for i in range(8, 16):
        n = decimal.Decimal(primos[i]).sqrt()  # raíz cuadrada del primo, usamos Decimal por precisión
        n -= int(n)  # eliminamos la parte entera
        n *= 2 ** 64  # corremos la coma 64 posiciones a la derecha (en binario, no en decimal)
        n = int(n)  # descartamos ahora la parte fraccional restante, obteniendo el entero de 64 bits buscado
        n = int2hex(n, 8)  # pasamos el entero a un string: número hexadecimal de 8 cifras (4 bytes)
        hash_json['SHA-384']['h'].append(n)
    # SHA-512 - h[0..7] - primeros 64 bits de la parte fraccional de las raíces cuadradas de los primeros 8 primos:
    for i in range(8):
        n = decimal.Decimal(primos[i]).sqrt()  # raíz cuadrada del primo, Decimal para precisión
        n -= int(n)  # eliminamos la parte entera
        n *= 2 ** 64  # corremos la coma 64 posiciones a la derecha (en binario, no en decimal)
        n = int(n)  # descartamos ahora la parte fraccional restante, obteniendo el entero de 64 bits que buscamos
        n = int2hex(n, 8)  # pasamos el entero a un string: número hexadecimal de 8 cifras (4 bytes)
        hash_json['SHA-512']['h'].append(n)
    # SHA-384 y SHA-512 - k[0..79] - primeros 64 bits de parte fraccional de raíces cúbicas de los primeros 80 primos:
    for i in range(80):
        exponente = decimal.Decimal(1) / decimal.Decimal(3)
        n = decimal.Decimal(primos[i]).__pow__(exponente)  # raíz cúbica primo, Decimal para precisión
        n -= int(n)  # eliminamos la parte entera
        n *= 2 ** 64  # corremos la coma 64 posiciones a la derecha (en binario, no en decimal)
        n = int (n)  # descartamos ahora la parte fraccional restante, obteniendo el entero de 64 bits que buscamos
        n = int2hex(n, 8)  # pasamos el entero a un string: número hexadecimal de 8 cifras (4 bytes)
        hash_json['SHA-384']['k'].append(n)
        hash_json['SHA-512']['k'].append(n)

    # Guardamos tablas:
    with open("datos/hash.json", "wt") as f:
        json.dump(hash_json, f, indent=4)
    print("Hecho.")

def menu_sha2_string():
    """Solicita string y calcula sus hashes SHA-2 (SHA-224, SHA-256, SHA-384 y SHA-512)"""
    ms = input("Introduce cualquier texto: ")
    digest = sha224(bytes(ms, "utf-8"), "hex")
    print("SHA-224:\n   ", digest)
    digest = sha256(bytes(ms, "utf-8"), "hex")
    print("SHA-256:\n   ", digest)
    digest = sha384(bytes(ms, "utf-8"), "hex")
    print("SHA-384:\n   ", digest)
    digest = sha512(bytes(ms, "utf-8"), "hex")
    print("SHA-512:\n   ", digest)

def menu_sha2_file():
    """Solicita nombre de archivo y calcula sus hashes SHA-2 (SHA-224, SHA-256, SHA-384 y SHA-512)"""
    archivos = os.listdir(".")
    arfiles = []
    for archivo in archivos:
        if os.path.isfile(archivo):
            arfiles.append(archivo)
    print("Archivos del directorio actual:")
    for arfile in arfiles:
        print(arfile)
    arch = input("Archivo (ruta relativa o absoluta): ")
    try:
        with open(arch, "rb") as f:
            ms = f.read()
    except FileNotFoundError:
        print("Archivo no encontrado.")
        return
    digest = sha224(ms, "hex")
    print("SHA-224:\n   ", digest)
    digest = sha256(ms, "hex")
    print("SHA-256:\n   ", digest)
    digest = sha384(ms, "hex")
    print("SHA-384:\n   ", digest)
    digest = sha512(ms, "hex")
    print("SHA-512:\n   ", digest)

# Menu *****************************************************************************************************************

opciones_menu = (
    ("Genera tablas", menu_generatabs),
    ("Hashes SHA-2 de un string", menu_sha2_string),
    ("Hashes SHA-2 de un archivo", menu_sha2_file)
)

# Programa *************************************************************************************************************

if __name__ == '__main__':  # no ejecutaremos menú si el archivo ha sido importado
    # Bucle principal:
    utils.menu(opciones_menu)
