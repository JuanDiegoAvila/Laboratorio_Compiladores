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

with open('./pickle/nodos.pickle', 'wb') as f:
    pickle.dump(nodos, f)

with open('./pickle/YALEX.pickle', 'wb') as f:
    pickle.dump(YALEX, f)

with open('./pickle/YAPAR.pickle', 'wb') as f:
    pickle.dump(YAPAR, f)



