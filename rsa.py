#!/usr/bin/env python3

# Utilidades relacionadas con la obtención de claves RSA.

import random

# Funciones auxiliares *************************************************************************************************

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


def pinta_menu():
    global menu
    maxlen = 0
    for opcion in menu:
        if len(opcion[0]) > maxlen:
            maxlen = len(opcion[0])
    print('╔' + (6 + maxlen) * '═' + '╗')
    for i in range(len(menu)):
        relleno = maxlen - len(menu[i][0]) + 1
        print(f'║ {i + 1:2}. {menu[i][0]}' + relleno * ' ' + '║')
    print('║  X. Salir' + (maxlen - 4) * ' ' + '║' )
    print('╚' + (6 + maxlen) * '═' + '╝')

# Funciones de las opciones de menú ************************************************************************************

# Menu *****************************************************************************************************************

menu = (
    ("Primera opción de menú", None),
    ("Segunda opción de menú", None)
)

# Programa *************************************************************************************************************

# Bucle principal:
accion = ''
while accion != 'X':
    pinta_menu()
    accion = input('Introduce opción: ').upper()
    if accion == 'X':
        continue
    try:
        numAccion = int(accion)
        if numAccion < 1 or numAccion > len(menu):
            raise ValueError
    except ValueError:
        print('Opción no válida.')
        continue
    menu[numAccion - 1][1]()
