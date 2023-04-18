from Yalex.yalex import * 
from Automatas.postfix import *
from Automatas.thompson import * 
from Automatas.simulacion import Simulacion
import pickle
import sys
sys.setrecursionlimit(5000)


# Path al archivo YALex

path = "./Yalex/ejemplo.txt"

YALEX = Yalex(path)

automatas = []

prioridad = 1
# Crear un atomata por cada token
for token in YALEX.tokens:
    expresion = YALEX.tokens[token]

    postfix = Postfix(expresion)
    postfix.toPostfix()
    expresion = postfix.final

    thompson = Thompson(expresion)
    nodos = thompson.visitados

    for n in nodos:
        if n.final:
            n.prioridad = prioridad
            n.valor_diccionario = token
            n.final_yalex = True
            

        n.inicial = False
        n.final = False

    prioridad += 1

    automatas.append(nodos)

# Crear un automata con todos los automatas del arreglo

# Crear un nodo inicial
inicial = Nodo('i', True, False, {})

# Crear un nodo final
final = Nodo('f', False, True, {})

for automata in automatas:
    # Crear una transicion del nodo inicial al primer nodo del automata
    inicial.addTransition(automata[0], "ε")

    # Buscar el elemento sin transicion del automata
    for nodo in automata:
        if nodo.transicion == {}:
            # Crear una transicion del nodo sin transicion al nodo final
            nodo.addTransition(final, "ε")
            break

    # # Crear una transicion del ultimo nodo del automata al nodo final
    # automata[-1].addTransition(final, "ε")


# crear un arreglo con todos los nodos

nodos = [inicial]
for automata in automatas:
    nodos += automata
nodos.append(final)

nodos = order_nodos(nodos[0])

with open('./pickle/nodos.pickle', 'wb') as f:
    pickle.dump(nodos, f)


with open('./pickle/YALEX.pickle', 'wb') as f:
    pickle.dump(YALEX, f)

simulacion = Simulacion(nodos)
with open('./pickle/simulacion.pickle', 'wb') as f:
    pickle.dump(simulacion, f)

# imprimir el grafo
# grafo = Grafo(nodos)


# escribir un script de python que utilice las reglas del yalex y simule el automata con un input

# new_script = """

# import pickle
# import re

# # Cargar el archivo con el arreglo nodos
# nodos = None
# with open('./pickle/nodos.pickle', 'rb') as f:
#     nodos = pickle.load(f)

# YALEX = None
# with open('./pickle/YALEX.pickle', 'rb') as f:
#     YALEX = pickle.load(f)

# simulacion = None
# with open('./pickle/simulacion.pickle', 'rb') as f:
#     simulacion = pickle.load(f)

# rules = YALEX.rules
# tokens = YALEX.tokens


# # Hacer la simulacion de el automata con cada cadena de entrada

# with open('./Yalex/Entrada 2.txt', 'r') as file:
#     output = []
#     count_lineas = 0
#     for line in file:
#         if line == '\\n':
#             continue
            
#         count_lineas += 1
#         line = re.sub(r'\s+', ' ', line)

#         words = line.split(' ')
#         if words[0] == '/*':
#             break
#         else:
#             count_word = 0

#             for word in words:
#                 if word == '':
#                     continue
                    
#                 count_word += 1
#                 # se hace la simulacion 
#                 result, aceptado = simulacion.simulacionAFN_YALEX(word)
#                 val = ""
#                 if not result and not aceptado:
#                     # buscar en el diccionario de reglas
#                     for key, value in rules.items():
#                         if key == word:
#                             val = value
#                             break

#                 if aceptado:
#                     output.append(aceptado[len(aceptado)-1])
#                 elif val != "":
#                     output.append(val)
#                 else:
#                     output.append("Error léxico en la línea " + str(count_lineas) + ", posicion " + str(count_word) + ": token no reconocido")
    
#     # escribir archivo con todos los elementos de output
#     with open('./Yalex/Output.txt', 'w', encoding='utf-8') as file:
#         for i in output:
#             file.write(i + "\\n")

# """

# # escribir el script en un archivo
# with open('./prueba.py', 'w', encoding='utf-8') as file:
#     file.write(new_script)






    


