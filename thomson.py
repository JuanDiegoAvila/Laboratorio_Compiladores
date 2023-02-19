class Thomson(object):
    def __init__(self, postfix):
        self.postfix = postfix
        self.conteo_nodos = 0
        self.nodos = []
        self.afn = self.thomson(([*postfix]))
    
    def thomson(self, stack):
        binarios = '|.'
        unarios = '*+'
        operadores = '|.*+'

        primero = stack.pop()

        if primero in binarios:
            nodo1 = stack.pop()

            if nodo1 in operadores:
                stack.append(nodo1)
                nodo1 = self.thomson(stack)
            
            nodo2 = stack.pop()

            if nodo2 in operadores:
                stack.append(nodo2)
                nodo2 = self.thomson(stack)
            
            #if isinstance(nodo1, str):
            nodo1i, nodo1f = self.simple(nodo1)
            
            #if isinstance(nodo2, str):
            nodo2i, nodo2f = self.simple(nodo2)
            
            if primero == "*":
                return self.kleene(nodo1i, nodo1f)

            elif primero == "+":
                return self.positiva(nodo2i, nodo2f)
            
            elif primero == "|":
                return self.orS(nodo1i, nodo1f, nodo2i, nodo2f)
            
            elif primero == ".":
                return self.concat(nodo1i, nodo1f, nodo2i, nodo2f)
        
        elif primero in unarios:
            nodo1 = stack.pop()

            if nodo1 in operadores:
                stack.append(nodo1)
                nodo1 = self.thomson(stack)

            nodo1i, nodo1f = self.simple(nodo1)
            
            if isinstance(nodo1, str):
                nodo1 = self.simple(nodo1)
            
            if primero == "*":
                return self.kleene(nodo1i, nodo1f)

            elif primero == "+":
                return self.positiva(nodo1i, nodo1f)
            
    
    def concat(self):
        return None

    def kleene(self, nodo1i, nodo1f):
        inicio = Nodo(self.conteo_nodos, False, False, {})
        self.conteo_nodos += 1
        n1 = nodo1i
        self.conteo_nodos += 1
        n2 = nodo1f
        self.conteo_nodos += 1
        final = Nodo(self.conteo_nodos, False, False, {})
        self.conteo_nodos += 1

        inicio.addTransition(final, "ε")
        inicio.addTransition(n1, "ε")
        n2.addTransition(n1, "ε")
        n2.addTransition(final, "ε")

        self.nodos.append(inicio)
        self.nodos.append(n1)
        self.nodos.append(n2)
        self.nodos.append(final)
        return inicio, final
    
    def orS(self, nodo):

        return None
    
    def positiva(self, nodo):
        return None

    def simple(self, valor):
        inicio = Nodo(self.conteo_nodos, False, False, {})
        self.conteo_nodos += 1
        final = Nodo(self.conteo_nodos, False, False, {})
        self.conteo_nodos += 1
        inicio.addTransition(final, valor)

        self.nodos.append(inicio)
        self.nodos.append(final)
        return inicio, final
        


class Nodo(object):
    def __init__(self, conteo, inicial = False, final = False, transicion = {}):
        self.conteo = conteo
        self.final = final
        self.inicial = inicial
        self.transicion = transicion
    
    def addTransition(self, nodo, valor):
        if nodo in self.transicion.keys() :
            self.transicion[nodo].append(valor)
        else:
            self.transicion[nodo] = [valor]

    def get_transition(self, nodo):
        return self.transicion[nodo]
        
        