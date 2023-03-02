from postfix import *
from thomson import Thomson
from grafo import *
from afd_directo import *

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
    print("\t[ 3 ] Salir")
    opcion = input("-> ")
    print("\n==========================================================================================\n")

    if opcion == '1':
        expresion = input("\n Ingrese la expresion regular que sera convertida a AFN -> ")

        # Se hace la conversion de la expresion regular a postfix.
        postfix = Postfix(expresion)
        postfix.toPostfix()
        expresion = postfix.final

        # Se aplica el algoritmo de thomspon para crear el afn.
        thomson = Thomson(expresion)
        nodos = thomson.visitados

        # Se crea el grafo con los nodos del afn.
        grafo = Grafo(nodos)
    
    elif opcion == '2':
        expresion = input("\n Ingrese la expresion regular que sera convertida a AFD -> ")

        # Se usa funcion de check_expresion para ver si hay algun error con la expresion regular y la regresa concatenada
        postfix = Postfix(expresion, True)
        postfix.toPostfix()
        expresion = postfix.final


        afd = AFD_D(expresion)


        pass

    elif opcion == '3':
        salir = True

