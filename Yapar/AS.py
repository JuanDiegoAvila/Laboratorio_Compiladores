
import pickle

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

