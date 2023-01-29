#!/usr/bin/env python3

# Utilidades relacionadas con la obtención de claves RSA.

import random
import utils

# Funciones auxiliares *************************************************************************************************

# Funciones de las opciones de menú ************************************************************************************

# Menu *****************************************************************************************************************

opciones_menu = (
    ("Primera opción de menú", None),
    ("Segunda opción de menú", None)
)

# Programa *************************************************************************************************************

# Bucle principal:
accion = utils.menu(opciones_menu)
while accion:
    accion()
    accion = utils.menu(opciones_menu)
