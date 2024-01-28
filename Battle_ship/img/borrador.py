import numpy as np
import random
import time
DIMENSIONES = 10, 10
tablero_jugador= {}
tablero_ia= {}
class Barco:
    def __init__(self, nombre, eslora):
        self.nombre = nombre
        self.eslora = eslora

class Tablero:
    def __init__(self, jugador_id, nombre_jugador, dimensiones=DIMENSIONES):
        self.jugador_id = jugador_id 
        self.nombre_jugador = nombre_jugador
        self.dimensiones = dimensiones 
        self.tablero_barcos = crear_tablero(self.dimensiones) # Donde el jugador tiene sus barcos
        self.tablero_disparos = crear_tablero(self.dimensiones) # Donde el jugador marca sus disparos
        self.barcos = {}
        self.posiciones = {} # Agregamos este atributo para guardar las posiciones de los barcos

    def agregar_barco (self, identificador, barco):
        self.barcos[identificador] = barco
    
    def colocar_barco(self, clave, barco):
       
            x = random.randint(0, self.dimensiones[0] - 1)
            y = random.randint(0, self.dimensiones[1] - 1)
            orient = orientacion_aleatoria()
            if verificar_posicion_barco(self, x, y, orient, barco):
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
   

# Acá creamos los 10 barcos como objetos dentro de la clase barco, estan definidos por nombre (key) : eslora (value)
def disparar(tablero_jugador,tablero_ia, x, y, es_jugador=True):
        if es_jugador: # Si es el jugador el que dispara
            if tablero_ia.tablero_barcos[x][y] == " ":
                print("Agua")
                tablero_jugador.tablero_disparos[x,y] = "-"
            else:
                print("Tocado")
                tablero_jugador.tablero_disparos[x,y] = "X"
                tablero_ia.tablero_barcos[x,y] = "X"
                for arreglo in tablero_ia.posiciones.values():
                    for i in range(len(arreglo)):
                        if arreglo[i] == (x,y):
                            arreglo[i] = "X"
        else: # Si es la IA la que dispara
            if tablero_jugador.tablero_barcos[x,y] == " ":
                print ("Agua")
                tablero_ia.tablero_disparos[x,y] = "-"
            else:
                print("Tocado")
                tablero_ia.tablero_disparos[x,y] = "X"
                tablero_jugador.tablero_barcos[x,y] = "X"
                for arreglo in tablero_jugador.posiciones.values():
                    for i in range(len(arreglo)):
                        if arreglo[i] == (x,y):
                            arreglo[i] = "X"

def crear_tablero(tamaño):
    """ Una función que creará un array de numpy
        con el tamaño de las dimensiones y lleno
        de strings de espacios vacios
        
        args: tamaño = DIMENSIONES (por defecto)
        return: Un array 10x10 con strings de espacios vacios
    """
    return np.full(tamaño, " ")

def orientacion_aleatoria():
    """ Esta función arroja un string aleatorio
        entre N,S,E,O
    """
    return random.choice(['N', 'S', 'E', 'O'])

def es_posicion_valida(tablero, x, y):
        return 0 <= x < tablero.dimensiones[0] and 0 <= y < tablero.dimensiones[1]
    
def verificar_posicion_barco(tablero, x, y, orient, barco):
        for _ in range(barco.eslora):
            if x < 0 or y < 0:
                return False
            if not es_posicion_valida(tablero, x, y):
                return False
            if tablero.tablero_barcos[x][y] == 'B':
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

def mostrar_tablero(tablero, tipo):
            print(f"Tablero de {tipo}:")
            for fila in tablero:
                fila_visual = []
                for c in fila:
                    if c == " ":
                        fila_visual.append(".")
                    else:
                        fila_visual.append(c)
                print(" ".join(fila_visual))
            print("\n")

def SetearTablero (tipo, id, nombre):
    if tipo == "JUGAR":
        BARCOS_DICT = {
        'barco_4': Barco('barco 4', 4),
        'barco_3a': Barco('barco 3a', 3),
        'barco_3b': Barco('barco 3b', 3),
        'barco_2a': Barco('barco 2a', 2),
        'barco_2b': Barco('barco 2b', 2),
        'barco_2c': Barco('barco 2c', 2),
        'barco_1a': Barco('barco 1a', 1),
        'barco_1b': Barco('barco 1b', 1),
        'barco_1c': Barco('barco 1c', 1),
        'barco_1d': Barco('barco 1d', 1)
        }  
        # Se crea el objeto tablero con el respectivo ID identificador y Nombre de usuario
        tablero = Tablero(id,nombre)
        # Colocar los barcos de los jugadores en su diccionario
        agregar_diccionario_barcos(BARCOS_DICT, tablero)
        # Colocar los barcos de los jugadores en su tablero
        agregar_barcos_tablero(tablero)
        return tablero
    elif tipo == "DEMO":  
        BARCOS_DICT = {
        'barco_4': Barco('barco 4', 4),
        'barco_3a': Barco('barco 3a', 3),
        'barco_2a': Barco('barco 2a', 2),
        'barco_1d': Barco('barco 1d', 1)
        }  
        # Se crea el objeto tablero con el respectivo ID identificador y Nombre de usuario
        tablero = Tablero(id,nombre,dimensiones=(5,5))
        # Colocar los barcos de los jugadores en su diccionario
        agregar_diccionario_barcos(BARCOS_DICT, tablero)
        # Colocar los barcos de los jugadores en su tablero
        agregar_barcos_tablero(tablero)
    return tablero

# Funcion que agrega los barcos del jugador en su diccionario
def agregar_diccionario_barcos(BARCOS_DICT, tablero):
    for clave, barco in BARCOS_DICT.items():
        tablero.agregar_barco(clave, barco)

# Funcion que agrega los barcos del jugador en su tablero
def agregar_barcos_tablero(tablero):
    todos_colocados = True
    for clave, barco in tablero.barcos.items():
        tablero.colocar_barco(clave, barco)
        if not tablero.posiciones.get(clave):
            todos_colocados = False
    if todos_colocados:
        print(f"Todos los barcos del jugador {tablero.nombre_jugador} fueron colocados con éxito.")
    else:
        print(f"No se pudo colocar todos los barcos del jugador {tablero.nombre_jugador}.")
  
def solicitar_coordenadas(tipodejuego):
    if tipodejuego == "DEMO":
        while True:
            try:
                x = int(input("Ingresa la coordenada x, entre (0-4):"))
                y = int(input("Ingresa la coordenada y, entre (0-4):"))
                if (0 <= x < 5) and (0 <= y < 5):
                    return x, y
                else:
                    print ("Coordenadas fuera de rango. Por favor, vuelve a intentarlo.")
            except ValueError:
                print ('Por favor, ingresa un número válido')
    else:
        while True:
            try:
                x = int(input("Ingresa la coordenada x, entre (0-9):"))
                y = int(input("Ingresa la coordenada y, entre (0-9):"))
                if (0 <= x < 10) and (0 <= y < 10):
                    return x, y
                else:
                    print ("Coordenadas fuera de rango. Por favor, vuelve a intentarlo.")
            except ValueError:
                print ('Por favor, ingresa un número válido')

def solicitar_nombre():
    while True:
        nombre = input("Ingrese nombre de jugador:")
        if len(nombre) == 0:
                print ("Debes introducir un nombre de jugador")
        else:
            return nombre

def juego_terminado(tablero):

    for arreglo in tablero.posiciones.values():
        for i in range(len(arreglo)):
            if arreglo[i] != "X":
                return False
    return True

def preguntar_continuidad():
    while True:
        seguir = input("Desea seguir jugando? (S/N):")
        if seguir != "S" and seguir != "N":
            print("Ingrese una opcion valida")
        elif seguir == "S":
                return True
        else:
            return False
            
def juego_en_desarrollo(tablero_jugador,tablero_ia,tipodejuego):
    turno_jugador = True
    while True:
        if turno_jugador:
            print (f"Es el turno de {tablero_jugador.nombre_jugador}")
            mostrar_tablero(tablero_jugador.tablero_barcos, "Barcos")
            mostrar_tablero(tablero_jugador.tablero_disparos, "Disparos")
            seguir = preguntar_continuidad()
            if seguir == False:
               break 
            x, y = solicitar_coordenadas(tipodejuego)
            if tablero_jugador.tablero_disparos[x][y] == "-" or tablero_jugador.tablero_disparos[x][y] == "X":
                turno_jugador = True
                print("Ya usaste esta coordenada, introduce una coordenada nueva.")
                time.sleep (2)
            else:
                disparar(tablero_jugador, tablero_ia,x, y)
                if tablero_ia.tablero_barcos[x][y] == "X":
                    print("¡Acertaste!")
                    turno_jugador = True
                else:
                    print("¡Fallaste!")
                    turno_jugador = False
        else:
            print ("Es el turno de la IA")
            time.sleep(2)
            if tipodejuego == "DEMO":
                x, y = random.randint(0, 4), random.randint(0, 4) # Aquí la IA elige coordenadas aleatorias
            else: 
                x, y = random.randint(0, 9), random.randint(0, 9)  # Aquí la IA elige coordenadas aleatorias

            if tablero_ia.tablero_disparos[x][y] == "-" or tablero_ia.tablero_disparos[x][y] == "X":
                turno_jugador = False
                time.sleep (2)
            else:
                disparar(tablero_jugador,tablero_ia,x, y, False)
                time.sleep(2)
                if tablero_jugador.tablero_barcos[x][y] == "X":
                    print("¡La IA acertó!")
                    turno_jugador = False
                else:
                    print("¡La IA falló!")
                    time.sleep(2)
                    turno_jugador = True
        if juego_terminado(tablero_jugador):
            print("¡La IA ha ganado!")
            break
        elif juego_terminado(tablero_ia):
             print("¡El jugador ha ganado!")
             break

def jugar(tipodejuego):
    nombre = solicitar_nombre()
    tablero_jugador= SetearTablero(tipodejuego,1,nombre)
    tablero_ia = SetearTablero(tipodejuego,2,"IA")
    juego_en_desarrollo(tablero_jugador,tablero_ia,tipodejuego)
        
def mostrar_menu():
    print("------ BATALLA NAVAL ------")
    print("1. Leer Instrucciones")
    print("2. Jugar Demo")
    print("3. Jugar")
    print("4. Salir")
    eleccion = input("Elige una opción: ")
    return eleccion

def mostrar_instrucciones():
    print ("\t In this game, you will play against the computer in a classic game of Battleship. The rules are as follows:", end='\n')
    print ('\n')
    print ("\t1. There are two players: you and the computer.")
    print ("\t2. The game is played on a 10x10 grid where both players place their ships.")
    print ("\t3. At the beginning of the game, each player places their ships on the grid.")
    print ('\n')
    print   ("\tThe ships are as follows:")
    print   ("\t- 4 ships of 1 cell length")
    print   ("\t- 3 ships of 2 cells length")
    print   ("\t- 2 ships of 3 cells length")
    print   ("\t- 1 ship of 4 cells length")
    print ('\n')
    print ("\t4. The objective is to sink all of your opponent's ships by guessing their coordinates.")
    print ("\t5. The game is turn-based, and you start first.")
    print ("\t6. On your turn, you choose a coordinate (X, Y) to fire at your opponent's grid.")
    print ("\tIf you hit a ship, you get another turn.")
    print ("\t7. On the computer's turn, it will randomly select a coordinate on your grid to fire at.")
    print ("\tIf the computer hits a ship, it gets another turn.")
    print ("\t8. The game continues until all of one player's ships are sunk.")
    print ("\t9. The first player to sink all of their opponent's ships wins the game.")
    
def main():
    while True:
        eleccion = mostrar_menu()

        if eleccion == "1":
            mostrar_instrucciones()
        elif eleccion == "2":
            jugar("DEMO")
        elif eleccion == "3":
            jugar("JUGAR")
        elif eleccion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, elige una opción del 1 al 4.")
if __name__ == "__main__":
    main()
    
