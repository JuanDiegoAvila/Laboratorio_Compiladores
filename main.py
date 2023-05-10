from Yalex.yalex import * 
from Yapar.yapar import *
from Automatas.postfix import *
from Automatas.thompson import * 
import sys
sys.setrecursionlimit(5000)

# Se lee el yalex y se crea el yapar
# path_yalex = "./Yapar/yal1.txt"
path_yapar = "./Yapar/slr-6.txt"

# YALEX = Yalex(path_yalex)
YAPAR = Yapar(path_yapar)

# YAPAR.checkErrors(YALEX.rules)
YAPAR.getPS()
# YAPAR.siguiente('E')




