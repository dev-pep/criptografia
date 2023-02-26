#!/usr/bin/env python3

# Utilidades relacionadas el álgebra para criptografía. Solo ofrece unas funciones auxiliares que trabajan
# con grupos de enteros.

# Funciones auxiliares *************************************************************************************************

def grupo_z_crea(n, oper, star, g=None, h=1):
    """ Retorna los elementos de un grupo de enteros

    :param n: orden del grupo
    :param oper: operador del grupo ('+' o '*')
    :param star: True si no queremos incluir el número 0 (normalmente True con multiplicación, y False con suma)
    :param g: número generador del grupo, o None para no generarlo así
    :param h: cofactor
    :return: elementos del grupo indicado
    """
    elementos = set()
    if g == 0:
        return elementos
    elif g:
        # Construiremos los elementos en base al generador g
        g = g * h  # aplicamos el cofactor
        for i in range(n):
            if oper == '+':
                elementos.add((i * g) % n)
            elif oper == '*':
                elementos.add(pow(g, i, n))
            else:
                assert False  # operación errónea
    else:
        # No hay generador
        for i in range(n):
            if not star or i:
                elementos.add(i)
    return elementos

def grupo_z_generadores(n, oper, star):
    """ Retorna el conjunto de generadores del grupo

    :param n: orden del grupo
    :param oper: operador del grupo ('+' o '*')
    :param star: True si no queremos incluir el número 0 (normalmente True con multiplicación, y False con suma)
    :return: lista de generadores
    """
    resul = []
    grupo_completo = grupo_z_crea(n, oper, star)
    for i in range(n):
        subgrupo = grupo_z_crea(n, oper, star, i)
        if len(subgrupo) == len(grupo_completo):
            resul.append(i)
    return resul
