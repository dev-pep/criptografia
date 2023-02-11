#!/usr/bin/env python3

# Funciones útiles para otros scripts.

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
