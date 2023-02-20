from collections import deque
from grafo import *

class Thomson(object):
    def __init__(self, postfix):
        self.postfix = postfix
        self.conteo_nodos = 0
        self.nodos = []
        self.thomson(([*postfix]))
        self.visitados = self.order_nodos(self.inicial)

    def order_nodos(self, first_node):
        first_node.inicial = True
        visitados = {first_node}
        queue = deque([first_node])
        nodos_ordenados = []

        while queue:
            nodo = queue.popleft()
            nodos_ordenados.append(nodo)

            for s_nodo, valor in nodo.transicion.items():
                if s_nodo not in visitados:
                    visitados.add(s_nodo)
                    queue.append(s_nodo)

        nodos_ordenados[len(nodos_ordenados)-1].final = True
        return nodos_ordenados

    
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

            
            if isinstance(nodo1, str):
                nodo1 = self.simple(nodo1)
            
            if isinstance(nodo2, str):
                nodo2 = self.simple(nodo2)

            
            if len(stack) <= 0:
                self.inicial = nodo2[0]
        
            
            if primero == "|":
                nodo1i = nodo1[0]
                nodo1f = nodo1[1]

                nodo2i = nodo2[0]
                nodo2f = nodo2[1]
                
                return self.orS(nodo2i, nodo2f, nodo1i, nodo1f)
            
            elif primero == ".":
                nodo1i = nodo1[0]
                nodo1f = nodo1[1]

                nodo2i = nodo2[0]
                nodo2f = nodo2[1]
                return self.concat(nodo1i, nodo1f, nodo2i, nodo2f)
        
        elif primero in unarios:
            nodo1 = stack.pop()

            if nodo1 in operadores:
                stack.append(nodo1)
                nodo1 = self.thomson(stack)

            if isinstance(nodo1, str):
                nodo1 = self.simple(nodo1)

            if len(stack) <= 0:
                self.inicial = nodo1[0]

            if primero == "*":
                nodo1i = nodo1[0]
                nodo1f = nodo1[1]
                print(nodo1i)
                print(nodo1f)
                return self.kleene(nodo1i, nodo1f)

            elif primero == "+":
                nodo1i = nodo1[0]
                nodo1f = nodo1[1]
                return self.positiva(nodo1i, nodo1f)
            
    def concat(self, nodo1i, nodo1f, nodo2i, nodo2f):
        inicio = nodo2f
        self.conteo_nodos += 1
        final = nodo1i
        self.conteo_nodos += 1
        inicio.addTransition(final, "ε")

        return [nodo2i, nodo1f]

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
        self.nodos.append(final)
        return [inicio, final]
    
    def orS(self, nodo1i, nodo1f, nodo2i, nodo2f):
        inicio = Nodo(self.conteo_nodos, False, False, {})
        self.conteo_nodos += 1
        n1 = nodo1i
        self.conteo_nodos += 1
        n2 = nodo1f
        self.conteo_nodos += 1
        n3 = nodo2i
        self.conteo_nodos += 1
        n4 = nodo2f
        self.conteo_nodos += 1
        final = Nodo(self.conteo_nodos, False, False, {})
        self.conteo_nodos += 1

        inicio.addTransition(n1, "ε")
        inicio.addTransition(n3, "ε")
        n2.addTransition(final, "ε")
        n4.addTransition(final, "ε")

        self.nodos.append(inicio)
        self.nodos.append(final)

        return [inicio, final]
    
    def positiva(self, nodo1i, nodo1f):
        inicio = Nodo(self.conteo_nodos, False, False, {})
        self.conteo_nodos += 1
        n1 = nodo1i
        self.conteo_nodos += 1
        n2 = nodo1f
        self.conteo_nodos += 1
        final = Nodo(self.conteo_nodos, False, False, {})
        self.conteo_nodos += 1

        inicio.addTransition(n1, "ε")
        n2.addTransition(n1, "ε")
        n2.addTransition(final, "ε")

        self.nodos.append(inicio)
        self.nodos.append(final)
        return [inicio, final]

    def simple(self, valor):
        inicio = Nodo(self.conteo_nodos, False, False, {})
        self.conteo_nodos += 1
        final = Nodo(self.conteo_nodos, False, False, {})
        self.conteo_nodos += 1
        inicio.addTransition(final, valor)

        self.nodos.append(inicio)
        self.nodos.append(final)
        return [inicio, final]
    
        


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

    def __str__(self):
        return str(self.conteo)