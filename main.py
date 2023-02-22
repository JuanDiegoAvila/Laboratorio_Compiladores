from postfix import Postfix
from thomson import Thomson
from grafo import *
from ass import Arbol

#expresion = "0?(1?)?0?"
# expresion = "ab"
expresion = "(a|b)*abb"
# expresion = "abb"
expresion = "a|b"
expresion = "a?b+"
expresion = "a**"
expresion = "0?(1?)?0*"
expresion = "a|x*a*|ε"
expresion = "(a|b)|(c|d)"
expresion = "(a|b) *|(c|d))*"


postfix = Postfix(expresion)
expresion = postfix.final
print(expresion)
thomson = Thomson(expresion)
nodos = thomson.visitados
grafo = Grafo(nodos)

