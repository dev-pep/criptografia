#!/usr/bin/env python3

# Utilidades relacionadas con el algoritmo AES.

import utils

# Funciones auxiliares *************************************************************************************************

# Funciones de las opciones de menú ************************************************************************************

# Menu *****************************************************************************************************************

opciones_menu = (
    ("Primera opción de menú", None),
    ("Segunda opción de menú", None)
)

# Programa *************************************************************************************************************

if __name__ == '__main__':  # no ejecutaremos menú si el archivo ha sido importado
    # Bucle principal:
    utils.menu(opciones_menu)
