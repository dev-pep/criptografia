#!/usr/bin/env python3

# Algoritmos de hashing RIPEMD, específicamente RIPEMD-160.

import os
import utils

# Variables globales ***************************************************************************************************

# Cantidad de puestos a rotar, según j:
s = [
    11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8,
    7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12,
    11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5,
    11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12,
    9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6
]

# s prima:
sp = [
    8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6,
    9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11,
    9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5,
    15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8,
    8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11
]

# Número de bloque a usar (0..15) según j (0..79):
r = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
    7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8,
    3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12,
    1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2,
    4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13
]

# r prima:
rp = [
    5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12,
    6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2,
    15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13,
    8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14,
    12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11
]

# Funciones auxiliares *************************************************************************************************

def k(numero, prima):
    """Retorna un valor de los vectores K o K'

    :param numero: número de índice
    :param prima: indica si retornar el valor de K o de K'
    :return: valor adecuado (prima o no) con tras corrección del índice
    """
    k_vals = [0x00000000, 0x5a827999, 0x6ed9eba1, 0x8f1bbcdc, 0xa953fd4e]  # K
    kp_vals = [0x50a28be6, 0x5c4dd124, 0x6d703ef3, 0x7a6d76e9, 0x00000000]  # K' (K prima)
    if prima:
        return kp_vals[numero // 16]
    else:
        return k_vals[numero // 16]

def func_f(j, x, y, z):
    """Función para barajar los bits de los argumentos de entrada x, y, z

    :param j: según j la función retornará una cosa u otra
    :param x: primer parámetro (int)
    :param y: segundo parámetro (int)
    :param z: tercer parámetro (int)
    :return: resultado a retornar (int)
    """
    if j < 16:
        return x ^ y ^ z
    if j < 32:
        return (x & y) | (~x & z)
    if j < 48:
        return (x | ~y) ^ z
    if j < 64:
        return (x & z) | (y & ~z)
    return x ^ (y | ~z)

def ripemd160(ms, formato="hex"):
    """Retorna el digest del mensaje de entrada, aplicando RIPEMD-160

    :param ms: Mensaje de entrada (bytes)
    :param formato: Formato de la salida: 'hex' (string), 'bin' (string), 'bytes' (bytes) o 'int' (entero)
    :return: El digest resultante
    """
    # Se asume que el mensaje tiene una longitud en bits múltiplo de 8 (porque la entrada es en bytes).
    # Los enteros aquí son Little Endian (!) de 32 bits, y las sumas, módulo 2^32.
    global s, sp, r, rp
    longitud = len(ms) * 8  # longitud en bits del mensaje inicial
    # La longitud de bits tras el padding debe ser de 448 bits módulo 512 (56 bytes módulo 64)
    ms += b'\x80'  # es obligatorio 1 bit '1', con lo que también los 7 '0' correspondientes
    if len(ms) % 64 == 56:
        bytes0_padding = 0
    elif len(ms) % 64 < 56:
        bytes0_padding = 56 - (len(ms) % 64)
    else:
        bytes0_padding = 120 - (len(ms) % 64)  # 64 - (len(ms) % 64) + 56: los que faltan para 64, más otros 56
    ms += bytes0_padding * b'\x00'
    # El entero con la longitud del mensaje inicial es un big endian de 64 bits (8 bytes):
    long64 = longitud.to_bytes(8, "little")
    ms += long64
    # El mensaje se divide en bloques de 512 bits (64 bytes)
    bloques = [ms[i:i+64] for i in range(0, len(ms), 64)]
    # Inicializamos h:
    h = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0]
    for bloque in bloques:
        # El bloque se divide en 16 palabras de 32 bits (4 bytes) little indian:
        words = [int.from_bytes(bloque[i:i + 4], "little") for i in range(0, 64, 4)]
        A, B, C, D, E = Ap, Bp, Cp, Dp, Ep = h
        for j in range(80):   # 5 rondas de 16 iteraciones
            # A - E:
            T = (A + func_f(j, B, C, D) + words[r[j]] + k(j, False)) % 0x100000000
            T = (utils.lr(T, s[j], 32) + E) % 0x100000000
            A = E
            E = D
            D = utils.lr(C, 10, 32)
            C = B
            B = T
            # A' - E':
            T = (Ap + func_f(79 - j, Bp, Cp, Dp) + words[rp[j]] + k(j, True)) % 0x100000000
            T = (utils.lr(T, sp[j], 32) + Ep) % 0x100000000
            Ap = Ep
            Ep = Dp
            Dp = utils.lr(Cp, 10, 32)
            Cp = Bp
            Bp = T
        T = (h[1] + C + Dp) % 0x100000000
        h[1] = (h[2] + D + Ep) % 0x100000000
        h[2] = (h[3] + E + Ap) % 0x100000000
        h[3] = (h[4] + A + Bp) % 0x100000000
        h[4] = (h[0] + B + Cp) % 0x100000000
        h[0] = T
    # Listo. El resultado está en h[0..4]; recordemos que los enteros deben representarse en little endian:
    resultado = b""
    for elemento in h:
        resultado += elemento.to_bytes(4, "little")
    if formato == "bytes":
        return resultado
    # Lo pasaremos a entero, manteniendo el orden de bytes little indian:
    resultado = int.from_bytes(resultado, "big")
    if formato == "hex":
        return utils.int2hex(resultado, 40, "")
    if formato == "bin":
        return utils.int2bin(resultado, 160, "")
    if formato == "int":
        return resultado
    return None

# Funciones de las opciones de menú ************************************************************************************

def menu_ripemd_string():
    """Solicita string y calcula su hash RIPEMD-160"""
    ms = input("Introduce cualquier texto: ")
    digest = ripemd160(bytes(ms, "utf-8"), "hex")
    print("RIPEMD-160:\n   ", digest)

def menu_ripemd_file():
    """Solicita nombre de archivo y calcula su hash RIPEMD-160"""
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
    digest = ripemd160(ms, "hex")
    print("RIPEMD-160:\n   ", digest)

# Menu *****************************************************************************************************************

opciones_menu = (
    ("Hash RIPEMD-160 de un string", menu_ripemd_string),
    ("Hash RIPEMD-160 de un archivo", menu_ripemd_file)
)

# Programa *************************************************************************************************************

if __name__ == '__main__':  # no ejecutaremos menú si el archivo ha sido importado
    # Bucle principal:
    utils.menu(opciones_menu)
