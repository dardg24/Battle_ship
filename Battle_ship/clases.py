from variables import DIMENSIONES
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
        tablero_barcos (list): Tablero donde el jugador tiene sus barcos.
        tablero_disparos (list): Tablero donde el jugador marca sus disparos.
        barcos (dict): Diccionario que mapea identificadores a objetos Barco.
        posiciones (dict): Guarda las posiciones de los barcos en el tablero.
    """
    
    def __init__(self, jugador_id:int, nombre_jugador:str, dimensiones=DIMENSIONES):        
        """
        Inicializa un nuevo tablero para un jugador.
        
        Args:
            jugador_id (int): Identificador único del jugador.
            nombre_jugador (str): Nombre del jugador.
            dimensiones (tuple, optional): Dimensiones del tablero. Por defecto DIMENSIONES.
        """
                
        self.jugador_id = jugador_id 
        self.nombre_jugador = nombre_jugador
        self.dimensiones = dimensiones 
        self.tablero_barcos = crear_tablero(self.dimensiones) # Donde el jugador tiene sus barcos
        self.tablero_disparos = crear_tablero(self.dimensiones) # Donde el jugador marca sus disparos
        self.barcos = {}
        self.posiciones = {} # Agregamos este atributo para guardar las posiciones de los barcos

    def agregar_barco (self, identificador, barco):
        """
        Agrega un barco al diccionario de barcos del tablero.
        
        Args:
            identificador (str/int): Identificador único del barco.
            barco (Barco): Objeto Barco a agregar.
        """
        
        self.barcos[identificador] = barco
    
    def colocar_barco(self, clave, barco):
       
        """
        Coloca un barco en el tablero en una posición y orientación aleatorias.
        
        Args:
            clave (str): Clave para guardar las posiciones del barco en el diccionario de posiciones.
            barco (Barco): Objeto Barco a colocar.
        """
       
        x = random.randint(0, self.dimensiones[0] - 1)
        y = random.randint(0, self.dimensiones[1] - 1)
        orient = orientacion_aleatoria()
        if verificar_posicion_barco(self, x, y, orient, barco):
            for _ in range(barco.eslora):
                self.tablero_barcos[x][y] = 'B'
                if clave not in self.posiciones: # Esta condicion me evalua si la clave no se encuentra en el dic
                    self.posiciones[clave] = [] # Sí es True, me crea una nueva entrada en el diccionario con la clave [clave] y le asigna una lista vacía como valor.
                self.posiciones[clave].append((x, y)) # Aquí registra el valor asociado a esa clave que se creo con las coordenadas x, y
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