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


# Hacer la simulacion de el automata con cada cadena de entrada

with open('./Yalex/Entrada 1.txt', 'r') as file:
    output = []
    count_lineas = 0
    expresion = ''
    
    for line in file:
        count_lineas += 1
        expresion += line+'\n '
        
    
    # se simula la expresion completa
    result, aceptado = simulacion.simulacionAFN_YALEX(expresion, rules)

    output = []
    for a in aceptado:
        existe = False
        for key, value in rules.items():
            if a == key:
                existe = True
                if value != '':
                    output.append(value)
        
        if not existe:
            string = 'Error: ' + repr(a) + ' es un token que no existe'
            output.append(string)
    print(output)
    # escribir archivo con todos los elementos de output
    with open('./Yalex/Output.txt', 'w', encoding='utf-8') as file:
        for i in output:
            file.write(i + "\n")

    #     line = re.sub(r'\s+', ' ', line)

    #     words = line.split(' ')
    #     if words[0] == '/*':
    #         break
    #     else:
    #         count_word = 0

    #         for word in words:
    #             if word == '':
    #                 continue
                    
    #             count_word += 1
    #             # se hace la simulacion 
    #             result, aceptado = simulacion.simulacionAFN_YALEX(word)
    #             val = ""
    #             if not result and not aceptado:
    #                 # buscar en el diccionario de reglas
    #                 for key, value in rules.items():
    #                     if key == word:
    #                         val = value
    #                         break

    #             if aceptado:
    #                 output.append(aceptado[len(aceptado)-1])
    #             elif val != "":
    #                 output.append(val)
    #             else:
    #                 output.append("Error léxico en la línea " + str(count_lineas) + ", posicion " + str(count_word) + ": token no reconocido")
    
    # # escribir archivo con todos los elementos de output
    # with open('./Yalex/Output.txt', 'w', encoding='utf-8') as file:
    #     for i in output:
    #         file.write(i + "\n")

