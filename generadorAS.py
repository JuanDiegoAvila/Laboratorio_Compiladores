import pickle
import sys
from Yapar.yapar import *
from Yalex.yalex import *
sys.setrecursionlimit(5000)

path_yalex = "./Yapar/yal1.txt"
path_yapar = "./Yapar/slr-1.txt"

YALEX = Yalex(path_yalex)
YAPAR = Yapar(path_yapar)

YAPAR.checkErrors(YALEX.rules)

nodos = YAPAR.nodos

with open('./Yapar/pickle/nodos.pickle', 'wb') as f:
    pickle.dump(nodos, f)

with open('./Yapar/pickle/YALEX.pickle', 'wb') as f:
    pickle.dump(YALEX, f)

with open('./Yapar/pickle/YAPAR.pickle', 'wb') as f:
    pickle.dump(YAPAR, f)



new_script = """

import pickle
from comunicador import Comunicador
import AL as AL

# Cargar el archivo con el arreglo nodos
nodos = None
with open('./Yapar/pickle/nodos.pickle', 'rb') as f:
    nodos = pickle.load(f)

YALEX = None
with open('./Yapar/pickle/YALEX.pickle', 'rb') as f:
    YALEX = pickle.load(f)

YAPAR = None
with open('./Yapar/pickle/YAPAR.pickle', 'rb') as f:
    YAPAR = pickle.load(f)

comunicador = None
with open('./pickle/comunicador.pickle', 'rb') as f:
    comunicador = pickle.load(f)

ANALIZADOR_LEXICO = AL.AL()

W = []
PILA = [0]
a = ANALIZADOR_LEXICO.getNext()

ACCION = YAPAR.tabla_analisis['accion']
IR_A = YAPAR.tabla_analisis['ir_A']

contador = 0


while True:
    S = str(PILA[-1])
    # a = W[0]
    # a = ANALIZADOR_LEXICO.getNext()

    if a in ACCION[S]:

        # ver si empieza con s o r

        if ACCION[S][a][0] == 's':
            accion = ACCION[S][a].split('s')[1]
            PILA.append(int(accion))
            # W = W[1:]
            a = ANALIZADOR_LEXICO.getNext()
            while(a in YAPAR.ignored):
                a = ANALIZADOR_LEXICO.getNext()

        elif ACCION[S][a][0] == 'r':

            # sacar el numero de la regla y el lado derecho de la regla
            regla = ACCION[S][a].split('r')[1]
            regla = int(regla)
            lado_izquierdo = YAPAR.gramaticaList[regla].split(' -> ')[0]
            lado_derecho = YAPAR.gramaticaList[regla].split(' -> ')[1].split(' ')

            # eliminar elementos vacios de la lista
            lado_derecho = list(filter(lambda a: a != '', lado_derecho))
            lado_izquierdos = list(filter(lambda a: a != '', lado_izquierdo))

            # sacar el numero de elementos que hay que sacar de la pila
            num_elementos = len(lado_derecho)

            # sacar los elementos de la pila
            for i in range(num_elementos):
                PILA.pop()

            # sacar el estado de la pila
            S = str(PILA[-1])

            # peter IR_A[t, A] en la pila
            nuevo = IR_A[S][lado_izquierdo]
            PILA.append(int(nuevo))

            # # agregar el lado izquierdo a la salida
            # print(lado_izquierdo)

        elif ACCION[S][a] == 'aceptar':
            print('aceptado')
            break

    else:
        print('Error sintactico en la entrada')
        break


"""

new_script = new_script.format()

# escribir el script en un archivo
with open('./AS.py', 'w', encoding='utf-8') as file:
    file.write(new_script)
