from collections import deque

class Simulacion(object):
    def __init__(self, nodos, alfabeto, expresion):
        self.expresion = expresion
        self.nodos = nodos
        self.alfabeto = alfabeto
        self.aceptado = self.simulacion()
        print(self.aceptado)

    def simulacion(self):
        expresion = [caracter for caracter in self.expresion]

        transiciones = []
        for simbolo in expresion:
            if simbolo not in self.alfabeto:
                print("La expresion no pertenece al alfabeto")
                return False
            
            transiciones.append(simbolo)

        inicio = self.nodos[0]
        final = self.nodos[-1]

        nodos = self.e_closure(inicio)

        for nodo in nodos:
            for s_nodo, valor in nodo.transicion.items():
                if valor == transiciones[0]:
                    nodos_visitados.append(s_nodo)
                    transiciones.pop(0)
                    if s_nodo.final:
                        print("Cadena aceptada")
                        return True
                    self.recorrer(s_nodo, transiciones, nodos_visitados)
                elif valor == ['ε']:
                    nodos = self.e_closure(nodo)
                    transicion = False
                    print(nodos)
                    for nodo in nodos:
                        transicion =  self.recorrer(nodo, transiciones, nodos_visitados)
                    
                    if transicion:
                        return True



        movimientos = ""
        nodos_visitados = []

    # def simulacion(self):
    #     expresion = [caracter for caracter in self.expresion]
    #     for simbolo in expresion:
    #         if simbolo not in self.alfabeto:
    #             print("La expresion no pertenece al alfabeto")
    #             return False
    #         else:
    #             return self.recorrer(self.nodos[0], simbolo)

    # def recorrer(self, nodo, simbolo):
    #     if nodo.transicion:
    #         for s_nodo, valor in nodo.transicion.items():
    #             simbolo = [simbolo]
    #             if valor == simbolo:
    #                 print("Estado actual: ", nodo.conteo, " Simbolo: ", simbolo, " Estado siguiente: ", s_nodo.conteo)
    #                 if s_nodo.final:
    #                     print("Cadena aceptada")
    #                     return True
    #                 self.recorrer(s_nodo, simbolo)
    #             elif valor == ['ε']:
    #                 nodos = self.e_closure(nodo)
    #                 transicion = False
    #                 print(nodos)
    #                 for nodo in nodos:
    #                     transicion =  self.recorrer(nodo, simbolo)
                    
    #                 if transicion:
    #                     return True
            
    #     else:
    #         return False
    

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
    
        
