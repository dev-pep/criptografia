#!/usr/bin/env python3

# Funciones útiles para otros scripts.

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

    :param x: entero del que calcular el inverso módulo n
    :param n: módulo para el cálculo
    :return: el inverso módulo n calculado
    """
    # El resultado será un número y tal que x*y ≡ 1 (mod n)
    assert n > x
    inv = euclid_ext(n, x)[2] % n  # aplicamos %n porque el resultado retornado puede ser negativo
    try:
        assert(x * inv % n == 1)
    except AssertionError:
        # x solo tiene inverso módulo n si x y n son coprimos
        return None
    return inv

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
        resul += int.to_bytes(int1 ^ int2, 1, "big")
    return resul
