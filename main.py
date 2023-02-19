from postfix import Postfix
from thomson import Thomson
from ass import Arbol

expresion = "0?(1?)?0?"
#expresion = "(a|b)*abb"

# arbol = Arbol(expresion)


postfix = Postfix(expresion)
expresion = postfix.final
print(expresion)
# thomson = Thomson(expresion)
#thomson.get_transiciones()

