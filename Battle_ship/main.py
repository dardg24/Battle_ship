from funciones import *



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