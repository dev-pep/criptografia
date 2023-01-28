#!/usr/bin/env python3

# Funciones útiles para otros scripts.

def menu(opciones):
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

def input_int(ms, vals, default=None):
    # vals puede ser una lista o un range
    resul = None
    while resul not in vals:
        n = input(f'{ms}: ')
        if n == '':
            resul = default
            continue
        try:
            resul = int(n)
        except ValueError:
            continue
    return resul
