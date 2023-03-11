from postfix import *
from thompson import *
from grafo import *
from afd_directo import *
from afd_subconjuntos import *
from simulacion import *
from minimizacion import *
from prueba import * 

# expresion = "0?(1?)?0?"
# expresion = "ab"
# expresion = "(a|b)*abb"
# expresion = "abb"
# expresion = "a|b"
# expresion = "a?b+"
# expresion = "a**"
# expresion = "0?(1?)?0*"
# expresion = "a|x*a*|ε"
# expresion = "(a|b)|(c|d)"
# expresion = "(a|b)*|(c|d)*"

salir = False

while not salir:
    print("\n==========================================================================================\n")
    print("Ingrese la opcion que desea realizar: ")
    print("\t[ 1 ] Construccion de AFN y AFD")
    print("\t[ 2 ] Simulacion de un AFN")
    print("\t[ 3 ] Simulacion de un AFD")
    print("\t[ 4 ] prueba")
    print("\t[ 5 ] Salir")
    opcion = input("-> ")
    print("\n==========================================================================================\n")


    if opcion == '1':
        expresiono = input("\n Ingrese la expresion regular que sera convertida a AFN -> ")

        # Se hace la conversion de la expresion regular a postfix.
        postfix = Postfix(expresiono)
        postfix.toPostfix()
        expresion = postfix.final

        # Se aplica el algoritmo de thomspon para crear el afn.
        thompson = Thompson(expresion)
        nodos = thompson.visitados


        # Se crea el grafo con los nodos del afn.
        grafo = Grafo(nodos, nombre = "expresion_a_AFN")

        print("\n==========================================================================================\n")
        print('\n\t AFN creado con exito.\n')
        print("\n==========================================================================================\n")

        
        postfix = Postfix(expresiono, True)
        postfix.toPostfix()
        expresion = postfix.final

        # Se hace la construccion directa de el AFD a partir de la expresion regular
        afd = AFD_D(expresion)

        # Se crea el grafo con los nodos del afd.
        grafo = Grafo(afd.nodos, nombre = "construccion_directa_afd")

        print("\n==========================================================================================\n")
        print('\n\t AFD por construccion directa creado con exito.\n')
        print("\n==========================================================================================\n")

        # Se convierte el AFN a un AFD
        afd2 = Subconjuntos(thompson)

        # Se crea el grafo con los nodos del afd.
        grafo = Grafo(afd2.afd, nombre = "construccion_subconjuntos_afd")
        

        print("\n==========================================================================================\n")
        print('\n\t AFD por subconjuntos a partir de AFNcreado con exito.\n')
        print("\n==========================================================================================\n")

        # Se minimiza el AFD directo
        afd_directo_minimizado = Minimizacion(afd.nodos, afd.alfabeto)

        # Se crea el grafo con los nodos del afd.
        grafo = Grafo(afd_directo_minimizado.minimizado, nombre = "afd_directo_minimizado")

        print("\n==========================================================================================\n")
        print('\n\t AFD directo minimizado creado con exito.\n')
        print("\n==========================================================================================\n")

        # Se minimiza el AFD por subconjuntos
        afd_subconjuntos_minimizado = Minimizacion(afd2.afd, afd2.alfabeto)

        # Se crea el grafo con los nodos del afd.
        grafo = Grafo(afd_subconjuntos_minimizado.minimizado, nombre = "afd_subconjuntos_minimizado")

        print("\n==========================================================================================\n")
        print('\n\t AFD por subconjuntos minimizado creado con exito.\n')
        print("\n==========================================================================================\n")

    elif opcion == '2':

        expresion = input("\n Ingrese la expresion regular que sera convertida a AFN -> ")

        # Se hace la conversion de la expresion regular a postfix.
        postfix = Postfix(expresion)
        postfix.toPostfix()
        expresion = postfix.final

        # Se aplica el algoritmo de thomspon para crear el afn.
        thompson = Thompson(expresion)
        nodos = thompson.visitados
        alfabeto = thompson.alfabeto

        # Se recibe la expresion a ver si es aceptado por el AFN

        expresion = input("\n Ingrese la expresion que sera evaluada por el AFN -> ")

        simulacion = Simulacion(nodos,alfabeto,expresion, "AFN")

        if(simulacion.aceptado):
            print("\n==========================================================================================\n")
            print("\n\tLa expresion es aceptada por el AFN. Los movimientos realizados son los siguientes:")
            movimientos = simulacion.movimientos
            print(movimientos)
            print("\n==========================================================================================\n")
        else:
            print("\n==========================================================================================\n")
            print("\n\tLa expresion no es aceptada por el AFN")
            print("\n==========================================================================================\n")


    elif opcion == '3':

        expresion = input("\n Ingrese la expresion regular que sera convertida a AFD de forma directa -> ")

        # Se usa funcion de check_expresion para ver si hay algun error con la expresion regular y la regresa concatenada
        postfix = Postfix(expresion, True)
        postfix.toPostfix()
        expresion = postfix.final

        # Se crea el AFD a partir de la expresion regular
        afd = AFD_D(expresion)
        alfabeto = afd.alfabeto
        nodos = afd.nodos

        # Se recibe la expresion a ver si es aceptado por el AFD

        expresion = input("\n Ingrese la expresion que sera evaluada por el AFD -> ")

        simulacion = Simulacion(nodos,alfabeto,expresion, "AFD")

        if(simulacion.aceptado):
            print("\n==========================================================================================\n")
            print("\n\tLa expresion es aceptada por el AFD. Los movimientos realizados son los siguientes:")
            movimientos = simulacion.movimientos
            print(movimientos)
            print("\n==========================================================================================\n")
        else:
            print("\n==========================================================================================\n")
            print("\n\tLa expresion no es aceptada por el AFD")
            print("\n==========================================================================================\n")

    elif opcion == '4':
        prueba()

    elif opcion == '5':
        salir = True



