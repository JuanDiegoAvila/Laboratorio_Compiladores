from postfix import *
from thompson import *
from grafo import *
from afd_directo import *
from afd_subconjuntos import *
from simulacion import *

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
    print("\t[ 1 ] Convertir una expresion regular a AFN")
    print("\t[ 2 ] Convertir una expresion regular a AFD de forma directa")
    print("\t[ 3 ] Convertir AFN a AFD por sub-conjuntos")
    print("\t[ 4 ] Simulacion de un AFN")
    print("\t[ 5 ] Simulacion de un AFD")
    print("\t[ 6 ] Salir")
    opcion = input("-> ")
    print("\n==========================================================================================\n")

    if opcion == '1':
        expresion = input("\n Ingrese la expresion regular que sera convertida a AFN -> ")

        # Se hace la conversion de la expresion regular a postfix.
        postfix = Postfix(expresion)
        postfix.toPostfix()
        expresion = postfix.final

        # Se aplica el algoritmo de thomspon para crear el afn.
        thompson = Thompson(expresion)
        nodos = thompson.visitados

        # Se crea el grafo con los nodos del afn.
        grafo = Grafo(nodos)
    
    elif opcion == '2':
        expresion = input("\n Ingrese la expresion regular que sera convertida a AFD de forma directa -> ")

        # Se usa funcion de check_expresion para ver si hay algun error con la expresion regular y la regresa concatenada
        postfix = Postfix(expresion, True)
        postfix.toPostfix()
        expresion = postfix.final

        print(expresion)

        # Se crea el AFD a partir de la expresion regular
        afd = AFD_D(expresion)
        grafo = Grafo(afd.nodos)


    elif opcion == '3':

        expresion = input("\n Ingrese la expresion regular que sera convertida a AFD por subconjuntos -> ")

        # Se hace la conversion de la expresion regular a postfix.
        postfix = Postfix(expresion)
        postfix.toPostfix()
        expresion = postfix.final

        # Se aplica el algoritmo de thomspon para crear el afn.
        thompson = Thompson(expresion)
        grafo = Grafo(thompson.visitados)



        # Se convierte el AFN a un AFD 
        afd = Subconjuntos(thompson)
        grafo = Grafo(afd.afd)

    elif opcion == '4':

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

        simulacion = Simulacion(nodos,alfabeto,expresion)


    elif opcion == '5':

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

        simulacion = Simulacion(nodos,alfabeto,expresion)

    
    elif opcion == '6':
        salir = True

