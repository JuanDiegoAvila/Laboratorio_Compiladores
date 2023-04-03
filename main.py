from Yalex.yalex import * 
from Automatas.postfix import *
from Automatas.thompson import * 

# Path al archivo YALex

path = "./Yalex/ejemplo.txt"

YALEX = Yalex(path)

# Crear un atomata por cada token
for token in YALEX.tokens:
    expresion = YALEX.tokens[token]
    print(expresion)

    postfix = Postfix(expresion)
    postfix.toPostfix()
    expresion = postfix.final

    print(expresion)

    thompson = Thompson(expresion)
    nodos = thompson.visitados

    # crear el grafo
    grafo = Grafo(nodos, nombre = token)


