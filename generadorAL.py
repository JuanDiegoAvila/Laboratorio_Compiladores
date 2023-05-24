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

        # Cargar el archivo con el arreglo nodos
        self.nodos = None
        with open('./Yalex/pickle/nodos.pickle', 'rb') as f:
            self.nodos = pickle.load(f)

        self.YALEX = None
        with open('./Yalex/pickle/YALEX.pickle', 'rb') as f:
            self.YALEX = pickle.load(f)

        self.simulacion = None
        with open('./Yalex/pickle/simulacion.pickle', 'rb') as f:
            self.simulacion = pickle.load(f)

        self.rules = self.YALEX.rules
        self.tokens =  self.YALEX.tokens
        self.token_keys = self.tokens.keys()
        self.suma_puntero = 0

        

    def getNext(self):
        self.next = True
        self.analizador_lexico()

        if 'Error' in self.output[0]:
            print(self.output[0])
            exit()

        temp = self.output[0].replace(' ', '')
        
        return temp
        


    def analizador_lexico(self):

        # Hacer la simulacion de el automata con cada cadena de entrada

        with open('{entrada}') as file:
            
            for line in file:
                line = line
                puntero = self.simulacion.getPuntero()
                # puntero = puntero -1 if puntero > 0 else puntero
                
                
                self.suma_puntero += puntero

                # agarrar la linea a partir del puntero 
                linea = line[self.suma_puntero:]

                self.simulacion.setEntrada(linea,  self.tokens.keys(),  self.rules)

                token, termino =  self.simulacion.simulacionAFN_YALEX_PUNTERO()
                
                if token != None:
                    self.output = token
                
                if termino:
                    self.output = ['$']
    

{trailer}
"""

new_script = new_script.format(header=header, trailer=trailer, entrada=entrada)

# escribir el script en un archivo
with open('./AL.py', 'w', encoding='utf-8') as file:
    file.write(new_script)






    


