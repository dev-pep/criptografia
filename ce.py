#!/usr/bin/env python3

# Utilidades relacionadas con la criptografía de curva elíptica.

import random
import json
import utils

# Funciones auxiliares *************************************************************************************************

# Clases ***************************************************************************************************************

class Curva:
    """Clase que define una curva elíptica"""

    def __init__(self, parms):
        """Inicializa los valores de la instancia al juego de parámetros indicado

        :param parms: string con el nombre de un archivo de parámetros (sin extensión ni prefijo "curva-")
        """
        with open(f"datos/curva-{parms}.json") as f:
            parametros = json.load(f)
        self.p = int(parametros["p"], 16)
        self.a = int(parametros["a"], 16)
        self.b = int(parametros["b"], 16)
        self.G = {  # un punto es un diccionario con claves "x", "y", y valores enteros, o ambos valores float("inf")
            "x": int(parametros["G"]["x"], 16),
            "y": int(parametros["G"]["y"], 16)
        }
        self.n = int(parametros["n"], 16)

    def calcula_y(self, x):
        """Dada una coordenada X, calcula las 2 y posibles y las retorna

        :param x: coordenada X
        :return: par de valores Y correspondientes a esa X, o float("inf")
        """
        # Si x es float("inf"), entonces y también lo será:
        if x == float("inf"):
            return [float("inf")]
        # Calculemos el valor de y^2: y^2 = x^3 + ax + b, módulo p:
        y2 = (x ** 3 + self.a * x + self.b) % self.p
        # Ahora, la raíz cuadrada de y2:
        y = utils.sqrt_mod(y2, self.p)
        # Hay que tener en cuenta que si el cofactor de este juego de parámetros no es 1,
        # este punto puede no ser uno de los puntos generados por G...
        return y

    def k_punto(self, k, punto):
        """Calcula un múltiplo del punto indicado (entero x punto)

        :param punto: punto a multiplicar
        :param k: entero no negativo por el que multiplicar el punto (con k=1 retornará ese punto)
        :return: coordenadas (x,y) del punto generado
        """
        # Aplicamos primero el módulo p al entero k:
        k = k % self.p
        # Doblar y añadir cuando proceda:
        testigo = punto
        resul = { "x": float("inf"), "y": float("inf")}  # punto 0
        while k:
            if k & 1:
                resul = self.suma_puntos(resul, testigo)
            k >>= 1
            testigo = self.duplica_punto(testigo)
        return resul

    def k_g(self, k):
        """Calcula un múltiplo del punto G, es decir, uno de los puntos que genera G

        :param k: entero no negativo por el que multiplicar G (con k=1 retornará G)
        :return: coordenadas (x,y) del punto generado
        """
        return self.k_punto(k, self.G)

    def negativo(self, punto):
        """Retorna el negativo (-P) de un punto P

        :param punto: punto inicial
        :return: punto negativo al inicial, tal que P + (-P) = 0
        """
        # Si es el punto en el infinito, se retorna él mismo:
        if punto["x"] == float("inf"):
            return punto
        return { "x": punto["x"], "y": -punto["y"] % self.p }

    def valida_punto(self, punto):
        """Comprueba que el punto pertenezca a la curva

        No comprueba que el punto esté generado por G, sino si pertenece a la curva completa. Por tanto,
        si el cofactor es mayor a 1, podría retornar True y ser un punto no generado por G.
        :param punto: punto a comprobar
        :return: True si pertenece, o False si no
        """
        x = punto["x"]
        if x == float("inf"):  # el punto 0 es válido
            return True
        if x != x % self.p:
            return False
        if punto["y"] in self.calcula_y(x):
            return True
        return False

    def punto_random_g(self):
        """Retorna un punto aleatorio, generado por G (incluye punto 0)

        :return: el punto generado
        """
        k = random.randint(0, self.n - 1)
        return self.k_g(k)

    def punto_random(self):
        """Retorna un punto aleatorio dentro de la curva (no forzosamente generado por G)

        :return: el punto generado
        """
        x = random.randint(0, self.p - 1)
        y = self.calcula_y(x)
        return y[random.randint(0, 1)]

    def suma_puntos(self, punto1, punto2):
        """Suma los dos puntos indicados, y retorna el resultado

        :param punto1: primer punto
        :param punto2: segundo punto
        :return: resultado de sumar los dos puntos
        """
        # Comprobaremos primero que los puntos pertenecen a la curva (no forzosamente generados por G):
        if not self.valida_punto(punto1) or not self.valida_punto(punto2):
            return None
        # Si uno de los puntos es el punto en el infinito, retornamos el otro:
        if punto1["x"] == float("inf"):
            return punto2
        if punto2["x"] == float("inf"):
            return punto1
        # Dos puntos finitos:
        x1, y1 = punto1["x"], punto1["y"]
        x2, y2 = punto2["x"], punto2["y"]
        # Si coincide la coordenada x de ambos, estamos en el caso P+P o  P+(-P):
        if x1 == x2:
            if y1 == y2:  # P+P, retornaremos punto doblado
                return self.duplica_punto(punto1)
            else:  # P+(-P), retornaremos punto en el infinito
                return { "x": float("inf"), "y": float("inf") }
        # Suma normal:
        pendiente = (y2 - y1) * utils.inverso_modn(x2 - x1, self.p)
        x3 = (pendiente ** 2 - x1 - x2) % self.p
        y3 = (pendiente * (x1 - x3) - y1) % self.p
        return { "x": x3, "y": y3 }

    def duplica_punto(self, punto):
        """Aplica la duplicación de un punto (point doubling)

        :param punto: el punto a duplicar
        :return: el nuevo punto resultante
        """
        # Comprobaremos primero que el punto pertenece a la curva (no forzosamente generado por G):
        if not self.valida_punto(punto):
            return None
        # Si el punto es el punto en el infinito, se retorna él mismo:
        if punto["x"] == float("inf"):
            return punto
        # Si el punto está en el eje X (y=0), retornamos el punto en el infinito:
        if punto["y"] == 0:
            return { "x": float("inf"), "y": float("inf") }
        # Punto finito:
        x1, y1 = punto["x"], punto["y"]
        # Duplicación:
        pendiente = (3 * x1 ** 2 + self.a) * utils.inverso_modn(2 * y1, self.p)
        x3 = (pendiente ** 2 - 2 * x1) % self.p
        y3 = (pendiente * (x1 - x3) - y1) % self.p
        return { "x": x3, "y": y3 }

# Funciones de las opciones de menú ************************************************************************************

# Menu *****************************************************************************************************************

opciones_menu = (
    ("Generar primeros (JSON)", menu_genera_json),
    ("Comprobar un número", menu_comprobar_num),
    ("Generar número primo", menu_generar_num)
)

# Programa *************************************************************************************************************

if __name__ == '__main__':  # no ejecutaremos menú si el archivo ha sido importado
    # Bucle principal:
    utils.menu(opciones_menu)
