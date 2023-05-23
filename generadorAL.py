import sys
from Yalex.yalex import *
from Automatas.postfix import *
from Automatas.thompson import * 
from Automatas.simulacion import Simulacion
import pickle
sys.setrecursionlimit(5000)

# Path al archivo YALex
path = "./Yapar/yal1.txt"
entrada = "./Yapar/entrada1.txt"

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

# crear un arreglo con todos los nodos

nodos = [inicial]
for automata in automatas:
    nodos += automata
nodos.append(final)

nodos = order_nodos(nodos[0])

with open('./Yalex/pickle/nodos.pickle', 'wb') as f:
    pickle.dump(nodos, f)


with open('./Yalex/pickle/YALEX.pickle', 'wb') as f:
    pickle.dump(YALEX, f)

simulacion = Simulacion(nodos)
with open('./Yalex/pickle/simulacion.pickle', 'wb') as f:
    pickle.dump(simulacion, f)

header = YALEX.header if YALEX.header is not None else None
trailer = YALEX.trailer if YALEX.trailer is not None else None

# escribir un script de python que utilice las reglas del yalex y simule el automata con un input

new_script = """
import pickle
from comunicador import Comunicador

{header}

class AL(object):
    def __init__(self):
        self.output = []
        self.actual = 0
        self.next = False
        

    def getNext(self):
    
        self.analizador_lexico()
        self.next = True
        self.actual += 1

        while(self.output == []):
            self.analizador_lexico()
            self.actual += 1

        temp = self.output[0].replace(' ', '')
        return temp
        


    def analizador_lexico(self):

        # Cargar el archivo con el arreglo nodos
        nodos = None
        with open('./Yalex/pickle/nodos.pickle', 'rb') as f:
            nodos = pickle.load(f)

        YALEX = None
        with open('./Yalex/pickle/YALEX.pickle', 'rb') as f:
            YALEX = pickle.load(f)

        simulacion = None
        with open('./Yalex/pickle/simulacion.pickle', 'rb') as f:
            simulacion = pickle.load(f)


        rules = YALEX.rules
        tokens = YALEX.tokens

        token_keys = tokens.keys()


        # Hacer la simulacion de el automata con cada cadena de entrada

        with open('{entrada}', 'r') as file:
            output = []
            count_lineas = 0
            expresion = ''
            
            for line in file:
                count_lineas += 1
                line = line + ' '
            
                # se simula la expresion completa
                result, aceptado, texto_reconocido = simulacion.simulacionAFN_YALEX(line)
                
                indice = 0
                # for a in aceptado:
                if self.actual >= len(aceptado):
                    self.output = ['$']
                    return

                a = aceptado[self.actual]

                for token in a:
                    existe = False

                    for key, value in rules.items():
                        if texto_reconocido[indice] == key:
                            if value != '':
                                output.append(value)
                                existe = True

                            break

                        if token == key and not existe:
                            if value != '':
                                output.append(value)
                                existe = True

                            break
                            
                
                    if not existe and token not in token_keys and token != '':
                        posicion = 0
                        for i in range(indice):
                            posicion += len(texto_reconocido[i])

                        string = 'Error lexico en la linea '+ str(count_lineas) +' en la posicion ' + str(posicion)+': ' + repr(token) + ' no es un token valido'
                        output.append(string)
                        print(string)
                        
                indice += 1
            
            self.output = output

            # escribir archivo con todos los elementos de output
            with open('./Yalex/Output.txt', 'w', encoding='utf-8') as file:
                for i in output:
                    file.write(i + "\\n")

    

{trailer}
"""

new_script = new_script.format(header=header, trailer=trailer, entrada=entrada)

# escribir el script en un archivo
with open('./AL.py', 'w', encoding='utf-8') as file:
    file.write(new_script)






    


