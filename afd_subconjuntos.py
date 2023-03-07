from collections import deque
from thompson import *

def is_operand(char):
    return True if char.isalpha() else char.isnumeric()

class Subconjuntos(object):
    def __init__(self, thompson):
        self.thompson = thompson
        self.nodos = thompson.visitados
        self.alfabeto = self.getAlfabeto()
        self.transiciones, self.subconjuntos = self.subconjuntos()
        self.nuevos_nodos = self.crear_automata()
        self.afd = self.order_nodos(self.nuevos_nodos[0])

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
    
    def crear_automata(self):
        subconjuntos = self.subconjuntos
        transiciones = self.transiciones
        nodos = []

        for subconjunto in subconjuntos:
            nombre_conjunto = ""
            for nodo in subconjunto:
                nombre_conjunto += str(nodo.conteo) + ","

            nodo = Nodo(nombre_conjunto)
            for nodo_subconjunto in subconjunto:
                if nodo_subconjunto.final:
                    nodo.final = True

                if subconjunto == subconjuntos[0]:
                    nodo.inicial = True
            nodos.append(nodo)
        
        for transicion in transiciones:
            for simbolo in transiciones[transicion]:
                actual = None
                for nodo in nodos:
                    if nodo.conteo == transicion:
                        actual = nodo
                for nodo in nodos:
                    if nodo.conteo == transiciones[transicion][simbolo]:
                        print(transicion)
                        print(simbolo)
                        actual.addTransition(nodo, simbolo)

        return nodos



    def getAlfabeto(self):
        alfabeto = []
        for char in self.thompson.postfix:
            if is_operand(char) and char not in alfabeto and char!='ε':
                alfabeto.append(char)
        return alfabeto

    def e_closure(self, nodo):
        nodos = [nodo]
        queue = deque([nodo])
        while queue:
            nodo = queue.popleft()
            for s_nodo, valor in nodo.transicion.items():
                if s_nodo not in nodos and valor == ['ε']:
                    nodos.append(s_nodo)
                    queue.append(s_nodo)
        return nodos

    def move(self, nodo, simbolo):
        nodos = []
        for s_nodo, valor in nodo.transicion.items():
            simbolo = [simbolo]
            if valor == simbolo:
                nodos.append(s_nodo)

        return nodos
    
    def sort_nodos(self, nodos):
        nodos_ordenados = []
        for nodo in nodos:
            nodos_ordenados.append(nodo.conteo)
        nodos_ordenados.sort()

        for i in range(len(nodos_ordenados)):
            for nodo in nodos:
                if nodos_ordenados[i] == nodo.conteo:
                    nodos_ordenados[i] = nodo
        return nodos_ordenados

    def subconjuntos(self):
        conjunto_inicial = [*self.e_closure(self.thompson.visitados[0])]
        subconjuntos = [conjunto_inicial]
        transiciones = {}

        queue = deque([conjunto_inicial])
        while queue:
            conjunto = queue.popleft()

            for simbolo in self.alfabeto:
                conjunto_move = []
                for nodo in conjunto:
                    conjunto_move.extend([*self.move(nodo, simbolo)])
                
                conjunto_temp = []
                for nodo in conjunto_move:
                    new = [*self.e_closure(nodo)]
                    for n in new:
                        if n not in conjunto_temp:
                            conjunto_temp.append(n)
                    # conjunto_temp.extend([*self.e_closure(nodo)])

                conjunto_temp = self.sort_nodos(conjunto_temp)

                if conjunto_temp not in subconjuntos and conjunto_temp != []:
                    subconjuntos.append(conjunto_temp)
                    queue.append(conjunto_temp)


                if conjunto != []:
                    nombre_conjunto = ""
                    for nodo in conjunto:
                        nombre_conjunto += str(nodo.conteo) + ","

                    if nombre_conjunto not in transiciones:
                        transiciones[nombre_conjunto] = {}

                    if simbolo not in transiciones[nombre_conjunto]:
                        transiciones[nombre_conjunto][simbolo] = {}

                    nombre_conjunto_temp = ""
                    for nodo in conjunto_temp:
                        nombre_conjunto_temp += str(nodo.conteo) + ","

                    transiciones[nombre_conjunto][simbolo] = nombre_conjunto_temp
        return transiciones, subconjuntos

