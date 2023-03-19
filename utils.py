#!/usr/bin/env python3

# Funciones útiles para otros scripts.

import random
import primos
import sha2_hashing


# Menú principal *******************************************************************************************************

def menu(opciones):
    """Pinta el menú de opciones (recible tupla de tuplas ("opción", función)), solicita opción y ejecuta la adecuada

    :param opciones: tupla con el menú
    """
    accion = ''
    while accion != 'X':
        # Pinta el menú:
        maxlen = 0
        for opcion in opciones:
            if len(opcion[0]) > maxlen:
                maxlen = len(opcion[0])
        print('╔' + (6 + maxlen) * '═' + '╗')
        for i in range(len(opciones)):
            relleno = maxlen - len(opciones[i][0]) + 1
            print(f'║ {i + 1:2}. {opciones[i][0]}' + relleno * ' ' + '║')
        print('║  X. Salir' + (maxlen - 4) * ' ' + '║')
        print('╚' + (6 + maxlen) * '═' + '╝')
        # Solicita acción:
        try:
            accion = input('Introduce opción: ').upper()
            if accion == 'X':
                continue
            try:
                numAccion = int(accion)
                if numAccion < 1 or numAccion > len(opciones):
                    raise ValueError
            except ValueError:
                print('Opción no válida.')
                continue
            opciones[numAccion - 1][1]()
        except KeyboardInterrupt:
            print("\nAbandonando aplicación...")
            accion = 'X'

# Entrada de datos *****************************************************************************************************

def input_int(ms, vals=None, default=None):
    """Solicita un número entero, y lo retorna

    :param ms: Mensaje del prompt
    :param vals: Valores aceptados: lista, range, o None (no comprobar)
    :param default: Valor a retornar si solo se pulsa Intro
    :return: el número entero introducido
    """
    resul = None
    ok = False
    while not ok:
        n = input(f"{ms}: ")
        if n == '':
            return default
        try:
            resul = int(n)
            ok = True
        except ValueError:
            continue
        if vals and resul not in vals:
            ok = False
    return resul

def input_bool(ms, default):
    """Solicita un booleano (sí,no), y lo retorna

    :param ms: Mensaje del prompt
    :param default: Valor por defecto, si solo se presiona Intro (booleano)
    :return: el booleano introducido
    """
    b = input(f"{ms} (s/n): ")
    if b == "":
        return default
    if b.upper() in ["S", "SI", "SÍ"]:
        return True
    return False

# Funciones matemáticas ***********************************************************************************************

def mcd(x, y):
    """Calcula el máximo común divisor de dos enteros mediante el algoritmo de Euclides

    :param x: primer entero
    :param y: segundo entero
    :return: máximo común divisor de los dos enteros
    """
    r = x % y
    while r:  # mientras el resto no sea 0
        x = y
        y = r
        r = x % y
    return y

def mcm(x, y):
    """Calcula el mínimo común múltiplo de dos enteros usando el algoritmo de Euclides para encontrar antes el mcd

    :param x: primer entero
    :param y: segundo entero
    :return: mínimo común múltiplo de los dos enteros
    """
    return abs(x * y) // mcd(x, y)

def euclid_ext(x, y):
    """Calcula el mcd y los factores de Bezout de dos enteros mediante el algoritmo extendido de Euclides

    :param x: primer entero
    :param y: segundo entero
    :return: máximo común divisor de los dos enteros, así como los coeficientes de Bezout (mcd, s, t)
    """
    # Buscaremos el mcd, así como los coeficientes s y t de la identidad de Bezout: mcd = s*x + t*y para algún x, y.
    # Para ello usaremos 4 series de datos:
    q = [None, None]  # cocientes, q0 y q1 no se usan
    r = [x, y]  # restos
    s = [1, 0]  # coeficientes s
    t = [0, 1]  # coeficientes t
    while r[-1]:  # mientras el último elemento de r no sea 0
        new_q = r[-2] // r[-1]
        new_r = r[-2] - new_q * r[-1]
        new_s = s[-2] - new_q * s[-1]
        new_t = t[-2] - new_q * t[-1]
        q.append(new_q)
        r.append(new_r)
        s.append(new_s)
        t.append(new_t)
    # Ya tenemos el resultado. Si lo usamos para encontrar el inverso módulo n, es decir, si buscamos
    # un número t tal que: ta ≡ 1 (mod n), mediante 1 = sn + ta, la respuesta es t[-2] (mod n). Al llamar a
    # esta función debemos tener en cuenta que si buscamos el inverso multiplicativo, tendremos que aplicarle
    # (módulo x) a ese t[-2], ya que este podría ser negativo.
    return r[-2], s[-2], t[-2]

def inverso_modn(x, n):
    """Calcula el inverso multiplicativo módulo n del entero x

    Utiliza el algoritmo de Euclides extendido, euclid_ext().

    :param x: entero distinto de 0 del que calcular el inverso módulo n
    :param n: módulo para el cálculo
    :return: el inverso módulo n calculado
    """
    # El resultado será un número y tal que x*y ≡ 1 (mod n).
    # Aplicamos primero módulo n a la entrada:
    x = x % n
    assert x != 0
    inv = euclid_ext(n, x)[2] % n  # aplicamos %n porque el resultado retornado puede ser negativo
    try:
        assert (x * inv) % n == 1
    except AssertionError:
        # x solo tiene inverso módulo n si x y n son coprimos
        return None
    return inv

def sqrt_mod(n, p):
    """ Calcula la raíz cuadrada del número n, módulo p, usando el algoritmo Tonelli–Shanks

    :param n: número del que calcular la raíz cuadrada (si no es mod p, se le aplicará al principio mod p)
    :param p: módulo (debe ser primo, mayor que 2)
    :return: las dos raíces (r1, r2), (0, None) si n=0, o (None, None) si no hay solución
    """
    if n == 0:
        return 0, None
    n = n % p
    if not primos.es_primo_mr(p, 10) or p <= 2:
        return None, None
    test = pow(n, (p - 1) // 2, p)    # tiene solución si da 1; si da -1 (o sea m-1) no (criterio de Euler)
    if test == p - 1:
        return None, None
    assert test == 1    # si no era -1, tiene que ser 1 (tiene solución)
    # Hallemos la solución. Primero calculamos Q y S tal que p-1 = Q * 2^S:
    Q = (p - 1) // 2
    S = 1
    while Q % 2 == 0:
        Q //= 2
        S += 1
    # Buscamos un entero z que no sea un residuo cuadrático (o sea, que no tenga raíz cuadrada módulo p):
    test = 1
    while test != p - 1:
        z = random.randint(2, p - 1)
        test = pow(z, (p - 1) // 2, p)    # criterio de Euler nuevamente
    M = S
    c = pow(z, Q, p)
    t = pow(n, Q, p)
    R = pow(n, (Q + 1) // 2, p)
    while True:
        if t == 0:
            r = 0
            break
        if t == 1:
            r = R
            break
        for i in range(1, M):
            if pow(t, 2 ** i, p) == 1:
                break
        assert pow(t, 2 ** i, p) == 1
        b = pow(c, 2 ** (M - i - 1), p)
        M = i
        c = (b ** 2) % p
        t = (t * b ** 2) % p
        R = (R * b) % p
    return r, p - r

# Bytes y enteros ******************************************************************************************************

def lr(entero, n, ancho):
    """
    Left rotation, rotación cíclica de bits a la izquierda

    :param entero:   El entero a rotar
    :param n:        Cuántos bits hay que rotar
    :param ancho:    Cuántos bits componen el entero
    :return: El entero rotado
    """
    assert(entero < 2 ** ancho)
    return (entero << n | entero >> (ancho - n)) & (2 ** ancho - 1)

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

def xor(b1, b2):
    """Calcula el xor de dos secuencias de bytes y lo retorna, también como bytes

    :param b1: primera secuencia bytes
    :param b2: segunda secuencia bytes
    :return: resultado, también bytes
    """
    # Tanto b1 como b2 deben tener la misma longitud en bytes; el resultado también lo tendrá
    assert(len(b1) == len(b2))
    resul = b''
    for i in range(len(b1)):
        int1 = b1[i]
        int2 = b2[i]
        resul += (int1 ^ int2).to_bytes(1, "big")
    return resul

def int2bytes(entero, bigendian=True):
    """Convierte un entero a bytes, sin tener que indicar longitud

    :param entero: entero a convertir
    :param bigendian: True indica Big Endian; False Little Endian
    :return: secuencia bytes resultante
    """
    resul = b""
    while entero:
        nextbyte = (entero & 0xff).to_bytes(1, "big")
        if bigendian:
            resul = nextbyte + resul
        else:
            resul += nextbyte
        entero >>= 8
    return resul

def bytes_reverse(b):
    """Retorna una secuencia de bytes en el orden inverso

    :param b: secuencia de bytes
    :return: secuencia invertida resultante (bytes)
    """
    return b[-1:0:-1] + b[0:1]

def int_reverse_bytes(i, n):
    """Retorna un entero con la endianness invertida a nivel de bytes

    :param i: entero a invertir
    :param n: número de bytes que componen el entero (int)
    :return: resultado (entero) invertido
    """
    bi = i.to_bytes(n, "big")
    return int.from_bytes(bi, "little")

# Base-64 y Base-58 ****************************************************************************************************

def to_base64(entero):
    """Convierte un entero o secuencia de bytes en una secuencia de bytes codificada en base64

    :param entero: entero o bytes a convertir
    :return: secuencia resultante
    """
    tabla = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    if isinstance(entero, int):
        entero = int2bytes(entero)
    # El entero ya es una secuencia de bytes.
    resul = b""
    while len(entero):
        if len(entero) >= 3:  # cada 3 bytes de entrada serán 4 bytes de 6 bits en la salida
            fragmento = int.from_bytes(entero[:3], "big")
            padding = b""
            entero = entero[3:]
            outbytes = 4
        elif len(entero) == 2:  # con 2 bytes de entrada serán 3 bytes de 6 bits en la salida, y padding "="
            fragmento = int.from_bytes(entero, "big")
            fragmento <<= 2  # 2*8+2=3*6
            padding = b"="
            entero = b""
            outbytes = 3
        elif len(entero) == 1:  # con 1 byte de entrada serán 2 bytes de 6 bits en la salida, y padding "="
            fragmento = int.from_bytes(entero, "big")
            fragmento <<= 4  # 1*8+4=2*6
            padding = b"=="
            entero = b""
            outbytes = 2
        # Construimos el nuevo fragmento
        newchunk = b""
        for i in range(outbytes):
            newchunk = tabla[fragmento & 0x3f].to_bytes(1, "big") + newchunk
            fragmento >>= 6
        resul += newchunk + padding
    return resul

def from_base64(ms, formato="hex"):
    """Decodifica una secuencia de bytes o string (utf-8) en base 64 a entero

    :param ms: mensaje a decodificar (bytes o string)
    :param formato: formato de salida "int" (entero), "hex" (string) o "bytes" (bytes)
    :return: el mensaje decodificado
    """
    tabla = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    if len(ms) % 4 != 0:  # un mensaje base64 tiene siempre una longitud múltiplo de 4 caracteres
        return None
    if isinstance(ms, str):
        ms = ms.encode("utf-8")
    # Ya tenemos el mensaje ms en una secuencia bytes; vamos a pasar a índices de la tabla:
    aux = ms
    ms = b""
    for b in aux:
        if b == 61:  # código de b"="
            ms += b"="
        else:
            ms += tabla.find(b).to_bytes(1, "big")
    # Ya están pasados a índices los bytes; procedamos a la decodificación:
    resul = b""
    while len(ms):
        fragmento = ms[:4]
        ms = ms[4:]
        if fragmento.endswith(b"=="):  # hay 1 byte
            byte1 = ((fragmento[0] << 2) | (fragmento[1] >> 4)).to_bytes(1, "big")
            fragmento = byte1
        elif fragmento.endswith(b"="):  # hay 2 bytes
            byte1 = ((fragmento[0] << 2) | (fragmento[1] >> 4)).to_bytes(1, "big")
            byte2 = ((fragmento[1] << 4) & 0xff | (fragmento[2] >> 2)).to_bytes(1, "big")
            fragmento = byte1 + byte2
        else:  # hay 3 bytes
            byte1 = ((fragmento[0] << 2) | (fragmento[1] >> 4)).to_bytes(1, "big")
            byte2 = ((fragmento[1] << 4) & 0xff | (fragmento[2] >> 2)).to_bytes(1, "big")
            byte3 = ((fragmento[2] << 6) & 0xff | fragmento[3]).to_bytes(1, "big")
            fragmento = byte1 + byte2 + byte3
        resul += fragmento
    if formato == "bytes":
        return resul
    if formato == "int":
        return int.from_bytes(resul, "big")
    return hex(int.from_bytes(resul, "big"))[2:]

def to_base58(entero, formato="bytes", check=False):
    """Convierte un entero o secuencia de bytes en una secuencia de bytes codificada en base58

    Base58 se hizo para generar direcciones Bitcoin, eliminando los caracteres "+/lI0O" de base64.
    :param entero: entero o bytes a convertir
    :param formato: indica el formato de salida: "str" o "bytes"
    :param check: si es True, aplica la versión con checksum, llamada Base58Check (bool)
    :return: secuencia resultante (bytes o str)
    """
    tabla = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    prefix = b""
    # Si es la versión check, lo debemos tener primero en bytes:
    if check:
        if isinstance(entero, int):
            entero = int2bytes(entero)
        checksum = sha2_hashing.sha256(sha2_hashing.sha256(entero, formato="bytes"), formato="bytes")[:4]
        entero += checksum
    if isinstance(entero, bytes):
        # Los leading zeroes se deben traducir al final como 1's:
        i = 0
        while entero[i] == 0:
            prefix += b"1"
            i += 1
        # Convertimos los bytes a entero:
        entero = int.from_bytes(entero, "big")
    # Ya tenemos el entero como tal, y el prefijo de unos que aplicaremos al final. Empecemos la codificación:
    resul = b""
    while entero:
        resul = tabla[entero % 58].to_bytes(1, "big") + resul
        entero //= 58
    resul = prefix + resul
    if formato == "str":
        return resul.decode("utf-8")
    return resul

def from_base58(ent_bytes, formato="int", check=False):
    """Convierte una secuencia de bytes codificada en base58 en un entero

    Base58 se hizo para generar direcciones Bitcoin, eliminando los caracteres "+/lI0O" de base64.
    :param ent_bytes: secuencia de bytes a decodificar (bytes)
    :param formato: formato de salida "int" (entero), "bytes" (bytes) o "hex" (string)
    :param check: si es True, tras descodificar eliminaremos los 4 últimos bytes (32 bits) del checksum (bool)
    :return: el mensaje decodificado
    """
    tabla = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    resul = 0
    for b in ent_bytes:
        numero = tabla.find(b)
        resul = resul * 58 + numero
    # Si es la versión check, tras la decodificación chequeamos los 32 últimos bits y los eliminamos del resultado:
    if check:
        checksum1 = (resul & 0xffffffff).to_bytes(4, "big")
        resul >>= 32
        checksum2 = sha2_hashing.sha256(sha2_hashing.sha256(int2bytes(resul), "bytes"), "bytes")[:4]
        assert checksum1 == checksum2, "El checksum no coincide"
    if formato == "int":
        return resul
    if formato == "bytes":
        return int2bytes(resul)
    return hex(resul)[2:]
