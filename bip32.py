#!/usr/bin/env python3

# Utilidades relacionadas con la generación de monederos jerárquicos determinísticos (HDW), BIP-32.
# https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki

import bip39
import ce
import ripemd_hashing
import sha2_hashing
import utils

# Variables globales ***************************************************************************************************

curva = ce.Curva("secp256k1")

# Clase nodo ***********************************************************************************************************

class Nodo:
    """Clase que define un nodo del árbol"""

    def __init__(self, clave, c, path, parent_fp, mainnet=True):
        """Inicializa los valores del nodo

        :param clave: clave privada (int) o pública (dict)
        :param c: chain code (bytes)
        :param path: ruta de derivación (derivation path, string); ejemplos: m, m/1/0, m/1'/0/5
        :param parent_fp: fingerprint del padre (bytes)
        :param mainnet: si es True, será de la red principal; si no, de la red de prueba
        """
        # Inicialización inicial de elementos:
        self.c, self.path, self.parent_fp, self.mainnet = c, path, parent_fp, mainnet
        # Veamos si 'clave' es pública o privada:
        if isinstance(clave, dict):
            # Es pública:
            self.k = 0  # Este nodo no dispondrá de clave privada
            self.K = clave
        else:
            # Es privada:
            self.k = clave
            # Calcularemos la clave pública según la clave privada:
            self.K = curva.k_g(self.k)
        # Calcularemos el nivel según el número de elementos de la ruta:
        ruta = self.path.split('/')
        self.depth = len(ruta) - 1
        # Calcularemos el número de hijo según el último elemento de la ruta:
        nhijo = ruta[-1]
        if nhijo == "m":  # ¿es el nodo maestro?
            self.i = 0
        elif nhijo[-1] == "'":  # ¿hardened index?
            assert self.k    # si es hardened, debemos tener clave privada
            self.i = int(nhijo[:-1]) + 0x80000000  # + 2^31
        else:
            self.i = int(nhijo)
        # Calcularemos el fingerprint del nodo, que es el Hash160 de la clave pública serializada:
        # Serializamos la clave pública:
        if self.K["y"] & 1:  # ¿impar?
            K_serializada = b"\x03" + self.K["x"].to_bytes(32, "big")
        else:
            K_serializada = b"\x02" + self.K["x"].to_bytes(32, "big")
        # Ahora aplicamos el Hash160 = RIPEMD160(SHA-256):
        fingerprint = ripemd_hashing.ripemd160(sha2_hashing.sha256(K_serializada, "bytes"), "bytes")
        self.fp = fingerprint[:4]

    def info(self):
        """Muestra en pantalla los datos del nodo"""
        print(f"Información del nodo {self.path}")
        if self.k:
            print("Clave privada:")
            print(f"    hex: {hex(self.k)[2:]}")
            print(f"    ext: {self.ext_key(public=False)}")
        else:
            print("Este nodo no dispone de clave privada.")
        print("Clave pública:")
        print(f"    hex: {hex(self.K['x'])[2:]}{hex(self.K['y'])[2:]}")
        print(f"    ext: {self.ext_key(public=True)}")
        print(f"Chain code: {hex(int.from_bytes(self.c, 'big'))[2:]}")
        print(f"Fingerprint: {hex(int.from_bytes(self.fp, 'big'))[2:]}")
        print(f"Parent fingerprint: {hex(int.from_bytes(self.parent_fp, 'big'))[2:]}")
        if self.i >= 0x80000000:    # 2^31
            print(f"Hijo (índice): {self.i - 0x80000000} (hardened)")
        else:
            print(f"Hijo (índice): {self.i}")
        print(f"Nivel: {self.depth}")
        if self.mainnet:
            print(f"Red principal: SÍ")
        else:
            print(f"Red principal: NO")
        print("-" * 80)

    def ext_key(self, public):
        """Retorna la clave extendida pública o privada, serializada y codificade en base-58

        :param public: si es True, retornará la pública; si no, la privada (bool)
        :return: la clave extendida solicitada, serializada y en formato base-58 (string)
        """
        if public:
            # Clave pública:
            if self.K["y"] & 1:  # ¿coordenada y es impar?
                clave_bytes = b"\x03" + self.K["x"].to_bytes(32, "big")
            else:
                clave_bytes = b"\x02" + self.K["x"].to_bytes(32, "big")
        else:
            # Clave privada:
            if not self.k:
                print("Este nodo no dispone de clave privada.")
                return None
            clave_bytes = b"\x00" + self.k.to_bytes(32, "big")
        if self.mainnet:
            if public:
                prefijo = 0x0488b21e.to_bytes(4, "big")
            else:
                prefijo = 0x0488ade4.to_bytes(4, "big")
        else:
            if public:
                prefijo = 0x043587cf.to_bytes(4, "big")
            else:
                prefijo = 0x04358394.to_bytes(4, "big")
        depth = self.depth.to_bytes(1, "big")
        childnum = self.i.to_bytes(4, "big")
        serializacion = prefijo + depth + self.parent_fp + childnum + self.c + clave_bytes
        # Antes de codificar en base-58, aplicaremos el checksum (doble hash), y tomaremos los primeros 4 bytes:
        checksum = sha2_hashing.sha256(sha2_hashing.sha256(serializacion, "bytes"), "bytes")[:4]
        # Añadimos el checksum:
        serializacion += checksum
        # Y aplicamos la codificación base-58:
        serializacion_int = int.from_bytes(serializacion, "big")
        return str(utils.to_base58(serializacion_int), "utf-8")

    def deriva(self, i, hardened):
        """Crea un hijo, derivando la clave privada extendida del nodo actual

        :param i: número de hijo (int), tal que 0 <= i < 2^31
        :param hardened: si es True, se sumará 2^31 al número de hijo (boolean)
        :return: el nodo hijo creado
        """
        if not self.k:
            print("No existe clave privada que derivar.")
            return None
        assert 0 <= i < 0x80000000
        if hardened:
            # Derivación hardened (i + 2^31)
            I = bip39.hmac_sha512(self.c, b"\x00" + self.k.to_bytes(32, "big") + (i + 0x80000000).to_bytes(4, "big"))
            hijo_sufijo = "'"
        else:
            # Derivación normal (no hardened)
            if self.K["y"] & 1:    # ¿impar?
                prefijo = b"\x03"
            else:
                prefijo = b"\x02"
            I = bip39.hmac_sha512(self.c, prefijo + self.K["x"].to_bytes(32, "big") + i.to_bytes(4, "big"))
            hijo_sufijo = ""
        IL = int.from_bytes(I[:32], "big")  # parte izquierda del resultado (int de 32 bytes)
        if IL >= curva.n:
            return None  # valor inválido; este hijo no se puede derivar
        k = (IL + self.k) % curva.n
        if k == 0:
            return None  # clave inválida; este hijo no se puede derivar
        c = I[32:]  # chain code del hijo, parte derecha de I (32 bytes)
        return Nodo(k, c, self.path + "/" + str(i) + hijo_sufijo, self.fp)

    def deriva_pub(self, i):
        """Crea un hijo, derivando la clave pública extendida del nodo actual (el hijo no dispondrá de clave privada)

        Un hijo sin clave privada no puede derivarse mediante derivación de clave privada extendida, sino solamente
        mediante derivación de clave pública extendida (esta función), con lo que todos los descendientes de este
        dispondrán únicamente de clave pública. No es posible la derivación hardened.

        :param i: número de hijo (int), tal que 0 <= i < 2^31
        :return: el nodo hijo creado
        """
        assert 0 <= i < 0x80000000
        # Primero serializamos la clave pública:
        if self.K["y"] & 1:    # ¿impar?
            prefijo = b"\x03"
        else:
            prefijo = b"\x02"
        I = bip39.hmac_sha512(self.c, prefijo + self.K["x"].to_bytes(32, "big") + i.to_bytes(4, "big"))
        IL = int.from_bytes(I[:32], "big")  # parte izquierda del resultado (int de 32 bytes)
        if IL >= curva.n:
            return None  # valor inválido; este hijo no se puede derivar
        K = curva.suma_puntos(curva.k_g(IL), self.K)
        if K["x"] == float("inf"):
            return None  # clave inválida; este hijo no se puede derivar
        c = I[32:]  # chain code del hijo, parte derecha de I (32 bytes)
        return Nodo(K, c, self.path + "/" + str(i), self.fp)

# Funciones auxiliares *************************************************************************************************

def seed2master(s, forcelen=None):
    """Genera y retorna un nodo maestro (de la mainnet) a partir de una semilla

    :param s: semilla a partir de la cual generar el nodo maestro (bytes o int)
    :param forcelen: si se especifica un número, la semilla tendrá esa longitud de bytes (None o int)
    :return: el nodo maestro (tipo Nodo) o None
    """
    if isinstance(s, int):
        seed = utils.int2bytes(s)
    else:
        seed = s
    if forcelen and forcelen > len(seed):
        seed = b"\x00" * (forcelen - len(seed)) + seed
    if len(seed) < 16 or len(seed) > 64:
        return None    # semilla con longitud errónea
    I = bip39.hmac_sha512(b"Bitcoin seed", seed)
    m = int.from_bytes(I[:32], "big")  # clave privada (int)
    if m == 0 or m >= curva.n:
        return None    # clave inválida; la semilla no sirve
    c = I[32:]  # chain code (bytes)
    return Nodo(m, c, "m", b"\x00\x00\x00\x00")

def seed_path_2node(s, ruta, forcelen=None):
    """Genera y retorna un nodo (de la mainnet) a partir de una semilla inicial y una ruta de derivación

    :param s: semilla a partir de la cual generar el nodo maestro (bytes o int)
    :param ruta: ruta de derivación para ir derivando hasta el nodo buscado (string); p.e. "m/2'/0/12"
    :param forcelen: si se especifica un número, la semilla tendrá esa longitud de bytes (None o int)
    :return: nodo resultante (o None)
    """
    nodo = seed2master(s, forcelen)
    if not nodo:
        print("Semilla no válida.")
        return nodo
    chunks = ruta.split("/")
    if chunks[0] != "m":
        print("Ruta no válida.")
    for chunk in chunks[1:]:  # sin contar el "m" inicial
        if chunk[-1] == "'":
            nodo = nodo.deriva(int(chunk[:-1]), True)
        else:
            nodo = nodo.deriva(int(chunk), False)
    return nodo

def key_info(key):
    """Recibe una clave extendida en formato Base-58 y muestra sus parámetros en pantalla

    La clave podría ser errónea. Esta función no lo detecta.

    :param key: Clave a decodificar, en formato Base-58 (bytes o str)
    """
    # Nos aseguramos que la clave está en bytes:
    if isinstance(key, str):
        key = key.encode("utf-8")
    # Decodificamos (base-58)
    key = utils.from_base58(key, "bytes")
    # Vamos a extraer los campos:
    version = hex(int.from_bytes(key[:4], "big")).lower()[2:]
    if version == "488b21e":
        version_str = "clave pública extendida, red principal"
    elif version == "488ade4":
        version_str = "clave privada extendida, red principal"
    elif version == "43587cf":
        version_str = "clave pública extendida, red de pruebas"
    elif version == "4358394":
        version_str = "clave privada extendida, red de pruebas"
    else:
        version_str = "desconocido"
    depth = key[4]
    parent_fp = int.from_bytes(key[5:9], "big")
    child = int.from_bytes(key[9:13], "big")
    c = hex(int.from_bytes(key[13:45], "big"))[2:]
    prefijo = key[45]
    clave = hex(int.from_bytes(key[46:78], "big"))[2:]
    checksum = hex(int.from_bytes(key[78:82], "big"))[2:]
    # Presentamos resultados
    print(f"Versión: {version} ({version_str})")
    print(f"Nivel: {depth}")
    print(f"Fingerprint del padre: {parent_fp}")
    print(f"Nº hijo: {child}")
    print(f"Chain code: {c}")
    print(f"Prefijo clave: {prefijo}")
    print(f"Clave: {clave}")
    print(f"Checksum: {checksum}")
    print("-" * 80)

def input_seed():
    """Espera la entrada de una seed en forma de entero decimal, hexadecimal (con o sin prefijo 0x) o seed phrase

    Si introducimos seed phrase, nos preguntará contraseña opcional.

    :return: seed (int)
    """
    entrada = input("Introduce seed (hexa o decimal), o seed phrase: ").strip()
    # Si empieza por 0x, será entero hexadecimal
    if entrada[:2] == "0x":
        try:
            seed = int(entrada[2:], 16)
        except ValueError:
            return 0
    else:
        # No empieza por 0x; veamos qué se ha introducido:
        try:
            # Intentamos entero decimal:
            seed = int(entrada)
        except ValueError:
            # No es entero decimal. Vamos a intentar entero hexadecimal:
            try:
                seed = int(entrada, 16)
            except ValueError:
                # Tampoco es entero hexadecimal. Solo puede ser una seed phrase:
                lista = bip39.string2list(entrada)
                if not lista or not bip39.check_phrase(lista):
                    return 0
                # Es una seed phrase correcta. Preguntaremos contraseña:
                password = input("Introduce contraseña (opcional): ")
                print("Calculando seed a partir de la seed phrase...")
                seed = bip39.phrase2seed(entrada, password)
    return seed

# Funciones de las opciones de menú ************************************************************************************

def menu_gen():
    """Pregunta una semilla o seed phrase, y un derivation path; luego muestra los nodos desde el maestro"""
    # Obtenemos seed:
    seed = input_seed()
    if not seed:
        print("Semilla incorrecta.")
        return
    # Obtenemos ruta (tipo m/4'/3/5'/4/0):
    ruta = input("Introduce una ruta de derivación: ").strip().split("/")
    print("Calculando...")
    ruta_tmp = ""
    for r in ruta:
        if ruta_tmp:
            ruta_tmp += "/"
        ruta_tmp += r
        nodo = seed_path_2node(seed, ruta_tmp, forcelen=64)
        nodo.info()

def menu_genpub():
    """Como menu_gen(), pero las derivaciones son de clave pública extendida solamente"""
    # Obtenemos seed:
    seed = input_seed()
    if not seed:
        print("Semilla incorrecta.")
        return
    # Obtenemos ruta (tipo m/4'/3/5'/4/0):
    ruta = input("Introduce una ruta de derivación: ").strip().split("/")
    print("Calculando...")
    nodo = seed2master(seed, forcelen=64)
    nodo.info()
    for r in ruta[1:]:
        try:
            i = int(r)
        except ValueError:
            print("Ruta incorrecta.")
            return
        nodo = nodo.deriva_pub(i)
        nodo.info()

def menu_clave():
    """Pregunta una clave extendida, en base-58, y muestra sus datos; no detecta si es incorrecta"""
    clave = input("Introduce una clave (pública o privada) extendida, codificada en base-58:\n")
    key_info(clave)

# Menu *****************************************************************************************************************

opciones_menu = (
    ("Generar árbol", menu_gen),
    ("Generar árbol con derivación pública", menu_genpub),
    ("Leer clave", menu_clave)
)

# Programa *************************************************************************************************************

if __name__ == '__main__':  # no ejecutaremos menú si el archivo ha sido importado
    # Bucle principal:
    utils.menu(opciones_menu)
