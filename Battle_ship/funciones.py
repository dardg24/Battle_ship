import numpy as np
import random
import time 

# Interfaz
def mostrar_menu():
    """Muestra el menú del juego al usuario.

    Returns:
        str: Opción seleccionada por el usuario.
    """
    print("------ BATALLA NAVAL ------")
    print("1. Leer Instrucciones")
    print("2. Jugar Demo")
    print("3. Jugar")
    print("4. Salir")
    eleccion = input("Elige una opción: ")
    return eleccion

# Instrucciones
def mostrar_instrucciones():
    """Muestra las instrucciones del juego al usuario."""
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

# Array de 10x10
def crear_tablero(tamaño:tuple):
    """ Crear un tablero.
    
    Esta función crea un array de numpy del tamaño especificado 
    y lo llena con strings de espacios vacíos.
    
    Args:
        tamaño (tuple): Una tupla con las dimensiones (x, y) del tablero.
    
    Returns:
        np.array: Un array de numpy lleno de strings de espacios vacíos.
    """
    return np.full(tamaño, " ")

def orientacion_aleatoria():
    """ Genera una orientación aleatoria para los barcos.
    
    Returns:
        str: Una de las orientaciones: N, S, E, O.
    """
    return random.choice(['N', 'S', 'E', 'O'])

def es_posicion_valida(tablero:object, x:int, y:int):
    """ Verificar si la posición (x, y) es válida en el tablero.
    
    Args:
        tablero (obj): El tablero donde se verifica.
        x (int): Coordenada en el eje X.
        y (int): Coordenada en el eje Y.
    
    Returns:
        bool: True si la posición es válida, False en caso contrario.
    """
    return 0 <= x < tablero.dimensiones[0] and 0 <= y < tablero.dimensiones[1]
    
def verificar_posicion_barco(tablero, x, y, orient, barco):
        """
    Verifica si la posición y orientación especificadas para un barco son válidas en el tablero.

    Parámetros:
    - tablero (TipoTablero): Objeto que representa el tablero del juego.
    - x (int): Coordenada en el eje x donde se desea ubicar el barco.
    - y (int): Coordenada en el eje y donde se desea ubicar el barco.
    - orient (str): Orientación del barco. Valores posibles: 'N' (Norte), 'S' (Sur), 'E' (Este), 'O' (Oeste).
    - barco (TipoBarco): Objeto que representa el barco que se desea ubicar.

    Retorna:
    - bool: True si es posible ubicar el barco en la posición y orientación especificadas, False en caso contrario.

    Ejemplo de uso:
    - tablero = Tablero(10, 10)
    - barco = Barco(3)
    - verificar_posicion_barco(tablero, 5, 5, 'N', barco)
    True
    """
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

# Agrega los barcos del jugador en su diccionario
def agregar_diccionario_barcos(BARCOS_DICT:dict, tablero:object):
    """Agrega los barcos del jugador en su diccionario.

    Args:
        BARCOS_DICT (dict): Diccionario de barcos a agregar.
        tablero (object): Tablero donde agregar los barcos.
    """
    for clave, barco in BARCOS_DICT.items():
        tablero.agregar_barco(clave, barco)

# Agrega los barcos al objeto tablero tanto jugador como IA
def agregar_barcos_tablero(tablero):
    """Agrega los barcos del jugador en su tablero.

    Args:
        tablero (object): Tablero donde agregar los barcos.
    """
    todos_colocados = True # True, esto indica que todos los barcos han sido colocados con éxito en el tablero.
    for clave, barco in tablero.barcos.items(): # Aquí, la función itera sobre el diccionario barcos del objeto tablero. Clave = "Barco_4": barco = el objeto asociado a esa clave.
        tablero.colocar_barco(clave, barco) # Se llama al método colocar_barco del objeto tablero con la clave y el barco actual. 
        if not tablero.posiciones.get(clave): # Verifica si el barco (identificado por su clave) ha sido colocado exitosamente en el tablero.
            todos_colocados = False # si esa clave no tiene posiciones asociadas en el tablero), entonces todos_colocados = False
    if todos_colocados:
        print(f"Todos los barcos del jugador {tablero.nombre_jugador} fueron colocados con éxito.")
    else:
        print(f"No se pudo colocar todos los barcos del jugador {tablero.nombre_jugador}.")

# Solicitar las coordenadas hasta que sean número válidos
def solicitar_coordenadas(tipo_de_juego):
    """Solicita al usuario las coordenadas para disparar.

    Args:
        tipo_de_juego (str): Tipo de juego, puede ser "DEMO" o otro.

    Returns:
        tuple: Coordenadas x, y introducidas por el usuario.
    """
    if tipo_de_juego == "DEMO":
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

# La función de disparar, evalua si es jugador, por defecto True
def disparar(tablero_jugador:object,tablero_ia:object, x:int, y:int, es_jugador=True):
        """ Disparar al tablero del oponente.
    
    Esta función realiza un disparo a las coordenadas (x,y) 
    del tablero del oponente y verifica si acertó a un barco.
    
    Args:
        tablero_jugador (obj): El tablero del jugador.
        tablero_ia (obj): El tablero de la IA.
        x (int): Coordenada en el eje X.
        y (int): Coordenada en el eje Y.
        es_jugador (bool): Indica si el que dispara es el jugador.
                           Por defecto es True.
    """
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

# Salir del juego durante el turno del jugador
def preguntar_continuidad():
    """Pregunta al usuario si desea continuar con el juego.

    Returns:
        bool: True si el usuario desea continuar, False en caso contrario.
    """
    while True:
        seguir = input("Desea seguir jugando? (S/N):")
        if seguir != "S" and seguir != "N":
            print("Ingrese una opcion valida")
        elif seguir == "S":
                return True
        else:
            return False

# Muestra los tableros al iniciar el turno del jugador, donde están los barcos y dónde está disparando
def mostrar_tablero(tablero, tipo):
            """ Muestra el tablero en consola con una representación visual.

    Parámetros:
    - tablero (list[list[str]]): Lista de listas que representa el tablero del juego. 
                                 Las casillas vacías están representadas por " " y las ocupadas por otras cadenas (por ejemplo, 'B' para barco).
    - tipo (str): Una descripción o tipo del tablero, por ejemplo, "jugador" o "enemigo".

    No retorna ningún valor, pero imprime el tablero en consola.

    Ejemplo de uso:
    tablero_ejemplo = [[" ", " ", "B"], ["B", " ", "B"], [" ", " ", " "]]
    mostrar_tablero(tablero_ejemplo, 'Jugador')
    Tablero de Jugador:
    . . B
    B . B
    . . .

    Nota:
    Las casillas vacías en el tablero (representadas por " ") se visualizan como "." en la salida.
    """
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

# Definir si Demo u otro
def jugar(tipo_de_juego:str):
    """Inicia el juego según el tipo especificado.

    Args:
        tipodejuego (str): Tipo de juego, puede ser "DEMO" o otro.
    """
    nombre = solicitar_nombre()
    tablero_jugador= setear_tablero(tipo_de_juego,1,nombre)
    tablero_ia = setear_tablero(tipo_de_juego,2,"IA")
    juego_en_desarrollo(tablero_jugador,tablero_ia,tipo_de_juego)

# El nombre como input
def solicitar_nombre():
    """Solicita al usuario su nombre para el juego.

    Returns:
        str: Nombre introducido por el usuario.
    """
    while True:
        nombre = input("Ingrese nombre de jugador:")
        if len(nombre) == 0:
                print ("Debes introducir un nombre de jugador")
        else:
            return nombre

# Hace los settings de los tableros y barcos dependiendo del tipo de juego que se desee
def setear_tablero (tipo:str, id:int, nombre:str):
    """Configura el tablero según el tipo de juego.

    Esta función configura el tablero del jugador o de la IA
    según el tipo de juego especificado, ya sea "JUGAR" o "DEMO".

    Args:
        tipo (str): Tipo de juego, puede ser "JUGAR" o "DEMO".
        id (int): Identificador del tablero.
        nombre (str): Nombre del jugador o "IA" para el tablero de la IA.

    Returns:
        object: Tablero configurado.
    """
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
        tablero = Tablero(id,nombre,dimensiones=(5,5)) # Para fines de la demo se usara una dimensión 5x5
        # Colocar los barcos de los jugadores en su diccionario
        agregar_diccionario_barcos(BARCOS_DICT, tablero)
        # Colocar los barcos de los jugadores en su tablero
        agregar_barcos_tablero(tablero)
    return tablero

# Flujo central del juego            
def juego_en_desarrollo(tablero_jugador:object,tablero_ia:object,tipo_de_juego:str):
    """Maneja el desarrollo del juego entre el jugador y la IA.

    Args:
        tablero_jugador (object): Tablero del jugador.
        tablero_ia (object): Tablero de la IA.
        tipodejuego (str): Tipo de juego, puede ser "DEMO" o otro.
    """
    turno_jugador = True
    while True:
        if turno_jugador:
            print (f"Es el turno de {tablero_jugador.nombre_jugador}")
            mostrar_tablero(tablero_jugador.tablero_barcos, "Barcos")
            mostrar_tablero(tablero_jugador.tablero_disparos, "Disparos")
            seguir = preguntar_continuidad() # Aquí damos la opción de salir del juego
            if seguir == False:
               break 
            x, y = solicitar_coordenadas(tipo_de_juego)
            if tablero_jugador.tablero_disparos[x][y] == "-" or tablero_jugador.tablero_disparos[x][y] == "X": # Condición que evalua si las coordenadas que se enviaron previamente ya fueron utilizadas
                turno_jugador = True # Mientrás siga siendo True, sigue siendo el turno del jugador
                print("Ya usaste esta coordenada, introduce una coordenada nueva.")
                time.sleep (2)
            else:
                disparar(tablero_jugador, tablero_ia,x, y)
                if tablero_ia.tablero_barcos[x][y] == "X":
                    print("¡Acertaste!")
                    turno_jugador = True # Al disparar se cambiar el valor de la posición por X y al cumplir la condición, envia print y mantiene el True
                else:
                    print("¡Fallaste!")
                    turno_jugador = False
        else:
            print ("Es el turno de la IA")
            time.sleep(2)
            if tipo_de_juego == "DEMO":
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
        if juego_terminado(tablero_jugador): # Acá evalua si en efecto, dentro del objeto tablero_jugador si todos los value tienen una X, esto significa que el juego término
            print("¡La IA ha ganado!")
            break
        elif juego_terminado(tablero_ia): # Igual que antes pero en el objeto tablero_ia
             print("¡El jugador ha ganado!")
             break

# Lógica para saber cuándo el juego ha terminado
def juego_terminado(tablero:object):
    """Verifica si el juego ha terminado.

    Esta función verifica si todos los barcos en un tablero han sido hundidos.

    Args:
        tablero (object): Tablero a verificar.

    Returns:
        bool: True si el juego ha terminado, False en caso contrario.
    """
    for arreglo in tablero.posiciones.values(): #  Este bucle itera sobre el índice de cada posición dentro de arreglo. 
        for i in range(len(arreglo)): # Por cada posición, verifica el estado de esa posición en el tablero.
            if arreglo[i] != "X": # La condición verifica si la posición actual (indicada por arreglo[i]) no es igual a "X"
                return False # significa que aún hay al menos un barco que no ha sido hundido. La función regresa False, indicando que el juego no ha terminado.
    return True