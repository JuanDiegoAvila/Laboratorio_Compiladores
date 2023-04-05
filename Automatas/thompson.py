from collections import deque
from Automatas.grafo import *
from prettytable import PrettyTable

def order_nodos(first_node):
    conteo_nodos = 0
    first_node.conteo = conteo_nodos
    visitados = {first_node}
    queue = deque([first_node])
    nodos_ordenados = []

    while queue:
        conteo_nodos += 1
        nodo = queue.popleft()
        nodo.conteo = conteo_nodos
        nodos_ordenados.append(nodo)

        for s_nodo, valor in nodo.transicion.items():
            if s_nodo not in visitados:
                visitados.add(s_nodo)
                queue.append(s_nodo)
    return nodos_ordenados

class Thompson(object):
    def __init__(self, postfix):
        self.postfix = postfix
        self.conteo_nodos = 0
        self.nodos = []

        expresion_separada = self.deconstruct_expresion(postfix)
        self.inicio, self.final = self.thompson(expresion_separada)
        self.inicio.inicial = True
        self.final.final = True
        self.visitados = self.order_nodos(self.inicio)
        self.alfabeto = self.getAlfabeto()

    def deconstruct_expresion(self, expresion):
        temp_expresion = ([*expresion])
        stack = []
        es_comilla = False
        temp = []
    
        for i in range(len(temp_expresion)):
            if temp_expresion[i] == "'":
                es_comilla = not es_comilla
                temp.append(temp_expresion[i])

                if not es_comilla:
                    stack.append("".join(temp))
                    temp = []

            elif es_comilla:
                temp.append(temp_expresion[i])
            else:
                stack.append(temp_expresion[i])
        return stack


    def getAlfabeto(self):
        alfabeto = []
        for char in self.postfix:
            if self.is_operand(char) and char not in alfabeto and char!='ε':
                alfabeto.append(char)
        return alfabeto
    
    def is_operand(self, char):
        return True if char.isalpha() else char.isnumeric()

    def order_nodos(self, first_node):
        conteo_nodos = 0
        first_node.conteo = conteo_nodos
        visitados = {first_node}
        queue = deque([first_node])
        nodos_ordenados = []

        while queue:
            conteo_nodos += 1
            nodo = queue.popleft()
            nodo.conteo = conteo_nodos
            nodos_ordenados.append(nodo)

            for s_nodo, valor in nodo.transicion.items():
                if s_nodo not in visitados:
                    visitados.add(s_nodo)
                    queue.append(s_nodo)

        return nodos_ordenados

    
    def thompson(self, stack):
        binarios = '|.'
        unarios = '*+'
        operadores = '|.*+'

        primero = stack.pop()

        if primero in binarios:
            nodo1 = stack.pop()

            if nodo1 in operadores:
                stack.append(nodo1)
                nodo1 = self.thompson(stack)
            
            nodo2 = stack.pop()

            if nodo2 in operadores:
                stack.append(nodo2)
                nodo2 = self.thompson(stack)

            
            if isinstance(nodo1, str):
                nodo1 = self.simple(nodo1)
            
            if isinstance(nodo2, str):
                nodo2 = self.simple(nodo2)
            
            if primero == "|":
                nodo1i = nodo1[0]
                nodo1f = nodo1[1]

                nodo2i = nodo2[0]
                nodo2f = nodo2[1]
                
                return self.orS(nodo1i, nodo1f, nodo2i, nodo2f)
            
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
                nodo1 = self.thompson(stack)

            if isinstance(nodo1, str):
                nodo1 = self.simple(nodo1)

            if primero == "*":
                nodo1i = nodo1[0]
                nodo1f = nodo1[1]
                return self.kleene(nodo1i, nodo1f)

            elif primero == "+":
                nodo1i = nodo1[0]
                nodo1f = nodo1[1]
                return self.positiva(nodo1i, nodo1f)
        
        else:
            return self.simple(primero)
            
    def concat(self, nodo1i, nodo1f, nodo2i, nodo2f):
        inicio = nodo2f
        final = nodo1i

        inicio.addTransition(final, "ε")

        return [nodo2i, nodo1f]

    def kleene(self, nodo1i, nodo1f):
        inicio = Nodo(0, False, False, {})
        n1 = nodo1i
        n2 = nodo1f
        final = Nodo(0, False, False, {})

        inicio.addTransition(final, "ε")
        inicio.addTransition(n1, "ε")
        n2.addTransition(n1, "ε")
        n2.addTransition(final, "ε")

        self.nodos.append(inicio)
        self.nodos.append(final)
        return [inicio, final]
    
    def orS(self, nodo1i, nodo1f, nodo2i, nodo2f):
        inicio = Nodo(0, False, False, {})
        n1 = nodo2i
        n2 = nodo2f
        n3 = nodo1i
        n4 = nodo1f
        final = Nodo(0, False, False, {})

        inicio.addTransition(n1, "ε")
        inicio.addTransition(n3, "ε")
        n2.addTransition(final, "ε")
        n4.addTransition(final, "ε")

        self.nodos.append(inicio)
        self.nodos.append(final)

        return [inicio, final]
    
    def positiva(self, nodo1i, nodo1f):
        inicio = Nodo(0, False, False, {})
        n1 = nodo1i
        n2 = nodo1f
        final = Nodo(0, False, False, {})

        inicio.addTransition(n1, "ε")
        n2.addTransition(n1, "ε")
        n2.addTransition(final, "ε")

        self.nodos.append(inicio)
        self.nodos.append(final)
        return [inicio, final]

    def simple(self, valor):
        inicio = Nodo(0, False, False, {})
        final = Nodo(0, False, False, {})
        inicio.addTransition(final, valor)

        self.nodos.append(inicio)
        self.nodos.append(final)
        return [inicio, final]
    
        


class Nodo(object):
    def __init__(self, conteo, inicial = False, final = False, transicion = None):
        self.conteo = conteo
        self.final = final
        self.inicial = inicial
        self.transicion = transicion if transicion is not None else {}
    
    def addTransition(self, nodo, valor):
        
        if nodo in self.transicion.keys() :
            self.transicion[nodo].append(valor)
        else:
            self.transicion[nodo] = [valor]

    def get_transition(self, nodo):
        return self.transicion[nodo]
    
    def get_transition_valor(self, valor):
        for nodo in self.transicion.keys():
            if valor in self.transicion[nodo]:
                return nodo

    def print_transiciones(self):
        for nodo in self.transicion.keys():
            print(self.conteo, " -> ", nodo.conteo, " : ", self.transicion[nodo])
    
    def __repr__(self):
        transiciones = []
        for nodo in self.transicion.keys():
            transiciones.append(str(nodo.conteo)+" -> "+str(self.transicion[nodo]))
        index = ", ".join(transiciones)


        x = PrettyTable()
        x.field_names = ["Nodo", "Inicial", "Final", "Transiciones"]
        x.add_row([self.conteo, self.inicial, self.final, index])
        return '\n'+str(x)+'\n'

    def __str__(self):
        transiciones = []
        for nodo in self.transicion.keys():
            transiciones.append(str(nodo.conteo)+" -> "+str(self.transicion[nodo]))
        index = ", ".join(transiciones)


        x = PrettyTable()
        x.field_names = ["Nodo", "Inicial", "Final", "Transiciones"]
        x.add_row([self.conteo, self.inicial, self.final, index])
        return '\n'+str(x)+'\n'
    

