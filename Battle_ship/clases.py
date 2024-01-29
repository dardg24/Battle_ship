import random
import numpy as np
from variables import DIMENSIONES
# from funciones import crear_tablero, orientacion_aleatoria, verificar_posicion_barco
class Barco:
    """
    Representa un barco dentro del juego "Hundir la flota".
    
    Attributes:
        nombre (str): Nombre del barco.
        eslora (int): Longitud del barco en casillas.
    """
        
    def __init__(self, nombre:str, eslora:int):
        """
        Inicializa un nuevo barco con un nombre y una eslora.
        
        Args:
            nombre (str): Nombre del barco.
            eslora (int): Longitud del barco en casillas.
        """        
        self.nombre = nombre
        self.eslora = eslora


class Tablero:
    """
    Representa el tablero del juego para un jugador.

    Attributes:
        jugador_id (int): Identificador único del jugador.
        nombre_jugador (str): Nombre del jugador.
        dimensiones (tuple): Dimensiones del tablero en forma (filas, columnas).
        tablero_barcos (np.array): Tablero donde el jugador tiene sus barcos.
        tablero_disparos (np.array): Tablero donde el jugador marca sus disparos.
        barcos (dict): Diccionario que mapea identificadores a objetos Barco.
        posiciones (dict): Guarda las posiciones de los barcos en el tablero.
    """
    
    def __init__(self, jugador_id:int, nombre_jugador:str, dimensiones=DIMENSIONES):        
        self.jugador_id = jugador_id 
        self.nombre_jugador = nombre_jugador
        self.dimensiones = dimensiones 
        self.tablero_barcos = self.crear_tablero() # Donde el jugador tiene sus barcos
        self.tablero_disparos = self.crear_tablero() # Donde el jugador marca sus disparos
        self.barcos = {}
        self.posiciones = {}

    def crear_tablero(self):
        return np.full(self.dimensiones, " ")

    def orientacion_aleatoria(self):
        return random.choice(['N', 'S', 'E', 'O'])

    def agregar_barco(self, identificador, barco):
        self.barcos[identificador] = barco
    
    def colocar_barco(self, clave, barco):
        x = random.randint(0, self.dimensiones[0] - 1)
        y = random.randint(0, self.dimensiones[1] - 1)
        orient = self.orientacion_aleatoria()
        if self.verificar_posicion_barco(x, y, orient, barco):
            for _ in range(barco.eslora):
                self.tablero_barcos[x][y] = 'B'
                if clave not in self.posiciones:
                    self.posiciones[clave] = []
                self.posiciones[clave].append((x, y))
                if orient == 'N':
                    x -= 1
                elif orient == 'S':
                    x += 1
                elif orient == 'E':
                    y += 1
                elif orient == 'O':
                    y -= 1
            return
        else:
            self.colocar_barco(clave, barco)
    
    def verificar_posicion_barco(self, x, y, orient, barco):
        for _ in range(barco.eslora):
            if x < 0 or y < 0:
                return False
            if not (0 <= x < self.dimensiones[0] and 0 <= y < self.dimensiones[1]):
                return False
            if self.tablero_barcos[x][y] == 'B':
                return False
            if orient == 'N':
                x -= 1
            elif orient == 'S':
                x += 1
            elif orient == 'E':
                y += 1
            elif orient == 'O':
                y -= 1
        return True
