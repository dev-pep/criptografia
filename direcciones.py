#!/usr/bin/env python3

# Funciones para generar las direcciones de las cuentas de varias criptomonedas a partir de
# las claves pública y/o privada. Son las direcciones del nodo maestro (m).

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
        checksum = keccak256(bytes(aux, "utf-8"), "bin")
        for i in range(40):
            if checksum[i * 4] == "1":
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

# Funciones de las opciones de menú ************************************************************************************

def menu_dirs():
    """Opción de menú para mostrar ejemplos de direcciones"""
    # Obtenemos semilla:
    semilla = bip32.input_seed()
    # Generamos nodo:
    master = bip32.seed2master(semilla, forcelen=64)
    # Extraemos sus claves:
    k = master.k  # clave privada
    K = (master.K["x"] << 256) | master.K["y"]  # clave pública
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

# Menu *****************************************************************************************************************

opciones_menu = (
    ("Direcciones a partir de una seed", menu_dirs),
)

# Programa *************************************************************************************************************

if __name__ == '__main__':  # no ejecutaremos menú si el archivo ha sido importado
    # Bucle principal:
    utils.menu(opciones_menu)
