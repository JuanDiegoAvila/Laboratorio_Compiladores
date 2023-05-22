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




"""

new_script = new_script.format()

# escribir el script en un archivo
with open('./AS.py', 'w', encoding='utf-8') as file:
    file.write(new_script)
