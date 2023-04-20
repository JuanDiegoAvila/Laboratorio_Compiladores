import pickle
import re

# Cargar el archivo con el arreglo nodos
nodos = None
with open('./pickle/nodos.pickle', 'rb') as f:
    nodos = pickle.load(f)

YALEX = None
with open('./pickle/YALEX.pickle', 'rb') as f:
    YALEX = pickle.load(f)

simulacion = None
with open('./pickle/simulacion.pickle', 'rb') as f:
    simulacion = pickle.load(f)

rules = YALEX.rules
tokens = YALEX.tokens

token_keys = tokens.keys()


# Hacer la simulacion de el automata con cada cadena de entrada

with open('./Yalex/Entrada 4.txt', 'r') as file:
    output = []
    count_lineas = 0
    expresion = ''
    
    for line in file:
        count_lineas += 1
        expresion += line+'\n '
        
    
    # se simula la expresion completa
    result, aceptado, texto_reconocido = simulacion.simulacionAFN_YALEX(expresion)

    output = []
    indice = 0
    for a in aceptado:

        for token in a:
            existe = False
            for key, value in rules.items():
                if texto_reconocido[indice] == key:
                    if value != '':
                        output.append(value)
                    existe = True
                    break

                if token == key:
                    existe = True
                    if value != '':
                        output.append(value)
        
            if not existe and token not in token_keys:
                string = 'Error: ' + repr(token) + ' es un token que no existe'
                output.append(string)
        indice += 1

    # escribir archivo con todos los elementos de output
    with open('./Yalex/Output.txt', 'w', encoding='utf-8') as file:
        for i in output:
            file.write(i + "\n")
