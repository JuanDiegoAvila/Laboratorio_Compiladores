import sys
from Yalex.yalex import *
from Automatas.postfix import *
from Automatas.thompson import * 
from Automatas.simulacion import Simulacion
import pickle
sys.setrecursionlimit(5000)

# Path al archivo YALex
path = "./Yapar/yal2.txt"
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
        self.error = False
        self.actual = 0
        self.next = False
        self.aceptar = False
        self.cantidad_lineas = self.cantidadLineas()
        self.linea_actual = 1

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

    def cantidadLineas(self):
        cantidad_lineas = 0
        with open('{entrada}') as file:
            for line in file:
                cantidad_lineas += 1
        return cantidad_lineas


    def getNext(self):
        self.next = True
        self.analizador_lexico()

        if 'Error' in self.output[0]:
            print(self.output[0])
            self.output = []
            self.error = True
            self.analizador_lexico()

        if self.output[0] == 'cambio de linea':
            self.output = []
            self.analizador_lexico()

        temp = self.output[0].replace(' ', '')
        print(temp)
        return temp
        

    def analizador_lexico(self):

        # Hacer la simulacion de el automata con cada cadena de entrada
        cantidad_lineas = 1
        termino = False


        with open('{entrada}') as file:
            
            for line in file:
            
                if self.simulacion.linea == cantidad_lineas:
                    line = line.replace('\\n', ' \\n')
                    puntero = self.simulacion.getPuntero()
                
                    self.suma_puntero += puntero

                    # agarrar la linea a partir del puntero 
                    linea = line[self.suma_puntero:]


                    if linea == ' \\n':
                        self.linea_actual += 1
                        self.simulacion.linea += 1
                        self.output = ['cambio de linea']
                        self.suma_puntero = 0
                        self.simulacion.setPuntero(0)

                        if self.linea_actual > self.cantidad_lineas:
                            self.output = ['$']

                        return
                        

                    self.simulacion.setEntrada(linea, self.tokens.keys(), self.rules)

                    token, termino = self.simulacion.simulacionAFN_YALEX_PUNTERO()
                    
                    if token != None:
                        self.output = token
                
                cantidad_lineas += 1
    

{trailer}
"""

new_script = new_script.format(header=header, trailer=trailer, entrada=entrada)

# escribir el script en un archivo
with open('./AL.py', 'w', encoding='utf-8') as file:
    file.write(new_script)






    


