#!/usr/bin/env python3

# Funciones para generar las direcciones de las cuentas de varias criptomonedas a partir de
# las claves pública y/o privada. Son las direcciones del nodo maestro (m).

import ce
import bip32
import sha2_hashing
import ripemd_hashing
import utils
from Cryptodome.Hash import keccak

# Funciones auxiliares *************************************************************************************************

def keccak256(ms, formato="hex"):
    """Retorna el digest del mensaje de entrada, aplicando Keccak-256

    :param ms: Mensaje de entrada (bytes o str)
    :param formato: Formato de la salida: 'hex' (string), 'bin' (string), 'bytes' (bytes) o 'int' (entero)
    :return: El digest resultante
    """
    # Primero nos aseguraremos de que el mensaje está en bytes:
    if isinstance(ms, str):
        ms = bytes(ms, "utf-8")
    assert isinstance(ms, bytes)
    k = keccak.new(digest_bits=256)
    k.update(ms)
    # Formateamos el resultado y lo retornamos:
    if formato == "hex":
        return k.hexdigest()
    if formato == "bytes":
        return k.digest()
    if formato == "int":
        return int.from_bytes(k.digest(), "big")
    if formato == "bin":
        return bin(int.from_bytes(k.digest(), "big"))[2:]
    return None

def ethereum_dir(clave, checksummed=True):
    """Retorna la dirección ethereum a partir de la clave pública

    :param clave: clave pública (int)
    :param checksummed: si es True, se le aplicará el checksum de mayúsculas (bool)
    :return: la dirección (str)
    """
    digest = keccak256(int.to_bytes(clave, 64, "big"), "int")
    digest = digest & (2 ** 160 - 1)    # solo nos interesan los últimos 160 bits
    aux = utils.int2hex(digest, 40, "")  # dirección sin checksum
    if checksummed:
        resul = ""
        checksum = keccak256(bytes(aux, "utf-8"), "int")
        checksum = utils.int2hex(checksum, 64, "")  # son 32 bytes, y por tanto 64 caracteres hexadecimales
        for i in range(40):
            if int(checksum[i], 16) >= 8:
                resul += aux[i].upper()
            else:
                resul += aux[i]
    else:
        resul = aux
    return "0x" + resul

def bitcoin_privada(clave, prefijo=b"\x80", compressed=True):
    """Genera la dirección privada WIF (Wallet Input Format), comprimida o no comprimida, a partir de la clave recibida

    :param clave: clave privada (int)
    :param prefijo: depende de la moneda (bytes): bitcoin 0x80, litecoin 0xb0, etc.
    :param compressed: si es True, generará la dirección WIF compressed; si no, la WIF uncompressed (bool)
    :return: la dirección resultante (str)
    """
    clave = prefijo + clave.to_bytes(32, "big")
    if compressed:
        clave += b"\x01"
    return utils.to_base58(clave, formato="str", check=True)

def bitcoin_publica(clave, prefijo=b"\x00", compressed=True):
    """Genera la dirección pública, comprimida o no comprimida, a partir de la clave recibida

    :param clave: clave pública (int)
    :param prefijo: depende de la moneda (bytes): bitcoin 0x00, litecoin 0x30, etc.
    :param compressed: si es True, generará la dirección compressed; si no, la uncompressed (bool)
    :return: la dirección resultante (str)
    """
    clave = clave.to_bytes(64, "big")
    if compressed:
        # Miramos último byte de coordenada y para ver si es par o impar:
        last = clave[-1]
        if last & 1:
            prefi = b"\x03"
        else:
            prefi = b"\x02"
        clave = prefi + clave[:32]
    else:
        clave = b"\x04" + clave
    # Primera tanda de hashes:
    clave = ripemd_hashing.ripemd160(sha2_hashing.sha256(clave, "bytes"), "bytes")
    # Añadimos prefijo de la moneda:
    clave = prefijo + clave
    # Ahora le aplicamos un Base58Check:
    return utils.to_base58(clave, formato="str", check=True)

def genera_dirs(k):
    """Genera las direcciones a partir de la clave privada indicada

    :param k: clave privada (int)
    """
    # Utilizaremos una curva elíptica para calcular la clave pública a partir de la privada:
    curva = ce.Curva("secp256k1")
    publica = curva.k_g(k)  # par de enteros (x,y)
    K = (publica["x"] << 256) | publica["y"]  # clave pública
    # General:
    print("\nGENERAL:")
    print(f"Clave privada: {hex(k)[2:]}")
    print(f"Clave pública: {hex(K)[2:]}")
    # Bitcoin:
    print("\nBITCOIN:")
    wif_priv_uncompressed = bitcoin_privada(k, compressed=False)
    print("WIF privada uncompressed:", wif_priv_uncompressed)
    wif_priv_compressed = bitcoin_privada(k, compressed=True)
    print("WIF privada compressed:", wif_priv_compressed)
    wif_pub_uncompressed = bitcoin_publica(K, compressed=False)
    print("Dirección uncompressed:", wif_pub_uncompressed)
    wif_pub_compressed = bitcoin_publica(K, compressed=True)
    print("Dirección compressed:", wif_pub_compressed)
    # Ethereum:
    print("\nETHEREUM:")
    dir_ethereum = ethereum_dir(K)
    print("Dirección:", dir_ethereum)

# Funciones de las opciones de menú ************************************************************************************

def menu_dirs_seed():
    """Opción de menú para mostrar ejemplos de direcciones a partir de una semilla"""
    # Obtenemos semilla:
    semilla = bip32.input_seed()
    # Generamos nodo maestro:
    master = bip32.seed2master(semilla, forcelen=64)
    # Extraemos su clave privada y la pasamos al generador de direcciones:
    genera_dirs(master.k)

def menu_dirs_k():
    """Opción de menú para mostrar ejemplos de direcciones a partir de una clave privada"""
    clave = input("Introduce clave privada: entero decimal/hexadecimal, o clave extendida (en base-58): ").strip()
    if clave.isnumeric():  # entero decimal
        k = int(clave)
    elif clave[:4] in ["xprv", "xpub", "tprv", "tpub"]:  # clave extendida (base-58)
        k = int(bip32.key_info(clave, True)["clave"], 16)
    else:  # entero hexadecimal
        k = int(clave, 16)
    genera_dirs(k)

# Menu *****************************************************************************************************************

opciones_menu = (
    ("Direcciones a partir de una seed", menu_dirs_seed),
    ("Direcciones a partir de una clave privada", menu_dirs_k),
)

# Programa *************************************************************************************************************

if __name__ == '__main__':  # no ejecutaremos menú si el archivo ha sido importado
    # Bucle principal:
    utils.menu(opciones_menu)
