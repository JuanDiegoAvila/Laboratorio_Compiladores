from Yalex.yalex import * 
from Automatas.postfix import *
from Automatas.thompson import * 


# Path al archivo YALex

path = "./Yalex/ejemplo3.txt"

YALEX = Yalex(path)

automatas = []
# Crear un atomata por cada token
for token in YALEX.tokens:
    expresion = YALEX.tokens[token]

    postfix = Postfix(expresion)
    postfix.toPostfix()
    expresion = postfix.final

    thompson = Thompson(expresion)
    nodos = thompson.visitados

    for n in nodos:
        n.inicial = False
        n.final = False
    
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

# crear el grafo

grafo = Grafo(nodos)





    


