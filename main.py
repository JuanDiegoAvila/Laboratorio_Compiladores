from postfix import Postfix
from thomson import Thomson
from grafo import *
from ass import Arbol

#expresion = "0?(1?)?0?"
# expresion = "ab"
expresion = "(a|b)*abb"
# expresion = "abb"
expresion = "a|b"
expresion = "0?(1?)?0*"

# arbol = Arbol(expresion)


postfix = Postfix(expresion)
expresion = postfix.final
print(expresion)
thomson = Thomson(expresion)
nodos = thomson.visitados
#print(nodos)
grafo = Grafo(nodos)

